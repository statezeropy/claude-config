---
name: docs-structure
description: Create a project's docs/ tree and root README from the house template, and move or rename documents without breaking links — inventory of references, git mv, link rewriting, the check_links.py verifier. Use when creating docs/ for a project, restructuring a flat pile of markdown, moving or renaming docs, or reviewing a docs tree for structure and staleness. The documentation rules themselves load from the docs rule whenever a file under docs/ or a README is touched.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
metadata:
  reviewed: 2026-11-12
---

# Documentation — creating, restructuring, reviewing

The rules — the tree, document types, page structure, file names — are in the `docs` rule
(`~/.claude/rules/docs.md`). Read that file first when the work starts outside `docs/`.

## Creating

Start the root README from `<skill>/templates/README.md`. Create only the buckets that have a
document to hold, and write the landing page (`docs/README.md`) with the placement rule.

## Restructuring safely

Moving docs breaks links silently. In this order:

1. **Inventory every reference**, including non-markdown ones — code comments and module
   docstrings routinely point at doc paths:

   ```bash
   grep -rn "docs/" --include="*.md" --include="*.py" --include="*.ts" --include="*.yml" . | grep -v node_modules
   ```

2. **Move with `git mv`** so history follows. Git-ignored files need a plain `mv`.
3. **Rewrite links by resolving them**, not by string-replacing filenames: resolve each link
   against its own file, map the old path to the new one, then recompute the relative path.
   Same-directory links and depth changes are what naive replacement misses. Keep links
   relative — on GitHub a `/`-rooted link resolves against the domain, not the repository.
4. **Fix prose mentions and headings too** — "see design.md §5" is a stale reference even
   though it is not a link.
5. **Verify**:

   ```bash
   python3 <skill>/scripts/check_links.py .          # 레포 전체, 깨진 링크 있으면 exit 1
   python3 <skill>/scripts/check_links.py docs README.md
   ```

   It resolves every relative markdown link and reports the ones that do not exist. For
   `file.md#anchor` only the file is checked.
6. **Update the landing page and the root README table in the same change.**

## Review checklist

- [ ] Each page answers one reader question; no page mixes procedure and reference.
- [ ] Reference material that could live in a docstring or the OpenAPI text is not duplicated
      under `docs/`.
- [ ] Caller-facing pages carry no design rationale.
- [ ] Buckets are two levels deep unless a third earned its keep.
- [ ] Each page opens with its title, freshness header and a summary naming its audience.
- [ ] Link text is descriptive; `check_links.py` passes.
- [ ] Contracts appear exactly once in the tree.
- [ ] File names are lowercase-hyphen ASCII, one style per directory.
- [ ] The landing page holds links only and names what is not documentation.
- [ ] Root README: the quick start works from a fresh clone; it names buckets, not files.
- [ ] Anything describing unimplemented work is a design doc with a Status or a `todo/` item.

## Sources

- [Software Engineering at Google, ch. 10 "Documentation"](https://abseil.io/resources/swe-book/html/ch10.html)
- [Google documentation guide](https://google.github.io/styleguide/docguide/)
- [Google developer documentation style guide](https://developers.google.com/style) —
  [headings](https://developers.google.com/style/headings),
  [procedures](https://developers.google.com/style/procedures),
  [filenames](https://developers.google.com/style/filenames)
- [Nygard, "Documenting Architecture Decisions"](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
