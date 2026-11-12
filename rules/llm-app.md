---
paths:
  - "**/{prompts,chains,graphs,agents,llm}/**/*.py"
  - "**/*{llm,prompt,chain,graph,agent}*.py"
---

# LLM applications

The default framework is LangChain with LangGraph, and its API changes faster than any document
about it. So this file names no class or method: before writing code, read the API in the
installed package at the pinned version. What stays fixed across versions and projects is
where things live and what crosses a boundary.

## Prompts are artifacts

- A prompt is a named, versioned artifact and is not written inline in service code.
- It has one source of truth: the project's prompt-management service where there is one
  (fetched by name, pinned to a label, versions and rollbacks kept there); otherwise
  `app/prompts/<use_case>.py`, one module per use case.
- A prompt is named `<domain>.<task>` (`support.summarize_ticket`), and the same string names
  its trace, so a trace and its prompt are one lookup apart.
- Few-shot examples live next to the prompt.

## Model-facing text has its own language rule

Prompts, system messages, few-shot examples, tool names and descriptions, and any docstring
that becomes a tool schema are part of the product, not comments.

- While the feature is being built they are written in Korean, because the developer rewrites a
  prompt many times and has to be able to skim it.
- When the feature is complete — the design doc's Status becomes `Implemented` — they switch to
  English, the language models are mostly trained and evaluated in.
- The switch is a prompt change and is checked like one.

## What crosses a boundary is a schema

- An LLM result that leaves the function that produced it is a validated Pydantic model. Free
  text is not parsed with a regex, and a raw completion is not decoded by hand.
- That model is a contract and is documented like any other schema.
- Inputs are validated the same way: the first step of a flow receives a model.

## Configuration is not in code

- Model id, sampling parameters, token limit and timeout come from settings (`LLM_MODEL`,
  `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `LLM_TIMEOUT_S`); no model id is a literal.
- The provider is chosen by configuration (`LLM_BASE_URL`), so a cloud API and a local server
  run the same code. A provider-specific SDK is used only for a capability with no common
  form, behind the same factory.
- One factory — `get_chat_model(purpose)` in `app/core/llm.py` — is the only place a model
  client is constructed; per-purpose overrides are named there.
- Provider keys are read from env by the provider's client and do not pass through logs.

## Every call is traceable, and tracing is optional

- Every invocation carries its name (the prompt name), tags (domain, environment) and the
  request and user ids.
- The tracing backend is attached once, in the factory. When it is not configured, nothing
  else changes.
- Cost and latency are read from traces, not logged by hand.

## The shape of a flow follows its state

- A stateless flow — prompt, model, parser, perhaps a retriever — is a pipe.
- A flow with state, branching, retries or a human step is a graph with a typed state, in
  `app/graphs/<flow>.py`, with plain functions as nodes.
- Retrieval components are chosen in settings and built in one module; chunking parameters are
  recorded with the index so a reindex is reproducible.

## Tests

- Unit tests never call a provider: the factory returns a fake model when `ENV=test`.
- Every LLM feature splits by oracle (`tests` rule): what can be computed is pytest; whether
  the output is good is a row in the QA sheet, judged on the real output.
- A prompt change is a judgment surface: the whole QA sheet is walked before its PR merges.
