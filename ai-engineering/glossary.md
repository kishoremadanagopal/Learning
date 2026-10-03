# AI engineering glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Adaptive thinking** | The model decides per request whether and how much to think. [10] |
| **API key** | The secret that identifies your account to the provider; keep it in an environment variable or a secrets manager. [7] |
| **Attention head** | One of several attention mechanisms run in parallel in a layer. [4] |
| **Bag of words** | A vector of word counts; matches identical words but not meaning. [3] |
| **Base64** | A way to encode binary data such as images as text, about a third larger than the original. [10] |
| **Batch API** | Submitting many requests for asynchronous processing at a discount. [11] |
| **Byte-pair encoding (BPE)** | Building a vocabulary by repeatedly merging the most frequent neighbouring pair of symbols. [2] |
| **Cache breakpoint** | The point in a request up to which content is cached. [11] |
| **Cache write and cache read** | Storing a prefix (slightly dearer than normal input) and reusing it (much cheaper). [11] |
| **Causal mask** | Prevents a token from attending to later tokens during text generation. [4] |
| **Constrained decoding** | Restricting which tokens the model may generate so the output always fits a grammar or schema. [9] |
| **Content block** | One typed piece of a message: text, image, document, tool call, tool result or thinking. [7] |
| **Context window** | The maximum number of tokens (input plus output) a model can handle in one request. [2] |
| **Cosine similarity** | The dot product divided by both vectors' lengths: how closely two vectors point the same way. [3] |
| **Custom ID** | Your label on each batch request, used to match results back to requests. [11] |
| **Delta** | An event carrying the next small piece of a content block. [8] |
| **Document block** | A content block carrying a PDF or other document. [10] |
| **Dot product** | The sum of the products of matching coordinates. [3] |
| **Effort** | A setting that trades quality for speed and cost across all output tokens. [10] |
| **Embedding** | A vector produced by a model so that similar meanings get similar vectors. [3] |
| **Enum** | A fixed list of allowed values for a field. [9] |
| **Evaluation set** | Representative examples with known good answers, used to compare models on your task. [6] |
| **Exponential backoff** | Waiting twice as long after each failed attempt, up to a cap. [8] |
| **Foundation model** | One general model adapted to many tasks through prompts, data and tools. [1] |
| **Greedy decoding** | Always choosing the single most likely token. [5] |
| **Hallucination** | A fluent, confident output that is false or unsupported. [1] |
| **Hosted model** | A model you use through a provider's API or a cloud platform. [6] |
| **Input and output tokens** | Tokens sent to the model and tokens it generates; priced separately. [2] |
| **Instruction tuning (supervised fine-tuning)** | Training on examples of instructions and good responses. [1] |
| **Jitter** | A random amount added to (or taken from) the wait so that clients don't retry in sync. [8] |
| **JSON** | A text format for data made of objects, arrays, strings, numbers, booleans and null. [9] |
| **JSON Schema** | A standard way to describe the allowed structure and types of JSON data. [9] |
| **Knowledge cutoff** | The date after which a model has no training data. [1] |
| **KV cache** | Stored keys and values of earlier tokens, reused while generating each new token. [4] |
| **Large language model (LLM)** | A neural network trained on huge amounts of text to predict the next token. [1] |
| **Latency** | How long a response takes; often split into time to first token and tokens per second. [6] |
| **Logit** | The raw score the model gives each vocabulary token before softmax. [4] |
| **Max tokens** | The limit on how many tokens a response may contain. [5] |
| **Media type** | The standard label for a file format, such as `image/png` or `application/pdf`. [10] |
| **Message** | One turn in the conversation, with a role (`user` or `assistant`) and content. [7] |
| **Model tier** | A provider's range from large and capable to small, fast and cheap models. [6] |
| **Nearest-neighbour search** | Finding the stored vectors most similar to a query vector. [3] |
| **Next-token prediction** | Generating text one token at a time, each chosen from the model's predicted probabilities. [1] |
| **Normalised vector** | A vector scaled to length 1. [3] |
| **Open-weight model** | A model whose trained weights can be downloaded and run on your own hardware. [6] |
| **Prefix** | The beginning of a request (tools, system prompt, early messages) that stays the same across calls. [11] |
| **Pretraining** | The first training stage: predicting the next token on a vast text corpus. [1] |
| **Prompt caching** | Storing a processed prompt prefix so later requests with the same prefix are cheaper and faster. [11] |
| **Pydantic** | A Python library that defines data models with type hints and validates data against them. [9] |
| **Query, key, value** | Per-token vectors used by attention: what a token seeks, what it offers to match, and what it passes on. [4] |
| **Reasoning model** | A model that can generate intermediate reasoning (thinking) before its answer. [10] |
| **Reinforcement learning from feedback** | Improving a model by rewarding preferred or verifiably correct responses. [1] |
| **Request ID** | The identifier of one API call, for debugging and support. [8] |
| **Retry-after** | A response header telling the client how long to wait before trying again. [8] |
| **Routing** | Sending each request to a model chosen for its difficulty or type. [6] |
| **Sampling** | Choosing the next token at random according to the model's probabilities. [5] |
| **Self-attention** | Each token computing a weighted mix of other tokens' information. [4] |
| **Server-sent events (SSE)** | The web standard used to push the stream of events over one HTTP response. [8] |
| **Softmax** | Turns a list of scores into probabilities that sum to 1. [4] |
| **Stateless API** | One that remembers nothing between calls, so each request carries the full history. [7] |
| **Stop reason** | Why the model stopped generating, such as `end_turn`, `max_tokens` or `tool_use`. [7] |
| **Stop sequence** | A string that ends generation when produced. [5] |
| **Streaming** | Receiving the response as a series of events while the model generates it. [8] |
| **Structured outputs** | An API feature that guarantees the reply matches a given schema. [9] |
| **System prompt** | Instructions and context that apply to the whole conversation. [7] |
| **Temperature** | A divisor applied to logits before softmax; lower is more focused, higher more varied. [5] |
| **Thinking block** | A content block holding the model's reasoning (or an omitted or summarised form of it). [10] |
| **Token** | A chunk of text (a word, part of a word, a symbol) that the model reads and writes as one unit. [2] |
| **Tokenizer** | The program that turns text into token IDs and back. [2] |
| **Top-k sampling** | Sampling only from the k most likely tokens. [5] |
| **Top-p (nucleus) sampling** | Sampling only from the smallest set of top tokens whose probabilities reach p. [5] |
| **Transformer** | The neural-network architecture behind modern LLMs, built from attention and feed-forward layers. [4] |
| **Transient error** | A temporary failure, such as a rate limit or an overloaded server, that may succeed on retry. [8] |
| **TTL (time to live)** | How long a cached prefix lasts without being used. [11] |
| **Usage** | The input and output token counts the response reports, which determine its cost. [7] |
| **Validation** | Checking that data has the required fields, types and allowed values. [9] |
| **Vector** | A list of numbers; here, a point in a many-dimensional space. [3] |
| **Vocabulary** | The fixed set of tokens a tokenizer can produce, each with an integer ID. [2] |
