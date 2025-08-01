from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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

def init_db(db_path):
    """데이터베이스 초기화 및 테이블 생성"""
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine
