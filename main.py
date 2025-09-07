import dotenv
import sys
import json
import os
from datetime import datetime
import re
from utils.logger import setup_logger, log_analysis_start, log_analysis_complete, log_error

dotenv.load_dotenv()

logger = setup_logger()

if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY가 환경변수에 설정되지 않았습니다.")
    print("❌ OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    sys.exit(1)

from crews.investment_advisor_crew import InvestmentAdvisorCrew
from crews.investment_item_recommendar_crew import InvestmentItemRecommendarCrew

def analyze_all_recommendations():
    """추천된 모든 주식을 자동으로 분석하고 보고서 생성"""
    from config.constants import MESSAGE_TEMPLATES
    
    print(MESSAGE_TEMPLATES['SYSTEM_START'])
    print("=" * 50)
    
    # 먼저 투자 종목 추천 시스템 실행
    print(f"\n{MESSAGE_TEMPLATES['RECOMMENDATION_START']}")
    print("이 과정은 1-2분 정도 소요될 수 있습니다.\n")
    
    recommendations = []
    analysis_results = []
    
    try:
        log_analysis_start(logger, "ALL", "투자종목추천")
        recommendar_crew = InvestmentItemRecommendarCrew()
        recommendation_result = recommendar_crew.crew().kickoff()
        
        log_analysis_complete(logger, "ALL", "투자종목추천", True)
        print("\n" + "="*60)
        print("✅ AI 추천 투자 종목 분석 완료!")
        print("="*60)
        
        # JSON 형태로 결과 파싱
        try:
            # CrewOutput 객체인 경우 raw 텍스트 추출
            if hasattr(recommendation_result, 'raw'):
                result_text = recommendation_result.raw
                print(f"\n🔍 CrewOutput 추출 성공! 텍스트 길이: {len(str(result_text))}")
            elif isinstance(recommendation_result, str):
                result_text = recommendation_result
                print(f"\n🔍 문자열 결과 확인! 길이: {len(result_text)}")
            else:
                # 다른 속성들 시도
                if hasattr(recommendation_result, 'result'):
                    result_text = str(recommendation_result.result)
                elif hasattr(recommendation_result, 'output'):
                    result_text = str(recommendation_result.output)
                else:
                    result_text = str(recommendation_result)
                print(f"\n🔍 객체를 문자열로 변환! 타입: {type(recommendation_result)}")
            
            print(f"📋 결과 미리보기: {str(result_text)[:300]}...")
            
            # 다양한 JSON 패턴으로 파싱 시도
            patterns = [
                r'\[[\s\S]*?\]',  # 기본 JSON 배열
                r'```json\s*(\[.*?\])\s*```',  # 마크다운 JSON 코드 블록
                r'```\s*(\[.*?\])\s*```',      # 일반 코드 블록
                r'(\[.*?\])',                   # 단순 배열 패턴
            ]
            
            found_json = False
            for i, pattern in enumerate(patterns):
                print(f"🔎 패턴 {i+1} 시도: {pattern}")
                json_match = re.search(pattern, result_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1) if json_match.groups() else json_match.group()
                    print(f"✅ JSON 패턴 발견! 길이: {len(json_text)}")
                    print(f"📄 추출된 JSON 미리보기: {json_text[:200]}...")
                    
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
                        break
                        
                    except json.JSONDecodeError as je:
                        print(f"❌ JSON 파싱 실패 (패턴 {i+1}): {str(je)}")
                        continue
                else:
                    print(f"❌ 패턴 {i+1} 매치 실패")
            
            if not found_json:
                logger.warning("모든 JSON 패턴 시도 실패")
                print("⚠️ 모든 JSON 패턴 시도 실패")
                print(f"📄 전체 결과 내용:\n{result_text}")
                return
                
        except Exception as parse_error:
            logger.error(f"추천 결과 파싱 중 오류: {str(parse_error)}")
            print(f"\n❌ 추천 결과 파싱 실패: {str(parse_error)}")
            return
            
    except Exception as e:
        log_error(logger, e, "투자종목추천시스템")
        log_analysis_complete(logger, "ALL", "투자종목추천", False)
        print(f"\n❌ 추천 시스템 실행 중 오류 발생: {str(e)}")
        return
    
    if not recommendations:
        print("\n❌ 추천 종목을 찾을 수 없어 분석을 중단합니다.")
        return
    
    # 각 추천 종목에 대해 상세 분석 수행
    print(f"\n{'='*60}")
    print("🔍 추천 종목들에 대한 상세 분석을 시작합니다...")
    print(f"총 {len(recommendations)}개 종목을 분석합니다. 예상 소요 시간: {len(recommendations) * 3}분")
    print(f"{'='*60}")
    
    for i, stock in enumerate(recommendations, 1):
        ticker = stock['ticker']
        stock_name = stock.get('name', ticker)
        
        print(f"\n📈 [{i}/{len(recommendations)}] {ticker} ({stock_name}) 분석 중...")
        print("-" * 50)
        
        try:
            log_analysis_start(logger, ticker, "개별종목분석")
            
            # 개별 주식 분석 크루 실행
            investment_crew = InvestmentAdvisorCrew()
            result = investment_crew.crew().kickoff(inputs={"ticker": ticker})
            
            log_analysis_complete(logger, ticker, "개별종목분석", True)
            
            # CrewOutput 객체인 경우 텍스트 추출
            if hasattr(result, 'raw'):
                analysis_text = result.raw
            elif hasattr(result, 'result'):
                analysis_text = str(result.result)
            elif hasattr(result, 'output'):
                analysis_text = str(result.output)
            else:
                analysis_text = str(result)
            
            # 분석 결과 저장
            analysis_results.append({
                'ticker': ticker,
                'name': stock_name,
                'recommendation_score': stock.get('score', 'N/A'),
                'current_price': stock.get('current_price', 'N/A'),
                'rsi': stock.get('rsi', 'N/A'),
                'analysis_result': analysis_text,
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            print(f"✅ {ticker} 분석 완료!")
            
        except Exception as e:
            log_error(logger, e, f"개별종목분석-{ticker}")
            log_analysis_complete(logger, ticker, "개별종목분석", False)
            
            print(f"❌ {ticker} 분석 실패: {str(e)}")
            
            # 실패한 경우에도 결과에 포함 (오류 정보와 함께)
            analysis_results.append({
                'ticker': ticker,
                'name': stock_name,
                'recommendation_score': stock.get('score', 'N/A'),
                'current_price': stock.get('current_price', 'N/A'),
                'rsi': stock.get('rsi', 'N/A'),
                'analysis_result': f"분석 실패: {str(e)}",
                'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': True
            })
    
    # HTML 보고서 생성
    if analysis_results:
        print(f"\n{'='*60}")
        print("📄 종합 투자 보고서를 생성하는 중...")
        print(f"{'='*60}")
        
        try:
            from utils.report_generator import generate_html_report
            report_path = generate_html_report(analysis_results, recommendations)
            
            print(f"✅ 보고서 생성 완료!")
            print(f"📁 보고서 위치: {report_path}")
            print(f"🌐 브라우저에서 보고서를 확인하세요!")
            
            # 자동으로 브라우저에서 열기 시도
            try:
                import webbrowser
                webbrowser.open(f'file://{report_path}')
                print("🚀 기본 브라우저에서 보고서를 열었습니다!")
            except Exception as browser_error:
                logger.warning(f"브라우저 자동 열기 실패: {str(browser_error)}")
                print("💡 수동으로 브라우저에서 보고서 파일을 열어주세요.")
                
        except Exception as report_error:
            logger.error(f"보고서 생성 실패: {str(report_error)}")
            print(f"❌ 보고서 생성 실패: {str(report_error)}")
            
            # 텍스트 형태로라도 결과 출력
            print(f"\n{'='*60}")
            print("📊 분석 결과 요약 (텍스트 형태)")
            print(f"{'='*60}")
            
            for result in analysis_results:
                print(f"\n🔹 {result['ticker']} ({result['name']})")
                print(f"   추천 점수: {result['recommendation_score']}/100")
                print(f"   현재가: ${result['current_price']}")
                print(f"   분석 시간: {result['analysis_time']}")
                if result.get('error'):
                    print(f"   상태: ❌ 분석 실패")
                else:
                    print(f"   상태: ✅ 분석 완료")
                print("-" * 40)
    else:
        print("\n❌ 분석된 결과가 없어 보고서를 생성할 수 없습니다.")

if __name__ == "__main__":
    from config.constants import MESSAGE_TEMPLATES
    
    # 자동 분석 및 보고서 생성 실행
    analyze_all_recommendations()
    
    print(f"\n{MESSAGE_TEMPLATES['DISCLAIMER']}")