from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json
from datetime import datetime, timedelta

class NewsSearchInput(BaseModel):
    """Input schema for news sentiment analysis tool."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, BOIL, MSFT)")

class NewsSentimentTool(BaseTool):
    name: str = "analyze_news_sentiment"
    description: str = "Search for recent news about a stock and analyze sentiment to generate investment score"
    args_schema: Type[BaseModel] = NewsSearchInput

    def _run(self, ticker: str) -> str:
        try:
            import os
            # NewsAPI를 사용한 뉴스 검색 (현재는 yfinance 사용)
            # api_key = os.getenv("NEWS_API_KEY")  # 환경변수에서 안전하게 가져오기

            # 지난 7일간의 뉴스 검색
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')

            # 여러 뉴스 소스에서 검색
            search_queries = [
                f"{ticker} stock",
                f"{ticker} investment",
                f"{ticker} earnings",
                f"{ticker} forecast"
            ]

            all_articles = []

            # 실제 뉴스 API 호출 시뮬레이션 (실제로는 NewsAPI, Alpha Vantage 등 사용)
            # 여기서는 yfinance의 뉴스 데이터를 활용
            import yfinance as yf

            stock = yf.Ticker(ticker)
            news = stock.news if hasattr(stock, 'news') else []

            if not news:
                return f"❌ {ticker}에 대한 최신 뉴스를 찾을 수 없습니다."

            # 뉴스 제목들을 분석하여 감정 점수 계산
            positive_keywords = [
                'bull', 'bullish', 'rise', 'gain', 'surge', 'up', 'increase', 'growth',
                'profit', 'revenue', 'beat', 'strong', 'outperform', 'upgrade', 'buy',
                'positive', 'good', 'excellent', 'success', 'boom', 'rally'
            ]

            negative_keywords = [
                'bear', 'bearish', 'fall', 'drop', 'decline', 'down', 'decrease', 'loss',
                'miss', 'weak', 'underperform', 'downgrade', 'sell', 'negative', 'bad',
                'poor', 'concern', 'worry', 'risk', 'crash', 'plunge'
            ]

            neutral_keywords = [
                'hold', 'stable', 'steady', 'maintain', 'unchanged', 'flat', 'sideways'
            ]

            sentiment_scores = []
            analyzed_articles = []

            for article in news[:10]:  # 최근 10개 기사만 분석
                # yfinance 뉴스 구조가 변경됨: article['content']에 실제 뉴스 데이터가 있음
                content = article.get('content', {})
                title = content.get('title', '').lower()
                summary = content.get('summary', '').lower()
                description = content.get('description', '').lower()
                
                text = f"{title} {summary} {description}"

                # 감정 점수 계산
                positive_count = sum(1 for keyword in positive_keywords if keyword in text)
                negative_count = sum(1 for keyword in negative_keywords if keyword in text)
                neutral_count = sum(1 for keyword in neutral_keywords if keyword in text)

                # 점수 계산 (0-100 스케일)
                if positive_count > negative_count:
                    if positive_count >= 3:
                        score = 85 + min(positive_count * 3, 15)  # 85-100
                    elif positive_count >= 2:
                        score = 70 + positive_count * 7  # 70-84
                    else:
                        score = 60 + positive_count * 10  # 60-70
                elif negative_count > positive_count:
                    if negative_count >= 3:
                        score = max(15 - negative_count * 3, 0)  # 0-15
                    elif negative_count >= 2:
                        score = 30 - negative_count * 7  # 16-30
                    else:
                        score = 50 - negative_count * 10  # 40-50
                else:
                    score = 50  # 중립

                sentiment_scores.append(score)

                # 감정 라벨 생성
                if score >= 70:
                    sentiment = "매우 긍정적"
                elif score >= 60:
                    sentiment = "긍정적"
                elif score >= 50:
                    sentiment = "중립"
                elif score >= 30:
                    sentiment = "부정적"
                else:
                    sentiment = "매우 부정적"

                analyzed_articles.append({
                    'title': content.get('title', 'N/A'),
                    'published': content.get('pubDate', ''),
                    'sentiment': sentiment,
                    'score': score,
                    'url': content.get('canonicalUrl', {}).get('url', 'N/A')
                })

            # 전체 평균 감정 점수
            if sentiment_scores:
                avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
            else:
                avg_sentiment_score = 50

            # 최종 감정 평가
            if avg_sentiment_score >= 75:
                overall_sentiment = "매우 긍정적"
                investment_signal = "강한 매수 신호"
            elif avg_sentiment_score >= 65:
                overall_sentiment = "긍정적"
                investment_signal = "매수 신호"
            elif avg_sentiment_score >= 45:
                overall_sentiment = "중립"
                investment_signal = "관망"
            elif avg_sentiment_score >= 35:
                overall_sentiment = "부정적"
                investment_signal = "매도 고려"
            else:
                overall_sentiment = "매우 부정적"
                investment_signal = "강한 매도 신호"

            # 결과 포맷팅
            result = f"""
📰 뉴스 감정 분석 보고서: {ticker}
=====================================
🎯 종합 감정 점수: {avg_sentiment_score:.1f}/100
📊 전반적 감정: {overall_sentiment}
💡 투자 시그널: {investment_signal}

📈 분석된 뉴스 기사 ({len(analyzed_articles)}개):
"""

            for i, article in enumerate(analyzed_articles[:5], 1):  # 상위 5개만 표시
                # pubDate는 ISO 형식 문자열이므로 직접 파싱
                published_date = 'N/A'
                if article['published']:
                    try:
                        from datetime import datetime as dt
                        published_date = dt.fromisoformat(article['published'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    except:
                        published_date = article['published'][:10] if len(article['published']) >= 10 else 'N/A'
                result += f"""
{i}. {article['title'][:80]}...
   • 발행일: {published_date}
   • 감정: {article['sentiment']} ({article['score']}/100)
"""

            result += f"""
🔍 분석 방법론:
• 최근 {len(analyzed_articles)}개 뉴스 기사 분석
• 긍정/부정 키워드 빈도 분석
• 가중 평균으로 종합 점수 산출

⚠️  주의사항:
• 뉴스 감정은 단기적 변동 요인입니다
• 펀더멘털 분석과 함께 종합 판단하세요
• 투자 결정은 본인 책임하에 하시기 바랍니다

📊 감정 점수 가이드:
• 80-100: 매우 긍정적 (강한 상승 기대)
• 60-79: 긍정적 (상승 기대)
• 40-59: 중립 (횡보 예상)
• 20-39: 부정적 (하락 우려)
• 0-19: 매우 부정적 (강한 하락 우려)
"""

            return result

        except Exception as e:
            return f"❌ 뉴스 감정 분석 실패 ({ticker}): {str(e)}\n※ 인터넷 연결과 티커 심볼을 확인해주세요."

# Tool instance
analyze_news_sentiment = NewsSentimentTool()