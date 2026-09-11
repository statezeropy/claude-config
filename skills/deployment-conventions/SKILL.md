---
name: deployment-conventions
description: How a service is packaged and run — what an app promises whatever sits in front of it (plain HTTP on PORT, proxy headers, /health and /ready, graceful shutdown, no local state, JSON logs), compose rules (healthcheck and depends_on conditions, the one-shot migrate job, profiles, no auto-updaters), nginx TLS termination with provided certificates, offline image delivery for sites without internet, hosting several projects on one VM, and the quality bar for SaaS products (AWS Marketplace / FTR). Use when writing compose files, packaging a release, adding a service to the stack, or deciding what an app may assume about its environment.
metadata:
  reviewed: 2026-09-11
---

# Deployment conventions

Where a product runs — hosted by us, installed at a customer site, or both — and how many
customers share an instance are decisions of that product's design doc, not of this skill.
What is fixed here is what stays true regardless of that answer.

## What the app promises the environment

Whatever terminates TLS in front of it — our nginx, a customer's proxy, a cloud load balancer —
the app behaves the same:

- Listens plain HTTP on `PORT` (default 8000). No certificates in the image.
- Trusts `X-Forwarded-For/Proto/Host` **only from the proxy**:
  `uvicorn --proxy-headers --forwarded-allow-ips=<proxy>`. Without this, redirects come out
  `http://` and every client IP is the proxy's.
- Answers `/health` and `/ready` (`fastapi-standards` §1).
- Handles SIGTERM with a graceful shutdown — finish in-flight requests, then exit. Rolling
  upgrades depend on it.
- Keeps no state in the process or on local disk: sessions in Redis, files in object storage.
- Logs JSON to stdout; collection is the environment's job.
- Reads every setting from env (`fastapi-standards` §4). A feature that needs the internet sits
  behind a capability flag, so a site without internet degrades instead of crashing.

## Compose rules

Start from `templates/compose.yml`.

- **Every service has a `healthcheck`, every dependency a condition**:
  `depends_on: <svc>: condition: service_healthy` (`service_completed_successfully` for jobs).
  Order alone (`depends_on: [db]`) is a race.
  - app → `GET /health` · db → `pg_isready` · redis → `redis-cli ping` · nginx → `GET :80/health`
- **Migrations are a one-shot service.** `migrate` runs `alembic upgrade head` and exits 0;
  `app` waits on `service_completed_successfully`. Nothing runs migrations at import time.
- `restart: unless-stopped` on long-running services; `"no"` on `migrate`.
- Secrets through `env_file: .env` (gitignored; `.env.example` committed). Variable names are
  the ones in `fastapi-standards` §4 — `ENV=prod|dev|test`, never `ENVIRONMENT`.
- Optional stacks behind `profiles` (`llm`, `monitoring`, `debug`): `docker compose --profile llm up -d`.
- Development uses `compose.override.yml` (auto-merged) with `develop.watch`; production
  directories never contain an override file.
- **No auto-updaters** (watchtower). The git tag is the deploy (`git-workflow` §3); an
  unreviewed image change is an incident.
- No `version:` key (Compose Specification). Named volumes carry an explicit `name:`.

## TLS and delivery when we do not own the network

- **Certificates are provided by the site** (its internal CA or its own ACME). nginx
  (`templates/nginx.conf`) reads `certs/fullchain.pem` and `certs/privkey.pem`; rotation is a
  file copy and `nginx -s reload`. The bundle never runs ACME itself.
- **Sites without internet** get images as files: `docker save <images> | gzip`, shipped with
  `SHA256SUMS`; on site `sha256sum -c && docker load`. Compare digests, not tags.
- A release for a site is one versioned directory — `compose.yml`, `.env.example`,
  `nginx/nginx.conf`, an empty `certs/`, `images/` when offline, and `docs/how-to/` for install,
  upgrade and backup-restore. A **verified restore is part of install QA**.

## Several projects on one VM

- The root `compose.yml` holds `include:` entries and the **only** definition of
  `shared-network`; project files declare it `external: true`. Defining it twice is the
  "conflicts with imported resource" error.
- Container and volume names are globally unique: `<project>-app`, `<project>-db-data`.
- One nginx `server` block per subdomain, all in the root nginx.
- Verify DNS with a public resolver before expecting anything: `nslookup <host> 8.8.8.8`.

## The bar for SaaS products

**A SaaS product is built to the AWS Marketplace standard: it must be able to pass the
[AWS Foundational Technical Review](https://aws.amazon.com/partners/foundational-technical-review/)
self-assessment.** The checklist is external and maintained — link it, do not copy it. It asks
for properties (encryption in transit, tenant isolation, backups with RTO/RPO, runbooks,
infrastructure as code, monitoring), and the project's design doc records how each is met.

## Troubleshooting — the four that recur

| Symptom | Cause | Fix |
|---|---|---|
| `networks.shared-network conflicts with imported resource` | network defined in a project file | keep only `external: true` there |
| nginx `cannot load certificate "/etc/nginx/certs/fullchain.pem"` | `certs/` empty | drop the site's pem files in, `docker compose restart nginx` |
| `502 Bad Gateway` | app not healthy, or wrong upstream name | `docker compose ps` (health column); `docker compose exec nginx getent hosts app` |
| app starts before the schema exists | `depends_on` without a condition | the `migrate` job + `service_completed_successfully` |
