# Notes API

Small REST API for text notes. Notes are stored in SQLite and survive process restarts.

## Setup

Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required.

```bash
uv sync --extra dev
```

## Run the API

```bash
uv run uvicorn notes.app:app
```

Default database file: `data/notes.sqlite` (created on first write, gitignored).

## Run tests

```bash
uv run pytest -q
```

Tests use a temporary SQLite file via `create_app(db_path)`. They do not touch `data/notes.sqlite`.

## Endpoints

| Method | Path | Success |
| --- | --- | --- |
| `POST` | `/notes` | `201 Created` |
| `GET` | `/notes` | `200 OK` |
| `GET` | `/notes/{id}` | `200 OK` |
| `PUT` | `/notes/{id}` | `200 OK` |
| `DELETE` | `/notes/{id}` | `204 No Content` |

Missing notes return `404 Not Found`. Invalid input returns `422 Unprocessable Entity`.

### Create / update body

```json
{
  "title": "Shopping List",
  "content": "Milk, bread, and apples"
}
```

### Note response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Shopping List",
  "content": "Milk, bread, and apples",
  "created_at": "2026-01-01T00:00:00+00:00",
  "updated_at": "2026-01-01T00:00:00+00:00"
}
```

`id` is a UUID. `created_at` does not change on update. `updated_at` does.

List (`GET /notes`) returns an array of note objects.

### Errors

```json
{
  "error": "Note not found"
}
```

```json
{
  "error": "Validation failed",
  "details": {
    "title": "title must not be empty"
  }
}
```

## Validation

`title` and `content` are required.

- Reject missing, empty, or whitespace-only values
- `title` max 200 characters
- `content` max 10,000 characters
- Malformed JSON is rejected with `422`
- Failed validation does not create or update a note
