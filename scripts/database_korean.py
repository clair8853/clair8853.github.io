"""
Database Migration Script for Korean Translation Support
Adds Korean translation fields to existing database schema
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, ForeignKey, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import text
import os
from datetime import datetime

Base = declarative_base()

# 논문과 카테고리의 다대다 관계를 위한 연결 테이블
paper_categories = Table(
    'paper_categories',
    Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Paper(Base):
    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True)
    pmid = Column(String(20), unique=True, nullable=False)
    title = Column(Text, nullable=False)
    abstract = Column(Text)
    journal_name = Column(String(255))
    journal_volume = Column(String(50))
    journal_issue = Column(String(50))
    publication_year = Column(String(4))
    created_date = Column(Date, default=datetime.now().date)
    
    # NEW: Korean Translation Fields
    abstract_korean = Column(Text, nullable=True)
    translation_status = Column(String(20), default='pending')  # pending, in_progress, completed, reviewed
    translation_date = Column(DateTime, nullable=True)
    translator_notes = Column(Text, nullable=True)
    
    # 관계 설정
    authors = relationship("Author", secondary="paper_authors")
    categories = relationship("Category", secondary=paper_categories)

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    papers = relationship("Paper", secondary="paper_authors")

class PaperAuthor(Base):
    __tablename__ = 'paper_authors'

    paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)
    author_order = Column(Integer)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)

class TranslationBatch(Base):
    """NEW: Track translation export/import batches"""
    __tablename__ = 'translation_batches'

    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50), unique=True, nullable=False)  # Format: YYYYMMDD_HHMMSS
    export_date = Column(DateTime, default=datetime.now)
    import_date = Column(DateTime, nullable=True)
    file_path = Column(String(255), nullable=False)
    total_papers = Column(Integer, default=0)
    completed_papers = Column(Integer, default=0)
    status = Column(String(20), default='exported')  # exported, in_progress, completed, imported
    notes = Column(Text, nullable=True)

def migrate_database(db_path):
    """Add Korean translation fields to existing database"""
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Create connection
    connection = engine.connect()
    
    try:
        # Check if new columns already exist
        result = connection.execute(text("PRAGMA table_info(papers)"))
        columns = [row[1] for row in result.fetchall()]
        
        # Add new columns if they don't exist
        if 'abstract_korean' not in columns:
            print("Adding Korean translation fields to papers table...")
            
            connection.execute(text("ALTER TABLE papers ADD COLUMN abstract_korean TEXT"))
            connection.execute(text("ALTER TABLE papers ADD COLUMN translation_status TEXT DEFAULT 'pending'"))
            connection.execute(text("ALTER TABLE papers ADD COLUMN translation_date DATETIME"))
            connection.execute(text("ALTER TABLE papers ADD COLUMN translator_notes TEXT"))
            
            # Update all existing papers to have 'pending' status
            connection.execute(text("UPDATE papers SET translation_status = 'pending' WHERE translation_status IS NULL"))
            
            connection.commit()
            print("✅ Korean translation fields added successfully!")
        else:
            print("✅ Korean translation fields already exist.")
        
        # Create new translation_batches table
        Base.metadata.create_all(engine, tables=[TranslationBatch.__table__])
        print("✅ Translation batches table created/verified!")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        connection.rollback()
    finally:
        connection.close()

def init_db(db_path):
    """데이터베이스 초기화 및 테이블 생성 (새 스키마 포함)"""
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    # Run migration on existing database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'mci_papers.db')
    
    if os.path.exists(db_path):
        print(f"🔄 Migrating existing database: {db_path}")
        migrate_database(db_path)
    else:
        print(f"🆕 Creating new database with Korean support: {db_path}")
        init_db(db_path)
        
    print("🎉 Database migration completed!")
