@@@ part
id: 5
title: Relationships and Regression
level: Advanced
blurb: Measure how two variables move together, fit a line to predict one from another, and use multiple regression to separate the effects of several factors.

@@@ lesson
id: correlation
title: Correlation
minutes: 18
summary: Scatter plots, Pearson's r, Spearman's rank correlation, testing a correlation, correlation matrices, and why correlation isn't causation.
---
"Do students who study more score higher?" is a question about two numerical variables moving together. Start with a picture: the **scatter plot**.

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.scatter(students["hours_studied"], students["math"], color="teal")
ax.set_xlabel("hours studied per week")
ax.set_ylabel("math score")
ax.set_title("Study time and math scores")
plt.show()
```

The points drift upwards: more hours tend to go with higher scores. A **correlation coefficient** puts a number on that.

### Pearson's r

**Pearson's correlation r** measures how closely points follow a **straight line**:

| r | Meaning |
|---|---|
| +1 | a perfect upward line |
| about +0.7 | a strong upward trend |
| about +0.3 | a weak upward trend |
| 0 | no straight-line relationship |
| negative | a downward trend (as one rises, the other falls) |

![Five scatter plots: r = -0.9 and -0.4 slope down, r = 0.4 and 0.9 slope up, and a U-shaped curve has r close to 0 even though x and y are clearly related](figures/correlation-gallery.svg)

The last panel is the classic warning: x and y are perfectly related by a curve, but r is about 0, because r only measures **straight-line** relationships. Always look at the scatter plot.

```python
import pandas as pd

students = pd.read_csv("students.csv")
print("hours vs math:     ", round(students["hours_studied"].corr(students["math"]), 2))
print("attendance vs math:", round(students["attendance_pct"].corr(students["math"]), 2))
print("attendance vs english:", round(students["attendance_pct"].corr(students["english"]), 2))
```

### Is the correlation real? Testing r

A correlation from a small sample could be luck. `stats.pearsonr` gives r with a p-value (H₀: the true correlation is 0) and a confidence interval:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
res = stats.pearsonr(students["hours_studied"], students["math"])
ci = res.confidence_interval(0.95)
print(f"r = {res.statistic:.2f}, p = {res.pvalue:.1e}, 95% CI {ci.low:.2f} to {ci.high:.2f}")
```

### Spearman's rank correlation

**Spearman's ρ** (rho) correlates the **ranks** instead of the values. It measures any steadily increasing or decreasing relationship (not just straight lines), and outliers can't dominate it:

```python
import numpy as np
from scipy import stats

x = np.arange(1, 11)
y = x ** 3                    # always rising, but curved
y_outlier = x.astype(float)
y_outlier[-1] = 100           # a straight line plus one wild value

print("curve:   Pearson", round(stats.pearsonr(x, y).statistic, 3), " Spearman", round(stats.spearmanr(x, y).statistic, 3))
print("outlier: Pearson", round(stats.pearsonr(x, y_outlier).statistic, 3), " Spearman", round(stats.spearmanr(x, y_outlier).statistic, 3))
```

Use Spearman for ranks, ordinal data (ratings 1–5), skewed data or data with outliers.

### Correlation matrices and heatmaps

`df.corr()` correlates every pair of columns at once. A **heatmap** makes the pattern easy to scan:

```python
import pandas as pd
import matplotlib.pyplot as plt

students = pd.read_csv("students.csv")
cols = ["hours_studied", "attendance_pct", "math", "science", "english"]
corr = students[cols].corr()
print(corr.round(2))

fig, ax = plt.subplots(figsize=(5.5, 4.5))
im = ax.imshow(corr, cmap="RdBu", vmin=-1, vmax=1)
ax.set_xticks(range(len(cols)), cols, rotation=45, ha="right")
ax.set_yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
fig.colorbar(im)
ax.set_title("Correlation matrix")
plt.show()
```

### Correlation is not causation

Ice-cream sales and drownings are correlated, because both rise in hot weather. A correlation can come from:

- **causation:** studying causes higher scores (probably partly true here);
- **reverse causation:** the arrow points the other way (students who are already good may enjoy studying more);
- a **confounder:** a third variable driving both (hot weather; or a student's motivation, which drives both hours and scores);
- **coincidence:** with enough variables, some correlate by chance.

To claim causation you need an **experiment** (randomly assign who gets the treatment, as in an A/B test) or careful methods that control for confounders. Regression, next, is the first step.

:::exercise Strongest link
Load `students.csv`. Among `hours_studied`, `attendance_pct`, `science` and `english`, find the variable with the **strongest** correlation with `math` (largest Pearson r). Store its name in `strongest` and its r in `r_value`.
```python starter
import pandas as pd

students = pd.read_csv("students.csv")

```
```python check
import pandas as pd
s = pd.read_csv("students.csv")
c = s[["hours_studied", "attendance_pct", "science", "english"]].corrwith(s["math"])
same(need("strongest"), c.abs().idxmax(), "strongest")
same(float(need("r_value")), float(c[c.abs().idxmax()]), "r_value")
```
```python solution
import pandas as pd

students = pd.read_csv("students.csv")
cols = ["hours_studied", "attendance_pct", "science", "english"]
r = students[cols].corrwith(students["math"])
strongest = r.abs().idxmax()
r_value = r[strongest]
print(r.round(2))
print(strongest, round(r_value, 2))
```
hint: `students[cols].corrwith(students["math"])` gives one r per column; `idxmax()` finds the biggest.
:::

:::exercise Pearson vs Spearman on houses
Load `housing.csv`. Store Pearson's r between `distance_km` and `price_k` in `pearson_r`, its p-value in `pearson_p`, and Spearman's ρ between the same columns in `spearman_rho`.
```python starter
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from scipy import stats
h = pd.read_csv("housing.csv")
r = stats.pearsonr(h["distance_km"], h["price_k"])
same(float(need("pearson_r")), float(r.statistic), "pearson_r")
same(float(need("pearson_p")), float(r.pvalue), "pearson_p")
same(float(need("spearman_rho")), float(stats.spearmanr(h["distance_km"], h["price_k"]).statistic), "spearman_rho")
```
```python solution
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
res = stats.pearsonr(housing["distance_km"], housing["price_k"])
pearson_r, pearson_p = res.statistic, res.pvalue
spearman_rho = stats.spearmanr(housing["distance_km"], housing["price_k"]).statistic
print(round(pearson_r, 3), pearson_p, round(spearman_rho, 3))
```
hint: `stats.pearsonr(x, y)` returns `.statistic` and `.pvalue`; `stats.spearmanr(x, y).statistic` gives ρ.
:::

:::quiz
? r = -0.8 between price and sales means:
+ A strong tendency for sales to fall as price rises
- Price has no effect on sales
- 80% of sales are caused by price
= The sign gives the direction and the size gives the strength of the straight-line relationship.
? Two variables have r ≈ 0. Can they still be strongly related?
+ Yes, by a curve, which r doesn't measure
- No, r ≈ 0 means unrelated
- Only if the sample is small
= r only measures straight-line relationships. Look at the scatter plot.
? Towns with more firefighters have more fire damage. The best explanation is:
- Firefighters cause damage
+ A confounder: bigger fires bring both more firefighters and more damage
- Coincidence
= A third variable (fire size) drives both. Correlation alone can't show cause.
:::

@@@ lesson
id: linear-regression
title: Simple linear regression
minutes: 22
summary: Fit the best straight line, read the slope and intercept, measure fit with R², check residuals, predict, and test the slope.
---
Correlation says "these move together". **Regression** goes further: it finds the line that best **predicts** one variable (the **outcome**, y) from another (the **predictor**, x):

y ≈ intercept + slope × x

- The **slope** is how much y changes, on average, when x goes up by 1.
- The **intercept** is the predicted y when x is 0.

### Least squares

Which line is "best"? For each point, the vertical gap between the actual y and the line's prediction is the **residual**. **Least squares** picks the line that makes the **sum of squared residuals** as small as possible.

![Math scores against study hours, with an orange fitted line and a grey vertical segment from each point to the line showing its residual](figures/regression-line.svg)

`stats.linregress` fits it:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
fit = stats.linregress(students["hours_studied"], students["math"])
print(f"math ≈ {fit.intercept:.1f} + {fit.slope:.2f} × hours")
print(f"r = {fit.rvalue:.2f}, R² = {fit.rvalue ** 2:.2f}, p-value for the slope = {fit.pvalue:.1e}")
```

**Read it in words:** each extra hour of study per week goes with about 4.5 more points in math, on average. A student who studies 0 hours is predicted to score about 32 (but no student studied 0 hours, so don't lean on that number).

### Predicting

Plug a new x into the equation:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
fit = stats.linregress(students["hours_studied"], students["math"])
for hours in (3, 6, 9):
    print(f"{hours} hours → predicted math {fit.intercept + fit.slope * hours:.1f}")
```

Only predict **within the range of the data** (here, about 1 to 10 hours). Predicting for 30 hours a week is **extrapolation**: the line might give a score over 100, which is impossible. Straight lines don't go on forever in real life.

### R²: how much does the line explain?

**R²** (the coefficient of determination) is the share of the variation in y that the line explains, from 0 to 1. With one predictor, it's simply r². An R² of 0.5 means study hours explain about half of the differences in math scores; the other half comes from everything else (talent, sleep, luck…).

```python
import numpy as np
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
x, y = students["hours_studied"], students["math"]
fit = stats.linregress(x, y)
predicted = fit.intercept + fit.slope * x
residuals = y - predicted

ss_total = ((y - y.mean()) ** 2).sum()      # total variation around the mean
ss_resid = (residuals ** 2).sum()            # variation the line doesn't explain
print("R² by hand:", round(1 - ss_resid / ss_total, 3), " r²:", round(fit.rvalue ** 2, 3))
print("typical prediction error (residual std):", round(np.std(residuals, ddof=2), 1), "points")
```

### Checking the residuals

A line is only a good summary if the residuals look like **random noise**: no pattern, roughly the same spread everywhere. A **residual plot** (residuals against predictions) shows problems that R² hides:

```python
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

students = pd.read_csv("students.csv")
x, y = students["hours_studied"], students["math"]
fit = stats.linregress(x, y)
predicted = fit.intercept + fit.slope * x

fig, ax = plt.subplots(figsize=(6, 3))
ax.scatter(predicted, y - predicted, color="teal")
ax.axhline(0, color="darkorange")
ax.set_xlabel("predicted math")
ax.set_ylabel("residual")
ax.set_title("Residuals: no pattern is good news")
plt.show()
```

| Residual plot shows | Problem | Try |
|---|---|---|
| a curve | the relationship isn't a straight line | add x², or transform x or y |
| a funnel (spread grows) | the error isn't constant | log-transform y |
| a few far-off points | outliers with big influence | investigate them |

### Is the slope real?

`linregress` also tests H₀: slope = 0 (no relationship). `fit.pvalue` is that test's p-value and `fit.stderr` the slope's standard error, so a 95% confidence interval for the slope is:

```python
import pandas as pd
from scipy import stats

students = pd.read_csv("students.csv")
fit = stats.linregress(students["hours_studied"], students["math"])
t = stats.t.ppf(0.975, len(students) - 2)
print(f"slope {fit.slope:.2f}, 95% CI {fit.slope - t * fit.stderr:.2f} to {fit.slope + t * fit.stderr:.2f}")
```

The whole interval is well above 0, so the relationship is very unlikely to be luck. The degrees of freedom are n − 2, because the line used up two numbers (slope and intercept).

### Regression to the mean

A side effect of imperfect correlation: extreme values tend to be followed by less extreme ones. Students with the very best scores on one test usually score a bit lower on the next, not because they got worse, but because some of their first score was luck. Keep this in mind before crediting a "fix" applied only to the worst performers.

:::exercise Size and price
Load `housing.csv` and fit `price_k` against `area_sqm` with `stats.linregress`. Store the slope in `slope`, R² in `r_squared`, and the predicted price of a **100 m²** home in `pred_100`.
```python starter
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from scipy import stats
h = pd.read_csv("housing.csv")
f = stats.linregress(h["area_sqm"], h["price_k"])
same(float(need("slope")), float(f.slope), "slope")
same(float(need("r_squared")), float(f.rvalue ** 2), "r_squared")
same(float(need("pred_100")), float(f.intercept + f.slope * 100), "pred_100")
```
```python solution
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
fit = stats.linregress(housing["area_sqm"], housing["price_k"])
slope = fit.slope
r_squared = fit.rvalue ** 2
pred_100 = fit.intercept + fit.slope * 100
print(round(slope, 2), round(r_squared, 3), round(pred_100, 1))
```
hint: x is `area_sqm`, y is `price_k`. R² is `fit.rvalue ** 2`.
:::

:::exercise Residuals by hand
Using the same fit (`price_k` on `area_sqm`), add a column `residual` to `housing` (actual price minus predicted price). Store the `home_id` of the home the line **underestimates** the most (the largest positive residual) in `underpriced_id`.
```python starter
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from scipy import stats
h = pd.read_csv("housing.csv")
f = stats.linregress(h["area_sqm"], h["price_k"])
res = h["price_k"] - (f.intercept + f.slope * h["area_sqm"])
got = need("housing", pd.DataFrame)
same(got["residual"], res, "housing['residual']")
same(int(need("underpriced_id")), int(h.loc[res.idxmax(), "home_id"]), "underpriced_id")
```
```python solution
import pandas as pd
from scipy import stats

housing = pd.read_csv("housing.csv")
fit = stats.linregress(housing["area_sqm"], housing["price_k"])
housing["residual"] = housing["price_k"] - (fit.intercept + fit.slope * housing["area_sqm"])
underpriced_id = housing.loc[housing["residual"].idxmax(), "home_id"]
print(underpriced_id)
```
hint: Residual = actual − (intercept + slope × area). The biggest positive residual is the home that costs much more than its size predicts.
:::

:::quiz
? A regression gives sales ≈ 200 + 15 × ads. What does 15 mean?
+ Each extra ad goes with about 15 more sales, on average
- 15% of sales come from ads
- Sales are 15 when there are no ads
= The slope is the average change in y per one-unit increase in x.
? R² = 0.36 means:
- The correlation is 0.36
+ The line explains about 36% of the variation in y
- 36% of predictions are correct
= R² is the share of variation explained; here r would be ±0.6.
? Why is predicting far outside the data's range risky?
- The formula stops working
+ The straight-line pattern may not continue there (extrapolation)
- R² becomes negative
= You have no evidence about how the relationship behaves beyond the data.
:::

@@@ lesson
id: multiple-regression
title: Multiple regression
minutes: 24
summary: Predict from several variables with statsmodels, read "holding the others fixed", use categories with dummy variables, compare models, and watch for multicollinearity.
---
House prices depend on size, but also on age, location and the number of bedrooms. **Multiple regression** fits all of them at once:

price ≈ b₀ + b₁ × area + b₂ × bedrooms + b₃ × age + …

Each **coefficient** (b₁, b₂…) is the effect of one variable **holding the others fixed**. That's the big advantage over looking at one variable at a time: it separates effects that come tangled together.

### Fitting with statsmodels

**statsmodels** is Python's main library for statistical models. Its formula interface reads like the equation: `"outcome ~ predictor1 + predictor2"`:

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km", data=housing).fit()
print(model.params.round(2))
print("R²:", round(model.rsquared, 3))
```

OLS stands for **ordinary least squares**, the same "smallest squared residuals" idea as before.

**Reading the coefficients:**

- `area_sqm` ≈ 3: each extra square metre adds about 3 (thousand) to the price, for homes with the same bedrooms, age and distance;
- `age_years` is negative: older homes are cheaper, other things equal;
- `distance_km` is negative: each km from the centre lowers the price.

### The summary table

`model.summary()` prints everything: coefficients, their standard errors, p-values and confidence intervals. The middle table is the important part:

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km", data=housing).fit()
table = pd.DataFrame({"coef": model.params, "p-value": model.pvalues}).join(model.conf_int().rename(columns={0: "CI low", 1: "CI high"}))
print(table.round(3))
```

Each p-value tests H₀: "this coefficient is 0, once the others are included". A predictor can look important on its own but become non-significant in a multiple regression, because another variable was already carrying its information.

### Categories as predictors: dummy variables

Neighbourhood is a category. Wrap it in `C(...)` and statsmodels creates **dummy variables** (0/1 columns), one per category except a **reference** category that the others are compared with:

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
print(model.params.round(1))
print("R²:", round(model.rsquared, 3), " adjusted R²:", round(model.rsquared_adj, 3))
```

Central is the reference (it's first alphabetically). `C(neighborhood)[T.Hillside]` ≈ −95 means: a Hillside home costs about 95 thousand **less than a Central home of the same size, age, bedrooms and distance**.

![Coefficients with 95% confidence intervals: per extra bedroom and per extra square metre are positive; per year of age and per km from the centre are slightly negative; Riverside and Hillside are well below Central](figures/coefficients.svg)

A coefficient plot like this shows every effect with its uncertainty: intervals that cross the dashed zero line are effects you can't be sure of.

### Comparing models: adjusted R²

Adding any variable, even pure noise, never lowers R². **Adjusted R²** penalises extra variables, so it only rises when a variable genuinely helps:

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
housing["noise"] = np.random.default_rng(0).normal(size=len(housing))
for formula in ["price_k ~ area_sqm",
                "price_k ~ area_sqm + C(neighborhood)",
                "price_k ~ area_sqm + C(neighborhood) + noise"]:
    m = smf.ols(formula, data=housing).fit()
    print(f"{formula:45} R² {m.rsquared:.3f}  adjusted {m.rsquared_adj:.3f}")
```

### Predicting

```python
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
new_homes = pd.DataFrame({
    "area_sqm": [80, 120], "bedrooms": [2, 4], "age_years": [10, 40],
    "distance_km": [2.0, 8.0], "neighborhood": ["Central", "Hillside"],
})
print(model.predict(new_homes).round(1))
```

### Checking the model

The same checks as simple regression apply: a residual plot should look like a shapeless cloud.

![Residuals of the house-price model plotted against predicted prices: a shapeless cloud around zero](figures/residual-plot.svg)

### Multicollinearity

When predictors are strongly correlated with each other (area and bedrooms here: bigger homes have more bedrooms), the model struggles to separate their effects: coefficients get wide confidence intervals and can even flip sign. Check the correlation between predictors, or the **variance inflation factor** (VIF; above about 5 to 10 is a warning):

```python
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

housing = pd.read_csv("housing.csv")
X = sm.add_constant(housing[["area_sqm", "bedrooms", "age_years", "distance_km"]])
print("area vs bedrooms r:", round(housing["area_sqm"].corr(housing["bedrooms"]), 2))
for i, col in enumerate(X.columns[1:], start=1):
    print(f"VIF {col}: {variance_inflation_factor(X.values, i):.1f}")
```

### Regression and machine learning

This is the same linear regression that machine learning libraries like scikit-learn fit. Statistics focuses on **understanding** the coefficients (effects, intervals, p-values); machine learning focuses on **predicting** new cases well and checks that on held-out data. The next course in the core path, machine learning, starts from here.

:::exercise Model the price
Load `housing.csv` and fit `price_k ~ area_sqm + age_years + distance_km + C(neighborhood)` with `smf.ols`. Store the fitted model in `model`, its adjusted R² in `adj_r2`, and the coefficient for `age_years` in `age_coef`.
```python starter
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
import statsmodels.formula.api as smf
h = pd.read_csv("housing.csv")
m = smf.ols("price_k ~ area_sqm + age_years + distance_km + C(neighborhood)", data=h).fit()
same(float(need("adj_r2")), float(m.rsquared_adj), "adj_r2")
same(float(need("age_coef")), float(m.params["age_years"]), "age_coef")
```
```python solution
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + age_years + distance_km + C(neighborhood)", data=housing).fit()
adj_r2 = model.rsquared_adj
age_coef = model.params["age_years"]
print(round(adj_r2, 3), round(age_coef, 2))
```
hint: `smf.ols("price_k ~ ...", data=housing).fit()`, then `.rsquared_adj` and `.params["age_years"]`.
:::

:::exercise Predict a home
Using the model `price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)`, store the predicted price of a **95 m², 3-bedroom, 20-year-old Riverside home 5 km from the centre** in `predicted` (a single number).
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
p = m.predict(pd.DataFrame({"area_sqm": [95], "bedrooms": [3], "age_years": [20], "distance_km": [5.0], "neighborhood": ["Riverside"]})).iloc[0]
same(float(need("predicted")), float(p), "predicted")
```
```python solution
import pandas as pd
import statsmodels.formula.api as smf

housing = pd.read_csv("housing.csv")
model = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=housing).fit()
home = pd.DataFrame({"area_sqm": [95], "bedrooms": [3], "age_years": [20],
                     "distance_km": [5.0], "neighborhood": ["Riverside"]})
predicted = model.predict(home).iloc[0]
print(round(predicted, 1))
```
hint: Build a one-row DataFrame with every predictor column, then `model.predict(df).iloc[0]`.
:::

:::quiz
? In a multiple regression, the coefficient for age is -0.9. What does it mean?
+ Each extra year of age lowers the predicted price by about 0.9, holding the other variables fixed
- Age explains 90% of the price
- Older homes are always cheaper
= Coefficients are effects with the other predictors held constant.
? Why prefer adjusted R² when comparing models with different numbers of predictors?
- It's always higher
+ Plain R² rises with any added variable, even noise; adjusted R² penalises extras
- It's easier to calculate
= Adjusted R² only increases when a variable improves the model more than chance would.
? What's multicollinearity?
- Too many rows
+ Predictors that are strongly correlated with each other, making their separate effects hard to estimate
- Residuals that form a curve
= Correlated predictors give unstable coefficients with wide intervals.
:::
