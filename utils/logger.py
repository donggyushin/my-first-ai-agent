import logging
import os
from datetime import datetime

def setup_logger(name: str = "investment_advisor", level: str = "INFO") -> logging.Logger:
    """투자 자문 시스템용 로거 설정"""
    
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper()))
    
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_filename = f"{logs_dir}/investment_advisor_{datetime.now().strftime('%Y%m%d')}.log"
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    console_handler.setLevel(logging.INFO)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_analysis_start(logger: logging.Logger, ticker: str, analysis_type: str):
    """분석 시작 로그"""
    logger.info(f"분석 시작 - 종목: {ticker}, 유형: {analysis_type}")

def log_analysis_complete(logger: logging.Logger, ticker: str, analysis_type: str, success: bool):
    """분석 완료 로그"""
    status = "성공" if success else "실패"
    logger.info(f"분석 완료 - 종목: {ticker}, 유형: {analysis_type}, 결과: {status}")

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """에러 로그"""
    logger.error(f"에러 발생 - {context}: {str(error)}", exc_info=True)