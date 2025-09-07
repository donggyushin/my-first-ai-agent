import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task

@CrewBase
class TranslatorCrew:

    @agent
    def translator_agent(self):
        return Agent(
            role="Human-like English to Korean Translator",
            goal="Provide natural, contextually appropriate Korean translations that capture both the literal meaning and cultural nuances of English text",
            backstory="You are an experienced translator with deep understanding of both English and Korean cultures. You have spent years bridging communication gaps between English and Korean speakers, specializing in making translations feel natural and human-like rather than robotic. You understand cultural context, idioms, and the subtle differences in formality levels in Korean language.",
            verbose=True
        )

    @task
    def translate_task(self):
        return Task(
            description="Translate the following English text to Korean with natural, human-like expressions that consider cultural context and appropriate formality levels: {text}",
            expected_output="A natural Korean translation that accurately conveys the meaning, tone, and cultural nuances of the original English text.",
            agent=self.translator_agent()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.translator_agent()],
            tasks=[self.translate_task()],
            process_mode='sequential',
            verbose=True
        )


if __name__ == "__main__":
    # 사용 예시
    translator_crew = TranslatorCrew()

    # 번역할 영어 텍스트 (더 어렵고 긴 내용)
    english_text = """
    The rapid advancement of artificial intelligence has fundamentally transformed the landscape of modern technology, creating unprecedented opportunities while simultaneously raising profound ethical questions about the future of human-machine interaction. As machine learning algorithms become increasingly sophisticated, they demonstrate remarkable capabilities in pattern recognition, natural language processing, and decision-making processes that were once considered exclusively within the domain of human cognition. However, this technological revolution also presents significant challenges regarding privacy, employment displacement, and the potential for algorithmic bias that could perpetuate existing societal inequalities. Consequently, it has become imperative for policymakers, technologists, and society at large to engage in thoughtful discourse about establishing comprehensive frameworks that can harness the transformative potential of AI while mitigating its associated risks and ensuring equitable access to its benefits across diverse communities.
    """

    # crew 실행
    result = translator_crew.crew().kickoff(inputs={"text": english_text})

    print("번역 결과:")
    print(result)