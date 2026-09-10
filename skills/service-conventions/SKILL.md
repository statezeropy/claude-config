---
name: service-conventions
description: Cross-cutting house rules for a Python service that cannot be inferred from a library — test directory layout, marker and fixture names, test database naming, asyncio rules (no asyncio.run in libraries, timeouts on every external call, TaskGroup over bare create_task), and the CI workflow file split. Use when laying out or adding tests, writing async code, or adding a CI workflow. Data-layer decisions are in data-conventions, API shape in fastapi-standards, LLM apps in llm-app-conventions.
metadata:
  reviewed: 2026-09-10
---

# Service conventions

Decisions, not knowledge: each has several defensible answers, and this is the one every
project uses. Library mechanics are not here — read the installed version
(`python-standards` §2). Sibling decision skills: `data-conventions` (PostgreSQL, SQLite,
SQLAlchemy, Alembic, Redis), `fastapi-standards` (API surface and internals),
`llm-app-conventions`.

## Tests

```
tests/
├── conftest.py        session-wide fixtures: app, engine, settings override
├── factories.py       test-data builders (plain functions or factory_boy)
├── unit/              no I/O, no network — seconds
├── integration/       real DB/Redis from docker compose; own conftest.py
└── e2e/               Playwright against the running stack
```

- Markers `unit`, `integration`, `e2e`, `slow` are registered in
  `python-standards/templates/pyproject-tooling.toml`; `--strict-markers` rejects any other.
- Fixture names are fixed across projects: `client` (httpx `AsyncClient` over the app),
  `db_session` (a transaction rolled back after each test), `redis` (flushed per test),
  `settings_override`. A new project should not invent `api_client` or `session`.
- The test database is `<app>_test`; `ENV=test` selects it and disables outbound calls.
- Files `test_<module>.py`, functions `test_<behaviour>`:
  `test_login_rejects_expired_token`, not `test_login_2`.
- CI runs `unit` and `integration` on every push and PR; `e2e` on `main` and on tags.

## asyncio

- Library and service code never calls `asyncio.run()`; only the entrypoint owns the loop.
- No blocking I/O on the event loop: sync drivers and CPU work go through
  `asyncio.to_thread` or a process pool.
- **Every external call has a timeout** (`async with asyncio.timeout(...)`, or the client's
  own). An awaited call with no timeout is an outage waiting for a slow dependency.
- Concurrent work is scoped with `asyncio.TaskGroup`, not bare `create_task` — a task that
  outlives its creator is a leak and a swallowed exception.
- Cancellation is honoured: no `except Exception` that eats `CancelledError`; cleanup goes in
  `finally`.

## CI workflows

- One concern per file under `.github/workflows/`: `ci.yml` (lint, type, test on push/PR —
  `python-standards/templates/ci.yml`), `release.yml` (on `v*` tags; `git-workflow` makes the
  tag the production trigger), scheduled jobs in their own file.
- A CI step runs **the same command the developer runs** (`uv run ruff check .`), never a
  CI-only variant. If it passes locally it passes in CI, and vice versa.
