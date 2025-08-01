# MCI Papers Research Tool - Project Structure Guide

**Version**: 1.0  
**Last updated**: 2025-08-01

---

## 📁 프로젝트 구조 개요

이 문서는 MCI Papers Research Tool 프로젝트의 파일 구조와 각 파일의 역할을 설명합니다.
프로젝트는 기능별로 체계적으로 구성되어 있으며, 개발자와 사용자가 쉽게 파악할 수 있도록 정리되었습니다.

## 🏗️ 전체 디렉토리 구조

```
mci_paper/
├── 📋 프로젝트 문서
│   ├── README.md                           # 프로젝트 소개 및 사용법
│   ├── PRD.md                             # 제품 요구사항 문서
│   ├── PROJECT_ROADMAP.md                 # 프로젝트 로드맵
│   ├── PROJECT_STRUCTURE.md               # 프로젝트 구조 가이드 (이 파일)
│   ├── korean_translation_workflow.md     # 한국어 번역 워크플로우 설명
│   └── html_gui_development_plan.md       # HTML GUI 개발 계획서
│
├── 🖥️ 메인 애플리케이션
│   ├── main.py                            # 논문 수집 메인 스크립트
│   ├── desktop_gui.py                     # 데스크톱 GUI 애플리케이션
│   └── console_viewer.py                  # 콘솔 기반 뷰어
│
├── 🌐 웹 GUI 시스템
│   └── web_gui/
│       ├── app.py                         # Flask 웹 애플리케이션 메인
│       ├── requirements_web.txt           # 웹 GUI 의존성
│       ├── templates/                     # HTML 템플릿
│       │   ├── base.html                  # 기본 레이아웃
│       │   ├── index.html                 # 메인 대시보드
│       │   ├── paper_list.html            # 논문 목록 페이지
│       │   ├── paper_detail.html          # 논문 상세 페이지
│       │   └── translation.html           # 번역 관리 페이지
│       └── static/                        # 정적 파일
│           ├── css/
│           │   └── custom.css             # 커스텀 CSS
│           └── js/
│               └── main.js                # JavaScript 기능
│
├── ⚙️ 백엔드 스크립트
│   └── scripts/
│       ├── 🗄️ 데이터베이스 관리
│       │   ├── database.py                # 데이터베이스 초기화
│       │   ├── database_korean.py         # 한국어 필드 마이그레이션
│       │   └── db_manager.py              # 데이터베이스 관리자
│       │
│       ├── 🕷️ 데이터 수집
│       │   ├── pubmed_crawler.py          # PubMed 크롤러
│       │   └── pubmed_parser.py           # PubMed 데이터 파서
│       │
│       ├── 🤖 AI 분석
│       │   ├── categorizer.py             # 논문 카테고리 분류기
│       │   └── analyzer.py                # 논문 분석 도구
│       │
│       ├── 🌐 번역 시스템
│       │   ├── translation_export.py      # 번역용 CSV 내보내기
│       │   └── translation_import.py      # 번역된 CSV 가져오기
│       │
│       └── 🔧 유틸리티
│           ├── logger.py                  # 로깅 시스템
│           └── blog_generator.py          # HTML 리포트 생성기
│
├── 📊 데이터 저장소
│   └── data/
│       ├── mci_papers.db                  # SQLite 데이터베이스
│       └── translations/                  # 번역 CSV 파일들
│           ├── export/                    # 내보낸 번역 파일
│           ├── import/                    # 가져올 번역 파일
│           └── archive/                   # 처리 완료된 파일
│
├── ⚙️ 설정 파일
│   ├── config/
│   │   └── (설정 파일들)
│   ├── requirements.txt                   # Python 의존성
│   └── .gitignore                        # Git 무시 파일 목록
│
└── 📝 로그 및 기록
    ├── logs/                             # 실행 로그 파일들
    └── project_enhancement_log.txt       # 프로젝트 개선 로그
```

## 📋 파일별 역할 및 설명

### 🏠 루트 레벨 파일들

| 파일명 | 타입 | 역할 | 설명 |
|--------|------|------|------|
| `main.py` | 실행 파일 | 논문 수집 메인 | PubMed에서 논문을 수집하는 메인 스크립트 |
| `desktop_gui.py` | GUI 앱 | 데스크톱 인터페이스 | Tkinter 기반 데스크톱 GUI 애플리케이션 |
| `console_viewer.py` | 유틸리티 | 콘솔 뷰어 | 터미널에서 논문을 확인하는 도구 |
| `requirements.txt` | 설정 | 의존성 목록 | Python 패키지 의존성 정의 |

### 📋 문서 파일들

| 파일명 | 타입 | 역할 | 대상 사용자 |
|--------|------|------|----------|
| `README.md` | 문서 | 프로젝트 소개 | 모든 사용자 |
| `PRD.md` | 문서 | 제품 요구사항 | 개발자, PM |
| `PROJECT_ROADMAP.md` | 문서 | 개발 로드맵 | 개발자, PM |
| `PROJECT_STRUCTURE.md` | 문서 | 구조 가이드 | 개발자, 신규 팀원 |
| `korean_translation_workflow.md` | 문서 | 번역 워크플로우 | 번역 작업자 |
| `html_gui_development_plan.md` | 문서 | 웹 GUI 개발 계획 | 웹 개발자 |

### ⚙️ 스크립트 파일들 (기능별 분류)

#### 🗄️ 데이터베이스 관리
- `scripts/database.py`: 데이터베이스 초기 설정
- `scripts/database_korean.py`: 한국어 필드 추가 마이그레이션
- `scripts/db_manager.py`: 데이터베이스 CRUD 작업

#### 🕷️ 데이터 수집
- `scripts/pubmed_crawler.py`: PubMed API를 통한 논문 수집
- `scripts/pubmed_parser.py`: 수집된 데이터 파싱 및 정제

#### 🤖 AI 및 분석
- `scripts/categorizer.py`: 머신러닝 기반 논문 분류
- `scripts/analyzer.py`: 논문 데이터 분석 도구

#### 🌐 번역 시스템
- `scripts/translation_export.py`: 번역할 논문을 CSV로 내보내기
- `scripts/translation_import.py`: 번역된 CSV를 데이터베이스로 가져오기

#### 🔧 유틸리티
- `scripts/logger.py`: 로깅 및 디버깅 시스템
- `scripts/blog_generator.py`: HTML 리포트 생성

### 🌐 웹 GUI 시스템

#### Flask 애플리케이션
- `web_gui/app.py`: Flask 웹 서버 메인 애플리케이션
- `web_gui/requirements_web.txt`: 웹 GUI 전용 의존성

#### HTML 템플릿 (Jinja2)
- `templates/base.html`: 기본 레이아웃 템플릿
- `templates/index.html`: 메인 대시보드
- `templates/paper_list.html`: 논문 목록 페이지
- `templates/paper_detail.html`: 논문 상세 정보 페이지
- `templates/translation.html`: 번역 관리 페이지

#### 정적 파일
- `static/css/custom.css`: 커스텀 스타일시트
- `static/js/main.js`: JavaScript 기능

## 🚀 실행 가이드

### 데스크톱 GUI 실행
```bash
python desktop_gui.py
```

### 웹 GUI 실행
```bash
python web_gui/app.py
# 브라우저에서 http://localhost:5000 접속
```

### 논문 수집 실행
```bash
python main.py --daily
```

### 번역 워크플로우
```bash
# 1. 번역할 논문 내보내기
python scripts/translation_export.py

# 2. CSV 파일에서 수동 번역 작업

# 3. 번역된 논문 가져오기
python scripts/translation_import.py
```

## 🔧 개발자 가이드

### 새로운 기능 추가 시
1. **스크립트 추가**: `scripts/` 디렉토리에 기능별로 분류하여 추가
2. **GUI 수정**: 데스크톱은 `desktop_gui.py`, 웹은 `web_gui/` 디렉토리 수정
3. **문서 업데이트**: 기능 추가 시 관련 문서들 업데이트
4. **테스트**: 두 GUI 모두에서 기능 테스트

### 코드 구조 원칙
- **단일 책임**: 각 스크립트는 하나의 명확한 기능을 담당
- **모듈화**: 기능별로 분리하여 재사용성 증대
- **문서화**: 모든 주요 기능은 문서화
- **듀얼 지원**: 데스크톱과 웹 GUI 모두 지원

---

**💡 팁**: 프로젝트 구조를 변경할 때는 이 문서를 먼저 업데이트하고, 관련 import 경로들을 확인하세요.
