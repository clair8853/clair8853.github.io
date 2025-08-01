"""
Korean Translation Import Module
Imports Korean translations from CSV files back into the database
"""

import os
import csv
import sqlite3
from datetime import datetime
import logging
import shutil

class TranslationImporter:
    def __init__(self, db_path, import_dir=None):
        self.db_path = db_path
        self.import_dir = import_dir or os.path.join(os.path.dirname(__file__), '..', 'data', 'translations', 'imports')
        self.archive_dir = os.path.join(self.import_dir, 'archive')
        self.ensure_directories()
        
        # Setup logging
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'translations', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'import_log.txt'), encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.import_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)

    def validate_csv_file(self, filepath):
        """Validate CSV file format and content"""
        if not os.path.exists(filepath):
            self.logger.error(f"❌ File not found: {filepath}")
            return False, "File not found"
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Check required columns
                required_columns = ['paper_id', 'abstract_korean', 'translation_status']
                missing_columns = [col for col in required_columns if col not in reader.fieldnames]
                
                if missing_columns:
                    return False, f"Missing required columns: {missing_columns}"
                
                # Check if there's any data
                rows = list(reader)
                if not rows:
                    return False, "No data rows found"
                
                # Validate each row
                valid_rows = 0
                for i, row in enumerate(rows, 1):
                    if not row['paper_id']:
                        continue  # Skip empty rows
                    
                    # Check paper_id is numeric
                    try:
                        int(row['paper_id'])
                    except ValueError:
                        return False, f"Invalid paper_id in row {i}: {row['paper_id']}"
                    
                    # Check translation status
                    valid_statuses = ['pending', 'in_progress', 'completed', 'reviewed']
                    if row['translation_status'] not in valid_statuses:
                        return False, f"Invalid translation_status in row {i}: {row['translation_status']}"
                    
                    valid_rows += 1
                
                if valid_rows == 0:
                    return False, "No valid translation rows found"
                
                self.logger.info(f"✅ CSV validation passed: {valid_rows} valid rows")
                return True, f"Valid CSV with {valid_rows} rows"
                
        except Exception as e:
            return False, f"CSV validation error: {e}"

    def import_translations(self, filepath, dry_run=False):
        """Import Korean translations from CSV file"""
        self.logger.info(f"🔄 Starting import from: {os.path.basename(filepath)}")
        
        # Validate file first
        is_valid, message = self.validate_csv_file(filepath)
        if not is_valid:
            self.logger.error(f"❌ Validation failed: {message}")
            return {'success': False, 'error': message}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported_count = 0
        updated_count = 0
        error_count = 0
        errors = []
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for i, row in enumerate(reader, 1):
                    if not row['paper_id']:
                        continue  # Skip empty rows
                    
                    try:
                        paper_id = int(row['paper_id'])
                        abstract_korean = row['abstract_korean'].strip()
                        translation_status = row['translation_status'].strip()
                        translator_notes = row.get('translator_notes', '').strip()
                        
                        # Skip if no Korean translation provided
                        if not abstract_korean and translation_status in ['completed', 'reviewed']:
                            self.logger.warning(f"⚠️  Row {i}: Status is '{translation_status}' but no Korean abstract provided")
                            continue
                        
                        # Check if paper exists
                        cursor.execute("SELECT id FROM papers WHERE id = ?", (paper_id,))
                        if not cursor.fetchone():
                            error_msg = f"Paper ID {paper_id} not found in database"
                            self.logger.warning(f"⚠️  Row {i}: {error_msg}")
                            errors.append(f"Row {i}: {error_msg}")
                            error_count += 1
                            continue
                        
                        if dry_run:
                            self.logger.info(f"[DRY RUN] Would update paper {paper_id}: {translation_status}")
                            imported_count += 1
                            continue
                        
                        # Update the paper with Korean translation
                        update_query = """
                        UPDATE papers 
                        SET abstract_korean = ?, 
                            translation_status = ?,
                            translation_date = ?,
                            translator_notes = ?
                        WHERE id = ?
                        """
                        
                        cursor.execute(update_query, (
                            abstract_korean,
                            translation_status,
                            datetime.now(),
                            translator_notes,
                            paper_id
                        ))
                        
                        if cursor.rowcount > 0:
                            imported_count += 1
                            if abstract_korean:  # Only count as updated if Korean text was added
                                updated_count += 1
                            self.logger.info(f"✅ Updated paper {paper_id}: {translation_status}")
                        
                    except Exception as e:
                        error_msg = f"Error processing row {i}: {e}"
                        self.logger.error(f"❌ {error_msg}")
                        errors.append(error_msg)
                        error_count += 1
            
            if not dry_run:
                conn.commit()
                self.logger.info(f"💾 Database changes committed")
            
            # Generate summary
            result = {
                'success': True,
                'imported_count': imported_count,
                'updated_count': updated_count,
                'error_count': error_count,
                'errors': errors,
                'dry_run': dry_run
            }
            
            self.logger.info(f"📊 Import Summary:")
            self.logger.info(f"   Processed: {imported_count}")
            self.logger.info(f"   With Korean text: {updated_count}")
            self.logger.info(f"   Errors: {error_count}")
            
            return result
            
        except Exception as e:
            conn.rollback()
            error_msg = f"Import failed: {e}"
            self.logger.error(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        
        finally:
            conn.close()

    def archive_imported_file(self, filepath, batch_id=None):
        """Move imported file to archive directory"""
        if not os.path.exists(filepath):
            return False
        
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if batch_id:
            archived_name = f"imported_{batch_id}_{timestamp}.csv"
        else:
            name, ext = os.path.splitext(filename)
            archived_name = f"imported_{name}_{timestamp}{ext}"
        
        archived_path = os.path.join(self.archive_dir, archived_name)
        
        try:
            shutil.move(filepath, archived_path)
            self.logger.info(f"📁 File archived: {archived_name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to archive file: {e}")
            return False

    def update_batch_status(self, batch_id, completed_papers):
        """Update translation batch status in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE translation_batches 
                SET import_date = ?,
                    completed_papers = ?,
                    status = 'imported'
                WHERE batch_id = ?
            """, (datetime.now(), completed_papers, batch_id))
            
            conn.commit()
            self.logger.info(f"📝 Batch {batch_id} status updated")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update batch status: {e}")
        finally:
            conn.close()

    def list_import_files(self):
        """List available CSV files for import"""
        if not os.path.exists(self.import_dir):
            return []
        
        csv_files = [f for f in os.listdir(self.import_dir) 
                    if f.endswith('.csv') and os.path.isfile(os.path.join(self.import_dir, f))]
        
        return csv_files

    def import_batch(self, filename, dry_run=False, auto_archive=True):
        """Complete batch import process"""
        filepath = os.path.join(self.import_dir, filename)
        
        self.logger.info(f"🚀 Starting Korean translation import...")
        self.logger.info(f"📁 File: {filename}")
        self.logger.info(f"🔍 Dry run: {dry_run}")
        
        # Import translations
        result = self.import_translations(filepath, dry_run=dry_run)
        
        if result['success'] and not dry_run:
            # Extract batch_id from filename if possible
            batch_id = None
            if 'translation_batch_' in filename:
                batch_id = filename.replace('translation_batch_', '').replace('.csv', '')
            
            # Update batch status
            if batch_id:
                self.update_batch_status(batch_id, result['updated_count'])
            
            # Archive file if requested
            if auto_archive:
                self.archive_imported_file(filepath, batch_id)
            
            self.logger.info(f"🎉 Import completed successfully!")
        
        return result

def main():
    """Command line interface for translation import"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import Korean translations from CSV')
    parser.add_argument('filename', help='CSV filename in imports directory')
    parser.add_argument('--dry-run', action='store_true', help='Validate only, do not import')
    parser.add_argument('--no-archive', action='store_true', help='Do not archive file after import')
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
    
    importer = TranslationImporter(db_path)
    
    # List available files if no specific file given
    if args.filename == 'list':
        files = importer.list_import_files()
        if files:
            print("📋 Available CSV files for import:")
            for i, f in enumerate(files, 1):
                print(f"   {i}. {f}")
        else:
            print("ℹ️  No CSV files found in imports directory")
        return
    
    result = importer.import_batch(
        args.filename, 
        dry_run=args.dry_run, 
        auto_archive=not args.no_archive
    )
    
    if result['success']:
        print(f"\n✅ Import Summary:")
        print(f"   Processed: {result['imported_count']}")
        print(f"   With Korean text: {result['updated_count']}")
        print(f"   Errors: {result['error_count']}")
        
        if result['errors']:
            print(f"\n⚠️  Errors encountered:")
            for error in result['errors'][:5]:  # Show first 5 errors
                print(f"   - {error}")
            if len(result['errors']) > 5:
                print(f"   ... and {len(result['errors']) - 5} more")
    else:
        print(f"❌ Import failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
