# Statistics with Python

A hands-on statistics course for complete beginners: 23 lessons from averages and charts to probability, the bell curve, confidence intervals, hypothesis tests, regression and A/B testing. Every idea comes with a picture and code you can run, in a sandbox that runs real Python, pandas and SciPy in your browser and checks your answers.

Statistics is part of the shared core for both the **AI engineer** and the **data / AI analyst** paths: it's how analysts tell a real effect from luck, and how machine learning measures whether a model works.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/statistics/)

The sandbox runs real Python 3.14 with NumPy, pandas, SciPy, statsmodels and matplotlib inside your browser (via [Pyodide](https://pyodide.org)). Nothing to install, no sign-up.

- every lesson, with **109 examples** you can run and change
- **46 exercises**, numbered by lesson, that check your code and tell you what's off
- **69 quiz questions**, with explanations
- **8 practice datasets** that load with one line, like `pd.read_csv("sales.csv")`
- a chart or diagram for every key idea, and charts drawn right under your code
- your progress and code saved in your own browser

**Before you start:** you should be comfortable with Python basics and pandas (loading a CSV, selecting columns, `groupby`). If not, do [Learn Python from scratch](../python/) and [Python for Data](../python-data/) first. No maths beyond school arithmetic is assumed: every formula is explained in words and checked with code.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 23 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every statistics term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | every formula, test and SciPy function on one page, plus a "which test?" table |
| 🗂️ [Datasets](https://github.com/kishoremadanagopal/learning/tree/main/statistics/data) | the practice files, to download and use on your own computer |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.

## Lessons

### Part 1: Describing Data (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What statistics is for](lessons/01-what-is-statistics.md) | populations and samples, statistics and parameters, descriptive vs inferential, kinds of variables | 1–2 |
| 2 | [The centre: mean, median and mode](lessons/02-center.md) | mean, median, mode, outliers, skew, choosing a "typical" value, weighted mean | 3–4 |
| 3 | [Spread: range, IQR and standard deviation](lessons/03-spread.md) | range, quartiles, IQR, variance, standard deviation, `n - 1`, box plots, coefficient of variation | 5–6 |
| 4 | [Shape, z-scores and outliers](lessons/04-shape-and-outliers.md) | histograms and bins, symmetric and skewed shapes, `skew()`, log transform, z-scores, outlier rules | 7–8 |
| 5 | [Categorical data: counts, shares and charts](lessons/05-categorical-data.md) | counts and proportions, the mean of 0/1 data, bar vs pie charts, two-way tables, row percentages | 9–10 |

### Part 2: Probability (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 6 | [Probability basics](lessons/06-probability-basics.md) | probability as a fraction and a long-run share, law of large numbers, complement, addition and multiplication rules, independence, counting | 11–12 |
| 7 | [Conditional probability and Bayes](lessons/07-conditional-probability.md) | P(A \| B), conditioning by filtering, independence, P(A \| B) vs P(B \| A), Bayes' rule, base rates, false positives | 13–14 |
| 8 | [Counting distributions: binomial and Poisson](lessons/08-discrete-distributions.md) | random variables, expected value, the binomial distribution, pmf, cdf and sf, the Poisson distribution, simulating with rvs | 15–16 |
| 9 | [The normal distribution](lessons/09-normal-distribution.md) | the bell curve, μ and σ, the 68-95-99.7 rule, areas with `norm.cdf` and `norm.sf`, percentiles with `norm.ppf`, the standard normal, checking normality | 17–18 |

### Part 3: Sampling and Estimation (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 10 | [Sampling and bias](lessons/10-sampling-and-bias.md) | simple random, stratified, cluster and convenience samples, selection, non-response, survivorship and measurement bias, sampling variability, standard error | 19–20 |
| 11 | [The central limit theorem](lessons/11-central-limit-theorem.md) | the distribution of sample averages, the central limit theorem, σ / √n, how large n must be, proportions | 21–22 |
| 12 | [Confidence intervals](lessons/12-confidence-intervals.md) | estimate ± critical value × standard error, the t distribution, degrees of freedom, `stats.t.interval`, interpreting 95%, interval width, intervals for proportions, margin of error | 23–24 |
| 13 | [The bootstrap](lessons/13-bootstrap.md) | resampling with replacement, bootstrap percentile intervals, intervals for medians and correlations, `scipy.stats.bootstrap`, differences between groups, limits | 25–26 |

### Part 4: Hypothesis Testing (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 14 | [Hypothesis testing and p-values](lessons/14-hypothesis-testing.md) | null and alternative hypotheses, test statistics, null distributions, permutation tests, p-values, α, one- vs two-sided tests, reading p-values correctly | 27–28 |
| 15 | [t-tests: comparing means](lessons/15-t-tests.md) | the t statistic, one-sample, Welch's two-sample and paired t-tests, confidence intervals for differences, Cohen's d, assumptions, Mann-Whitney and Wilcoxon | 29–30 |
| 16 | [Errors, power and sample size](lessons/16-errors-and-power.md) | Type I and II errors, α and β, power, simulating false alarms and power, sample size calculations, multiple testing, Bonferroni | 31–32 |
| 17 | [Chi-square tests for counts](lessons/17-chi-square.md) | observed vs expected counts, the χ² statistic, goodness-of-fit tests, tests of independence, expected frequencies, Cramér's V, Fisher's exact test | 33–34 |
| 18 | [Comparing several groups with ANOVA](lessons/18-anova.md) | one-way ANOVA, between- and within-group variation, the F statistic, `f_oneway`, Tukey's HSD, Kruskal-Wallis, eta squared | 35–36 |

### Part 5: Relationships and Regression (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 19 | [Correlation](lessons/19-correlation.md) | scatter plots, Pearson's r, testing a correlation with `pearsonr`, Spearman's rank correlation, correlation matrices and heatmaps, confounders, correlation vs causation | 37–38 |
| 20 | [Simple linear regression](lessons/20-linear-regression.md) | the regression line, least squares, slope and intercept, `stats.linregress`, prediction and extrapolation, R², residuals and residual plots, testing the slope, regression to the mean | 39–40 |
| 21 | [Multiple regression](lessons/21-multiple-regression.md) | multiple regression, statsmodels formulas, coefficients "holding others fixed", p-values and intervals for coefficients, dummy variables with `C()`, adjusted R², prediction, residual checks, multicollinearity and VIF | 41–42 |

### Part 6: Statistics at Work (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 22 | [A/B testing](lessons/22-ab-testing.md) | randomised experiments, pre-registration, sample size for proportions, sample ratio mismatch, the two-proportion z-test, absolute vs relative lift, guardrail metrics, segments, peeking | 43–44 |
| 23 | [Final project: what drives house prices?](lessons/23-final-project.md) | an end-to-end statistical analysis: describing, visualising, intervals, ANOVA, multiple regression, model checks, residual-based insights, and a write-up with caveats | 45–46 |

## The practice datasets

| File | Rows | What's in it |
|---|---|---|
| [`students.csv`](data/students.csv) | 60 | 60 students: class, hours studied, attendance and exam scores. |
| [`sales.csv`](data/sales.csv) | 600 | 600 orders from 2025: date, customer, region, product, units and price. |
| [`customers.csv`](data/customers.csv) | 120 | 120 customers: name, city, segment, age and signup date. |
| [`weather.csv`](data/weather.csv) | 1095 | Daily temperature and rain for London, Mumbai and New York in 2025. |
| [`ab_test.csv`](data/ab_test.csv) | 4000 | 4,000 website visitors split between page A and page B: device, whether they bought, and revenue. |
| [`housing.csv`](data/housing.csv) | 160 | 160 homes: neighborhood, area, bedrooms, age, distance to the centre and price. |
| [`training.csv`](data/training.csv) | 30 | 30 employees' test scores before and after a training course. |
| [`movies.json`](data/movies.json) | 40 | 40 (made-up) films: year, genre, runtime, rating and box office. |

All of the data is made up for practice, so it's safe to share and experiment with.

## Running it on your own computer

Everything in the course also works in a normal Python setup. Install Python from [python.org](https://www.python.org/), then:

```bash
pip install numpy pandas matplotlib scipy statsmodels jupyterlab
jupyter lab
```

Download the files from [`data/`](data/) into the same folder as your notebook. The sandbox runs pandas 3, so if your computer has an older pandas, upgrade with `pip install --upgrade pandas`.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
