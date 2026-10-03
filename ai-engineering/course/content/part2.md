@@@ part
id: 2
title: Working with LLM APIs
level: Beginner
blurb: Calling models from code: the anatomy of a request and response, conversation history, streaming, errors and retries, getting reliable JSON out, reasoning effort, images and documents, and keeping cost down with caching and batches.

@@@ lesson
id: messages-api
title: Requests, responses and conversations
minutes: 24
summary: The anatomy of a model API call (model, max tokens, system prompt, messages, content blocks), the response (content blocks, stop reasons, token usage), why APIs are stateless and how to manage conversation history, and how other providers' APIs compare.
---
Every chat-style model API works the same way at heart: you send a list of **messages** and settings, and get back the model's reply plus some metadata. This lesson uses Anthropic's **Messages API** as the example; other providers differ in names, not in ideas.

### The request

```py-static
import anthropic

client = anthropic.Anthropic()          # reads the ANTHROPIC_API_KEY environment variable

response = client.messages.create(
    model="claude-sonnet-5-5",          # which model
    max_tokens=1024,                    # the most tokens the reply may use
    system="You are a concise assistant for a bike shop.",   # instructions that apply throughout
    messages=[
        {"role": "user", "content": "Do you sell tubeless tyres?"},
    ],
)
print(response.content[0].text)
print(response.stop_reason, response.usage.input_tokens, response.usage.output_tokens)
```

| Field | Meaning |
|---|---|
| `model` | the model to use (Lesson 6) |
| `max_tokens` | a hard cap on output tokens, **including** any thinking tokens; required |
| `system` | the **system prompt**: the role, rules and context for the whole conversation |
| `messages` | the conversation so far, alternating `user` and `assistant` turns, ending with a `user` turn |
| `tools`, `output_config`, … | optional features: tools (Part 5), structured output (Lesson 9), effort (Lesson 10) |

Keep the API key out of your code: put it in an environment variable or a secrets manager, never in a file you commit.

### Content blocks

A message's `content` can be a plain string, or a **list of content blocks** of different types: text, images, documents (PDFs), and in replies, tool calls and thinking. A string is shorthand for one text block.

```python
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "What's wrong with this bike part?"},
        {"type": "image", "source": {"type": "url", "url": "https://example.com/chain.jpg"}},
    ],
}
print([block["type"] for block in message["content"]])
```

### The response

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-5-5",
  "content": [{"type": "text", "text": "Yes! We stock tubeless tyres in…"}],
  "stop_reason": "end_turn",
  "usage": {"input_tokens": 31, "output_tokens": 54}
}
```

The reply's `content` is a list of blocks too, so **don't assume `content[0]` is text**: a reply may start with a thinking block or contain a tool call. Loop over the blocks and pick out the ones you need (the first exercise).

The **stop reason** says why generation ended. Always check it:

| `stop_reason` | Meaning | What to do |
|---|---|---|
| `end_turn` | the model finished naturally | use the reply |
| `max_tokens` | it hit your `max_tokens` cap | the reply is cut off: raise the cap or ask it to continue |
| `stop_sequence` | it produced one of your stop sequences | expected, if you set them |
| `tool_use` | it wants to call a tool | run the tool and send the result back (Part 5) |
| `pause_turn` | a server-side tool loop paused | send the conversation back to let it continue |
| `refusal` | it declined to respond | show a suitable message; don't retry blindly |
| `model_context_window_exceeded` | the conversation filled the context window | trim or summarise the history |

### Conversations: the API remembers nothing

The API is **stateless**. Each request must include the whole conversation you want the model to see. A chat app keeps the history itself and appends each new turn:

```python
class FakeClient:
    """Stands in for a real API client so this runs anywhere: it echoes how much history it received."""
    def create(self, system, messages):
        last = messages[-1]["content"]
        return {"content": [{"type": "text", "text": f"(reply to {last!r}; saw {len(messages)} messages)"}],
                "stop_reason": "end_turn"}

client = FakeClient()
history = []

def chat(user_text):
    history.append({"role": "user", "content": user_text})
    reply = client.create(system="You are helpful.", messages=history)
    text = "".join(b["text"] for b in reply["content"] if b["type"] == "text")
    history.append({"role": "assistant", "content": text})   # store the reply for the next turn
    return text

print(chat("Hi!"))
print(chat("What did I just say?"))
print(len(history), "messages stored")
```

Because every request resends the history, **long conversations get slower and more expensive with every turn**, and eventually hit the context window. Common strategies:

- **Keep only the most recent turns** that fit a token budget (the second exercise).
- **Summarise** older turns into a short paragraph, kept in the system prompt or an early message.
- **Prompt caching** (Lesson 11) makes the repeated prefix much cheaper.
- Store long-term facts outside the conversation and retrieve them when relevant (Parts 4 and 5).

On the newest Claude models you can also add a `{"role": "system", ...}` message **partway through** a conversation to change the instructions from that point on, without disturbing the cached history before it.

### Other providers

The concepts carry over directly. OpenAI's current **Responses API**, for example:

```py-static
from openai import OpenAI

client = OpenAI()                                     # reads OPENAI_API_KEY
response = client.responses.create(
    model="gpt-5.1",                                  # check OpenAI's models page for current names
    instructions="You are a concise assistant for a bike shop.",
    input="Do you sell tubeless tyres?",
)
print(response.output_text)
```

Libraries such as **LiteLLM**, **LangChain** and the cloud platforms (Amazon Bedrock, Google Vertex AI, Azure AI Foundry) wrap many providers behind one interface, which helps when you route between models.

:::exercise Get the text out of a reply
A reply is a dict with a `"content"` list of blocks. Write `reply_text(reply)` returning all the text blocks' `"text"` joined together (in order), ignoring other block types such as `"thinking"` and `"tool_use"`. Return `""` if there are no text blocks.
```python starter
def reply_text(reply):
    pass

reply = {"content": [{"type": "thinking", "thinking": "Let me check…"},
                     {"type": "text", "text": "Yes, "},
                     {"type": "text", "text": "we do."}],
         "stop_reason": "end_turn"}
print(reply_text(reply))   # Yes, we do.
```
```python check
fn = need("reply_text")
test(fn, cases=[
    (({"content": [{"type": "thinking", "thinking": "hmm"}, {"type": "text", "text": "Yes, "}, {"type": "text", "text": "we do."}]},), "Yes, we do.", "thinking then two text blocks"),
    (({"content": [{"type": "text", "text": "Hello"}]},), "Hello", "a single text block"),
    (({"content": []},), "", "no blocks"),
    (({"content": [{"type": "tool_use", "id": "t1", "name": "get_stock", "input": {"sku": "A1"}}]},), "", "only a tool call"),
    (({"content": [{"type": "text", "text": "Checking. "}, {"type": "tool_use", "id": "t1", "name": "x", "input": {}}, {"type": "text", "text": "Done."}]},), "Checking. Done.", "text around a tool call"),
])
```
```python solution
def reply_text(reply):
    return "".join(block["text"] for block in reply["content"] if block["type"] == "text")

reply = {"content": [{"type": "thinking", "thinking": "Let me check…"},
                     {"type": "text", "text": "Yes, "},
                     {"type": "text", "text": "we do."}],
         "stop_reason": "end_turn"}
print(reply_text(reply))
```
hint: The text isn't always in the first block. Look at each block's `"type"`.
hint: Keep the blocks whose type is `"text"` and collect their `"text"` values in order.
hint: `"".join(block["text"] for block in reply["content"] if block["type"] == "text")`.
approach:
1. **Understand:** keep text blocks only, in order, joined with nothing in between; none → "".
2. **Examples:** thinking + two text blocks → the two texts joined.
3. **Brute force:** a loop with a result string: fine.
4. **Pattern:** **filter by type, then join**.
5. **Plan:** a generator over the content list with a type test.
6. **Code and test:** empty content, tool-only replies, text around a tool call.
walkthrough:
**Line by line**

- The generator walks `reply["content"]` in order and keeps only blocks whose `"type"` is `"text"`.
- `"".join(...)` concatenates them; with no text blocks it returns an empty string.
- Other block types (thinking, tool calls) are skipped instead of crashing on a missing `"text"` key.

**Trace** on the example: thinking (skipped), "Yes, " (kept), "we do." (kept) → "Yes, we do."

**Complexity:** O(total text length).

**Common wrong approach:** `reply["content"][0]["text"]`, which fails when the first block is thinking or a tool call, and drops any later text.
:::

:::exercise Keep the history within a budget
Write `trim_history(messages, max_tokens)` returning the **most recent** messages whose total estimated tokens fit within `max_tokens`, using `len(text) // 4` (at least 1) as each message's estimate. The result must **start with a `"user"` message** (drop a leading assistant message if needed), and keep the messages in their original order. If not even the last message fits, return `[]`.
```python starter
def trim_history(messages, max_tokens):
    pass

msgs = [{"role": "user", "content": "a" * 40},       # 10 tokens
        {"role": "assistant", "content": "b" * 40},  # 10 tokens
        {"role": "user", "content": "c" * 20}]       # 5 tokens
print(trim_history(msgs, 16))   # the last user message only: adding the assistant would leave it first
```
```python check
fn = need("trim_history")
_u = lambda n, ch="x": {"role": "user", "content": ch * n}
_a = lambda n, ch="y": {"role": "assistant", "content": ch * n}
_m = [_u(40, "a"), _a(40, "b"), _u(20, "c")]
test(fn, cases=[
    ((_m, 100), _m, "everything fits"),
    ((_m, 25), _m, "exactly fits"),
    ((_m, 16), [_m[2]], "the assistant message can't lead"),
    ((_m, 15), [_m[2]], "only the last message"),
    ((_m, 4), [], "nothing fits"),
    (([_u(4)], 1), [_u(4)], "a tiny message counts as 1 token"),
    (([_u(40), _a(8), _u(8), _a(8), _u(8)], 5), [_u(8)], "room for two, but must start with a user turn"),
    (([_u(40), _a(8), _u(8), _a(8), _u(8)], 10), [_u(8), _a(8), _u(8)], "several recent turns"),
])
```
```python solution
def trim_history(messages, max_tokens):
    kept, used = [], 0
    for message in reversed(messages):                   # newest first
        cost = max(1, len(message["content"]) // 4)
        if used + cost > max_tokens:
            break
        kept.append(message)
        used += cost
    kept.reverse()                                        # back to chronological order
    while kept and kept[0]["role"] != "user":
        kept.pop(0)                                       # the history must start with a user turn
    return kept

msgs = [{"role": "user", "content": "a" * 40},
        {"role": "assistant", "content": "b" * 40},
        {"role": "user", "content": "c" * 20}]
print(trim_history(msgs, 16))
```
hint: Which messages matter most? Start from the end of the list and work backwards.
hint: Add messages from newest to oldest while the running total stays within `max_tokens`; stop at the first one that doesn't fit (keeping a contiguous recent window). Then restore the original order.
hint: After reversing back, drop messages from the front while the first one isn't a `"user"` message.
approach:
1. **Understand:** a contiguous window of the newest messages within the budget; it must begin with a user turn; order preserved.
2. **Examples:** budget 16 → the last user message (5) plus the assistant (10) fits, but the window would start with an assistant turn, so only the user message remains.
3. **Brute force:** try every starting index from the newest backwards: also fine, O(n²) worst case.
4. **Pattern:** **walk backwards accumulating a budget**, then fix the boundary.
5. **Plan:** reversed loop with a running total → reverse → strip leading assistant turns.
6. **Code and test:** everything fits, nothing fits, exactly fits, assistant at the boundary.
walkthrough:
**Line by line**

- Iterating `reversed(messages)` considers the newest messages first, because they matter most for the next reply.
- `break` (not `continue`) keeps the window contiguous: skipping a big message to fit an older one would leave a confusing gap.
- After reversing back to chronological order, leading assistant messages are removed, because the API expects the conversation to start with the user.

**Trace** on budget 10 with tokens [10, 2, 2, 2, 2] (u, a, u, a, u): newest u (2, total 2), a (4), u (6), a (8), then the first u costs 10 → stop. Kept [a, u, a, u] → strip the leading a → [u, a, u].

**Complexity:** O(n).

**Common wrong approach:** keeping the **oldest** messages that fit, which keeps the greeting and loses the question being asked right now.
:::

:::quiz
? What does it mean that the Messages API is stateless?
+ It remembers nothing between calls, so you must send the conversation history each time
- It can't return text
- It only works once per day
= Your application stores and resends the history.
? A reply has stop_reason "max_tokens". What happened?
+ The reply was cut off at your max_tokens limit
- The model finished naturally
- The model wants to call a tool
= Raise the limit, or ask the model to continue.
? Why shouldn't you read only response.content[0].text?
+ The first block may be thinking or a tool call, and later blocks may hold more text
- content is always empty
- The text is in usage instead
= Loop over the blocks and filter by type.
? Why do long chats get more expensive per message?
+ Every request resends the whole history, so input tokens grow with each turn
- The model charges more after ten messages
- Responses get longer automatically
= Trimming, summarising and caching keep it under control.
:::

@@@ lesson
id: streaming-and-retries
title: Streaming, errors and retries
minutes: 24
summary: Streaming responses token by token with server-sent events, assembling a stream into a message, the API's error codes and which are safe to retry, exponential backoff with jitter and retry-after, timeouts, and fallbacks.
---
A model can take seconds (or minutes, for long answers with lots of thinking) to finish. Two things make an application feel good and stay up: **streaming** the answer as it's generated, and handling the **errors** that every busy API sometimes returns.

### Streaming

With streaming, the API sends the response as a series of small **events** (server-sent events, SSE) while the model is still generating. The user sees the first words in well under a second instead of waiting for the whole reply, and long requests don't hit network timeouts.

```py-static
import anthropic

client = anthropic.Anthropic()
with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain tubeless tyres in three sentences."}],
) as stream:
    for text in stream.text_stream:          # text arrives in small pieces
        print(text, end="", flush=True)
    final = stream.get_final_message()       # the complete Message, as a non-streaming call returns
print("\n", final.stop_reason, final.usage.output_tokens)
```

![Two timelines for the same 8-second reply. Without streaming, the user sees nothing until the whole reply arrives at 8 seconds. With streaming, the first words appear after about half a second and the text keeps growing until it finishes at the same 8 seconds](figures/streaming.svg)

Underneath, a stream is a sequence of typed events:

| Event | Carries |
|---|---|
| `message_start` | the message envelope (id, model) with empty content |
| `content_block_start` | the start of a block (text, tool call, thinking) at an index |
| `content_block_delta` | a piece of a block: `text_delta` text, `input_json_delta` partial tool input, `thinking_delta` |
| `content_block_stop` | the end of a block |
| `message_delta` | top-level changes such as the `stop_reason` and cumulative usage |
| `message_stop` | the end of the stream |
| `ping`, `error` | keep-alives, and errors that happen mid-stream |

```python
events = [
    {"type": "message_start", "message": {"id": "msg_1", "content": []}},
    {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Tubeless tyres "}},
    {"type": "ping"},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "seal themselves."}},
    {"type": "content_block_stop", "index": 0},
    {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 6}},
    {"type": "message_stop"},
]

for e in events:
    if e["type"] == "content_block_delta" and e["delta"]["type"] == "text_delta":
        print(e["delta"]["text"], end="", flush=True)     # what the user sees appearing
print()
```

Assembling these events into the final text and stop reason is the first exercise. In practice the SDKs do it for you (`get_final_message()`), but knowing the events helps when you stream to a web page or debug a stream that stopped early.

### Errors

The API returns standard HTTP status codes with a JSON body naming the error type:

| Status | Error type | Retry? |
|---|---|---|
| 400 | `invalid_request_error` | **no**: fix the request (bad parameter, unsupported feature, too many tokens) |
| 401 | `authentication_error` | no: check the API key |
| 403 | `permission_error` | no |
| 404 | `not_found_error` | no: check the model name or endpoint |
| 413 | `request_too_large` | no: send less (the Messages API allows up to 32 MB) |
| 429 | `rate_limit_error` | **yes, after waiting**: honour the `retry-after` header |
| 500 | `api_error` | yes, with backoff |
| 504 | `timeout_error` | yes; for long generations, use streaming instead |
| 529 | `overloaded_error` | yes, with backoff |

Every response carries a `request-id` header (`req_…`); log it, because support needs it to investigate a specific request.

### Retrying with exponential backoff

For temporary failures (429, 5xx, dropped connections), **retry**, but wait longer each time so a struggling service gets room to recover: 1 s, 2 s, 4 s, 8 s… up to a cap. Add random **jitter** so thousands of clients don't all retry at the same instant, and if the server sends `retry-after`, wait at least that long.

![A chart of wait time against attempt number. The capped exponential delay doubles, 1, 2, 4, 8, 16 seconds, then levels off at the 30-second cap. Dots show jittered waits scattered randomly between zero and that curve](figures/backoff.svg)

```python
import random

def backoff_delays(attempts, base=1.0, cap=30.0, seed=0):
    rng = random.Random(seed)
    delays = []
    for attempt in range(attempts):
        exp = min(cap, base * 2 ** attempt)          # exponential growth, capped
        delays.append(round(rng.uniform(0, exp), 2)) # "full jitter": anywhere from 0 to exp
    return delays

print(backoff_delays(6))

class TransientError(Exception):
    pass

def call_with_retries(fn, max_retries=3):
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except TransientError as e:
            if attempt == max_retries:
                raise                                 # give up: let the caller decide
            print(f"attempt {attempt + 1} failed ({e}); retrying")
            # a real version sleeps first: time.sleep(the backoff delay for this attempt)

outcomes = iter([TransientError("529 overloaded"), TransientError("529 overloaded"), "OK: here is the reply"])
def flaky_call():
    result = next(outcomes)
    if isinstance(result, Exception):
        raise result
    return result

print(call_with_retries(flaky_call))
```

The official SDKs already retry connection errors, 429s and 5xx errors **twice by default** with exponential backoff, honouring `retry-after`; set `max_retries` on the client to change that. You still decide what happens when retries run out.

### Designing for failure

- **Timeouts:** set a sensible client timeout; for long outputs, stream (non-streaming SDK calls refuse requests expected to take over 10 minutes).
- **Fallbacks:** if the primary model keeps failing, fall back to another model or provider, or to a non-AI path ("we'll email you the summary").
- **Idempotency:** before retrying an action with side effects (sending an email, charging a card), make sure retrying can't do it twice.
- **Mid-stream errors:** a stream can fail after it started successfully; handle `error` events and partial output.
- **Rate limits** are per organisation and per model, in requests and tokens per minute: smooth out bursts with a queue, and move non-urgent work to batches (Lesson 11).

:::exercise Assemble a stream
Write `assemble(events)` that takes a list of stream event dicts (as in the lesson) and returns a tuple `(text, stop_reason)`: all `text_delta` pieces joined in order, and the `stop_reason` from the `message_delta` event (or `None` if there wasn't one). Ignore every other event type, including `ping` and non-text deltas.
```python starter
def assemble(events):
    pass

events = [
    {"type": "message_start", "message": {"id": "msg_1", "content": []}},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hel"}},
    {"type": "ping"},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "lo!"}},
    {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 2}},
    {"type": "message_stop"},
]
print(assemble(events))   # ('Hello!', 'end_turn')
```
```python check
fn = need("assemble")
_t = lambda s: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": s}}
_md = lambda r: {"type": "message_delta", "delta": {"stop_reason": r}, "usage": {"output_tokens": 3}}
test(fn, key=lambda r: tuple(r) if isinstance(r, (list, tuple)) else r, cases=[
    (([{"type": "message_start", "message": {}}, _t("Hel"), {"type": "ping"}, _t("lo!"), _md("end_turn"), {"type": "message_stop"}],), ("Hello!", "end_turn"), "the example"),
    (([],), ("", None), "an empty stream"),
    (([_t("cut off"), _md("max_tokens")],), ("cut off", "max_tokens"), "a stream stopped by max_tokens"),
    (([_t("Let me check. "), {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"sku\""}}, _md("tool_use")],), ("Let me check. ", "tool_use"), "tool input deltas aren't text"),
    (([{"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "hmm"}}, _t("Done.")],), ("Done.", None), "thinking deltas and no message_delta"),
])
```
```python solution
def assemble(events):
    pieces, stop_reason = [], None
    for event in events:
        kind = event.get("type")
        if kind == "content_block_delta" and event["delta"].get("type") == "text_delta":
            pieces.append(event["delta"]["text"])
        elif kind == "message_delta":
            stop_reason = event["delta"].get("stop_reason", stop_reason)
    return "".join(pieces), stop_reason

events = [
    {"type": "message_start", "message": {"id": "msg_1", "content": []}},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hel"}},
    {"type": "ping"},
    {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "lo!"}},
    {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 2}},
    {"type": "message_stop"},
]
print(assemble(events))
```
hint: Only two event types matter: text deltas and the message delta.
hint: A text piece is in `event["delta"]["text"]` when `event["type"] == "content_block_delta"` and `event["delta"]["type"] == "text_delta"`. The stop reason is in a `message_delta` event's `event["delta"]["stop_reason"]`.
hint: Collect text pieces in a list, join them at the end, and return `("".join(pieces), stop_reason)` with `stop_reason` starting as None.
approach:
1. **Understand:** text deltas in order; the stop reason from message_delta; ignore everything else.
2. **Examples:** "Hel" + "lo!" → "Hello!", "end_turn".
3. **Brute force:** string concatenation in a loop: fine (a list + join is the idiomatic version).
4. **Pattern:** **event dispatch on type** while accumulating state.
5. **Plan:** loop, two branches, return the tuple.
6. **Code and test:** empty stream, tool-input deltas, thinking deltas, no message_delta.
walkthrough:
**Line by line**

- `event.get("type")` reads the event type safely.
- Only `text_delta` deltas are appended; `input_json_delta` (tool input) and `thinking_delta` belong to other blocks.
- The `message_delta` event carries the final `stop_reason`; starting from None covers streams that never sent one.

**Trace** on the example: message_start (ignored), "Hel" (kept), ping (ignored), "lo!" (kept), message_delta → end_turn, message_stop (ignored).

**Complexity:** O(number of events + text length).

**Common wrong approach:** concatenating every delta's content regardless of type, which mixes partial tool JSON and thinking into the visible answer.
:::

:::exercise Should this request be retried?
Write `should_retry(status, attempt, max_retries)` returning `True` if a request that failed with HTTP `status` should be retried: the status must be retryable (429, 500, 504 or 529; not other 4xx errors) **and** `attempt` (the number of attempts already made, starting at 1) must be at most `max_retries`. Then write `wait_seconds(attempt, retry_after=None, base=1.0, cap=30.0)` returning `min(cap, base * 2 ** (attempt - 1))`, or `retry_after` if that's given and larger.
```python starter
def should_retry(status, attempt, max_retries):
    pass

def wait_seconds(attempt, retry_after=None, base=1.0, cap=30.0):
    pass

print(should_retry(529, 1, 2), should_retry(400, 1, 2), should_retry(429, 3, 2))   # True False False
print(wait_seconds(1), wait_seconds(4), wait_seconds(2, retry_after=10))          # 1.0 8.0 10
```
```python check
sr = need("should_retry"); ws = need("wait_seconds")
test(sr, cases=[
    ((529, 1, 2), True, "overloaded, first attempt"),
    ((429, 2, 2), True, "rate limited, still within the limit"),
    ((429, 3, 2), False, "out of retries"),
    ((400, 1, 5), False, "a bad request never gets better"),
    ((401, 1, 5), False, "an authentication error"),
    ((404, 1, 5), False, "not found"),
    ((500, 1, 1), True, "a server error"),
    ((504, 1, 1), True, "a timeout"),
    ((200, 1, 3), False, "success needs no retry"),
])
test(ws, cases=[
    ((1,), 1.0, "first retry"),
    ((4,), 8.0, "doubling each time"),
    ((10,), 30.0, "capped at 30 seconds"),
    ((2, 10), 10, "retry-after is longer"),
    ((3, 1), 4.0, "retry-after is shorter: keep the backoff"),
    ((3, None, 0.5, 30.0), 2.0, "a smaller base"),
])
```
```python solution
RETRYABLE = {429, 500, 504, 529}

def should_retry(status, attempt, max_retries):
    return status in RETRYABLE and attempt <= max_retries

def wait_seconds(attempt, retry_after=None, base=1.0, cap=30.0):
    delay = min(cap, base * 2 ** (attempt - 1))       # 1, 2, 4, 8, ... seconds, capped
    if retry_after is not None and retry_after > delay:
        return retry_after                            # the server asked us to wait longer
    return delay

print(should_retry(529, 1, 2), should_retry(400, 1, 2), should_retry(429, 3, 2))
print(wait_seconds(1), wait_seconds(4), wait_seconds(2, retry_after=10))
```
hint: Which errors can succeed if you simply try again later? Which mean the request itself is wrong?
hint: Retry rate limits (429), server errors (500), timeouts (504) and overload (529). Never retry 400, 401, 403, 404 or 413: the same request will fail again.
hint: `should_retry` is `status in {429, 500, 504, 529} and attempt <= max_retries`. `wait_seconds` computes `min(cap, base * 2 ** (attempt - 1))` and returns `retry_after` instead when it's larger.
approach:
1. **Understand:** retryable statuses only, within the retry budget; exponential delay with a cap, overridden upwards by retry-after.
2. **Examples:** 529 on attempt 1 with 2 retries → True; 400 → False; delay for attempt 4 → 8 s.
3. **Brute force:** a chain of `if` statements: works, a set is clearer.
4. **Pattern:** **classify errors + exponential backoff**.
5. **Plan:** a set of retryable codes; a capped power of two; `max` with retry-after.
6. **Code and test:** each status type, the cap, retry-after shorter and longer.
walkthrough:
**Line by line**

- The set `RETRYABLE` lists the transient failures; set membership is O(1) and easy to read.
- `attempt <= max_retries` allows exactly `max_retries` retries after the first try.
- `base * 2 ** (attempt - 1)` gives 1, 2, 4, 8… for base 1; `min(cap, …)` stops it growing forever.
- `retry-after` is a minimum the server asks for, so it only ever lengthens the wait.

**Trace:** attempts 1–6 with base 1 and cap 30 wait 1, 2, 4, 8, 16, 30 seconds.

**Complexity:** O(1).

**Common wrong approach:** retrying every error, including 400s, which wastes time and money and can trigger more rate limiting. (In production, also add random jitter to the delay.)
:::

:::quiz
? What is the main benefit of streaming a response?
+ Users see the answer appear immediately, and long generations avoid network timeouts
- It makes the model smarter
- It halves the cost
= The total work is the same; the experience and robustness improve.
? Which error should NOT be retried?
+ 400 invalid_request_error
- 429 rate_limit_error
- 529 overloaded_error
= A malformed request fails the same way every time.
? Why add jitter to exponential backoff?
+ So many clients don't all retry at exactly the same moment
- To make retries faster
- To make the delays shorter than the server asked
= Randomising the wait spreads retries out.
? What should you log for every API call to help debugging later?
+ The request-id from the response
- The API key
- Nothing; the provider keeps everything
= Support uses the request ID to find a specific call; never log API keys.
:::

@@@ lesson
id: structured-output
title: Getting reliable JSON out
minutes: 26
summary: Why free-text replies are hard for programs to use, asking for JSON in the prompt and parsing it defensively, JSON Schema, guaranteed structured outputs with output_config and Pydantic, validating values, and retrying when a reply doesn't fit.
---
A person reads a reply; a **program** needs data it can rely on: a dict with the right keys and the right types, every time. Getting there takes three layers: **ask** for the structure, **constrain** the model to it where the API allows, and **validate** what comes back.

### Layer 1: ask for JSON and parse defensively

The simplest approach is to describe the format in the prompt and parse the reply. It works most of the time, but models sometimes wrap the JSON in a Markdown code fence or add a sentence before it, so parse defensively:

```python
import json

fence = "`" * 3                                     # a Markdown code fence
reply = f"""Here's the product:
{fence}json
{{"name": "Trail tyre 29x2.4", "price": 54.99, "in_stock": true}}
{fence}"""
print(reply)

start, end = reply.find("{"), reply.rfind("}")      # the outermost braces
data = json.loads(reply[start:end + 1])
print(data["name"], data["price"], type(data["in_stock"]).__name__)
```

JSON has its own spellings: `true`, `false` and `null` become Python's `True`, `False` and `None`, and every key is a string. `json.loads` raises `json.JSONDecodeError` (a subclass of `ValueError`) when the text isn't valid JSON, so always be ready to catch it. The first exercise builds a robust parser.

### Layer 2: constrain the output with a schema

**JSON Schema** is the standard way to describe the shape of JSON data: which fields exist, their types, which are required.

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
        "in_stock": {"type": "boolean"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["name", "price", "in_stock", "tags"],
    "additionalProperties": False,
}
print("fields:", list(schema["properties"]))
print("all required:", set(schema["required"]) == set(schema["properties"]))
```

Most providers can **guarantee** that the reply matches a schema: they restrict which tokens the model may generate at each step (constrained decoding), so the output always parses. With Claude, pass the schema in `output_config`:

```py-static
import json
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract the product: 'Trail tyre 29x2.4, £54.99, in stock, tubeless-ready.'"}],
    output_config={"format": {"type": "json_schema", "schema": schema}},
)
text = next(block.text for block in response.content if block.type == "text")
product = json.loads(text)        # guaranteed to parse and match the schema
```

The SDK can build the schema from a **Pydantic** model and hand you a parsed object back:

```py-static
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    tags: list[str]

response = client.messages.parse(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract the product: 'Trail tyre 29x2.4, £54.99, in stock, tubeless-ready.'"}],
    output_format=Product,
)
product = response.parsed_output   # a Product instance
print(product.price)
```

Things to know about guaranteed structured outputs:

- Not every JSON Schema feature is supported (for Claude, for example: no recursive schemas, no numeric ranges or string-length limits, and objects need `"additionalProperties": false`). The SDK adapts Pydantic models for you; check the docs for the current list.
- The format is guaranteed, **the values are not**. The model can still put the wrong price in a perfectly valid field.
- If the reply stops early (`stop_reason` is `max_tokens`) or the model refuses (`refusal`), the output may not match. Check the stop reason first.
- For tools (Part 5), `"strict": true` on a tool definition gives the same guarantee for the tool's arguments.
- Other providers have the same idea under names like *structured outputs* or *JSON mode*; JSON mode alone only guarantees valid JSON, not your schema.

### Layer 3: validate the values, and retry

Validation catches what the schema can't express: a negative price, an unknown category, an end date before a start date. Pydantic does type checks and lets you add your own rules; for simple cases a few lines of Python are enough (the second exercise). When validation fails, a common pattern is to **send the errors back** and ask the model to fix its answer, a limited number of times:

```python
import json

class FakeModel:
    """Returns a bad answer first, then a corrected one: enough to show the loop."""
    def __init__(self):
        self.replies = ['{"name": "Trail tyre", "price": "54.99"}',
                        '{"name": "Trail tyre", "price": 54.99}']
    def ask(self, messages):
        return self.replies.pop(0)

def problems(data):
    errors = []
    if not isinstance(data.get("name"), str):
        errors.append("name should be a string")
    if isinstance(data.get("price"), bool) or not isinstance(data.get("price"), (int, float)):
        errors.append("price should be a number")
    return errors

def extract(model, text, attempts=3):
    messages = [{"role": "user", "content": f"Return JSON with name and price for: {text}"}]
    for _ in range(attempts):
        reply = model.ask(messages)
        try:
            data = json.loads(reply)
            errors = problems(data)
        except json.JSONDecodeError as e:
            errors = [f"invalid JSON: {e}"]
        if not errors:
            return data
        print("retrying because:", errors)
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": "Please fix: " + "; ".join(errors)}]
    raise ValueError("no valid answer after retries")

print(extract(FakeModel(), "Trail tyre 29x2.4, £54.99"))
```

Design tips that make structured output more accurate:

- **Name fields clearly** and add a `description` to each property in the schema; the model reads them.
- Use **enums** (`{"enum": ["road", "gravel", "mtb"]}`) for categories, so the model can't invent new ones.
- Allow `null` (or an `"unknown"` option) for information that may be missing; otherwise the model is pushed to make something up.
- Put a free-text `"reasoning"` field **before** the answer fields if you want the model to think first; later fields are generated after earlier ones.

:::exercise Parse a JSON reply
Write `parse_json_reply(text)` that returns the **dict** in a model's reply, or `None` if there isn't a valid one. The reply may:

- be plain JSON,
- be wrapped in a Markdown code fence (three backticks, optionally followed by `json`),
- have extra text before or after the JSON.

Take the text from the first `{` to the last `}` and parse it with `json.loads`. Return `None` if there are no braces, the text isn't valid JSON, or the result isn't a dict.
```python starter
import json

def parse_json_reply(text):
    pass

print(parse_json_reply('Sure! {"name": "Bell", "price": 12.5} Hope that helps.'))
print(parse_json_reply("Sorry, I can't find a product in that text."))   # None
```
```python check
import json
fn = need("parse_json_reply")
_fence = "```"
test(fn, cases=[
    (('{"a": 1}',), {"a": 1}, "plain JSON"),
    (('Sure! {"name": "Bell", "price": 12.5} Hope that helps.',), {"name": "Bell", "price": 12.5}, "text around it"),
    ((_fence + 'json\n{"ok": true, "n": null}\n' + _fence,), {"ok": True, "n": None}, "a json code fence"),
    ((_fence + '\n{"tags": ["a", "b"]}\n' + _fence,), {"tags": ["a", "b"]}, "a plain code fence"),
    (('{"outer": {"inner": 2}}',), {"outer": {"inner": 2}}, "nested objects"),
    (("Sorry, I can't find a product.",), None, "no JSON at all"),
    (('{"name": "Bell", "price": }',), None, "invalid JSON"),
    (("} oops {",), None, "braces in the wrong order"),
    (('[1, 2] and {"a"',), None, "not a complete object"),
    (("",), None, "empty reply"),
])
```
```python solution
import json

def parse_json_reply(text):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end < start:
        return None
    try:
        data = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None

print(parse_json_reply('Sure! {"name": "Bell", "price": 12.5} Hope that helps.'))
print(parse_json_reply("Sorry, I can't find a product in that text."))
```
hint: `text.find("{")` gives the first index of `{` (or -1); `text.rfind("}")` gives the last index of `}`.
hint: Slice from the first `{` to the last `}` **inclusive** (`end + 1`), and handle the cases where either is missing or they're in the wrong order. The fence and any extra text are outside the slice, so they disappear.
hint: Wrap `json.loads` in `try` / `except json.JSONDecodeError: return None`, then check `isinstance(data, dict)`.
approach:
1. **Understand:** find the JSON object inside surrounding noise; anything unusable gives `None` rather than an exception.
2. **Examples:** a fenced reply → the slice between the braces is exactly the object.
3. **Brute force:** try `json.loads` on every substring: very slow and unnecessary.
4. **Pattern:** **locate, slice, parse, check** (defensive parsing).
5. **Plan:** `find` / `rfind` → guard → `try json.loads` → type check.
6. **Code and test:** no braces, reversed braces, invalid JSON, nested objects.
walkthrough:
**Line by line**

- `find("{")` and `rfind("}")` take the **outermost** braces, so nested objects stay intact and any fence or chatter outside them is dropped.
- `end < start` covers text like `} oops {`, and `start == -1` covers replies with no object at all.
- `json.JSONDecodeError` is what `json.loads` raises on bad input; catching only that keeps real bugs visible.
- The final `isinstance` check makes the function's promise simple: a dict or `None`.

**Trace** on the code-fence case: the first `{` is just after the `json` line, the last `}` just before the closing fence; the slice is `{"ok": true, "n": null}` → `{"ok": True, "n": None}`.

**Complexity:** O(n) for a reply of length n.

**Common wrong approach:** `json.loads(text)` on the raw reply, which crashes whenever the model adds a fence or a friendly sentence. (With guaranteed structured outputs you can parse directly, but defensive parsing is still useful for other providers and older models.)
:::

:::exercise Validate a record
Write `validate(record, schema)` returning a **list of problems** (empty if the record is fine). `schema` maps each required field to a Python type: `str`, `int`, `float`, `bool` or `list`. Report, in this order:

1. For each field in the schema (in schema order): `"missing <field>"` if absent, or `"<field> should be <type name>"` if the value has the wrong type.
2. Then for each field in the record that isn't in the schema (in record order): `"unexpected <field>"`.

Two JSON details: a `float` field also accepts an `int` (JSON doesn't distinguish `5` from `5.0`), and `True`/`False` are **not** valid for `int` or `float` fields (in Python, `bool` is a subclass of `int`).
```python starter
def validate(record, schema):
    pass

schema = {"name": str, "price": float, "in_stock": bool}
print(validate({"name": "Bell", "price": 12, "in_stock": True}, schema))   # []
print(validate({"name": "Bell", "price": "12", "colour": "red"}, schema))
# ['price should be float', 'missing in_stock', 'unexpected colour']
```
```python check
fn = need("validate")
_s = {"name": str, "price": float, "in_stock": bool}
test(fn, cases=[
    (({"name": "Bell", "price": 12.5, "in_stock": True}, _s), [], "a valid record"),
    (({"name": "Bell", "price": 12, "in_stock": False}, _s), [], "an int is fine for a float field"),
    (({"name": "Bell", "price": "12", "colour": "red"}, _s), ["price should be float", "missing in_stock", "unexpected colour"], "wrong type, missing and extra"),
    (({"name": "Bell", "price": True, "in_stock": True}, _s), ["price should be float"], "a bool is not a number"),
    (({"qty": True}, {"qty": int}), ["qty should be int"], "a bool is not an int"),
    (({"qty": 2.0}, {"qty": int}), ["qty should be int"], "a float is not an int"),
    (({"in_stock": 1}, {"in_stock": bool}), ["in_stock should be bool"], "1 is not a bool"),
    (({}, _s), ["missing name", "missing price", "missing in_stock"], "an empty record"),
    (({"tags": ["a"], "z": 1, "a": 2}, {"tags": list}), ["unexpected z", "unexpected a"], "extras in record order"),
    (({"tags": "a,b"}, {"tags": list}), ["tags should be list"], "a string is not a list"),
    (({"name": None}, {"name": str}), ["name should be str"], "null is not a string"),
])
```
```python solution
def validate(record, schema):
    problems = []
    for field, kind in schema.items():
        if field not in record:
            problems.append(f"missing {field}")
            continue
        value = record[field]
        if kind is float:
            ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        elif kind is int:
            ok = isinstance(value, int) and not isinstance(value, bool)
        else:
            ok = isinstance(value, kind)
        if not ok:
            problems.append(f"{field} should be {kind.__name__}")
    for field in record:
        if field not in schema:
            problems.append(f"unexpected {field}")
    return problems

schema = {"name": str, "price": float, "in_stock": bool}
print(validate({"name": "Bell", "price": 12, "in_stock": True}, schema))
print(validate({"name": "Bell", "price": "12", "colour": "red"}, schema))
```
hint: Two loops: one over `schema.items()` for missing and wrong-typed fields, then one over `record` for unexpected fields.
hint: `isinstance(value, kind)` works for most types, but `isinstance(True, int)` is `True`. Handle `int` and `float` specially, excluding `bool`.
hint: For a `float` field: `isinstance(value, (int, float)) and not isinstance(value, bool)`. A type's name is `kind.__name__`.
approach:
1. **Understand:** collect every problem (don't stop at the first), in a fixed order, with exact messages.
2. **Examples:** `"12"` for price → wrong type; `True` for price → also wrong.
3. **Brute force:** this is already linear; the work is in the edge cases.
4. **Pattern:** **schema-driven validation** with special cases for JSON numbers.
5. **Plan:** loop over the schema (missing → `continue`; type check) → loop over the record for extras.
6. **Code and test:** int for float, bool for int and float, `None`, empty record, extras order.
walkthrough:
**Line by line**

- `continue` after "missing" avoids reading a value that isn't there.
- `float` accepts `int` because JSON numbers like `12` parse as Python `int`.
- `not isinstance(value, bool)` is needed because `bool` is a subclass of `int`: without it, `True` would pass as a price of 1.
- The second loop reports fields the schema doesn't know, which often signal a typo in a field name (`"colour"` versus `"color"`).

**Trace** on the second example: name ok; price `"12"` is a str → "price should be float"; in_stock absent → "missing in_stock"; colour isn't in the schema → "unexpected colour".

**Complexity:** O(fields).

**Common wrong approach:** `type(value) == kind`, which rejects `12` for a float field, or plain `isinstance`, which lets `True` through as a number. In real projects, Pydantic handles these rules for you (and can be set to strict mode).
:::

:::quiz
? What does a guaranteed structured-output feature guarantee?
+ The reply will parse and match your schema's structure
- Every value in the reply will be factually correct
- The reply will be shorter
= Format, not correctness: still validate values that matter.
? Why make a field nullable (or add an "unknown" option)?
+ So the model isn't pushed to invent a value when the information is missing
- Because JSON requires it
- To make parsing faster
= Leaving no way to say "not given" invites made-up answers.
? In Python, why can True slip through a check for an int field?
+ bool is a subclass of int, so isinstance(True, int) is True
- JSON converts true to 1
- isinstance is broken for numbers
= Exclude bool explicitly when checking numbers.
? Validation fails on a model's JSON. What is a good next step?
+ Send the specific errors back and ask the model to fix its answer, a limited number of times
- Retry the identical request forever
- Silently fill in default values
= Feedback plus a retry limit fixes most cases without endless loops.
:::

@@@ lesson
id: reasoning-and-multimodal
title: Reasoning, images and documents
minutes: 24
summary: Thinking (reasoning) models and how adaptive thinking works, the effort setting and its cost and speed trade-off, thinking tokens and max_tokens, sending images and PDFs as content blocks, estimating image tokens, and the limits of vision.
---
Two features change what a single call can do: models that **think** before answering, and models that **see** images and documents.

### Thinking models

A **reasoning model** can write out intermediate reasoning (**thinking**) before its final answer. Working through a problem step by step makes it much better at maths, code, planning and multi-step analysis, at the cost of more output tokens and more time.

On current Claude models thinking is **adaptive**: the model decides per request whether and how much to think, so a simple question gets a quick answer and a hard one gets careful reasoning. You steer it with the **effort** setting:

```py-static
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,                       # includes thinking tokens, so leave room
    output_config={"effort": "high"},       # low, medium, high, xhigh or max
    messages=[{"role": "user", "content": "Plan a database migration that avoids downtime."}],
)
print(response.usage.output_tokens)         # billed output, including all thinking
```

| Effort | Use for |
|---|---|
| `low` | simple, high-volume tasks where speed and cost matter most |
| `medium` | a balanced default (the default on Opus 5.5) |
| `high` | complex reasoning, coding and agent work (the default on most other models) |
| `xhigh`, `max` | the hardest problems, when quality matters far more than time and cost |

Effort affects **all** output, not just thinking: lower effort also means shorter answers and fewer tool calls. Start at the default, then try a lower level on your evaluation set (Part 6); keep it if quality holds.

Details that trip people up (current as of late 2026; check the docs for your model):

- `max_tokens` **includes** thinking. Set it too low and the reply can stop at `max_tokens` before any answer appears.
- You are billed for **all** the thinking tokens. By default the newest Claude models return thinking blocks with the text **omitted**; `thinking={"type": "adaptive", "display": "summarized"}` returns a readable summary instead. Either way the cost is the same.
- When you send a conversation back (especially with tools), **pass thinking blocks back unchanged**: they carry the reasoning behind earlier steps.
- Thinking can't be switched off on Opus 5.5 or Fable 5.1 (effort is the control). Sonnet 5.5 can skip up-front thinking with `thinking={"type": "between_tools"}`. Haiku 4.5 is the reverse: thinking is off unless you turn it on with a token budget.
- Don't ask a thinking model to "think step by step" in the prompt for things it already reasons about; tell it **what** a good answer looks like instead (Part 3).

### Images

Vision models accept images as content blocks, from a URL, base64 data, or a file uploaded with the Files API:

```py-static
import base64

with open("receipt.jpg", "rb") as f:
    data = base64.standard_b64encode(f.read()).decode("ascii")

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}},
        {"type": "text", "text": "List each item and price on this receipt as JSON."},
    ]}],
)
```

- Formats: **JPEG, PNG, GIF** (first frame only) and **WebP**. Up to 10 MB per image (base64) on the Claude API.
- Put images **before** the question; it tends to work best.
- Images cost tokens. Claude splits an image into 28×28-pixel patches: about ⌈width ÷ 28⌉ × ⌈height ÷ 28⌉ tokens. Large images are scaled down first (on Claude 4.7 and later, to at most 2,576 pixels on the long edge and 4,784 tokens). The first exercise estimates it.
- Base64 is about a third bigger than the raw bytes; for repeated use, upload once with the **Files API** and reference the `file_id`.
- Limits: counting many small objects and precise positions are approximate; small, blurry or rotated text may be misread; models don't identify real people from their faces. Check important readings.

### PDFs and documents

A PDF goes in a `document` block. Claude reads each page **both** as extracted text and as an image, so it understands charts, tables and layout, not just the words:

```py-static
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": [
        {"type": "document", "source": {"type": "url", "url": "https://example.com/annual-report.pdf"}},
        {"type": "text", "text": "Summarise the revenue trend shown in the charts."},
    ]}],
)
```

Expect roughly **1,500–3,000 text tokens per page plus the page image**, so a long PDF is expensive: cache it (Lesson 11) when you ask several questions about the same document, or extract only the pages you need. Plain-text formats (Markdown, CSV, code) are cheapest sent as text.

:::exercise Estimate an image's tokens
Write `image_tokens(width, height, max_edge=2576, max_tokens=4784)` estimating how many tokens an image costs:

1. If the longer side is more than `max_edge`, scale **both** sides by `max_edge / longer side` (keep them as floats).
2. The estimate is `ceil(width / 28) * ceil(height / 28)`, capped at `max_tokens`.
```python starter
import math

def image_tokens(width, height, max_edge=2576, max_tokens=4784):
    pass

print(image_tokens(1000, 1000))   # 1296
print(image_tokens(3840, 2160))   # 4784 (a 4K screenshot is scaled down first)
```
```python check
fn = need("image_tokens")
test(fn, cases=[
    ((1000, 1000), 1296, "a 1000×1000 photo"),
    ((3840, 2160), 4784, "a 4K screenshot"),
    ((28, 28), 1, "one patch"),
    ((29, 28), 2, "a pixel over one patch"),
    ((200, 100), 32, "a small image"),
    ((2576, 1000), 3312, "exactly the maximum edge"),
    ((1000, 5152), 1656, "a tall image, scaled by half"),
    ((4000, 4000), 4784, "a large square, capped"),
    ((1920, 1080), 2691, "a full-HD screenshot"),
    ((800, 600, 1568, 1568), 638, "older-model limits, under the cap"),
    ((3840, 2160, 1568, 1568), 1568, "older-model limits, capped"),
])
```
```python solution
import math

def image_tokens(width, height, max_edge=2576, max_tokens=4784):
    longest = max(width, height)
    if longest > max_edge:
        scale = max_edge / longest
        width, height = width * scale, height * scale
    return min(max_tokens, math.ceil(width / 28) * math.ceil(height / 28))

print(image_tokens(1000, 1000))
print(image_tokens(3840, 2160))
```
hint: First decide whether the image needs shrinking: compare `max(width, height)` with `max_edge`.
hint: Shrinking multiplies both sides by the same factor, `max_edge / longest`, which keeps the shape. Partial patches still count, so round **up** with `math.ceil`.
hint: `min(max_tokens, math.ceil(width / 28) * math.ceil(height / 28))`.
approach:
1. **Understand:** scale down only when too big, keep the aspect ratio, count 28-pixel patches rounded up, then cap.
2. **Examples:** 3840×2160 → scale 2576/3840 → 2576×1449 → 92 × 52 = 4784.
3. **Brute force:** not needed: it's a formula.
4. **Pattern:** **clamp, then compute**.
5. **Plan:** longest side → optional scale → ceil × ceil → min with the cap.
6. **Code and test:** exactly at the edge, just over a patch, tall images, the cap.
walkthrough:
**Line by line**

- Using the **longer** side for the scale factor guarantees both sides end up within `max_edge`.
- Scaling both sides by the same factor keeps the aspect ratio, as the real resizing does.
- `math.ceil` counts a partial patch as a whole one: a 29-pixel-wide image needs two columns of patches.
- `min(max_tokens, …)` applies the per-image token limit.

**Trace** for 1000×5152: the longest side 5152 > 2576, so scale by 0.5 → 500×2576 → ⌈500 / 28⌉ × ⌈2576 / 28⌉ = 18 × 92 = 1656.

**Complexity:** O(1).

**Common wrong approach:** rounding down (`//`), which undercounts every image whose sides aren't multiples of 28. Remember it's an **estimate**: the real resizer shrinks an image a little further when it's over the token limit (a 4K screenshot on older models costs 1,560 tokens, not the capped 1,568), so use the token-counting API for exact numbers.
:::

:::exercise Build a multimodal message
Write `build_content(files, question)` turning a list of `(filename, data)` pairs (`data` is `bytes`) and a question into a list of content blocks: one block per file **in order**, then a text block with the question.

- `.png`, `.jpg`/`.jpeg`, `.gif`, `.webp` → `{"type": "image", "source": {"type": "base64", "media_type": ..., "data": ...}}` with media types `image/png`, `image/jpeg`, `image/gif`, `image/webp`.
- `.pdf` → the same shape with `"type": "document"` and `application/pdf`.
- The extension check ignores case (`PHOTO.JPG` is fine). `data` is `base64.b64encode(data).decode("ascii")`.
- Any other extension → `raise ValueError(f"unsupported file: {filename}")`.
```python starter
import base64

def build_content(files, question):
    pass

blocks = build_content([("chart.png", b"\x89PNG..."), ("report.pdf", b"%PDF-1.7")], "What changed?")
for block in blocks:
    print(block["type"], block.get("source", {}).get("media_type", ""))
```
```python check
import base64
fn = need("build_content")
_b = lambda kind, media, raw: {"type": kind, "source": {"type": "base64", "media_type": media, "data": base64.b64encode(raw).decode("ascii")}}
_q = lambda text: {"type": "text", "text": text}
test(fn, cases=[
    (([("chart.png", b"png-bytes"), ("report.pdf", b"%PDF-1.7")], "What changed?"),
     [_b("image", "image/png", b"png-bytes"), _b("document", "application/pdf", b"%PDF-1.7"), _q("What changed?")], "an image and a PDF"),
    (([], "Hello"), [_q("Hello")], "no files"),
    (([("PHOTO.JPG", b"\xff\xd8")], "Describe it."), [_b("image", "image/jpeg", b"\xff\xd8"), _q("Describe it.")], "upper-case extension"),
    (([("a.jpeg", b"1"), ("b.gif", b"2"), ("c.webp", b"3")], "Compare."),
     [_b("image", "image/jpeg", b"1"), _b("image", "image/gif", b"2"), _b("image", "image/webp", b"3"), _q("Compare.")], "every image type, in order"),
    (([("my.photo.png", b"x")], "?"), [_b("image", "image/png", b"x"), _q("?")], "dots in the name"),
])
for _bad in ["notes.docx", "image.bmp", "README", "archive.png.zip"]:
    try:
        fn([(_bad, b"x")], "?")
    except ValueError as _e:
        assert _bad in str(_e), f"The error message for {_bad!r} should include the file name, like: unsupported file: {_bad}"
    else:
        raise AssertionError(f"build_content should raise ValueError for {_bad!r}, but it returned normally.")
```
```python solution
import base64

MEDIA_TYPES = {
    "png": ("image", "image/png"),
    "jpg": ("image", "image/jpeg"),
    "jpeg": ("image", "image/jpeg"),
    "gif": ("image", "image/gif"),
    "webp": ("image", "image/webp"),
    "pdf": ("document", "application/pdf"),
}

def build_content(files, question):
    blocks = []
    for filename, data in files:
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if extension not in MEDIA_TYPES:
            raise ValueError(f"unsupported file: {filename}")
        kind, media_type = MEDIA_TYPES[extension]
        blocks.append({"type": kind, "source": {"type": "base64", "media_type": media_type,
                                                "data": base64.b64encode(data).decode("ascii")}})
    blocks.append({"type": "text", "text": question})   # the question goes after the files
    return blocks

blocks = build_content([("chart.png", b"\x89PNG..."), ("report.pdf", b"%PDF-1.7")], "What changed?")
for block in blocks:
    print(block["type"], block.get("source", {}).get("media_type", ""))
```
hint: A dict from extension to `(block type, media type)` keeps the rules in one place.
hint: The extension is the text after the **last** dot: `filename.rsplit(".", 1)[-1].lower()`. A name with no dot has no extension.
hint: Build each block, append the text block last, and `raise ValueError(f"unsupported file: {filename}")` for unknown extensions.
approach:
1. **Understand:** files first (images before text works best), then the question; exact block shapes; reject unknown types loudly.
2. **Examples:** `PHOTO.JPG` → jpeg; `archive.png.zip` → zip → error.
3. **Brute force:** a chain of `if`/`elif` per extension: works but repetitive.
4. **Pattern:** **lookup table** plus a loop.
5. **Plan:** extension → table lookup or error → block → append question.
6. **Code and test:** no files, upper case, several dots, no extension.
walkthrough:
**Line by line**

- `rsplit(".", 1)[-1]` splits once from the right, so `my.photo.png` gives `png` and `archive.png.zip` gives `zip`.
- `.lower()` makes `JPG` and `jpg` the same.
- The table maps each extension to both the block type and the media type, so adding a format is a one-line change.
- `base64.b64encode` returns bytes; `.decode("ascii")` turns it into the string JSON needs.

**Trace:** `chart.png` → image/png block; `report.pdf` → document block; then the question text block.

**Complexity:** O(total bytes), for the encoding.

**Common wrong approach:** checking `"png" in filename`, which accepts `png_notes.txt`, or guessing the media type wrongly (`image/jpg` isn't a valid media type: it's `image/jpeg`).
:::

:::quiz
? Why can a reply hit max_tokens before any visible answer appears?
+ max_tokens includes the thinking tokens, which come first
- Thinking is free but slow
- Images use up max_tokens
= Leave room for thinking plus the answer.
? What does lowering effort change?
+ All output: less thinking, shorter answers and fewer tool calls
- Only the price per token
- Only the thinking display
= It trades quality for speed and cost across the whole response.
? Thinking display is set to omitted. What do you pay for?
+ All the thinking tokens the model actually generated
- Nothing for thinking
- Only the summary
= Display changes what you see, not what you're billed.
? What is a sensible way to ask several questions about one long PDF?
+ Cache the document (prompt caching) or send only the relevant pages
- Send it base64-encoded twice for accuracy
- Convert it to an image first
= Each page costs text tokens plus an image, so avoid paying for it repeatedly.
:::

@@@ lesson
id: cost-and-caching
title: Cost, caching and batches
minutes: 26
summary: Where the money goes in an LLM application, reading token usage, prompt caching (how prefixes are cached, automatic and explicit breakpoints, lifetimes, minimum lengths, what breaks the cache), the Batch API for half-price offline work, token counting, and other levers for cutting cost and latency.
---
A prototype that costs a few cents a day can cost thousands a month in production. Cost is predictable, though: it's **tokens × price**, and a handful of techniques cut it dramatically.

### Where the money goes

Every response reports its token usage. With prompt caching in play, input is split into three parts:

```python
usage = {
    "input_tokens": 150,                  # normal input after the last cache point
    "cache_creation_input_tokens": 0,     # input written to the cache on this call
    "cache_read_input_tokens": 12000,     # input read from the cache (cheap)
    "output_tokens": 420,                 # the reply, including any thinking
}
total_input = usage["input_tokens"] + usage["cache_creation_input_tokens"] + usage["cache_read_input_tokens"]
print("total input tokens:", total_input)
```

Each part has its own price. For Claude, relative to the normal input price:

| Token type | Price |
|---|---|
| normal input | 1× |
| cache write, 5-minute lifetime | 1.25× |
| cache write, 1-hour lifetime | 2× |
| cache read | 0.1× (lower on some models: 0.05× on Opus 5.5, 0.025× on Fable 5.1) |
| output | the model's output price, usually 5× its input price |

Output is the expensive part per token, but in many applications **input dominates the bill** because every call resends a long system prompt, documents, tool definitions and the conversation history. That repeated input is exactly what caching targets.

### Prompt caching

Calls in a real application often share a long, identical **prefix**: the same system prompt, the same tool list, the same document. With **prompt caching**, the provider stores its processed form for a while; a later request that starts with the **exact same prefix** reads it from the cache, which is much cheaper and faster.

![Three requests drawn as horizontal bars. Each starts with the same long prefix (tools, system prompt, a document) and ends with a different short question. The first request writes the prefix to the cache (slightly more expensive); the second and third read it from the cache (about a tenth of the price) and pay full price only for their new question](figures/prompt-caching.svg)

With Claude, the simplest form is **automatic caching**: one `cache_control` setting on the request, and the system places the cache point and moves it forward as a conversation grows:

```py-static
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},          # automatic caching
    system=LONG_SHOP_POLICY,                      # identical on every call
    messages=[{"role": "user", "content": "Can I return a used helmet?"}],
)
print(response.usage.cache_creation_input_tokens, response.usage.cache_read_input_tokens)
```

You can instead mark up to **four explicit breakpoints** by putting `"cache_control": {"type": "ephemeral"}` on specific content blocks, which helps when different sections change at different rates.

The rules that decide whether you actually get cache hits:

- **Exact prefix match.** Caching covers everything up to the breakpoint, in the order **tools → system → messages**. Change one character early on (a timestamp in the system prompt, a reordered tool list, keys in a different order in JSON you send) and everything after it misses.
- **Put stable content first, variable content last**: instructions and documents at the top, the user's question at the end.
- **Lifetime:** 5 minutes by default, refreshed each time the cache is read; `{"type": "ephemeral", "ttl": "1h"}` keeps it for an hour at a higher write price.
- **Minimum length:** prefixes shorter than the model's minimum (for example 512 tokens on current Claude 5.x models, 4,096 on Haiku 4.5) aren't cached at all, with no error: you'll just see zero cache tokens.
- **Check it works:** watch `cache_read_input_tokens` in production. If it stays at 0, something in your prefix is changing.

Other providers cache too (OpenAI caches long prefixes automatically, for example); the details and discounts differ, but "stable prefix first" is always the rule.

### Batches: half price when you can wait

Many jobs don't need an instant answer: classifying a million reviews, generating test data, running an evaluation set overnight. The **Message Batches API** takes up to 100,000 requests (or 256 MB) at once and processes them asynchronously at **50% of the normal price**. Most batches finish within an hour; results are guaranteed within 24 hours and kept for 29 days.

```py-static
batch = client.messages.batches.create(requests=[
    {"custom_id": f"review-{i}",
     "params": {"model": "claude-haiku-4-5-20251001", "max_tokens": 50,
                "messages": [{"role": "user", "content": f"Sentiment (positive/negative/mixed): {text}"}]}}
    for i, text in enumerate(reviews)
])

# Later (poll, or check back after a while):
batch = client.messages.batches.retrieve(batch.id)
if batch.processing_status == "ended":
    for item in client.messages.batches.results(batch.id):
        if item.result.type == "succeeded":
            print(item.custom_id, item.result.message.content[0].text)
        else:
            print(item.custom_id, "failed:", item.result.type)   # errored, canceled or expired
```

Results can come back in **any order**, so match them up by `custom_id`. Caching discounts stack with the batch discount, so a shared prefix across a batch makes it cheaper still.

### Count before you send

To know a request's size before paying for it (for a long PDF, a big conversation, or to enforce a budget), use the **token-counting** endpoint. It's free (with its own rate limits):

```py-static
count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    system=LONG_SHOP_POLICY,
    messages=[{"role": "user", "content": "Can I return a used helmet?"}],
)
print(count.input_tokens)
```

### More ways to cut cost and latency

| Lever | Typical saving | Trade-off |
|---|---|---|
| a smaller model for easy requests (routing) | 2–10× | needs an evaluation to prove quality holds |
| lower effort | fewer output tokens, faster | may reduce quality on hard tasks |
| shorter outputs (ask for brevity, set `max_tokens`) | proportional to output | — |
| prompt caching | up to ~90% of repeated input | prefix must stay identical |
| batches | 50% | answers arrive later |
| trimming history and retrieved context | proportional to input | may drop useful context |
| caching **answers** for repeated questions in your own app | 100% on a hit | stale or mismatched answers |

The cheapest token is the one you don't send. Measure first: log the usage of every call (Part 6), then fix the biggest line on the bill.

:::exercise What did this call cost?
Write `call_cost(usage, price_in, price_out, ttl="5m", read_multiplier=0.1)` returning the cost **in dollars** of one call. Prices are in **dollars per million tokens**. `usage` has the four keys shown in the lesson:

- `input_tokens` at `price_in`,
- `cache_creation_input_tokens` at `price_in × 1.25` when `ttl` is `"5m"`, or `× 2` when it's `"1h"`,
- `cache_read_input_tokens` at `price_in × read_multiplier`,
- `output_tokens` at `price_out`.
```python starter
def call_cost(usage, price_in, price_out, ttl="5m", read_multiplier=0.1):
    pass

usage = {"input_tokens": 150, "cache_creation_input_tokens": 0,
         "cache_read_input_tokens": 12000, "output_tokens": 420}
print(round(call_cost(usage, 2.0, 10.0), 6))   # Sonnet 5.5 prices: 0.0069
```
```python check
fn = need("call_cost")
_u = lambda i=0, w=0, r=0, o=0: {"input_tokens": i, "cache_creation_input_tokens": w, "cache_read_input_tokens": r, "output_tokens": o}
test(fn, cases=[
    ((_u(150, 0, 12000, 420), 2.0, 10.0), 0.0069, "a cache hit"),
    ((_u(1_000_000), 2.0, 10.0), 2.0, "a million input tokens"),
    ((_u(o=1_000_000), 2.0, 10.0), 10.0, "a million output tokens"),
    ((_u(w=1_000_000), 2.0, 10.0), 2.5, "a 5-minute cache write"),
    ((_u(w=1_000_000), 2.0, 10.0, "1h"), 4.0, "a 1-hour cache write"),
    ((_u(r=1_000_000), 4.0, 20.0, "5m", 0.05), 0.2, "a cache read on Opus 5.5"),
    ((_u(100, 5000, 0, 300), 1.0, 5.0), 0.00785, "a first call that writes the cache"),
    ((_u(), 2.0, 10.0), 0.0, "no tokens"),
])
```
```python solution
def call_cost(usage, price_in, price_out, ttl="5m", read_multiplier=0.1):
    write_multiplier = 2.0 if ttl == "1h" else 1.25
    dollars_per_million = (
        usage["input_tokens"] * price_in
        + usage["cache_creation_input_tokens"] * price_in * write_multiplier
        + usage["cache_read_input_tokens"] * price_in * read_multiplier
        + usage["output_tokens"] * price_out
    )
    return dollars_per_million / 1_000_000

usage = {"input_tokens": 150, "cache_creation_input_tokens": 0,
         "cache_read_input_tokens": 12000, "output_tokens": 420}
print(round(call_cost(usage, 2.0, 10.0), 6))
```
hint: Each of the four token counts has its own price per million tokens; multiply, add them up, then divide by 1,000,000.
hint: The cache-write price depends on `ttl`: 1.25 × `price_in` for `"5m"`, 2 × for `"1h"`. Reads are `price_in × read_multiplier`.
hint: `(input × pin + writes × pin × w + reads × pin × r + output × pout) / 1_000_000`.
approach:
1. **Understand:** four token types, four prices, one total in dollars.
2. **Examples:** 150 × 2 + 12,000 × 0.2 + 420 × 10 = 300 + 2,400 + 4,200 = 6,900 → $0.0069.
3. **Brute force:** it's a formula.
4. **Pattern:** **weighted sum** of counts and prices.
5. **Plan:** pick the write multiplier from `ttl` → sum → divide by a million.
6. **Code and test:** each token type alone, both lifetimes, a different read multiplier, zero usage.
walkthrough:
**Line by line**

- The write multiplier is chosen once from `ttl`, keeping the main formula readable.
- Summing in "dollars per million" units and dividing once at the end avoids lots of tiny numbers.
- The read multiplier is a parameter because it differs between models.

**Trace** on the example: 300 + 0 + 2,400 + 4,200 = 6,900 → 6,900 / 1,000,000 = $0.0069. Without the cache, those 12,000 tokens would have cost 24,000 instead of 2,400: the call would be about four times dearer.

**Complexity:** O(1).

**Common wrong approach:** forgetting that `input_tokens` excludes the cached tokens, and so computing the cache saving from the wrong total (or adding the cached tokens twice).
:::

:::exercise Does caching pay off?
A prefix of `prefix_tokens` is sent on `calls` requests (all within the cache lifetime). Write `cache_savings(prefix_tokens, calls, price_in, ttl="5m", read_multiplier=0.1, min_tokens=512)` returning the **dollars saved on the prefix** by caching it, compared with sending it uncached every time:

- Uncached: every call pays `price_in` for the prefix.
- Cached: the first call pays the write price (1.25× for `"5m"`, 2× for `"1h"`), the rest pay the read price.
- If `prefix_tokens < min_tokens`, nothing is cached, so the saving is `0.0`.

The result can be **negative** when caching costs more than it saves. Prices are per million tokens.
```python starter
def cache_savings(prefix_tokens, calls, price_in, ttl="5m", read_multiplier=0.1, min_tokens=512):
    pass

print(round(cache_savings(10_000, 100, 2.0), 4))          # 1.777
print(round(cache_savings(10_000, 2, 2.0, ttl="1h"), 4))  # -0.002: not worth it
```
```python check
fn = need("cache_savings")
test(fn, cases=[
    ((10_000, 100, 2.0), 1.777, "many calls"),
    ((10_000, 2, 2.0, "1h"), -0.002, "two calls with a 1-hour cache"),
    ((10_000, 3, 2.0, "1h"), 0.016, "three calls with a 1-hour cache"),
    ((10_000, 1, 2.0), -0.005, "a single call pays the write premium"),
    ((10_000, 2, 2.0), 0.013, "two calls with a 5-minute cache"),
    ((400, 1000, 2.0), 0.0, "too short to cache"),
    ((512, 2, 4.0, "5m", 0.05), 0.0014336, "exactly the minimum, Opus 5.5 read price"),
    ((2_000, 10, 1.0, "5m", 0.1, 4096), 0.0, "below Haiku's minimum"),
])
```
```python solution
def cache_savings(prefix_tokens, calls, price_in, ttl="5m", read_multiplier=0.1, min_tokens=512):
    if prefix_tokens < min_tokens:
        return 0.0                                        # too short: nothing is cached
    write_multiplier = 2.0 if ttl == "1h" else 1.25
    uncached = calls * 1.0
    cached = write_multiplier + (calls - 1) * read_multiplier
    return (uncached - cached) * prefix_tokens * price_in / 1_000_000

print(round(cache_savings(10_000, 100, 2.0), 4))
print(round(cache_savings(10_000, 2, 2.0, ttl="1h"), 4))
```
hint: Work in "multiples of the prefix's normal price" first: uncached is `calls × 1`; cached is one write plus `calls − 1` reads.
hint: The saving is `(uncached − cached) × prefix_tokens × price_in / 1,000,000`. Check `min_tokens` first.
hint: With a 5-minute cache: `cached = 1.25 + (calls - 1) * read_multiplier`; with `"1h"`, use 2.0 instead of 1.25.
approach:
1. **Understand:** compare two totals for the same prefix; the difference may be negative.
2. **Examples:** 2 calls, 1-hour cache: uncached 2×, cached 2 + 0.1 = 2.1× → a small loss.
3. **Brute force:** add up each call's cost in a loop for both strategies: fine.
4. **Pattern:** **break-even analysis**: a fixed premium paid back by per-use savings.
5. **Plan:** minimum-length guard → multipliers → difference × tokens × price.
6. **Code and test:** one call, two calls with each lifetime, below the minimum.
walkthrough:
**Line by line**

- The guard mirrors the real behaviour: short prefixes are silently not cached, so there's neither a premium nor a saving.
- Measuring both strategies in "multiples of the normal price" makes the break-even visible: the 5-minute cache pays off from the **second** call (2 vs 1.35); the 1-hour cache from the **third** (3 vs 2.2).
- Multiplying by `prefix_tokens × price_in / 1,000,000` converts to dollars only at the end.

**Trace** for 100 calls, 5-minute cache: uncached 100; cached 1.25 + 99 × 0.1 = 11.15; saving 88.85 × 10,000 × 2 / 1,000,000 = $1.777, about 89% of the prefix's cost.

**Complexity:** O(1).

**Common wrong approach:** assuming caching always saves money. A one-off request, or a 1-hour cache used only twice, costs more than not caching.
:::

:::quiz
? Your cache_read_input_tokens stays at 0. What is the most likely cause?
+ Something early in the prompt changes on every call, such as a timestamp, or the prefix is below the minimum length
- Caching only works on Fridays
- The output is too long
= Caching needs an identical prefix of at least the minimum length.
? Where should a user's question go in a cached prompt?
+ At the end, after the stable instructions and documents
- At the very start
- In the tool definitions
= Stable content first, variable content last.
? Which job suits the Batch API?
+ Classifying 200,000 support tickets overnight
- A live chat reply
- Autocomplete as the user types
= Batches are half price but asynchronous.
? Batch results come back. How do you match each result to its request?
+ By the custom_id you gave each request
- By their order in the results
- By the model name
= Results can arrive in any order.
:::
