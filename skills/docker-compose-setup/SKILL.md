---
name: docker-compose-setup
description: Integrate multiple independent projects into a single Docker Compose environment with subdomain-based routing (*.domain.com), Nginx reverse proxy, and automatic Let's Encrypt SSL management. Use when setting up multi-project Docker infrastructure, configuring subdomain routing, or automating SSL certificates.
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Docker Compose Multi-Project Integration

**IMPORTANT:** Always respond in Korean to the user.

## When to use
- **Multi-Project Setup:** When integrating multiple independent projects into a unified Docker environment.
- **Subdomain Routing:** When configuring `*.domain.com` routing with Nginx reverse proxy.
- **SSL Configuration:** When setting up automatic Let's Encrypt SSL certificates.
- **Infrastructure Troubleshooting:** When debugging Docker network, Nginx, or certificate issues.

## Instructions

Integrate multiple independent projects into a unified Docker Compose setup with subdomain routing and automatic SSL.

### Prerequisites check

Before starting, verify:

```bash
# Check Docker Compose version (requires v2.20+)
docker compose version

# Confirm you have:
# - Domain name
# - Subdomain for each project
# - Each project's internal port
# - List of project directories to integrate
```

### Integration Steps

Copy this checklist and check off items as you complete them:

```
Integration Progress:
- [ ] Step 1: Create main docker-compose.yml
- [ ] Step 2: Create infrastructure directories
- [ ] Step 3: Integrate first project
- [ ] Step 4: Verify DNS and issue SSL
- [ ] Step 5: Enable HTTPS
- [ ] Step 6: Add additional projects (repeat 3-5)
```

#### Step 1: Create main docker-compose.yml

Create at workspace root:

```yaml
include:
  # Add project compose files here as you integrate them
  # - project1/docker-compose.project.yml

services:
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    depends_on: []  # Add project services here
    networks:
      - shared-network

  certbot:
    image: certbot/certbot
    container_name: certbot
    restart: unless-stopped
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: /bin/sh -c 'trap exit TERM; while :; do certbot renew --deploy-hook "echo Certificate renewed at $$(date)"; sleep 12h & wait $${!}; done;'

  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --cleanup --schedule "0 20 * * *"
    networks:
      - shared-network

networks:
  shared-network:
    driver: bridge
```

**Critical rule**: Network is defined ONLY in main file.

#### Step 2: Create infrastructure directories

```bash
mkdir -p nginx/conf.d
mkdir -p certbot/{conf,www}
```

Create `init-letsencrypt.sh`. See [scripts/init-letsencrypt.sh](scripts/init-letsencrypt.sh) for complete script.

Make executable:
```bash
chmod +x init-letsencrypt.sh
```

#### Step 3: Integrate first project

For each project, complete these sub-steps:

**3.1: Create docker-compose.project.yml in project directory**

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: unique-app-name
    restart: unless-stopped
    volumes:
      - app-data:/app/data
    env_file:
      - .env
    networks:
      - shared-network

volumes:
  app-data:
    name: unique-app-data

networks:
  shared-network:
    external: true  # MUST be external: true
```

**Critical rules**:
- Container name must be unique across all projects
- Volume name must be unique across all projects
- Network must have `external: true`

**3.2: Update main docker-compose.yml**

```yaml
include:
  - project-name/docker-compose.project.yml  # Add this line

services:
  nginx:
    depends_on:
      - app  # Add service name
```

**3.3: Create Nginx HTTP config (no SSL yet)**

Create `nginx/conf.d/subdomain.domain.com.conf`:

```nginx
server {
    listen 80;
    server_name subdomain.domain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://app-container-name:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Replace:
- `subdomain.domain.com` with actual subdomain
- `app-container-name:8000` with container name and port

**3.4: Prepare HTTPS config for later**

Create `nginx/conf.d/subdomain.domain.com.conf.disabled` with HTTPS config. See [templates/nginx-https.conf](templates/nginx-https.conf).

**3.5: Start containers**

```bash
docker compose up -d
```

Verify:
```bash
docker compose ps  # All should be "Up"
docker compose logs nginx  # Check for errors
```

#### Step 4: Verify DNS and issue SSL

**4.1: Verify DNS propagation**

**CRITICAL**: Check with public DNS servers, not local DNS.

```bash
# Check with Google DNS (used by Let's Encrypt)
nslookup subdomain.domain.com 8.8.8.8

# Check with Cloudflare DNS
nslookup subdomain.domain.com 1.1.1.1
```

If you see `NXDOMAIN`, DNS is not propagated yet. **STOP and wait** for propagation (up to 48 hours).

**4.2: Test HTTP access**

```bash
curl -I http://subdomain.domain.com
```

Must return 200 or valid response.

**4.3: Issue SSL certificate**

Only after DNS is fully propagated:

```bash
sudo ./init-letsencrypt.sh subdomain.domain.com
```

For testing (no rate limits):
```bash
sudo ./init-letsencrypt.sh subdomain.domain.com --staging
```

Verify success message:
```
✅ Certificate successfully obtained for subdomain.domain.com
```

#### Step 5: Enable HTTPS

**5.1: Activate HTTPS config**

```bash
cp nginx/conf.d/subdomain.domain.com.conf.disabled \
   nginx/conf.d/subdomain.domain.com.conf

docker compose exec nginx nginx -s reload
```

**5.2: Verify HTTPS**

```bash
# Test HTTPS
curl -I https://subdomain.domain.com

# Test HTTP → HTTPS redirect
curl -I http://subdomain.domain.com
```

Should see:
- HTTPS: `HTTP/2 200` or valid response
- HTTP: `301 Moved Permanently` with `Location: https://...`

#### Step 6: Add additional projects

For each new project, repeat Steps 3-5.

### Common issues

#### Network conflict error

```
Error: networks.shared-network conflicts with imported resource
```

**Fix**: Remove network definition from project file. Use only `external: true`.

#### Nginx fails to start

```
nginx: [emerg] open() "/etc/letsencrypt/..." failed
```

**Cause**: HTTPS config active but no SSL certificate.

**Fix**: Use HTTP-only config first, issue SSL, then enable HTTPS.

#### SSL issuance fails

```
DNS problem: NXDOMAIN looking up A for domain.com
```

**Cause**: DNS not propagated to public DNS servers.

**Fix**: Verify with `nslookup domain.com 8.8.8.8`. Wait for propagation.

#### Container communication fails

```
502 Bad Gateway
```

**Check**:
```bash
# Verify container is running
docker compose ps

# Test DNS resolution
docker compose exec nginx ping app-container-name

# Check network
docker network inspect shared-network
```

### Templates and scripts

- [templates/docker-compose.project.yml](templates/docker-compose.project.yml) - Project compose template
- [templates/nginx-http.conf](templates/nginx-http.conf) - HTTP-only Nginx config
- [templates/nginx-https.conf](templates/nginx-https.conf) - HTTPS Nginx config
- [scripts/init-letsencrypt.sh](scripts/init-letsencrypt.sh) - SSL certificate script

### Key principles

**DO**:
- Define network only in main docker-compose.yml
- Use `external: true` in all project files
- Start with HTTP, then add HTTPS after SSL
- Verify DNS with public DNS servers (8.8.8.8)
- Use unique container and volume names

**DON'T**:
- Define network with `driver: bridge` in project files
- Enable HTTPS config before SSL certificate exists
- Trust local DNS for verification
- Use duplicate container/volume names
- Modify nginx command (use defaults)

## Examples

### Example docker-compose.yml

```yaml
services:
  web:
    image: nginx
    networks:
      - shared-network
networks:
  shared-network:
    external: true
```
