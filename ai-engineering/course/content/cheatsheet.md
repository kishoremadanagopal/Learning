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
