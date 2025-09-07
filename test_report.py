#!/usr/bin/env python3
"""
보고서 생성 기능 테스트 스크립트
"""

from utils.report_generator import generate_html_report
from datetime import datetime

def test_report_generation():
    """테스트용 보고서 생성"""
    
    # 테스트 데이터 생성
    test_recommendations = [
        {
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'score': 85.5,
            'current_price': 175.25,
            'rsi': 45.2
        },
        {
            'ticker': 'MSFT',
            'name': 'Microsoft Corporation',
            'score': 78.3,
            'current_price': 332.89,
            'rsi': 52.1
        },
        {
            'ticker': 'GOOGL',
            'name': 'Alphabet Inc.',
            'score': 72.8,
            'current_price': 138.45,
            'rsi': 38.9
        }
    ]
    
    test_analysis_results = [
        {
            'ticker': 'AAPL',
            'name': 'Apple Inc.',
            'recommendation_score': 85.5,
            'current_price': 175.25,
            'rsi': 45.2,
            'analysis_result': '''# 최종 투자 결정 보고서: AAPL

## 📊 종합 분석 결과
- **최종 투자 점수**: 85/100 (뉴스 감정: 34점 + 기술적 분석: 51점)
- **투자 권고**: 매수
- **신뢰도**: 높음

## 🎯 투자 전략
- **추천 투자 비중**: 포트폴리오의 15%
- **목표 가격**: $185 (상승 여력: 5.6%)
- **손절매 가격**: $165 (하락 위험: 5.8%)
- **투자 기간**: 중기

## ⚖️ 리스크 분석
- **주요 리스크**: 중국 시장 의존도, 공급망 차질, 경쟁 심화
- **리스크 수준**: 보통
- **대응 방안**: 분산투자, 손절매 준수

## 💡 핵심 투자 포인트
1. **매수 이유**: 견고한 재무구조와 혁신적 제품 포트폴리오
2. **주의사항**: 고평가 구간에서의 투자
3. **모니터링 지표**: 아이폰 판매량, 서비스 수익 성장''',
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'ticker': 'MSFT',
            'name': 'Microsoft Corporation',
            'recommendation_score': 78.3,
            'current_price': 332.89,
            'rsi': 52.1,
            'analysis_result': '''# 최종 투자 결정 보고서: MSFT

## 📊 종합 분석 결과
- **최종 투자 점수**: 78/100 (뉴스 감정: 31점 + 기술적 분석: 47점)
- **투자 권고**: 매수
- **신뢰도**: 높음

## 🎯 투자 전략
- **추천 투자 비중**: 포트폴리오의 12%
- **목표 가격**: $350 (상승 여력: 5.1%)
- **손절매 가격**: $310 (하락 위험: 6.9%)
- **투자 기간**: 장기

## ⚖️ 리스크 분석
- **주요 리스크**: 클라우드 경쟁 심화, 규제 위험, 경기 둔화
- **리스크 수준**: 낮음
- **대응 방안**: 장기 보유, 정기 매수

## 💡 핵심 투자 포인트
1. **매수 이유**: Azure 성장세와 AI 기술 선도
2. **주의사항**: 밸류에이션 부담
3. **모니터링 지표**: Azure 성장률, AI 서비스 매출''',
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'ticker': 'GOOGL',
            'name': 'Alphabet Inc.',
            'recommendation_score': 72.8,
            'current_price': 138.45,
            'rsi': 38.9,
            'analysis_result': '분석 실패: API 호출 제한 초과',
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': True
        }
    ]
    
    try:
        # 보고서 생성
        report_path = generate_html_report(test_analysis_results, test_recommendations)
        print(f"✅ 테스트 보고서 생성 성공!")
        print(f"📁 보고서 위치: {report_path}")
        
        # 브라우저에서 열기 시도
        import webbrowser
        webbrowser.open(f'file://{report_path}')
        print("🚀 브라우저에서 테스트 보고서를 열었습니다!")
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 보고서 생성 실패: {str(e)}")
        return False

if __name__ == "__main__":
    print("📄 보고서 생성 기능 테스트 시작...")
    print("=" * 50)
    
    success = test_report_generation()
    
    print("=" * 50)
    if success:
        print("✅ 모든 테스트가 성공적으로 완료되었습니다!")
    else:
        print("❌ 테스트 중 오류가 발생했습니다.")