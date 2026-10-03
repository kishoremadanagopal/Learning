@@ messages-api
topics: the anatomy of a request (model, max tokens, system prompt, messages), content blocks, the response and its content blocks, stop reasons, token usage, stateless APIs, storing and resending conversation history, trimming and summarising history, mid-conversation system messages, other providers' APIs and multi-provider libraries, keeping API keys safe
terms:
- **API key:** the secret that identifies your account to the provider; keep it in an environment variable or a secrets manager.
- **System prompt:** instructions and context that apply to the whole conversation.
- **Message:** one turn in the conversation, with a role (`user` or `assistant`) and content.
- **Content block:** one typed piece of a message: text, image, document, tool call, tool result or thinking.
- **Stop reason:** why the model stopped generating, such as `end_turn`, `max_tokens` or `tool_use`.
- **Usage:** the input and output token counts the response reports, which determine its cost.
- **Stateless API:** one that remembers nothing between calls, so each request carries the full history.
mistakes:
- Reading only `content[0].text` when the reply may begin with thinking or a tool call.
- Ignoring the stop reason and treating a cut-off reply as complete.
- Committing an API key to a repository.
- Letting the history grow forever until requests become slow, costly or too long.
- Starting a trimmed history with an assistant turn.

glance:
- Get the reply text | join the text blocks; skip other types | O(reply length) | O(reply length)
- Keep history in budget | walk newest to oldest within a token budget; start with a user turn | O(n) | O(n)
- Long-running chats | trim, summarise older turns, cache the prefix | — | —

@@ streaming-and-retries
topics: server-sent events, stream event types, text and JSON deltas, assembling a streamed message, SDK streaming helpers, HTTP status codes and error types, which errors to retry, exponential backoff, jitter, retry-after, timeouts, SDK automatic retries, request IDs, fallbacks to another model or provider
terms:
- **Streaming:** receiving the response as a series of events while the model generates it.
- **Server-sent events (SSE):** the web standard used to push the stream of events over one HTTP response.
- **Delta:** an event carrying the next small piece of a content block.
- **Transient error:** a temporary failure, such as a rate limit or an overloaded server, that may succeed on retry.
- **Exponential backoff:** waiting twice as long after each failed attempt, up to a cap.
- **Jitter:** a random amount added to (or taken from) the wait so that clients don't retry in sync.
- **Retry-after:** a response header telling the client how long to wait before trying again.
- **Request ID:** the identifier of one API call, for debugging and support.
mistakes:
- Retrying permanent errors such as 400 or 401.
- Retrying immediately in a tight loop instead of backing off.
- Ignoring the server's retry-after value.
- Retrying without a limit, so a failure turns into a hang.
- Logging API keys or full sensitive prompts instead of request IDs and metadata.

glance:
- Assemble a stream | append each text delta to its block; read stop reason from message_delta | O(events) | O(text length)
- Retry decision | retryable status and attempts left | O(1) | O(1)
- Backoff delay | min(cap, base × 2^(attempt − 1)), at least retry-after, plus jitter | O(1) | O(1)

@@ structured-output
topics: why programs need structured data, asking for JSON in the prompt, defensive parsing, JSON Schema, constrained decoding and guaranteed structured outputs, output_config format, Pydantic models with the SDK, schema limitations, strict tool use, validating values, retrying with error feedback, designing schemas with descriptions, enums and nullable fields
terms:
- **JSON:** a text format for data made of objects, arrays, strings, numbers, booleans and null.
- **JSON Schema:** a standard way to describe the allowed structure and types of JSON data.
- **Structured outputs:** an API feature that guarantees the reply matches a given schema.
- **Constrained decoding:** restricting which tokens the model may generate so the output always fits a grammar or schema.
- **Pydantic:** a Python library that defines data models with type hints and validates data against them.
- **Validation:** checking that data has the required fields, types and allowed values.
- **Enum:** a fixed list of allowed values for a field.
mistakes:
- Calling `json.loads` on a raw reply that may include a code fence or extra text.
- Trusting values just because the format is guaranteed.
- Forgetting that `bool` is a subclass of `int` in Python type checks.
- Requiring a value the input may not contain, which invites the model to invent one.
- Retrying invalid output forever instead of a fixed number of times.

glance:
- Parse JSON from a reply | slice first { to last }; json.loads; catch errors | O(n) | O(n)
- Validate a record | check each schema field, then extra fields | O(fields) | O(problems)
- Reliable structure | structured outputs, then validate values, then retry with feedback | — | —

@@ reasoning-and-multimodal
topics: reasoning models, adaptive thinking, the effort parameter, thinking tokens and billing, max tokens and thinking, thinking display options, passing thinking blocks back, model differences, image content blocks, supported image formats and limits, estimating image tokens, the Files API, PDF document blocks, how PDFs are processed, vision limitations
terms:
- **Reasoning model:** a model that can generate intermediate reasoning (thinking) before its answer.
- **Adaptive thinking:** the model decides per request whether and how much to think.
- **Effort:** a setting that trades quality for speed and cost across all output tokens.
- **Thinking block:** a content block holding the model's reasoning (or an omitted or summarised form of it).
- **Base64:** a way to encode binary data such as images as text, about a third larger than the original.
- **Media type:** the standard label for a file format, such as `image/png` or `application/pdf`.
- **Document block:** a content block carrying a PDF or other document.
mistakes:
- Setting `max_tokens` too low for a thinking model, so the answer never arrives.
- Assuming hidden thinking is free.
- Editing or dropping thinking blocks when sending a conversation back.
- Sending huge images when a smaller version would do.
- Relying on precise counts, positions or tiny text read from an image without checking.

glance:
- Image token estimate | scale to the maximum edge; ceil(w ÷ 28) × ceil(h ÷ 28); cap | O(1) | O(1)
- Build a multimodal message | files as blocks first, question text last | O(total bytes) | O(total bytes)
- Choose effort | start at the default; lower it while evaluations hold | — | —

@@ cost-and-caching
topics: where the cost of an LLM application comes from, reading usage fields, cache write and read prices, prompt caching and prefix matching, automatic caching and explicit breakpoints, cache lifetimes, minimum cacheable length, what invalidates the cache, the Message Batches API, matching batch results, token counting, routing, effort, output length and other cost levers
terms:
- **Prompt caching:** storing a processed prompt prefix so later requests with the same prefix are cheaper and faster.
- **Prefix:** the beginning of a request (tools, system prompt, early messages) that stays the same across calls.
- **Cache breakpoint:** the point in a request up to which content is cached.
- **Cache write and cache read:** storing a prefix (slightly dearer than normal input) and reusing it (much cheaper).
- **TTL (time to live):** how long a cached prefix lasts without being used.
- **Batch API:** submitting many requests for asynchronous processing at a discount.
- **Custom ID:** your label on each batch request, used to match results back to requests.
mistakes:
- Putting a timestamp or other changing text at the start of a prompt, so the cache never hits.
- Caching prefixes shorter than the minimum length and expecting savings.
- Paying for a one-hour cache on a prefix used only once or twice.
- Assuming batch results come back in the same order as the requests.
- Optimising cost without logging usage to find the biggest line on the bill.

glance:
- Call cost | sum of each token type × its price, per million | O(1) | O(1)
- Caching saving | calls × 1 − (write + (calls − 1) × read), × tokens × price | O(1) | O(1)
- Offline bulk work | Batch API at half price; match results by custom_id | O(requests) | O(requests)
