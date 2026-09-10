---
name: service-conventions
description: Cross-cutting house rules for a Python service that cannot be inferred from a library — test directory layout, marker and fixture names, test database naming, the oracle rule that decides what is a pytest test versus a row in tests/qa/qasheet.csv (human- or AI-judged QA), asyncio rules (no asyncio.run in libraries, timeouts on every external call, TaskGroup over bare create_task), and the CI workflow file split. Use when laying out or adding tests, writing async code, or adding a CI workflow, and when deciding whether a check belongs in pytest or in the QA sheet. Data-layer decisions are in data-conventions, API shape in fastapi-standards, LLM apps in llm-app-conventions.
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
├── e2e/               Playwright against the running stack
└── qa/qasheet.csv     judgment checks — walked by a person or an AI, not by pytest
```

**The oracle decides where a check goes, not its size.** If pass/fail can be computed —
a value, a status code, a schema, a length limit, a forbidden word, a row in the DB — it is a
pytest test, whatever layer it touches. If pass/fail needs someone to look at the result in
context — is this summary faithful, is this draft usable, does this screen read right — it is
a row in `tests/qa/qasheet.csv`. Never imitate a judgment oracle with a regex.

An LLM feature therefore splits: "the response parses into the Pydantic model, is under N
tokens, is in Korean" is pytest; "the response is a good answer" is the QA sheet.

- Markers `unit`, `integration`, `e2e`, `slow` are registered in
  `python-standards/templates/pyproject-tooling.toml`; `--strict-markers` rejects any other.
- Fixture names are fixed across projects: `client` (httpx `AsyncClient` over the app),
  `db_session` (a transaction rolled back after each test), `redis` (flushed per test),
  `settings_override`. A new project should not invent `api_client` or `session`.
- The test database is `<app>_test`; `ENV=test` selects it and disables outbound calls.
- Files `test_<module>.py`, functions `test_<behaviour>`:
  `test_login_rejects_expired_token`, not `test_login_2`.
- CI runs `unit` and `integration` on every push and PR; `e2e` on `main` and on tags.

## QA sheet — `tests/qa/qasheet.csv`

One file, four columns, no runner. It is read and executed by a person or by an AI agent that
can drive a browser; both must be able to pick it up without extra explanation.

| Column | Holds |
|---|---|
| `id` | `1, 2, 3, …` — referenced from PRs as "QA 3 fail" |
| `description` | **why this row exists** — what regressed, the issue number, what it guards. The judge needs the intent to judge in context |
| `scenario` | how to reproduce. Web: screen and actions. LLM: the input and the entry point (endpoint, screen, CLI) |
| `expected` | what a pass looks like, in words. This is the criterion — no scale, no rubric column |

- **`scenario` points at data, it does not contain it.** Long inputs (a ticket, a conversation,
  a document) are **seed data** and are referenced by id — `시드 티켓 1088(63턴)`. If the case is
  not in the seed, adding it to the seed comes first; the same seed serves the Playwright e2e
  tests, so the sheet turns the seed into a corpus of cases that actually broke. Inline input in
  a cell is at most one sentence.
- **When:** before merging any PR that touches a judgment surface — prompts, chains, graphs,
  UI rendering, user flows. **The whole sheet is walked**, never a subset.
- **Verdict:** each row is pass or fail against `expected`, judged on the actual output. No
  partial credit. **One failing row blocks the merge.**
- **Record:** one line in the PR body — `QA: 12/12 pass` or `QA: 3 fail — <what was seen>`.
  No results file; the PR is the record.
- **Rows are added** when a judgment-type regression is found or a judgment-type feature ships,
  with the trigger written into `description`. **Rows are removed** only when the feature is
  removed — never because they keep passing.
- Not collected by pytest, not run by CI, not documentation (so not under `docs/`).

Start from `templates/qasheet.csv`.

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
