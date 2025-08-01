from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import List, Dict, Any
from datetime import datetime

from scripts.database import Paper, Author, Category, init_db
from scripts.logger import setup_logging
from scripts.categorizer import PaperCategorizer

class DatabaseManager:
    def __init__(self, db_path: str):
        self.logger = setup_logging()
        self.engine = init_db(db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.categorizer = PaperCategorizer()

    def add_paper(self, paper_data: Dict[str, Any]) -> bool:
        """새로운 논문 정보를 데이터베이스에 추가합니다."""
        session = self.Session()
        try:
            # 이미 존재하는 논문인지 확인
            existing_paper = session.query(Paper).filter_by(pmid=paper_data['pmid']).first()
            if existing_paper:
                self.logger.info(f"Paper with PMID {paper_data['pmid']} already exists")
                return False

            # 새 논문 객체 생성
            # 논문 카테고리 분류
            categories = self.categorizer.categorize_paper(
                paper_data['title'],
                paper_data['abstract']
            )
            
            # 논문 객체 생성
            new_paper = Paper(
                pmid=paper_data['pmid'],
                title=paper_data['title'],
                abstract=paper_data['abstract'],
                journal_name=paper_data['journal']['name'],
                journal_volume=paper_data['journal']['volume'],
                journal_issue=paper_data['journal']['issue'],
                publication_year=paper_data['journal']['year']
            )
            
            # 카테고리 추가
            for category_name in categories:
                category = session.query(Category).filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                new_paper.categories.append(category)

            # 저자 정보 추가
            for idx, author_name in enumerate(paper_data['authors'], 1):
                author = session.query(Author).filter_by(name=author_name).first()
                if not author:
                    author = Author(name=author_name)
                    session.add(author)
                new_paper.authors.append(author)

            session.add(new_paper)
            session.commit()
            self.logger.info(f"Successfully added paper with PMID {paper_data['pmid']}")
            return True

        except SQLAlchemyError as e:
            self.logger.error(f"Database error while adding paper: {str(e)}")
            session.rollback()
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while adding paper: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_all_categories(self) -> List[str]:
        """모든 카테고리 목록을 반환합니다."""
        session = self.Session()
        try:
            categories = session.query(Category.name).all()
            return [category[0] for category in categories]
        except Exception as e:
            self.logger.error(f"Error retrieving categories: {str(e)}")
            return []
        finally:
            session.close()
            
    def get_paper_by_pmid(self, pmid: str) -> Dict[str, Any]:
        """PMID로 논문 정보를 조회합니다."""
        session = self.Session()
        try:
            paper = session.query(Paper).filter_by(pmid=pmid).first()
            if not paper:
                return None

            return {
                'pmid': paper.pmid,
                'title': paper.title,
                'abstract': paper.abstract,
                'authors': [author.name for author in paper.authors],
                'journal': {
                    'name': paper.journal_name,
                    'volume': paper.journal_volume,
                    'issue': paper.journal_issue,
                    'year': paper.publication_year
                }
            }

        except Exception as e:
            self.logger.error(f"Error retrieving paper with PMID {pmid}: {str(e)}")
            return None
        finally:
            session.close()

    def get_all_papers(self):
        """모든 논문 정보를 조회합니다."""
        session = self.Session()
        try:
            papers = session.query(Paper).all()
            return papers
        except Exception as e:
            self.logger.error(f"Error retrieving all papers: {str(e)}")
            return []
        finally:
            session.close()

