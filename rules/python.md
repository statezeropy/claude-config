---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
---

# Python

Formatting, naming, import order, docstring presence, bare `except`, `print()` and comment
hygiene are enforced by the ruff/mypy configuration, not by this file. A project without that
configuration gets it from the `python-standards` skill. What follows is what tooling cannot
decide.

## Dependencies

- Add dependencies with `uv add <pkg>` (`--dev` for tooling); `dependencies` and
  `[dependency-groups]` are not edited by hand. Run with `uv run`, one-off tools with `uvx`.
- `uv sync` matches the lockfile, `uv lock` updates it. `uv.lock` is committed.
- Inside a container image or a CI bootstrap where uv is absent, pip is correct — with versions
  exported from the lockfile (`uv export`), not a hand-written range.

## Types

- Public functions and methods are annotated, in modern syntax (`list[str]`, `str | None`).
- Avoid `Any`; where it is unavoidable, a comment says why the type cannot be narrowed.
- Do not guess an external package's types. Read them in
  `.venv/lib/python*/site-packages/<pkg>/` — a `py.typed` marker, `.pyi` stubs, or the source.
  A guessed signature is a bug mypy cannot catch.

## Exceptions and logging

- Catch specific exception types. If you cannot recover, do not catch — let it propagate.
  Swallowing an exception to return a default erases the cause at the call site.
- Having caught one, do exactly one of: recover, wrap and re-raise as a domain exception
  (`raise OrderNotFound(...) from e`), or log it with `logger.exception()` at the top-level
  boundary (request handler, task runner, `main`).
- `logger = logging.getLogger(__name__)`. `print` is for user-facing CLI output only.
- Secrets, tokens and personal data are not logged.

## Input, secrets, paths

- Settings come from `pydantic-settings` with `.env`; `.env` is gitignored and `.env.example`
  committed. No secret is written in code.
- Every external input — request bodies, query params, files, env vars — passes through a
  Pydantic model before use.
- SQL goes through the ORM or parameter binding. Subprocesses take a list of arguments.
- Paths go through `pathlib`. An externally supplied path is resolved against an explicit
  anchor and checked with `is_relative_to`; a CWD-relative path breaks the moment the process
  starts from elsewhere.

## asyncio

- Library and service code never calls `asyncio.run()`; only the entrypoint owns the loop.
- No blocking I/O on the event loop: sync drivers and CPU work go through `asyncio.to_thread`
  or a process pool.
- Every external call has a timeout. An awaited call with no timeout is an outage waiting for a
  slow dependency.
- Concurrent work is scoped with `asyncio.TaskGroup`; a task that outlives its creator is a
  leak and a swallowed exception.
- Cancellation is honoured: nothing catches `CancelledError` and continues; cleanup goes in
  `finally`.

## Version

The package version is the GitHub Release tag (`git` rule). `pyproject.toml` declares
`dynamic = ["version"]` and hatch-vcs computes it; there is no version field to add or bump.
A build without `.git` passes the tag as `SETUPTOOLS_SCM_PRETEND_VERSION`, and fails without
it. Compare versions with `packaging.version.Version`, never as strings. The mechanics are in
the `python-standards` skill.
