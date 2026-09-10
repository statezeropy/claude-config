---
name: vllm-serving
description: Serve and debug models on vLLM's OpenAI-compatible server — endpoint surface, speech-to-text (transcriptions/translations/realtime), model-specific request-field handling, GPU memory and startup failures, container/compose wiring. Use when deploying a vLLM server, choosing which vLLM endpoint a gateway should call, adding an ASR/STT tier, pinning image versions, or diagnosing a vLLM container that fails to start or rejects requests.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# vLLM Serving

**IMPORTANT:** Always respond in Korean to the user.

Serving guidance grounded in the vLLM source, not in blog posts. vLLM's request schema, model
support, and flag names change every few minor versions — verify against the **tag you pin**
before designing around a field.

## Verify before you design

The single highest-value habit: read the source at the pinned tag.

```bash
TAG=v0.25.1  # 반드시 실제로 쓰는 태그
B=https://raw.githubusercontent.com/vllm-project/vllm/$TAG

# 1) 요청 스키마 — 어떤 필드를 받는가
curl -s $B/vllm/entrypoints/speech_to_text/transcription/protocol.py | grep -n "^    [a-z_]*:"

# 2) 모델이 그 필드를 실제로 쓰는가 (받는 것과 쓰는 것은 다르다)
curl -s $B/vllm/model_executor/models/<model>.py | grep -n "def get_generation_prompt" -A 60

# 3) 아키텍처가 그 태그에 등록돼 있는가
curl -s $B/vllm/model_executor/models/registry.py | grep -i "<arch-name>"
```

Step 2 catches the most expensive class of bug: a field exists in the API and is silently
ignored by the model. Example — the transcription API has a `hotwords` field, but Qwen3-ASR's
`get_generation_prompt()` only reads `request_prompt`, so hotwords passed there do nothing.

Step 3 catches "the model card says vLLM supports it" when support landed after your pinned
tag (e.g. `HYV3ForCausalLM` is in `main` but not in 0.25.x, while `HunYuanDenseV1ForCausalLM` is
in both).

## Endpoint surface

Full field-level detail: [references/speech-to-text.md](references/speech-to-text.md).

| Endpoint | Use for |
|---|---|
| `POST /v1/chat/completions` | text generation, and multimodal input via `audio_url`/`image_url` |
| `POST /v1/audio/transcriptions` | ASR. `stream=true` streams output tokens as SSE `transcription.chunk` |
| `POST /v1/audio/translations` | speech→English (or `to_language`) **only if the model was trained for it** |
| `WS /v1/realtime` | streaming audio in / text deltas out. Model-specific, see caveats below |
| `GET /v1/models`, `/health`, `/load`, `/ping`, `/version`, `/metrics` | routing key + ops |
| `POST /tokenize`, `/detokenize`, `GET /tokenizer_info` | token accounting |
| `POST /invocations` | SageMaker-compatible mirror — **not covered by `--api-key`**, block at the proxy |

`--api-key` only guards `/v1`, `/v2`, `/inference` paths. Never expose a vLLM port directly to
users: put a gateway in front and keep model names out of your public API so models stay swappable.

## Speech-to-text

Load [references/speech-to-text.md](references/speech-to-text.md) before wiring an ASR tier. Key
facts that break deployments:

- **The official `vllm/vllm-openai` image has no audio dependencies.** Every upload fails with
  `400 Invalid or unsupported audio file.` Fix with a thin layer:

  ```dockerfile
  FROM vllm/vllm-openai:v0.25.1
  RUN pip install --no-cache-dir librosa soundfile
  ```

- **`stream=true` streams output only.** The audio upload must be complete — the endpoint cannot
  accept a growing audio stream. Real-time transcription therefore requires the caller to buffer
  and segment (see the tick guidance in the reference).
- **Long audio is chunked server-side** at the model's feature-extractor `chunk_length`
  (30s for Whisper-style extractors) with 1s overlap and low-energy split points. Do not
  pre-chunk unless you need control over boundaries.
- Upload cap defaults to 25MB (`VLLM_MAX_AUDIO_CLIP_FILESIZE_MB`).

## Startup failures

| Symptom in logs | Cause and fix |
|---|---|
| `Available KV cache memory: -0.38 GiB` | Weights + CUDA graphs exceed the utilization budget. Raise `--gpu-memory-utilization`; remember the fraction is of **total** GPU memory, so other processes on the card eat into it |
| `max_num_seqs (256) exceeds available Mamba cache blocks (224)` | Hybrid/Mamba models allocate one cache block per decode sequence. Lower `--max-num-seqs` (64 is plenty for a gateway with low concurrency) or raise the memory budget |
| `Engine core initialization failed ... Failed core proc(s): {}` | Generic wrapper. Grep the log for `ERROR` **above** it — the real cause is always earlier |
| `Unknown vLLM environment variable detected` | Harmless image build vars |

## Runtime guards

- **Repetition loops are a real failure mode**, not a curiosity: a single request can spin until
  `max_tokens`, turning a 0.5s call into 40s. Always send `repetition_penalty` (1.05 is a common
  model-card value) and a `max_tokens`/`max_completion_tokens` cap.
- **`--enable-prefix-caching` pays off for growing text prompts** (typing, conversation context).
  It does not help audio inputs — a growing audio window re-encodes from scratch.
- Cold start distorts the first measurement (one warm-up request per session fixes TTFT spikes).

## Compose wiring

- **Pin the image tag** (`vllm/vllm-openai:v0.25.1`), never `latest` — flags and schemas move.
- **Pin the GPU explicitly** when running more than one tier:

  ```yaml
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            device_ids: ["1"]   # count: 1 은 매번 GPU0 을 집어 tier 가 겹친다
            capabilities: [gpu]
  ```

- Give every model service a `/health` healthcheck and make dependents wait on
  `condition: service_healthy`. Model load plus CUDA graph capture takes 1–3 minutes; anything
  polling before that gets connection refused.
- Mount a shared HF cache (`~/.cache/huggingface`) so re-creating a container does not re-download
  weights.
