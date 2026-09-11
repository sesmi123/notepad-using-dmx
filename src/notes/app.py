from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from notes.api import create_router, register_exception_handlers
from notes.repository import NotesRepository, default_db_path
from notes.service import NotesService


def create_app(db_path: Path | None = None) -> FastAPI:
    repository = NotesRepository(db_path=db_path or default_db_path())
    service = NotesService(repository=repository)
    app = FastAPI(title="Notes API")
    register_exception_handlers(app)
    app.include_router(create_router(service))
    return app


app = create_app()
