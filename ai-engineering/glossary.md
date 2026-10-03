# AI engineering glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Attention head** | One of several attention mechanisms run in parallel in a layer. [4] |
| **Bag of words** | A vector of word counts; matches identical words but not meaning. [3] |
| **Byte-pair encoding (BPE)** | Building a vocabulary by repeatedly merging the most frequent neighbouring pair of symbols. [2] |
| **Causal mask** | Prevents a token from attending to later tokens during text generation. [4] |
| **Context window** | The maximum number of tokens (input plus output) a model can handle in one request. [2] |
| **Cosine similarity** | The dot product divided by both vectors' lengths: how closely two vectors point the same way. [3] |
| **Dot product** | The sum of the products of matching coordinates. [3] |
| **Embedding** | A vector produced by a model so that similar meanings get similar vectors. [3] |
| **Evaluation set** | Representative examples with known good answers, used to compare models on your task. [6] |
| **Foundation model** | One general model adapted to many tasks through prompts, data and tools. [1] |
| **Greedy decoding** | Always choosing the single most likely token. [5] |
| **Hallucination** | A fluent, confident output that is false or unsupported. [1] |
| **Hosted model** | A model you use through a provider's API or a cloud platform. [6] |
| **Input and output tokens** | Tokens sent to the model and tokens it generates; priced separately. [2] |
| **Instruction tuning (supervised fine-tuning)** | Training on examples of instructions and good responses. [1] |
| **Knowledge cutoff** | The date after which a model has no training data. [1] |
| **KV cache** | Stored keys and values of earlier tokens, reused while generating each new token. [4] |
| **Large language model (LLM)** | A neural network trained on huge amounts of text to predict the next token. [1] |
| **Latency** | How long a response takes; often split into time to first token and tokens per second. [6] |
| **Logit** | The raw score the model gives each vocabulary token before softmax. [4] |
| **Max tokens** | The limit on how many tokens a response may contain. [5] |
| **Model tier** | A provider's range from large and capable to small, fast and cheap models. [6] |
| **Nearest-neighbour search** | Finding the stored vectors most similar to a query vector. [3] |
| **Next-token prediction** | Generating text one token at a time, each chosen from the model's predicted probabilities. [1] |
| **Normalised vector** | A vector scaled to length 1. [3] |
| **Open-weight model** | A model whose trained weights can be downloaded and run on your own hardware. [6] |
| **Pretraining** | The first training stage: predicting the next token on a vast text corpus. [1] |
| **Query, key, value** | Per-token vectors used by attention: what a token seeks, what it offers to match, and what it passes on. [4] |
| **Reinforcement learning from feedback** | Improving a model by rewarding preferred or verifiably correct responses. [1] |
| **Routing** | Sending each request to a model chosen for its difficulty or type. [6] |
| **Sampling** | Choosing the next token at random according to the model's probabilities. [5] |
| **Self-attention** | Each token computing a weighted mix of other tokens' information. [4] |
| **Softmax** | Turns a list of scores into probabilities that sum to 1. [4] |
| **Stop sequence** | A string that ends generation when produced. [5] |
| **Temperature** | A divisor applied to logits before softmax; lower is more focused, higher more varied. [5] |
| **Token** | A chunk of text (a word, part of a word, a symbol) that the model reads and writes as one unit. [2] |
| **Tokenizer** | The program that turns text into token IDs and back. [2] |
| **Top-k sampling** | Sampling only from the k most likely tokens. [5] |
| **Top-p (nucleus) sampling** | Sampling only from the smallest set of top tokens whose probabilities reach p. [5] |
| **Transformer** | The neural-network architecture behind modern LLMs, built from attention and feed-forward layers. [4] |
| **Vector** | A list of numbers; here, a point in a many-dimensional space. [3] |
| **Vocabulary** | The fixed set of tokens a tokenizer can produce, each with an integer ID. [2] |
