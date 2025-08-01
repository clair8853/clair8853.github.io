#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI 논문 데이터베이스 콘솔 뷰어
데이터베이스의 논문들을 콘솔에서 확인
"""
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

def display_paper(paper, index):
    """논문 정보를 보기 좋게 출력합니다."""
    print(f"\n{'='*80}")
    print(f"📋 논문 {index + 1}")
    print(f"{'='*80}")
    print(f"📋 제목: {paper.title}")
    print(f"🔗 PMID: {paper.pmid}")
    print(f"📖 저널: {paper.journal_name}")
    
    if paper.journal_volume:
        print(f"📄 Volume: {paper.journal_volume}")
    if paper.journal_issue:
        print(f"📄 Issue: {paper.journal_issue}")
    
    print(f"📅 발행연도: {paper.publication_year}")
    
    # 저자 정보
    if paper.authors:
        authors = [author.name for author in paper.authors]
        print(f"👥 저자: {', '.join(authors[:3])}")
        if len(authors) > 3:
            print(f"      (외 {len(authors)-3}명)")
    
    # 카테고리 정보
    if paper.categories:
        category_names = [cat.name for cat in paper.categories]
        category_display = {
            'clinical_study': '🏥 임상연구',
            'neuroscience': '🧬 신경과학',
            'biomarker': '🔬 바이오마커',
            'ai_ml': '🤖 AI/머신러닝',
            'imaging': '📸 이미징',
            'cognitive_assessment': '🧪 인지평가'
        }
        display_categories = [category_display.get(cat, cat) for cat in category_names]
        print(f"🏷️ 카테고리: {', '.join(display_categories)}")
    
    # 초록
    if paper.abstract:
        print(f"\n📝 초록:")
        print("-" * 60)
        # 초록을 80자씩 줄바꿈
        abstract = paper.abstract
        for i in range(0, len(abstract), 80):
            print(abstract[i:i+80])
    
    print(f"\n🔗 PubMed 링크: https://pubmed.ncbi.nlm.nih.gov/{paper.pmid}/")

def main():
    print("🧠 MCI 논문 데이터베이스 콘솔 뷰어")
    print("=" * 50)
    
    try:
        # 데이터베이스 연결
        db_manager = DatabaseManager('data/mci_papers.db')
        papers = db_manager.get_all_papers()
        
        if not papers:
            print("❌ 데이터베이스에 논문이 없습니다.")
            return
        
        # 통계 정보
        print(f"\n📊 통계 정보")
        print(f"- 총 논문 수: {len(papers)}편")
        
        journals = set(paper.journal_name for paper in papers if paper.journal_name)
        print(f"- 저널 수: {len(journals)}개")
        
        years = set(paper.publication_year for paper in papers if paper.publication_year)
        if years:
            print(f"- 연도 범위: {min(years)}-{max(years)}")
        
        categories = set()
        for paper in papers:
            if paper.categories:
                categories.update(cat.name for cat in paper.categories)
        print(f"- 카테고리 수: {len(categories)}개")
        
        # 카테고리별 분포
        if categories:
            print(f"\n🏷️ 카테고리별 논문 수:")
            category_count = {}
            for paper in papers:
                if paper.categories:
                    for cat in paper.categories:
                        category_count[cat.name] = category_count.get(cat.name, 0) + 1
            
            category_display = {
                'clinical_study': '🏥 임상연구',
                'neuroscience': '🧬 신경과학',
                'biomarker': '🔬 바이오마커',
                'ai_ml': '🤖 AI/머신러닝',
                'imaging': '📸 이미징',
                'cognitive_assessment': '🧪 인지평가'
            }
            
            for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
                display_name = category_display.get(category, category)
                print(f"  - {display_name}: {count}편")
        
        # 사용자 선택
        while True:
            print(f"\n📚 논문 보기 옵션:")
            print("1. 최신 논문 5편 보기")
            print("2. 전체 논문 목록 보기")
            print("3. 카테고리별 논문 보기")
            print("4. 검색")
            print("5. 종료")
            
            choice = input("\n선택하세요 (1-5): ").strip()
            
            if choice == '1':
                print(f"\n📚 최신 논문 5편:")
                recent_papers = papers[-5:]
                for i, paper in enumerate(recent_papers):
                    display_paper(paper, i)
                    input("\n다음 논문을 보려면 Enter를 누르세요...")
            
            elif choice == '2':
                print(f"\n📚 전체 논문 목록 ({len(papers)}편):")
                for i, paper in enumerate(papers):
                    display_paper(paper, i)
                    if (i + 1) % 3 == 0:  # 3편마다 멈춤
                        response = input(f"\n계속 보시겠습니까? (y/n): ").strip().lower()
                        if response != 'y':
                            break
            
            elif choice == '3':
                if not categories:
                    print("❌ 카테고리 정보가 없습니다.")
                    continue
                
                print(f"\n🏷️ 카테고리 선택:")
                category_list = sorted(list(categories))
                for i, cat in enumerate(category_list, 1):
                    display_name = category_display.get(cat, cat)
                    count = sum(1 for paper in papers 
                              if paper.categories and any(c.name == cat for c in paper.categories))
                    print(f"{i}. {display_name} ({count}편)")
                
                try:
                    cat_choice = int(input("카테고리 번호를 선택하세요: ")) - 1
                    if 0 <= cat_choice < len(category_list):
                        selected_category = category_list[cat_choice]
                        filtered_papers = [paper for paper in papers 
                                         if paper.categories and any(c.name == selected_category for c in paper.categories)]
                        
                        display_name = category_display.get(selected_category, selected_category)
                        print(f"\n📚 {display_name} 카테고리 논문 ({len(filtered_papers)}편):")
                        
                        for i, paper in enumerate(filtered_papers):
                            display_paper(paper, i)
                            if (i + 1) % 2 == 0:  # 2편마다 멈춤
                                response = input(f"\n계속 보시겠습니까? (y/n): ").strip().lower()
                                if response != 'y':
                                    break
                    else:
                        print("❌ 잘못된 선택입니다.")
                except ValueError:
                    print("❌ 숫자를 입력해주세요.")
            
            elif choice == '4':
                search_term = input("검색어를 입력하세요: ").strip().lower()
                if search_term:
                    matching_papers = []
                    for paper in papers:
                        if (search_term in paper.title.lower() if paper.title else False) or \
                           (search_term in paper.abstract.lower() if paper.abstract else False):
                            matching_papers.append(paper)
                    
                    if matching_papers:
                        print(f"\n🔍 검색 결과: '{search_term}' ({len(matching_papers)}편)")
                        for i, paper in enumerate(matching_papers):
                            display_paper(paper, i)
                            if (i + 1) % 2 == 0:  # 2편마다 멈춤
                                response = input(f"\n계속 보시겠습니까? (y/n): ").strip().lower()
                                if response != 'y':
                                    break
                    else:
                        print(f"❌ '{search_term}'에 대한 검색 결과가 없습니다.")
            
            elif choice == '5':
                print("👋 프로그램을 종료합니다.")
                break
            
            else:
                print("❌ 잘못된 선택입니다. 1-5 사이의 숫자를 입력하세요.")
    
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
