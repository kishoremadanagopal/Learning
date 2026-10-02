@@@ part
id: 2
title: Regression: Predicting Numbers
level: Beginner
blurb: Predict prices, scores and energy use with linear models, measure the errors honestly, and see overfitting and its cure with your own eyes.

@@@ lesson
id: linear-regression
title: Linear regression with many features
minutes: 16
summary: How a linear model combines several features, how to read its coefficients, and how to check its predictions against reality.
---
In Lesson 2 you predicted maths scores from one feature, hours studied: the model drew a line. With several features, a **linear regression** does the same thing in more directions at once. For homes it learns a recipe like:

> price = intercept + (a × area) + (b × bedrooms) + (c × age) + (d × distance)

Training finds the numbers `a`, `b`, `c` and `d` (the **coefficients**) and the **intercept** that make the predictions as close as possible to the real prices in the training data. "As close as possible" has a precise meaning: it makes the **sum of squared errors** as small as it can be, which is why this method is called **least squares**.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

model = LinearRegression().fit(X_train, y_train)
print("intercept:", round(model.intercept_, 1))
print(pd.Series(model.coef_, index=X.columns).round(2))
```

### Reading the coefficients

Prices are in thousands, so each coefficient is "thousands of pounds per unit":

| Feature | Coefficient | In words |
|---|---|---|
| `area_sqm` | 3.13 | each extra m² adds about 3,100 to the price |
| `bedrooms` | 13.32 | each extra bedroom adds about 13,000 |
| `age_years` | −0.63 | each year older takes off about 600 |
| `distance_km` | −7.35 | each km further from the centre takes off about 7,400 |

Each coefficient is the effect of one feature **while the others stay the same**. "An extra bedroom adds 13,000" means: two homes with the same area, age and distance, one of which has an extra bedroom. That's not the same as "homes with more bedrooms cost 13,000 more", because homes with more bedrooms also tend to be bigger.

Two cautions:

- **Units matter.** A coefficient's size depends on its feature's units. Area's 3.13 looks small next to bedrooms' 13.32, but area changes by tens of m² between homes. Don't compare coefficient sizes to decide which feature "matters most" (Lesson 8 shows how to compare fairly).
- **Prediction is not cause.** The model learns patterns in this data. It can't tell you that adding a bedroom to **your** home will raise its value by 13,000.

### Predicting a new home

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
model = LinearRegression().fit(X_train, y_train)

new_home = pd.DataFrame({"area_sqm": [90], "bedrooms": [3], "age_years": [20], "distance_km": [5.0]})
print("predicted price (thousands):", model.predict(new_home).round(1))
```

You can check the arithmetic by hand: 114.6 + 3.13×90 + 13.32×3 − 0.63×20 − 7.35×5 ≈ 387. That's all a linear model is.

### Predicted versus actual

The best quick check of a regression model is a scatter of **predicted** against **actual** values for the test set. A perfect model puts every point on the diagonal line.

![Scatter of predicted price against actual price for 40 test homes. The points lie close to the dashed diagonal "perfect prediction" line, with some homes well above or below it](figures/predicted-vs-actual.svg)

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
pred = LinearRegression().fit(X_train, y_train).predict(X_test)

plt.scatter(y_test, pred)
plt.plot([200, 650], [200, 650], linestyle="--", color="grey")   # the "perfect" line
plt.xlabel("actual price (thousands)")
plt.ylabel("predicted price (thousands)")
plt.title("Test homes: predicted vs actual")
plt.show()
```

Points above the line are homes the model **over**-priced; points below were **under**-priced. Most are close, but some are off by 100 or more. Part of that is because the model can't see one important feature yet: the neighbourhood, which is text. You'll add it in Lesson 16.

:::exercise The distance effect
Using the split below, fit a `LinearRegression` called `model` on the training data. Store the coefficient for `distance_km` in `dist_coef` (a single number).
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=2)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
h = pd.read_csv("housing.csv")
a, b, c, d = train_test_split(h[["area_sqm", "bedrooms", "distance_km"]], h["price_k"], test_size=0.25, random_state=2)
ref = LinearRegression().fit(a, c)
m = need("model", LinearRegression)
if not hasattr(m, "coef_"):
    raise AssertionError("Fit the model with model.fit(X_train, y_train).")
same(float(need("dist_coef")), float(ref.coef_[2]), "dist_coef (the third coefficient, trained on X_train)", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=2)

model = LinearRegression().fit(X_train, y_train)
dist_coef = model.coef_[2]          # same order as X's columns
print(pd.Series(model.coef_, index=X.columns).round(2))
```
hint: `model.coef_` lists the coefficients in the same order as `X`'s columns; `distance_km` is the third one, `model.coef_[2]`.
:::

:::exercise Price a flat
Fit a `LinearRegression` on **all** 160 homes (no split this time) using `area_sqm`, `bedrooms`, `age_years` and `distance_km`. Store the predicted price of a 60 m², 2-bedroom, 45-year-old flat 1.5 km from the centre in `flat_price` (a single number, in thousands).
```python starter
import pandas as pd
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from sklearn.linear_model import LinearRegression
h = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km"]
ref = LinearRegression().fit(h[cols], h["price_k"])
row = pd.DataFrame({"area_sqm": [60], "bedrooms": [2], "age_years": [45], "distance_km": [1.5]})
same(float(need("flat_price")), float(ref.predict(row)[0]), "flat_price", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
cols = ["area_sqm", "bedrooms", "age_years", "distance_km"]
model = LinearRegression().fit(housing[cols], housing["price_k"])

flat = pd.DataFrame({"area_sqm": [60], "bedrooms": [2], "age_years": [45], "distance_km": [1.5]})
flat_price = model.predict(flat)[0]
print(round(flat_price, 1))
```
hint: Build a one-row DataFrame with the same four columns, then take `model.predict(flat)[0]`.
:::

:::quiz
? A linear model's coefficient for age_years is -0.63 (prices in thousands). What does it mean?
+ Each extra year of age lowers the predicted price by about 630, other features unchanged
- Older homes are 63% cheaper
- Age explains 63% of the price
= A coefficient is the change in prediction per unit of the feature, holding the others fixed.
? Why shouldn't you compare raw coefficient sizes to find the most important feature?
- Because coefficients are random
+ Because each depends on its feature's units: per m², per bedroom, per km
- Because negative coefficients don't count
= A feature measured in small units gets a small coefficient even if it matters a lot. Scale features first (Lesson 8 and 15).
? On a predicted-vs-actual plot, a point far above the diagonal is a home the model:
+ Priced too high
- Priced too low
- Priced perfectly
= Above the line means predicted > actual.
? "Least squares" means the model chooses coefficients that:
- Use the fewest features
+ Make the sum of squared errors on the training data as small as possible
- Make every error exactly zero
= Squaring makes every error positive and punishes big misses more.
:::

@@@ lesson
id: regression-metrics
title: Measuring regression errors
minutes: 15
summary: MAE, MSE, RMSE and R²: what each one means, how to compute them, and which to report.
---
A regression model is never exactly right, so you need a number that says **how wrong** it is, on average, on the test set. Every metric starts from the **errors**, also called **residuals**: actual minus predicted, one per test row.

![Eight points and a fitted line, with a vertical segment from each point to the line. The segments are the errors (residuals); MAE averages their lengths, RMSE squares them first so long segments count more](figures/residuals.svg)

| Metric | How it's made | Units | Good value | Read it as |
|---|---|---|---|---|
| **MAE** (mean absolute error) | average of the error sizes | same as y (thousands) | small | "typically off by this much" |
| **MSE** (mean squared error) | average of squared errors | y squared | small | hard to read; used in training |
| **RMSE** (root mean squared error) | square root of MSE | same as y | small | like MAE, but big misses count extra |
| **R²** (coefficient of determination) | 1 − (model's squared errors ÷ baseline's) | none | close to 1 | share of the variation the model explains |

### Computing them by hand, then with scikit-learn

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
pred = LinearRegression().fit(X_train, y_train).predict(X_test)

errors = y_test - pred
print("first five errors:", errors.head().round(1).tolist())
print("MAE: ", np.abs(errors).mean().round(1))
print("MSE: ", (errors ** 2).mean().round(1))
print("RMSE:", np.sqrt((errors ** 2).mean()).round(1))
```

The same, using `sklearn.metrics`. Every metric function takes **actual first, predicted second**:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
model = LinearRegression().fit(X_train, y_train)
pred = model.predict(X_test)

print("MAE: ", round(mean_absolute_error(y_test, pred), 1))
print("MSE: ", round(mean_squared_error(y_test, pred), 1))
print("RMSE:", round(root_mean_squared_error(y_test, pred), 1))
print("R²:  ", round(r2_score(y_test, pred), 3))
print("R² from model.score:", round(model.score(X_test, y_test), 3))
```

In words: the model's price is typically off by about **41 thousand** (MAE), big misses push RMSE up to **50 thousand**, and it explains about **82%** of the variation in test prices (R²). `model.score` gives the same R² for any regressor.

### Understanding R²

R² compares your model with the baseline that always predicts the average:

- **R² = 1**: perfect predictions.
- **R² = 0**: no better than guessing the average for every row.
- **R² < 0**: **worse** than guessing the average. It happens with bad models, and you saw a slightly negative baseline in Lesson 4.

R² has no units, so it's handy for comparing across problems. MAE and RMSE are in the label's units, so they're what you tell people: "our price estimate is typically within 41,000".

### MAE or RMSE?

RMSE is always at least as big as MAE. The gap tells you something: if RMSE is much bigger, a few predictions are **very** wrong. Choose based on what hurts:

- Is a 100k miss twice as bad as a 50k miss? Use **MAE**.
- Is a 100k miss much worse than two 50k misses (a big surprise could sink a budget)? Use **RMSE**, which punishes big errors more.

### Look at the residuals too

A single number hides patterns. Plot the residuals against the predictions: a healthy model shows a shapeless cloud around zero. A curve or a funnel means the model is missing something.

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
pred = LinearRegression().fit(X_train, y_train).predict(X_test)

plt.scatter(pred, y_test - pred)
plt.axhline(0, color="grey", linestyle="--")
plt.xlabel("predicted price")
plt.ylabel("residual (actual - predicted)")
plt.title("Residuals of the test homes")
plt.show()
```

:::exercise Three numbers for the report
Using the model and split below, compute the test-set `mae`, `rmse` and `r2` with `sklearn.metrics`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

students = pd.read_csv("students.csv")
X = students[["hours_studied", "attendance_pct"]]
y = students["math"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)
model = LinearRegression().fit(X_train, y_train)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
s = pd.read_csv("students.csv")
a, b, c, d = train_test_split(s[["hours_studied", "attendance_pct"]], s["math"], test_size=0.3, random_state=4)
p = LinearRegression().fit(a, c).predict(b)
same(float(need("mae")), mean_absolute_error(d, p), "mae (on the test set)")
same(float(need("rmse")), root_mean_squared_error(d, p), "rmse")
same(float(need("r2")), r2_score(d, p), "r2")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

students = pd.read_csv("students.csv")
X = students[["hours_studied", "attendance_pct"]]
y = students["math"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)
model = LinearRegression().fit(X_train, y_train)

pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
rmse = root_mean_squared_error(y_test, pred)
r2 = r2_score(y_test, pred)
print(round(mae, 2), round(rmse, 2), round(r2, 3))
```
hint: Predict on `X_test` first, then pass `(y_test, pred)` to each metric, actual first.
:::

:::exercise How much better than guessing?
With the same split, compute the test MAE of a `DummyRegressor()` in `base_mae` and of a `LinearRegression()` in `model_mae`, both trained on the training data. Store `base_mae - model_mae` in `saved`: how many points closer the model gets, on average.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

students = pd.read_csv("students.csv")
X = students[["hours_studied", "attendance_pct"]]
y = students["math"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
s = pd.read_csv("students.csv")
a, b, c, d = train_test_split(s[["hours_studied", "attendance_pct"]], s["math"], test_size=0.3, random_state=4)
bm = mean_absolute_error(d, DummyRegressor().fit(a, c).predict(b))
mm = mean_absolute_error(d, LinearRegression().fit(a, c).predict(b))
same(float(need("base_mae")), bm, "base_mae")
same(float(need("model_mae")), mm, "model_mae")
same(float(need("saved")), bm - mm, "saved")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

students = pd.read_csv("students.csv")
X = students[["hours_studied", "attendance_pct"]]
y = students["math"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4)

base_mae = mean_absolute_error(y_test, DummyRegressor().fit(X_train, y_train).predict(X_test))
model_mae = mean_absolute_error(y_test, LinearRegression().fit(X_train, y_train).predict(X_test))
saved = base_mae - model_mae
print(round(base_mae, 2), round(model_mae, 2), round(saved, 2))
```
hint: Same recipe twice: fit on the training data, predict `X_test`, then `mean_absolute_error(y_test, pred)`.
:::

:::quiz
? A price model has MAE = 41 (thousands). What's the plain-English reading?
+ Its predictions are typically off by about 41,000
- It's right 41% of the time
- It explains 41% of the variation
= MAE is in the label's units: the average size of the errors.
? RMSE is much bigger than MAE. What does that tell you?
- The model is perfect
+ A few predictions are very wrong
- You used the wrong units
= Squaring makes big errors count extra, so a big RMSE-MAE gap points to some large misses.
? A model has R² = -0.2 on the test set. That means:
- It explains 20% of the variation
+ It does worse than always predicting the average
- The metric is broken
= R² below 0 means the model loses to the simplest baseline.
? Which argument comes first in mean_absolute_error?
+ The actual values (y_test)
- The predictions
- It doesn't matter for any metric
= scikit-learn metrics are metric(y_true, y_pred). For MAE the order doesn't change the answer, but for many others (like precision) it does, so build the habit.
:::

@@@ lesson
id: overfitting
title: Underfitting and overfitting
minutes: 18
summary: Too simple misses the pattern; too complex learns the noise. See both on a curve, and find the sweet spot with a test set.
---
The `energy.csv` file has 40 days of outdoor temperature and an office building's energy use. Cold days need heating, hot days need air conditioning, so energy use is lowest in the middle: a U shape.

```python
import pandas as pd
import matplotlib.pyplot as plt

energy = pd.read_csv("energy.csv")
plt.scatter(energy["temperature_c"], energy["energy_kwh"])
plt.xlabel("outdoor temperature (°C)")
plt.ylabel("energy used (kWh)")
plt.title("Energy use: high when cold, high when hot")
plt.show()
```

A straight line can't follow a U. To fit curves, we can give a linear model extra features: temperature², temperature³ and so on. A model with powers up to 2 can draw a U; with higher powers it can draw ever wigglier curves. The **degree** is the highest power, and it controls how **flexible** (complex) the model is.

`make_pipeline` chains steps so they act like one model: make the powers, put them on a similar scale (so huge numbers like 30¹⁵ don't cause trouble), then fit the linear regression. Lesson 17 covers pipelines properly; for now, read it as "do these steps in order".

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X = energy[["temperature_c"]]
y = energy["energy_kwh"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

for degree in [1, 2, 10, 15]:
    model = make_pipeline(PolynomialFeatures(degree), StandardScaler(), LinearRegression())
    model.fit(X_train, y_train)
    train_rmse = root_mean_squared_error(y_train, model.predict(X_train))
    test_rmse = root_mean_squared_error(y_test, model.predict(X_test))
    print(f"degree {degree:>2}:  train RMSE {train_rmse:5.1f}   test RMSE {test_rmse:5.1f}")
```

Read the table from top to bottom:

- **Degree 1 (a straight line): underfitting.** It's bad on the training data **and** the test data (RMSE above 50 on both). The model is too simple to capture the U.
- **Degree 2: just right.** Training and test errors are both low (about 23) and close together.
- **Degrees 10 and 15: overfitting.** The training error keeps falling, because the curve bends to pass near every training point, but the test error **rises** (27, then 41). The extra wiggles follow random noise in these 28 days, which doesn't repeat on new days.

![Three panels with the same training points. Degree 1: a straight line that misses the U (underfit). Degree 2: a smooth U through the middle of the points (good fit). Degree 15: a wild curve that swings up and down between points (overfit)](figures/under-over-fit.svg)

### The complexity curve

Plot training and test error against complexity and you get the most important picture in machine learning:

![Two lines against model degree from 1 to 15. Training error falls steadily. Test error falls at first, is lowest around degree 2 to 4, then climbs. The left side is labelled underfitting, the right side overfitting, and the low point the sweet spot](figures/complexity-curve.svg)

- On the left, both errors are high: **underfitting** (also called **high bias**: the model's assumptions are too rigid).
- On the right, training error is low but test error is high: **overfitting** (also called **high variance**: the model changes a lot depending on which rows it saw).
- The **sweet spot** is where the test error is lowest.

Every model has a "complexity knob": the degree here, `n_neighbors` for KNN (small k = more complex), the depth of a decision tree, the number of features. Finding the right setting is called **tuning**, and you'll automate it in Lesson 19.

### What helps against overfitting

- **A simpler model**, or fewer features.
- **More training data.** Noise averages out, and a wiggly curve can't pass near thousands of points.
- **Regularisation**: penalise complexity (next lesson).
- **Honest testing**: as long as you judge by unseen data, you'll **notice** overfitting, which is half the battle.

:::exercise Find the sweet spot
Using the split below, try every degree from 1 to 8 with the same pipeline as the lesson. Store the degree with the **lowest test RMSE** in `best_degree` (an int).
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
e = pd.read_csv("energy.csv")
a, b, c, d = train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=3)
scores = {deg: root_mean_squared_error(d, make_pipeline(PolynomialFeatures(deg), StandardScaler(), LinearRegression()).fit(a, c).predict(b)) for deg in range(1, 9)}
same(int(need("best_degree")), min(scores, key=scores.get), "best_degree")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

test_rmse = {}
for degree in range(1, 9):
    model = make_pipeline(PolynomialFeatures(degree), StandardScaler(), LinearRegression()).fit(X_train, y_train)
    test_rmse[degree] = root_mean_squared_error(y_test, model.predict(X_test))
    print(degree, round(test_rmse[degree], 1))

best_degree = min(test_rmse, key=test_rmse.get)
print("best:", best_degree)
```
hint: Store each degree's test RMSE in a dictionary, then `min(d, key=d.get)` gives the key with the smallest value.
:::

:::exercise Measure the gap
With the same split (`random_state=3`), fit the degree-15 pipeline and store its training RMSE in `train_rmse` and its test RMSE in `test_rmse`. Then set `overfit` to `True` if the test RMSE is more than 1.5 times the training RMSE.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
e = pd.read_csv("energy.csv")
a, b, c, d = train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=3)
m = make_pipeline(PolynomialFeatures(15), StandardScaler(), LinearRegression()).fit(a, c)
tr, te = root_mean_squared_error(c, m.predict(a)), root_mean_squared_error(d, m.predict(b))
same(float(need("train_rmse")), tr, "train_rmse", tol=1e-4)
same(float(need("test_rmse")), te, "test_rmse", tol=1e-4)
same(need("overfit"), bool(te > 1.5 * tr), "overfit")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

model = make_pipeline(PolynomialFeatures(15), StandardScaler(), LinearRegression()).fit(X_train, y_train)
train_rmse = root_mean_squared_error(y_train, model.predict(X_train))
test_rmse = root_mean_squared_error(y_test, model.predict(X_test))
overfit = test_rmse > 1.5 * train_rmse
print(round(train_rmse, 1), round(test_rmse, 1), overfit)
```
hint: Predict on both `X_train` and `X_test` and compare each with its own true values.
:::

:::quiz
? A model has high error on both the training and test sets. It is probably:
+ Underfitting: too simple for the pattern
- Overfitting
- Perfect
= Bad everywhere means the model can't even capture the training data's pattern.
? As a model gets more complex, what usually happens to the training error?
+ It keeps falling
- It keeps rising
- It stays the same
= More flexibility lets the model hug the training points, even their noise. That's why training error can't pick the model.
? Where is the sweet spot on a complexity curve?
- Where the training error is lowest
+ Where the test (or validation) error is lowest
- At the most complex model
= The goal is good predictions on unseen data.
? Which of these does NOT help against overfitting?
- Collecting more training data
- Using a simpler model
+ Judging the model by its training score
= Training score rewards memorising. The other two genuinely reduce overfitting.
:::

@@@ lesson
id: regularization
title: Regularisation: Ridge and Lasso
minutes: 16
summary: Penalise big coefficients to tame overfitting. Ridge shrinks them; Lasso can switch useless features off.
---
An overfitting curve gets its wild wiggles from **huge coefficients** that pull in opposite directions. **Regularisation** adds a penalty for big coefficients to the training goal. The model now has to balance two things:

> fit the training data well **+** keep the coefficients small

The strength of the penalty is a hyperparameter called **`alpha`**. `alpha = 0` means no penalty (plain linear regression). Bigger `alpha` means a simpler, smoother model; too big and it underfits.

| Model | Penalty | Effect |
|---|---|---|
| `Ridge` | sum of **squared** coefficients | shrinks all coefficients towards zero, smoothly |
| `Lasso` | sum of **absolute** coefficients | shrinks them, and sets some **exactly to zero**: it picks features for you |
| `ElasticNet` | a mix of both | a middle ground |

![Left: the energy data with three degree-15 curves. With no penalty the curve swings wildly; with Ridge alpha 0.1 it's a smooth U; with alpha 100 it's almost flat. Right: Lasso coefficients for nine house features as alpha grows: the five random "noise" features drop to exactly zero first, while area stays large](figures/regularization.svg)

### Ridge rescues the wiggly curve

Same degree-15 model as last lesson, same split, but with `Ridge` instead of `LinearRegression`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=1)

plain = make_pipeline(PolynomialFeatures(15), StandardScaler(), LinearRegression()).fit(X_train, y_train)
print("no penalty:    test RMSE", round(root_mean_squared_error(y_test, plain.predict(X_test)), 1))

for alpha in [0.01, 0.1, 1, 10, 100]:
    ridge = make_pipeline(PolynomialFeatures(15), StandardScaler(), Ridge(alpha=alpha)).fit(X_train, y_train)
    print(f"Ridge alpha={alpha:<5} test RMSE", round(root_mean_squared_error(y_test, ridge.predict(X_test)), 1))
```

The test error drops from 40.9 to about 23 with a small penalty, as good as the "just right" degree-2 model. With `alpha` too large (1 and above here), the curve flattens and the model underfits again. `alpha` is another complexity knob to tune.

### Scale first

The penalty treats every coefficient the same, but coefficients depend on units (Lesson 5). A feature in millimetres needs a tiny coefficient; the same feature in kilometres needs a huge one, and would be punished far more. So **always standardise features before Ridge or Lasso**. `StandardScaler` puts every feature on the same scale (mean 0, standard deviation 1). That's why it's in every pipeline here.

### Lasso picks features

To see Lasso at work, give the housing model five extra columns of **pure random noise**. They have nothing to do with price, but plain linear regression will still give them coefficients, because it finds accidental patterns in the training rows:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Lasso

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]].copy()
rng = np.random.default_rng(0)
for i in range(5):
    X[f"noise_{i}"] = rng.normal(size=len(X)).round(2)     # columns of random numbers
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

plain = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
lasso = make_pipeline(StandardScaler(), Lasso(alpha=10)).fit(X_train, y_train)

coefs = pd.DataFrame({"plain": plain[-1].coef_, "lasso": lasso[-1].coef_}, index=X.columns)
print(coefs.round(1))
print("test R²  plain:", round(plain.score(X_test, y_test), 3), "  lasso:", round(lasso.score(X_test, y_test), 3))
```

`plain[-1]` means "the last step of the pipeline", the model itself. Because the features are standardised, these coefficients **can** be compared: each is "thousands per one standard deviation of the feature". Area is clearly the biggest driver.

Plain regression gives the noise columns coefficients up to about 12. Lasso sets all five **exactly to 0** (`-0.0` is just zero printed with a minus sign), keeps the real features, and scores better on the test set (0.823 against 0.775). That's **feature selection** done automatically.

### Which to use?

- Start with **Ridge** when you have many features that might all matter a little. It's stable and rarely hurts.
- Use **Lasso** when you suspect many features are useless and you want a simpler model that's easier to explain.
- Either way, choose `alpha` by testing on unseen data, not by guessing (Lesson 19 shows how to search for it automatically).

:::exercise Tame the curve
Using the split below (`random_state=3`), fit a degree-15 pipeline with `Ridge(alpha=0.1)`, exactly like the lesson. Store its test RMSE in `ridge_rmse`, and the test RMSE of the same pipeline with plain `LinearRegression()` in `plain_rmse`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import root_mean_squared_error
e = pd.read_csv("energy.csv")
a, b, c, d = train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=3)
r = root_mean_squared_error(d, make_pipeline(PolynomialFeatures(15), StandardScaler(), Ridge(alpha=0.1)).fit(a, c).predict(b))
p = root_mean_squared_error(d, make_pipeline(PolynomialFeatures(15), StandardScaler(), LinearRegression()).fit(a, c).predict(b))
same(float(need("ridge_rmse")), r, "ridge_rmse", tol=1e-4)
same(float(need("plain_rmse")), p, "plain_rmse", tol=1e-4)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=3)

ridge = make_pipeline(PolynomialFeatures(15), StandardScaler(), Ridge(alpha=0.1)).fit(X_train, y_train)
plain = make_pipeline(PolynomialFeatures(15), StandardScaler(), LinearRegression()).fit(X_train, y_train)
ridge_rmse = root_mean_squared_error(y_test, ridge.predict(X_test))
plain_rmse = root_mean_squared_error(y_test, plain.predict(X_test))
print(round(plain_rmse, 1), "->", round(ridge_rmse, 1))
```
hint: Only the last step changes: `Ridge(alpha=0.1)` instead of `LinearRegression()`.
:::

:::exercise Which features survive?
The code below adds three noise columns to the housing features. Fit `make_pipeline(StandardScaler(), Lasso(alpha=8))` on the training data and store, in `kept`, a list of the column names whose Lasso coefficient is **not** zero.
```python starter
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]].copy()
rng = np.random.default_rng(1)
for i in range(3):
    X[f"noise_{i}"] = rng.normal(size=len(X)).round(2)
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

```
```python check
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
h = pd.read_csv("housing.csv")
X_ = h[["area_sqm", "bedrooms", "age_years", "distance_km"]].copy()
rng_ = np.random.default_rng(1)
for i in range(3):
    X_[f"noise_{i}"] = rng_.normal(size=len(X_)).round(2)
a, b, c, d = train_test_split(X_, h["price_k"], test_size=0.25, random_state=0)
m = make_pipeline(StandardScaler(), Lasso(alpha=8)).fit(a, c)
exp = [col for col, w in zip(X_.columns, m[-1].coef_) if w != 0]
same(sorted(list(need("kept"))), sorted(exp), "kept")
```
```python solution
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]].copy()
rng = np.random.default_rng(1)
for i in range(3):
    X[f"noise_{i}"] = rng.normal(size=len(X)).round(2)
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

lasso = make_pipeline(StandardScaler(), Lasso(alpha=8)).fit(X_train, y_train)
coefs = pd.Series(lasso[-1].coef_, index=X.columns)
print(coefs.round(2))
kept = coefs[coefs != 0].index.tolist()
print(kept)
```
hint: `lasso[-1].coef_` holds the coefficients in the order of `X.columns`. Put them in a Series and keep the names where the value isn't 0.
:::

:::quiz
? What does a larger alpha do in Ridge?
+ Penalises big coefficients more, making the model simpler and smoother
- Makes the model more complex
- Removes the intercept
= alpha is the strength of the penalty. Too large and the model underfits.
? What can Lasso do that Ridge can't?
- Predict categories
+ Set some coefficients exactly to zero, dropping those features
- Work without any data
= The absolute-value penalty pushes weak features all the way to 0.
? Why scale features before Ridge or Lasso?
+ The penalty treats all coefficients equally, but their sizes depend on each feature's units
- Scaling makes training data larger
- scikit-learn refuses to fit otherwise
= Without scaling, features in small units get punished more than features in big units.
? How should you choose alpha?
- Always use alpha=1
+ Try several values and keep the one that does best on unseen (validation) data
- Pick the one with the best training score
= Like any hyperparameter, alpha is tuned on data the model didn't train on.
:::
