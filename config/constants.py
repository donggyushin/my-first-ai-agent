# 투자 자문 시스템 상수 정의

# 기술적 분석 점수 가중치
TECHNICAL_ANALYSIS_WEIGHTS = {
    'RSI_WEIGHT': 30,
    'MOVING_AVERAGE_WEIGHT': 25,
    'VOLUME_WEIGHT': 20,
    'MOMENTUM_WEIGHT': 25
}

# 투자 의사결정 가중치
DECISION_WEIGHTS = {
    'NEWS_SENTIMENT_WEIGHT': 0.4,
    'TECHNICAL_ANALYSIS_WEIGHT': 0.6
}

# RSI 임계값
RSI_THRESHOLDS = {
    'OVERSOLD': 30,
    'OVERBOUGHT': 70,
    'OPTIMAL_MIN': 40,
    'OPTIMAL_MAX': 60
}

# 투자 등급 기준
INVESTMENT_GRADES = {
    'A_PLUS': {'min': 80, 'label': 'A+ (강한 매수)'},
    'A': {'min': 70, 'label': 'A (매수)'},
    'B_PLUS': {'min': 60, 'label': 'B+ (약간 매수)'},
    'B': {'min': 50, 'label': 'B (중립)'},
    'C_PLUS': {'min': 40, 'label': 'C+ (약간 매도)'},
    'C': {'min': 30, 'label': 'C (매도)'},
    'D': {'min': 0, 'label': 'D (강한 매도)'}
}

# 인기 주식 티커 목록
POPULAR_TICKERS = [
    # Tech giants
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
    # Financial
    'JPM', 'BAC', 'WFC', 'GS', 'MS',
    # Healthcare
    'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK',
    # Consumer
    'KO', 'PEP', 'WMT', 'HD', 'DIS',
    # Energy
    'XOM', 'CVX', 'COP',
    # Other popular
    'V', 'MA', 'NFLX', 'AMD', 'INTC'
]

# 분석 기간 설정
ANALYSIS_PERIODS = {
    'NEWS_DAYS': 7,
    'TECHNICAL_MONTHS': 3,
    'ADVANCED_MONTHS': 6
}

# 메시지 템플릿
MESSAGE_TEMPLATES = {
    'SYSTEM_START': "🚀 실시간 주식 투자 자문 시스템",
    'RECOMMENDATION_START': "🔍 AI가 추천하는 투자 종목 5선을 먼저 확인해보세요!",
    'INDIVIDUAL_ANALYSIS': "개별 종목 상세 분석",
    'TICKER_INPUT_PROMPT': "📈 상세 분석하고 싶은 주식 티커를 입력하세요 (예: AAPL, BOIL, TSLA): ",
    'ANALYSIS_COMPLETE': "✅ 종합 투자 분석이 완료되었습니다!",
    'DISCLAIMER': "⚠️  면책조항: 본 분석은 투자 참고용이며, 최종 투자 결정은 본인의 책임입니다."
}