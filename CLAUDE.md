# Max's Global Development Standards

## 언어

- 사용자에게는 항상 한국어로 답한다. 코드·주석·커밋·문서는 프로젝트의 기존 언어를 따른다.

## 원칙

- **혼자 개발해도 팀이 이어받을 수 있게.** 효율과 인수인계 가능성이 충돌하면 인수인계가 이긴다.
  개인 취향이 아니라 커뮤니티가 합의한 규약을 따른다.
- **규칙은 문서가 아니라 시스템이 강제한다.** 린터·포매터·훅·CI로 옮길 수 있는 규칙은 옮긴다
  (`python-standards/templates/`). 혼자여도 branch → PR → CI → 머지를 깨지 않는다.
- **인프라는 코드다.** Docker Compose·nginx·마이그레이션까지 코드로 정의하고,
  새 팀원이 `docker compose up` 한 번으로 전체 환경을 띄울 수 있어야 한다.
- **테스트가 증거다.** "되는 것 같다"가 아니라 테스트 통과가 완료 기준이다.
  E2E로 실제 사용자 시나리오를 검증하고 DB에 데이터가 저장되는지까지 확인한다.
- **설계가 먼저다.** 설계 문서(`docs/design/`)가 구현의 근거다. 코드부터 짜지 않는다.
- **문서는 코드와 같은 PR에서 바뀐다.** 기능 완료 후 `docs/`를 동기화한다 —
  구조·수명 규칙은 `docs-structure` skill.

## 표준 스택 — 각 항목의 결정은 괄호 안 skill이 단일 출처

- **Python**: uv · ruff · mypy · pydantic (`python-standards` + `templates/`)
- **API**: FastAPI (`fastapi-standards`)
- **Data**: PostgreSQL · SQLite · SQLAlchemy · Alembic · Redis (`data-conventions`)
- **테스트·CI**: pytest + Playwright E2E, GitHub Actions (`service-conventions`)
- **인프라**: Docker Compose + nginx (`docker-compose-setup`)
- **Git·릴리즈**: Modified GitHub Flow, Conventional Commits, CHANGELOG (`git-workflow`)
- **AI/LLM**: LangChain/LangGraph, Langfuse (`llm-app-conventions`)
- **문서**: `docs/` 2-depth, 설계서 기반 (`docs-structure`, `design-doc`)

## Git·릴리즈

- 항상 feature branch에서 작업한다. PR 생성까지가 AI의 몫이고, 리뷰·머지는 사용자가 한다.
- `CHANGELOG.md`가 릴리즈 노트의 단일 출처다. 항목은 커밋 제목 복붙이 아니라 **영향**으로 쓴다.
- 버전을 지정하지 않으면 **`Z`만 +1**. `X`·`Y`는 명시적으로 번호를 말할 때만 올린다 —
  `feat:`·`BREAKING CHANGE:`로 추론하지 않는다. 절차와 노트 형식은 `git-workflow` skill.

## 코드 품질

- 라이브러리 지식은 skill에 복사하지 않는다. 설치된 버전의 소스(`site-packages`)와 MCP 문서에서 읽는다.
- 불필요한 코드와 패키지는 삭제한다.
