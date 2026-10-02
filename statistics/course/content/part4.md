@@@ part
id: 4
title: Hypothesis Testing
level: Intermediate
blurb: Decide whether a difference is real or could just be luck: null hypotheses, p-values, permutation tests, t-tests, errors and power, chi-square tests and ANOVA.

@@@ lesson
id: hypothesis-testing
title: Hypothesis testing and p-values
minutes: 20
summary: The logic of a test, null and alternative hypotheses, p-values explained with a permutation test, and how (not) to read them.
---
Page B converted 12.8% of visitors and page A 10.2%. Is B really better, or did B just get luckier visitors this time? A **hypothesis test** answers: *if there were really no difference, how surprising would a gap this big be?*

### The logic, step by step

1. **Null hypothesis (H₀):** the boring explanation: "there's no difference; any gap is luck."
2. **Alternative hypothesis (H₁):** what you suspect: "there is a difference."
3. Pick a **test statistic** that measures the gap (here, rate B − rate A).
4. Work out what values the statistic would take **if H₀ were true**: the **null distribution**.
5. The **p-value** is the probability of a result at least as extreme as yours, if H₀ were true.
6. If the p-value is small (usually below **0.05**, the **significance level** α), reject H₀: the result is **statistically significant**.

![A bell-shaped null distribution with the observed statistic marked far out on the right; both tails beyond it are shaded red and labelled p = 0.036](figures/p-value.svg)

It's like a court: the defendant (H₀) is presumed innocent, and you only convict if the evidence would be very unlikely under innocence. "Not significant" means "not enough evidence", **not** "proved innocent".

### A permutation test: build the null distribution yourself

If the page made no difference, the "A" and "B" labels are meaningless: you could shuffle them and the gap would be just as big. So shuffle the labels thousands of times and see how often a shuffled gap is as big as the real one:

```python
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
converted = ab["converted"].to_numpy()
is_b = (ab["group"] == "B").to_numpy()
observed = converted[is_b].mean() - converted[~is_b].mean()

rng = np.random.default_rng(0)
null_gaps = []
for _ in range(5000):
    shuffled = rng.permutation(is_b)            # random labels: H0 is true by design
    null_gaps.append(converted[shuffled].mean() - converted[~shuffled].mean())
null_gaps = np.array(null_gaps)

p_value = (np.abs(null_gaps) >= abs(observed)).mean()
print(f"observed gap: {observed:.4f}")
print(f"p-value: {p_value:.4f}")
```

Only a tiny share of the shuffled gaps are as big as the real one, so the p-value is small and we reject H₀: page B's advantage is unlikely to be luck.

Let's draw the null distribution and where the real gap falls:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ab = pd.read_csv("ab_test.csv")
converted = ab["converted"].to_numpy()
is_b = (ab["group"] == "B").to_numpy()
observed = converted[is_b].mean() - converted[~is_b].mean()
rng = np.random.default_rng(0)
null_gaps = [converted[s].mean() - converted[~s].mean() for s in (rng.permutation(is_b) for _ in range(3000))]

fig, ax = plt.subplots(figsize=(7, 3))
ax.hist(null_gaps, bins=40, color="lightgrey", edgecolor="white")
ax.axvline(observed, color="darkorange", linewidth=2, label="observed gap")
ax.set_xlabel("gap in conversion rate (B - A) when labels are shuffled")
ax.legend()
plt.show()
```

### One-sided or two-sided?

A **two-sided** test asks "is there a difference in either direction?" and counts both tails (that's why we used `np.abs`). A **one-sided** test asks only "is B better?" and counts one tail. Decide **before** looking at the data; two-sided is the safe default.

### Reading p-values correctly

| The p-value IS | The p-value is NOT |
|---|---|
| how surprising the data would be if H₀ were true | the probability that H₀ is true |
| a measure of evidence against H₀ | the size or importance of the effect |
| affected by the sample size | proof of anything |

- **p = 0.03:** if there were no real difference, a gap this big would turn up only 3% of the time. Evidence against H₀.
- **p = 0.40:** gaps this big are common by chance alone. Not evidence of a difference (but not proof of no difference either).
- With huge samples, tiny, unimportant differences become "significant". Always report the **effect size** (how big the difference is) alongside the p-value.

### The 0.05 threshold

0.05 is a convention, not a law of nature. Some fields use 0.01 or stricter (particle physics uses about 0.0000003). Report the actual p-value rather than just "significant" or not, and never change α after seeing the results.

:::exercise Permutation test for study hours
Do students in class A study more hours than students in class B? Load `students.csv`, keep classes A and B, and compute `observed`: the mean `hours_studied` of A minus that of B. Then, with `rng = np.random.default_rng(1)`, shuffle the class labels **4,000** times (use `rng.permutation(is_a)` each time) and store the **two-sided** p-value in `p_value`.
```python starter
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
ab = students[students["class"].isin(["A", "B"])]
hours = ab["hours_studied"].to_numpy()
is_a = (ab["class"] == "A").to_numpy()
rng = np.random.default_rng(1)

```
```python check
import numpy as np
import pandas as pd
s = pd.read_csv("students.csv")
d = s[s["class"].isin(["A", "B"])]
h = d["hours_studied"].to_numpy(); ia = (d["class"] == "A").to_numpy()
obs = h[ia].mean() - h[~ia].mean()
same(float(need("observed")), float(obs), "observed")
rng = np.random.default_rng(1)
gaps = []
for _ in range(4000):
    sh = rng.permutation(ia)
    gaps.append(h[sh].mean() - h[~sh].mean())
p = (np.abs(gaps) >= abs(obs)).mean()
same(float(need("p_value")), float(p), "p_value")
```
```python solution
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
ab = students[students["class"].isin(["A", "B"])]
hours = ab["hours_studied"].to_numpy()
is_a = (ab["class"] == "A").to_numpy()
rng = np.random.default_rng(1)

observed = hours[is_a].mean() - hours[~is_a].mean()
gaps = []
for _ in range(4000):
    shuffled = rng.permutation(is_a)
    gaps.append(hours[shuffled].mean() - hours[~shuffled].mean())
p_value = (np.abs(gaps) >= abs(observed)).mean()
print(round(observed, 2), p_value)
```
hint: Inside the loop, `shuffled = rng.permutation(is_a)`, then the gap is `hours[shuffled].mean() - hours[~shuffled].mean()`. The p-value is the share of `abs(gap) >= abs(observed)`.
:::

:::exercise Read the result
A test of a new checkout button gives p = 0.21. Set `reject` to `True` or `False` for α = 0.05, and set `meaning` to the letter of the correct statement:

- `"a"`: the new button has no effect;
- `"b"`: a difference this big would happen fairly often by chance, so there isn't enough evidence of an effect;
- `"c"`: there is a 21% chance the new button works.
```python starter
reject = None
meaning = ""
```
```python check
same(need("reject"), False, "reject")
same(need("meaning"), "b", "meaning")
```
```python solution
reject = False
meaning = "b"
```
hint: 0.21 is above 0.05. And a p-value is never "the chance the hypothesis is true".
:::

:::quiz
? What is the null hypothesis in an A/B test?
+ There's no real difference between A and B
- B is better than A
- The test was run correctly
= H₀ is the "nothing is going on" explanation that the test tries to find evidence against.
? p = 0.002 means:
- There's a 0.2% chance H₀ is true
+ If H₀ were true, a result this extreme would happen only 0.2% of the time
- The effect is large
= A p-value is a probability about the data assuming H₀, not about H₀ itself.
? A huge test finds p = 0.001 for a 0.01% lift in sales. What should you conclude?
- It's an important improvement
+ It's statistically significant but probably too small to matter
- The test is wrong
= Large samples make tiny effects significant. Judge the effect size too.
:::

@@@ lesson
id: t-tests
title: t-tests: comparing means
minutes: 20
summary: The one-sample, two-sample (Welch) and paired t-tests with SciPy, their assumptions, and reporting an effect size.
---
The **t-test** is the classic way to compare averages. It turns a difference into a **t statistic** (the difference divided by its standard error, "how many standard errors apart?") and compares it with the t distribution to get a p-value. SciPy has one function for each situation:

| Question | Test | SciPy |
|---|---|---|
| Is one group's mean different from a fixed value? | one-sample t-test | `stats.ttest_1samp(x, value)` |
| Do two separate groups have different means? | two-sample (Welch's) t-test | `stats.ttest_ind(a, b, equal_var=False)` |
| Did the same people change between two measurements? | paired t-test | `stats.ttest_rel(before, after)` |

### One-sample t-test

The school's target is an average math score of 60. Are these students below target?

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
res = stats.ttest_1samp(students["math"], 60)
print(f"mean {students['math'].mean():.1f}, t = {res.statistic:.2f}, p = {res.pvalue:.3f}")
```

The mean is 56.6, below 60, but p = 0.078 is above 0.05: a gap this size could plausibly be chance, so there isn't enough evidence that the true average is below target. If you had decided **in advance** to ask only "is it below 60?", a one-sided test (`alternative="less"`) would halve the p-value to about 0.04. That's exactly why the direction must be chosen before looking.

### Two-sample t-test

Do class A and class B differ in math? Use **Welch's** t-test (`equal_var=False`), which doesn't assume the two groups have the same spread. It's the safer default:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
a = students.loc[students["class"] == "A", "math"]
b = students.loc[students["class"] == "B", "math"]
res = stats.ttest_ind(a, b, equal_var=False)
print(f"A {a.mean():.1f} vs B {b.mean():.1f}: t = {res.statistic:.2f}, p = {res.pvalue:.3f}")
```

A difference of about 6 points, but p is well above 0.05: with only 22 students per class and lots of spread, a gap this size could easily be chance.

### Paired t-test

When the **same people** are measured twice (before and after training), compare each person with themselves. That removes the big differences **between** people and makes the test far more sensitive:

![Thirty lines, one per employee, joining their score before training to their score after; most lines slope upwards](figures/before-after.svg)

```python
import pandas as pd
from scipy import stats

training = pd.read_csv("training.csv")
diff = training["after"] - training["before"]
paired = stats.ttest_rel(training["after"], training["before"])
wrong = stats.ttest_ind(training["after"], training["before"], equal_var=False)
print(f"average improvement: {diff.mean():.1f} points")
print(f"paired t-test:       p = {paired.pvalue:.4f}")
print(f"(wrong) unpaired:    p = {wrong.pvalue:.4f}")
```

The paired test finds a clear improvement; the unpaired test, which ignores who is who, misses it. **Use the paired test whenever measurements come in pairs.**

### A confidence interval for the difference

A p-value says whether there's evidence of a difference; a confidence interval says **how big** it might be. Results from `ttest_rel` and `ttest_ind` have a `confidence_interval()` method:

```python
import pandas as pd
from scipy import stats

training = pd.read_csv("training.csv")
res = stats.ttest_rel(training["after"], training["before"])
ci = res.confidence_interval(0.95)
print(f"improvement: 95% CI {ci.low:.1f} to {ci.high:.1f} points")
```

### Effect size: Cohen's d

**Cohen's d** expresses a difference in standard deviations, so it can be compared across studies: about 0.2 is small, 0.5 medium, 0.8 large.

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
a = students.loc[students["class"] == "A", "math"]
b = students.loc[students["class"] == "B", "math"]
pooled_sd = np.sqrt((a.var() + b.var()) / 2)
print("Cohen's d:", round((a.mean() - b.mean()) / pooled_sd, 2))
```

### Assumptions

t-tests assume independent observations, and roughly normal data **or** large enough samples (about 30 per group, thanks to the central limit theorem). For small, very skewed samples, use a **rank-based** test that doesn't assume normality: **Mann-Whitney U** instead of the two-sample t-test, or **Wilcoxon signed-rank** instead of the paired test:

```python
import pandas as pd
from scipy import stats

training = pd.read_csv("training.csv")
print("Wilcoxon signed-rank p:", round(stats.wilcoxon(training["after"], training["before"]).pvalue, 4))

students = pd.read_csv("students.csv")
a = students.loc[students["class"] == "A", "math"]
b = students.loc[students["class"] == "B", "math"]
print("Mann-Whitney U p:      ", round(stats.mannwhitneyu(a, b).pvalue, 3))
```

### Reporting

A good report includes the means, the difference with its confidence interval, the test and the p-value: *"After training, scores rose by 4.1 points on average (95% CI 1.9 to 6.2; paired t-test, p < 0.001)."*

:::exercise Did training help?
Load `training.csv`. Run a **paired** t-test of `after` against `before` and store the p-value in `p_paired`. Store the average improvement (after − before) in `mean_gain`.
```python starter
import pandas as pd
from scipy import stats

training = pd.read_csv("training.csv")

```
```python check
import pandas as pd
from scipy import stats
t = pd.read_csv("training.csv")
same(float(need("p_paired")), float(stats.ttest_rel(t["after"], t["before"]).pvalue), "p_paired")
same(float(need("mean_gain")), float((t["after"] - t["before"]).mean()), "mean_gain")
```
```python solution
import pandas as pd
from scipy import stats

training = pd.read_csv("training.csv")
p_paired = stats.ttest_rel(training["after"], training["before"]).pvalue
mean_gain = (training["after"] - training["before"]).mean()
print(round(mean_gain, 2), p_paired)
```
hint: `stats.ttest_rel(training["after"], training["before"]).pvalue`.
:::

:::exercise Revenue per buyer
Load `ab_test.csv` and keep only visitors who **converted**. Compare their `revenue` between group A and group B with **Welch's** t-test and store the p-value in `p_rev`. Set `significant` to `True` if p < 0.05, otherwise `False`.
```python starter
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
from scipy import stats
a = pd.read_csv("ab_test.csv")
b = a[a["converted"] == 1]
p = stats.ttest_ind(b.loc[b["group"] == "A", "revenue"], b.loc[b["group"] == "B", "revenue"], equal_var=False).pvalue
same(float(need("p_rev")), float(p), "p_rev")
same(need("significant"), bool(p < 0.05), "significant")
```
```python solution
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
buyers = ab[ab["converted"] == 1]
rev_a = buyers.loc[buyers["group"] == "A", "revenue"]
rev_b = buyers.loc[buyers["group"] == "B", "revenue"]
p_rev = stats.ttest_ind(rev_a, rev_b, equal_var=False).pvalue
significant = bool(p_rev < 0.05)
print(round(p_rev, 3), significant)
```
hint: Filter `converted == 1` first, then split by group and use `stats.ttest_ind(a, b, equal_var=False)`.
:::

:::quiz
? The same 30 employees are tested before and after a course. Which test fits?
- Welch's two-sample t-test
+ Paired t-test
- One-sample t-test against 0 on the before scores
= Each person is measured twice, so compare each person with themselves.
? Why is Welch's t-test (`equal_var=False`) a good default?
+ It doesn't assume the two groups have equal spread
- It always gives smaller p-values
- It works without any data
= When spreads differ, the classic equal-variance test can mislead; Welch's handles both cases.
? Cohen's d of 0.8 means:
- p = 0.8
+ The means differ by about 0.8 standard deviations, a large effect
- 80% of people improved
= Cohen's d measures the size of a difference in standard-deviation units.
:::

@@@ lesson
id: errors-and-power
title: Errors, power and sample size
minutes: 18
summary: Type I and Type II errors, statistical power, how many people you need in a study, and the multiple-testing trap.
---
A test can be wrong in two ways:

| | H₀ really true (no effect) | H₀ really false (real effect) |
|---|---|---|
| **You reject H₀** | ❌ **Type I error**: a false alarm. Probability α | ✅ correct: you found it. Probability = **power** |
| **You don't reject H₀** | ✅ correct | ❌ **Type II error**: a missed effect. Probability β |

![Two overlapping bell curves, one for no effect and one for a real effect, with a decision line; the red area past the line under the first curve is α, the grey area before the line under the second curve is β, and the rest of the second curve is the power](figures/errors-power.svg)

- **α (alpha)**, the significance level, is the false-alarm rate you accept, usually 5%.
- **β (beta)** is the chance of missing a real effect.
- **Power = 1 − β**: the chance of detecting an effect that's really there. 80% is the usual target.

Moving the decision line trades one error for the other: a stricter α means fewer false alarms but more missed effects. The only way to reduce **both** is more data.

### See α by simulation

If H₀ is true, a test at α = 0.05 should give a false alarm about 5% of the time. Run 2,000 A/A tests (both groups from the same population):

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(0)
false_alarms = 0
for _ in range(2000):
    a = rng.normal(50, 10, 40)
    b = rng.normal(50, 10, 40)          # same population: no real effect
    false_alarms += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05
print("false-alarm rate:", false_alarms / 2000)
```

### See power by simulation

Now give group B a real, modest effect (+5 points, half a standard deviation) and count how often the test finds it, for different sample sizes:

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(1)
for n in (10, 30, 64, 100):
    found = sum(stats.ttest_ind(rng.normal(50, 10, n), rng.normal(55, 10, n), equal_var=False).pvalue < 0.05
                for _ in range(1000))
    print(f"n = {n:3} per group: power ≈ {found / 1000:.0%}")
```

With 10 per group, a real effect is usually missed. You need about 64 per group to reach 80% power for an effect of this size.

### Power depends on four things

| Increase this… | …and power |
|---|---|
| sample size n | goes up |
| true effect size | goes up (big effects are easier to spot) |
| α (being less strict) | goes up, but with more false alarms |
| spread (noise) in the data | goes down |

### Sample size before you start

Decide the sample size **before** collecting data: pick the smallest effect worth detecting, α and the power you want. statsmodels solves for n:

```python
from statsmodels.stats.power import TTestIndPower

n = TTestIndPower().solve_power(effect_size=0.5, alpha=0.05, power=0.8)
print(f"about {n:.0f} people per group for a medium effect (d = 0.5)")
n_small = TTestIndPower().solve_power(effect_size=0.2, alpha=0.05, power=0.8)
print(f"about {n_small:.0f} per group for a small effect (d = 0.2)")
```

Small effects need **lots** of data: since n grows with 1 / effect², halving the effect size needs four times the people.

### The multiple-testing trap

Run 20 tests at α = 0.05 on data with no real effects, and you'd expect **one** false alarm. Test enough things ("does the new design work for mobile? For desktop? On Tuesdays? For users in Leeds?") and something will look significant by luck. This is how many false discoveries are made (also called **p-hacking** when it's done by digging until something works).

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(5)
pvals = [stats.ttest_ind(rng.normal(0, 1, 50), rng.normal(0, 1, 50)).pvalue for _ in range(20)]
print("tests 'significant' by luck:", sum(p < 0.05 for p in pvals), "of 20")
print("with Bonferroni (α / 20):  ", sum(p < 0.05 / 20 for p in pvals), "of 20")
```

Fixes: decide the tests in advance, and correct for the number of tests. The **Bonferroni** correction divides α by the number of tests (simple but strict); `statsmodels.stats.multitest.multipletests` offers gentler methods like Holm and Benjamini-Hochberg.

:::exercise Simulate power
With `rng = np.random.default_rng(3)`, run **500** simulated experiments where group A is `rng.normal(100, 15, 25)` and group B is `rng.normal(110, 15, 25)` (draw A first, then B, each time). Use Welch's t-test and store the share of experiments with p < 0.05 in `power`.
```python starter
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)

```
```python check
import numpy as np
from scipy import stats
rng = np.random.default_rng(3)
hits = 0
for _ in range(500):
    a = rng.normal(100, 15, 25); b = rng.normal(110, 15, 25)
    hits += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05
same(float(need("power")), hits / 500, "power")
```
```python solution
import numpy as np
from scipy import stats

rng = np.random.default_rng(3)
hits = 0
for _ in range(500):
    a = rng.normal(100, 15, 25)
    b = rng.normal(110, 15, 25)
    if stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05:
        hits += 1
power = hits / 500
print(power)
```
hint: Loop 500 times; draw `a` then `b`; count p-values below 0.05; divide by 500.
:::

:::exercise How many people?
Using `TTestIndPower().solve_power`, store the number of people needed **per group** to detect an effect size of **0.3** with α = 0.05 and **90%** power in `n_needed`, rounded **up** to a whole number with `math.ceil`.
```python starter
import math
from statsmodels.stats.power import TTestIndPower

```
```python check
import math
from statsmodels.stats.power import TTestIndPower
same(int(need("n_needed")), math.ceil(TTestIndPower().solve_power(effect_size=0.3, alpha=0.05, power=0.9)), "n_needed")
```
```python solution
import math
from statsmodels.stats.power import TTestIndPower

n = TTestIndPower().solve_power(effect_size=0.3, alpha=0.05, power=0.9)
n_needed = math.ceil(n)
print(n_needed)
```
hint: `TTestIndPower().solve_power(effect_size=0.3, alpha=0.05, power=0.9)`, then `math.ceil(...)`. You can't recruit part of a person, so round up.
:::

:::quiz
? A Type I error is:
+ Concluding there's an effect when there isn't one (a false alarm)
- Missing a real effect
- A mistake in the code
= Rejecting a true null hypothesis; its probability is α.
? What's the most direct way to increase power without more false alarms?
- Lower α to 0.01
+ Collect a larger sample
- Run more tests
= More data shrinks the standard error, making real effects easier to detect.
? You test 40 different customer segments and find 2 "significant" at α = 0.05. What's the concern?
- None: 2 effects were found
+ About 2 false alarms are expected by chance alone with 40 tests
- The sample was too large
= Multiple testing: correct for the number of tests or treat the findings as hypotheses to check.
:::

@@@ lesson
id: chi-square
title: Chi-square tests for counts
minutes: 18
summary: Test whether counts match what you'd expect (goodness of fit), and whether two categorical variables are related (independence).
---
t-tests compare averages. For **counts in categories** (how many customers in each city, how many buyers per page version), the tool is the **chi-square test** (χ², "kai-square"). It compares the counts you **observed** with the counts you'd **expect** if H₀ were true:

χ² = Σ (observed − expected)² / expected

Big gaps between observed and expected give a big χ² and a small p-value.

![Grouped bars for each dice face: observed counts next to the expected 10 per face; face 6 came up 17 times](figures/observed-expected.svg)

### Goodness of fit: does the data match a claim?

A dice is rolled 60 times. A fair dice should give about 10 of each face. Face 6 came up 17 times. Loaded, or luck?

```python
from scipy import stats

observed = [8, 9, 10, 7, 9, 17]
expected = [10] * 6
res = stats.chisquare(observed, expected)
print(f"chi-square = {res.statistic:.2f}, p = {res.pvalue:.3f}")
```

p is above 0.05: 17 sixes in 60 rolls isn't unusual enough to call the dice loaded. You'd need more rolls.

The expected counts don't have to be equal. A company claims its customers are 55% consumers, 30% business and 15% students. Does our data fit?

```python
import pandas as pd
from scipy import stats

customers = pd.read_csv("customers.csv")
observed = customers["segment"].value_counts().reindex(["Consumer", "Business", "Student"])
expected = [0.55 * len(customers), 0.30 * len(customers), 0.15 * len(customers)]
print(observed.tolist(), [round(e, 1) for e in expected])
print("p =", round(stats.chisquare(observed, expected).pvalue, 3))
```

The expected counts must add up to the same total as the observed ones.

### Test of independence: are two categories related?

Is a visitor's device related to whether they convert? Make a two-way table of counts and run `chi2_contingency`:

```python
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
table = pd.crosstab(ab["device"], ab["converted"])
print(table)
res = stats.chi2_contingency(table)
print(f"chi-square = {res.statistic:.1f}, p = {res.pvalue:.1e}, degrees of freedom = {res.dof}")
print("expected counts if unrelated:")
print(pd.DataFrame(res.expected_freq, index=table.index, columns=table.columns).round(1))
```

H₀ is "device and converting are independent". The expected table shows the counts you'd get if each device converted at the overall rate. The observed counts are far from it (p is tiny): device and converting are related, which matches the conversion rates you saw earlier.

The same test answers "does page version affect conversion?", the core of an A/B test with yes/no outcomes:

```python
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
table = pd.crosstab(ab["group"], ab["converted"])
print("p =", round(stats.chi2_contingency(table).pvalue, 4))
```

### How strong is the relationship?

As with t-tests, a p-value doesn't say how **strong** a relationship is. **Cramér's V** does, on a 0 (none) to 1 (perfect) scale:

```python
import numpy as np
import pandas as pd
from scipy import stats

customers = pd.read_csv("customers.csv")
table = pd.crosstab(customers["city"], customers["segment"])
chi2 = stats.chi2_contingency(table).statistic
n = table.to_numpy().sum()
v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))
print("p =", round(stats.chi2_contingency(table).pvalue, 3), " Cramér's V =", round(v, 2))
```

### Rules of thumb

- Use **counts**, never percentages, in the table.
- Each **expected** count should be at least about 5. With smaller counts, combine categories, or use **Fisher's exact test** for 2 × 2 tables (`stats.fisher_exact`).
- Each row of data should be counted in exactly one cell (independent observations).

:::exercise Fair coin?
A coin is flipped 200 times and lands heads 116 times. Run a chi-square goodness-of-fit test against a fair coin (expected 100 heads and 100 tails) and store the p-value in `p_coin`. Set `fair_looking` to `True` if p ≥ 0.05, otherwise `False`.
```python starter
from scipy import stats

```
```python check
from scipy import stats
p = stats.chisquare([116, 84], [100, 100]).pvalue
same(float(need("p_coin")), float(p), "p_coin")
same(need("fair_looking"), bool(p >= 0.05), "fair_looking")
```
```python solution
from scipy import stats

p_coin = stats.chisquare([116, 84], [100, 100]).pvalue
fair_looking = bool(p_coin >= 0.05)
print(round(p_coin, 4), fair_looking)
```
hint: Observed `[116, 84]`, expected `[100, 100]`.
:::

:::exercise Segment by city
Load `customers.csv`, build the two-way table of `city` by `segment` with `pd.crosstab`, and run `stats.chi2_contingency`. Store the p-value in `p_city_seg` and the degrees of freedom in `dof`.
```python starter
import pandas as pd
from scipy import stats

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
from scipy import stats
c = pd.read_csv("customers.csv")
r = stats.chi2_contingency(pd.crosstab(c["city"], c["segment"]))
same(float(need("p_city_seg")), float(r.pvalue), "p_city_seg")
same(int(need("dof")), int(r.dof), "dof")
```
```python solution
import pandas as pd
from scipy import stats

customers = pd.read_csv("customers.csv")
table = pd.crosstab(customers["city"], customers["segment"])
res = stats.chi2_contingency(table)
p_city_seg = res.pvalue
dof = res.dof
print(round(p_city_seg, 3), dof)
```
hint: `res = stats.chi2_contingency(table)`, then `res.pvalue` and `res.dof`.
:::

:::quiz
? Which question needs a chi-square test rather than a t-test?
+ Is product preference related to the customer's region?
- Is the average order value different between two regions?
- Did scores improve after training?
= Two categorical variables call for a chi-square test of independence.
? What goes into `chi2_contingency`?
- Percentages
+ A table of counts
- Raw text values
= Chi-square tests work on counts; percentages give wrong results.
? An expected count in your table is 2. What should you do?
- Nothing
+ Combine categories, or use Fisher's exact test for a 2 × 2 table
- Multiply the counts by 10
= The chi-square approximation needs expected counts of about 5 or more.
:::

@@@ lesson
id: anova
title: Comparing several groups with ANOVA
minutes: 16
summary: Test whether three or more group means differ with one-way ANOVA, follow up with Tukey's test, and use Kruskal-Wallis when data isn't normal.
---
With three or more groups, running a t-test for every pair inflates false alarms (the multiple-testing trap). **One-way ANOVA** (analysis of variance) tests all the groups at once:

- **H₀:** all the group means are equal.
- **H₁:** at least one group mean is different.

Despite its name, ANOVA compares **means**. It does it by comparing two kinds of variation:

- **between groups:** how far the group means are from the overall mean;
- **within groups:** how spread out the values are inside each group.

Their ratio is the **F statistic**. If the groups are further apart than the noise inside them would explain, F is large and p is small.

![Box plots of math scores for classes A, B and C with the individual scores scattered on top and a dashed line at the overall mean; the boxes overlap a lot](figures/anova-classes.svg)

### One-way ANOVA with SciPy

Do the three classes differ in math?

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
groups = [students.loc[students["class"] == c, "math"] for c in ["A", "B", "C"]]
print(students.groupby("class")["math"].agg(["mean", "std", "count"]).round(1))
res = stats.f_oneway(*groups)
print(f"F = {res.statistic:.2f}, p = {res.pvalue:.3f}")
```

`*groups` passes the list's items as separate arguments. p is well above 0.05: the differences between classes are small compared with the spread inside each class, so there's no evidence the classes differ. The picture agrees: the boxes overlap heavily.

### A case where groups do differ

House prices across the three neighbourhoods:

```python
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
print(housing.groupby("neighborhood")["price_k"].agg(["mean", "count"]).round(1))
groups = [g["price_k"] for _, g in housing.groupby("neighborhood")]
res = stats.f_oneway(*groups)
print(f"F = {res.statistic:.1f}, p = {res.pvalue:.2e}")
```

`2e-10`-style numbers are scientific notation: 2 × 10⁻¹⁰, a tiny p-value.

### Which groups differ? Tukey's test

ANOVA only says "at least one differs". **Tukey's HSD** (honestly significant difference) test then compares every pair while keeping the overall false-alarm rate at 5%:

```python
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
names = ["Central", "Hillside", "Riverside"]
groups = [housing.loc[housing["neighborhood"] == n, "price_k"] for n in names]
res = stats.tukey_hsd(*groups)
for i in range(3):
    for j in range(i + 1, 3):
        print(f"{names[i]} vs {names[j]}: difference {groups[i].mean() - groups[j].mean():6.1f}, p = {res.pvalue[i, j]:.4f}")
```

### Assumptions and the alternative

ANOVA assumes independent observations, roughly normal data within each group (or decent group sizes), and similar spreads. When the data is clearly skewed or has outliers, the **Kruskal-Wallis** test compares groups using ranks instead:

```python
import pandas as pd
from scipy import stats

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
groups = [g["revenue"] for _, g in sales.groupby("region")]
print("Kruskal-Wallis p:", round(stats.kruskal(*groups).pvalue, 3))
```

### Effect size: eta squared

**Eta squared** (η²) is the share of the total variation explained by the groups, from 0 to 1:

```python
import pandas as pd

housing = pd.read_csv("housing.csv")
overall = housing["price_k"].mean()
between = housing.groupby("neighborhood")["price_k"].apply(lambda g: len(g) * (g.mean() - overall) ** 2).sum()
total = ((housing["price_k"] - overall) ** 2).sum()
print("eta squared:", round(between / total, 2))
```

Neighbourhood alone explains this share of the variation in prices; the rest comes from size, age and everything else (that's what regression handles, in Part 5).

:::exercise English by class
Load `students.csv` and run a one-way ANOVA on `english` scores across the three classes A, B and C. Store the F statistic in `f_stat` and the p-value in `p_eng`.
```python starter
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
from scipy import stats
s = pd.read_csv("students.csv")
r = stats.f_oneway(*[s.loc[s["class"] == c, "english"] for c in "ABC"])
same(float(need("f_stat")), float(r.statistic), "f_stat")
same(float(need("p_eng")), float(r.pvalue), "p_eng")
```
```python solution
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
groups = [students.loc[students["class"] == c, "english"] for c in ["A", "B", "C"]]
res = stats.f_oneway(*groups)
f_stat, p_eng = res.statistic, res.pvalue
print(round(f_stat, 2), round(p_eng, 3))
```
hint: Build a list of three Series (one per class), then `stats.f_oneway(*groups)`.
:::

:::exercise Rain across cities
Load `weather.csv`. Daily rain is very skewed (most days are dry), so compare `rain_mm` across the three cities with the **Kruskal-Wallis** test. Store the p-value in `p_rain`.
```python starter
import pandas as pd
from scipy import stats

weather = pd.read_csv("weather.csv")

```
```python check
import pandas as pd
from scipy import stats
w = pd.read_csv("weather.csv")
p = stats.kruskal(*[g["rain_mm"] for _, g in w.groupby("city")]).pvalue
same(float(need("p_rain")), float(p), "p_rain")
```
```python solution
import pandas as pd
from scipy import stats

weather = pd.read_csv("weather.csv")
groups = [g["rain_mm"] for _, g in weather.groupby("city")]
p_rain = stats.kruskal(*groups).pvalue
print(p_rain)
```
hint: `[g["rain_mm"] for _, g in weather.groupby("city")]` gives one Series per city.
:::

:::quiz
? Why use ANOVA instead of three t-tests for three groups?
+ Several t-tests inflate the chance of a false alarm
- t-tests can't compare means
- ANOVA needs less data
= One test at α = 0.05 keeps the overall false-alarm rate at 5%.
? ANOVA gives p = 0.001. What do you know?
- All three groups differ from each other
+ At least one group mean differs; a follow-up test like Tukey's says which
- The first group is the largest
= ANOVA is an overall test; post-hoc tests identify the pairs.
? When would you choose Kruskal-Wallis over ANOVA?
- When there are only two groups
+ When the data is strongly skewed or has outliers
- When the groups have equal means
= Kruskal-Wallis uses ranks, so it doesn't assume normal data.
:::
