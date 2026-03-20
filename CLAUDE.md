# Max's Global Development Standards

이 문서는 모든 프로젝트에 공통으로 적용되는 개발 원칙입니다.

## 핵심 원칙: "내가 없어도 돌아가는 코드"

혼자 개발하더라도 **팀이 이어받을 수 있는 코드**를 작성한다.
효율보다 **인수인계 가능성**이 우선이다.

## 1. 코드는 문서다

- 코드 자체가 의도를 설명해야 한다. 표준 패턴, 타입 힌트, 명확한 네이밍으로 "읽으면 이해되는 코드"를 작성한다.
- 개인 취향이 아닌 **커뮤니티가 합의한 규약**을 따른다.
- 누군가 내 코드를 처음 열었을 때 "표준 구조"라고 느끼게 한다.

## 2. 프로세스는 시스템이 강제한다

- 컨벤션을 "기억"에 의존하지 않는다. Git workflow, CI/CD, 테스트 등 **자동화된 체계**가 품질을 보장한다.
- feature branch → PR → 테스트 통과 → 머지. 혼자여도 이 흐름을 깨지 않는다.
- 비효율을 감수하더라도 **프로세스의 일관성**이 장기적으로 더 큰 가치다.

## 3. 인프라까지 코드로 관리한다

- Docker Compose, nginx, DB 마이그레이션 등 모든 인프라를 코드로 정의한다.
- 새 팀원이 `docker compose up` 한 번으로 전체 환경을 띄울 수 있어야 한다.
- 서버에 SSH 접속해서 수동으로 설정하지 않는다.

## 4. 테스트는 증거다

- "잘 되는 것 같다"가 아니라 **"테스트가 통과했다"**가 기준이다.
- E2E 테스트로 실제 사용자 시나리오를 검증하고, DB에 데이터가 정상 저장되는지까지 확인한다.
- 테스트는 팀원에게 "이 기능은 이렇게 동작해야 한다"는 **살아있는 명세서**다.

## 5. 지식을 축적하고 재사용한다

- 한 번 해결한 문제는 skill, 문서, 패턴으로 정리해서 다음 프로젝트에도 적용한다.
- 프로젝트가 바뀌어도 개발 철학은 바뀌지 않는다.

## 6. 설계가 먼저다

- 설계 문서가 곧 구현의 근거다. 코드부터 짜지 않는다.
- 단계를 나누고, 품질 게이트를 거치며, 점진적으로 전달한다.
- 기능 개발 완료 후 반드시 docs/를 코드와 동기화한다:
  - `docs/*.md`: 구현된 내용을 설계서에 반영 (변경된 구조, API, 패턴 등)
  - `docs/todo/*.md`: 적용된 항목은 파일에서 삭제한다. 모든 항목이 적용되었으면 파일 자체를 삭제한다.
  - 코드 변경과 문서 업데이트를 하나의 작업 단위로 취급한다.

## 개발 표준 스택

- **Python**: python-standards, type hints, pydantic validation
- **API**: FastAPI standards, RESTful 원칙
- **ORM**: SQLAlchemy + Alembic migration
- **DB**: PostgreSQL
- **캐싱**: Redis
- **테스트**: pytest + Playwright E2E
- **인프라**: Docker Compose + nginx
- **Git**: Modified GitHub Flow (feature branch), Conventional Commits
- **AI/LLM**: LangChain/LangGraph orchestration
- **문서**: 설계서 기반 개발 (docs/*.md)

## Git 규칙

- 항상 feature branch에서 작업한다.
- Conventional Commits를 따른다. (feat:, fix:, docs:, refactor:, test:, chore:)
- 1인 개발이라도 PR 프로세스를 유지한다.

## 코드 품질

- skills를 적극 활용하여 최신 문법과 표준 패턴을 도입한다.
- MCP 도구를 활용하여 최신 라이브러리 문서를 참조한다.
- 불필요한 코드와 패키지는 검토하여 삭제한다.
