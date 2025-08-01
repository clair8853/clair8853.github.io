#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI 논문 데이터베이스 빠른 확인 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

def main():
    print("🧠 MCI 논문 데이터베이스 빠른 확인")
    print("=" * 50)
    
    try:
        db_manager = DatabaseManager('data/mci_papers.db')
        papers = db_manager.get_all_papers()
        
        print(f"총 논문 수: {len(papers)}편")
        
        if not papers:
            print("❌ 데이터베이스에 논문이 없습니다.")
            return
        
        # 카테고리별 통계
        categories = {}
        for paper in papers:
            if paper.categories:
                for cat in paper.categories:
                    categories[cat.name] = categories.get(cat.name, 0) + 1
        
        print(f"\n🏷️ 카테고리별 논문 수:")
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
            print(f"  - {display_name}: {count}편")
        
        print(f"\n📚 최신 논문 5편:")
        print("-" * 80)
        
        recent_papers = papers[-5:]
        for i, paper in enumerate(recent_papers, 1):
            print(f"\n{i}. 📋 {paper.title}")
            print(f"   🔗 PMID: {paper.pmid}")
            print(f"   📖 저널: {paper.journal_name} ({paper.publication_year})")
            
            if paper.categories:
                cats = [category_display.get(cat.name, cat.name) for cat in paper.categories]
                print(f"   🏷️ 카테고리: {', '.join(cats)}")
            
            if paper.abstract:
                abstract_preview = paper.abstract[:200] + "..." if len(paper.abstract) > 200 else paper.abstract
                print(f"   📝 초록: {abstract_preview}")
            
            print(f"   🌐 PubMed: https://pubmed.ncbi.nlm.nih.gov/{paper.pmid}/")
            print("-" * 80)
        
        print(f"\n✅ 데이터베이스에 {len(papers)}편의 MCI 관련 논문이 저장되어 있습니다.")
        print("📖 각 논문은 카테고리별로 분류되어 있으며, PubMed 링크를 통해 원문을 확인할 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
