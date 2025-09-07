from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import os
import yfinance as yf
import requests
import json
from typing import List

class InvestmentItemRecommendarCrew:
    """투자 종목 추천을 위한 크루 - 인기 종목 검색 및 기술적 분석 기반 추천"""

    def __init__(self):
        # GPT-4o 모델 설정
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # 웹 검색 도구
        self.search_tool = SerperDevTool()

    def get_popular_stocks(self) -> str:
        """현재 인기 있는 미국 주식 종목들을 가져오는 도구"""
        try:
            # S&P 500 상위 종목들과 최근 인기 종목들 수집
            popular_tickers = [
                # Tech giants
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
                # Financial
                'JPM', 'BAC', 'WFC', 'GS', 'MS',
                # Healthcare
                'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK',
                # Consumer
                'KO', 'PEP', 'WMT', 'HD', 'DIS',
                # Energy
                'XOM', 'CVX', 'COP',
                # Other popular
                'V', 'MA', 'NFLX', 'AMD', 'INTC'
            ]
            
            # yfinance를 사용해서 실시간 데이터 확인 및 필터링
            valid_stocks = []
            for ticker in popular_tickers[:30]:  # 30개 확인해서 최소 20개 이상 확보
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    if 'regularMarketPrice' in info and info['regularMarketPrice'] is not None:
                        valid_stocks.append({
                            'ticker': ticker,
                            'name': info.get('longName', ticker),
                            'price': info.get('regularMarketPrice', 0),
                            'volume': info.get('regularMarketVolume', 0),
                            'marketCap': info.get('marketCap', 0)
                        })
                except:
                    continue
                    
            return json.dumps(valid_stocks[:25], indent=2)  # 25개 반환
            
        except Exception as e:
            return f"Error fetching popular stocks: {str(e)}"

    def analyze_technical_indicators(self, stocks_data: str) -> str:
        """기술적 분석을 통해 종목들을 점수화하는 도구"""
        try:
            stocks = json.loads(stocks_data) if isinstance(stocks_data, str) else stocks_data
            scored_stocks = []
            
            for stock in stocks:
                ticker = stock['ticker']
                try:
                    # yfinance로 상세 데이터 가져오기
                    yf_stock = yf.Ticker(ticker)
                    hist = yf_stock.history(period="3mo")  # 3개월 데이터
                    info = yf_stock.info
                    
                    if len(hist) < 20:  # 충분한 데이터가 없으면 스킵
                        continue
                    
                    # 기술적 지표 계산
                    current_price = hist['Close'].iloc[-1]
                    
                    # RSI 계산
                    delta = hist['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs)).iloc[-1]
                    
                    # 이동평균선
                    ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                    ma50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else ma20
                    
                    # 거래량 증가율
                    avg_volume = hist['Volume'].rolling(window=20).mean().iloc[-20:-1].mean()
                    recent_volume = hist['Volume'].iloc[-5:].mean()
                    volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
                    
                    # 가격 모멘텀
                    price_change_20d = (current_price - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21] * 100 if len(hist) >= 21 else 0
                    
                    # 점수 계산 (0-100)
                    score = 0
                    
                    # RSI 점수 (30점 만점)
                    if 30 <= rsi <= 70:
                        score += 30  # 적정 범위
                    elif 20 <= rsi < 30:
                        score += 25  # 과매도 (매수 기회)
                    elif rsi < 20:
                        score += 20  # 심한 과매도
                    else:
                        score += 10  # 과매수
                    
                    # 이동평균선 점수 (25점 만점)
                    if current_price > ma20 > ma50:
                        score += 25  # 상승 추세
                    elif current_price > ma20:
                        score += 20  # 단기 상승
                    elif current_price > ma50:
                        score += 15  # 중기 상승
                    else:
                        score += 5   # 하락 추세
                    
                    # 거래량 점수 (20점 만점)
                    if volume_ratio > 1.5:
                        score += 20  # 거래량 급증
                    elif volume_ratio > 1.2:
                        score += 15  # 거래량 증가
                    elif volume_ratio > 0.8:
                        score += 10  # 정상 거래량
                    else:
                        score += 5   # 거래량 저조
                    
                    # 모멘텀 점수 (25점 만점)
                    if price_change_20d > 10:
                        score += 25  # 강한 상승
                    elif price_change_20d > 5:
                        score += 20  # 상승
                    elif price_change_20d > 0:
                        score += 15  # 약한 상승
                    elif price_change_20d > -5:
                        score += 10  # 약한 하락
                    else:
                        score += 5   # 강한 하락
                    
                    scored_stocks.append({
                        'ticker': ticker,
                        'name': stock.get('name', ticker),
                        'current_price': round(current_price, 2),
                        'score': round(score, 1),
                        'rsi': round(rsi, 1),
                        'price_vs_ma20': round(((current_price - ma20) / ma20) * 100, 1),
                        'volume_ratio': round(volume_ratio, 2),
                        'momentum_20d': round(price_change_20d, 1)
                    })
                    
                except Exception as e:
                    continue
            
            # 점수 순으로 정렬하여 상위 5개 선택
            scored_stocks.sort(key=lambda x: x['score'], reverse=True)
            top_5_stocks = scored_stocks[:5]
            
            return json.dumps(top_5_stocks, indent=2)
            
        except Exception as e:
            return f"Error in technical analysis: {str(e)}"

    def stock_researcher(self) -> Agent:
        """현재 시장에서 인기 있는 미국 주식 종목들을 검색하는 에이전트"""
        
        # Create a simple function-based tool
        class PopularStocksTool:
            def __init__(self, crew_instance):
                self.crew = crew_instance
            
            def run(self, query: str = "") -> str:
                """현재 인기 있는 미국 주식 종목들을 수집합니다."""
                return self.crew.get_popular_stocks()
        
        popular_stocks_tool = PopularStocksTool(self)
        
        return Agent(
            role='주식 시장 리서처',
            goal='현재 시장에서 인기 있는 미국 주식 종목 20개 이상을 수집하고 기본 정보를 제공합니다',
            verbose=True,
            memory=True,
            backstory="""당신은 미국 주식 시장 전문 리서처로서 실시간으로 인기 종목들을 추적합니다.
            S&P 500, NASDAQ의 주요 종목들과 최근 트렌드를 파악하여 
            투자자들에게 관심받고 있는 종목들을 선별하는 전문가입니다.
            특히 거래량, 시가총액, 최근 성과 등을 종합적으로 고려하여
            투자 가치가 있는 종목들을 식별합니다.""",
            tools=[self.search_tool],
            llm=self.llm,
        )

    def technical_analyst(self) -> Agent:
        """기술적 분석을 통해 상위 5개 종목을 선별하는 에이전트"""
        
        return Agent(
            role='기술적 분석 전문가',
            goal='제공받은 주식 종목들을 기술적 분석하여 가장 높은 점수를 받은 5개 종목을 선별합니다',
            verbose=True,
            memory=True,
            backstory="""당신은 CFA 자격증을 보유한 기술적 분석 전문가입니다.
            RSI, 이동평균선, 거래량 분석, 가격 모멘텀 등의 기술적 지표를 활용하여
            객관적인 점수 체계로 종목을 평가합니다.
            단기에서 중기까지의 수익 가능성이 높은 종목들을 선별하는데 뛰어난 능력을 가지고 있으며,
            리스크 대비 수익률을 극대화하는 종목 선정에 특화되어 있습니다.
            
            당신은 이전 에이전트로부터 받은 주식 종목 리스트를 분석하여 
            각 종목의 기술적 지표를 계산하고 점수를 매깁니다.""",
            tools=[],
            llm=self.llm,
        )

    def research_popular_stocks_task(self) -> Task:
        """인기 미국 주식 종목들을 수집하는 태스크"""
        
        # 미리 계산된 인기 종목 리스트를 제공
        popular_stocks_data = self.get_popular_stocks()
        
        return Task(
            description=f"""다음은 현재 시장에서 인기 있는 미국 주식 종목들입니다:

            {popular_stocks_data}

            이 데이터를 기반으로 최소 20개 이상의 인기 종목 정보를 정리하고 검증하세요.

            수행할 작업:
            1. 제공된 종목 리스트를 검토하고 검증
            2. 필요시 웹 검색을 통해 추가 정보나 최신 동향 확인
            3. 다양한 섹터에서 균형있게 선별된 것인지 확인
            4. JSON 형식으로 최종 결과 정리

            주의사항:
            - 실제로 거래되고 있는 종목들만 포함
            - 최소 20개 이상의 종목 확보
            - 정확한 JSON 형식으로 출력""",
            expected_output="""다음 JSON 형식으로 인기 미국 주식 종목 리스트를 제공하세요:

            [
                {
                    "ticker": "AAPL",
                    "name": "Apple Inc.",
                    "price": 150.25,
                    "volume": 50000000,
                    "marketCap": 2400000000000
                },
                ...
            ]

            최소 20개 이상의 종목을 포함해야 합니다.""",
            agent=self.stock_researcher(),
        )

    def technical_analysis_task(self) -> Task:
        """기술적 분석을 통해 상위 5개 종목을 선별하는 태스크"""
        return Task(
            description="""이전 단계에서 수집된 주식 종목들을 분석하여 가장 투자 가치가 높은 5개 종목을 선별하세요.

            분석 방법:
            1. 이전 에이전트가 제공한 종목 리스트에서 각 종목을 평가
            2. RSI, 이동평균선, 거래량, 가격 모멘텀 등을 고려한 종합 점수 계산
            3. 100점 만점으로 점수를 매기고 상위 5개 선별
            4. 실제 yfinance 데이터를 활용한 객관적 분석 수행

            점수 기준:
            - 기술적 지표의 건전성
            - 최근 주가 추세
            - 거래량 패턴
            - 위험 대비 수익 가능성

            중요사항:
            - 반드시 실시간 데이터를 기반으로 분석
            - 객관적이고 정량적인 평가 수행
            - 단기~중기 투자 관점에서 평가""",
            expected_output="""다음 JSON 형식으로 상위 5개 종목의 분석 결과를 제공하세요:

            [
                {
                    "ticker": "AAPL",
                    "name": "Apple Inc.",
                    "current_price": 150.25,
                    "score": 87.5,
                    "rsi": 45.2,
                    "price_vs_ma20": 5.3,
                    "volume_ratio": 1.8,
                    "momentum_20d": 8.7
                },
                ...
            ]

            정확히 5개의 종목만 포함하고, 점수 순으로 정렬해주세요.""",
            agent=self.technical_analyst(),
            context=[self.research_popular_stocks_task()],
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.stock_researcher(),
                self.technical_analyst()
            ],
            tasks=[
                self.research_popular_stocks_task(),
                self.technical_analysis_task()
            ],
            process=Process.sequential,
            verbose=True,
        )