import dotenv
import sys

dotenv.load_dotenv()

from crews.investment_advisor_crew import InvestmentAdvisorCrew

if __name__ == "__main__":
    print("🚀 실시간 주식 투자 자문 시스템")
    print("=" * 50)
    
    # 유저로부터 주식 티커 입력받기
    ticker = input("\n📈 분석하고 싶은 주식 티커를 입력하세요 (예: AAPL, BOIL, TSLA): ").upper().strip()
    
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