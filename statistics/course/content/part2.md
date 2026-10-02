@@@ part
id: 2
title: Probability
level: Beginner
blurb: The language of chance: probability rules, conditional probability and Bayes, and the distributions that describe counts and measurements, including the bell curve.

@@@ lesson
id: probability-basics
title: Probability basics
minutes: 18
summary: What a probability is, the addition, complement and multiplication rules, independence, and checking answers by simulation.
---
A **probability** is a number from 0 to 1 that says how likely something is: 0 means impossible, 1 means certain, 0.5 means "as likely as not". Percentages are the same idea times 100.

When every outcome is equally likely, a probability is a fraction:

P(event) = (number of ways it can happen) / (number of possible outcomes)

A fair dice has 6 outcomes, so P(rolling a 5) = 1/6, and P(an even number) = 3/6 = 0.5.

### Probability as a long-run share

The other way to see a probability is "the share of times it happens if you repeat it many, many times". That's how you estimate probabilities from data, and how simulations check them:

```python
import numpy as np

rng = np.random.default_rng(1)
rolls = rng.integers(1, 7, size=100_000)
print("P(5) is about   ", round((rolls == 5).mean(), 4), " exact:", round(1 / 6, 4))
print("P(even) is about", round((rolls % 2 == 0).mean(), 4), " exact: 0.5")
```

![Three running proportions of heads that wander at first, then settle on 0.5 as the number of flips grows](figures/law-of-large-numbers.svg)

With a few flips, the share of heads jumps around. With thousands, it settles on the true probability. This is the **law of large numbers**, and it's why big samples give reliable estimates.

### The basic rules

| Rule | Formula | Example (one dice) |
|---|---|---|
| **Complement**: "not A" | P(not A) = 1 − P(A) | P(not a 6) = 1 − 1/6 = 5/6 |
| **Addition**: "A or B" | P(A or B) = P(A) + P(B) − P(A and B) | P(even or > 4) = 3/6 + 2/6 − 1/6 = 4/6 |
| **Multiplication** (independent): "A and B" | P(A and B) = P(A) × P(B) | P(two 6s in two rolls) = 1/6 × 1/6 = 1/36 |

The addition rule subtracts P(A and B) because outcomes in both groups would otherwise be counted twice (6 is both even and > 4).

### Independence

Two events are **independent** when one happening doesn't change the chance of the other: two dice rolls, two coin flips. Then you multiply their probabilities. Many real events are **not** independent (rain today and rain tomorrow), and multiplying their probabilities gives badly wrong answers.

The complement rule plus independence answers "at least one" questions neatly. What's the chance of at least one 6 in four rolls?

```python
import numpy as np

exact = 1 - (5 / 6) ** 4        # 1 - P(no 6 in four rolls)
rng = np.random.default_rng(2)
rolls = rng.integers(1, 7, size=(100_000, 4))
simulated = (rolls == 6).any(axis=1).mean()
print(round(exact, 4), round(simulated, 4))
```

"At least one" is almost always easiest as **1 − P(none)**.

### Probabilities from data

With real data, a probability is the share of rows where something happens:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
p_london = (customers["city"] == "London").mean()
p_business = (customers["segment"] == "Business").mean()
p_both = ((customers["city"] == "London") & (customers["segment"] == "Business")).mean()
print(f"P(London) = {p_london:.3f}")
print(f"P(Business) = {p_business:.3f}")
print(f"P(London and Business) = {p_both:.3f}")
print(f"if independent we'd expect {p_london * p_business:.3f}")
```

If the observed P(both) is close to P(A) × P(B), the two look independent. Part 4 shows how to test that properly.

### Counting outcomes

When outcomes are equally likely you often need to count them. Python's `math` module has the two classic counts:

```python
import math

print(math.perm(5, 3))   # ways to arrange 3 of 5 people in order (1st, 2nd, 3rd)
print(math.comb(5, 3))   # ways to choose a team of 3 from 5 (order doesn't matter)
print(1 / math.comb(49, 6))   # chance of winning a 6-from-49 lottery
```

:::exercise At least one double six
Two dice are rolled 24 times. Store the exact probability of getting **at least one** double six in `exact` (hint: P(double six) = 1/36 for one roll of two dice). Then estimate it by simulation: make `rng = np.random.default_rng(7)`, roll `rng.integers(1, 7, size=(100_000, 24, 2))`, and store the share of games with at least one double six in `simulated`.
```python starter
import numpy as np

```
```python check
import numpy as np
same(float(need("exact")), 1 - (35 / 36) ** 24, "exact")
rng = np.random.default_rng(7)
r = rng.integers(1, 7, size=(100_000, 24, 2))
sim = ((r == 6).all(axis=2)).any(axis=1).mean()
same(float(need("simulated")), float(sim), "simulated", tol=1e-9)
```
```python solution
import numpy as np

exact = 1 - (35 / 36) ** 24

rng = np.random.default_rng(7)
rolls = rng.integers(1, 7, size=(100_000, 24, 2))
double_six = (rolls == 6).all(axis=2)        # True where both dice show 6
simulated = double_six.any(axis=1).mean()    # at least one in each game of 24
print(round(exact, 4), round(simulated, 4))
```
hint: Exact: `1 - (35/36) ** 24`. Simulated: `(rolls == 6).all(axis=2)` marks double sixes; `.any(axis=1)` asks "at least one per game"; `.mean()` gives the share.
:::

:::exercise Probabilities from the A/B data
Load `ab_test.csv`. Store P(a visitor is on mobile) in `p_mobile`, P(a visitor converted) in `p_conv`, and P(mobile **and** converted) in `p_both`.
```python starter
import pandas as pd

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
a = pd.read_csv("ab_test.csv")
same(float(need("p_mobile")), float((a["device"] == "mobile").mean()), "p_mobile")
same(float(need("p_conv")), float(a["converted"].mean()), "p_conv")
same(float(need("p_both")), float(((a["device"] == "mobile") & (a["converted"] == 1)).mean()), "p_both")
```
```python solution
import pandas as pd

ab = pd.read_csv("ab_test.csv")
p_mobile = (ab["device"] == "mobile").mean()
p_conv = ab["converted"].mean()
p_both = ((ab["device"] == "mobile") & (ab["converted"] == 1)).mean()
print(p_mobile, p_conv, p_both)
```
hint: The mean of a True/False condition is its probability. Combine conditions with `&`.
:::

:::quiz
? P(rain) = 0.3. What is P(no rain)?
- 0.3
+ 0.7
- 1.3
= The complement rule: 1 − 0.3.
? Two fair coins are flipped. What is P(both heads)?
+ 0.25
- 0.5
- 1
= Independent events multiply: 0.5 × 0.5.
? What does the law of large numbers say?
- Big numbers are more likely
+ With more repetitions, the observed share gets closer to the true probability
- After many tails, heads becomes more likely
= The long-run share converges. It does not mean a coin "makes up" for past results.
:::

@@@ lesson
id: conditional-probability
title: Conditional probability and Bayes
minutes: 18
summary: Probabilities that depend on what you already know, why P(A given B) isn't P(B given A), and Bayes' rule with a medical-test example.
---
A **conditional probability** is a probability **given** that you know something else. It's written P(A | B), read "the probability of A given B":

P(A | B) = P(A and B) / P(B)

In words: among the cases where B happened, what share also had A? With data, that's just filtering first and then taking a share:

```python
import pandas as pd

ab = pd.read_csv("ab_test.csv")
p_conv = ab["converted"].mean()
p_conv_given_desktop = ab.loc[ab["device"] == "desktop", "converted"].mean()
p_conv_given_mobile = ab.loc[ab["device"] == "mobile", "converted"].mean()
print(f"P(convert)           = {p_conv:.3f}")
print(f"P(convert | desktop) = {p_conv_given_desktop:.3f}")
print(f"P(convert | mobile)  = {p_conv_given_mobile:.3f}")
```

Knowing the device changes the probability, so device and converting are **not independent**. Independence means exactly this: P(A | B) = P(A).

### Order matters: P(A | B) is not P(B | A)

P(a visitor is on mobile | they converted) and P(they converted | they're on mobile) answer different questions and have different values:

```python
import pandas as pd

ab = pd.read_csv("ab_test.csv")
mobile = ab["device"] == "mobile"
conv = ab["converted"] == 1
print("P(mobile | converted) =", round((mobile & conv).sum() / conv.sum(), 3))
print("P(converted | mobile) =", round((mobile & conv).sum() / mobile.sum(), 3))
```

Mixing the two up is one of the most common reasoning errors in news, courts and medicine.

### Bayes' rule: flipping the condition

**Bayes' rule** turns one conditional probability into the other:

P(A | B) = P(B | A) × P(A) / P(B)

The classic example is a medical test. A disease affects 1% of people. The test catches 90% of sick people (P(positive | sick) = 0.9) but also flags 5% of healthy people (a **false positive**). You test positive. What's the chance you're sick?

![A rectangle of 10,000 people: a thin red strip of 100 sick people (90 test positive) above a large grey area of 9,900 healthy people, of whom 495 test positive](figures/medical-test.svg)

Most people guess 90%. The answer is about 15%. Counting with 10,000 imaginary people makes it obvious:

```python
people = 10_000
sick = people * 0.01                 # 100
healthy = people - sick              # 9,900
true_pos = sick * 0.90               # 90 sick people test positive
false_pos = healthy * 0.05           # 495 healthy people test positive anyway
print("P(sick | positive) =", round(true_pos / (true_pos + false_pos), 3))
```

There are so many more healthy people that their 5% of false alarms outnumber the real cases. The starting probability (here 1%) is called the **prior** or **base rate**, and ignoring it is the **base rate fallacy**.

The same calculation with the formula:

```python
p_sick = 0.01
p_pos_given_sick = 0.90
p_pos_given_healthy = 0.05

p_pos = p_pos_given_sick * p_sick + p_pos_given_healthy * (1 - p_sick)   # all ways to test positive
p_sick_given_pos = p_pos_given_sick * p_sick / p_pos
print(round(p_sick_given_pos, 3))
```

### Why this matters for AI

A spam filter, a fraud detector or a medical AI has exactly this problem: when the thing you're looking for is rare, even an accurate model raises many false alarms. That's why machine-learning teams look at **precision** (of the cases flagged, how many are real) and not just accuracy. And Bayes' rule is the basis of a whole family of models (naive Bayes) and of Bayesian statistics.

:::exercise Conversion given group
Load `ab_test.csv`. Store P(converted | group A) in `p_a` and P(converted | group B) in `p_b`. Then store P(group B | converted), the share of buyers who saw page B, in `p_b_given_conv`.
```python starter
import pandas as pd

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
a = pd.read_csv("ab_test.csv")
same(float(need("p_a")), float(a.loc[a["group"] == "A", "converted"].mean()), "p_a")
same(float(need("p_b")), float(a.loc[a["group"] == "B", "converted"].mean()), "p_b")
same(float(need("p_b_given_conv")), float((a.loc[a["converted"] == 1, "group"] == "B").mean()), "p_b_given_conv")
```
```python solution
import pandas as pd

ab = pd.read_csv("ab_test.csv")
p_a = ab.loc[ab["group"] == "A", "converted"].mean()
p_b = ab.loc[ab["group"] == "B", "converted"].mean()
buyers = ab[ab["converted"] == 1]
p_b_given_conv = (buyers["group"] == "B").mean()
print(p_a, p_b, p_b_given_conv)
```
hint: "Given X" means filter to X first. For the last one, filter to buyers, then take the share in group B.
:::

:::exercise Fraud alarms
1 in 500 transactions is fraud. A fraud model flags 95% of frauds, and wrongly flags 2% of honest transactions. Store P(fraud | flagged) in `p_fraud_given_flag`.
```python starter
p_fraud = 1 / 500

```
```python check
pf = 1 / 500
pp = 0.95 * pf + 0.02 * (1 - pf)
same(float(need("p_fraud_given_flag")), 0.95 * pf / pp, "p_fraud_given_flag")
```
```python solution
p_fraud = 1 / 500
p_flag_given_fraud = 0.95
p_flag_given_honest = 0.02

p_flag = p_flag_given_fraud * p_fraud + p_flag_given_honest * (1 - p_fraud)
p_fraud_given_flag = p_flag_given_fraud * p_fraud / p_flag
print(round(p_fraud_given_flag, 3))
```
hint: First P(flagged) = 0.95 × P(fraud) + 0.02 × P(honest). Then Bayes: 0.95 × P(fraud) / P(flagged).
:::

:::quiz
? How do you compute P(converted | mobile) from data?
+ Keep only mobile visitors, then take the share who converted
- Take the share of converters who are on mobile
- Multiply P(converted) by P(mobile)
= "Given mobile" means you restrict to mobile visitors first.
? A rare disease, an accurate test, a positive result. Why might the chance of being sick still be low?
- The test is broken
+ Healthy people vastly outnumber sick ones, so their false positives outnumber the true positives
- Probabilities don't apply to medicine
= The base rate matters: a small error rate on a huge group swamps a rare condition.
? Events A and B are independent when:
- P(A and B) = 0
+ P(A | B) = P(A)
- P(A) = P(B)
= Knowing B happened doesn't change the probability of A.
:::

@@@ lesson
id: discrete-distributions
title: Counting distributions: binomial and Poisson
minutes: 18
summary: Random variables, expected value, the binomial distribution for "how many successes", and Poisson for "how many events".
---
A **random variable** is a number that comes out of a random process: the number of heads in 10 flips, the number of customers in the next hour, tomorrow's temperature. Its **distribution** lists every possible value and how likely each one is.

**Discrete** random variables take countable values (0, 1, 2…); **continuous** ones can take any value in a range (next lesson).

### Expected value

The **expected value** (or mean) of a random variable is the long-run average: each value times its probability, added up. A fair dice:

```python
import numpy as np

values = np.array([1, 2, 3, 4, 5, 6])
probs = np.full(6, 1 / 6)
print("expected value:", (values * probs).sum())

rng = np.random.default_rng(0)
print("average of 100,000 rolls:", rng.integers(1, 7, 100_000).mean().round(3))
```

You never roll 3.5, but over many rolls that's the average. Expected values decide whether a bet, insurance policy or marketing campaign pays off on average.

### The binomial distribution

The **binomial** distribution counts **successes in a fixed number of independent tries**, each with the same chance of success:

- n = the number of tries;
- p = the chance of success on each try.

Examples: heads in 10 flips (n = 10, p = 0.5); how many of 200 visitors buy (n = 200, p = 0.1); how many of 20 parts are faulty.

![Two bar charts of binomial probabilities for 10 tries: symmetric around 5 when p = 0.5, piled up near 2 when p = 0.2](figures/binomial.svg)

SciPy's `stats.binom` gives the probabilities:

```python
from scipy import stats

print("P(exactly 5 heads in 10)   =", round(stats.binom.pmf(5, 10, 0.5), 4))
print("P(at most 2 heads in 10)   =", round(stats.binom.cdf(2, 10, 0.5), 4))
print("P(more than 7 heads in 10) =", round(stats.binom.sf(7, 10, 0.5), 4))
print("expected heads:", stats.binom.mean(10, 0.5), " std:", round(stats.binom.std(10, 0.5), 3))
```

| Method | Gives | Read it as |
|---|---|---|
| `pmf(k, n, p)` | P(X = k) | exactly k |
| `cdf(k, n, p)` | P(X ≤ k) | at most k |
| `sf(k, n, p)` | P(X > k) = 1 − cdf | more than k |

The expected number of successes is n × p, and the standard deviation is √(n × p × (1 − p)).

### A practical binomial question

A page converts 10% of visitors. Tomorrow 200 people visit. How surprising would 30 or more sales be?

```python
from scipy import stats

n, p = 200, 0.10
print("expected sales:", n * p)
print("P(30 or more) =", round(stats.binom.sf(29, n, p), 4))   # sf(29) = P(X > 29) = P(X >= 30)
```

Under 2%. If it happened, you'd suspect something had changed. That's the idea behind hypothesis testing in Part 4.

### The Poisson distribution

The **Poisson** distribution counts **events in a fixed amount of time or space** when they happen independently at a steady average rate: customers per hour, website errors per day, typos per page. It has one number, the average rate λ (lambda):

![Bar chart of Poisson probabilities with an average of 4: highest at 3 and 4, falling away to almost nothing by 12](figures/poisson.svg)

```python
from scipy import stats

rate = 4          # on average 4 customers arrive per hour
print("P(exactly 4) =", round(stats.poisson.pmf(4, rate), 4))
print("P(0)         =", round(stats.poisson.pmf(0, rate), 4))
print("P(8 or more) =", round(stats.poisson.sf(7, rate), 4))
```

For a Poisson distribution the mean and the variance both equal λ.

### Drawing random values

Every SciPy distribution can also **generate** values with `.rvs()`, which is how you simulate:

```python
from scipy import stats

sim = stats.binom.rvs(10, 0.5, size=10_000, random_state=1)
print("simulated share of exactly 5 heads:", (sim == 5).mean())
```

:::exercise Defective parts
A machine makes parts with a 3% defect rate. A box holds 50 parts. Using `scipy.stats.binom`, store P(no defects in a box) in `p_none`, P(at most 2 defects) in `p_at_most_2`, and the expected number of defects in `expected`.
```python starter
from scipy import stats

```
```python check
from scipy import stats
same(float(need("p_none")), float(stats.binom.pmf(0, 50, 0.03)), "p_none")
same(float(need("p_at_most_2")), float(stats.binom.cdf(2, 50, 0.03)), "p_at_most_2")
same(float(need("expected")), 1.5, "expected")
```
```python solution
from scipy import stats

n, p = 50, 0.03
p_none = stats.binom.pmf(0, n, p)
p_at_most_2 = stats.binom.cdf(2, n, p)
expected = n * p
print(p_none, p_at_most_2, expected)
```
hint: Exactly 0 is `pmf(0, 50, 0.03)`; at most 2 is `cdf(2, 50, 0.03)`; expected is n × p.
:::

:::exercise Support tickets
A help desk gets 6 tickets an hour on average. Using `scipy.stats.poisson`, store P(more than 10 tickets in an hour) in `p_busy`, and P(fewer than 3) in `p_quiet`.
```python starter
from scipy import stats

```
```python check
from scipy import stats
same(float(need("p_busy")), float(stats.poisson.sf(10, 6)), "p_busy")
same(float(need("p_quiet")), float(stats.poisson.cdf(2, 6)), "p_quiet")
```
```python solution
from scipy import stats

p_busy = stats.poisson.sf(10, 6)      # P(X > 10)
p_quiet = stats.poisson.cdf(2, 6)     # P(X <= 2), i.e. fewer than 3
print(round(p_busy, 4), round(p_quiet, 4))
```
hint: "More than 10" is `sf(10, 6)`. "Fewer than 3" means at most 2: `cdf(2, 6)`.
:::

:::quiz
? Which situation fits a binomial distribution?
+ The number of buyers among 500 visitors, each buying with probability 0.08
- The time until the next bus
- People's heights
= A fixed number of independent tries, each with the same success probability.
? What does `stats.binom.cdf(3, 10, 0.5)` give?
- P(exactly 3)
+ P(3 or fewer)
- P(more than 3)
= cdf is cumulative: the probability of k or less.
? A Poisson distribution has λ = 5. What's its mean?
+ 5
- 2.5
- √5
= For Poisson, the mean (and the variance) equal λ.
:::

@@@ lesson
id: normal-distribution
title: The normal distribution
minutes: 20
summary: The bell curve, the 68-95-99.7 rule, areas with norm.cdf, percentiles with norm.ppf, and checking whether data is normal.
---
The **normal distribution** is the bell curve. Measurements that are the sum of many small, independent influences tend to follow it: heights, measurement errors, test scores, and (as you'll see in Part 3) **averages of samples**. It's described by two numbers: the mean μ (mu), which sets the centre, and the standard deviation σ (sigma), which sets the width.

![A bell curve with the middle shaded: 68% of values within 1 standard deviation of the mean, 95% within 2, 99.7% within 3](figures/normal-68-95.svg)

### The 68-95-99.7 rule

For any normal distribution:

- about **68%** of values are within 1 standard deviation of the mean;
- about **95%** are within 2;
- about **99.7%** are within 3.

So if adult heights are normal with mean 170 cm and std 8 cm, 95% of adults are between 154 and 186 cm, and someone over 194 cm (3 std above) is rare: about 1 in 740.

Let's check the rule by simulation:

```python
import numpy as np

rng = np.random.default_rng(3)
heights = rng.normal(170, 8, 100_000)
for k in (1, 2, 3):
    inside = ((heights > 170 - k * 8) & (heights < 170 + k * 8)).mean()
    print(f"within {k} std: {inside:.3f}")
```

### Continuous probabilities are areas

For continuous variables, the probability of any exact value (exactly 170.000… cm) is zero. Probabilities are **areas under the curve** between two values. SciPy's `stats.norm` calculates them:

![A bell curve with the area to the left of 180 cm shaded, labelled P(height ≤ 180) = norm.cdf(180, 170, 8) = 0.894](figures/normal-cdf.svg)

```python
from scipy import stats

mu, sigma = 170, 8
print("P(height <= 180)        =", round(stats.norm.cdf(180, mu, sigma), 4))
print("P(height > 190)         =", round(stats.norm.sf(190, mu, sigma), 4))
print("P(160 < height < 180)   =", round(stats.norm.cdf(180, mu, sigma) - stats.norm.cdf(160, mu, sigma), 4))
```

| You want | Use |
|---|---|
| P(X ≤ x), the area to the left | `stats.norm.cdf(x, mu, sigma)` |
| P(X > x), the area to the right | `stats.norm.sf(x, mu, sigma)` |
| P(a < X < b) | `cdf(b) - cdf(a)` |
| the value with a given area to its left | `stats.norm.ppf(area, mu, sigma)` |

### Going backwards: percentiles with ppf

`ppf` (the percent point function) answers "what value is at the 90th percentile?". A door designer wants 99% of adults to fit under the frame:

```python
from scipy import stats

print("99th percentile height:", round(stats.norm.ppf(0.99, 170, 8), 1), "cm")
print("middle 95% runs from", round(stats.norm.ppf(0.025, 170, 8), 1), "to", round(stats.norm.ppf(0.975, 170, 8), 1))
print("z for the top 2.5%:", round(stats.norm.ppf(0.975), 2))
```

That last number, **1.96**, will appear again and again: 95% of a normal distribution lies within 1.96 standard deviations of the mean.

### The standard normal and z-scores

The **standard normal** distribution has mean 0 and std 1. Any normal value turns into a standard normal value by computing its z-score, (x − μ) / σ, so one table (or one SciPy call without `mu` and `sigma`) covers every normal distribution:

```python
from scipy import stats

z = (180 - 170) / 8
print("z =", z, "→ P =", round(stats.norm.cdf(z), 4))     # same as cdf(180, 170, 8)
```

### Is my data normal?

Many methods assume roughly normal data, so it's worth checking. Two quick ways: compare the histogram with a fitted bell curve, and run a **normality test**. The Shapiro-Wilk test gives a p-value (Part 4 explains them properly); a small value, below 0.05, suggests the data is not normal:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

students = pd.read_csv("students.csv")
math = students["math"]
x = np.linspace(math.min() - 10, math.max() + 10, 200)

fig, ax = plt.subplots(figsize=(6, 3.2))
ax.hist(math, bins=12, density=True, color="lightseagreen", edgecolor="white", label="math scores")
ax.plot(x, stats.norm.pdf(x, math.mean(), math.std()), color="darkorange", linewidth=2, label="normal curve")
ax.legend()
ax.set_title("Math scores vs a normal curve")
plt.show()

print("Shapiro-Wilk p-value (math):", round(stats.shapiro(math).pvalue, 3))
sales = pd.read_csv("sales.csv")
print("Shapiro-Wilk p-value (order units):", stats.shapiro(sales["units"]).pvalue)
```

`density=True` scales the histogram so its total area is 1, which lets the curve sit on top of it. Math scores look normal; order units clearly don't. With very large samples, normality tests flag even tiny, harmless departures, so always look at the picture too.

:::exercise IQ scores
IQ scores are normal with mean 100 and standard deviation 15. Store P(IQ > 130) in `p_gifted`, P(85 < IQ < 115) in `p_middle`, and the IQ at the 90th percentile in `iq_90`.
```python starter
from scipy import stats

```
```python check
from scipy import stats
same(float(need("p_gifted")), float(stats.norm.sf(130, 100, 15)), "p_gifted")
same(float(need("p_middle")), float(stats.norm.cdf(115, 100, 15) - stats.norm.cdf(85, 100, 15)), "p_middle")
same(float(need("iq_90")), float(stats.norm.ppf(0.9, 100, 15)), "iq_90")
```
```python solution
from scipy import stats

p_gifted = stats.norm.sf(130, 100, 15)
p_middle = stats.norm.cdf(115, 100, 15) - stats.norm.cdf(85, 100, 15)
iq_90 = stats.norm.ppf(0.90, 100, 15)
print(round(p_gifted, 4), round(p_middle, 4), round(iq_90, 1))
```
hint: Right tail: `sf`. Between: `cdf(b) - cdf(a)`. Percentile: `ppf(0.90, 100, 15)`.
:::

:::exercise Delivery promise
Delivery times are normal with mean 42 minutes and std 7. The shop wants to promise a time that 95% of deliveries beat. Store that time in `promise`, and the share of deliveries that take **longer than 55 minutes** in `late_share`.
```python starter
from scipy import stats

```
```python check
from scipy import stats
same(float(need("promise")), float(stats.norm.ppf(0.95, 42, 7)), "promise")
same(float(need("late_share")), float(stats.norm.sf(55, 42, 7)), "late_share")
```
```python solution
from scipy import stats

promise = stats.norm.ppf(0.95, 42, 7)
late_share = stats.norm.sf(55, 42, 7)
print(round(promise, 1), round(late_share, 4))
```
hint: "95% beat it" means 95% of the area is to its left: `ppf(0.95, 42, 7)`.
:::

:::quiz
? Heights are normal, mean 170, std 8. About what share are between 162 and 178?
+ 68%
- 95%
- 50%
= 162 to 178 is the mean ± 1 std, which holds about 68%.
? What does `stats.norm.ppf(0.975)` return?
- 0.975
+ About 1.96: the z with 97.5% of the area to its left
- The area to the right of 0.975
= ppf goes from an area back to a value. 1.96 marks the top 2.5%.
? Why is P(height = exactly 170 cm) zero for a continuous variable?
- Nobody is 170 cm
+ Probabilities are areas, and a single point has no width
- The normal distribution is wrong
= You can only ask about ranges, like 169.5 to 170.5.
:::
