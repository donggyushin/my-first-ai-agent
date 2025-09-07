import dotenv
import sys
import json
import os
from utils.logger import setup_logger, log_analysis_start, log_analysis_complete, log_error

dotenv.load_dotenv()

logger = setup_logger()

if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY가 환경변수에 설정되지 않았습니다.")
    print("❌ OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    sys.exit(1)

from crews.investment_advisor_crew import InvestmentAdvisorCrew
from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew

if __name__ == "__main__":
    from config.constants import MESSAGE_TEMPLATES
    
    print(MESSAGE_TEMPLATES['SYSTEM_START'])
    print("=" * 50)
    
    # 먼저 투자 종목 추천 시스템 실행
    print(f"\n{MESSAGE_TEMPLATES['RECOMMENDATION_START']}")
    print("이 과정은 1-2분 정도 소요될 수 있습니다.\n")
    
    try:
        log_analysis_start(logger, "ALL", "투자종목추천")
        recommendar_crew = InvestmentItemRecommendarCrew()
        recommendation_result = recommendar_crew.crew().kickoff()
        
        log_analysis_complete(logger, "ALL", "투자종목추천", True)
        print("\n" + "="*60)
        print("✅ AI 추천 투자 종목 분석 완료!")
        print("="*60)
        
        # JSON 형태로 결과 파싱 시도
        try:
            if isinstance(recommendation_result, str):
                # 결과에서 JSON 부분 추출
                import re
                json_match = re.search(r'\[[\s\S]*\]', recommendation_result)
                if json_match:
                    recommendations = json.loads(json_match.group())
                    print("\n📊 AI 추천 투자 종목 TOP 5:")
                    print("-" * 40)
                    for i, stock in enumerate(recommendations, 1):
                        print(f"{i}. {stock['ticker']} ({stock['name']})")
                        print(f"   현재가: ${stock['current_price']}")
                        print(f"   AI 점수: {stock['score']}/100")
                        print(f"   RSI: {stock['rsi']}")
                        print()
                else:
                    print("\n📊 AI 추천 결과:")
                    print(recommendation_result)
            else:
                print("\n📊 AI 추천 결과:")
                print(recommendation_result)
                
        except:
            print("\n📊 AI 추천 결과:")
            print(recommendation_result)
            
    except Exception as e:
        log_error(logger, e, "투자종목추천시스템")
        log_analysis_complete(logger, "ALL", "투자종목추천", False)
        print(f"\n⚠️ 추천 시스템 실행 중 오류 발생: {str(e)}")
        print("개별 종목 분석으로 진행합니다...\n")
    
    print("\n" + "="*60)
    print(MESSAGE_TEMPLATES['INDIVIDUAL_ANALYSIS'])
    print("="*60)
    
    # 유저로부터 주식 티커 입력받기
    ticker = input(f"\n{MESSAGE_TEMPLATES['TICKER_INPUT_PROMPT']}").upper().strip()
    
    if not ticker:
        logger.warning("사용자가 빈 티커를 입력했습니다.")
        print("❌ 유효한 티커를 입력해주세요.")
        sys.exit(1)
    
    # 티커 유효성 기본 검증
    if len(ticker) < 1 or len(ticker) > 10:
        logger.warning(f"유효하지 않은 티커 길이: {ticker}")
        print("❌ 유효한 티커 형식을 입력해주세요 (1-10자).")
        sys.exit(1)
    
    logger.info(f"사용자가 선택한 분석 대상 티커: {ticker}")
    print(f"\n🔍 '{ticker}'에 대한 종합 투자 분석을 시작합니다...")
    print("이 과정은 2-3분 정도 소요될 수 있습니다.\n")
    
    # 실시간 투자 자문 크루 실행
    try:
        log_analysis_start(logger, ticker, "개별종목분석")
        investment_crew = InvestmentAdvisorCrew()
        result = investment_crew.crew().kickoff(inputs={"ticker": ticker})
        
        log_analysis_complete(logger, ticker, "개별종목분석", True)
        print("\n" + "="*60)
        print(MESSAGE_TEMPLATES['ANALYSIS_COMPLETE'])
        print("="*60)
        
        # 결과 출력
        print("\n📊 최종 분석 결과:")
        print("-" * 30)
        print(result)
        
    except Exception as e:
        log_error(logger, e, f"개별종목분석-{ticker}")
        log_analysis_complete(logger, ticker, "개별종목분석", False)
        print(f"\n❌ 분석 중 오류가 발생했습니다: {str(e)}")
        print("💡 다음 사항을 확인해보세요:")
        print("• 인터넷 연결 상태")
        print("• 올바른 주식 티커 입력 (예: AAPL, MSFT)")
        print("• API 키 설정 (.env 파일)")
        print("• 상세한 오류 로그는 logs/ 폴더에서 확인하세요")
    
    print(f"\n{MESSAGE_TEMPLATES['DISCLAIMER']}")