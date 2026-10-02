@@@ part
id: 6
title: Statistics at Work
level: Advanced
blurb: Run and analyse an A/B test the way product teams do, then put the whole course together in a final analysis project.

@@@ lesson
id: ab-testing
title: A/B testing
minutes: 24
summary: Design an experiment, check it ran fairly, test conversion and revenue, report the lift with a confidence interval, and avoid the classic mistakes.
---
An **A/B test** (a randomised controlled experiment) is how companies decide whether a change works: show the current version (**A**, the control) to some users and the new version (**B**, the treatment) to others, **at random**, then compare. Randomisation is what makes it powerful: because chance alone decides who sees B, any difference beyond chance is **caused** by the change.

`ab_test.csv` is a finished experiment: 4,000 visitors, each randomly shown page A or page B.

### 1. Design before you start

Decide these **before** collecting data, and write them down:

| Decision | Our test |
|---|---|
| **Primary metric** | conversion rate (did the visitor buy?) |
| **Hypotheses** | H₀: same conversion rate; H₁: rates differ (two-sided) |
| **α and power** | 0.05 and 80% |
| **Minimum detectable effect** | +3 percentage points (from about 10% to 13%) |
| **Sample size** | worked out below |
| **Guardrail metrics** | revenue per visitor shouldn't drop |

statsmodels works out the sample size for two proportions:

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

effect = proportion_effectsize(0.13, 0.10)        # 10% → 13%
n = NormalIndPower().solve_power(effect_size=effect, alpha=0.05, power=0.8)
print(f"about {n:.0f} visitors per group")
```

We have about 2,000 per group, a little more than needed. (Detecting a smaller lift, say +2 points, would need about 3,800 per group: small effects are expensive.)

### 2. Check the experiment ran fairly

Before looking at results, check that randomisation worked: the groups should be similar in size and in their mix of visitors. A **sample ratio mismatch** (say 60/40 instead of 50/50) usually means a bug, and invalidates the test.

```python
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
counts = ab["group"].value_counts()
print(counts)
print("split test p =", round(stats.chisquare(counts).pvalue, 3))
print(pd.crosstab(ab["group"], ab["device"], normalize="index").round(3))
```

The split is close to 50/50 (p well above 0.05) and both groups have the same device mix. Good.

### 3. Test the primary metric

Conversion is yes/no, so compare two **proportions** with a **z-test** (for large samples it gives the same answer as the chi-square test from Part 4):

```python
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

ab = pd.read_csv("ab_test.csv")
summary = ab.groupby("group")["converted"].agg(["sum", "count", "mean"])
print(summary)
z, p = proportions_ztest(summary["sum"], summary["count"])
print(f"z = {z:.2f}, p = {p:.4f}")
```

### 4. Estimate the lift with a confidence interval

The p-value says B's advantage is unlikely to be luck. The business needs to know **how big** it is:

```python
import numpy as np
import pandas as pd

ab = pd.read_csv("ab_test.csv")
g = ab.groupby("group")["converted"].agg(["mean", "count"])
pa, na = g.loc["A", "mean"], g.loc["A", "count"]
pb, nb = g.loc["B", "mean"], g.loc["B", "count"]

diff = pb - pa
se = np.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
print(f"A {pa:.2%}  B {pb:.2%}")
print(f"absolute lift: {diff:+.2%} (95% CI {diff - 1.96 * se:+.2%} to {diff + 1.96 * se:+.2%})")
print(f"relative lift: {diff / pa:+.0%}")
```

![Bar chart of conversion rates: page A 10.2% and page B 12.8%, each with a 95% interval error bar](figures/ab-test-result.svg)

**Absolute** lift is in percentage points (10.2% → 12.8% is +2.7 points); **relative** lift is the percentage change (+26%). Say which one you mean; mixing them up is a classic reporting error.

### 5. Check the guardrail: revenue per visitor

More buyers is good, but not if each buyer spends less. Revenue per visitor (including the zeros for non-buyers) is very skewed, so use Welch's t-test (fine with 2,000 per group thanks to the CLT) and a bootstrap interval as a cross-check:

```python
import numpy as np
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
ra = ab.loc[ab["group"] == "A", "revenue"].to_numpy()
rb = ab.loc[ab["group"] == "B", "revenue"].to_numpy()
print(f"revenue per visitor: A {ra.mean():.2f}, B {rb.mean():.2f}")
print("Welch p =", round(stats.ttest_ind(rb, ra, equal_var=False).pvalue, 4))

rng = np.random.default_rng(0)
diffs = [rng.choice(rb, len(rb)).mean() - rng.choice(ra, len(ra)).mean() for _ in range(3000)]
print("bootstrap 95% CI for B - A:", np.percentile(diffs, [2.5, 97.5]).round(2))
```

### 6. Segments: interesting, but careful

It's tempting to slice the results (mobile vs desktop, new vs returning…). Slices have smaller samples and multiply the number of tests, so treat them as **ideas to test next**, not conclusions, unless they were planned in advance:

```python
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

ab = pd.read_csv("ab_test.csv")
for device, d in ab.groupby("device"):
    s = d.groupby("group")["converted"].agg(["sum", "count", "mean"])
    _, p = proportions_ztest(s["sum"], s["count"])
    print(f"{device:8} A {s.loc['A', 'mean']:.1%}  B {s.loc['B', 'mean']:.1%}  p = {p:.3f}")
```

### Classic A/B testing mistakes

| Mistake | Why it's a problem | Do instead |
|---|---|---|
| **Peeking**: stopping as soon as p < 0.05 | checking repeatedly inflates false alarms far above 5% | fix the sample size in advance (or use sequential methods built for peeking) |
| testing many metrics and reporting the winner | multiple testing | one primary metric, decided in advance |
| too short a test | misses weekly cycles and the novelty effect | run whole weeks |
| ignoring practical significance | a "significant" +0.1% may not pay for the change | compare the lift's interval with what matters to the business |
| believing p = 0.06 means "no effect" | it means not enough evidence | report the interval; consider more data |

### Writing the result

> **Launch page B.** In a 4,000-visitor randomised test, B converted 12.8% of visitors against 10.2% for A: an absolute lift of 2.7 percentage points (95% CI 0.7 to 4.6; p = 0.008). Revenue per visitor also rose. The split and device mix were balanced. Segment results (mobile vs desktop) are suggestive only and weren't pre-planned.

:::exercise Is the split fair?
Load `ab_test.csv`. Test whether the A/B split is consistent with 50/50 using `stats.chisquare` on the group counts, and store the p-value in `p_split`. Set `srm` (sample ratio mismatch) to `True` if p < 0.01, otherwise `False`.
```python starter
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
from scipy import stats
a = pd.read_csv("ab_test.csv")
p = stats.chisquare(a["group"].value_counts()).pvalue
same(float(need("p_split")), float(p), "p_split")
same(need("srm"), bool(p < 0.01), "srm")
```
```python solution
import pandas as pd
from scipy import stats

ab = pd.read_csv("ab_test.csv")
counts = ab["group"].value_counts()
p_split = stats.chisquare(counts).pvalue
srm = bool(p_split < 0.01)
print(counts.to_dict(), round(p_split, 3), srm)
```
hint: `stats.chisquare(counts)` with no expected counts assumes equal shares.
:::

:::exercise Desktop test
Load `ab_test.csv` and keep **desktop** visitors. Run `proportions_ztest` comparing conversions in A and B, and store the p-value in `p_desktop`. Store B's conversion rate minus A's in `lift_desktop`.
```python starter
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
a = pd.read_csv("ab_test.csv")
d = a[a["device"] == "desktop"]
s = d.groupby("group")["converted"].agg(["sum", "count", "mean"])
same(float(need("p_desktop")), float(proportions_ztest(s["sum"], s["count"])[1]), "p_desktop")
same(float(need("lift_desktop")), float(s.loc["B", "mean"] - s.loc["A", "mean"]), "lift_desktop")
```
```python solution
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

ab = pd.read_csv("ab_test.csv")
desktop = ab[ab["device"] == "desktop"]
s = desktop.groupby("group")["converted"].agg(["sum", "count", "mean"])
_, p_desktop = proportions_ztest(s["sum"], s["count"])
lift_desktop = s.loc["B", "mean"] - s.loc["A", "mean"]
print(round(lift_desktop, 4), round(p_desktop, 4))
```
hint: Filter to desktop, group by `group` and aggregate `sum` and `count` of `converted`, then pass those two columns to `proportions_ztest`.
:::

:::quiz
? Why does randomly assigning visitors to A or B let you conclude B caused the difference?
+ Randomisation balances everything else between the groups, so only the page differs systematically
- Random numbers are always accurate
- It makes the sample bigger
= With random assignment, confounders are spread evenly, so a difference beyond chance is due to the change.
? A test is checked every morning and stopped the first day p < 0.05. What's wrong?
- Nothing
+ Peeking inflates the false-alarm rate well above 5%
- The p-value becomes too large
= Repeated looks give chance many opportunities to cross 0.05. Fix the sample size or use a sequential method.
? Conversion goes from 10% to 12%. What are the absolute and relative lifts?
+ +2 percentage points absolute, +20% relative
- +20 percentage points absolute, +2% relative
- +2% both ways
= Absolute is the difference in rates; relative divides it by the starting rate.
:::

@@@ lesson
id: final-project
title: "Final project: what drives house prices?"
minutes: 35
summary: A complete statistical analysis from question to recommendation, using every part of the course.
---
A property company asks: *"What drives house prices in our three neighbourhoods, and how confident can we be? We want a rule of thumb for valuing homes and to know which neighbourhood is the best value."*

You'll answer with `housing.csv`, step by step. Run each step and read the output before moving on.

### Step 1: Describe the data (Part 1)

```python
import pandas as pd

housing = pd.read_csv("housing.csv")
print(housing.shape)
print(housing.describe().round(1))
print(housing["neighborhood"].value_counts())
print("price skew:", round(housing["price_k"].skew(), 2))
```

Prices are roughly symmetric, so means and medians will agree and standard methods are safe.

### Step 2: Look at the outcome and the predictors (Parts 1 and 5)

```python
import pandas as pd
import matplotlib.pyplot as plt

housing = pd.read_csv("housing.csv")
fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
axes[0].hist(housing["price_k"], bins=20, color="teal", edgecolor="white")
axes[0].set_title("Price (thousands)")
axes[1].scatter(housing["area_sqm"], housing["price_k"], s=12, color="teal")
axes[1].set_title("Price vs area")
axes[2].boxplot([g["price_k"] for _, g in housing.groupby("neighborhood")],
                tick_labels=sorted(housing["neighborhood"].unique()))
axes[2].set_title("Price by neighbourhood")
plt.show()

print(housing[["price_k", "area_sqm", "bedrooms", "age_years", "distance_km"]].corr()["price_k"].round(2))
```

### Step 3: Estimate the typical price with uncertainty (Part 3)

```python
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
for name, g in housing.groupby("neighborhood"):
    p = g["price_k"]
    low, high = stats.t.interval(0.95, len(p) - 1, loc=p.mean(), scale=stats.sem(p))
    print(f"{name:10} mean {p.mean():6.1f}  95% CI {low:6.1f} to {high:6.1f}  (n = {len(p)})")
```

### Step 4: Are the neighbourhoods really different? (Part 4)

```python
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
groups = [g["price_k"] for _, g in housing.groupby("neighborhood")]
print("ANOVA p =", f"{stats.f_oneway(*groups).pvalue:.1e}")
```

Yes, but raw price differences mix up location with **size**, age and distance: maybe Central homes are just bigger. Comparing fairly needs regression.

### Step 5: Separate the effects (Part 5)

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
out = pd.DataFrame({"coef": model.params, "low": model.conf_int()[0], "high": model.conf_int()[1], "p": model.pvalues})
print(out.round(2))
print(f"R² {model.rsquared:.2f}, typical error ±{model.resid.std():.0f}k")
```

### Step 6: Check the model

```python
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
fig, axes = plt.subplots(1, 2, figsize=(10, 3.2))
axes[0].scatter(model.fittedvalues, model.resid, s=12, color="teal")
axes[0].axhline(0, color="darkorange")
axes[0].set_title("Residuals vs predicted")
axes[1].hist(model.resid, bins=20, color="teal", edgecolor="white")
axes[1].set_title("Residuals")
plt.show()
```

No pattern in the residuals and a roughly bell-shaped histogram: the straight-line model is a fair summary.

### Step 7: Find the best-value homes

A home priced well **below** what the model predicts for its size, age and location is potentially good value:

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
housing["predicted"] = model.fittedvalues.round(1)
housing["gap"] = (housing["price_k"] - housing["predicted"]).round(1)
print(housing.nsmallest(5, "gap")[["home_id", "neighborhood", "area_sqm", "age_years", "price_k", "predicted", "gap"]])
```

### Step 8: The write-up

> **What drives prices.** Size, location and distance from the centre explain about 89% of the variation in price. Each extra square metre adds about 3,200 (95% CI roughly 2,800 to 3,500), holding the other factors fixed; each km from the centre takes off about 4,200, and each year of age about 800.
>
> **Neighbourhoods.** For the same home, Riverside costs about 52,000 less than Central and Hillside about 95,000 less. Raw averages overstate some of these gaps because homes differ in size and age.
>
> **Rule of thumb.** Price ≈ the model's formula, with a typical error of about ±39,000; homes priced well below their predicted value (listed above) are worth a closer look.
>
> **Caveats.** 160 homes from one period; the model shows associations in this data, not guaranteed causes; predictions are reliable only for homes like these (35 to 175 m², up to about 25 km out).

Check every number in the write-up against your output before sending it.

### What you've learned

You can now describe data honestly, reason about probability, estimate with confidence intervals, test claims, measure relationships, fit regression models and run A/B tests: the statistical core of both the analyst and AI engineer paths. The next course, **machine learning**, builds directly on regression and on the idea of judging models with data they haven't seen.

:::exercise Best and worst value
Fit the final model (`price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)`), add `gap` = actual price − predicted price to `housing`, and store the `home_id` of the **most overpriced** home (largest positive gap) in `overpriced_id`, and the number of homes priced more than **50 below** their prediction in `n_bargains`.
```python starter
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
import statsmodels.formula.api as smf
h = pd.read_csv("housing.csv")
m = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=h).fit()
gap = h["price_k"] - m.fittedvalues
same(int(need("overpriced_id")), int(h.loc[gap.idxmax(), "home_id"]), "overpriced_id")
same(int(need("n_bargains")), int((gap < -50).sum()), "n_bargains")
```
```python solution
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
housing["gap"] = housing["price_k"] - model.fittedvalues
overpriced_id = housing.loc[housing["gap"].idxmax(), "home_id"]
n_bargains = (housing["gap"] < -50).sum()
print(overpriced_id, n_bargains)
```
hint: `model.fittedvalues` holds each home's predicted price. "More than 50 below" means `gap < -50`.
:::

:::exercise Central's premium
Using the same model, store the estimated price difference between **Riverside** and **Central** (the `C(neighborhood)[T.Riverside]` coefficient) in `riverside_coef`, and the lower and upper ends of its 95% confidence interval in `ci_low` and `ci_high`.
```python starter
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
import statsmodels.formula.api as smf
h = pd.read_csv("housing.csv")
m = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=h).fit()
k = "C(neighborhood)[T.Riverside]"
same(float(need("riverside_coef")), float(m.params[k]), "riverside_coef")
ci = m.conf_int().loc[k]
same(float(need("ci_low")), float(ci[0]), "ci_low")
same(float(need("ci_high")), float(ci[1]), "ci_high")
```
```python solution
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
name = "C(neighborhood)[T.Riverside]"
riverside_coef = model.params[name]
ci_low, ci_high = model.conf_int().loc[name]
print(round(riverside_coef, 1), round(ci_low, 1), round(ci_high, 1))
```
hint: `model.params[name]` and `model.conf_int().loc[name]` (which gives the two ends).
:::

:::quiz
? Why fit a regression instead of just comparing average prices by neighbourhood?
+ To compare like with like: holding size, age and distance fixed
- Regression always gives bigger differences
- Averages can't be calculated by neighbourhood
= Raw averages mix location with other factors; regression separates them.
? A model explains 89% of price variation. Does it prove that a bigger area causes a higher price?
- Yes, R² proves cause
+ No: it shows a strong association; causal claims need more (experiments or strong reasoning)
- Only if p < 0.05
= Observational data shows associations. Here causation is plausible, but the model alone doesn't prove it.
? What belongs in the caveats of a good write-up?
+ The sample's limits, what the model can't show, and where predictions are reliable
- The code
- Every p-value calculated
= Caveats tell the reader how far to trust and generalise the results.
:::
