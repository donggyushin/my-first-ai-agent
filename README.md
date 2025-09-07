# 📈 AI 주식 분석 에이전트 시스템

CrewAI 프레임워크를 사용한 다중 에이전트 주식 분석 및 포트폴리오 관리 시스템입니다.

## 🤖 AI Agent란?

AI Agent(AI 에이전트)는 특정 목표를 달성하기 위해 자율적으로 행동하고, 환경을 인식하며, 도구를 사용할 수 있는 AI 시스템입니다. 

### 주요 특징
- **자율성**: 인간의 개입 없이 독립적으로 작업 수행
- **반응성**: 환경 변화에 실시간으로 대응
- **능동성**: 목표 달성을 위해 주도적으로 행동
- **사회성**: 다른 에이전트와 협력하여 복잡한 작업 해결

이 프로젝트에서는 주식 분석, 투자 조언, 번역, 리포트 작성 등의 전문적인 역할을 수행하는 여러 AI 에이전트들이 협력합니다.

## 🎯 시스템 개요

### 주식 분석 크루 (Stock Crew)
1. **Research Specialist** - 최신 시장 뉴스 및 정보 수집
2. **Investment Analyst** - 투자 분석 및 구체적인 매매 타이밍 제시
3. **Translator** - 영문 분석 보고서의 전문적인 한글 번역
4. **Report Writer** - 고급 투자자를 위한 한글 요약 보고서 작성

### 포트폴리오 관리 크루 (Portfolio Crew)
1. **Portfolio Analyzer** - 고객의 현재 포지션 분석
2. **Risk Manager** - 리스크 평가 및 위험 관리 전략 수립
3. **Portfolio Advisor** - 개인화된 한글 투자 조언 제공

## 🚀 프로젝트 실행

### 환경 설정
1. 환경변수 파일(.env) 설정:
```bash
OPENAI_API_KEY="your_openai_api_key"
SERPER_API_KEY="your_serper_api_key"
```

2. 의존성 설치 및 실행:
```bash
# UV를 사용한 의존성 설치
uv sync

# 프로그램 실행
uv run python main.py
```

### 사용 방법
1. **1단계**: 분석할 주식 티커 또는 회사명 입력
2. **2단계**: AI 에이전트들이 순차적으로 분석 수행
   - 뉴스 리서치 → 투자 분석 → 한글 번역 → 요약 보고서
3. **3단계**: 개인 포트폴리오 조언 옵션 선택
   - 보유 평균 단가 입력 시 개인화된 매매 조언 제공

### 생성되는 보고서
- `research_report.md` - 최신 뉴스 및 시장 동향
- `investment_analysis.md` - 영문 상세 투자 분석
- `investment_analysis_kr.md` - 한글 투자 분석
- `compacted_investment_analysis_kr.md` - 한글 요약 보고서
- `portfolio_recommendation_kr.md` - 개인화된 포트폴리오 조언 (선택적)

## 🛠 UV 프로젝트 매니저

이 프로젝트는 **UV**를 패키지 매니저로 사용합니다. UV는 Python을 위한 빠르고 현대적인 패키지 관리 및 프로젝트 관리 도구입니다.

### UV란?

UV는 Rust로 작성된 Python 패키지 매니저로, 기존의 pip, virtualenv, poetry 등을 대체할 수 있는 올인원 도구입니다:

- **빠른 속도**: Rust로 작성되어 매우 빠른 패키지 설치 및 의존성 해결
- **통합 도구**: 가상환경, 패키지 설치, 프로젝트 관리를 하나의 도구로
- **호환성**: 기존 Python 생태계와 완벽 호환
- **간편함**: 복잡한 설정 없이 바로 사용 가능

### UV 사용법

#### 패키지 관리
```bash
# 패키지 설치
uv add requests

# 개발 의존성 설치
uv add --dev pytest

# 모든 의존성 설치
uv sync
```

#### 가상환경 관리
```bash
# 가상환경에서 스크립트 실행
uv run python main.py

# 쉘 활성화
uv shell
```

## 📁 프로젝트 구조

```
my-first-ai-agent/
├── crews/
│   ├── stock_crew.py      # 주식 분석 멀티 에이전트
│   └── portfolio_crew.py  # 포트폴리오 관리 멀티 에이전트
├── tools/
│   └── financial_tools.py # 실시간 금융 데이터 도구
├── output/                # 생성된 분석 보고서들
├── main.py               # 메인 실행 파일
└── .env                  # 환경변수 설정
```

## 🔧 기술 스택

- **CrewAI**: 멀티 에이전트 오케스트레이션 프레임워크
- **OpenAI GPT-5-mini**: 고성능 언어 모델
- **yfinance**: 실시간 금융 데이터 API
- **SerperDev**: 웹 검색 및 뉴스 수집 도구
- **UV**: Python 패키지 및 프로젝트 관리
