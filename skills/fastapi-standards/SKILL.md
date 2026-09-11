---
name: fastapi-standards
description: API surface conventions for FastAPI — the /api/v1 prefix rule, resource URL shape (plural nouns, kebab-case, hierarchy, query params for filtering), status codes, Pydantic request/response models, and router/service/schema layout. Use when adding or renaming endpoints, designing an API's URL surface, or reviewing endpoints for RESTful compliance. Also the internals every project shares — settings and env names, dependency names, schema suffixes (Create/Update/Read), error response shape, router registration, auth path, request id. Library mechanics are read from the installed version; data-layer decisions live in data-conventions.
metadata:
  reviewed: 2026-09-10
---

# FastAPI API Conventions

This skill covers **the shape of the API surface** only — the part a client sees and cannot be
changed later without breaking someone. Implementation mechanics (OAuth2/JWT, session handling,
exception handlers, `AsyncClient` tests) are deliberately not pinned here: they move with library
versions, so read the installed one — `.venv/lib/python*/site-packages/<pkg>` and its docs via
MCP (`python-standards` §2). Column types, migrations and Redis keys are in `data-conventions`;
test layout in `service-conventions`.

## 1. URL surface

**Every endpoint is served under the `/api/v1` prefix.** Set it once where the router is
included (`app.include_router(router, prefix="/api/v1")`), not on each route. A new
incompatible contract becomes `/api/v2` alongside `v1`; it never silently changes `v1`.

The rest follows standard REST resource naming:

| Rule | Good | Bad |
|---|---|---|
| Nouns — the HTTP method is the verb | `POST /api/v1/chats` | `POST /api/v1/createChat` |
| Plural collections | `/api/v1/users` | `/api/v1/user` |
| kebab-case in paths | `/api/v1/user-profiles` | `/api/v1/userProfiles`, `/api/v1/user_profiles` |
| Nesting shows ownership, max 3 levels | `/api/v1/users/{id}/chats` | `/api/v1/get-user-chats?id=` |
| Filtering/sorting/paging in query params | `/api/v1/chats?sort=desc&limit=10` | `/api/v1/chats/recent/10` |

*Exception:* an asynchronous processing job is itself a resource — `POST /api/v1/summarizations`
creates a job you can then `GET`. That is a noun, not a disguised verb.

**Operational endpoints live outside the prefix.** They are a contract with the infrastructure
(compose `healthcheck`, nginx/Caddy, CI smoke), not with API clients, so they are unversioned,
unauthenticated, and identical in every project:

| Path | Answers | Response |
|---|---|---|
| `GET /health` | is the process up (liveness) | `200 {"status": "ok"}` — no dependencies touched |
| `GET /ready` | can it serve traffic (readiness) | `200 {"status": "ok", "checks": {"db": "ok", "redis": "ok"}}`; any failing check → `503` with the same shape |
| `GET /metrics` | Prometheus scrape, only when the project exposes metrics | text exposition format |

Compose and CI probe `/health`; a load balancer or orchestrator gates on `/ready`. Nothing else
escapes `/api/v1`.

## 2. Status codes & responses

- `201` for a created resource (with the resource in the body), `204` for a delete with no body,
  `200` otherwise. `202` for a job accepted but not finished.
- `4xx` for the caller's mistake, `5xx` for ours. Never return `200 OK` with
  `{"error": ...}` — raise `HTTPException`, or a domain exception mapped by a handler.
- Every request and response body is a Pydantic model, declared via `response_model`. No bare
  `dict` returns — the OpenAPI schema is the contract, and a `dict` erases it.
- Separate models per direction: `ItemCreate` (input), `ItemUpdate` (all fields optional),
  `ItemRead` (output). Never accept an input model that carries `id`, `created_at`, or role
  fields the client must not set.

## 3. Layout

```
app/
├── main.py        앱 생성, 라우터 include, 예외 핸들러 등록
├── api/           라우터 — 요청 파싱과 응답만. 비즈니스 로직 금지
├── schemas/       Pydantic 모델
├── services/      비즈니스 로직 — 라우터가 얇아지는 만큼 여기가 두꺼워진다
└── models/        SQLAlchemy 모델
```

Routes stay thin: parse, delegate to a service, return. Anything a second endpoint could need
belongs in `services/`. Shared per-request resources (session, current user, settings) arrive
through `Depends()` — never module-level global state.

Adding a repository layer on top of SQLAlchemy is optional and usually unnecessary; the ORM
session is already a data-mapper. Add one only when a service must swap the data source.

## 4. Internals every project shares

| Thing | Where and what it is called |
|---|---|
| settings | `app/core/config.py` — `class Settings(BaseSettings)`, `get_settings()` with `@lru_cache`, injected by `Depends(get_settings)`. Env names are fixed: `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ENV` (`dev` / `test` / `prod`), `LOG_LEVEL`, `PORT`, `TENANCY_MODE` (`saas` / `single`), `TENANT_ID` (single only), `LLM_BASE_URL`, `AUTH_BACKEND` |
| tenancy | `get_tenant` in `deps.py` is the **only** reader of the tenant id: `saas` → the JWT `tid` claim, `single` → `settings.tenant_id`. Never from a body, query or header the client controls. Every service call receives the tenant from this dependency (`data-conventions` §Tenancy) |
| environment | the app promises the same behaviour behind any edge — plain HTTP on `PORT`, proxy headers trusted only from the proxy, `/health` + `/ready`, graceful SIGTERM, no local state, JSON logs to stdout (`deployment-conventions`). Anything that needs the internet is behind a capability flag |
| dependencies | `app/api/deps.py` — `get_db`, `get_settings`, `get_current_user`, `get_current_active_user`, `require_role(...)`. Same names in every project |
| schemas | `XCreate` (input), `XUpdate` (every field optional), `XRead` (output, `model_config = ConfigDict(from_attributes=True)`). Read models never expose password hashes or internal flags |
| errors | body `{"detail": str, "error_code": "UPPER_SNAKE"}`. Domain exceptions in `app/core/exceptions.py` subclass `AppError(code, status)`; one `@app.exception_handler(AppError)` in `main.py`. Services raise domain errors, never `HTTPException` |
| routers | `app/api/v1/router.py` aggregates; each module declares `router = APIRouter(prefix="/users", tags=["users"])`; **tag == resource == module name**. `main.py` includes the aggregate once with `prefix="/api/v1"` |
| lifecycle | a `lifespan` context manager for startup/shutdown (`on_event` is deprecated) |
| auth | `POST /api/v1/auth/token`; `Authorization: Bearer <jwt>`; claims `sub`, `exp`, `scopes`, `tid`. The identity source is an adapter chosen by `AUTH_BACKEND` — OIDC in `saas`; the on-site backend (hospital directory or local accounts) is decided per deployment. Password hashing via `pwdlib[bcrypt]` |
| request id | middleware echoes `X-Request-ID` if present, else mints a uuid4; every log line carries it; JSON logs when `ENV=prod` |

## Review checklist

- [ ] Path starts with `/api/v1`, prefix set at router include (not repeated per route);
      only `/health`, `/ready`, `/metrics` are outside it.
- [ ] Plural noun collections, kebab-case, ≤3 levels of nesting, filters in query params.
- [ ] Correct method and status code; errors raised, never returned with `200`.
- [ ] `response_model` set; separate input/output models; no client-settable server fields.
- [ ] Route body has no business logic and no global state.
- [ ] Dependency, schema and env names match §4 — nothing project-specific invented.
