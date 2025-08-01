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
        """일일 업데이트를 실행합니다."""
        try:
            self.logger.info("Starting daily update...")
            
            # 새로운 논문 수집
            papers = self.crawler.search_papers(days_back=1)
            self.logger.info(f"Found {len(papers)} new papers")
            
            # 데이터베이스에 저장
            for paper in papers:
                success = self.db_manager.add_paper(paper)
                if not success:
                    self.logger.warning(f"Failed to add paper: {paper['pmid']}")
            
            # 트렌드 분석 및 리포트 생성
            current_date = datetime.now().strftime('%Y%m%d')
            
            # 카테고리 트렌드 플롯
            trend_plot_path = os.path.join(self.output_path, f'category_trends_{current_date}.png')
            self.analyzer.plot_category_trends(months=12, save_path=trend_plot_path)
            

            
            # 트렌드 리포트 생성
            report = self.analyzer.generate_trend_report(months=12)
            
            # 블로그 포스트 생성
            from scripts.blog_generator import generate_blog_post
            categories = list(self.db_manager.get_all_categories())
            latest_papers = self.db_manager.get_all_papers()[-20:]  # 최신 20개 논문
            
            blog_post = generate_blog_post(
                trend_report=report,
                date=current_date,
                categories=categories,
                papers=latest_papers
            )
            
            # 블로그 포스트 저장
            blog_dir = os.path.join(self.base_path, 'blog', 'content', 'posts')
            os.makedirs(blog_dir, exist_ok=True)
            post_path = os.path.join(blog_dir, f'trend-report-{current_date}.md')
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(blog_post)
                
            self.logger.info(f"Blog post created: {post_path}")
            
            self.logger.info("Daily update completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during daily update: {str(e)}")
    
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
    parser = argparse.ArgumentParser(description='MCI Papers Pipeline')
    parser.add_argument('--daily', action='store_true', help='Run daily update once')
    parser.add_argument('--scheduler', action='store_true', help='Start scheduler')
    args = parser.parse_args()
    
    pipeline = MCIPapersPipeline()
    
    if args.daily:
        pipeline.run_daily_update()
    elif args.scheduler:
        pipeline.start_scheduler()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
