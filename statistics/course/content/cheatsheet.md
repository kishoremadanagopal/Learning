# Statistics cheat sheet

Every formula, test and function from the course on one page. The number in brackets is the lesson.

## Which summary? [2–5]

| Data | Centre | Spread | Chart |
|---|---|---|---|
| numbers, symmetric | mean `s.mean()` | std `s.std()` | histogram |
| numbers, skewed or with outliers | median `s.median()` | IQR `s.quantile(.75) - s.quantile(.25)` | histogram, box plot |
| categories | mode `s.mode()[0]` | — | sorted bar chart |
| yes/no (1/0) | proportion `s.mean()` | — | bar chart |
| two categories | — | — | `pd.crosstab(a, b, normalize="index")`, stacked bars |

```python
s.describe()                         # count, mean, std, min, quartiles, max        [1]
np.average(x, weights=w)             # weighted mean                                 [2]
s.var(), s.std()                     # sample variance and std (divide by n - 1)     [3]
np.std(x, ddof=1)                    # NumPy needs ddof=1 for the sample std         [3]
s.skew()                             # ~0 symmetric, > 0 right tail, < 0 left tail   [4]
(x - x.mean()) / x.std()             # z-scores                                      [4]
q1, q3 = s.quantile([.25, .75]); out = (s < q1 - 1.5*(q3-q1)) | (s > q3 + 1.5*(q3-q1))   # IQR outliers [4]
```

## Probability [6–9]

| Rule | Formula |
|---|---|
| complement | P(not A) = 1 − P(A) |
| or | P(A or B) = P(A) + P(B) − P(A and B) |
| and (independent) | P(A and B) = P(A) × P(B) |
| at least one | 1 − P(none) |
| conditional | P(A \| B) = P(A and B) / P(B) |
| Bayes | P(A \| B) = P(B \| A) × P(A) / P(B) |

```python
from scipy import stats
stats.binom.pmf(k, n, p)   .cdf(k, n, p)   .sf(k, n, p)    # exactly k / at most k / more than k  [8]
stats.poisson.pmf(k, lam)  .cdf(k, lam)   .sf(k, lam)                                        [8]
stats.norm.cdf(x, mu, sd)  # P(X ≤ x)        stats.norm.sf(x, mu, sd)  # P(X > x)             [9]
stats.norm.ppf(0.95, mu, sd)   # the value with 95% below it; ppf(0.975) = 1.96                [9]
stats.shapiro(x).pvalue        # normality test                                                [9]
```

Normal curve: 68% within 1 std, 95% within 2 (1.96), 99.7% within 3. [9]

## Sampling and estimation [10–13]

| Quantity | Formula |
|---|---|
| standard error of a mean | s / √n |
| standard error of a proportion | √(p(1 − p) / n) |
| 95% CI for a mean | mean ± t* × SE, with t* = `stats.t.ppf(0.975, n - 1)` |
| 95% CI for a proportion | p ± 1.96 × SE |
| CI for a difference in proportions | (p₂ − p₁) ± 1.96 × √(p₁(1−p₁)/n₁ + p₂(1−p₂)/n₂) |

```python
df.sample(n=30, random_state=1)                    df.groupby("g").sample(frac=0.2)        # [10]
stats.sem(x)                                                                              # [10]
stats.t.interval(0.95, len(x) - 1, loc=x.mean(), scale=stats.sem(x))                      # [12]
boot = [np.mean(rng.choice(x, len(x))) for _ in range(5000)]; np.percentile(boot, [2.5, 97.5])  # [13]
stats.bootstrap((x,), np.median, random_state=0).confidence_interval                      # [13]
```

## Which test? [14–18]

| Question | Data | Test | SciPy / statsmodels |
|---|---|---|---|
| one mean vs a value | numbers | one-sample t | `stats.ttest_1samp(x, value)` |
| two separate groups' means | numbers | Welch's t | `stats.ttest_ind(a, b, equal_var=False)` |
| same subjects, before vs after | paired numbers | paired t | `stats.ttest_rel(after, before)` |
| two groups, skewed / small | numbers | Mann-Whitney U | `stats.mannwhitneyu(a, b)` |
| paired, skewed / small | paired numbers | Wilcoxon signed-rank | `stats.wilcoxon(after, before)` |
| 3+ groups' means | numbers | one-way ANOVA (+ Tukey) | `stats.f_oneway(*groups)`, `stats.tukey_hsd(*groups)` |
| 3+ groups, skewed | numbers | Kruskal-Wallis | `stats.kruskal(*groups)` |
| counts vs a claimed split | counts | chi-square goodness of fit | `stats.chisquare(observed, expected)` |
| two categorical variables | counts table | chi-square independence | `stats.chi2_contingency(pd.crosstab(a, b))` |
| 2 × 2 table, small counts | counts | Fisher's exact | `stats.fisher_exact(table)` |
| two proportions (A/B test) | yes/no | two-proportion z | `proportions_ztest(successes, totals)` |
| any statistic | anything | permutation test | shuffle labels, compare [14] |
| two numbers related? | pairs | Pearson / Spearman | `stats.pearsonr(x, y)`, `stats.spearmanr(x, y)` |

Reading results: p < α (usually 0.05) → reject H₀ ("statistically significant"). Always report the effect size and a confidence interval, not just p.

| | H₀ true | H₀ false |
|---|---|---|
| reject H₀ | Type I error (α) | correct (power) |
| keep H₀ | correct | Type II error (β) |

```python
TTestIndPower().solve_power(effect_size=0.5, alpha=0.05, power=0.8)       # n per group     [16]
NormalIndPower().solve_power(proportion_effectsize(0.13, 0.10), alpha=0.05, power=0.8)       [22]
```

Effect sizes: Cohen's d = difference / pooled std (0.2 small, 0.5 medium, 0.8 large) [15] · Cramér's V [17] · η² [18]

## Relationships and regression [19–21]

```python
df["x"].corr(df["y"])                     df[cols].corr()                          # [19]
fit = stats.linregress(x, y)              # .slope .intercept .rvalue .pvalue .stderr  [20]
pred = fit.intercept + fit.slope * x_new  # R² = fit.rvalue ** 2                       [20]

import statsmodels.formula.api as smf
model = smf.ols("y ~ x1 + x2 + C(category)", data=df).fit()                        # [21]
model.params   model.pvalues   model.conf_int()   model.rsquared_adj   model.summary()
model.predict(new_df)      model.fittedvalues      model.resid
```

Slope = change in y per 1 unit of x · R² = share of variation explained · residual = actual − predicted · coefficients in multiple regression = effect holding the others fixed · correlation ≠ causation.

## A/B test checklist [22]

1. Pick one primary metric, α, power and the minimum effect **before** starting; compute the sample size.
2. Check the split (sample ratio mismatch) and the balance of the groups.
3. Test the primary metric; report the absolute and relative lift with a 95% CI.
4. Check guardrail metrics.
5. Don't peek; treat unplanned segments as ideas, not conclusions.
