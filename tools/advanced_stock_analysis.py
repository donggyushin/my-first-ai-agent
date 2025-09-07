from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
import datetime
import numpy as np

class StockAnalysisInput(BaseModel):
    """Input schema for advanced stock analysis tool."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, BOIL, MSFT)")

class AdvancedStockAnalysisTool(BaseTool):
    name: str = "get_advanced_stock_analysis"
    description: str = "Get comprehensive stock analysis including technical indicators, financial metrics, and investment score"
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 현재 날짜 가져오기
            today = datetime.date.today().strftime("%Y-%m-%d")
            
            # 기본 정보
            current_price = info.get("regularMarketPrice") or info.get("currentPrice") or "N/A"
            company_name = info.get("longName", ticker)
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            market_cap = info.get("marketCap", "N/A")
            
            # 과거 가격 데이터 가져오기 (기술적 분석용)
            hist = stock.history(period="6mo")  # 6개월 데이터
            
            if hist.empty:
                return f"❌ {ticker}의 과거 데이터를 가져올 수 없습니다."
            
            # 기술적 지표 계산
            current_close = hist['Close'].iloc[-1]
            sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else None
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
            
            # RSI 계산
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1] if not rsi.empty else None
            
            # 변동성 계산 (30일)
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.rolling(window=30).std().iloc[-1] * np.sqrt(252) * 100 if len(returns) >= 30 else None
            
            # 거래량 분석
            avg_volume = hist['Volume'].rolling(window=20).mean().iloc[-1] if len(hist) >= 20 else None
            current_volume = hist['Volume'].iloc[-1]
            
            # 재무 지표
            pe_ratio = info.get("trailingPE")
            pb_ratio = info.get("priceToBook")
            debt_to_equity = info.get("debtToEquity")
            if debt_to_equity:
                debt_to_equity = debt_to_equity / 100
            roe = info.get("returnOnEquity")
            if roe:
                roe = roe * 100
            profit_margin = info.get("profitMargins")
            if profit_margin:
                profit_margin = profit_margin * 100
            
            # 배당 정보
            dividend_yield = info.get("dividendYield")
            if dividend_yield:
                dividend_yield = dividend_yield * 100
            
            # 점수 계산 시스템
            total_score = 0
            max_possible_score = 0
            score_breakdown = []
            
            # 1. 기술적 분석 점수 (30점)
            technical_score = 0
            max_possible_score += 30
            
            # RSI 분석 (10점)
            if current_rsi is not None:
                if 40 <= current_rsi <= 60:
                    technical_score += 10
                    score_breakdown.append("✅ RSI 건강 (40-60 범위): +10점")
                elif 30 <= current_rsi <= 70:
                    technical_score += 7
                    score_breakdown.append("⚠️ RSI 보통 (30-70 범위): +7점")
                elif current_rsi > 70:
                    technical_score += 3
                    score_breakdown.append("⚠️ RSI 과매수 (>70): +3점")
                elif current_rsi < 30:
                    technical_score += 5
                    score_breakdown.append("⚠️ RSI 과매도 (<30): +5점")
            else:
                score_breakdown.append("📊 RSI 데이터 없음")
            
            # 이동평균선 분석 (10점)
            if sma_20 is not None and sma_50 is not None:
                if current_close > sma_20 > sma_50:
                    technical_score += 10
                    score_breakdown.append("✅ 강한 상승 추세 (가격 > SMA20 > SMA50): +10점")
                elif current_close > sma_20:
                    technical_score += 7
                    score_breakdown.append("✅ 단기 상승 추세 (가격 > SMA20): +7점")
                elif current_close > sma_50:
                    technical_score += 5
                    score_breakdown.append("⚠️ 중장기 상승 (가격 > SMA50): +5점")
                else:
                    technical_score += 2
                    score_breakdown.append("⚠️ 하락 추세: +2점")
            else:
                score_breakdown.append("📊 이동평균선 데이터 부족")
            
            # 거래량 분석 (10점)
            if current_volume and avg_volume:
                volume_ratio = current_volume / avg_volume
                if volume_ratio > 1.5:
                    technical_score += 8
                    score_breakdown.append("✅ 높은 거래량 (평균 대비 1.5배 이상): +8점")
                elif volume_ratio > 1.2:
                    technical_score += 6
                    score_breakdown.append("✅ 증가된 거래량 (평균 대비 1.2배 이상): +6점")
                elif volume_ratio > 0.8:
                    technical_score += 5
                    score_breakdown.append("⚠️ 보통 거래량: +5점")
                else:
                    technical_score += 3
                    score_breakdown.append("⚠️ 낮은 거래량: +3점")
            
            total_score += technical_score
            
            # 2. 밸류에이션 점수 (25점)
            valuation_score = 0
            max_possible_score += 25
            
            # PE 비율 분석 (15점)
            if pe_ratio and pe_ratio > 0:
                if pe_ratio < 15:
                    valuation_score += 15
                    score_breakdown.append(f"✅ 저평가 PER ({pe_ratio:.1f}): +15점")
                elif pe_ratio < 25:
                    valuation_score += 10
                    score_breakdown.append(f"✅ 적정 PER ({pe_ratio:.1f}): +10점")
                elif pe_ratio < 35:
                    valuation_score += 5
                    score_breakdown.append(f"⚠️ 높은 PER ({pe_ratio:.1f}): +5점")
                else:
                    valuation_score += 2
                    score_breakdown.append(f"⚠️ 매우 높은 PER ({pe_ratio:.1f}): +2점")
            else:
                score_breakdown.append("📊 PER 데이터 없음")
            
            # PB 비율 분석 (10점)
            if pb_ratio and pb_ratio > 0:
                if pb_ratio < 1:
                    valuation_score += 10
                    score_breakdown.append(f"✅ 저평가 PBR ({pb_ratio:.1f}): +10점")
                elif pb_ratio < 3:
                    valuation_score += 7
                    score_breakdown.append(f"✅ 적정 PBR ({pb_ratio:.1f}): +7점")
                elif pb_ratio < 5:
                    valuation_score += 4
                    score_breakdown.append(f"⚠️ 높은 PBR ({pb_ratio:.1f}): +4점")
                else:
                    valuation_score += 1
                    score_breakdown.append(f"⚠️ 매우 높은 PBR ({pb_ratio:.1f}): +1점")
            else:
                score_breakdown.append("📊 PBR 데이터 없음")
            
            total_score += valuation_score
            
            # 3. 재무 건전성 점수 (25점)
            financial_score = 0
            max_possible_score += 25
            
            # 부채비율 (8점)
            if debt_to_equity is not None:
                if debt_to_equity < 0.3:
                    financial_score += 8
                    score_breakdown.append(f"✅ 우수한 부채비율 ({debt_to_equity:.1f}): +8점")
                elif debt_to_equity < 0.6:
                    financial_score += 6
                    score_breakdown.append(f"✅ 양호한 부채비율 ({debt_to_equity:.1f}): +6점")
                elif debt_to_equity < 1.0:
                    financial_score += 4
                    score_breakdown.append(f"⚠️ 보통 부채비율 ({debt_to_equity:.1f}): +4점")
                else:
                    financial_score += 2
                    score_breakdown.append(f"⚠️ 높은 부채비율 ({debt_to_equity:.1f}): +2점")
            
            # ROE (8점)
            if roe is not None:
                if roe > 20:
                    financial_score += 8
                    score_breakdown.append(f"✅ 우수한 ROE ({roe:.1f}%): +8점")
                elif roe > 15:
                    financial_score += 6
                    score_breakdown.append(f"✅ 양호한 ROE ({roe:.1f}%): +6점")
                elif roe > 10:
                    financial_score += 4
                    score_breakdown.append(f"⚠️ 보통 ROE ({roe:.1f}%): +4점")
                else:
                    financial_score += 2
                    score_breakdown.append(f"⚠️ 낮은 ROE ({roe:.1f}%): +2점")
            
            # 순이익률 (9점)
            if profit_margin is not None:
                if profit_margin > 20:
                    financial_score += 9
                    score_breakdown.append(f"✅ 우수한 순이익률 ({profit_margin:.1f}%): +9점")
                elif profit_margin > 10:
                    financial_score += 7
                    score_breakdown.append(f"✅ 양호한 순이익률 ({profit_margin:.1f}%): +7점")
                elif profit_margin > 5:
                    financial_score += 4
                    score_breakdown.append(f"⚠️ 보통 순이익률 ({profit_margin:.1f}%): +4점")
                else:
                    financial_score += 2
                    score_breakdown.append(f"⚠️ 낮은 순이익률 ({profit_margin:.1f}%): +2점")
            
            total_score += financial_score
            
            # 4. 리스크 점수 (20점)
            risk_score = 20  # 기본 점수에서 리스크 요인 차감
            
            # 변동성 분석
            if volatility is not None:
                if volatility > 50:
                    risk_score -= 10
                    score_breakdown.append(f"⚠️ 높은 변동성 ({volatility:.1f}%): -10점")
                elif volatility > 30:
                    risk_score -= 5
                    score_breakdown.append(f"⚠️ 보통 변동성 ({volatility:.1f}%): -5점")
                else:
                    score_breakdown.append(f"✅ 낮은 변동성 ({volatility:.1f}%): 0점")
            
            total_score += max(risk_score, 0)
            
            # 최종 점수 계산 (백분율)
            if max_possible_score > 0:
                final_score = int((total_score / max_possible_score) * 100)
            else:
                final_score = 0
            
            # 투자 등급 결정
            if final_score >= 80:
                investment_grade = "A+ (강한 매수)"
                recommendation = "적극 매수 추천"
            elif final_score >= 70:
                investment_grade = "A (매수)"
                recommendation = "매수 추천"
            elif final_score >= 60:
                investment_grade = "B+ (약간 매수)"
                recommendation = "신중한 매수 고려"
            elif final_score >= 50:
                investment_grade = "B (중립)"
                recommendation = "관망"
            elif final_score >= 40:
                investment_grade = "C+ (약간 매도)"
                recommendation = "신중한 매도 고려"
            elif final_score >= 30:
                investment_grade = "C (매도)"
                recommendation = "매도 권장"
            else:
                investment_grade = "D (강한 매도)"
                recommendation = "적극 매도 권장"
            
            # 포맷 함수
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
            
            # 포맷팅 함수들
            def format_float(value, decimals=1):
                return f"{value:.{decimals}f}" if value is not None else 'N/A'
            
            def format_currency(value, decimals=2):
                return f"${value:.{decimals}f}" if value is not None else 'N/A'
            
            # 결과 출력
            result = f"""
🚀 종합 주식 분석 보고서: {company_name} ({ticker})
=======================================================
📊 종합 투자 점수: {final_score}/100
🎯 투자 등급: {investment_grade}
💡 투자 권고: {recommendation}

📈 기본 정보:
• 현재가: ${current_price} ({today} 기준)
• 업종: {sector} - {industry}
• 시가총액: {format_number(market_cap)}

🔍 기술적 지표:
• RSI: {format_float(current_rsi)}
• SMA20: {format_currency(sma_20)}
• SMA50: {format_currency(sma_50)}
• 변동성 (연환산): {format_float(volatility)}%

💰 밸류에이션:
• PER: {format_float(pe_ratio)}
• PBR: {format_float(pb_ratio)}
• 배당수익률: {format_float(dividend_yield, 2)}%

🏦 재무 지표:
• 부채비율: {format_float(debt_to_equity, 2)}
• ROE: {format_float(roe)}%
• 순이익률: {format_float(profit_margin)}%

📊 점수 상세 분석:
"""
            
            for breakdown in score_breakdown:
                result += f"• {breakdown}\n"
            
            result += f"""
🎯 투자 가이드:
• 80-100점: 매우 우수한 투자 기회
• 70-79점: 좋은 투자 기회
• 60-69점: 보통, 신중한 검토 필요
• 50-59점: 중립, 다른 옵션 고려
• 40-49점: 투자 리스크 높음
• 40점 미만: 투자 비추천

⚠️ 면책 조항:
본 분석은 참고용이며 투자 결정은 본인 책임입니다.
추가 리서치와 전문가 상담을 권장합니다.

※ 데이터 출처: Yahoo Finance (실시간)
※ 분석 날짜: {today}
"""
            
            return result
            
        except Exception as e:
            return f"❌ 주식 분석 실패 ({ticker}): {str(e)}\n※ 올바른 티커 심볼을 입력했는지 확인하세요."

# Tool instance
get_advanced_stock_analysis = AdvancedStockAnalysisTool()