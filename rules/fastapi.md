---
paths:
  - "**/{api,routers,schemas}/**/*.py"
  - "**/main.py"
---

# FastAPI

The shape of the API surface — the part a client sees and that cannot change later without
breaking someone — and the names every project shares. Library mechanics (OAuth2/JWT, session
handling, exception handlers, test clients) move with versions: read the installed one.

## URL surface

- **Every endpoint is served under `/api/v1`**, set once where the router is included, not on
  each route. An incompatible contract becomes `/api/v2` alongside `v1`; `v1` never changes
  silently.
- Resources are plural nouns in kebab-case (`/api/v1/user-profiles`); the HTTP method is the
  verb. Nesting shows ownership, three levels at most. Filtering, sorting and paging are query
  parameters.
- An asynchronous job is itself a resource: `POST /api/v1/summarizations` creates a job that
  can then be read with `GET`.
- **Operational endpoints live outside the prefix** — unversioned, unauthenticated, identical
  in every project, because they are a contract with the infrastructure:

| Path | Answers | Response |
|---|---|---|
| `GET /health` | is the process up | `200 {"status": "ok"}`, no dependency touched |
| `GET /ready` | can it serve traffic | `200 {"status": "ok", "checks": {"db": "ok", "redis": "ok"}}`; a failing check → `503`, same shape |
| `GET /metrics` | Prometheus scrape, only where metrics are exposed | text exposition format |

## Status codes and bodies

- `201` for a created resource with the resource in the body, `204` for a delete, `202` for a
  job accepted but not finished, `200` otherwise.
- `4xx` is the caller's mistake, `5xx` ours. An error is raised, never returned as `200` with
  `{"error": ...}`.
- Every request and response body is a Pydantic model declared through `response_model`; a
  bare `dict` erases the OpenAPI contract.
- Models are separate per direction: `XCreate`, `XUpdate` (every field optional), `XRead`. An
  input model carries no `id`, `created_at` or role field the client must not set; a read
  model exposes no password hash or internal flag.

## Layout

```
app/
├── main.py        app creation, router include, exception handlers
├── api/           routers — parse the request, return the response
├── schemas/       Pydantic models
├── services/      business logic
└── models/        SQLAlchemy models
```

Routes stay thin: parse, delegate to a service, return. Per-request resources (session, current
user, settings) arrive through `Depends()`, not module-level state. A repository layer on top
of the ORM is added only when a service must swap its data source.

## Names every project shares

| Thing | Where and what it is called |
|---|---|
| settings | `app/core/config.py` — `class Settings(BaseSettings)`, `get_settings()` cached, injected with `Depends`. Env names: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ENV` (`dev` / `test` / `prod`), `LOG_LEVEL`, `PORT`, `LLM_BASE_URL` |
| dependencies | `app/api/deps.py` — `get_db`, `get_settings`, `get_current_user`, `get_current_active_user`, `require_role(...)` |
| tenancy | multi-tenant products only: `get_tenant` in `deps.py` is the only reader of the tenant id (the JWT `tid` claim), never a body, query or header the client controls |
| errors | body `{"detail": str, "error_code": "UPPER_SNAKE"}`. Domain exceptions in `app/core/exceptions.py` subclass `AppError(code, status)`, mapped by one handler in `main.py`. Services raise domain errors, not `HTTPException` |
| routers | `app/api/v1/router.py` aggregates; each module declares `router = APIRouter(prefix="/users", tags=["users"])`; tag == resource == module name |
| auth | `POST /api/v1/auth/token`; `Authorization: Bearer <jwt>`; claims `sub`, `exp`, `scopes` (plus `tid` when multi-tenant) |
| request id | middleware echoes `X-Request-ID` or mints a uuid4; every log line carries it |

## Caller-facing text

FastAPI publishes some strings to whoever calls the API: decorator `summary` / `description`,
the route function's docstring, `Field(description=)`, model docstrings, `FastAPI(description=)`
and error `detail`. Their reader is the caller, so the comment rules in `CLAUDE.md` do not
decide their content.

- Write what the endpoint does, what goes in and comes out, and what each status code means.
  One line is the default.
- Leave out design rationale, internal structure, a partner's circumstances, history and
  `docs/design/` paths — the caller cannot see the repository.
- Module docstrings and `#` comments in the API layer are not published; they follow
  `CLAUDE.md`.
