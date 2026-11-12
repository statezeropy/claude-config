---
paths:
  - "**/{compose,docker-compose}*.{yml,yaml}"
  - "**/Dockerfile*"
  - "**/nginx/**"
  - "**/nginx*.conf"
---

# Deployment

Where a product runs — hosted by us, installed at a customer site, or both — and how many
customers share an instance are decisions of that product's design doc. What is fixed here
stays true whatever that answer is. Templates, delivery steps and troubleshooting are in the
`deployment-conventions` skill.

## What the app promises the environment

Whatever terminates TLS in front of it, the app behaves the same:

- Listens plain HTTP on `PORT` (default 8000). No certificates in the image.
- Trusts `X-Forwarded-*` only from the proxy; without that, redirects come out `http://` and
  every client IP is the proxy's.
- Answers `/health` and `/ready` (`fastapi` rule).
- Handles SIGTERM gracefully: finish in-flight requests, then exit.
- Keeps no state in the process or on local disk: sessions in Redis, files in object storage.
- Logs JSON to stdout; collection is the environment's job.
- Reads every setting from env. A feature that needs the internet sits behind a capability
  flag, so a site without internet degrades instead of crashing.

## Compose

- Every service has a `healthcheck` and every dependency a condition
  (`service_healthy`, or `service_completed_successfully` for jobs). Order alone is a race.
- Migrations are a one-shot `migrate` service that runs `alembic upgrade head` and exits 0;
  `app` waits on it. Nothing runs migrations at import time.
- `restart: unless-stopped` on long-running services, `"no"` on `migrate`.
- Secrets come through `env_file: .env`. The environment variable is `ENV=prod|dev|test`.
- Optional stacks sit behind `profiles` (`llm`, `monitoring`, `debug`).
- Development uses `compose.override.yml`; a production directory never contains one.
- No auto-updater. The GitHub Release is the deploy; an unreviewed image change is an incident.
- No `version:` key. Named volumes carry an explicit `name:`.
- Several projects on one host: the root compose file holds the only definition of the shared
  network and project files declare it `external: true`; container and volume names are
  globally unique (`<project>-app`, `<project>-db-data`).

## Image version

- The image is tagged with the release version and with the commit, and labelled
  `org.opencontainers.image.version`. `TAG=<version>` in `.env` selects it; there is no
  `latest` to deploy from.
- The Dockerfile takes `ARG VERSION` with no default and exports it as
  `SETUPTOOLS_SCM_PRETEND_VERSION`: a build that does not know its version fails.

## TLS and delivery when we do not own the network

- Certificates are provided by the site. nginx reads `certs/fullchain.pem` and
  `certs/privkey.pem`; rotation is a file copy and a reload. The bundle never runs ACME.
- A site without internet gets images as files with `SHA256SUMS`; digests are compared, not
  tags.
- A release for a site is one versioned directory: `compose.yml`, `.env.example`,
  `nginx/nginx.conf`, an empty `certs/`, `images/` when offline, and the install, upgrade and
  backup-restore how-tos. A verified restore is part of install QA.

## The bar for SaaS products

A SaaS product is built so that it can pass the
[AWS Foundational Technical Review](https://aws.amazon.com/partners/foundational-technical-review/)
self-assessment. The checklist is external and maintained — link it; the product's design doc
records how each property is met.
