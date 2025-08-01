# Korean Translation Workflow Design
## Phase 2 Implementation Plan

### 🎯 Workflow Overview
Manual translation system where translators work with CSV files to provide Korean abstracts for research papers.

### 📋 Workflow Steps

#### Step 1: Export Papers for Translation
- Export untranslated papers to CSV format
- Include: Paper ID, Title, English Abstract, Publication Date
- Status field to track translation progress

#### Step 2: Manual Translation Process  
- Translator opens CSV file in Excel/Google Sheets
- Adds Korean translations in designated columns
- Marks translation status as "completed"

#### Step 3: Import Translated Content
- System imports completed CSV files
- Updates database with Korean abstracts
- Logs translation activity
- Validates data integrity

#### Step 4: Display Integration
- GUI shows Korean abstracts alongside English
- Language toggle functionality
- Bilingual search capabilities

### 🗄️ Database Schema Changes

#### New Fields for papers table:
```sql
- abstract_korean TEXT
- translation_status ENUM('pending', 'in_progress', 'completed', 'reviewed')
- translation_date DATETIME
- translator_notes TEXT
```

#### New table: translation_batches
```sql
- batch_id INT PRIMARY KEY
- export_date DATETIME
- file_path VARCHAR(255)
- total_papers INT
- completed_papers INT
- status ENUM('exported', 'in_progress', 'completed', 'imported')
```

### 📁 File Structure
```
data/translations/
├── exports/
│   ├── batch_YYYYMMDD_HHMMSS.csv
│   └── template.csv
├── imports/
│   ├── completed_batch_YYYYMMDD.csv
│   └── archive/
└── logs/
    ├── export_log.txt
    └── import_log.txt
```

### 🔧 Implementation Components

#### 1. CSV Export Module (`scripts/translation_export.py`)
- Generate translation batches
- Create formatted CSV files
- Track export history

#### 2. CSV Import Module (`scripts/translation_import.py`)
- Validate CSV format
- Import Korean translations
- Update database records
- Generate import reports

#### 3. GUI Integration
- Add Korean abstract display
- Language toggle buttons
- Translation status indicators
- Export/Import controls

#### 4. Translation Management
- Batch tracking interface
- Progress monitoring
- Quality control features

### 📊 CSV File Format

#### Export CSV Structure:
| paper_id | title | abstract_english | publication_date | doi | translation_status | notes |
|----------|-------|------------------|------------------|-----|-------------------|-------|

#### Import CSV Structure:
| paper_id | abstract_korean | translation_status | translator_notes | quality_check |
|----------|------------------|-------------------|------------------|---------------|

### 🔄 Automated Features
- Periodic export of new papers (weekly/monthly)
- Email notifications for completed translations
- Backup of translation data
- Progress tracking dashboard

### 🛡️ Quality Control
- Validation of Korean text encoding
- Character limit checks
- Completeness verification
- Translation review workflow

### 📈 Success Metrics
- Translation completion rate
- Time from export to import
- Translation quality scores
- User satisfaction feedback

---

**Status:** Design Complete - Ready for Implementation
**Next:** Begin coding CSV export functionality
