<!-- .github/pull_request_template.md — PR 을 열면 자동으로 채워진다. 해당 없는 항목은 지우지 말고 "해당 없음" 으로 남긴다. -->

## 무엇을, 왜
<!-- 한 단락. 설계 문서나 이슈가 있으면 링크: docs/design/DESIGN_<name>.md · #123 -->

## 검증
- [ ] `uv run pytest -m "unit or integration"` 로컬 통과 (CI 가 다시 확인)
- [ ] 판단 표면(프롬프트·체인·그래프·UI·사용자 흐름)을 건드렸다면 `tests/qa/qasheet.csv` 전체 실행 → `QA: n/n pass` / 해당 없음

## 문서·기록
- [ ] `CHANGELOG.md` `[Unreleased]` 에 영향 중심 한 줄 추가
- [ ] `docs/` 를 같은 PR 에서 갱신 (`concepts/`·`reference/`) / 해당 없음
- [ ] 설계 문서가 있다면 Status → `Implemented` / 해당 없음

## 배포 노트
- [ ] 마이그레이션 포함 여부 — 포함 시 `downgrade()` 구현 확인
- [ ] 새 env 변수 · compose · nginx 변경 여부 (있으면 아래에 명시)

<!-- 위 항목이 전부 체크되거나 "해당 없음" 이어야 머지 가능. 하나라도 비어 있으면 PR 은 열린 채로 둔다. -->
