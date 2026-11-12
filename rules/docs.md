---
paths:
  - "**/docs/**/*.md"
  - "**/README.md"
---

# Documentation

Documentation is code: it lives in the repository, sits next to what it documents, changes in
the same PR, has an owner, and is deleted when it dies. Moving or renaming documents, and the
link checker, are in the `docs-structure` skill.

## The tree

```
docs/
├── README.md        landing page — where to go
├── concepts/        what this is and how it fits together
├── how-to/          how to do X — procedures
├── reference/       exact values, fields, contracts
├── design/          why it was decided this way (`design-docs` rule)
└── todo/            work not yet done — not documentation
```

Two levels is the default. A third level is earned when a bucket has grown past roughly seven
files and splits along a boundary the reader already knows. A bucket is added when three or
more documents want it, and its placement rule goes on the landing page. No directory holds a
single file, and the tree does not mirror the source tree.

## Choose the type before the file

| Reader arrives asking | Type | Lives in |
|---|---|---|
| How do I call this function or endpoint? | reference | the code — docstring, OpenAPI text |
| What is the exact field, flag or error code? | reference | `reference/` |
| What is this and how does it fit together? | conceptual | `concepts/` |
| How do I accomplish X? | how-to | `how-to/` |
| Why was it built this way? | design doc | `design/` |
| Where do I go? | landing page | `docs/README.md` |

- A page answers one reader question; a page doing two jobs is split.
- Reference material belongs in the code. `docs/reference/` holds only contracts with no home
  in code: flows across endpoints, config keys, event names, error-code tables.
- A contract appears in exactly one file and everything else links to it.

## Planned work is not documentation

- A project with an issue tracker has no `docs/todo/`.
- Otherwise `docs/todo/` is the tracker: one file per work stream; every item links to its
  context; an applied item is deleted, and a file whose items are all applied is deleted.
- The plan and its reasoning are a design doc. When the work lands, the design doc's Status
  becomes `Implemented`, what is now true is folded into `concepts/` and `reference/`, and the
  todo file is deleted.

## Page structure

1. One `# Title`, sentence case: a bare infinitive for a task page, a noun phrase for a
   concept page.
2. Freshness metadata, so staleness is measurable:
   `<!--* freshness: { owner: '<owner>' reviewed: 'YYYY-MM-DD' } *-->`. A design doc carries
   its own header table instead.
3. One to three sentences: who the page is for, what it covers, what the reader leaves with.
4. Prerequisites, on how-to pages.
5. Body: H2 and deeper without skipping a level; numbered lists for sequences, tables only for
   tabular data. Steps are one action each, imperative verb first, condition before
   instruction.
6. Two or three links to the natural follow-ups. Link text names the destination, never
   `여기` or a bare filename.

## Keeping docs alive

- A small set of fresh, accurate documents beats a large set in disrepair.
- Docs change in the same PR as the code.
- Dead documentation is deleted. A page describing a plan rather than the code is labelled
  (`설계 확정, 미구현`) or deleted.
- Link to the documentation of a common technology; do not rewrite it.

## Landing page and root README

- `docs/README.md` holds links only: a situation → document table, the directory layout, what
  in the tree is not documentation, and the rule for where a new document goes.
- The root `README.md` is the front door: what the project is and for whom, a quick start of
  at most three commands that work from a fresh clone, the top-level directories, a pointer to
  `docs/README.md` naming buckets only, and the first commands a contributor runs.
- The README is written to change rarely. Version, status, owner, individual document links,
  API reference, rationale and changelog live elsewhere (the GitHub Release tag,
  `CHANGELOG.md`, `docs/`).

## File names

- A file name is the page title as a path: lowercase, hyphen-joined, ASCII — also when the
  body is Korean (`배포 절차` → `deploy.md`).
- A topic prefix that groups a flat bucket (`data-`, `ui-`, `ops-`) is fine. A number or date
  is not part of a name, except where a bucket adopts a convention that requires it (ADRs).
- One style per directory: match what is there, or rename all of it in one change.
- Renaming is moving: the same links break.
