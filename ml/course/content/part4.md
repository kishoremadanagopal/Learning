@@@ part
id: 4
title: Real-World Data and Workflow
level: Intermediate
blurb: Real data has text, gaps and wildly different units. Scale, encode and fill it inside pipelines that can't leak, then judge and tune models with cross-validation.

@@@ lesson
id: scaling
title: Scaling features
minutes: 14
summary: StandardScaler, MinMaxScaler and RobustScaler; the fit / transform pattern; which models need scaling and which don't.
---
Features come in different units: centimetres and grams, months and pounds. Some models are blind to units (trees); others are dominated by whichever feature has the biggest numbers (anything that measures distances or penalises coefficients). **Scaling** puts every feature on a comparable scale.

![Two scatter plots of the same 150 fruits. Left, raw units: width spans about 4 cm while weight spans about 200 g, so the cloud is a thin streak along the weight axis. Right, after StandardScaler: both features are centred on 0 and spread about -2 to 2, and the shape of the data is visible](figures/scaling.svg)

| Scaler | What it does | Result | Use when |
|---|---|---|---|
| `StandardScaler` | subtract the mean, divide by the standard deviation | mean 0, std 1 (z-scores) | the default choice |
| `MinMaxScaler` | squeeze into a range | 0 to 1 | you need a fixed range (e.g. pixel values, some neural networks) |
| `RobustScaler` | subtract the median, divide by the IQR | middle half spans about 1 | the data has big outliers |

### Transformers: fit, then transform

Scalers are **transformers**: instead of `predict`, they have `transform`, which returns a changed copy of the data. Like models, they **learn** something in `fit`: `StandardScaler` learns each column's mean and standard deviation.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
X_train, X_test = train_test_split(X, test_size=0.25, random_state=3)

scaler = StandardScaler()
scaler.fit(X_train)                       # learn the means and standard deviations from TRAINING data
print("learned means:", scaler.mean_.round(1))
print("learned stds: ", scaler.scale_.round(1))

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)  # use the TRAINING means on the test data
print(pd.DataFrame(X_train_scaled, columns=X.columns).describe().loc[["mean", "std"]].round(2))
```

(`-0.0` is zero; the tiny minus sign comes from rounding a number like −0.0000001.)

The rule that matters most: **fit the scaler on the training data only**, then use it to transform both training and test data. The test set stands for future data, and you won't know future data's mean when you train. Fitting on everything lets information from the test set leak into training (Lesson 17).

`fit_transform(X_train)` does `fit` and `transform` in one step. Use it on training data only; on test data, only ever call `transform`.

The scaled training data has mean 0 and standard deviation 1 in every column. The test data's mean will be close to 0, not exactly 0, and that's correct.

### Which models need scaling?

| Needs scaling | Doesn't care |
|---|---|
| k-nearest neighbours (distances) | decision trees |
| Ridge, Lasso, logistic regression (penalties; also trains faster) | random forests |
| support vector machines, neural networks | gradient boosting |
| k-means clustering, PCA (Part 5) | plain linear regression (predictions don't change, only the coefficients) |

When in doubt, scale: it never hurts a tree, and it often helps everything else.

### Scaled coefficients can be compared

A bonus from Lesson 5: after `StandardScaler`, a linear model's coefficients are all "per standard deviation", so their sizes **can** be compared:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.25, random_state=0, stratify=churn["churned"])

scaler = StandardScaler().fit(X_train)
model = LogisticRegression().fit(scaler.transform(X_train), y_train)
print(pd.Series(model.coef_[0], index=features).round(2).sort_values())
```

Tenure has the biggest effect (negative: long-standing customers stay), then support calls. Monthly charge and data use matter much less.

### Outliers and RobustScaler

The mean and standard deviation are pulled around by extreme values. If a column has a few huge outliers, `RobustScaler` uses the median and the interquartile range instead, which outliers barely affect:

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler

incomes = pd.DataFrame({"income_k": [28, 31, 35, 38, 41, 44, 47, 52, 900]})   # one billionaire-ish outlier
incomes["standard"] = StandardScaler().fit_transform(incomes[["income_k"]]).round(2).ravel()
incomes["robust"] = RobustScaler().fit_transform(incomes[["income_k"]]).round(2).ravel()
incomes["minmax"] = MinMaxScaler().fit_transform(incomes[["income_k"]]).round(2).ravel()
print(incomes)
```

With `StandardScaler` and `MinMaxScaler`, the one outlier squashes the eight normal incomes into a tiny range. `RobustScaler` keeps them spread out.

:::exercise Scale the right way
Fit a `StandardScaler` called `scaler` on `X_train` only. Store the transformed training data in `X_train_scaled` and the transformed test data in `X_test_scaled`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "age_years", "distance_km"]]
X_train, X_test = train_test_split(X, test_size=0.25, random_state=0)

```
```python check
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
h = pd.read_csv("housing.csv")
a, b = train_test_split(h[["area_sqm", "age_years", "distance_km"]], test_size=0.25, random_state=0)
ref = StandardScaler().fit(a)
s = need("scaler", StandardScaler)
same(np.asarray(s.mean_), ref.mean_, "the scaler's learned means (fit it on X_train only)")
same(np.asarray(need("X_train_scaled")), ref.transform(a), "X_train_scaled")
same(np.asarray(need("X_test_scaled")), ref.transform(b), "X_test_scaled (transform, don't refit)")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "age_years", "distance_km"]]
X_train, X_test = train_test_split(X, test_size=0.25, random_state=0)

scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(X_train_scaled.mean(axis=0).round(2), X_test_scaled.mean(axis=0).round(2))
```
hint: `scaler = StandardScaler().fit(X_train)`, then `scaler.transform(...)` on each set. Never fit on `X_test`.
:::

:::exercise Zero to one
Use `MinMaxScaler` to scale the `spending_score` and `annual_income_k` columns of `shoppers.csv` (all rows: there's no label, so no split is needed). Store the result as a DataFrame called `scaled` with the same two column names.
```python starter
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

shoppers = pd.read_csv("shoppers.csv")
cols = ["spending_score", "annual_income_k"]

```
```python check
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
s = pd.read_csv("shoppers.csv")
cols = ["spending_score", "annual_income_k"]
got = need("scaled", pd.DataFrame)
same(list(got.columns), cols, "scaled's columns")
same(got.to_numpy(), MinMaxScaler().fit_transform(s[cols]), "scaled's values")
```
```python solution
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

shoppers = pd.read_csv("shoppers.csv")
cols = ["spending_score", "annual_income_k"]
scaled = pd.DataFrame(MinMaxScaler().fit_transform(shoppers[cols]), columns=cols)
print(scaled.describe().loc[["min", "max"]])
```
hint: `MinMaxScaler().fit_transform(shoppers[cols])` returns an array; wrap it with `pd.DataFrame(..., columns=cols)`.
:::

:::quiz
? Why fit the scaler on the training data only?
+ The test set stands for future data, whose statistics you can't know when training
- Fitting on the test data is slower
- scikit-learn doesn't allow it
= Fitting on test data leaks information from it into training, making scores look better than they will be.
? After StandardScaler, each training column has:
+ Mean 0 and standard deviation 1
- Values between 0 and 1
- Median 0 and no outliers
= That's standardising. MinMaxScaler gives 0 to 1.
? Which model does NOT need scaled features?
- k-nearest neighbours
- Logistic regression with a penalty
+ A random forest
= Trees split on one feature at a time, so units don't matter.
? A column has a few extreme outliers. Which scaler is least affected?
- StandardScaler
- MinMaxScaler
+ RobustScaler
= It uses the median and IQR, which outliers barely move.
:::

@@@ lesson
id: encoding-and-missing
title: Text categories and missing values
minutes: 18
summary: One-hot and ordinal encoding, filling gaps with SimpleImputer, and ColumnTransformer to treat each column the right way.
---
Models only understand numbers, and most can't handle blanks. Real tables have both text and gaps. Two kinds of transformer fix them: **encoders** turn categories into numbers, **imputers** fill missing values.

### One-hot encoding

You can't just number the categories (month-to-month = 0, one-year = 1, two-year = 2): the model would think "two-year" is twice "one-year". **One-hot encoding** makes one 0/1 column per category instead:

![A column "contract" with values month-to-month, one-year, two-year, month-to-month becomes three 0/1 columns, one per contract type. Each row has a single 1 in the column of its own category](figures/one-hot.svg)

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

churn = pd.read_csv("churn.csv")
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded = encoder.fit_transform(churn[["contract"]])

print(encoder.categories_)
print(encoder.get_feature_names_out())
print(encoded[:4])
print(churn["contract"].head(4).tolist())
```

- `handle_unknown="ignore"` means a category the encoder never saw in training (say, a new "three-year" contract) becomes all zeros instead of an error. Always set it for real data.
- `sparse_output=False` returns a normal array you can print. (By default it returns a compact **sparse** matrix, which is better for columns with thousands of categories.)
- You used `pd.get_dummies` in Lesson 14. It's handy for exploring, but `OneHotEncoder` **remembers** the categories it learned in training, so the test data and future data get exactly the same columns.

### Ordinal encoding: when order is real

Some categories **do** have an order: basic < standard < premium, small < medium < large, survey answers 1 to 5. Then a single column of numbers is right, as long as you give the order yourself:

```python
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

churn = pd.read_csv("churn.csv")
encoder = OrdinalEncoder(categories=[["basic", "standard", "premium"]])
churn["plan_level"] = encoder.fit_transform(churn[["plan"]])
print(churn[["plan", "plan_level"]].drop_duplicates().sort_values("plan_level"))
```

Without `categories=`, the encoder sorts alphabetically (basic, premium, standard), which gets the order wrong.

### Missing values

The `age` column of `churn.csv` has gaps. Most scikit-learn models refuse to train on them:

```python error
import pandas as pd
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
print("missing ages:", churn["age"].isna().sum())
LogisticRegression().fit(churn[["tenure_months", "age"]], churn["churned"])
```

You could drop the rows with gaps, but you'd lose data, and you'd still need a plan when a **new** customer arrives without an age. `SimpleImputer` fills each gap with a value learned from the training data:

| `strategy=` | Fills with | Good for |
|---|---|---|
| `"median"` | the column's median | numbers, especially skewed ones |
| `"mean"` | the column's mean | numbers without outliers |
| `"most_frequent"` | the most common value | categories (text) |
| `"constant"` | a value you choose (`fill_value=`) | e.g. "unknown" |

```python
import pandas as pd
from sklearn.impute import SimpleImputer

churn = pd.read_csv("churn.csv")
imputer = SimpleImputer(strategy="median", add_indicator=True)
filled = imputer.fit_transform(churn[["age"]])

print("learned median:", imputer.statistics_)
print(imputer.get_feature_names_out())
print(filled[churn["age"].isna().to_numpy()][:3])   # three rows that were missing
```

`add_indicator=True` adds a 0/1 column saying "this value was missing". Sometimes **whether** something is missing is itself a clue (customers who didn't give their age might behave differently).

### ColumnTransformer: the right step for each column

Real tables mix numbers and text, so different columns need different steps. `ColumnTransformer` applies each transformer to its own list of columns and glues the results side by side:

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

churn = pd.read_csv("churn.csv")
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
categorical = ["contract", "plan"]

prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
X_ready = prep.fit_transform(churn)
print(X_ready.shape)
print(prep.get_feature_names_out())
```

Each entry is `(a name, the transformer, the columns)`. Columns you don't list (like `customer_id` and `churned`) are dropped. The numeric columns get "fill the gaps, then scale"; the text columns get one-hot encoded. 5 numbers + 3 contracts + 3 plans = 11 columns.

### What it buys you

The housing data has a text column you've ignored so far: `neighborhood`. Adding it with a `ColumnTransformer`:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

housing = pd.read_csv("housing.csv")
numeric = ["area_sqm", "bedrooms", "age_years", "distance_km"]
X_train, X_test, y_train, y_test = train_test_split(
    housing[numeric + ["neighborhood"]], housing["price_k"], test_size=0.25, random_state=5)

without = LinearRegression().fit(X_train[numeric], y_train)
prep = ColumnTransformer([
    ("num", "passthrough", numeric),                                  # "passthrough" keeps columns as they are
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"]),
])
with_hood = make_pipeline(prep, LinearRegression()).fit(X_train, y_train)

print("MAE without neighborhood:", round(mean_absolute_error(y_test, without.predict(X_test[numeric])), 1))
print("MAE with neighborhood:   ", round(mean_absolute_error(y_test, with_hood.predict(X_test)), 1))
print("R² with neighborhood:    ", round(with_hood.score(X_test, y_test), 3))
```

The typical error drops from about 41 thousand to 27 thousand, and R² rises from 0.82 to 0.92. One text column, properly encoded, was worth more than any model change so far.

:::exercise Encode the plans
Make a `OneHotEncoder(sparse_output=False, handle_unknown="ignore")` called `encoder`, fit it on the `plan` column of `churn.csv`, and store the transformed array in `plan_encoded` and the new column names (from `get_feature_names_out()`) in `names`.
```python starter
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

churn = pd.read_csv("churn.csv")

```
```python check
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
c = pd.read_csv("churn.csv")
ref = OneHotEncoder(sparse_output=False, handle_unknown="ignore").fit(c[["plan"]])
need("encoder", OneHotEncoder)
same(list(need("names")), list(ref.get_feature_names_out()), "names")
same(np.asarray(need("plan_encoded")), ref.transform(c[["plan"]]), "plan_encoded")
```
```python solution
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

churn = pd.read_csv("churn.csv")
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
plan_encoded = encoder.fit_transform(churn[["plan"]])
names = encoder.get_feature_names_out()
print(names, plan_encoded[:3])
```
hint: Use double brackets, `churn[["plan"]]`: encoders also want a table.
:::

:::exercise Every column, prepared
Build a `ColumnTransformer` called `prep` for `churn.csv` that fills the missing values of `age` and `tenure_months` with their **median** (no scaling needed here) and one-hot encodes `contract` with `handle_unknown="ignore"`. Fit it on the training rows, and store the transformed **test** rows in `X_test_ready`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

churn = pd.read_csv("churn.csv")
X_train, X_test = train_test_split(churn, test_size=0.25, random_state=0)

```
```python check
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
c = pd.read_csv("churn.csv")
a, b = train_test_split(c, test_size=0.25, random_state=0)
ref = ColumnTransformer([("num", SimpleImputer(strategy="median"), ["age", "tenure_months"]),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract"])]).fit(a)
need("prep", ColumnTransformer)
got = np.asarray(need("X_test_ready"))
exp = ref.transform(b)
same(got.shape, exp.shape, "X_test_ready's shape (2 numeric + 3 contract columns)")
if np.isnan(got.astype(float)).any():
    raise AssertionError("X_test_ready still has missing values: impute age with SimpleImputer(strategy='median').")
same(np.sort(got, axis=1), np.sort(exp, axis=1), "X_test_ready (fit on X_train, transform X_test)")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

churn = pd.read_csv("churn.csv")
X_train, X_test = train_test_split(churn, test_size=0.25, random_state=0)

prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["age", "tenure_months"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract"]),
])
prep.fit(X_train)
X_test_ready = prep.transform(X_test)
print(prep.get_feature_names_out())
print(X_test_ready[:3])
```
hint: One entry per group of columns: `("num", SimpleImputer(strategy="median"), [...])` and `("cat", OneHotEncoder(handle_unknown="ignore"), ["contract"])`.
:::

:::quiz
? Why not encode contract types as 0, 1, 2 in one column?
+ The model would treat them as ordered numbers, as if two-year were "twice" one-year
- Because numbers take more memory
- It's fine for every model
= Unordered categories need one-hot encoding. Ordinal encoding is only for categories with a real order.
? What does handle_unknown="ignore" do in OneHotEncoder?
+ Encodes a category never seen in training as all zeros instead of raising an error
- Drops rows with missing values
- Ignores the column completely
= New categories appear in real life; this keeps predictions working.
? Which SimpleImputer strategy suits a text column?
- "mean"
- "median"
+ "most_frequent"
= You can't average text; the most common value (or a constant like "unknown") works.
? What does ColumnTransformer do?
+ Applies different transformers to different columns and joins the results
- Changes column names
- Transposes the table
= It's how you scale numbers and encode text in one step.
:::

@@@ lesson
id: pipelines-and-leakage
title: Pipelines and data leakage
minutes: 19
summary: Bundle preparation and model into one Pipeline, so it fits on training data only and predicts on raw new rows. Recognise and prevent data leakage.
---
A **Pipeline** chains transformers and a final model into one object that behaves like a model:

![A pipeline diagram. Raw rows with text and gaps go into a ColumnTransformer, where numeric columns are imputed and scaled and categorical columns are one-hot encoded, then into LogisticRegression, which outputs churn probabilities. pipe.fit(X_train, y_train) fits every step on the training data in order; pipe.predict(new_rows) applies the same learned steps to new rows](figures/pipeline.svg)

- `pipe.fit(X_train, y_train)`: each step learns from the **training data** (the imputer its medians, the scaler its means, the encoder its categories) and passes the transformed data on; the last step, the model, trains on the result.
- `pipe.predict(X_new)`: the new rows go through the **same learned** steps, then the model predicts.

You've used `make_pipeline` since Lesson 7. `Pipeline` is the same, but you name each step yourself, which makes them easier to reach later.

### The full churn pipeline

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
categorical = ["contract", "plan"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())])

pipe.fit(X_train, y_train)
print("test accuracy:", round(pipe.score(X_test, y_test), 3))
print("test AUC:     ", round(roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1]), 3))
```

Accuracy 0.828 and AUC 0.844: the best churn model in the course so far, and it's "only" logistic regression. With every column prepared properly, a simple model can match or beat a forest. Good preparation often matters more than a clever model.

### Predicting from raw rows

Because the preparation is inside, the pipeline takes **raw** data: text, gaps and all. That's exactly what you need when a model goes live:

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())]).fit(X, churn["churned"])

new_customers = pd.DataFrame({
    "contract": ["month-to-month", "two-year"],
    "plan": ["basic", "premium"],
    "tenure_months": [2, 40],
    "monthly_charge": [31.5, 80.0],
    "support_calls": [4, 0],
    "age": [np.nan, 52],          # age unknown: the pipeline's imputer fills it
    "data_gb": [30.2, 12.0],
})
print(pipe.predict_proba(new_customers)[:, 1].round(3))

# reach inside: coefficients with readable names
names = pipe.named_steps["prep"].get_feature_names_out()
print(pd.Series(pipe.named_steps["model"].coef_[0], index=names).round(2).sort_values())
```

The new month-to-month customer with lots of support calls is very likely to leave; the long-standing two-year customer is not. `pipe.named_steps["model"]` (or `pipe[-1]`) reaches a step by name or position.

### Data leakage

**Data leakage** is when information that wouldn't be available at prediction time sneaks into training. The model looks great in testing and then disappoints in real use. It's one of the most common and expensive mistakes in machine learning. Two kinds:

![Two panels. Left, train-test contamination: a scaler or feature selector is fitted on all rows, including the test rows, before splitting, so the test set is no longer unseen. Right, target leakage: a feature like "cancellation fee paid" only exists after a customer has churned, so it gives away the answer](figures/leakage.svg)

**1. Train-test contamination.** Any step that learns from data (scaling, imputing, choosing features) must learn from training rows only. Here's how dramatic it can get. The data below is **pure random noise**: 2,000 random features, random labels. No model can genuinely do better than 50%. But choose the "best" 20 features using **all** the rows first, and cross-validation (Lesson 18) reports far better than chance:

```python
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(5)
X = rng.normal(size=(100, 2000))        # 100 rows of random numbers
y = rng.integers(0, 2, size=100)        # random labels: nothing to learn

# WRONG: pick the 20 features most related to y using ALL rows, then evaluate
X_picked = SelectKBest(f_classif, k=20).fit_transform(X, y)
print("leaky:  ", cross_val_score(LogisticRegression(), X_picked, y, cv=5).mean().round(2))

# RIGHT: selection inside a pipeline, so it's redone on the training part of every split
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
print("honest: ", cross_val_score(pipe, X, y, cv=5).mean().round(2))
```

The leaky version claims 88% accuracy on pure noise, because the features were chosen by peeking at the very rows used to test. Inside a pipeline the score drops to about 0.5: a coin toss, which is the truth. **Putting every learned step inside a pipeline is the cure.**

**2. Target leakage.** A feature that's only known **after** the outcome, or is caused by it. Imagine the churn table had a column "cancellation fee paid": only people who left paid it. A model would lean on it and look nearly perfect, but at prediction time (before anyone has left) the column doesn't exist yet.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
rng = np.random.default_rng(1)
# a made-up column that is only filled in AFTER someone leaves: 90% of leavers paid a fee
churn["cancel_fee_paid"] = ((churn["churned"] == 1) & (rng.random(len(churn)) < 0.9)).astype(int)

X = churn[["tenure_months", "support_calls", "cancel_fee_paid"]]
X_train, X_test, y_train, y_test = train_test_split(X, churn["churned"], test_size=0.25, random_state=0)
model = LogisticRegression().fit(X_train, y_train)
print("AUC with the leaky column:", round(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]), 3))
```

The warning sign: **results that are too good to be true.** For every feature, ask: "Would I know this value at the moment I need to make the prediction?"

:::exercise A house-price pipeline
Build a `Pipeline` called `pipe` with two steps: `"prep"`, a `ColumnTransformer` that scales `area_sqm`, `bedrooms`, `age_years` and `distance_km` with `StandardScaler` and one-hot encodes `neighborhood` (with `handle_unknown="ignore"`); and `"model"`, a `Ridge(alpha=1.0)`. Fit it on the training data and store its test R² in `r2`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

housing = pd.read_csv("housing.csv")
X = housing.drop(columns=["home_id", "price_k"])
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
h = pd.read_csv("housing.csv")
a, b, c, d = train_test_split(h.drop(columns=["home_id", "price_k"]), h["price_k"], test_size=0.25, random_state=1)
ref = Pipeline([("prep", ColumnTransformer([("num", StandardScaler(), ["area_sqm", "bedrooms", "age_years", "distance_km"]),
                                             ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"])])),
                ("model", Ridge(alpha=1.0))]).fit(a, c)
p = need("pipe", Pipeline)
same(list(p.named_steps), ["prep", "model"], "the step names")
same(float(need("r2")), ref.score(b, d), "r2", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

housing = pd.read_csv("housing.csv")
X = housing.drop(columns=["home_id", "price_k"])
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

prep = ColumnTransformer([
    ("num", StandardScaler(), ["area_sqm", "bedrooms", "age_years", "distance_km"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"]),
])
pipe = Pipeline([("prep", prep), ("model", Ridge(alpha=1.0))])
pipe.fit(X_train, y_train)
r2 = pipe.score(X_test, y_test)
print(round(r2, 3))
```
hint: `Pipeline([("prep", ColumnTransformer([...])), ("model", Ridge(alpha=1.0))])`, then fit and score like any model.
:::

:::exercise Find the leak
The code below adds three new columns to the churn data. One of them is target leakage. For each new column, fit a `LogisticRegression` on the training data using **only that column**, and compute its test AUC. Store the name of the column with the suspiciously high AUC in `leaky`.
```python starter
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
rng = np.random.default_rng(7)
churn["app_logins"] = rng.poisson(9, len(churn))
churn["final_bill_refunded"] = ((churn["churned"] == 1) & (rng.random(len(churn)) < 0.85)).astype(int)
churn["emails_opened"] = rng.poisson(3, len(churn))
new_columns = ["app_logins", "final_bill_refunded", "emails_opened"]
X_train, X_test, y_train, y_test = train_test_split(churn, churn["churned"], test_size=0.25, random_state=0)

```
```python check
same(str(need("leaky")), "final_bill_refunded", "leaky")
```
```python solution
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
rng = np.random.default_rng(7)
churn["app_logins"] = rng.poisson(9, len(churn))
churn["final_bill_refunded"] = ((churn["churned"] == 1) & (rng.random(len(churn)) < 0.85)).astype(int)
churn["emails_opened"] = rng.poisson(3, len(churn))
new_columns = ["app_logins", "final_bill_refunded", "emails_opened"]
X_train, X_test, y_train, y_test = train_test_split(churn, churn["churned"], test_size=0.25, random_state=0)

aucs = {}
for col in new_columns:
    model = LogisticRegression().fit(X_train[[col]], y_train)
    aucs[col] = roc_auc_score(y_test, model.predict_proba(X_test[[col]])[:, 1])
print(aucs)
leaky = max(aucs, key=aucs.get)
```
hint: A loop over `new_columns`; for each, fit on `X_train[[col]]` and score on `X_test[[col]]`. Then ask: could you know a final bill refund before the customer leaves?
:::

:::quiz
? What's the main benefit of putting preprocessing inside a Pipeline?
+ Every step learns from the training data only, and new raw rows get exactly the same treatment
- It makes the model more accurate on its own
- It removes the need for a test set
= Pipelines prevent leakage and make the model easy to use on raw data.
? Which is target leakage?
- Using customer age to predict churn
+ Using "account closed date" to predict whether a customer will leave
- Scaling features
= The closed date only exists after the customer leaves, so it gives away the answer.
? A model scores 99.8% on a hard problem. What should you do first?
+ Suspect leakage and check whether any feature carries the answer
- Deploy it immediately
- Add more features
= Results that are too good to be true usually are.
? In pipe = Pipeline([("prep", prep), ("model", LogisticRegression())]), how do you reach the logistic regression?
+ pipe.named_steps["model"] or pipe[-1]
- pipe.model
- pipe.steps.model
= Steps can be reached by name or by position.
:::

@@@ lesson
id: cross-validation
title: Cross-validation
minutes: 16
summary: One split is a coin toss. K-fold cross-validation scores a model on several splits, for a fairer number and an idea of its wobble.
---
A single train/test split depends on luck: which rows happened to land in the test set. Change `random_state` and the score moves:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

for seed in range(6):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(5)).fit(X_train, y_train)
    print(f"split {seed}: test accuracy {model.score(X_test, y_test):.3f}")
```

Same model, same data, accuracy anywhere from 0.79 to 0.89. If you compared two models on one split, the "winner" could just be the luckier one.

### K-fold cross-validation

**Cross-validation** (CV) uses every row for testing once. With **5-fold** CV:

![Five rows, one per round. The training data is cut into five equal folds. In round 1, fold 1 is the validation fold and folds 2 to 5 are used for training; in round 2, fold 2 validates; and so on. The five validation scores are averaged into the CV score](figures/kfold.svg)

1. Cut the data into 5 equal parts (**folds**).
2. Train on 4 folds and score on the 5th (the **validation fold**).
3. Repeat 5 times, so each fold is the validation fold once.
4. Report the **mean** of the 5 scores, and their **standard deviation** as the wobble.

```python
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

model = make_pipeline(StandardScaler(), KNeighborsClassifier(5))
scores = cross_val_score(model, X, y, cv=5)
print(scores.round(3))
print(f"accuracy {scores.mean():.3f} ± {scores.std():.3f}")
```

`cross_val_score` does the splitting, fitting and scoring for you. It refits a fresh copy of the model each round, and because the scaler is inside the pipeline, it's refit on each round's training folds: no leakage.

Details worth knowing:

- For classifiers, `cv=5` automatically uses **stratified** folds (each fold keeps the class mix).
- For regression, folds are taken **in order** without shuffling. If your rows are sorted (by date, by price…), pass `cv=KFold(5, shuffle=True, random_state=0)`.
- `scoring=` picks the metric: `"accuracy"`, `"roc_auc"`, `"f1"`, `"recall"`, `"r2"`, `"neg_mean_absolute_error"`… Error metrics are **negated** (`neg_`) because scikit-learn always treats higher as better; flip the sign back to read them.
- 5 or 10 folds are the usual choices. More folds means more training data per round but more time.

### Comparing models fairly

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
candidates = {
    "baseline": DummyClassifier(),
    "logistic regression": LogisticRegression(),
    "random forest": RandomForestClassifier(n_estimators=200, min_samples_leaf=3, random_state=0),
    "gradient boosting": HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, random_state=0),
}
for name, model in candidates.items():
    scores = cross_val_score(Pipeline([("prep", prep), ("model", model)]), X_train, y_train, cv=5, scoring="roc_auc")
    print(f"{name:<20} AUC {scores.mean():.3f} ± {scores.std():.3f}")
```

The three real models are within about 0.01 of each other, much less than their wobble (±0.03 to 0.06). The honest conclusion: **they're about equally good** on this data. When that happens, prefer the simplest, fastest and easiest to explain: here, logistic regression.

### Where the test set fits in

Cross-validation runs on the **training** set and is for **making choices**: which model, which features, which settings. The test set stays locked away and is used **once**, at the very end, to report the final model's score.

| Data | Used for |
|---|---|
| Training folds | fitting models |
| Validation folds (CV) | comparing and choosing |
| Test set | one final, honest score |

If you choose using test scores, the test set quietly becomes part of training, and your final number is optimistic.

`cross_validate` gives several metrics at once, and training scores too, which is handy for spotting overfitting:

```python
import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]

result = cross_validate(DecisionTreeClassifier(random_state=0), X, y, cv=5,
                        scoring=["accuracy", "roc_auc"], return_train_score=True)
print("train AUC:     ", result["train_roc_auc"].mean().round(3))
print("validation AUC:", result["test_roc_auc"].mean().round(3))
```

A perfect training AUC against about 0.6 on the validation folds: the unlimited tree is overfitting, exactly as Lesson 13 found with one split. (`cross_validate` calls the validation scores `test_...`.)

:::exercise Score with five folds
Store the 5-fold cross-validation **accuracy** scores of `make_pipeline(StandardScaler(), LogisticRegression())` on the fruit data in `scores`, and their mean in `mean_acc`.
```python starter
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

```
```python check
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
f = pd.read_csv("fruit.csv")
exp = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), f[["width_cm", "height_cm", "weight_g"]], f["fruit"], cv=5)
same(np.asarray(need("scores")), exp, "scores")
same(float(need("mean_acc")), exp.mean(), "mean_acc")
```
```python solution
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

scores = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression()), X, y, cv=5)
mean_acc = scores.mean()
print(scores.round(3), round(mean_acc, 3))
```
hint: `cross_val_score(model, X, y, cv=5)` returns an array of 5 scores.
:::

:::exercise Which k, fairly?
Using 5-fold cross-validated accuracy on the fruit data, compare `make_pipeline(StandardScaler(), KNeighborsClassifier(k))` for k = 1, 5, 9 and 15. Store a dictionary `cv_means` mapping each k to its mean CV accuracy, and the best k in `best_k` (smaller k on a tie).
```python starter
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

```
```python check
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
f = pd.read_csv("fruit.csv")
X_ = f[["width_cm", "height_cm", "weight_g"]]
exp = {k: cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(k)), X_, f["fruit"], cv=5).mean() for k in [1, 5, 9, 15]}
got = need("cv_means", dict)
same({int(k): float(v) for k, v in got.items()}, exp, "cv_means")
same(int(need("best_k")), max(exp, key=lambda k: (exp[k], -k)), "best_k")
```
```python solution
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
y = fruit["fruit"]

cv_means = {}
for k in [1, 5, 9, 15]:
    cv_means[k] = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(k)), X, y, cv=5).mean()
best_k = max(cv_means, key=lambda k: (cv_means[k], -k))
print({k: round(v, 3) for k, v in cv_means.items()}, best_k)
```
hint: Fill the dictionary in a loop. For the best k, `max(cv_means, key=cv_means.get)` works; to prefer the smaller k on a tie, use `key=lambda k: (cv_means[k], -k)`.
:::

:::quiz
? Why use cross-validation instead of one train/test split to compare models?
+ One split's score depends on luck; CV averages over several splits
- CV needs less data
- CV makes models train faster
= Averaging over folds gives a steadier score and shows how much it wobbles.
? In 5-fold CV, how many times is each row used for validation?
+ Exactly once
- Five times
- Never
= Each fold is the validation fold in one round.
? Why does scikit-learn report "neg_mean_absolute_error"?
+ It always treats higher scores as better, so errors are negated
- Because errors can be negative
- It's a different metric from MAE
= Flip the sign to read the usual MAE.
? Two models score 0.814 ± 0.03 and 0.813 ± 0.06 in CV. What's the sensible conclusion?
+ They're about equally good; prefer the simpler one
- The first is clearly better
- Cross-validation failed
= A difference far smaller than the wobble isn't a real difference.
:::

@@@ lesson
id: tuning
title: Tuning hyperparameters
minutes: 17
summary: Search for the best settings automatically with GridSearchCV and RandomizedSearchCV, read validation curves, and keep the test set honest.
---
Every model has settings you choose: `n_neighbors`, `max_depth`, `alpha`, `C`, `learning_rate`. These **hyperparameters** often matter as much as the choice of model. **Tuning** means trying different values and keeping the best, judged by cross-validation.

### A validation curve

Before searching, it helps to **see** how one setting affects training and validation scores:

![Validation curve for a decision tree on the churn data: training AUC rises steadily with max_depth towards 1.0, while cross-validated AUC peaks around depth 3 to 5 and then falls. The gap between the lines grows as the tree overfits](figures/validation-curve.svg)

```python
import pandas as pd
from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]

depths = [1, 2, 3, 4, 5, 6, 8, 10, 15]
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=0), X, y,
    param_name="max_depth", param_range=depths, cv=5, scoring="roc_auc")

for d, tr, va in zip(depths, train_scores.mean(axis=1), val_scores.mean(axis=1)):
    print(f"max_depth={d:>2}  train AUC {tr:.3f}  validation AUC {va:.3f}")
```

It's the complexity curve from Lesson 7, measured with cross-validation: the validation score peaks at a middle depth, then overfitting sets in.

### GridSearchCV: try every combination

`GridSearchCV` tries **every combination** of the values you list, scores each with cross-validation, and keeps the best. Inside a pipeline, name parameters as **`step__parameter`** (two underscores):

```python
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.25, random_state=0, stratify=fruit["fruit"])

pipe = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier())])
grid = {
    "knn__n_neighbors": [1, 3, 5, 7, 9, 15, 25],
    "knn__weights": ["uniform", "distance"],      # "distance": closer neighbours get a bigger vote
}
search = GridSearchCV(pipe, grid, cv=5, scoring="accuracy")
search.fit(X_train, y_train)

print("best settings:", search.best_params_)
print("best CV accuracy:", round(search.best_score_, 3))
print("test accuracy:   ", round(search.score(X_test, y_test), 3))
```

7 × 2 = 14 combinations × 5 folds = 70 fits, done for you. Then:

- `best_params_` and `best_score_` (the best **mean CV** score) tell you what won.
- By default the search **refits** the winning settings on the whole training set, so `search` itself is the final model: `search.predict(...)` and `search.score(...)` use it. `search.best_estimator_` is that refitted pipeline.
- The test score is checked **once**, at the end. It may be a bit lower than the CV score: the best CV score is slightly optimistic, because it was the maximum of many tries.

`search.cv_results_` holds every combination's scores; it reads nicely as a DataFrame:

```python
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])

search = GridSearchCV(pipe, {"model__C": [0.001, 0.01, 0.1, 1, 10, 100]}, cv=5, scoring="roc_auc").fit(X, y)
results = pd.DataFrame(search.cv_results_)[["param_model__C", "mean_test_score", "std_test_score"]]
print(results.round(3))
```

For logistic regression, **`C`** is the regularisation knob, but **backwards** from Ridge's `alpha`: `C` is 1 ÷ penalty strength, so **small C = strong penalty = simpler model**. Very small C (0.001) shrinks everything and underfits; from about C = 0.1 upward the score levels off.

### RandomizedSearchCV: when the grid is huge

A grid with 4 settings of 5 values each is 5⁴ = 625 combinations, times 5 folds. `RandomizedSearchCV` instead tries a fixed number (`n_iter`) of **random** combinations. It finds nearly-as-good settings much faster, and it's the usual choice for models with many hyperparameters, like gradient boosting:

```python
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import HistGradientBoostingClassifier

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
y = churn["churned"]

space = {
    "learning_rate": [0.01, 0.03, 0.05, 0.1, 0.2],
    "max_depth": [2, 3, 4, 6, None],
    "max_iter": [100, 200, 400],
    "min_samples_leaf": [10, 20, 40],
}
search = RandomizedSearchCV(HistGradientBoostingClassifier(random_state=0), space, n_iter=12, cv=5,
                            scoring="roc_auc", random_state=0)
search.fit(X, y)
print(search.best_params_)
print("best CV AUC:", round(search.best_score_, 3))
```

12 random tries out of 225 possible combinations. (This one takes a few seconds in the browser.)

### Good habits

- Tune on the **training** set with CV. Touch the test set once.
- Start **coarse** (0.001, 0.01, 0.1, 1, 10), then zoom in around the best value.
- Don't chase tiny CV differences: within the wobble, prefer the simpler setting.
- If you must report a really honest estimate of "tuning + model" together, **nested cross-validation** wraps the whole search inside another CV loop.

:::exercise Grid search a tree
Use `GridSearchCV` with 5 folds and `scoring="roc_auc"` to tune a `DecisionTreeClassifier(random_state=0)` on the churn training data, trying `max_depth` in [2, 3, 4, 5, 6] and `min_samples_leaf` in [1, 10, 30]. Call it `search`. Store the best settings in `best_params` and the **test** AUC of the refitted best tree in `test_auc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "monthly_charge", "support_calls", "data_gb"]], c["churned"], test_size=0.25, random_state=0, stratify=c["churned"])
ref = GridSearchCV(DecisionTreeClassifier(random_state=0), {"max_depth": [2, 3, 4, 5, 6], "min_samples_leaf": [1, 10, 30]}, cv=5, scoring="roc_auc").fit(a, cc)
need("search", GridSearchCV)
same(dict(need("best_params", dict)), ref.best_params_, "best_params")
same(float(need("test_auc")), roc_auc_score(d, ref.predict_proba(b)[:, 1]), "test_auc", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

grid = {"max_depth": [2, 3, 4, 5, 6], "min_samples_leaf": [1, 10, 30]}
search = GridSearchCV(DecisionTreeClassifier(random_state=0), grid, cv=5, scoring="roc_auc")
search.fit(X_train, y_train)
best_params = search.best_params_
test_auc = roc_auc_score(y_test, search.predict_proba(X_test)[:, 1])
print(best_params, round(search.best_score_, 3), round(test_auc, 3))
```
hint: After `search.fit(X_train, y_train)`, `search.best_params_` holds the winner and `search.predict_proba(X_test)` uses the refitted best tree.
:::

:::exercise Tune alpha
Tune the Ridge penalty for the wiggly degree-10 energy model. Search `model__alpha` over [0.001, 0.01, 0.1, 1, 10] with `GridSearchCV(pipe, ..., cv=5, scoring="neg_root_mean_squared_error")` on the training data. Store the best alpha in `best_alpha` and the **test** RMSE of the refitted search in `test_rmse` (a positive number).
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=1)
pipe = Pipeline([("poly", PolynomialFeatures(10)), ("scale", StandardScaler()), ("model", Ridge())])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error
e = pd.read_csv("energy.csv")
a, b, c, d = train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=1)
p = Pipeline([("poly", PolynomialFeatures(10)), ("scale", StandardScaler()), ("model", Ridge())])
s = GridSearchCV(p, {"model__alpha": [0.001, 0.01, 0.1, 1, 10]}, cv=5, scoring="neg_root_mean_squared_error").fit(a, c)
same(float(need("best_alpha")), s.best_params_["model__alpha"], "best_alpha")
same(float(need("test_rmse")), root_mean_squared_error(d, s.predict(b)), "test_rmse (positive)", tol=1e-4)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error

energy = pd.read_csv("energy.csv")
X_train, X_test, y_train, y_test = train_test_split(
    energy[["temperature_c"]], energy["energy_kwh"], test_size=0.3, random_state=1)
pipe = Pipeline([("poly", PolynomialFeatures(10)), ("scale", StandardScaler()), ("model", Ridge())])

search = GridSearchCV(pipe, {"model__alpha": [0.001, 0.01, 0.1, 1, 10]}, cv=5, scoring="neg_root_mean_squared_error")
search.fit(X_train, y_train)
best_alpha = search.best_params_["model__alpha"]
test_rmse = root_mean_squared_error(y_test, search.predict(X_test))
print(best_alpha, round(-search.best_score_, 1), round(test_rmse, 1))
```
hint: The parameter name is `"model__alpha"` because the Ridge step is called `"model"`. Compute the test RMSE with `root_mean_squared_error(y_test, search.predict(X_test))`.
:::

:::quiz
? In a pipeline with a step named "knn", how do you name its n_neighbors in a grid?
+ "knn__n_neighbors"
- "n_neighbors"
- "knn.n_neighbors"
= Step name, two underscores, parameter name.
? What does GridSearchCV do after finding the best settings (by default)?
+ Refits a model with those settings on the whole training set
- Deletes the other models and stops
- Scores the test set automatically
= refit=True means the search object becomes the final model.
? Why is best_score_ usually a little optimistic?
+ It's the maximum of many CV scores, so some luck is baked in
- It's computed on training data
- It includes the test set
= Picking the best of many tries favours the luckiest one a bit. The test set gives the honest final number.
? For LogisticRegression, a smaller C means:
+ A stronger penalty and a simpler model
- A weaker penalty
- More iterations
= C is the inverse of the penalty strength, the opposite direction from Ridge's alpha.
:::
