from __future__ import annotations
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunStore:
    def __init__(self, path: str | None = None):
        self.path = path or get_settings().database_path
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    route TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    requires_approval INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    approved_at TEXT
                )
            """)

    def save(self, run_id: str, query: str, route: str, answer: str, requires_approval: bool):
        status = "pending_approval" if requires_approval else "completed"
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (run_id, query, route, answer, int(requires_approval), status, _now(), None),
            )
        return status

    def get(self, run_id: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        return dict(row) if row else None

    def approve(self, run_id: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT status FROM runs WHERE id = ?", (run_id,)).fetchone()
            if not row:
                return None
            if row["status"] == "pending_approval":
                conn.execute("UPDATE runs SET status='approved', approved_at=? WHERE id=?", (_now(), run_id))
                return "approved"
            return row["status"]
