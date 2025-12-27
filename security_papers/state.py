from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def load_last_run(path: str) -> datetime | None:
    state_path = Path(path)
    if not state_path.exists():
        return None
    value = state_path.read_text(encoding="utf-8").strip()
    if not value:
        return None
    return datetime.fromisoformat(value)


def save_last_run(path: str, timestamp: datetime) -> None:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(timestamp.astimezone(timezone.utc).isoformat(), encoding="utf-8")
