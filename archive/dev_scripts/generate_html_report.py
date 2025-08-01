#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI 논문 데이터베이스 HTML 리포트 생성기
"""
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

def generate_html_report():
    """HTML 형태의 논문 리포트를 생성합니다."""
    
    try:
        db_manager = DatabaseManager('data/mci_papers.db')
        papers = db_manager.get_all_papers()
        
        # HTML 헤더
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 MCI 논문 데이터베이스 리포트</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; }}
        .stats {{ display: flex; justify-content: space-around; background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .stat-item {{ text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #3498db; }}
        .paper {{ border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; background-color: #fafafa; }}
        .paper-title {{ font-size: 1.2em; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
        .paper-info {{ margin: 5px 0; }}
        .categories {{ background-color: #e8f4f8; padding: 5px 10px; border-radius: 15px; display: inline-block; margin: 2px; font-size: 0.9em; }}
        .abstract {{ background-color: #f8f9fa; padding: 10px; border-left: 4px solid #3498db; margin: 10px 0; font-style: italic; }}
        .pubmed-link {{ background-color: #3498db; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; display: inline-block; margin-top: 10px; }}
        .pubmed-link:hover {{ background-color: #2980b9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 MCI 논문 데이터베이스 리포트</h1>
        <p style="text-align: center; color: #7f8c8d;">생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</p>
"""
        
        if not papers:
            html_content += "<h2>❌ 데이터베이스에 논문이 없습니다.</h2></div></body></html>"
            return html_content
        
        # 통계 정보
        journals = set(paper.journal_name for paper in papers if paper.journal_name)
        years = set(paper.publication_year for paper in papers if paper.publication_year)
        
        categories = {}
        for paper in papers:
            if paper.categories:
                for cat in paper.categories:
                    categories[cat.name] = categories.get(cat.name, 0) + 1
        
        html_content += f"""
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(papers)}</div>
                <div>총 논문 수</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(journals)}</div>
                <div>저널 수</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{min(years) if years else 'N/A'}-{max(years) if years else 'N/A'}</div>
                <div>연도 범위</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(categories)}</div>
                <div>카테고리 수</div>
            </div>
        </div>
"""
        
        # 카테고리별 통계
        if categories:
            html_content += "<h2>🏷️ 카테고리별 논문 분포</h2>"
            category_display = {
                'clinical_study': '🏥 임상연구',
                'neuroscience': '🧬 신경과학',
                'biomarker': '🔬 바이오마커',
                'ai_ml': '🤖 AI/머신러닝',
                'imaging': '📸 이미징',
                'cognitive_assessment': '🧪 인지평가'
            }
            
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                display_name = category_display.get(cat, cat)
                percentage = (count / len(papers)) * 100
                html_content += f'<span class="categories">{display_name}: {count}편 ({percentage:.1f}%)</span> '
        
        # 논문 목록
        html_content += f"<h2>📚 수록 논문 목록 (총 {len(papers)}편)</h2>"
        
        # 최신 순으로 정렬
        for i, paper in enumerate(papers, 1):
            categories_html = ""
            if paper.categories:
                category_display = {
                    'clinical_study': '🏥 임상연구',
                    'neuroscience': '🧬 신경과학',
                    'biomarker': '🔬 바이오마커',
                    'ai_ml': '🤖 AI/머신러닝',
                    'imaging': '📸 이미징',
                    'cognitive_assessment': '🧪 인지평가'
                }
                for cat in paper.categories:
                    display_name = category_display.get(cat.name, cat.name)
                    categories_html += f'<span class="categories">{display_name}</span> '
            
            abstract_html = ""
            if paper.abstract:
                abstract_preview = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
                abstract_html = f'<div class="abstract">📝 <strong>초록:</strong> {abstract_preview}</div>'
            
            html_content += f"""
        <div class="paper">
            <div class="paper-title">{i}. {paper.title}</div>
            <div class="paper-info">🔗 <strong>PMID:</strong> {paper.pmid}</div>
            <div class="paper-info">📖 <strong>저널:</strong> {paper.journal_name}"""
            
            if paper.journal_volume:
                html_content += f" Vol.{paper.journal_volume}"
            if paper.journal_issue:
                html_content += f" Issue.{paper.journal_issue}"
            
            html_content += f" ({paper.publication_year})</div>"
            
            if categories_html:
                html_content += f'<div class="paper-info">🏷️ <strong>카테고리:</strong> {categories_html}</div>'
            
            html_content += abstract_html
            html_content += f'<a href="https://pubmed.ncbi.nlm.nih.gov/{paper.pmid}/" target="_blank" class="pubmed-link">🌐 PubMed에서 보기</a>'
            html_content += "</div>"
        
        # HTML 푸터
        html_content += """
        <hr style="margin: 30px 0;">
        <p style="text-align: center; color: #7f8c8d;">
            📖 이 리포트는 MCI(경도인지장애) 관련 논문들을 연구 학습 목적으로 정리한 것입니다.<br>
            각 논문의 원문은 PubMed 링크를 통해 확인하실 수 있습니다.
        </p>
    </div>
</body>
</html>"""
        
        return html_content
        
    except Exception as e:
        error_html = f"""<!DOCTYPE html>
<html><head><title>오류</title></head><body>
<h1>❌ 오류가 발생했습니다</h1>
<p>{str(e)}</p>
</body></html>"""
        return error_html

def main():
    print("📄 MCI 논문 데이터베이스 HTML 리포트 생성 중...")
    
    html_report = generate_html_report()
    
    # HTML 파일 저장
    output_file = "mci_papers_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"✅ HTML 리포트가 생성되었습니다: {output_file}")
    print("📖 웹브라우저에서 해당 파일을 열어서 논문 목록을 확인하실 수 있습니다.")

if __name__ == "__main__":
    main()
