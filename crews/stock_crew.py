from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from tools.financial_tools import get_real_time_valuation, get_real_time_financial_health
from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class LatestStockCrew():
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            role="Stock Market News Research Specialist",
            goal="Find and gather the most relevant and timely stock market news, company earnings reports, market analysis, and financial developments from credible financial sources. Always prioritize information from the current date and the most recent trading days.",
            backstory="You are an experienced financial journalist and market researcher with deep expertise in stock markets, financial analysis, and investment news. You have years of experience tracking market trends, company performance, and economic indicators. You know how to identify reliable financial news sources and filter out market noise to find the most impactful news that could affect stock prices and investment decisions. You always focus on the most current information available and understand that market conditions change rapidly, so you prioritize today's date and recent developments over older news.",
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def investment_analyst(self) -> Agent:
        return Agent(
            role="Professional Investment Analyst",
            goal="Analyze research reports and provide actionable investment recommendations with specific buy and sell price targets. Determine optimal entry points (buy zones), profit-taking levels (sell zones), and stop-loss levels based on fundamental analysis, technical indicators, risk assessment, and current market conditions.",
            backstory="You are a seasoned investment analyst with over 15 years of experience in equity research and portfolio management. You have worked at top-tier investment firms and have a proven track record of making profitable investment recommendations with precise price targets. You excel at analyzing company fundamentals, market trends, valuation metrics, and risk factors to provide clear, actionable investment advice with specific entry and exit strategies. You always provide concrete price ranges for buying opportunities, profit-taking levels, and risk management stop-losses. You are known for your conservative approach and always highlight both opportunities and risks with quantified price levels.",
            verbose=True,
            tools=[get_real_time_valuation, get_real_time_financial_health]
        )

    @agent
    def translator(self) -> Agent:
        return Agent(
            role="Professional Financial Document Translator",
            goal="Translate English investment analysis reports to natural, professional Korean while maintaining all financial terminology accuracy and preserving the analytical structure and recommendations. Ensure Korean readers can fully understand the investment insights.",
            backstory="You are an expert financial translator with deep knowledge of both English and Korean financial markets terminology. You have over 10 years of experience translating investment reports, analyst recommendations, and financial documents for Korean institutional investors and retail clients. You understand the nuances of financial language in both cultures and excel at making complex investment analysis accessible to Korean readers while maintaining professional accuracy. You are particularly skilled at translating technical financial terms, valuation metrics, and investment recommendations in a way that resonates with Korean investment culture and regulatory environment.",
            verbose=True,
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            role="Executive Report Writer and Korean Investment Summary Specialist",
            goal="Create concise, executive-level Korean investment reports that distill complex analysis into actionable insights for Korean clients. Transform detailed investment analysis into compact, high-impact Korean summary reports with key recommendations and price targets.",
            backstory="You are a senior financial communications specialist with 12+ years of experience writing executive summaries and client-facing investment reports for top-tier Korean investment firms. You excel at condensing complex financial analysis into clear, actionable insights that busy Korean executives and high-net-worth clients can quickly understand and act upon. Your reports are known for their clarity, precision, and ability to highlight the most critical information in a structured Korean format. You understand that Korean clients want immediate answers to 'Should I buy?', 'At what price?', and 'What are the risks?' without having to read through lengthy analysis documents. You ALWAYS write reports in Korean language using professional Korean financial terminology and cultural context.",
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            description="Research the latest stock market news and developments related to: {topic}. Focus on finding recent market movements, earnings reports, analyst ratings, company announcements, and any significant events that could impact stock prices. Include both positive and negative developments. Current year is 2025.",
            expected_output="A comprehensive list of 10 bullet points covering the most relevant and recent stock market information about {topic}, including price movements, financial news, analyst opinions, and market trends that investors should be aware of.",
            agent=self.researcher(),
            output_file="output/research_report.md"
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            description="Based on the research report about {topic}, provide a comprehensive investment analysis with specific price targets. Analyze fundamental and technical aspects, evaluate current valuation, assess risk factors, and provide clear BUY/HOLD/SELL recommendation with precise entry points, profit-taking levels, and stop-loss prices. Include both short-term trading and long-term investment perspectives with specific price ranges.",
            expected_output="A detailed investment analysis report with specific price targets including: - Executive Summary with clear BUY/HOLD/SELL recommendation - Current Price Analysis and Fair Value Estimation - BUY ZONES: Specific price ranges for optimal entry points - SELL ZONES: Target prices for profit-taking (25%, 50%, 100% gains) - STOP-LOSS: Risk management price levels - Fundamental Analysis (strengths, weaknesses, financial health) - Technical Analysis (support/resistance levels, trend analysis) - Risk Assessment with quantified risk/reward ratios - Timeline: Short-term (3-6 months) and Long-term (1-2 years) price targets - Investment Strategy: Position sizing and portfolio allocation suggestions. Format as a professional investment recommendation report with actionable price levels.",
            agent=self.investment_analyst(),
            output_file="output/investment_analysis.md"
        )

    @task
    def translation_task(self) -> Task:
        return Task(
            description="Translate the investment analysis report about {topic} from English to Korean. Maintain all financial terminology accuracy, preserve the analytical structure, and ensure the Korean version is natural and professional for Korean investors. Keep all numerical data, percentages, and recommendations exactly as in the original. Use appropriate Korean financial terminology and maintain the professional tone throughout the document.",
            expected_output="A complete Korean translation of the investment analysis report including: - All sections translated with accurate financial terminology - Preserved numerical data and recommendations - Natural Korean language flow suitable for professional investors - Maintained document structure and formatting - Professional tone appropriate for Korean financial markets",
            agent=self.translator(),
            output_file="output/investment_analysis_kr.md"
        )

    @task
    def final_report_task(self) -> Task:
        return Task(
            description="Based on the detailed Korean investment analysis report about {topic}, create a concise executive summary report for busy Korean clients. Extract and condense the most critical information including investment recommendation, key price targets, major risks, and actionable insights. Focus on what Korean clients need to know to make immediate investment decisions. Write the entire report in Korean language.",
            expected_output="A compact executive investment summary report in Korean (maximum 2-3 pages) including: - Investment recommendation summary (BUY/HOLD/SELL with confidence level) - Key price information (current price, buy zones, target price, stop-loss) - Major investment rationale (3-5 key points) - Major risk factors (3 key risks) - Investment scenarios (optimistic/base/pessimistic cases) - Portfolio allocation suggestions - Time-based action plan (short-term/long-term). Format as a professional, client-ready executive summary with clear action items. The entire report must be written in Korean language with professional Korean financial terminology and cultural context appropriate for Korean investors.",
            agent=self.report_writer(),
            output_file="output/compacted_investment_analysis_kr.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestStockCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )