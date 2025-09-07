import os
import json
from datetime import datetime
from typing import List, Dict, Any

def generate_html_report(analysis_results: List[Dict[str, Any]], recommendations: List[Dict[str, Any]]) -> str:
    """
    분석 결과를 바탕으로 예쁜 HTML 보고서를 생성합니다.
    
    Args:
        analysis_results: 개별 분석 결과 리스트
        recommendations: 초기 추천 결과 리스트
        
    Returns:
        str: 생성된 HTML 파일의 경로
    """
    
    # 보고서 디렉토리 생성
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # 파일명 생성 (현재 시간 기준)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"investment_report_{timestamp}.html"
    report_path = os.path.join(reports_dir, report_filename)
    
    # HTML 템플릿 생성
    html_content = generate_html_template(analysis_results, recommendations)
    
    # 파일에 저장
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath(report_path)

def generate_html_template(analysis_results: List[Dict[str, Any]], recommendations: List[Dict[str, Any]]) -> str:
    """HTML 템플릿을 생성합니다."""
    
    current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")
    
    # 성공한 분석과 실패한 분석 분리
    successful_analyses = [r for r in analysis_results if not r.get('error', False)]
    failed_analyses = [r for r in analysis_results if r.get('error', False)]
    
    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 투자 종합 분석 보고서</title>
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {generate_header(current_time)}
        {generate_executive_summary(analysis_results, recommendations)}
        {generate_recommendation_overview(recommendations)}
        {generate_detailed_analysis(successful_analyses)}
        {generate_failed_analysis_section(failed_analyses)}
        {generate_footer()}
    </div>
    
    <script>
        {get_javascript()}
    </script>
</body>
</html>
"""
    return html

def get_css_styles() -> str:
    """CSS 스타일을 반환합니다."""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .card h2 {
            color: #5a67d8;
            margin-bottom: 1rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .summary-item {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
        }
        
        .summary-item.warning {
            background: linear-gradient(135deg, #ed8936, #dd6b20);
            box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3);
        }
        
        .summary-item h3 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .summary-item p {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .recommendation-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stock-card {
            background: linear-gradient(135deg, #f7fafc, #edf2f7);
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1.2rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stock-card:hover {
            background: linear-gradient(135deg, #e2e8f0, #cbd5e0);
            transform: translateY(-3px);
        }
        
        .stock-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, #5a67d8, #667eea);
        }
        
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .stock-ticker {
            font-size: 1.3rem;
            font-weight: bold;
            color: #2d3748;
        }
        
        .score-badge {
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .score-badge.high {
            background: linear-gradient(135deg, #48bb78, #38a169);
        }
        
        .score-badge.medium {
            background: linear-gradient(135deg, #ed8936, #dd6b20);
        }
        
        .score-badge.low {
            background: linear-gradient(135deg, #e53e3e, #c53030);
        }
        
        .stock-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: #4a5568;
        }
        
        .analysis-section {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #5a67d8;
        }
        
        .analysis-content {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            white-space: pre-wrap;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        .error-card {
            background: linear-gradient(135deg, #fed7d7, #feb2b2);
            border: 1px solid #fc8181;
            color: #742a2a;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .error-title {
            font-weight: bold;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .timestamp {
            font-size: 0.85rem;
            color: #718096;
            font-style: italic;
        }
        
        .footer {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: #4a5568;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-top: 3rem;
        }
        
        .footer h3 {
            color: #e53e3e;
            margin-bottom: 1rem;
        }
        
        .footer p {
            font-size: 0.9rem;
            line-height: 1.8;
            max-width: 600px;
            margin: 0 auto;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .summary-grid,
            .recommendation-grid {
                grid-template-columns: 1fr;
            }
            
            .stock-details {
                grid-template-columns: 1fr;
            }
        }
    """

def get_javascript() -> str:
    """JavaScript 코드를 반환합니다."""
    return """
        // 페이지 로드 시 애니메이션
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.card, .stock-card');
            cards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
        
        // 스크롤 시 헤더 고정 효과
        window.addEventListener('scroll', function() {
            const header = document.querySelector('.header');
            if (window.scrollY > 100) {
                header.style.position = 'sticky';
                header.style.top = '0';
                header.style.zIndex = '1000';
            } else {
                header.style.position = 'static';
            }
        });
    """

def generate_header(current_time: str) -> str:
    """헤더 섹션을 생성합니다."""
    return f"""
        <div class="header">
            <h1>🤖 AI 투자 종합 분석 보고서</h1>
            <p class="subtitle">생성일시: {current_time}</p>
        </div>
    """

def generate_executive_summary(analysis_results: List[Dict], recommendations: List[Dict]) -> str:
    """경영진 요약 섹션을 생성합니다."""
    total_analyzed = len(analysis_results)
    successful = len([r for r in analysis_results if not r.get('error', False)])
    failed = total_analyzed - successful
    
    return f"""
        <div class="card">
            <h2>📊 분석 요약</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>{len(recommendations)}</h3>
                    <p>AI 추천 종목 수</p>
                </div>
                <div class="summary-item">
                    <h3>{successful}</h3>
                    <p>성공적 분석 완료</p>
                </div>
                {f'<div class="summary-item warning"><h3>{failed}</h3><p>분석 실패</p></div>' if failed > 0 else ''}
            </div>
        </div>
    """

def generate_recommendation_overview(recommendations: List[Dict]) -> str:
    """추천 종목 개요를 생성합니다."""
    html = """
        <div class="card">
            <h2>🎯 AI 추천 종목 개요</h2>
            <div class="recommendation-grid">
    """
    
    for i, stock in enumerate(recommendations, 1):
        score = stock.get('score', 0)
        score_class = 'high' if score >= 80 else 'medium' if score >= 60 else 'low'
        
        html += f"""
            <div class="stock-card">
                <div class="stock-header">
                    <div>
                        <div class="stock-ticker">{i}. {stock['ticker']}</div>
                        <div style="font-size: 0.9rem; color: #718096;">{stock.get('name', stock['ticker'])}</div>
                    </div>
                    <div class="score-badge {score_class}">{score}/100</div>
                </div>
                <div class="stock-details">
                    <div><strong>현재가:</strong> ${stock.get('current_price', 'N/A')}</div>
                    <div><strong>RSI:</strong> {stock.get('rsi', 'N/A')}</div>
                </div>
            </div>
        """
    
    html += """
            </div>
        </div>
    """
    
    return html

def generate_detailed_analysis(successful_analyses: List[Dict]) -> str:
    """상세 분석 섹션을 생성합니다."""
    if not successful_analyses:
        return ""
    
    html = """
        <div class="card">
            <h2>📈 상세 투자 분석 결과</h2>
    """
    
    for i, result in enumerate(successful_analyses, 1):
        analysis_text = str(result.get('analysis_result', '분석 결과 없음'))
        
        html += f"""
            <div class="analysis-section">
                <h3 style="color: #2d3748; margin-bottom: 1rem;">
                    {i}. {result['ticker']} ({result['name']}) 
                    <span style="font-size: 0.8rem; color: #718096;">- 추천점수: {result['recommendation_score']}/100</span>
                </h3>
                <div class="timestamp">분석 완료: {result['analysis_time']}</div>
                <div class="analysis-content">{analysis_text}</div>
            </div>
        """
    
    html += """
        </div>
    """
    
    return html

def generate_failed_analysis_section(failed_analyses: List[Dict]) -> str:
    """실패한 분석 섹션을 생성합니다."""
    if not failed_analyses:
        return ""
    
    html = """
        <div class="card">
            <h2>⚠️ 분석 실패 종목</h2>
            <p style="margin-bottom: 1rem; color: #718096;">다음 종목들은 분석 중 오류가 발생했습니다:</p>
    """
    
    for result in failed_analyses:
        html += f"""
            <div class="error-card">
                <div class="error-title">{result['ticker']} ({result['name']})</div>
                <div>오류 내용: {result.get('analysis_result', '알 수 없는 오류')}</div>
                <div class="timestamp">시도 시간: {result['analysis_time']}</div>
            </div>
        """
    
    html += """
        </div>
    """
    
    return html

def generate_footer() -> str:
    """푸터 섹션을 생성합니다."""
    return """
        <div class="footer">
            <h3>⚠️ 투자 위험 고지</h3>
            <p>
                본 분석 보고서는 AI 기반 투자 참고 자료로서 투자 권유나 종목 추천을 위한 것이 아닙니다. 
                모든 투자 결정은 투자자 본인의 판단과 책임 하에 이루어져야 하며, 
                투자 시 발생할 수 있는 손실에 대해서는 투자자가 모든 책임을 집니다. 
                <br><br>
                <strong>과거 수익률이 미래 수익률을 보장하지 않으며, 투자 전 충분한 검토와 전문가 상담을 권장합니다.</strong>
            </p>
            <p style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;">
                Generated by AI Investment Analysis System
            </p>
        </div>
    """