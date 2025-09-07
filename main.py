import dotenv

dotenv.load_dotenv()

from crews.stock_crew import LatestStockCrew

if __name__ == "__main__":
    crew = LatestStockCrew()

    # 유저로부터 주식 티커 또는 회사명 입력받기
    topic = input("연구하고 싶은 주식 티커나 회사명을 입력하세요: ")

    print(f"\n'{topic}'에 대한 주식 연구를 시작합니다...\n")
    # 입력받은 주제로 연구 실행
    crew.crew().kickoff(inputs={"topic": topic})