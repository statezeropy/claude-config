# Translation prompt templates

Two families: the templates an MT-specialized model ships with, and the chat-style shape used for
general LLMs. Both carry the same information; the model decides which performs better, so test both.

## MT-specialized (Hy-MT2 family, from the model card)

Use the model's own English/Chinese branch as documented — these models are trained on the exact
shapes. No default system prompt; everything goes in the user turn.

**Default**

```
Translate the following text into {target_lang}. Note that you must
**ONLY output the translated result without any additional explanation**:

{source_text}
```

**Terminology (glossary / hotword)**

```
Reference the following translations:
{term} translates to {translation}
{term} translates to {translation}

Translate the following text into {target_lang}. Note that you must
**ONLY output the translated result without any additional explanation**:

{source_text}
```

**Background information (conversational context)**

```
[Background Information]
{previous turns · domain · participants}

Please translate the following text into {target_lang}, taking the provided
background information into consideration.

[Source Text]
{source_text}
```

**Style**, **Personalization**, **Delimiters**, **Structured data** variants also exist — force a
register, apply a list of user preferences, preserve delimiter counts, or translate only
user-facing values inside JSON/XML while locking keys and placeholders. Check the current model
card rather than copying from memory.

Recommended sampling from the card: `temperature 0.7, top_p 0.6, top_k 20, repetition_penalty 1.05,
max_tokens 4096`. For reproducible evaluation use `temperature 0` and say so in the report;
keep `repetition_penalty` — repetition loops are a real failure mode on long inputs.

## General LLM (chat style)

```
system: You are a professional interpreter at {domain}. Translate the user's
        {source_lang} utterance into {target_lang}. Output only the translation
        itself — no explanation, no romanization, no quotes.

user:   Conversation so far:
        {previous turns}

        Glossary (use these exact translations):
        - {term} → {translation}

        {explicitation rule, optional}

        Now translate this utterance into {target_lang}:
        {source_text}
```

The domain clause in the system prompt is not decoration — it measurably resolves polysemy and
register on its own.

## Explicitation rule

Optional extra sentence, useful for real-time interpretation UIs where "cancel it" is less useful
than "cancel the appointment":

```
Resolve pronouns, omitted subjects and omitted objects using the background,
and make the referent explicit in the translation instead of using a bare pronoun.
```

Measured: +4 items fixed, −1 regressed out of 20. A/B before shipping.

## Injecting a glossary into both stages of a cascade

One dictionary, two injection points:

| Stage | How |
|---|---|
| ASR | transcription `prompt` field — a fixed block: domain line, terms, notation instruction. Do not pipe raw previous transcripts (it flips inverse text normalization) |
| MT | Terminology lines + `[Background Information]` block |

Retrieve per session/user (a "RAG-user" glossary) rather than sending an entire dictionary: keep the
block short enough that it does not dominate the prompt.
