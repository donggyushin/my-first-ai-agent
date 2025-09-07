#!/usr/bin/env python3
"""
추천 시스템만 테스트하는 스크립트
"""

import dotenv
import sys
import json
import re
from utils.logger import setup_logger, log_analysis_start, log_analysis_complete, log_error

dotenv.load_dotenv()
logger = setup_logger()

def test_recommendation_system():
    """추천 시스템만 테스트"""
    from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew
    from config.constants import MESSAGE_TEMPLATES
    
    print(MESSAGE_TEMPLATES['SYSTEM_START'])
    print("=" * 50)
    print("\n🧪 추천 시스템 단독 테스트 시작...")
    print("이 과정은 1-2분 정도 소요될 수 있습니다.\n")
    
    try:
        log_analysis_start(logger, "ALL", "투자종목추천")
        
        # 추천 크루 실행
        recommendar_crew = InvestmentItemRecommendarCrew()
        recommendation_result = recommendar_crew.crew().kickoff()
        
        log_analysis_complete(logger, "ALL", "투자종목추천", True)
        
        print("\n" + "="*60)
        print("✅ AI 추천 투자 종목 분석 완료!")
        print("="*60)
        
        # 결과 출력
        print(f"\n📊 추천 시스템 원본 결과:")
        print("-" * 40)
        print(f"결과 타입: {type(recommendation_result)}")
        print(f"결과 길이: {len(str(recommendation_result))}")
        print("\n원본 결과:")
        print(str(recommendation_result)[:1000] + ("..." if len(str(recommendation_result)) > 1000 else ""))
        
        # JSON 파싱 시도
        print(f"\n🔍 JSON 파싱 시도...")
        print("-" * 40)
        
        try:
            if isinstance(recommendation_result, str):
                # 다양한 JSON 패턴 시도
                patterns = [
                    r'\[[\s\S]*?\]',  # 기본 JSON 배열
                    r'\[.*?\]',       # 단일 라인 JSON 배열
                    r'```json\s*(\[.*?\])\s*```',  # 마크다운 코드 블록
                    r'```\s*(\[.*?\])\s*```'       # 일반 코드 블록
                ]
                
                found_json = False
                for i, pattern in enumerate(patterns):
                    print(f"패턴 {i+1} 시도: {pattern}")
                    json_match = re.search(pattern, recommendation_result, re.DOTALL)
                    if json_match:
                        json_text = json_match.group(1) if json_match.groups() else json_match.group()
                        print(f"✅ JSON 패턴 발견!")
                        print(f"추출된 JSON: {json_text[:200]}...")
                        
                        try:
                            recommendations = json.loads(json_text)
                            print(f"✅ JSON 파싱 성공! {len(recommendations)}개 종목 발견")
                            
                            # 추천 종목 출력
                            print("\n📊 AI 추천 투자 종목:")
                            print("-" * 40)
                            for j, stock in enumerate(recommendations, 1):
                                print(f"{j}. {stock.get('ticker', 'N/A')} ({stock.get('name', 'N/A')})")
                                print(f"   현재가: ${stock.get('current_price', 'N/A')}")
                                print(f"   AI 점수: {stock.get('score', 'N/A')}/100")
                                print(f"   RSI: {stock.get('rsi', 'N/A')}")
                                print()
                            
                            found_json = True
                            return recommendations
                            
                        except json.JSONDecodeError as je:
                            print(f"❌ JSON 파싱 실패: {str(je)}")
                            continue
                    else:
                        print("❌ 패턴 매치 실패")
                
                if not found_json:
                    print("⚠️ 모든 JSON 패턴 시도 실패")
                    print("원본 결과를 다시 확인해보세요:")
                    print(recommendation_result)
                    return None
                    
            else:
                print(f"⚠️ 예상치 못한 결과 타입: {type(recommendation_result)}")
                return None
                
        except Exception as parse_error:
            print(f"❌ 파싱 중 예외 발생: {str(parse_error)}")
            return None
            
    except Exception as e:
        log_error(logger, e, "투자종목추천시스템")
        log_analysis_complete(logger, "ALL", "투자종목추천", False)
        print(f"\n❌ 추천 시스템 실행 중 오류 발생: {str(e)}")
        print(f"오류 타입: {type(e).__name__}")
        return None

if __name__ == "__main__":
    result = test_recommendation_system()
    
    print("\n" + "="*60)
    if result:
        print(f"✅ 테스트 성공! {len(result)}개 종목 추천 완료")
    else:
        print("❌ 테스트 실패 - 추천 결과 없음")
    print("="*60)