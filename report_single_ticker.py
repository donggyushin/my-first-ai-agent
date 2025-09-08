import dotenv
import sys
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

def validate_ticker(ticker):
    """티커 형식 유효성 검사"""
    if not ticker:
        return False
    
    # 기본적인 티커 형식 검사 (1-5글자 영문)
    ticker_pattern = re.compile(r'^[A-Za-z]{1,5}$')
    return ticker_pattern.match(ticker.strip().upper()) is not None

def analyze_single_ticker(ticker):
    """단일 티커에 대한 상세 분석 수행"""
    ticker = ticker.strip().upper()
    
    print(f"\n{'='*60}")
    print(f"📈 {ticker} 주식 분석을 시작합니다...")
    print(f"{'='*60}")
    print("이 과정은 2-3분 정도 소요될 수 있습니다.\n")
    
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
        
        # 분석 결과 데이터 구성
        analysis_result = {
            'ticker': ticker,
            'name': ticker,  # 실제 회사명은 분석 결과에서 추출 가능
            'analysis_result': analysis_text,
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"✅ {ticker} 분석 완료!")
        
        # HTML 보고서 생성
        print(f"\n{'='*60}")
        print("📄 투자 분석 보고서를 생성하는 중...")
        print(f"{'='*60}")
        
        try:
            from utils.report_generator import generate_html_report
            # 단일 종목이므로 리스트로 감싸서 전달
            report_path = generate_html_report([analysis_result], [])
            
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
            print(f"📊 {ticker} 분석 결과")
            print(f"{'='*60}")
            print(analysis_text)
            
    except Exception as e:
        log_error(logger, e, f"개별종목분석-{ticker}")
        log_analysis_complete(logger, ticker, "개별종목분석", False)
        
        print(f"❌ {ticker} 분석 실패: {str(e)}")
        return False
    
    return True

def main():
    """메인 실행 함수"""
    from config.constants import MESSAGE_TEMPLATES
    
    print(MESSAGE_TEMPLATES['SYSTEM_START'])
    print("=" * 50)
    print("\n🎯 단일 종목 투자 분석 시스템")
    print("분석하고 싶은 미국 주식의 티커를 입력하세요.")
    print("종료하려면 'q' 또는 'quit'을 입력하세요.\n")
    
    while True:
        try:
            # 사용자 입력 받기
            user_input = input("📝 티커 입력 (예: AAPL, TSLA, MSFT): ").strip()
            
            # 종료 조건 확인
            if user_input.lower() in ['q', 'quit']:
                print("\n👋 프로그램을 종료합니다. 좋은 투자 되세요!")
                break
            
            # 빈 입력 처리
            if not user_input:
                print("⚠️ 티커를 입력해주세요.\n")
                continue
            
            # 티커 유효성 검사
            if not validate_ticker(user_input):
                print("❌ 올바른 티커 형식이 아닙니다. (예: AAPL, TSLA, MSFT)\n")
                continue
            
            # 티커 분석 실행
            ticker = user_input.upper()
            success = analyze_single_ticker(ticker)
            
            if success:
                print(f"\n✅ {ticker} 분석이 완료되었습니다!")
            else:
                print(f"\n❌ {ticker} 분석에 실패했습니다.")
            
            print(f"\n{'='*60}")
            print("다른 종목을 분석하시겠습니까?")
            print("새로운 티커를 입력하거나 'q'/'quit'으로 종료하세요.")
            print(f"{'='*60}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다. 좋은 투자 되세요!")
            break
        except Exception as e:
            logger.error(f"메인 루프 실행 중 오류: {str(e)}")
            print(f"\n❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
            print("다시 시도해주세요.\n")

if __name__ == "__main__":
    main()