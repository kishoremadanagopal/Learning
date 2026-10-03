# AI engineering glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Abstention** | The model declining to answer when it lacks the information. [30] |
| **Adaptive thinking** | The model decides per request whether and how much to think. [10] |
| **Agent** | A system where a model decides its next action in a loop, using tools and feedback. [24] |
| **Agent loop** | Call the model, run any requested tools, append the results, repeat until it stops. [24] |
| **Allow-list** | A list of things explicitly permitted; everything else is refused. [16] |
| **API key** | The secret that identifies your account to the provider; keep it in an environment variable or a secrets manager. [7] |
| **Approximate nearest-neighbour (ANN) search** | An index that finds nearly the best matches while scoring only some vectors. [20] |
| **Attention head** | One of several attention mechanisms run in parallel in a layer. [4] |
| **Audit log** | A record of every action, its arguments, result and approval. [27] |
| **Bag of words** | A vector of word counts; matches identical words but not meaning. [3] |
| **Base64** | A way to encode binary data such as images as text, about a third larger than the original. [10] |
| **Batch API** | Submitting many requests for asynchronous processing at a discount. [11] |
| **Bi-encoder** | A model that embeds query and document separately; fast and precomputable. [21] |
| **BM25** | A ranking formula combining IDF, saturated term frequency and document-length normalisation. [19] |
| **Byte-pair encoding (BPE)** | Building a vocabulary by repeatedly merging the most frequent neighbouring pair of symbols. [2] |
| **Cache breakpoint** | The point in a request up to which content is cached. [11] |
| **Cache write and cache read** | Storing a prefix (slightly dearer than normal input) and reusing it (much cheaper). [11] |
| **Causal mask** | Prevents a token from attending to later tokens during text generation. [4] |
| **Chain-of-thought (CoT)** | Prompting a model to write out its reasoning before the answer. [14] |
| **Chain-of-verification** | Drafting, generating verification questions, answering them independently, then revising. [30] |
| **Chunk** | A passage of a document, the unit that is indexed and retrieved. [17] |
| **Chunk header** | The title and section path prepended to a chunk's text. [18] |
| **Chunk size** | How much text goes in each chunk, usually measured in tokens. [18] |
| **Citation** | A reference from a statement in the answer to the source that supports it. [17] |
| **Client tool** | A tool your application executes. [23] |
| **Cohen's kappa** | Agreement between two graders, corrected for agreement expected by chance. [29] |
| **Compaction** | Replacing older conversation turns with a summary. [26] |
| **Constrained decoding** | Restricting which tokens the model may generate so the output always fits a grammar or schema. [9] |
| **Content block** | One typed piece of a message: text, image, document, tool call, tool result or thinking. [7] |
| **Context editing** | Automatically clearing old tool results or thinking from the history. [26] |
| **Context engineering** | Choosing what information goes into the model's context at each step. [26] |
| **Context rot** | Degraded recall and reasoning as the context grows long and noisy. [26] |
| **Contextual retrieval** | Prepending a short model-written context to each chunk before indexing it. [18] |
| **Context window** | The maximum number of tokens (input plus output) a model can handle in one request. [2] |
| **Corpus** | The whole collection of documents you search. [17] |
| **Cosine similarity** | The dot product divided by both vectors' lengths: how closely two vectors point the same way. [3] |
| **Cross-encoder (reranker)** | A model that reads query and document together and scores their relevance. [21] |
| **Custom ID** | Your label on each batch request, used to match results back to requests. [11] |
| **Data leakage** | Test examples (or near-copies) appearing in the training data. [33] |
| **Delta** | An event carrying the next small piece of a content block. [8] |
| **Direct preference optimisation (DPO)** | Training on pairs of better and worse responses. [33] |
| **Distillation** | Training a smaller model to imitate a larger model on a task. [33] |
| **Document block** | A content block carrying a PDF or other document. [10] |
| **Dot product** | The sum of the products of matching coordinates. [3] |
| **Dry run** | Producing the plan of changes without applying them. [27] |
| **Effort** | A setting that trades quality for speed and cost across all output tokens. [10] |
| **Embedding** | A vector produced by a model so that similar meanings get similar vectors. [3] |
| **Enum** | A fixed list of allowed values for a field. [9] |
| **Eval (evaluation)** | A repeatable measurement of how well an AI system performs on a set of cases. [28] |
| **Evaluation set** | Representative examples with known good answers, used to compare models on your task. [6, 22] |
| **Evaluator-optimiser** | One model producing and another critiquing, in a loop. [24] |
| **Exact (brute-force) search** | Scoring every vector; perfectly accurate, linear in the corpus size. [20] |
| **Excessive agency** | An AI system having more tools, permissions or autonomy than its task needs. [27] |
| **Exfiltration** | Sending data out to an attacker, for example inside a URL. [16] |
| **Exponential backoff** | Waiting twice as long after each failed attempt, up to a cap. [8] |
| **Faithfulness** | Agreement between an answer and the sources it was given. [30] |
| **Faithfulness (groundedness)** | Whether every claim in an answer is supported by the retrieved context. [22] |
| **Fallback** | An alternative model, provider or non-AI path used when the primary fails. [32] |
| **Few-shot** | A prompt that includes a few input and output examples. [13] |
| **Fine-tuning** | Further training of a pretrained model on your own examples. [33] |
| **Foundation model** | One general model adapted to many tasks through prompts, data and tools. [1] |
| **Gate** | A code check between steps of a chain that can stop it. [14] |
| **Grader** | Code, a model or a person that scores a trial. [28] |
| **Greedy decoding** | Always choosing the single most likely token. [5] |
| **Grounding** | Basing an answer on quoted evidence from the provided documents. [13, 17] |
| **Hallucination** | A fluent, confident output that is false or unsupported. [1, 30] |
| **HNSW** | A layered graph of neighbouring vectors, searched by greedy walks. [20] |
| **Hosted model** | A model you use through a provider's API or a cloud platform. [6] |
| **Human in the loop** | A person approving or reviewing consequential actions. [27] |
| **Hybrid search** | Running keyword and vector search and merging their results. [21] |
| **HyDE** | Searching with the embedding of a model-written hypothetical answer. [21] |
| **Indirect prompt injection** | Injected instructions hidden in content the model reads, such as a web page or email. [16] |
| **Ingestion** | Loading, cleaning, chunking and indexing documents ahead of time. [17] |
| **Input and output tokens** | Tokens sent to the model and tokens it generates; priced separately. [2] |
| **Instruction tuning (supervised fine-tuning)** | Training on examples of instructions and good responses. [1] |
| **Inverse document frequency (IDF)** | A weight that is high for words found in few documents. [19] |
| **Inverted index** | A map from each word to the documents (and often positions) where it appears. [19] |
| **IVF (inverted file index)** | Vectors grouped into buckets around centroids; a query searches the nearest buckets. [20] |
| **Jailbreak** | A prompt crafted to get around a model's safety training. [16] |
| **Jitter** | A random amount added to (or taken from) the wait so that clients don't retry in sync. [8] |
| **JSON** | A text format for data made of objects, arrays, strings, numbers, booleans and null. [9] |
| **JSON-RPC 2.0** | The request-response message format MCP uses. [25] |
| **JSON Schema** | A standard way to describe the allowed structure and types of JSON data. [9] |
| **Just-in-time context** | Loading information through tools only when it's needed. [26] |
| **Knowledge cutoff** | The date after which a model has no training data. [1] |
| **KV cache** | Stored keys and values of earlier tokens, reused while generating each new token. [4] |
| **Large language model (LLM)** | A neural network trained on huge amounts of text to predict the next token. [1] |
| **Latency** | How long a response takes; often split into time to first token and tokens per second. [6] |
| **Least privilege** | Giving a component only the access it needs. [16] |
| **Lemmatisation** | Mapping words to their dictionary form. [19] |
| **Length (verbosity) bias** | A judge favouring longer answers. [29] |
| **Lethal trifecta** | Private data, untrusted content and external communication in one system. [16] |
| **Linter** | A tool that flags likely problems using simple rules. [12] |
| **LLM as a judge** | Using a model, prompted with a rubric, to grade outputs. [29] |
| **Logit** | The raw score the model gives each vocabulary token before softmax. [4] |
| **Long-term memory** | Information stored outside the model and loaded into later conversations. [26] |
| **LoRA** | A parameter-efficient method that trains small adapter matrices on frozen weights. [33] |
| **Max tokens** | The limit on how many tokens a response may contain. [5] |
| **MCP host** | The application the user works in, which contains MCP clients. [25] |
| **MCP server** | A program exposing tools, resources and prompts from some system. [25] |
| **Mean reciprocal rank (MRR)** | The average of 1 ÷ the rank of the first relevant result. [22] |
| **Media type** | The standard label for a file format, such as `image/png` or `application/pdf`. [10] |
| **Memory tool** | A tool that lets the model create, read and update memory files. [26] |
| **Message** | One turn in the conversation, with a role (`user` or `assistant`) and content. [7] |
| **Min-max normalisation** | Rescaling scores to 0–1 using the list's minimum and maximum. [21] |
| **Model Context Protocol (MCP)** | An open standard for connecting AI applications to tools and data sources. [25] |
| **Model tier** | A provider's range from large and capable to small, fast and cheap models. [6] |
| **nDCG** | A ranking score that rewards relevant results near the top, allowing graded relevance. [22] |
| **Nearest-neighbour search** | Finding the stored vectors most similar to a query vector. [3] |
| **Next-token prediction** | Generating text one token at a time, each chosen from the model's predicted probabilities. [1] |
| **Non-greedy match** | A regex quantifier such as `.*?` that matches as little text as possible. [13] |
| **Normalised vector** | A vector scaled to length 1. [3] |
| **Observability** | Recording enough about each request to explain its behaviour afterwards. [31] |
| **Online evaluation** | Grading a sample of live production traffic. [31] |
| **OpenTelemetry** | An open standard and toolkit for traces, metrics and logs. [31] |
| **Open-weight model** | A model whose trained weights can be downloaded and run on your own hardware. [6] |
| **Orchestrator-workers** | A lead agent splitting a task among sub-agents and combining their results. [24] |
| **Output speed** | How many tokens per second the model generates. [32] |
| **Overlap** | Text repeated at the end of one chunk and the start of the next. [18] |
| **Pairwise judging** | Asking which of two outputs is better. [29] |
| **Parallel tool calls** | Several tool calls requested in one reply. [23] |
| **pass@k** | The probability that at least one of k attempts succeeds. [28] |
| **pass^k** | The probability that all k attempts succeed. [28] |
| **Pass rate** | The fraction of test cases a prompt version passes. [15] |
| **Percentile (p95)** | The value below which that percentage of measurements fall. [32] |
| **Permission policy** | Rules deciding whether each action is allowed, needs approval or is denied. [27] |
| **PII (personally identifiable information)** | Data that identifies a person, such as an email address or phone number. [16] |
| **Placeholder** | A marker in a template, such as `{{review}}`, replaced with a value. [15] |
| **Position bias** | A judge favouring an answer because of where it appears. [29] |
| **Postings list** | The list of documents for one word in an inverted index. [19] |
| **Precision@k** | The share of the top k results that are relevant. [22] |
| **Prefill** | Starting the assistant's reply for it; not supported on the newest Claude models. [12] |
| **Prefix** | The beginning of a request (tools, system prompt, early messages) that stays the same across calls. [11] |
| **Pretraining** | The first training stage: predicting the next token on a vast text corpus. [1] |
| **Prompt** | Everything the model sees for a request: system prompt, conversation, documents and examples. [12] |
| **Prompt caching** | Storing a processed prompt prefix so later requests with the same prefix are cheaper and faster. [11] |
| **Prompt chain** | A pipeline where each model call's output feeds the next prompt. [14] |
| **Prompt engineering** | Designing, testing and refining prompts so a model does a task reliably. [12] |
| **Prompt injection** | Text that makes a model follow instructions its developer didn't intend. [16] |
| **Prompt template** | Fixed prompt text with placeholders filled at run time. [15] |
| **Pydantic** | A Python library that defines data models with type hints and validates data against them. [9] |
| **Quantisation** | Storing numbers with fewer bits to save memory. [20] |
| **Query, key, value** | Per-token vectors used by attention: what a token seeks, what it offers to match, and what it passes on. [4] |
| **Query rewriting** | Turning a question into a better search query, such as a standalone version of a follow-up. [21] |
| **Reasoning model** | A model that can generate intermediate reasoning (thinking) before its answer. [10] |
| **Recall@k** | The share of the true top-k results that a search returns. [20, 22] |
| **Reciprocal rank fusion (RRF)** | Merging ranked lists by summing 1 ÷ (k + rank) for each document. [21] |
| **Recursive splitting** | Splitting on the largest separator first, falling back to smaller ones only when needed. [18] |
| **Refusal accuracy** | Whether the system declines exactly the questions it can't answer from its sources. [22] |
| **Regression** | Something that used to work and broke after a change. [15] |
| **Regression eval** | A suite that should keep passing, run on every change. [28] |
| **Reinforcement fine-tuning (RFT)** | Training that rewards responses a grader scores highly. [33] |
| **Reinforcement learning from feedback** | Improving a model by rewarding preferred or verifiably correct responses. [1] |
| **Request ID** | The identifier of one API call, for debugging and support. [8] |
| **Resource** | Data an MCP server offers for the application to read into context. [25] |
| **Response cache** | Stored answers reused for repeated questions. [32] |
| **Retrieval-augmented generation (RAG)** | Retrieving relevant passages and adding them to the prompt so the model answers from them. [17] |
| **Retriever** | The component that finds the chunks most relevant to a query. [17] |
| **Retry-after** | A response header telling the client how long to wait before trying again. [8] |
| **Role prompt** | A sentence in the system prompt saying who the model is acting as and for whom. [12] |
| **Routing** | Sending each request to a model chosen for its difficulty or type. [6, 14] |
| **Rubric** | The explicit criteria and score definitions a grader applies. [29] |
| **Sampling** | Choosing the next token at random according to the model's probabilities. [5] |
| **Sandbox** | An isolated environment where code can run without access to real systems or secrets. [27] |
| **Scoped credentials** | Access tokens limited to the minimum resources and operations. [27] |
| **Self-attention** | Each token computing a weighted mix of other tokens' information. [4] |
| **Self-consistency check** | Comparing several samples to find details that vary. [30] |
| **Self-consistency (voting)** | Asking several times and taking the most common answer. [14] |
| **Self-preference bias** | A judge favouring outputs from its own model or style. [29] |
| **Self-verification** | Asking the model to check its answer against criteria before finishing. [14] |
| **Semantic cache** | A response cache that matches questions by meaning (embeddings) rather than exact text. [32] |
| **Semantic search** | Finding text by meaning, using embeddings, rather than by shared words. [20] |
| **Server-sent events (SSE)** | The web standard used to push the stream of events over one HTTP response. [8] |
| **Server tool** | A tool the provider executes, such as web search or code execution. [23] |
| **Slopsquatting** | Registering package names that models commonly invent, to trap people who install them. [30] |
| **Small-to-big retrieval** | Matching small chunks but giving the model their larger parent section. [18] |
| **Softmax** | Turns a list of scores into probabilities that sum to 1. [4] |
| **Span** | One timed step of a request, with a name, a parent and attributes. [31] |
| **Stateless API** | One that remembers nothing between calls, so each request carries the full history. [7] |
| **Stemming** | Cutting words to a common root so variants match. [19] |
| **Stop reason** | Why the model stopped generating, such as `end_turn`, `max_tokens` or `tool_use`. [7] |
| **Stop sequence** | A string that ends generation when produced. [5] |
| **Streaming** | Receiving the response as a series of events while the model generates it. [8] |
| **Structure-aware chunking** | Splitting along a document's own structure, such as headings or code functions. [18] |
| **Structured outputs** | An API feature that guarantees the reply matches a given schema. [9] |
| **Supervised fine-tuning (SFT)** | Training on example conversations with ideal responses. [33] |
| **System prompt** | Instructions and context that apply to the whole conversation. [7, 12] |
| **Tail latency** | The slowest requests, measured by p95 and p99. [32] |
| **Task (case)** | One test input with its success criteria. [28] |
| **Temperature** | A divisor applied to logits before softmax; lower is more focused, higher more varied. [5] |
| **Template injection** | User input that contains template syntax and gets expanded when it shouldn't. [15] |
| **Term frequency (TF)** | How often a word appears in a document. [19] |
| **Test set** | A fixed collection of realistic inputs with checks for each. [15] |
| **Thinking block** | A content block holding the model's reasoning (or an omitted or summarised form of it). [10] |
| **Time to first token (TTFT)** | The delay before the first output token arrives. [32] |
| **Token** | A chunk of text (a word, part of a word, a symbol) that the model reads and writes as one unit. [2] |
| **Tokenizer** | The program that turns text into token IDs and back. [2] |
| **Tool definition** | A tool's name, description and JSON Schema for its input. [23] |
| **Tool (function) calling** | The model requesting that your code run a named function with arguments it chooses. [23] |
| **Tool poisoning** | Malicious instructions hidden in a tool's description or results. [25] |
| **tool_result block** | Your reply to a tool call, matched by `tool_use_id`, with the output or an error. [23] |
| **tool_use block** | The part of a reply that names a tool, its arguments and a call id. [23] |
| **Top-k sampling** | Sampling only from the k most likely tokens. [5] |
| **Top-p (nucleus) sampling** | Sampling only from the smallest set of top tokens whose probabilities reach p. [5] |
| **Trace** | The record of one request, made of nested spans. [31] |
| **Transcript (trace)** | The full record of a trial, including tool calls and intermediate steps. [28] |
| **Transformer** | The neural-network architecture behind modern LLMs, built from attention and feed-forward layers. [4] |
| **Transient error** | A temporary failure, such as a rate limit or an overloaded server, that may succeed on retry. [8] |
| **Transport** | How messages travel: stdio for local subprocesses, Streamable HTTP for web services. [25] |
| **Trial** | One attempt at a task; several trials reveal variability. [28] |
| **TTL (time to live)** | How long a cached prefix lasts without being used. [11] |
| **Turn limit** | The maximum number of model calls an agent may make for one task. [24] |
| **Usage** | The input and output token counts the response reports, which determine its cost. [7] |
| **Validation** | Checking that data has the required fields, types and allowed values. [9] |
| **Vector** | A list of numbers; here, a point in a many-dimensional space. [3] |
| **Vector database** | A store for vectors and metadata with indexes for similarity search and filtering. [20] |
| **Vocabulary** | The fixed set of tokens a tokenizer can produce, each with an integer ID. [2] |
| **Waterfall** | A chart of spans on a timeline showing where time was spent. [31] |
| **Workflow** | A fixed sequence of model calls and tools defined by your code. [24] |
| **XML tags** | Named markers such as `<document>…</document>` that separate the parts of a prompt. [13] |
| **Zero-shot** | A prompt with instructions but no examples. [13] |
