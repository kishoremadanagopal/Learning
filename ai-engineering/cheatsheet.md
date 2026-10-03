# AI engineering cheat sheet

The key patterns of building with large language models in one place. The number in brackets is the lesson. The table of every concept with its approach and complexity is at the end.

## How LLMs work [1–6]

- An LLM **predicts the next token**, repeatedly. It generates plausible text, not verified facts.
- **Tokens:** about 4 characters or ¾ of an English word each. Price, speed and context limits are all in tokens.
- **Embeddings:** vectors where similar meanings are close. Compare them with **cosine similarity** (the dot product, for normalised vectors).
- **Attention:** each token mixes in information from earlier tokens: softmax(QKᵀ / √d) V. Its cost grows with the square of the length.
- **Sampling:** temperature < 1 for focused output, ≈ 1 for varied output; top-p keeps the likely "nucleus".
- **Choosing a model:** use the cheapest, fastest model that clears your quality bar on **your own** evaluation set.

| Task | Temperature |
|---|---|
| extraction, classification, code | 0–0.3 |
| general assistant | default (often 1.0) |
| brainstorming, varied test data | ≈ 1.0 or more |

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
