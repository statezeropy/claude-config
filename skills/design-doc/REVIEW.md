# Reviewing a design doc

Reviewing is not reformatting. Do **not** rewrite the document into the template. A doc that
violates the structure but makes the decision clear is better than a compliant doc that hides it.

Report findings grouped as **Blocking** (approval should not proceed) and **Non-blocking**.
Quote the passage you are objecting to. If a section is fine, say nothing about it.

## Blocking checks

### The decision is identifiable

Can you state, in one sentence, what is being decided and what the alternative was? If not,
that is the first finding — everything else is secondary.

### Alternatives Considered is real

- Fewer than 2 alternatives → blocking.
- An alternative with no honest case for it → strawman, blocking.
- A disqualifying reason that is not checkable ("too slow", "doesn't scale", "too complex")
  → blocking. Ask for the number or the constraint.
- All alternatives conveniently fail on the same axis the chosen design happens to win →
  suspicious; say so.

### Non-Goals are real

- Fewer than 2 → blocking.
- Non-Goals that are just negated Goals, or generic filler ("performance optimization",
  "anything not listed") → blocking. Ask what a reader would *wrongly assume* is in scope.

### Cross-cutting concerns are addressed

Security, privacy, observability, cost — each either has an impact statement or an explicit
"no impact because ...". A missing section is blocking, not cosmetic.

If personal data, health records, EMR/HIS data, or clinical documents are anywhere in the
data flow and Privacy does not name them → blocking.

### The design is falsifiable

At least one number a reviewer could later prove wrong: latency budget, volume, cost ceiling,
retention period. A design with no numbers cannot fail review, which means review is theatre.

### Status header

Author, named Reviewers, Status, Last Updated all present. Empty Reviewers → blocking.

## Non-blocking checks

- **Context contains argument.** Persuasion in Context should move to Actual Design.
- **Length.** Over 3 pages for a non-cross-team decision usually signals the trade-off has not
  been found. Say which section is carrying the bloat.
- **Spec creep.** Actual Design enumerating behaviour rather than stating trade-offs.
- **Reversibility unstated.** Degree of freedom missing — reviewers cannot tell what is
  expensive to undo.
- **Open questions with no owner.**

## Output shape

```
## Blocking (N)

1. **<section> — <one-line claim>**
   > <quoted passage>

   <why it blocks, and what would resolve it>

## Non-blocking (N)

1. **<section> — <one-line claim>** — <what to change>

## Verdict

<Approve / Approve with changes / Needs another round> — <one sentence>
```

Do not soften a blocking finding to be agreeable, and do not manufacture findings when the
document is sound. "No blocking findings" is a valid review.
