---
name: python-standards
description: Set up a Python project's tooling from the house templates — ruff/mypy/pytest configuration, pre-commit with the commit-msg hook, CI and release workflows — and wire the package version to the GitHub Release tag with hatch-vcs. Use when starting a Python project, adding the linter or CI configuration to one that lacks it, or fixing how a project computes its version. The Python conventions themselves load from the python rule whenever a .py file is touched.
metadata:
  reviewed: 2026-11-12
---

# Python project tooling

The conventions — dependencies, types, exceptions, input handling, asyncio — are in the
`python` rule (`~/.claude/rules/python.md`). This skill sets up the tooling that enforces the
rest: formatting, naming, import order, docstring presence, bare `except`, `print()`, TODO
format, commented-out code, `# noqa` / `# type: ignore` without a code.

## Setup

```bash
uv init --build-backend hatch              # hatchling 이 아래 버전 읽기를 맡는다
uv add --dev ruff mypy pre-commit pytest pytest-asyncio pytest-cov
cat <skill>/templates/pyproject-tooling.toml >> pyproject.toml   # [tool.*] 만 이어붙인다
cp <skill>/templates/.pre-commit-config.yaml .
mkdir -p .github/workflows && cp <skill>/templates/ci.yml <skill>/templates/release.yml .github/workflows/
uv run pre-commit install                  # 이후 커밋마다 자동 검사
uv run ruff check . && uv run ruff format . && uv run mypy .
```

The template holds tool configuration only, because `dependencies` and `[dependency-groups]`
are written by `uv add`.

## Version from the release tag

Two hand edits after `uv init --build-backend hatch` — the only edits made outside `[tool.*]`:

```toml
[project]
dynamic = ["version"]              # version = "…" 줄은 지운다

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"
```

`[tool.hatch.version]` and `[tool.uv] cache-keys` come with the template. What follows from it:

- `uv.lock` records no version for the project, so `uv sync --locked` passes across releases.
- Between releases the version is `X.Y.(Z+1).devN+g<sha>`.
- A build without `.git` — a Docker context, a rebuilt sdist — needs
  `SETUPTOOLS_SCM_PRETEND_VERSION=<X.Y.Z>`; `release.yml` passes the tag as
  `--build-arg VERSION` for this. There is no `fallback-version`: an image that reports `0.0.0`
  is worse than no image.
- `uv version` refuses a dynamic version. There is nothing to bump.
- One release per commit. With two release tags on one commit `git describe` picks one and the
  version is ambiguous.
- uv's own backend `uv_build` rejects dynamic metadata (astral-sh/uv#14561); that is why the
  backend is hatchling.
