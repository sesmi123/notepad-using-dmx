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

Not yet established — no framework or modules are in the tree. When code is added, match whatever conventions that stack uses (routing, validation, error mapping, test layout).

Expected patterns from the spec:

- CRUD resources under `/notes`
- Consistent error JSON, no stack traces or internals in responses
- Tests create their own data and clean up; no shared global fixtures required to run the suite
- Prefer the project's existing persistence/config mechanism once one exists; until then, the simplest local persistent store that works in tests

## Component relationships

The repo currently contains `spec.md`, Cursor/dmx config, and no `src/` (or equivalent) tree. After the first implementation phases, expect API handlers → service → repository → storage, plus a test suite beside or under the app package.

Do not introduce a second competing pattern for the same concern (two ORMs, two error formats, two config styles).
