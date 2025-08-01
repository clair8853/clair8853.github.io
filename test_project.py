#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
프로젝트 기능 테스트 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.db_manager import DatabaseManager

def test_database():
    """데이터베이스 상태 확인"""
    print('=== 데이터베이스 상태 확인 ===')
    try:
        db_manager = DatabaseManager('data/mci_papers.db')
        papers = db_manager.get_all_papers()
        categories = db_manager.get_all_categories()

        print(f'총 논문 수: {len(papers)}편')
        print(f'카테고리 수: {len(categories)}개')
        print(f'카테고리: {categories}')

        if papers:
            latest = papers[-1]
            print(f'\n최신 논문 예시:')
            print(f'- 제목: {latest.title[:50]}...')
            print(f'- PMID: {latest.pmid}')
            print(f'- 저널: {latest.journal_name}')
            if latest.categories:
                cats = [cat.name for cat in latest.categories]
                print(f'- 카테고리: {cats}')
        
        print('\n데이터베이스 상태: 정상 ✅')
        return True
        
    except Exception as e:
        print(f'❌ 데이터베이스 오류: {str(e)}')
        return False

def test_main_functionality():
    """main.py 기능 테스트"""
    print('\n=== main.py 기능 테스트 ===')
    try:
        import main
        pipeline = main.MCIPapersPipeline()
        print('main.py 초기화: 정상 ✅')
        
        # 테스트 실행
        pipeline.run_collection_test()
        print('논문 수집 테스트: 정상 ✅')
        return True
        
    except Exception as e:
        print(f'❌ main.py 오류: {str(e)}')
        return False

def test_gui():
    """GUI 애플리케이션 테스트"""
    print('\n=== GUI 애플리케이션 테스트 ===')
    try:
        # desktop_gui.py 가져오기 테스트
        import desktop_gui
        print('desktop_gui.py 모듈 로드: 정상 ✅')
        
        # console_viewer.py 테스트
        import console_viewer
        print('console_viewer.py 모듈 로드: 정상 ✅')
        
        return True
        
    except Exception as e:
        print(f'❌ GUI 테스트 오류: {str(e)}')
        return False

def main():
    """전체 테스트 실행"""
    print('🧠 MCI Papers Research Tool - 기능 테스트')
    print('=' * 60)
    
    test_results = []
    
    # 테스트 실행
    test_results.append(test_database())
    test_results.append(test_main_functionality())
    test_results.append(test_gui())
    
    # 결과 요약
    print('\n' + '=' * 60)
    print('📊 테스트 결과 요약:')
    if all(test_results):
        print('✅ 모든 테스트 통과 - 프로젝트 정상 작동')
    else:
        print('❌ 일부 테스트 실패 - 문제 확인 필요')
        
    print('\n사용 가능한 기능:')
    print('- python main.py --test    : 논문 수집 테스트')
    print('- python main.py --daily   : 일일 논문 수집')
    print('- python desktop_gui.py    : GUI로 논문 탐색')
    print('- python console_viewer.py : 콘솔에서 논문 확인')

if __name__ == "__main__":
    main()
