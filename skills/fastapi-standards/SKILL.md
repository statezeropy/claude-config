---
name: fastapi-standards
description: API surface conventions for FastAPI — the /api/v1 prefix rule, resource URL shape (plural nouns, kebab-case, hierarchy, query params for filtering), status codes, Pydantic request/response models, and router/service/schema layout. Use when adding or renaming endpoints, designing an API's URL surface, or reviewing endpoints for RESTful compliance. Implementation guidance (auth, DB sessions, error handlers, testing) lives in fastapi-development, sqlalchemy, and pytest-patterns.
---

# FastAPI API Conventions

This skill covers **the shape of the API surface** only — the part a client sees and cannot be
changed later without breaking someone. For implementation patterns use the other skills:

| Need | Skill |
|---|---|
| Auth (OAuth2/JWT), error handlers, middleware, deployment | `fastapi-development` |
| Async sessions, queries, transactions | `sqlalchemy` |
| Schema/request model validation | `pydantic` |
| Tests, fixtures, `AsyncClient` | `pytest-patterns` |
| Migrations | `alembic` |

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

## 2. Status codes & responses

- `201` for a created resource (with the resource in the body), `204` for a delete with no body,
  `200` otherwise. `202` for a job accepted but not finished.
- `4xx` for the caller's mistake, `5xx` for ours. Never return `200 OK` with
  `{"error": ...}` — raise `HTTPException`, or a domain exception mapped by a handler.
- Every request and response body is a Pydantic model, declared via `response_model`. No bare
  `dict` returns — the OpenAPI schema is the contract, and a `dict` erases it.
- Separate models per direction: `ItemCreate` (input) / `Item` (output). Never accept an input
  model that carries `id`, `created_at`, or role fields the client must not set.

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

## Review checklist

- [ ] Path starts with `/api/v1`, prefix set at router include (not repeated per route).
- [ ] Plural noun collections, kebab-case, ≤3 levels of nesting, filters in query params.
- [ ] Correct method and status code; errors raised, never returned with `200`.
- [ ] `response_model` set; separate input/output models; no client-settable server fields.
- [ ] Route body has no business logic and no global state.
