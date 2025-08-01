import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.db_manager import DatabaseManager
from scripts.pubmed_crawler import PubMedCrawler

def test_database():
    # 데이터베이스 경로 설정
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mci_papers.db')
    
    # 데이터베이스 매니저 초기화
    db_manager = DatabaseManager(db_path)
    
    # PubMed 크롤러로 데이터 가져오기
    crawler = PubMedCrawler()
    papers = crawler.search_papers(days_back=1)
    
    # 데이터베이스에 논문 추가
    for paper in papers:
        success = db_manager.add_paper(paper)
        if success:
            print(f"Added paper: {paper['title'][:100]}...")
        
    # 저장된 논문 확인
    if papers:
        first_paper = papers[0]
        retrieved_paper = db_manager.get_paper_by_pmid(first_paper['pmid'])
        if retrieved_paper:
            print("\nRetrieved paper from database:")
            print(f"Title: {retrieved_paper['title']}")
            print(f"Authors: {', '.join(retrieved_paper['authors'])}")
            print(f"Journal: {retrieved_paper['journal']['name']}")

if __name__ == "__main__":
    test_database()
