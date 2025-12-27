from __future__ import annotations

from collections.abc import Iterable
from security_papers.models import Paper
import arxiv


def _html_url_from_entry_id(entry_id: str) -> str | None:
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
    sort_by: str = "submittedDate",
    sort_order: str = "descending",
) -> Iterable[Paper]:

    sort_by_map = {
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "relevance": arxiv.SortCriterion.Relevance,
    }
    sort_order_map = {
        "ascending": arxiv.SortOrder.Ascending,
        "descending": arxiv.SortOrder.Descending,
    }

    print(f"Fetching papers from arXiv with query: {search_query}")

    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        # start=start,
        sort_by=sort_by_map.get(sort_by, arxiv.SortCriterion.SubmittedDate),
        sort_order=sort_order_map.get(sort_order, arxiv.SortOrder.Descending),
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
