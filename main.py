import dotenv

dotenv.load_dotenv()

from crewai.project import CrewBase, agent, crew, task
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent

from crewai_tools import SerperDevTool

@CrewBase
class LatestStcokCrew():

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def investment_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_analyst'], # type: ignore[index]
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestStcokCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

if __name__ == "__main__":
    crew = LatestStcokCrew()

    # 유저로부터 주식 티커 또는 회사명 입력받기
    topic = input("연구하고 싶은 주식 티커나 회사명을 입력하세요: ")

    print(f"\n'{topic}'에 대한 주식 연구를 시작합니다...\n")

    # 입력받은 주제로 연구 실행
    result = crew.crew().kickoff(inputs={"topic": topic})

    print("\n" + "="*50)
    print("연구 결과:")
    print("="*50)
    print(result)