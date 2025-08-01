#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI Papers Database - Web GUI
Flask-based web interface for the MCI papers database
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import sqlite3
from sqlalchemy.orm import sessionmaker

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.database_korean import Paper, Author, Category, TranslationBatch, init_db
from scripts.db_manager import DatabaseManager
from scripts.translation_export import TranslationExporter
from scripts.translation_import import TranslationImporter

app = Flask(__name__)
app.secret_key = 'mci_papers_secret_key_2025'  # Change in production

# Configuration
class Config:
    DATABASE_PATH = os.path.join(project_root, 'data', 'mci_papers.db')
    UPLOAD_FOLDER = os.path.join(project_root, 'data', 'translations', 'imports')
    ALLOWED_EXTENSIONS = {'csv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config.from_object(Config)

# Initialize database components
db_manager = DatabaseManager(app.config['DATABASE_PATH'])
translation_exporter = TranslationExporter(app.config['DATABASE_PATH'])
translation_importer = TranslationImporter(app.config['DATABASE_PATH'])

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_translation_stats():
    """Get translation statistics for dashboard"""
    try:
        papers = db_manager.get_all_papers()
        total = len(papers)
        translated = 0
        in_progress = 0
        pending = 0
        
        for paper in papers:
            status = getattr(paper, 'translation_status', 'pending')
            if status in ['completed', 'reviewed']:
                translated += 1
            elif status == 'in_progress':
                in_progress += 1
            else:
                pending += 1
        
        return {
            'total': total,
            'translated': translated,
            'in_progress': in_progress,
            'pending': pending,
            'percentage': round((translated / total * 100) if total > 0 else 0, 1)
        }
    except Exception as e:
        app.logger.error(f"Error getting translation stats: {e}")
        return {'total': 0, 'translated': 0, 'in_progress': 0, 'pending': 0, 'percentage': 0}

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get basic statistics
        papers = db_manager.get_all_papers()
        total_papers = len(papers)
        
        # Get unique journals and years
        journals = set(paper.journal_name for paper in papers if paper.journal_name)
        years = set(paper.publication_year for paper in papers if paper.publication_year)
        
        # Get categories
        categories = db_manager.get_categories()
        
        # Get translation statistics
        translation_stats = get_translation_stats()
        
        # Get recent papers (last 10)
        recent_papers = papers[:10] if papers else []
        
        return render_template('index.html',
                             total_papers=total_papers,
                             total_journals=len(journals),
                             year_range=f"{min(years) if years else 'N/A'}-{max(years) if years else 'N/A'}",
                             total_categories=len(categories),
                             translation_stats=translation_stats,
                             recent_papers=recent_papers)
    
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        flash(f"오류가 발생했습니다: {str(e)}", 'error')
        return render_template('index.html', 
                             total_papers=0, total_journals=0, 
                             year_range="N/A", total_categories=0,
                             translation_stats={'total': 0, 'translated': 0, 'percentage': 0},
                             recent_papers=[])

@app.route('/papers')
def papers_list():
    """Papers listing page with filtering"""
    try:
        # Get filter parameters
        category_filter = request.args.get('category', 'all')
        year_filter = request.args.get('year', 'all')
        translation_filter = request.args.get('translation', 'all')
        search_query = request.args.get('search', '').strip()
        language = request.args.get('lang', 'korean')
        
        # Get all papers
        papers = db_manager.get_all_papers()
        
        # Apply filters
        filtered_papers = []
        for paper in papers:
            # Category filter
            if category_filter != 'all':
                paper_categories = [cat.name for cat in paper.categories] if paper.categories else []
                if category_filter not in paper_categories:
                    continue
            
            # Year filter
            if year_filter != 'all' and paper.publication_year != year_filter:
                continue
            
            # Translation filter
            if translation_filter != 'all':
                status = getattr(paper, 'translation_status', 'pending')
                if translation_filter == 'translated' and status not in ['completed', 'reviewed']:
                    continue
                elif translation_filter == 'pending' and status != 'pending':
                    continue
                elif translation_filter == 'in_progress' and status != 'in_progress':
                    continue
            
            # Search filter
            if search_query:
                search_text = f"{paper.title} {paper.abstract or ''}".lower()
                if hasattr(paper, 'abstract_korean') and paper.abstract_korean:
                    search_text += f" {paper.abstract_korean}"
                if search_query.lower() not in search_text:
                    continue
            
            filtered_papers.append(paper)
        
        # Get filter options
        categories = db_manager.get_categories()
        years = sorted(set(paper.publication_year for paper in papers if paper.publication_year), reverse=True)
        
        return render_template('paper_list.html',
                             papers=filtered_papers,
                             categories=categories,
                             years=years,
                             current_category=category_filter,
                             current_year=year_filter,
                             current_translation=translation_filter,
                             search_query=search_query,
                             language=language,
                             total_results=len(filtered_papers))
    
    except Exception as e:
        app.logger.error(f"Error in papers_list route: {e}")
        flash(f"논문 목록을 불러오는 중 오류가 발생했습니다: {str(e)}", 'error')
        return render_template('paper_list.html', papers=[], categories=[], years=[])

@app.route('/paper/<int:paper_id>')
def paper_detail(paper_id):
    """Individual paper detail page"""
    try:
        # Get paper by ID
        papers = db_manager.get_all_papers()
        paper = next((p for p in papers if p.id == paper_id), None)
        
        if not paper:
            flash('요청하신 논문을 찾을 수 없습니다.', 'error')
            return redirect(url_for('papers_list'))
        
        language = request.args.get('lang', 'korean')
        
        return render_template('paper_detail.html', paper=paper, language=language)
    
    except Exception as e:
        app.logger.error(f"Error in paper_detail route: {e}")
        flash(f"논문 상세 정보를 불러오는 중 오류가 발생했습니다: {str(e)}", 'error')
        return redirect(url_for('papers_list'))

@app.route('/translation')
def translation_management():
    """Translation management page"""
    try:
        # Get translation statistics
        translation_stats = get_translation_stats()
        
        # Get recent batches (this would need to be implemented in db_manager)
        recent_batches = []  # Placeholder
        
        # Get available import files
        import_files = translation_importer.list_import_files()
        
        return render_template('translation.html',
                             translation_stats=translation_stats,
                             recent_batches=recent_batches,
                             import_files=import_files)
    
    except Exception as e:
        app.logger.error(f"Error in translation_management route: {e}")
        flash(f"번역 관리 페이지를 불러오는 중 오류가 발생했습니다: {str(e)}", 'error')
        return render_template('translation.html',
                             translation_stats={'total': 0, 'translated': 0, 'percentage': 0},
                             recent_batches=[],
                             import_files=[])

@app.route('/export_translation', methods=['POST'])
def export_translation():
    """Export papers for translation"""
    try:
        limit = int(request.form.get('limit', 50))
        status_filter = request.form.get('status', 'pending')
        
        result = translation_exporter.export_batch(limit=limit, status_filter=status_filter)
        
        if result:
            flash(f'번역용 CSV 파일이 성공적으로 생성되었습니다. (배치 ID: {result["batch_id"]}, 논문 수: {result["paper_count"]}편)', 'success')
            return send_file(result['filepath'], as_attachment=True)
        else:
            flash('내보낼 논문이 없습니다.', 'warning')
            return redirect(url_for('translation_management'))
    
    except Exception as e:
        app.logger.error(f"Error in export_translation route: {e}")
        flash(f'번역 내보내기 중 오류가 발생했습니다: {str(e)}', 'error')
        return redirect(url_for('translation_management'))

@app.route('/import_translation', methods=['POST'])
def import_translation():
    """Import completed translations"""
    try:
        if 'file' not in request.files:
            flash('파일이 선택되지 않았습니다.', 'error')
            return redirect(url_for('translation_management'))
        
        file = request.files['file']
        if file.filename == '':
            flash('파일이 선택되지 않았습니다.', 'error')
            return redirect(url_for('translation_management'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Import the translations
            result = translation_importer.import_batch(filename, dry_run=False, auto_archive=True)
            
            if result['success']:
                flash(f'번역이 성공적으로 가져왔습니다. (처리: {result["imported_count"]}편, 한국어 번역: {result["updated_count"]}편)', 'success')
            else:
                flash(f'번역 가져오기 중 오류가 발생했습니다: {result.get("error", "알 수 없는 오류")}', 'error')
        else:
            flash('허용되지 않은 파일 형식입니다. CSV 파일만 업로드 가능합니다.', 'error')
    
    except Exception as e:
        app.logger.error(f"Error in import_translation route: {e}")
        flash(f'번역 가져오기 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('translation_management'))

@app.route('/api/search')
def api_search():
    """AJAX search endpoint"""
    try:
        query = request.args.get('q', '').strip()
        language = request.args.get('lang', 'korean')
        
        if not query:
            return jsonify({'results': []})
        
        papers = db_manager.get_all_papers()
        results = []
        
        for paper in papers[:50]:  # Limit to 50 results for performance
            search_text = f"{paper.title} {paper.abstract or ''}".lower()
            if hasattr(paper, 'abstract_korean') and paper.abstract_korean:
                search_text += f" {paper.abstract_korean}"
            
            if query.lower() in search_text:
                results.append({
                    'id': paper.id,
                    'title': paper.title,
                    'year': paper.publication_year,
                    'journal': paper.journal_name,
                    'pmid': paper.pmid
                })
        
        return jsonify({'results': results})
    
    except Exception as e:
        app.logger.error(f"Error in api_search route: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the Flask application
    print("🚀 MCI Papers Web GUI starting...")
    print(f"📊 Database: {app.config['DATABASE_PATH']}")
    print(f"🌐 Web interface will be available at: http://localhost:5000")
    print("📝 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
