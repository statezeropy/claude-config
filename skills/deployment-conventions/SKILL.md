---
name: deployment-conventions
description: How a product ships in its two deployment modes — SaaS application plane (TENANCY_MODE=saas, behind the platform's edge) and single-tenant on-premise install inside a hospital network (TENANCY_MODE=single, air-gapped, customer-issued certificates). The mode contract, what the app promises whatever terminates TLS, the versioned compose bundle, the migrate job, offline image delivery, nginx TLS termination with provided certs, healthcheck and depends_on rules, profiles, and the multi-project substrate for one VM. Use when writing compose files, packaging a release for a customer site, adding a service to the stack, or deciding what an app may assume about its environment.
metadata:
  reviewed: 2026-09-11
---

# Deployment conventions

One image, one codebase, two deployment modes. The mode is an environment variable; the code
never branches on "am I SaaS or on-prem" — only settings and adapters do (`fastapi-standards`
§4, `llm-app-conventions`). Everything below exists to keep that true.

## Scope — product by default, `internal` opts out

Every project is a **product** — something that ships to customers as SaaS, as an on-site
install, or both — unless its design doc (or README, when there is no design doc) declares
`Product class: internal`. A demo UI, an experiment, a script for our own use is `internal`.

| | product (default) | `internal` |
|---|---|---|
| this skill | all sections | only *Compose rules* and *Several products on one VM* |
| `data-conventions` Tenancy + Audit log | required | skipped |
| `fastapi-standards` §4 tenancy / environment rows | required | skipped |
| design-doc Reliability section | required | optional |
| The bar (below) | required | — |

Declare it once, at the start. If an `internal` project turns into a product, update the design
doc and apply the product sections then — do not pre-apply them "just in case".

## The two modes

| | `TENANCY_MODE=saas` | `TENANCY_MODE=single` |
|---|---|---|
| Runs | on the platform, one instance for many tenants | inside the customer's (hospital's) network, one tenant |
| Tenant | resolved per request from the JWT `tid` claim | fixed: `TENANT_ID` from env |
| Edge / TLS | the platform's (ALB, ingress) — not ours | the bundle's nginx with **customer-issued certificates** |
| Internet | yes | **assume none** (망분리): no ACME, no registry pulls, no cloud APIs |
| LLM | cloud API | OpenAI-compatible endpoint on site (`LLM_BASE_URL`) |
| Tracing | Langfuse | self-hosted Langfuse, or off (`LANGFUSE_HOST` unset) |
| Delivery | CI deploys the tagged image | versioned bundle carried in |

The app cannot tell the modes apart except through `Settings`. A feature that needs the
internet sits behind a capability flag that `single` turns off — it degrades, it never crashes.

## What the app promises the environment

Whoever terminates TLS — hospital nginx or platform load balancer — the app behaves the same:

- Listens plain HTTP on `PORT` (default 8000). No certificates in the image.
- Trusts `X-Forwarded-For/Proto/Host` **only from the proxy**:
  `uvicorn --proxy-headers --forwarded-allow-ips=<proxy>`. Without this, redirects come out
  `http://` and every client IP is the proxy's.
- Answers `/health` and `/ready` (`fastapi-standards` §1).
- Handles SIGTERM with a graceful shutdown — finish in-flight requests, then exit. Rolling
  upgrades depend on it.
- Keeps no state in the process or on local disk: sessions in Redis, files in object storage.
- Logs JSON to stdout; collection is the environment's job.
- Reads every setting from env (`fastapi-standards` §4).

## The bundle (single mode)

A release for a customer site is one directory, versioned by the git tag (`git-workflow` §3):

```
<product>-v1.4.2/
├── compose.yml          templates/compose.yml — nginx, app, migrate, db, redis (+ profiles)
├── .env.example         every variable the app reads, with safe defaults
├── nginx/nginx.conf     templates/nginx.conf — TLS termination with the provided certs
├── certs/               EMPTY: the customer drops fullchain.pem + privkey.pem here
├── images/              air-gapped sites only: <product>-<tag>.tar.gz + SHA256SUMS
└── docs/how-to/         install, upgrade, backup-restore (docs-structure)
```

- **Migrations are a one-shot service.** `migrate` runs `alembic upgrade head` and exits 0;
  `app` waits with `depends_on: migrate: condition: service_completed_successfully`. Upgrade =
  load the new images, `docker compose up -d`. Nothing runs migrations at import time.
- **Offline delivery**: `docker save <images> | gzip > images/<product>-<tag>.tar.gz`, ship with
  `SHA256SUMS`; on site `sha256sum -c SHA256SUMS && docker load -i …`. Compare digests, not tags.
- **Certificates come from the customer** (internal CA). The bundle never runs ACME. nginx reads
  `certs/fullchain.pem` and `certs/privkey.pem`; rotation is a file copy and `nginx -s reload`.
- **No auto-updaters** (watchtower): an unreviewed image change inside a hospital is an
  incident, and it contradicts "the tag is the deploy".
- Backups are the PostgreSQL volume plus object storage; `docs/how-to/backup-restore.md`
  documents `pg_dump` and restore, and a **verified restore is part of install QA**.

## Compose rules (both modes)

- **Every service has a `healthcheck`, every dependency a condition**:
  `depends_on: <svc>: condition: service_healthy` (`service_completed_successfully` for jobs).
  Order alone (`depends_on: [db]`) is a race.
  - app → `GET /health` · db → `pg_isready` · redis → `redis-cli ping` · nginx → `GET :80/health`
- `restart: unless-stopped` on long-running services; `"no"` on `migrate`.
- Secrets through `env_file: .env` (gitignored; `.env.example` committed). Variable names are
  the ones in `fastapi-standards` §4 — `ENV=prod|dev|test`, never `ENVIRONMENT`.
- Optional stacks behind `profiles`: `llm` (on-site OpenAI-compatible server), `monitoring`,
  `debug`. `docker compose --profile llm up -d`.
- Development uses `compose.override.yml` (auto-merged) with `develop.watch` on the app source.
  Production directories never contain an override file.
- No `version:` key (Compose Specification). Named volumes carry an explicit `name:`.

## Several products on one VM (the developer / SaaS-side substrate)

- The root `compose.yml` holds `include:` entries and the **only** definition of
  `shared-network`; project files declare it `external: true`. Defining it twice is the
  "conflicts with imported resource" error.
- Container and volume names are globally unique: `<project>-app`, `<project>-db-data`.
- One nginx `server` block per subdomain, all in the root nginx. Certificates there *may* come
  from ACME — the VM has internet — but that is that environment's decision, recorded in its
  `docs/design/`, not a product convention.
- Verify DNS with a public resolver before expecting anything: `nslookup <host> 8.8.8.8`.

## The bar — what "production-ready" means for a product

A product is ready when it could pass the **AWS Foundational Technical Review** self-assessment:
the *Partner Hosted* checklist for `saas`, the *Customer Deployed* checklist for `single`. We
do not copy the checklist — it is external, maintained, and revised — we link it:
[FTR guide](https://aws.amazon.com/partners/foundational-technical-review/) and the checklists
in AWS Partner Central. The FTR asks for **properties**, not methods, which is why it fits:

| FTR asks for | already enforced by | the project decides (in `docs/design/`) |
|---|---|---|
| TLS ≥ 1.2 in transit | `templates/nginx.conf` | — |
| tenant isolation | `data-conventions` §Tenancy (RLS, both modes) | any model beyond pool |
| backups, restore, **RTO / RPO** | "verified restore is part of install QA" | the numbers, cadence, location |
| high availability | — | topology |
| incident runbooks | `docs/how-to/` bucket | contents |
| audit logging | `data-conventions` §Audit log | retention |
| infrastructure as code, CI/CD | `templates/compose.yml`, `python-standards/templates/ci.yml` | deploy targets |
| monitoring and alerting | `/health`, `/ready`, JSON logs | thresholds, dashboards |
| secrets handling | `.env` + `.env.example`, no secrets in logs | the secret store |
| account hygiene (root MFA, IAM, CloudTrail, CIS) | — outside any repository | — |

The rule that keeps this table honest: **if two of our products could reasonably differ on it,
it belongs to the project; if they must not differ, it belongs here.**

## Troubleshooting — the four that recur

| Symptom | Cause | Fix |
|---|---|---|
| `networks.shared-network conflicts with imported resource` | network defined in a project file | keep only `external: true` there |
| nginx `cannot load certificate "/etc/nginx/certs/fullchain.pem"` | `certs/` empty | drop the customer's pem files in, `docker compose restart nginx` |
| `502 Bad Gateway` | app not healthy, or wrong upstream name | `docker compose ps` (health column); `docker compose exec nginx getent hosts app` |
| app starts before the schema exists | `depends_on` without a condition | the `migrate` job + `service_completed_successfully` |
