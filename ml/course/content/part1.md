@@@ part
id: 1
title: Machine Learning Foundations
level: Beginner
blurb: What machine learning is, how a model learns from examples, and the habits that keep you honest: testing on unseen data and beating a simple baseline.

@@@ lesson
id: what-is-ml
title: What machine learning is
minutes: 14
summary: Learning rules from examples instead of writing them by hand: features, labels, and the main kinds of machine learning.
---
In normal programming, **you** write the rules. To sort fruit you might write: "if it's yellow and long, it's a lemon". That works until you meet a green lemon, a yellow apple, or a thousand other cases you didn't think of.

**Machine learning (ML)** flips this around. You give the computer lots of **examples with the right answers**, and it works out the rules itself. The result is called a **model**: a rule learned from data that can make a guess (a **prediction**) for new examples it has never seen.

![Two flows. Traditional programming: rules plus data go into a program that produces answers. Machine learning: data plus the answers go into training, which produces the rules (a model)](figures/rules-vs-learning.svg)

### Features and labels

Every ML dataset is a table. Each **row** is one example (a fruit, a house, a customer). The columns come in two kinds:

- **Features** are the clues the model looks at: width, height, weight. In code they're called **`X`** (capital, because it's a table).
- The **label** (also called the **target**) is the answer you want to predict: the kind of fruit. In code it's called **`y`** (small, because it's one column).

```python
import pandas as pd

fruit = pd.read_csv("fruit.csv")
print(fruit.head())

X = fruit[["width_cm", "height_cm", "weight_g"]]   # features: the clues
y = fruit["fruit"]                                  # label: the answer
print(X.shape, y.shape)
```

`X` has 150 rows and 3 columns; `y` has 150 answers, one per row. Training means: "look at these 150 examples and learn how the clues relate to the answer".

### The main kinds of machine learning

![A tree: machine learning splits into supervised learning (regression predicts a number, classification predicts a category) and unsupervised learning (clustering finds groups, dimensionality reduction squeezes many columns into a few)](figures/ml-types.svg)

| Kind | You have | The model learns to | Example |
|---|---|---|---|
| **Supervised: regression** | features + a **number** to predict | predict a number | a home's price from its size |
| **Supervised: classification** | features + a **category** to predict | pick a category | spam or not spam |
| **Unsupervised: clustering** | features only, **no answers** | find natural groups | customer segments |
| **Unsupervised: dimensionality reduction** | features only | summarise many columns with a few | a 2-D map of 50 measurements |

**Supervised** means every training example comes with the right answer, like a teacher marking homework. **Unsupervised** means there are no answers; the model looks for structure on its own.

The quickest way to tell regression from classification: look at the label. Can you average it (price, temperature, minutes)? Regression. Is it a category (yes/no, apple/orange/lemon)? Classification.

```python
import pandas as pd

housing = pd.read_csv("housing.csv")
churn = pd.read_csv("churn.csv")

print(housing["price_k"].head(3))           # a number      -> regression
print(churn["churned"].value_counts())      # 0 or 1 (no/yes) -> classification
```

`churned` is stored as 0 and 1, but it's still a category ("stayed" or "left"). Numbers that are really labels make it a classification problem.

### Where ML shows up in 2026

- **Every day:** spam filters, card-fraud alerts, recommendations ("you might also like"), maps estimating arrival times, photo search.
- **In business:** predicting which customers will leave (churn), forecasting demand, scoring leads, flagging unusual transactions.
- **In AI:** large language models (LLMs) like Claude are machine learning too: very large models trained on text to predict what comes next. The ideas in this course (training data, testing on unseen data, overfitting, evaluation) are exactly the ones AI engineers use when they fine-tune and evaluate those models.

You'll use **scikit-learn**, the standard Python library for "classic" machine learning on tables. It's free, it runs in this sandbox, and its design (create a model, `fit` it, `predict` with it) is copied by almost every other ML library.

```python
import sklearn
print("scikit-learn version:", sklearn.__version__)
```

:::exercise Features and label for houses
Load `housing.csv`. Make `X` a DataFrame with the columns `area_sqm`, `bedrooms` and `age_years`, and `y` the `price_k` column.
```python starter
import pandas as pd

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
h = pd.read_csv("housing.csv")
X_ = need("X", pd.DataFrame)
y_ = need("y", pd.Series)
same(list(X_.columns), ["area_sqm", "bedrooms", "age_years"], "X's columns")
same(y_, h["price_k"], "y")
```
```python solution
import pandas as pd

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years"]]
y = housing["price_k"]
print(X.shape, y.shape)
```
hint: Double brackets pick several columns as a table: `housing[["area_sqm", "bedrooms", "age_years"]]`. Single brackets pick one column.
:::

:::exercise Which kind of problem?
Make a dictionary `kinds` that maps each task to `"regression"`, `"classification"` or `"clustering"`:
`"predict tomorrow's temperature"`, `"is this email spam?"`, `"group shoppers by behaviour, no labels"`, `"which of 3 fruits is this?"`, `"how many minutes will delivery take?"`.
```python starter
kinds = {
    "predict tomorrow's temperature": "",
}
```
```python check
same(need("kinds", dict), {
    "predict tomorrow's temperature": "regression",
    "is this email spam?": "classification",
    "group shoppers by behaviour, no labels": "clustering",
    "which of 3 fruits is this?": "classification",
    "how many minutes will delivery take?": "regression",
}, "kinds")
```
```python solution
kinds = {
    "predict tomorrow's temperature": "regression",
    "is this email spam?": "classification",
    "group shoppers by behaviour, no labels": "clustering",
    "which of 3 fruits is this?": "classification",
    "how many minutes will delivery take?": "regression",
}
print(kinds)
```
hint: A number you could average is regression; a category is classification; no answers at all is clustering.
:::

:::quiz
? In machine learning, who writes the rules?
- The programmer, by hand
+ The computer, by learning them from examples with answers
- Nobody: models don't use rules
= You supply examples and answers; training finds the rule. The learned rule is the model.
? In a table of houses, which column would be the label for predicting price?
- area_sqm
- neighborhood
+ price_k
= The label (target) is what you want to predict. Everything you use as clues is a feature.
? A model predicts whether a customer will cancel (yes/no). This is:
- Regression
+ Classification
- Clustering
= The answer is a category (yes or no), so it's classification, even if it's stored as 0 and 1.
? What makes learning "unsupervised"?
- It runs without a computer
+ The training data has no answers (labels)
- It uses more data
= Without labels, the model can only look for structure, such as groups.
:::

@@@ lesson
id: first-model
title: Your first model: fit and predict
minutes: 16
summary: The three-step scikit-learn pattern (create, fit, predict) with a straight-line model and a nearest-neighbours classifier.
---
Every model in scikit-learn is used the same way, in three steps:

![Three boxes in a row: 1. create the model, LinearRegression(); 2. fit it to examples, model.fit(X, y), which learns the rule; 3. predict new rows, model.predict(new_X), which uses the rule](figures/fit-predict.svg)

1. **Create** an empty model: `model = LinearRegression()`. It knows nothing yet.
2. **Fit** it to examples: `model.fit(X, y)`. This is the **training**: the model studies the features and answers and stores what it learned inside itself.
3. **Predict**: `model.predict(new_X)` gives answers for new rows.

A model object in scikit-learn is called an **estimator**. Once you know these three steps, you can use any of the dozens of models in the library.

### A model that predicts a number

Do students who study more score higher in maths? A **linear regression** model draws the best straight line through the points, and then reads predictions off the line.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

students = pd.read_csv("students.csv")
X = students[["hours_studied"]]     # a table with one column (note the double brackets)
y = students["math"]

model = LinearRegression()          # 1. create
model.fit(X, y)                     # 2. fit (train)

new = pd.DataFrame({"hours_studied": [2, 6, 10]})
print(model.predict(new).round(1))  # 3. predict
```

The model predicts about 41 points for 2 hours of study and about 77 for 10. It learned that each extra hour is worth roughly 4.5 points:

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

students = pd.read_csv("students.csv")
model = LinearRegression().fit(students[["hours_studied"]], students["math"])

print("slope:", model.coef_.round(2))          # points per extra hour
print("intercept:", round(model.intercept_, 1)) # predicted score at 0 hours
```

Things a model **learned** from data end with an underscore in scikit-learn: `coef_`, `intercept_`. They only exist after `fit`. (`.fit()` also hands back the model itself, which is why `LinearRegression().fit(...)` on one line works.)

### X must be a table

The most common beginner error: passing a single column as `students["hours_studied"]` (a Series, 1-D). scikit-learn always wants **X as a table** (2-D), even with one feature, so use **double brackets**: `students[["hours_studied"]]`. The label `y` is the other way round: one column, single brackets.

```python error
import pandas as pd
from sklearn.linear_model import LinearRegression

students = pd.read_csv("students.csv")
LinearRegression().fit(students["hours_studied"], students["math"])
```

### A model that predicts a category

Now a classifier. **k-nearest neighbours** (KNN) is the simplest idea in ML: to label a new fruit, find the `k` most similar fruits in the training data and take a vote. Same three steps:

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm"]]
y = fruit["fruit"]

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, y)

mystery = pd.DataFrame({"width_cm": [6.0, 7.5], "height_cm": [8.5, 7.1]})
print(knn.predict(mystery))
```

A narrow, tall fruit (6 cm wide, 8.5 cm high) is called a lemon; a round 7.5 by 7.1 cm one is an apple. `n_neighbors=5` is a setting **you** choose before training. Settings like this are called **hyperparameters**, to tell them apart from the things the model learns.

For classifiers, `predict_proba` shows how sure the model is: the share of the 5 neighbours that voted for each class, in the order of `knn.classes_`.

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
knn = KNeighborsClassifier(n_neighbors=5).fit(fruit[["width_cm", "height_cm"]], fruit["fruit"])

mystery = pd.DataFrame({"width_cm": [7.6], "height_cm": [7.3]})
print(knn.classes_)
print(knn.predict_proba(mystery))
print(knn.predict(mystery))
```

This fruit is borderline: some of its neighbours are apples and some are oranges, and the majority wins. Probabilities like these are often more useful than the bare answer.

:::exercise Price from size
Fit a `LinearRegression` called `model` that predicts `price_k` from `area_sqm` in `housing.csv`. Then store the predicted price of a 100 m² home in `pred_100` (a single number).
```python starter
import pandas as pd
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
from sklearn.linear_model import LinearRegression
h = pd.read_csv("housing.csv")
m = need("model", LinearRegression)
if not hasattr(m, "coef_"):
    raise AssertionError("Call model.fit(X, y) to train the model.")
ref = LinearRegression().fit(h[["area_sqm"]], h["price_k"])
same(float(m.coef_[0]), float(ref.coef_[0]), "the model's slope (did you use area_sqm and price_k?)", tol=1e-6)
same(float(need("pred_100")), float(ref.predict(pd.DataFrame({"area_sqm": [100]}))[0]), "pred_100", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
model = LinearRegression()
model.fit(housing[["area_sqm"]], housing["price_k"])
pred_100 = model.predict(pd.DataFrame({"area_sqm": [100]}))[0]
print(round(pred_100, 1))
```
hint: `model.predict(...)` returns an array; take its first value with `[0]`.
:::

:::exercise Name that fruit
Train a `KNeighborsClassifier` with `n_neighbors=7` called `knn` on `fruit.csv`, using all three measurements (`width_cm`, `height_cm`, `weight_g`). Store its prediction for a fruit 7.9 cm wide, 7.8 cm high and 195 g in `answer` (a string such as `"apple"`).
```python starter
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")

```
```python check
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
f = pd.read_csv("fruit.csv")
k = need("knn", KNeighborsClassifier)
same(k.n_neighbors, 7, "n_neighbors")
cols = ["width_cm", "height_cm", "weight_g"]
ref = KNeighborsClassifier(n_neighbors=7).fit(f[cols], f["fruit"])
row = pd.DataFrame({"width_cm": [7.9], "height_cm": [7.8], "weight_g": [195]})
same(str(need("answer")), str(ref.predict(row)[0]), "answer")
```
```python solution
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
knn = KNeighborsClassifier(n_neighbors=7).fit(X, fruit["fruit"])
row = pd.DataFrame({"width_cm": [7.9], "height_cm": [7.8], "weight_g": [195]})
answer = knn.predict(row)[0]
print(answer)
```
hint: The new row must have the same columns, in the same order, as the training data.
:::

:::quiz
? What does model.fit(X, y) do?
- Draws a chart of X and y
+ Trains the model: it learns from the examples and stores what it learned
- Predicts y for new rows
= fit is training. predict comes after, and uses what fit stored.
? Why does students[["hours_studied"]] have two pairs of brackets?
+ scikit-learn needs X as a table (2-D), even with one column
- It makes the code run faster
- It removes missing values
= Single brackets give a Series (1-D). Double brackets give a one-column DataFrame, which is what fit expects for X.
? In scikit-learn, what does a trailing underscore, as in coef_, tell you?
- The attribute is private
+ It was learned from the data during fit
- It's a hyperparameter you set
= Learned attributes end with _ and only exist after fit.
? n_neighbors=5 in KNeighborsClassifier is:
- Something the model learns from data
+ A hyperparameter: a setting you choose before training
- The number of features
= Hyperparameters are chosen by you; parameters (like coef_) are learned.
:::

@@@ lesson
id: train-test
title: Train and test: checking on unseen data
minutes: 16
summary: Why a model must be judged on data it never saw, how train_test_split works, and how to spot a model that memorised.
---
A model is only useful if it works on **new** data: next month's customers, tomorrow's emails. So you can't judge it on the examples it learned from. That's like giving students the exam questions to study, then using the same questions in the exam: they could score 100% by memorising.

The fix is simple: before training, **hold back** some rows. Train on the rest, then test on the held-back rows the model has never seen.

![A bar of 150 rows split into two parts: 112 training rows (75%) used for fit, and 38 test rows (25%) kept hidden until the end and used only for score](figures/train-test-split.svg)

- The **training set** is what the model learns from.
- The **test set** is the model's final exam. Use it only to measure, never to learn from.
- A typical split is 75/25 or 80/20.

### train_test_split

```python
import pandas as pd
from sklearn.model_selection import train_test_split

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm"]]
y = fruit["fruit"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)
```

It shuffles the rows and cuts them into four pieces. Learn the order by heart, because it's always the same: **`X_train, X_test, y_train, y_test`**.

- `test_size=0.25` keeps 25% for testing.
- `random_state=42` fixes the shuffle, so you get the same split every time you run it (any number works; 42 is just tradition). Without it, every run gives a different split and different scores.

### Score on the test set

Every model has a `score` method. For classifiers it's **accuracy**, the share of correct answers; for regressors it's R², which you'll meet in Lesson 6.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
X_train, X_test, y_train, y_test = train_test_split(X, fruit["fruit"], test_size=0.25, random_state=3)

knn = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
print("training accuracy:", round(knn.score(X_train, y_train), 3))
print("test accuracy:    ", round(knn.score(X_test, y_test), 3))
```

The model gets 84% of its training fruit right but 82% of the test fruit. The test accuracy is the honest number: it's how the model does on fruit it has never seen.

### Spotting memorisation

With `n_neighbors=1`, each training fruit's nearest neighbour is **itself**, so the model gets every training fruit right: it has simply memorised them. Training accuracy says "perfect"; the test set says otherwise:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X = fruit[["width_cm", "height_cm", "weight_g"]]
X_train, X_test, y_train, y_test = train_test_split(X, fruit["fruit"], test_size=0.25, random_state=3)

for k in [1, 5, 15]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
    print(f"k={k:>2}  train {knn.score(X_train, y_train):.3f}   test {knn.score(X_test, y_test):.3f}")
```

k=1 is perfect on training data but the worst on the test set. A big gap between training and test scores is the warning sign of **overfitting**: the model learned the noise in its training data, not the general pattern. Part 2 shows how to find the sweet spot.

### Keep the classes balanced with stratify

If a class is rare, a random split might put too few of them in the test set. `stratify=y` keeps the same mix of classes in both parts:

```python
import pandas as pd
from sklearn.model_selection import train_test_split

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)
print("all:  ", y.mean().round(3))
print("train:", y_train.mean().round(3))
print("test: ", y_test.mean().round(3))
```

With `stratify`, about 27.5% of customers churned in the full data, in training and in testing alike. Use it for classification whenever you split.

:::exercise Split the churn data
Load `churn.csv`. Use `X = churn[["tenure_months", "monthly_charge", "support_calls"]]` and `y = churn["churned"]`. Split them into `X_train, X_test, y_train, y_test` with 30% for testing, `random_state=1` and stratified by `y`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
c = pd.read_csv("churn.csv")
r = train_test_split(c[["tenure_months", "monthly_charge", "support_calls"]], c["churned"], test_size=0.3, random_state=1, stratify=c["churned"])
for name, exp in zip(["X_train", "X_test", "y_train", "y_test"], r):
    got = need(name)
    same(len(got), len(exp), f"the number of rows in {name}")
    same(list(got.index), list(exp.index), f"the rows in {name} (check test_size, random_state and stratify)")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
print(X_train.shape, X_test.shape)
```
hint: `train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)` returns four things, in the order X_train, X_test, y_train, y_test.
:::

:::exercise Train versus test
Using the fruit split below, train a `KNeighborsClassifier(n_neighbors=3)` called `knn` on the training data. Store its training accuracy in `train_acc` and its test accuracy in `test_acc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.25, random_state=7, stratify=fruit["fruit"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
f = pd.read_csv("fruit.csv")
a, b, c, d = train_test_split(f[["width_cm", "height_cm", "weight_g"]], f["fruit"], test_size=0.25, random_state=7, stratify=f["fruit"])
ref = KNeighborsClassifier(n_neighbors=3).fit(a, c)
same(need("knn", KNeighborsClassifier).n_neighbors, 3, "n_neighbors")
same(float(need("train_acc")), ref.score(a, c), "train_acc")
same(float(need("test_acc")), ref.score(b, d), "test_acc (score on X_test, y_test)")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.25, random_state=7, stratify=fruit["fruit"])
knn = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
train_acc = knn.score(X_train, y_train)
test_acc = knn.score(X_test, y_test)
print(round(train_acc, 3), round(test_acc, 3))
```
hint: `knn.score(X_train, y_train)` and `knn.score(X_test, y_test)`.
:::

:::quiz
? Why keep a test set the model never trains on?
- To make training faster
+ To measure how well the model does on new, unseen data
- Because scikit-learn requires it
= Scoring on training data rewards memorising. Only unseen data shows real performance.
? A model scores 1.00 on training data and 0.70 on test data. The most likely problem is:
- Underfitting
+ Overfitting: it memorised the training data
- A bug in train_test_split
= A big train/test gap means the model learned noise that doesn't carry over to new rows.
? What does random_state=42 do in train_test_split?
- Uses 42% of rows for testing
+ Fixes the shuffle so the split is the same every run
- Makes the split more accurate
= It seeds the random shuffle. Any number works; the point is repeatability.
? When should you pass stratify=y?
+ For classification, so train and test keep the same mix of classes
- For regression only
- Never: it causes leakage
= Stratifying keeps rare classes represented in both parts.
:::

@@@ lesson
id: workflow-and-baselines
title: The ML workflow and baselines
minutes: 15
summary: The steps of every ML project, getting X and y into shape, and the "dumb" baseline every model must beat.
---
Real projects follow the same steps every time. This course is organised around them:

![Seven steps in a row: 1. define the question, 2. get the data, 3. split train/test, 4. prepare features, 5. train models, 6. evaluate on test, 7. deploy and monitor, with an arrow looping back from evaluate to prepare to show that you iterate](figures/ml-workflow.svg)

1. **Define the question.** What exactly do you predict, for whom, and what will people do with the prediction? "Which customers will cancel in the next month, so the retention team can call them" is a good question.
2. **Get the data**, and check it (Python for Data skills).
3. **Split** into training and test sets, **before** you look closely at patterns.
4. **Prepare features**: numbers only, no missing values, sensible scales (Part 4).
5. **Train** a few models.
6. **Evaluate** them on data they didn't train on. Go back to step 4 or 5 and improve.
7. **Deploy and monitor**: use the model, and watch that it keeps working (Lesson 23).

### Getting X and y into shape

scikit-learn models need:

| Rule | Why | How |
|---|---|---|
| X is a table (2-D), y is one column | that's the format `fit` expects | `df[["a", "b"]]` and `df["target"]` |
| Only numbers in X | models do arithmetic | encode text columns (Lesson 16) |
| No missing values (for most models) | you can't multiply by "nothing" | fill or drop them (Lesson 16) |
| The label is **not** in X | otherwise the model just copies the answer | `df.drop(columns="target")` |

A quick way to build X from "every column except a few":

```python
import pandas as pd

churn = pd.read_csv("churn.csv")
print(churn.dtypes)

X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
print(X.columns.tolist())
```

`customer_id` is dropped because an ID number is just a name. A model could find accidental patterns in it ("IDs above 1500 churn more") that mean nothing for new customers.

### Always start with a baseline

How good is "80% accuracy"? It depends. If 80% of customers stay, a "model" that always says **"stays"** is already 80% accurate, without learning anything.

A **baseline** is the score of the dumbest sensible guess. scikit-learn has them built in:

- `DummyClassifier()` always predicts the most common class.
- `DummyRegressor()` always predicts the average of the training labels.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

baseline = DummyClassifier().fit(X_train, y_train)
knn = KNeighborsClassifier(n_neighbors=15).fit(X_train, y_train)
print("baseline accuracy:", round(baseline.score(X_test, y_test), 3))
print("knn accuracy:     ", round(knn.score(X_test, y_test), 3))
```

The baseline already gets 0.724, because about 72% of customers stay. The real model does better, but by less than "0.77 accuracy" sounds on its own. Always report your model **next to** the baseline. If a model can't beat it, it hasn't learned anything useful.

The same idea for numbers:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

baseline = DummyRegressor().fit(X_train, y_train)
linear = LinearRegression().fit(X_train, y_train)
print("baseline guess for every home:", round(baseline.predict(X_test)[0], 1))
print("baseline R²:", round(baseline.score(X_test, y_test), 3))
print("linear R²:  ", round(linear.score(X_test, y_test), 3))
```

The baseline guesses the same average price for every home and scores an R² just below 0: it explains none of the differences between homes (it's slightly negative because the test homes' average isn't exactly the training average). The linear model explains most of the variation. You'll learn exactly what R² means in Lesson 6.

:::exercise Beat the baseline
Using the split below, store the test accuracy of a `DummyClassifier()` in `base_acc` and of a `KNeighborsClassifier(n_neighbors=25)` in `knn_acc`, both trained on the training data. Then set `better` to `True` if KNN beats the baseline, else `False`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "support_calls"]], c["churned"], test_size=0.3, random_state=3, stratify=c["churned"])
ba = DummyClassifier().fit(a, cc).score(b, d)
ka = KNeighborsClassifier(n_neighbors=25).fit(a, cc).score(b, d)
same(float(need("base_acc")), ba, "base_acc")
same(float(need("knn_acc")), ka, "knn_acc")
same(need("better"), bool(ka > ba), "better")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)

base_acc = DummyClassifier().fit(X_train, y_train).score(X_test, y_test)
knn_acc = KNeighborsClassifier(n_neighbors=25).fit(X_train, y_train).score(X_test, y_test)
better = knn_acc > base_acc
print(round(base_acc, 3), round(knn_acc, 3), better)
```
hint: Fit each model on `X_train, y_train`, then `.score(X_test, y_test)`.
:::

:::exercise Features without leaks
From `housing.csv`, build `X` with **every** column except `home_id`, `neighborhood` (text, which you'll learn to handle later) and the label `price_k`. Make `y` the `price_k` column.
```python starter
import pandas as pd

housing = pd.read_csv("housing.csv")

```
```python check
import pandas as pd
X_ = need("X", pd.DataFrame)
y_ = need("y", pd.Series)
same(sorted(X_.columns), sorted(["area_sqm", "bedrooms", "age_years", "distance_km"]), "X's columns")
if "price_k" in X_.columns:
    raise AssertionError("The label price_k must not be in X.")
same(y_.name, "price_k", "y's name")
```
```python solution
import pandas as pd

housing = pd.read_csv("housing.csv")
X = housing.drop(columns=["home_id", "neighborhood", "price_k"])
y = housing["price_k"]
print(X.columns.tolist())
```
hint: `housing.drop(columns=[...])` returns every other column.
:::

:::quiz
? 90% of emails are not spam. A model is 90% accurate. What do you know?
- It's an excellent model
+ It may have learned nothing: always saying "not spam" also scores 90%
- It's overfitting
= Compare with a baseline. A DummyClassifier would score 90% here.
? What does DummyRegressor() predict by default?
- Zero for every row
+ The average of the training labels, for every row
- A random number
= It's the simplest sensible guess, so a real model must beat it.
? Why drop customer_id from the features?
+ An ID is just a name; any pattern in it is accidental and won't hold for new customers
- IDs are text
- It makes training slower
= IDs carry no real information about behaviour, so they only invite fake patterns.
? Which step should come before you study patterns in the data closely?
- Deploying the model
+ Splitting off the test set
- Tuning hyperparameters
= Split first, so nothing you learn from the data (even by eye) leaks from the test set into your choices.
:::
