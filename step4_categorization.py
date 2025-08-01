from scripts.categorizer import PaperCategorizer
from scripts.db_manager import DatabaseManager

# Step 4: Test categorization
print("=== Step 4: Categorization Analysis ===")

categorizer = PaperCategorizer()
db = DatabaseManager('data/mci_papers.db')

# Test categorizer with sample paper
papers = db.get_all_papers()
if papers:
    sample_paper = papers[0]
    print(f"Sample paper title: {sample_paper.title}")
    print(f"Sample paper abstract (first 200 chars): {sample_paper.abstract[:200]}...")
    
    # Test categorization
    categories = categorizer.categorize_paper(sample_paper.title, sample_paper.abstract)
    print(f"Categorizer result: {categories}")
    
    # Check existing categories in paper
    print(f"Paper's stored categories: {[cat.name for cat in sample_paper.categories]}")
    
    # Test a few more papers
    print("\nTesting categorization on 3 more papers:")
    for i, paper in enumerate(papers[1:4], 2):
        cats = categorizer.categorize_paper(paper.title, paper.abstract)
        stored_cats = [cat.name for cat in paper.categories]
        print(f"{i}. '{paper.title[:50]}...' -> New: {cats}, Stored: {stored_cats}")

print("=== Step 4 Complete ===")
