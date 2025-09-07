import dotenv
import sys
import json

dotenv.load_dotenv()

from crews.investment_advisor_crew import InvestmentAdvisorCrew
from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew

if __name__ == "__main__":
    print("🚀 실시간 주식 투자 자문 시스템")
    print("=" * 50)
    
    # 먼저 투자 종목 추천 시스템 실행
    print("\n🔍 AI가 추천하는 투자 종목 5선을 먼저 확인해보세요!")
    print("이 과정은 1-2분 정도 소요될 수 있습니다.\n")
    
    try:
        recommendar_crew = InvestmentItemRecommendarCrew()
        recommendation_result = recommendar_crew.crew().kickoff()
        
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
        print(f"\n⚠️ 추천 시스템 실행 중 오류 발생: {str(e)}")
        print("개별 종목 분석으로 진행합니다...\n")
    
    print("\n" + "="*60)
    print("개별 종목 상세 분석")
    print("="*60)
    
    # 유저로부터 주식 티커 입력받기
    ticker = input("\n📈 상세 분석하고 싶은 주식 티커를 입력하세요 (예: AAPL, BOIL, TSLA): ").upper().strip()
    
    if not ticker:
        print("❌ 유효한 티커를 입력해주세요.")
        sys.exit(1)
    
    print(f"\n🔍 '{ticker}'에 대한 종합 투자 분석을 시작합니다...")
    print("이 과정은 2-3분 정도 소요될 수 있습니다.\n")
    
    # 실시간 투자 자문 크루 실행
    try:
        investment_crew = InvestmentAdvisorCrew()
        result = investment_crew.crew().kickoff(inputs={"ticker": ticker})
        
        print("\n" + "="*60)
        print("✅ 종합 투자 분석이 완료되었습니다!")
        print("="*60)
        
        # 결과 출력
        print("\n📊 최종 분석 결과:")
        print("-" * 30)
        print(result)
        
    except Exception as e:
        print(f"\n❌ 분석 중 오류가 발생했습니다: {str(e)}")
        print("💡 다음 사항을 확인해보세요:")
        print("• 인터넷 연결 상태")
        print("• 올바른 주식 티커 입력 (예: AAPL, MSFT)")
        print("• API 키 설정 (.env 파일)")
    
    print(f"\n⚠️  면책조항: 본 분석은 투자 참고용이며, 최종 투자 결정은 본인의 책임입니다.")