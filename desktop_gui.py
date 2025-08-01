#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCI 논문 데이터베이스 데스크톱 GUI 뷰어
Tkinter를 사용한 데스크톱 애플리케이션
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import webbrowser
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

class MCIPapersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 MCI 논문 데이터베이스")
        self.root.geometry("1200x800")
        
        # 언어 설정
        self.current_language = 'korean'  # 'korean' or 'english'
        
        # 데이터베이스 연결
        try:
            self.db_manager = DatabaseManager('data/mci_papers.db')
            self.papers = self.db_manager.get_all_papers()
            self.filtered_papers = self.papers.copy()
        except Exception as e:
            messagebox.showerror("오류", f"데이터베이스 연결 실패: {str(e)}")
            return
        
        self.setup_ui()
        self.refresh_papers_list()
        self.update_translation_stats()
    
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="🧠 MCI 논문 데이터베이스", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # 통계 정보
        stats_frame = ttk.LabelFrame(main_frame, text="📊 통계 정보", padding="5")
        stats_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        total_papers = len(self.papers)
        journals = set(paper.journal_name for paper in self.papers if paper.journal_name)
        years = set(paper.publication_year for paper in self.papers if paper.publication_year)
        categories = set()
        for paper in self.papers:
            if paper.categories:
                categories.update(cat.name for cat in paper.categories)
        
        ttk.Label(stats_frame, text=f"총 논문 수: {total_papers}편").grid(row=0, column=0, padx=10)
        ttk.Label(stats_frame, text=f"저널 수: {len(journals)}개").grid(row=0, column=1, padx=10)
        ttk.Label(stats_frame, text=f"연도 범위: {min(years) if years else 'N/A'}-{max(years) if years else 'N/A'}").grid(row=0, column=2, padx=10)
        
        # 번역 통계 (새로 추가)
        self.translation_stats_label = ttk.Label(stats_frame, text="")
        self.translation_stats_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(5, 0))
        
        # 언어 토글 버튼 (새로 추가)
        language_frame = ttk.Frame(stats_frame)
        language_frame.grid(row=1, column=2, columnspan=2, sticky=tk.E, padx=10, pady=(5, 0))
        
        ttk.Label(language_frame, text="초록 언어:").pack(side=tk.LEFT)
        self.language_var = tk.StringVar(value=self.current_language)
        
        korean_radio = ttk.Radiobutton(language_frame, text="한국어", variable=self.language_var, 
                                     value='korean', command=self.change_language)
        korean_radio.pack(side=tk.LEFT, padx=(5, 0))
        
        english_radio = ttk.Radiobutton(language_frame, text="English", variable=self.language_var,
                                      value='english', command=self.change_language)
        english_radio.pack(side=tk.LEFT, padx=(5, 0))
        
        # 필터 섹션
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 필터 및 검색", padding="5")
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 카테고리 필터
        ttk.Label(filter_frame, text="카테고리:").grid(row=0, column=0, padx=(0, 5))
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, width=20)
        category_options = ['전체'] + sorted(list(categories))
        category_combo['values'] = category_options
        category_combo.set('전체')
        category_combo.grid(row=0, column=1, padx=(0, 10))
        category_combo.bind('<<ComboboxSelected>>', self.filter_papers)
        
        # 연도 필터
        ttk.Label(filter_frame, text="연도:").grid(row=0, column=2, padx=(0, 5))
        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var, width=10)
        year_options = ['전체'] + sorted(list(years), reverse=True)
        year_combo['values'] = year_options
        year_combo.set('전체')
        year_combo.grid(row=0, column=3, padx=(0, 10))
        year_combo.bind('<<ComboboxSelected>>', self.filter_papers)
        
        # 검색
        ttk.Label(filter_frame, text="검색:").grid(row=0, column=4, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=5, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.filter_papers)
        
        # 초기화 버튼
        ttk.Button(filter_frame, text="초기화", command=self.reset_filters).grid(row=0, column=6)
        
        # 논문 목록 (왼쪽)
        list_frame = ttk.LabelFrame(main_frame, text="📚 논문 목록", padding="5")
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 리스트박스 with 스크롤바
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.papers_listbox = tk.Listbox(listbox_frame, height=20, width=50)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.papers_listbox.yview)
        self.papers_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.papers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.papers_listbox.bind('<<ListboxSelect>>', self.show_paper_details)
        
        # 논문 상세 정보 (오른쪽)
        detail_frame = ttk.LabelFrame(main_frame, text="📖 논문 상세 정보", padding="5")
        detail_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=20, width=70, wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # PubMed 링크 버튼
        self.pubmed_button = ttk.Button(detail_frame, text="🔗 PubMed에서 보기", command=self.open_pubmed)
        self.pubmed_button.pack(pady=(10, 0))
        self.current_pmid = None
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def refresh_papers_list(self):
        """논문 목록을 새로고침합니다."""
        self.papers_listbox.delete(0, tk.END)
        
        for i, paper in enumerate(self.filtered_papers):
            display_text = f"[{paper.publication_year}] {paper.title[:80]}..."
            self.papers_listbox.insert(tk.END, display_text)
    
    def filter_papers(self, event=None):
        """필터 조건에 따라 논문을 필터링합니다."""
        category = self.category_var.get()
        year = self.year_var.get()
        search_term = self.search_var.get().lower()
        
        self.filtered_papers = []
        
        for paper in self.papers:
            # 카테고리 필터
            if category != '전체':
                if not paper.categories or not any(cat.name == category for cat in paper.categories):
                    continue
            
            # 연도 필터
            if year != '전체':
                if str(paper.publication_year) != year:
                    continue
            
            # 검색 필터
            if search_term:
                title_match = search_term in paper.title.lower() if paper.title else False
                abstract_match = search_term in paper.abstract.lower() if paper.abstract else False
                if not (title_match or abstract_match):
                    continue
            
            self.filtered_papers.append(paper)
        
        self.refresh_papers_list()
        self.detail_text.delete(1.0, tk.END)
        self.current_pmid = None
    
    def reset_filters(self):
        """필터를 초기화합니다."""
        self.category_var.set('전체')
        self.year_var.set('전체')
        self.search_var.set('')
        self.filtered_papers = self.papers.copy()
        self.refresh_papers_list()
        self.detail_text.delete(1.0, tk.END)
        self.current_pmid = None
    
    def show_paper_details(self, event):
        """선택된 논문의 상세 정보를 표시합니다."""
        selection = self.papers_listbox.curselection()
        if not selection:
            return
        
        paper_index = selection[0]
        paper = self.filtered_papers[paper_index]
        self.current_pmid = paper.pmid
        
        # 상세 정보 텍스트 구성
        details = []
        details.append(f"📋 제목: {paper.title}\n")
        details.append(f"🔗 PMID: {paper.pmid}")
        details.append(f"📖 저널: {paper.journal_name}")
        
        if paper.journal_volume:
            details.append(f"📄 Volume: {paper.journal_volume}")
        if paper.journal_issue:
            details.append(f"📄 Issue: {paper.journal_issue}")
        
        details.append(f"📅 발행연도: {paper.publication_year}\n")
        
        # 저자 정보
        if paper.authors:
            authors = [author.name for author in paper.authors]
            details.append(f"👥 저자: {', '.join(authors[:5])}")
            if len(authors) > 5:
                details.append(f" (외 {len(authors)-5}명)")
            details.append("\n")
        
        # 카테고리 정보
        if paper.categories:
            category_names = [cat.name for cat in paper.categories]
            category_display = {
                'clinical_study': '🏥 임상연구',
                'neuroscience': '🧬 신경과학',
                'biomarker': '🔬 바이오마커',
                'ai_ml': '🤖 AI/머신러닝',
                'imaging': '📸 이미징',
                'cognitive_assessment': '🧪 인지평가'
            }
            display_categories = [category_display.get(cat, cat) for cat in category_names]
            details.append(f"🏷️ 카테고리: {', '.join(display_categories)}\n")
        
        # 번역 상태 표시 (새로 추가)
        translation_status = getattr(paper, 'translation_status', 'pending')
        status_icons = {
            'pending': '⏳ 번역 대기',
            'in_progress': '🔄 번역 진행중',
            'completed': '✅ 번역 완료',
            'reviewed': '🔍 검토 완료'
        }
        details.append(f"🌐 번역 상태: {status_icons.get(translation_status, translation_status)}")
        
        if hasattr(paper, 'translation_date') and paper.translation_date:
            details.append(f" ({paper.translation_date.strftime('%Y-%m-%d')})")
        details.append("\n")
        
        # 초록 (언어별 표시)
        if self.current_language == 'korean' and hasattr(paper, 'abstract_korean') and paper.abstract_korean:
            details.append(f"📝 초록 (한국어):\n{paper.abstract_korean}")
        elif paper.abstract:
            details.append(f"📝 초록 (English):\n{paper.abstract}")
        else:
            details.append("📝 초록: 사용할 수 없음")
        
        # 번역자 노트 (있는 경우)
        if hasattr(paper, 'translator_notes') and paper.translator_notes:
            details.append(f"\n📎 번역자 노트: {paper.translator_notes}")
        
        # 텍스트 표시
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(1.0, '\n'.join(details))
    
    def change_language(self):
        """언어 설정을 변경하고 현재 표시된 논문 상세 정보를 업데이트합니다."""
        self.current_language = self.language_var.get()
        
        # 현재 선택된 논문이 있으면 상세 정보를 다시 표시
        selection = self.papers_listbox.curselection()
        if selection:
            # 가짜 이벤트 객체 생성하여 show_paper_details 호출
            class FakeEvent:
                pass
            self.show_paper_details(FakeEvent())
    
    def update_translation_stats(self):
        """번역 통계 정보를 업데이트합니다."""
        try:
            # 번역 상태별 논문 수 계산
            translated_count = 0
            pending_count = 0
            in_progress_count = 0
            
            for paper in self.papers:
                status = getattr(paper, 'translation_status', 'pending')
                if status in ['completed', 'reviewed']:
                    translated_count += 1
                elif status == 'in_progress':
                    in_progress_count += 1
                else:
                    pending_count += 1
            
            total_papers = len(self.papers)
            translated_percentage = (translated_count / total_papers * 100) if total_papers > 0 else 0
            
            stats_text = f"🌐 번역 현황: {translated_count}/{total_papers}편 완료 ({translated_percentage:.1f}%)"
            if in_progress_count > 0:
                stats_text += f", {in_progress_count}편 진행중"
            
            self.translation_stats_label.config(text=stats_text)
            
        except Exception as e:
            self.translation_stats_label.config(text="🌐 번역 통계를 불러올 수 없습니다")
    
    def open_pubmed(self):
        """PubMed 페이지를 웹브라우저에서 엽니다."""
        if self.current_pmid:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{self.current_pmid}/"
            webbrowser.open(url)
        else:
            messagebox.showwarning("경고", "선택된 논문이 없습니다.")

def main():
    root = tk.Tk()
    app = MCIPapersGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
