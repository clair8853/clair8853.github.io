import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pubmed_crawler import PubMedCrawler

def test_crawler():
    crawler = PubMedCrawler()
    papers = crawler.search_papers(days_back=1)
    
    if papers:
        print(f"Found {len(papers)} papers:")
        for paper in papers:
            print(f"Title: {paper.get('title', 'N/A')}")
            print(f"Authors: {paper.get('authors', 'N/A')}")
            print(f"Abstract: {paper.get('abstract', 'N/A')[:200]}...")
            print("-" * 80)
    else:
        print("No papers found or error occurred")

if __name__ == "__main__":
    test_crawler()
