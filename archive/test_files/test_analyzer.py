import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.analyzer import TrendAnalyzer
from scripts.db_manager import DatabaseManager
from scripts.pubmed_crawler import PubMedCrawler

def test_analyzer():
    # 데이터베이스 경로 설정
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mci_papers.db')
    
    # 데이터베이스 매니저 초기화
    db_manager = DatabaseManager(db_path)
    
    # 분석기 초기화
    analyzer = TrendAnalyzer(db_manager)
    
    # 출력 디렉토리 생성
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating trend analysis...")
    
    # 카테고리 트렌드 플롯 생성
    trend_plot_path = os.path.join(output_dir, 'category_trends.png')
    analyzer.plot_category_trends(months=12, save_path=trend_plot_path)
    print(f"Category trends plot saved to: {trend_plot_path}")
    
    # 키워드 분포 플롯 생성
    keyword_plot_path = os.path.join(output_dir, 'keyword_distribution.png')
    analyzer.plot_keyword_distribution(n=15, save_path=keyword_plot_path)
    print(f"Keyword distribution plot saved to: {keyword_plot_path}")
    
    # 트렌드 리포트 생성
    report = analyzer.generate_trend_report(months=12)
    report_path = os.path.join(output_dir, 'trend_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Trend report saved to: {report_path}")

if __name__ == "__main__":
    test_analyzer()
