from typing import List

def generate_blog_post(trend_report: str, date: str, categories: List[str]) -> str:
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
    return front_matter + trend_report
