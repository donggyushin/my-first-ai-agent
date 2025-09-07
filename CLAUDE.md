# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
- `uv run python main.py` - Run the main investment advisory system
- `uv sync` - Install/update dependencies using UV package manager 
- `uv add <package>` - Add new dependencies to pyproject.toml

### Testing Commands
- `uv run python -c "import crews.investment_advisor_crew; print('✅ Import successful')"` - Test basic imports
- `uv run python -c "from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew; crew = InvestmentItemRecommendarCrew(); print('✅ Crew created')"` - Test crew instantiation

## Architecture Overview

This is a multi-agent AI investment advisory system built with CrewAI, GPT-4o, and real-time financial data APIs. The system provides two main workflows:

### 1. Investment Item Recommender Crew (`crews/investment_item_recommendar_crew.py`)
A sequential 2-agent system that:
- **Stock Researcher Agent**: Collects 20+ popular US stock tickers with basic info (price, volume, market cap)
- **Technical Analyst Agent**: Performs technical analysis (RSI, moving averages, volume, momentum) and selects top 5 stocks with scores

### 2. Individual Stock Analysis Crew (`crews/investment_advisor_crew.py`)
A sequential 3-agent system for detailed single-stock analysis:
- **News Sentiment Analyst**: Analyzes recent news sentiment (30% weight in final decision)
- **Technical Analyst**: Comprehensive technical and financial analysis (70% weight)
- **Investment Advisor**: Makes final buy/sell/hold recommendation with specific price targets

### Main Execution Flow (`main.py`)
1. First runs the Investment Item Recommender to show top 5 AI-recommended stocks
2. Then prompts user for detailed analysis of a specific ticker
3. Runs the Individual Stock Analysis crew for the chosen ticker
4. Outputs comprehensive investment report with specific recommendations

## Key Technical Components

### Financial Data Tools (`tools/`)
- **financial_tools.py**: Real-time valuation (PER, PBR, PSR) and financial health scoring
- **advanced_stock_analysis.py**: Technical indicators, comprehensive scoring system (0-100 points)
- **news_sentiment_tool.py**: News sentiment analysis with keyword-based scoring

### Data Sources
- **yfinance**: Primary source for real-time stock data, financial ratios, price history
- **Firecrawl**: Web scraping for news sentiment analysis and financial content
- All analysis uses real API data, no mock/synthetic data

### Technical Analysis Methodology
The system uses a 100-point scoring system combining:
- RSI analysis (30 points): Optimal range 30-70, penalties for extreme values
- Moving average trends (25 points): Price above SMA20 and SMA50 indicates strength
- Volume analysis (20 points): Recent volume vs historical average
- Price momentum (25 points): 20-day price change percentage

### Agent Communication Pattern
Agents pass structured data between each other:
- Stock lists as JSON arrays with ticker, name, price, volume, marketCap
- Technical analysis results as JSON with scores, indicators, and metrics
- Final recommendations in formatted text reports

## Environment Setup

Required environment variables in `.env`:
- `OPENAI_API_KEY`: For GPT-4o model access
- `FIRECRAWL_API_KEY`: For web scraping (optional, used for news analysis)

## Dependencies Management

The project uses UV for Python package management with Python 3.13.2+. Key dependencies:
- `crewai>=0.177.0` - Multi-agent orchestration framework
- `openai>=1.106.1` - GPT-4o model access
- `yfinance>=0.2.65` - Real-time financial data
- `pandas>=2.2.0` - Data manipulation for technical analysis
- `numpy>=2.3.2` - Numerical computations

## Investment Analysis Scoring

### Financial Health Scoring (0-100):
- Debt-to-equity ratio (25 pts): <30% excellent, >100% concerning
- Current ratio (25 pts): >2.0 strong liquidity, <1.0 concerning
- ROE (25 pts): >20% excellent profitability
- Profit margins (25 pts): >20% excellent, <5% concerning

### Technical Analysis Scoring (0-100):
Combines multiple technical indicators with specific point allocations and thresholds for objective stock evaluation.

## Error Handling Strategy

The system includes comprehensive error handling:
- API failures gracefully degrade (e.g., if recommendation system fails, individual analysis still works)
- Invalid tickers are caught and reported with helpful messages
- ETF/mutual fund limitations are explicitly handled and explained to users
- Missing financial data is handled gracefully with "N/A" indicators

## Korean Language Interface

The system uses Korean for user interface and reports while maintaining English variable names and technical terms in code. Reports include both Korean explanations and English technical indicators for clarity.