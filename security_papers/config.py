from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class EmailConfig:
    smtp_host: str
    smtp_port: int
    smtp_user: str | None
    smtp_password: str | None
    smtp_starttls: bool
    mail_from: str
    mail_to: str
    subject_prefix: str


@dataclass(frozen=True)
class JobConfig:
    query: str
    max_results: int
    state_path: str
    lookback_hours: int


@dataclass(frozen=True)
class AppConfig:
    email: EmailConfig
    job: JobConfig


def _get_bool(name: str, default: str = "false") -> bool:
    value = os.getenv(name, default).strip().lower()
    return value in {"1", "true", "yes", "on"}


def load_config() -> AppConfig:
    email = EmailConfig(
        smtp_host=os.getenv("SMTP_HOST", ""),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_user=os.getenv("SMTP_USER"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
        smtp_starttls=_get_bool("SMTP_STARTTLS", "true"),
        mail_from=os.getenv("MAIL_FROM", ""),
        mail_to=os.getenv("MAIL_TO", ""),
        subject_prefix=os.getenv("MAIL_SUBJECT_PREFIX", "Security Papers"),
    )
    job = JobConfig(
        query=os.getenv("ARXIV_QUERY", "cat:cs.CR"),
        max_results=int(os.getenv("ARXIV_MAX_RESULTS", "50")),
        state_path=os.getenv("STATE_PATH", "/data/last_run.txt"),
        lookback_hours=int(os.getenv("LOOKBACK_HOURS", "24")),
    )
    return AppConfig(email=email, job=job)
