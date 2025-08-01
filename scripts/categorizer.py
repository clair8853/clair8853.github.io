import os
import yaml
import logging
from typing import List, Dict, Set
from scripts.logger import setup_logging

class PaperCategorizer:
    def __init__(self):
        self.logger = setup_logging()
        self.categories = self._load_category_rules()
        
    def _load_category_rules(self) -> Dict[str, Set[str]]:
        """카테고리 규칙을 로드합니다."""
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'category_rules.yaml'
            )
            
            with open(config_path, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
            
            # 키워드를 소문자로 변환하여 저장
            categories = {}
            for category, data in rules['categories'].items():
                categories[category] = {keyword.lower() for keyword in data['keywords']}
            
            self.logger.info(f"Loaded {len(categories)} categories with rules")
            return categories
            
        except Exception as e:
            self.logger.error(f"Error loading category rules: {str(e)}")
            return {}
            
    def categorize_paper(self, title: str, abstract: str) -> List[str]:
        """논문의 제목과 초록을 기반으로 카테고리를 할당합니다."""
        if not self.categories:
            self.logger.error("No category rules loaded")
            return []
            
        # 텍스트를 소문자로 변환
        text = (title + " " + abstract).lower()
        
        # 각 카테고리의 키워드 확인
        matched_categories = []
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in text:
                    matched_categories.append(category)
                    self.logger.debug(f"Matched category '{category}' with keyword '{keyword}'")
                    break  # 한 카테고리당 한 번만 매칭
        
        if matched_categories:
            self.logger.info(f"Found {len(matched_categories)} matching categories")
        else:
            self.logger.info("No matching categories found")
            
        return matched_categories
        
    def get_category_stats(self, papers: List[Dict]) -> Dict[str, int]:
        """논문 리스트에서 카테고리별 통계를 계산합니다."""
        stats = {category: 0 for category in self.categories.keys()}
        
        for paper in papers:
            categories = self.categorize_paper(paper['title'], paper.get('abstract', ''))
            for category in categories:
                stats[category] += 1
                
        return stats
