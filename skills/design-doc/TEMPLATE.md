# <Design doc title — the decision, not the feature>

| | |
|---|---|
| **Author** | <name> |
| **Reviewers** | <name (role)>, <name (role)> |
| **Status** | Draft \| In Review \| Approved \| Implemented \| Superseded |
| **Last Updated** | YYYY-MM-DD |

---

## Context and Scope

<Background a reviewer needs to follow the rest. What exists today, what changed, why this is
being decided now. Maximum 3 paragraphs. No new claims, no persuasion — those belong in
Actual Design.>

## Goals and Non-Goals

### Goals

- <Observable outcome, ideally measurable.>
- <...>

### Non-Goals

- <Something a reasonable reader would assume is in scope, and explicitly is not. Say why.>
- <Minimum 2. Not "performance optimization" or "anything not listed above".>

## Actual Design

<The chosen design and — more importantly — the trade-offs it accepts. Lead with the shape of
the solution, then the consequences.>

### System context

<Where this sits relative to existing components. A diagram belongs here if the interaction is
non-obvious.>

### Interfaces and data

<APIs, schemas, storage. Include only what constrains the decision; full specs go elsewhere.>

### Constraints and budgets

<Numbers that make the design falsifiable: latency budget, data volume, QPS, retention,
cost ceiling. A design with no numbers cannot be reviewed.>

### Degree of freedom

<What this design leaves open for later, and what it locks in. Reviewers need to know which
parts are expensive to reverse.>

## Alternatives Considered

### Alternative 1: <name>

**Why it was attractive:** <the honest case for it>

**What disqualified it:** <specific, checkable reason — a number, a constraint, a dependency>

### Alternative 2: <name — "Do nothing" is a legitimate entry>

**Why it was attractive:** <...>

**What disqualified it:** <...>

## Cross-cutting concerns

### Security

<Attack surface added or removed, authn/authz changes, secrets handling. State "no impact
because ..." if that is the case.>

### Privacy

<What personal data is processed, where it is stored, retention, de-identification. If the
system touches health records, EMR/HIS data, or clinical documents, this section is mandatory
and specific.>

### Product class and deployment modes

<`product` (default) or `internal`. If `internal` — a demo, an experiment, an internal tool —
write the word and stop; the tenancy, audit, deployment-mode and reliability requirements do
not apply. If `product`: how the design behaves in `saas` and in `single` (hospital,
air-gapped) — any dependency that needs the internet and its offline fallback, tenant-scoped
data introduced and its RLS policy, what an upgrade at a customer site requires.>

### Reliability

<Product only. Failure modes and what the user sees for each; RTO and RPO as numbers; backup
cadence and where the last verified restore is recorded; what degrades when a dependency (LLM
endpoint, Redis, object storage) is down.>

### Observability

<What signals prove this works in production: metrics, logs, traces, alerts. How a failure
would be noticed.>

### Cost

<Infrastructure, licensing, operational load. Include the ongoing cost, not just build cost.>

---

## Open questions

- <Unresolved items that block approval, with an owner for each.>
