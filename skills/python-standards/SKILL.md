---
name: python-standards
description: Enforce Python core coding standards, OOP, Type Hints, Security, and Error Handling. Includes `uv` for environment management. Use for ALL Python code writing, refactoring, or reviewing.
allowed-tools: Read, Grep, Glob, Bash
---

# Python Core Standards & Security Guide

**IMPORTANT:** Always respond in Korean to the user.

## When to use
- **New Python Code:** When writing any new Python modules, classes, or functions.
- **Refactoring:** When improving existing code for readability, performance, or maintainability.
- **Code Review:** When checking for style violations, security issues, or anti-patterns.
- **Dependency Management:** When adding packages or setting up project environments with `uv`.

## Instructions

### 1. Environment & Dependency Management (uv)
The project uses `uv` for management.

1.1. **Virtual Environments:**
   - Assume `.venv` managed by `uv`.
   - To create: `uv venv --python <version>`.

1.2. **Installing Packages:**
   - **MUST use:** `uv add <package_name>` (or `--dev`).
   - **NEVER use:** `pip install`.

1.3. **Running Scripts:**
   - **MUST use:** `uv run python script.py`.
   - This ensures correct environment activation.

1.4. **Syncing & Locking:**
   - Use `uv sync` to align environment with lockfile.
   - Use `uv lock` for dependency updates.
   - Use `uvx <tool>` or `uv tool run <tool>`.

### 2. Core Principles
- **Clarity:** Code must be easy to understand.
- **Consistency:** Follow project-wide style.
- **Simplicity:** Code should be "Pythonic".
- **Efficiency:** Adhere to DRY; use appropriate data structures.
- **Maintainability:** Easy to modify/extend.

### 3. Naming Conventions
3.1. **Variables/Functions:** `snake_case`. Verb-first for functions (e.g., `get_user_data`).
3.2. **Classes:** `PascalCase`.
3.3. **Constants:** `UPPER_CASE` at module level.
3.4. **Modules:** `lowercase` (short).

### 4. Code Style (ruff)
4.1. **Primary Rule:** Must pass `ruff format` and `ruff check`.
4.2. **Guidelines:**
   - Use 4-space indentation (no tabs).
   - Follow project `pyproject.toml` config.

### 5. Comments and Docstrings
5.1. **Docstrings:** Mandatory for public modules, functions, classes.
   - Use `"""Triple double quotes"""`.
   - Structure: Summary -> Args -> Returns -> Raises.
5.2. **Comments:** Explain *why*, not *what*. Use `#` sparingly.

### 6. Minimize Duplication (DRY)
- Identify redundant code.
- Abstract into functions/classes.

### 7. Object-Oriented Design
7.1. **SOLID Principles:** S (Single Resp), O (Open/Closed), L (Liskov), I (Interface Segregation), D (Dependency Inv).
7.2. **Composition over Inheritance:** Prefer `has-a` relationships.
7.3. **Python OOP:** Use Protocol for interfaces, `@dataclass` for value objects.

### 8. Conciseness & Pythonic Style
8.1. **Pythonic:** Use list comprehensions, `enumerate`, `zip`, `with`, f-strings.
8.2. **File Paths:**
   - **MUST use relative paths** from project root.
   - Use `pathlib.Path`.
   - Absolute paths are strictly prohibited unless for system-level config.

### 9. Type Hints (PEP 484)
9.1. **Required:** All public functions/methods must have types.
9.2. **Modern Syntax (3.9+):** `list[str]`, `dict[str, int]`, `str | None`.
9.3. **Tools:** Use `mypy`/`pyright`.
9.4. **Any:** Avoid `Any`. If used, explain why in comments.
9.5. **External Packages:**
   - Verify types by reading installed files in `.venv/.../site-packages/`.
   - Look for `.pyi` stubs or `py.typed` marker. **NEVER guess types.**

### 10. Error Handling & Logging (Robustness)
10.1. **Exceptions:**
   - Catch specific types (`ValueError`), NEVER bare `except:`.
   - **Dev Mode:** Let it crash (re-raise) to find bugs.
   - **Prod Mode:** Handle I/O & Network errors gracefully.
10.2. **Logging:**
   - **NEVER use `print()`.** Use `logging` module.
   - `logger = logging.getLogger(__name__)`.
   - Use `logger.exception()` in `except` blocks.

### 11. Security Principles
11.1. **Secrets:** **NEVER hardcode secrets**. Use `.env` & `pydantic-settings`.
11.2. **Input Validation:** Validate ALL external inputs using Pydantic.
11.3. **Injection Prevention:**
   - SQL: Use ORM or parameterized queries.
   - Command: Avoid `shell=True`. Use list arguments.
11.4. **Path Traversal:** Validate paths using `Path.resolve().is_relative_to()`.

### Checklist
Before finishing, verify:
- [ ] Used `uv add` / `uv run`.
- [ ] Code passes `ruff`, uses `snake_case`/`PascalCase`.
- [ ] Public functions have Docstrings & Type Hints.
- [ ] Logic follows DRY & SOLID.
- [ ] **Logging used instead of `print()`.**
- [ ] **No hardcoded secrets.**
- [ ] **Inputs & File paths are validated.**

## Examples

### UV Commands
```bash
uv add requests
uv run python main.py
```

### Type Hints
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### Logging
```python
import logging
logger = logging.getLogger(__name__)

try:
    process_data()
except ValueError as e:
    logger.exception("Failed to process data")
```
