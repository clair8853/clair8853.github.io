# MCI P## 1. Background
Research teams stud### 5.1 Functional
1. Daily 07:00 JST cron job → fetch newest paper (PubMed API) matching keyword set with flexible date range.
2. Extract metadata + abstract from papers.
3. Append to `mci_daily.csv` and `mci_papers.db`.
4. Categorise using `category_rules.yaml`.
5. Generate category trend analysis and visualizations.
6. Blog auto‑deploy via GitHub Actions (`deploy.yml`).ld Cognitive Impairment (MCI) need up‑to‑date literature but manual tracking is time‑consuming.  
This project automates daily retrieval and categorisation of MCI‑related PubMed papers, storing results in CSV/SQLite and publishing weekly digests to a Hugo (PaperMod) blog.

## 2. Goals
| Goal | Success Metric |
|------|---------------|
| Deliver fresh MCI paper data every morning | Daily scheduler success ≥ 99 % /30 days |
| Enable easy browsing & trend analysis | Hugo site auto‑deploy within 5 min of commit |
| Zero recurring cost to operate | No paid APIs or cloud services |er & Summarizer – Product Requirements Document (PRD)

**Version**: 0.6  
**Last updated**: 2025-07-31

---

## 1. Background
Research teams studying Mild Cognitive Impairment (MCI) need up‑to‑date literature but manual tracking is time‑consuming.  
This project automates daily retrieval, summarisation and categorisation of MCI‑related PubMed papers, storing results in CSV/SQLite and publishing weekly digests to a Hugo (PaperMod) blog.

## 2. Goals
| Goal | Success Metric |
|------|---------------|
| Deliver fresh MCI paper data every morning | Daily scheduler success ≥ 99 % /30 days |
| Provide concise abstracts and summaries | ROUGE‑L ≥ 30 on monthly 30‑sample audit |
| Enable easy browsing & trend analysis | Hugo site auto‑deploy within 5 min of commit |
| Zero recurring cost to operate | No paid APIs or cloud services |

### Non‑Goals
* Automatic Korean translation accuracy – handled manually.
* GUI frontend (planned post‑MVP).

## 3. Personas
* **Researcher** – needs daily updates and keyword trends.
* **Data Scientist** – wants CSV/DB access for further analysis.
* **Student** – reads blog digests to follow the field.

## 4. User Stories
1. As a *researcher*, I enter keywords and receive a CSV with today’s MCI papers.
2. As a *data scientist*, I run `python analyzer.py --trend` to plot monthly keyword frequencies.
3. As a *student*, I open the blog each week to read curated summaries.

## 5. Requirements
### 5.1 Functional
1. Daily 07:00 JST cron job → fetch newest paper (PubMed API) matching keyword set.
2. Extract metadata + abstract → summarise with local **pegasus‑pubmed**.
3. Append to `mci_daily.csv` and `mci_papers.db`.
4. Categorise using `category_rules.yaml`.
5. Generate/update keyword‑trend figures on demand.
6. Blog auto‑deploy via GitHub Actions (`deploy.yml`).

### 5.2 Non‑Functional
* Processing 1 paper < 30 s on RTX 3060.
* PubMed API usage within 3 requests/day (safe).
* Code licensed MIT, runs offline (no internet dependency after download).

## 6. System Architecture
```mermaid
flowchart TD
    A[Scheduler (cron/APScheduler)] --> B[PubMed Crawler]
    B --> C[Parser]
    C --> D[Summariser<br/>(pegasus-pubmed)]
    D --> E[Analyzer<br/>(keywords, category)]
    E --> F[Exporter<br/>CSV + SQLite]
    F --> G[Blog Generator<br/>(markdown)]
    G --> H[GitHub Actions Deploy]
```

## 7. Schedule (16‑week roadmap)
| Weeks | Milestone |
|-------|-----------|
| 1‑2 | Repo init, env setup |
| 3‑4 | PubMed crawler MVP |
| 5‑6 | Parser & data model |
| 7‑8 | Scheduler integration |
| 9‑10 | Keyword analyzer |
| 11‑12 | Summariser (pegasus‑pubmed) |
| 13‑14 | Trend visualiser & blog generator |
| 15 | Integration & tests |
| 16 | Docs, release v0.9 |

## 8. Success Metrics
* Daily job success ≥ 99 %
* ROUGE‑L ≥ 30 on audits
* Processing 500‑paper batch ≤ 1 min
* Blog deploy latency ≤ 5 min

## 9. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| PubMed API change | Job fails | Graceful retry & update parser |
| GPU unavailable | Slow summaries | Fallback to TextRank |
| Model hallucination | Wrong summaries | Monthly manual review |

## 10. Future Roadmap
* GUI (Streamlit) dashboard
* Figure OCR + caption summarisation
* Automatic Korean translation using fine‑tuned NLLB
* Slack/email notifications

---
