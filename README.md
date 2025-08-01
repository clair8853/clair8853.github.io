# MCI Papers Research Tool

**MCI 연구 논문을 자동으로 수집하여 로컬 데이터베이스에 정리하는 개인 연구용 도구입니다.**

## 🎯 프로젝트 목적
- **개인 연구 지원**: MCI 분야 논문을 체계적으로 수집하고 분류
- **논문 관리**: 수집된 논문들을 카테고리별로 정리 및 검색
- **로컬 데이터베이스**: 개인 연구를 위한 논문 데이터 저장
- **효율적 탐색**: GUI를 통한 직관적인 논문 탐색 환경

## 📚 수집 데이터
* **논문 정보**: PMID, 제목, 초록, 저자, 저널 정보
* **카테고리별 분류**: 임상연구, 신경과학, 바이오마커, AI/ML, 이미징, 인지평가
* **메타데이터**: 발행연도, 저널 권호 정보
* **원문 링크**: PubMed 바로가기 제공

## 🖥️ 데이터 확인 방법
### GUI 애플리케이션 (추천)
```bash
python desktop_gui.py
```
- 카테고리별 필터링
- 키워드 검색
- 논문 상세 정보 확인
- PubMed 직접 연결

### 기타 확인 방법
- **웹 인터페이스**: `python gui_viewer.py` (Streamlit)
- **콘솔 탐색**: `python console_viewer.py`
- **HTML 리포트**: `python generate_html_report.py`

## 💡 주요 특징
- ✅ **로컬 저장**: 모든 데이터는 로컬 데이터베이스에 저장
- ✅ **자동 분류**: AI 기반 카테고리 자동 분류
- ✅ **검색 기능**: 제목, 초록 기반 키워드 검색
- ✅ **개인용**: 개인 연구 목적의 비공개 도구

---

## 기술적 세부사항 (개발자용)

### 시스템 구조
```
PubMed API → 논문 수집 → 카테고리 분류 → 로컬 데이터베이스 저장 → GUI 확인
```

### 폴더 구조
```
mci-papers/
├── scripts/              # Python 스크립트들
├── config/               # 설정 파일들
├── data/                 # SQLite 데이터베이스
├── archive/              # 개발 과정 파일들
└── logs/                 # 실행 로그
```

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

# 논문 수집 실행
python main.py --daily

# GUI로 데이터 확인
python desktop_gui.py
```
