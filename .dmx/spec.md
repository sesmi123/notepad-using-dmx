---
branch: feature-add-notes-rest-api-with-persistence-and-tests
summary: Add notes REST API with persistence and tests
ticketing: none
---

# Add notes REST API with persistence and tests

**Ticket:** _(no ticketing system)_
**Type:** feature
**Branch:** feature-add-notes-rest-api-with-persistence-and-tests

---

## Context

This repo is an empty playground whose product is a small notes backend. Root `spec.md` already defines the HTTP contract, validation, persistence, tests, and acceptance criteria. This ticket turns that requirement into the first (and only) application in the tree: a layered REST API that stores notes across restarts.

## Scope

- HTTP/API layer: `POST /notes`, `GET /notes`, `GET /notes/{id}`, `PUT /notes/{id}`, `DELETE /notes/{id}`
- Business/service layer: validation rules, timestamp behaviour (`created_at` immutable, `updated_at` on write)
- Persistence/repository layer: durable storage, not in-memory-only; tests use isolated storage
- Note model: `id`, `title`, `content`, `created_at`, `updated_at`
- Consistent error JSON (`error`, optional `details`); 404 for missing notes; 400/422 for validation; 201/200/204 as specified
- Automated tests for CRUD, missing resources, validation, and persistence
- Docs: how to run the API, how to run tests, endpoints, request/response, validation

## Out of Scope

- Auth, accounts, authorization, sharing
- Search, tags, folders, rich text, attachments, realtime sync
- Frontend / UI and cloud deployment
- Pagination unless the chosen stack forces a listing convention
- Changing dmx config or inventing extra endpoints

## Technical Approach

No application code or package manifest exists yet, so this is a greenfield service that must still follow the layered layout in `systemPatterns.md`:

```text
HTTP/API layer → business/service layer → persistence/repository layer → storage
```

- HTTP handlers map status codes and error JSON only. They do not talk to the database.
- Service owns validation (title/content required, non-whitespace, 200 / 10_000 char limits) and timestamp rules.
- Repository owns persistence. Tests must hit the real persistence mechanism, with isolated test storage.
- Prefer the smallest local stack that matches this machine: Python 3.12 (uv) + a small HTTP framework + SQLite, unless Questions below choose otherwise.
- One error format, one persistence library, one test runner. Do not add a second pattern for the same concern.

TODO: lock language/framework and storage in Questions before `/dmx/plan`.

---

## Questions
<!-- Answer each question before running /dmx/plan. -->

1. Language and HTTP framework: use Python 3.12 + FastAPI (fits uv on this machine, easy tests), or a different stack?
   Answer: This is fine.

2. Persistence: SQLite file on disk (simplest local store that survives restart and isolates in tests), or something else?
   Answer: SQLite file on disk.

3. Note `id`: UUID string generated in the service, or integer autoincrement from the database?
   Answer: UUID

4. Validation error status: `422 Unprocessable Entity` (FastAPI default) or `400 Bad Request`?
   Answer: 422

5. Test runner and app layout: `pytest` with `src/notes/` (api, service, repository packages) plus `tests/`, or a different layout?
   Answer: This works.
