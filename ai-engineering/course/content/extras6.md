@@ evals
topics: why LLM features need evals, success criteria, tasks, trials, graders, transcripts and outcomes, code, model and human grading, capability and regression evals, pass@k and pass^k, how many cases to start with, noise in small samples, paired comparison of runs, eval-driven development, reading transcripts, grading outcomes rather than paths, overfitting to an eval set
terms:
- **Eval (evaluation):** a repeatable measurement of how well an AI system performs on a set of cases.
- **Task (case):** one test input with its success criteria.
- **Trial:** one attempt at a task; several trials reveal variability.
- **Grader:** code, a model or a person that scores a trial.
- **Transcript (trace):** the full record of a trial, including tool calls and intermediate steps.
- **Regression eval:** a suite that should keep passing, run on every change.
- **pass@k:** the probability that at least one of k attempts succeeds.
- **pass^k:** the probability that all k attempts succeed.
mistakes:
- Changing prompts or models without running an eval.
- Comparing totals instead of which cases flipped.
- Treating small differences on small sets as real.
- Grading the steps an agent took instead of the outcome.
- Tuning against the same cases until the prompt overfits them.

glance:
- pass@k and pass^k | per task: 1 − C(n − c, k) ÷ C(n, k) and C(c, k) ÷ C(n, k); average | O(trials) | O(tasks)
- Compare runs | shared cases; rates; fixed and broken lists | O(n log n) | O(n)
- Margin of a pass rate | about 1.96 × √(p(1 − p) ÷ n) | O(1) | O(1)

@@ llm-as-judge
topics: model-graded evaluation, judge prompts and rubrics, pass/fail and small scales, reasoning before the verdict, one criterion per judge, pointwise, reference-based and pairwise judging, position bias, length bias, self-preference, leniency, calibrating judges against human labels, raw agreement versus Cohen's kappa, judge cost
terms:
- **LLM as a judge:** using a model, prompted with a rubric, to grade outputs.
- **Rubric:** the explicit criteria and score definitions a grader applies.
- **Pairwise judging:** asking which of two outputs is better.
- **Position bias:** a judge favouring an answer because of where it appears.
- **Length (verbosity) bias:** a judge favouring longer answers.
- **Self-preference bias:** a judge favouring outputs from its own model or style.
- **Cohen's kappa:** agreement between two graders, corrected for agreement expected by chance.
mistakes:
- Vague rubrics such as "rate the quality from 1 to 10".
- Trusting a judge that was never compared with human labels.
- Reporting raw agreement when one label dominates.
- Judging pairs in only one order.
- Letting one judge score many unrelated criteria at once.

glance:
- Cohen's kappa | (observed − chance agreement) ÷ (1 − chance agreement) | O(n × labels) | O(labels)
- Pairwise verdict | judge both orders; count only consistent wins | 2 judge calls | O(1)
- Calibrate a judge | human labels on a sample; agreement and kappa; read disagreements | O(sample) | O(sample)

@@ hallucinations
topics: factual and unfaithful hallucinations, fabricated references, invented code and packages, false action reports, why models hallucinate, rewards for guessing, grounding, permission to abstain, quotes and citations, tools for facts, narrowing tasks, verification passes and chain-of-verification, checking numbers and claims against sources, consistency across samples, faithfulness judges, measuring hallucination rates
terms:
- **Hallucination:** fluent, confident output that is false or unsupported.
- **Faithfulness:** agreement between an answer and the sources it was given.
- **Abstention:** the model declining to answer when it lacks the information.
- **Chain-of-verification:** drafting, generating verification questions, answering them independently, then revising.
- **Self-consistency check:** comparing several samples to find details that vary.
- **Slopsquatting:** registering package names that models commonly invent, to trap people who install them.
mistakes:
- Asking models to recall facts they could look up with a tool.
- Not giving the model a way to say "I don't know".
- Trusting an agent's report of an action without checking the outcome.
- Installing a package a model suggested without checking it exists and is legitimate.
- Treating every flagged number or unverifiable claim as a confirmed hallucination.

glance:
- Unsupported numbers | extract; normalise to values; set difference with the sources | O(answer + sources) | O(numbers)
- Verify claims | normalised (subject, attribute) lookup; supported, contradicted or unverifiable | O(facts + claims) | O(facts)
- Reduce hallucination | ground, allow abstention, quote, cite, use tools, verify | — | —

@@ observability
topics: why LLM applications need observability, traces and spans, waterfalls, what to record for requests, model calls, retrieval and tools, user feedback, OpenTelemetry generative-AI conventions, LLM observability tools, privacy, redaction and retention, online evaluation of live traffic, dashboards, alerts, turning traces into eval cases
terms:
- **Observability:** recording enough about each request to explain its behaviour afterwards.
- **Trace:** the record of one request, made of nested spans.
- **Span:** one timed step of a request, with a name, a parent and attributes.
- **Waterfall:** a chart of spans on a timeline showing where time was spent.
- **OpenTelemetry:** an open standard and toolkit for traces, metrics and logs.
- **Online evaluation:** grading a sample of live production traffic.
mistakes:
- Logging only errors, so normal-but-wrong answers leave no trace.
- Not recording which prompt and model version produced an answer.
- Storing full prompts and responses with personal data and no retention policy.
- Assuming child spans arrive after their parents.
- Never turning production failures into eval cases.

glance:
- Trace tree | group spans by parent; depth-first walk from the roots | O(n) | O(n)
- Trace summary | counts and sums with defaults; the slowest span | O(n) | O(1)
- Production loop | trace → dashboards and alerts → sample and grade → new eval cases | — | —

@@ cost-and-latency
topics: the parts of request latency, time to first token, output speed, why output length dominates, agents and tool time, percentiles and tail latency, latency and cost levers, routing, effort, prompt caching, streaming, parallel calls, exact and semantic response caches, the Batch API, rate limits, capacity planning, queues, timeouts and fallbacks, projecting monthly cost
terms:
- **Time to first token (TTFT):** the delay before the first output token arrives.
- **Output speed:** how many tokens per second the model generates.
- **Percentile (p95):** the value below which that percentage of measurements fall.
- **Tail latency:** the slowest requests, measured by p95 and p99.
- **Response cache:** stored answers reused for repeated questions.
- **Semantic cache:** a response cache that matches questions by meaning (embeddings) rather than exact text.
- **Fallback:** an alternative model, provider or non-AI path used when the primary fails.
mistakes:
- Reporting average latency instead of percentiles.
- Ignoring output length as the main driver of latency and cost.
- Caching answers that depend on the user or on live data.
- Planning capacity for average rather than peak traffic.
- Having no timeout or fallback when the model API is slow or down.

glance:
- Latency estimate | TTFT + output tokens ÷ tokens per second | O(1) | O(1)
- Nearest-rank percentile | sort; value at rank ceil(p ÷ 100 × n) | O(n log n) | O(n)
- Exact response cache | normalised key → stored time; hit if younger than the TTL | O(n) | O(distinct questions)

@@ fine-tuning-vs-rag
topics: the ladder of ways to adapt a model, prompting, examples, retrieval and tools, fine-tuning, training from scratch, what fine-tuning changes, supervised, preference and reinforcement fine-tuning, DPO, LoRA and QLoRA, distillation, where fine-tuning is available, open-weight models, JSONL training data, data quality, validation, deduplication and leakage, comparing with a prompted baseline, ongoing costs
terms:
- **Fine-tuning:** further training of a pretrained model on your own examples.
- **Supervised fine-tuning (SFT):** training on example conversations with ideal responses.
- **Direct preference optimisation (DPO):** training on pairs of better and worse responses.
- **Reinforcement fine-tuning (RFT):** training that rewards responses a grader scores highly.
- **LoRA:** a parameter-efficient method that trains small adapter matrices on frozen weights.
- **Distillation:** training a smaller model to imitate a larger model on a task.
- **Data leakage:** test examples (or near-copies) appearing in the training data.
mistakes:
- Fine-tuning to add facts that change, instead of using retrieval.
- Fine-tuning before trying better prompts and examples.
- Training on noisy or inconsistent examples.
- Splitting train and test before removing near-duplicates.
- Forgetting the ongoing costs: hosting, retraining and missing base-model upgrades.

glance:
- Validate chat data | per record: structure, roles and content, alternation, final assistant | O(messages) | O(problems)
- Leak-free split | dedupe normalised inputs; seeded shuffle; slice | O(n) | O(n)
- Choose an approach | prompt → examples → RAG and tools → fine-tune, climbing only when evals demand it | — | —
