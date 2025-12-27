# security-papers

Base utilities for fetching arXiv papers via the `arxiv` Python package.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Fetch recent papers

```bash
python -m security_papers.cli --query "cat:cs.CR" --max-results 5
```

The output includes metadata, abstracts, and links to the abstract, PDF, and HTML (if available).
