# Tech Context

## Stack

Not yet established — update as the team defines this. There is no `package.json`, `pyproject.toml`, `go.mod`, or other manifest. Language, framework, and database are still open (the spec allows any small local persistent store).

## Key dependencies

None yet. Choose the minimum needed for HTTP, validation, persistence, and tests when implementation starts.

## Dev setup

Not yet established — update as the team defines this. After the first code lands, document:

- How to install dependencies
- How to run the API locally
- How to run tests
- Where local/test database files or URLs live

## Constraints

- Python 3.10 is the system default on this machine; dmx itself runs via uv on Python 3.12. If the API is Python, prefer 3.12+ to match that, or document an explicit version.
- No GitHub `origin` yet. `owner` and `repo` in `.dmx/config.md` are `{REQUIRED}` until a remote is added.
- GitHub MCP is connected but currently returns bad credentials. Branch/PR skills that call GitHub will fail until that token is fixed.
- Ticketing is `none`: branch names come from the work description, not from Jira/GitHub issue IDs.
- Integration and production branch are both `main`.
- Do not hard-code secrets. Keep test storage isolated from any later real data.
