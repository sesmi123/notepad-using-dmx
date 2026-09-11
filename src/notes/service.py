from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from notes.models import Note
from notes.repository import NotesRepository

TITLE_MAX_LENGTH = 200
CONTENT_MAX_LENGTH = 10_000


class NoteValidationError(Exception):
    """Invalid title or content. Map to HTTP 422."""

    def __init__(self, details: dict[str, str], message: str = "Validation failed") -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class NoteNotFoundError(Exception):
    """Note id does not exist. Map to HTTP 404."""

    def __init__(self, note_id: UUID) -> None:
        super().__init__("Note not found")
        self.note_id = note_id
        self.message = "Note not found"


def _field_error(value: str | None, *, name: str, max_length: int) -> str | None:
    if value is None:
        return f"{name} is required"
    if not value.strip():
        return f"{name} must not be empty"
    if len(value) > max_length:
        return f"{name} must be at most {max_length} characters"
    return None


def validate_title_and_content(title: str | None, content: str | None) -> dict[str, str]:
    details: dict[str, str] = {}
    title_error = _field_error(title, name="title", max_length=TITLE_MAX_LENGTH)
    content_error = _field_error(content, name="content", max_length=CONTENT_MAX_LENGTH)
    if title_error is not None:
        details["title"] = title_error
    if content_error is not None:
        details["content"] = content_error
    return details


@dataclass(frozen=True, slots=True)
class NotesService:
    repository: NotesRepository

    def create(self, title: str | None, content: str | None) -> Note:
        details = validate_title_and_content(title, content)
        if details:
            raise NoteValidationError(details)
        now = datetime.now(timezone.utc)
        note = Note(
            id=uuid4(),
            title=title or "",
            content=content or "",
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(note)

    def get(self, note_id: UUID) -> Note:
        note = self.repository.get(note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note

    def list_all(self) -> tuple[Note, ...]:
        return self.repository.list_all()

    def update(self, note_id: UUID, title: str | None, content: str | None) -> Note:
        existing = self.get(note_id)
        details = validate_title_and_content(title, content)
        if details:
            raise NoteValidationError(details)
        updated = Note(
            id=existing.id,
            title=title or "",
            content=content or "",
            created_at=existing.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        saved = self.repository.update(updated)
        if saved is None:
            raise NoteNotFoundError(note_id)
        return saved

    def delete(self, note_id: UUID) -> None:
        if not self.repository.delete(note_id):
            raise NoteNotFoundError(note_id)
