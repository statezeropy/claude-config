# Writing

Applies to every piece of prose you write: replies to the user, `docs/`, README, commit and PR
bodies, comments, outbound drafts. Write it natural the first time — do not draft in AI style
and then polish. Adapted from humanize-korean (`epoko77-ai/im-not-ai`, quick-rules v2.0),
`daleseo/korean-skills` humanizer and `blader/humanizer` (all MIT). For rewriting text someone
else supplies, use the `humanize-korean` skill instead of this rule.

## Never change

- Meaning, facts, numbers, dates, units, names, product and model names, direct quotes,
  citations, causal direction, negation, the conclusion.
- Code blocks, inline code, commands, paths, identifiers, frontmatter, link targets, fixed
  section names (`Context and Scope`), standard abbreviations (API, LLM, MCP).
- Register. 격식체 stays 격식체; a doc does not drop into blog tone.
- When editing existing prose, change only what matches a pattern below. Over ~30% of the
  words changed means you are rewriting, not editing — stop and keep the author's voice.
- Do not add metaphors, rhetoric or flourishes that were not there.

## Korean — 번역투

- `~에 대해` → 목적격 조사 (`X에 대해 논의` → `X를 논의`). `~를 통해`, `~에 있어서`,
  `~와 관련하여`, `~에 기반하여` → `~로`, `~에서`, `~에`, or rephrase.
- `가지고 있다`, have/make/take + 명사 직역 → 동사·형용사 (`경쟁력을 가지고 있다` → `경쟁력이 강하다`).
- 이중 피동 `~되어진다` → `~된다`. `~에 의해` 피동 → 행위자를 주어로.
- `~할 수 있다` where the thing simply happens → 단언 (`높일 수 있다` → `높인다`).
- `그/그것/그들` repeated → 생략하거나 명사로. Korean drops obvious subjects.
- 3어절 넘는 관형절이 명사 앞에 쌓이면 문장을 나눈다. 이중 조사 `~에서의`, `~으로의` → 절로 푼다.
- `-적 N` 사슬, `-성/-화` 명사화 누적 → 동사로 푼다 (`정책의 시행` → `정책을 시행하면`).
- Plural `-들` on abstract or inanimate nouns → 뺀다.

## Korean — AI 관용구와 리듬

- 결산 피벗 `결론적으로·요약하면·이를 통해·따라서` → 대부분 지운다. 결론은 그냥 쓴다.
- `시사하는 바가 크다`, `주목할 만하다`, `본질적으로`, `핵심적으로` → 지우거나 구체적 사실로.
- Hype `혁신적·획기적·강력한·압도적` → 수치나 사실로.
- 결말 공식 `~할 때다`, `~해야 한다`, `~인 것이다`, `~라는 의미다` → 평서로 닫는다.
- 문두 접속사 `또한·나아가·아울러·게다가·즉` → 문장 순서가 흐름을 잡게 하고 지운다.
- 메타 진입 `이는`, `이 점에서` 반복 → 본문에 녹인다.
- 연결어미 뒤 쉼표 (`-고,` `-며,` `-지만,`) → 쉼표를 뺀다. 영어식 쉼표 배치도 뺀다.
- 같은 종결어미 연속, 같은 길이 문장 연속 → 길이와 끝맺음을 섞는다.
  `~고 있다` → 단순 시제로 되면 단순 시제 (`읽고 있다` → `읽는다`).
- 추정 `~로 보인다`, 미래 `~할 것이다`, 균형 `장점도 있지만` → 확인한 것은 단언한다.
- 괄호 영어 병기는 첫 등장에만. 한국어로 자연스러운 말은 한국어로.

## Both languages — structure and leftovers

- Not-X-but-Y framing, forced triads, `A인가 B인가` 대구, `X에서 Y로` 변환 공식 반복 → 한 번만 쓰거나 평서로.
- Staged run-ups (`Let's dive in`, `살펴보겠습니다`), one-line dramatic closers, sayings that sound
  deep → 지운다. Start with the content.
- Chatbot residue (`좋은 질문입니다`, `도움이 되었으면 합니다`), restating the request,
  re-explaining what the reader already knows → 지운다.
- Headings: no `X: Y` subtitle pattern, no emoji, no bold inside headings. A heading is not
  repeated as the first sentence.
- Bold, quotes for emphasis, bullets and `(1)(2)(3)` only where they carry structure. Prose
  reads as prose.
- English: drop AI vocabulary (delve, pivotal, testament, seamless, robust), `serves as` for
  `is`, shallow `-ing` tails, unnamed authorities, dashes as default punctuation.

## Self-check before sending

Facts, numbers and quotes untouched; register kept; no 결산 피벗, 이중 피동, 연결어미 쉼표,
문두 접속사 run, or chatbot residue left; nothing added that the source did not say.
