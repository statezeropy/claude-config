# Docker Compose Multi-Project Integration Skill

An Agent Skill for integrating multiple independent projects into a unified Docker Compose environment with subdomain routing and automatic SSL management.

## What this Skill does

This Skill guides Claude through:
- Setting up Docker Compose with the `include` feature
- Configuring Nginx reverse proxy for subdomain-based routing
- Automating Let's Encrypt SSL certificate issuance and renewal
- Integrating existing standalone projects into the unified environment
- Troubleshooting common integration issues

## Structure

```
docker-compose-multi-project/
├── SKILL.md                           # Main instructions
├── scripts/
│   └── init-letsencrypt.sh           # SSL certificate automation
└── templates/
    ├── docker-compose.project.yml    # Project compose template
    ├── nginx-http.conf               # HTTP-only config
    └── nginx-https.conf              # HTTPS config
```

## Usage

Claude automatically uses this Skill when you mention:
- Integrating multiple Docker projects
- Setting up subdomain routing
- Configuring Nginx for multiple services
- Automating SSL certificates

## Key concepts

### Progressive disclosure
- **Level 1 (Metadata)**: Always loaded - Skill name and description
- **Level 2 (Instructions)**: Loaded when triggered - SKILL.md workflow
- **Level 3 (Resources)**: Loaded as needed - Templates and scripts

### Critical principles
1. **Network definition**: Only in main docker-compose.yml
2. **Project files**: Must use `external: true` for shared network
3. **SSL workflow**: HTTP first → Issue SSL → Enable HTTPS
4. **DNS verification**: Check with public DNS (8.8.8.8), not local

## Installation

### Claude Code
Place this directory in `~/.claude/skills/`:
```bash
cp -r docker-compose-multi-project ~/.claude/skills/
```

### Claude API
Upload as a custom Skill via the Skills API.

### Claude.ai
Zip this directory and upload via Settings > Features.

## Testing

Test the Skill with requests like:
- "Help me integrate my Docker projects into a single environment"
- "Set up Nginx routing for app1.domain.com and app2.domain.com"
- "Configure automatic SSL for my multi-project Docker setup"

## Based on real experience

This Skill captures lessons from integrating the `aichat` and `TTA` projects:
- Network conflicts when both main and project files define networks
- Nginx startup failures when SSL config loads before certificates exist
- DNS propagation delays causing SSL issuance failures
- Container communication issues from network misconfiguration

## License

This Skill is provided as-is for integration guidance based on Docker Compose best practices.

