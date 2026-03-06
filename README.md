# Claude Config

Claude Code global settings and skills.

## Setup

```bash
cd ~/.claude
git clone git@github.com:statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CLAUDE.md
ln -sf claude-config/skills skills
```

## Plugins

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
