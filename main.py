import dotenv

dotenv.load_dotenv()

from crewai import Crew
from crewai.project import CrewBase, agent, task

@CrewBase
class TranslatorCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def translator_agent(self):
        return self.agents_config['translator_agent']

    @task
    def translate_task(self):
        return self.tasks_config['translate_task']

    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process_mode='sequential',
            verbose=True
        )