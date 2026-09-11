from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from notes.models import Note

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def default_db_path() -> Path:
    return Path("data/notes.sqlite")


def isolated_db_path(tmp_dir: Path) -> Path:
    """Return a SQLite path under tmp_dir, never the default dev database."""
    return tmp_dir / "notes-test.sqlite"


def _row_to_note(row: sqlite3.Row) -> Note:
    return Note(
        id=UUID(row["id"]),
        title=row["title"],
        content=row["content"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


@dataclass(frozen=True, slots=True)
class NotesRepository:
    db_path: Path

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute(SCHEMA)
        return conn

    def create(self, note: Note) -> Note:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO notes (id, title, content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(note.id),
                    note.title,
                    note.content,
                    note.created_at.isoformat(),
                    note.updated_at.isoformat(),
                ),
            )
        return note

    def get(self, note_id: UUID) -> Note | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?",
                (str(note_id),),
            ).fetchone()
        return _row_to_note(row) if row is not None else None

    def list_all(self) -> tuple[Note, ...]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY created_at"
            ).fetchall()
        return tuple(_row_to_note(row) for row in rows)

    def update(self, note: Note) -> Note | None:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    note.title,
                    note.content,
                    note.updated_at.isoformat(),
                    str(note.id),
                ),
            )
            if cursor.rowcount == 0:
                return None
        return note

    def delete(self, note_id: UUID) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM notes WHERE id = ?", (str(note_id),))
            return cursor.rowcount > 0


def isolated_repository(tmp_dir: Path) -> NotesRepository:
    """Repository backed by a throwaway SQLite file for tests."""
    return NotesRepository(db_path=isolated_db_path(tmp_dir))
