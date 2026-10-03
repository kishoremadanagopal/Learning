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

## Tools and agents [23–27]

- **Tool calling:** define name + description + JSON Schema; on `stop_reason: "tool_use"`, append the whole reply, run each call, and return a `tool_result` for **every** `tool_use` id (errors with `is_error: true`). Descriptions are prompts.
- **Agents:** a bounded loop: model → tools → results → repeat. Prefer a fixed workflow when the steps are known. Guard every loop with a turn limit, a budget, timeouts and repeated-call detection.
- **MCP:** a standard way to expose tools, resources and prompts to any host, over JSON-RPC (stdio locally, Streamable HTTP remotely). Install only trusted servers; namespace tool names; enable only the servers a task needs.
- **Context:** the smallest high-signal context wins. Write (notes, memory), select (just-in-time tools), compress (compaction, clear old tool results), isolate (sub-agents).
- **Safety:** default deny; allow contained, reversible actions; ask before consequential ones; sandbox and scope credentials; log every action.

| Action | Policy |
|---|---|
| read files, run tests in a sandbox | allow |
| edit shared work, open a pull request | ask |
| send, pay, delete production data, publish | ask every time, or deny |
| any tool not in the policy | deny |

## Evals and production [28–33]

- **Evals:** tasks + trials + graders. Use code graders where possible, model judges for judgement calls, humans for reference labels. Start with 20–50 cases from real failures; compare runs **case by case**; regression suites should pass near 100%.
- **pass@k** (at least one of k succeeds) for "one success is enough"; **pass^k** (all k succeed) for reliability.
- **LLM judges:** specific rubric, one criterion, reasoning before a pass/fail or 1–5 score. Swap positions in pairwise judging. Check judges against human labels with **Cohen's kappa**, not raw agreement.
- **Hallucinations:** ground in sources, allow "I don't know", quote and cite, use tools for facts, verify tool outcomes. Detect with number and claim checks, citation checks, consistency across samples and faithfulness judges; track the rate.
- **Observability:** trace every request (spans for model calls, retrieval, tools) with prompt version, tokens, cost, latency and feedback; redact personal data; grade a sample of live traffic; turn failures into eval cases.
- **Cost and latency:** latency ≈ TTFT + output tokens ÷ speed, so shorten outputs first. Report p50/p95/p99. Levers: routing, effort, caching, streaming, parallel calls, batches. Plan for peak with timeouts and fallbacks.
- **Adapting a model:** prompt → examples → RAG and tools → fine-tune. RAG changes what it knows; fine-tuning changes how it behaves. Validate data, dedupe before splitting, and beat the prompted baseline.

| Grader | Use for |
|---|---|
| code | labels, formats, required facts, tests passing |
| model judge | tone, helpfulness, faithfulness, reasoning quality |
| human | reference labels, judge calibration, high-stakes review |

## Every concept at a glance

Generated from the **At a glance** table at the end of each lesson. The number in brackets links to the lesson.

| Concept | Approach | Time | Space | Lesson |
|---|---|---|---|---|
| Bigram model | count which word follows which; sample in proportion | O(n) to train | O(vocabulary pairs) | [1](lessons/01-what-is-an-llm.md) |
| Greedy decoding | always pick the most likely next token | O(vocabulary) per token | O(1) | [1](lessons/01-what-is-an-llm.md) |
| Fixing a knowledge gap | provide documents (RAG) or a search tool | — | — | [1](lessons/01-what-is-an-llm.md) |
| An LLM feature | prompt → call → parse/validate → act → evaluate | — | — | [1](lessons/01-what-is-an-llm.md) |
| Rough token estimate (English) | characters ÷ 4, or words ÷ 0.75 | O(1) | O(1) | [2](lessons/02-tokens.md) |
| Exact token count | the provider's tokenizer or count-tokens endpoint | O(n) | O(n) | [2](lessons/02-tokens.md) |
| BPE training step | count neighbouring pairs; merge the most frequent | O(total symbols) per merge | O(pairs) | [2](lessons/02-tokens.md) |
| Request cost | tokens_in × price_in + tokens_out × price_out, per million | O(1) | O(1) | [2](lessons/02-tokens.md) |
| Cosine similarity | dot(a, b) / (‖a‖ · ‖b‖) | O(d) | O(1) | [3](lessons/03-embeddings.md) |
| Similarity on normalised vectors | dot product | O(d) | O(1) | [3](lessons/03-embeddings.md) |
| Exact top-k search | score every vector, keep the best k | O(n · d) per query | O(n) | [3](lessons/03-embeddings.md) |
| Many similarities at once | matrix-vector product in NumPy | O(n · d) | O(n · d) | [3](lessons/03-embeddings.md) |
| Stable softmax | subtract the max, exponentiate, normalise | O(n) | O(n) | [4](lessons/04-attention.md) |
| Attention for one query | softmax(q · kᵢ / √d), then weighted sum of values | O(n · d) | O(n) | [4](lessons/04-attention.md) |
| Full self-attention | softmax(QKᵀ / √d) V | O(n² · d) | O(n²) | [4](lessons/04-attention.md) |
| Temperature | softmax(logits / T) | O(vocabulary) | O(vocabulary) | [5](lessons/05-sampling.md) |
| Top-k filter | keep the k highest probabilities; renormalise | O(V log V) | O(k) | [5](lessons/05-sampling.md) |
| Top-p filter | sort; keep the prefix reaching p; renormalise | O(V log V) | O(V) | [5](lessons/05-sampling.md) |
| Choose a model | filter by quality and latency; pick the cheapest | O(models) | O(models) | [6](lessons/06-choosing-a-model.md) |
| Monthly cost | requests × (tokens_in × price_in + tokens_out × price_out) / 1M | O(1) | O(1) | [6](lessons/06-choosing-a-model.md) |
| Routing | classify the request; send it to a small or large model | O(1) per request | — | [6](lessons/06-choosing-a-model.md) |
| Get the reply text | join the text blocks; skip other types | O(reply length) | O(reply length) | [7](lessons/07-messages-api.md) |
| Keep history in budget | walk newest to oldest within a token budget; start with a user turn | O(n) | O(n) | [7](lessons/07-messages-api.md) |
| Long-running chats | trim, summarise older turns, cache the prefix | — | — | [7](lessons/07-messages-api.md) |
| Assemble a stream | append each text delta to its block; read stop reason from message_delta | O(events) | O(text length) | [8](lessons/08-streaming-and-retries.md) |
| Retry decision | retryable status and attempts left | O(1) | O(1) | [8](lessons/08-streaming-and-retries.md) |
| Backoff delay | min(cap, base × 2^(attempt − 1)), at least retry-after, plus jitter | O(1) | O(1) | [8](lessons/08-streaming-and-retries.md) |
| Parse JSON from a reply | slice first { to last }; json.loads; catch errors | O(n) | O(n) | [9](lessons/09-structured-output.md) |
| Validate a record | check each schema field, then extra fields | O(fields) | O(problems) | [9](lessons/09-structured-output.md) |
| Reliable structure | structured outputs, then validate values, then retry with feedback | — | — | [9](lessons/09-structured-output.md) |
| Image token estimate | scale to the maximum edge; ceil(w ÷ 28) × ceil(h ÷ 28); cap | O(1) | O(1) | [10](lessons/10-reasoning-and-multimodal.md) |
| Build a multimodal message | files as blocks first, question text last | O(total bytes) | O(total bytes) | [10](lessons/10-reasoning-and-multimodal.md) |
| Choose effort | start at the default; lower it while evaluations hold | — | — | [10](lessons/10-reasoning-and-multimodal.md) |
| Call cost | sum of each token type × its price, per million | O(1) | O(1) | [11](lessons/11-cost-and-caching.md) |
| Caching saving | calls × 1 − (write + (calls − 1) × read), × tokens × price | O(1) | O(1) | [11](lessons/11-cost-and-caching.md) |
| Offline bulk work | Batch API at half price; match results by custom_id | O(requests) | O(requests) | [11](lessons/11-cost-and-caching.md) |
| Lint a prompt | split into words; set checks for shouting, vagueness, format | O(n) | O(n) | [12](lessons/12-prompt-basics.md) |
| Check a reply | one check per rule in the spec; collect failures | O(n × rules) | O(rules) | [12](lessons/12-prompt-basics.md) |
| Clear prompt | context and why, task, output format, edge cases | — | — | [12](lessons/12-prompt-basics.md) |
| Few-shot prompt | instructions, examples in tags, then the input | O(text) | O(text) | [13](lessons/13-examples-and-structure.md) |
| Extract tagged sections | re.findall with (.*?) and DOTALL | O(n) | O(matches) | [13](lessons/13-examples-and-structure.md) |
| Long-context layout | documents first, instructions, question last | — | — | [13](lessons/13-examples-and-structure.md) |
| Prompt chain | output of step k becomes input of step k + 1; optional gate | O(steps) calls | O(steps) | [14](lessons/14-reasoning-and-chaining.md) |
| Majority vote | extract, normalise, count; ties go to the first seen | O(n) | O(n) | [14](lessons/14-reasoning-and-chaining.md) |
| Map and combine | same prompt on each piece, then merge | O(pieces) calls | O(pieces) | [14](lessons/14-reasoning-and-chaining.md) |
| Render a template | one regex pass with a callback; KeyError on missing | O(n) | O(n) | [15](lessons/15-templates-and-testing.md) |
| Score a prompt | run every case, catch errors, record failures | O(cases) calls | O(cases) | [15](lessons/15-templates-and-testing.md) |
| Compare versions | same test set, compare pass rates, read failures | O(versions × cases) | O(cases) | [15](lessons/15-templates-and-testing.md) |
| Redact PII | ordered regex substitution, most specific first | O(n) | O(n) | [16](lessons/16-prompt-injection.md) |
| Safe link check | parse; https; host equals or ends with .domain | O(len × domains) | O(1) | [16](lessons/16-prompt-injection.md) |
| Defence in depth | label data, least privilege, confirm actions, check output | — | — | [16](lessons/16-prompt-injection.md) |
| Word-overlap retrieval | score = shared distinct words; stable sort; top k | O(n · m + n log n) | O(n) | [17](lessons/17-rag-pipeline.md) |
| Check citations | regex for [n]; split sentences; set arithmetic | O(n) | O(n) | [17](lessons/17-rag-pipeline.md) |
| RAG query | retrieve → insert chunks with sources → question last → answer with citations | — | — | [17](lessons/17-rag-pipeline.md) |
| Fixed-size chunks | sliding window with step size − overlap | O(n) | O(n) | [18](lessons/18-chunking.md) |
| Split by headings | stack of open headings; flush at each heading | O(n) | O(n) | [18](lessons/18-chunking.md) |
| Context for chunks | headers, contextual retrieval, small-to-big | — | — | [18](lessons/18-chunking.md) |
| Build an inverted index | for each document, add its id to each distinct word's list | O(total tokens) | O(total tokens) | [19](lessons/19-keyword-search.md) |
| AND query | intersect the postings lists | O(sum of list lengths) | O(shortest list) | [19](lessons/19-keyword-search.md) |
| BM25 score | Σ IDF × f(k1 + 1) ÷ (f + k1(1 − b + b·len ÷ avgdl)) | O(query terms × postings) | O(documents) | [19](lessons/19-keyword-search.md) |
| Exact vector search | normalise; matrix-vector product; argsort | O(n · d) | O(n · d) | [20](lessons/20-vector-search.md) |
| Filtered search | pre-filter by metadata, then rank | O(n · d + m log m) | O(m) | [20](lessons/20-vector-search.md) |
| IVF search | score centroids; search the n_probe nearest buckets | O(c · d + m · d) | O(n · d) | [20](lessons/20-vector-search.md) |
| HNSW search | greedy walk through layered neighbour graphs | about O(log n) per query | O(n · d + links) | [20](lessons/20-vector-search.md) |
| Reciprocal rank fusion | sum 1 ÷ (k + rank) per document; sort | O(entries + D log D) | O(D) | [21](lessons/21-hybrid-and-reranking.md) |
| Weighted fusion | min-max each list; α·vector + (1 − α)·keyword | O(D log D) | O(D) | [21](lessons/21-hybrid-and-reranking.md) |
| Rerank | score each shortlist item with a cross-encoder; keep the top n | O(shortlist) model calls | O(shortlist) | [21](lessons/21-hybrid-and-reranking.md) |
| Recall and precision at k | hits in top k ÷ relevant, and ÷ k | O(queries × k) | O(k) | [22](lessons/22-evaluating-rag.md) |
| Mean reciprocal rank | 1 ÷ rank of the first hit, averaged | O(queries × k) | O(1) | [22](lessons/22-evaluating-rag.md) |
| Crude groundedness | content-word overlap with the best single source | O(sentences × sources × words) | O(words) | [22](lessons/22-evaluating-rag.md) |
| Schema from a function | inspect the signature; map type hints; no default means required | O(parameters) | O(parameters) | [23](lessons/23-tool-calling.md) |
| Execute tool calls | dispatch table; one result per call; errors as is_error results | O(calls) | O(calls) | [23](lessons/23-tool-calling.md) |
| One tool round | reply with tool_use → run → tool_result message → call again | — | — | [23](lessons/23-tool-calling.md) |
| Agent loop | model → tools → results → repeat; stop on a non-tool reply or the limit | O(turns) calls | O(history) | [24](lessons/24-agent-loop.md) |
| Stuck detection | last k calls identical, or the last 2k alternate | O(k) | O(k) | [24](lessons/24-agent-loop.md) |
| Choose a design | workflow if the steps are known; agent if they aren't | — | — | [24](lessons/24-agent-loop.md) |
| MCP request handling | route by method; echo the id; result or error | O(1) dispatch | O(tools) for a list | [25](lessons/25-mcp.md) |
| Namespaced tool names | server__tool; validate the pattern; reject duplicates | O(tools) | O(tools) | [25](lessons/25-mcp.md) |
| Pick a transport | local subprocess → stdio; shared or remote → Streamable HTTP | — | — | [25](lessons/25-mcp.md) |
| Compact history | summarise the older part; keep a recent tail starting with a user turn | O(n) + 1 call | O(n) | [26](lessons/26-memory-and-context.md) |
| Clear old tool results | copy; replace all but the newest k results with a placeholder | O(blocks) | O(n) | [26](lessons/26-memory-and-context.md) |
| Context strategies | write, select, compress, isolate | — | — | [26](lessons/26-memory-and-context.md) |
| Permission decision | look up a rule (default deny); call it if it's a function; deny on error | O(1) | O(1) | [27](lessons/27-agent-safety.md) |
| Budget | add usage after each call; raise when over a limit | O(1) per call | O(1) | [27](lessons/27-agent-safety.md) |
| Action risk | reversible and contained → allow; consequential → ask; irreversible and external → ask or deny | — | — | [27](lessons/27-agent-safety.md) |
| pass@k and pass^k | per task: 1 − C(n − c, k) ÷ C(n, k) and C(c, k) ÷ C(n, k); average | O(trials) | O(tasks) | [28](lessons/28-evals.md) |
| Compare runs | shared cases; rates; fixed and broken lists | O(n log n) | O(n) | [28](lessons/28-evals.md) |
| Margin of a pass rate | about 1.96 × √(p(1 − p) ÷ n) | O(1) | O(1) | [28](lessons/28-evals.md) |
| Cohen's kappa | (observed − chance agreement) ÷ (1 − chance agreement) | O(n × labels) | O(labels) | [29](lessons/29-llm-as-judge.md) |
| Pairwise verdict | judge both orders; count only consistent wins | 2 judge calls | O(1) | [29](lessons/29-llm-as-judge.md) |
| Calibrate a judge | human labels on a sample; agreement and kappa; read disagreements | O(sample) | O(sample) | [29](lessons/29-llm-as-judge.md) |
| Unsupported numbers | extract; normalise to values; set difference with the sources | O(answer + sources) | O(numbers) | [30](lessons/30-hallucinations.md) |
| Verify claims | normalised (subject, attribute) lookup; supported, contradicted or unverifiable | O(facts + claims) | O(facts) | [30](lessons/30-hallucinations.md) |
| Reduce hallucination | ground, allow abstention, quote, cite, use tools, verify | — | — | [30](lessons/30-hallucinations.md) |
| Trace tree | group spans by parent; depth-first walk from the roots | O(n) | O(n) | [31](lessons/31-observability.md) |
| Trace summary | counts and sums with defaults; the slowest span | O(n) | O(1) | [31](lessons/31-observability.md) |
| Production loop | trace → dashboards and alerts → sample and grade → new eval cases | — | — | [31](lessons/31-observability.md) |
| Latency estimate | TTFT + output tokens ÷ tokens per second | O(1) | O(1) | [32](lessons/32-cost-and-latency.md) |
| Nearest-rank percentile | sort; value at rank ceil(p ÷ 100 × n) | O(n log n) | O(n) | [32](lessons/32-cost-and-latency.md) |
| Exact response cache | normalised key → stored time; hit if younger than the TTL | O(n) | O(distinct questions) | [32](lessons/32-cost-and-latency.md) |
| Validate chat data | per record: structure, roles and content, alternation, final assistant | O(messages) | O(problems) | [33](lessons/33-fine-tuning-vs-rag.md) |
| Leak-free split | dedupe normalised inputs; seeded shuffle; slice | O(n) | O(n) | [33](lessons/33-fine-tuning-vs-rag.md) |
| Choose an approach | prompt → examples → RAG and tools → fine-tune, climbing only when evals demand it | — | — | [33](lessons/33-fine-tuning-vs-rag.md) |
