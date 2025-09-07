from crewai.project import CrewBase, agent, crew, task
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool

@CrewBase
class PortfolioCrew():

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def portfolio_analyzer(self) -> Agent:
        return Agent(
            role="Portfolio Management Specialist",
            goal="Analyze client's current position and provide actionable recommendations for additional purchases, profit-taking, or stop-loss decisions based on current average cost and investment analysis reports",
            backstory="You are a senior portfolio manager with 15+ years of experience managing client portfolios and making tactical allocation decisions. You excel at analyzing client positions relative to current market conditions and investment analysis to provide clear buy/sell/hold recommendations. You understand the importance of cost basis, risk management, and position sizing in portfolio optimization.",
            verbose=True,
            tools=[
                FileReadTool(file_path="output/research_report.md"),
                FileReadTool(file_path="output/investment_analysis.md"),
                FileReadTool(file_path="output/investment_analysis_kr.md"),
                FileReadTool(file_path="output/compacted_investment_analysis_kr.md")
            ]
        )

    @agent
    def risk_manager(self) -> Agent:
        return Agent(
            role="Risk Management Specialist", 
            goal="Assess portfolio risk and provide risk-adjusted recommendations based on client's current position and market analysis",
            backstory="You are a quantitative risk management expert with deep experience in portfolio risk assessment. You specialize in evaluating position risk, calculating risk-reward ratios, and providing recommendations that balance potential returns with downside protection. You always consider position sizing, diversification, and risk management principles.",
            verbose=True,
            tools=[
                FileReadTool(file_path="output/research_report.md"),
                FileReadTool(file_path="output/investment_analysis.md"),
                FileReadTool(file_path="output/investment_analysis_kr.md"),
                FileReadTool(file_path="output/compacted_investment_analysis_kr.md")
            ]
        )

    @agent
    def portfolio_advisor(self) -> Agent:
        return Agent(
            role="Client Portfolio Advisor",
            goal="Synthesize analysis and provide clear, actionable Korean recommendations for clients regarding their current stock position",
            backstory="You are a senior client advisor who specializes in translating complex portfolio analysis into clear, actionable advice for Korean clients. You have over 10 years of experience working with Korean investors and understand their investment preferences and risk tolerance. You always provide recommendations in Korean with clear reasoning and specific action steps.",
            verbose=True,
            tools=[
                FileReadTool(file_path="output/investment_analysis_kr.md"),
                FileReadTool(file_path="output/compacted_investment_analysis_kr.md")
            ]
        )

    @task
    def analyze_current_position(self) -> Task:
        return Task(
            description="Analyze the client's current position in {ticker} with average cost of ${avg_cost} USD. Use the FileReadTool to read and analyze all available reports: output/research_report.md, output/investment_analysis.md, output/investment_analysis_kr.md, and output/compacted_investment_analysis_kr.md. Compare current market price with client's average cost and assess the position's performance.",
            expected_output="A comprehensive analysis of the client's current position including unrealized P&L, position performance metrics, comparison with current market conditions, and synthesis of investment recommendations from all available reports.",
            agent=self.portfolio_analyzer()
        )

    @task
    def assess_portfolio_risk(self) -> Task:
        return Task(
            description="Based on the position analysis and by reading the investment reports using FileReadTool (output/research_report.md, output/investment_analysis.md), assess the risk profile of maintaining, increasing, or decreasing the position in {ticker}. Consider the client's current cost basis of ${avg_cost} and provide risk-adjusted scenarios for different actions.",
            expected_output="Risk assessment covering downside risk, upside potential, risk-reward ratios for different actions (buy more, hold, sell), recommended position sizing based on current analysis, and specific risk management strategies.",
            agent=self.risk_manager()
        )

    @task
    def provide_portfolio_recommendation(self) -> Task:
        return Task(
            description="Based on the position analysis and risk assessment, and by reading the Korean reports using FileReadTool (output/investment_analysis_kr.md, output/compacted_investment_analysis_kr.md), provide clear recommendations for the client's {ticker} position with average cost ${avg_cost}. Consider all available analysis reports and provide specific action recommendations in Korean.",
            expected_output="Clear Korean recommendations including: 1) 추천 행동 (추가매수/보유/손절), 2) 구체적인 실행 계획, 3) 리스크 관리 방안, 4) 목표 수익률 및 손절선, 5) 포지션 사이즈 조절 제안, 6) 평균 단가 대비 현재 상황 분석. Format as actionable advice for Korean investors with specific price levels and timelines.",
            agent=self.portfolio_advisor(),
            output_file="output/portfolio_recommendation_kr.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Portfolio Management Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )