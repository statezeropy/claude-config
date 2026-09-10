---
name: llm-translation
description: Choose, prompt, and evaluate open translation models — MT-specialized vs general LLM, quantization limits for instruction following, conversational context and glossary/hotword injection, cascade speech translation, and contrastive evaluation that proves context actually helps. Use when selecting a local MT model, designing translation prompts with context or terminology constraints, deciding FP8 vs INT4, building a speech-translation pipeline, or measuring translation quality beyond BLEU/COMET.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch
---

# LLM Translation

Practical guidance for translation with locally served open models. Public benchmarks measure
**isolated sentences**; production translation lives in conversations with terminology. This skill
covers the gap.

## Model selection

Start from [references/model-landscape.md](references/model-landscape.md) for the 2026 open-model
table (sizes, licenses, single-GPU fit, benchmark numbers).

Three rules that hold across the measurements there:

1. **A translation-specialized 7B beats a general 400B on translation.** Measured on FLORES-200
   XX⇔XX: Hy-MT2-7B 86.89 XCOMET vs Qwen3.5-397B-A17B 86.29, and vs Qwen3.6-35B-A3B 82.11.
   Do not reach for a bigger general model to fix translation quality.
2. **General small LLMs do not exploit context and they hallucinate.** In a 20-item contrastive
   test, Qwen3.5-4B gained **0pp** from conversational context (35% → 35%) where Hy-MT2-7B gained
   30pp (25% → 55%), and it invented a person's name ("원장님" → "Dr. Lee") in 2 of 4 conditions.
   Specialized models scored 0 hallucinated names.
3. **Quantization degrades instruction following long before it degrades translation.**

| Variant | FLORES XX⇔XX | Instruction following (IFMTBench) |
|---|---|---|
| 7B BF16 | 87.06 | 83.14 |
| 7B FP8 | 86.92 (−0.14) | 82.38 (−0.76) |
| 7B INT4 (Q4_K_M) | 86.90 (−0.16) | **75.11 (−8.03)** |

   If the pipeline uses glossaries or context blocks, **FP8 is the floor** — INT4 keeps translating
   fine while quietly ignoring your instructions.

## Prompting

Templates: [references/prompt-templates.md](references/prompt-templates.md). Use the model card's
own templates when the model ships them; MT-specialized models are trained on those exact shapes.

Measured effect of each layer (Hy-MT2-7B-FP8, 20 context-dependent utterances, ko→en/id):

| Prompt | Score |
|---|---|
| sentence alone | 25% |
| + conversation context block | 55% |
| + glossary lines | 55% |
| + context + explicitation instruction | **70%** |

Four things that only show up when you measure:

- **A domain line in the system prompt is itself context.** Adding "you are an interpreter at a
  medical clinic front desk" lifted the *no-context* condition from 25% to 45%. Cheapest quality
  win available; never leave the domain implicit.
- **Glossary and context solve different problems.** A glossary pins the rendering of a known term
  ("원장님" → "the clinic director") but cannot resolve a pronoun. Context resolves the pronoun but
  does not enforce your preferred wording. Ship both.
- **Explicitation instructions help but can regress.** "Resolve pronouns and omitted arguments
  explicitly" fixed 4 items and broke 1 (a correct "She is parking" flipped to "You are parking").
  A/B it rather than assuming.
- **Models copy numbers from context; they do not compute them.** "3:30 appointment, push it an
  hour" produced "reschedule to 3:30 p.m., one hour later". Arithmetic belongs in application code.

Prompt shape also interacts with the model: the same general LLM scored **higher with the MT-style
template (55%) than with a chat-style system prompt (45%)**. Test both before settling.

## Speech translation

Prefer **cascade** (ASR → MT) over an end-to-end speech-translation endpoint unless the model was
trained and benchmarked for translation:

- Verification machinery (back-translation, word alignment, QE, witness language) needs the text
  intermediate. End-to-end throws it away.
- ASR models frequently expose a "translate" task that has no translation training behind it —
  check the technical report for a speech-translation benchmark, not just an API field.
- Cascade also lets the same glossary feed both stages: ASR biasing prompt **and** MT glossary
  lines. Fixing the term at transcription time prevents an error the translator cannot recover from.

## Evaluating with your own data

BLEU/COMET on FLORES tells you nothing about context handling, and public benchmarks rarely cover
non-English pairs. Build a contrastive set instead — utterances that **cannot** be translated
correctly without the preceding turns.

```bash
scripts/contrastive_context_eval.py testset.json --url http://localhost:8000/v1 --model my-model
scripts/contrastive_context_eval.py testset.json --dry-run    # 프롬프트만 출력해 점검
```

Each item carries `history`, `source`, `expect` (strings that appear when context is used) and
optional `avoid` (what appears when it is ignored) and `glossary`. The script runs four conditions
(plain / context / context+glossary / context+explicit), scores each, and reports per-condition
accuracy and latency. See the file header for the JSON schema.

Building a fair set — 20 items is enough to see a 20pp gap:

- Target real phenomena: zero anaphora, omitted objects, polysemy that the domain disambiguates,
  register/honorifics, and terminology.
- **Keep the domain out of the no-context condition**, or the baseline is inflated.
- Separate *wrong translation* from *unresolved pronoun*. "cancel it" is grammatical English, not an
  error — count it separately from "teacher" where the source means "doctor".
- Scan outputs for invented names, numbers, and clauses. A model that adds facts is disqualified for
  medical or legal use no matter its score.
- Fix sampling (`temperature=0`) so reruns are comparable, and note the deviation from the model
  card's recommended sampling in the report.
