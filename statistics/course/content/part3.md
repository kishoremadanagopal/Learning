@@@ part
id: 3
title: Sampling and Estimation
level: Intermediate
blurb: How samples behave, why averages become bell-shaped (the central limit theorem), and how to give an honest range for an estimate with confidence intervals and the bootstrap.

@@@ lesson
id: sampling-and-bias
title: Sampling and bias
minutes: 16
summary: Random, stratified and convenience samples, the kinds of bias that ruin them, and the standard error.
---
Everything in inferential statistics depends on one assumption: **the sample represents the population**. A huge sample that's collected badly is worse than a small one collected well.

### Ways to sample

| Method | How | Good because |
|---|---|---|
| **Simple random sample** | every member has the same chance of being picked | no systematic favouritism |
| **Stratified sample** | split into groups (strata), sample randomly within each | every group is represented in proportion |
| **Cluster sample** | randomly pick whole groups (schools, stores), use everyone in them | cheaper to collect |
| **Convenience sample** | whoever is easy to reach | ❌ usually biased |

pandas does random and stratified sampling in one line each:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
simple = customers.sample(n=30, random_state=1)
stratified = customers.groupby("segment").sample(frac=0.25, random_state=1)

print("population mix:\n", customers["segment"].value_counts(normalize=True).round(2))
print("simple random sample mix:\n", simple["segment"].value_counts(normalize=True).round(2))
print("stratified sample mix:\n", stratified["segment"].value_counts(normalize=True).round(2))
```

The stratified sample keeps the segment mix almost exactly; the simple random sample is close but wobbles.

### Bias: when the sample systematically misses

**Bias** means the method tends to miss in the same direction every time. More data doesn't fix it:

![Forty estimates from random samples cluster around the true average; forty estimates from biased samples all land well above it](figures/sampling-bias.svg)

Common sources:

- **Selection bias:** who gets into the sample isn't random (an online survey misses people who aren't online).
- **Non-response bias:** the people who answer differ from those who don't (only angry customers fill in the feedback form).
- **Survivorship bias:** you only see the survivors (studying only successful startups to find the "secrets of success").
- **Measurement bias:** the question or instrument pushes answers one way ("Don't you agree that…?").

Let's see selection bias in action. Suppose we only survey customers who signed up in the last year, and ask their age:

```python
import pandas as pd

customers = pd.read_csv("customers.csv", parse_dates=["signup_date"])
recent = customers[customers["signup_date"] >= "2025-01-01"]
print("true average age:   ", customers["age"].mean().round(1))
print("recent sign-ups only:", recent["age"].mean().round(1), f"({len(recent)} people)")
```

Whether the difference is big or small here, the point stands: unless the restricted group is like everyone else, its average answers a different question.

### Sampling variability and the standard error

Even with perfect random sampling, every sample gives a slightly different answer. That's **sampling variability**, and it's not a mistake: it's what statistics measures. Let's draw 1,000 random samples of 10 students and look at how their averages spread:

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
math = students["math"].to_numpy()
rng = np.random.default_rng(0)

for n in (5, 10, 30):
    means = [rng.choice(math, n, replace=False).mean() for _ in range(1000)]
    print(f"samples of {n:2}: averages vary with std {np.std(means):.2f}")
```

Bigger samples give averages that vary less. The standard deviation of a sample average has its own name, the **standard error** (SE), and a formula:

SE = s / √n

where s is the standard deviation of the data and n the sample size. To halve the standard error you need **four times** the data, because of the square root.

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
sample = students.sample(30, random_state=4)["math"]
se = sample.std() / np.sqrt(len(sample))
print("sample mean:", round(sample.mean(), 1), " standard error:", round(se, 2))
```

`scipy.stats.sem(x)` computes the same thing.

:::exercise A stratified sample
Load `customers.csv` and take a stratified sample of **20%** of each `city` with `groupby("city").sample(frac=0.2, random_state=3)`. Store it in `strat`, and store the **largest absolute difference** between the city shares in the sample and in the full data in `max_gap`.
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
s = c.groupby("city").sample(frac=0.2, random_state=3)
got = need("strat", pd.DataFrame)
assert len(got) == len(s), f"strat should have {len(s)} rows."
gap = (s["city"].value_counts(normalize=True) - c["city"].value_counts(normalize=True)).abs().max()
same(float(need("max_gap")), float(gap), "max_gap")
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
strat = customers.groupby("city").sample(frac=0.2, random_state=3)
diff = strat["city"].value_counts(normalize=True) - customers["city"].value_counts(normalize=True)
max_gap = diff.abs().max()
print(max_gap)
```
hint: Subtract the two `value_counts(normalize=True)` Series (they line up by city), take `.abs().max()`.
:::

:::exercise Standard error
Load `housing.csv`. Store the standard error of the mean of `price_k` in `se_price` (std / √n, using pandas `.std()`), and the standard error you'd get with **four times** as many homes (same std) in `se_4x`.
```python starter
import numpy as np
import pandas as pd

housing = pd.read_csv("housing.csv")

```
```python check
import numpy as np
import pandas as pd
p = pd.read_csv("housing.csv")["price_k"]
se = p.std() / np.sqrt(len(p))
same(float(need("se_price")), float(se), "se_price")
same(float(need("se_4x")), float(p.std() / np.sqrt(4 * len(p))), "se_4x")
```
```python solution
import numpy as np
import pandas as pd

housing = pd.read_csv("housing.csv")
price = housing["price_k"]
se_price = price.std() / np.sqrt(len(price))
se_4x = price.std() / np.sqrt(4 * len(price))
print(se_price, se_4x)      # four times the data halves the standard error
```
hint: `std / np.sqrt(n)`. With four times the data, n becomes `4 * n`.
:::

:::quiz
? A company surveys customers by email. Who is missed?
+ Customers who don't read or answer email, so the sample may be biased
- Nobody, email reaches everyone
- Only very young customers
= That's selection and non-response bias: the people who answer may differ from those who don't.
? Does collecting a much bigger biased sample fix bias?
- Yes
+ No, it just gives a more precise wrong answer
- Only if the sample is over 1,000
= Bias is a systematic error. More data shrinks the random wobble, not the bias.
? To halve the standard error of a mean, you need:
- Twice the data
+ Four times the data
- Half the data
= SE = s / √n, and √4 = 2.
:::

@@@ lesson
id: central-limit-theorem
title: The central limit theorem
minutes: 16
summary: Why averages of samples are bell-shaped even when the data isn't, and why that makes most of statistics work.
---
Here's the most important result in statistics. Take **any** population, however strange its shape. Draw many random samples of size n and work out each sample's average. If n is large enough, those averages:

1. form a **normal** (bell-shaped) distribution;
2. are centred on the **population mean**;
3. have a standard deviation of σ / √n: the **standard error**.

That's the **central limit theorem** (CLT).

![A strongly skewed population histogram, then histograms of averages of samples of 2, 10 and 40: each one narrower and more bell-shaped](figures/clt.svg)

The population on the left is very skewed: lots of small values, a long tail. Averages of 2 values are still skewed. Averages of 10 are nearly a bell. Averages of 40 are a narrow, almost perfect bell around the true mean.

### Watch it happen

Order revenue in `sales.csv` is very right-skewed. Let's treat the 600 orders as a population and look at averages of random samples:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
revenue = (sales["units"] * sales["unit_price"]).to_numpy()
rng = np.random.default_rng(1)

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].hist(revenue, bins=40, color="grey")
axes[0].set_title("orders (skewed)")
for ax, n in zip(axes[1:], (5, 50)):
    means = rng.choice(revenue, size=(4000, n)).mean(axis=1)
    ax.hist(means, bins=40, color="teal")
    ax.set_title(f"averages of {n} orders")
plt.show()

print("population mean:", revenue.mean().round(1))
```

### Check the formula

The CLT says the averages' standard deviation should be σ / √n. Let's compare:

```python
import numpy as np
import pandas as pd

sales = pd.read_csv("sales.csv")
revenue = (sales["units"] * sales["unit_price"]).to_numpy()
rng = np.random.default_rng(2)
n = 50
means = rng.choice(revenue, size=(10_000, n)).mean(axis=1)
print("mean of the averages:", means.mean().round(1), " population mean:", revenue.mean().round(1))
print("std of the averages: ", means.std().round(2), " formula σ/√n:", (revenue.std() / np.sqrt(n)).round(2))
```

They match. That means you can know how much a sample average wobbles **from a single sample**, without drawing thousands of them: use the sample's std in place of σ.

### Why it matters

Because sample averages are approximately normal, everything you learned about the normal curve applies to them:

- 95% of sample averages land within about 1.96 standard errors of the true mean. Turn that around and you get a **confidence interval** (next lesson).
- If an average lands far outside that range, something unusual is going on. That's a **hypothesis test** (Part 4).

### How large is "large enough"?

| Population shape | n needed for a good bell |
|---|---|
| already roughly normal | any n |
| mildly skewed | about 15 to 30 |
| strongly skewed or with outliers | 50 or more |

The CLT is about **averages** (and sums and proportions). It doesn't make the data itself normal, and it doesn't rescue a **biased** sample.

### Proportions are averages too

A proportion is the average of 0/1 values, so the CLT covers it. Its standard error is √(p(1 − p) / n):

```python
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
p = ab["converted"].mean()
n = len(ab)
print("conversion rate:", round(p, 4), " standard error:", round(np.sqrt(p * (1 - p) / n), 4))
```

:::exercise Simulate the CLT
Load `weather.csv` and take Mumbai's `rain_mm` (very skewed: most days are dry). With `rng = np.random.default_rng(5)`, draw **5,000** samples of **30** days with replacement (`rng.choice(rain, size=(5000, 30))`) and store the 5,000 sample averages in `means`. Store `means.std()` in `sim_se` and the formula value, `rain.std(ddof=0) / np.sqrt(30)`, in `formula_se`.
```python starter
import numpy as np
import pandas as pd

weather = pd.read_csv("weather.csv")
rain = weather.loc[weather["city"] == "Mumbai", "rain_mm"].to_numpy()

```
```python check
import numpy as np
import pandas as pd
w = pd.read_csv("weather.csv")
r = w.loc[w["city"] == "Mumbai", "rain_mm"].to_numpy()
rng = np.random.default_rng(5)
m = rng.choice(r, size=(5000, 30)).mean(axis=1)
same(need("means", np.ndarray), m, "means")
same(float(need("sim_se")), float(m.std()), "sim_se")
same(float(need("formula_se")), float(r.std() / np.sqrt(30)), "formula_se")
```
```python solution
import numpy as np
import pandas as pd

weather = pd.read_csv("weather.csv")
rain = weather.loc[weather["city"] == "Mumbai", "rain_mm"].to_numpy()

rng = np.random.default_rng(5)
means = rng.choice(rain, size=(5000, 30)).mean(axis=1)
sim_se = means.std()
formula_se = rain.std(ddof=0) / np.sqrt(30)
print(round(sim_se, 3), round(formula_se, 3))
```
hint: `rng.choice(rain, size=(5000, 30))` makes a 5000 × 30 array; `.mean(axis=1)` averages each row.
:::

:::exercise Standard error of a proportion
Load `ab_test.csv` and keep group B. Store its conversion rate in `p_b` and the standard error of that rate, √(p(1 − p) / n), in `se_b`.
```python starter
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")

```
```python check
import numpy as np
import pandas as pd
a = pd.read_csv("ab_test.csv")
b = a.loc[a["group"] == "B", "converted"]
p = b.mean()
same(float(need("p_b")), float(p), "p_b")
same(float(need("se_b")), float(np.sqrt(p * (1 - p) / len(b))), "se_b")
```
```python solution
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
b = ab.loc[ab["group"] == "B", "converted"]
p_b = b.mean()
se_b = np.sqrt(p_b * (1 - p_b) / len(b))
print(round(p_b, 4), round(se_b, 4))
```
hint: Filter group B's `converted` column; n is its length.
:::

:::quiz
? The central limit theorem says that, for large samples:
- The data becomes normal
+ The sample averages are approximately normal
- Every sample has the same average
= It's about the distribution of averages, not of the raw data.
? Averages of samples of 100 are more spread out than averages of samples of 25. True or false?
- True
+ False: bigger samples give averages that vary less
- It depends on the data's shape
= The spread of averages is σ / √n, which shrinks as n grows.
? Why does the CLT matter so much?
+ It lets us use the normal curve to measure uncertainty in averages and proportions
- It removes bias from samples
- It means we never need large samples
= Confidence intervals and many tests rest on it.
:::

@@@ lesson
id: confidence-intervals
title: Confidence intervals
minutes: 20
summary: Give a range instead of a single number: confidence intervals for a mean and for a proportion, what 95% really means, and what makes an interval narrow.
---
A single estimate ("the average is 56.6") hides how uncertain it is. A **confidence interval** gives a range of plausible values for the population number: "the average is between 52.8 and 60.4, with 95% confidence".

The recipe, straight from the central limit theorem:

**estimate ± (critical value) × (standard error)**

For a 95% interval the critical value is about 2 (1.96 for the normal distribution, a little more for small samples).

### A confidence interval for a mean

For means we use the **t distribution** instead of the normal. It's like the normal but with fatter tails, which accounts for the extra uncertainty of estimating the std from the sample itself:

![A normal curve and three t curves; with 2 degrees of freedom the t curve has much fatter tails, and with 30 it is almost identical to the normal](figures/t-vs-normal.svg)

The t distribution's shape depends on the **degrees of freedom**, n − 1 for a single mean. As n grows it becomes the normal distribution.

```python
import numpy as np
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
math = students["math"]
n = len(math)
mean = math.mean()
se = math.std() / np.sqrt(n)
t_crit = stats.t.ppf(0.975, df=n - 1)        # 2.5% in each tail

print(f"mean {mean:.1f}, SE {se:.2f}, t* {t_crit:.3f}")
print(f"95% CI: {mean - t_crit * se:.1f} to {mean + t_crit * se:.1f}")
```

SciPy does the same in one call:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
math = students["math"]
low, high = stats.t.interval(0.95, df=len(math) - 1, loc=math.mean(), scale=stats.sem(math))
print(round(low, 1), round(high, 1))
```

### What "95% confidence" really means

It's a statement about the **method**, not about one interval. If you repeated the study many times, about 95% of the intervals you built would contain the true value:

![Fifty horizontal intervals from fifty samples; all but one cross the dashed line at the true mean](figures/confidence-intervals.svg)

Any single interval either contains the true value or it doesn't; you just don't know which. So say "we're 95% confident the average is between 52.8 and 60.4", and avoid "there's a 95% probability the true average is in this interval" (strictly, that's a different, Bayesian statement).

Let's check the 95% by simulation, using a population where we know the truth:

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(10)
true_mean, hits = 50, 0
for _ in range(2000):
    sample = rng.normal(true_mean, 12, 25)
    low, high = stats.t.interval(0.95, 24, loc=sample.mean(), scale=stats.sem(sample))
    hits += low <= true_mean <= high
print("share of intervals containing the true mean:", hits / 2000)
```

### What makes an interval narrow?

| Change | Effect on the interval |
|---|---|
| bigger sample (n ↑) | narrower (SE = s / √n shrinks) |
| more spread in the data (s ↑) | wider |
| higher confidence (99% instead of 95%) | wider: to be surer, you need a bigger net |

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
math = students["math"]
for level in (0.90, 0.95, 0.99):
    low, high = stats.t.interval(level, len(math) - 1, loc=math.mean(), scale=stats.sem(math))
    print(f"{level:.0%}: {low:.1f} to {high:.1f}  (width {high - low:.1f})")
```

### A confidence interval for a proportion

For a proportion p from n yes/no values, the standard error is √(p(1 − p) / n), and the normal critical value 1.96 is used:

```python
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
a = ab.loc[ab["group"] == "A", "converted"]
p, n = a.mean(), len(a)
se = np.sqrt(p * (1 - p) / n)
print(f"page A converts {p:.1%}, 95% CI {p - 1.96 * se:.1%} to {p + 1.96 * se:.1%}")
```

This simple "plus or minus 1.96 SE" interval works well when there are at least about 10 successes and 10 failures. For tiny samples or rates near 0% or 100%, use the Wilson interval (`statsmodels.stats.proportion.proportion_confint(..., method="wilson")`).

This is the "margin of error" you see in polls: "52% support, ±3 points" is a 95% interval from about 1,000 people.

:::exercise Average home price
Load `housing.csv` and build a **95%** confidence interval for the mean `price_k` with `stats.t.interval`. Store the lower and upper ends in `low` and `high`.
```python starter
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from scipy import stats
p = pd.read_csv("housing.csv")["price_k"]
lo, hi = stats.t.interval(0.95, len(p) - 1, loc=p.mean(), scale=stats.sem(p))
same(float(need("low")), float(lo), "low")
same(float(need("high")), float(hi), "high")
```
```python solution
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
price = housing["price_k"]
low, high = stats.t.interval(0.95, df=len(price) - 1, loc=price.mean(), scale=stats.sem(price))
print(round(low, 1), round(high, 1))
```
hint: `stats.t.interval(0.95, df=n - 1, loc=mean, scale=stats.sem(price))`.
:::

:::exercise Margin of error
Load `ab_test.csv`, keep **mobile** visitors, and compute a 95% confidence interval for their conversion rate using p ± 1.96 × √(p(1 − p) / n). Store the rate in `p_mobile` and the margin of error (1.96 × SE) in `margin`.
```python starter
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")

```
```python check
import numpy as np
import pandas as pd
a = pd.read_csv("ab_test.csv")
m = a.loc[a["device"] == "mobile", "converted"]
p = m.mean()
same(float(need("p_mobile")), float(p), "p_mobile")
same(float(need("margin")), float(1.96 * np.sqrt(p * (1 - p) / len(m))), "margin")
```
```python solution
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
mobile = ab.loc[ab["device"] == "mobile", "converted"]
p_mobile = mobile.mean()
margin = 1.96 * np.sqrt(p_mobile * (1 - p_mobile) / len(mobile))
print(f"{p_mobile:.1%} ± {margin:.1%}")
```
hint: Filter mobile visitors' `converted` column, then `1.96 * np.sqrt(p * (1 - p) / n)`.
:::

:::quiz
? What does "95% confidence" mean?
+ The method captures the true value in about 95% of repeated samples
- 95% of the data is inside the interval
- The true value moves around inside the interval 95% of the time
= Confidence is about the long-run success rate of the method.
? You want a narrower interval without changing the confidence level. What helps?
- Using 99% confidence
+ Collecting a bigger sample
- Rounding the mean
= SE = s / √n, so more data narrows the interval.
? Why use the t distribution for a mean's interval?
- It's always narrower
+ It allows for the extra uncertainty of estimating the standard deviation from the sample
- The normal distribution can't be used for means
= With small samples the t's fatter tails give an honestly wider interval.
:::

@@@ lesson
id: bootstrap
title: The bootstrap
minutes: 16
summary: Estimate uncertainty for any statistic by resampling your own data, no formula needed.
---
The formulas in the last lesson work for means and proportions. But what about a confidence interval for a **median**, a 90th percentile, a ratio, or a correlation? The **bootstrap** handles all of them with one idea:

> Treat your sample as a stand-in for the population. Draw many new samples **from your sample, with replacement**, recompute the statistic each time, and see how much it varies.

"With replacement" means the same row can be picked more than once, so each resample is a slightly different version of your data, the same size as the original.

```python
import numpy as np

rng = np.random.default_rng(0)
data = np.array([3, 7, 8, 12, 15])
for _ in range(3):
    print(rng.choice(data, size=len(data), replace=True))
```

### A bootstrap confidence interval for the mean

1. resample the data with replacement, thousands of times;
2. compute the mean of each resample;
3. the middle 95% of those means (the 2.5th to 97.5th percentiles) is a 95% confidence interval.

![A bell-shaped histogram of 5,000 resampled average math scores, with orange lines marking the 95% interval from 52.9 to 60.3](figures/bootstrap.svg)

```python
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
math = students["math"].to_numpy()
rng = np.random.default_rng(1)

boot_means = np.array([rng.choice(math, size=len(math)).mean() for _ in range(5000)])
low, high = np.percentile(boot_means, [2.5, 97.5])
print(f"bootstrap 95% CI for the mean: {low:.1f} to {high:.1f}")
```

That's almost the same as the t-interval (52.8 to 60.4), which is reassuring: for a mean, both methods agree.

### The real power: any statistic

The median of order revenue has no simple standard-error formula. The bootstrap doesn't care:

```python
import numpy as np
import pandas as pd

sales = pd.read_csv("sales.csv")
revenue = (sales["units"] * sales["unit_price"]).to_numpy()
rng = np.random.default_rng(2)

boot_medians = np.array([np.median(rng.choice(revenue, size=len(revenue))) for _ in range(3000)])
low, high = np.percentile(boot_medians, [2.5, 97.5])
print(f"median order: {np.median(revenue):.1f}, 95% CI {low:.1f} to {high:.1f}")
```

### SciPy's bootstrap

`scipy.stats.bootstrap` does the resampling for you, with a more accurate interval method (BCa) by default. Data goes in as a tuple:

```python
import numpy as np
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
res = stats.bootstrap((housing["price_k"].to_numpy(),), np.median, n_resamples=2000, random_state=3)
ci = res.confidence_interval
print(f"95% CI for the median price: {ci.low:.1f} to {ci.high:.1f}")
```

### Bootstrapping a difference

The bootstrap also gives an interval for a **difference between two groups**: resample each group separately, take the difference each time.

```python
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
a = ab.loc[ab["group"] == "A", "converted"].to_numpy()
b = ab.loc[ab["group"] == "B", "converted"].to_numpy()
rng = np.random.default_rng(4)

diffs = np.array([rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(3000)])
low, high = np.percentile(diffs, [2.5, 97.5])
print(f"B - A: {b.mean() - a.mean():.2%}, 95% CI {low:.2%} to {high:.2%}")
```

The whole interval is above zero, so page B's advantage is very unlikely to be just luck. You'll test that formally in Part 6.

### Limits

- The bootstrap can only reflect the data you have. A small or biased sample gives a misleading bootstrap too.
- It struggles with extreme statistics (the maximum, the 99.9th percentile) and with very small samples (below about 15).

:::exercise Bootstrap a median
Load `housing.csv`. With `rng = np.random.default_rng(8)`, make **2,000** bootstrap resamples of `price_k` (each the same size as the data, with replacement), store the 2,000 medians in `boot_medians`, and the 95% percentile interval in `low` and `high`.
```python starter
import numpy as np
import pandas as pd

housing = pd.read_csv("housing.csv")
price = housing["price_k"].to_numpy()
rng = np.random.default_rng(8)

```
```python check
import numpy as np
import pandas as pd
p = pd.read_csv("housing.csv")["price_k"].to_numpy()
rng = np.random.default_rng(8)
m = np.array([np.median(rng.choice(p, size=len(p))) for _ in range(2000)])
got = np.asarray(need("boot_medians"))
assert got.shape == (2000,), "boot_medians should hold 2,000 medians."
same(got, m, "boot_medians")
lo, hi = np.percentile(m, [2.5, 97.5])
same(float(need("low")), float(lo), "low")
same(float(need("high")), float(hi), "high")
```
```python solution
import numpy as np
import pandas as pd

housing = pd.read_csv("housing.csv")
price = housing["price_k"].to_numpy()
rng = np.random.default_rng(8)

boot_medians = np.array([np.median(rng.choice(price, size=len(price))) for _ in range(2000)])
low, high = np.percentile(boot_medians, [2.5, 97.5])
print(round(low, 1), round(high, 1))
```
hint: A list comprehension: `[np.median(rng.choice(price, size=len(price))) for _ in range(2000)]`, then `np.percentile(..., [2.5, 97.5])`.
:::

:::exercise Bootstrap a correlation
Load `students.csv`. With `rng = np.random.default_rng(9)`, resample **rows** 2,000 times (pick row positions with `rng.integers(0, n, n)`), compute the correlation between `hours_studied` and `math` for each resample with `np.corrcoef(x, y)[0, 1]`, and store the 95% percentile interval in `low` and `high`.
```python starter
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
x = students["hours_studied"].to_numpy()
y = students["math"].to_numpy()
n = len(x)
rng = np.random.default_rng(9)

```
```python check
import numpy as np
import pandas as pd
s = pd.read_csv("students.csv")
x = s["hours_studied"].to_numpy(); y = s["math"].to_numpy(); n = len(x)
rng = np.random.default_rng(9)
rs = []
for _ in range(2000):
    i = rng.integers(0, n, n)
    rs.append(np.corrcoef(x[i], y[i])[0, 1])
lo, hi = np.percentile(rs, [2.5, 97.5])
same(float(need("low")), float(lo), "low")
same(float(need("high")), float(hi), "high")
```
```python solution
import numpy as np
import pandas as pd

students = pd.read_csv("students.csv")
x = students["hours_studied"].to_numpy()
y = students["math"].to_numpy()
n = len(x)
rng = np.random.default_rng(9)

rs = []
for _ in range(2000):
    idx = rng.integers(0, n, n)          # the same rows for x and y keeps each pair together
    rs.append(np.corrcoef(x[idx], y[idx])[0, 1])
low, high = np.percentile(rs, [2.5, 97.5])
print(round(low, 2), round(high, 2))
```
hint: Pick `idx = rng.integers(0, n, n)` once per resample and use it for both `x` and `y`, so each student's pair stays together.
:::

:::quiz
? What does "resampling with replacement" mean?
+ Drawing rows from your data where the same row can be picked more than once
- Replacing missing values
- Drawing a new sample from the population
= Each resample is a shuffled, slightly different copy of your sample.
? What's the bootstrap's main advantage over formulas?
- It's always more accurate
+ It works for almost any statistic, like a median or a correlation
- It fixes biased samples
= No special formula is needed; you just recompute the statistic.
? A bootstrap 95% interval for B − A runs from 1% to 4%. What does that suggest?
+ B is very likely truly better than A
- A is better than B
- Nothing, since bootstrap intervals can't be interpreted
= The whole interval is above zero, so a zero difference looks implausible.
:::
