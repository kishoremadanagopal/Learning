@@@ part
id: 1
title: Describing Data
level: Beginner
blurb: Summarise any dataset with a few honest numbers and the right picture: averages, spread, shape, outliers and categories.

@@@ lesson
id: what-is-statistics
title: What statistics is for
minutes: 12
summary: Populations and samples, the kinds of variables, and the two big jobs of statistics.
---
**Statistics** is the art of learning from data when you can't see everything. You can't survey every customer, test every light bulb or wait for every future sale, so you look at **some** of the data and make careful statements about **all** of it.

![Grey dots are a whole population; 30 orange dots are a sample drawn from it](figures/population-sample.svg)

- The **population** is everything you care about: all customers, all students, every visit to a website.
- A **sample** is the part you actually measure.
- A **statistic** is a number calculated from the sample, like its average. You use it to estimate the matching number for the population, called a **parameter**.

Statistics has two big jobs, and this course follows them in order:

| Job | Question | Parts of this course |
|---|---|---|
| **Descriptive statistics** | "What does this data look like?" | 1 |
| **Inferential statistics** | "What can I conclude about everyone from this sample, and how sure am I?" | 2 to 6 |

### Kinds of variables

A **variable** is anything you record about each row. The kind of variable decides which summaries and charts make sense:

| Kind | Examples | Summaries | Charts |
|---|---|---|---|
| **Numerical, continuous** | height, price, temperature | mean, median, spread | histogram, box plot |
| **Numerical, discrete** (counts) | number of orders, goals | mean, median | bar chart of counts |
| **Categorical** | city, product, yes/no | counts, percentages | bar chart |
| **Ordinal** (categories with an order) | small/medium/large, survey ratings 1–5 | counts, median | bar chart in order |

Let's look at the students dataset, which you'll use a lot:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students.head())
print(students.dtypes)
```

`class` is categorical; `hours_studied` is continuous; the scores are discrete numbers but behave like continuous ones because they have many possible values.

### Describing in one line

pandas' `describe()` gives the most common descriptive statistics at once. By the end of Part 1 you'll know what every number in it means:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students[["hours_studied", "math"]].describe().round(1))
```

### A sample is not the population

Here's the key idea of the whole course in five lines. We take a random sample of 10 students, several times, and each sample gives a slightly different average:

```python
import pandas as pd

students = pd.read_csv("students.csv")
print("all 60 students:", students["math"].mean().round(1))
for seed in range(5):
    sample = students.sample(10, random_state=seed)
    print("sample of 10:   ", sample["math"].mean().round(1))
```

Samples wobble. Inferential statistics is about measuring that wobble, so you can say "the average is about 57, give or take 4" instead of pretending one sample is the truth.

### Where statistics shows up in data and AI work

- **Analysts** use it to report fairly ("sales rose 8%, which is more than normal monthly noise") and to run **A/B tests**.
- **AI engineers** use it to check whether a model is really better than the last one, to understand training data, and in the probability behind every machine-learning model.

:::exercise Sample versus everyone
Load `students.csv`. Store the average `science` score of **all** students in `pop_mean`, and the average science score of a random sample of 15 students, taken with `students.sample(15, random_state=1)`, in `sample_mean`.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
same(float(need("pop_mean")), float(s["science"].mean()), "pop_mean")
same(float(need("sample_mean")), float(s.sample(15, random_state=1)["science"].mean()), "sample_mean")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
pop_mean = students["science"].mean()
sample_mean = students.sample(15, random_state=1)["science"].mean()
print(pop_mean, sample_mean)
```
hint: `students["science"].mean()`, then the same on `students.sample(15, random_state=1)`.
:::

:::exercise Name the variable types
Make a dictionary `kinds` that maps each of these columns of `students.csv` to `"categorical"` or `"numerical"`: `"class"`, `"hours_studied"`, `"attendance_pct"`, `"student"`.
```python starter
kinds = {}
```
```python check
same(need("kinds", dict), {"class": "categorical", "hours_studied": "numerical", "attendance_pct": "numerical", "student": "categorical"}, "kinds")
```
```python solution
kinds = {
    "class": "categorical",
    "hours_studied": "numerical",
    "attendance_pct": "numerical",
    "student": "categorical",
}
print(kinds)
```
hint: Ask "can I average it?" A name or a class letter can't be averaged.
:::

:::quiz
? A poll asks 1,000 voters out of millions. What are the 1,000?
- The population
+ A sample
- A parameter
= The sample is the part you measure; the population is everyone you want to draw conclusions about.
? Which is descriptive statistics?
+ "The average order this month was 54 dollars."
- "Page B will convert better for all future visitors."
- "Our customers in general prefer email."
= Describing the data you have is descriptive. Generalising to everyone is inferential.
? Survey answers on a 1-5 "agree" scale are best described as:
- Continuous
+ Ordinal
- Not a variable
= They're categories with a natural order, so they're ordinal.
:::

@@@ lesson
id: center
title: The centre: mean, median and mode
minutes: 16
summary: Three ways to say "typical", when each one is honest, and how outliers and skew pull the mean.
---
"What's a typical value?" has three common answers:

| Measure | What it is | pandas |
|---|---|---|
| **Mean** | add everything up, divide by how many | `s.mean()` |
| **Median** | the middle value when sorted | `s.median()` |
| **Mode** | the most common value | `s.mode()` |

```python
import pandas as pd

scores = pd.Series([4, 7, 7, 8, 9, 10, 12])
print("mean  ", scores.mean())
print("median", scores.median())
print("mode  ", scores.mode().tolist())
```

With an even number of values the median is the average of the middle two. `mode()` returns a list because there can be ties.

### Outliers pull the mean

The mean uses every value's size, so one extreme value drags it. The median only cares about order, so it barely moves:

```python
import pandas as pd

salaries = pd.Series([38, 41, 44, 46, 52])          # thousands
print(salaries.mean(), salaries.median())

salaries_with_ceo = pd.concat([salaries, pd.Series([900])])
print(salaries_with_ceo.mean().round(1), salaries_with_ceo.median())
```

One CEO turned an average salary of 44k into 187k, but the median only moved from 44 to 45. That's why house prices and incomes are usually reported as medians.

![Histogram of incomes with a long right tail: the dashed mean line sits to the right of the solid median line](figures/mean-median-skew.svg)

When data has a long tail on one side (it's **skewed**), the mean is pulled towards the tail. In the picture, most people earn 20–60k, but a few very high earners stretch the tail to the right, so the mean (54k) sits above the median (41k). **Rule of thumb:** if the mean and median are far apart, report the median, or both.

### Which one to use

| Data | Best "typical" value |
|---|---|
| roughly symmetric, no extreme values | mean (or median: they agree) |
| skewed or with outliers (incomes, prices, waiting times) | median |
| categories (most popular city, product) | mode |

### Centre by group

Combining `groupby` with these summaries answers "typical value for each group":

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby("category")["revenue"].agg(["mean", "median"]).round(1))
```

For Electronics, the mean order (about 730) is more than double the median (about 320): a few laptop orders drag it up. Which number you report changes the story, so say which you used.

### Weighted mean

Sometimes values count unequally. A **weighted mean** multiplies each value by its weight, adds them up, and divides by the total weight. NumPy's `np.average` does it:

```python
import numpy as np

grades = np.array([72, 85, 90])      # coursework, midterm, final
weights = np.array([0.2, 0.3, 0.5])  # how much each counts
print(np.average(grades, weights=weights))
print(grades.mean())                 # the unweighted mean is different
```

:::exercise Typical order
Load `sales.csv` and add `revenue` (units × unit_price). Store the **mean** revenue per order in `mean_rev` and the **median** in `median_rev`. Then set `report` to the string `"median"` if the mean is more than 20% above the median, otherwise `"mean"`.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
r = s["units"] * s["unit_price"]
same(float(need("mean_rev")), float(r.mean()), "mean_rev")
same(float(need("median_rev")), float(r.median()), "median_rev")
same(need("report"), "median" if r.mean() > 1.2 * r.median() else "mean", "report")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
mean_rev = sales["revenue"].mean()
median_rev = sales["revenue"].median()
report = "median" if mean_rev > 1.2 * median_rev else "mean"
print(mean_rev, median_rev, report)
```
hint: "More than 20% above" means `mean_rev > 1.2 * median_rev`.
:::

:::exercise Most common product
Load `sales.csv` and store the most frequently ordered `product` (the mode) in `top_product`, as a string.
```python starter
import pandas as pd

sales = pd.read_csv("sales.csv")

```
```python check
import pandas as pd
s = pd.read_csv("sales.csv")
same(need("top_product"), s["product"].mode()[0], "top_product")
```
```python solution
import pandas as pd

sales = pd.read_csv("sales.csv")
top_product = sales["product"].mode()[0]
print(top_product)
```
hint: `mode()` returns a Series; take its first item with `[0]`.
:::

:::quiz
? House prices in a city have a few mansions. Which "typical price" is most honest?
- Mean
+ Median
- Mode
= The few very expensive homes pull the mean up; the median shows what a typical home costs.
? In a right-skewed dataset, where is the mean compared with the median?
+ Higher (pulled towards the long right tail)
- Lower
- Always equal
= The long tail of big values drags the mean in their direction.
? What does `s.mode()` return?
- A single number
+ A Series, because several values can tie for most common
- The middle value
= Take `s.mode()[0]` when you want one value.
:::

@@@ lesson
id: spread
title: Spread: range, IQR and standard deviation
minutes: 18
summary: How spread out values are, measured four ways, and how to read a box plot.
---
Two classes can have the same average score but be completely different: in one everyone scored about 60, in the other scores ranged from 20 to 100. The average alone hides that. **Spread** (also called variability or dispersion) measures it.

![Two bell curves with the same mean of 60: a tall narrow one (std 5) and a wide flat one (std 15)](figures/same-mean-different-spread.svg)

### Range

The simplest measure: largest minus smallest. It's easy to understand but uses only the two most extreme values, so one outlier wrecks it.

```python
import pandas as pd

students = pd.read_csv("students.csv")
math = students["math"]
print("range:", math.max() - math.min())
```

### Interquartile range (IQR)

The **quartiles** split sorted data into four equal parts. Q1 has 25% of values below it, Q2 is the median (50%), and Q3 has 75% below it. The **IQR** is Q3 − Q1: the spread of the middle half of the data. Outliers can't affect it.

```python
import pandas as pd

students = pd.read_csv("students.csv")
q1, q3 = students["math"].quantile([0.25, 0.75])
print("Q1:", q1, " Q3:", q3, " IQR:", q3 - q1)
```

### Variance and standard deviation

The **standard deviation** (std) is the most used measure of spread. Think of it as "the typical distance of a value from the mean". It's built in three steps:

1. find each value's distance from the mean (its **deviation**);
2. square the deviations (so negatives don't cancel positives) and average them: that's the **variance**;
3. take the square root, so the units are the same as the data again: that's the **standard deviation**.

```python
import numpy as np

x = np.array([4, 7, 7, 8, 9])
deviations = x - x.mean()
variance = (deviations ** 2).sum() / (len(x) - 1)
print("deviations:", deviations)
print("variance:  ", variance)
print("std:       ", np.sqrt(variance))
print("pandas std:", round(float(np.std(x, ddof=1)), 4))
```

Why divide by `n − 1` instead of `n`? A sample's values sit closer to their own mean than to the population's mean, so dividing by `n` slightly underestimates the spread. Dividing by `n − 1` corrects it. This is the **sample** standard deviation, and it's what pandas' `.std()` uses. (NumPy's `np.std` divides by `n` unless you pass `ddof=1`, a common source of tiny mismatches.)

```python
import pandas as pd

students = pd.read_csv("students.csv")
print(students[["math", "science", "english"]].agg(["mean", "std"]).round(1))
```

### Reading a box plot

A **box plot** draws the quartiles, so you can see the centre, spread and outliers at a glance:

![An annotated box plot: the box runs from Q1 to Q3 with the median inside, whiskers reach the lowest and highest typical values, and dots beyond them are outliers](figures/boxplot-anatomy.svg)

- the **box** spans Q1 to Q3 (the middle 50%, whose width is the IQR);
- the line inside is the **median**;
- the **whiskers** reach the furthest values within 1.5 × IQR of the box;
- dots beyond the whiskers are **outliers**.

Box plots shine when comparing groups:

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.boxplot([students["math"], students["science"], students["english"]], tick_labels=["math", "science", "english"])
ax.set_ylabel("score")
ax.set_title("Score spread by subject")
plt.show()
```

### Coefficient of variation

Comparing the spread of things measured in different units (house prices and house sizes) is unfair with the std alone. The **coefficient of variation** divides the std by the mean, giving spread as a share of the typical value:

```python
import pandas as pd

housing = pd.read_csv("housing.csv")
for col in ["price_k", "area_sqm"]:
    cv = housing[col].std() / housing[col].mean()
    print(f"{col}: std {housing[col].std():.1f}, CV {cv:.0%}")
```

:::exercise Spread of science scores
Load `students.csv`. For the `science` column, store the range in `sci_range`, the IQR in `sci_iqr` and the standard deviation (pandas' `.std()`) in `sci_std`.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")["science"]
same(float(need("sci_range")), float(s.max() - s.min()), "sci_range")
same(float(need("sci_iqr")), float(s.quantile(0.75) - s.quantile(0.25)), "sci_iqr")
same(float(need("sci_std")), float(s.std()), "sci_std")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
sci = students["science"]
sci_range = sci.max() - sci.min()
sci_iqr = sci.quantile(0.75) - sci.quantile(0.25)
sci_std = sci.std()
print(sci_range, sci_iqr, sci_std)
```
hint: `quantile(0.75) - quantile(0.25)` is the IQR.
:::

:::exercise Standard deviation by hand
Without using `.std()` or `np.std`, calculate the sample standard deviation of `x` and store it in `sd`. Follow the three steps: deviations, variance (divide by n − 1), square root.
```python starter
import numpy as np

x = np.array([12, 15, 11, 18, 14, 20])

```
```python check
import numpy as np
x = np.array([12, 15, 11, 18, 14, 20])
same(float(need("sd")), float(np.std(x, ddof=1)), "sd")
assert not uses(".std(") and not uses("np.std"), "Work it out step by step, without .std()."
```
```python solution
import numpy as np

x = np.array([12, 15, 11, 18, 14, 20])
deviations = x - x.mean()
variance = (deviations ** 2).sum() / (len(x) - 1)
sd = np.sqrt(variance)
print(sd)
```
hint: `variance = ((x - x.mean()) ** 2).sum() / (len(x) - 1)`, then `np.sqrt(variance)`.
:::

:::quiz
? Which measure of spread is not affected by a single extreme outlier?
- Range
+ IQR
- Standard deviation
= The IQR uses only the middle 50% of values, so the extremes don't matter.
? What does a standard deviation of 15 on an exam (mean 60) roughly mean?
+ Scores typically sit about 15 points from 60
- Every score is between 45 and 75
- 15 students scored 60
= The std is the typical distance from the mean, not a hard limit.
? In a box plot, what does the box itself show?
- The full range of the data
+ The middle 50% of values, from Q1 to Q3
- The mean plus or minus one standard deviation
= The box spans the interquartile range, with the median inside.
:::

@@@ lesson
id: shape-and-outliers
title: Shape, z-scores and outliers
minutes: 18
summary: Read a histogram's shape, standardise values with z-scores, and flag outliers two ways.
---
Centre and spread are two numbers. The **shape** of the data is the rest of the story, and a histogram shows it best.

![Three histograms: symmetric with mean and median together; right-skewed with the mean to the right; left-skewed with the mean to the left](figures/distribution-shapes.svg)

| Shape | Looks like | Mean vs median | Real examples |
|---|---|---|---|
| **Symmetric** | a hill with matching sides | about equal | heights, measurement errors |
| **Right-skewed** | long tail to the right | mean > median | incomes, house prices, waiting times |
| **Left-skewed** | long tail to the left | mean < median | age at retirement, easy exam scores |

Other shapes to watch for: **bimodal** (two hills, usually two groups mixed together) and **uniform** (flat).

### Drawing a histogram

The number of **bins** (bars) changes what you see. Try a few:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]

fig, axes = plt.subplots(1, 2, figsize=(9, 3))
axes[0].hist(sales["revenue"], bins=10, color="teal")
axes[0].set_title("10 bins")
axes[1].hist(sales["revenue"], bins=40, color="teal")
axes[1].set_title("40 bins")
for ax in axes:
    ax.set_xlabel("order revenue")
plt.show()
```

Order revenue is strongly right-skewed: most orders are small, a few laptop orders are huge.

### Measuring skew

`skew()` puts a number on it: about 0 means symmetric, positive means a right tail, negative a left tail. Beyond about ±1, the skew is strong.

```python
import pandas as pd

sales = pd.read_csv("sales.csv")
sales["revenue"] = sales["units"] * sales["unit_price"]
students = pd.read_csv("students.csv")
print("revenue skew:", round(sales["revenue"].skew(), 2))
print("math skew:   ", round(students["math"].skew(), 2))
```

A common fix for strong right skew is to analyse the **logarithm** of the values, which pulls the long tail in. `np.log(sales["revenue"])` is much more symmetric.

### z-scores: how unusual is a value?

A **z-score** says how many standard deviations a value is from the mean:

z = (value − mean) / std

![A bell curve with markers at z = -2 (unusually low), z = 0 (exactly average) and z = 1.5 (1.5 std above)](figures/z-scores.svg)

z-scores put different measurements on one scale. Is 80 in math or 75 in english the better result?

```python
import pandas as pd

students = pd.read_csv("students.csv")
for subject, score in [("math", 80), ("english", 75)]:
    m, sd = students[subject].mean(), students[subject].std()
    print(f"{subject}: {score} has z = {(score - m) / sd:.2f}")
```

The math score is further above its own class average, so it's the more impressive one, even though english scores might look similar.

### Two ways to flag outliers

| Rule | Outlier if | Good for |
|---|---|---|
| **z-score rule** | \|z\| > 3 | roughly symmetric data |
| **IQR rule** (the box plot rule) | below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR | any shape, including skewed |

```python
import pandas as pd

housing = pd.read_csv("housing.csv")
price = housing["price_k"]

z = (price - price.mean()) / price.std()
print("z-rule outliers:", int((z.abs() > 3).sum()))

q1, q3 = price.quantile([0.25, 0.75])
iqr = q3 - q1
outside = (price < q1 - 1.5 * iqr) | (price > q3 + 1.5 * iqr)
print("IQR-rule outliers:", int(outside.sum()))
```

An outlier is a reason to **look**, not a reason to delete. It might be a typing error, or your most important customer.

:::exercise Standardise the scores
Load `students.csv` and add a column `math_z`: each student's math z-score (using the column's mean and pandas `.std()`). Store the name of the student with the **highest** z-score in `top_student`.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
z = (s["math"] - s["math"].mean()) / s["math"].std()
got = need("students", pd.DataFrame)
same(got["math_z"], z, "students['math_z']")
same(need("top_student"), s.loc[z.idxmax(), "student"], "top_student")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
m, sd = students["math"].mean(), students["math"].std()
students["math_z"] = (students["math"] - m) / sd
top_student = students.loc[students["math_z"].idxmax(), "student"]
print(top_student)
```
hint: `(students["math"] - mean) / std`, then `idxmax()` to find the row.
:::

:::exercise IQR outliers in rain
Load `weather.csv` and keep only London. Using the IQR rule on `rain_mm`, store the number of **high** outlier days (above Q3 + 1.5 × IQR) in `wet_outliers`.
```python starter
import pandas as pd

weather = pd.read_csv("weather.csv")

```
```python check
import pandas as pd
w = pd.read_csv("weather.csv")
r = w.loc[w["city"] == "London", "rain_mm"]
q1, q3 = r.quantile([0.25, 0.75])
same(int(need("wet_outliers")), int((r > q3 + 1.5 * (q3 - q1)).sum()), "wet_outliers")
```
```python solution
import pandas as pd

weather = pd.read_csv("weather.csv")
rain = weather.loc[weather["city"] == "London", "rain_mm"]
q1, q3 = rain.quantile([0.25, 0.75])
iqr = q3 - q1
wet_outliers = (rain > q3 + 1.5 * iqr).sum()
print(wet_outliers)
```
hint: Filter London, find `q1, q3 = rain.quantile([0.25, 0.75])`, then count values above `q3 + 1.5 * (q3 - q1)`.
:::

:::quiz
? A histogram has a long tail to the right. What's true?
+ It's right-skewed and the mean is above the median
- It's left-skewed
- The mean and median are equal
= The tail of large values pulls the mean up, above the median.
? A value has z = -2. What does that mean?
- It's 2 units below the mean
+ It's 2 standard deviations below the mean
- It's an error
= z-scores count standard deviations, so -2 is well below average.
? Why is the IQR rule better than the z-score rule for skewed data?
- It finds more outliers
+ It doesn't assume the data is symmetric, and outliers don't distort it
- It's faster
= The mean and std are themselves pulled by skew and outliers; quartiles aren't.
:::

@@@ lesson
id: categorical-data
title: Categorical data: counts, shares and charts
minutes: 15
summary: Summarise categories with counts and percentages, compare two categories with a two-way table, and choose bar charts over pie charts.
---
For categories (city, product, yes/no) there's no mean or standard deviation. You count, and you turn counts into **proportions** (shares).

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
counts = customers["segment"].value_counts()
shares = customers["segment"].value_counts(normalize=True)
print(pd.DataFrame({"count": counts, "share": shares.round(3)}))
```

A proportion is always between 0 and 1. For yes/no data stored as 1/0, the **mean is the proportion of 1s**, a trick you'll use constantly in A/B testing:

```python
import pandas as pd

ab = pd.read_csv("ab_test.csv")
print("conversion rate:", round(ab["converted"].mean(), 4))
print("same as:", ab["converted"].sum(), "/", len(ab))
```

### Bar charts beat pie charts

![The same three shares drawn as a pie chart and as a sorted bar chart](figures/bar-vs-pie.svg)

People compare lengths far more accurately than angles. With two or three slices a pie is fine for "part of a whole", but with more categories, or when the values are close, use a **sorted bar chart**:

```python
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("sales.csv")
counts = sales["product"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(counts.index, counts.values, color="teal")
ax.set_xlabel("orders")
ax.set_title("Orders by product")
plt.show()
```

### Two categories together: two-way tables

A **two-way table** (contingency table) counts every combination of two categories. `pd.crosstab` builds it:

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
print(pd.crosstab(customers["city"], customers["segment"], margins=True))
```

Raw counts are hard to compare when groups differ in size, so convert each row to percentages with `normalize="index"`. This answers "within each city, what share is each segment?":

```python
import pandas as pd

customers = pd.read_csv("customers.csv")
pct = pd.crosstab(customers["city"], customers["segment"], normalize="index") * 100
print(pct.round(0))
```

![A 100% stacked bar per city showing the share of Business, Consumer and Student customers](figures/stacked-bar.svg)

Each bar adds up to 100%, so you compare the mix, not the size. In Part 4 you'll test whether differences like these are real or just chance (the chi-square test).

### Proportions by group

`groupby` with the mean of a 0/1 column gives a rate per group:

```python
import pandas as pd

ab = pd.read_csv("ab_test.csv")
print(ab.groupby(["device", "group"])["converted"].mean().unstack().round(3))
```

Desktop visitors convert more often than mobile ones in both versions of the page. Whenever groups differ like this, compare like with like.

:::exercise Segment shares
Load `customers.csv` and store the **percentage** of customers in each `segment` in `seg_pct` (a Series that adds up to 100).
```python starter
import pandas as pd

customers = pd.read_csv("customers.csv")

```
```python check
import pandas as pd
c = pd.read_csv("customers.csv")
exp = c["segment"].value_counts(normalize=True) * 100
got = need("seg_pct", pd.Series)
for k in exp.index:
    same(float(got[k]), float(exp[k]), f"seg_pct[{k!r}]")
```
```python solution
import pandas as pd

customers = pd.read_csv("customers.csv")
seg_pct = customers["segment"].value_counts(normalize=True) * 100
print(seg_pct.round(1))
```
hint: `value_counts(normalize=True)` gives shares; multiply by 100.
:::

:::exercise Conversion by device
Load `ab_test.csv` and store each `device`'s conversion rate (the mean of `converted`) in `rate_by_device`. Store the name of the device with the higher rate in `better_device`.
```python starter
import pandas as pd

ab = pd.read_csv("ab_test.csv")

```
```python check
import pandas as pd
a = pd.read_csv("ab_test.csv")
r = a.groupby("device")["converted"].mean()
got = need("rate_by_device", pd.Series)
for k in r.index:
    same(float(got[k]), float(r[k]), f"rate_by_device[{k!r}]")
same(need("better_device"), r.idxmax(), "better_device")
```
```python solution
import pandas as pd

ab = pd.read_csv("ab_test.csv")
rate_by_device = ab.groupby("device")["converted"].mean()
better_device = rate_by_device.idxmax()
print(rate_by_device.round(3))
print(better_device)
```
hint: `ab.groupby("device")["converted"].mean()`, then `idxmax()`.
:::

:::quiz
? What is the mean of a column of 1s and 0s?
- Always 0.5
+ The proportion of 1s
- The number of 1s
= Adding 1s counts them; dividing by the total turns the count into a share.
? Why prefer a sorted bar chart to a pie chart with seven slices?
+ People compare lengths more accurately than angles
- Pie charts can't show percentages
- Bar charts use less ink
= With many similar slices, a pie becomes guesswork; bars make the ranking obvious.
? What does `normalize="index"` do in `pd.crosstab`?
- Sorts the rows
+ Turns each row into percentages of that row's total
- Removes missing values
= Each row then adds up to 1 (or 100%), so groups of different sizes can be compared.
:::
