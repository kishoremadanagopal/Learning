@@@ part
id: 3
title: Classification: Predicting Categories
level: Intermediate
blurb: Predict yes/no and which-kind answers, measure them properly (accuracy is not enough), and meet the models that power real systems: logistic regression, nearest neighbours, decision trees, random forests and gradient boosting.

@@@ lesson
id: logistic-regression
title: Logistic regression: predicting yes or no
minutes: 17
summary: Turn a linear score into a probability with the S-shaped curve, then into a decision. The workhorse model for yes/no questions.
---
Will this customer leave? Is this transaction fraud? Most real classification questions have two answers. Despite its name, **logistic regression** is a **classification** model, and usually the first one to try for yes/no questions.

It works in three steps:

1. Like linear regression, it adds up the features times coefficients to get a **score**. Higher score means "more likely yes".
2. It squeezes the score through the **sigmoid** (S-shaped) function, which turns any number into a **probability** between 0 and 1.
3. It turns the probability into a **decision**: yes if the probability is at least 0.5 (the **threshold**), otherwise no.

![An S-shaped curve: the model's predicted probability of churning (from 0 to 1) against tenure in months, for a customer paying 50 a month with one support call. The probability starts just above 0.5 for brand-new customers and falls towards 0 for long-standing ones. A dashed line marks the 0.5 threshold. Real customers are shown as dots at 0 (stayed) and 1 (left)](figures/sigmoid.svg)

### Fit and predict probabilities

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

model = LogisticRegression().fit(X_train, y_train)

print(model.predict_proba(X_test.head()).round(3))   # columns: P(stayed), P(left)
print(model.predict(X_test.head()))                   # 1 if P(left) >= 0.5
print("test accuracy:", round(model.score(X_test, y_test), 3))
```

`predict_proba` gives one column per class, in the order of `model.classes_` (here 0 then 1). The second column, `predict_proba(X)[:, 1]`, is the probability of "yes": it's the one you'll use most.

The test accuracy is 0.76, against the baseline's 0.724 from Lesson 4. Better, but keep that baseline in mind: the next lesson shows why accuracy alone can be misleading here.

### Reading the coefficients

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
model = LogisticRegression().fit(X_train, y_train)

print(pd.Series(model.coef_[0], index=X.columns).round(3))
```

The **sign** tells you the direction:

- `tenure_months` is negative: the longer someone has been a customer, the **less** likely they are to leave.
- `monthly_charge` and `support_calls` are positive: higher bills and more complaints mean **more** likely to leave.

The size is harder to read than in linear regression, because it's on the "score" scale, not the probability scale. One handy fact: each extra support call multiplies the **odds** of leaving by e^0.475 ≈ 1.6. (Odds are probability ÷ (1 − probability): a 20% chance is odds of 0.25.) The same coefficient moves the **probability** by different amounts depending on where on the S-curve a customer is.

### More than two classes

Logistic regression also handles several classes, like the three fruits. scikit-learn does it automatically: one probability per class, summing to 1, and the prediction is the class with the highest probability.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.25, random_state=3, stratify=fruit["fruit"])

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print(model.classes_)
print(model.predict_proba(X_test.head(3)).round(2))
print("test accuracy:", round(model.score(X_test, y_test), 3))
```

`max_iter=1000` gives the training more steps to settle. If you ever see a `ConvergenceWarning`, raising `max_iter` (or scaling the features, Lesson 15) usually fixes it.

:::exercise How likely is she to leave?
Train a `LogisticRegression` called `model` on **all** rows of `churn.csv`, using `tenure_months` and `support_calls`. Store the probability that a customer with 3 months' tenure and 4 support calls **leaves** in `p_leave` (a number between 0 and 1).
```python starter
import pandas as pd
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")

```
```python check
import pandas as pd
from sklearn.linear_model import LogisticRegression
c = pd.read_csv("churn.csv")
ref = LogisticRegression().fit(c[["tenure_months", "support_calls"]], c["churned"])
row = pd.DataFrame({"tenure_months": [3], "support_calls": [4]})
same(float(need("p_leave")), float(ref.predict_proba(row)[0, 1]), "p_leave (the probability of class 1)", tol=1e-4)
```
```python solution
import pandas as pd
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
model = LogisticRegression().fit(churn[["tenure_months", "support_calls"]], churn["churned"])

customer = pd.DataFrame({"tenure_months": [3], "support_calls": [4]})
p_leave = model.predict_proba(customer)[0, 1]
print(round(p_leave, 3))
```
hint: `model.predict_proba(customer)` returns one row with two columns; the probability of leaving is `[0, 1]` (row 0, column 1).
:::

:::exercise Who gets a call?
Using the split below, fit a `LogisticRegression()` on the training data. Store how many **test** customers it predicts will leave in `n_flagged`, and its test accuracy in `acc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "monthly_charge", "support_calls", "data_gb"]], c["churned"], test_size=0.3, random_state=8, stratify=c["churned"])
m = LogisticRegression().fit(a, cc)
same(int(need("n_flagged")), int(m.predict(b).sum()), "n_flagged")
same(float(need("acc")), m.score(b, d), "acc")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)

model = LogisticRegression().fit(X_train, y_train)
n_flagged = model.predict(X_test).sum()      # predictions are 0/1, so the sum counts the 1s
acc = model.score(X_test, y_test)
print(n_flagged, round(acc, 3))
```
hint: Predictions are 0s and 1s, so `.sum()` counts the predicted leavers.
:::

:::quiz
? Logistic regression is used for:
- Predicting numbers like prices
+ Classification, especially yes/no questions
- Clustering
= The name is historical. It predicts the probability of a class.
? What does the sigmoid function do?
+ Turns any score into a probability between 0 and 1
- Removes outliers
- Picks the features
= The S-curve maps very negative scores near 0 and very positive scores near 1.
? model.predict_proba(X)[:, 1] gives:
- The predicted class
+ The probability of the second class in model.classes_ (here: leaving)
- The model's accuracy
= One column per class, in the order of classes_. Column 1 is class 1.
? A coefficient for support_calls is positive. This means:
+ More support calls make the model predict a higher chance of churning
- Support calls reduce churn
- Each call adds exactly 0.47 to the probability
= The sign gives the direction. The effect on probability isn't a fixed amount, because of the S-curve.
:::

@@@ lesson
id: classification-metrics
title: Beyond accuracy: precision and recall
minutes: 18
summary: The confusion matrix, precision, recall and F1: what they mean, how to compute them, and how to choose the one that matters.
---
The churn model from the last lesson is 76% accurate. Sounds decent. But the business question is: **of the customers who really leave, how many did we catch?** Accuracy can't answer that. The **confusion matrix** can.

### The confusion matrix

It counts the four possible outcomes on the test set:

![A 2-by-2 grid with real answer down the side (stayed, left) and prediction across the top (stay, leave). True negatives 167: stayed, predicted stay. False positives 14: stayed but predicted leave (false alarms). False negatives 46: left but predicted stay (missed). True positives 23: left, predicted leave (caught)](figures/confusion-matrix.svg)

| | Predicted "stays" (0) | Predicted "leaves" (1) |
|---|---|---|
| **Really stayed (0)** | **True negative (TN)**: correctly left alone | **False positive (FP)**: a false alarm |
| **Really left (1)** | **False negative (FN)**: missed | **True positive (TP)**: caught |

"Positive" means the class you're looking for (leaving, fraud, spam), not "good".

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)

print(confusion_matrix(y_test, pred))
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print("TN", tn, " FP", fp, " FN", fn, " TP", tp)
```

Of the 69 customers who really left, the model caught only **23** and missed **46**. The 76% accuracy comes mostly from correctly saying "stays" about customers who were staying anyway.

### Precision and recall

Two questions, two metrics:

| Metric | Question | Formula | Here |
|---|---|---|---|
| **Precision** | When the model says "leaves", how often is it right? | TP ÷ (TP + FP) | 23 ÷ 37 = 0.62 |
| **Recall** | Of everyone who really left, how many did it catch? | TP ÷ (TP + FN) | 23 ÷ 69 = 0.33 |
| **F1 score** | One number balancing both | 2 × P × R ÷ (P + R) | 0.43 |
| **Accuracy** | How often is it right overall? | (TP + TN) ÷ all | 190 ÷ 250 = 0.76 |

So: when this model raises the alarm it's right 62% of the time (decent precision), but it catches only a third of leavers (poor recall).

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)

print("precision:", round(precision_score(y_test, pred), 3))
print("recall:   ", round(recall_score(y_test, pred), 3))
print("F1:       ", round(f1_score(y_test, pred), 3))
print(classification_report(y_test, pred, target_names=["stayed", "left"]))
```

`classification_report` prints precision, recall and F1 for **each** class, plus **support** (how many test rows are in that class). Read the "left" row for the positive class.

### Which one matters?

It depends on which mistake costs more:

| Situation | Worse mistake | Focus on |
|---|---|---|
| Spam filter | Hiding a real email (false positive) | **Precision** |
| Cancer screening, fraud alerts | Missing a real case (false negative) | **Recall** |
| Churn: a cheap retention offer | Missing a leaver (false negative) | **Recall**, with precision not too low |
| You need one balanced number | both | **F1** |

You can usually trade one for the other: flag more people and recall goes up while precision goes down. The next lesson shows how.

### Drawing it

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
model = LogisticRegression().fit(X_train, y_train)

ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=["stayed", "left"], cmap="Blues")
plt.title("Churn model on the test set")
plt.show()
```

:::exercise Count the outcomes
Using the predictions below, store the four counts in `tn`, `fp`, `fn`, `tp`, then compute `precision` and `recall` **by hand** from them (not with the scikit-learn functions).
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=5, stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "support_calls"]], c["churned"], test_size=0.3, random_state=5, stratify=c["churned"])
p = LogisticRegression().fit(a, cc).predict(b)
TN, FP, FN, TP = confusion_matrix(d, p).ravel()
for name, val in [("tn", TN), ("fp", FP), ("fn", FN), ("tp", TP)]:
    same(int(need(name)), int(val), name)
same(float(need("precision")), TP / (TP + FP), "precision = tp / (tp + fp)")
same(float(need("recall")), TP / (TP + FN), "recall = tp / (tp + fn)")
if "precision_score" in __source__ or "recall_score" in __source__:
    raise AssertionError("Compute precision and recall from the four counts, without precision_score / recall_score.")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=5, stratify=y)
pred = LogisticRegression().fit(X_train, y_train).predict(X_test)

tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
precision = tp / (tp + fp)
recall = tp / (tp + fn)
print(tn, fp, fn, tp, round(precision, 3), round(recall, 3))
```
hint: `confusion_matrix(y_test, pred).ravel()` gives the counts in the order tn, fp, fn, tp.
:::

:::exercise Precision or recall?
Make a dictionary `focus` mapping each system to `"precision"` or `"recall"`, depending on which mistake is worse: `"spam filter"`, `"airport weapon scanner"`, `"recommend a film"`, `"detect a gas leak"`.
```python starter
focus = {}
```
```python check
same(need("focus", dict), {"spam filter": "precision", "airport weapon scanner": "recall", "recommend a film": "precision", "detect a gas leak": "recall"}, "focus")
```
```python solution
focus = {
    "spam filter": "precision",            # a false alarm hides a real email
    "airport weapon scanner": "recall",    # missing a weapon is far worse than an extra bag check
    "recommend a film": "precision",       # bad suggestions annoy; missing one good film is harmless
    "detect a gas leak": "recall",         # never miss a real leak
}
print(focus)
```
hint: Ask "is a false alarm worse, or a miss?" False alarms hurt precision; misses hurt recall.
:::

:::quiz
? A fraud model has recall 0.9. What does that mean?
+ It catches 90% of the real frauds
- 90% of its alerts are real frauds
- It's right 90% of the time overall
= Recall = TP / (TP + FN): the share of real positives that were found.
? A false positive in a spam filter is:
- A spam email that reached the inbox
+ A real email wrongly sent to spam
- A spam correctly blocked
= "Positive" is the predicted class (spam). False positive: predicted spam, but it wasn't.
? Why can a model be 95% accurate and still useless?
+ If 95% of rows are one class, always predicting it scores 95% while catching nothing
- Accuracy above 90% is impossible
- Because accuracy is computed on training data
= With imbalanced classes, look at recall and precision for the rare class.
? Which metric balances precision and recall in one number?
- Support
+ F1 score
- R²
= F1 is the harmonic mean of precision and recall; it's low if either one is low.
:::

@@@ lesson
id: thresholds-roc
title: Thresholds, ROC curves and AUC
minutes: 17
summary: Move the 0.5 threshold to trade precision for recall, compare models at every threshold with the ROC curve and AUC, and handle rare classes.
---
`predict` uses a threshold of 0.5: "leaves" if the probability is at least 50%. Nothing makes 0.5 special. If missing a leaver costs more than a false alarm, flag people at a **lower** probability.

### Moving the threshold

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
proba = LogisticRegression().fit(X_train, y_train).predict_proba(X_test)[:, 1]

for threshold in [0.5, 0.4, 0.3, 0.2]:
    pred = (proba >= threshold).astype(int)
    print(f"threshold {threshold}:  flagged {pred.sum():>3}   precision {precision_score(y_test, pred):.2f}   recall {recall_score(y_test, pred):.2f}")
```

Lowering the threshold flags more customers. Recall climbs from 0.33 to 0.83: you catch most leavers. Precision falls from 0.62 to 0.40: more of the people you call were going to stay anyway. That's the **precision–recall trade-off**.

![Precision and recall plotted against the threshold from 0.05 to 0.8. Recall starts near 1 at low thresholds and falls as the threshold rises; precision starts low and rises. The default threshold of 0.5 is marked, along with a lower threshold of 0.3 that catches far more leavers](figures/threshold-tradeoff.svg)

How to pick the threshold? From the **costs**. If a retention offer costs 10 and a lost customer costs 200, catching leavers matters far more than wasting some offers, so a low threshold makes sense. Pick it on validation data (Lesson 18), never by peeking at the test set.

### The ROC curve: every threshold at once

To compare **models** without choosing a threshold, look at all thresholds together. The **ROC curve** plots, for every threshold:

- the **true positive rate** (recall: share of leavers caught) on the y-axis, against
- the **false positive rate** (share of stayers wrongly flagged) on the x-axis.

![ROC curves: the logistic model's curve bows up towards the top-left corner, well above the diagonal dashed line of random guessing. The area under the model's curve is 0.76. A perfect model would go straight up to the top-left corner](figures/roc-curve.svg)

- A model that guesses at random follows the diagonal.
- A perfect model goes straight up to the top-left corner: it catches everyone with no false alarms.
- The **AUC** (area under the curve) sums it up in one number: 0.5 is random guessing, 1.0 is perfect. AUC is also the chance that the model gives a random leaver a higher probability than a random stayer.

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, RocCurveDisplay

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
model = LogisticRegression().fit(X_train, y_train)

proba = model.predict_proba(X_test)[:, 1]
print("AUC:", round(roc_auc_score(y_test, proba), 3))

RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.plot([0, 1], [0, 1], linestyle="--", color="grey")
plt.title("ROC curve")
plt.show()
```

Note that `roc_auc_score` needs the **probabilities**, not the 0/1 predictions: it's about how well the model **ranks** customers.

### Rare classes: class_weight

When the positive class is rare, models drift towards predicting the common class. `class_weight="balanced"` tells the model that each mistake on the rare class counts more (in proportion to how rare it is):

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

for weights in [None, "balanced"]:
    model = LogisticRegression(class_weight=weights).fit(X_train, y_train)
    pred = model.predict(X_test)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"class_weight={weights}:  precision {precision_score(y_test, pred):.2f}  recall {recall_score(y_test, pred):.2f}  AUC {auc:.3f}")
```

Recall jumps from 0.33 to 0.71, precision drops, and AUC barely moves. That's a clue: balancing mostly moves the threshold. The model ranks customers about as well either way; it just flags more of them.

:::exercise A lower threshold
Using the probabilities below, make `pred` the 0/1 predictions at a threshold of **0.35**, then store the recall and precision of those predictions in `recall_35` and `precision_35`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)
proba = LogisticRegression().fit(X_train, y_train).predict_proba(X_test)[:, 1]

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "monthly_charge", "support_calls", "data_gb"]], c["churned"], test_size=0.3, random_state=8, stratify=c["churned"])
pr = LogisticRegression().fit(a, cc).predict_proba(b)[:, 1]
p = (pr >= 0.35).astype(int)
same(list(map(int, need("pred"))), list(map(int, p)), "pred")
same(float(need("recall_35")), recall_score(d, p), "recall_35")
same(float(need("precision_35")), precision_score(d, p), "precision_35")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)
proba = LogisticRegression().fit(X_train, y_train).predict_proba(X_test)[:, 1]

pred = (proba >= 0.35).astype(int)
recall_35 = recall_score(y_test, pred)
precision_35 = precision_score(y_test, pred)
print(round(recall_35, 3), round(precision_35, 3))
```
hint: `(proba >= 0.35)` gives True/False; `.astype(int)` turns it into 1/0.
:::

:::exercise Compare by AUC
With the same split, compute the test AUC of a `LogisticRegression()` using **only** `tenure_months` in `auc_one`, and using all four features in `auc_four`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
c = pd.read_csv("churn.csv")
a, b, cc, d = train_test_split(c[["tenure_months", "monthly_charge", "support_calls", "data_gb"]], c["churned"], test_size=0.3, random_state=8, stratify=c["churned"])
one = roc_auc_score(d, LogisticRegression().fit(a[["tenure_months"]], cc).predict_proba(b[["tenure_months"]])[:, 1])
four = roc_auc_score(d, LogisticRegression().fit(a, cc).predict_proba(b)[:, 1])
same(float(need("auc_one")), one, "auc_one")
same(float(need("auc_four")), four, "auc_four")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = churn[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8, stratify=y)

one = LogisticRegression().fit(X_train[["tenure_months"]], y_train)
auc_one = roc_auc_score(y_test, one.predict_proba(X_test[["tenure_months"]])[:, 1])
four = LogisticRegression().fit(X_train, y_train)
auc_four = roc_auc_score(y_test, four.predict_proba(X_test)[:, 1])
print(round(auc_one, 3), round(auc_four, 3))
```
hint: Remember `roc_auc_score` wants probabilities: `model.predict_proba(...)[:, 1]`. For one feature, use `X_train[["tenure_months"]]` and the same column of `X_test`.
:::

:::quiz
? You lower the threshold from 0.5 to 0.3. What usually happens?
+ Recall goes up, precision goes down
- Both go up
- Both go down
= More rows are flagged: you catch more real positives but also raise more false alarms.
? A model's AUC is 0.5. It is:
- Perfect
+ No better than random guessing at ranking
- Half as good as random
= 0.5 is the diagonal line. 1.0 is perfect ranking.
? What does roc_auc_score need as its second argument?
- The 0/1 predictions
+ The predicted probabilities (or scores) for the positive class
- The training data
= AUC measures ranking, so it needs the probabilities, not hard decisions.
? How should you choose a threshold?
+ From the costs of each kind of mistake, using validation data
- Always 0.5
- The value that gives the highest test accuracy
= The right threshold depends on what mistakes cost, and must not be tuned on the test set.
:::

@@@ lesson
id: knn
title: k-nearest neighbours and distance
minutes: 16
summary: How KNN predicts from similar rows, what k does to the decision boundary, and why features must be on the same scale.
---
k-nearest neighbours is the easiest model to explain to anyone: **to predict for a new row, find the k most similar rows in the training data and let them vote** (or, for numbers, average them).

![A scatter of fruit by width and height. A new grey fruit sits among them, with a circle drawn around its 5 nearest neighbours: 3 apples and 2 oranges, so KNN predicts apple](figures/knn-neighbours.svg)

"Similar" means **close**, measured by **distance**. KNN uses the everyday straight-line distance (called Euclidean distance): for two fruits, it's √((width difference)² + (height difference)²), and the same with more features.

```python
import numpy as np

fruit_a = np.array([7.4, 7.0])    # width, height of a fruit
fruit_b = np.array([7.8, 7.7])
distance = np.sqrt(((fruit_a - fruit_b) ** 2).sum())
print(round(distance, 3))
```

KNN doesn't really "learn" anything during `fit`; it just stores the training rows. All the work happens at prediction time, which makes it slow on big data but great for small, well-understood problems.

### What k does

![Two maps of the same fruit data coloured by what KNN predicts in each region. With k=1 the regions are jagged, with islands around single fruits. With k=15 the boundaries are smooth](figures/knn-boundaries.svg)

- **Small k** (like 1): the prediction follows single points, including odd ones. Jagged boundaries, **overfitting**.
- **Large k**: smooth boundaries that ignore local detail. Too large and it **underfits** (at k = all rows, it always predicts the most common class).
- An odd k avoids ties between two classes.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm"]], fruit["fruit"], test_size=0.25, random_state=3, stratify=fruit["fruit"])

for k in [1, 5, 15, 51, 111]:
    knn = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
    print(f"k={k:>3}  train {knn.score(X_train, y_train):.3f}  test {knn.score(X_test, y_test):.3f}")
```

At k=111 almost all 112 training fruits get a vote on every prediction, so the answer barely depends on the fruit's own shape any more: training and test accuracy both drop to about two-thirds.

### Distance needs the same scale

Here's a trap. Width and height are in centimetres and vary by about 1 cm; weight is in grams and varies by about 36 g. In the distance formula, a 36 g difference counts as much as a 36 cm difference, so **weight swamps everything else**. Adding a useful feature can make KNN **worse**:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
print(fruit[["width_cm", "height_cm", "weight_g"]].std().round(1))

two, three, scaled = [], [], []
for seed in range(20):                      # 20 different splits, then average: fairer than one split
    X_train, X_test, y_train, y_test = train_test_split(
        fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.25, random_state=seed, stratify=fruit["fruit"])
    wh = ["width_cm", "height_cm"]
    two.append(KNeighborsClassifier(5).fit(X_train[wh], y_train).score(X_test[wh], y_test))
    three.append(KNeighborsClassifier(5).fit(X_train, y_train).score(X_test, y_test))
    scaled.append(make_pipeline(StandardScaler(), KNeighborsClassifier(5)).fit(X_train, y_train).score(X_test, y_test))

print("width + height:           ", round(np.mean(two), 3))
print("+ weight, unscaled:       ", round(np.mean(three), 3))
print("+ weight, StandardScaler: ", round(np.mean(scaled), 3))
```

Unscaled, the weight column drowns out the shape information and accuracy **falls**. After `StandardScaler` puts every feature on the same scale, the extra feature finally helps. Lesson 15 covers scaling in detail; for now, remember: **any model that uses distances needs scaled features.**

### KNN for numbers

`KNeighborsRegressor` predicts the **average** label of the k nearest rows:

```python
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

students = pd.read_csv("students.csv")
knn = KNeighborsRegressor(n_neighbors=5).fit(students[["hours_studied"]], students["math"])
print(knn.predict(pd.DataFrame({"hours_studied": [2, 6, 10]})).round(1))
```

:::exercise Choose k
Using the split below, try `n_neighbors` = 1, 3, 5, 7, 9, 11, 15 and 21 (with width and height only). Store the k with the **highest test accuracy** in `best_k`. If two values tie, keep the **smaller** k.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm"]], fruit["fruit"], test_size=0.3, random_state=11, stratify=fruit["fruit"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
f = pd.read_csv("fruit.csv")
a, b, c, d = train_test_split(f[["width_cm", "height_cm"]], f["fruit"], test_size=0.3, random_state=11, stratify=f["fruit"])
scores = [(KNeighborsClassifier(k).fit(a, c).score(b, d), -k) for k in [1, 3, 5, 7, 9, 11, 15, 21]]
same(int(need("best_k")), -max(scores)[1], "best_k")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm"]], fruit["fruit"], test_size=0.3, random_state=11, stratify=fruit["fruit"])

best_k, best_acc = None, -1
for k in [1, 3, 5, 7, 9, 11, 15, 21]:
    acc = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train).score(X_test, y_test)
    print(k, round(acc, 3))
    if acc > best_acc:            # strictly better, so ties keep the smaller k
        best_k, best_acc = k, acc
print("best k:", best_k)
```
hint: Loop over the k values in order and only replace your best when the accuracy is strictly higher.
:::

:::exercise Scale before measuring
Using all three fruit measurements and the split below, store the test accuracy of `KNeighborsClassifier(n_neighbors=7)` **without** scaling in `acc_raw`, and of `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7))` in `acc_scaled`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.3, random_state=11, stratify=fruit["fruit"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
f = pd.read_csv("fruit.csv")
a, b, c, d = train_test_split(f[["width_cm", "height_cm", "weight_g"]], f["fruit"], test_size=0.3, random_state=11, stratify=f["fruit"])
same(float(need("acc_raw")), KNeighborsClassifier(7).fit(a, c).score(b, d), "acc_raw")
same(float(need("acc_scaled")), make_pipeline(StandardScaler(), KNeighborsClassifier(7)).fit(a, c).score(b, d), "acc_scaled")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

fruit = pd.read_csv("fruit.csv")
X_train, X_test, y_train, y_test = train_test_split(
    fruit[["width_cm", "height_cm", "weight_g"]], fruit["fruit"], test_size=0.3, random_state=11, stratify=fruit["fruit"])

acc_raw = KNeighborsClassifier(n_neighbors=7).fit(X_train, y_train).score(X_test, y_test)
acc_scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7)).fit(X_train, y_train).score(X_test, y_test)
print(round(acc_raw, 3), round(acc_scaled, 3))
```
hint: The pipeline is used exactly like a model: `.fit(X_train, y_train)` then `.score(X_test, y_test)`.
:::

:::quiz
? How does KNN classify a new row?
+ It finds the k closest training rows and takes a vote
- It draws a straight line between classes
- It asks a series of yes/no questions
= KNN predicts from the most similar stored examples.
? With k=1, KNN tends to:
+ Overfit: jagged boundaries that follow single points
- Underfit
- Always predict the most common class
= One neighbour means every odd training point gets its own little region.
? Why does adding weight_g in grams hurt an unscaled KNN?
+ Its large numbers dominate the distance, drowning out width and height
- Weight is a useless feature
- KNN can't use more than two features
= Distances add up differences in each feature's own units, so big-unit features dominate. Scale first.
? What happens at prediction time with KNN on a huge dataset?
- It's instant
+ It's slow, because it compares the new row with every stored row
- It fails
= fit just stores the data; the searching happens when you predict.
:::

@@@ lesson
id: decision-trees
title: Decision trees
minutes: 17
summary: A model that asks a series of yes/no questions. Easy to read, no scaling needed, and a lesson in how depth controls overfitting.
---
A **decision tree** predicts by asking yes/no questions about the features, one after another, like a game of 20 questions:

![A small decision tree for churn. The first question at the top (the root) is "tenure 10.5 months or less?". Each branch then asks "more than 2.5 support calls?". The leaf for new customers with many calls predicts "leaves"; the other leaves predict "stays". Each box shows how many training customers reached it and what share of them left](figures/decision-tree.svg)

- The first question is the **root**. Each question is a **node** (or split); the end points that give the answer are **leaves**.
- To predict, start at the root and follow the answers down to a leaf. The leaf predicts the most common class among the training rows that ended up there.
- The **depth** is the number of questions on the longest path.

### How a tree picks its questions

At each node the tree tries **every feature and every cut-off** ("tenure ≤ 1?", "≤ 2?", … "support calls ≤ 3?"…) and keeps the question that best separates the classes: the one that makes the two groups it creates as **pure** as possible (mostly stayers on one side, mostly leavers on the other). The usual measure of mixed-ness is **Gini impurity**: 0 for a group that's all one class, 0.5 for a 50/50 mix of two classes. Then it repeats inside each group.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.25, random_state=0, stratify=churn["churned"])

tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
print(export_text(tree, feature_names=features))
print("test accuracy:", round(tree.score(X_test, y_test), 3))
```

`export_text` prints the tree as indented rules. The tree found, by itself, the pattern a retention manager would put in plain words: **new customers who keep calling support are the ones who leave.** (The right-hand branch ends in two "class: 0" leaves; the split still made those groups purer, it just didn't change the vote.)

### Trees in pictures

![Left: the fruit data with the regions a depth-3 tree predicts. The boundaries are all straight horizontal and vertical lines, making rectangles. Right: the same with an unlimited tree, which carves many tiny rectangles around single fruits](figures/tree-boundary.svg)

Trees cut the feature space into **rectangles**, because every question is about one feature at a time. This also means:

- **No scaling needed.** "Is weight ≤ 150 g?" works the same in grams or kilos.
- They capture **interactions** (an effect that depends on another feature, like support calls mattering mostly for new customers) and **non-linear** patterns without extra work.

### Depth controls overfitting

With no limit, a tree keeps splitting until every leaf is pure, which on noisy data means memorising:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.25, random_state=0, stratify=churn["churned"])

for depth in [1, 2, 3, 4, 6, 10, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    print(f"max_depth={str(depth):>4}  leaves {tree.get_n_leaves():>3}  train {tree.score(X_train, y_train):.3f}  test {tree.score(X_test, y_test):.3f}")
```

The unlimited tree (`None`) has 182 leaves and a perfect training score, but the worst test score. The shallow trees do best here. Besides `max_depth`, you can limit trees with `min_samples_leaf` (each leaf needs at least this many training rows) or `max_leaf_nodes`.

Single trees are easy to read but **unstable**: a few different training rows can produce a very different tree. The next lesson fixes that by combining many trees.

### Which features did it use?

`feature_importances_` says how much each feature reduced impurity across all the tree's splits (they add up to 1):

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.25, random_state=0, stratify=churn["churned"])

tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)
print(pd.Series(tree.feature_importances_, index=features).round(3).sort_values(ascending=False))
```

:::exercise A readable rule
Train a `DecisionTreeClassifier(max_depth=1, random_state=0)` called `stump` on the split below. A depth-1 tree asks a single question. Store the name of the feature it splits on in `first_feature`, and its test accuracy in `acc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

fruit = pd.read_csv("fruit.csv")
features = ["width_cm", "height_cm", "weight_g"]
X_train, X_test, y_train, y_test = train_test_split(
    fruit[features], fruit["fruit"], test_size=0.25, random_state=3, stratify=fruit["fruit"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
f = pd.read_csv("fruit.csv")
cols = ["width_cm", "height_cm", "weight_g"]
a, b, c, d = train_test_split(f[cols], f["fruit"], test_size=0.25, random_state=3, stratify=f["fruit"])
t = DecisionTreeClassifier(max_depth=1, random_state=0).fit(a, c)
need("stump", DecisionTreeClassifier)
same(str(need("first_feature")), cols[t.tree_.feature[0]], "first_feature")
same(float(need("acc")), t.score(b, d), "acc")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

fruit = pd.read_csv("fruit.csv")
features = ["width_cm", "height_cm", "weight_g"]
X_train, X_test, y_train, y_test = train_test_split(
    fruit[features], fruit["fruit"], test_size=0.25, random_state=3, stratify=fruit["fruit"])

stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X_train, y_train)
print(export_text(stump, feature_names=features))
first_feature = "width_cm"        # read it from the printed rule
acc = stump.score(X_test, y_test)
print(round(acc, 3))
```
hint: Print `export_text(stump, feature_names=features)`; the first line names the feature.
:::

:::exercise Best depth
For the churn split below, try `max_depth` from 1 to 8 (with `random_state=0`). Store the depth with the highest **test accuracy** in `best_depth` (keep the smaller depth if tied), and the training accuracy of the **unlimited** tree (`max_depth=None`) in `full_train_acc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.3, random_state=2, stratify=churn["churned"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
c = pd.read_csv("churn.csv")
cols = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
a, b, cc, d = train_test_split(c[cols], c["churned"], test_size=0.3, random_state=2, stratify=c["churned"])
scores = [(DecisionTreeClassifier(max_depth=k, random_state=0).fit(a, cc).score(b, d), -k) for k in range(1, 9)]
same(int(need("best_depth")), -max(scores)[1], "best_depth")
same(float(need("full_train_acc")), DecisionTreeClassifier(random_state=0).fit(a, cc).score(a, cc), "full_train_acc")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

churn = pd.read_csv("churn.csv")
features = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
X_train, X_test, y_train, y_test = train_test_split(
    churn[features], churn["churned"], test_size=0.3, random_state=2, stratify=churn["churned"])

best_depth, best_acc = None, -1
for depth in range(1, 9):
    acc = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train).score(X_test, y_test)
    if acc > best_acc:
        best_depth, best_acc = depth, acc
full = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
full_train_acc = full.score(X_train, y_train)
print(best_depth, round(best_acc, 3), full_train_acc)
```
hint: Same pattern as choosing k: loop, and replace the best only when strictly better.
:::

:::quiz
? Why don't decision trees need scaled features?
+ Each split compares one feature with a cut-off, so units don't matter
- They scale features automatically inside fit
- They only work with 0/1 features
= "weight <= 150 g" and "weight <= 0.15 kg" split the rows identically.
? A tree with no depth limit scores 1.00 on training data and 0.67 on test data. What's happening?
- Underfitting
+ Overfitting: it grew until it memorised the training rows
- Data leakage
= Unlimited trees keep splitting until every leaf is pure. Limit max_depth or min_samples_leaf.
? What does a leaf of a classification tree predict?
+ The most common class among the training rows that reached it
- The average of all labels
- A random class
= Each leaf votes with the training rows that ended up in it.
? What shape are the regions a decision tree draws on a 2-D chart?
- Circles
+ Rectangles, with horizontal and vertical edges
- Diagonal stripes
= Every question is about one feature, so every boundary is parallel to an axis.
:::

@@@ lesson
id: ensembles
title: Random forests and gradient boosting
minutes: 19
summary: Many trees beat one. Random forests average many different trees; gradient boosting builds trees that fix each other's mistakes. The go-to models for tables in 2026.
---
One deep tree overfits; one shallow tree is too simple. The fix is to combine **many** trees into an **ensemble**. Two ways to do it dominate machine learning on tables, and in 2026 they're still the first models most practitioners try for spreadsheet-style data:

![Left: a random forest. The same training data is resampled into many different bootstrap samples, each grows its own tree, and their predictions are averaged into one vote. Right: gradient boosting. Tree 1 makes predictions, tree 2 is trained on tree 1's mistakes, tree 3 on what's still wrong, and the final prediction adds them all up](figures/ensembles.svg)

| | Random forest | Gradient boosting |
|---|---|---|
| Trees are built | independently, in parallel | one after another |
| Each tree | is deep, trained on a random **bootstrap sample** of rows, with random features at each split | is small, and trained to fix the **errors** of the trees so far |
| Combined by | averaging (a vote) | adding up |
| Main idea | many different "opinions" cancel out each other's noise | lots of small corrections add up to a strong model |
| scikit-learn | `RandomForestClassifier` / `Regressor` | `HistGradientBoostingClassifier` / `Regressor` |

A **bootstrap sample** is a sample of rows drawn **with replacement** (some rows appear twice, some not at all), as in the bootstrap from Statistics. Training each tree on different rows (**bagging**) and letting it consider only a random subset of features at each split makes the trees **different from each other**. Their individual mistakes then point in different directions and largely cancel when you average them.

### Using every column

So far the churn models used only the number columns. The strongest clue, the contract type, is text. `pd.get_dummies` turns each text column into 0/1 columns, one per category. (Lesson 16 shows the proper way to do this inside a pipeline; `get_dummies` is fine for a quick experiment.) Trees in scikit-learn 1.8 also handle the missing ages by themselves.

```python
import pandas as pd

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
print(X.columns.tolist())
print(X.head(3))
```

### One tree versus a forest versus boosting

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

models = {
    "one deep tree": DecisionTreeClassifier(random_state=0),
    "one tree, depth 4": DecisionTreeClassifier(max_depth=4, random_state=0),
    "random forest": RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0),
    "gradient boosting": HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, random_state=0),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"{name:<18}  accuracy {model.score(X_test, y_test):.3f}   AUC {auc:.3f}")
```

The single deep tree is the worst; limiting its depth helps; both ensembles beat any single tree by a wide margin (AUC around 0.83 against 0.67 for the deep tree).

The main settings:

- **Random forest:** `n_estimators` (number of trees: more is better but slower; a few hundred is typical), `max_features` (features tried per split), `min_samples_leaf` or `max_depth` (how big each tree grows).
- **Gradient boosting:** `learning_rate` (how big each correction is: smaller is usually better but needs more trees), `max_iter` (number of trees), `max_depth` (each tree's size).

scikit-learn's `HistGradientBoostingClassifier` is the fast, modern implementation (it groups values into bins, which is the "Hist"). Outside scikit-learn, **XGBoost**, **LightGBM** and **CatBoost** are popular libraries built on the same idea, often used in competitions and production. They work the same way you've learned: create, fit, predict.

### Which features matter?

Random forests have `feature_importances_`, but it has a known bias: it favours columns with many different values (like age or charges) even when they barely help. **Permutation importance** is more honest. It shuffles one column of the **test** data at a time and measures how much the score drops. If shuffling a column hurts a lot, the model relied on it.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
forest = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0).fit(X_train, y_train)

result = permutation_importance(forest, X_test, y_test, scoring="roc_auc", n_repeats=10, random_state=0)
importance = pd.DataFrame({
    "built-in": forest.feature_importances_,
    "permutation": result.importances_mean,
}, index=X.columns).round(3)
print(importance.sort_values("permutation", ascending=False))
```

![Two bar charts of feature importance for the churn forest. Built-in importance puts tenure first and gives age and data use large bars. Permutation importance puts the month-to-month contract first, then tenure and support calls, and gives age almost nothing](figures/feature-importance.svg)

Permutation importance says the month-to-month contract, tenure and support calls drive the predictions, while age barely matters, even though the built-in measure gives age a sizeable share. When the two disagree, trust permutation importance on the test set.

:::exercise Grow a forest
Using the split below, train `RandomForestClassifier(n_estimators=200, random_state=1)` as `forest`. Store its test AUC in `forest_auc`, and the test AUC of a single `DecisionTreeClassifier(random_state=1)` in `tree_auc`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4, stratify=y)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
c = pd.read_csv("churn.csv")
X_ = pd.get_dummies(c.drop(columns=["customer_id", "churned"]), dtype=int)
a, b, cc, d = train_test_split(X_, c["churned"], test_size=0.3, random_state=4, stratify=c["churned"])
f = RandomForestClassifier(n_estimators=200, random_state=1).fit(a, cc)
t = DecisionTreeClassifier(random_state=1).fit(a, cc)
fr = need("forest", RandomForestClassifier)
same(fr.n_estimators, 200, "n_estimators")
same(float(need("forest_auc")), roc_auc_score(d, f.predict_proba(b)[:, 1]), "forest_auc", tol=1e-6)
same(float(need("tree_auc")), roc_auc_score(d, t.predict_proba(b)[:, 1]), "tree_auc", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

churn = pd.read_csv("churn.csv")
X = pd.get_dummies(churn.drop(columns=["customer_id", "churned"]), dtype=int)
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4, stratify=y)

forest = RandomForestClassifier(n_estimators=200, random_state=1).fit(X_train, y_train)
tree = DecisionTreeClassifier(random_state=1).fit(X_train, y_train)
forest_auc = roc_auc_score(y_test, forest.predict_proba(X_test)[:, 1])
tree_auc = roc_auc_score(y_test, tree.predict_proba(X_test)[:, 1])
print(round(tree_auc, 3), "->", round(forest_auc, 3))
```
hint: Both models use `.predict_proba(X_test)[:, 1]` for the AUC.
:::

:::exercise Boost the house prices
Ensembles predict numbers too. Using the housing split below, store the test R² of `HistGradientBoostingRegressor(random_state=0)` in `boost_r2` and of `LinearRegression()` in `linear_r2`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
h = pd.read_csv("housing.csv")
a, b, c, d = train_test_split(h[["area_sqm", "bedrooms", "age_years", "distance_km"]], h["price_k"], test_size=0.25, random_state=5)
same(float(need("boost_r2")), HistGradientBoostingRegressor(random_state=0).fit(a, c).score(b, d), "boost_r2", tol=1e-6)
same(float(need("linear_r2")), LinearRegression().fit(a, c).score(b, d), "linear_r2", tol=1e-6)
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor

housing = pd.read_csv("housing.csv")
X = housing[["area_sqm", "bedrooms", "age_years", "distance_km"]]
y = housing["price_k"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)

boost_r2 = HistGradientBoostingRegressor(random_state=0).fit(X_train, y_train).score(X_test, y_test)
linear_r2 = LinearRegression().fit(X_train, y_train).score(X_test, y_test)
print("boosting:", round(boost_r2, 3), " linear:", round(linear_r2, 3))
```
hint: `.score` on a regressor gives R². Fit each on the training data and score on the test data.
:::

:::quiz
? Why does averaging many trees beat one deep tree?
+ Each tree overfits in a different way, so their errors largely cancel out
- Each tree in the forest is more accurate than a single tree
- Forests use more features than trees can
= The individual trees are noisy; the average is stable.
? How are the trees in gradient boosting built?
- All at once, independently
+ One after another, each fixing the errors of the trees before it
- By deleting branches from one big tree
= Boosting adds small corrections in sequence.
? What does permutation importance measure?
+ How much the test score drops when one feature's values are shuffled
- How often a feature is used in splits
- The correlation of each feature with the label
= If shuffling a feature hurts the score, the model depended on it.
? For a new table-shaped (spreadsheet-like) problem in 2026, a strong first choice is:
- A deep neural network
+ A tree ensemble such as a random forest or gradient boosting, next to a simple baseline
- k-nearest neighbours with k=1
= Tree ensembles remain the go-to for tabular data; always compare with a baseline and a simple model.
:::
