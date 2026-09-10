---
name: docs-structure
description: Organize and write repository documentation the Google way — split docs by reader purpose (concepts / how-to / reference / decisions), landing page and per-page structure, procedure writing, descriptive link text, single source of truth, and safe restructuring with link verification. Use when creating a docs/ directory, restructuring a flat pile of markdown, deciding where a new document belongs, renaming or moving docs, or reviewing documentation for structure and staleness.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Documentation Structure (Google convention)

Google's documentation guidance splits on **why the reader opened the page**, not on which team
wrote it. A `docs/` folder organized by team artifact (`product/`, `architecture/`, `api/`) forces
readers to know the org chart; one organized by purpose does not.

For design docs / RFCs / ADR write-ups themselves, use the `design-doc` skill. This skill is about
how a repository's documentation is organized and written.

## Choose the type first

| Reader's question | Type | Directory | Title shape |
|---|---|---|---|
| "What is this and how does it work?" | conceptual | `concepts/` | noun phrase — *시스템 설계* |
| "How do I do X?" | procedural | `how-to/` | task — *스택 띄우기* |
| "What is the exact value/field?" | reference | `reference/` | noun phrase — *공개 API 계약* |
| "Why was it done this way?" | decision record | `decisions/` | *설계 결정 이력* |

A document that mixes types is the signal to split. A serving guide that contains both "run these
three commands" and "here are all the GPU flags" becomes `how-to/run-the-stack.md` +
`reference/serving-config.md`, cross-linked.

```
docs/
├── README.md      landing page — where to go, by situation
├── concepts/
├── how-to/
├── reference/
└── decisions/
```

Non-documents (design assets, generated exports, measurement harnesses) stay outside these
buckets and are named as such on the landing page, so nobody reads them as docs.

## Page structure

Every page:

1. **H1 title** that describes the content, not the file's history. Sentence case in English.
2. **One to three sentence summary** — what this page covers and who it is for. No preamble.
3. **Prerequisites** section for how-to pages, before step 1.
4. **Body.** Numbered lists for sequences, bulleted lists for everything else, tables for paired
   data (field/meaning, flag/reason, symptom/fix).
5. **`다음 단계` / What's next** — two or three descriptive links to the natural follow-ups.

Procedures: one action per step, imperative verb first, conditions before instructions
("If the GPU is missing, use the CPU profile" — not "Use the CPU profile if…"). Put the expected
result after the command when it is not obvious.

Link text names the destination, never the mechanics: `[서빙 설정](../reference/serving-config.md)`,
not `[여기](…)` or `[serving-config.md](…)`. Code, filenames, flags, and env vars in code font.

## Rules that keep docs alive

- **Minimum viable documentation.** A small set of accurate docs beats a large set in disrepair.
  Splitting a 100-line document into four 25-line documents is usually a loss.
- **Docs change in the same PR as the code.** A doc updated later is a doc updated never.
- **Delete dead documentation.** Wrong docs are worse than missing docs. If a doc describes a plan
  rather than the code, label it explicitly (`설계 확정, 미구현`) or delete it.
- **Single source of truth.** Contracts — endpoints, schemas, event names, error codes — live in
  exactly one file. Everything else links to it. Two copies of a contract always diverge.
- **Link, don't duplicate.** Never restate a common technology's guide; point at it.

## Restructuring safely

Moving docs breaks links silently. Follow this order:

1. **Inventory the references first**, including non-markdown ones:

   ```bash
   grep -rn "docs/" --include="*.md" --include="*.py" --include="*.ts" --include="*.yml" . | grep -v node_modules
   ```

   Code comments and module docstrings routinely point at doc paths.

2. **Move with `git mv`** so history follows. Files ignored by git (design assets) need a plain
   `mv` — `git mv` fails with "source directory is empty".

3. **Rewrite links by resolving them**, not by string-replacing filenames: resolve each link
   relative to its own file, map the canonical old path to the new one, then recompute the relative
   path. Same-directory links (`](design.md)`) and depth changes (`../bench/` → `../../bench/`)
   are what naive replacement misses.

4. **Fix prose mentions and headings too** — "see design.md §5" and "## 13. design.md와의 관계"
   are stale references even though they are not links.

5. **Verify**:

   ```bash
   scripts/check_links.py .          # 레포 전체
   scripts/check_links.py docs README.md
   ```

   The script parses markdown links and reports every relative target that does not resolve.
   Anchors are checked for existence of the file only.

6. **Update the landing page and the root README table** in the same change.

## Landing page

`docs/README.md` (GitHub renders it when browsing the folder; Google's own tooling uses `index.md`)
holds only navigation:

- a "read this if…" table mapping situations to documents,
- the directory layout with one line per bucket,
- what in the tree is **not** documentation,
- the rule for where a new document goes, so the structure survives the next contributor.

The repository root `README.md` stays the entry point — purpose, status, quick usage, and links
into `docs/`. Detailed content does not live there.

## Review checklist

- [ ] Each document answers one reader question; no page mixes procedure and reference.
- [ ] Page opens with a summary; how-to pages list prerequisites.
- [ ] Steps are numbered, imperative, one action each.
- [ ] Link text is descriptive; no bare filenames or "여기".
- [ ] Contracts appear exactly once in the tree.
- [ ] `check_links.py` passes; prose mentions of moved files updated.
- [ ] Anything describing an unimplemented plan is labelled or deleted.
