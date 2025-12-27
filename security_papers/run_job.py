from __future__ import annotations

from datetime import datetime, timedelta, timezone

from security_papers.arxiv_client import fetch_papers
from security_papers.config import load_config
from security_papers.emailer import build_email, send_email
from security_papers.models import Paper
from security_papers.state import load_last_run, save_last_run


def filter_papers_since(papers: list[Paper], since: datetime) -> list[Paper]:
    return [paper for paper in papers if paper.published >= since]


def run() -> int:
    config = load_config()
    now = datetime.now(timezone.utc)
    last_run = load_last_run(config.job.state_path)
    if last_run is None:
        last_run = now - timedelta(hours=config.job.lookback_hours)

    papers = list(
        fetch_papers(
            search_query=config.job.query,
            max_results=config.job.max_results,
            start=0,
        )
    )
    new_papers = filter_papers_since(papers, last_run)
    print(f"Found {len(new_papers)} new papers since {last_run.isoformat()}")

    if new_papers:
        message = build_email(config.email, new_papers)
        send_email(config.email, message)
    else:
        print("No new papers found; no email sent.")

    save_last_run(config.job.state_path, now)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
