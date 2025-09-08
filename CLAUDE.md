# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
- `uv run python main.py` - Run the main investment advisory system (auto-analyzes top 5 recommended stocks)
- `uv run python report_single_ticker.py` - Interactive single ticker analysis with user input
- `uv run python test_recommendation_only.py` - Test only the recommendation system (faster testing)
- `uv run python test_report.py` - Test HTML report generation functionality
- `uv sync` - Install/update dependencies using UV package manager 
- `uv add <package>` - Add new dependencies to pyproject.toml

### Testing Commands
- `uv run python -c "import crews.investment_advisor_crew; print('✅ Import successful')"` - Test basic imports
- `uv run python -c "from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew; crew = InvestmentItemRecommendarCrew(); print('✅ Crew created')"` - Test crew instantiation
- `uv run python -c "from utils.logger import setup_logger; logger = setup_logger(); print('✅ Logger test successful')"` - Test logging system
- `uv run python -c "from config.constants import MESSAGE_TEMPLATES; print('✅ Config loaded:', len(MESSAGE_TEMPLATES), 'templates')"` - Test configuration system
- `uv run python -c "from utils.report_generator import generate_html_report; print('✅ Report generator test successful')"` - Test HTML report generation

## Architecture Overview

This is a multi-agent AI investment advisory system built with CrewAI, GPT-4o, and real-time financial data APIs. The system provides three main execution modes:

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
5. **NEW**: Optional HTML report generation for better visualization and sharing

### 3. Interactive Single Ticker Analysis (`report_single_ticker.py`)
A user-interactive mode for analyzing specific stocks:
- **User Input**: Interactive ticker input with validation
- **Real-time Analysis**: On-demand analysis of user-specified stocks
- **Continuous Operation**: Loop-based interface for multiple analyses
- **Exit Options**: 'q' or 'quit' commands to terminate
- **HTML Reports**: Automatic report generation for each analysis

### Alternative Execution Modes
- **`test_recommendation_only.py`**: Quick testing of recommendation system only
- **`test_report.py`**: Testing HTML report generation with sample data
- **`main_old.py`**: Previous version maintained for reference

## Key Technical Components

### Financial Data Tools (`tools/`)
- **financial_tools.py**: Real-time valuation (PER, PBR, PSR) and financial health scoring
- **advanced_stock_analysis.py**: Technical indicators, comprehensive scoring system (0-100 points)
- **news_sentiment_tool.py**: News sentiment analysis with keyword-based scoring
- **firecrawl_tool.py**: Web scraping tool for news and financial content

### System Infrastructure (`utils/`, `config/`)
- **utils/logger.py**: Comprehensive logging system with daily log files and structured error tracking
- **utils/report_generator.py**: HTML report generation with markdown-to-HTML conversion and professional styling
- **config/constants.py**: Centralized configuration management for weights, thresholds, and templates
- Automated log rotation and error tracking for production monitoring

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

## Error Handling & Monitoring Strategy

The system includes comprehensive error handling and monitoring:
- **Graceful Degradation**: API failures are handled gracefully (e.g., if recommendation system fails, individual analysis continues)
- **Input Validation**: Invalid tickers are caught with helpful error messages and suggestions
- **Security**: API keys are validated at startup; sensitive information is protected via environment variables
- **Logging & Monitoring**: All operations are logged to `logs/` directory with detailed error tracking and stack traces
- **ETF/Fund Handling**: ETF/mutual fund limitations are explicitly handled with user-friendly explanations
- **Data Resilience**: Missing financial data is handled gracefully with "N/A" indicators and alternative data sources
- **Memory Management**: Automatic cleanup of large data objects to prevent memory leaks during batch processing

## Korean Language Interface

The system uses Korean for user interface and reports while maintaining English variable names and technical terms in code. Reports include both Korean explanations and English technical indicators for clarity.

## Project Structure

```
my-first-ai-agent/
├── main.py                     # Main entry point - auto-analyzes top 5 recommended stocks
├── report_single_ticker.py     # Interactive single ticker analysis with user input
├── main_old.py                 # Previous version for reference
├── test_recommendation_only.py # Quick recommendation system testing
├── test_report.py             # HTML report generation testing
├── .env                       # Environment variables (API keys)
├── pyproject.toml            # UV package management
├── CLAUDE.md                 # This file
├── README.md                 # Project documentation
├── .gitignore                # Git ignore patterns
├── crews/                    # CrewAI agent definitions
│   ├── __init__.py
│   ├── investment_advisor_crew.py      # 3-agent analysis crew
│   └── investment_item_recommendar_crew.py  # 2-agent recommendation crew
├── tools/                    # Analysis tools and data sources
│   ├── __init__.py
│   ├── advanced_stock_analysis.py     # Technical analysis engine
│   ├── financial_tools.py            # Valuation and health metrics
│   ├── news_sentiment_tool.py        # News sentiment analysis
│   └── firecrawl_tool.py            # Web scraping utilities
├── utils/                    # System utilities
│   ├── __init__.py
│   ├── logger.py                     # Comprehensive logging system
│   └── report_generator.py           # HTML report generation (NEW)
├── config/                   # Configuration management
│   ├── __init__.py
│   └── constants.py                  # Centralized constants and settings
├── logs/                     # Generated log files (AUTO-CREATED)
│   └── investment_advisor_YYYYMMDD.log
└── reports/                  # Generated HTML reports (AUTO-CREATED)
    └── investment_report_YYYYMMDD_HHMMSS.html
```

## Recent Improvements (2025-09-08)

### 🔧 System Enhancements
1. **Logging System**: Added comprehensive logging with daily rotation and error tracking
2. **Configuration Management**: Centralized constants and settings in `config/` module
3. **Memory Optimization**: Improved memory management for batch stock processing
4. **Security**: Enhanced API key protection and input validation
5. **Error Handling**: Robust error handling with user-friendly messages and detailed logging
6. **HTML Report Generation**: Professional HTML reports with markdown conversion and styling
7. **Testing Suite**: Dedicated test scripts for different components

### 🧪 Testing Infrastructure
- Complete test coverage for all modules and integrations
- Automated validation of imports, configurations, and core functionalities
- End-to-end system testing with real data sources
- Performance and memory usage validation
- **NEW**: Isolated testing scripts (`test_recommendation_only.py`, `test_report.py`)
- **NEW**: HTML report generation testing with sample data

### 📊 Production Readiness
- Structured logging for monitoring and debugging
- Graceful error handling and recovery mechanisms
- Resource cleanup and memory management
- Security best practices implementation
- **NEW**: Professional HTML report output for sharing and presentation
- **NEW**: Modular testing approach for faster development cycles

### 📋 HTML Report Generation Features
- **Markdown to HTML Conversion**: Clean conversion with proper styling
- **Professional Layout**: CSS styling with proper typography and spacing
- **Responsive Design**: Works well on different screen sizes
- **Data Visualization**: Tables and structured data display
- **Export Ready**: Easily shareable HTML files with embedded styles
- **Auto-Generated Filenames**: Timestamped files in `reports/` directory