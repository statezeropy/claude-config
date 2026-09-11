---
name: data-conventions
description: Decisions for the data layer that stay identical across every project — PostgreSQL and SQLite column types, common columns and mixins, SQLAlchemy Base with naming convention, session and transaction rules, Alembic env.py and revision rules, enum storage, multi-tenancy (tenant_id on every table, tenant-first indexes, PostgreSQL row-level security in both deployment modes), the audit log, and the Redis key vocabulary, TTL tiers, value format and single key-builder module. Use when creating or changing tables, models, migrations, cache/lock/session keys, or wiring a database engine.
metadata:
  reviewed: 2026-09-10
---

# Data conventions

Decisions, not knowledge: each item has several defensible answers, and this is the one every
project uses so that a table or a Redis key written in one service is recognisable in the next.
Library mechanics are not here — read the installed version (`python-standards` §2).

## Column types

| Need | PostgreSQL | SQLAlchemy | Not |
|---|---|---|---|
| timestamp | `timestamptz` | `DateTime(timezone=True)` | naive `timestamp` |
| free text | `TEXT` | `Text`, or `String` without length | `VARCHAR(n)` unless the length is a business rule |
| primary key | `BIGINT` identity | `BigInteger().with_variant(Integer, "sqlite"), Identity()` | `INTEGER`, `SERIAL` |
| external id | `UUID`, only when minted outside the DB | `Uuid` | UUID as the pk "just because" |
| semi-structured | `JSONB` | `JSON().with_variant(JSONB, "postgresql")` | `TEXT` holding JSON |
| exact amounts | `NUMERIC(p, s)` | `Numeric(p, s)` | `FLOAT` |
| enum | `TEXT` + `CHECK` | `String` + `StrEnum` + `CheckConstraint` | native `ENUM` |

- Enums are text with a CHECK constraint, never a native PostgreSQL `ENUM`: adding a value is a
  one-line migration instead of `ALTER TYPE`, autogenerate sees it, and SQLite behaves the same.
- The `with_variant` pattern is the general rule: **a model runs unchanged on SQLite in tests
  and PostgreSQL in production.** The pk variant matters — SQLite only auto-assigns ids to an
  `INTEGER PRIMARY KEY`, so a bare `BigInteger` pk fails on insert there.

## Naming

- Tables plural snake_case (`user_profiles`); columns snake_case; booleans are predicates
  (`is_active`); timestamps end `_at`, dates `_on`; foreign keys `<singular>_id` (`user_id`).
- **Every constraint is named by the metadata**, never by hand and never left unnamed — an
  unnamed constraint cannot be dropped in `downgrade()`:

  ```python
  # app/models/base.py
  NAMING_CONVENTION = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s",
  }

  class Base(DeclarativeBase):
      metadata = MetaData(naming_convention=NAMING_CONVENTION)
  ```

  `unique=True` already creates an index — do not add `index=True` on the same column, or you
  get one unique *index* named `ix_…` and no `uq_…` constraint.

  `CheckConstraint` needs an explicit `name=` (the convention supplies only the prefix and
  table): `CheckConstraint("status IN ('active','disabled')", name="status")` → `ck_users_status`.

## Common columns

Every table has `id`, `created_at`, `updated_at`. Soft delete only where the product needs it,
as `deleted_at` (NULL = live). Timestamps come from the **database clock**
(`server_default=func.now()`), not from Python, so psql, migrations and other services agree.

```python
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

PK = BigInteger().with_variant(Integer, "sqlite")

class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(PK, Identity(), primary_key=True)
```

## Models and sessions

- `app/models/<entity>.py`, one aggregate per file. `app/models/__init__.py` re-exports every
  model so `Base.metadata` — and therefore Alembic autogenerate — sees every table.
- One `AsyncSession` per request from `get_db`; `async_sessionmaker(expire_on_commit=False)`.
- **The transaction boundary is the service method.** Routers never call `commit()`.
- Queries live in services. A repository layer only when a service must swap data sources.

## SQLite

For local development, tests and single-process tools — never a multi-writer production store.
It follows every rule above, plus:

- URL `sqlite+aiosqlite:///./data/app.db`; `data/` is gitignored.
- Pragmas on every connection:

  ```python
  @event.listens_for(engine.sync_engine, "connect")
  def _sqlite_pragmas(dbapi_conn, _record):
      cur = dbapi_conn.cursor()
      cur.execute("PRAGMA journal_mode=WAL")
      cur.execute("PRAGMA foreign_keys=ON")
      cur.execute("PRAGMA busy_timeout=5000")
      cur.close()
  ```
- Always UTC. SQLite stores timestamps as ISO-8601 text; `DateTime(timezone=True)` everywhere is
  what keeps them comparable with PostgreSQL rows.
- Alembic `render_as_batch=True` — SQLite cannot `ALTER` most things in place.

## Alembic

- Directory `alembic/` at the project root. `sqlalchemy.url` is **not** in `alembic.ini`;
  `env.py` sets it from `settings.database_url`.
- `env.py`: `target_metadata = Base.metadata`, `compare_type=True`,
  `compare_server_default=True`, `render_as_batch=True` when the dialect is SQLite.
- `alembic.ini`: `file_template = %%(year)d%%(month).2d%%(day).2d_%%(rev)s_%%(slug)s` so files
  sort chronologically.
- Message lowercase imperative: `-m "add user_profiles table"`.
- Read every autogenerated file before committing: a rename comes out as drop+create; server
  defaults and CHECK changes are missed.
- `downgrade()` is real, never `pass`. An irreversible step says so in the docstring.
- A revision that has run anywhere — the dev server counts — is never edited. Add a new one.
- Schema and data migrations are separate revisions; data migrations use `op.execute()` with
  SQL, never ORM models (models drift; a migration must not).

## Tenancy

*Only for a product where several customers share one instance.* Whether a product is
multi-tenant is its design doc's decision — but decide it at the start: retrofitting
`tenant_id` into every table later is the most expensive migration a product goes through, so
if there is any realistic path to a shared instance, apply this section now. A multi-tenant
product installed for a single customer keeps the same schema and simply has one tenant.

- **Every tenant-owned table has `tenant_id`** (`BIGINT`, NOT NULL, FK → `tenants.id`) via
  `TenantMixin`. Only global tables — settings, code lists, `tenants` itself — omit it.
- **Every index on a tenant-owned table leads with `tenant_id`**: `(tenant_id, status, created_at)`.
  A filter on tenant alone, or tenant + status, uses it; an index that does not start with
  `tenant_id` is a full scan for every tenant-scoped query — the most common RLS performance
  mistake.
- **Isolation is enforced twice.** The service filters by the current tenant, and PostgreSQL
  **row-level security** refuses other tenants' rows even when the service forgets:

  ```sql
  ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;
  ALTER TABLE tickets FORCE ROW LEVEL SECURITY;   -- 소유자 롤도 예외 없음 (없으면 우회됨)
  CREATE POLICY tenant_isolation ON tickets
      USING (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::bigint);
  ```

  The app sets the tenant **per transaction** — `SET LOCAL app.tenant_id = :tid` right after
  `BEGIN` (a SQLAlchemy `after_begin` listener reading the request context) — so it cannot leak
  across pooled connections; with no context set, a query returns zero rows rather than
  everything. The policy also blocks an INSERT for another tenant. Cost ≈ 0.3 ms per query.
  The app connects as a **non-superuser role** (superusers bypass every policy), and each
  policy is created in the same Alembic revision as its table.
- `get_tenant` (`fastapi-standards` §4) is the only place a tenant id is read. Models never
  accept `tenant_id` from a client payload; the mixin fills it from the request context.
- SQLite has no RLS: unit tests exercise the service filter only; integration tests run on
  PostgreSQL so the policy is exercised too.

## Audit log

*For a product that handles patient or other regulated personal data.* It records who did what to whose data. One append-only table; the app role
has INSERT and SELECT only, no UPDATE or DELETE:

```
audit_log(id, tenant_id, at timestamptz, actor_id, action, entity, entity_id, request_id, detail jsonb)
```

Written by the service layer on every create / update / delete of a domain entity and on every
read of a patient record. `detail` holds the names of changed fields, never their values — the
audit log must not become a second copy of the PHI it guards.

## Redis

### Key vocabulary

`<prefix>:<domain>:<id>[:<attribute>]`, lowercase, colon-separated. **The first segment comes
from this table.** A new prefix is added here before it is used anywhere.

| Prefix | Holds | TTL |
|---|---|---|
| `cache:` | derived data that can be recomputed — `cache:user:123:profile` | `TTL_DEFAULT` |
| `session:` | login/session state — `session:abc123` | `TTL_SESSION`, refreshed on access |
| `lock:` | mutual exclusion — `lock:order:789` | ≤ 30 s, value = owner token |
| `queue:` | work items — `queue:emails:pending` | none (drained) |
| `rate:` | rate-limit windows — `rate:api:user:123:1m` | the window length |
| `counter:` | counters, analytics — `counter:api:requests:2026-09-10` | `TTL_DAY` or longer |
| `idem:` | idempotency keys — `idem:payment:<request_id>` | `TTL_DAY` |

Pub/sub channels are `events:<domain>:<event>` (`events:order:created`). When several services
share one instance, the service name goes first: `billing:cache:user:123:profile`. Logical DB is
always `0`; separation is by prefix or instance, never `SELECT n`.

### Keys are built in one module

```python
# app/core/keys.py — the only place a Redis key string is assembled
def user_profile(user_id: int) -> str:
    return f"cache:user:{user_id}:profile"

def order_lock(order_id: int) -> str:
    return f"lock:order:{order_id}"
```

No key f-strings in services. One test imports every public function in `keys.py`, calls it
with sample arguments, and asserts the result matches `^[a-z]+(:[a-z0-9_.-]+)+$` and starts
with a prefix from the table. That test is what stops `userProfile:123` and `user_profile_123`
from reappearing in the next project.

### TTL tiers

```python
# app/core/cache.py
TTL_SHORT = 300        # 5 min — volatile lookups
TTL_DEFAULT = 3600     # 1 h   — cache:
TTL_SESSION = 1800     # 30 min sliding — session:
TTL_DAY = 86400
```

Every key that is not a permanent record is written with a TTL (`SET … EX`, `SETEX`). A key
without a TTL is a memory leak on a delay. Numbers never appear inline — use the constants.

### Values

- JSON only, with `decode_responses=True`; objects go through `model_dump_json()` /
  `model_validate_json()`. **Never pickle** — it is remote code execution and it couples the
  cache to a class version.
- One hash per entity (`HSET cache:user:123 name … email …`) rather than N string keys.
- Locks: `SET lock:… <owner-token> NX EX 30`; release only if the token still matches
  (compare-and-delete in Lua).
