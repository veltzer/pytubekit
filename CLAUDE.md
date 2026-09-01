# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

pytubekit is a Python CLI (entry point `pytubekit.main:main`) for bulk operations on a YouTube account via the YouTube Data API v3 — playlist cleanup, dedup, merge, diff, downloads.

## Generated files — do not hand-edit

`README.md` and `src/pytubekit/static.py` are rendered by rsconstruct's tera processor. To change them, edit the source instead and regenerate:

- Templates: `tera.templates/**/*.tera`
- Project metadata (name, description, version, author): `config/*.lua`
- Regenerate: `rsconstruct build` (this is also what CI runs)

`pyproject.toml` is hand-edited and is the authoritative dependency list; `uv.lock` pins the closure.

## Checks

Run the full local check suite before considering work done:

```
rsconstruct build
```

This runs `pytest tests`, `ruff check`, `pylint` and `mypy` over `src config tests`, plus `luacheck`, `taplo` and `actionlint`, and renders the tera templates.

## Code style

- Double-quoted strings only.
- Line length: 130 (ruff).
- No formatter is used; ruff is a linter only. Ignore the "black" badge in README — it's a stale template artifact.

## Gotchas

- Mutating commands are dry-run by default; they require `--do-delete` to actually change anything.
- YouTube Data API v3 has a 10,000 units/day quota; prefer the local/dump-file commands (`local_diff`, `local_dedup`, etc.) when possible. API responses are paginated at 50 items (handled by `PagedRequest` in `util.py`).
- Tests mock the YouTube API — no network or credentials needed for `pytest tests`.
- Auth is OAuth2 via `pygooglehelper`: `~/.config/pytubekit/client_secret.json` if present, else the copy shipped in the package by `hatch_build.py`. No environment variables are required at runtime.
