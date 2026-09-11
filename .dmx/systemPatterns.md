# System Patterns

## High-level architecture

No application code exists yet. The spec requires a layered layout when implementation starts:

```text
HTTP/API layer
      |
      v
Business/service layer
      |
      v
Persistence/repository layer
      |
      v
Database/storage
```

The HTTP layer should not contain database-specific details. Business logic should not depend on HTTP request objects unless a chosen framework forces that. The persistence layer owns storage.

## Key patterns

Persistence is a frozen `NotesRepository` in `src/notes/repository.py`. It owns SQLite schema and CRUD. HTTP handlers must not open SQLite connections.

The service layer is `NotesService` in `src/notes/service.py`. It owns UUID generation, timestamps, and title/content validation. It raises `NoteValidationError` (field `details`, map to HTTP 422) and `NoteNotFoundError` (map to HTTP 404). The API maps these exceptions; it must not re-implement validation.

The HTTP layer is FastAPI in `src/notes/api.py`. Handlers only map HTTP and JSON. Exception handlers turn `NoteValidationError` into 422 `{error, details}` and `NoteNotFoundError` into 404 `{error}`. `create_app(db_path)` in `src/notes/app.py` wires repository → service → router. Tests must pass an isolated SQLite path, not the default file.

Note records are an immutable `Note` dataclass in `src/notes/models.py` (UUID `id`, timestamps as `datetime`).

Expected patterns from the spec:

- CRUD resources under `/notes`
- Consistent error JSON, no stack traces or internals in responses
- Tests create their own data and clean up; no shared global fixtures required to run the suite
- Prefer the project's existing persistence/config mechanism once one exists; until then, the simplest local persistent store that works in tests

## Component relationships

`src/notes/models.py` is the in-memory note shape. `src/notes/repository.py` maps it to SQLite. `src/notes/service.py` is the business layer. `src/notes/api.py` + `src/notes/app.py` are the HTTP layer: API → service → repository.

Do not introduce a second competing pattern for the same concern (two ORMs, two error formats, two config styles).
