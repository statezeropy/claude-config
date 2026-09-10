---
name: docs-structure
description: Organize a project's docs/ directory the way Google does — the five document types (reference, conceptual, how-to/tutorial, design doc, landing page) mapped onto a two-level docs/ tree, what belongs in the code instead of docs/, where planned-but-unimplemented work goes, per-page structure with freshness metadata, the root README (what it holds, what it links to, what never goes in it), and safe restructuring with link verification. Use when creating docs/, restructuring a flat pile of markdown, deciding where a new document belongs, moving or renaming docs, or reviewing documentation for structure and staleness.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
metadata:
  reviewed: 2026-09-10
---

# Documentation structure

Google's premise is that **documentation is code**: it lives in the repository under version
control, sits next to what it documents, changes in the same PR, has an owner, and gets deleted
when it dies. Every rule below follows from that. Sources are at the bottom — read them before
overriding a rule here.

## The tree

Documentation lives in `docs/` at the project root, two levels deep:

```
docs/
├── README.md        landing page — 어디로 갈지만 알려준다
├── concepts/        "이게 뭐고 어떻게 맞물려 돌아가나"
├── how-to/          "X 를 어떻게 하나" — 절차
├── reference/       "정확한 값·필드·계약은 무엇인가"
├── design/          "왜 이렇게 결정했나" — 설계 문서 (design-doc skill 이 생성)
└── todo/            아직 하지 않은 일. 문서가 아니다 (아래 별도 절)
```

**Two levels is the default; three is allowed but not free.** Go to
`docs/reference/api/chat.md` only when a bucket has grown past roughly seven files *and* splits
along a boundary the reader already knows — a subsystem, an API surface, a deployment target.
Google's landing-page trigger generalizes to every bucket: if the list scrolls past one screen,
reorganize it by taxonomy. Never create a directory for a single file, and never nest to mirror
the source tree — someone reading `docs/` does not yet know your package layout.

**The tree is a starting point, not a fixture.** Real projects grow buckets: `docs/runbooks/`
once there is something to operate at 3 a.m., `docs/adr/` once short decision records outnumber
full design docs, `docs/how-to/ops/` once the operators and the developers stop reading the same
pages. Add a bucket when three or more documents want it — not for the first one — and write the
placement rule onto the landing page. That rule, not the initial layout, is what survives.

## Choose the type before choosing the file

Google recognizes five kinds of document, each with a different job. A page that does two jobs is
the signal to split it.

| Reader arrives asking | Type | Lives in | Optimizes for |
|---|---|---|---|
| "How do I call this function?" | reference | **the code** — docstring, 헤더 주석 | completeness |
| "What is the exact field / flag / error code?" | reference (코드에 못 담는 것) | `reference/` | completeness |
| "What is this and how does it fit together?" | conceptual | `concepts/` | clarity |
| "How do I accomplish X?" | how-to / tutorial | `how-to/` | 한 번에 성공하는 하나의 경로 |
| "Why was it built this way?" | design doc | `design/` | 기록 |
| "Where do I go?" | landing page | `docs/README.md` | navigation only |

Two rules carry most of the weight:

- **Reference documentation belongs in the code.** Signatures, parameters, raised exceptions,
  field meanings go in the docstring or header next to the thing they describe — that is the only
  copy that a reader trusts and a reviewer notices. `docs/reference/` is for contracts with no
  home in code: the HTTP surface, config keys, event names, error-code tables.
- **You get two of completeness, accuracy, clarity — rarely all three.** Name the one this page
  is for and let the others go. A concept page may simplify to stay readable; a reference page may
  not. Trying for all three is how a 400-line page nobody reads gets written.

## Planned work is not documentation

Google's answer to "where do unfinished items live" is *the tracker*. Its style guides require
every code `TODO` to carry a link to a tracked resource — current form
`# TODO: crbug.com/192795 - Investigate cpufreq optimizations.` — precisely so a pending item
cannot survive as untracked prose. "Documentation is like code" likewise includes *have issues
tracked, as bugs are tracked in code*. So:

- **If the project has an issue tracker, `docs/todo/` should not exist.** GitHub Issues wins. A
  second backlog in markdown drifts from the first within a week, and then neither is trusted.
- **If it does not** — the common case for a solo project — `docs/todo/` *is* the tracker. Then it
  must behave like one, and the landing page must name it as not-documentation:
  - one file per work stream (`docs/todo/serving-hardening.md`), never one file per item;
  - every item carries what a Google TODO carries: a link to the context (a design-doc section, a
    file path, an issue) and an owner once more than one person could pick it up;
  - **an applied item is deleted, not ticked off.** When a file's items are all applied, delete the
    file. A finished backlog is dead documentation, and dead documentation misinforms.
- **The plan and the reasoning are not backlog.** They are a design doc, and Google keeps design
  docs as a historical record. When the work lands: flip the design doc's **Status** to
  `Implemented`, fold what is now true into `concepts/` and `reference/`, delete the todo file.
  The design doc stays — it is the only place that still answers "why like this".

## Page structure

Canonical order, from Google's Markdown style guide:

1. **`# Title`** — exactly one H1, sentence case, descriptive. Task pages take a bare infinitive
   ("Run the stack"), concept pages a noun phrase ("Serving architecture"). No `-ing` opener, no
   numbers used to imply sequence.
2. **Freshness metadata**, so staleness is measurable instead of merely felt:

   ```markdown
   <!--* freshness: { owner: 'statezeropy' reviewed: '2026-09-10' } *-->
   ```

   Google's tooling mails the owner when a doc goes untouched for months. Even without tooling the
   line answers "is this still true?" faster than `git log` — and a doc with no owner goes stale.
   *Design docs are the exception:* they carry the `design-doc` template's header table (Author /
   Reviewers / Status / Last Updated), which already holds owner and date. One header per page,
   not both.
3. **One to three sentences** covering WHO / WHAT / WHY: who the page is for, what it covers, what
   the reader walks away with. WHEN is the reviewed date; WHERE is the repository.
4. **Prerequisites**, on how-to pages, before step 1.
5. **Body** — H2 and deeper, never skipping a level. Numbered lists for sequences, bullets for
   everything else, tables only for genuinely tabular data.
6. **`다음 단계` / See also** — two or three descriptive links to the natural follow-ups.

Write for both readers Google names: the **seeker**, who knows what they want and scans for it —
served by consistent structure — and the **stumbler**, who does not know yet and needs the opening
paragraph to say whether to keep reading.

Procedures: one action per step, imperative verb first, condition before instruction ("If the GPU
is missing, use the CPU profile" — not "Use the CPU profile if…"). State the expected result when
it is not obvious. Link text names the destination —
`[서빙 설정](../reference/serving-config.md)`, never `[여기](…)` or a bare filename. Code,
filenames, flags and env vars in code font. Wrap at 80 columns; links, tables, headings and code
blocks may run over.

Keep pages short: *"By keeping a document short and clear, you will ensure that it will satisfy
both an expert and a novice."* In practice that means writing the long version, then cutting it.

## Rules that keep docs alive

- **Minimum viable documentation.** *"A small set of fresh and accurate docs is better than a large
  assembly of 'documentation' in various states of disrepair."* Docs are a bonsai: alive, and
  frequently trimmed. Splitting a 100-line document into four 25-line documents is usually a loss.
- **Docs change in the same PR as the code.** A doc updated later is a doc updated never.
- **Delete dead documentation.** Dead docs *"misinform, they slow down, they incite despair in
  engineers and laziness in team leads."* If a page describes a plan rather than the code, label it
  (`설계 확정, 미구현`) or delete it; when in doubt, delete.
- **Single source of truth.** A contract — endpoint, schema, event name, error code — appears in
  exactly one file, and everything else links to it. Two copies always diverge.
- **Link, don't duplicate.** *"Do not write your own guide to a common Google technology or
  process. Link to it instead."* The same holds for FastAPI, Docker, or uv.
- **Review it.** Technical review for accuracy, audience review for clarity. One reviewer beats
  none; on a solo project the audience reviewer is you in three months, which is what the freshness
  date is for.

## Landing page

`docs/README.md` is a traffic cop: *"ensure that a landing page clearly identifies its purpose, and
then include only links to other pages."* It holds

- a "이런 상황이면 여기" table mapping situations to documents,
- the directory layout, one line per bucket,
- what in the tree is **not** documentation — `todo/`, design assets, generated exports, benchmark
  harnesses — so nobody reads them as docs,
- the rule for where a new document goes.

It holds no content of its own, and it does not serve two audiences at once — split the operator
page from the contributor page rather than sectioning one page. The repository root `README.md`
stays the entry point: purpose, status, quick start, links into `docs/`.

## Root README

The repository root `README.md` is the front door, not the house: someone who has never seen
the project learns in thirty seconds what it is and how to run it, then follows a link. Google's
rule for a package README is a short summary plus copyable commands plus links to the real
documentation — nothing more. Start from `templates/README.md`.

What it holds, in reader-urgency order:

1. **Title and one line** — what, for whom.
2. **Quick start** — at most three commands that work from a fresh clone, then the URL to open.
   This is where "`docker compose up` brings up the whole stack" is proven.
3. **구성** — the top-level directories in one line each.
4. **문서** — a pointer to `docs/README.md` and a four-row table naming the **buckets only**
   (`concepts/`, `how-to/`, `reference/`, `design/`).
5. **개발** — the two or three commands a contributor runs first.

**The README is written to change rarely.** Everything in it is something that stays true for
months — directories, buckets, the three commands. Things that change every week live where
they are already tracked:

| Not in the README | Lives in |
|---|---|
| version, release date | git tags, `pyproject.toml`, `CHANGELOG.md` |
| status, owner, contact | git history and the platform; a stale status line is worse than none |
| individual document links | `docs/README.md` — the README names buckets, never files |
| API reference | `docs/reference/` or the served OpenAPI page |
| design rationale | `docs/design/` |
| changelog | `CHANGELOG.md` |
| tutorials, troubleshooting | `docs/how-to/` |

Two consequences: the README stays under one screen, and a README diff in a PR means a
command, a directory, or the one-line purpose actually changed — never a routine bump.

In a monorepo each top-level package directory gets its own two-line README ("what is in here,
where its docs are"); the root README lists the packages.

## Restructuring safely

Moving docs breaks links silently. In this order:

1. **Inventory every reference first**, including non-markdown ones:

   ```bash
   grep -rn "docs/" --include="*.md" --include="*.py" --include="*.ts" --include="*.yml" . | grep -v node_modules
   ```

   Code comments and module docstrings routinely point at doc paths.

2. **Move with `git mv`** so history follows. Git-ignored files (design assets) need a plain `mv` —
   `git mv` fails there with "source directory is empty".

3. **Rewrite links by resolving them**, not by string-replacing filenames: resolve each link
   against its own file, map the canonical old path to the new one, then recompute the relative
   path. Same-directory links (`](design.md)`) and depth changes (`../bench/` → `../../bench/`) are
   what naive replacement misses.

   Google's own guide says to use absolute paths and avoid `../`; that is for its internal renderer.
   On GitHub a `/`-rooted link resolves against the domain, not the repo, so **keep links relative**
   and lean on the checker below.

4. **Fix prose mentions and headings too** — "see design.md §5" and "## 13. design.md와의 관계" are
   stale references even though they are not links.

5. **Verify**:

   ```bash
   scripts/check_links.py .          # 레포 전체, 깨진 링크 있으면 exit 1 → CI 게이트로 사용
   scripts/check_links.py docs README.md
   ```

   It resolves every relative markdown link and reports the ones that do not exist. For
   `file.md#anchor` only the file is checked.

6. **Update the landing page and the root README table in the same change.**

## Review checklist

- [ ] Each page answers one reader question; no page mixes procedure and reference.
- [ ] Reference material that could live in a docstring is not duplicated under `docs/`.
- [ ] Buckets are two levels deep unless a third earned its keep (>7 files, known boundary).
- [ ] Page opens with H1 + freshness header + a summary naming its audience; how-to pages list
      prerequisites.
- [ ] Steps numbered, imperative, one action each.
- [ ] Link text descriptive; no bare filenames, no "여기"; `check_links.py` passes.
- [ ] Contracts appear exactly once in the tree.
- [ ] Landing page links only, and names what is not documentation.
- [ ] Root README: Quick start works from a fresh clone; names buckets not files; no version,
      status or owner line.
- [ ] Anything describing unimplemented work is a design doc with a Status, or a `todo/` item with
      a context link — not an unlabelled page.

## Sources

- [Software Engineering at Google, ch. 10 "Documentation"](https://abseil.io/resources/swe-book/html/ch10.html)
  — document types, WHO/WHAT/WHEN/WHERE/WHY, seekers vs stumblers, freshness metadata, ownership,
  landing pages, completeness/accuracy/clarity.
- [Google documentation guide](https://google.github.io/styleguide/docguide/) — best practices
  (minimum viable documentation, same-CL updates, deleting dead docs, don't duplicate), philosophy,
  and the Markdown style guide's page layout.
- [Google developer documentation style guide](https://developers.google.com/style) — in particular
  [headings and titles](https://developers.google.com/style/headings) and
  [procedures](https://developers.google.com/style/procedures).
- [Technical Writing Two — organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
  — when to split, task-based headings, progressive disclosure.
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) — the `TODO`
  format that pending items must carry a tracked link.
