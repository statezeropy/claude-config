# Release notes — CHANGELOG.md

`CHANGELOG.md` at the repository root is the single source of truth
([Keep a Changelog](https://keepachangelog.com): `[Unreleased]` accumulates, dated version
sections below it, compare links at the bottom). A GitHub Release body is derived from the
matching section — extracted by CI if possible, copied by hand otherwise — never written
separately, so the two cannot drift.

Entries are **curated, not generated**: do not paste commit or PR titles. Restate each change as
its **impact**, so a teammate, an operator, or an API consumer reads "what this means for me".

## Rhythm

- **On every merge:** add an entry under `## [Unreleased]`.
- **On release:** move `[Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add the compare link at the
  bottom, bump the version (rule in SKILL.md §3.1).

## Version section

Emit a heading only when it has items.

```markdown
## v<X.Y.Z> — <한 줄 테마> (<YYYY-MM-DD>)

### ⚠️ Breaking / 마이그레이션      ← 있으면 최상단
- <변경> — **영향**: <누가 뭘 해야> · **조치**: <명령/config>

### ✨ Features          (feat)
- **<scope>**: <영향 한 줄>. <왜/맥락> (#PR)
### 🐛 Fixes             (fix)
- **<scope>**: <증상 → 원인 → 해결> (#PR)
### ♻️ Refactor / ⚡ Performance   (refactor, perf)
### 🔧 Infra / Ops / CI  (chore, ci, build — 배포·인프라·deps)
### 📝 Docs              (docs)

---
**배포 노트**: 마이그레이션 실행 여부 · 새 env · 인프라(nginx/모니터링 등) 변경
**Full Changelog**: <compare 링크>
```

## Procedure — fill it deterministically from the sources

1. `git log v<PREV>..HEAD` — Conventional prefix (`feat`/`fix`/…) → category.
2. Merged PR titles and bodies → the impact sentence, keeping `#<number>` for traceability.
3. Changes under the migrations directory → ⚠️ 마이그레이션 + 배포 노트.
4. Changes to deps, docker-compose, nginx, env → 🔧 Infra/Ops + 배포 노트.
5. `BREAKING CHANGE:` footer or `type!:` → ⚠️ isolated at the top.

## Rules

- Impact first — no title copy-paste.
- Group by Conventional type.
- Breaking, migration and ops items sit at the top, separately.
- Keep the auto-generated raw list, folded, in a `<details>` block at the very bottom.
