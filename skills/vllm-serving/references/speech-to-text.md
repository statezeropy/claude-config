# vLLM Speech-to-Text

Field-level reference for the transcription, translation, and realtime surfaces. Verified against
`v0.25.1` source (`vllm/entrypoints/speech_to_text/`). Re-verify against your pinned tag.

## Contents

- [Transcriptions](#transcriptions)
- [Response formats](#response-formats)
- [Streaming](#streaming)
- [Server-side chunking](#server-side-chunking)
- [Translations](#translations)
- [Realtime WebSocket](#realtime-websocket)
- [Model-specific field handling](#model-specific-field-handling)
- [Buffered real-time transcription](#buffered-real-time-transcription)

## Transcriptions

`POST /v1/audio/transcriptions`, `multipart/form-data`, OpenAI-compatible.

| Field | Notes |
|---|---|
| `file` | flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm. 25MB default cap (`VLLM_MAX_AUDIO_CLIP_FILESIZE_MB`) |
| `model` | must match `--served-model-name` |
| `language` | ISO 639-1. Omitted → model does language ID |
| `prompt` | free text passed to the model. **How it is used is model-specific** |
| `hotwords` | separate biasing field — many models ignore it |
| `response_format` | `json`, `text`, `verbose_json`, `srt`, `vtt`, `diarized_json` (diarization models only) |
| `stream`, `stream_include_usage`, `stream_continuous_usage_stats` | SSE output |
| `temperature`, `top_p`, `top_k`, `min_p`, `seed`, `repetition_penalty`, `frequency_penalty`, `presence_penalty`, `max_completion_tokens` | sampling |
| `timestamp_granularities` | accepted, but only meaningful for models that emit timestamps |
| `to_language` | target language for the translate task |
| `vllm_xargs` | extension passthrough |

## Response formats

```jsonc
// json
{ "text": "...", "usage": { "type": "duration", "seconds": 13 } }

// verbose_json — segments carry chunk-level timing, avg_logprob, compression_ratio
{ "text": "...", "language": "ko", "duration": 5.42, "segments": [ … ] }
```

`srt`/`vtt` return subtitle text. `diarized_json` returns speaker-labelled segments and only works
on models that implement diarization.

## Streaming

`stream=true` returns `text/event-stream`:

```
data: {"id":"trsc-…","object":"transcription.chunk","model":"…",
       "choices":[{"delta":{"content":"안녕하"},"finish_reason":null}]}
data: [DONE]
```

The **input** must still be a complete upload. Streaming applies to generated tokens only.

## Server-side chunking

`SpeechToTextConfig` (per model) controls it:

| Field | Default | Effect |
|---|---|---|
| `sample_rate` | 16000 | server resamples uploads |
| `max_audio_clip_s` | model's feature-extractor `chunk_length` (30s for Whisper-style) | longer audio is split |
| `overlap_chunk_second` | 1 | overlap between chunks |
| `min_energy_split_window_size` | 1600 samples (~100ms) | split at the quietest point so words are not cut. `None` disables chunking |

A model can disable chunking entirely (realtime variants set `max_audio_clip_s=None`).

## Translations

`POST /v1/audio/translations` mirrors transcriptions with `language` (source) and `to_language`
(target); no `hotwords`/`timestamp_granularities`.

**The endpoint existing does not mean the model can translate.** vLLM only swaps the task tag in
the prompt; `to_language` is validated against a generic ISO list, not against model capability.
Check the model's technical report for a speech-translation benchmark before using it — an
ASR-only model will typically transcribe in the source language or produce a mismatched tag.

## Realtime WebSocket

`WS /v1/realtime`, audio as base64 **PCM16 / 16kHz / mono**.

| Direction | Events |
|---|---|
| client → server | `session.update` (model), `input_audio_buffer.append` (`{"audio":"<base64>"}`), `input_audio_buffer.commit` (`{"final":bool}`) |
| server → client | `session.created`, `transcription.delta`, `transcription.done`, `error` |

Caveats that decide whether it is usable:

- Requires a **separate server instance** with a realtime architecture override, e.g.
  `--hf-overrides '{"architectures":["Qwen3ASRRealtimeGeneration"]}'` — it cannot coexist with the
  REST transcription tier in one process.
- Segment duration may be **hardcoded** in the model file (Qwen3-ASR: `segment_duration_s = 5.0`),
  with no session parameter.
- Some implementations process each segment in isolation (no cross-segment context, no
  draft/finalize revision, raw prompt tags leaking into deltas). Read the model's
  `buffer_realtime_audio()` before relying on it.

## Model-specific field handling

Read `get_generation_prompt()` in `vllm/model_executor/models/<model>.py`. Example — Qwen3-ASR:

- `prompt` → emitted as a **system turn** = context/terminology biasing. This is where hotwords go.
- `hotwords` → **not read at all**.
- `language` → forces a `language {Name}<asr_text>` prefix; omitted means language ID.
- `task_type=translate` → swaps the tag to `to_language`; no translation training behind it.
- User-supplied text is sanitized of ChatML tokens, so prompt injection through `prompt` is blocked.

Context injection through `prompt` has a side effect worth testing: it can change **inverse text
normalization**. Feeding raw previous transcripts flipped digit output (`15m`) into spelled-out
Korean numerals (`십오 미터`). Use a fixed block — domain line, glossary, notation instruction —
rather than piping the previous transcript in verbatim.

## Buffered real-time transcription

Since the endpoint needs complete audio, the caller owns buffering. Two strategies, measured on
90s of Korean speech with Qwen3-ASR-1.7B on one RTX 4090:

| Strategy | Tick | Latency/req | RTF | CER |
|---|---|---|---|---|
| offline baseline (whole file) | — | 0.76s | 0.008 | 6.1% |
| fixed segment | 1s | 0.05s | 0.051 | 26.9% |
| fixed segment | **5s** | **0.12s** | **0.024** | **10.1%** |
| fixed segment | 10s | 0.18s | 0.018 | 9.5% |
| 30s sliding re-transcribe | 5s | 0.50s | 0.505 | prefix stability 22–46% |

Reading:

- **1s ticks destroy accuracy** — the window cuts mid-word and the model has no context to recover.
- **5s is the knee**: 4pp worse than offline, 40× real-time headroom on one GPU.
- Sliding re-transcription keeps context but rewrites more than half the text every tick, so render
  it as tentative and only translate/commit confirmed segments. It is also where repetition loops
  appear — cap tokens and set a repetition penalty.
- Cut at silence (VAD) or an explicit end-of-utterance signal instead of a fixed boundary when
  accuracy matters more than simplicity.
