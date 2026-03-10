# Claude Config

Claude Code / Gemini CLI / Codex CLI global settings and skills.

## Setup

### Claude Code

**macOS / Linux**

```bash
cd ~/.claude
git clone https://github.com/statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CLAUDE.md
ln -sf claude-config/skills skills
```

**Windows (CMD)**

```cmd
cd %USERPROFILE%\.claude
git clone https://github.com/statezeropy/claude-config.git
mklink CLAUDE.md claude-config\CLAUDE.md
mklink /D skills claude-config\skills
```

### Gemini CLI

**macOS / Linux**

```bash
cd ~/.gemini
git clone https://github.com/statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md GEMINI.md
ln -sf claude-config/skills skills
```

**Windows (CMD)**

```cmd
cd %USERPROFILE%\.gemini
git clone https://github.com/statezeropy/claude-config.git
mklink GEMINI.md claude-config\CLAUDE.md
mklink /D skills claude-config\skills
```

### Codex CLI

**macOS / Linux**

```bash
cd ~/.codex
git clone https://github.com/statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CODEX.md
ln -sf claude-config/skills skills
```

**Windows (CMD)**

```cmd
cd %USERPROFILE%\.codex
git clone https://github.com/statezeropy/claude-config.git
mklink CODEX.md claude-config\CLAUDE.md
mklink /D skills claude-config\skills
```

> **Note**: Windows에서 `mklink`은 관리자 권한 또는 [개발자 모드](https://learn.microsoft.com/ko-kr/windows/apps/get-started/enable-your-device-for-development) 활성화가 필요합니다.

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
