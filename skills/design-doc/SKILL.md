---
name: design-doc
description: Write or review a technical design doc (design doc, RFC, architecture proposal, ADR) using the Google design doc convention — Context and Scope, Goals and Non-Goals, Actual Design, Alternatives Considered, Cross-cutting concerns — and decide whether a change needs one at all. Use before implementation starts on a change to structure, a contract or a data model, when a decision needs sign-off, when the design changed during implementation, or when critiquing an existing design doc. After approval, hands off to implementation scopes tracked in docs/todo/. Do NOT use for writing code or for UI/visual design.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
metadata:
  reviewed: 2026-11-12
---

# Design Doc (Google convention)

A design doc records a **decision and the trade-offs it accepts**, written before the code so
that someone can disagree while disagreeing is still cheap. It is not a specification and not
an implementation plan. A section that does not help a reader challenge or approve the decision
does not belong in it.

Write the document in **Korean** — it is a project deliverable under `docs/`, read by people and
agents alike (`CLAUDE.md` 언어). What is English stays English: identifiers, code, external
terms, and the section headings, which are fixed (below) under their Google names — do not
rename or translate them; the template and [REVIEW.md](REVIEW.md) refer to them by those names.

## Is a design doc needed?

Decide this first. The test is whether the **design is ambiguous**: are there real alternatives,
and would a wrong choice be expensive to undo?

- **Write one** when the change sets structure, a contract with a caller or partner, or a data
  model, and at least two approaches are defensible.
- **Write a mini design doc** — the same sections, each a few lines — when the decision is
  real but small.
- **Do not write one** when the solution is clear and the document would only say "this is how
  it is implemented". That is an implementation manual; the code and its PR description carry
  it better. A bug fix, a rename, a copy change or a single-file change does not get a design
  doc. Say that none is needed and proceed.

When unsure which of the three applies, ask.

## Mode selection

- **WRITE** — no existing document, or the user asks for a new design doc → *Writing workflow*.
- **UPDATE** — the design changed while it was being built, or a decision in an existing doc is
  being reopened → *Life of a design doc*.
- **REVIEW** — an existing doc is supplied or referenced → follow [REVIEW.md](REVIEW.md).
  Do not rewrite the document into the template. Critique it.

When ambiguous, ask which one.

## Writing workflow

### 1. Gather before drafting

Draft from the code, the existing docs and prior design docs the decision touches, not from
the prompt alone. Identify:

- what the reader already knows (goes in Context, briefly)
- what is genuinely undecided (this is the document's real subject)
- what is already fixed by constraints outside this decision (state it, do not re-litigate it)

Alternatives come from outside as well as from the code: look at how established systems
solved the same problem (a registry, a standard's resource model, a well-known library) and
take two or three as the candidates. An alternative invented only to be rejected is a strawman.

If the decision is already made and cannot change, say so and stop; a design doc for a
foregone conclusion wastes the reader's time.

### 2. Draft against the template

Use [TEMPLATE.md](TEMPLATE.md). The file goes to `docs/design/<title>.md`, named as the
`docs-structure` skill sets for every page — the decision, not the feature
(`tenant-isolation-by-schema.md`, not `multi-tenancy.md`). If the directory already follows
another naming style, match it; do not start a second one.

The template is a default. Google's own first rule is to write the document in the form that
makes most sense for the project, so drop a subsection that has nothing to say for this
decision and say so in one line; do not fill it with filler.

Link to interface and schema definitions; do not paste them. A design doc that carries the
full schema or the full API goes stale the day the code changes, and its trade-offs get buried.
Code appears only where a new algorithm cannot be explained without it.

### 3. Self-check

Check the draft against *What makes it reviewable* below before showing it, and fix what fails.

### 4. Hand off — scopes, not a plan document

Once the document is **Approved**, what follows is not a third document; it is a list of
**scopes** in `docs/todo/<feature>.md` (the work-stream file `docs-structure` defines — items
deleted as they land, file deleted when empty).

- A scope is a **vertical slice** that can be finished and merged on its own: it touches every
  layer it needs (schema, service, endpoint, UI) and only the parts it needs. A layer ("do the
  models", "do the endpoints") is not a scope.
- **Scope 1 is the walking skeleton**: the thinnest end-to-end path that proves the design
  works in a running system. Width comes after.
- One scope = one PR. Its done-criterion follows the oracle rule (`service-conventions`
  §Tests): a test when pass/fail can be computed, a QA-sheet row when it needs judgment. No
  coverage percentages, no hour estimates.
- Get the user's approval of the scope list before starting, and **redraw it after scope 1** —
  the real structure of the work is discovered by walking it.

## Life of a design doc

| Status | Meaning | What changes the document |
|---|---|---|
| `Draft` | being written | anything |
| `In Review` | shown to whoever decides | their objections |
| `Approved` | decided; implementation may start | **design changes found while building** |
| `Implemented` | shipped | only the Amendments list |
| `Superseded` | replaced by a later decision | a link to the doc that replaced it |

- **Until the design ships, the document follows the design.** When building shows the design
  was wrong, update the document in the same PR as the code and say what changed and why; an
  approved doc that no longer matches what is being built misleads the next reader more than no
  doc.
- **After it ships, do not rewrite history.** A later change of direction is a new design doc;
  the old one becomes `Superseded` and links forward. A small correction goes in the
  Amendments list at the end of the document, dated, with the reason.
- When the work lands, flip **Status** to `Implemented` and fold what is now true into
  `docs/concepts/` and `docs/reference/` (see `docs-structure`). The design doc stays as the
  record of why.
- **Who decides.** In a repository with reviewers, Reviewers names them and Approved means they
  agreed. In a solo repository — the project's `CLAUDE.md` says there is no human review —
  Reviewers is `없음` and the user's go-ahead is what moves the status to Approved. Ask for
  reviewer names only when the project has reviewers and none are named.

## What makes it reviewable

These are the parts that decay first. Each has a reason; apply the reason, not a count.

### Status header

Every document opens with Author / Reviewers / Status / Last Updated, Status being one of the
five values above. Without it nobody can tell whether the document is a proposal or a record.

### Length follows the decision

A mini design doc is one to three pages; a large cross-team design is ten to twenty, and past
that it is split. Context and Scope stays short — a few paragraphs. Length is a proxy for
whether the decision is understood: a long document for a small change usually means the real
trade-off has not been found, or that specification detail has crept in. When a draft runs
long, cut scope or split it, and say which.

### Context and Scope is background, not argument

Context states what a reader unfamiliar with this corner of the system needs in order to follow
the rest: objective facts, no persuasion. Every assertion that supports the chosen design
belongs in Actual Design, where it can be attacked. "Therefore we should" in Context is in the
wrong section.

### Non-Goals are things a reader would wrongly assume

A Non-Goal is something that **could reasonably be a goal and is deliberately not**. It exists
to prevent a specific misunderstanding.

- Good: "Migrating existing records written before v2 — they stay on the old path indefinitely."
- Not a Non-Goal: "Performance optimization", "Full test coverage", "Anything not listed above."

Most decisions have at least one or two. If none comes to mind, ask what a reader of the title
alone would expect to be included; do not pad the list to reach a number.

### Alternatives Considered: real contenders

For reviewers this is one of the most valuable sections. Each alternative needs **both**:

1. **Why it was attractive** — the honest case for it. If you cannot make the case, it was not
   considered.
2. **What disqualified it** — a specific, checkable reason. "Performance would be worse" is not
   a reason; "p99 would exceed the 200 ms budget because each read fans out to N shards" is.

"Do nothing" counts and is often the strongest. An alternative that is worse on every axis is a
strawman — replace it with a real contender. A document with no alternative at all is an
implementation manual (see *Is a design doc needed?*). If writing this section is hard, write
it before Actual Design; that usually shows the decision is not yet made.

### Cross-cutting concerns are addressed

Cover **security, privacy, observability, and cost**. For each, state the impact or state that
there is none and why — silence reads as "not considered".

If the system touches personal data, health records, EMR/HIS data, or clinical documents, state
what data is processed, where it is stored, how long it is retained, and what de-identification
applies, even when the answer is "none of the above".

## Anti-patterns

| Symptom | What it means | Fix |
|---|---|---|
| Every section is long except Alternatives | Decision was made before the doc | Write Alternatives first |
| Non-Goals are negations of Goals | No real scoping done | Ask what readers would wrongly assume |
| Design section lists features | This is a spec, not a design | State trade-offs, not behaviour |
| Schemas and endpoint tables pasted in full | Reference material in the wrong place | Link to the code or `docs/reference/` |
| No numbers anywhere | Nothing is falsifiable | Add budgets, limits, volumes |
| Approved, but the code went another way | The doc stopped following the design | Update it, or supersede it |

## Sources

- [Malte Ubl, "Design Docs at Google"](https://www.industrialempathy.com/posts/design-docs-at-google/)
  — purpose, the section order, when not to write one, the mini design doc, updating the doc
  while the system has not shipped.
- [Software Engineering at Google, ch. 10 "Documentation"](https://abseil.io/resources/swe-book/html/ch10.html)
  — a design doc covers goals, implementation strategy and trade-offs, and once approved acts
  as a historical record and a measure of whether the project met its goals.
