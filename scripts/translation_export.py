"""
Korean Translation Export Module
Exports papers needing Korean translation to CSV format for manual translation
"""

import os
import csv
import sqlite3
from datetime import datetime
import logging

class TranslationExporter:
    def __init__(self, db_path, export_dir=None):
        self.db_path = db_path
        self.export_dir = export_dir or os.path.join(os.path.dirname(__file__), '..', 'data', 'translations', 'exports')
        self.ensure_directories()
        
        # Setup logging
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'translations', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'export_log.txt'), encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.export_dir, exist_ok=True)
        
        # Create translations directory structure
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'translations')
        for subdir in ['exports', 'imports', 'imports/archive', 'logs']:
            os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

    def get_untranslated_papers(self, limit=None, status_filter='pending'):
        """Get papers that need Korean translation"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
        SELECT 
            p.id as paper_id,
            p.pmid,
            p.title,
            p.abstract as abstract_english,
            p.journal_name,
            p.publication_year,
            p.created_date,
            p.translation_status,
            p.abstract_korean,
            p.translator_notes
        FROM papers p
        WHERE p.translation_status = ?
        AND p.abstract IS NOT NULL
        AND p.abstract != ''
        ORDER BY p.created_date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
            
        cursor.execute(query, (status_filter,))
        papers = cursor.fetchall()
        conn.close()
        
        return papers

    def export_to_csv(self, papers, batch_id=None):
        """Export papers to CSV file for translation"""
        if not papers:
            self.logger.warning("No papers to export for translation")
            return None
            
        # Generate batch ID if not provided
        if not batch_id:
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"translation_batch_{batch_id}.csv"
        filepath = os.path.join(self.export_dir, filename)
        
        # CSV Headers
        headers = [
            'paper_id',
            'pmid', 
            'title',
            'abstract_english',
            'journal_name',
            'publication_year',
            'created_date',
            'translation_status',
            'abstract_korean',
            'translator_notes',
            'quality_check'  # For translator to mark quality
        ]
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers
                writer.writerow(headers)
                
                # Write paper data
                for paper in papers:
                    row = [
                        paper['paper_id'],
                        paper['pmid'],
                        paper['title'],
                        paper['abstract_english'],
                        paper['journal_name'],
                        paper['publication_year'],
                        paper['created_date'],
                        paper['translation_status'],
                        paper['abstract_korean'] or '',  # Empty if no existing translation
                        paper['translator_notes'] or '',
                        ''  # Empty quality_check for translator to fill
                    ]
                    writer.writerow(row)
            
            # Record batch in database
            self.record_batch(batch_id, filepath, len(papers))
            
            self.logger.info(f"✅ Exported {len(papers)} papers to {filepath}")
            self.logger.info(f"📦 Batch ID: {batch_id}")
            
            return {
                'batch_id': batch_id,
                'filepath': filepath,
                'paper_count': len(papers),
                'status': 'exported'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Export failed: {e}")
            return None

    def record_batch(self, batch_id, filepath, paper_count):
        """Record export batch in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO translation_batches 
                (batch_id, export_date, file_path, total_papers, completed_papers, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (batch_id, datetime.now(), filepath, paper_count, 0, 'exported'))
            
            conn.commit()
            self.logger.info(f"📝 Batch {batch_id} recorded in database")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to record batch: {e}")
        finally:
            conn.close()

    def create_template_file(self):
        """Create a template CSV file for translators"""
        template_path = os.path.join(self.export_dir, 'translation_template.csv')
        
        headers = [
            'paper_id',
            'pmid',
            'title',
            'abstract_english',
            'journal_name',
            'publication_year',
            'created_date',
            'translation_status',
            'abstract_korean',
            'translator_notes', 
            'quality_check'
        ]
        
        sample_data = [
            ['1', '12345678', 'Sample Paper Title', 'Sample English abstract text...', 'Journal Name', '2024', '2024-01-01', 'pending', '', '', ''],
            ['', '', '', '▲ Translate to Korean ▲', '', '', '', '', '▼ Korean translation here ▼', '▼ Notes here ▼', '▼ OK/Review ▼']
        ]
        
        with open(template_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(sample_data)
        
        self.logger.info(f"📄 Template file created: {template_path}")
        return template_path

    def export_batch(self, limit=50, status_filter='pending'):
        """Complete batch export process"""
        self.logger.info(f"🚀 Starting Korean translation export...")
        self.logger.info(f"📊 Filter: {status_filter}, Limit: {limit}")
        
        # Get papers needing translation
        papers = self.get_untranslated_papers(limit=limit, status_filter=status_filter)
        
        if not papers:
            self.logger.info("ℹ️  No papers found needing translation")
            return None
        
        # Export to CSV
        result = self.export_to_csv(papers)
        
        if result:
            self.logger.info(f"🎉 Export completed successfully!")
            self.logger.info(f"📁 File: {result['filepath']}")
            self.logger.info(f"📝 Papers: {result['paper_count']}")
            
            # Create template if it doesn't exist
            template_path = os.path.join(self.export_dir, 'translation_template.csv')
            if not os.path.exists(template_path):
                self.create_template_file()
        
        return result

def main():
    """Command line interface for translation export"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export papers for Korean translation')
    parser.add_argument('--limit', type=int, default=50, help='Maximum number of papers to export')
    parser.add_argument('--status', default='pending', help='Translation status filter')
    parser.add_argument('--db', help='Database path (optional)')
    
    args = parser.parse_args()
    
    # Default database path
    if not args.db:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mci_papers.db')
    else:
        db_path = args.db
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    exporter = TranslationExporter(db_path)
    result = exporter.export_batch(limit=args.limit, status_filter=args.status)
    
    if result:
        print(f"\n✅ Export Summary:")
        print(f"   Batch ID: {result['batch_id']}")
        print(f"   File: {result['filepath']}")
        print(f"   Papers: {result['paper_count']}")
        print(f"\n📝 Next steps:")
        print(f"   1. Open CSV file in Excel/Google Sheets")
        print(f"   2. Add Korean translations in 'abstract_korean' column")
        print(f"   3. Update 'translation_status' to 'completed'")
        print(f"   4. Use import script to load translations back")

if __name__ == "__main__":
    main()
