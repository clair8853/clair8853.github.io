from scripts.categorizer import PaperCategorizer
from scripts.db_manager import DatabaseManager
from scripts.database import Category, Paper
from sqlalchemy.orm import joinedload

# Step 5: Re-categorize existing papers
print("=== Step 5: Re-categorizing Existing Papers ===")

categorizer = PaperCategorizer()
db_manager = DatabaseManager('data/mci_papers.db')

# Get session for bulk operations
session = db_manager.Session()
success_count = 0
error_count = 0

try:
    # Get all papers with relationships loaded
    from sqlalchemy.orm import joinedload
    papers = session.query(Paper).options(
        joinedload(Paper.categories),
        joinedload(Paper.authors)
    ).all()
    
    print(f"Found {len(papers)} papers to re-categorize")
    
    for i, paper in enumerate(papers, 1):
        try:
            # Clear existing categories
            paper.categories.clear()
            
            # Re-categorize
            categories = categorizer.categorize_paper(paper.title, paper.abstract)
            print(f"{i}/{len(papers)}: '{paper.title[:50]}...' -> {categories}")
            
            # Add new categories
            for category_name in categories:
                category = session.query(Category).filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                paper.categories.append(category)
            
            success_count += 1
            
            # Commit every 10 papers to avoid transaction issues
            if i % 10 == 0:
                session.commit()
                print(f"  -> Committed batch {i//10}")
                
        except Exception as e:
            print(f"Error processing paper {i}: {str(e)}")
            error_count += 1
            session.rollback()
    
    # Final commit
    session.commit()
    print(f"\n=== Re-categorization Complete ===")
    print(f"Success: {success_count}, Errors: {error_count}")
    
except Exception as e:
    print(f"Critical error: {str(e)}")
    session.rollback()
finally:
    session.close()

print("=== Step 5 Complete ===")
