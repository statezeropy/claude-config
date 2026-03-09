# Claude Config

Claude Code / Gemini CLI / Codex CLI global settings and skills.

## Setup

### Claude Code

```bash
cd ~/.claude
git clone git@github.com:statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CLAUDE.md
ln -sf claude-config/skills skills
```

### Gemini CLI

```bash
cd ~/.gemini
git clone git@github.com:statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md GEMINI.md
ln -sf claude-config/skills skills
```

### Codex CLI

```bash
cd ~/.codex
git clone git@github.com:statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CODEX.md
ln -sf claude-config/skills skills
```

## Plugins (Claude only)

### Document Skills
문서 작업 도구 모음. PDF, DOCX, PPTX, XLSX 생성/편집, 프론트엔드 디자인, 알고리즘 아트 등을 지원.

```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

### Claude HUD
Claude Code 터미널에 상태바(statusline)를 표시. 현재 모델, 토큰 사용량, 컨텍스트 등을 실시간 확인.

```
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```
