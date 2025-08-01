# MCI Papers Crawler

Automated pipeline to **crawl and categorise** Mild Cognitive Impairment (MCI) papers from PubMed every day, store them in CSV/SQLite, and publish weekly digests to a Hugo (PaperMod) blog.

## Features
* ✅ Daily 07:00 JST crawl of the latest MCI‑related paper
* ✅ Keyword categorisation (Biomarker, AI/ML, ADNI, MRI, Big‑Data)
* ✅ Trend visualisation on demand
* ✅ Static blog deployment via GitHub Actions (`mci-papers` repo)rs Crawler & Summarizer

Automated pipeline to **crawl, summarise and categorise** Mild Cognitive Impairment (MCI) papers from PubMed every day, store them in CSV/SQLite, and publish weekly digests to a Hugo (PaperMod) blog.

## Features
* ✅ Daily 07:00 JST crawl of the latest MCI‑related paper
* ✅ Local summarisation with `google/pegasus-pubmed` (requires GPU)
* ✅ Keyword categorisation (Biomarker, AI/ML, ADNI, MRI, Big‑Data)
* ✅ Trend visualisation on demand
* ✅ Static blog deployment via GitHub Actions (`mci-papers` repo)

## Installation
```bash
# Clone repository
git clone https://github.com/yourname/mci-papers.git
cd mci-papers

# Create Python 3.11 venv
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Hardware: NVIDIA RTX 3060 12 GB (or better) recommended.

## Quick Start
```bash
# One‑off crawl & summary
python main.py --crawl --keywords config/keywords.txt

# Generate keyword trend charts
python analyzer.py --trend --months 12
```

Cron example (Ubuntu):
```cron
0 7 * * * /home/user/mci-papers/.venv/bin/python /home/user/mci-papers/main.py --daily
```

## Configuration
* **config/category_rules.yaml** – keyword→category mapping  
* **config/config.yaml** – scheduler time, paths  
* **deploy.yml** – GitHub Actions workflow for Hugo blog

## Folder Structure
```
mci-papers/
├── data/                 # CSV & SQLite outputs
├── scripts/              # CLI modules
├── config/               # YAML configs
├── blog/                 # Hugo site source
├── .github/workflows/    # deploy.yml
└── README.md
```

## License
MIT – see `LICENSE`.

## Acknowledgements
* PubMed API
* HuggingFace Transformers & `google/pegasus-pubmed`
* PaperMod Hugo theme
