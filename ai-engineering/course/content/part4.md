@@@ part
id: 4
title: Retrieval-Augmented Generation (RAG)
level: Intermediate
blurb: Answering from your own documents: the RAG pipeline, splitting documents into chunks, keyword search with BM25, vector search and vector databases, hybrid search and reranking, and measuring whether retrieval and answers are any good.

@@@ lesson
id: rag-pipeline
title: The RAG pipeline
minutes: 24
summary: Why models need your documents, retrieval-augmented generation step by step (ingest, retrieve, augment, generate), a tiny end-to-end RAG system, citing sources, saying "I don't know", when to skip retrieval and put everything in the prompt, and the API's built-in citations.
---
A model knows only what was in its training data, up to its **knowledge cutoff**. It has never seen your product manual, your company's policies or yesterday's support tickets. Ask about them and it will either refuse or, worse, **make up** a plausible answer.

**Retrieval-augmented generation (RAG)** fixes this by looking up the relevant passages first and putting them in the prompt, so the model answers from evidence rather than memory. It's like an open-book exam: the model still needs to read and reason, but the facts are in front of it.

### The pipeline

![Two rows. Ingestion, done ahead of time: documents are loaded and cleaned, split into chunks, embedded or indexed, and stored in a search index. Query time: the user's question is used to search the index, the top chunks are inserted into the prompt with the question, the model generates an answer citing the chunks, and the answer goes back to the user](figures/rag-pipeline.svg)

**Ingestion** (ahead of time, and again whenever documents change):

1. **Load and clean** the documents: PDFs, web pages, wiki pages, tickets. Strip navigation menus, headers and footers; keep titles and dates.
2. **Chunk** them into passages of a few hundred tokens (Lesson 18).
3. **Index** the chunks: a keyword index (Lesson 19), embeddings in a vector index (Lesson 20), or both (Lesson 21). Keep **metadata** with each chunk: source, title, date, access permissions.

**Query time** (on every question):

1. **Retrieve** the chunks most relevant to the question.
2. **Augment** the prompt: insert the chunks, each tagged with its source, then the question (Lesson 13's layout).
3. **Generate** an answer that uses only the provided chunks and **cites** them.

### A tiny RAG system

Real systems use better retrieval, but the shape is the same:

```python
import re

chunks = [
    {"source": "returns.md", "text": "Unused items can be returned within 30 days with a receipt."},
    {"source": "warranty.md", "text": "Frames have a lifetime warranty against manufacturing defects."},
    {"source": "repairs.md", "text": "Puncture repairs cost £12 and are usually done the same day."},
]

STOP = {"a", "an", "the", "how", "much", "does", "do", "is", "are", "and", "with", "can"}

def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP     # ignore common words

def retrieve(question, k=2):
    q = words(question)
    scored = sorted(chunks, key=lambda c: len(q & words(c["text"])), reverse=True)
    return [c for c in scored[:k] if q & words(c["text"])]

def build_prompt(question, found):
    docs = "\n".join(f'<document index="{i}"><source>{c["source"]}</source>\n{c["text"]}\n</document>'
                     for i, c in enumerate(found, start=1))
    return (f"<documents>\n{docs}\n</documents>\n\n"
            "Answer using only the documents above, citing them like [1]. "
            "If they don't contain the answer, say you don't know.\n\n"
            f"<question>{question}</question>")

question = "How much does a puncture repair cost?"
print(build_prompt(question, retrieve(question)))
```

Try removing `- STOP`: the word "a" alone then matches the returns chunk, which gets retrieved for a question about punctures. Crude scoring like this is why Lessons 19–21 build better retrieval.

The instructions matter as much as the retrieval:

- **"Use only the documents"** keeps the model from mixing in guesses from its training data.
- **"Say you don't know"** gives it an honest way out when retrieval missed. Without it, the model is pushed to answer anyway.
- **"Cite your sources"** lets users check the answer and lets you measure **groundedness** (Lesson 22).

### Citations built into the API

Claude can produce citations itself: send each source as a `document` block with citations enabled, and the reply's text blocks carry the exact passages they rely on.

```py-static
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": [
        {"type": "document",
         "source": {"type": "text", "media_type": "text/plain", "data": returns_policy_text},
         "title": "returns.md",
         "citations": {"enabled": True}},
        {"type": "text", "text": "Can I return a helmet I've worn once?"},
    ]}],
)
for block in response.content:
    if block.type == "text":
        print(block.text, [c.cited_text for c in (block.citations or [])])
```

Each citation includes the quoted text and its location (character range for text, page range for PDFs). The quoted `cited_text` doesn't count towards output tokens. Citations can't be combined with structured outputs in the same request.

### When you don't need retrieval

Retrieval adds moving parts, and every part can fail. Consider simpler options first:

- **The knowledge fits in the prompt.** With context windows of hundreds of thousands of tokens, a few hundred pages of documentation can simply be included, with prompt caching (Lesson 11) to keep repeat calls cheap. Anthropic's own guidance suggests this for knowledge bases up to roughly 200,000 tokens.
- **The data is structured.** Prices, stock levels and order status belong in a database; give the model a tool to query it (Part 5) rather than embedding rows as text.
- **The model already knows it.** General knowledge doesn't need retrieval; your private or fast-changing information does.

RAG earns its place when the corpus is **large** (thousands of documents and up), **changes often**, or needs **per-user permissions** (a user should only retrieve what they're allowed to read).

:::exercise A word-overlap retriever
Write `retrieve(question, chunks, k)` returning up to `k` chunks (dicts with a `"text"` key), best first:

- Tokenise with `re.findall(r"[a-z0-9]+", text.lower())`, and drop the stop words in `STOP`.
- A chunk's **score** is the number of **distinct** question words that also appear in the chunk.
- Sort by score, highest first; equal scores keep their original order. Leave out chunks with a score of 0.
```python starter
import re

STOP = {"a", "an", "the", "is", "are", "to", "of", "and", "in", "on", "for", "my", "i",
        "do", "does", "can", "what", "how", "you", "your", "it", "much"}

def retrieve(question, chunks, k):
    pass

chunks = [{"source": "returns.md", "text": "Unused items can be returned within 30 days with a receipt."},
          {"source": "warranty.md", "text": "Frames have a lifetime warranty against manufacturing defects."},
          {"source": "repairs.md", "text": "Puncture repairs cost £12 and are usually done the same day."}]
print(retrieve("How much does a puncture repair cost?", chunks, 2))
```
```python check
fn = need("retrieve")
_c = [{"source": "returns.md", "text": "Unused items can be returned within 30 days with a receipt."},
      {"source": "warranty.md", "text": "Frames have a lifetime warranty against manufacturing defects."},
      {"source": "repairs.md", "text": "Puncture repairs cost £12 and are usually done the same day."},
      {"source": "hours.md", "text": "We are open 9 to 5. Repairs are booked online."}]
test(fn, cases=[
    (("How much does a puncture repair cost?", _c, 2), [_c[2]], "only one chunk matches"),
    (("Can I book repairs for the same day?", _c, 3), [_c[2], _c[3]], "best first"),
    (("What is the warranty on frames?", _c, 5), [_c[1]], "k larger than the matches"),
    (("Hello there", _c, 2), [], "nothing matches"),
    (("Is it the 30 days?", _c, 2), [_c[0]], "numbers count; stop words don't"),
    (("repairs repairs repairs", _c, 4), [_c[2], _c[3]], "repeated words count once; ties keep order"),
    (("Returned items", _c, 0), [], "k = 0"),
], show="retrieve({0}, chunks, {2})")
```
```python solution
import re

STOP = {"a", "an", "the", "is", "are", "to", "of", "and", "in", "on", "for", "my", "i",
        "do", "does", "can", "what", "how", "you", "your", "it", "much"}

def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP

def retrieve(question, chunks, k):
    query = words(question)
    scored = [(len(query & words(chunk["text"])), chunk) for chunk in chunks]
    scored = [pair for pair in scored if pair[0] > 0]
    scored.sort(key=lambda pair: pair[0], reverse=True)    # stable: ties keep their order
    return [chunk for _, chunk in scored[:k]]

chunks = [{"source": "returns.md", "text": "Unused items can be returned within 30 days with a receipt."},
          {"source": "warranty.md", "text": "Frames have a lifetime warranty against manufacturing defects."},
          {"source": "repairs.md", "text": "Puncture repairs cost £12 and are usually done the same day."}]
print(retrieve("How much does a puncture repair cost?", chunks, 2))
```
hint: Turn the question and each chunk into **sets** of words (minus `STOP`); the size of the intersection `&` is the score.
hint: Pair each chunk with its score, drop the zeros, then sort by score with `reverse=True`. Python's sort is **stable**, so equal scores keep their original order.
hint: `scored.sort(key=lambda pair: pair[0], reverse=True)`, then take the chunks from the first `k` pairs.
approach:
1. **Understand:** score = shared distinct words; best first; stable ties; no zero scores; at most k.
2. **Examples:** "puncture repair cost" vs repairs.md: "puncture" and "cost" match, but "repair" doesn't match "repairs" (no stemming yet: Lesson 19).
3. **Brute force:** this is already a linear scan plus a sort.
4. **Pattern:** **score every document, sort, take the top k**: the skeleton of every retriever.
5. **Plan:** a `words` helper → scores → filter → stable sort → slice.
6. **Code and test:** ties, repeats, numbers, stop words, k = 0.
walkthrough:
**Line by line**

- Sets make repeated words count once and make the overlap a single `&`.
- Removing stop words stops "the" and "is" from matching every chunk.
- `sort(..., reverse=True)` keeps ties in their original order, because Python's sort is stable even when reversed.
- Slicing `[:k]` handles `k` larger than the number of matches, and `k = 0`.

**Trace** on "Can I book repairs for the same day?": query words {book, repairs, same, day}; repairs.md matches {repairs, same, day} = 3; hours.md matches only {repairs} = 1, because "booked" isn't "book" → [repairs.md, hours.md].

**Complexity:** O(n · m + n log n) for n chunks of m words.

**Common wrong approach:** counting raw word occurrences, so a chunk that repeats "the bike" ten times outranks the one that answers the question. Real keyword search (BM25, Lesson 19) weighs rare words more and long chunks less.
:::

:::exercise Check an answer's citations
The model was told to cite documents like `[1]`. Write `check_citations(answer, n_docs)` returning a dict:

- `"cited"`: the sorted, distinct citation numbers from 1 to `n_docs`;
- `"invalid"`: the sorted, distinct citation numbers outside that range;
- `"unsupported"`: the sentences that contain no citation at all, in order.

A citation is `[` digits `]`. Split sentences with `re.split(r"(?<=[.!?])\s+", answer.strip())`, ignoring empty pieces.
```python starter
import re

def check_citations(answer, n_docs):
    pass

answer = "Puncture repairs cost £12 [3]. They're usually same-day [3]. We also sell tubes."
print(check_citations(answer, 3))
# {'cited': [3], 'invalid': [], 'unsupported': ['We also sell tubes.']}
```
```python check
fn = need("check_citations")
test(fn, cases=[
    (("Puncture repairs cost £12 [3]. They're usually same-day [3]. We also sell tubes.", 3),
     {"cited": [3], "invalid": [], "unsupported": ["We also sell tubes."]}, "one unsupported sentence"),
    (("Returns take 30 days [1][2]. Frames have a lifetime warranty [2].", 2),
     {"cited": [1, 2], "invalid": [], "unsupported": []}, "fully cited"),
    (("See [4] and [0]. Also [2].", 3), {"cited": [2], "invalid": [0, 4], "unsupported": []}, "out-of-range numbers"),
    (("I don't know.", 3), {"cited": [], "invalid": [], "unsupported": ["I don't know."]}, "no citations"),
    (("", 3), {"cited": [], "invalid": [], "unsupported": []}, "empty answer"),
    (("Yes! [1] Really? Yes [10].", 12), {"cited": [1, 10], "invalid": [], "unsupported": ["Yes!"]}, "a citation after the punctuation"),
    (("Prices are in [GBP] [1].", 1), {"cited": [1], "invalid": [], "unsupported": []}, "brackets without digits aren't citations"),
], show="check_citations({0}, {1})")
```
```python solution
import re

def check_citations(answer, n_docs):
    numbers = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", answer.strip()) if s]
    return {
        "cited": sorted(n for n in numbers if 1 <= n <= n_docs),
        "invalid": sorted(n for n in numbers if not 1 <= n <= n_docs),
        "unsupported": [s for s in sentences if not re.search(r"\[\d+\]", s)],
    }

answer = "Puncture repairs cost £12 [3]. They're usually same-day [3]. We also sell tubes."
print(check_citations(answer, 3))
```
hint: `re.findall(r"\[(\d+)\]", answer)` returns the digits inside every citation, as strings.
hint: Put the numbers in a set (distinct), then split them into valid (`1 <= n <= n_docs`) and invalid, each sorted.
hint: Split the answer into sentences with the given regex, drop empty strings, and keep those where `re.search(r"\[\d+\]", sentence)` finds nothing.
approach:
1. **Understand:** three facts about an answer: which sources it used, which numbers are bogus, which claims have no source.
2. **Examples:** "Yes! [1] Really? Yes [10]." splits into "Yes!", "[1] Really?" and "Yes [10]."; the `[1]` lands at the start of the second piece.
3. **Brute force:** scanning characters by hand: more code, same result.
4. **Pattern:** **regex extraction plus set arithmetic**.
5. **Plan:** numbers → valid/invalid; sentences → those without a citation.
6. **Code and test:** out-of-range numbers, repeats, empty answers, non-numeric brackets.
walkthrough:
**Line by line**

- The capture group `(\d+)` returns just the digits; `int` converts them; the set removes repeats.
- `1 <= n <= n_docs` is a chained comparison, Python's neat way to test a range.
- The look-behind `(?<=[.!?])` splits **after** sentence-ending punctuation, keeping it in the sentence.
- `if s` drops the empty string that `re.split` returns for an empty answer.

**Trace** on the last-but-one case: the pieces are "Yes!", "[1] Really?" and "Yes [10]." The `[1]` was meant for "Yes!", but because it comes after the `!`, it lands in the next piece, so "Yes!" is reported as unsupported. With 12 documents, 1 and 10 are both valid.

That's a real limitation of splitting on punctuation: a citation placed **after** the full stop ("…same day. [3]") attaches to the following sentence. Prompt the model to put citations **before** the full stop, and treat this check as a cheap signal, not proof. (Lesson 22 measures groundedness properly.)

**Complexity:** O(n) for an answer of n characters.

**Common wrong approach:** trusting citations blindly. A citation number can be out of range, or point at a document that doesn't actually support the sentence; checking the numbers is the cheap first step.
:::

:::quiz
? What problem does RAG solve?
+ The model lacks your private or recent information, so you retrieve it and put it in the prompt
- The model is too slow
- The model's context window is too small for any documents
= It turns a closed-book exam into an open-book one.
? Why tell the model to say "I don't know" when the documents don't contain the answer?
+ Otherwise it's pushed to answer anyway, often by making something up
- It's required by the API
- It makes retrieval faster
= An honest way out reduces hallucinations when retrieval misses.
? Your whole knowledge base is 80 pages. What's a sensible first approach?
+ Put it all in the prompt with prompt caching
- Build a vector database with three rerankers
- Fine-tune a model on it
= Retrieval adds moving parts; start simple when the content fits.
? Why keep metadata such as source and permissions with each chunk?
+ To cite sources and to retrieve only what the user is allowed to see
- Metadata makes embeddings more accurate
- Vector databases require it
= Citations and access control both depend on it.
:::

@@@ lesson
id: chunking
title: Chunking documents
minutes: 24
summary: Why documents are split into chunks, the chunk-size trade-off, fixed-size chunks with overlap, splitting on sentences and paragraphs, recursive splitting, structure-aware chunking with headings, chunk metadata and headers, contextual retrieval, and small-to-big retrieval.
---
Retrieval works on **chunks**: passages small enough to match a specific question and to fit, several at a time, into a prompt. How you cut documents into chunks quietly decides what retrieval can ever find.

### Why chunk at all?

- **Precision.** A question about puncture prices matches one paragraph, not a 40-page manual. One embedding for a whole manual blurs every topic in it together.
- **Prompt budget.** You can put the top 5–20 chunks in a prompt, not the top 20 documents.
- **Limits.** Embedding models accept a limited input length per text.

### The size trade-off

| Chunks that are… | Good | Bad |
|---|---|---|
| small (a sentence or two) | precise matches | lose context ("It costs £12": what does?) |
| large (pages) | full context | vague matches; fewer fit in the prompt; costlier |

A few hundred tokens per chunk with **10–20% overlap** is a common starting point. Then tune it, along with how many chunks you retrieve, on your own questions (Lesson 22). There's no universally best size.

### Fixed-size chunks with overlap

The simplest method takes a fixed number of words (or tokens) at a time. **Overlap** repeats a little text at each boundary, so a sentence cut in half still appears whole in one of the chunks:

![A row of 10 words split into chunks of 4 words with an overlap of 1. Chunk 1 covers words 1–4, chunk 2 covers words 4–7, chunk 3 covers words 7–10. The shared words at each boundary are highlighted](figures/chunk-overlap.svg)

The step between chunk starts is `size − overlap`. The first exercise implements this.

### Respecting boundaries

Cutting mid-sentence hurts. Better splitters prefer natural boundaries:

- **Sentences and paragraphs:** gather whole sentences until the chunk is full.
- **Recursive splitting:** try to split on the biggest separator first (blank lines between paragraphs), and only fall back to smaller ones (line breaks, sentence ends, spaces) for pieces that are still too long. Libraries such as LangChain and LlamaIndex provide this.
- **Structure-aware:** use the document's own structure: Markdown or HTML headings, sections of a contract, functions in code, rows of a table. Never split a table row or a code block down the middle (the second exercise splits by headings).

```python
import re

text = """Unused items can be returned within 30 days. Bring your receipt.

Helmets can only be returned unworn. This is for safety reasons.

Refunds go back to the original payment method."""

paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
sentences = [s for p in paragraphs for s in re.split(r"(?<=[.!?])\s+", p)]
print(len(paragraphs), "paragraphs;", len(sentences), "sentences")
for p in paragraphs:
    print("-", p)
```

### Give every chunk its context

A chunk on its own often loses vital context: "The fee is £12." Which fee? Fixes, from simple to sophisticated:

- **Metadata:** store the source, title, section path, date and permissions with each chunk; use them for citations and filtering.
- **Chunk headers:** prepend the document title and section path to the text before indexing: `Repairs guide > Punctures: The fee is £12.`
- **Contextual retrieval:** use an LLM to write a short context (Anthropic used 50–100 tokens) situating each chunk in its document, and prepend that before embedding and keyword indexing. In Anthropic's 2024 tests, this cut the top-20 retrieval failure rate by 49%, and by 67% when combined with reranking (Lesson 21). Prompt caching makes it affordable, since the whole document is resent for each of its chunks.
- **Contextualised chunk embeddings:** some embedding models (for example Voyage's `voyage-context-4`) take the whole document and return one embedding per chunk that already reflects its surroundings.

### Small to big

Another pattern **retrieves small and returns big**: index small chunks (precise matching), but when one matches, give the model its surrounding section or the neighbouring chunks (enough context to answer). Store each chunk's parent ID or position to make this possible.

:::exercise Fixed-size chunks with overlap
Write `chunk_words(text, size, overlap=0)` splitting `text` into words (`text.split()`) and returning a list of chunks, each the words joined with single spaces:

- each chunk has `size` words (the last may have fewer);
- each chunk starts `size − overlap` words after the previous one;
- stop once a chunk reaches the end of the text (don't add a final chunk that only repeats overlap);
- raise `ValueError` unless `0 <= overlap < size`;
- an empty text gives `[]`.
```python starter
def chunk_words(text, size, overlap=0):
    pass

text = "one two three four five six seven eight nine ten"
print(chunk_words(text, 4, overlap=1))
# ['one two three four', 'four five six seven', 'seven eight nine ten']
```
```python check
fn = need("chunk_words")
_t = "one two three four five six seven eight nine ten"
test(fn, cases=[
    ((_t, 4, 1), ["one two three four", "four five six seven", "seven eight nine ten"], "overlap of 1"),
    ((_t, 4), ["one two three four", "five six seven eight", "nine ten"], "no overlap; a short last chunk"),
    ((_t, 5, 0), ["one two three four five", "six seven eight nine ten"], "exact fit"),
    ((_t, 6, 2), ["one two three four five six", "five six seven eight nine ten"], "the second chunk reaches the end"),
    ((_t, 20, 5), [_t], "one chunk"),
    (("  spaced   out\nwords  ", 2), ["spaced out", "words"], "any whitespace"),
    (("", 3, 1), [], "empty text"),
    ((_t, 3, 2), ["one two three", "two three four", "three four five", "four five six", "five six seven", "six seven eight", "seven eight nine", "eight nine ten"], "step of 1"),
], show="chunk_words(text, {1}, ...)")
for _size, _ov in [(4, 4), (4, 5), (3, -1), (0, 0)]:
    try:
        fn(_t, _size, _ov)
    except ValueError:
        pass
    else:
        raise AssertionError(f"chunk_words(text, {_size}, overlap={_ov}) should raise ValueError.")
```
```python solution
def chunk_words(text, size, overlap=0):
    if not 0 <= overlap < size:
        raise ValueError("need 0 <= overlap < size")
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break                      # this chunk reached the end
    return chunks

text = "one two three four five six seven eight nine ten"
print(chunk_words(text, 4, overlap=1))
```
hint: The chunks start at 0, `step`, `2 × step`, … where `step = size − overlap`: `range(0, len(words), step)`.
hint: Each chunk is `words[start:start + size]`; slicing past the end is safe in Python.
hint: After adding a chunk, `break` if `start + size >= len(words)`; without this, overlap creates extra chunks made only of words you've already covered. Check the `ValueError` condition first.
approach:
1. **Understand:** a sliding window of `size` words moving `size − overlap` at a time, ending at the first window that touches the end.
2. **Examples:** size 4, overlap 1 → starts 0, 3, 6; the window at 6 covers words 7–10 and ends the text.
3. **Brute force:** this is already linear.
4. **Pattern:** **sliding window with a step**.
5. **Plan:** validate → split → loop over starts → slice and join → stop at the end.
6. **Code and test:** no overlap, exact fit, step 1, odd whitespace, empty text, invalid settings.
walkthrough:
**Line by line**

- `0 <= overlap < size` guarantees a positive step; an overlap equal to the size would never move forward.
- `text.split()` with no argument splits on any run of whitespace and ignores it at the ends.
- `range(0, len(words), step)` produces the window starts; for an empty text it produces none.
- The `break` stops as soon as a window covers the last word.

**Trace** with size 6, overlap 2 (step 4): start 0 → words 1–6; start 4 → words 5–10, and 4 + 6 = 10 reaches the end → stop.

**Complexity:** O(n · size ÷ step) words copied; O(n) when the overlap is small.

**Common wrong approach:** forgetting the `break`, which with size 4 and overlap 1 adds a fourth chunk, "ten", repeating text already covered. (Real systems usually count **tokens** rather than words, and prefer sentence boundaries.)
:::

:::exercise Split Markdown by headings
Write `split_markdown(text)` returning a list of `(path, body)` pairs, one per section:

- A heading is a line matching `^(#{1,6})\s+(.*)$`; its level is the number of `#`s.
- A section's `path` is the titles of the enclosing headings joined with `" > "`, such as `"Returns > Helmets"`. A heading closes any open headings of the same or a deeper level.
- A section's `body` is the lines up to the next heading, joined with `"\n"` and stripped. Skip sections whose body is empty.
- Text before the first heading has the path `""`.
```python starter
import re

def split_markdown(text):
    pass

doc = """# Returns
Unused items within 30 days.
## Helmets
Only if unworn.
# Repairs
## Punctures
£12, same day."""
for path, body in split_markdown(doc):
    print(f"{path}: {body}")
```
```python check
fn = need("split_markdown")
_d = "# Returns\nUnused items within 30 days.\n## Helmets\nOnly if unworn.\n# Repairs\n## Punctures\n£12, same day."
test(fn, cases=[
    ((_d,), [("Returns", "Unused items within 30 days."), ("Returns > Helmets", "Only if unworn."), ("Repairs > Punctures", "£12, same day.")], "nested headings; an empty section is skipped"),
    (("Intro text.\n# A\nBody A",), [("", "Intro text."), ("A", "Body A")], "text before the first heading"),
    (("# A\n### C\ndeep\n## B\nmid",), [("A > C", "deep"), ("A > B", "mid")], "skipped levels"),
    (("# A\nline 1\n\nline 2\n\n# B\n\n",), [("A", "line 1\n\nline 2")], "multi-line bodies; blank-only section skipped"),
    (("#NoSpace is not a heading\ntext",), [("", "#NoSpace is not a heading\ntext")], "a heading needs a space after the #s"),
    (("",), [], "empty text"),
    (("## Start at two\nx\n# Top\ny\n## Sub\nz",), [("Start at two", "x"), ("Top", "y"), ("Top > Sub", "z")], "a shallower heading closes deeper ones"),
], show="split_markdown(...)")
```
```python solution
import re

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

def split_markdown(text):
    sections = []
    stack = []                         # (level, title) of the open headings
    lines = []

    def flush():
        body = "\n".join(lines).strip()
        if body:
            sections.append((" > ".join(title for _, title in stack), body))

    for line in text.split("\n"):
        match = HEADING.match(line)
        if match:
            flush()
            lines = []
            level = len(match.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()            # close headings at the same or a deeper level
            stack.append((level, match.group(2).strip()))
        else:
            lines.append(line)
    flush()
    return sections

doc = """# Returns
Unused items within 30 days.
## Helmets
Only if unworn.
# Repairs
## Punctures
£12, same day."""
for path, body in split_markdown(doc):
    print(f"{path}: {body}")
```
hint: Walk the lines once. Keep the lines of the current section in a list, and a **stack** of the open headings as `(level, title)` pairs.
hint: At each heading: first save the current section (if its body isn't empty), then pop headings from the stack while the top one's level is ≥ the new level, then push the new heading.
hint: The path is `" > ".join(title for level, title in stack)`. Don't forget to save the last section after the loop.
approach:
1. **Understand:** sections split at headings; each knows its chain of parent headings.
2. **Examples:** `# A`, `### C`, `## B`: B (level 2) closes C (level 3) but not A (level 1) → "A > B".
3. **Brute force:** for each section, scan backwards for the nearest heading of each lower level: O(n²).
4. **Pattern:** **stack of open headings**, like matching nested brackets.
5. **Plan:** for each line → heading? flush, pop, push : collect → final flush.
6. **Code and test:** text before any heading, skipped levels, empty sections, `#` without a space.
walkthrough:
**Line by line**

- The regex requires whitespace after the `#`s, so `#NoSpace` is ordinary text (as in Markdown itself).
- `flush` builds the path from the stack **as it was** for that section, so it must run before the stack changes.
- Popping while `stack[-1][0] >= level` closes siblings (same level) and their children (deeper levels).
- The final `flush()` after the loop saves the last section.

**Trace** on the first example: "Returns" body saved with path "Returns"; "Helmets" → "Returns > Helmets"; `# Repairs` pops both and has no body (skipped); "Punctures" → "Repairs > Punctures".

**Complexity:** O(n) for n lines (each heading is pushed and popped at most once).

**Common wrong approach:** treating `#` lines inside fenced code blocks as headings. A production splitter tracks whether it's inside a fence, or uses a real Markdown parser.
:::

:::quiz
? What is the main risk of very small chunks?
+ They lose context, such as what "it" or "the fee" refers to
- They can't be embedded
- They make the index too small
= Precise but context-poor; add headers or small-to-big retrieval.
? Why add overlap between chunks?
+ So text cut at a boundary still appears whole in one chunk
- To make the index larger
- Because embedding models require it
= A little repetition protects ideas that straddle a cut.
? What does contextual retrieval add to each chunk before indexing?
+ A short, model-written description situating the chunk within its document
- The full document
- A random ID
= In Anthropic's tests it cut retrieval failures substantially.
? A chunk matches, but the answer needs the surrounding section. Which pattern helps?
+ Small-to-big: retrieve the small chunk, give the model its parent section
- Bigger embeddings
- More overlap only
= Match precisely, answer with context.
:::

@@@ lesson
id: keyword-search
title: Keyword search with BM25
minutes: 26
summary: Inverted indexes, term frequency and inverse document frequency, the BM25 ranking formula and its k1 and b settings, tokenising (lower-casing, stop words, stemming), where keyword search beats embeddings, and the tools that provide it.
---
Before embeddings, search engines ranked documents by the **words** they share with the query, and the best of those methods, **BM25**, is still a strong baseline. It's fast, needs no model, explains its results, and is excellent at exact terms such as part numbers, error codes and names, where embeddings often struggle.

### The inverted index

Scanning every document for every query doesn't scale. An **inverted index** maps each word to the documents containing it, like the index at the back of a book:

```python
import re
from collections import defaultdict

docs = ["Puncture repair costs 12 pounds.",
        "Tubeless tyres rarely puncture.",
        "We repair frames and wheels. Frame repair takes a week.",
        "Opening hours: 9 to 5."]

index = defaultdict(set)
for doc_id, text in enumerate(docs):
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        index[word].add(doc_id)

print("puncture ->", sorted(index["puncture"]))
print("repair   ->", sorted(index["repair"]))
both = index["puncture"] & index["repair"]       # documents containing both words
print("both     ->", sorted(both))
```

A query only touches the lists for its own words, so lookups stay fast even with millions of documents.

### Scoring: which matches matter most?

Two intuitions drive keyword ranking:

- **Term frequency (TF):** a document that mentions "puncture" several times is probably more about punctures. But the tenth mention adds less than the first.
- **Inverse document frequency (IDF):** a word that appears in **few** documents ("tubeless") tells you much more than one that appears in nearly all ("bike" in a bike shop's documents).

**BM25** ("Best Matching 25") combines these, and also adjusts for document length, since a long document mentions everything more often. For a query with terms t:

```text
score(D) = Σ  IDF(t) × f(t, D) × (k1 + 1) / ( f(t, D) + k1 × (1 − b + b × |D| / avgdl) )
           t

IDF(t)   = ln( (N − n(t) + 0.5) / (n(t) + 0.5) + 1 )
```

| Symbol | Meaning |
|---|---|
| f(t, D) | how many times term t appears in document D |
| \|D\|, avgdl | D's length in words, and the average length of all documents |
| N, n(t) | the number of documents, and how many contain t |
| k1 | **saturation**, usually 1.2–2.0: how quickly extra mentions stop counting |
| b | **length normalisation**, usually 0.75: 0 ignores length, 1 fully normalises |

![A line chart of a term's score contribution against how many times it appears in a document, from 0 to 10. A straight line shows raw counting, growing without limit. Three BM25 curves for k1 = 0.5, 1.2 and 2.0 rise quickly and then flatten towards a ceiling of k1 + 1; smaller k1 saturates sooner](figures/bm25-saturation.svg)

The `+ 1` inside the logarithm (the form used by Lucene, and so by Elasticsearch and OpenSearch) keeps IDF positive even for words in more than half the documents. Libraries differ in such details, so scores from different tools aren't directly comparable, but the rankings are usually similar.

### Tokenising: what counts as "the same word"?

BM25 matches **tokens**, so how text is split and normalised matters:

- **Lower-casing**, so "Puncture" matches "puncture".
- **Stop words:** very common words ("the", "and") can be dropped; IDF already gives them little weight.
- **Stemming** cuts words to a root so "repairs", "repaired" and "repairing" all match "repair" (the Porter and Snowball stemmers are common). **Lemmatisation** does this with a dictionary ("better" → "good").
- **Language:** other languages need their own rules; Chinese and Japanese need word segmentation, since they don't use spaces.

Without stemming, the scorer below misses "frames" when you search for "frame".

### Keyword or vector search?

| Query | Keyword search (BM25) | Vector search (Lesson 20) |
|---|---|---|
| `SH-M8100 brake lever` | ✅ exact part number | ❌ may match "brake lever" generally |
| `error E-504 on the motor` | ✅ | ❌ codes have little "meaning" |
| `my chain keeps falling off` | ⚠️ needs the same words | ✅ matches "chain drops" and "derailleur adjustment" |
| `bicycle` vs documents saying `bike` | ❌ no synonyms | ✅ |

Each fails where the other succeeds, which is why production systems often use **both** (Lesson 21). BM25 is available in Elasticsearch and OpenSearch, SQLite's FTS5 (`bm25()`), Tantivy and Lucene, and Python libraries such as `bm25s` and `rank_bm25`.

:::exercise Build an inverted index
Write `build_index(docs)` returning a dict mapping each token to a **sorted list of the indexes** of the documents that contain it (each index once). Tokenise with `re.findall(r"[a-z0-9]+", text.lower())`. Then write `search_all(index, query)` returning the sorted indexes of the documents that contain **every** token of the query (an empty query gives `[]`).
```python starter
import re

def build_index(docs):
    pass

def search_all(index, query):
    pass

docs = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
        "We repair frames and wheels. Frame repair takes a week."]
index = build_index(docs)
print(index["repair"])                        # [0, 2]
print(search_all(index, "Puncture REPAIR"))   # [0]
```
```python check
bi = need("build_index"); sa = need("search_all")
_d = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
      "We repair frames and wheels. Frame repair takes a week.", "Opening hours: 9 to 5."]
_ix = bi(_d)
assert isinstance(_ix, dict), f"build_index should return a dict, but it returned a {type(_ix).__name__}."
for _w, _want in [("repair", [0, 2]), ("puncture", [0, 1]), ("9", [3]), ("frame", [2]), ("frames", [2]), ("a", [2])]:
    same(_ix.get(_w), _want, what=f"index[{_w!r}]")
assert "Repair" not in _ix and "pounds." not in _ix, "Tokens should be lower-case letters and digits only."
same(len(_ix), 21, what="The number of distinct tokens in the index")
same(bi([]), {}, what="build_index([])")
test(sa, cases=[
    ((_ix, "puncture repair"), [0], "two words"),
    ((_ix, "Puncture REPAIR!"), [0], "query is tokenised the same way"),
    ((_ix, "repair"), [0, 2], "one word"),
    ((_ix, "repair helmet"), [], "a word in no document"),
    ((_ix, ""), [], "empty query"),
    ((_ix, "repair repair"), [0, 2], "repeated word"),
], show="search_all(index, {1})")
```
```python solution
import re

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def build_index(docs):
    index = {}
    for doc_id, text in enumerate(docs):
        for word in set(tokens(text)):
            index.setdefault(word, []).append(doc_id)   # doc_ids arrive in order, so lists stay sorted
    return index

def search_all(index, query):
    words = set(tokens(query))
    if not words:
        return []
    result = None
    for word in words:
        found = set(index.get(word, []))
        result = found if result is None else result & found
    return sorted(result)

docs = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
        "We repair frames and wheels. Frame repair takes a week."]
index = build_index(docs)
print(index["repair"])
print(search_all(index, "Puncture REPAIR"))
```
hint: Loop over `enumerate(docs)`; for each **distinct** token in a document (a set), append the document's index to that token's list.
hint: `index.setdefault(word, []).append(doc_id)` creates the list the first time. Because you visit documents in order, each list is already sorted.
hint: For `search_all`, intersect the sets of document indexes for every query token (`&`); a missing token gives an empty set.
approach:
1. **Understand:** word → which documents; then an AND query is an intersection of those lists.
2. **Examples:** "repair" → [0, 2]; "puncture" → [0, 1]; both → [0].
3. **Brute force:** for each query, scan every document's text: O(total text) per query.
4. **Pattern:** **inverted index + set intersection**.
5. **Plan:** tokenise once per document → postings lists → intersect per query.
6. **Code and test:** repeated words in a document, unknown words, empty query, punctuation.
walkthrough:
**Line by line**

- `set(tokens(text))` ensures a document is added once per word, even if the word repeats.
- `setdefault` returns the existing list or inserts a new empty one.
- `index.get(word, [])` treats an unknown word as matching nothing, so the intersection becomes empty.
- Starting `result` as `None` lets the first word's set become the starting point.

**Trace:** "puncture repair" → {0, 1} & {0, 2} = {0} → [0].

**Complexity:** building is O(total tokens); a query is O(sum of its postings-list lengths).

**Common wrong approach:** storing the full text per word or scanning documents at query time, which throws away the index's whole advantage. (Real engines also store each word's **count** and positions per document, for scoring and phrase search.)
:::

:::exercise Score documents with BM25
Write `bm25_scores(query, docs, k1=1.5, b=0.75)` returning a list with each document's BM25 score for the query, using the formulas in the lesson:

- tokenise with `re.findall(r"[a-z0-9]+", text.lower())`;
- use each **distinct** query token once;
- a token that appears in no document adds nothing;
- `avgdl` is the average number of tokens per document;
- no documents → `[]`.
```python starter
import math
import re

def bm25_scores(query, docs, k1=1.5, b=0.75):
    pass

docs = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
        "We repair frames and wheels. Frame repair takes a week.", "Opening hours: 9 to 5."]
print([round(s, 4) for s in bm25_scores("puncture repair", docs)])
# [1.4987, 0.8155, 0.8155, 0.0]
```
```python check
fn = need("bm25_scores")
_d = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
      "We repair frames and wheels. Frame repair takes a week.", "Opening hours: 9 to 5."]
_r4 = lambda scores: [round(s, 4) for s in scores]
test(fn, cases=[
    (("puncture repair", _d), [1.4987, 0.8155, 0.8155, 0.0], "two terms"),
    (("frame repair", _d), [0.7493, 0.0, 1.7416, 0.0], "frame but not frames"),
    (("tubeless", _d), [0.0, 1.4164, 0.0, 0.0], "a rare word scores high"),
    (("helmet", _d), [0.0, 0.0, 0.0, 0.0], "no matches"),
    (("repair repair", _d), [0.7493, 0.0, 0.8155, 0.0], "a repeated query word counts once"),
    (("puncture", _d, 1.2, 0.0), [0.6931, 0.6931, 0.0, 0.0], "b = 0 ignores length"),
    (("repair", ["repair repair repair repair", "repair", "bike"]), [0.7094, 0.6065, 0.0], "saturation and length"),
    (("anything", []), [], "no documents"),
], key=_r4, show="bm25_scores({0}, docs, ...)")
```
```python solution
import math
import re

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def bm25_scores(query, docs, k1=1.5, b=0.75):
    if not docs:
        return []
    doc_tokens = [tokens(d) for d in docs]
    n_docs = len(docs)
    avgdl = sum(len(t) for t in doc_tokens) / n_docs
    scores = [0.0] * n_docs
    for term in set(tokens(query)):
        df = sum(1 for t in doc_tokens if term in t)            # documents containing the term
        if df == 0:
            continue
        idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
        for i, t in enumerate(doc_tokens):
            f = t.count(term)
            if f:
                norm = k1 * (1 - b + b * len(t) / avgdl)
                scores[i] += idf * f * (k1 + 1) / (f + norm)
    return scores

docs = ["Puncture repair costs 12 pounds.", "Tubeless tyres rarely puncture.",
        "We repair frames and wheels. Frame repair takes a week.", "Opening hours: 9 to 5."]
print([round(s, 4) for s in bm25_scores("puncture repair", docs)])
```
hint: Tokenise every document once. You need each document's length, the average length, and for each query term the number of documents containing it.
hint: For each distinct query term with `df > 0`: `idf = math.log((N - df + 0.5) / (df + 0.5) + 1)`. Then for each document with `f = tokens.count(term)` > 0, add `idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(doc) / avgdl))`.
hint: Start from a list of zeros, one per document, and add each term's contribution.
approach:
1. **Understand:** a sum over distinct query terms of IDF × saturated, length-normalised term frequency.
2. **Examples:** "puncture" is in 2 of 4 documents → IDF = ln(2.5/2.5 + 1) = ln 2 ≈ 0.693.
3. **Brute force:** this direct version is O(terms × total tokens), fine for small collections; an inverted index with stored counts makes it fast.
4. **Pattern:** **TF × IDF with saturation and length normalisation**.
5. **Plan:** tokenise → avgdl → per term: df, idf → per document: add the term's contribution.
6. **Code and test:** rare versus common words, repeated query words, b = 0, long documents, no documents.
walkthrough:
**Line by line**

- `set(tokens(query))` uses each query word once, matching the specification.
- `df` (document frequency) counts documents containing the term, not total mentions.
- The denominator `f + k1 × (…)` makes the contribution approach `idf × (k1 + 1)` as `f` grows: saturation.
- Longer-than-average documents get a larger denominator (when b > 0), so the same count is worth less.

**Trace** for "repair" in `["repair repair repair repair", "repair", "bike"]`: df = 2, IDF = ln(1.5/2.5 + 1) = ln 1.6 ≈ 0.470; avgdl = 2. Document 0: f = 4, norm = 1.5 × (0.25 + 0.75 × 4/2) = 2.625 → 0.470 × 10 / 6.625 ≈ 0.709. Document 1: f = 1, norm = 1.5 × (0.25 + 0.375) = 0.9375 → 0.470 × 2.5 / 1.9375 ≈ 0.607. Four mentions earned only about 17% more than one.

**Complexity:** O(q × T) here, for q query terms and T total tokens.

**Common wrong approach:** raw counts without IDF, so common words dominate, or without saturation, so keyword stuffing wins.
:::

:::quiz
? What does an inverted index map?
+ Each word to the documents that contain it
- Each document to its embedding
- Each query to its answer
= Like the index at the back of a book.
? Why does BM25 give a rare word more weight than a common one?
+ A word that appears in few documents tells you more about which documents are relevant (IDF)
- Rare words are longer
- Common words are always stop words
= Inverse document frequency rewards specificity.
? What does the k1 setting control?
+ How quickly extra mentions of a word stop increasing the score
- The number of results
- The length of the query
= Smaller k1 saturates sooner.
? Which query is BM25 likely to handle better than vector search?
+ An exact part number such as SH-M8100
- "my chain keeps falling off"
- A question using synonyms of the document's words
= Exact identifiers carry little "meaning" for embeddings.
:::

@@@ lesson
id: vector-search
title: Vector search and vector databases
minutes: 26
summary: Semantic search with embeddings, embedding documents and queries, exact search as a matrix product, memory costs and how to cut them, approximate nearest-neighbour indexes (IVF, HNSW, quantisation) and the recall trade-off, metadata filtering, and choosing a vector database.
---
Keyword search matches **words**; vector search matches **meaning**. Embed every chunk once (Lesson 3), embed each query when it arrives, and return the chunks whose vectors are closest. "My chain keeps falling off" then finds the chunk about "adjusting a derailleur so the chain doesn't drop", without a single shared keyword.

### Documents and queries

```py-static
import voyageai

vo = voyageai.Client()
chunk_vectors = vo.embed(chunk_texts, model="voyage-4", input_type="document").embeddings   # once, at ingestion
query_vector = vo.embed([question], model="voyage-4", input_type="query").embeddings[0]     # per question
```

- Use the **same model** for documents and queries; vectors from different models live in unrelated spaces. Changing model means re-embedding the whole corpus.
- Some models, including Voyage's, take an **input type**: questions and passages are phrased differently, and the model adjusts for it.
- Embed at ingestion and store the vectors; never re-embed the corpus per query.

### Exact search

With normalised vectors, cosine similarity is a dot product, so scoring **every** chunk at once is one matrix-vector product:

```python
import numpy as np

rng = np.random.default_rng(0)
vectors = rng.normal(size=(10_000, 256))                         # 10,000 chunks, 256 dimensions
vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)        # normalise once, at ingestion

query = vectors[42] + 0.03 * rng.normal(size=256)                # a query near chunk 42
query /= np.linalg.norm(query)

scores = vectors @ query                                         # 10,000 cosine similarities
top = np.argsort(-scores)[:5]                                    # best five
print(top, np.round(scores[top], 3))
```

This **exact** (brute-force) search is perfectly accurate and, with NumPy, fast up to hundreds of thousands of vectors. Its cost grows linearly with the corpus, and so does memory:

| Chunks | Dimensions | float32 storage |
|---|---|---|
| 100,000 | 1,024 | 0.4 GB |
| 1,000,000 | 1,024 | 4 GB |
| 10,000,000 | 1,024 | 41 GB |

Two ways to shrink it: **fewer dimensions** (many current models, including Voyage 4, can output 256, 512, 1,024 or 2,048 dimensions, trading a little quality for size), and **quantisation** (storing each number in 8 bits or even 1 bit instead of 32).

### Approximate nearest-neighbour (ANN) search

For millions of vectors, indexes find **almost** the best matches while scoring only a small fraction of them. They trade a little **recall** (the share of the true top-k results found) for a lot of speed.

- **IVF (inverted file):** cluster the vectors into buckets around **centroids** ahead of time. At query time, find the few nearest centroids and score only the vectors in those buckets. More buckets probed means better recall and slower search (the second exercise).
- **HNSW (hierarchical navigable small world):** a graph linking each vector to its neighbours, in layers from sparse to dense. Search starts at the top layer and walks greedily towards the query, dropping a layer at a time. It's the most common index today: fast, with high recall, at the cost of extra memory for the graph.
- **Product quantisation (PQ):** compress vectors into short codes; often combined with IVF for billion-scale collections.

![Points in a plane, coloured by which of four clusters they belong to, with a cross marking each cluster's centroid. A query star sits near the border of two clusters. The single nearest cluster is probed and shaded; one of the query's true nearest neighbours lies just across the border in an unprobed cluster, so it is missed. Probing two clusters would find it](figures/ivf.svg)

Index settings (such as HNSW's `ef_search` or IVF's `n_probe`) tune the speed/recall trade-off. Measure recall against exact search on a sample of queries before trusting an index.

### Filtering

Real queries come with conditions: only this user's documents, only English, only the current product range. Store **metadata** with each vector and filter on it:

- **Pre-filtering** (apply the condition, then search what's left) always returns k results if enough match, but can be slow with an ANN index.
- **Post-filtering** (search, then drop non-matching results) is fast but can return **fewer than k**, even none, when the filter is selective.

Good vector databases filter **during** the index search. Access-control filters are not optional: retrieval must never surface a document the user isn't allowed to read.

### Where to store vectors

| Option | Good for |
|---|---|
| NumPy array or FAISS (a library) | prototypes, up to a few hundred thousand vectors in memory, or custom setups |
| **pgvector** (PostgreSQL extension) | apps already on Postgres: vectors next to your data, SQL filters, HNSW indexes |
| dedicated vector databases: Pinecone, Qdrant, Weaviate, Milvus, Chroma, LanceDB | large scale, managed hosting, built-in hybrid search and filtering |
| search engines with vector support: Elasticsearch, OpenSearch | when you also need strong keyword search |

```py-static
# pgvector: cosine distance is <=>, so the nearest rows come first
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
cur.execute("CREATE TABLE chunks (id bigserial PRIMARY KEY, lang text, body text, embedding vector(1024))")
cur.execute("CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)")
cur.execute("SELECT body FROM chunks WHERE lang = %s ORDER BY embedding <=> %s::vector LIMIT 5",
            ("en", str(query_vector)))
```

Start simple: for most applications the database you already run is enough.

:::exercise Vector search with a filter
Write `filtered_search(query, vectors, metadata, k, where=None)` returning the indexes of the `k` vectors most similar to `query` by **cosine similarity**, best first, among those whose metadata matches:

- `vectors` is a list of vectors (or a 2-D array); `metadata[i]` is a dict for vector `i`;
- `where` is a dict; a vector matches if its metadata has **every** key with an equal value (`None` means no filter);
- filter **first**, then rank (pre-filtering), so you return `k` results whenever at least `k` match;
- equal similarities keep the lower index first. Return a list of ints.
```python starter
import numpy as np

def filtered_search(query, vectors, metadata, k, where=None):
    pass

vectors = [[1, 0], [0.9, 0.1], [0, 1], [0.7, 0.7], [-1, 0]]
metadata = [{"lang": "en"}, {"lang": "fr"}, {"lang": "en"}, {"lang": "en"}, {"lang": "en"}]
print(filtered_search([1, 0], vectors, metadata, 2))                        # [0, 1]
print(filtered_search([1, 0], vectors, metadata, 2, where={"lang": "en"}))  # [0, 3]
```
```python check
import numpy as np
fn = need("filtered_search")
_v = [[1, 0], [0.9, 0.1], [0, 1], [0.7, 0.7], [-1, 0]]
_m = [{"lang": "en", "type": "faq"}, {"lang": "fr", "type": "faq"}, {"lang": "en", "type": "manual"},
      {"lang": "en", "type": "faq"}, {"lang": "en", "type": "manual"}]
test(fn, cases=[
    (([1, 0], _v, _m, 2), [0, 1], "no filter"),
    (([1, 0], _v, _m, 2, {"lang": "en"}), [0, 3], "one condition"),
    (([1, 0], _v, _m, 3, {"type": "manual"}), [2, 4], "fewer matches than k"),
    (([1, 0], _v, _m, 5, {"lang": "en", "type": "faq"}), [0, 3], "two conditions"),
    (([1, 0], _v, _m, 2, {"lang": "de"}), [], "nothing matches"),
    (([1, 0], _v, _m, 0), [], "k = 0"),
    (([0, 2], _v, _m, 2), [2, 3], "the query isn't normalised"),
    (([1, 1], [[1, 0], [0, 1]], [{}, {}], 2), [0, 1], "a tie keeps the lower index"),
    (([1, 0], np.array(_v, dtype=float), _m, 1, {"lang": "fr"}), [1], "a NumPy array"),
    (([1, 0], [[10, 10], [0.5, 0.01]], [{}, {}], 2), [1, 0], "cosine, not the raw dot product"),
], show="filtered_search({0}, vectors, metadata, {3}, ...)")
```
```python solution
import numpy as np

def filtered_search(query, vectors, metadata, k, where=None):
    where = where or {}
    keep = [i for i, meta in enumerate(metadata)
            if all(meta.get(key) == value for key, value in where.items())]
    if not keep or k <= 0:
        return []
    candidates = np.asarray(vectors, dtype=float)[keep]
    q = np.asarray(query, dtype=float)
    scores = candidates @ q / (np.linalg.norm(candidates, axis=1) * np.linalg.norm(q))
    order = np.argsort(-scores, kind="stable")[:k]           # stable: ties keep the lower index
    return [keep[j] for j in order]

vectors = [[1, 0], [0.9, 0.1], [0, 1], [0.7, 0.7], [-1, 0]]
metadata = [{"lang": "en"}, {"lang": "fr"}, {"lang": "en"}, {"lang": "en"}, {"lang": "en"}]
print(filtered_search([1, 0], vectors, metadata, 2))
print(filtered_search([1, 0], vectors, metadata, 2, where={"lang": "en"}))
```
hint: First collect the indexes whose metadata matches: `all(meta.get(key) == value for key, value in where.items())` (true for every vector when there's no filter).
hint: Cosine similarity for many vectors at once: `candidates @ q / (np.linalg.norm(candidates, axis=1) * np.linalg.norm(q))`.
hint: `np.argsort(-scores, kind="stable")[:k]` gives positions within the candidates, best first; map them back with `keep[j]`.
approach:
1. **Understand:** filter → cosine-rank the survivors → top k → original indexes.
2. **Examples:** filter `lang = en` removes index 1, so the second-best becomes index 3 (0.707).
3. **Brute force:** compute every similarity, sort everything, then drop non-matches (post-filtering): same answer here, but in an ANN index post-filtering can lose results.
4. **Pattern:** **pre-filter, then exact search**.
5. **Plan:** matching indexes → candidate matrix → cosine scores → stable argsort → map back.
6. **Code and test:** no filter, empty result, k larger than the matches, unnormalised vectors, ties.
walkthrough:
**Line by line**

- `where or {}` turns `None` into "no conditions", so `all(...)` over an empty dict is `True` for every vector.
- `meta.get(key)` returns `None` for a missing key, so a vector without that field doesn't match.
- Dividing by both norms makes this cosine similarity. Without it, a long vector wins just for being long: for the query `[1, 0]`, the raw dot product prefers `[10, 10]` (10 versus 0.5), but cosine correctly prefers `[0.5, 0.01]`, which points almost exactly the same way (0.9998 versus 0.707).
- `kind="stable"` keeps equal scores in index order; NumPy's default sort makes no such promise.

**Trace** with `where={"lang": "en"}`: keep = [0, 2, 3, 4]; their scores are [1, 0, 0.707, −1]; the best two **positions** are 0 and 2 → `keep[0]`, `keep[2]` → [0, 3].

**Complexity:** O(n · d) to filter and score, plus O(m log m) to sort m matches.

**Common wrong approach:** searching first and filtering afterwards with a fixed k, which can return far fewer than k results (even none) when the filter is selective.
:::

:::exercise An IVF index search
An **IVF** index has already clustered the (normalised) vectors: `centroids` is a list of centroid vectors and `assignments[i]` is the bucket of vector `i`. Write `ivf_search(query, centroids, assignments, vectors, k, n_probe)`:

1. Score every centroid by its dot product with the query; probe the `n_probe` best buckets (ties: lower bucket number first).
2. Score only the vectors in the probed buckets by dot product with the query.
3. Return the indexes of the best `k` of them, best first (ties: lower index first), as a list of ints.
```python starter
import numpy as np

def ivf_search(query, centroids, assignments, vectors, k, n_probe):
    pass

import math
angles = [0, 10, 20, 95, 100, 110, 185, 190, 200, 275]
vectors = [[math.cos(math.radians(a)), math.sin(math.radians(a))] for a in angles]
centroids = [[1, 0], [0, 1], [-1, 0], [0, -1]]
assignments = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
query = [0.643, 0.766]                      # 50 degrees: between buckets 0 and 1
print(ivf_search(query, centroids, assignments, vectors, 3, n_probe=1))   # [3, 4, 5]: misses the true best
print(ivf_search(query, centroids, assignments, vectors, 3, n_probe=2))   # [2, 1, 3]: the exact answer
```
```python check
import math
fn = need("ivf_search")
_ang = [0, 10, 20, 95, 100, 110, 185, 190, 200, 275]
_v = [[math.cos(math.radians(a)), math.sin(math.radians(a))] for a in _ang]
_c = [[1, 0], [0, 1], [-1, 0], [0, -1]]
_a = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
test(fn, cases=[
    (([1, 0], _c, _a, _v, 3, 1), [0, 1, 2], "query inside one bucket"),
    (([0.643, 0.766], _c, _a, _v, 3, 1), [3, 4, 5], "near a border, one probe"),
    (([0.643, 0.766], _c, _a, _v, 3, 2), [2, 1, 3], "near a border, two probes"),
    (([0, -1], _c, _a, _v, 2, 1), [9], "fewer vectors than k in the bucket"),
    (([-1, 0], _c, _a, _v, 4, 1), [6, 7, 8], "one bucket"),
    (([-1, 0], _c, _a, _v, 4, 4), [6, 7, 8, 5], "probing every bucket is exact search"),
    (([1, 0], _c, [0, 0, 0, 1, 1, 1, 2, 2, 2, 1], _v, 2, 1), [0, 1], "a bucket can hold vectors anywhere"),
    (([0.7071, 0.7071], [[1, 0], [0, 1]], [0, 1], [[1, 0], [0, 1]], 2, 1), [0], "a tie between centroids goes to the lower bucket"),
], show="ivf_search({0}, centroids, assignments, vectors, {4}, n_probe={5})")
```
```python solution
import numpy as np

def ivf_search(query, centroids, assignments, vectors, k, n_probe):
    q = np.asarray(query, dtype=float)
    centroid_scores = np.asarray(centroids, dtype=float) @ q
    probed = set(np.argsort(-centroid_scores, kind="stable")[:n_probe].tolist())
    candidates = [i for i, bucket in enumerate(assignments) if bucket in probed]
    if not candidates:
        return []
    scores = np.asarray(vectors, dtype=float)[candidates] @ q
    order = np.argsort(-scores, kind="stable")[:k]
    return [candidates[j] for j in order]

import math
angles = [0, 10, 20, 95, 100, 110, 185, 190, 200, 275]
vectors = [[math.cos(math.radians(a)), math.sin(math.radians(a))] for a in angles]
centroids = [[1, 0], [0, 1], [-1, 0], [0, -1]]
assignments = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
query = [0.643, 0.766]
print(ivf_search(query, centroids, assignments, vectors, 3, n_probe=1))
print(ivf_search(query, centroids, assignments, vectors, 3, n_probe=2))
```
hint: Two rounds of the same idea: score with a matrix-vector product, then take the best few with `np.argsort(-scores, kind="stable")`.
hint: Round one picks buckets: the top `n_probe` centroids. Round two considers only the vectors whose `assignments[i]` is one of those buckets.
hint: Keep the list of candidate indexes so you can map positions in the candidate scores back to original indexes: `[candidates[j] for j in order]`.
approach:
1. **Understand:** coarse search over centroids, then exact search inside the chosen buckets.
2. **Examples:** the query at 50° is slightly closer to centroid 1 (at 90°) than centroid 0 (at 0°), but its true nearest vector (20°) lives in bucket 0.
3. **Brute force:** score every vector: exact, and what `n_probe` = number of buckets reproduces.
4. **Pattern:** **two-stage search**: cheap coarse filter, precise re-scoring.
5. **Plan:** centroid scores → probed set → candidates → candidate scores → top k → original indexes.
6. **Code and test:** border queries, small buckets, probing everything, centroid ties.
walkthrough:
**Line by line**

- One small product (`centroids @ q`) chooses buckets, instead of scoring all vectors.
- A `set` of probed buckets makes the membership test fast.
- Only candidates are scored, which is where the speed comes from with thousands of buckets.
- Mapping `candidates[j]` restores the original vector indexes.

**Trace** for the border query, `n_probe=1`: centroid scores [0.643, 0.766, −0.643, −0.766] → bucket 1 → candidates [3, 4, 5] → best three are all of them. The true top three are [2, 1, 3]: recall = 1/3. With `n_probe=2`, buckets 1 and 0 are searched and the result is exact.

**Complexity:** O(c · d) for c centroids plus O(m · d) for m candidates, instead of O(n · d).

**Common wrong approach:** assuming an ANN index returns the true nearest neighbours. Measure recall against exact search and raise `n_probe` (or HNSW's `ef_search`) until it's high enough for your use.
:::

:::quiz
? You switch to a newer embedding model. What must you do?
+ Re-embed every document, because vectors from different models aren't comparable
- Nothing: vectors are universal
- Only embed new documents with the new model
= Queries and documents must come from the same model.
? What does an approximate nearest-neighbour index trade away?
+ A little recall, for much faster search
- All accuracy
- The ability to filter
= Measure recall against exact search.
? Why can post-filtering return fewer than k results?
+ It drops non-matching results after the search has already picked its top candidates
- Filters are always buggy
- k is ignored by vector databases
= Pre-filter or filter during the search.
? Roughly how much memory do 1,000,000 vectors of 1,024 float32 numbers need?
+ About 4 GB
- About 4 MB
- About 4 TB
= 1,000,000 × 1,024 × 4 bytes ≈ 4.1 GB.
:::

@@@ lesson
id: hybrid-and-reranking
title: Hybrid search and reranking
minutes: 24
summary: Combining keyword and vector search, why their scores can't simply be added, reciprocal rank fusion, weighted fusion with min-max normalisation, rerankers (cross-encoders) and the retrieval funnel, contextual retrieval results, and rewriting queries before searching.
---
Keyword search finds exact terms; vector search finds meaning (Lessons 19–20). Each misses what the other catches, so strong RAG systems run **both** and merge the results: **hybrid search**. Then a slower, more accurate **reranker** re-orders the shortlist before it reaches the prompt.

### The retrieval funnel

![A funnel. At the top, keyword search and vector search each return about 100 candidates from the whole corpus. Fusion merges them into one list of about 150. A reranker reads each candidate together with the query and keeps the best 20. Those 20 chunks go into the prompt](figures/retrieval-funnel.svg)

Each stage is more accurate and more expensive per item than the one before, so each handles fewer items. Anthropic's 2024 contextual-retrieval experiments followed this shape: retrieving 150 candidates, reranking, and passing the top 20 to the model, with 20 chunks working better than 5 or 10.

### Fusing two result lists

The scores can't simply be added: BM25 scores are unbounded (12.4 means nothing on its own), while cosine similarities sit between −1 and 1, and both shift from query to query. Two standard fixes:

**Reciprocal rank fusion (RRF)** ignores the scores and uses only each document's **rank** in each list:

```text
RRF(d) = Σ  1 / (k + rank_r(d))        with k = 60 by convention
         r
```

A document near the top of **both** lists beats one that tops only one. RRF needs no tuning, which makes it the usual default (the first exercise).

**Weighted score fusion** rescales each list's scores to 0–1 (for example with min-max normalisation) and blends them: `α × vector + (1 − α) × keyword`. It keeps information about **how much** better one result is, but needs α tuned on your evaluation set (the second exercise).

```python
keyword = ["sh-m8100-manual", "brake-pads", "lever-install"]    # BM25 ranking
vector = ["lever-install", "brake-bleeding", "sh-m8100-manual"]  # embedding ranking

scores = {}
for ranking in (keyword, vector):
    for rank, doc in enumerate(ranking, start=1):
        scores[doc] = scores.get(doc, 0) + 1 / (60 + rank)

for doc in sorted(scores, key=scores.get, reverse=True):
    print(f"{scores[doc]:.4f}  {doc}")
```

### Rerankers

An embedding model encodes the query and each document **separately** (a **bi-encoder**): fast, because document vectors are computed once in advance, but the model never sees them together. A **reranker** (a **cross-encoder**) reads the query and a candidate **together** and outputs a relevance score. It's far more accurate, and far too slow to run over a whole corpus, so it only re-orders the shortlist.

```py-static
import voyageai

vo = voyageai.Client()
result = vo.rerank(query=question, documents=candidate_texts, model="rerank-2.5", top_k=20)
for r in result.results:                     # best first
    print(r.index, round(r.relevance_score, 3), r.document[:60])
```

Options include Voyage's `rerank-2.5` and `rerank-2.5-lite`, Cohere Rerank, open-weight rerankers (such as the BGE rerankers on Hugging Face), or an LLM prompted to grade relevance. In Anthropic's experiments, adding contextual retrieval (Lesson 18), BM25 and a reranker together cut the top-20 retrieval failure rate from 5.7% to 1.9%, a 67% reduction.

### Fix the query, too

Retrieval can only be as good as the query you send it:

- **Rewrite follow-ups.** In a conversation, "What about helmets?" means nothing on its own. Have a model rewrite it into a standalone query ("What is the returns policy for helmets?") using the chat history.
- **Multiple queries.** Generate a few phrasings, search with each, and fuse the results (RRF again).
- **Hypothetical answers (HyDE).** Have a model write a plausible answer, embed **that**, and search with it: answers often look more like the documents than questions do.
- **Route.** Some questions need a database or a tool, not document search at all (Part 5).

Each extra step adds latency and cost; add them when your evaluation (Lesson 22) shows retrieval failing on those kinds of question.

:::exercise Reciprocal rank fusion
Write `rrf(rankings, k=60)`. `rankings` is a list of ranked lists of document IDs (best first; ranks start at 1). Each document's score is the sum over the lists it appears in of `1 / (k + rank)`. Return all the document IDs sorted by score, highest first; ties keep the order in which the documents were **first seen** (reading the lists in order, each from its top).
```python starter
def rrf(rankings, k=60):
    pass

keyword = ["sh-m8100-manual", "brake-pads", "lever-install"]
vector = ["lever-install", "brake-bleeding", "sh-m8100-manual"]
print(rrf([keyword, vector]))
# ['sh-m8100-manual', 'lever-install', 'brake-pads', 'brake-bleeding']
```
```python check
fn = need("rrf")
test(fn, cases=[
    (([["sh-m8100-manual", "brake-pads", "lever-install"], ["lever-install", "brake-bleeding", "sh-m8100-manual"]],),
     ["sh-m8100-manual", "lever-install", "brake-pads", "brake-bleeding"], "two lists"),
    (([["a", "b", "c"], ["c", "a", "d"]],), ["a", "c", "b", "d"], "top of both lists wins"),
    (([["a", "b", "c"], ["c", "b", "a"]],), ["a", "c", "b"], "a tie keeps first-seen order"),
    (([["x", "y"], ["y", "z"], ["z", "x"]],), ["x", "y", "z"], "three lists, all tied"),
    (([["p", "q", "r", "s"], ["s"]],), ["s", "p", "q", "r"], "two appearances beat one top spot"),
    (([["a", "b"], ["b", "a"]], 1), ["a", "b"], "a different k"),
    (([["only"]],), ["only"], "one list"),
    (([],), [], "no lists"),
    (([[], ["a"]],), ["a"], "an empty list"),
])
```
```python solution
def rrf(rankings, k=60):
    scores = {}                                   # dicts remember insertion (first-seen) order
    for ranking in rankings:
        for rank, doc in enumerate(ranking, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1 / (k + rank)
    return sorted(scores, key=lambda doc: scores[doc], reverse=True)   # stable sort keeps ties in order

keyword = ["sh-m8100-manual", "brake-pads", "lever-install"]
vector = ["lever-install", "brake-bleeding", "sh-m8100-manual"]
print(rrf([keyword, vector]))
```
hint: Keep a dict from document ID to its running score; `enumerate(ranking, start=1)` gives each document's rank.
hint: Add `1 / (k + rank)` for every appearance. A Python dict remembers the order keys were first inserted.
hint: `sorted(scores, key=lambda d: scores[d], reverse=True)` is stable, so tied documents stay in first-seen order.
approach:
1. **Understand:** sum of reciprocal ranks across lists; sort; stable ties.
2. **Examples:** `p` is first in one list (1/61 ≈ 0.0164); `s` is fourth in one and first in another (1/64 + 1/61 ≈ 0.0320), so `s` wins.
3. **Brute force:** for each document, search every list for its rank: O(D × L × n).
4. **Pattern:** **accumulate scores in a dict, then sort**.
5. **Plan:** loop lists and ranks → add → stable sort descending.
6. **Code and test:** ties, three lists, empty lists, a different k.
walkthrough:
**Line by line**

- `scores.get(doc, 0.0)` starts a new document at zero.
- `start=1` makes the top result rank 1, so it adds `1 / 61` with the default k.
- Sorting with `reverse=True` is still stable in Python: equal scores keep the dict's insertion order.
- The constant k dampens the difference between rank 1 and rank 2, so agreement across lists matters more than one first place.

**Trace** on the lesson example: sh-m8100-manual = 1/61 + 1/63 ≈ 0.0323; lever-install = 1/63 + 1/61 (the same); brake-pads = 1/62; brake-bleeding = 1/62. Ties are broken by first appearance.

**Complexity:** O(total entries + D log D) for D distinct documents.

**Common wrong approach:** adding raw BM25 and cosine scores, so whichever scale is larger dominates the result.
:::

:::exercise Weighted fusion with min-max scaling
Write `weighted_fusion(keyword_scores, vector_scores, alpha=0.5)`. Both arguments are dicts from document ID to a score (higher is better).

1. **Min-max normalise** each dict separately: `(score − min) / (max − min)`. If all of a dict's scores are equal, each becomes `1.0`.
2. A document's fused score is `alpha × vector + (1 − alpha) × keyword`, using `0` for a list it's missing from.
3. Return every document ID, sorted by fused score (highest first); ties by ID in alphabetical order.
```python starter
def weighted_fusion(keyword_scores, vector_scores, alpha=0.5):
    pass

keyword = {"d1": 12.0, "d2": 3.0, "d3": 0.5}
vector = {"d2": 0.82, "d3": 0.79, "d4": 0.40}
print(weighted_fusion(keyword, vector))             # ['d2', 'd1', 'd3', 'd4']
print(weighted_fusion(keyword, vector, alpha=0.9))  # ['d2', 'd3', 'd1', 'd4']
```
```python check
fn = need("weighted_fusion")
_k = {"d1": 12.0, "d2": 3.0, "d3": 0.5}
_v = {"d2": 0.82, "d3": 0.79, "d4": 0.40}
test(fn, cases=[
    ((_k, _v), ["d2", "d1", "d3", "d4"], "equal weights"),
    ((_k, _v, 0.9), ["d2", "d3", "d1", "d4"], "mostly vector"),
    ((_k, _v, 0.0), ["d1", "d2", "d3", "d4"], "keyword only; zero scores tie by ID"),
    ((_k, _v, 1.0), ["d2", "d3", "d1", "d4"], "vector only; d1 and d4 both score 0"),
    (({"a": 5.0}, {"b": 0.3}), ["a", "b"], "single scores become 1.0; a tie by ID"),
    (({}, {"b": 0.3, "a": 0.1}), ["b", "a"], "one empty dict"),
    (({}, {}), [], "nothing"),
    (({"x": 2.0, "y": 2.0}, {"x": -0.5, "y": 0.5}), ["y", "x"], "equal keyword scores"),
], show="weighted_fusion(keyword, vector, ...)")
```
```python solution
def normalise(scores):
    if not scores:
        return {}
    low, high = min(scores.values()), max(scores.values())
    if high == low:
        return {doc: 1.0 for doc in scores}
    return {doc: (s - low) / (high - low) for doc, s in scores.items()}

def weighted_fusion(keyword_scores, vector_scores, alpha=0.5):
    kw, vec = normalise(keyword_scores), normalise(vector_scores)
    fused = {doc: alpha * vec.get(doc, 0.0) + (1 - alpha) * kw.get(doc, 0.0)
             for doc in set(kw) | set(vec)}
    return sorted(fused, key=lambda doc: (-fused[doc], doc))

keyword = {"d1": 12.0, "d2": 3.0, "d3": 0.5}
vector = {"d2": 0.82, "d3": 0.79, "d4": 0.40}
print(weighted_fusion(keyword, vector))
print(weighted_fusion(keyword, vector, alpha=0.9))
```
hint: Write a helper that min-max normalises one dict, handling the empty dict and the all-equal case.
hint: The documents to score are the union of both dicts' keys: `set(a) | set(b)`. Use `.get(doc, 0.0)` for missing ones.
hint: Sort with `key=lambda doc: (-fused[doc], doc)`: the minus sign puts high scores first, and the ID breaks ties alphabetically.
approach:
1. **Understand:** put both score lists on a 0–1 scale, blend, rank.
2. **Examples:** keyword d2 = (3 − 0.5) / 11.5 ≈ 0.217; vector d2 = 1.0 → fused 0.609, the best.
3. **Brute force:** adding raw scores: BM25's larger numbers would swamp the cosines.
4. **Pattern:** **normalise, then weighted sum**.
5. **Plan:** normalise each dict → union of IDs → blend → sort with a tuple key.
6. **Code and test:** α = 0 and 1, single entries, empty dicts, equal scores.
walkthrough:
**Line by line**

- The helper returns `{}` for an empty dict, avoiding `min()` of nothing.
- When every score is equal, the formula would divide by zero; treating them all as 1.0 says "equally top of this list".
- `set(kw) | set(vec)` includes documents found by only one method.
- The tuple key `(-score, doc)` sorts by score descending, then ID ascending.

**Trace** with α = 0.9: d2 = 0.9 × 1.0 + 0.1 × 0.217 ≈ 0.922; d3 = 0.9 × 0.929 + 0.1 × 0 ≈ 0.836; d1 = 0.1 × 1.0 = 0.1; d4 = 0.

**Complexity:** O(D log D) for D documents.

**Common wrong approach:** forgetting that min-max scaling is per query: the top result always gets 1.0 even when nothing is really relevant. That's one reason RRF (which ignores scores) is the safer default, and why a reranker's absolute scores are useful for dropping weak results.
:::

:::quiz
? Why can't BM25 and cosine scores simply be added?
+ They're on different, query-dependent scales, so one would dominate
- Python can't add floats from different libraries
- BM25 scores are always negative
= Fuse ranks (RRF) or normalise first.
? What makes a reranker more accurate than embedding similarity?
+ It reads the query and the document together instead of encoding them separately
- It uses bigger vectors
- It ignores the query
= Cross-encoders compare directly; that's also why they're slow.
? Why rerank only a shortlist?
+ Rerankers are too slow and costly to run over the whole corpus
- Rerankers only accept 10 documents
- The shortlist is always correct
= Each funnel stage is more accurate but costlier per item.
? A user asks "What about helmets?" after a question about returns. What should happen before retrieval?
+ Rewrite it into a standalone query using the conversation
- Search for "What about helmets?" as is
- Skip retrieval
= Follow-ups lack the context retrieval needs.
:::

@@@ lesson
id: evaluating-rag
title: Evaluating RAG
minutes: 26
summary: Why retrieval and generation must be measured separately, building an evaluation set with relevant chunks and unanswerable questions, retrieval metrics (hit rate, recall@k, precision@k, MRR, nDCG), answer metrics (faithfulness, relevance, correctness, citation accuracy, refusals), a crude groundedness check, diagnosing failures, evaluation tools, and monitoring in production.
---
A RAG system has many settings: chunk size, overlap, embedding model, k, fusion, reranker, prompt. Without measurement, every change is a guess. And because a RAG answer can go wrong in two different places, you measure **both**:

1. **Retrieval:** did the right chunks reach the prompt?
2. **Generation:** did the model answer correctly, using only those chunks?

If retrieval missed, no prompt can fix the answer. If retrieval succeeded and the answer is still wrong, fix the prompt or the model, not the index.

### An evaluation set

Collect **50–200 realistic questions** (from real users if you can), and for each record:

- the **IDs of the chunks** that contain the answer (for retrieval metrics);
- a **reference answer**, or the key facts it must contain (for answer metrics);
- some **unanswerable** questions, whose correct response is "I don't know", to check the system doesn't invent answers;
- some **hard cases**: questions needing two documents, exact part numbers, follow-ups, other languages.

Writing this by hand is slow. A common shortcut is to have an LLM **generate questions from chunks** ("write a question this passage answers"), then have people review and edit them. Generated questions tend to reuse the chunk's wording, which flatters keyword search, so mix in real ones.

### Retrieval metrics

For one query, with the retrieved list (best first) and the set of relevant chunk IDs:

| Metric | Question it answers | Formula |
|---|---|---|
| hit rate@k | did **any** relevant chunk make the top k? | 1 or 0 |
| recall@k | what share of the relevant chunks made the top k? | relevant in top k ÷ all relevant |
| precision@k | what share of the top k is relevant? | relevant in top k ÷ k |
| MRR (mean reciprocal rank) | how high is the **first** relevant chunk? | 1 ÷ its rank (0 if absent) |
| nDCG@k | are the relevant chunks near the top, with graded relevance? | discounted gain ÷ ideal gain |

Average each over all queries. For RAG, **recall@k** usually matters most: the model can ignore an irrelevant chunk, but can't use one that never arrived. Precision still matters for cost and focus.

```python
retrieved = ["c7", "c2", "c9", "c4", "c1"]     # best first
relevant = {"c2", "c4", "c8"}
k = 3
top = retrieved[:k]
hits = [doc for doc in top if doc in relevant]
print("recall@3   ", round(len(hits) / len(relevant), 3))
print("precision@3", round(len(hits) / k, 3))
first = next((rank for rank, doc in enumerate(retrieved, start=1) if doc in relevant), None)
print("reciprocal rank", round(1 / first, 3) if first else 0)
```

### Answer metrics

| Metric | Question |
|---|---|
| **faithfulness (groundedness)** | is every claim in the answer supported by the retrieved chunks? |
| answer relevance | does it actually answer the question asked? |
| correctness | does it match the reference answer's key facts? |
| citation accuracy | do the cited chunks really support the sentences that cite them? |
| refusal accuracy | does it say "I don't know" for unanswerable questions, and only for them? |

A few of these can be checked with code: citation numbers (Lesson 17), required facts present (Lesson 12), a crude word-overlap groundedness score (the second exercise). Most need **judgement**, so teams use an LLM as a grader with a clear rubric, checked against human ratings (Part 6). Libraries such as **Ragas** and **DeepEval** package these metrics (faithfulness, answer relevancy, context precision and context recall, among others).

### Diagnosing failures

| Symptom | Likely cause | Try |
|---|---|---|
| the relevant chunk isn't retrieved at all | vocabulary mismatch; chunk lacks context; bad chunking | hybrid search, contextual retrieval, different chunk size |
| it's retrieved, but ranked below k | weak ranking | reranker, larger k |
| exact codes and names are missed | embeddings only | add BM25 (hybrid) |
| follow-up questions fail | query lacks context | query rewriting |
| right chunks, wrong answer | prompt, model, or conflicting chunks | clearer instructions, quotes first, a stronger model |
| confident answers to unanswerable questions | no permission to refuse | "say you don't know"; test refusals |
| outdated answers | stale index | re-ingest on change; store dates; prefer recent |

Change **one thing at a time** and re-run the whole evaluation; improving one kind of question often worsens another.

### In production

Log each query with the retrieved chunk IDs and scores, the answer and any user feedback (thumbs up or down, follow-up corrections). Watch for queries with **low retrieval scores** (gaps in the documents), documents that are **never retrieved**, and questions users keep rephrasing. Add the interesting failures to your evaluation set: it should grow with the product.

:::exercise Retrieval metrics
Write `retrieval_metrics(results, relevant, k)`. `results[i]` is the ranked list of chunk IDs retrieved for query `i` (best first); `relevant[i]` is the set of relevant IDs for that query. For each query, using only the **top k**:

- recall = relevant IDs in the top k ÷ number of relevant IDs;
- precision = relevant IDs in the top k ÷ k;
- reciprocal rank = 1 ÷ the rank (from 1) of the first relevant ID in the top k, or 0 if none.

Skip queries whose relevant set is empty. Return a dict with the averages: `{"recall": …, "precision": …, "mrr": …}`, or all `0.0` if no queries count.
```python starter
def retrieval_metrics(results, relevant, k):
    pass

results = [["c7", "c2", "c9", "c4", "c1"], ["c3", "c5", "c6"]]
relevant = [{"c2", "c4", "c8"}, {"c3"}]
print(retrieval_metrics(results, relevant, 3))
# recall (1/3 + 1)/2 ≈ 0.667, precision (1/3 + 1/3)/2 ≈ 0.333, mrr (1/2 + 1)/2 = 0.75
```
```python check
fn = need("retrieval_metrics")
_r4 = lambda d: {key: round(v, 4) for key, v in d.items()} if isinstance(d, dict) else d
_res = [["c7", "c2", "c9", "c4", "c1"], ["c3", "c5", "c6"]]
_rel = [{"c2", "c4", "c8"}, {"c3"}]
test(fn, cases=[
    ((_res, _rel, 3), {"recall": 0.6667, "precision": 0.3333, "mrr": 0.75}, "two queries, k = 3"),
    ((_res, _rel, 5), {"recall": 0.8333, "precision": 0.3, "mrr": 0.75}, "k = 5"),
    ((_res, _rel, 1), {"recall": 0.5, "precision": 0.5, "mrr": 0.5}, "k = 1"),
    (([["a", "b"]], [{"z"}], 2), {"recall": 0.0, "precision": 0.0, "mrr": 0.0}, "a complete miss"),
    (([["a", "b"], ["c"]], [{"b"}, set()], 2), {"recall": 1.0, "precision": 0.5, "mrr": 0.5}, "a query without relevant IDs is skipped"),
    (([], [], 3), {"recall": 0.0, "precision": 0.0, "mrr": 0.0}, "no queries"),
    (([["x", "y", "a"]], [{"a"}], 2), {"recall": 0.0, "precision": 0.0, "mrr": 0.0}, "relevant, but below k"),
    (([["a"]], [{"a", "b"}], 4), {"recall": 0.5, "precision": 0.25, "mrr": 1.0}, "fewer results than k"),
], key=_r4, show="retrieval_metrics(results, relevant, {2})")
```
```python solution
def retrieval_metrics(results, relevant, k):
    recalls, precisions, reciprocal_ranks = [], [], []
    for retrieved, wanted in zip(results, relevant):
        if not wanted:
            continue                                   # nothing to find for this query
        top = retrieved[:k]
        hits = [doc for doc in top if doc in wanted]
        recalls.append(len(hits) / len(wanted))
        precisions.append(len(hits) / k)
        first = next((rank for rank, doc in enumerate(top, start=1) if doc in wanted), None)
        reciprocal_ranks.append(1 / first if first else 0.0)
    if not recalls:
        return {"recall": 0.0, "precision": 0.0, "mrr": 0.0}
    n = len(recalls)
    return {"recall": sum(recalls) / n, "precision": sum(precisions) / n, "mrr": sum(reciprocal_ranks) / n}

results = [["c7", "c2", "c9", "c4", "c1"], ["c3", "c5", "c6"]]
relevant = [{"c2", "c4", "c8"}, {"c3"}]
print(retrieval_metrics(results, relevant, 3))
```
hint: Walk the queries with `zip(results, relevant)`, skipping empty relevant sets, and work only with `retrieved[:k]`.
hint: The hits are the top-k IDs that are in the relevant set. Precision divides by `k` (not by the number retrieved).
hint: For the reciprocal rank, find the first `rank` (from 1) in the top k whose ID is relevant: `next((rank for rank, doc in enumerate(top, start=1) if doc in wanted), None)`.
approach:
1. **Understand:** three per-query numbers from the top k, averaged over the queries that have relevant IDs.
2. **Examples:** query 1 top 3 = c7, c2, c9: one hit (c2, rank 2) → recall 1/3, precision 1/3, RR 1/2.
3. **Brute force:** this is already one pass per query.
4. **Pattern:** **per-query metrics, then macro-average**.
5. **Plan:** loop → skip empties → top k → hits → three numbers → averages.
6. **Code and test:** k = 1, a complete miss, fewer results than k, empty relevant sets, no queries.
walkthrough:
**Line by line**

- Skipping queries with no relevant IDs avoids dividing by zero in recall (unanswerable questions are evaluated on the answer instead).
- Precision divides by `k` even when fewer than k results came back: empty slots count as misses.
- `next(..., None)` returns the first matching rank or `None`, giving a reciprocal rank of 0.
- Each metric is averaged over the same set of queries, so they're comparable.

**Trace** for k = 5: query 1 top 5 has c2 (rank 2) and c4 (rank 4) → recall 2/3, precision 2/5, RR 1/2; query 2 → recall 1, precision 1/5, RR 1. Averages: 0.833, 0.3, 0.75.

**Complexity:** O(queries × k).

**Common wrong approach:** measuring only the final answers, so when quality drops you can't tell whether retrieval or generation broke.
:::

:::exercise A crude groundedness check
Before reaching for an LLM grader, a word-overlap check catches the worst unsupported sentences. Write `groundedness(answer, sources, threshold=0.5)` returning `(score, unsupported)`:

- Split the answer into sentences with `re.split(r"(?<=[.!?])\s+", answer.strip())`, ignoring empty pieces.
- A sentence's **content words** are its distinct tokens (`re.findall(r"[a-z0-9]+", sentence.lower())`) that have **4 or more characters** or contain a **digit**.
- A sentence is **supported** if, for at least one source, the fraction of its content words appearing in that source's tokens is at least `threshold`. Sentences with no content words are ignored.
- `score` is supported sentences ÷ counted sentences (`1.0` if none were counted); `unsupported` lists the unsupported sentences in order.
```python starter
import re

def groundedness(answer, sources, threshold=0.5):
    pass

sources = ["Puncture repairs cost £12 and are usually done the same day.",
           "Unused items can be returned within 30 days with a receipt."]
answer = "A puncture repair costs £12. It is usually done the same day. We also offer free tea."
print(groundedness(answer, sources))
# (0.6666666666666666, ['We also offer free tea.'])
```
```python check
fn = need("groundedness")
_s = ["Puncture repairs cost £12 and are usually done the same day.",
      "Unused items can be returned within 30 days with a receipt."]
_r = lambda result: (round(result[0], 4), result[1]) if isinstance(result, tuple) and len(result) == 2 else result
test(fn, cases=[
    (("A puncture repair costs £12. It is usually done the same day. We also offer free tea.", _s),
     (0.6667, ["We also offer free tea."]), "one invented sentence"),
    (("Unused items can be returned within 30 days.", _s), (1.0, []), "fully supported"),
    (("Returns are accepted within 90 days.", _s), (0.0, ["Returns are accepted within 90 days."]), "a wrong number"),
    (("Yes. OK!", _s), (1.0, []), "no content words: nothing to check"),
    (("", _s), (1.0, []), "empty answer"),
    (("Puncture repairs and returned items.", _s), (1.0, []), "2 of 4 content words from one source meets the threshold"),
    (("Puncture repairs and returned items.", _s, 0.75), (0.0, ["Puncture repairs and returned items."]), "a stricter threshold"),
    (("Frames have a lifetime warranty.", []), (0.0, ["Frames have a lifetime warranty."]), "no sources"),
], key=_r, show="groundedness({0}, sources, ...)")
```
```python solution
import re

def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def content_words(sentence):
    return {w for w in tokens(sentence) if len(w) >= 4 or any(ch.isdigit() for ch in w)}

def groundedness(answer, sources, threshold=0.5):
    source_tokens = [tokens(s) for s in sources]
    counted, unsupported = 0, []
    for sentence in re.split(r"(?<=[.!?])\s+", answer.strip()):
        words = content_words(sentence)
        if not sentence or not words:
            continue
        counted += 1
        best = max((len(words & st) / len(words) for st in source_tokens), default=0.0)
        if best < threshold:
            unsupported.append(sentence)
    score = 1.0 if counted == 0 else (counted - len(unsupported)) / counted
    return score, unsupported

sources = ["Puncture repairs cost £12 and are usually done the same day.",
           "Unused items can be returned within 30 days with a receipt."]
answer = "A puncture repair costs £12. It is usually done the same day. We also offer free tea."
print(groundedness(answer, sources))
```
hint: Turn each source into a set of tokens once. For each sentence, build its set of content words (4+ characters, or containing a digit).
hint: A sentence's support is its **best** overlap with any single source: `max(len(words & src) / len(words) for src in source_tokens)`. Use `default=0.0` for no sources.
hint: Count only sentences with content words; the score is (counted − unsupported) ÷ counted, or 1.0 when nothing was counted.
approach:
1. **Understand:** per sentence, is most of its vocabulary present in one source? Then a ratio and the failures.
2. **Examples:** "A puncture repair costs £12." → content words {puncture, repair, costs, 12}; the repairs source has puncture and 12 (not "repair" or "costs") → 2/4 = 0.5 → supported at threshold 0.5.
3. **Brute force:** this is already direct.
4. **Pattern:** **lexical overlap as a cheap proxy** for support.
5. **Plan:** source token sets → for each sentence: content words → best overlap → compare with the threshold → score.
6. **Code and test:** invented sentences, wrong numbers, no content words, no sources, thresholds.
walkthrough:
**Line by line**

- Counting tokens with digits as content words means numbers get checked: "Returns are accepted within 90 days." has content words {returns, accepted, within, 90, days}, and only "within" and "days" appear in the returns source (2/5 = 0.4), so it's flagged.
- Taking the **best single source** (not all sources pooled) avoids "supporting" a claim with words scattered across unrelated documents.
- Sentences like "Yes." have no content words and are skipped, rather than counted as unsupported.
- `max(..., default=0.0)` handles an empty source list.

**Trace** on the first case: sentence 1 overlaps 2/4 with the repairs source → supported; sentence 2 {usually, done, same} → all three present → supported; sentence 3 {also, offer, free} → nothing → unsupported. Score 2/3.

**Complexity:** O(sentences × sources × words).

**Common wrong approach:** treating this as proof. Word overlap misses paraphrases ("costs" versus "cost") and can't see contradictions that reuse the source's words ("returns are **not** accepted within 30 days" overlaps perfectly). Use it as a fast first filter, and an LLM judge or human review for the real verdict (Part 6).
:::

:::quiz
? Retrieval found the right chunk, but the answer is wrong. Where should you look?
+ The generation step: the prompt, the model, or conflicting chunks
- The embedding model
- The chunk size
= Diagnose which half failed before changing anything.
? Why does recall@k usually matter more than precision@k for RAG?
+ The model can ignore an irrelevant chunk but can't use a relevant one that was never retrieved
- Precision can't be measured
- Recall is cheaper to compute
= Missing evidence can't be recovered later in the pipeline.
? Why include unanswerable questions in a RAG evaluation set?
+ To check the system says "I don't know" instead of inventing an answer
- To make the scores look better
- Because every question must be unanswerable
= Refusal accuracy is part of quality.
? What's a weakness of word-overlap groundedness checks?
+ They miss paraphrases and can't detect contradictions that reuse the source's words
- They're too slow
- They need a GPU
= Use them as a cheap filter, not a verdict.
:::
