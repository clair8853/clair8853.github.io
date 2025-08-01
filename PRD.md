# MCI Papers Research Tool – Product Requirements Document (PRD)

**Version**: 3.0  
**Last updated**: 2025-08-01

---

## 1. Background
연구자들이 Mild Cognitive Impairment (MCI) 분야의 최신 연구 동향을 파악하고 개인 연구를 수행하는 것은 시간이 많이 소요됩니다.  
이 프로젝트는 PubMed에서 MCI 관련 논문을 자동으로 수집, 분류하여 **로컬 데이터베이스에 저장**하고 **듀얼 GUI(데스크톱/웹)를 통해 탐색**할 수 있는 **개인용 연구 도구**를 제공하며, **한국어 번역 기능**을 통해 국내 연구자들의 접근성을 향상시키는 것을 목표로 합니다.

## 2. Goals
| Goal | Success Metric |
|------|---------------|
| MCI 논문 자동 수집 및 분류 | 논문 수집 및 분류 성공률 ≥ 95% |
| 듀얼 인터페이스 제공 | 데스크톱 + 웹 GUI 모두 완전 기능 |
| 한국어 번역 워크플로우 구현 | CSV 기반 번역 시스템 완전 동작 |
| 효율적인 논문 검색 및 탐색 환경 제공 | 카테고리별 필터링 및 키워드 검색 기능 |
| 로컬 데이터베이스 기반 개인 연구 지원 | 데이터 무결성 및 접근성 보장 |
| 개인 정보 보호 | 모든 데이터 로컬 저장, 외부 전송 없음 |

### Non‑Goals
* 실시간 자동 번역 (수동 번역 워크플로우 사용)
* 다중 사용자 지원
* 실시간 공유 기능

## 3. Target User
* **개인 연구자** – MCI 분야 논문을 체계적으로 수집하고 관리하려는 연구자
* **한국어 사용자** – 영문 초록의 한국어 번역이 필요한 연구자

## 4. User Stories
1. **연구자로서**, 관심 있는 MCI 논문들을 자동으로 수집하여 개인 데이터베이스에 저장하고 싶다.
2. **연구자로서**, 수집된 논문들을 카테고리별로 필터링하여 원하는 논문을 빠르게 찾고 싶다.
3. **연구자로서**, 키워드 검색을 통해 특정 주제의 논문들을 쉽게 탐색하고 싶다.
4. **연구자로서**, 논문의 상세 정보를 확인하고 PubMed에서 원문을 바로 열고 싶다.
5. **한국어 사용자로서**, 영문 초록을 한국어로 번역하여 더 쉽게 이해하고 싶다.
6. **연구자로서**, 데스크톱과 웹 환경 모두에서 논문을 탐색하고 싶다.
7. **번역 작업자로서**, CSV 파일을 통해 효율적으로 논문을 번역하고 관리하고 싶다.

## 5. Requirements
### 5.1 Functional
1. PubMed API를 통한 MCI 관련 논문 자동 수집
2. 논문 제목, 초록, 메타데이터를 로컬 SQLite 데이터베이스에 저장
3. AI 기반 논문 카테고리 자동 분류 시스템
4. **듀얼 GUI**: 데스크톱(Tkinter) + 웹(Flask) 인터페이스 제공
5. 카테고리별 필터링 및 키워드 검색 기능
6. PubMed 원문 링크 바로 연결 기능
7. **한국어 번역 워크플로우**: CSV 기반 수동 번역 시스템
8. **번역 상태 관리**: 번역 진행률, 배치 추적 기능

### 5.2 Data Requirements
1. **논문 정보**: PMID, 제목, 초록, 저자, 저널 정보, 발행연도
2. **카테고리 분류**: 임상연구, 신경과학, 바이오마커, AI/ML, 이미징, 인지평가
3. **한국어 번역**: 초록 한국어 번역, 번역 상태, 번역 날짜, 번역자 노트
4. **로컬 저장**: 모든 데이터는 로컬 SQLite 데이터베이스에 저장
5. **개인정보 보호**: 외부 서버로 데이터 전송 없음

### 5.3 Interface Requirements
1. **데스크톱 GUI**: Tkinter 기반 사용자 친화적 인터페이스
   - 한국어/영어 초록 전환 기능
   - 번역 상태 및 진행률 표시
2. **웹 GUI**: Flask + Bootstrap 5 기반 반응형 웹 인터페이스
   - 모바일 친화적 반응형 디자인
   - 실시간 AJAX 검색
   - 드래그&드롭 파일 업로드
3. **검색 기능**: 제목, 초록 기반 키워드 검색
4. **필터링**: 카테고리별, 연도별, 번역 상태별 논문 필터링
5. **상세 보기**: 논문 정보 상세 표시 및 PubMed 링크
## 6. Success Metrics
* 논문 수집 및 분류 정확도 ≥ 95%
* 데스크톱 GUI 응답 시간 < 1초
* 웹 GUI 응답 시간 < 2초
* 번역 워크플로우 성공률 ≥ 98%
* 데이터베이스 무결성 유지
* 사용자 인터페이스 직관성
* 모바일 반응형 웹 디자인 호환성

## 7. Technical Architecture
* **Backend**: Python 3.8+ + SQLite + SQLAlchemy
* **Desktop GUI**: Tkinter with Korean/English toggle
* **Web GUI**: Flask 2.3+ + Bootstrap 5 + Jinja2
* **AI Classification**: scikit-learn 기반 텍스트 분류
* **Data Source**: PubMed API
* **Translation System**: CSV-based manual workflow
* **Database**: Enhanced SQLite schema with Korean fields

## 8. Translation Workflow
### 8.1 Export Process
- Script: `scripts/translation_export.py`
- Output: CSV file with untranslated papers
- Batch tracking for translation management

### 8.2 Manual Translation
- CSV editing with Korean abstract column
- Quality control and review process
- Translator notes support

### 8.3 Import Process
- Script: `scripts/translation_import.py`
- Validation and error handling
- Status tracking and batch management
