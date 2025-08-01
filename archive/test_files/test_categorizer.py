import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.categorizer import PaperCategorizer
from scripts.db_manager import DatabaseManager
from scripts.pubmed_crawler import PubMedCrawler

def test_categorizer():
    # 카테고리 분류기 초기화
    categorizer = PaperCategorizer()
    print("\nLoaded categories:", list(categorizer.categories.keys()))
    
    # PubMed에서 논문 가져오기
    crawler = PubMedCrawler()
    papers = crawler.search_papers(days_back=1)
    
    if not papers:
        print("No papers found to categorize")
        return
    
    # 데이터베이스 매니저 초기화
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mci_papers.db')
    db_manager = DatabaseManager(db_path)
    
    # 각 논문 처리 및 카테고리 분류
    print(f"\nProcessing {len(papers)} papers...")
    for paper in papers[:5]:  # 테스트를 위해 처음 5개만 처리
        print(f"\nPaper: {paper['title']}")
        
        # 카테고리 분류
        categories = categorizer.categorize_paper(paper['title'], paper.get('abstract', ''))
        if categories:
            print(f"Categories: {', '.join(categories)}")
        else:
            print("No matching categories")
        
        # 데이터베이스에 저장
        success = db_manager.add_paper(paper)
        if success:
            print("Successfully saved to database")
        else:
            print("Failed to save to database")
    
    # 전체 통계 계산
    stats = categorizer.get_category_stats(papers)
    print("\nCategory Statistics:")
    for category, count in stats.items():
        print(f"{category}: {count} papers")

if __name__ == "__main__":
    test_categorizer()
