from __future__ import annotations

import html
import smtplib
from email.message import EmailMessage
from typing import Iterable

from security_papers.config import EmailConfig
from security_papers.models import Paper


def build_email(config: EmailConfig, papers: Iterable[Paper]) -> EmailMessage:
    # Convert to list to allow multiple iterations
    papers_list = list(papers)
    
    message = EmailMessage()
    message["From"] = config.mail_from
    message["To"] = config.mail_to
    subject = config.subject_prefix
    message["Subject"] = subject

    # Plain text version
    paper_lines = []
    for index, paper in enumerate(papers_list, start=1):
        lines = [
            f"{index}. {paper.title}",
            f"   Authors: {', '.join(paper.authors)}",
            f"   Published: {paper.published.date().isoformat()}",
            f"   Abstract: {paper.abstract}",
            f"   Abstract URL: {paper.abs_url}",
            f"   PDF URL: {paper.pdf_url}",
        ]
        if paper.html_url:
            lines.append(f"   HTML URL: {paper.html_url}")
        paper_lines.append("\n".join(lines))

    text_body = "\n\n".join([
        "Security Papers Update",
        "",
        *paper_lines,
    ])
    message.set_content(text_body)

    # HTML version
    html_papers = []
    for index, paper in enumerate(papers_list, start=1):
        title = html.escape(paper.title)
        authors = html.escape(", ".join(paper.authors))
        published = paper.published.date().isoformat()
        abstract = html.escape(paper.abstract)
        
        links = [
            f'<a href="{paper.abs_url}" style="color: #3498db; text-decoration: none; font-weight: bold;">Abstract</a>',
            f'<a href="{paper.pdf_url}" style="color: #3498db; text-decoration: none; font-weight: bold;">PDF</a>',
        ]
        if paper.html_url:
            links.append(f'<a href="{paper.html_url}" style="color: #3498db; text-decoration: none; font-weight: bold;">HTML</a>')
        
        links_html = " | ".join(links)
        
        html_papers.append(f"""
            <div style="margin-bottom: 40px; border-bottom: 1px solid #ecf0f1; padding-bottom: 20px;">
                <h2 style="font-size: 20px; color: #2c3e50; margin-top: 0; margin-bottom: 10px;">{index}. {title}</h2>
                <p style="font-style: italic; color: #7f8c8d; margin-bottom: 10px; font-size: 14px;">{authors}</p>
                <p style="font-size: 12px; color: #95a5a6; margin-bottom: 15px;">Published: {published}</p>
                <div style="line-height: 1.6; color: #34495e; background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                    {abstract}
                </div>
                <p style="margin-top: 10px;">{links_html}</p>
            </div>
        """)

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 30px; color: #333; background-color: #ffffff;">
        <header style="margin-bottom: 40px; text-align: center;">
            <h1 style="color: #2980b9; border-bottom: 3px solid #2980b9; padding-bottom: 15px; display: inline-block; margin-top: 0;">Security Papers Update</h1>
        </header>
        <main>
            {"".join(html_papers)}
        </main>
        <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #bdc3c7; text-align: center;">
            <p>This is an automated update from your Security Papers Bot.</p>
        </footer>
    </body>
    </html>
    """
    message.add_alternative(html_body, subtype="html")

    return message


def send_email(config: EmailConfig, message: EmailMessage) -> None:
    with smtplib.SMTP(config.smtp_host, config.smtp_port) as smtp:
        if config.smtp_starttls:
            smtp.starttls()
        if config.smtp_user and config.smtp_password:
            smtp.login(config.smtp_user, config.smtp_password)
        smtp.send_message(message)
