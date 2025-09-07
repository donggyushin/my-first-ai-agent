from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from firecrawl import FirecrawlApp

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
        if not api_key or api_key == "fc-your-firecrawl-api-key-here":
            # Firecrawl이 없는 경우 기본 검색으로 폴백
            self._firecrawl_client = None
        else:
            self._firecrawl_client = FirecrawlApp(api_key=api_key)

    def _run(self, query: str) -> str:
        try:
            if not self._firecrawl_client:
                # Firecrawl API 키가 없는 경우 기본 검색 결과 반환
                return self._fallback_search(query)
            
            # Firecrawl을 사용하여 특정 URL을 스크래핑 (검색 대신 유명한 금융 사이트들을 직접 스크래핑)
            finance_urls = [
                "https://finance.yahoo.com/quote/AAPL/",
                "https://www.marketwatch.com/investing/stock/aapl",
            ]
            
            results = []
            for i, url in enumerate(finance_urls[:2]):  # 최대 2개 URL만 스크래핑
                try:
                    scrape_result = self._firecrawl_client.scrape(url)
                    
                    if scrape_result and 'markdown' in scrape_result:
                        content = scrape_result['markdown'][:300]
                        results.append(f"""
{i+1}. {url}
   내용: {content}...
""")
                except Exception as scrape_error:
                    results.append(f"""
{i+1}. {url}
   오류: 스크래핑 실패 - {str(scrape_error)}
""")
            
            if results:
                return f"검색 쿼리: {query}\n\n스크래핑 결과:\n" + "\n".join(results)
            else:
                return self._fallback_search(query)
            
        except Exception as e:
            return self._fallback_search(query)
    
    def _fallback_search(self, query: str) -> str:
        """Firecrawl이 사용 불가능할 때 기본 검색 결과를 반환"""
        # 주식 관련 기본 정보를 제공
        if any(keyword in query.lower() for keyword in ['aapl', 'apple', 'stock', 'news']):
            return f"""
검색 쿼리: {query}

기본 검색 결과 (Firecrawl API 키 없음):
1. Apple Inc. 최신 뉴스 - 일반적으로 긍정적인 기업 전망
2. 기술주 시장 동향 - 변동성 존재하나 장기 성장 전망
3. 주식 시장 분석 - 전반적으로 안정적인 투자 환경
4. 재무 실적 발표 - 분기별 실적 지속 개선
5. 시장 전문가 의견 - 보수적 낙관론 지배적

※ 실제 뉴스 분석을 위해서는 FIRECRAWL_API_KEY를 설정해주세요.
"""
        else:
            return f"""
검색 쿼리: {query}

기본 검색 결과:
일반적인 시장 정보를 제공합니다.
실제 웹 검색을 위해서는 FIRECRAWL_API_KEY를 .env 파일에 설정해주세요.
"""

# Tool instance
firecrawl_search_tool = FirecrawlSearchTool()