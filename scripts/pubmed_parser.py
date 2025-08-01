from xml.etree import ElementTree as ET
from typing import Optional
import logging

class PubMedXMLParser:
    @staticmethod
    def parse_article(article_elem: ET.Element) -> dict:
        """XML 형식의 논문 정보를 파싱하여 딕셔너리로 반환합니다."""
        try:
            # PMID 추출
            pmid = article_elem.find('.//PMID').text

            # 제목 추출
            title_elem = article_elem.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else ''

            # 저자 정보 추출
            authors = []
            author_list = article_elem.findall('.//Author')
            for author in author_list:
                last_name = author.find('LastName')
                fore_name = author.find('ForeName')
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")

            # 초록 추출
            abstract = ''
            abstract_texts = article_elem.findall('.//Abstract/AbstractText')
            for abstract_text in abstract_texts:
                if abstract_text.text:
                    abstract += abstract_text.text + ' '

            # 저널 정보 추출
            journal_elem = article_elem.find('.//Journal')
            journal_info = {
                'name': PubMedXMLParser._get_text(journal_elem, './/Title'),
                'volume': PubMedXMLParser._get_text(journal_elem, './/Volume'),
                'issue': PubMedXMLParser._get_text(journal_elem, './/Issue'),
                'year': PubMedXMLParser._get_text(journal_elem, './/Year')
            }

            return {
                'pmid': pmid,
                'title': title.strip(),
                'authors': authors,
                'abstract': abstract.strip(),
                'journal': journal_info
            }

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error parsing article {pmid if 'pmid' in locals() else 'unknown'}: {str(e)}")
            return None

    @staticmethod
    def _get_text(elem: Optional[ET.Element], xpath: str) -> str:
        """XML 요소에서 텍스트를 안전하게 추출합니다."""
        if elem is None:
            return ''
        found = elem.find(xpath)
        return found.text if found is not None else ''
