#!/usr/bin/env python3
"""Contrastive evaluation of context and glossary effects on translation quality.

Runs the same test set through four prompt conditions against an OpenAI-compatible
endpoint and scores each output by string matching, so the gain from context is a
number instead of an impression.

  plain         source sentence alone
  context       + conversation history as a background block
  ctx+term      + glossary lines (items without a glossary fall back to `context`)
  ctx+explicit  + instruction to resolve pronouns and omitted arguments explicitly

Test set schema (JSON):

  {
    "domain": "a medical clinic front desk",        // optional, used by --style chat
    "language_names": {"en": "English", "id": "Indonesian"},
    "items": [
      {
        "id": "polyseme-teacher",
        "target": "en",
        "history": ["간호사: 3번 진료실에서 진료 보시면 됩니다."],
        "source": "선생님은 지금 계신가요?",
        "expect": ["doctor", "physician"],          // context-resolved rendering
        "avoid": ["teacher"],                       // rendering when context is ignored
        "glossary": [["원장님", "the clinic director"]],   // optional
        "note": "'선생님' = 의사 vs 교사"
      }
    ]
  }

Usage:

  contrastive_context_eval.py testset.json --url http://localhost:8000/v1 --model my-model
  contrastive_context_eval.py testset.json --style chat --no-think
  contrastive_context_eval.py testset.json --dry-run          # 서버 없이 프롬프트만 확인

Only the standard library is used, so it runs anywhere Python 3.9+ does.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

CONDITIONS = ("plain", "context", "ctx+term", "ctx+explicit")

EXPLICIT_RULE = (
    "Resolve pronouns, omitted subjects and omitted objects using the background, "
    "and make the referent explicit in the translation instead of using a bare pronoun."
)


def language_name(spec: dict, code: str) -> str:
    return (spec.get("language_names") or {}).get(code, code)


def mt_prompt(spec: dict, item: dict, condition: str) -> tuple[str | None, str]:
    """Model-card style template used by MT-specialized models (system, user)."""
    target = language_name(spec, item["target"])
    blocks: list[str] = []
    if condition != "plain" and item.get("history"):
        blocks.append("[Background Information]\n" + "\n".join(item["history"]))
    if condition == "ctx+term" and item.get("glossary"):
        terms = "\n".join(f"{a} translates to {b}" for a, b in item["glossary"])
        blocks.append("Reference the following translations:\n" + terms)

    if blocks:
        rule = f" {EXPLICIT_RULE}" if condition == "ctx+explicit" else ""
        blocks.append(
            f"Please translate the following text into {target}, taking the provided "
            f"background information into consideration.{rule} Only output the translated "
            f"result.\n\n[Source Text]\n{item['source']}"
        )
        return None, "\n\n".join(blocks)

    return None, (
        f"Translate the following text into {target}. Note that you must **ONLY output "
        f"the translated result without any additional explanation**:\n\n{item['source']}"
    )


def chat_prompt(spec: dict, item: dict, condition: str) -> tuple[str | None, str]:
    """Chat style used by general-purpose LLMs (system, user)."""
    target = language_name(spec, item["target"])
    domain = spec.get("domain")
    system = (
        f"You are a professional interpreter{f' at {domain}' if domain else ''}. "
        f"Translate the user's utterance into {target}. Output only the translation "
        f"itself — no explanation, no romanization, no quotes."
    )
    blocks: list[str] = []
    if condition != "plain" and item.get("history"):
        blocks.append("Conversation so far:\n" + "\n".join(item["history"]))
    if condition == "ctx+term" and item.get("glossary"):
        blocks.append(
            "Glossary (use these exact translations):\n"
            + "\n".join(f"- {a} → {b}" for a, b in item["glossary"])
        )
    if condition == "ctx+explicit":
        blocks.append(EXPLICIT_RULE)

    if blocks:
        blocks.append(f"Now translate this utterance into {target}:\n{item['source']}")
        return system, "\n\n".join(blocks)
    return system, item["source"]


def translate(url: str, model: str, system: str | None, user: str, no_think: bool) -> tuple[str, float]:
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user}
    ]
    payload: dict[str, object] = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,  # 재현성. 모델 카드 권장값과 다르면 리포트에 명시할 것
        "repetition_penalty": 1.05,  # 반복 루프 가드
        "max_tokens": 512,
    }
    if no_think:
        payload["chat_template_kwargs"] = {"enable_thinking": False}

    request = urllib.request.Request(
        f"{url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        body = json.load(response)
    text = body["choices"][0]["message"]["content"].strip()
    return text, time.perf_counter() - started


def judge(item: dict, output: str) -> bool:
    lowered = output.lower()
    hit = any(e.lower() in lowered for e in item["expect"])
    miss = any(a.lower() in lowered for a in item.get("avoid", []))
    return hit and not miss


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("testset", type=Path)
    parser.add_argument("--url", default="http://localhost:8000/v1")
    parser.add_argument("--model", default="model")
    parser.add_argument("--style", choices=("mt", "chat"), default="mt")
    parser.add_argument("--no-think", action="store_true", help="hybrid 모델의 thinking 비활성")
    parser.add_argument("--dry-run", action="store_true", help="호출 없이 프롬프트만 출력")
    parser.add_argument("--out", type=Path, help="결과 JSON 저장 경로")
    args = parser.parse_args()

    spec = json.loads(args.testset.read_text(encoding="utf-8"))
    items = spec["items"]
    build = mt_prompt if args.style == "mt" else chat_prompt

    scores = {c: 0 for c in CONDITIONS}
    latencies: dict[str, list[float]] = {c: [] for c in CONDITIONS}
    rows: list[dict[str, object]] = []

    for item in items:
        print(f"\n■ {item['id']} ({item['target']}) — {item.get('note', '')}")
        print(f"  원문: {item['source']}")
        row: dict[str, object] = {"id": item["id"], "source": item["source"]}
        for condition in CONDITIONS:
            system, user = build(spec, item, condition)
            if args.dry_run:
                print(f"  [{condition}] system={system!r}\n    user={user!r}")
                continue
            try:
                text, elapsed = translate(args.url, args.model, system, user, args.no_think)
            except (urllib.error.URLError, TimeoutError) as exc:
                raise SystemExit(f"요청 실패({condition}) — 서버 확인 필요: {exc}") from exc
            ok = judge(item, text)
            scores[condition] += ok
            latencies[condition].append(elapsed)
            row[condition] = {"text": text, "ok": ok, "latency_s": round(elapsed, 3)}
            print(f"  [{condition:12s}] {'O' if ok else 'X'} {text}")
        rows.append(row)

    if args.dry_run:
        return

    print("\n=== 요약 ===")
    for condition in CONDITIONS:
        average = sum(latencies[condition]) / len(latencies[condition])
        print(
            f"{condition:13s} 정답 {scores[condition]:2d}/{len(items)}"
            f" ({scores[condition] / len(items):.1%})  평균 지연 {average:.2f}s"
        )

    gained = [r["id"] for r in rows if not r["plain"]["ok"] and r["ctx+explicit"]["ok"]]
    lost = [r["id"] for r in rows if r["plain"]["ok"] and not r["ctx+explicit"]["ok"]]
    print(f"\n문맥으로 고쳐진 항목 {len(gained)}: {gained}")
    print(f"문맥 때문에 퇴행한 항목 {len(lost)}: {lost}")

    if args.out:
        args.out.write_text(
            json.dumps(
                {
                    "model": args.model,
                    "style": args.style,
                    "total": len(items),
                    "scores": scores,
                    "latency_avg_s": {c: round(sum(v) / len(v), 3) for c, v in latencies.items()},
                    "rows": rows,
                },
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
