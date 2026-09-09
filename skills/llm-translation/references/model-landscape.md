# Open translation models (2026 snapshot)

Numbers below are **self-reported by each model's own paper** unless marked otherwise — vendors
benchmark their own models favourably. Treat the ordering as a shortlist, not a verdict, and
re-measure on your own language pairs.

Verify current sizes, licenses, and architectures with the HF API before committing:

```bash
curl -s "https://huggingface.co/api/models/<repo-id>" | python3 -c "
import json,sys; d=json.load(sys.stdin); st=d.get('safetensors') or {}
print(round((st.get('total') or 0)/1e9,1),'B', d.get('cardData',{}).get('license'), d.get('createdAt','')[:10])"
curl -s "https://huggingface.co/<repo-id>/raw/main/config.json" | head -5   # architectures
```

## Quality (FLORES-200 XX⇔XX and WMT25, XCOMET-XXL / CometKiwi / GEMBA)

| Model | Released | FLORES XX⇔XX | WMT25 |
|---|---|---|---|
| Gemini 3.1 Pro (proprietary) | — | 88.74 / 77.60 / 90.97 | 57.58 / 69.06 / 82.23 |
| GPT-5.5 (proprietary) | — | 87.92 / 77.20 / 90.37 | 56.41 / 69.15 / 83.41 |
| Hy-MT2-30B-A3B | 2026-05 | 87.47 / 76.34 / 88.79 | 62.89 / 71.08 / 84.34 |
| **Hy-MT2-7B** | 2026-05 | 86.89 / 76.03 / 87.23 | **63.86** / 71.21 / 82.24 |
| Gemma4-31B | 2026 | 86.84 / 76.16 / 88.67 | 52.49 / 65.66 / 75.75 |
| Qwen3.5-397B-A17B | 2026-02 | 86.29 / 76.39 / 88.87 | 55.79 / 68.80 / 83.14 |
| Qwen3.6-35B-A3B | 2026-04 | 82.11 / 74.81 / 84.92 | 51.11 / 66.70 / 75.28 |
| HY-MT1.5-7B | 2026-01 | 80.98 / 73.36 / 78.30 | 61.59 / 68.85 / 75.91 |
| Hy-MT2-1.8B | 2026-05 | 79.77 / 73.41 / 78.64 | 50.30 / 64.59 / 70.36 |
| HY-MT1.5-1.8B | 2025-12 | 78.40 / 71.82 / 75.12 | 53.08 / 61.95 / 63.58 |

Instruction following on translation tasks (IFMTBench): Hy-MT2-7B 83.14, Hy-MT2-30B-A3B 84.69,
Qwen3.5-397B-A17B 80.13, Qwen3.6-35B-A3B 74.66, Hy-MT2-1.8B 69.36 — i.e. a 7B MT model follows
glossary/format instructions better than a 397B general model.

**MiLMMT-46** (Xiaomi, 1B/4B/12B, Gemma3-based, 46 languages, Gemma license) is the only family
publishing per-language numbers for Korean and Indonesian: 12B-v1.0 en→ko 92.43/88.02 and
en→id 94.04/86.73 (reference-free XCOMET/CometKiwi), beating TranslateGemma-27B and Tower-Plus-72B.

Pre-2026 baselines still cited in papers: Seed-X-7B (2025-07), Tower-Plus 2B/9B/72B (2025-06),
EuroLLM-9B, TranslateGemma 4B/12B/27B (2026-01, Gemma license, gated).

## Single 24GB GPU (RTX 4090) fit

Budget weights at ≤18GB to leave room for KV cache and CUDA graphs.

| Model | Params | bf16 | FP8 | INT4 | Verdict |
|---|---|---|---|---|---|
| Hy-MT2-1.8B | 2.0B | 4GB | 2GB | 0.4GB (1.25-bit GGUF exists) | 여유 |
| **Hy-MT2-7B** | 8.0B | 16GB | **8GB** | ~4.5GB | FP8 권장 |
| Hy-MT2-30B-A3B | 30.1B | ✗ | ✗ 30GB | ~17GB GGUF | 4bit 전용 |
| MiLMMT-46-12B | 12.2B | ✗ 24.4GB | 12.2GB | ~7GB | FP8 |
| MiLMMT-46-4B | 4.3B | 8.6GB | 4.3GB | — | 여유 |
| TranslateGemma 4B / 12B / 27B | 5.0 / 13.2 / 28.8B | 10GB / ✗ / ✗ | 5GB / 13.2GB / ✗ | — | 27B 은 4bit 전용 |
| Qwen3.5-4B / 9B | 4.7 / 9.7B | 9.4 / 19.4GB | — / 9.7GB | — | 범용 모델 |
| Qwen3.6-27B, Qwen3.8-27B | 27.8B | ✗ | ✗ | ~16GB | INT4 전용 |

Check architecture support in the **pinned** serving version, not `main`: `HunYuanDenseV1ForCausalLM`
(Hy-MT2 1.8B/7B) and `Gemma3ForConditionalGeneration` (MiLMMT) are widely available, while the
MoE `HYV3ForCausalLM` (Hy-MT2-30B-A3B) landed later.

## Not translation models

Small general SLMs (MiniCPM5-1B, NVIDIA Nemotron-3-Nano-4B) publish no translation benchmarks, and
their multilingual claims come from MMLU-style knowledge evals. Nemotron's post-training corpus
covers ko but not id; MiniCPM5 targets en/zh. Useful for auxiliary gateway work — term extraction,
sentence-boundary decisions, post-processing labels — not for the translation tier itself.

ASR models with a "translate" task (e.g. Qwen3-ASR) are not translators either: the technical
report evaluates WER, language ID, timestamps, and singing recognition, with no translation
benchmark at all.
