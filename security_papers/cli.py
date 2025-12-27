from __future__ import annotations

import argparse
import json
from typing import Iterable

from security_papers.arxiv_client import fetch_papers
from security_papers.models import Paper


def _serialize_paper(paper: Paper) -> dict[str, object]:
    return {
        "entry_id": paper.entry_id,
        "title": paper.title,
        "authors": paper.authors,
        "abstract": paper.abstract,
        "categories": paper.categories,
        "published": paper.published.isoformat(),
        "updated": paper.updated.isoformat(),
        "abs_url": paper.abs_url,
        "pdf_url": paper.pdf_url,
        "html_url": paper.html_url,
    }


def _print_papers(papers: Iterable[Paper]) -> None:
    payload = [_serialize_paper(paper) for paper in papers]
    print(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch recent arXiv papers via the arxiv API",
    )
    parser.add_argument(
        "--query",
        default="cat:cs.CR",
        help="arXiv search query, e.g. 'cat:cs.CR'",
    )
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()

    papers = fetch_papers(
        search_query=args.query,
        max_results=args.max_results,
        start=args.start,
    )
    _print_papers(papers)


if __name__ == "__main__":
    main()
