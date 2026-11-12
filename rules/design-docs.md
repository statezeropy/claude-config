---
paths:
  - "**/docs/design/**/*.md"
---

# Design docs

A design doc records a decision and the trade-offs it accepts. It is not a specification and
not an implementation plan; a section that does not help a reader challenge or approve the
decision does not belong in it. Writing and reviewing one are procedures in the `design-doc`
skill; this file is what every design doc has to satisfy.

The document is written in Korean. Section headings keep their Google names — Context and
Scope, Goals and Non-Goals, Actual Design, Alternatives Considered, Cross-cutting concerns.

## Life of a design doc

| Status | Meaning | What changes the document |
|---|---|---|
| `Draft` | being written | anything |
| `In Review` | shown to whoever decides | their objections |
| `Approved` | decided; implementation may start | design changes found while building |
| `Implemented` | shipped | only the Amendments list |
| `Superseded` | replaced by a later decision | a link to the doc that replaced it |

- Until the design ships, the document follows the design: when building shows the design was
  wrong, the document changes in the same PR as the code and says what changed and why.
- After it ships, history is not rewritten. A later change of direction is a new design doc and
  the old one becomes `Superseded`; a small correction goes in the dated Amendments list.
- In a repository with reviewers, Reviewers names them and Approved means they agreed. In a
  solo repository Reviewers is `없음` and the user's go-ahead moves the status to Approved.

## What makes it reviewable

- **Status header.** Author / Reviewers / Status / Last Updated open the document, so a reader
  can tell a proposal from a record.
- **Length follows the decision.** A small decision is one to three pages; a large cross-team
  design ten to twenty, and past that it is split. A long document for a small change usually
  means the real trade-off has not been found or specification detail has crept in.
- **Context and Scope is background.** Objective facts a reader needs to follow the rest. Every
  claim that supports the chosen design goes in Actual Design, where it can be attacked.
- **Non-Goals are what a reader would wrongly assume.** Something that could reasonably be a
  goal and is deliberately not — "existing records written before v2 stay on the old path".
  "Performance optimization" and "anything not listed" are not Non-Goals. The list is not
  padded to reach a number.
- **Alternatives are real contenders.** Each states why it was attractive and the specific,
  checkable reason it lost ("p99 would exceed the 200 ms budget because each read fans out to
  N shards"). "Do nothing" counts. An alternative worse on every axis is a strawman.
- **Cross-cutting concerns are addressed.** Security, privacy, observability and cost each
  state an impact or state that there is none and why. Where personal data, health records or
  clinical documents are in the flow, the document says what is processed, where it is stored,
  how long it is kept and what de-identification applies.
- **Definitions are linked.** Interface and schema definitions stay in the code or
  `docs/reference/`; a design doc that pastes them goes stale the day the code changes.
