# AI engineering cheat sheet

The key patterns of building with large language models in one place. The number in brackets is the lesson. The table of every concept with its approach and complexity is at the end.

## How LLMs work [1–6]

- An LLM **predicts the next token**, repeatedly. It generates plausible text, not verified facts.
- **Tokens:** about 4 characters or ¾ of an English word each. Price, speed and context limits are all in tokens.
- **Embeddings:** vectors where similar meanings are close. Compare them with **cosine similarity** (the dot product, for normalised vectors).
- **Attention:** each token mixes in information from earlier tokens: softmax(QKᵀ / √d) V. Its cost grows with the square of the length.
- **Sampling:** temperature < 1 for focused output, ≈ 1 for varied output; top-p keeps the likely "nucleus".
- **Choosing a model:** use the cheapest, fastest model that clears your quality bar on **your own** evaluation set.

Where a model exposes sampling settings (current Claude models don't; use the prompt, structured outputs and `effort` instead):

| Task | Temperature |
|---|---|
| extraction, classification, code | 0–0.3 |
| general assistant | default (often 1.0) |
| brainstorming, varied test data | ≈ 1.0 or more |

## Working with LLM APIs [7–11]

- A request = **model + max_tokens + system prompt + messages** (+ tools, output format, effort). The API is **stateless**: resend the history every time.
- Read **all** text blocks, not `content[0]`, and always check the **stop reason** (`max_tokens` means cut off).
- **Stream** long or user-facing replies. **Retry** only 429, 500, 504 and 529, with exponential backoff, jitter and `retry-after`; never retry 4xx request errors. Log the request ID.
- **Structured output:** guaranteed schemas where available (`output_config.format`, `messages.parse`), then **validate values** and retry with the errors. Allow `null` for missing data.
- **Thinking:** `max_tokens` includes thinking, and all thinking is billed. Steer with **effort** (`low` … `max`).
- **Images and PDFs** are content blocks, placed **before** the question. Image tokens ≈ ⌈w ÷ 28⌉ × ⌈h ÷ 28⌉ after scaling.
- **Prompt caching:** stable content first, variable last; the prefix must match exactly and be long enough. Reads cost about 0.1× input or less; 5-minute writes 1.25×, 1-hour writes 2×.
- **Batches:** 50% off for work that can wait up to 24 hours; match results by `custom_id`.

| Status | Retry? |
|---|---|
| 400, 401, 403, 404, 413 | no: fix the request, key, permissions or size |
| 429 | yes, after `retry-after` |
| 500, 504, 529 | yes, with backoff |
