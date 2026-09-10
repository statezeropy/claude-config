<!-- 템플릿. 복사 후 <…> 를 채운다. 아래 링크는 대상 프로젝트 기준이므로 이 저장소에서는 해석되지 않는다. -->
# <프로젝트명>

<한 줄: 무엇을, 누구를 위해. 5초 안에 "내 일인가" 판단할 수 있게.>

## Quick start

```bash
git clone <repo-url> && cd <dir>
cp .env.example .env
docker compose up
```

→ http://localhost:8000/docs

## 구성

- `app/` — <한 줄>
- `alembic/` — 마이그레이션
- `tests/` — unit · integration · e2e
- `docs/` — 아래 참조

## 문서

전체 지도는 [docs/README.md](docs/README.md).

| 궁금한 것 | 위치 |
|---|---|
| 이게 어떻게 돌아가나 | `docs/concepts/` |
| X 를 어떻게 하나 | `docs/how-to/` |
| 정확한 값·계약 | `docs/reference/` |
| 왜 이렇게 결정했나 | `docs/design/` |

## 개발

```bash
uv sync && uv run pre-commit install
uv run pytest -m unit
```
