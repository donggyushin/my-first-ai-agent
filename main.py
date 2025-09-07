import dotenv

dotenv.load_dotenv()

from crews.stock_crew import LatestStockCrew
from crews.portfolio_crew import PortfolioCrew

if __name__ == "__main__":
    # 1. 주식 분석 실행
    stock_crew = LatestStockCrew()

    # 유저로부터 주식 티커 또는 회사명 입력받기
    topic = input("연구하고 싶은 주식 티커나 회사명을 입력하세요: ")

    print(f"\n'{topic}'에 대한 주식 연구를 시작합니다...\n")
    # 입력받은 주제로 연구 실행
    stock_crew.crew().kickoff(inputs={"topic": topic})

    print("\n" + "="*60)
    print("🎉 주식 분석이 완료되었습니다!")
    print("output 폴더에 다음 보고서들이 생성되었습니다:")
    print("• research_report.md (뉴스 리서치)")
    print("• investment_analysis.md (영문 투자분석)")
    print("• investment_analysis_kr.md (한글 투자분석)")
    print("• compacted_investment_analysis_kr.md (한글 요약보고서)")
    print("="*60)

    # 2. 개인화된 포트폴리오 조언 옵션
    portfolio_advice = input("\n📈 개인화된 포트폴리오 조언을 받으시겠습니까? (y/n): ").lower().strip()

    if portfolio_advice == 'y':
        try:
            # 평균 단가 입력받기
            avg_cost = input(f"\n💰 {topic} 주식의 현재 평균 단가를 달러로 입력하세요 (예: 150.50): $")
            avg_cost_float = float(avg_cost)

            print(f"\n🔍 평균 단가 ${avg_cost}를 기준으로 {topic}에 대한 개인화된 포트폴리오 분석을 시작합니다...\n")

            # 포트폴리오 분석 실행
            portfolio_crew = PortfolioCrew()
            portfolio_crew.crew().kickoff(inputs={
                "ticker": topic,
                "avg_cost": avg_cost
            })

            print("\n" + "="*60)
            print("🎯 개인화된 포트폴리오 조언이 완료되었습니다!")
            print("• portfolio_recommendation_kr.md (한글 포트폴리오 추천)")
            print("="*60)

        except ValueError:
            print("❌ 올바른 숫자 형식으로 입력해주세요. 프로그램을 다시 실행해보세요.")
        except Exception as e:
            print(f"❌ 포트폴리오 분석 중 오류가 발생했습니다: {str(e)}")

    elif portfolio_advice == 'n':
        print("\n✅ 분석을 종료합니다. output 폴더의 보고서를 확인해보세요!")
    else:
        print("❌ 'y' 또는 'n'으로 입력해주세요. 프로그램을 다시 실행해보세요.")