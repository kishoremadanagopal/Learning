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

## Prompt engineering [12–16]

- **New-colleague test:** would a capable newcomer understand exactly what to do? Give **context and the reason** for rules, the output format and the edge cases.
- Say **what to do**, not only what not to do. Write calmly: capitals and "MUST" make modern models over-apply rules.
- **Few-shot:** 3–5 relevant, **diverse** examples in `<example>` tags. Separate instructions, documents and inputs with **XML tags**.
- **Long inputs:** documents first, question **last**; ask for relevant quotes before the answer.
- **Reasoning:** thinking models want goals and a self-check, not scripts. Without thinking, ask for `<thinking>` then `<answer>`; reasoning must come first.
- **Chains:** split a task into calls you can log and check (draft → review → refine; map → combine; route). Vote across several answers for important decisions.
- **Templates:** keep prompts in version control; fill slots in one pass (`{{name}}`, `string.Template`, Jinja), never `str.format` on prompts with JSON. Test every change on a fixed test set, and again after a model change.
- **Injection:** any text the model reads can carry instructions. Avoid the **lethal trifecta** (private data + untrusted content + external communication); use least privilege, human confirmation, allow-listed links, escaped output and redacted logs.

| Prompt part | Where |
|---|---|
| role, rules, format | system prompt (stable, cacheable) |
| long documents | top of the prompt, each in tags with its source |
| examples | `<examples>` after the documents |
| the user's question | last |

## Retrieval-augmented generation [17–22]

- **RAG:** retrieve relevant chunks → put them in the prompt with their sources (question last) → answer only from them, with citations, or say "I don't know". If everything fits in the prompt (with caching), skip retrieval.
- **Chunking:** a few hundred tokens with 10–20% overlap is a starting point; split on structure (headings, paragraphs); give chunks context (headers, contextual retrieval, small-to-big).
- **BM25:** IDF × saturated term frequency with length normalisation (k1 ≈ 1.2–2.0, b = 0.75). Best for exact terms such as codes and names; needs stemming for word variants.
- **Vector search:** same embedding model for documents and queries; normalise, then dot product. ANN indexes (HNSW, IVF) trade a little recall for speed: measure recall. Pre-filter by metadata, and always by permissions.
- **Hybrid:** keyword + vector, fused with **RRF** (Σ 1 ÷ (60 + rank)); then a **reranker** (cross-encoder) on the shortlist. Rewrite follow-up questions before searching.
- **Evaluate both halves:** retrieval (recall@k, MRR) and answers (faithfulness, correctness, citations, refusals). Change one thing at a time.

| Stage | Typical size |
|---|---|
| each retriever | top 50–150 |
| after reranking | top 5–20 into the prompt |
