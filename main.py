import dotenv

dotenv.load_dotenv()

from crewai.project import CrewBase, agent, crew, task
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent

from crewai_tools import SerperDevTool, tool

@tool
def calculate_valuation_metrics(current_price: float, eps: float, book_value: float, revenue: float, market_cap: float) -> str:
    """
    Calculate key valuation metrics for investment analysis.
    
    Args:
        current_price: Current stock price
        eps: Earnings per share (annual)
        book_value: Book value per share
        revenue: Annual revenue
        market_cap: Market capitalization
        
    Returns:
        Formatted string with PE ratio, P/B ratio, and P/S ratio analysis
    """
    try:
        # PE Ratio
        pe_ratio = current_price / eps if eps > 0 else "N/A (negative earnings)"
        
        # Price-to-Book Ratio
        pb_ratio = current_price / book_value if book_value > 0 else "N/A"
        
        # Price-to-Sales Ratio (approximate)
        ps_ratio = market_cap / revenue if revenue > 0 else "N/A"
        
        # Valuation assessment
        valuation_assessment = ""
        if isinstance(pe_ratio, float):
            if pe_ratio < 15:
                valuation_assessment = "Potentially undervalued (low PE)"
            elif pe_ratio > 30:
                valuation_assessment = "Potentially overvalued (high PE)"
            else:
                valuation_assessment = "Fairly valued"
        
        result = f"""
VALUATION METRICS ANALYSIS:
==========================
• PE Ratio: {pe_ratio}
• P/B Ratio: {pb_ratio}
• P/S Ratio: {ps_ratio}
• Assessment: {valuation_assessment}

INTERPRETATION:
- PE Ratio < 15: Often considered undervalued
- PE Ratio 15-25: Generally fair value range
- PE Ratio > 25: May indicate overvaluation or high growth expectations
"""
        return result
    except Exception as e:
        return f"Error calculating valuation metrics: {str(e)}"

@tool  
def calculate_financial_health_score(debt_to_equity: float, current_ratio: float, roe: float, profit_margin: float) -> str:
    """
    Calculate a comprehensive financial health score based on key financial ratios.
    
    Args:
        debt_to_equity: Debt-to-equity ratio
        current_ratio: Current assets / Current liabilities
        roe: Return on Equity (as percentage)
        profit_margin: Net profit margin (as percentage)
        
    Returns:
        Financial health score and detailed analysis
    """
    try:
        score = 0
        max_score = 100
        analysis = []
        
        # Debt-to-Equity Analysis (25 points)
        if debt_to_equity < 0.3:
            score += 25
            analysis.append("✓ Excellent debt management (D/E < 0.3)")
        elif debt_to_equity < 0.6:
            score += 20
            analysis.append("✓ Good debt management (D/E < 0.6)")
        elif debt_to_equity < 1.0:
            score += 15
            analysis.append("⚠ Moderate debt levels (D/E < 1.0)")
        else:
            score += 5
            analysis.append("⚠ High debt levels (D/E ≥ 1.0)")
        
        # Current Ratio Analysis (25 points)
        if current_ratio > 2.0:
            score += 25
            analysis.append("✓ Strong liquidity (Current Ratio > 2.0)")
        elif current_ratio > 1.5:
            score += 20
            analysis.append("✓ Good liquidity (Current Ratio > 1.5)")
        elif current_ratio > 1.0:
            score += 15
            analysis.append("⚠ Adequate liquidity (Current Ratio > 1.0)")
        else:
            score += 5
            analysis.append("⚠ Poor liquidity (Current Ratio ≤ 1.0)")
        
        # ROE Analysis (25 points)
        if roe > 20:
            score += 25
            analysis.append("✓ Excellent profitability (ROE > 20%)")
        elif roe > 15:
            score += 20
            analysis.append("✓ Good profitability (ROE > 15%)")
        elif roe > 10:
            score += 15
            analysis.append("⚠ Moderate profitability (ROE > 10%)")
        else:
            score += 5
            analysis.append("⚠ Low profitability (ROE ≤ 10%)")
        
        # Profit Margin Analysis (25 points)
        if profit_margin > 20:
            score += 25
            analysis.append("✓ Excellent profit margins (>20%)")
        elif profit_margin > 10:
            score += 20
            analysis.append("✓ Good profit margins (>10%)")
        elif profit_margin > 5:
            score += 15
            analysis.append("⚠ Moderate profit margins (>5%)")
        else:
            score += 5
            analysis.append("⚠ Low profit margins (≤5%)")
        
        # Overall assessment
        if score >= 85:
            overall = "EXCELLENT - Strong financial position"
        elif score >= 70:
            overall = "GOOD - Solid financial health"
        elif score >= 55:
            overall = "FAIR - Some areas of concern"
        else:
            overall = "POOR - Significant financial risks"
        
        result = f"""
FINANCIAL HEALTH ANALYSIS:
==========================
Overall Score: {score}/{max_score} - {overall}

DETAILED BREAKDOWN:
{chr(10).join(analysis)}

INVESTMENT IMPLICATIONS:
• Score 85-100: Low financial risk, suitable for conservative investors
• Score 70-84: Moderate risk, good for balanced portfolios
• Score 55-69: Higher risk, requires careful monitoring
• Score <55: High risk, suitable only for risk-tolerant investors
"""
        return result
    except Exception as e:
        return f"Error calculating financial health score: {str(e)}"

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
            tools=[calculate_valuation_metrics, calculate_financial_health_score]
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