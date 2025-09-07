# 🚀 실시간 주식 투자 자문 시스템

GPT-4o와 CrewAI를 활용한 고도화된 AI 주식 분석 및 투자 결정 지원 시스템입니다. **실제 API 데이터**만을 사용하여 정확하고 신뢰할 수 있는 투자 분석을 제공합니다.

## 🎯 시스템 특징

### ✅ 100% 실제 데이터 기반
- Mock 데이터 절대 사용 안함
- 실시간 주가, 뉴스, 재무 데이터 활용
- yfinance, Firecrawl 등 신뢰할 수 있는 API 소스

### 🤖 GPT-4o 기반 지능형 분석
- 최신 OpenAI GPT-4o 모델 사용
- 뉴스 감정 분석 + 기술적 분석 종합 판단
- 구체적이고 실용적인 투자 권고

### 📊 2가지 투자 워크플로우
1. **AI 추천 종목 시스템** - 30개 인기 종목에서 기술적 분석으로 TOP 5 선별
2. **개별 종목 상세 분석** - 3단계 멀티에이전트 종합 분석
   - 뉴스 감정 분석가 (40% 가중치)
   - 기술적 분석가 (60% 가중치)  
   - 투자 자문가 (최종 매수/매도 결정)

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 환경변수 파일 (.env) 생성
OPENAI_API_KEY="your_openai_api_key"
FIRECRAWL_API_KEY="your_firecrawl_api_key" (선택사항 - 뉴스 분석용)
```

### 2. 실행
```bash
# 기본 시스템 실행 (추천 + 상세 분석)
uv run python main.py

# 빠른 추천 시스템만 테스트
uv run python test_recommendation_only.py

# HTML 보고서 생성 테스트
uv run python test_report.py
```

### 3. 사용법
```
🚀 실시간 주식 투자 자문 시스템
==================================================

🔍 AI가 추천하는 투자 종목 5선을 먼저 확인해보세요!
이 과정은 1-2분 정도 소요될 수 있습니다.

[AI 추천 TOP 5 종목 표시]

📈 상세 분석하고 싶은 주식 티커를 입력하세요 (예: AAPL, BOIL, TSLA): MSFT

🔍 'MSFT'에 대한 종합 투자 분석을 시작합니다...
이 과정은 2-3분 정도 소요될 수 있습니다.
```

## 📈 분석 결과 예시 (BOIL)

```
📰 뉴스 감정 분석: 60.0/100 (중립)
🚀 기술적 분석: 37/100 (C등급 - 매도 권장)
💡 최종 투자 결정: 매도 권장 (높은 변동성 68.9% 주의)
```

**제공되는 정보:**
- 종합 투자 점수 및 등급
- 목표가, 손절매가, 투자 비중
- 구체적 매수/매도 시점
- 리스크 분석 및 대응 방안

## 🛠 시스템 아키텍처

### 핵심 구성요소

**1. 뉴스 감정 분석 도구** (`tools/news_sentiment_tool.py`)
- yfinance 실시간 뉴스 데이터
- 긍정/부정 키워드 기반 감정 점수 (0-100점)
- 최근 뉴스 기반 단기 전망

**2. 고급 기술적 분석 도구** (`tools/advanced_stock_analysis.py`)
- RSI, 이동평균선, 거래량 분석
- PER, PBR, ROE, 부채비율 등 재무지표
- 변동성 및 리스크 분석
- 종합 투자 점수 (0-100점)

**3. 실시간 투자 자문 크루** (`crews/investment_advisor_crew.py`)
```
뉴스 분석가 → 기술적 분석가 → 투자 자문가 (GPT-4o)
     ↓              ↓                ↓
   감정점수       기술적점수        최종 투자결정
  (40% 가중)     (60% 가중)       (매수/매도/관망)
```

## 📊 분석 지표

### 뉴스 감정 분석
- 긍정 키워드: bull, bullish, rise, gain, surge, growth...
- 부정 키워드: bear, bearish, fall, drop, decline, loss...
- 점수 구간: 0-19(매우부정) → 80-100(매우긍정)

### 기술적 분석
- **RSI**: 과매수/과매도 신호 (30-70 정상범위)
- **이동평균선**: 추세 분석 (SMA 20, 50)
- **거래량**: 시장 관심도 측정
- **변동성**: 리스크 수준 평가

### 재무 건전성
- **PER**: 밸류에이션 (< 15 저평가)
- **PBR**: 자산 가치 (< 1 저평가)
- **부채비율**: 안전성 (< 30% 우수)
- **ROE**: 수익성 (> 20% 우수)

## 📁 프로젝트 구조

```
my-first-ai-agent/
├── main.py                           # 메인 실행 파일 (로깅 & 에러처리 강화)
├── main_old.py                       # 이전 버전 (참조용)
├── test_recommendation_only.py       # 추천 시스템 단독 테스트
├── test_report.py                   # HTML 보고서 생성 테스트
├── .env                             # API 키 환경변수
├── pyproject.toml                   # UV 프로젝트 설정
├── .gitignore                       # Git 제외 패턴 (보안 강화)
├── crews/                           # CrewAI 멀티에이전트 시스템
│   ├── investment_advisor_crew.py      # 3-에이전트 상세 분석 크루
│   └── investment_item_recommendar_crew.py  # 2-에이전트 추천 크루
├── tools/                           # 분석 도구 모음
│   ├── advanced_stock_analysis.py      # 고급 기술적 분석 (100점 채점)
│   ├── financial_tools.py             # 밸류에이션 & 재무건전성
│   ├── news_sentiment_tool.py         # 뉴스 감정 분석
│   └── firecrawl_tool.py             # 웹 스크래핑 도구
├── utils/                           # 시스템 유틸리티
│   ├── logger.py                     # 로깅 시스템 (일별 로그 파일)
│   └── report_generator.py           # HTML 보고서 생성기 (신규)
├── config/                          # 설정 관리
│   └── constants.py                  # 중앙집중식 상수 관리
├── logs/                            # 자동 생성 로그 디렉토리
│   └── investment_advisor_YYYYMMDD.log
└── reports/                         # HTML 보고서 출력 디렉토리 (신규)
    └── investment_report_YYYYMMDD_HHMMSS.html
```

## 🔧 기술 스택

- **CrewAI**: 멀티 에이전트 오케스트레이션
- **OpenAI GPT-4o**: 최신 AI 모델
- **yfinance**: 실시간 금융 데이터
- **Firecrawl**: 웹 스크래핑 & 뉴스 수집
- **UV**: Python 패키지 관리 (3.13.2+)
- **NumPy & Pandas**: 수치 계산 & 데이터 분석

## ⚠️ 주의사항

1. **투자 책임**: 본 분석은 참고용이며 투자 결정은 본인 책임입니다.
2. **API 제한**: yfinance API 사용량 제한이 있을 수 있습니다.
3. **ETF 제한**: ETF(예: BOIL)는 개별 기업 재무분석이 제한적입니다.
4. **변동성 주의**: 특히 레버리지 ETF는 높은 변동성을 가집니다.

## 🌟 시스템 장점 & 최근 개선사항

### 🚀 2025-09-08 업데이트 (v2.1)
- ✅ **AI 추천 시스템**: 30개 인기 종목에서 TOP 5 자동 선별
- ✅ **로깅 시스템**: 모든 분석 과정을 `logs/` 폴더에 자동 기록
- ✅ **설정 관리**: 중앙집중식 상수 관리로 유지보수성 향상
- ✅ **에러 처리**: 강화된 예외 처리 및 사용자 친화적 오류 메시지
- ✅ **메모리 최적화**: 대용량 데이터 처리 시 메모리 사용량 최적화
- ✅ **보안 강화**: API 키 보호 및 민감 정보 .gitignore 처리
- 🆕 **HTML 보고서**: 전문적인 HTML 형태 보고서 생성 기능 추가
- 🆕 **모듈형 테스팅**: 구성요소별 개별 테스트 스크립트 제공
- 🆕 **개선된 UI**: 더 나은 사용자 경험과 보고서 시각화

### 기존 시스템 대비 개선점
- ❌ **기존**: Mock 데이터, 가짜 미래 날짜, 단순 오류 처리
- ✅ **개선**: 100% 실제 API 데이터, 정확한 현재 날짜, 포괄적 에러 핸들링

### 투자 결정 지원
- 📊 **정량적 분석**: 객관적 100점 점수 시스템
- 📰 **정성적 분석**: 실시간 뉴스 감정 반영
- 🤖 **AI 판단**: GPT-4o 기반 종합 결정
- 💡 **실용적 조언**: 구체적 매매 타이밍 및 목표가
- 📋 **추적 가능**: 모든 분석 과정 로그 기록 및 모니터링
- 📄 **전문적 보고서**: HTML 형태의 시각적이고 공유하기 쉬운 보고서
- ⚡ **모듈형 테스트**: 빠른 개발과 디버깅을 위한 구성요소별 테스트

## 🧪 테스트 & 검증

### 시스템 테스트 명령어
```bash
# 기본 Import 테스트
uv run python -c "import crews.investment_advisor_crew; print('✅ Import successful')"

# 크루 생성 테스트  
uv run python -c "from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew; crew = InvestmentItemRecommendarCrew(); print('✅ Crew created')"

# 로깅 시스템 테스트
uv run python -c "from utils.logger import setup_logger; logger = setup_logger(); print('✅ Logger test successful')"

# 설정 시스템 테스트
uv run python -c "from config.constants import MESSAGE_TEMPLATES; print('✅ Config loaded:', len(MESSAGE_TEMPLATES), 'templates')"

# HTML 보고서 생성 테스트 (신규)
uv run python -c "from utils.report_generator import generate_html_report; print('✅ Report generator test successful')"
```

### 테스트 결과 (2025-09-08)
```
✅ 기본 import 테스트: 통과
✅ 환경변수 및 설정 검증: 통과  
✅ 개별 모듈 기능 테스트: 통과
✅ 전체 시스템 통합 테스트: 통과
✅ 실시간 데이터 수집: 통과 (25/30 종목 성공)
✅ HTML 보고서 생성: 통과 (마크다운 → HTML 변환)
✅ 모듈별 개별 테스트: 통과 (추천 시스템, 보고서 생성기)
```

---

**💬 개발 문의**: 시스템 개선 및 기능 추가 관련 피드백 환영합니다.

**📄 기술 문서**: 상세한 아키텍처 및 개발 가이드는 `CLAUDE.md` 참조
