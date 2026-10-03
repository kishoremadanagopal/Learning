# AI Engineering with LLMs

A hands-on course on building software with large language models (LLMs): 6 lessons on how LLMs work, calling model APIs, prompt engineering, retrieval-augmented generation (RAG), tools and agents, and evaluating and running AI features in production.

Each idea is built from scratch in plain Python, so you see exactly what happens inside: a tokenizer, embeddings and similarity search, sampling, a retrieval pipeline, a tool-calling agent loop and an evaluation harness. Real API code (Anthropic and OpenAI) is shown alongside, ready to run on your own computer with an API key.

AI engineering is the core of the **AI engineer** path and increasingly part of the **data / AI analyst** role: almost every product team now ships features built on LLMs.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/ai-engineering/)

The sandbox runs real Python 3.14 inside your browser (via [Pyodide](https://pyodide.org)), with NumPy. Nothing to install, no sign-up, and no API key needed: exercises use small stand-in models so every result is repeatable.

- every lesson, with **11 examples** you can run and change
- **11 exercises** with hidden tests, each with an approach, hints and a walkthrough
- **24 quiz questions**, with explanations
- diagrams for the key ideas
- your progress and code saved in your own browser

**Before you start:** you should be comfortable with Python basics: lists, dictionaries, loops, functions and a little JSON. If not, do [Learn Python from scratch](../python/) first. [Python for Data](../python-data/) helps for the NumPy parts but isn't required.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 6 lessons, each with key terms, examples, common mistakes, exercises, walkthroughs and a quiz |
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

## Running it on your own computer

The exercise code works in any Python 3.10 or newer (some lessons use NumPy). The API examples need the `anthropic` or `openai` package and an API key, set as an environment variable.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
