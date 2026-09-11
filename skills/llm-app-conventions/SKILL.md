---
name: llm-app-conventions
description: Version-independent decisions for LLM applications built with LangChain/LangGraph — where prompts live (Langfuse prompt management first, app/prompts/ otherwise), Pydantic models as the only output boundary, model configuration through settings and one factory, tracing with fixed run names and tags, and when a flow is a LangGraph graph versus an LCEL pipe. Use when adding a prompt, chain, graph, LLM call, retriever, or tracing to an application.
metadata:
  reviewed: 2026-09-10
---

# LLM application conventions

LangChain's API moves faster than any document about it, so nothing here names a class that
could be renamed next quarter. Verify the current API in the installed package
(`.venv/lib/python*/site-packages/langchain_core`) before writing code — read the source at
the pinned version, not a blog post. What is fixed is **where things live and what crosses a boundary**.

## Prompts

- **Never inline in service code.** A prompt is a named, versioned artifact.
- Source of truth, in order: **Langfuse prompt management** when the project has Langfuse
  (fetch by name, pin a label such as `production`; versions and rollbacks live there);
  otherwise `app/prompts/<use_case>.py`, one module per use case, exporting the template and
  its `NAME`.
- Prompt names are `<domain>.<task>` (`support.summarize_ticket`). The same string is the
  tracing `run_name`, so a trace and its prompt are one lookup apart.
- Few-shot examples live next to the prompt, not in the calling code.

## Boundaries

- An LLM result that leaves the function that produced it is a **Pydantic model**
  (`with_structured_output(Model)` or its current equivalent). No regex over free text, no
  `json.loads` on raw completions.
- That model is a contract: it is documented in `docs/reference/` like any other schema.
- Inputs are validated the same way — a chain's first step receives a model, not a dict.

## Model configuration

- Model id, temperature, max tokens and timeout come from `Settings`: `LLM_MODEL`,
  `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, `LLM_TIMEOUT_S`. No literal model ids in code.
- **The provider is an OpenAI-compatible endpoint chosen by `LLM_BASE_URL`.** In `saas` it is
  a cloud API; in `single` (hospital, no internet) it is an on-site server such as vLLM
  (`deployment-conventions`, profile `llm`). Same client, same code — only the URL and model
  name change. A provider-specific SDK is used only when a capability has no OpenAI-compatible
  form, and then behind the same factory.
- One factory, `get_chat_model(purpose: str = "default")` in `app/core/llm.py`, is the only
  place a chat model is constructed. Per-purpose overrides (`"extraction"` at temperature 0)
  are named there, not scattered through services.
- Provider keys are env vars read by the provider SDK (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`);
  they never pass through our settings object into logs.

## Tracing

- Every invocation carries `run_name` (= prompt name), `tags` (`["<domain>", "<env>"]`) and
  `metadata` (`{"user_id": …, "request_id": …}`) through the runnable config.
- Langfuse is the tracing backend: `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`,
  `LANGFUSE_HOST`. The callback is attached once in `get_chat_model()`, not per call.
- **Tracing is optional by construction.** When `LANGFUSE_HOST` is unset (a `single` site with
  no self-hosted Langfuse), the factory attaches no callback and nothing else changes.
- Cost and latency are read from the trace, never logged by hand.

## Shape of a flow

- A **stateless pipe** (prompt → model → parser, perhaps a retriever) is an LCEL runnable.
- Anything with **state, branching, retries or a human step** is a LangGraph graph with a
  typed state model. The graph lives in `app/graphs/<flow>.py`; nodes are plain functions.
- Retrieval: vector store and embedding model are chosen in settings (`VECTOR_STORE`,
  `EMBEDDING_MODEL`) and built in `app/core/retrieval.py`. Chunking parameters are recorded
  with the index name so a reindex is reproducible.

## Tests

- Unit tests never call a provider: the factory returns a fake model when `ENV=test`.
- Split every LLM feature by oracle (`service-conventions` §Tests): what can be computed —
  the output parses into its Pydantic model, length and language limits, forbidden content —
  is pytest; whether the output is *good* is a row in `tests/qa/qasheet.csv`, judged by a
  person or an AI on the real output, with the case's input living in seed data.
- A prompt change is a judgment surface: the whole QA sheet is walked before its PR merges.
