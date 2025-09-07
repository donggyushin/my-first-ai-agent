from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from tools.news_sentiment_tool import analyze_news_sentiment
from tools.advanced_stock_analysis import get_advanced_stock_analysis
from tools.financial_tools import get_real_time_valuation, get_real_time_financial_health
import os

class InvestmentAdvisorCrew:
    """실시간 주식 분석 및 투자 조언을 제공하는 크루"""

    def __init__(self):
        # GPT-4o 모델 설정
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # 웹 검색 도구
        self.search_tool = SerperDevTool()

    def news_analyst(self) -> Agent:
        return Agent(
            role='뉴스 감정 분석가',
            goal='주식 종목에 대한 최신 뉴스를 분석하여 시장 감정을 평가합니다',
            verbose=True,
            memory=True,
            backstory="""당신은 금융 뉴스 분석 전문가로서 10년 이상의 경험을 가지고 있습니다.
            다양한 뉴스 소스를 통해 주식에 대한 시장 감정을 정확히 분석하고,
            투자자들에게 신뢰할 수 있는 뉴스 기반 인사이트를 제공합니다.
            특히 단기적 주가 변동에 영향을 미치는 뉴스 요인들을 잘 파악합니다.""",
            tools=[analyze_news_sentiment, self.search_tool],
            llm=self.llm,
        )

    def technical_analyst(self) -> Agent:
        return Agent(
            role='기술적 분석가',
            goal='주식의 기술적 지표와 재무 데이터를 분석하여 투자 점수를 계산합니다',
            verbose=True,
            memory=True,
            backstory="""당신은 CFA 자격을 가진 기술적 분석 전문가입니다.
            RSI, 이동평균선, 거래량 등의 기술적 지표와 PER, PBR, ROE 등의
            재무 지표를 종합적으로 분석하여 객관적인 투자 점수를 산출합니다.
            특히 실시간 데이터를 바탕으로 한 정확한 분석을 제공합니다.""",
            tools=[get_advanced_stock_analysis, get_real_time_valuation, get_real_time_financial_health],
            llm=self.llm,
        )

    def investment_advisor(self) -> Agent:
        return Agent(
            role='최종 투자 자문가',
            goal='뉴스 감정 분석과 기술적 분석을 종합하여 최종 투자 결정을 제공합니다',
            verbose=True,
            memory=True,
            backstory="""당신은 20년 경력의 포트폴리오 매니저로서 수많은 성공적인 투자를 이끌어왔습니다.
            뉴스 감정 분석과 기술적 분석 결과를 종합하여 리스크를 최소화하면서
            수익을 극대화할 수 있는 투자 전략을 제시합니다.
            실제 투자에 사용할 수 있는 구체적이고 실용적인 조언을 제공합니다.

            절대로 모의 데이터나 가상의 데이터를 사용하지 않으며,
            오직 실제 API를 통해 수집된 실시간 데이터만을 기반으로 분석합니다.""",
            tools=[self.search_tool],
            llm=self.llm,
        )

    def analyze_news_sentiment_task(self) -> Task:
        return Task(
            description="""주어진 주식 종목 '{ticker}'에 대한 뉴스 감정 분석을 수행하세요.

            수행할 작업:
            1. 최근 7일간의 주요 뉴스 기사들을 수집하고 분석
            2. 긍정적/부정적 키워드를 바탕으로 감정 점수 계산 (0-100점)
            3. 각 뉴스 기사의 투자 관점에서의 영향도 평가
            4. 전반적인 시장 감정과 단기 주가 전망 제시

            주의사항:
            - 실제 뉴스 데이터만 사용하고 가상의 데이터는 절대 사용하지 마세요
            - 감정 점수는 객관적 기준에 따라 계산하세요
            - 뉴스의 신뢰성과 영향력을 고려하세요""",
            expected_output="""다음 형식으로 뉴스 감정 분석 결과를 제공하세요:

            ## 뉴스 감정 분석 결과
            - **종합 감정 점수**: X/100
            - **시장 감정**: 긍정적/부정적/중립
            - **주요 뉴스 요약**: (상위 3-5개 뉴스의 핵심 내용)
            - **단기 전망**: (뉴스 기반 1-2주 주가 전망)
            - **리스크 요인**: (부정적 뉴스나 우려사항)""",
            agent=self.news_analyst(),
        )

    def technical_analysis_task(self) -> Task:
        return Task(
            description="""주어진 주식 종목 '{ticker}'에 대한 종합적인 기술적 분석을 수행하세요.

            수행할 작업:
            1. 실시간 주가 데이터와 기술적 지표 분석 (RSI, 이동평균선, 거래량 등)
            2. 재무 건전성 지표 분석 (PER, PBR, 부채비율, ROE 등)
            3. 밸류에이션 분석 및 적정 가격 평가
            4. 종합 투자 점수 계산 (0-100점)
            5. 리스크 요인 및 변동성 분석

            주의사항:
            - 반드시 실시간 API 데이터를 사용하세요
            - 모든 지표의 계산 근거를 명확히 제시하세요
            - 객관적이고 정량적인 분석을 우선하세요""",
            expected_output="""다음 형식으로 기술적 분석 결과를 제공하세요:

            ## 기술적 분석 결과
            - **종합 투자 점수**: X/100
            - **투자 등급**: A+/A/B+/B/C+/C/D
            - **현재 가격**: $X.XX (날짜 기준)
            - **주요 기술적 지표**:
              - RSI: XX (과매수/과매도/중립)
              - 이동평균선: 상승/하락 추세
              - 거래량: 증가/감소/보통
            - **재무 건전성**:
              - PER: XX (저평가/적정/고평가)
              - 부채비율: XX (우수/양호/위험)
              - ROE: XX% (우수/보통/낮음)
            - **리스크 수준**: 높음/보통/낮음
            - **적정 가격대**: $XX - $XX""",
            agent=self.technical_analyst(),
        )

    def final_investment_decision_task(self) -> Task:
        return Task(
            description="""뉴스 감정 분석과 기술적 분석 결과를 종합하여 최종 투자 결정을 내리세요.

            분석할 내용:
            1. 뉴스 감정 점수와 기술적 분석 점수의 가중 평균 계산
            2. 두 분석 결과 간의 일치도 또는 차이점 분석
            3. 단기/중기/장기 투자 관점별 전략 제시
            4. 구체적인 매수/매도/보유 권고안 결정
            5. 목표 가격, 손절매 가격, 투자 비중 제시

            가중치:
            - 뉴스 감정 분석: 40%
            - 기술적 분석: 60%

            주의사항:
            - 실제 투자에 사용할 수 있을 정도로 구체적이고 실용적인 조언 제공
            - 리스크를 명확히 고지하고 위험 관리 방안 제시
            - 시장 상황 변화에 따른 대응 방안 포함""",
            expected_output="""다음 형식으로 최종 투자 결정을 제공하세요:

            # 최종 투자 결정 보고서: {ticker}

            ## 📊 종합 분석 결과
            - **최종 투자 점수**: X/100 (뉴스 감정: X점 + 기술적 분석: X점)
            - **투자 권고**: 강한 매수/매수/보유/매도/강한 매도
            - **신뢰도**: 높음/보통/낮음

            ## 🎯 투자 전략
            - **추천 투자 비중**: 포트폴리오의 X%
            - **목표 가격**: $XX (상승 여력: X%)
            - **손절매 가격**: $XX (하락 위험: X%)
            - **투자 기간**: 단기/중기/장기

            ## ⚖️ 리스크 분석
            - **주요 리스크**: (구체적 위험 요인 3개)
            - **리스크 수준**: 높음/보통/낮음
            - **대응 방안**: (리스크 관리 전략)

            ## 💡 핵심 투자 포인트
            1. **매수 이유**: (가장 강력한 매수 근거)
            2. **주의사항**: (투자 시 주의할 점)
            3. **모니터링 지표**: (지속적으로 관찰해야 할 지표들)

            ## ⚠️ 면책조항
            본 분석은 투자 참고용이며, 최종 투자 결정은 본인의 책임입니다.
            """,
            agent=self.investment_advisor(),
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.news_analyst(),
                self.technical_analyst(),
                self.investment_advisor()
            ],
            tasks=[
                self.analyze_news_sentiment_task(),
                self.technical_analysis_task(),
                self.final_investment_decision_task()
            ],
            process=Process.sequential,
            verbose=True,
            # memory=True,
            # output_log_file="investment_analysis_log.txt"
        )