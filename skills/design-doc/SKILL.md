---
name: design-doc
description: Write, update or review a technical design doc (design doc, RFC, architecture proposal, ADR) in the Google design doc convention, and decide whether a change needs one at all. Use before implementation starts on a change to structure, a contract or a data model, when a decision needs sign-off, when the design changed during implementation, or when critiquing an existing design doc. After approval, hands off to implementation scopes tracked in docs/todo/. Do NOT use for writing code or for UI/visual design.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
metadata:
  reviewed: 2026-11-12
---

# Design doc — writing, updating, reviewing

What every design doc has to satisfy — the status lifecycle and what makes it reviewable — is
in the `design-docs` rule (`~/.claude/rules/design-docs.md`). Read that file before drafting
or reviewing; this skill is the procedure around it.

## Is a design doc needed?

Decide this first. The test is whether the design is ambiguous: are there real alternatives,
and would a wrong choice be expensive to undo?

- **Write one** when the change sets structure, a contract with a caller or partner, or a data
  model, and at least two approaches are defensible.
- **Write a mini design doc** — the same sections, each a few lines — when the decision is
  real but small.
- **Do not write one** when the solution is clear and the document would only say "this is how
  it is implemented"; the code and its PR description carry that better. A bug fix, a rename, a
  copy change or a single-file change does not get a design doc. Say that none is needed and
  proceed.

When unsure which of the three applies, ask.

## Mode

- **WRITE** — no existing document, or the user asks for a new one → *Writing*.
- **UPDATE** — the design changed while it was being built, or a decision in an existing doc is
  being reopened → the lifecycle in the `design-docs` rule says whether to edit, amend or
  supersede.
- **REVIEW** — an existing doc is supplied or referenced → [REVIEW.md](REVIEW.md). Critique it;
  do not rewrite it into the template.

## Writing

1. **Gather before drafting.** Draft from the code, the existing docs and prior design docs the
   decision touches. Identify what the reader already knows (Context, briefly), what is
   genuinely undecided (the document's subject), and what is fixed by constraints outside this
   decision (state it, do not re-litigate it). Take the alternatives from how established
   systems solved the same problem — a registry, a standard's resource model, a well-known
   library — two or three of them. If the decision is already made and cannot change, say so
   and stop.
2. **Draft against [TEMPLATE.md](TEMPLATE.md)**, into `docs/design/<title>.md`, the file named
   for the decision (`tenant-isolation-by-schema.md`, not `multi-tenancy.md`) in the style the
   directory already uses. The template is a default: drop a subsection that has nothing to say
   for this decision and say so in one line.
3. **Check the draft** against the `design-docs` rule before showing it, and fix what fails.
4. **Hand off as scopes, not a plan document.** Once Approved, list scopes in
   `docs/todo/<feature>.md`:
   - a scope is a vertical slice that can be finished and merged on its own, touching every
     layer it needs and only the parts it needs — a layer ("do the models") is not a scope;
   - scope 1 is the walking skeleton, the thinnest end-to-end path that proves the design in a
     running system;
   - one scope is one PR, with a done-criterion by the oracle rule (`tests` rule): a test when
     pass/fail can be computed, a QA-sheet row when it needs judgment;
   - get the user's approval of the list before starting, and redraw it after scope 1.

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
- [Software Engineering at Google, ch. 10 "Documentation"](https://abseil.io/resources/swe-book/html/ch10.html)
