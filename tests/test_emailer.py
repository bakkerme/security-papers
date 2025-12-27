from datetime import datetime, timezone

from security_papers.config import EmailConfig
from security_papers.emailer import build_email
from security_papers.models import Paper


def test_build_email_includes_links():
    config = EmailConfig(
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user=None,
        smtp_password=None,
        smtp_starttls=True,
        mail_from="from@example.com",
        mail_to="to@example.com",
        subject_prefix="Security Papers",
    )
    paper = Paper(
        entry_id="http://arxiv.org/abs/1234.5678v1",
        title="Example Paper",
        authors=["Ada Lovelace"],
        abstract="Abstract text.",
        categories=["cs.CR"],
        published=datetime(2024, 4, 1, tzinfo=timezone.utc),
        updated=datetime(2024, 4, 2, tzinfo=timezone.utc),
        abs_url="http://arxiv.org/abs/1234.5678v1",
        pdf_url="http://arxiv.org/pdf/1234.5678v1",
        html_url="https://arxiv.org/html/1234.5678v1",
    )

    message = build_email(config, [paper])
    
    # Check plain text part
    text_part = message.get_body(preferencelist=('plain',))
    text_body = text_part.get_content()

    assert "Example Paper" in text_body
    assert "Abstract URL" in text_body
    assert "PDF URL" in text_body
    assert "HTML URL" in text_body

    # Check HTML part
    html_part = message.get_body(preferencelist=('html',))
    html_body = html_part.get_content()

    assert "Security Papers Update" in html_body
    assert "Example Paper" in html_body
    assert 'href="http://arxiv.org/abs/1234.5678v1"' in html_body
    assert 'href="http://arxiv.org/pdf/1234.5678v1"' in html_body
    assert 'href="https://arxiv.org/html/1234.5678v1"' in html_body
