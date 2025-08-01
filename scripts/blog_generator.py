from typing import List, Dict, Any
from datetime import datetime

def generate_blog_post(trend_report: str, date: str, categories: List[str], papers: List[Any] = None) -> str:
    """블로그 포스트 마크다운을 생성합니다."""
    front_matter = f"""---
title: "MCI 논문 동향 리포트 ({date})"
date: {date}
categories: [{', '.join(categories)}]
tags: [MCI, Research, Trends]
author: "CLAIR"
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: true
---

"""
    
    content = trend_report
    
    # 최신 논문 목록 추가
    if papers and len(papers) > 0:
        content += "\n\n## 최신 수집 논문\n\n"
        for i, paper in enumerate(papers[:10], 1):  # 최대 10개만 표시
            content += f"### {i}. {paper.title}\n\n"
            content += f"**저널**: {paper.journal_name}"
            if paper.journal_volume:
                content += f" Vol.{paper.journal_volume}"
            if paper.journal_issue:
                content += f" Issue.{paper.journal_issue}"
            content += f" ({paper.publication_year})\n\n"
            
            content += f"**PMID**: [{paper.pmid}](https://pubmed.ncbi.nlm.nih.gov/{paper.pmid}/)\n\n"
            
            if paper.abstract:
                abstract_preview = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
                content += f"**요약**: {abstract_preview}\n\n"
            
            # 논문의 카테고리 표시
            if paper.categories:
                categories_str = ", ".join([cat.name for cat in paper.categories])
                content += f"**카테고리**: {categories_str}\n\n"
            
            content += "---\n\n"
    
    return front_matter + content
