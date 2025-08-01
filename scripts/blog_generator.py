from typing import List, Dict, Any
from datetime import datetime

def generate_paper_summary(paper) -> str:
    """논문의 핵심 요약을 생성합니다."""
    abstract = paper.abstract if paper.abstract else "초록 정보가 없습니다."
    
    # 첫 문장과 주요 키워드 추출
    sentences = abstract.split('. ')
    if len(sentences) > 3:
        summary = '. '.join(sentences[:2]) + '.'
    else:
        summary = abstract[:300] + "..." if len(abstract) > 300 else abstract
    
    return summary

def categorize_papers_by_category(papers: List[Any]) -> Dict[str, List[Any]]:
    """논문을 카테고리별로 분류합니다."""
    categorized = {}
    
    for paper in papers:
        if paper.categories:
            for category in paper.categories:
                if category.name not in categorized:
                    categorized[category.name] = []
                categorized[category.name].append(paper)
        else:
            # 카테고리가 없는 논문은 "기타"로 분류
            if "기타" not in categorized:
                categorized["기타"] = []
            categorized["기타"].append(paper)
    
    return categorized

def generate_blog_post(trend_report: str, date: str, categories: List[str], papers: List[Any] = None) -> str:
    """개선된 블로그 포스트를 생성합니다."""
    front_matter = f"""---
title: "MCI 논문 동향 리포트 ({date})"
date: {date}
categories: [{', '.join(categories)}]
tags: [MCI, Research, Trends, Papers]
author: "CLAIR"
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: true
description: "MCI 관련 최신 논문 요약 및 연구 동향 분석"
---

"""
    
    content = f"""# 🧠 MCI 연구 동향 리포트

> **생성일**: {datetime.now().strftime('%Y년 %m월 %d일')}  
> **수집 논문 수**: {len(papers) if papers else 0}개

---

## 📊 연구 동향 분석

{trend_report}

---

"""
    
    # 논문을 카테고리별로 분류하여 표시
    if papers and len(papers) > 0:
        categorized_papers = categorize_papers_by_category(papers[-20:])  # 최신 20개
        
        content += "## 📚 최신 논문 요약\n\n"
        
        # 각 카테고리별로 논문 표시
        for category_name, category_papers in categorized_papers.items():
            if category_papers:
                # 카테고리명을 한국어로 변환
                category_display = {
                    'clinical_study': '🏥 임상연구',
                    'neuroscience': '🧬 신경과학',
                    'biomarker': '🔬 바이오마커',
                    'ai_ml': '🤖 AI/머신러닝',
                    'imaging': '📸 이미징',
                    'cognitive_assessment': '🧪 인지평가',
                    '기타': '📋 기타'
                }.get(category_name, f'📄 {category_name}')
                
                content += f"### {category_display}\n\n"
                
                for i, paper in enumerate(category_papers[:5], 1):  # 카테고리당 최대 5개
                    content += f"#### {i}. {paper.title}\n\n"
                    
                    # 저널 정보
                    content += f"**📖 저널**: {paper.journal_name}"
                    if paper.journal_volume:
                        content += f" Vol.{paper.journal_volume}"
                    if paper.journal_issue:
                        content += f" Issue.{paper.journal_issue}"
                    content += f" ({paper.publication_year})\n\n"
                    
                    # PubMed 링크
                    content += f"**🔗 PubMed**: [{paper.pmid}](https://pubmed.ncbi.nlm.nih.gov/{paper.pmid}/)\n\n"
                    
                    # 논문 요약
                    summary = generate_paper_summary(paper)
                    content += f"**📝 요약**: {summary}\n\n"
                    
                    # 연구 카테고리
                    if paper.categories:
                        categories_str = ", ".join([cat.name for cat in paper.categories])
                        content += f"**🏷️ 카테고리**: {categories_str}\n\n"
                    
                    content += "---\n\n"
    
    # Footer 추가
    content += """
## 💡 이용 안내

- **논문 원문**: PubMed 링크를 통해 전문을 확인하실 수 있습니다.
- **업데이트**: 매일 오전 7시(JST)에 새로운 논문이 자동으로 추가됩니다.
- **피드백**: 개선 사항이나 오류 발견 시 GitHub 이슈로 알려주세요.

---

*본 블로그는 MCI 연구 학습을 위한 목적으로 운영됩니다.*
"""
    
    return front_matter + content
