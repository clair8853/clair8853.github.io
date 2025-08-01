import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sqlalchemy import func, and_
from scripts.logger import setup_logging
from scripts.database import Paper, Category

class TrendAnalyzer:
    def __init__(self, db_manager):
        self.logger = setup_logging()
        self.db_manager = db_manager
        
    def analyze_category_trends(self, months: int = 12) -> pd.DataFrame:
        """
        지정된 기간 동안의 카테고리별 논문 수 추이를 분석합니다.
        """
        session = self.db_manager.Session()
        try:
            # 날짜 범위 계산
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=months * 30)
            
            # 카테고리별 월간 논문 수 집계
            results = (session.query(
                func.strftime('%Y-%m', Paper.created_date).label('month'),
                Category.name,
                func.count(Paper.id).label('count'))
                .join(Paper.categories)
                .filter(Paper.created_date >= start_date)
                .group_by('month', Category.name)
                .all())
            
            # 결과를 DataFrame으로 변환
            df = pd.DataFrame(results, columns=['month', 'category', 'count'])
            df_pivot = df.pivot(index='month', columns='category', values='count').fillna(0)
            
            self.logger.info(f"Analyzed trends over {months} months")
            return df_pivot
            
        except Exception as e:
            self.logger.error(f"Error analyzing category trends: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def plot_category_trends(self, months: int = 12, save_path: Optional[str] = None):
        """
        카테고리별 트렌드를 시각화합니다.
        """
        try:
            df = self.analyze_category_trends(months)
            if df.empty:
                self.logger.error("No data available for plotting")
                return
                
            plt.figure(figsize=(12, 6))
            for category in df.columns:
                plt.plot(df.index, df[category], marker='o', label=category)
                
            plt.title(f'Paper Categories Trend Over {months} Months')
            plt.xlabel('Month')
            plt.ylabel('Number of Papers')
            plt.xticks(rotation=45)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path)
                self.logger.info(f"Saved trend plot to {save_path}")
            else:
                plt.show()
                
        except Exception as e:
            self.logger.error(f"Error plotting category trends: {str(e)}")
        finally:
            plt.close()
            


    def generate_trend_report(self, months: int = 12) -> str:
        """
        트렌드 분석 리포트를 생성합니다.
        """
        try:
            # 카테고리 트렌드 분석
            df = self.analyze_category_trends(months)
            
            # 리포트 생성
            report = ["# MCI Papers Trend Report", f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n"]
            
            # 카테고리 트렌드 섹션
            report.append("## Category Trends")
            for category in df.columns:
                total = int(df[category].sum())
                avg = df[category].mean()
                report.append(f"\n### {category}")
                report.append(f"- Total papers: {total}")
                report.append(f"- Average papers per month: {avg:.1f}")
                
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"Error generating trend report: {str(e)}")
            return f"Error generating report: {str(e)}"
