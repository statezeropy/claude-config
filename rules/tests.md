---
paths:
  - "**/tests/**"
  - "**/conftest.py"
  - "**/.github/workflows/**"
---

# Tests and CI

## Layout

```
tests/
├── conftest.py        session-wide fixtures: app, engine, settings override
├── factories.py       test-data builders
├── unit/              no I/O, no network — seconds
├── integration/       real DB/Redis from docker compose; own conftest.py
├── e2e/               Playwright against the running stack
└── qa/qasheet.csv     judgment checks — walked by a person or an AI, not by pytest
```

- Markers are `unit`, `integration`, `e2e`, `slow`; `--strict-markers` rejects any other.
- Fixture names are the same in every project: `client` (an async HTTP client over the app),
  `db_session` (a transaction rolled back after each test), `redis` (flushed per test),
  `settings_override`.
- The test database is `<app>_test`; `ENV=test` selects it and disables outbound calls.
- Files are `test_<module>.py`, functions `test_<behaviour>`:
  `test_login_rejects_expired_token`, not `test_login_2`.

## The oracle decides where a check goes

If pass/fail can be computed — a value, a status code, a schema, a length limit, a forbidden
word, a row in the DB — it is a pytest test, whatever layer it touches. If pass/fail needs
someone to look at the result in context — is this summary faithful, does this screen read
right — it is a row in `tests/qa/qasheet.csv`. A judgment is not imitated with a regex.

An LLM feature therefore splits: "the response parses into its model, is under N tokens, is in
Korean" is pytest; "the response is a good answer" is the QA sheet.

## QA sheet

One CSV, four columns, no runner; a person or an AI agent that can drive a browser picks it up
without further explanation.

```csv
id,description,scenario,expected
1,"요약이 원문에 없는 사실을 만들어낸 적이 있음. 압축이지 창작이 아님을 확인","시드 티켓 1042 → /tickets/1042 → '요약' 클릭","요약의 모든 문장이 원문에서 근거를 찾을 수 있다. 원문에 없는 이름·금액·날짜가 나오면 실패"
```

- `description` says why the row exists — what regressed, what it guards — so the judge can
  judge in context. `expected` is the criterion in words; there is no scale or rubric column.
- `scenario` points at data and does not contain it: long inputs are seed data referenced by
  id, shared with the e2e tests. Inline input is one sentence at most.
- The whole sheet is walked before merging any PR that touches a judgment surface — prompts,
  chains, UI rendering, user flows. Each row is pass or fail on the actual output; one failing
  row blocks the merge.
- The record is one line in the PR body: `QA: 12/12 pass` or `QA: 3 fail — <what was seen>`.
- A row is added when a judgment-type regression is found or a judgment-type feature ships, and
  removed only when the feature is removed.

## CI

- One concern per workflow file: `ci.yml` (lint, type, test on push and PR), `release.yml`
  (on `release: published`), scheduled jobs in their own file.
- A CI step runs the same command the developer runs (`uv run ruff check .`), never a CI-only
  variant.
- `unit` and `integration` run on every push and PR; `e2e` on `main` and on releases.
