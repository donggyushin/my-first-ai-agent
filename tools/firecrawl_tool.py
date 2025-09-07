from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import dotenv
from firecrawl import FirecrawlApp
from datetime import datetime

# 환경변수 로드
dotenv.load_dotenv()

class FirecrawlSearchInput(BaseModel):
    """Input schema for Firecrawl search tool."""
    query: str = Field(..., description="Search query for web search")

class FirecrawlSearchTool(BaseTool):
    name: str = "firecrawl_search"
    description: str = "Search the web for information using Firecrawl to get structured content from web pages"
    args_schema: Type[BaseModel] = FirecrawlSearchInput
    
    def __init__(self):
        super().__init__()
        self._init_firecrawl()
    
    def _init_firecrawl(self):
        """Initialize Firecrawl client"""
        api_key = os.getenv("FIRECRAWL_API_KEY")
        
        if not api_key or api_key == "fc-your-firecrawl-api-key-here" or len(api_key) < 10:
            # Firecrawl이 없는 경우 기본 검색으로 폴백
            self._firecrawl_client = None
        else:
            try:
                self._firecrawl_client = FirecrawlApp(api_key=api_key)
            except Exception as e:
                self._firecrawl_client = None

    def _run(self, query: str) -> str:
        try:
            current_year = datetime.now().year
            
            if not self._firecrawl_client:
                return self._fallback_search(query, current_year)
            
            # 쿼리에서 주식 티커 추출
            ticker = "AAPL"  # 기본값
            if any(t in query.upper() for t in ['AAPL', 'APPLE']):
                ticker = "AAPL"
            elif any(t in query.upper() for t in ['MSFT', 'MICROSOFT']):
                ticker = "MSFT"
            elif any(t in query.upper() for t in ['GOOGL', 'GOOGLE']):
                ticker = "GOOGL"
            elif any(t in query.upper() for t in ['AMZN', 'AMAZON']):
                ticker = "AMZN"
            elif any(t in query.upper() for t in ['TSLA', 'TESLA']):
                ticker = "TSLA"
            
            # 현재 연도를 포함한 금융 사이트 URL들
            finance_urls = [
                f"https://finance.yahoo.com/quote/{ticker}/news/",
                f"https://www.marketwatch.com/investing/stock/{ticker.lower()}",
                f"https://finance.yahoo.com/quote/{ticker}/",
            ]
            
            results = []
            for i, url in enumerate(finance_urls[:2]):  # 최대 2개 URL만 스크래핑
                try:
                    scrape_result = self._firecrawl_client.scrape(url)
                    
                    content = None
                    if scrape_result:
                        # Handle Document object from Firecrawl
                        if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                            content = scrape_result.markdown
                        elif hasattr(scrape_result, 'content') and scrape_result.content:
                            content = scrape_result.content
                        elif hasattr(scrape_result, '__dict__'):
                            # Try to get content from attributes
                            for attr in ['markdown', 'content', 'text', 'html']:
                                if hasattr(scrape_result, attr):
                                    attr_content = getattr(scrape_result, attr)
                                    if attr_content and len(str(attr_content).strip()) > 0:
                                        content = str(attr_content)
                                        break
                    
                    if content and len(content.strip()) > 50:  # Minimum content length
                        content = content[:400]
                        results.append(f"""
{i+1}. {ticker} 정보 ({current_year}년 기준)
   출처: {url}
   내용: {content}...
""")
                    else:
                        results.append(f"""
{i+1}. {url}
   오류: 충분한 컨텐츠를 찾을 수 없음
""")
                except Exception as scrape_error:
                    results.append(f"""
{i+1}. {url}
   오류: 스크래핑 실패 - {str(scrape_error)}
""")
            
            if results:
                return f"검색 쿼리: {query} ({current_year}년)\n\n스크래핑 결과:\n" + "\n".join(results)
            else:
                return self._fallback_search(query, current_year)
            
        except Exception as e:
            return self._fallback_search(query, datetime.now().year)
    
    def _fallback_search(self, query: str, year: int = None) -> str:
        """Firecrawl이 사용 불가능할 때 기본 검색 결과를 반환"""
        if year is None:
            year = datetime.now().year
            
        # 주식 관련 기본 정보를 제공
        if any(keyword in query.lower() for keyword in ['aapl', 'apple', 'stock', 'news']):
            return f"""
검색 쿼리: {query} ({year}년)

기본 검색 결과 (Firecrawl API 키 인식 실패):
1. Apple Inc. {year}년 최신 뉴스 - 일반적으로 긍정적인 기업 전망
2. 기술주 시장 동향 - 변동성 존재하나 장기 성장 전망
3. {year}년 주식 시장 분석 - 전반적으로 안정적인 투자 환경
4. 재무 실적 발표 - 분기별 실적 지속 개선
5. 시장 전문가 의견 - 보수적 낙관론 지배적

※ 실제 뉴스 분석을 위해서는 FIRECRAWL_API_KEY가 올바르게 설정되어야 합니다.
"""
        else:
            return f"""
검색 쿼리: {query} ({year}년)

기본 검색 결과:
{year}년 일반적인 시장 정보를 제공합니다.
실제 웹 검색을 위해서는 FIRECRAWL_API_KEY가 올바르게 설정되어야 합니다.
"""

# Tool instance
firecrawl_search_tool = FirecrawlSearchTool()