@@ what-is-an-llm
topics: next-token prediction, a bigram language model from scratch, pretraining, instruction tuning and reinforcement learning from feedback, foundation models, reasoning models, strengths and weaknesses, hallucinations, where an LLM fits in software
terms:
- **Large language model (LLM):** a neural network trained on huge amounts of text to predict the next token.
- **Next-token prediction:** generating text one token at a time, each chosen from the model's predicted probabilities.
- **Pretraining:** the first training stage: predicting the next token on a vast text corpus.
- **Instruction tuning (supervised fine-tuning):** training on examples of instructions and good responses.
- **Reinforcement learning from feedback:** improving a model by rewarding preferred or verifiably correct responses.
- **Foundation model:** one general model adapted to many tasks through prompts, data and tools.
- **Knowledge cutoff:** the date after which a model has no training data.
- **Hallucination:** a fluent, confident output that is false or unsupported.
mistakes:
- Treating a model's answer as looked-up fact rather than generated text.
- Expecting the model to remember previous API calls (each call is stateless).
- Asking about recent or private information without providing it.
- Using a model for exact arithmetic instead of giving it a calculator tool.

glance:
- Bigram model | count which word follows which; sample in proportion | O(n) to train | O(vocabulary pairs)
- Greedy decoding | always pick the most likely next token | O(vocabulary) per token | O(1)
- Fixing a knowledge gap | provide documents (RAG) or a search tool | — | —
- An LLM feature | prompt → call → parse/validate → act → evaluate | — | —

@@ tokens
topics: tokens and vocabularies, characters versus words versus subwords, byte-pair encoding, counting and estimating tokens, token-based pricing, context windows, tokenizer quirks with spelling, numbers and other languages
terms:
- **Token:** a chunk of text (a word, part of a word, a symbol) that the model reads and writes as one unit.
- **Vocabulary:** the fixed set of tokens a tokenizer can produce, each with an integer ID.
- **Tokenizer:** the program that turns text into token IDs and back.
- **Byte-pair encoding (BPE):** building a vocabulary by repeatedly merging the most frequent neighbouring pair of symbols.
- **Context window:** the maximum number of tokens (input plus output) a model can handle in one request.
- **Input and output tokens:** tokens sent to the model and tokens it generates; priced separately.
mistakes:
- Estimating cost or context use in words or characters instead of tokens.
- Assuming every provider's tokenizer gives the same count.
- Forgetting that output tokens usually cost several times more than input tokens.
- Asking a model to count letters or do long arithmetic without a tool.

glance:
- Rough token estimate (English) | characters ÷ 4, or words ÷ 0.75 | O(1) | O(1)
- Exact token count | the provider's tokenizer or count-tokens endpoint | O(n) | O(n)
- BPE training step | count neighbouring pairs; merge the most frequent | O(total symbols) per merge | O(pairs)
- Request cost | tokens_in × price_in + tokens_out × price_out, per million | O(1) | O(1)

@@ embeddings
topics: vectors and embeddings, meaning as direction, dot product, cosine similarity, Euclidean distance, normalisation, nearest-neighbour search, bag-of-words vectors versus learned embeddings, embedding APIs, uses of embeddings
terms:
- **Vector:** a list of numbers; here, a point in a many-dimensional space.
- **Embedding:** a vector produced by a model so that similar meanings get similar vectors.
- **Dot product:** the sum of the products of matching coordinates.
- **Cosine similarity:** the dot product divided by both vectors' lengths: how closely two vectors point the same way.
- **Normalised vector:** a vector scaled to length 1.
- **Nearest-neighbour search:** finding the stored vectors most similar to a query vector.
- **Bag of words:** a vector of word counts; matches identical words but not meaning.
mistakes:
- Comparing embeddings from two different models (their spaces don't match).
- Using the raw dot product on vectors that aren't normalised.
- Expecting bag-of-words vectors to match synonyms.
- Re-embedding the whole document collection for every query instead of once.

glance:
- Cosine similarity | dot(a, b) / (‖a‖ · ‖b‖) | O(d) | O(1)
- Similarity on normalised vectors | dot product | O(d) | O(1)
- Exact top-k search | score every vector, keep the best k | O(n · d) per query | O(n)
- Many similarities at once | matrix-vector product in NumPy | O(n · d) | O(n · d)

@@ attention
topics: the transformer architecture, token and position embeddings, softmax, self-attention with queries, keys and values, scaling by the square root of the dimension, causal masking, multi-head attention, the cost of long contexts, the KV cache
terms:
- **Transformer:** the neural-network architecture behind modern LLMs, built from attention and feed-forward layers.
- **Logit:** the raw score the model gives each vocabulary token before softmax.
- **Softmax:** turns a list of scores into probabilities that sum to 1.
- **Self-attention:** each token computing a weighted mix of other tokens' information.
- **Query, key, value:** per-token vectors used by attention: what a token seeks, what it offers to match, and what it passes on.
- **Causal mask:** prevents a token from attending to later tokens during text generation.
- **Attention head:** one of several attention mechanisms run in parallel in a layer.
- **KV cache:** stored keys and values of earlier tokens, reused while generating each new token.
mistakes:
- Computing softmax without subtracting the maximum (overflow on large scores).
- Forgetting the √d scaling in attention.
- Assuming a long context is free: cost and latency grow with length.
- Burying the most important instructions in the middle of a very long prompt.

glance:
- Stable softmax | subtract the max, exponentiate, normalise | O(n) | O(n)
- Attention for one query | softmax(q · kᵢ / √d), then weighted sum of values | O(n · d) | O(n)
- Full self-attention | softmax(QKᵀ / √d) V | O(n² · d) | O(n²)

@@ sampling
topics: logits and probabilities, greedy decoding, random sampling, temperature, top-k, top-p (nucleus) sampling, max tokens, stop sequences, seeds and determinism, choosing settings by task
terms:
- **Sampling:** choosing the next token at random according to the model's probabilities.
- **Greedy decoding:** always choosing the single most likely token.
- **Temperature:** a divisor applied to logits before softmax; lower is more focused, higher more varied.
- **Top-k sampling:** sampling only from the k most likely tokens.
- **Top-p (nucleus) sampling:** sampling only from the smallest set of top tokens whose probabilities reach p.
- **Stop sequence:** a string that ends generation when produced.
- **Max tokens:** the limit on how many tokens a response may contain.
mistakes:
- Using a high temperature for extraction or classification.
- Adjusting temperature and top-p at the same time without testing.
- Assuming temperature 0 makes every output identical.
- Setting max tokens too low, cutting answers off mid-sentence.

glance:
- Temperature | softmax(logits / T) | O(vocabulary) | O(vocabulary)
- Top-k filter | keep the k highest probabilities; renormalise | O(V log V) | O(k)
- Top-p filter | sort; keep the prefix reaching p; renormalise | O(V log V) | O(V)

@@ choosing-a-model
topics: capability, context window, output limits, latency, price per input and output token, reasoning modes, modalities, hosted versus open-weight models, model tiers, a method for choosing, cost estimates, routing
terms:
- **Model tier:** a provider's range from large and capable to small, fast and cheap models.
- **Latency:** how long a response takes; often split into time to first token and tokens per second.
- **Open-weight model:** a model whose trained weights can be downloaded and run on your own hardware.
- **Hosted model:** a model you use through a provider's API or a cloud platform.
- **Routing:** sending each request to a model chosen for its difficulty or type.
- **Evaluation set:** representative examples with known good answers, used to compare models on your task.
mistakes:
- Choosing by public benchmark scores instead of your own evaluation set.
- Always using the largest model, paying more and waiting longer than needed.
- Ignoring output-token prices when estimating cost.
- Hard-coding model names without a plan to update them as new models are released.

glance:
- Choose a model | filter by quality and latency; pick the cheapest | O(models) | O(models)
- Monthly cost | requests × (tokens_in × price_in + tokens_out × price_out) / 1M | O(1) | O(1)
- Routing | classify the request; send it to a small or large model | O(1) per request | —
