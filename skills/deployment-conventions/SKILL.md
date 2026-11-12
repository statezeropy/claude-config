---
name: deployment-conventions
description: Start a service's compose stack and nginx from the house templates, package a release for a customer site (versioned directory, offline images with checksums), and fix the deployment failures that recur — shared-network conflict, missing certificates, 502, app starting before the schema. Use when creating compose or nginx files for a project, preparing an on-site or offline delivery, or debugging one of those failures. The deployment rules themselves load from the deployment rule whenever a compose file, Dockerfile or nginx config is touched.
metadata:
  reviewed: 2026-11-12
---

# Deployment — templates, delivery, troubleshooting

The rules are in the `deployment` rule (`~/.claude/rules/deployment.md`).

## Starting a stack

Copy `<skill>/templates/compose.yml` and `<skill>/templates/nginx.conf`, then name the
services, volumes and network for the project. The healthcheck commands the template uses:

- app → `GET /health` · db → `pg_isready` · redis → `redis-cli ping` · nginx → `GET :80/health`

## Packaging a release for a site

1. Build the image from the release tag; record its digest.
2. Offline site: `docker save <images> | gzip > images/<name>-<version>.tar.gz` and write
   `SHA256SUMS`. On site: `sha256sum -c SHA256SUMS && docker load`.
3. Assemble one versioned directory: `compose.yml`, `.env.example`, `nginx/nginx.conf`, an
   empty `certs/`, `images/` when offline, and the install, upgrade and backup-restore how-tos.
4. Install QA includes a verified restore.

Verify DNS with a public resolver before expecting anything: `nslookup <host> 8.8.8.8`.

## Troubleshooting — the four that recur

| Symptom | Cause | Fix |
|---|---|---|
| `networks.shared-network conflicts with imported resource` | network defined in a project file | keep only `external: true` there |
| nginx `cannot load certificate "/etc/nginx/certs/fullchain.pem"` | `certs/` empty | drop the site's pem files in, `docker compose restart nginx` |
| `502 Bad Gateway` | app not healthy, or wrong upstream name | `docker compose ps` (health column); `docker compose exec nginx getent hosts app` |
| app starts before the schema exists | `depends_on` without a condition | the `migrate` job + `service_completed_successfully` |
