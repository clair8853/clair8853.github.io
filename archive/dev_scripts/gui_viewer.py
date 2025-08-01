#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI 논문 데이터베이스 GUI 뷰어
Streamlit을 사용한 웹 인터페이스
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

# 페이지 설정
st.set_page_config(
    page_title="MCI 논문 데이터베이스",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_papers():
    """논문 데이터를 로드합니다."""
    db_manager = DatabaseManager('data/mci_papers.db')
    papers = db_manager.get_all_papers()
    return papers

def format_paper_data(papers):
    """논문 데이터를 DataFrame으로 변환합니다."""
    data = []
    for paper in papers:
        categories = [cat.name for cat in paper.categories] if paper.categories else []
        authors = [author.name for author in paper.authors] if paper.authors else []
        
        data.append({
            'PMID': paper.pmid,
            'Title': paper.title,
            'Journal': paper.journal_name,
            'Year': paper.publication_year,
            'Volume': paper.journal_volume,
            'Issue': paper.journal_issue,
            'Categories': ', '.join(categories),
            'Authors': ', '.join(authors[:3]) + ('...' if len(authors) > 3 else ''),
            'Abstract': paper.abstract[:200] + '...' if paper.abstract and len(paper.abstract) > 200 else paper.abstract
        })
    
    return pd.DataFrame(data)

def main():
    # 헤더
    st.title("🧠 MCI 논문 데이터베이스")
    st.markdown("---")
    
    # 사이드바
    st.sidebar.title("📊 필터 옵션")
    
    # 데이터 로드
    try:
        papers = load_papers()
        if not papers:
            st.error("❌ 데이터베이스에 논문이 없습니다.")
            return
        
        df = format_paper_data(papers)
        
        # 통계 정보
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("총 논문 수", len(papers))
        with col2:
            unique_journals = df['Journal'].nunique()
            st.metric("저널 수", unique_journals)
        with col3:
            year_range = f"{df['Year'].min()}-{df['Year'].max()}"
            st.metric("연도 범위", year_range)
        with col4:
            # 카테고리 수 계산
            all_categories = set()
            for paper in papers:
                if paper.categories:
                    all_categories.update([cat.name for cat in paper.categories])
            st.metric("카테고리 수", len(all_categories))
        
        st.markdown("---")
        
        # 사이드바 필터
        # 연도 필터
        years = sorted(df['Year'].unique())
        selected_years = st.sidebar.multiselect(
            "📅 연도 선택",
            years,
            default=years
        )
        
        # 카테고리 필터
        all_categories = set()
        for paper in papers:
            if paper.categories:
                all_categories.update([cat.name for cat in paper.categories])
        
        category_mapping = {
            'clinical_study': '🏥 임상연구',
            'neuroscience': '🧬 신경과학',
            'biomarker': '🔬 바이오마커',
            'ai_ml': '🤖 AI/머신러닝',
            'imaging': '📸 이미징',
            'cognitive_assessment': '🧪 인지평가'
        }
        
        category_options = [category_mapping.get(cat, cat) for cat in sorted(all_categories)]
        selected_categories = st.sidebar.multiselect(
            "🏷️ 카테고리 선택",
            category_options,
            default=category_options
        )
        
        # 필터 적용
        filtered_df = df[df['Year'].isin(selected_years)]
        
        if selected_categories:
            # 카테고리 필터링
            category_filter = filtered_df['Categories'].apply(
                lambda x: any(cat in x for cat in selected_categories)
            )
            filtered_df = filtered_df[category_filter]
        
        # 검색 기능
        search_term = st.sidebar.text_input("🔍 제목/초록 검색")
        if search_term:
            search_filter = (
                filtered_df['Title'].str.contains(search_term, case=False, na=False) |
                filtered_df['Abstract'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[search_filter]
        
        # 결과 표시
        st.subheader(f"📚 논문 목록 ({len(filtered_df)}편)")
        
        if len(filtered_df) == 0:
            st.warning("⚠️ 선택한 조건에 맞는 논문이 없습니다.")
            return
        
        # 논문 카드 형태로 표시
        for idx, row in filtered_df.iterrows():
            with st.expander(f"**{row['Title']}** ({row['Year']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**📖 저널**: {row['Journal']}")
                    if row['Volume'] or row['Issue']:
                        volume_issue = []
                        if row['Volume']:
                            volume_issue.append(f"Vol.{row['Volume']}")
                        if row['Issue']:
                            volume_issue.append(f"Issue.{row['Issue']}")
                        st.write(f"**📄 권호**: {' '.join(volume_issue)}")
                    
                    st.write(f"**👥 저자**: {row['Authors']}")
                    st.write(f"**🏷️ 카테고리**: {row['Categories']}")
                    
                    if row['Abstract']:
                        st.write("**📝 초록**:")
                        st.write(row['Abstract'])
                
                with col2:
                    st.write(f"**🔗 PMID**: [{row['PMID']}](https://pubmed.ncbi.nlm.nih.gov/{row['PMID']}/)")
                    if st.button(f"PubMed 열기", key=f"pmid_{row['PMID']}"):
                        st.write(f"👉 [PubMed에서 보기](https://pubmed.ncbi.nlm.nih.gov/{row['PMID']}/)")
        
        # 다운로드 기능
        st.markdown("---")
        st.subheader("💾 데이터 다운로드")
        
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📊 CSV 파일로 다운로드",
            data=csv,
            file_name=f"mci_papers_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
