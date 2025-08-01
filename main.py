import os
import sys
import yaml
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from scripts.pubmed_crawler import PubMedCrawler
from scripts.db_manager import DatabaseManager
from scripts.analyzer import TrendAnalyzer
from scripts.logger import setup_logging

class MCIPapersPipeline:
    def __init__(self):
        self.logger = setup_logging()
        self.config = self._load_config()
        
        # 경로 설정
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.base_path, 'data')
        self.output_path = os.path.join(self.base_path, 'output')
        
        # 필요한 디렉토리 생성
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        
        # 컴포넌트 초기화
        self.db_path = os.path.join(self.data_path, 'mci_papers.db')
        self.db_manager = DatabaseManager(self.db_path)
        self.crawler = PubMedCrawler()
        self.analyzer = TrendAnalyzer(self.db_manager)
        
    def _load_config(self):
        """설정 파일을 로드합니다."""
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def run_daily_update(self):
        """일일 논문 수집 업데이트를 실행합니다."""
        try:
            self.logger.info("Starting daily paper collection...")
            
            # 새로운 논문 수집
            papers = self.crawler.search_papers(days_back=1)
            self.logger.info(f"Found {len(papers)} new papers")
            
            # 데이터베이스에 저장
            added_count = 0
            for paper in papers:
                success = self.db_manager.add_paper(paper)
                if success:
                    added_count += 1
                else:
                    self.logger.warning(f"Failed to add paper: {paper['pmid']}")
            
            self.logger.info(f"Successfully added {added_count} new papers to database")
            
            # 트렌드 분석 결과 저장 (선택적)
            current_date = datetime.now().strftime('%Y%m%d')
            
            # 카테고리 트렌드 플롯 생성
            try:
                trend_plot_path = os.path.join(self.output_path, f'category_trends_{current_date}.png')
                self.analyzer.plot_category_trends(months=12, save_path=trend_plot_path)
                self.logger.info(f"Trend plot saved: {trend_plot_path}")
            except Exception as e:
                self.logger.warning(f"Failed to generate trend plot: {str(e)}")
            
            # 트렌드 리포트 생성
            try:
                report = self.analyzer.generate_trend_report(months=12)
                report_path = os.path.join(self.output_path, f'trend_report_{current_date}.txt')
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                self.logger.info(f"Trend report saved: {report_path}")
            except Exception as e:
                self.logger.warning(f"Failed to generate trend report: {str(e)}")
            
            # 데이터베이스 상태 출력
            total_papers = len(self.db_manager.get_all_papers())
            self.logger.info(f"Total papers in database: {total_papers}")
            
            self.logger.info("Daily paper collection completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during daily update: {str(e)}")
    
    def run_collection_test(self):
        """논문 수집 테스트를 실행합니다."""
        try:
            self.logger.info("Starting collection test...")
            
            # 최근 7일간 논문 수집 테스트
            papers = self.crawler.search_papers(days_back=7)
            self.logger.info(f"Found {len(papers)} papers in last 7 days")
            
            # 몇 개 샘플 출력
            for i, paper in enumerate(papers[:3]):
                self.logger.info(f"Sample paper {i+1}: {paper['title'][:100]}...")
            
            # 데이터베이스 상태 확인
            total_papers = len(self.db_manager.get_all_papers())
            categories = self.db_manager.get_all_categories()
            
            self.logger.info(f"Database status:")
            self.logger.info(f"  - Total papers: {total_papers}")
            self.logger.info(f"  - Categories: {', '.join(categories)}")
            
        except Exception as e:
            self.logger.error(f"Error during collection test: {str(e)}")
    
    def start_scheduler(self):
        """스케줄러를 시작합니다."""
        scheduler = BlockingScheduler()
        scheduler_time = self.config['scheduler']['time']
        scheduler_timezone = self.config['scheduler']['timezone']
        
        scheduler.add_job(
            self.run_daily_update,
            'cron',
            hour=scheduler_time.split(':')[0],
            minute=scheduler_time.split(':')[1],
            timezone=scheduler_timezone
        )
        
        self.logger.info(f"Scheduler started. Will run daily at {scheduler_time} {scheduler_timezone}")
        scheduler.start()

def main():
    """메인 실행 함수"""
    import argparse
    parser = argparse.ArgumentParser(description='MCI Papers Research Tool')
    parser.add_argument('--daily', action='store_true', help='Run daily paper collection')
    parser.add_argument('--test', action='store_true', help='Test paper collection')
    parser.add_argument('--scheduler', action='store_true', help='Start scheduler for automatic collection')
    args = parser.parse_args()
    
    pipeline = MCIPapersPipeline()
    
    if args.daily:
        pipeline.run_daily_update()
    elif args.test:
        pipeline.run_collection_test()
    elif args.scheduler:
        pipeline.start_scheduler()
    else:
        print("MCI Papers Research Tool")
        print("사용법:")
        print("  --daily     : 일일 논문 수집 실행")
        print("  --test      : 논문 수집 테스트")
        print("  --scheduler : 자동 수집 스케줄러 시작")
        print("\n데이터 확인:")
        print("  python desktop_gui.py  : GUI로 논문 탐색")
        print("  python console_viewer.py : 콘솔에서 논문 확인")

if __name__ == "__main__":
    main()
