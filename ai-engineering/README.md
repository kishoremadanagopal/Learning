# AI Engineering with LLMs

A hands-on course on building software with large language models (LLMs): 27 lessons on how LLMs work, calling model APIs, prompt engineering, retrieval-augmented generation (RAG), tools and agents, and evaluating and running AI features in production.

Each idea is built from scratch in plain Python, so you see exactly what happens inside: a tokenizer, embeddings and similarity search, sampling, a retrieval pipeline, a tool-calling agent loop and an evaluation harness. Real API code (Anthropic and OpenAI) is shown alongside, ready to run on your own computer with an API key.

AI engineering is the core of the **AI engineer** path and increasingly part of the **data / AI analyst** role: almost every product team now ships features built on LLMs.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/ai-engineering/)

The sandbox runs real Python 3.14 inside your browser (via [Pyodide](https://pyodide.org)), with NumPy. Nothing to install, no sign-up, and no API key needed: exercises use small stand-in models so every result is repeatable.

- every lesson, with **37 examples** you can run and change
- **53 exercises** with hidden tests, each with an approach, hints and a walkthrough
- **108 quiz questions**, with explanations
- diagrams for the key ideas
- your progress and code saved in your own browser

**Before you start:** you should be comfortable with Python basics: lists, dictionaries, loops, functions and a little JSON. If not, do [Learn Python from scratch](../python/) first. [Python for Data](../python-data/) helps for the NumPy parts but isn't required.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 27 lessons, each with key terms, examples, common mistakes, exercises, walkthroughs and a quiz |
| 📖 [Glossary](glossary.md) | every AI engineering term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | API patterns, prompt techniques, RAG and agent recipes, and every concept at a glance |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Try each exercise before opening help; press **Check** to run the hidden tests.
4. Stuck? Open **How to approach it**, then the hints one at a time, and the **walkthrough** only after a real attempt.
5. Try the API examples on your own computer with an API key: that's where the ideas meet real models.

## Lessons

### Part 1: How LLMs Work (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What an LLM is](lessons/01-what-is-an-llm.md) | next-token prediction, a bigram language model from scratch, pretraining, instruction tuning and reinforcement learning from feedback, foundation models, reasoning models, strengths and weaknesses, hallucinations, where an LLM fits in software | 1–2 |
| 2 | [Tokens and tokenization](lessons/02-tokens.md) | tokens and vocabularies, characters versus words versus subwords, byte-pair encoding, counting and estimating tokens, token-based pricing, context windows, tokenizer quirks with spelling, numbers and other languages | 3–4 |
| 3 | [Embeddings and similarity](lessons/03-embeddings.md) | vectors and embeddings, meaning as direction, dot product, cosine similarity, Euclidean distance, normalisation, nearest-neighbour search, bag-of-words vectors versus learned embeddings, embedding APIs, uses of embeddings | 5–6 |
| 4 | [Transformers and attention](lessons/04-attention.md) | the transformer architecture, token and position embeddings, softmax, self-attention with queries, keys and values, scaling by the square root of the dimension, causal masking, multi-head attention, the cost of long contexts, the KV cache | 7–8 |
| 5 | [Sampling and temperature](lessons/05-sampling.md) | logits and probabilities, greedy decoding, random sampling, temperature, top-k, top-p (nucleus) sampling, max tokens, stop sequences, seeds and determinism, choosing settings by task | 9–10 |
| 6 | [Choosing a model](lessons/06-choosing-a-model.md) | capability, context window, output limits, latency, price per input and output token, reasoning modes, modalities, hosted versus open-weight models, model tiers, a method for choosing, cost estimates, routing | 11 |

### Part 2: Working with LLM APIs (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 7 | [Requests, responses and conversations](lessons/07-messages-api.md) | the anatomy of a request (model, max tokens, system prompt, messages), content blocks, the response and its content blocks, stop reasons, token usage, stateless APIs, storing and resending conversation history, trimming and summarising history, mid-conversation system messages, other providers' APIs and multi-provider libraries, keeping API keys safe | 12–13 |
| 8 | [Streaming, errors and retries](lessons/08-streaming-and-retries.md) | server-sent events, stream event types, text and JSON deltas, assembling a streamed message, SDK streaming helpers, HTTP status codes and error types, which errors to retry, exponential backoff, jitter, retry-after, timeouts, SDK automatic retries, request IDs, fallbacks to another model or provider | 14–15 |
| 9 | [Getting reliable JSON out](lessons/09-structured-output.md) | why programs need structured data, asking for JSON in the prompt, defensive parsing, JSON Schema, constrained decoding and guaranteed structured outputs, output_config format, Pydantic models with the SDK, schema limitations, strict tool use, validating values, retrying with error feedback, designing schemas with descriptions, enums and nullable fields | 16–17 |
| 10 | [Reasoning, images and documents](lessons/10-reasoning-and-multimodal.md) | reasoning models, adaptive thinking, the effort parameter, thinking tokens and billing, max tokens and thinking, thinking display options, passing thinking blocks back, model differences, image content blocks, supported image formats and limits, estimating image tokens, the Files API, PDF document blocks, how PDFs are processed, vision limitations | 18–19 |
| 11 | [Cost, caching and batches](lessons/11-cost-and-caching.md) | where the cost of an LLM application comes from, reading usage fields, cache write and read prices, prompt caching and prefix matching, automatic caching and explicit breakpoints, cache lifetimes, minimum cacheable length, what invalidates the cache, the Message Batches API, matching batch results, token counting, routing, effort, output length and other cost levers | 20–21 |

### Part 3: Prompt Engineering (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 12 | [Writing clear prompts](lessons/12-prompt-basics.md) | what a prompt is in an application, the new-colleague test, giving context and reasons, specifying the output, positive instructions, ordered steps, matching prompt style to output style, calm wording for modern models, edge cases, roles and system prompts, prefill and sampling on the newest models, checking replies against the spec | 22–23 |
| 13 | [Examples and structure](lessons/13-examples-and-structure.md) | zero-shot and few-shot prompting, choosing relevant and diverse examples, how many examples, examples for thinking models, XML tags for instructions, documents, examples and inputs, the layout of a long prompt, documents first and question last, document metadata, grounding answers in quotes, tagged output, extracting tags with regular expressions | 24–25 |
| 14 | [Reasoning and prompt chains](lessons/14-reasoning-and-chaining.md) | when reasoning helps, prompting thinking models with goals, self-verification, chain-of-thought prompting with thinking and answer tags, reasoning before answering, prompt chains, sequential chains, parallel map and combine, routing, draft review and refine, gates between steps, voting and self-consistency | 26–27 |
| 15 | [Prompt templates and testing](lessons/15-templates-and-testing.md) | prompts as code, version control and review, naming and logging prompt versions, why format and f-strings break on braces, string.Template, Mustache-style placeholders, Jinja templates, single-pass substitution and template injection, keeping stable text cacheable, prompt test sets, pass rates, comparing prompt versions, re-testing after model changes, prompt generators | 28–29 |
| 16 | [Prompt injection and safety](lessons/16-prompt-injection.md) | direct and indirect prompt injection, jailbreaks, hidden context exposure, why prompts can't fully prevent injection, the lethal trifecta, data exfiltration through links and images, the OWASP Top 10 for LLM applications, labelling untrusted data, least privilege, human confirmation, treating output as untrusted, link allow-lists, keeping secrets out of prompts, redacting personal data, input and output screening, limits, monitoring and red-teaming | 30–31 |

### Part 4: Retrieval-Augmented Generation (RAG) (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 17 | [The RAG pipeline](lessons/17-rag-pipeline.md) | knowledge cutoffs and private data, retrieval-augmented generation, ingestion (load, clean, chunk, index, metadata), query time (retrieve, augment, generate), a tiny end-to-end RAG system, instructions to use only the documents, saying "I don't know", citing sources, the citations API, when to put everything in the prompt instead, structured data and tools, per-user permissions | 32–33 |
| 18 | [Chunking documents](lessons/18-chunking.md) | why documents are chunked, the chunk-size trade-off, fixed-size chunks, overlap, sentence and paragraph boundaries, recursive splitting, structure-aware chunking with headings, tables and code, chunk metadata, chunk headers, contextual retrieval, contextualised chunk embeddings, small-to-big retrieval | 34–35 |
| 19 | [Keyword search with BM25](lessons/19-keyword-search.md) | inverted indexes and postings lists, boolean AND queries, term frequency, inverse document frequency, the BM25 formula, saturation (k1) and length normalisation (b), Lucene's IDF variant, tokenising, stop words, stemming and lemmatisation, other languages, keyword versus vector search, BM25 tools and libraries | 36–37 |
| 20 | [Vector search and vector databases](lessons/20-vector-search.md) | semantic search, embedding documents and queries, input types, using one model for both, exact search as a matrix-vector product, memory costs, reducing dimensions, quantisation, approximate nearest-neighbour search, IVF, HNSW, product quantisation, recall, metadata filtering, pre-filtering and post-filtering, access control, pgvector, FAISS and vector databases | 38–39 |
| 21 | [Hybrid search and reranking](lessons/21-hybrid-and-reranking.md) | hybrid search, the retrieval funnel, why scores from different retrievers can't be added, reciprocal rank fusion, weighted score fusion, min-max normalisation, bi-encoders and cross-encoders, rerankers, how many chunks to pass to the model, contextual retrieval results, query rewriting, multi-query retrieval, hypothetical document embeddings (HyDE), routing | 40–41 |
| 22 | [Evaluating RAG](lessons/22-evaluating-rag.md) | measuring retrieval and generation separately, building an evaluation set, relevant chunk labels, reference answers, unanswerable and hard questions, generated questions, hit rate, recall@k, precision@k, mean reciprocal rank, nDCG, faithfulness, answer relevance, correctness, citation accuracy, refusal accuracy, LLM graders, Ragas and DeepEval, diagnosing failures, monitoring in production | 42–43 |

### Part 5: Tools and Agents (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 23 | [Tool calling](lessons/23-tool-calling.md) | why models need tools, tool definitions with names, descriptions and JSON Schemas, the tool_use and tool_result cycle, stop_reason tool_use, returning errors with is_error, parallel tool calls, tool_choice and its limits on the newest models, strict tools, client tools and server tools, tool token overhead, designing tools a model uses well | 44–45 |
| 24 | [The agent loop](lessons/24-agent-loop.md) | workflows versus agents, when to use an agent, the agent loop, stopping conditions, turn limits, budgets and timeouts, other stop reasons, SDK tool runners, the Claude Agent SDK and other agent frameworks, tools and environment feedback, plans and checkpoints, reading transcripts, detecting stuck agents, orchestrator-worker and evaluator-optimiser patterns | 46–47 |
| 25 | [The Model Context Protocol (MCP)](lessons/25-mcp.md) | the integration problem, hosts, clients and servers, tools, resources and prompts, JSON-RPC 2.0 requests, responses, errors and notifications, stdio and Streamable HTTP transports, the 2026-07-28 specification, the Python SDK, connecting servers to hosts and the MCP connector, namespacing tools, too many tools and tool search, MCP security and tool poisoning, governance under the Agentic AI Foundation | 48–49 |
| 26 | [Memory and context management](lessons/26-memory-and-context.md) | context engineering, context rot, what fills an agent's context, write, select, compress and isolate, just-in-time context, compaction and summaries, server-side compaction, clearing old tool results and context editing, sub-agents, long-term memory, the memory tool, progress files, stale memories, privacy and injected memories | 50–51 |
| 27 | [Keeping agents safe](lessons/27-agent-safety.md) | excessive agency, classifying actions by reversibility and reach, allow, ask and deny policies, default deny, meaningful human approval, sandboxes, scoped credentials, staging and dry runs, idempotency, turn, token and cost budgets, timeouts and rate limits, injection through tool results, action review, audit logs, behavioural testing | 52–53 |

## Running it on your own computer

The exercise code works in any Python 3.10 or newer (some lessons use NumPy). The API examples need the `anthropic` or `openai` package and an API key, set as an environment variable.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
