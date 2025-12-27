from datetime import datetime, timezone

from security_papers.models import Paper
from security_papers.run_job import filter_papers_since


def test_filter_papers_since():
    cutoff = datetime(2024, 4, 10, tzinfo=timezone.utc)
    old_paper = Paper(
        entry_id="http://arxiv.org/abs/1111.1111v1",
        title="Old",
        authors=["Author"],
        abstract="Old abstract",
        categories=["cs.CR"],
        published=datetime(2024, 4, 1, tzinfo=timezone.utc),
        updated=datetime(2024, 4, 1, tzinfo=timezone.utc),
        abs_url="http://arxiv.org/abs/1111.1111v1",
        pdf_url="http://arxiv.org/pdf/1111.1111v1",
        html_url=None,
    )
    new_paper = Paper(
        entry_id="http://arxiv.org/abs/2222.2222v1",
        title="New",
        authors=["Author"],
        abstract="New abstract",
        categories=["cs.CR"],
        published=datetime(2024, 4, 12, tzinfo=timezone.utc),
        updated=datetime(2024, 4, 12, tzinfo=timezone.utc),
        abs_url="http://arxiv.org/abs/2222.2222v1",
        pdf_url="http://arxiv.org/pdf/2222.2222v1",
        html_url=None,
    )

    filtered = filter_papers_since([old_paper, new_paper], cutoff)

    assert filtered == [new_paper]
