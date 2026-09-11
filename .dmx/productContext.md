# Product Context

## Why this exists

Engineers need a small, complete backend example: a notes API that is specified clearly, persisted, validated, and tested. It is meant for local learning and demonstration, not as a multi-user product.

## How it works

HTTP clients send JSON to a notes API:

- `POST /notes` — create (201 + note body)
- `GET /notes/{id}` — read (200, or 404 if missing)
- `GET /notes` — list all notes (200)
- `PUT /notes/{id}` — replace title/content (200, or 404 if missing); `updated_at` changes, `created_at` does not
- `DELETE /notes/{id}` — delete (204, or 404 if missing)

A note has `id`, `title`, `content`, `created_at`, and `updated_at`. Title is required, non-blank, max 200 characters. Content is required, non-blank, max 10,000 characters. Invalid input is rejected with a client error (400 or 422) and no data change. Errors use a consistent JSON shape (`error`, optional `details`).

Storage is persistent (not in-memory-only). Restarting the process must not drop notes.

## Who uses it

- The developer learning dmx and implementing the spec
- Local HTTP clients or tests talking to the API
- No end-user accounts or UI in this project
