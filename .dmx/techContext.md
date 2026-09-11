# Tech Context

## Stack

Python 3.12, FastAPI, uvicorn, SQLite file on disk. Package layout is `src/notes/` managed with uv (`pyproject.toml`, `uv.lock`).

## Key dependencies

- `fastapi` — HTTP API (`notes.api` / `notes.app`)
- `uvicorn` — ASGI server
- `pytest` / `httpx` — tests (dev extra)
- stdlib `sqlite3` — persistence

## Dev setup

- Install: `uv sync --extra dev`
- Dev SQLite file: `data/notes.sqlite` (gitignored)
- Test SQLite: `isolated_repository(tmp_dir)` in `src/notes/repository.py` — never the default file
- Run API: `uv run uvicorn notes.app:app`
- Run tests: `uv run pytest -q`
- HTTP tests should call `create_app(isolated_sqlite_path)` so they never touch `data/notes.sqlite`
- API tests live in `tests/test_api.py` and use `TestClient(create_app(tmp_path / "notes-test.sqlite"))`

## Constraints

- Python 3.10 is the system default on this machine; dmx itself runs via uv on Python 3.12. If the API is Python, prefer 3.12+ to match that, or document an explicit version.
- No GitHub `origin` yet. `owner` and `repo` in `.dmx/config.md` are `{REQUIRED}` until a remote is added.
- GitHub MCP is connected but currently returns bad credentials. Branch/PR skills that call GitHub will fail until that token is fixed.
- Ticketing is `none`: branch names come from the work description, not from Jira/GitHub issue IDs.
- Integration and production branch are both `main`.
- Do not hard-code secrets. Keep test storage isolated from any later real data.
