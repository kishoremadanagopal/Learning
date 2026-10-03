@@ rag-pipeline
topics: knowledge cutoffs and private data, retrieval-augmented generation, ingestion (load, clean, chunk, index, metadata), query time (retrieve, augment, generate), a tiny end-to-end RAG system, instructions to use only the documents, saying "I don't know", citing sources, the citations API, when to put everything in the prompt instead, structured data and tools, per-user permissions
terms:
- **Retrieval-augmented generation (RAG):** retrieving relevant passages and adding them to the prompt so the model answers from them.
- **Corpus:** the whole collection of documents you search.
- **Chunk:** a passage of a document, the unit that is indexed and retrieved.
- **Ingestion:** loading, cleaning, chunking and indexing documents ahead of time.
- **Retriever:** the component that finds the chunks most relevant to a query.
- **Grounding:** basing an answer on provided evidence rather than the model's memory.
- **Citation:** a reference from a statement in the answer to the source that supports it.
mistakes:
- Building retrieval when the whole knowledge base would fit in the prompt.
- Not telling the model what to do when the documents don't contain the answer.
- Dropping source and permission metadata during ingestion.
- Embedding structured data such as prices or stock levels as text instead of querying it.
- Trusting citation numbers without checking them.

glance:
- Word-overlap retrieval | score = shared distinct words; stable sort; top k | O(n · m + n log n) | O(n)
- Check citations | regex for [n]; split sentences; set arithmetic | O(n) | O(n)
- RAG query | retrieve → insert chunks with sources → question last → answer with citations | — | —

@@ chunking
topics: why documents are chunked, the chunk-size trade-off, fixed-size chunks, overlap, sentence and paragraph boundaries, recursive splitting, structure-aware chunking with headings, tables and code, chunk metadata, chunk headers, contextual retrieval, contextualised chunk embeddings, small-to-big retrieval
terms:
- **Chunk size:** how much text goes in each chunk, usually measured in tokens.
- **Overlap:** text repeated at the end of one chunk and the start of the next.
- **Recursive splitting:** splitting on the largest separator first, falling back to smaller ones only when needed.
- **Structure-aware chunking:** splitting along a document's own structure, such as headings or code functions.
- **Chunk header:** the title and section path prepended to a chunk's text.
- **Contextual retrieval:** prepending a short model-written context to each chunk before indexing it.
- **Small-to-big retrieval:** matching small chunks but giving the model their larger parent section.
mistakes:
- Picking a chunk size without testing it on real questions.
- Splitting sentences, table rows or code blocks in half.
- Losing the title and section that give a chunk its meaning.
- Treating `#` lines inside code blocks as headings.
- Adding chunks that only repeat the overlap.

glance:
- Fixed-size chunks | sliding window with step size − overlap | O(n) | O(n)
- Split by headings | stack of open headings; flush at each heading | O(n) | O(n)
- Context for chunks | headers, contextual retrieval, small-to-big | — | —

@@ keyword-search
topics: inverted indexes and postings lists, boolean AND queries, term frequency, inverse document frequency, the BM25 formula, saturation (k1) and length normalisation (b), Lucene's IDF variant, tokenising, stop words, stemming and lemmatisation, other languages, keyword versus vector search, BM25 tools and libraries
terms:
- **Inverted index:** a map from each word to the documents (and often positions) where it appears.
- **Postings list:** the list of documents for one word in an inverted index.
- **Term frequency (TF):** how often a word appears in a document.
- **Inverse document frequency (IDF):** a weight that is high for words found in few documents.
- **BM25:** a ranking formula combining IDF, saturated term frequency and document-length normalisation.
- **Stemming:** cutting words to a common root so variants match.
- **Lemmatisation:** mapping words to their dictionary form.
mistakes:
- Ranking by raw word counts, so long or repetitive documents win.
- Expecting keyword search to match synonyms or paraphrases.
- Forgetting stemming, so "frames" never matches "frame".
- Comparing BM25 scores from different tools or collections as if they were on one scale.
- Scanning every document at query time instead of using an index.

glance:
- Build an inverted index | for each document, add its id to each distinct word's list | O(total tokens) | O(total tokens)
- AND query | intersect the postings lists | O(sum of list lengths) | O(shortest list)
- BM25 score | Σ IDF × f(k1 + 1) ÷ (f + k1(1 − b + b·len ÷ avgdl)) | O(query terms × postings) | O(documents)

@@ vector-search
topics: semantic search, embedding documents and queries, input types, using one model for both, exact search as a matrix-vector product, memory costs, reducing dimensions, quantisation, approximate nearest-neighbour search, IVF, HNSW, product quantisation, recall, metadata filtering, pre-filtering and post-filtering, access control, pgvector, FAISS and vector databases
terms:
- **Semantic search:** finding text by meaning, using embeddings, rather than by shared words.
- **Exact (brute-force) search:** scoring every vector; perfectly accurate, linear in the corpus size.
- **Approximate nearest-neighbour (ANN) search:** an index that finds nearly the best matches while scoring only some vectors.
- **IVF (inverted file index):** vectors grouped into buckets around centroids; a query searches the nearest buckets.
- **HNSW:** a layered graph of neighbouring vectors, searched by greedy walks.
- **Quantisation:** storing numbers with fewer bits to save memory.
- **Recall@k:** the share of the true top-k results that a search returns.
- **Vector database:** a store for vectors and metadata with indexes for similarity search and filtering.
mistakes:
- Embedding queries and documents with different models.
- Re-embedding the corpus on every query.
- Ranking by raw dot products of unnormalised vectors.
- Post-filtering with a fixed k and getting too few results.
- Trusting an ANN index without measuring its recall.

glance:
- Exact vector search | normalise; matrix-vector product; argsort | O(n · d) | O(n · d)
- Filtered search | pre-filter by metadata, then rank | O(n · d + m log m) | O(m)
- IVF search | score centroids; search the n_probe nearest buckets | O(c · d + m · d) | O(n · d)
- HNSW search | greedy walk through layered neighbour graphs | about O(log n) per query | O(n · d + links)

@@ hybrid-and-reranking
topics: hybrid search, the retrieval funnel, why scores from different retrievers can't be added, reciprocal rank fusion, weighted score fusion, min-max normalisation, bi-encoders and cross-encoders, rerankers, how many chunks to pass to the model, contextual retrieval results, query rewriting, multi-query retrieval, hypothetical document embeddings (HyDE), routing
terms:
- **Hybrid search:** running keyword and vector search and merging their results.
- **Reciprocal rank fusion (RRF):** merging ranked lists by summing 1 ÷ (k + rank) for each document.
- **Min-max normalisation:** rescaling scores to 0–1 using the list's minimum and maximum.
- **Bi-encoder:** a model that embeds query and document separately; fast and precomputable.
- **Cross-encoder (reranker):** a model that reads query and document together and scores their relevance.
- **Query rewriting:** turning a question into a better search query, such as a standalone version of a follow-up.
- **HyDE:** searching with the embedding of a model-written hypothetical answer.
mistakes:
- Adding raw scores from different retrievers.
- Running a reranker over the entire corpus.
- Passing only one or two chunks when the evaluation shows more help.
- Searching with an unrewritten follow-up question.
- Adding retrieval tricks without measuring whether they help.

glance:
- Reciprocal rank fusion | sum 1 ÷ (k + rank) per document; sort | O(entries + D log D) | O(D)
- Weighted fusion | min-max each list; α·vector + (1 − α)·keyword | O(D log D) | O(D)
- Rerank | score each shortlist item with a cross-encoder; keep the top n | O(shortlist) model calls | O(shortlist)

@@ evaluating-rag
topics: measuring retrieval and generation separately, building an evaluation set, relevant chunk labels, reference answers, unanswerable and hard questions, generated questions, hit rate, recall@k, precision@k, mean reciprocal rank, nDCG, faithfulness, answer relevance, correctness, citation accuracy, refusal accuracy, LLM graders, Ragas and DeepEval, diagnosing failures, monitoring in production
terms:
- **Evaluation set:** a fixed collection of questions with the expected relevant chunks and answers.
- **Recall@k:** the share of relevant chunks that appear in the top k results.
- **Precision@k:** the share of the top k results that are relevant.
- **Mean reciprocal rank (MRR):** the average of 1 ÷ the rank of the first relevant result.
- **nDCG:** a ranking score that rewards relevant results near the top, allowing graded relevance.
- **Faithfulness (groundedness):** whether every claim in an answer is supported by the retrieved context.
- **Refusal accuracy:** whether the system declines exactly the questions it can't answer from its sources.
mistakes:
- Judging a RAG system only by its final answers.
- Evaluating only on questions generated from the chunks themselves.
- Leaving out unanswerable questions.
- Changing several settings at once and re-running nothing.
- Treating a word-overlap score as proof of faithfulness.

glance:
- Recall and precision at k | hits in top k ÷ relevant, and ÷ k | O(queries × k) | O(k)
- Mean reciprocal rank | 1 ÷ rank of the first hit, averaged | O(queries × k) | O(1)
- Crude groundedness | content-word overlap with the best single source | O(sentences × sources × words) | O(words)
