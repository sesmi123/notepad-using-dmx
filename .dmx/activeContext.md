# Active Context

## Open Learnings
_(none yet — append observations here during implementation; promoted to core files on commit or create-pr)_

## Open Decisions
- GitHub MCP still uses a placeholder PAT in `~/.cursor/mcp.json` (`ghp_your_token_here`). `gh` CLI is not logged in. Git push works via HTTPS credentials; MCP `create_pull_request` may still fail until a real token or `gh auth login` is set.

## Session Notes
- `/dmx/init` completed with workflow `sdlc` and ticketing `none`.
- Product requirements live in root `spec.md` (Notepad REST API). `.dmx/spec.md` is created on the first ticket branch.
- spec loop completed (outcome: success) — chained to plan (job `feature-add-notes-rest-api-with-persistence-and-tests`).
- plan loop completed (outcome: success) — chained to dev (job `feature-add-notes-rest-api-with-persistence-and-tests`).
- Added SQLite notes repository and project skeleton — Phase 1 complete.
- Added NotesService validation and CRUD — Phase 2 complete.
- Added FastAPI notes router and create_app() — Phase 3 complete.
- Added HTTP TestClient tests and README — Phase 4 complete.
- dev loop completed (outcome: warning) (job `feature-add-notes-rest-api-with-persistence-and-tests`).
- validate loop completed (outcome: success) — chained to release (job `feature-add-notes-rest-api-with-persistence-and-tests`).
- Origin is `https://github.com/sesmi123/notepad-using-dmx.git` (personal account, not Wasabi). Feature branch was accidentally renamed to `main`; restored `feature-add-notes-rest-api-with-persistence-and-tests`. GitHub `main` already contains the full feature, so a PR would only show later config/job commits unless `origin/main` is reset to the init commit.
