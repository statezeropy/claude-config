# Claude Config

Claude Code / Codex CLI global settings and skills.

## Setup

### Claude Code

```bash
cd ~/.claude
git clone https://github.com/statezeropy/claude-config.git
ln -sf claude-config/CLAUDE.md CLAUDE.md
ln -sf claude-config/skills skills

# 공유 설정(outputStyle 등)을 전역 settings.json 에 병합 — 기존 키는 보존된다 (jq 필요)
# 링크가 아니라 병합인 이유: settings.json 은 Claude Code 가 직접 쓰는 파일이다(권한 응답, 머신별 경로).
[ -f settings.json ] || echo '{}' > settings.json
jq -s '.[0] * .[1]' settings.json claude-config/settings.json > settings.json.tmp && mv settings.json.tmp settings.json
```

공유할 설정이 늘면 `claude-config/settings.json` 만 고치고 위 병합 명령을 다시 실행한다.

### Codex CLI

```bash
cd ~/.codex
git clone https://github.com/statezeropy/claude-config.git
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

### Humanize Korean
AI(ChatGPT·Claude·Gemini 등)가 쓴 한글 텍스트를 사람이 쓴 글처럼 윤문. 번역투·피동태·기계적 병렬 등 AI 티 패턴을 탐지해 내용은 유지한 채 문체만 자연스럽게 교정.

```
/plugin marketplace add epoko77-ai/im-not-ai
/plugin install humanize-korean@im-not-ai
```

### Korean Skills (humanizer)
한국어 글쓰기 도구 모음 — humanizer(AI 티 제거), grammar-checker(맞춤법·문법 검사), style-guide(문체 일관성). daleseo/korean-skills 마켓플레이스에서 설치.

```
npx skills add daleseo/korean-skills
claude /plugin marketplace add daleseo/korean-skills
claude /plugin install korean-skills@korean-skills
```

### drawio
다이어그램·플로우차트·아키텍처도·ER·UML(시퀀스/클래스)·네트워크 토폴로지·ML 모델 도식 등을 `.drawio` XML로 생성하고 draw.io desktop CLI로 PNG/SVG/PDF/JPG 내보내기. 커스텀 스타일링·스윔레인 등 리치한 표현에 적합.

```
/plugin marketplace add Agents365-ai/365-skills
/plugin install drawio@365-skills
```

## Skill 작성 원칙

이 저장소의 skill 은 **결정**(규약·구조·워크플로)을 담고, 라이브러리 **지식**은 담지 않는다.

- 지식은 버전과 함께 썩는다. 2026-09 정리 때 지식형 skill 10개(41k줄)에서 Pydantic v1·SQLAlchemy 1.x·
  deprecated LangChain API 가 발견됐고, 같은 기간 결정형 skill 은 한 줄도 무효가 되지 않았다.
- skill 이 고정해도 되는 것은 **모양** — 이름·URL·디렉토리·커밋 형식·계약 위치. **메커니즘** — 어떤
  라이브러리·언제 캐시·동기/비동기 — 은 프로젝트의 `docs/design/` 에서 측정과 함께 결정한다.
- 린터·포매터·훅으로 옮길 수 있는 규칙은 산문으로 두지 않는다 (`python-standards/templates/`).
- 빠르게 움직이는 라이브러리는 사실을 적지 말고 **확인하는 방법**을 적는다 (핀한 버전의 소스 읽기).
- 소유한 skill 에는 `metadata.reviewed` 날짜를 둔다. 오래된 것부터 다시 읽는다.
