import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task

@CrewBase
class NewsCrew:

    @agent
    def searcher(self):
        return Agent(
            role="News Search Specialist",
            goal="Find and gather relevant news articles on specified topics from reliable sources",
            backstory="You are an experienced news researcher with expertise in finding credible and up-to-date information from various news sources. You know how to identify reliable sources and filter out noise to find the most relevant news articles.",
            verbose=True
        )

    @agent
    def summarizer(self):
        return Agent(
            role="News Summarization Expert",
            goal="Create concise, informative summaries of news articles while preserving key information and context",
            backstory="You are a skilled journalist and editor with years of experience in distilling complex news stories into clear, digestible summaries. You understand how to identify the most important points and present them in a structured, easy-to-understand format.",
            verbose=True
        )

    @agent
    def curator(self):
        return Agent(
            role="News Content Curator",
            goal="Select and organize the most relevant and important news articles for the target audience",
            backstory="You are a seasoned news curator with excellent judgment in determining newsworthiness and audience relevance. You understand how to prioritize stories, eliminate redundancy, and create well-structured news collections that provide maximum value to readers.",
            verbose=True
        )

    @agent
    def translator(self):
        return Agent(
            role="English to Korean News Translator",
            goal="Provide accurate and natural Korean translations of English news content while maintaining journalistic tone and cultural context",
            backstory="You are a professional translator specializing in news and media content with expertise in both English and Korean languages. You understand the nuances of journalistic writing in both languages and can adapt content to Korean cultural context while preserving the original meaning and tone.",
            verbose=True
        )

    @task
    def search_news_task(self):
        return Task(
            description="Search for recent news articles about the topic: {topic}. Find at least 5 relevant articles from credible sources.",
            expected_output="A list of news articles with titles, sources, URLs, and brief descriptions.",
            agent=self.searcher()
        )

    @task
    def summarize_news_task(self):
        return Task(
            description="Create concise summaries of the found news articles. Each summary should be 2-3 sentences capturing the key points.",
            expected_output="Summarized versions of each news article with key information preserved.",
            agent=self.summarizer()
        )

    @task
    def curate_news_task(self):
        return Task(
            description="Select the top 3 most important and relevant articles from the summarized news. Rank them by importance and relevance.",
            expected_output="A curated list of the top 3 news articles with explanations for why they were selected.",
            agent=self.curator()
        )

    @task
    def translate_news_task(self):
        return Task(
            description="Translate the curated English news articles to Korean while maintaining journalistic tone and accuracy.",
            expected_output="Korean translations of the curated news articles that are natural and culturally appropriate.",
            agent=self.translator()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.searcher(), self.summarizer(), self.curator(), self.translator()],
            tasks=[self.search_news_task(), self.summarize_news_task(), self.curate_news_task(), self.translate_news_task()],
            process_mode='sequential',
            verbose=True
        )


if __name__ == "__main__":
    news_crew = NewsCrew()
    
    # 뉴스 주제
    topic = "artificial intelligence latest developments"
    
    # crew 실행
    result = news_crew.crew().kickoff(inputs={"topic": topic})
    
    print("뉴스 처리 결과:")
    print(result)