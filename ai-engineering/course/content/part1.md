@@@ part
id: 1
title: How LLMs Work
level: Beginner
blurb: What a large language model really does (predict the next token), how text becomes tokens and vectors, the attention mechanism at the heart of transformers, how sampling settings shape answers, and how to choose a model.

@@@ lesson
id: what-is-an-llm
title: What an LLM is
minutes: 20
summary: Large language models as next-token predictors, how they're trained (pretraining, instruction tuning, reinforcement learning from feedback), a tiny next-word model built from scratch, what LLMs are good and bad at, and where they fit in software.
---
A **large language model (LLM)** is a program that has learned, from a huge amount of text, to do one thing extremely well: given some text, **predict what comes next**. Everything else (answering questions, writing code, summarising, calling tools) is built on that single skill.

When you send a model a message, it doesn't look anything up in a database of answers. It predicts the most fitting next piece of text, adds it to what's there, and repeats, one small piece (a **token**, next lesson) at a time, until it decides to stop.

![A loop: the text so far, "The capital of France is", goes into the model, which outputs probabilities for the next token (" Paris" 92%, " a" 3%, " the" 2%, …). One token is picked, appended to the text, and the longer text goes back into the model to predict the following token](figures/next-token.svg)

### A next-word model you can build in a minute

The simplest language model counts, in some training text, which word follows which. To continue a text, it looks at the last word and picks a likely follower. Real LLMs replace the counting table with a neural network billions of times larger, look at the whole text instead of one word, and work on tokens instead of words, but the loop is the same.

```python
import random
from collections import Counter, defaultdict

text = """the cat sat on the mat . the dog sat on the rug .
the cat saw the dog . the dog saw the cat ."""

follows = defaultdict(Counter)          # word -> Counter of the words that came next
words = text.split()
for current, nxt in zip(words, words[1:]):
    follows[current][nxt] += 1

print(follows["the"])                   # what tends to follow "the"
print(follows["sat"])

def generate(start, length, seed=0):
    rng = random.Random(seed)
    out = [start]
    for _ in range(length):
        options = follows[out[-1]]
        if not options:
            break
        choices, weights = zip(*options.items())
        out.append(rng.choices(choices, weights)[0])     # sample in proportion to the counts
    return " ".join(out)

print(generate("the", 8))
print(generate("the", 8, seed=3))
```

This **bigram** model already shows the key ideas: it learned only from data, its output is **probabilistic** (a different random seed gives a different continuation), and it produces fluent-looking text with no understanding of whether it's true.

### How real LLMs are trained

| Stage | What happens | What the model gains |
|---|---|---|
| **Pretraining** | Predict the next token on trillions of tokens of web pages, books, code and more | Grammar, facts, reasoning patterns, coding ability |
| **Instruction tuning** (supervised fine-tuning) | Train on examples of instructions and good answers | Following requests, answering in a helpful format |
| **Reinforcement learning from feedback** | Reward responses that people (or reward models) prefer, and responses that solve checkable tasks | Helpfulness, honesty, safety, step-by-step reasoning |

The result is often called a **foundation model**: one general model that can be steered to many tasks with instructions (prompts), examples, retrieved documents and tools, without retraining.

Many current models can also **reason** before answering: they generate intermediate thinking tokens (sometimes hidden from the user) that work through the problem, which improves answers on maths, coding and multi-step tasks at the cost of more tokens and time.

### What LLMs are good and bad at

| Good at | Weak at, without help |
|---|---|
| Writing, rewriting, summarising, translating | Exact arithmetic on large numbers (use a calculator tool) |
| Extracting structure from messy text | Facts after their **knowledge cutoff** (give them documents or a search tool) |
| Writing and explaining code | Remembering earlier conversations (each API call is stateless) |
| Classifying, tagging, routing requests | Knowing when they don't know: they can produce confident, wrong answers (**hallucinations**) |
| Following detailed instructions and examples | Your private data (they've never seen it unless you provide it) |

Almost all of AI engineering is about the right-hand column: giving the model the **context** it lacks (Part 4), the **tools** it needs (Part 5), and **checking** its output (Part 6).

### Where an LLM sits in software

To your program, a model is a function behind an API: you send text (and possibly images, documents and tool definitions) and get text back. The engineering is everything around that call:

1. Build the **prompt**: instructions, examples, the user's input, retrieved documents.
2. **Call** the model API, handling errors, timeouts and cost.
3. **Parse and validate** the output (for example, as JSON).
4. **Act** on it: show it, store it, or call a tool and loop.
5. **Evaluate** quality over many examples, and monitor it in production.

:::exercise Count what comes next
Write `next_word_counts(text)` that splits `text` on whitespace and returns a dict mapping each word to a dict of `{next_word: count}`: how many times each word directly followed it. The last word has nothing after it, so it only appears as a key if it also appears earlier.
```python starter
def next_word_counts(text):
    pass

print(next_word_counts("the cat sat on the mat"))
# {'the': {'cat': 1, 'mat': 1}, 'cat': {'sat': 1}, 'sat': {'on': 1}, 'on': {'the': 1}}
```
```python check
fn = need("next_word_counts")
def _plain(d):
    return {k: dict(v) for k, v in d.items()} if isinstance(d, dict) else d
test(fn, key=_plain, cases=[
    (("the cat sat on the mat",), {"the": {"cat": 1, "mat": 1}, "cat": {"sat": 1}, "sat": {"on": 1}, "on": {"the": 1}}, "the example"),
    (("a a a",), {"a": {"a": 2}}, "a word following itself"),
    (("hello",), {}, "a single word"),
    (("",), {}, "empty text"),
    (("to be or not to be",), {"to": {"be": 2}, "be": {"or": 1}, "or": {"not": 1}, "not": {"to": 1}}, "a repeated pair"),
    (("one  two\nthree",), {"one": {"two": 1}, "two": {"three": 1}}, "extra spaces and a newline"),
])
```
```python solution
def next_word_counts(text):
    words = text.split()                     # split() handles any whitespace
    counts = {}
    for current, nxt in zip(words, words[1:]):
        inner = counts.setdefault(current, {})
        inner[nxt] = inner.get(nxt, 0) + 1
    return counts

print(next_word_counts("the cat sat on the mat"))
```
hint: You need every pair of neighbouring words: (word 0, word 1), (word 1, word 2), and so on.
hint: `zip(words, words[1:])` produces exactly those pairs. For each pair, add 1 to `counts[current][nxt]`.
hint: Use `counts.setdefault(current, {})` to get (or create) the inner dict, then `inner[nxt] = inner.get(nxt, 0) + 1`.
approach:
1. **Understand:** count adjacent pairs; split on any whitespace; the last word gets no entry of its own.
2. **Examples:** "a a a" → {'a': {'a': 2}}.
3. **Brute force:** loop over indexes i and look at words[i + 1]: works fine.
4. **Pattern:** **pairs of neighbours** with `zip(words, words[1:])` and a **nested counting dict**.
5. **Plan:** split, zip, count.
6. **Code and test:** a single word, empty text, irregular whitespace.
walkthrough:
**Line by line**

- `text.split()` with no argument splits on runs of spaces, tabs and newlines, and ignores leading and trailing whitespace.
- `zip(words, words[1:])` pairs each word with the one after it; with fewer than two words it produces nothing.
- `setdefault` returns the inner dict for `current`, creating it the first time.
- `inner.get(nxt, 0) + 1` increments the count, starting from 0.

**Trace** on "to be or not to be":

| pair | counts after |
|---|---|
| (to, be) | to: {be: 1} |
| (be, or) | be: {or: 1} |
| (or, not) | or: {not: 1} |
| (not, to) | not: {to: 1} |
| (to, be) | to: {be: **2**} |

**Complexity:** O(n) for n words.

**Common wrong approach:** `text.split(" ")`, which produces empty strings for double spaces and keeps newlines inside words.
:::

:::exercise Most likely next word
Using the counts from the previous exercise (passed in as `counts`), write `predict_next(counts, word)` returning the word that most often followed `word`. If several are tied, return the alphabetically first. If `word` never appeared with a follower, return `None`. This is **greedy decoding**: always picking the single most likely next token.
```python starter
def predict_next(counts, word):
    pass

counts = {"the": {"cat": 2, "dog": 2, "mat": 1}, "cat": {"sat": 1}}
print(predict_next(counts, "the"))   # cat (tied with dog; alphabetically first)
print(predict_next(counts, "sat"))   # None
```
```python check
fn = need("predict_next")
_c = {"the": {"cat": 2, "dog": 2, "mat": 1}, "cat": {"sat": 1}, "sat": {"on": 3, "in": 1}, "on": {}}
test(fn, cases=[
    ((_c, "the"), "cat", "a tie broken alphabetically"),
    ((_c, "cat"), "sat", "only one follower"),
    ((_c, "sat"), "on", "a clear winner"),
    ((_c, "dog"), None, "a word never seen"),
    ((_c, "on"), None, "a word with no followers"),
    (({"x": {"b": 1, "a": 1, "c": 1}}, "x"), "a", "a three-way tie"),
])
```
```python solution
def predict_next(counts, word):
    options = counts.get(word)
    if not options:
        return None                                     # unseen word, or nothing ever followed it
    return min(options, key=lambda w: (-options[w], w)) # highest count first, then alphabetical

counts = {"the": {"cat": 2, "dog": 2, "mat": 1}, "cat": {"sat": 1}}
print(predict_next(counts, "the"))
print(predict_next(counts, "sat"))
```
hint: First handle the cases where there's nothing to choose from: the word isn't a key, or its dict is empty.
hint: You want the highest count, and among equal counts the alphabetically smallest word. One sort key can express both.
hint: `min(options, key=lambda w: (-options[w], w))`: negating the count makes the largest count come first, and the word breaks ties.
approach:
1. **Understand:** argmax over counts; ties → alphabetical; missing or empty → None.
2. **Examples:** {"cat": 2, "dog": 2, "mat": 1} → "cat".
3. **Brute force:** loop, tracking the best word and its count, comparing ties by string order.
4. **Pattern:** **argmax with a tie-breaking key**.
5. **Plan:** guard, then `min` with the key `(-count, word)`.
6. **Code and test:** ties, a missing word, an empty dict.
walkthrough:
**Line by line**

- `counts.get(word)` returns None for an unseen word; `not options` is also true for an empty dict.
- Tuples compare element by element, so `(-count, word)` orders by count descending, then by word ascending.
- `min` over the dict iterates its keys and returns the key with the smallest tuple.

**Trace** on {"cat": 2, "dog": 2, "mat": 1}: keys map to (−2, "cat"), (−2, "dog"), (−1, "mat"); the smallest is (−2, "cat").

**Complexity:** O(k) for k distinct followers.

**Common wrong approach:** `max(options, key=options.get)`, which returns whichever tied word comes first in the dict, not the alphabetically first one.
:::

:::quiz
? At its core, what does a large language model do?
+ Predicts the next token given the text so far, repeatedly
- Looks up answers in a database of facts
- Runs a search engine query for every question
= Every capability is built on next-token prediction, one token at a time.
? Which training stage teaches a model to follow instructions and answer helpfully?
+ Instruction tuning (supervised fine-tuning), refined with reinforcement learning from feedback
- Pretraining on web text alone
- Tokenization
= Pretraining gives knowledge and language; tuning shapes behaviour.
? Why might a model answer a question about last month's news wrongly?
+ Its knowledge stops at its training cutoff unless you give it the information
- Models can only answer questions about code
- Because of the temperature setting
= Retrieval (RAG) or a search tool supplies current information.
? What is a hallucination?
+ A fluent, confident answer that isn't true or isn't supported by the sources
- A refusal to answer
- A very long answer
= Next-token prediction optimises for plausible text, not verified truth.
:::

@@@ lesson
id: tokens
title: Tokens and tokenization
minutes: 22
summary: Why models read tokens instead of characters or words, how byte-pair encoding builds a vocabulary by merging frequent pairs, token counts for different languages and content, and why tokens decide cost, speed and context limits.
---
Models don't read letters or words: they read **tokens**, chunks of text from a fixed **vocabulary** of tens of thousands to a few hundred thousand pieces. Common words are usually one token (" the", " cat"); rarer words are split into several (" token" + "ization"); spaces, punctuation and digits are tokens too. Each token is just an integer ID to the model.

![The sentence "Tokenization isn't magic!" split into coloured tokens: "Token", "ization", " isn", "'t", " magic", "!". Below each token is its integer ID. Spaces usually attach to the start of the following word](figures/tokens.svg)

### Why not characters, or whole words?

| Unit | Vocabulary | Problem |
|---|---|---|
| Characters | tiny (~100s) | texts become very long sequences, and the model must learn spelling from scratch |
| Whole words | enormous (millions, and new words appear all the time) | any word not in the vocabulary can't be represented |
| **Subwords (tokens)** | tens of thousands | frequent words stay whole, rare words split into known pieces: nothing is ever "unknown" |

### Byte-pair encoding (BPE)

The most common way to build a subword vocabulary is **byte-pair encoding**. Start with single characters (or bytes); count every pair of neighbouring symbols across the training text; **merge the most frequent pair** into a new symbol; repeat until the vocabulary is the size you want. Frequent words end up as single tokens because their pieces keep getting merged.

```python
from collections import Counter

def most_frequent_pair(words):
    pairs = Counter()
    for symbols, freq in words.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[(a, b)] += freq                 # weight by how often the word occurs
    return max(pairs, key=pairs.get) if pairs else None

def merge(words, pair):
    merged = {}
    for symbols, freq in words.items():
        out, i = [], 0
        while i < len(symbols):
            if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == pair:
                out.append(symbols[i] + symbols[i + 1])   # glue the pair into one symbol
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        merged[tuple(out)] = freq
    return merged

corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
words = {tuple(w): f for w, f in corpus.items()}       # start from single characters
for step in range(6):
    pair = most_frequent_pair(words)
    words = merge(words, pair)
    print(f"merge {step + 1}: {pair[0]!r} + {pair[1]!r}   ->", list(words))
```

After a few merges, "est" and "low" have become single symbols: the vocabulary has learned the common pieces of the language. Real tokenizers do this on bytes (so any text, emoji or language can be encoded) with tens of thousands of merges.

### Tokens are what you pay for and what fills the context

- **Cost:** APIs charge per token, usually per million, and **output tokens cost several times more than input tokens**.
- **Context window:** the maximum number of tokens (input plus output) the model can handle in one request, from about 200,000 to over 1,000,000 tokens for current frontier models.
- **Speed:** output is generated one token at a time, so long answers take longer.

A handy rule of thumb for English is **about 4 characters, or ¾ of a word, per token**. Other languages, code and numbers often use more tokens for the same content, so measure rather than guess:

```python
def rough_tokens(text):
    return max(1, round(len(text) / 4))          # the ~4 characters per token rule of thumb

for sample in ["Hello, world!",
               "The quick brown fox jumps over the lazy dog.",
               "def add(a, b):\n    return a + b"]:
    print(f"{rough_tokens(sample):>3} tokens (estimate)  {sample!r}")

words = 750
print(f"{words} English words is roughly {round(words / 0.75)} tokens")
```

Each provider's tokenizer is different, so the same text has a different token count with different models. The APIs report exact counts in every response, and have token-counting endpoints:

```py-static
import anthropic

client = anthropic.Anthropic()                       # reads ANTHROPIC_API_KEY from the environment
count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    messages=[{"role": "user", "content": "Tokenization isn't magic!"}],
)
print(count.input_tokens)

# OpenAI models: the open-source tiktoken library counts tokens locally
import tiktoken
enc = tiktoken.get_encoding("o200k_base")
print(len(enc.encode("Tokenization isn't magic!")))
```

### Quirks that come from tokens

- **Spelling and counting letters** ("how many r's in strawberry?") is hard for models, because they see tokens, not letters.
- **Arithmetic** on long numbers is error-prone: digits may be grouped into tokens unevenly. Give the model a calculator tool for exact maths (Part 5).
- **Trailing spaces and formatting** change tokenization, which can subtly change outputs.
- **Non-English text** typically costs more tokens per word, so the same conversation costs more and fills the context faster.

:::exercise Count the pairs
Write `pair_counts(words)` where `words` maps a tuple of symbols to how often that word appears, e.g. `{("l", "o", "w"): 5}`. Return a dict mapping every pair of neighbouring symbols to its total count across all words (weighted by each word's frequency). This is the first step of every BPE merge.
```python starter
def pair_counts(words):
    pass

print(pair_counts({("l", "o", "w"): 5, ("l", "o", "t"): 2}))
# {('l', 'o'): 7, ('o', 'w'): 5, ('o', 't'): 2}
```
```python check
fn = need("pair_counts")
test(fn, key=lambda d: dict(d) if isinstance(d, dict) else d, cases=[
    (({("l", "o", "w"): 5, ("l", "o", "t"): 2},), {("l", "o"): 7, ("o", "w"): 5, ("o", "t"): 2}, "the example"),
    (({("a",): 3},), {}, "a one-symbol word has no pairs"),
    (({},), {}, "no words"),
    (({("a", "a", "a"): 2},), {("a", "a"): 4}, "a repeated pair inside one word"),
    (({("lo", "w"): 1, ("lo", "w", "er"): 3},), {("lo", "w"): 4, ("w", "er"): 3}, "symbols longer than one character"),
])
```
```python solution
def pair_counts(words):
    counts = {}
    for symbols, freq in words.items():
        for pair in zip(symbols, symbols[1:]):     # neighbouring symbols
            counts[pair] = counts.get(pair, 0) + freq
    return counts

print(pair_counts({("l", "o", "w"): 5, ("l", "o", "t"): 2}))
```
hint: Inside each word, which pairs of symbols are neighbours?
hint: `zip(symbols, symbols[1:])` gives the neighbouring pairs of one word. Each occurrence of a pair should add the word's frequency, not 1.
hint: For each `(symbols, freq)` in `words.items()` and each pair from the zip, do `counts[pair] = counts.get(pair, 0) + freq`.
approach:
1. **Understand:** pairs inside each word, weighted by the word's frequency; overlapping pairs count separately.
2. **Examples:** ("a", "a", "a") × 2 → the pair ("a", "a") occurs twice in the word, so 4.
3. **Brute force:** index loops over each word: fine.
4. **Pattern:** **neighbour pairs + weighted counting**.
5. **Plan:** two nested loops, a dict of counts.
6. **Code and test:** one-symbol words, no words, multi-character symbols.
walkthrough:
**Line by line**

- Each word is a tuple of symbols (single characters at the start of BPE, longer pieces after merges).
- `zip(symbols, symbols[1:])` produces each neighbouring pair once per position.
- Adding `freq` (not 1) weights each pair by how common the word is in the corpus.

**Trace** on {("l","o","w"): 5, ("l","o","t"): 2}: low gives (l,o) +5, (o,w) +5; lot gives (l,o) +2, (o,t) +2 → (l,o): 7.

**Complexity:** O(total symbols).

**Common wrong approach:** counting each pair once per word instead of `freq` times, which makes rare words as influential as common ones.
:::

:::exercise Estimate the cost of a request
Prices are quoted per **million** tokens. Write `request_cost(input_tokens, output_tokens, input_price, output_price)` returning the cost in dollars, rounded to 6 decimal places. For example, 2,000 input tokens and 500 output tokens at $3 / $15 per million cost 0.006 + 0.0075 = 0.0135.
```python starter
def request_cost(input_tokens, output_tokens, input_price, output_price):
    pass

print(request_cost(2_000, 500, 3, 15))   # 0.0135
```
```python check
fn = need("request_cost")
test(fn, cases=[
    ((2_000, 500, 3, 15), 0.0135, "the example"),
    ((0, 0, 3, 15), 0.0, "an empty request"),
    ((1_000_000, 0, 2, 10), 2.0, "a million input tokens"),
    ((0, 1_000_000, 2, 10), 10.0, "a million output tokens"),
    ((123_456, 7_890, 1, 5), 0.162906, "rounded to 6 decimal places"),
    ((150_000, 4_000, 4, 20), 0.68, "a long document summary"),
])
```
```python solution
def request_cost(input_tokens, output_tokens, input_price, output_price):
    cost = input_tokens / 1_000_000 * input_price + output_tokens / 1_000_000 * output_price
    return round(cost, 6)

print(request_cost(2_000, 500, 3, 15))
```
hint: Prices are per million tokens, so first work out how many millions of tokens each side used.
hint: Input cost = `input_tokens / 1_000_000 * input_price`; the output side is the same with its own price.
hint: Add the two and return `round(total, 6)`.
approach:
1. **Understand:** separate prices for input and output; per million; round to 6 decimals.
2. **Examples:** 2,000 in at $3/M = $0.006; 500 out at $15/M = $0.0075.
3. **Brute force:** none needed: it's a formula.
4. **Pattern:** **unit conversion** (tokens → millions of tokens).
5. **Plan:** two products, a sum, a round.
6. **Code and test:** zeros, exactly one million, a value that needs rounding.
walkthrough:
**Line by line**

- Dividing by 1,000,000 converts tokens into millions of tokens, the unit the price is quoted in.
- Input and output are priced separately; output is usually several times dearer.
- `round(…, 6)` removes floating-point noise like 0.013500000000000002.

**Trace:** 2,000 / 1e6 × 3 = 0.006; 500 / 1e6 × 15 = 0.0075; total 0.0135.

**Complexity:** O(1).

**Common wrong approach:** multiplying by the price per token as if it were per thousand, which is off by a factor of 1,000.
:::

:::quiz
? Why do LLMs use subword tokens instead of whole words?
+ Frequent words stay whole while rare words split into known pieces, so no text is ever "unknown"
- Subwords are always shorter than characters
- Whole words can't be stored in a computer
= Subwords balance vocabulary size against sequence length.
? What does byte-pair encoding repeatedly do?
+ Merges the most frequent pair of neighbouring symbols into a new symbol
- Splits every word in half
- Removes rare words from the text
= Frequent pieces like "est" and "low" become single tokens.
? Roughly how many tokens is 750 English words?
+ About 1,000
- About 100
- About 7,500
= Rule of thumb: about ¾ of a word (4 characters) per token.
? Why are models often bad at counting the letters in a word?
+ They see tokens, which can hide individual letters
- They don't know the alphabet
- Letters cost more tokens than words
= "strawberry" might be one or two tokens, not ten letters.
:::

@@@ lesson
id: embeddings
title: Embeddings and similarity
minutes: 24
summary: Representing meaning as vectors of numbers, dot product and cosine similarity, finding the nearest neighbours of a query, bag-of-words vectors versus learned embeddings, and what embeddings are used for: search, recommendations, clustering and classification.
---
Inside a model, every token becomes a list of numbers called a **vector** or **embedding**. The numbers are learned during training so that texts with **similar meaning end up close together**: "dog" near "puppy", "invoice" near "receipt". Separate **embedding models** turn a whole sentence or document into one vector; comparing vectors then measures how related two texts are, which is the foundation of semantic search and RAG (Part 4).

![A 2-D map of word embeddings. Animal words (dog, puppy, cat, kitten) cluster in one corner, vehicle words (car, truck, bus) in another, and food words (pizza, pasta, bread) in a third. An arrow from "dog" to "puppy" has the same direction and length as the arrow from "cat" to "kitten"](figures/embedding-space.svg)

Real embeddings have hundreds to a few thousand dimensions (often 256 to 3,072), not two; the picture squashes them down to show the idea.

### Measuring similarity

| Measure | Formula | Notes |
|---|---|---|
| **Dot product** | a · b = Σ aᵢ bᵢ | grows with vector length as well as direction |
| **Cosine similarity** | (a · b) / (‖a‖ ‖b‖) | the angle only: 1 = same direction, 0 = unrelated, −1 = opposite |
| **Euclidean distance** | √Σ (aᵢ − bᵢ)² | straight-line distance; smaller = more similar |

Most embedding models return **normalised** vectors (length 1), and then the dot product and cosine similarity are identical: the dot product is the cheapest to compute, so vector databases use it.

```python
import math

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(a):
    return math.sqrt(dot(a, a))

def cosine(a, b):
    return dot(a, b) / (norm(a) * norm(b))

dog, puppy, car = [0.9, 0.8, 0.1], [0.85, 0.9, 0.05], [0.1, 0.2, 0.95]
print(round(cosine(dog, puppy), 3), round(cosine(dog, car), 3))
print(round(cosine([1, 2, 3], [2, 4, 6]), 3), "(same direction, different length)")
```

With NumPy, the same maths runs on thousands of vectors at once:

```python
import numpy as np

docs = np.array([[0.9, 0.8, 0.1],      # "dog"
                 [0.85, 0.9, 0.05],    # "puppy"
                 [0.1, 0.2, 0.95],     # "car"
                 [0.2, 0.1, 0.9]])     # "truck"
names = ["dog", "puppy", "car", "truck"]
docs = docs / np.linalg.norm(docs, axis=1, keepdims=True)   # normalise each row to length 1

query = np.array([0.15, 0.15, 0.9])
query = query / np.linalg.norm(query)
scores = docs @ query                      # one matrix-vector product = all cosine similarities
for i in np.argsort(-scores):              # best first
    print(f"{names[i]:6} {scores[i]:.3f}")
```

### Where do the vectors come from?

A simple, transparent starting point is a **bag of words**: one dimension per vocabulary word, counting how often it appears. It captures shared words but not meaning ("car" and "automobile" share nothing). **Learned embeddings** from a neural model capture meaning, synonyms and even cross-language similarity.

```python
from collections import Counter
import math

def bag_of_words(text, vocab):
    counts = Counter(text.lower().split())
    return [counts[w] for w in vocab]

def cosine(a, b):
    d = sum(x * y for x, y in zip(a, b))
    return d / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)

docs = ["the cat sat on the mat", "a dog chased the cat", "stock prices fell sharply today"]
vocab = sorted({w for d in docs for w in d.split()})
vectors = [bag_of_words(d, vocab) for d in docs]
query = bag_of_words("where did the cat sit", vocab)
for d, v in zip(docs, vectors):
    print(f"{cosine(query, v):.2f}  {d}")
```

In practice you call an embedding model through an API (or run an open model locally). Anthropic recommends Voyage AI for embeddings; OpenAI, Google, Cohere and open-source models (such as those on Hugging Face) are common choices:

```py-static
import voyageai                                     # pip install voyageai
vo = voyageai.Client()                              # reads VOYAGE_API_KEY
result = vo.embed(["The cat sat on the mat.", "Stock prices fell."], model="voyage-3.5", input_type="document")
print(len(result.embeddings[0]))                    # the vector size

from openai import OpenAI                           # pip install openai
client = OpenAI()                                   # reads OPENAI_API_KEY
resp = client.embeddings.create(model="text-embedding-3-small", input=["The cat sat on the mat."])
print(len(resp.data[0].embedding))
```

Model names and sizes change; check the provider's documentation for the current recommended model.

### What embeddings are used for

| Use | How |
|---|---|
| **Semantic search** and **RAG** | embed documents once; embed each query; return the most similar documents |
| **Recommendations** | "more like this": nearest neighbours of an item's vector |
| **Clustering** | group similar support tickets or reviews (k-means on the vectors) |
| **Classification** | train a small classifier (logistic regression) on the vectors |
| **De-duplication** | near-identical vectors flag near-duplicate texts |
| **Anomaly detection** | a vector far from everything else is unusual |

:::exercise Cosine similarity
Write `cosine_similarity(a, b)` for two equal-length lists of numbers. Return 0.0 if either vector is all zeros (the formula would divide by zero).
```python starter
import math

def cosine_similarity(a, b):
    pass

print(cosine_similarity([1, 0], [0, 1]))      # 0.0: perpendicular
print(cosine_similarity([1, 2, 3], [2, 4, 6]))  # 1.0: same direction
```
```python check
fn = need("cosine_similarity")
test(fn, cases=[
    (([1, 0], [0, 1]), 0.0, "perpendicular vectors"),
    (([1, 2, 3], [2, 4, 6]), 1.0, "same direction, different length"),
    (([1, 0], [-1, 0]), -1.0, "opposite directions"),
    (([0, 0, 0], [1, 2, 3]), 0.0, "a zero vector"),
    (([3, 4], [4, 3]), 0.96, "an angle in between"),
    (([0.9, 0.8, 0.1], [0.85, 0.9, 0.05]), 0.9953, "dog vs puppy (rounded)"),
], valid=None, key=lambda v: round(v, 5) if isinstance(v, (int, float)) else v)
```
```python solution
import math

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0                              # undefined for a zero vector: treat as unrelated
    return dot / (norm_a * norm_b)

print(cosine_similarity([1, 0], [0, 1]))
print(cosine_similarity([1, 2, 3], [2, 4, 6]))
```
hint: Cosine similarity is the dot product divided by the product of the two lengths.
hint: Dot product: `sum(x * y for x, y in zip(a, b))`. Length: `math.sqrt(sum(x * x for x in a))`.
hint: If either length is 0, return 0.0 before dividing.
approach:
1. **Understand:** angle-based similarity in [−1, 1]; zero vectors give 0.0.
2. **Examples:** [1, 2, 3] vs [2, 4, 6] → 1.0 (same direction).
3. **Brute force:** index loops: fine.
4. **Pattern:** **dot product / (norm × norm)**.
5. **Plan:** compute the dot and both norms, guard zeros, divide.
6. **Code and test:** perpendicular, opposite, zero vector.
walkthrough:
**Line by line**

- The dot product multiplies matching coordinates and adds them up.
- Each norm is the square root of a vector's dot product with itself, its length.
- Dividing by both lengths removes the effect of magnitude, leaving only direction.

**Trace** for [3, 4] and [4, 3]: dot = 12 + 12 = 24; norms 5 and 5; 24 / 25 = 0.96.

**Complexity:** O(d) for d dimensions.

**Common wrong approach:** returning the raw dot product, which rates long vectors as "more similar" just because they're longer.
:::

:::exercise Top-k nearest documents
`docs` maps a document name to its vector. Write `top_k(query, docs, k)` returning the names of the `k` documents most similar to `query` by cosine similarity, most similar first (ties broken alphabetically by name). Assume no zero vectors. This is the heart of semantic search.
```python starter
import math

def top_k(query, docs, k):
    pass

docs = {"dog": [0.9, 0.8, 0.1], "puppy": [0.85, 0.9, 0.05], "car": [0.1, 0.2, 0.95], "truck": [0.2, 0.1, 0.9]}
print(top_k([0.15, 0.15, 0.9], docs, 2))   # ['car', 'truck']
```
```python check
fn = need("top_k")
_d = {"dog": [0.9, 0.8, 0.1], "puppy": [0.85, 0.9, 0.05], "car": [0.1, 0.2, 0.95], "truck": [0.2, 0.1, 0.9]}
test(fn, cases=[
    (([0.15, 0.15, 0.9], _d, 2), ["car", "truck"], "vehicles"),
    (([1.0, 1.0, 0.0], _d, 1), ["puppy"], "the single best match"),
    (([1.0, 0.9, 0.0], _d, 4), ["dog", "puppy", "truck", "car"], "rank everything"),
    (([0.0, 0.0, 1.0], _d, 0), [], "k = 0"),
    (([1.0, 0.0], {"b": [2.0, 0.0], "a": [5.0, 0.0], "c": [0.0, 1.0]}, 2), ["a", "b"], "a tie broken by name"),
    (([0.5, 0.5, 0.5], _d, 10), ["dog", "puppy", "truck", "car"], "k larger than the number of documents"),
])
```
```python solution
import math

def top_k(query, docs, k):
    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    scored = [(-cosine(query, vec), name) for name, vec in docs.items()]
    scored.sort()                                  # highest similarity first, then by name
    return [name for _, name in scored[:k]]

docs = {"dog": [0.9, 0.8, 0.1], "puppy": [0.85, 0.9, 0.05], "car": [0.1, 0.2, 0.95], "truck": [0.2, 0.1, 0.9]}
print(top_k([0.15, 0.15, 0.9], docs, 2))
```
hint: Score every document against the query, then keep the best k.
hint: Build a list of `(score, name)` pairs and sort it. To get the highest score first but alphabetical names on ties, sort by `(-score, name)`.
hint: `scored = sorted((-cosine(query, v), name) for name, v in docs.items())`, then `[name for _, name in scored[:k]]`. For huge collections, `heapq.nsmallest(k, ...)` avoids sorting everything.
approach:
1. **Understand:** rank by cosine similarity, descending; ties by name; k may exceed the number of docs.
2. **Examples:** a "vehicle-like" query returns car, then truck.
3. **Brute force:** this **is** brute-force (exact) nearest-neighbour search: O(n · d) per query, perfect up to a few hundred thousand vectors.
4. **Pattern:** **score everything, sort, slice** (or a heap for top k).
5. **Plan:** cosine per doc → sort by (−score, name) → first k names.
6. **Code and test:** k = 0, k larger than n, ties.
walkthrough:
**Line by line**

- Negating the score turns "highest first" into an ascending sort, so the tuple sort handles ties by name automatically.
- `scored[:k]` copes with k = 0 (empty list) and k > n (all documents).
- The cosine helper normalises both vectors, so magnitude doesn't matter: [2, 0] and [5, 0] score the same against [1, 0], and the name decides.

**Trace** for the query [1.0, 0.0] with a: [5, 0], b: [2, 0], c: [0, 1]: scores 1, 1, 0 → sorted (−1, a), (−1, b), (0, c) → ["a", "b"].

**Complexity:** O(n · d + n log n) per query. Vector databases use approximate indexes to avoid scoring every vector (Lesson 21).

**Common wrong approach:** sorting with `reverse=True` on `(score, name)`, which reverses the name order too, so ties come out in reverse alphabetical order.
:::

:::quiz
? What does it mean for two embeddings to have cosine similarity close to 1?
+ They point in nearly the same direction: the texts are closely related in meaning
- They have the same length
- They contain exactly the same words
= Cosine similarity ignores length and measures the angle.
? Why are dot product and cosine similarity the same for normalised vectors?
+ Normalised vectors have length 1, so dividing by the lengths changes nothing
- Because both use subtraction
- They're never the same
= That's why vector databases often just use the dot product.
? Which representation knows that "car" and "automobile" are related?
+ A learned embedding from a neural model
- A bag-of-words count vector
- A one-hot vector
= Bag of words only matches identical words.
? Which task is NOT a typical use of embeddings?
+ Exact arithmetic on large numbers
- Semantic search
- Clustering similar documents
= Embeddings capture meaning, not precise calculation.
:::

@@@ lesson
id: attention
title: Transformers and attention
minutes: 24
summary: How a transformer turns tokens into predictions: token and position embeddings, self-attention with queries, keys and values, softmax, multiple heads and stacked layers, why long contexts are expensive, and the KV cache.
---
Almost every modern LLM is a **transformer**, an architecture introduced in 2017 ("Attention Is All You Need"). You don't need its full mathematics to build with LLMs, but knowing the shape of it explains context windows, costs and many model behaviours.

### From tokens to a prediction

1. Each token ID is looked up in an **embedding table**, giving one vector per token. **Position information** is added, so the model knows word order.
2. A stack of **transformer layers** (dozens in large models) updates every token's vector. Each layer has two parts:
   - **Self-attention:** each token gathers information from the other tokens that matter to it.
   - A **feed-forward network:** processes each token's vector on its own.
3. The final vector of the **last** token is turned into a score (a **logit**) for every token in the vocabulary; **softmax** turns the scores into probabilities for the next token (Lesson 5).

![A stack: input tokens at the bottom go through an embedding layer, then N repeated transformer blocks (self-attention, then a feed-forward network), then an output layer producing a probability for every vocabulary token for the next position](figures/transformer.svg)

### Softmax: from scores to probabilities

Softmax turns any list of scores into positive numbers that add up to 1, keeping their order and exaggerating the gaps: `softmax(x)ᵢ = exp(xᵢ) / Σ exp(xⱼ)`. Subtracting the maximum score first gives the same result without overflowing.

```python
import math

def softmax(scores):
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]     # subtract the max: same result, no overflow
    total = sum(exps)
    return [e / total for e in exps]

print([round(p, 3) for p in softmax([2.0, 1.0, 0.1])])
print([round(p, 3) for p in softmax([1000, 999, 998])])   # would overflow without the max trick
```

### Self-attention: queries, keys and values

In "The animal didn't cross the street because **it** was too tired", the vector for "it" needs information from "animal". Attention does this with three vectors per token, each made by multiplying the token's vector by a learned matrix:

- a **query** (q): "what am I looking for?"
- a **key** (k): "what do I contain?"
- a **value** (v): "what information do I pass on?"

Each token compares its query with every token's key (a dot product), scales the scores by √d, turns them into weights with softmax, and takes the weighted average of the values: **attention(Q, K, V) = softmax(QKᵀ / √d) V**. In models that generate text, a **causal mask** stops a token from attending to tokens that come after it.

![An attention heatmap for the sentence "the animal was tired because it". Rows are the tokens doing the attending, columns the tokens attended to. The row for "it" puts most of its weight on "animal". Cells above the diagonal are blank: each token can only attend to itself and earlier tokens](figures/attention.svg)

```python
import numpy as np

rng = np.random.default_rng(0)
tokens = ["the", "cat", "sat"]
d = 4
X = rng.normal(size=(3, d))                       # one embedding per token (made up)
Wq, Wk, Wv = (rng.normal(size=(d, d)) for _ in range(3))
Q, K, V = X @ Wq, X @ Wk, X @ Wv                  # queries, keys, values

scores = Q @ K.T / np.sqrt(d)                     # every query against every key
mask = np.triu(np.ones((3, 3), dtype=bool), k=1)  # causal mask: no looking ahead
scores[mask] = -np.inf
weights = np.exp(scores - scores.max(axis=1, keepdims=True))
weights /= weights.sum(axis=1, keepdims=True)     # softmax along each row
out = weights @ V                                 # each token: a weighted mix of the values

print(np.round(weights, 2))                       # row i: how much token i attends to each token
print(out.shape)
```

Real models run many attention **heads** in parallel (each can track a different kind of relationship, such as grammar or coreference), across dozens of layers, with vectors of thousands of dimensions.

### Why this matters when you build

- **Context windows:** attention compares every token with every other, so its cost grows roughly with the **square** of the sequence length. Engineering tricks have pushed windows past a million tokens, but long prompts still cost more and take longer.
- **Output is slower than input:** the whole prompt is processed in parallel, but output tokens are generated **one at a time**, each needing a pass through the model.
- **The KV cache:** during generation, keys and values of earlier tokens are stored and reused rather than recomputed. Providers extend this idea across requests with **prompt caching** (Lesson 11): a repeated prompt prefix can be cheaper and faster.
- **Position matters:** models can pay less attention to material buried in the middle of a very long context, so put key instructions and the most relevant documents where they're easy to find, and test it.

:::exercise Softmax
Write `softmax(scores)` returning a list of probabilities: `exp(score)` for each score divided by the sum of all of them. Subtract the maximum score first so huge scores like 1000 don't overflow.
```python starter
import math

def softmax(scores):
    pass

print(softmax([2.0, 1.0, 0.1]))   # about [0.659, 0.242, 0.099]
```
```python check
import math as _m
fn = need("softmax")
def _sm(xs):
    m = max(xs); e = [_m.exp(x - m) for x in xs]; t = sum(e); return [v / t for v in e]
test(fn, cases=[
    (([2.0, 1.0, 0.1],), _sm([2.0, 1.0, 0.1]), "the example"),
    (([0.0, 0.0],), [0.5, 0.5], "equal scores"),
    (([5.0],), [1.0], "a single score"),
    (([1000.0, 999.0],), _sm([1000.0, 999.0]), "huge scores (no overflow)"),
    (([-1000.0, 0.0],), _sm([-1000.0, 0.0]), "a very negative score"),
    (([1.0, 2.0, 3.0, 4.0],), _sm([1.0, 2.0, 3.0, 4.0]), "four scores"),
])
```
```python solution
import math

def softmax(scores):
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]   # largest exponent is exp(0) = 1: no overflow
    total = sum(exps)
    return [e / total for e in exps]

print(softmax([2.0, 1.0, 0.1]))
```
hint: Exponentiate each score, then divide each by the total so they add up to 1.
hint: `math.exp(1000)` overflows. Subtracting the same number from every score doesn't change the result, because it cancels out in the division.
hint: `m = max(scores)`; `exps = [math.exp(s - m) for s in scores]`; return each `e / sum(exps)`.
approach:
1. **Understand:** positive outputs that sum to 1, same order as the inputs; must survive huge scores.
2. **Examples:** [0, 0] → [0.5, 0.5]; [5] → [1.0].
3. **Brute force:** `exp` without the max shift: overflows on [1000, 999].
4. **Pattern:** **numerically stable softmax** (subtract the max).
5. **Plan:** shift, exponentiate, normalise.
6. **Code and test:** huge, very negative, single scores.
walkthrough:
**Line by line**

- exp(s − m) = exp(s) / exp(m); the exp(m) factor appears in every term and the total, so it cancels.
- After the shift the largest exponent is 0, giving exp(0) = 1, so nothing overflows; very negative values safely become 0.0.
- Dividing by the total makes the outputs sum to 1.

**Trace** for [2.0, 1.0, 0.1]: shift by 2 → [0, −1, −1.9]; exps ≈ [1, 0.368, 0.150]; total ≈ 1.518 → [0.659, 0.242, 0.099].

**Complexity:** O(n).

**Common wrong approach:** dividing each score by the sum of scores. That's not softmax: it fails for negative scores and doesn't exaggerate the gaps.
:::

:::exercise Attention weights for one query
Write `attention_weights(query, keys)` for one query vector and a list of key vectors (all of length d). Return the softmax of the scaled dot products: `softmax([dot(query, k) / sqrt(d) for k in keys])`, as a list.
```python starter
import math

def attention_weights(query, keys):
    pass

print(attention_weights([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]))   # the first key gets more weight
```
```python check
import math as _m
fn = need("attention_weights")
def _ref(q, ks):
    d = len(q); s = [sum(a * b for a, b in zip(q, k)) / _m.sqrt(d) for k in ks]
    m = max(s); e = [_m.exp(x - m) for x in s]; t = sum(e); return [v / t for v in e]
test(fn, cases=[
    (([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]), _ref([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]), "two keys"),
    (([0.0, 0.0], [[1.0, 2.0], [3.0, 4.0]]), [0.5, 0.5], "a zero query attends evenly"),
    (([1.0, 1.0, 1.0, 1.0], [[1.0, 1.0, 1.0, 1.0]]), [1.0], "a single key"),
    (([2.0, 0.0, 0.0, 0.0], [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [1.0, 1.0, 0, 0]]), _ref([2.0, 0.0, 0.0, 0.0], [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [1.0, 1.0, 0, 0]]), "scaled by sqrt(4) = 2"),
    (([30.0, 30.0], [[30.0, 30.0], [-30.0, -30.0]]), _ref([30.0, 30.0], [[30.0, 30.0], [-30.0, -30.0]]), "large scores stay stable"),
])
```
```python solution
import math

def attention_weights(query, keys):
    d = len(query)
    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(d) for key in keys]   # scaled dot products
    m = max(scores)
    exps = [math.exp(s - m) for s in scores]                                          # stable softmax
    total = sum(exps)
    return [e / total for e in exps]

print(attention_weights([1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]))
```
hint: Two steps: a score for each key, then softmax over the scores.
hint: Each score is the dot product of the query and that key, divided by `math.sqrt(d)` where d is the vector length.
hint: Reuse your stable softmax: subtract the max score before `math.exp`.
approach:
1. **Understand:** one query, many keys; weights must sum to 1; scale by √d.
2. **Examples:** a zero query gives equal scores, so equal weights.
3. **Brute force:** loops are fine; NumPy would do `softmax(K @ q / sqrt(d))`.
4. **Pattern:** **scaled dot-product attention** for a single row.
5. **Plan:** scores → stable softmax.
6. **Code and test:** a single key, a zero query, large scores.
walkthrough:
**Line by line**

- The dot product measures how well each key matches what the query is looking for.
- Dividing by √d keeps scores from growing with the vector size, which would make softmax too peaky.
- The stable softmax turns the scores into weights that sum to 1.

**Trace** for q = [1, 0], keys [1, 0] and [0, 1]: scores 1/√2 ≈ 0.707 and 0 → softmax ≈ [0.670, 0.330].

**Complexity:** O(n · d) for n keys: done for every token, that's the O(n² · d) cost of attention.

**Common wrong approach:** forgetting the √d scaling, which gives the right ordering but the wrong (too extreme) weights.
:::

:::quiz
? In self-attention, what does a token's query get compared with?
+ The keys of the tokens it can attend to
- The values of every token
- The vocabulary
= Query–key dot products decide the attention weights; values are what gets mixed.
? Why do long prompts cost more time and compute?
+ Attention compares tokens pairwise, so cost grows roughly with the square of the length
- Each token is processed by a different model
- Long prompts are sent over the network twice
= That's also why context windows have limits.
? What does the causal mask do in a text-generating model?
+ Stops each token from attending to tokens after it
- Hides offensive words
- Removes padding tokens from the output
= The model must predict the future without seeing it.
? Why is generating output slower per token than reading input?
+ Output tokens are produced one at a time, each needing a pass through the model
- Output tokens are longer
- Input is cached on disk
= The prompt can be processed in parallel; generation can't.
:::

@@@ lesson
id: sampling
title: Sampling and temperature
minutes: 22
summary: How the next token is chosen from the model's probabilities: greedy decoding, random sampling, temperature, top-k and top-p (nucleus) sampling, stop sequences and maximum length, and when to use which settings.
---
At every step the model produces a **logit** (a score) for each token in its vocabulary; softmax turns them into probabilities. **Sampling** is how one token is picked. These settings are what you control when you call a model, and they change the character of the output a lot.

![Bar charts of the probabilities of five candidate next tokens at three temperatures. At temperature 0.2 almost all the probability is on the top token; at 1.0 the original distribution; at 2.0 the bars are much flatter, so unlikely tokens get picked more often](figures/temperature.svg)

### Greedy decoding

Always take the most likely token. Deterministic for a given model and prompt, but it can be repetitive and bland, and it's not necessarily the most likely **sequence** overall.

### Temperature

Divide every logit by a **temperature** T before softmax:

- **T < 1** sharpens the distribution: the top tokens get even more likely. More focused and consistent.
- **T = 1** uses the model's own probabilities.
- **T > 1** flattens it: unlikely tokens get picked more often. More varied, and more likely to go off track.
- **T → 0** approaches greedy decoding.

```python
import math

def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    return [v / sum(e) for v in e]

tokens = [" Paris", " a", " the", " located", " beautiful"]
logits = [6.0, 2.5, 2.0, 1.5, 1.0]
for t in (0.2, 1.0, 2.0):
    probs = softmax([l / t for l in logits])
    print(f"T={t}: " + "  ".join(f"{tok.strip()}={p:.2f}" for tok, p in zip(tokens, probs)))
```

### Top-k and top-p

Even at moderate temperatures, thousands of very unlikely tokens together hold a noticeable share of the probability, and one bad pick can derail a response. Two filters cut them off before sampling:

- **Top-k:** keep only the k most likely tokens.
- **Top-p (nucleus sampling):** keep the smallest set of top tokens whose probabilities add up to at least p (say 0.9), then renormalise. It adapts: when the model is confident the set is tiny, when it's unsure the set grows.

```python
import random

def top_p(probs, p):
    ranked = sorted(probs.items(), key=lambda kv: -kv[1])
    kept, total = {}, 0.0
    for token, prob in ranked:
        kept[token] = prob
        total += prob
        if total >= p:
            break                                  # the nucleus is complete
    return {t: q / total for t, q in kept.items()} # renormalise to sum to 1

probs = {"Paris": 0.80, "Lyon": 0.08, "France": 0.05, "the": 0.04, "banana": 0.03}
nucleus = top_p(probs, 0.9)
print({t: round(q, 3) for t, q in nucleus.items()})

rng = random.Random(42)
print([rng.choices(list(nucleus), weights=list(nucleus.values()))[0] for _ in range(10)])
```

### Other generation settings

| Setting | What it does |
|---|---|
| **max tokens** | the longest output allowed; the response stops (and says why) if it's reached |
| **stop sequences** | strings that end generation early, such as `"\n\n"` or `"</answer>"` |
| **seed** (some APIs) | makes sampling repeatable, although results can still vary across model versions and hardware |

### Choosing settings

| Task | Typical settings |
|---|---|
| Extraction, classification, code, factual Q&A | low temperature (0 to 0.3): consistent, focused |
| General assistant, explanations | the provider's default (often 1.0) |
| Brainstorming, creative writing, varied test data | higher temperature (around 1.0 or more), or several samples |

Some notes for current models:

- Even at temperature 0, outputs are not guaranteed to be identical every time. Design and test for some variation.
- Many providers recommend adjusting **either** temperature **or** top-p, not both.
- Reasoning models, and models with thinking turned on, may fix or limit sampling settings. Check the model's documentation.

:::exercise Apply a temperature
Write `with_temperature(logits, t)` returning the probabilities after dividing every logit by temperature `t` (> 0) and applying a numerically stable softmax.
```python starter
import math

def with_temperature(logits, t):
    pass

print(with_temperature([2.0, 1.0], 1.0))   # about [0.731, 0.269]
print(with_temperature([2.0, 1.0], 0.5))   # sharper: about [0.881, 0.119]
```
```python check
import math as _m
fn = need("with_temperature")
def _ref(ls, t):
    s = [l / t for l in ls]; m = max(s); e = [_m.exp(x - m) for x in s]; tot = sum(e); return [v / tot for v in e]
test(fn, cases=[
    (([2.0, 1.0], 1.0), _ref([2.0, 1.0], 1.0), "temperature 1"),
    (([2.0, 1.0], 0.5), _ref([2.0, 1.0], 0.5), "a lower temperature sharpens"),
    (([2.0, 1.0], 4.0), _ref([2.0, 1.0], 4.0), "a higher temperature flattens"),
    (([3.0, 3.0, 3.0], 0.7), [1 / 3, 1 / 3, 1 / 3], "equal logits stay equal"),
    (([10.0, 0.0], 0.01), _ref([10.0, 0.0], 0.01), "a tiny temperature (no overflow)"),
])
```
```python solution
import math

def with_temperature(logits, t):
    scaled = [l / t for l in logits]          # T < 1 widens the gaps, T > 1 narrows them
    m = max(scaled)
    exps = [math.exp(s - m) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]

print(with_temperature([2.0, 1.0], 1.0))
print(with_temperature([2.0, 1.0], 0.5))
```
hint: Temperature is applied to the logits, before softmax.
hint: Divide each logit by t, then do the usual stable softmax: subtract the max, exponentiate, normalise.
hint: With t = 0.01, the scaled logits are 1000 and 0: without subtracting the max, `math.exp(1000)` overflows.
approach:
1. **Understand:** scale logits by 1/t, then softmax; t > 0.
2. **Examples:** [2, 1] at t = 0.5 → logits [4, 2] → [0.881, 0.119].
3. **Brute force:** none: it's a formula.
4. **Pattern:** **temperature scaling + stable softmax**.
5. **Plan:** divide, shift by the max, exponentiate, normalise.
6. **Code and test:** equal logits, a tiny temperature, a large one.
walkthrough:
**Line by line**

- Dividing by t < 1 multiplies the gaps between logits, so softmax favours the leader more; t > 1 shrinks the gaps.
- The stable softmax from Lesson 4 keeps a tiny temperature from overflowing.
- Equal logits stay equal at any temperature.

**Trace** for [2.0, 1.0] at t = 0.5: scaled [4, 2]; shifted [0, −2]; exps [1, 0.135]; probabilities [0.881, 0.119].

**Complexity:** O(n) for n tokens.

**Common wrong approach:** dividing the probabilities (instead of the logits) by t and renormalising, which doesn't change their ratios at all.
:::

:::exercise Nucleus (top-p) filtering
`probs` maps tokens to probabilities (summing to 1). Write `nucleus(probs, p)` that keeps the most likely tokens until their total probability reaches at least `p`, and returns them as a dict of renormalised probabilities (summing to 1). Ties in probability are broken alphabetically by token.
```python starter
def nucleus(probs, p):
    pass

print(nucleus({"Paris": 0.8, "Lyon": 0.1, "Rome": 0.06, "cat": 0.04}, 0.85))
# {'Paris': 0.888..., 'Lyon': 0.111...}
```
```python check
fn = need("nucleus")
test(fn, cases=[
    (({"Paris": 0.8, "Lyon": 0.1, "Rome": 0.06, "cat": 0.04}, 0.85), {"Paris": 0.8 / 0.9, "Lyon": 0.1 / 0.9}, "two tokens reach 0.85"),
    (({"Paris": 0.8, "Lyon": 0.1, "Rome": 0.06, "cat": 0.04}, 0.5), {"Paris": 1.0}, "the top token alone is enough"),
    (({"a": 0.5, "b": 0.3, "c": 0.2}, 1.0), {"a": 0.5, "b": 0.3, "c": 0.2}, "p = 1 keeps everything"),
    (({"b": 0.4, "a": 0.4, "c": 0.2}, 0.3), {"a": 1.0}, "a tie at the top, broken alphabetically"),
    (({"x": 0.25, "y": 0.25, "z": 0.25, "w": 0.25}, 0.5), {"w": 0.5, "x": 0.5}, "exactly reaching p stops there"),
])
```
```python solution
def nucleus(probs, p):
    ranked = sorted(probs.items(), key=lambda kv: (-kv[1], kv[0]))   # most likely first, ties by name
    kept, total = {}, 0.0
    for token, prob in ranked:
        kept[token] = prob
        total += prob
        if total >= p - 1e-12:            # reached p (with a tiny allowance for float rounding)
            break
    return {token: prob / total for token, prob in kept.items()}

print(nucleus({"Paris": 0.8, "Lyon": 0.1, "Rome": 0.06, "cat": 0.04}, 0.85))
```
hint: Sort the tokens from most to least likely, then add them one by one.
hint: Stop as soon as the running total is at least p. Then divide each kept probability by the total so they sum to 1.
hint: Sort with the key `lambda kv: (-kv[1], kv[0])` for "highest probability, then alphabetical". Floating-point sums like 0.25 + 0.25 are exact, but 0.1 + 0.2 isn't, so compare with a tiny tolerance.
approach:
1. **Understand:** the smallest top set reaching p; renormalise; ties alphabetical.
2. **Examples:** p = 0.85 keeps Paris (0.8) and Lyon (total 0.9).
3. **Brute force:** try every subset: pointless, since the best set is always a prefix of the sorted list.
4. **Pattern:** **sort + running total (prefix sum)** with an early stop.
5. **Plan:** sort, accumulate until ≥ p, renormalise.
6. **Code and test:** p = 1, ties at the top, totals that hit p exactly.
walkthrough:
**Line by line**

- Sorting by (−probability, token) puts the most likely tokens first and makes ties deterministic.
- Each token is added before checking the total, so at least one token is always kept.
- The loop stops at the first point the total reaches p; the result is the smallest such prefix.
- Dividing by `total` renormalises the kept probabilities.

**Trace** for p = 0.85: Paris → 0.8 (< 0.85), Lyon → 0.9 (≥ 0.85) stop; renormalised 0.889 and 0.111.

**Complexity:** O(n log n) for the sort.

**Common wrong approach:** keeping tokens whose individual probability is at least p, which is a different (and usually empty) set.
:::

:::quiz
? What does a temperature below 1 do?
+ Sharpens the distribution, making the most likely tokens even more likely
- Makes every token equally likely
- Stops the model from generating
= Dividing logits by T < 1 widens the gaps before softmax.
? What does top-p = 0.9 keep?
+ The smallest set of most likely tokens whose probabilities add up to at least 0.9
- Every token with probability at least 0.9
- The 90 most likely tokens
= The nucleus adapts to how confident the model is.
? Which settings suit extracting fields from invoices into JSON?
+ A low temperature, for consistent and focused output
- A high temperature, for creativity
- Top-k = 1 and temperature 2.0 together
= Extraction should give the same answer every time.
? Does temperature 0 guarantee identical outputs on every call?
+ No: small variations can still occur, so systems should tolerate them
- Yes, always
- Only on weekends
= Hardware and serving details can introduce tiny differences.
:::

@@@ lesson
id: choosing-a-model
title: Choosing a model
minutes: 20
summary: The trade-offs between models: capability, context window, output length, speed, price per input and output token, reasoning modes, modalities, open-weight versus hosted models, and a simple method for choosing, plus routing requests between models.
---
There is no single best model. Each request has a quality bar, a latency budget and a cost budget, and the right model is usually the **cheapest and fastest one that reliably clears the quality bar on your own evaluations** (Part 6).

### What differs between models

| Property | Why it matters |
|---|---|
| **Capability** | harder reasoning, coding and long multi-step agent tasks need stronger models |
| **Context window** | how much text (documents, history, tool results) fits in one request |
| **Max output** | the longest answer it can write in one response |
| **Latency** | time to the first token, and tokens per second after that |
| **Price** | per million input and output tokens; output is usually several times dearer |
| **Reasoning / thinking** | extra thinking tokens raise quality on hard tasks, and cost and latency too |
| **Modalities** | text, images, PDFs, audio; which inputs and outputs are supported |
| **Tool use, structured output, caching, batch** | API features your design may rely on |
| **Hosting** | a provider's API, a cloud platform (AWS Bedrock, Google Vertex AI, Azure), or open-weight models you run yourself |

### Families and tiers

Providers usually offer a **tier** of models in each generation: a large, most capable one; a balanced middle one; and a small, fast, cheap one. As of October 2026, Anthropic's current Claude models are:

| Model | API name | Context window | Positioning |
|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M tokens | demanding reasoning and long-horizon agentic work |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M tokens | long-running agentic coding and knowledge work; the recommended starting point |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | 1M tokens | balance of speed and intelligence |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K tokens | fastest, for high-volume and latency-sensitive work |

OpenAI, Google (Gemini) and others offer similar tiers, and **open-weight** model families (from Meta, Mistral, Alibaba's Qwen, DeepSeek and others) can be downloaded and run on your own hardware. Models are updated every few months, so always check the provider's current models and pricing pages before choosing; names, prices and limits in any course will date.

### Hosted API or open weights?

| | Hosted API | Open-weight, self-hosted |
|---|---|---|
| Quality | usually the frontier | strong and improving, often a step behind |
| Effort | an API key and a few lines of code | GPUs, serving software, scaling, updates |
| Cost | pay per token | pay for hardware, whether busy or idle |
| Data | sent to the provider (check its data policies and regional options) | stays on your infrastructure |
| Customisation | prompts, tools, some fine-tuning | full fine-tuning, quantisation, any changes |

### A practical method

1. **Write down the requirements:** the task, the quality bar, the latency budget (for example, a first token within 1 second for chat), the expected volume and the budget.
2. **Start with a strong model** to see what's possible, and build a small evaluation set of real examples (Part 6).
3. **Try cheaper and faster models** on the same set; keep the cheapest one that meets the bar.
4. **Route** if requests differ: send simple requests to a small model and hard ones to a large one (a rule, a classifier, or a small model deciding).
5. **Re-evaluate** when new models appear or your traffic changes.

```python
models = [
    {"name": "large",  "quality": 0.95, "latency_s": 6.0, "price_in": 10.0, "price_out": 50.0},
    {"name": "medium", "quality": 0.91, "latency_s": 2.5, "price_in": 2.0,  "price_out": 10.0},
    {"name": "small",  "quality": 0.84, "latency_s": 0.8, "price_in": 1.0,  "price_out": 5.0},
]

def monthly_cost(m, requests, tokens_in, tokens_out):
    return requests * (tokens_in * m["price_in"] + tokens_out * m["price_out"]) / 1_000_000

for m in models:
    print(f'{m["name"]:6} quality {m["quality"]:.2f}  latency {m["latency_s"]} s  '
          f'${monthly_cost(m, 300_000, 1_500, 300):,.0f} per month')
```

The "quality" numbers here are made up: in practice they come from **your** evaluation set, because public benchmark scores rarely predict how a model does on your specific task.

:::exercise Pick a model
Each model is a dict with `"name"`, `"quality"`, `"latency_s"`, `"price_in"` and `"price_out"` (dollars per million tokens). Write `pick_model(models, min_quality, max_latency, tokens_in, tokens_out)` returning the name of the model that meets `quality >= min_quality` and `latency_s <= max_latency` and is **cheapest** for a request of that size (ties broken by higher quality, then by name). Return `None` if no model qualifies.
```python starter
def pick_model(models, min_quality, max_latency, tokens_in, tokens_out):
    pass

models = [
    {"name": "large",  "quality": 0.95, "latency_s": 6.0, "price_in": 10.0, "price_out": 50.0},
    {"name": "medium", "quality": 0.91, "latency_s": 2.5, "price_in": 2.0,  "price_out": 10.0},
    {"name": "small",  "quality": 0.84, "latency_s": 0.8, "price_in": 1.0,  "price_out": 5.0},
]
print(pick_model(models, 0.9, 3.0, 1_500, 300))   # medium
```
```python check
fn = need("pick_model")
_m = [
    {"name": "large",  "quality": 0.95, "latency_s": 6.0, "price_in": 10.0, "price_out": 50.0},
    {"name": "medium", "quality": 0.91, "latency_s": 2.5, "price_in": 2.0,  "price_out": 10.0},
    {"name": "small",  "quality": 0.84, "latency_s": 0.8, "price_in": 1.0,  "price_out": 5.0},
]
_t = [
    {"name": "b", "quality": 0.9, "latency_s": 1.0, "price_in": 1.0, "price_out": 4.0},
    {"name": "a", "quality": 0.9, "latency_s": 1.0, "price_in": 2.0, "price_out": 3.0},
    {"name": "c", "quality": 0.95, "latency_s": 1.0, "price_in": 0.5, "price_out": 4.5},
]
test(fn, cases=[
    ((_m, 0.9, 3.0, 1_500, 300), "medium", "the example"),
    ((_m, 0.8, 1.0, 1_500, 300), "small", "a strict latency budget"),
    ((_m, 0.94, 10.0, 1_500, 300), "large", "a high quality bar"),
    ((_m, 0.99, 10.0, 1_500, 300), None, "no model is good enough"),
    ((_m, 0.9, 1.0, 1_500, 300), None, "good enough models are too slow"),
    ((_t, 0.85, 2.0, 1_000, 1_000), "c", "equal cost: the higher quality wins"),
    ((_t[:2], 0.85, 2.0, 1_000, 1_000), "a", "equal cost and quality: by name"),
])
```
```python solution
def pick_model(models, min_quality, max_latency, tokens_in, tokens_out):
    def cost(m):
        return (tokens_in * m["price_in"] + tokens_out * m["price_out"]) / 1_000_000
    eligible = [m for m in models if m["quality"] >= min_quality and m["latency_s"] <= max_latency]
    if not eligible:
        return None
    best = min(eligible, key=lambda m: (round(cost(m), 12), -m["quality"], m["name"]))
    return best["name"]

models = [
    {"name": "large",  "quality": 0.95, "latency_s": 6.0, "price_in": 10.0, "price_out": 50.0},
    {"name": "medium", "quality": 0.91, "latency_s": 2.5, "price_in": 2.0,  "price_out": 10.0},
    {"name": "small",  "quality": 0.84, "latency_s": 0.8, "price_in": 1.0,  "price_out": 5.0},
]
print(pick_model(models, 0.9, 3.0, 1_500, 300))
```
hint: First throw away every model that fails the quality or latency requirement.
hint: Among the rest, compute each model's cost for this request: `(tokens_in * price_in + tokens_out * price_out) / 1_000_000`.
hint: `min(eligible, key=lambda m: (cost(m), -m["quality"], m["name"]))` picks the cheapest, then the highest quality, then the first name. Return None if nothing is eligible.
approach:
1. **Understand:** hard constraints (quality, latency), then minimise cost; tie-breakers given.
2. **Examples:** quality ≥ 0.9 and latency ≤ 3 s → only medium qualifies (large is too slow, small isn't good enough).
3. **Brute force:** check every model: it **is** the right approach for a handful of models.
4. **Pattern:** **filter, then argmin with a tuple key**.
5. **Plan:** filter list → None if empty → min by (cost, −quality, name).
6. **Code and test:** nothing qualifies, cost ties, full ties.
walkthrough:
**Line by line**

- The list comprehension keeps only models meeting both requirements.
- `cost` turns per-million prices into the price of this request.
- The tuple key sorts by cost first; negating quality makes higher quality win ties; the name settles anything left. Rounding the cost avoids floating-point noise deciding a "tie".

**Trace** for the example (1,500 tokens in, 300 out, quality ≥ 0.9, latency ≤ 3 s):

| model | quality ok? | latency ok? | cost of this request |
|---|---|---|---|
| large | yes | no (6.0 s) | — |
| medium | yes | yes | (1,500 × 2 + 300 × 10) / 1,000,000 = $0.006 |
| small | no (0.84) | yes | — |

Only medium qualifies, so it's the answer.

**Complexity:** O(n) for n models.

**Common wrong approach:** comparing only the input price, which ignores that output tokens are several times dearer.
:::

:::quiz
? What is usually the right model for a task?
+ The cheapest, fastest model that reliably meets your quality bar on your own evaluations
- Always the largest model available
- Whichever has the highest public benchmark score
= Benchmarks rarely match your exact task; measure.
? Why do output tokens matter so much for cost?
+ They're typically priced several times higher than input tokens
- They're free
- They're counted twice
= Long answers, and thinking tokens, can dominate the bill.
? What is a key advantage of running an open-weight model yourself?
+ Your data stays on your infrastructure and you can customise the model fully
- It's always more capable than hosted models
- It needs no hardware
= The trade-off is the effort and cost of running it.
? What does routing mean in an LLM application?
+ Sending each request to a suitable model, such as simple ones to a small model and hard ones to a large one
- Sending every request to every model
- Choosing a random model per request
= It balances quality and cost across varied traffic.
:::
