from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import pytest
import sqlite3

from notes.models import Note
from notes.repository import (
    NotesRepository,
    default_db_path,
    isolated_db_path,
    isolated_repository,
)


def _note(*, title: str = "title", content: str = "content", created_offset: int = 0) -> Note:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=created_offset)
    return Note(
        id=uuid4(),
        title=title,
        content=content,
        created_at=now,
        updated_at=now,
    )


def test_default_db_path_is_dev_file() -> None:
    assert default_db_path() == Path("data/notes.sqlite")


def test_isolated_db_path_is_not_the_dev_file(tmp_path: Path) -> None:
    path = isolated_db_path(tmp_path)

    assert path.parent == tmp_path
    assert path != default_db_path()
    assert path.name == "notes-test.sqlite"


def test_isolated_repository_uses_isolated_path(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)

    assert repo.db_path == isolated_db_path(tmp_path)


def test_create_then_get_returns_the_same_note(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    note = _note()

    created = repo.create(note)
    loaded = repo.get(note.id)

    assert created == note
    assert loaded == note


def test_get_returns_none_when_id_is_missing(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)

    assert repo.get(uuid4()) is None


def test_list_all_returns_empty_tuple_when_no_notes(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)

    assert repo.list_all() == ()


def test_list_all_orders_by_created_at(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    later = _note(title="later", created_offset=10)
    earlier = _note(title="earlier", created_offset=0)

    repo.create(later)
    repo.create(earlier)

    listed = repo.list_all()

    assert [note.title for note in listed] == ["earlier", "later"]


def test_update_replaces_title_content_and_updated_at(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    original = repo.create(_note())
    updated = Note(
        id=original.id,
        title="new title",
        content="new content",
        created_at=original.created_at,
        updated_at=original.updated_at + timedelta(seconds=30),
    )

    result = repo.update(updated)
    loaded = repo.get(original.id)

    assert result == updated
    assert loaded == updated
    assert loaded is not None
    assert loaded.created_at == original.created_at


def test_update_returns_none_when_id_is_missing(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    missing = _note()

    assert repo.update(missing) is None
    assert repo.get(missing.id) is None


def test_delete_returns_true_and_removes_note(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    note = repo.create(_note())

    deleted = repo.delete(note.id)

    assert deleted is True
    assert repo.get(note.id) is None


def test_delete_returns_false_when_id_is_missing(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)

    assert repo.delete(uuid4()) is False


def test_data_survives_new_repository_on_same_file(tmp_path: Path) -> None:
    first = isolated_repository(tmp_path)
    note = first.create(_note())

    second = NotesRepository(db_path=first.db_path)

    assert second.get(note.id) == note


def test_create_rejects_duplicate_id(tmp_path: Path) -> None:
    repo = isolated_repository(tmp_path)
    note = repo.create(_note())

    with pytest.raises(sqlite3.IntegrityError):
        repo.create(note)
