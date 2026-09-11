from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict

from notes.models import Note
from notes.service import NoteNotFoundError, NotesService, NoteValidationError


class NoteWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    content: str | None = None


class NoteRead(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


def note_to_read(note: Note) -> NoteRead:
    return NoteRead(
        id=note.id,
        title=note.title,
        content=note.content,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


def error_body(error: str, details: dict[str, str] | None = None) -> dict[str, object]:
    body: dict[str, object] = {"error": error}
    if details is not None:
        body["details"] = details
    return body


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NoteValidationError)
    async def handle_validation(_request: Request, exc: NoteValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content=error_body(exc.message, exc.details))

    @app.exception_handler(NoteNotFoundError)
    async def handle_not_found(_request: Request, exc: NoteNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content=error_body(exc.message))

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = {
            ".".join(str(part) for part in err.get("loc", ())): str(err.get("msg", "invalid"))
            for err in exc.errors()
        }
        return JSONResponse(
            status_code=422,
            content=error_body("Validation failed", details),
        )


def create_router(service: NotesService) -> APIRouter:
    router = APIRouter()

    @router.post("/notes", status_code=201)
    def create_note(body: NoteWrite) -> NoteRead:
        return note_to_read(service.create(body.title, body.content))

    @router.get("/notes")
    def list_notes() -> list[NoteRead]:
        return [note_to_read(note) for note in service.list_all()]

    @router.get("/notes/{note_id}")
    def get_note(note_id: UUID) -> NoteRead:
        return note_to_read(service.get(note_id))

    @router.put("/notes/{note_id}")
    def update_note(note_id: UUID, body: NoteWrite) -> NoteRead:
        return note_to_read(service.update(note_id, body.title, body.content))

    @router.delete("/notes/{note_id}", status_code=204)
    def delete_note(note_id: UUID) -> Response:
        service.delete(note_id)
        return Response(status_code=204)

    return router
