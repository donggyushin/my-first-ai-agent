from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf

class StockTickerInput(BaseModel):
    """Input schema for stock analysis tools."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA, MSFT)")

class RealTimeValuationTool(BaseTool):
    name: str = "get_real_time_valuation"
    description: str = "Get real-time stock valuation metrics including PE, P/B, P/S ratios and current price data"
    args_schema: Type[BaseModel] = StockTickerInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Current stock data
            current_price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            market_cap = info.get("marketCap", "N/A")
            
            # Valuation metrics from Yahoo Finance
            pe_ratio = info.get("trailingPE", "N/A")
            pb_ratio = info.get("priceToBook", "N/A") 
            ps_ratio = info.get("priceToSalesTrailing12Months", "N/A")
            
            # Additional metrics
            eps = info.get("trailingEps", "N/A")
            book_value = info.get("bookValue", "N/A")
            revenue = info.get("totalRevenue", "N/A")
            
            # Company info
            company_name = info.get("longName", ticker)
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            
            # Valuation assessment
            valuation_assessment = "N/A"
            if isinstance(pe_ratio, (int, float)) and pe_ratio > 0:
                if pe_ratio < 15:
                    valuation_assessment = "잠재적 저평가 (낮은 PER)"
                elif pe_ratio > 30:
                    valuation_assessment = "잠재적 고평가 (높은 PER)"
                else:
                    valuation_assessment = "적정 가치"
            
            # Format market cap and revenue
            def format_number(num):
                if isinstance(num, (int, float)):
                    if num >= 1e12:
                        return f"${num/1e12:.2f}조"
                    elif num >= 1e9:
                        return f"${num/1e9:.2f}십억"
                    elif num >= 1e6:
                        return f"${num/1e6:.2f}백만"
                    else:
                        return f"${num:,.0f}"
                return num
            
            result = f"""
실시간 주식 밸류에이션 분석: {company_name} ({ticker})
=================================================
📊 기본 정보:
• 업종: {sector} - {industry}
• 현재가: ${current_price}
• 시가총액: {format_number(market_cap)}
• 연간 매출: {format_number(revenue)}

💰 밸류에이션 지표:
• PER (주가수익비율): {pe_ratio}
• PBR (주가순자산비율): {pb_ratio}  
• PSR (주가매출비율): {ps_ratio}
• EPS (주당순이익): ${eps}
• BPS (주당순자산): ${book_value}

📈 투자 평가: {valuation_assessment}

해석 가이드:
- PER < 15: 저평가 가능성
- PER 15-25: 적정 가치 범위
- PER > 25: 고평가 또는 고성장 기대
- PBR < 1: 주가가 순자산보다 낮음
- PBR > 3: 프리미엄 밸류에이션
"""
            return result
        except Exception as e:
            return f"❌ 주식 데이터 조회 실패 ({ticker}): {str(e)}\n※ 올바른 티커 심볼을 입력했는지 확인하세요."

class RealTimeFinancialHealthTool(BaseTool):
    name: str = "get_real_time_financial_health"
    description: str = "Get real-time financial health score based on actual company financial ratios and metrics"
    args_schema: Type[BaseModel] = StockTickerInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get financial ratios from Yahoo Finance
            debt_to_equity = info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else None
            current_ratio = info.get("currentRatio", None)
            roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None
            profit_margin = info.get("profitMargins", 0) * 100 if info.get("profitMargins") else None
            
            # Additional metrics
            quick_ratio = info.get("quickRatio", None)
            gross_margins = info.get("grossMargins", 0) * 100 if info.get("grossMargins") else None
            operating_margins = info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") else None
            
            score = 0
            max_score = 100
            analysis = []
            available_metrics = 0
            
            # Debt-to-Equity Analysis (25 points)
            if debt_to_equity is not None:
                available_metrics += 1
                if debt_to_equity < 0.3:
                    score += 25
                    analysis.append("✅ 우수한 부채 관리 (부채비율 < 30%)")
                elif debt_to_equity < 0.6:
                    score += 20
                    analysis.append("✅ 양호한 부채 관리 (부채비율 < 60%)")
                elif debt_to_equity < 1.0:
                    score += 15
                    analysis.append("⚠️ 보통 부채 수준 (부채비율 < 100%)")
                else:
                    score += 5
                    analysis.append("⚠️ 높은 부채 수준 (부채비율 ≥ 100%)")
            else:
                analysis.append("📊 부채비율 데이터 없음")
            
            # Current Ratio Analysis (25 points)
            if current_ratio is not None:
                available_metrics += 1
                if current_ratio > 2.0:
                    score += 25
                    analysis.append("✅ 강력한 유동성 (유동비율 > 2.0)")
                elif current_ratio > 1.5:
                    score += 20
                    analysis.append("✅ 양호한 유동성 (유동비율 > 1.5)")
                elif current_ratio > 1.0:
                    score += 15
                    analysis.append("⚠️ 적절한 유동성 (유동비율 > 1.0)")
                else:
                    score += 5
                    analysis.append("⚠️ 부족한 유동성 (유동비율 ≤ 1.0)")
            else:
                analysis.append("📊 유동비율 데이터 없음")
            
            # ROE Analysis (25 points) 
            if roe is not None:
                available_metrics += 1
                if roe > 20:
                    score += 25
                    analysis.append("✅ 우수한 수익성 (ROE > 20%)")
                elif roe > 15:
                    score += 20
                    analysis.append("✅ 양호한 수익성 (ROE > 15%)")
                elif roe > 10:
                    score += 15
                    analysis.append("⚠️ 보통 수익성 (ROE > 10%)")
                else:
                    score += 5
                    analysis.append("⚠️ 낮은 수익성 (ROE ≤ 10%)")
            else:
                analysis.append("📊 ROE 데이터 없음")
            
            # Profit Margin Analysis (25 points)
            if profit_margin is not None:
                available_metrics += 1
                if profit_margin > 20:
                    score += 25
                    analysis.append("✅ 우수한 순이익률 (>20%)")
                elif profit_margin > 10:
                    score += 20
                    analysis.append("✅ 양호한 순이익률 (>10%)")
                elif profit_margin > 5:
                    score += 15
                    analysis.append("⚠️ 보통 순이익률 (>5%)")
                else:
                    score += 5
                    analysis.append("⚠️ 낮은 순이익률 (≤5%)")
            else:
                analysis.append("📊 순이익률 데이터 없음")
            
            # Adjust score based on available metrics
            if available_metrics > 0:
                adjusted_score = int((score / available_metrics) * 4)  # Scale to 100
            else:
                adjusted_score = 0
                
            # Overall assessment
            if adjusted_score >= 85:
                overall = "우수 - 강력한 재무 건전성"
                risk_level = "낮음"
            elif adjusted_score >= 70:
                overall = "양호 - 견고한 재무 상태"
                risk_level = "보통"
            elif adjusted_score >= 55:
                overall = "보통 - 일부 우려 사항"
                risk_level = "보통-높음"
            else:
                overall = "주의 - 상당한 재무 리스크"
                risk_level = "높음"
            
            company_name = info.get("longName", ticker)
            
            result = f"""
실시간 재무 건전성 분석: {company_name} ({ticker})
==============================================
📊 종합 점수: {adjusted_score}/100 - {overall}
🎯 투자 위험도: {risk_level}

📈 상세 분석:
{chr(10).join(analysis)}

💡 추가 재무 지표:
• 당좌비율: {quick_ratio if quick_ratio else 'N/A'}
• 매출총이익률: {gross_margins:.2f}% if gross_margins else 'N/A'
• 영업이익률: {operating_margins:.2f}% if operating_margins else 'N/A'

🎯 투자 가이드라인:
• 85-100점: 보수적 투자자에게 적합 (저위험)
• 70-84점: 균형 포트폴리오에 적합 (중위험)  
• 55-69점: 적극적 투자자에게 적합 (고위험)
• 55점 미만: 위험 감수 투자자만 적합 (매우 고위험)

※ 데이터 출처: Yahoo Finance (실시간)
"""
            return result
        except Exception as e:
            return f"❌ 재무 데이터 조회 실패 ({ticker}): {str(e)}\n※ 올바른 티커 심볼을 입력했는지 확인하세요."

# Tool instances
get_real_time_valuation = RealTimeValuationTool()
get_real_time_financial_health = RealTimeFinancialHealthTool()