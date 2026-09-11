---
name: design-doc
description: Write or review a technical design doc (design doc, RFC, architecture proposal, ADR) using the Google design doc convention — Context and Scope, Goals and Non-Goals, Actual Design, Alternatives Considered, Cross-cutting concerns. Use before implementation starts, when a decision needs reviewer sign-off, or when critiquing an existing design doc. After approval, hands off to implementation scopes tracked in docs/todo/. Do NOT use for writing code or for UI/visual design.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
metadata:
  reviewed: 2026-09-10
---

# Design Doc (Google convention)

A design doc is a **decision artifact**, not a specification and not a plan. It exists to get
the right people to disagree with you *before* the code is written. If a section does not help
a reviewer challenge or approve the decision, it does not belong in the document.

Write documents in **English**. Section headings are fixed (below); do not rename them.

## Mode selection

Read the request before doing anything:

- **WRITE** — no existing document, or the user asks for a new design doc → follow *Writing workflow*.
- **REVIEW** — an existing doc is supplied or referenced → follow [REVIEW.md](REVIEW.md).
  Do not rewrite the document into the template. Critique it.

When ambiguous, ask which one.

## Writing workflow

### 1. Gather before drafting

Never draft from the prompt alone. Read the code, existing docs, and prior design docs the
decision touches. Identify:

- what the reviewer already knows (goes in Context, briefly)
- what is genuinely undecided (this is the document's real subject)
- what is already fixed by constraints outside this decision (state it, do not re-litigate it)

If the decision is already made and unchangeable, say so and stop. A design doc for a
foregone conclusion wastes reviewer time.

### 2. Draft against the template

Use [TEMPLATE.md](TEMPLATE.md). Fill every section. Write to
`docs/design/DESIGN_<short-name>.md`, creating `docs/design/` if needed.
When the work lands, flip **Status** to `Implemented` and fold what is now true into
`docs/concepts/` and `docs/reference/` — the design doc stays as the record of why
(see the `docs-structure` skill).

### 3. Self-check against the hard rules

Run the hard rules below against your own draft before showing it. Fix violations silently;
do not present a draft you know is non-compliant.

### 4. Hand off — scopes, not a plan document

Once the document reaches **Approved**, the design doc's job is done. What follows is not a
third document; it is a list of **scopes** in `docs/todo/<feature>.md` (the work-stream file
`docs-structure` defines — items deleted as they land, file deleted when empty).

- A scope is a **vertical slice** that can be finished and merged on its own: it touches every
  layer it needs (schema, service, endpoint, UI) and only the parts it needs. Never a layer
  ("do the models", "do the endpoints").
- **Scope 1 is the walking skeleton**: the thinnest end-to-end path that proves the design
  works in a running system. Width comes after.
- One scope = one PR. Its done-criterion follows the oracle rule (`service-conventions`
  §Tests): a test when pass/fail can be computed, a QA-sheet row when it needs judgment. No
  coverage percentages, no hour estimates.
- Get the user's approval of the scope list before starting, and **redraw it after scope 1** —
  the real structure of the work is discovered by walking it, not imagined up front.

## Hard rules

These are the parts that decay first. Enforce them.

### Status header is mandatory

Every document opens with Author / Reviewers / Status / Last Updated. Status is exactly one of
`Draft`, `In Review`, `Approved`, `Superseded`. A document with no named reviewer is not a
design doc — it is a memo. If the user has not named reviewers, ask.

### Length is capped

Default target is **1-3 pages**. Only a genuinely large, cross-team design earns 10-20 pages.
Context and Scope is **3 paragraphs maximum**. If the draft exceeds the cap, do not shrink the
font of the argument — split the document or cut scope, and say which you did.

Length is a proxy for whether the decision is actually understood. A 12-page doc for a
2-week change usually means the author has not found the real trade-off yet.

### Context and Scope is background, not argument

Context states what a reviewer unfamiliar with this corner of the system needs in order to
follow the rest. It contains **no new claims and no persuasion**. Every assertion that supports
the chosen design belongs in Actual Design, where it can be attacked.

If you catch yourself writing "therefore we should" in Context, move it.

### Non-Goals: minimum 2, and they must be plausible

A Non-Goal is something a reasonable reader **would otherwise assume is in scope**. It exists
to prevent a specific misunderstanding.

- Good: "Migrating existing records written before v2 — they stay on the old path indefinitely."
- Not a Non-Goal: "Performance optimization", "Full test coverage", "Anything not listed above."

The second kind is laziness dressed as scoping. Reject it and write a real one.

### Alternatives Considered: no strawmen

Each alternative needs **both**:

1. **Why it was attractive** — the honest case for it. If you cannot make the case, you did not
   consider it.
2. **What disqualified it** — a specific, checkable reason. "Performance would be worse" is not
   a reason; "p99 would exceed the 200 ms budget because each read fans out to N shards" is.

Minimum 2 alternatives. "Do nothing" counts and is often the strongest one. An alternative that
is obviously worse in every dimension is a strawman — delete it and find a real contender.

This section is the highest-value part of the document for reviewers. Write it before you write
Actual Design if you are struggling; it usually reveals that the decision is not yet made.

### Cross-cutting concerns are always addressed

Cover **security, privacy, observability, and cost** in every document. For each, either state
the impact or state explicitly that there is none and why. Silence reads as "not considered".

If the system touches personal data, health records, EMR/HIS data, or clinical documents,
privacy is not a checkbox — state what data is processed, where it is stored, how long it is
retained, and what de-identification applies. Say so even when the answer is "none of the above".

## Anti-patterns

| Symptom | What it means | Fix |
|---|---|---|
| Every section is long except Alternatives | Decision was made before the doc | Write Alternatives first |
| Non-Goals are negations of Goals | No real scoping done | Ask what readers would wrongly assume |
| Design section lists features | This is a spec, not a design | State trade-offs, not behaviour |
| No numbers anywhere | Nothing is falsifiable | Add budgets, limits, volumes |
| Reviewers field empty | Not a design doc | Ask who signs off |
