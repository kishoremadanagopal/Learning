@@@ part
id: 6
title: Evals and Production
level: Advanced
blurb: Shipping LLM features you can trust: building evaluation sets, grading with code and with models, catching hallucinations, tracing and monitoring in production, managing cost and latency, and deciding between prompting, RAG and fine-tuning.

@@@ lesson
id: evals
title: Evaluations (evals)
minutes: 26
summary: Why LLM features need evals, success criteria, tasks, trials, graders and transcripts, code-based, model-based and human grading, capability and regression evals, pass@k and pass^k, how many cases you need and the noise in small samples, comparing two runs case by case, and eval-driven development.
---
Traditional code is tested with exact expectations: `add(2, 3) == 5`. LLM output varies from run to run, has many acceptable forms, and changes when you edit a prompt or switch model. **Evals** (evaluations) are how you still know whether a change made things better or worse. Without them, every prompt tweak is a guess, and every model upgrade is a gamble.

### The vocabulary

Anthropic's engineering guide to agent evals (January 2026) uses a clear set of terms:

- **Task (case):** one test: an input plus success criteria.
- **Trial:** one attempt at a task. Outputs vary, so important tasks get several trials.
- **Grader:** the logic that scores some aspect of a trial.
- **Transcript (trace):** the full record of a trial: the output, tool calls, reasoning and intermediate results.
- **Outcome:** the final state of the world, such as whether the refund was actually issued, not just whether the agent **said** it was.

### Three kinds of grader

| Grader | Good | Bad | Example |
|---|---|---|---|
| **code** | fast, cheap, objective, repeatable | brittle: may reject valid variations | exact label match, valid JSON, required phrases, tests pass |
| **model** (LLM as judge) | flexible, handles nuance, scales | non-deterministic; must be calibrated | "Is this reply polite and does it answer the question? 1–5" |
| **human** | the gold standard | slow and expensive | expert review of a sample |

Use code wherever the criterion allows it (Lessons 9 and 12 built several such checks), a model for judgement calls (Lesson 29), and humans to build reference labels and to check that the model grader agrees with people.

Anthropic's evaluation guidance favours **volume**: more cases with automated, slightly noisier grading beat a handful of perfect human-graded ones.

### Capability and regression evals

- **Capability evals** measure what the system **can't yet** do well. They should start with a low pass rate, and they show progress.
- **Regression evals** check the system **still** handles everything it used to. They should pass at close to 100%, and run on every change, like unit tests in CI.

When a capability eval reaches a high pass rate, its cases graduate into the regression suite.

### Several trials: pass@k and pass^k

When outputs vary, one trial per task can mislead. With several trials per task:

- **pass@k:** the probability that **at least one** of k attempts succeeds. Right when one success is enough (generate five candidate fixes, keep one that passes the tests).
- **pass^k:** the probability that **all** k attempts succeed. Right when users need it to work **every** time (a customer-facing agent).

A task solved in 3 of 5 trials looks good on pass@5 (it almost always gets there eventually) and poor on pass^5. The first exercise computes both.

### How many cases?

Start with **20–50 tasks** drawn from real failures and real usage; early on, improvements are large enough to see. But small sets are noisy:

```python
import math

for n in (20, 50, 200, 1000):
    p = 0.8                                             # an observed pass rate of 80%
    margin = 1.96 * math.sqrt(p * (1 - p) / n)          # approximate 95% interval
    print(f"{n:>5} cases: 80% ± {margin:.0%}")
```

With 50 cases, 80% means "somewhere around 69–91%". A two-point improvement on such a set is noise. Grow the set as the system matures, and compare versions **on the same cases** (the second exercise): the cases that flipped tell you more than the totals.

### Eval-driven development

![A cycle of five steps: collect real failures and usage into eval cases; run the evals on the current version; read the transcripts of failures; change one thing (prompt, retrieval, tools, model); re-run and compare case by case, then repeat. Passing capability cases move into the regression suite](figures/eval-cycle.svg)

- **Write the eval before the fix:** turn every bug report into a case.
- **Read transcripts.** Scores say *that* something failed; transcripts say *why*, and whether the grader was wrong. Failures should look fair.
- **Grade the outcome, not the path:** don't fail an agent for solving a task in a different order than you expected.
- **Watch for overfitting:** tuning a prompt against the same 30 cases for weeks makes it good at those 30. Keep a held-out set.

:::exercise pass@k and pass^k
For each task you ran `n` trials and recorded which passed. Write `pass_metrics(trials, k)`, where `trials` maps each task to its list of booleans. For a task with `n` trials of which `c` passed, the standard unbiased estimates are:

- pass@k = 1 − C(n − c, k) / C(n, k)
- pass^k = C(c, k) / C(n, k)

where C is the binomial coefficient (`math.comb`, which returns 0 when the top is smaller than the bottom). Return `{"pass@k": …, "pass^k": …}`, each **averaged over the tasks**. Raise `ValueError` if any task has fewer than `k` trials, or if there are no tasks.
```python starter
import math

def pass_metrics(trials, k):
    pass

trials = {"refund": [True, True, False, True, False],
          "address-change": [True, True, True, True, True],
          "cancel-order": [False, False, False, True, False]}
print(pass_metrics(trials, 1))
print(pass_metrics(trials, 3))
```
```python check
import math
fn = need("pass_metrics")
_r4 = lambda d: {key: round(v, 4) for key, v in d.items()} if isinstance(d, dict) else d
_t = {"refund": [True, True, False, True, False], "address-change": [True] * 5, "cancel-order": [False, False, False, True, False]}
test(fn, cases=[
    ((_t, 1), {"pass@k": 0.6, "pass^k": 0.6}, "k = 1 is the plain pass rate"),
    ((_t, 3), {"pass@k": 0.8667, "pass^k": 0.3667}, "k = 3"),
    ((_t, 5), {"pass@k": 1.0, "pass^k": 0.3333}, "k = n"),
    (({"a": [True, False]}, 2), {"pass@k": 1.0, "pass^k": 0.0}, "one success in two trials"),
    (({"a": [False, False, False]}, 2), {"pass@k": 0.0, "pass^k": 0.0}, "never passes"),
    (({"a": [True, True, True, False]}, 2), {"pass@k": 1.0, "pass^k": 0.5}, "three of four"),
], key=_r4, show="pass_metrics(trials, {1})")
for _bad, _k in [({"a": [True]}, 2), ({}, 1)]:
    try:
        fn(_bad, _k)
    except ValueError:
        pass
    else:
        raise AssertionError(f"pass_metrics({_bad}, {_k}) should raise ValueError.")
```
```python solution
import math

def pass_metrics(trials, k):
    if not trials:
        raise ValueError("no tasks")
    at_least_one, all_pass = [], []
    for task, results in trials.items():
        n, c = len(results), sum(results)
        if n < k:
            raise ValueError(f"task {task!r} has {n} trials; need at least {k}")
        total = math.comb(n, k)
        at_least_one.append(1 - math.comb(n - c, k) / total)   # 1 − P(all k picked trials failed)
        all_pass.append(math.comb(c, k) / total)               # P(all k picked trials passed)
    return {"pass@k": sum(at_least_one) / len(trials), "pass^k": sum(all_pass) / len(trials)}

trials = {"refund": [True, True, False, True, False],
          "address-change": [True, True, True, True, True],
          "cancel-order": [False, False, False, True, False]}
print(pass_metrics(trials, 1))
print(pass_metrics(trials, 3))
```
hint: For each task, `n = len(results)` and `c = sum(results)` (True counts as 1).
hint: C(n − c, k) / C(n, k) is the chance that k trials picked at random are **all failures**; pass@k is one minus that. C(c, k) / C(n, k) is the chance they're **all successes**.
hint: Average each metric over the tasks; check `n < k` (and no tasks) first and raise `ValueError`.
approach:
1. **Understand:** per task, two probabilities about choosing k of its n recorded trials; then the mean over tasks.
2. **Examples:** refund has c = 3 of n = 5; for k = 3: pass@3 = 1 − C(2, 3)/C(5, 3) = 1 − 0/10 = 1, pass^3 = C(3, 3)/10 = 0.1.
3. **Brute force:** enumerate every subset of k trials and count: same numbers, exponentially slower.
4. **Pattern:** **combinatorial estimates** averaged over tasks.
5. **Plan:** validate → per task (n, c, two formulas) → averages.
6. **Code and test:** k = 1, k = n, all failing, all passing, too few trials.
walkthrough:
**Line by line**

- `sum(results)` counts the passes because `True` is 1 in arithmetic.
- `math.comb(n - c, k)` is 0 when there are fewer than k failures, so pass@k becomes exactly 1: any k trials must include a success.
- With k = 1 both formulas reduce to c / n, the ordinary pass rate.
- Averaging per task (rather than pooling all trials) weights every task equally.

**Trace** for k = 3: refund (1, 0.1), address-change (1, 1), cancel-order (1 − C(4, 3)/10 = 0.6, 0) → pass@3 = 2.6/3 ≈ 0.867, pass^3 = 1.1/3 ≈ 0.367.

**Complexity:** O(total trials).

**Common wrong approach:** estimating pass@k as 1 − (1 − p)^k from the overall pass rate p. It assumes every task is equally hard; in reality some tasks always pass and others never do, which the per-task formula captures.
:::

:::exercise Compare two eval runs
Totals hide what changed. Write `compare_runs(before, after)`, where each maps case IDs to `True` (pass) or `False` (fail). Consider only the cases present in **both** runs. Return:

```text
{"before": pass rate before, "after": pass rate after,
 "fixed": sorted IDs that went False → True,
 "broken": sorted IDs that went True → False}
```

Pass rates are fractions between 0 and 1 (`0.0` if there are no shared cases).
```python starter
def compare_runs(before, after):
    pass

before = {"refund": True, "cancel": False, "address": True, "warranty": False}
after = {"refund": True, "cancel": True, "address": False, "warranty": True, "new-case": True}
print(compare_runs(before, after))
# {'before': 0.5, 'after': 0.75, 'fixed': ['cancel', 'warranty'], 'broken': ['address']}
```
```python check
fn = need("compare_runs")
test(fn, cases=[
    (({"refund": True, "cancel": False, "address": True, "warranty": False},
      {"refund": True, "cancel": True, "address": False, "warranty": True, "new-case": True}),
     {"before": 0.5, "after": 0.75, "fixed": ["cancel", "warranty"], "broken": ["address"]}, "fixes and a break"),
    (({"a": True, "b": True}, {"a": True, "b": True}), {"before": 1.0, "after": 1.0, "fixed": [], "broken": []}, "no change"),
    (({"a": True, "b": False}, {"a": False, "b": True}), {"before": 0.5, "after": 0.5, "fixed": ["b"], "broken": ["a"]}, "same total, different cases"),
    (({"x": True}, {"y": False}), {"before": 0.0, "after": 0.0, "fixed": [], "broken": []}, "no shared cases"),
    (({}, {}), {"before": 0.0, "after": 0.0, "fixed": [], "broken": []}, "empty runs"),
    (({"c": False, "a": False, "b": False}, {"c": True, "a": True, "b": True}), {"before": 0.0, "after": 1.0, "fixed": ["a", "b", "c"], "broken": []}, "sorted IDs"),
], show="compare_runs(before, after)")
```
```python solution
def compare_runs(before, after):
    shared = before.keys() & after.keys()
    if not shared:
        return {"before": 0.0, "after": 0.0, "fixed": [], "broken": []}
    return {
        "before": sum(before[c] for c in shared) / len(shared),
        "after": sum(after[c] for c in shared) / len(shared),
        "fixed": sorted(c for c in shared if not before[c] and after[c]),
        "broken": sorted(c for c in shared if before[c] and not after[c]),
    }

before = {"refund": True, "cancel": False, "address": True, "warranty": False}
after = {"refund": True, "cancel": True, "address": False, "warranty": True, "new-case": True}
print(compare_runs(before, after))
```
hint: `before.keys() & after.keys()` gives the shared case IDs (dict key views support set operations).
hint: Pass rates are `sum(results) / count` over the shared IDs, because `True` counts as 1.
hint: Fixed: `not before[c] and after[c]`; broken: `before[c] and not after[c]`; sort both lists.
approach:
1. **Understand:** a paired comparison on the same cases: rates plus the flips in each direction.
2. **Examples:** same total (0.5 → 0.5) can hide one fix and one break.
3. **Brute force:** this is already linear.
4. **Pattern:** **paired comparison** over the intersection.
5. **Plan:** intersection → guard → rates → fixed and broken lists.
6. **Code and test:** unchanged, swapped, disjoint, empty.
walkthrough:
**Line by line**

- Using only shared cases keeps the comparison fair when the eval set grew between runs (`new-case` is ignored).
- Key views support `&`, so there's no need to build sets by hand.
- `sorted(...)` gives stable, readable output for reports and tests.
- The early return avoids dividing by zero.

**Trace:** shared = refund, cancel, address, warranty → before 2/4, after 3/4; cancel and warranty flipped to pass, address flipped to fail.

**Complexity:** O(n log n) for the sorting.

**Common wrong approach:** reporting only "75% → 78%" and shipping. The broken list is where the risk is: a change that fixes ten easy cases and breaks your most important one is a regression.
:::

:::quiz
? Why do LLM features need evals rather than only ordinary unit tests?
+ Outputs vary between runs and have many acceptable forms, so you measure pass rates over many cases
- LLMs can't be called from tests
- Unit tests are too fast
= Evals turn "seems better" into a measurement.
? What's the difference between a capability eval and a regression eval?
+ Capability evals target what the system can't yet do (low pass rate); regression evals check it still does what it did (near 100%)
- They're the same thing
- Regression evals only run once
= Passing capability cases graduate into the regression suite.
? A customer-facing agent must work every time a user asks. Which metric fits?
+ pass^k: all k trials succeed
- pass@k: at least one of k trials succeeds
- The average output length
= Reliability needs consistency across trials.
? Your pass rate went from 80% to 82% on 50 cases. What can you conclude?
+ Probably nothing yet: that difference is within the noise of a 50-case set
- The new version is definitely better
- The eval is broken
= Look at which cases flipped, and grow the set.
:::

@@@ lesson
id: llm-as-judge
title: LLM as a judge
minutes: 26
summary: Grading open-ended output with a model, rubrics and scales, pointwise, reference-based and pairwise judging, the known biases of model judges (position, length, self-preference) and how to counter them, reasoning before the verdict, checking a judge against human labels with agreement and Cohen's kappa, and judge costs.
---
Many qualities can't be checked with code: is this reply **polite**, **helpful**, **faithful to the documents**, **correctly reasoned**? Human grading is the gold standard but slow. An **LLM judge** (a model prompted to grade outputs against a rubric) scales that judgement to thousands of cases. It's one of the most useful tools in AI engineering, and one of the easiest to misuse.

### A judge prompt

```text
You are grading a bike shop's support replies.

<rubric>
Score 1 (pass) only if ALL of these hold:
- It answers the customer's actual question.
- Every factual claim is supported by the policy in <policy>.
- It's polite and under 120 words.
Otherwise score 0 (fail).
</rubric>

<policy>{{policy}}</policy>
<question>{{question}}</question>
<reply>{{reply}}</reply>

Think through each rubric point first, then give your verdict as
<score>0</score> or <score>1</score>.
```

Principles (echoing Anthropic's grading guidance):

- **Specific rubrics:** spell out what earns each score, with examples of borderline cases. "Is it good?" gives vague, unstable grades.
- **Narrow, checkable output:** pass/fail or a small scale (1–5) with defined levels, in tags or structured output, so code can parse it.
- **Reason, then score:** ask for the reasoning first, or use a thinking model, so the verdict follows from the analysis.
- **One criterion per judge** where you can: separate judges for faithfulness, tone and completeness are easier to check and debug than one judge doing everything.
- **Give it the evidence:** the source documents, the reference answer, or the conversation, whatever a careful human grader would need.

### Ways to judge

| Style | How | Good for |
|---|---|---|
| **pointwise** | score one output against the rubric | monitoring, pass rates, regression suites |
| **reference-based** | compare the output with a known good answer | factual questions with a clear answer |
| **pairwise** | which of two outputs is better? | comparing prompt or model versions |

People (and models) are more consistent at **comparing** two answers than at assigning absolute scores, which makes pairwise judging a strong way to decide between two versions.

### Known biases

Model judges have systematic biases, documented since the early "LLM-as-a-judge" studies (Zheng et al., 2023):

- **Position bias:** favouring the first (or second) answer shown. Fix: judge **both orders** and only count consistent verdicts (the second exercise).
- **Length (verbosity) bias:** preferring longer answers. Fix: say in the rubric that length isn't quality; compare answers of similar length; penalise padding explicitly.
- **Self-preference:** favouring outputs written in its own style or by its own model family. Fix: use a different model as the judge where you can, and check against humans.
- **Leniency and rubric drift:** passing everything, or interpreting a criterion loosely. Fix: concrete pass and fail examples in the prompt.

### Trust, but verify the judge

A judge is itself a model output, so **evaluate the judge**:

1. Have people label 50–200 cases with the same rubric.
2. Run the judge on the same cases.
3. Measure agreement, and read the disagreements: is the rubric unclear, or the judge wrong?

Raw agreement can flatter: if 90% of replies pass, a judge that always says "pass" agrees 90% of the time while being useless. **Cohen's kappa** corrects for agreement expected by chance:

```text
kappa = (observed agreement − chance agreement) / (1 − chance agreement)
```

Kappa is 1 for perfect agreement and 0 for chance level. As a rough guide, above about 0.6 is substantial and above 0.8 strong; how much is enough depends on the stakes. The first exercise computes it.

Re-check the judge whenever you change its prompt or model, and spot-check its verdicts in production. Judges also cost tokens: run cheap code checks first, and use a smaller model as the judge if it agrees well enough with people.

:::exercise Cohen's kappa
Write `cohen_kappa(a, b)` for two equal-length lists of labels (from two graders on the same cases):

- observed agreement `po` = the fraction of cases where the labels match;
- chance agreement `pe` = the sum, over every label used by either grader, of (fraction of `a` with that label) × (fraction of `b` with that label);
- kappa = `(po − pe) / (1 − pe)`; if `pe` is 1 (both graders used one identical label throughout), return `1.0`.

Raise `ValueError` if the lists are empty or of different lengths.
```python starter
def cohen_kappa(a, b):
    pass

human = ["pass", "pass", "fail", "pass", "fail", "pass", "pass", "fail", "pass", "pass"]
judge = ["pass", "pass", "fail", "pass", "pass", "pass", "pass", "fail", "fail", "pass"]
print(round(cohen_kappa(human, judge), 3))     # 0.524: 80% raw agreement
```
```python check
fn = need("cohen_kappa")
_r4 = lambda v: round(v, 4) if isinstance(v, float) else v
_h = ["pass", "pass", "fail", "pass", "fail", "pass", "pass", "fail", "pass", "pass"]
_j = ["pass", "pass", "fail", "pass", "pass", "pass", "pass", "fail", "fail", "pass"]
test(fn, cases=[
    ((_h, _j), 0.5238, "80% agreement"),
    ((_h, _h), 1.0, "perfect agreement"),
    ((["a", "b", "a", "b"], ["b", "a", "b", "a"]), -1.0, "complete disagreement"),
    ((["p"] * 9 + ["f"], ["p"] * 10), 0.0, "90% agreement, but no better than chance"),
    (([1, 2, 3, 1, 2, 3], [1, 2, 3, 1, 2, 1]), 0.75, "three labels"),
    ((["good", "bad", "good", "good"], ["good", "bad", "bad", "good"]), 0.5, "a small sample"),
    ((["x"] * 5, ["x"] * 5), 1.0, "one label throughout"),
], key=_r4, show="cohen_kappa({0}, {1})")
for _a, _b in [([], []), (["a"], ["a", "b"])]:
    try:
        fn(_a, _b)
    except ValueError:
        pass
    else:
        raise AssertionError(f"cohen_kappa({_a}, {_b}) should raise ValueError.")
```
```python solution
def cohen_kappa(a, b):
    if not a or len(a) != len(b):
        raise ValueError("need two non-empty lists of the same length")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(label) / n) * (b.count(label) / n) for label in set(a) | set(b))
    if pe == 1:
        return 1.0
    return (po - pe) / (1 - pe)

human = ["pass", "pass", "fail", "pass", "fail", "pass", "pass", "fail", "pass", "pass"]
judge = ["pass", "pass", "fail", "pass", "pass", "pass", "pass", "fail", "fail", "pass"]
print(round(cohen_kappa(human, judge), 3))
```
hint: Observed agreement: `sum(x == y for x, y in zip(a, b)) / n`.
hint: Chance agreement: if grader A says "pass" 70% of the time and B says "pass" 70% of the time, by chance they'd both say "pass" on 0.7 × 0.7 = 49% of cases. Add that up over every label.
hint: Loop over `set(a) | set(b)` and use `a.count(label) / n` and `b.count(label) / n`.
approach:
1. **Understand:** agreement beyond what the graders' label frequencies would produce by luck.
2. **Examples:** 9 of 10 "p" versus all "p": po = 0.9, pe = 0.9 × 1 + 0.1 × 0 = 0.9 → kappa 0.
3. **Brute force:** counting pairs with a confusion matrix: the same numbers, more code.
4. **Pattern:** **observed versus expected** (chance-corrected agreement).
5. **Plan:** validate → po → pe over all labels → the formula, guarding pe = 1.
6. **Code and test:** perfect, opposite, chance-level, three labels, a single label.
walkthrough:
**Line by line**

- `x == y` is `True` (1) or `False` (0), so the sum counts matches.
- Labels used by only one grader contribute 0 to `pe` (their count in the other list is 0), so including them is harmless.
- The `pe == 1` guard avoids dividing by zero when both graders used one label for everything (then they agree perfectly).
- Kappa can be negative: systematic disagreement is worse than chance.

**Trace** on the starter: po = 8/10 = 0.8; human passes 7/10, judge passes 7/10 → pe = 0.7 × 0.7 + 0.3 × 0.3 = 0.58 → kappa = 0.22 / 0.42 ≈ 0.524.

**Complexity:** O(n × labels) with `count`; O(n) with a `Counter`.

**Common wrong approach:** quoting raw agreement alone. On a set where 90% of cases pass, a judge that always says "pass" scores 90% agreement and kappa 0.
:::

:::exercise A position-swapped pairwise judge
Write `pairwise_verdict(judge, question, answer_a, answer_b)`. `judge(question, first, second)` returns `"first"`, `"second"` or `"tie"`. Call it **twice**: once with `(answer_a, answer_b)` and once with `(answer_b, answer_a)`. Return:

- `"A"` if answer A wins in **both** orders (it's `"first"` in the first call and `"second"` in the second);
- `"B"` if answer B wins in both orders;
- `"tie"` otherwise (including inconsistent verdicts and ties).
```python starter
def pairwise_verdict(judge, question, answer_a, answer_b):
    pass

def first_bias_judge(question, first, second):
    return "first"                                  # always prefers whatever it sees first

def length_judge(question, first, second):
    return "first" if len(first) > len(second) else "second" if len(second) > len(first) else "tie"

print(pairwise_verdict(first_bias_judge, "Q", "short", "a much longer answer"))   # tie
print(pairwise_verdict(length_judge, "Q", "short", "a much longer answer"))       # B
```
```python check
fn = need("pairwise_verdict")
_first = lambda q, f, s: "first"
_second = lambda q, f, s: "second"
_tie = lambda q, f, s: "tie"
_longer = lambda q, f, s: "first" if len(f) > len(s) else "second" if len(s) > len(f) else "tie"
_likes_x = lambda q, f, s: "first" if "x" in f else "second" if "x" in s else "tie"
_half = lambda q, f, s: "first" if "x" in f else "tie"
test(fn, cases=[
    ((_first, "Q", "a", "bb"), "tie", "always-first judge: position bias cancels out"),
    ((_second, "Q", "a", "bb"), "tie", "always-second judge"),
    ((_longer, "Q", "short", "a much longer answer"), "B", "consistent preference for B"),
    ((_longer, "Q", "a much longer answer", "short"), "A", "consistent preference for A"),
    ((_tie, "Q", "a", "b"), "tie", "the judge sees no difference"),
    ((_likes_x, "Q", "has x", "nope"), "A", "content-based preference"),
    ((_half, "Q", "nope", "has x"), "tie", "a win in only one order"),
], show="pairwise_verdict(judge, {1}, {2}, {3})")
_seen = []
def _rec(q, f, s):
    _seen.append((q, f, s))
    return "tie"
fn(_rec, "Which is better?", "AAA", "BBB")
assert _seen == [("Which is better?", "AAA", "BBB"), ("Which is better?", "BBB", "AAA")], \
    f"Call the judge with (question, A, B) and then (question, B, A); it was called with {_seen}."
```
```python solution
def pairwise_verdict(judge, question, answer_a, answer_b):
    forward = judge(question, answer_a, answer_b)     # A shown first
    backward = judge(question, answer_b, answer_a)    # B shown first
    if forward == "first" and backward == "second":
        return "A"
    if forward == "second" and backward == "first":
        return "B"
    return "tie"                                      # inconsistent or tied: no reliable winner

def first_bias_judge(question, first, second):
    return "first"

def length_judge(question, first, second):
    return "first" if len(first) > len(second) else "second" if len(second) > len(first) else "tie"

print(pairwise_verdict(first_bias_judge, "Q", "short", "a much longer answer"))
print(pairwise_verdict(length_judge, "Q", "short", "a much longer answer"))
```
hint: Make two calls: `judge(question, answer_a, answer_b)` and `judge(question, answer_b, answer_a)`.
hint: In the second call A is shown second, so "A wins" there means the verdict is `"second"`.
hint: Only two combinations give a winner: ("first", "second") → A and ("second", "first") → B. Everything else is a tie.
approach:
1. **Understand:** a verdict counts only if it survives swapping the order.
2. **Examples:** a judge that always says "first" picks A, then B: inconsistent → tie.
3. **Brute force:** one call: exposed to position bias.
4. **Pattern:** **counterbalancing**: run both orders, keep agreement.
5. **Plan:** two calls → map to A, B or tie.
6. **Code and test:** always-first, always-second, consistent preferences, half wins.
walkthrough:
**Line by line**

- Swapping positions turns position bias into a **disagreement**, which the function reports as a tie instead of a fake win.
- The mapping is explicit, so it's easy to audit.
- A tie also covers the case where the judge itself says "tie" in either order.
- Note the length judge in the starter: it's perfectly consistent, but it's measuring length, not quality. Swapping fixes position bias, not every bias.

**Trace:** the always-first judge returns ("first", "first"); A wins the first call, B wins the second → "tie".

**Complexity:** two judge calls.

**Common wrong approach:** judging in one fixed order and reporting a win rate, which can mostly measure the judge's position preference. Over many comparisons, also randomise which version appears as "A".
:::

:::quiz
? Why should a judge reason before giving its score?
+ The verdict then follows from the analysis, which makes grading more accurate on complex criteria
- It makes the judge cheaper
- Scores must always come last in JSON
= Ask for reasoning first, or use a thinking model.
? A judge agrees with humans 90% of the time, but 90% of cases are passes. What does Cohen's kappa tell you?
+ Whether the agreement is better than a grader that just says "pass" by habit
- Nothing: 90% is always good
- The judge's cost
= Kappa corrects for chance agreement.
? How do you counter position bias in pairwise judging?
+ Judge both orders and count only consistent verdicts
- Always put the better answer first
- Use a longer rubric
= Swapping turns bias into visible inconsistency.
? Which judge setup is easiest to check and debug?
+ One judge per criterion with a specific rubric and a pass/fail output
- One judge scoring "overall quality" from 1 to 100
- A judge with no rubric
= Narrow, specific judgements are more reliable.
:::

@@@ lesson
id: hallucinations
title: Catching hallucinations
minutes: 24
summary: What hallucinations are (factual errors, unfaithful answers, invented citations, packages and APIs), why models produce them, prevention (grounding, permission to say "I don't know", quotes first, tools for facts, verification passes), detection (checking numbers and claims against sources, consistency across samples, model judges), and measuring hallucination rates.
---
A **hallucination** is fluent, confident output that isn't true or isn't supported. It's the failure users notice most and trust least, and in a product it can cost money, reputation, or worse.

### Kinds of hallucination

| Kind | Example |
|---|---|
| **factual** (wrong about the world) | "The Tour de France starts in July every year since 1890" (it began in 1903) |
| **unfaithful** (contradicts or goes beyond the given sources) | the policy says 30 days; the answer says 60 |
| **fabricated references** | a citation, URL or court case that doesn't exist |
| **invented code** | a function, parameter or package that doesn't exist; attackers even register commonly hallucinated package names ("slopsquatting") |
| **false actions** | an agent saying it sent the email when the tool call failed |

### Why models do it

A language model generates the most plausible continuation (Lesson 1); plausible and true usually coincide, but not always: rare facts, precise numbers, recent events, private information and long chains of reasoning are where they part. OpenAI researchers argued in 2025 that training and evaluation also **reward guessing**: like a multiple-choice exam with no penalty for wrong answers, a model scores better by guessing than by saying "I don't know". Newer models abstain more often and hallucinate less, but none is immune.

### Prevention

Most of this course is hallucination prevention:

- **Ground answers in sources** (RAG, Part 4) and instruct the model to use **only** them.
- **Allow "I don't know"** explicitly, and test that it's used (Lesson 22).
- **Quotes first:** have the model extract relevant quotes, then answer from them (Lesson 13); use **citations** so claims are checkable (Lesson 17).
- **Use tools for facts:** a calculator for arithmetic, a database for prices, search for recent events (Part 5). Don't ask the model to remember what it can look up.
- **Narrow the task:** extraction into a schema hallucinates less than open-ended writing.
- **Check actions against outcomes:** confirm in code that the tool call succeeded before the agent reports success.
- **Verification passes:** draft an answer, then check it, for example with **chain-of-verification** (plan questions that would verify each claim, answer them independently, then revise).

### Detection

Some checks are cheap and automatic:

- **Numbers and names against the sources:** every figure in an answer should appear in the evidence (the first exercise).
- **Claims against a knowledge base:** extract claims as (subject, attribute, value) and look them up (the second exercise).
- **Citations:** check they exist and point at text that supports the sentence (Lesson 17).
- **Consistency:** ask the same question several times; facts the model really knows come out the same, while invented details vary between samples. Disagreement is a useful uncertainty signal (and voting, Lesson 14, uses the agreement).
- **Model judges** for faithfulness, with the sources in the prompt (Lesson 29).

```python
answer = "Puncture repairs cost £12 and are done within 48 hours. We stock 40 tyre sizes."
sources = "Puncture repairs cost £12 and are usually done the same day."

answer_words = set(answer.lower().replace(".", "").split())
source_words = set(sources.lower().replace(".", "").split())
print("in the answer but not the source:", sorted(answer_words - source_words))
```

Even this crude word difference points at the invented parts ("48 hours", "40 tyre sizes").

### Measure it

Treat hallucination as a **rate** you track, not an anecdote: run your eval set with a faithfulness grader, count unsupported claims per answer and refusal accuracy on unanswerable questions, and watch the numbers when you change prompts, retrieval or models. Show users the sources, and make it easy to report a wrong answer.

:::exercise Find unsupported numbers
Write `unsupported_numbers(answer, sources)` returning the numbers in `answer` that don't appear in any of the `sources` (a list of strings):

- A number is a match of `\d[\d,]*(?:\.\d+)?` with any trailing commas removed (so `"30,"` at the end of a clause is `"30"`).
- Compare by **value**: remove the thousands commas and convert to `float`, so `1,200` matches `1200` and `12` matches `12.00`.
- Return the unsupported numbers **as written** (after removing trailing commas), in order of first appearance, each value once.
```python starter
import re

def unsupported_numbers(answer, sources):
    pass

sources = ["Puncture repairs cost £12.00 and are usually done the same day.",
           "We have repaired 1200 bikes since 2015. Returns within 30 days."]
print(unsupported_numbers("Repairs cost £12 and take 2 days; we have fixed 1,200 bikes since 2019.", sources))
# ['2', '2019']
```
```python check
fn = need("unsupported_numbers")
_s = ["Puncture repairs cost £12.00 and are usually done the same day.",
      "We have repaired 1200 bikes since 2015. Returns within 30 days."]
test(fn, cases=[
    (("Repairs cost £12 and take 2 days; we have fixed 1,200 bikes since 2019.", _s), ["2", "2019"], "two invented numbers"),
    (("Returns are accepted within 30 days.", _s), [], "fully supported"),
    (("Returns within 30 or 60 days, 60 for members.", _s), ["60"], "each value once"),
    (("No numbers here.", _s), [], "no numbers"),
    (("Prices: 3.5, 3.50, 1,000,000.", _s), ["3.5", "1,000,000"], "decimals and thousands"),
    (("In 2015, 12, 30,", _s), [], "trailing commas"),
    (("We fixed 1200 bikes.", []), ["1200"], "no sources"),
], show="unsupported_numbers({0}, sources)")
```
```python solution
import re

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")

def numbers_in(text):
    return [match.rstrip(",") for match in NUMBER.findall(text)]

def value(number):
    return float(number.replace(",", ""))

def unsupported_numbers(answer, sources):
    known = {value(n) for source in sources for n in numbers_in(source)}
    unsupported, seen = [], set()
    for number in numbers_in(answer):
        v = value(number)
        if v not in known and v not in seen:
            seen.add(v)
            unsupported.append(number)
    return unsupported

sources = ["Puncture repairs cost £12.00 and are usually done the same day.",
           "We have repaired 1200 bikes since 2015. Returns within 30 days."]
print(unsupported_numbers("Repairs cost £12 and take 2 days; we have fixed 1,200 bikes since 2019.", sources))
```
hint: Write a helper that finds the numbers in a text (`re.findall` with the pattern, then `.rstrip(",")` on each).
hint: Convert to comparable values with `float(n.replace(",", ""))`, and build a set of every value in the sources.
hint: Walk the answer's numbers in order; keep one if its value isn't in the sources' set and you haven't already reported that value.
approach:
1. **Understand:** extract, normalise, set difference, keep order and distinctness.
2. **Examples:** `£12` versus `£12.00` → both 12.0 → supported; `1,200` versus `1200` → supported.
3. **Brute force:** compare the raw strings: "1,200" ≠ "1200" gives false alarms.
4. **Pattern:** **normalise, then set membership**.
5. **Plan:** helpers → source value set → filter the answer's numbers in order.
6. **Code and test:** decimals, thousands separators, trailing commas, repeats, no sources.
walkthrough:
**Line by line**

- The regex starts with a digit, so a trailing comma or a lone comma can't start a number; `rstrip(",")` removes the clause comma the pattern swallowed.
- Converting to `float` makes `3.5` and `3.50` the same value, and `12` the same as `12.00`.
- The `seen` set reports each value once, even if the answer repeats it.
- Numbers are returned as written, which is what you'd show a reviewer.

**Trace:** answer numbers 12, 2, 1,200, 2019; source values {12, 1200, 2015, 30} → 2 and 2019 are unsupported.

**Complexity:** O(len(answer) + total source length).

**Common wrong approach:** treating every flagged number as a hallucination. "2 days" might be a legitimate calculation or come from general knowledge; the check finds candidates for review, it doesn't deliver verdicts. (It also misses numbers written as words, like "thirty".)
:::

:::exercise Verify claims against facts
Suppose another step has extracted the answer's factual claims as dicts `{"subject": …, "attribute": …, "value": …}`. Write `verify_claims(claims, facts)`, where `facts` maps `(subject, attribute)` pairs to known values. Return a list with one verdict per claim, in order:

- `"supported"` if the pair is in `facts` and the values match,
- `"contradicted"` if the pair is in `facts` but the values differ,
- `"unverifiable"` if the pair isn't in `facts`.

Compare subjects, attributes and values after `str(x).strip().lower()`.
```python starter
def verify_claims(claims, facts):
    pass

facts = {("puncture repair", "price"): "£12", ("returns", "window"): "30 days",
         ("frames", "warranty"): "lifetime"}
claims = [{"subject": "Puncture repair", "attribute": "price", "value": "£12"},
          {"subject": "returns", "attribute": "window", "value": "60 days"},
          {"subject": "helmets", "attribute": "colour", "value": "red"}]
print(verify_claims(claims, facts))   # ['supported', 'contradicted', 'unverifiable']
```
```python check
fn = need("verify_claims")
_f = {("puncture repair", "price"): "£12", ("returns", "window"): "30 days", ("Frames", "Warranty"): "Lifetime", ("shop", "opens"): 9}
_c = lambda s, a, v: {"subject": s, "attribute": a, "value": v}
test(fn, cases=[
    (([_c("Puncture repair", "price", "£12"), _c("returns", "window", "60 days"), _c("helmets", "colour", "red")], _f),
     ["supported", "contradicted", "unverifiable"], "one of each"),
    (([_c(" FRAMES ", "warranty", "lifetime ")], _f), ["supported"], "case and spaces are ignored on both sides"),
    (([_c("shop", "opens", "9")], _f), ["supported"], "numbers compare as text"),
    (([_c("shop", "opens", 10)], _f), ["contradicted"], "a different number"),
    (([], _f), [], "no claims"),
    (([_c("returns", "window", "30 days")], {}), ["unverifiable"], "no facts"),
], show="verify_claims(claims, facts)")
```
```python solution
def norm(x):
    return str(x).strip().lower()

def verify_claims(claims, facts):
    known = {(norm(s), norm(a)): norm(v) for (s, a), v in facts.items()}
    verdicts = []
    for claim in claims:
        key = (norm(claim["subject"]), norm(claim["attribute"]))
        if key not in known:
            verdicts.append("unverifiable")
        elif known[key] == norm(claim["value"]):
            verdicts.append("supported")
        else:
            verdicts.append("contradicted")
    return verdicts

facts = {("puncture repair", "price"): "£12", ("returns", "window"): "30 days",
         ("frames", "warranty"): "lifetime"}
claims = [{"subject": "Puncture repair", "attribute": "price", "value": "£12"},
          {"subject": "returns", "attribute": "window", "value": "60 days"},
          {"subject": "helmets", "attribute": "colour", "value": "red"}]
print(verify_claims(claims, facts))
```
hint: Normalise the **facts** once, building a new dict whose keys and values are normalised, so lookups are simple.
hint: For each claim, build the normalised `(subject, attribute)` key; then it's a three-way choice.
hint: `norm = lambda x: str(x).strip().lower()`; `str` lets numbers compare with text.
approach:
1. **Understand:** a lookup with three outcomes; normalisation on both sides.
2. **Examples:** the fact's key is `("Frames", "Warranty")`, the claim says `" FRAMES "`: both normalise to `("frames", "warranty")`.
3. **Brute force:** scanning every fact for every claim: O(claims × facts).
4. **Pattern:** **normalise into a lookup table**, then classify.
5. **Plan:** normalised facts dict → per claim: key → missing / equal / different.
6. **Code and test:** case and spacing, numbers, empty inputs.
walkthrough:
**Line by line**

- Normalising the facts once (not on every lookup) keeps each claim check O(1).
- `str(x)` lets the number 9 match the text "9".
- "Unverifiable" is not "false": it means your knowledge base can't say, which is common, and worth tracking separately.
- Contradictions are the most serious result: the answer disagrees with something you know.

**Trace:** the price matches (supported); the returns window differs (contradicted); there's no fact about helmet colours (unverifiable).

**Complexity:** O(facts + claims).

**Common wrong approach:** counting "unverifiable" as hallucination, or as fine. Neither is right: report the three counts separately, and route unverifiable claims to a model judge or a human. (Extracting claims reliably is itself a model task, so check that step too.)
:::

:::quiz
? Which is an unfaithful hallucination?
+ The policy says returns within 30 days, but the answer says 60
- The model refuses an off-topic request
- The answer is shorter than expected
= Faithfulness means agreeing with the given sources.
? Why can evaluations encourage models to guess?
+ When wrong answers cost no more than "I don't know", guessing scores better on average
- Evaluations always reward long answers
- Guessing is faster to compute
= Reward abstention where appropriate.
? An agent reports "email sent" but the tool call returned an error. What prevents this?
+ Checking tool outcomes in code before the agent reports success
- A longer system prompt
- Using a smaller model
= Verify outcomes, not claims.
? Why does disagreement across several samples hint at a hallucination?
+ Facts the model knows tend to come out the same each time, while invented details vary
- Disagreement means the API is broken
- Samples always disagree
= Consistency is a useful uncertainty signal.
:::

@@@ lesson
id: observability
title: Tracing and monitoring
minutes: 24
summary: Why LLM applications need observability, traces and spans, what to record for model calls, retrieval and tools, OpenTelemetry's generative-AI conventions, observability tools, privacy and retention, user feedback, online evaluation of production traffic, dashboards and alerts, and turning production traces into eval cases.
---
Once real users arrive, things go wrong that no eval predicted: a question type you never tested, a document that confuses retrieval, a tool that times out at peak hours, a cost spike from one runaway agent. **Observability** means recording enough about every request to answer "what happened, and why?" afterwards.

### Traces and spans

A **trace** records one request end to end. It's made of **spans**: timed steps with a name, a parent and attributes. A RAG chat request might look like this:

![A waterfall chart of one request lasting about 3.2 seconds. The root span "chat request" spans the whole bar. Beneath it: "rewrite query" (an LLM call, 0.4 s), "retrieve" (0.3 s) with children "bm25 search" and "vector search" running in parallel, "rerank" (0.18 s), and "generate answer" (an LLM call, 2.2 s, the longest). Each LLM span lists its model and token counts](figures/trace-waterfall.svg)

The waterfall shows at a glance where the time went (here, mostly generating the answer) and which step failed when something breaks.

### What to record

| Span | Record |
|---|---|
| every request | user or session ID (pseudonymous), prompt **version**, app version, total latency, outcome |
| model calls | model, parameters (effort, max tokens), input and output tokens (including cache reads and writes), cost, stop reason, time to first token, request ID |
| retrieval | the query, the IDs and scores of retrieved chunks, the index version |
| tool calls | tool name, arguments, result size, errors, approval decisions |
| feedback | thumbs up or down, corrections, whether the user rephrased |

**OpenTelemetry**, the open standard for traces, has semantic conventions for generative AI (attributes such as `gen_ai.request.model` and `gen_ai.usage.input_tokens`), so traces can go to any compatible backend. Dedicated LLM observability tools (Langfuse, LangSmith, Arize Phoenix, Braintrust, Helicone, Weights & Biases Weave and others) add prompt and response viewers, cost tracking, evaluation and dataset features on top.

A tiny tracer shows the idea:

```python
import time
from contextlib import contextmanager

spans, stack = [], []

@contextmanager
def span(name, **attributes):
    record = {"id": len(spans) + 1, "parent": stack[-1] if stack else None, "name": name, **attributes}
    spans.append(record)
    stack.append(record["id"])
    start = time.perf_counter()
    try:
        yield record
    finally:
        record["ms"] = round((time.perf_counter() - start) * 1000, 1)
        stack.pop()

with span("chat request"):
    with span("retrieve", k=20):
        sum(range(200_000))                     # stand-in for real work
    with span("generate", model="claude-sonnet-5-5") as s:
        sum(range(400_000))
        s["output_tokens"] = 180

for record in spans:
    extra = {k: v for k, v in record.items() if k not in ("id", "parent", "name", "ms")}
    print(f"span {record['id']} (parent {record['parent']}): {record['name']} {extra}")
```

### Privacy and retention

Prompts and responses often contain personal data. Decide deliberately:

- **What to store:** full text for debugging, or only metadata (tokens, latency, IDs) for most requests and full text for a sample.
- **Redaction** of personal data before logging (Lesson 16).
- **Retention:** how long logs live, who can read them, and how a user's data is deleted on request.

### Online evaluation and alerts

- Run **code checks and model judges on a sample of live traffic** (faithfulness, tone, refusals), not just on your eval set.
- **Dashboards:** request volume, latency percentiles (Lesson 32), error and refusal rates, cost per day and per user, cache hit rate, feedback rates.
- **Alerts** on sudden changes: error spikes, p95 latency, cost per hour, a drop in thumbs-up rate.
- **Close the loop:** turn interesting production failures into eval cases (Lesson 28). Traces are the best source of realistic test data you'll ever have.

:::exercise Draw a trace tree
Write `trace_tree(spans)` returning a list of text lines that show the spans as an indented tree. Each span is a dict with `"id"`, `"parent"` (another span's id, or `None`), `"name"` and `"ms"`. Each line is two spaces per level of depth followed by `f"{name} ({ms} ms)"`. Roots (parent `None`, or a parent that isn't in the list) come first in input order; each span's children follow it, in input order.
```python starter
def trace_tree(spans):
    pass

spans = [{"id": 1, "parent": None, "name": "chat request", "ms": 3200},
         {"id": 2, "parent": 1, "name": "retrieve", "ms": 300},
         {"id": 3, "parent": 2, "name": "bm25 search", "ms": 120},
         {"id": 4, "parent": 2, "name": "vector search", "ms": 180},
         {"id": 5, "parent": 1, "name": "generate answer", "ms": 2200}]
print("\n".join(trace_tree(spans)))
```
```python check
fn = need("trace_tree")
_s = [{"id": 1, "parent": None, "name": "chat request", "ms": 3200},
      {"id": 2, "parent": 1, "name": "retrieve", "ms": 300},
      {"id": 3, "parent": 2, "name": "bm25 search", "ms": 120},
      {"id": 4, "parent": 2, "name": "vector search", "ms": 180},
      {"id": 5, "parent": 1, "name": "generate answer", "ms": 2200}]
test(fn, cases=[
    ((_s,), ["chat request (3200 ms)", "  retrieve (300 ms)", "    bm25 search (120 ms)", "    vector search (180 ms)", "  generate answer (2200 ms)"], "a nested trace"),
    (([],), [], "no spans"),
    (([{"id": "b", "parent": "a", "name": "child", "ms": 5}, {"id": "a", "parent": None, "name": "root", "ms": 9}],),
     ["root (9 ms)", "  child (5 ms)"], "a child listed before its parent"),
    (([{"id": 1, "parent": None, "name": "job A", "ms": 1}, {"id": 2, "parent": None, "name": "job B", "ms": 2},
       {"id": 3, "parent": 1, "name": "step", "ms": 0.5}],), ["job A (1 ms)", "  step (0.5 ms)", "job B (2 ms)"], "two roots"),
    (([{"id": 7, "parent": 99, "name": "orphan", "ms": 3}],), ["orphan (3 ms)"], "a missing parent makes a root"),
], show="trace_tree(spans)")
```
```python solution
def trace_tree(spans):
    ids = {s["id"] for s in spans}
    children = {}
    roots = []
    for s in spans:
        if s["parent"] is None or s["parent"] not in ids:
            roots.append(s)
        else:
            children.setdefault(s["parent"], []).append(s)

    lines = []
    def walk(s, depth):
        lines.append("  " * depth + f"{s['name']} ({s['ms']} ms)")
        for child in children.get(s["id"], []):
            walk(child, depth + 1)
    for root in roots:
        walk(root, 0)
    return lines

spans = [{"id": 1, "parent": None, "name": "chat request", "ms": 3200},
         {"id": 2, "parent": 1, "name": "retrieve", "ms": 300},
         {"id": 3, "parent": 2, "name": "bm25 search", "ms": 120},
         {"id": 4, "parent": 2, "name": "vector search", "ms": 180},
         {"id": 5, "parent": 1, "name": "generate answer", "ms": 2200}]
print("\n".join(trace_tree(spans)))
```
hint: First group spans by parent: a dict from parent id to the list of its children (in input order). Spans with no valid parent are roots.
hint: Then walk the tree depth-first from each root, adding a line for each span before its children.
hint: A recursive helper `walk(span, depth)` appends `"  " * depth + f"{name} ({ms} ms)"` and calls itself for each child with `depth + 1`.
approach:
1. **Understand:** spans form a tree via parent ids; print it depth-first with indentation.
2. **Examples:** a child listed before its parent still appears under it.
3. **Brute force:** for each span, scan the whole list for its children: O(n²).
4. **Pattern:** **adjacency list + depth-first traversal** (a pre-order walk).
5. **Plan:** ids → children map and roots → recursive walk → lines.
6. **Code and test:** nesting, out-of-order input, several roots, orphans, empty input.
walkthrough:
**Line by line**

- Building the `children` dict first means the input order of parents and children doesn't matter.
- `s["parent"] not in ids` turns an orphan (its parent span was lost or sampled out) into a root rather than dropping it.
- The pre-order walk prints a span before its children, which is how trace viewers show them.
- Depth controls the indentation; two spaces per level.

**Trace:** chat request (depth 0) → retrieve (1) → bm25 search (2), vector search (2) → generate answer (1).

**Complexity:** O(n).

**Common wrong approach:** assuming parents always appear before children. Spans are usually recorded when they **finish**, so children often arrive first.
:::

:::exercise Summarise a trace
Write `trace_summary(spans)`. Each span has `"name"`, `"kind"` (such as `"llm"`, `"tool"` or `"retrieval"`) and `"ms"`, and may have `"input_tokens"`, `"output_tokens"`, `"cost"` and `"error"` (a bool). Return:

```text
{"llm_calls": number of "llm" spans, "tool_calls": number of "tool" spans,
 "tokens": total input + output tokens, "cost": total cost rounded to 6 decimals,
 "errors": number of spans with "error" True, "slowest": name of the span with the largest "ms"}
```

Missing numbers count as 0; `"slowest"` is the **first** such span on a tie, or `None` for no spans.
```python starter
def trace_summary(spans):
    pass

spans = [{"name": "rewrite query", "kind": "llm", "ms": 400, "input_tokens": 300, "output_tokens": 40, "cost": 0.0010},
         {"name": "retrieve", "kind": "retrieval", "ms": 300},
         {"name": "get_stock", "kind": "tool", "ms": 900, "error": True},
         {"name": "generate answer", "kind": "llm", "ms": 2200, "input_tokens": 5200, "output_tokens": 350, "cost": 0.0139}]
print(trace_summary(spans))
```
```python check
fn = need("trace_summary")
_s = [{"name": "rewrite query", "kind": "llm", "ms": 400, "input_tokens": 300, "output_tokens": 40, "cost": 0.0010},
      {"name": "retrieve", "kind": "retrieval", "ms": 300},
      {"name": "get_stock", "kind": "tool", "ms": 900, "error": True},
      {"name": "generate answer", "kind": "llm", "ms": 2200, "input_tokens": 5200, "output_tokens": 350, "cost": 0.0139}]
test(fn, cases=[
    ((_s,), {"llm_calls": 2, "tool_calls": 1, "tokens": 5890, "cost": 0.0149, "errors": 1, "slowest": "generate answer"}, "a RAG request"),
    (([],), {"llm_calls": 0, "tool_calls": 0, "tokens": 0, "cost": 0.0, "errors": 0, "slowest": None}, "no spans"),
    (([{"name": "a", "kind": "tool", "ms": 5}, {"name": "b", "kind": "tool", "ms": 5, "error": False}],),
     {"llm_calls": 0, "tool_calls": 2, "tokens": 0, "cost": 0.0, "errors": 0, "slowest": "a"}, "a tie goes to the first"),
    (([{"name": "x", "kind": "llm", "ms": 1, "output_tokens": 10, "cost": 0.1}, {"name": "y", "kind": "llm", "ms": 2, "input_tokens": 5, "cost": 0.2}],),
     {"llm_calls": 2, "tool_calls": 0, "tokens": 15, "cost": 0.3, "errors": 0, "slowest": "y"}, "partial token counts; cost rounding"),
], show="trace_summary(spans)")
```
```python solution
def trace_summary(spans):
    slowest = None
    for s in spans:
        if slowest is None or s["ms"] > slowest["ms"]:
            slowest = s                                   # strict > keeps the first on a tie
    return {
        "llm_calls": sum(1 for s in spans if s["kind"] == "llm"),
        "tool_calls": sum(1 for s in spans if s["kind"] == "tool"),
        "tokens": sum(s.get("input_tokens", 0) + s.get("output_tokens", 0) for s in spans),
        "cost": round(sum(s.get("cost", 0) for s in spans), 6),
        "errors": sum(1 for s in spans if s.get("error")),
        "slowest": slowest["name"] if slowest else None,
    }

spans = [{"name": "rewrite query", "kind": "llm", "ms": 400, "input_tokens": 300, "output_tokens": 40, "cost": 0.0010},
         {"name": "retrieve", "kind": "retrieval", "ms": 300},
         {"name": "get_stock", "kind": "tool", "ms": 900, "error": True},
         {"name": "generate answer", "kind": "llm", "ms": 2200, "input_tokens": 5200, "output_tokens": 350, "cost": 0.0139}]
print(trace_summary(spans))
```
hint: `s.get("input_tokens", 0)` treats a missing field as 0; the same works for cost, and `s.get("error")` is falsy when missing.
hint: Counting with a condition: `sum(1 for s in spans if s["kind"] == "llm")`.
hint: For the slowest span, loop and replace your current best only when `s["ms"] > best["ms"]` (strictly greater keeps the first on ties). `max(spans, key=...)` also returns the first maximum.
approach:
1. **Understand:** a handful of aggregates over a list of dicts with optional fields.
2. **Examples:** tokens = 300 + 40 + 5,200 + 350 = 5,890; cost = 0.0010 + 0.0139 = 0.0149.
3. **Brute force:** this is already one pass per aggregate.
4. **Pattern:** **aggregate with defaults**.
5. **Plan:** slowest → counts → sums with `.get` → round the cost.
6. **Code and test:** empty input, ties, missing fields, float rounding.
walkthrough:
**Line by line**

- `.get(field, 0)` handles spans that don't carry tokens or cost (retrieval and tools usually don't).
- Rounding the summed cost hides floating-point noise such as 0.30000000000000004.
- `s.get("error")` is `None` for spans without the field, which counts as not an error.
- The slowest span tells you where to look first when a request is slow.

**Trace:** two LLM spans, one tool span (which errored), 5,890 tokens, $0.0149, slowest "generate answer" at 2,200 ms.

**Complexity:** O(n).

**Common wrong approach:** summing only the root span's latency and the final model call's tokens. Multi-step requests spend tokens and time in many places; summaries like this per request, aggregated across requests, show where the money and time really go.
:::

:::quiz
? What is a span in a trace?
+ One timed step of a request, such as a model call or a tool call, with a parent and attributes
- A whole day of logs
- A user's session
= A trace is a tree of spans.
? Why record the prompt version with every request?
+ To trace a bad answer back to the exact prompt that produced it, and compare versions
- The API requires it
- It reduces cost
= Prompts are code; log which version ran.
? What should you do with interesting production failures?
+ Turn them into eval cases so they're tested from now on
- Delete them
- Ignore them unless a user complains twice
= Production traces are the best test data.
? Why decide what text to store in traces?
+ Prompts and responses may contain personal data, which needs redaction, retention limits and access control
- Text is too large to store
- Tracing tools can't store text
= Observability and privacy must be designed together.
:::

@@@ lesson
id: cost-and-latency
title: Cost and latency in production
minutes: 24
summary: Where the time goes in an LLM request (queueing, input processing, time to first token, output generation, tools), why output length dominates, percentiles and tail latency, the levers for speed and cost, response caching, rate limits and capacity planning, timeouts and fallbacks, and projecting monthly cost.
---
A demo can take ten seconds and cost a few cents per question. A product with thousands of users can't. In production, cost and latency are features: they decide whether people wait for the answer, and whether the business can afford to give it.

### Where the time goes

![A horizontal timeline of one request: a short network and queueing segment, then input processing up to the first token (time to first token, about 0.6 s), then a long segment generating 400 output tokens at about 80 tokens per second (5 s). With streaming, the user starts reading at the first token; without it, they wait for the end](figures/latency-anatomy.svg)

```text
total latency ≈ time to first token (TTFT) + output tokens ÷ output speed (+ tool calls and retries)
```

- **TTFT** grows with input length (longer prompts take longer to process), queueing at busy times, and thinking before the first visible token. Prompt caching cuts it for repeated prefixes.
- **Output generation** usually dominates: tokens come out one at a time, so 1,000 output tokens take many times longer than 100. **Shorter outputs are the most effective speed-up.**
- Agents multiply everything by the number of turns, plus the time tools take.

```python
def latency(ttft, output_tokens, tokens_per_second):
    return ttft + output_tokens / tokens_per_second

for tokens in (100, 400, 1500):
    print(f"{tokens:>5} output tokens: {latency(0.6, tokens, 80):.1f} s")
```

(These speeds are illustrative; measure your own model, region and prompt sizes.)

### Measure percentiles, not averages

Latency varies from request to request, and a few slow ones hurt. Report **percentiles**: p50 (the median: a typical request), **p95** and **p99** (the slow tail that some users hit every day). An average of 2 s can hide a p99 of 15 s. The first exercise computes them.

### Levers

| Lever | Speed | Cost | Trade-off |
|---|---|---|---|
| shorter outputs (instructions, `max_tokens`, structured output) | ✅✅ | ✅✅ | may lose detail |
| smaller, faster model for easy requests (routing) | ✅✅ | ✅✅ | needs evals to prove quality holds |
| lower effort | ✅ | ✅ | less reasoning on hard tasks |
| prompt caching (Lesson 11) | ✅ (TTFT) | ✅✅ on repeated input | prefix must stay identical |
| streaming | ✅ perceived | — | none for the user; more code |
| parallel calls (independent steps at once) | ✅ | — | more concurrent load |
| fewer round trips (batch tool calls, fewer agent turns) | ✅ | ✅ | design work |
| response caching (reuse answers to repeated questions) | ✅✅ on a hit | ✅✅ on a hit | stale or mismatched answers |
| Batch API (Lesson 11) | ❌ (hours) | ✅ 50% | offline only |

**Response caching** stores whole answers. An **exact** cache (after normalising case and spacing) is safe and simple; a **semantic** cache (reusing the answer to a question with a similar embedding) hits more often but can return the answer to a subtly different question. Expire entries when the underlying data changes (the second exercise).

### Rate limits and capacity

Providers limit requests and tokens per minute per organisation and model (on the Claude API, input and output tokens are limited separately). Plan for peak, not average:

- estimate peak requests per minute × tokens per request, and request higher limits ahead of launch;
- **queue** non-urgent work and smooth bursts; use the Batch API for bulk jobs;
- handle 429s with backoff (Lesson 8), and set **timeouts** so a stuck call doesn't hold a user forever;
- have a **fallback**: another model, another region or provider, or a graceful non-AI response.

### Projecting cost

```python
requests_per_day = 20_000
input_tokens, output_tokens = 3_000, 350           # per request, measured from logs
cached_share = 0.8                                 # share of input read from the prompt cache
price_in, price_out = 2.0, 10.0                    # $ per million tokens (Sonnet 5.5 list price)

input_cost = input_tokens * ((1 - cached_share) * price_in + cached_share * price_in * 0.1)
per_request = (input_cost + output_tokens * price_out) / 1_000_000
print(f"${per_request:.4f} per request, ${per_request * requests_per_day * 30:,.0f} per month")
```

Recompute this from **real logged usage** (Lesson 31) after launch; estimates made before launch are usually wrong in both directions.

:::exercise Latency percentiles
Write `percentiles(values, ps=(50, 95, 99))` returning a dict like `{"p50": …, "p95": …, "p99": …}` using the **nearest-rank** method: sort the values; the p-th percentile is the value at rank `ceil(p / 100 × n)` (counting from 1, and at least rank 1). Raise `ValueError` for an empty list.
```python starter
import math

def percentiles(values, ps=(50, 95, 99)):
    pass

latencies = [1.2, 0.9, 1.4, 1.1, 8.5, 1.0, 1.3, 0.8, 1.6, 12.0]
print(percentiles(latencies))    # {'p50': 1.2, 'p95': 12.0, 'p99': 12.0}
```
```python check
fn = need("percentiles")
_l = [1.2, 0.9, 1.4, 1.1, 8.5, 1.0, 1.3, 0.8, 1.6, 12.0]
test(fn, cases=[
    ((_l,), {"p50": 1.2, "p95": 12.0, "p99": 12.0}, "ten latencies"),
    ((list(range(1, 101)),), {"p50": 50, "p95": 95, "p99": 99}, "1 to 100"),
    (([5],), {"p50": 5, "p95": 5, "p99": 5}, "one value"),
    ((_l, (0, 10, 90, 100)), {"p0": 0.8, "p10": 0.8, "p90": 8.5, "p100": 12.0}, "other percentiles"),
    (([3, 1, 2, 4],), {"p50": 2, "p95": 4, "p99": 4}, "an even count"),
    ((list(range(1, 21)), (95,)), {"p95": 19}, "p95 of 20 values"),
], show="percentiles(values, ...)")
try:
    fn([])
except ValueError:
    pass
else:
    raise AssertionError("percentiles([]) should raise ValueError.")
```
```python solution
import math

def percentiles(values, ps=(50, 95, 99)):
    if not values:
        raise ValueError("no values")
    ordered = sorted(values)
    n = len(ordered)
    result = {}
    for p in ps:
        rank = max(1, math.ceil(p / 100 * n))
        result[f"p{p}"] = ordered[rank - 1]
    return result

latencies = [1.2, 0.9, 1.4, 1.1, 8.5, 1.0, 1.3, 0.8, 1.6, 12.0]
print(percentiles(latencies))
```
hint: Sort first. The nearest-rank method picks an actual value from the sorted list; no interpolation.
hint: Rank `ceil(p / 100 × n)` counts from 1, so the list index is `rank − 1`; `max(1, …)` handles p = 0.
hint: Build the key with `f"p{p}"`.
approach:
1. **Understand:** sort; for each p, the smallest value with at least p% of values at or below it.
2. **Examples:** 10 values, p95 → rank ceil(9.5) = 10 → the largest value (12.0).
3. **Brute force:** for each p, test every value: O(n²).
4. **Pattern:** **sort once, index by rank**.
5. **Plan:** validate → sort → ranks → dict.
6. **Code and test:** one value, 1 to 100, p0 and p100, an even count.
walkthrough:
**Line by line**

- Sorting once serves every percentile.
- `math.ceil` makes p50 of 4 values rank 2 (the lower middle value), as nearest-rank defines it.
- `max(1, …)` stops p0 producing rank 0 (which would wrongly index the last element with `-1`).
- Other definitions (with interpolation, such as NumPy's default) give slightly different numbers; what matters is using one method consistently.

**Trace:** sorted = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 8.5, 12.0]; p50 → rank 5 → 1.2; p95 and p99 → rank 10 → 12.0. The mean is 2.98 s, which describes nobody's experience.

**Complexity:** O(n log n).

**Common wrong approach:** reporting the mean, or p95 of a tiny sample. With 10 requests, p95 and p99 are just the slowest one; you need hundreds of requests for a stable tail estimate.
:::

:::exercise An exact-match response cache
Simulate a response cache and report its hit rate. Write `cache_hit_rate(requests, ttl)`, where `requests` is a list of `(time_in_seconds, question)` in time order:

- Normalise each question: lower-case and collapse whitespace (`" ".join(q.lower().split())`).
- A request is a **hit** if its normalised question is in the cache and was stored less than `ttl` seconds earlier.
- Otherwise it's a miss, and the answer is stored with the current time (replacing any expired entry). Hits don't refresh the stored time.

Return hits ÷ requests (`0.0` for no requests).
```python starter
def cache_hit_rate(requests, ttl):
    pass

requests = [(0, "What are your opening hours?"), (30, "what are your  opening hours?"),
            (90, "Do you fix e-bikes?"), (400, "What are your opening hours?")]
print(cache_hit_rate(requests, ttl=300))   # 0.25: one hit; the last request is too late
```
```python check
fn = need("cache_hit_rate")
_q = "What are your opening hours?"
test(fn, cases=[
    (([(0, _q), (30, "what are your  opening hours?"), (90, "Do you fix e-bikes?"), (400, _q)], 300), 0.25, "one hit, one expired"),
    (([], 60), 0.0, "no requests"),
    (([(0, "a"), (1, "a"), (2, "a"), (3, "a")], 60), 0.75, "repeats within the lifetime"),
    (([(0, "a"), (60, "a")], 60), 0.0, "exactly at the lifetime is expired"),
    (([(0, "a"), (59, "a"), (61, "a"), (100, "a")], 60), 0.5, "hits don't refresh; the expired entry is replaced"),
    (([(0, "Hello"), (1, "HELLO "), (2, " hello")], 10), 2 / 3, "normalisation"),
    (([(0, "a"), (1, "b"), (2, "c")], 100), 0.0, "all different"),
], show="cache_hit_rate(requests, {1})")
```
```python solution
def cache_hit_rate(requests, ttl):
    if not requests:
        return 0.0
    stored = {}                                       # normalised question -> time stored
    hits = 0
    for t, question in requests:
        key = " ".join(question.lower().split())
        if key in stored and t - stored[key] < ttl:
            hits += 1
        else:
            stored[key] = t                           # miss: (re)fill the cache
    return hits / len(requests)

requests = [(0, "What are your opening hours?"), (30, "what are your  opening hours?"),
            (90, "Do you fix e-bikes?"), (400, "What are your opening hours?")]
print(cache_hit_rate(requests, ttl=300))
```
hint: Keep a dict from normalised question to the time its answer was stored.
hint: A hit needs both: the key is present **and** `t - stored[key] < ttl`. Anything else is a miss.
hint: On a miss, set `stored[key] = t`. On a hit, change nothing.
approach:
1. **Understand:** simulate the cache in time order; count hits.
2. **Examples:** stored at 0 with ttl 60: a request at 59 hits; at 61 it's expired → a miss that re-stores at 61; at 100, 100 − 61 = 39 < 60 → hit.
3. **Brute force:** for each request, scan all earlier ones: O(n²).
4. **Pattern:** **simulation with a dict** keyed by the normalised input.
5. **Plan:** loop → normalise → hit test → update on a miss → ratio.
6. **Code and test:** expiry at exactly ttl, refresh rules, normalisation.
walkthrough:
**Line by line**

- `" ".join(q.lower().split())` collapses runs of spaces and trims the ends, so trivial differences still hit.
- The strict `<` means an entry is expired at exactly `ttl` seconds.
- Not refreshing on hits means every entry is re-fetched at least once per `ttl`, which bounds how stale an answer can get.
- Overwriting an expired entry on a miss is the "refetch" step.

**Trace** on the starter: 0 miss (store), 30 hit, 90 miss (new question), 400 → 400 − 0 ≥ 300 → miss → 1 hit in 4 = 0.25.

**Complexity:** O(n × question length).

**Common wrong approach:** caching answers that depend on the user or on live data (an order status, stock levels). Cache only answers that are the same for everyone, include anything that changes the answer in the key, and keep the lifetime short.
:::

:::quiz
? What usually dominates the latency of a long LLM response?
+ Generating the output tokens, one after another
- Sending the request over the network
- JSON parsing
= Shorter outputs are the biggest speed-up.
? Why report p95 latency instead of only the average?
+ The average hides the slow tail that some users hit regularly
- p95 is always smaller
- Averages can't be computed for latency
= Percentiles describe real users' experience.
? What's the main risk of a semantic response cache?
+ Returning a cached answer to a question that's similar but different in an important way
- It's slower than no cache
- It can't store text
= Exact caches are safer; semantic caches hit more often.
? Traffic is expected to triple at launch. What should you plan?
+ Rate-limit headroom at peak, queues for non-urgent work, timeouts and a fallback
- Nothing: APIs scale infinitely
- Removing streaming
= Capacity planning is part of shipping.
:::

@@@ lesson
id: fine-tuning-vs-rag
title: Prompting, RAG or fine-tuning?
minutes: 24
summary: The ladder of ways to adapt a model (prompting, examples, retrieval and tools, fine-tuning, training from scratch), what fine-tuning changes and what it doesn't, supervised, preference and reinforcement fine-tuning, LoRA and other parameter-efficient methods, distillation, preparing training data and avoiding leakage, evaluating against a prompted baseline, and the ongoing costs.
---
When a model doesn't do what you need, there are several ways to change its behaviour. They differ hugely in cost, speed of iteration and what they can fix, so the order you try them in matters.

### The ladder

![A ladder of five rungs from bottom to top: prompt engineering (minutes to change, no training); few-shot examples; retrieval and tools (add knowledge and actions); fine-tuning (days, needs hundreds to thousands of examples, changes behaviour and style); training a model from scratch (months, enormous cost). Arrows show cost and time to iterate rising towards the top. Advice: climb only when the rung below is proven insufficient by evals](figures/adaptation-ladder.svg)

1. **Prompting:** clearer instructions, context, format (Part 3). Changes in minutes.
2. **Examples:** few-shot demonstrations of the behaviour you want.
3. **Retrieval and tools:** give the model **knowledge** it lacks (Part 4) and **actions** it can take (Part 5).
4. **Fine-tuning:** further training on your examples to change its **behaviour**.
5. **Training from scratch:** almost never the right choice outside large AI labs.

Climb a rung only when your evals (Lesson 28) show the rung below can't reach the bar. Most production systems never need step 4.

### What fine-tuning is (and isn't) good for

| Fine-tuning helps with | Fine-tuning is a poor fit for |
|---|---|
| a consistent format, style or tone that's hard to describe | adding facts, especially ones that change (use RAG) |
| narrow, repetitive tasks (classification, extraction) done cheaper by a **smaller** model | citing sources (retrieval provides the evidence) |
| shorter prompts: behaviour learned instead of instructed every call | tasks a better prompt already solves |
| specialised skills where you have many graded examples | small datasets (a few dozen examples) |

The distinction to remember: **RAG changes what the model knows at answer time; fine-tuning changes how it behaves.** They combine well: a fine-tuned model can still answer from retrieved documents.

### Kinds of fine-tuning

- **Supervised fine-tuning (SFT):** train on example conversations ending with the ideal response.
- **Preference fine-tuning** (such as **DPO**, direct preference optimisation): train on pairs of a better and a worse response to the same prompt.
- **Reinforcement fine-tuning (RFT):** the model generates answers, a grader scores them, and training reinforces what scored well. Suited to tasks with checkable answers.

Full fine-tuning updates every weight. **Parameter-efficient** methods such as **LoRA** (low-rank adaptation) train small adapter matrices alongside frozen weights; **QLoRA** does it on a quantised model, so even large open models can be tuned on a single GPU.

**Distillation** trains a small, cheap model on the outputs of a large one, for a narrow task. Check the larger model's terms of service before using its outputs for training.

### Where you can fine-tune

Availability changes often, so check your provider's current documentation:

- **Hosted APIs:** OpenAI offers supervised, preference and reinforcement fine-tuning on selected models; Google's Vertex AI and Amazon Bedrock offer fine-tuning for some of their models. Anthropic's current Claude models are customised through prompting, tools and retrieval rather than public fine-tuning on the Claude API.
- **Open-weight models** (such as Llama, Mistral, Qwen, Gemma and OpenAI's gpt-oss): fine-tune them yourself with Hugging Face's **TRL** and **PEFT** libraries, or tools such as **Unsloth**, then host the result.

### Data is the work

Training data for chat fine-tuning is usually **JSONL**: one JSON object per line, each a short conversation ending with the ideal assistant reply:

```python
import json

examples = [
    {"messages": [{"role": "system", "content": "Classify bike-shop tickets."},
                  {"role": "user", "content": "My brakes squeal when wet."},
                  {"role": "assistant", "content": "repair"}]},
    {"messages": [{"role": "system", "content": "Classify bike-shop tickets."},
                  {"role": "user", "content": "Where is my order 1182?"},
                  {"role": "assistant", "content": "delivery"}]},
]
jsonl = "\n".join(json.dumps(e) for e in examples)
print(jsonl.splitlines()[0][:80], "…")
print(len(jsonl.splitlines()), "training examples")
```

- **Quality beats quantity:** hundreds of correct, consistent, diverse examples beat thousands of noisy ones. Every mistake in the data is taught.
- **Validate the format** before uploading (the first exercise).
- **Hold out a test set**, and make sure no test example also appears in training (**leakage**), including near-duplicates (the second exercise).

### Evaluate, then decide

Compare the fine-tuned model with the **best prompted baseline** on the same held-out eval set: quality, latency and cost per request. Then count the ongoing costs: training runs, hosting a custom model (often priced differently from the base model), re-training whenever your task or data changes, and losing the free improvements of each new base model release, which a prompted system picks up just by switching models.

:::exercise Validate fine-tuning data
Write `validate_examples(records)`. Each record should be a dict with a `"messages"` list. Return a list of `(index, problem)` pairs for the invalid records, in order, reporting only the **first** problem found in each record, checked in this order:

1. `"missing messages"`: not a dict, no `"messages"` key, or it isn't a non-empty list.
2. For each message in order: `"unknown role: <role>"` if the role isn't `system`, `user` or `assistant` (use `None` for a missing role); `"empty content"` if the content isn't a non-empty string (after stripping).
3. `"roles must alternate"`: after an optional **first** `system` message, the roles must go user, assistant, user, assistant, … starting with `user`.
4. `"must end with an assistant message"`.
```python starter
def validate_examples(records):
    pass

records = [
    {"messages": [{"role": "user", "content": "Brakes squeal."}, {"role": "assistant", "content": "repair"}]},
    {"messages": [{"role": "user", "content": "Where's my order?"}]},
    {"messages": [{"role": "user", "content": "Hi"}, {"role": "user", "content": "Hello?"},
                  {"role": "assistant", "content": "other"}]},
]
print(validate_examples(records))
# [(1, 'must end with an assistant message'), (2, 'roles must alternate')]
```
```python check
fn = need("validate_examples")
_m = lambda role, content: {"role": role, "content": content}
_good = {"messages": [_m("system", "Classify."), _m("user", "Brakes squeal."), _m("assistant", "repair")]}
test(fn, cases=[
    (([_good],), [], "a valid record with a system message"),
    (([{"messages": [_m("user", "a"), _m("assistant", "b"), _m("user", "c"), _m("assistant", "d")]}],), [], "a multi-turn record"),
    (([{"messages": [_m("user", "Where's my order?")]}],), [(0, "must end with an assistant message")], "no answer"),
    (([{"messages": [_m("user", "Hi"), _m("user", "Hello?"), _m("assistant", "x")]}],), [(0, "roles must alternate")], "two user turns"),
    (([{"messages": [_m("assistant", "Hi"), _m("user", "x"), _m("assistant", "y")]}],), [(0, "roles must alternate")], "starts with assistant"),
    (([{"messages": [_m("user", "a"), _m("system", "b"), _m("assistant", "c")]}],), [(0, "roles must alternate")], "a system message later on"),
    (([{"messages": []}, {"prompt": "x"}, "not a dict", {"messages": "text"}],),
     [(0, "missing messages"), (1, "missing messages"), (2, "missing messages"), (3, "missing messages")], "missing or invalid messages"),
    (([{"messages": [_m("user", "  "), _m("assistant", "b")]}],), [(0, "empty content")], "blank content"),
    (([{"messages": [_m("user", "a"), {"content": "b"}]}],), [(0, "unknown role: None")], "a missing role"),
    (([{"messages": [_m("tool", "a"), _m("assistant", "b")]}],), [(0, "unknown role: tool")], "an unsupported role"),
    (([{"messages": [_m("user", "a"), _m("assistant", 5)]}],), [(0, "empty content")], "content that isn't a string"),
    (([_good, {"messages": [_m("user", "x")]}, _good],), [(1, "must end with an assistant message")], "indexes"),
], show="validate_examples(records)")
```
```python solution
ROLES = {"system", "user", "assistant"}

def problem(record):
    if not isinstance(record, dict) or not isinstance(record.get("messages"), list) or not record["messages"]:
        return "missing messages"
    messages = record["messages"]
    for m in messages:
        role = m.get("role")
        if role not in ROLES:
            return f"unknown role: {role}"
        content = m.get("content")
        if not isinstance(content, str) or not content.strip():
            return "empty content"
    turns = messages[1:] if messages[0]["role"] == "system" else messages
    for i, m in enumerate(turns):
        if m["role"] != ("user" if i % 2 == 0 else "assistant"):
            return "roles must alternate"
    if messages[-1]["role"] != "assistant":
        return "must end with an assistant message"
    return None

def validate_examples(records):
    found = []
    for index, record in enumerate(records):
        p = problem(record)
        if p:
            found.append((index, p))
    return found

records = [
    {"messages": [{"role": "user", "content": "Brakes squeal."}, {"role": "assistant", "content": "repair"}]},
    {"messages": [{"role": "user", "content": "Where's my order?"}]},
    {"messages": [{"role": "user", "content": "Hi"}, {"role": "user", "content": "Hello?"},
                  {"role": "assistant", "content": "other"}]},
]
print(validate_examples(records))
```
hint: Write a helper that returns the first problem of **one** record (or `None`), checking in the stated order; returning early makes "first problem only" automatic.
hint: For alternation, drop a leading system message, then the role at position `i` must be `"user"` when `i` is even and `"assistant"` when it's odd. A system message anywhere else fails this check.
hint: `m.get("role")` gives `None` for a missing role, so the message is `f"unknown role: {role}"` → "unknown role: None".
approach:
1. **Understand:** a sequence of checks per record; report the first failure with its index.
2. **Examples:** `[user, user, assistant]` → position 1 should be assistant → "roles must alternate".
3. **Brute force:** collecting every problem per record: more output, but harder to act on.
4. **Pattern:** **validation with early return**, one helper per item.
5. **Plan:** structure → per-message checks → alternation → final role → collect.
6. **Code and test:** each failure type, a valid multi-turn record, mixed lists.
walkthrough:
**Line by line**

- The first check guards everything after it: once `messages` is a non-empty list, indexing `[0]` and `[-1]` is safe.
- Checking roles and content before the alternation rule means the alternation check only sees valid roles.
- Slicing off one leading system message keeps the even/odd rule simple.
- `enumerate(records)` provides the index to report, so you can find the bad line in the file.

**Trace** on the starter: record 0 is valid; record 1 ends with a user message; record 2 has user at position 1 where assistant should be.

**Complexity:** O(total messages).

**Common wrong approach:** uploading without validating and discovering the problem after a failed (or worse, a successful but wrong) training run. Also check consistency **across** records: the same system prompt and label spellings everywhere.
:::

:::exercise Split without leakage
Write `split_dataset(examples, test_fraction, seed)`, where each example is a dict with an `"input"` and an `"output"`:

1. **Deduplicate** by normalised input (`" ".join(input.lower().split())`), keeping the **first** occurrence.
2. Shuffle the deduplicated list with `random.Random(seed).shuffle(...)`.
3. The first `round(len(unique) × test_fraction)` examples are the test set; the rest are training.

Return `(train, test)`. Don't modify the input list.
```python starter
import random

def split_dataset(examples, test_fraction, seed):
    pass

examples = [{"input": "My brakes squeal", "output": "repair"},
            {"input": "Where is order 1182?", "output": "delivery"},
            {"input": "my  brakes squeal", "output": "repair"},          # a near-duplicate
            {"input": "Do you sell helmets?", "output": "sales"},
            {"input": "Chain keeps slipping", "output": "repair"}]
train, test = split_dataset(examples, 0.25, seed=7)
print(len(train), "train,", len(test), "test")                          # 3 train, 1 test
```
```python check
import random
fn = need("split_dataset")
_norm = lambda s: " ".join(s.lower().split())
def _ref(examples, frac, seed):
    seen, unique = set(), []
    for e in examples:
        k = _norm(e["input"])
        if k not in seen:
            seen.add(k)
            unique.append(e)
    random.Random(seed).shuffle(unique)
    n = round(len(unique) * frac)
    return unique[n:], unique[:n]
_ex = [{"input": f"ticket {i}: {'brakes' if i % 3 else 'order'} issue", "output": "x"} for i in range(40)]
_ex += [{"input": "TICKET 5:  brakes issue", "output": "dup"}, {"input": "ticket 7: brakes issue ", "output": "dup"}]
_before = [dict(e) for e in _ex]
_res = fn(_ex, 0.2, 42)
assert isinstance(_res, tuple) and len(_res) == 2, "Return a (train, test) tuple."
_tr, _te = _res
assert _ex == _before, "Don't modify the input list."
same(len(_tr) + len(_te), 40, what="The total after removing the 2 near-duplicates")
same(len(_te), 8, what="The test set size (round(40 × 0.2))")
_overlap = {_norm(e["input"]) for e in _tr} & {_norm(e["input"]) for e in _te}
assert not _overlap, f"Leakage: these inputs are in both sets: {sorted(_overlap)[:3]}"
assert all(e["output"] != "dup" for e in _tr + _te), "Keep the first occurrence of a duplicate, not a later one."
same(fn(_ex, 0.2, 42), _res, what="A second call with the same seed (should be identical)")
_exp = _ref(_ex, 0.2, 42)
assert (_tr, _te) == _exp, "The split has the right shape but not the expected order: dedupe first (keeping the first), then random.Random(seed).shuffle the unique list, then take the first n as the test set."
same(fn([], 0.3, 1), ([], []), what="split_dataset([], 0.3, 1)")
same(len(fn(_ex, 0.0, 1)[1]), 0, what="The test size with test_fraction 0")
```
```python solution
import random

def split_dataset(examples, test_fraction, seed):
    seen, unique = set(), []
    for example in examples:
        key = " ".join(example["input"].lower().split())
        if key not in seen:                       # keep the first of any near-duplicates
            seen.add(key)
            unique.append(example)
    random.Random(seed).shuffle(unique)           # a new list, so the input is untouched
    n_test = round(len(unique) * test_fraction)
    return unique[n_test:], unique[:n_test]

examples = [{"input": "My brakes squeal", "output": "repair"},
            {"input": "Where is order 1182?", "output": "delivery"},
            {"input": "my  brakes squeal", "output": "repair"},
            {"input": "Do you sell helmets?", "output": "sales"},
            {"input": "Chain keeps slipping", "output": "repair"}]
train, test = split_dataset(examples, 0.25, seed=7)
print(len(train), "train,", len(test), "test")
```
hint: Deduplicate first with a `seen` set of normalised inputs, building a new list (this also protects the input from the shuffle).
hint: `random.Random(seed)` is a random generator with its own seed: the same seed always gives the same shuffle, without affecting the global `random` state.
hint: `n_test = round(len(unique) * test_fraction)`; return `unique[n_test:], unique[:n_test]`.
approach:
1. **Understand:** remove near-duplicates **before** splitting, so no input lands in both sets; make the split reproducible.
2. **Examples:** "My brakes squeal" and "my  brakes squeal" normalise to the same key → one is dropped.
3. **Brute force:** split first, then dedupe each half: duplicates can still straddle the split.
4. **Pattern:** **dedupe → seeded shuffle → slice**.
5. **Plan:** normalised keys → unique list → shuffle → split.
6. **Code and test:** duplicates, reproducibility, an empty list, a fraction of 0.
walkthrough:
**Line by line**

- The normalisation matches how near-duplicates usually differ (case and spacing); real pipelines also catch paraphrases with embeddings.
- Building `unique` as a new list means shuffling it can't reorder the caller's data.
- A local `random.Random(seed)` makes the split reproducible, so results can be compared across experiments.
- `round` gives the nearest whole number of test examples (Python rounds halves to even: `round(2.5)` is 2).

**Trace** on the starter: 5 examples → 4 unique → shuffled → round(4 × 0.25) = 1 test, 3 train.

**Complexity:** O(n).

**Common wrong approach:** splitting before deduplicating, so the same ticket appears in training and test; the test score then measures memory, not skill, and looks far better than real performance.
:::

:::quiz
? Your support bot needs to answer from a policy document that changes monthly. What's the right tool?
+ Retrieval (RAG), so answers use the current document
- Fine-tuning on the policy each month
- Training a model from scratch
= Fine-tuning changes behaviour; RAG supplies changing knowledge.
? When is fine-tuning most likely to pay off?
+ A narrow, repetitive task with many good examples, where a smaller tuned model can replace a larger prompted one
- When you have 12 examples
- When a better prompt already solves it
= Prove the need with evals first.
? What does LoRA do?
+ Trains small adapter matrices while keeping the original weights frozen
- Deletes layers to make the model smaller
- Adds retrieval to a model
= Parameter-efficient fine-tuning cuts memory and cost.
? Why remove near-duplicates before splitting train and test sets?
+ Otherwise the same example can appear in both, and the test score measures memorisation
- To make training faster
- Because JSONL forbids duplicates
= Leakage makes results look better than they are.
:::
