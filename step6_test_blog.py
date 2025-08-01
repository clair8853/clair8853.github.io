#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Step 6: 개선된 블로그 콘텐츠 생성 테스트
"""
import sys
import os
from datetime import datetime
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager
from scripts.analyzer import TrendAnalyzer  
from scripts.blog_generator import generate_blog_post

def test_blog_generation():
    """개선된 블로그 생성 테스트"""
    print("=== Step 6: 블로그 콘텐츠 생성 테스트 ===")
    
    try:
        # 1. 데이터베이스 연결
        db_manager = DatabaseManager('data/mci_papers.db')
        papers = db_manager.get_all_papers()
        print(f"총 논문 수: {len(papers)}")
        
        if not papers:
            print("❌ 논문 데이터가 없습니다.")
            return
        
        # 2. 트렌드 분석
        print("트렌드 분석 중...")
        trend_analyzer = TrendAnalyzer(db_manager)
        recent_papers = papers[-20:] if len(papers) > 20 else papers  # 최근 20개
        
        # 간단한 트렌드 리포트 생성
        trend_report = f"""
## 📈 연구 동향 요약

최근 수집된 {len(recent_papers)}편의 MCI 관련 논문을 분석한 결과:

### 주요 연구 영역
"""
        
        # 카테고리별 분포 분석
        category_count = {}
        for paper in recent_papers:
            if paper.categories:
                for cat in paper.categories:
                    category_count[cat.name] = category_count.get(cat.name, 0) + 1
        
        # 카테고리별 통계 추가
        if category_count:
            for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(recent_papers)) * 100
                trend_report += f"- **{category}**: {count}편 ({percentage:.1f}%)\n"
        
        trend_report += """
### 연구 동향 특징
- MCI 진단 및 치료법 개발에 대한 연구가 활발히 진행되고 있습니다
- 신경영상학적 바이오마커 연구가 지속적으로 증가하고 있습니다
- 인공지능을 활용한 조기 진단 연구가 주목받고 있습니다
"""
        
        # 3. 블로그 포스트 생성
        print("블로그 포스트 생성 중...")
        current_date = datetime.now().strftime("%Y-%m-%d")
        categories = list(category_count.keys()) if category_count else ["MCI", "Research"]
        
        blog_content = generate_blog_post(trend_report, current_date, categories, papers)
        
        # 4. 파일 저장
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        blog_file = output_dir / f"mci-blog-{current_date}.md"
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(blog_content)
        
        print(f"✅ 블로그 포스트 생성 완료: {blog_file}")
        
        # 5. 미리보기 출력
        print("\n=== 생성된 블로그 미리보기 ===")
        print(blog_content[:1000] + "..." if len(blog_content) > 1000 else blog_content)
        
        # 6. 통계 정보
        print(f"\n=== 통계 정보 ===")
        print(f"- 총 글자 수: {len(blog_content):,}자")
        print(f"- 포함된 논문 수: {len(recent_papers)}편")
        print(f"- 카테고리 수: {len(categories)}개")
        
        # 로그 기록
        with open("step_log.txt", "a", encoding='utf-8') as log:
            log.write(f"Step 6 완료 - 블로그 포스트 생성: {datetime.now()} - {blog_file}\n")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 로그 기록
        with open("step_log.txt", "a", encoding='utf-8') as log:
            log.write(f"Step 6 오류: {datetime.now()} - {str(e)}\n")

if __name__ == "__main__":
    test_blog_generation()
