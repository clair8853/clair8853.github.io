import os
import yaml
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from xml.etree import ElementTree as ET
from scripts.logger import setup_logging

class PubMedCrawler:
    def __init__(self):
        self.logger = setup_logging()
        self.config = self._load_config()
        self.base_url = self.config['pubmed']['api_base_url']
        self.max_requests = self.config['pubmed']['max_requests_per_day']
        self.retry_attempts = self.config['pubmed']['retry_attempts']
        self.retry_delay = self.config['pubmed']['retry_delay']

    def _load_config(self) -> Dict[str, Any]:
        """설정 파일을 로드합니다."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_keywords(self) -> List[str]:
        """검색 키워드를 로드합니다."""
        keywords_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'keywords.txt')
        with open(keywords_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def search_papers(self, days_back: int = 1, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """
        논문을 검색합니다.
        
        Args:
            days_back: 몇 일 전까지의 논문을 검색할지 지정 (start_date, end_date가 지정되지 않은 경우에만 사용)
            start_date: 검색 시작 날짜 (YYYY/MM/DD 형식)
            end_date: 검색 종료 날짜 (YYYY/MM/DD 형식)
        """
        """최근 논문들을 검색합니다."""
        keywords = self._load_keywords()
        query = ' OR '.join(f'"{keyword}"' for keyword in keywords)
        
        # 날짜 범위 설정
        if start_date and end_date:
            date_range = f"{start_date}:{end_date}[Date - Create]"
        else:
            end = datetime.now()
            start = end - timedelta(days=days_back)
            date_range = f"{start.strftime('%Y/%m/%d')}:{end.strftime('%Y/%m/%d')}[Date - Create]"
        
        try:
            # PubMed 검색 API 호출
            search_url = f"{self.base_url}/esearch.fcgi"
            params = {
                'db': 'pubmed',
                'term': f"({query}) AND {date_range}",
                'retmode': 'json',
                'retmax': 100
            }
            
            self.logger.info(f"Searching PubMed with query: {query}")
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            search_results = response.json()
            pmids = search_results['esearchresult']['idlist']
            
            if not pmids:
                self.logger.info("No new papers found")
                return []
            
            # 논문 상세 정보 가져오기
            self.logger.info(f"Found {len(pmids)} papers. Fetching details...")
            fetch_url = f"{self.base_url}/efetch.fcgi"
            params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml',
            }
            
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            
            # XML 응답을 파싱하여 필요한 정보 추출
            return self.parse_paper_details(response.text)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error during PubMed API request: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return []

    def parse_paper_details(self, xml_content: str) -> List[Dict[str, Any]]:
        """XML 형식의 논문 정보를 파싱합니다."""
        from scripts.pubmed_parser import PubMedXMLParser
        
        try:
            root = ET.fromstring(xml_content)
            articles = root.findall('.//PubmedArticle')
            
            results = []
            for article in articles:
                paper_info = PubMedXMLParser.parse_article(article)
                if paper_info:
                    results.append(paper_info)
            
            self.logger.info(f"Successfully parsed {len(results)} papers")
            return results
            
        except ET.ParseError as e:
            self.logger.error(f"XML parsing error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error during parsing: {str(e)}")
            return []
