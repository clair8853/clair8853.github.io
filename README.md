# MCI Papers Research Tool

**MCI 연구 논문을 자동으로 수집하여 로컬 데이터베이스에 정리하는 개인 연구용 도구입니다.**

## 🎯 프로젝트 목적
- **개인 연구 지원**: MCI 분야 논문을 체계적으로 수집하고 분류
- **논문 관리**: 수집된 논문들을 카테고리별로 정리 및 검색
- **로컬 데이터베이스**: 개인 연구를 위한 논문 데이터 저장
- **효율적 탐색**: 듀얼 GUI(데스크톱/웹)를 통한 직관적인 논문 탐색 환경
- **한국어 지원**: 초록의 한국어 번역 기능 제공

## 📚 수집 데이터
* **논문 정보**: PMID, 제목, 초록, 저자, 저널 정보
* **카테고리별 분류**: 임상연구, 신경과학, 바이오마커, AI/ML, 이미징, 인지평가
* **메타데이터**: 발행연도, 저널 권호 정보
* **원문 링크**: PubMed 바로가기 제공
* **한국어 번역**: 초록의 한국어 번역 및 번역 상태 관리

## 🖥️ 사용 방법
### 🖥️ 데스크톱 GUI (권장)
```bash
python desktop_gui.py
```
- 🔍 카테고리별 필터링 및 키워드 검색
- 🌐 한국어/영어 초록 전환 기능
- 📊 번역 진행 상황 통계
- 🔗 PubMed 직접 연결

### 🌐 웹 GUI (모던 인터페이스)
```bash
python web_gui/app.py
```
웹브라우저에서 `http://localhost:5000` 접속
- 📱 반응형 모바일 친화적 디자인
- 🎨 Bootstrap 5 기반 모던 UI
- 🔍 실시간 AJAX 검색
- 📄 드래그&드롭 파일 업로드

### 🌐 한국어 번역 워크플로우
```bash
# 번역할 논문을 CSV로 내보내기
python scripts/translation_export.py

# CSV 파일에서 수동 번역 작업 후
python scripts/translation_import.py
```

### 기타 확인 방법
- **콘솔 탐색**: `python console_viewer.py`
- **HTML 리포트**: `python generate_html_report.py`

## 💡 주요 특징
- ✅ **듀얼 GUI**: 데스크톱(Tkinter) + 웹(Flask) 인터페이스
- ✅ **로컬 저장**: 모든 데이터는 로컬 데이터베이스에 저장
- ✅ **자동 분류**: AI 기반 카테고리 자동 분류
- ✅ **검색 기능**: 제목, 초록 기반 키워드 검색
- ✅ **한국어 번역**: CSV 기반 수동 번역 워크플로우
- ✅ **번역 관리**: 번역 상태, 배치, 진행률 추적
- ✅ **반응형 웹**: 모바일 친화적 Bootstrap 5 디자인
- ✅ **개인용**: 개인 연구 목적의 비공개 도구

---

## 기술적 세부사항 (개발자용)

### 시스템 구조
```
PubMed API → 논문 수집 → 카테고리 분류 → 로컬 데이터베이스 저장 → 듀얼 GUI 확인
                                                                           ├── 데스크톱 GUI
                                                                           └── 웹 GUI
```

### 폴더 구조
```
mci-papers/
├── scripts/              # Python 스크립트들
│   ├── db_manager.py     # 데이터베이스 관리
│   ├── translation_export.py  # 번역용 CSV 내보내기
│   ├── translation_import.py  # 번역된 CSV 가져오기
│   └── database_korean.py     # 한국어 필드 마이그레이션
├── web_gui/              # Flask 웹 인터페이스
│   ├── app.py           # Flask 애플리케이션 메인
│   ├── templates/       # HTML 템플릿들
│   └── static/          # CSS, JS 정적 파일들
├── config/               # 설정 파일들
├── data/                 # SQLite 데이터베이스
├── translations/         # 번역 CSV 파일들
├── archive/              # 개발 과정 파일들
└── logs/                 # 실행 로그
```

### 번역 워크플로우
1. **내보내기**: `translation_export.py`로 번역할 논문을 CSV로 추출
2. **번역 작업**: CSV 파일에서 `abstract_korean` 컬럼에 한국어 번역 입력
3. **가져오기**: `translation_import.py`로 번역된 내용을 데이터베이스에 저장
4. **확인**: 데스크톱/웹 GUI에서 번역 상태 및 내용 확인

### 설치 및 실행
```bash
# 저장소 클론
git clone https://github.com/clair8853/clair8853.github.io.git
cd clair8853.github.io

# 파이썬 가상환경 설정
python -m venv .venv
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 한국어 마이그레이션 (최초 1회)
python scripts/database_korean.py

# 논문 수집 실행
python main.py --daily

# 데스크톱 GUI로 데이터 확인
python desktop_gui.py

# 또는 웹 GUI 실행
python web_gui/app.py
```

### 기술 스택
- **Backend**: Python 3.8+, SQLAlchemy, SQLite
- **Desktop GUI**: Tkinter
- **Web GUI**: Flask 2.3+, Bootstrap 5, Jinja2
- **AI Classification**: scikit-learn 기반 텍스트 분류
- **Data Source**: PubMed API
- **Translation**: CSV 기반 수동 번역 워크플로우
