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
            if isinstance(recommendation_result, str):
                # 결과에서 JSON 부분 추출 (더 정확한 정규식 사용)
                json_match = re.search(r'\[[\s\S]*?\]', recommendation_result)
                if json_match:
                    recommendations = json.loads(json_match.group())
                    print("\n📊 AI 추천 투자 종목 TOP 5:")
                    print("-" * 40)
                    for i, stock in enumerate(recommendations, 1):
                        print(f"{i}. {stock['ticker']} ({stock.get('name', stock['ticker'])})")
                        print(f"   현재가: ${stock.get('current_price', 'N/A')}")
                        print(f"   AI 점수: {stock.get('score', 'N/A')}/100")
                        print(f"   RSI: {stock.get('rsi', 'N/A')}")
                        print()
                else:
                    logger.warning("추천 결과에서 JSON 형식을 찾을 수 없습니다")
                    print(f"\n⚠️ 추천 결과 파싱 실패. 원본 결과:\n{recommendation_result}")
                    return
            else:
                logger.warning("추천 결과가 예상된 문자열 형식이 아닙니다")
                print(f"\n⚠️ 예상치 못한 추천 결과 형식: {type(recommendation_result)}")
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
            
            # 분석 결과 저장
            analysis_results.append({
                'ticker': ticker,
                'name': stock_name,
                'recommendation_score': stock.get('score', 'N/A'),
                'current_price': stock.get('current_price', 'N/A'),
                'rsi': stock.get('rsi', 'N/A'),
                'analysis_result': result,
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