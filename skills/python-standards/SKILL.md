---
name: python-standards
description: Python conventions a linter cannot enforce — uv dependency management, verifying types of external packages, exception and logging policy, secrets, input validation, and path handling. Formatting, naming, import order, docstring presence and print/bare-except bans are delegated to the ruff/mypy config in templates/. Use when writing, refactoring, or reviewing Python, and when setting up a new project's tooling.
---

# Python Standards

Formatting, naming, import order, docstring presence, bare `except`, and `print()` are **not
enforced by this document — they are enforced by the linter.** Set that up once per project:

```bash
uv init                                    # [project] 생성 — uv 가 관리하는 영역
uv add --dev ruff mypy pre-commit pytest pytest-asyncio pytest-cov
cat <skill>/templates/pyproject-tooling.toml >> pyproject.toml   # [tool.*] 만 이어붙인다
cp <skill>/templates/.pre-commit-config.yaml .
uv run pre-commit install                  # 이후 커밋마다 자동 검사
uv run ruff check . && uv run ruff format . && uv run mypy .
```

`dependencies` 와 `[dependency-groups]` 는 `uv add` 가 쓰는 곳이므로 손으로 편집하지 않는다.
템플릿이 도구 설정만 담은 이유가 그것이다.

What follows is only what tooling cannot decide for you.

## 1. Environment & dependencies (uv)

- Add dependencies with `uv add <pkg>` (`--dev` for tooling). Never manage project dependencies
  with `pip install`.
- Run with `uv run python script.py`; run one-off tools with `uvx <tool>`.
- `uv sync` to match the lockfile, `uv lock` to update it. **Commit `uv.lock`.**
- *Exception:* inside a container image or a CI bootstrap where uv is absent, pip is correct.
  Even there the versions come from the lockfile (`uv export`) — never from a hand-written range.

## 2. Types

- Public functions and methods are annotated. Modern syntax only: `list[str]`, `dict[str, int]`,
  `str | None` — not `typing.List` or `Optional[...]`.
- Avoid `Any`. When unavoidable, a comment says why the type cannot be narrowed.
- **Never guess an external package's types — read them.** Check
  `.venv/lib/python*/site-packages/<pkg>/` for a `py.typed` marker or `.pyi` stubs; if there are
  none, read the source. A guessed signature is a bug that mypy cannot catch.

## 3. Exceptions & logging

- Catch specific exception types. If you cannot recover, do not catch — let it propagate.
  Swallowing an exception to return a default erases the cause at the call site.
- Having caught it, do exactly one of: recover, wrap and re-raise as a domain exception
  (`raise OrderNotFound(...) from e`), or log it with `logger.exception()` at the top-level
  boundary (request handler, task runner, `main`).
- `logger = logging.getLogger(__name__)`. **No `print()` for logging** — user-facing CLI output
  via `print`/`rich` is fine and expected.
- Never log secrets, tokens, or personal data.

## 4. Security

- No hardcoded secrets. Use `pydantic-settings` with `.env` — `.env` is gitignored,
  `.env.example` is committed.
- Validate every external input (request bodies, query params, files, env vars) through a
  Pydantic model before use.
- SQL through the ORM or parameter binding. Never build queries with string formatting.
- Subprocesses take a list of arguments, never `shell=True`.
- Paths go through `pathlib`. Resolve externally supplied paths against an explicit anchor and
  verify they do not escape it:

  ```python
  root = Path(__file__).resolve().parent      # 또는 설정에서 온 명시적 루트
  target = (root / user_input).resolve()
  if not target.is_relative_to(root):
      raise ValueError(f"path escapes {root}: {user_input}")
  ```

  Do not open a CWD-relative path — it breaks the moment the process is started from elsewhere.
