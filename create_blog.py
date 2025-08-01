from scripts.db_manager import DatabaseManager
from scripts.analyzer import TrendAnalyzer
from scripts.blog_generator import generate_blog_post
from datetime import datetime
import os

# 데이터베이스 연결
db = DatabaseManager('data/mci_papers.db')
analyzer = TrendAnalyzer(db)

# 현재 날짜
current_date = datetime.now().strftime('%Y%m%d')

# 트렌드 리포트 생성
report = analyzer.generate_trend_report(months=12)

# 최신 논문들 가져오기
latest_papers = db.get_all_papers()

# 카테고리들 가져오기
categories = list(db.get_all_categories())

print(f'논문 수: {len(latest_papers)}')
print(f'카테고리: {categories}')

# 블로그 포스트 생성
blog_post = generate_blog_post(
    trend_report=report,
    date=current_date,
    categories=categories,
    papers=latest_papers[-10:]  # 최신 10개
)

# 파일 저장
blog_dir = 'blog/content/posts'
os.makedirs(blog_dir, exist_ok=True)
post_path = f'{blog_dir}/detailed-report-{current_date}.md'
with open(post_path, 'w', encoding='utf-8') as f:
    f.write(blog_post)

print(f'새 블로그 포스트 생성: {post_path}')
