from scripts.db_manager import DatabaseManager

# Step 2: Database Verification
db = DatabaseManager('data/mci_papers.db')
papers = db.get_all_papers()
categories = db.get_all_categories()

print(f'=== Step 2: Database Verification Results ===')
print(f'Total papers: {len(papers)}')
print(f'Categories: {categories}')

if papers:
    print(f'Sample paper: {papers[0].title}')
    print(f'Sample abstract: {papers[0].abstract[:100]}...')
    print(f'Sample categories: {[cat.name for cat in papers[0].categories]}')
    
    # Check recent papers
    recent_papers = papers[-5:]
    print(f'\nRecent 5 papers:')
    for i, paper in enumerate(recent_papers, 1):
        print(f'{i}. {paper.title[:60]}...')
        
print(f'\n=== Step 2 Complete ===')
