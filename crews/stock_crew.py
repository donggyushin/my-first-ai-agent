from crewai.project import CrewBase, agent, crew, task
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent

from crewai_tools import SerperDevTool
from tools.financial_tools import get_real_time_valuation, get_real_time_financial_health

@CrewBase
class LatestStockCrew():

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
            tools=[get_real_time_valuation, get_real_time_financial_health]
        )

    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config['translator'], # type: ignore[index]
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'], # type: ignore[index]
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

    @task
    def translation_task(self) -> Task:
        return Task(
            config=self.tasks_config['translation_task'], # type: ignore[index]
        )

    @task
    def final_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_report_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestStockCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )