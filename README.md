# security-papers

Base utilities for fetching arXiv papers via the `arxiv` Python package and delivering
summaries via email.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Fetch recent papers

```bash
python -m security_papers.cli --query "cat:cs.CR" --max-results 5
```

## Run the cron job locally

Set the required environment variables and run:

```bash
python -m security_papers.run_job
```

### Required environment variables

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `MAIL_FROM`
- `MAIL_TO`

### Optional environment variables

- `ARXIV_QUERY` (default: `cat:cs.CR`)
- `ARXIV_MAX_RESULTS` (default: `50`)
- `MAIL_SUBJECT_PREFIX` (default: `Security Papers`)
- `SMTP_STARTTLS` (default: `true`)
- `STATE_PATH` (default: `/data/last_run.txt`)
- `LOOKBACK_HOURS` (default: `24`)
- `CRON_SCHEDULE` (default: `0 * * * *`)

## Docker

```bash
docker build -t security-papers .

docker run --rm \
  -e SMTP_HOST=mail.example.com \
  -e SMTP_PORT=587 \
  -e SMTP_USER=user \
  -e SMTP_PASSWORD=pass \
  -e MAIL_FROM=alerts@example.com \
  -e MAIL_TO=team@example.com \
  -e ARXIV_QUERY="cat:cs.CR" \
  -v $(pwd)/data:/data \
  security-papers
```
