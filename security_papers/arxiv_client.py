from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional

import arxiv


@dataclass(frozen=True)
class Paper:
    entry_id: str
    title: str
    authors: list[str]
    abstract: str
    categories: list[str]
    published: datetime
    updated: datetime
    abs_url: str
    pdf_url: str
    html_url: Optional[str]


def _html_url_from_entry_id(entry_id: str) -> Optional[str]:
    if not entry_id:
        return None
    arxiv_id = entry_id.rsplit("/", maxsplit=1)[-1]
    if not arxiv_id:
        return None
    return f"https://arxiv.org/html/{arxiv_id}"


def fetch_papers(
    search_query: str,
    max_results: int = 25,
    start: int = 0,
    sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate,
    sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending,
) -> Iterable[Paper]:
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        start=start,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    client = arxiv.Client()
    for result in client.results(search):
        yield Paper(
            entry_id=result.entry_id,
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            categories=list(result.categories),
            published=result.published,
            updated=result.updated,
            abs_url=result.entry_id,
            pdf_url=result.pdf_url,
            html_url=_html_url_from_entry_id(result.entry_id),
        )
