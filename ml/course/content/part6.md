@@@ part
id: 6
title: Machine Learning in Practice
level: Advanced
blurb: Classify text, take a model from notebook to real use (saving, monitoring, fairness), see where classic ML sits next to LLMs in 2026, and finish with an end-to-end project.

@@@ lesson
id: text-classification
title: Classifying text
minutes: 18
summary: Turn messages into numbers with bag-of-words and TF-IDF, build a spam filter, see which words drive it, and where embeddings and LLMs fit in.
---
Models need numbers, but much of the world's data is text: emails, reviews, support tickets. The classic way to turn text into numbers is the **bag of words**: count how often each word appears, and ignore the order.

![Three short messages become a table. Each column is a word from the vocabulary (call, free, lunch, now, prize, tomorrow, win, you…) and each row counts how many times that word appears in the message. Most cells are 0](figures/bag-of-words.svg)

### CountVectorizer

```python
from sklearn.feature_extraction.text import CountVectorizer

messages = [
    "Win a free prize now",
    "Are you free for lunch tomorrow?",
    "Call now to claim your free prize",
]
vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(messages)

print(vectorizer.get_feature_names_out())
print(counts.toarray())
```

`fit` learns the **vocabulary** (every distinct word in the training texts, lower-cased, punctuation removed); `transform` counts them. The result is a **document-term matrix**: one row per message, one column per word. It's **sparse** (mostly zeros), so scikit-learn stores only the non-zero counts; `.toarray()` shows it in full. Words that weren't in the training vocabulary are simply ignored at prediction time.

Useful options:

- `stop_words="english"` drops very common words (the, a, to…).
- `ngram_range=(1, 2)` also counts **pairs** of neighbouring words ("free prize", "call now"), which keeps a little word order.
- `min_df=2` ignores words that appear in fewer than 2 messages.

### TF-IDF

Plain counts give common words a lot of weight. **TF-IDF** (term frequency × inverse document frequency) scales each count down if the word appears in many messages, so distinctive words stand out. `TfidfVectorizer` works exactly like `CountVectorizer`; it's usually the better default.

### A spam filter

`messages.csv` has 400 text messages labelled `spam` or `ham` (normal). The vectorizer goes in a pipeline like any other transformer, and the pipeline takes raw text:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

data = pd.read_csv("messages.csv")
print(data["label"].value_counts())
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.25, random_state=0, stratify=data["label"])

for name, model in [("Naive Bayes + counts", make_pipeline(CountVectorizer(), MultinomialNB())),
                    ("LogisticRegression + TF-IDF", make_pipeline(TfidfVectorizer(), LogisticRegression()))]:
    model.fit(X_train, y_train)
    print(f"{name}: accuracy {model.score(X_test, y_test):.3f}")
    print(confusion_matrix(y_test, model.predict(X_test), labels=["ham", "spam"]))
```

Note that `X` here is a **single column of text** (`data["text"]`, one pair of brackets): text vectorizers expect a list of strings, not a table.

**Naive Bayes** is a classic, very fast text model: it learns how likely each word is in spam and in ham, and combines those probabilities (it "naively" treats words as independent, which works surprisingly well). Both models do extremely well here, because spam messages use quite different words from normal ones.

### Which words give spam away?

For a linear model on TF-IDF, each word gets a coefficient: positive pushes towards spam, negative towards ham.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

data = pd.read_csv("messages.csv")
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.25, random_state=0, stratify=data["label"])
model = make_pipeline(TfidfVectorizer(), LogisticRegression()).fit(X_train, y_train)

words = pd.Series(model[-1].coef_[0], index=model[0].get_feature_names_out()).sort_values()
print("most 'ham' words: ", words.head(6).index.tolist())
print("most 'spam' words:", words.tail(6).index.tolist())

new = ["Congratulations! You won a free cruise, call now",
       "Are you free for lunch tomorrow?",
       "Your parcel fee is unpaid, pay at www.post-fee.biz"]
for text, p in zip(new, model.predict_proba(new)[:, 1]):
    print(f"{p:.2f}  {text}")
```

("spam" comes after "ham" alphabetically, so column 1 of `predict_proba` is the spam probability.) The first new message is only borderline (about 0.5), even though a person would call it spam at once. Words like "free" and "won" also appear in normal messages here ("Are you free…", "We won the quiz…"), and "cruise" and "congratulations" never appeared in a training spam message, so the model can't use them. A bag of words only knows the words it has seen.

### Beyond bag-of-words: embeddings and LLMs (2026)

Bag-of-words ignores meaning: "cheap" and "inexpensive" are unrelated columns, and "not good" looks a lot like "good". Modern systems usually go further:

| Approach | How it works | Strengths | Costs |
|---|---|---|---|
| **Bag-of-words / TF-IDF + linear model** | count words, as in this lesson | fast, cheap, explainable, runs anywhere | misses meaning and word order |
| **Embeddings + classic model** | a pre-trained language model turns each text into a vector of numbers that captures meaning; then train logistic regression on those vectors | understands synonyms and phrasing; needs fewer labels | needs an embedding model (a library or an API) |
| **Ask an LLM** | describe the categories in a prompt and let a large language model label each text, with no training | no labelled data needed to start; handles new categories easily | slower and costlier per message; must be checked carefully |

Whichever you use, the rules from this course stay the same: hold out labelled test examples, measure precision and recall, watch for leakage, and compare against a simple baseline. Evaluating LLM systems this way is called running **evals**, and it's a core skill for AI engineers.

:::exercise Count the words
Use a `CountVectorizer` called `vectorizer` on the four `reviews` below. Store the document-term matrix as a normal (dense) array in `matrix`, and the number of distinct words in the vocabulary in `n_words`.
```python starter
from sklearn.feature_extraction.text import CountVectorizer

reviews = [
    "Great phone, great battery",
    "Battery died after a week",
    "Great value for money",
    "The screen cracked after a day",
]

```
```python check
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
r = ["Great phone, great battery", "Battery died after a week", "Great value for money", "The screen cracked after a day"]
v = CountVectorizer().fit(r)
need("vectorizer", CountVectorizer)
same(int(need("n_words")), len(v.get_feature_names_out()), "n_words")
same(np.asarray(need("matrix")), v.transform(r).toarray(), "matrix")
```
```python solution
from sklearn.feature_extraction.text import CountVectorizer

reviews = [
    "Great phone, great battery",
    "Battery died after a week",
    "Great value for money",
    "The screen cracked after a day",
]
vectorizer = CountVectorizer()
matrix = vectorizer.fit_transform(reviews).toarray()
n_words = len(vectorizer.get_feature_names_out())
print(vectorizer.get_feature_names_out())
print(matrix)
print(n_words)
```
hint: `fit_transform` returns a sparse matrix; `.toarray()` turns it into a normal array. Notice that the single letter "a" isn't in the vocabulary: by default, words need at least two characters.
:::

:::exercise Your own spam filter
Build `model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB())`, fit it on the training messages, and store its test accuracy in `acc`. Then store its prediction (`"spam"` or `"ham"`) for the message `"Claim your FREE gift card now, text WIN to 80082"` in `verdict`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

data = pd.read_csv("messages.csv")
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.3, random_state=2, stratify=data["label"])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
m = pd.read_csv("messages.csv")
a, b, c, d = train_test_split(m["text"], m["label"], test_size=0.3, random_state=2, stratify=m["label"])
ref = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB()).fit(a, c)
same(float(need("acc")), ref.score(b, d), "acc")
same(str(need("verdict")), str(ref.predict(["Claim your FREE gift card now, text WIN to 80082"])[0]), "verdict")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

data = pd.read_csv("messages.csv")
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.3, random_state=2, stratify=data["label"])

model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), MultinomialNB()).fit(X_train, y_train)
acc = model.score(X_test, y_test)
verdict = model.predict(["Claim your FREE gift card now, text WIN to 80082"])[0]
print(round(acc, 3), verdict)
```
hint: predict wants a list of texts, even for one message: `model.predict(["..."])[0]`.
:::

:::quiz
? What does a bag-of-words representation keep?
+ How many times each word appears in each text
- The order of the words
- The meaning of each sentence
= It counts words and throws the order away.
? Why does TF-IDF often beat raw counts?
+ It down-weights words that appear in many texts, so distinctive words count more
- It translates the text
- It keeps word order
= Common words carry little information about the class.
? A word that never appeared in training shows up in a new message. A CountVectorizer pipeline will:
+ Ignore it
- Crash
- Add a new column automatically
= The vocabulary is fixed at fit time.
? You use an LLM to label support tickets. How should you check it?
+ Compare its labels with human labels on held-out tickets, using precision and recall
- Trust it because LLMs are accurate
- Measure how fast it answers
= Same rules as any model: test on labelled examples it wasn't tuned on. That's an eval.
:::

@@@ lesson
id: model-to-product
title: From model to product, responsibly
minutes: 18
summary: Save and load a trained pipeline, keep watch for drift once it's live, check fairness across groups, write a model card, and decide when classic ML or an LLM is the right tool.
---
A model in a notebook helps nobody. To be useful it has to be **saved**, **served** (made available to other software), **monitored**, and **trusted**. This lesson walks through each step.

![The model lifecycle as a loop: data, then train and evaluate, then save the pipeline, then serve predictions, then monitor (drift, fairness, accuracy), then back to data to retrain](figures/lifecycle.svg)

### Saving and loading a pipeline

Save the **whole pipeline**, not just the model, so the preparation steps travel with it. `joblib` comes with scikit-learn:

```python
import joblib
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

joblib.dump(pipe, "churn_model.joblib")            # save to a file
loaded = joblib.load("churn_model.joblib")         # later, maybe on another computer

print(loaded.predict_proba(X.head(3))[:, 1].round(3))
print(pipe.predict_proba(X.head(3))[:, 1].round(3))
```

Two warnings:

- **Load with the same scikit-learn version** you saved with (here 1.8). Record the version next to the file.
- **Never load a model file from someone you don't trust.** joblib and pickle files can run code when loaded. The `skops` library offers a safer format for sharing.

### Serving predictions

In production, a model usually sits behind a small function or web service (for example, built with **FastAPI**): other software sends a customer's details and gets a probability back. The heart of it is just this:

```python
import joblib
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
joblib.dump(Pipeline([("prep", prep), ("model", LogisticRegression())]).fit(X, churn["churned"]), "churn_model.joblib")

MODEL = joblib.load("churn_model.joblib")           # load once, when the service starts

def churn_risk(customer: dict) -> float:
    """Return the probability that one customer leaves."""
    row = pd.DataFrame([customer])
    return float(MODEL.predict_proba(row)[0, 1])

print(round(churn_risk({"contract": "month-to-month", "plan": "basic", "tenure_months": 1,
                        "monthly_charge": 33.0, "support_calls": 5, "age": None, "data_gb": 28.0}), 3))
```

### Monitoring: models get stale

A model is trained on the past. When the world changes, it quietly gets worse:

- **Data drift**: the inputs change. A marketing campaign brings in many brand-new customers, so tenure looks very different from the training data.
- **Concept drift**: the relationship changes. A competitor's cheap offer makes even happy customers leave, so the old patterns no longer predict churn.

Simple checks catch a lot. Compare live data with the training data, and track predictions over time:

```python
import numpy as np
import pandas as pd

churn = pd.read_csv("churn.csv")
rng = np.random.default_rng(3)
# a made-up "next month": a campaign brought in many new customers, so tenure is much lower
next_month = churn.sample(300, random_state=1).copy()
next_month["tenure_months"] = rng.integers(1, 7, 300)

compare = pd.DataFrame({
    "training mean": churn[["tenure_months", "monthly_charge", "support_calls"]].mean(),
    "next month mean": next_month[["tenure_months", "monthly_charge", "support_calls"]].mean(),
}).round(1)
compare["change %"] = ((compare["next month mean"] / compare["training mean"] - 1) * 100).round(0)
print(compare)
```

Tenure has dropped by about 90%: a red flag. The model has seen relatively few customers like these, and its predictions for them deserve less trust. Teams set alerts for shifts like this, track accuracy once the real outcomes arrive, and **retrain** on fresh data regularly.

### Fairness: check every group

A model can work well on average and badly for some group of people. Before using a model on people, **compute your metrics per group**:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())]).fit(X_train, y_train)
flagged = (pipe.predict_proba(X_test)[:, 1] >= 0.3).astype(int)

report = pd.DataFrame({"age group": pd.cut(X_test["age"], [0, 35, 55, 100], labels=["18-35", "36-55", "56+"]),
                       "left": y_test, "flagged": flagged}).dropna()
for group, rows in report.groupby("age group", observed=True):
    print(f"{group:>6}: customers {len(rows):>3}  churn rate {rows['left'].mean():.2f}  "
          f"flagged {rows['flagged'].mean():.2f}  recall {recall_score(rows['left'], rows['flagged']):.2f}")
```

Here the model catches leavers in every age group, though less well among older customers. Things to keep in mind:

- **Small groups give shaky numbers.** A group with 13 leavers can swing a lot by chance; report the counts alongside the rates.
- **Removing a sensitive column doesn't remove bias.** Other columns (postcode, job, shopping habits) can act as **proxies** for age, gender or ethnicity.
- **The stakes decide how careful to be.** Offering a discount is low-stakes; decisions about loans, jobs, housing, healthcare or policing can harm people and are regulated in many places (for example under the EU AI Act). They need careful testing, human oversight and a way for people to challenge the result.

### Document it: a model card

A **model card** is a short document that travels with a model. It answers:

| Section | Example for the churn model |
|---|---|
| Intended use | Rank current customers for retention calls; not for pricing or credit decisions |
| Training data | 1,000 customers, one snapshot; age missing for 6% |
| Performance | Test AUC 0.84; at threshold 0.3: recall about 0.75, precision about 0.53 |
| Groups checked | Age bands, plan, contract (with counts) |
| Limits | Not trained on customers who joined via campaigns; retrain monthly |
| Version | scikit-learn 1.8, trained on (date) |

### Classic ML or an LLM?

In 2026 many teams can also solve a problem by prompting a large language model. A rough guide:

| Use classic ML (this course) when… | Consider an LLM when… |
|---|---|
| the data is a table of numbers and categories | the input is free text, images or conversation |
| you have labelled examples (hundreds or more) | you have few or no labels yet |
| you need fast, cheap predictions at scale | volume is modest and flexibility matters |
| decisions must be explained and audited | the task changes often (new categories, new rules) |

They're not rivals: LLM features (like text embeddings) often feed classic models, and every LLM system needs the same discipline you've learned: held-out test data, the right metrics, baselines, leakage checks and monitoring.

:::exercise Save, load, compare
Fit the pipeline below on all the housing data, save it to `"house_model.joblib"` with `joblib.dump`, load it back into `loaded`, and set `same_predictions` to `True` if `loaded.predict(X)` equals `pipe.predict(X)` for every row (use `np.allclose`).
```python starter
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

housing = pd.read_csv("housing.csv")
X = housing.drop(columns=["home_id", "price_k"])
y = housing["price_k"]
prep = ColumnTransformer([
    ("num", StandardScaler(), ["area_sqm", "bedrooms", "age_years", "distance_km"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"]),
])
pipe = Pipeline([("prep", prep), ("model", Ridge())]).fit(X, y)

```
```python check
import os
import numpy as np
from sklearn.pipeline import Pipeline
if not os.path.exists("house_model.joblib"):
    raise AssertionError("Save the pipeline with joblib.dump(pipe, \"house_model.joblib\").")
l = need("loaded", Pipeline)
same(need("same_predictions"), True, "same_predictions")
uses("joblib.load")
```
```python solution
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

housing = pd.read_csv("housing.csv")
X = housing.drop(columns=["home_id", "price_k"])
y = housing["price_k"]
prep = ColumnTransformer([
    ("num", StandardScaler(), ["area_sqm", "bedrooms", "age_years", "distance_km"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["neighborhood"]),
])
pipe = Pipeline([("prep", prep), ("model", Ridge())]).fit(X, y)

joblib.dump(pipe, "house_model.joblib")
loaded = joblib.load("house_model.joblib")
same_predictions = bool(np.allclose(loaded.predict(X), pipe.predict(X)))
print(same_predictions)
```
hint: `joblib.dump(pipe, "house_model.joblib")`, then `loaded = joblib.load("house_model.joblib")`.
:::

:::exercise Recall by contract
Using the fitted pipeline and the 0.3-threshold predictions below, compute recall separately for each contract type in the test set. Store a dictionary `recall_by_contract` mapping each contract type to its recall, and a dictionary `leavers_by_contract` mapping each type to how many test customers of that type really left.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())]).fit(X_train, y_train)
flagged = (pipe.predict_proba(X_test)[:, 1] >= 0.3).astype(int)

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
c = pd.read_csv("churn.csv")
X_ = c.drop(columns=["customer_id", "churned"])
a, b, cc, d = train_test_split(X_, c["churned"], test_size=0.25, random_state=0, stratify=c["churned"])
pr = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"])])
f = (Pipeline([("prep", pr), ("model", LogisticRegression())]).fit(a, cc).predict_proba(b)[:, 1] >= 0.3).astype(int)
df = pd.DataFrame({"g": b["contract"].to_numpy(), "y": d.to_numpy(), "p": f})
exp_r = {g: recall_score(r["y"], r["p"], zero_division=0) for g, r in df.groupby("g")}
exp_n = {g: int(r["y"].sum()) for g, r in df.groupby("g")}
same({str(k): float(v) for k, v in need("recall_by_contract", dict).items()}, exp_r, "recall_by_contract")
same({str(k): int(v) for k, v in need("leavers_by_contract", dict).items()}, exp_n, "leavers_by_contract")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())]).fit(X_train, y_train)
flagged = (pipe.predict_proba(X_test)[:, 1] >= 0.3).astype(int)

report = pd.DataFrame({"contract": X_test["contract"], "left": y_test, "flagged": flagged})
recall_by_contract, leavers_by_contract = {}, {}
for contract, rows in report.groupby("contract"):
    recall_by_contract[contract] = recall_score(rows["left"], rows["flagged"], zero_division=0)
    leavers_by_contract[contract] = int(rows["left"].sum())
print(recall_by_contract)
print(leavers_by_contract)
```
hint: Put contract, the real outcome and the flags in one DataFrame, then loop over `groupby("contract")`. `zero_division=0` avoids a warning for a group with no leavers flagged. Look at the counts before trusting any group's recall.
:::

:::quiz
? Why save the whole pipeline instead of just the model?
+ So the exact same preparation (imputing, scaling, encoding) is applied to new data
- Pipelines are smaller files
- Models can't be saved on their own
= The model only understands data prepared the way it was during training.
? A model's accuracy slowly drops months after launch, though nothing in the code changed. The likely cause is:
+ Drift: the data or the relationship it learned has changed
- A bug in scikit-learn
- Overfitting during training
= The world moves on; monitor and retrain.
? You remove the "gender" column from a hiring model. Is it now fair?
+ Not necessarily: other columns can act as proxies, so you must still measure outcomes per group
- Yes, completely
- Only if accuracy stays the same
= Bias can come in through correlated features. Measure, don't assume.
? Why must you never load a .joblib file from an unknown source?
+ Loading it can run arbitrary code on your computer
- It might be the wrong size
- It will overwrite your data
= joblib and pickle files execute code when loaded.
:::

@@@ lesson
id: final-project
title: "Final project: a churn model, start to finish"
minutes: 25
summary: Put the whole course together: frame the question, split, baseline, pipeline, compare with cross-validation, tune, choose a threshold, test once, explain and report.
---
A phone company wants to call customers who are likely to leave and offer them a deal. The retention team can make a few hundred calls a month and wants to **reach at least 70% of the customers who would leave**. Your job: build the model that picks whom to call, and report honestly how well it will work.

![The project's steps in order: 1. question and success measure, 2. split off a test set, 3. baseline, 4. pipeline, 5. compare models with cross-validation, 6. tune the winner, 7. choose the threshold with cross-validated predictions, 8. test once, 9. explain and report](figures/project-steps.svg)

### 1–2. Frame it and split it

- **Prediction:** the probability that a customer leaves (`churned = 1`).
- **Success measure:** recall of at least 0.7 (catch 70% of leavers), with precision as high as possible (fewer wasted calls). AUC to compare models.
- **Split first**, stratified, and put the test set away until the end.

```python
import pandas as pd
from sklearn.model_selection import train_test_split

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

print("training rows:", len(X_train), " test rows:", len(X_test))
print("churn rate in training:", y_train.mean().round(3))
print(X_train.isna().sum()[X_train.isna().sum() > 0])
```

### 3–5. Baseline, pipeline, compare

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
for name, model in [("baseline", DummyClassifier()),
                    ("logistic regression", LogisticRegression(max_iter=1000)),
                    ("gradient boosting", HistGradientBoostingClassifier(learning_rate=0.05, max_depth=3, random_state=0))]:
    scores = cross_val_score(Pipeline([("prep", prep), ("model", model)]), X_train, y_train, cv=5, scoring="roc_auc")
    print(f"{name:<20} CV AUC {scores.mean():.3f} ± {scores.std():.3f}")
```

Both real models beat the baseline by a mile and tie with each other. Logistic regression is simpler, faster and easier to explain to the retention team, so it goes forward.

### 6. Tune it

```python
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])

search = GridSearchCV(pipe, {"model__C": [0.01, 0.03, 0.1, 0.3, 1, 3]}, cv=5, scoring="roc_auc")
search.fit(X_train, y_train)
print(search.best_params_, "CV AUC", round(search.best_score_, 3))
```

The best C gives a CV AUC of about 0.815. The differences between C values from 0.1 upward are tiny (Lesson 19), so the choice hardly matters, which is reassuring.

### 7. Choose the threshold, without the test set

You need probabilities for rows the model **didn't train on**, but you can't use the test set yet. `cross_val_predict` gives exactly that: each training row's prediction comes from the CV round in which it was in the validation fold.

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))])

cv_proba = cross_val_predict(pipe, X_train, y_train, cv=5, method="predict_proba")[:, 1]
for t in [0.5, 0.4, 0.35, 0.3, 0.25]:
    pred = (cv_proba >= t).astype(int)
    print(f"threshold {t:<4}  recall {recall_score(y_train, pred):.2f}  precision {precision_score(y_train, pred):.2f}  calls {pred.sum()} of {len(pred)}")
```

A threshold of **0.3** is the highest one that reaches the 70% recall target, with about half of the calls going to real leavers.

### 8–9. Test once, explain, report

Now, and only now, the test set:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.inspection import permutation_importance

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
final = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))]).fit(X_train, y_train)

proba = final.predict_proba(X_test)[:, 1]
calls = (proba >= 0.3).astype(int)
print("test AUC:      ", round(roc_auc_score(y_test, proba), 3))
print("test recall:   ", round(recall_score(y_test, calls), 3))
print("test precision:", round(precision_score(y_test, calls), 3))
print("calls:", calls.sum(), "of", len(calls), "customers")

imp = permutation_importance(final, X_test, y_test, scoring="roc_auc", n_repeats=10, random_state=0)
print(pd.Series(imp.importances_mean, index=X_test.columns).round(3).sort_values(ascending=False))
```

Permutation importance works on the **raw** columns here, because the whole pipeline is shuffled-and-scored as one model: contract type, tenure and support calls are what the model relies on.

The report for the retention team, in plain words:

> **Churn model, version 1.** Calling everyone the model scores at 30% or higher reaches about 3 in 4 customers who would leave (test recall 0.75), by calling about 2 in 5 customers. About half of those calls go to customers who really were about to leave (precision 0.53). The strongest warning signs are a month-to-month contract, a short time as a customer, and repeated support calls. Tested on 250 customers the model never saw. To be retrained monthly and checked for drift; not for pricing or credit decisions.

That's a real deliverable: a number people can plan with, an honest measure of it, the reasons behind it, and its limits.

### Where to go next

- **Practice on new data:** try the same steps on other datasets (Kaggle and the UCI repository have hundreds).
- **Go deeper on models:** XGBoost and LightGBM for tables; **PyTorch** for neural networks (images, text, audio).
- **Into AI engineering:** embeddings, retrieval-augmented generation (RAG), and evaluating LLM systems all build on what you now know: features, splits, metrics, leakage and monitoring.

:::exercise Pick the threshold
Using the cross-validated probabilities below, find the **highest** threshold from `[0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15]` whose recall on the training labels is **at least 0.75**. Store it in `threshold`, and the precision at that threshold in `precision_at_t`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))])
cv_proba = cross_val_predict(pipe, X_train, y_train, cv=5, method="predict_proba")[:, 1]

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
c = pd.read_csv("churn.csv")
X_ = c.drop(columns=["customer_id", "churned"])
a, b, cc, d = train_test_split(X_, c["churned"], test_size=0.25, random_state=0, stratify=c["churned"])
pr = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"])])
p = cross_val_predict(Pipeline([("prep", pr), ("model", LogisticRegression(C=3, max_iter=1000))]), a, cc, cv=5, method="predict_proba")[:, 1]
exp_t = next(t for t in [0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15] if recall_score(cc, (p >= t).astype(int)) >= 0.75)
same(float(need("threshold")), exp_t, "threshold")
same(float(need("precision_at_t")), precision_score(cc, (p >= exp_t).astype(int)), "precision_at_t")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))])
cv_proba = cross_val_predict(pipe, X_train, y_train, cv=5, method="predict_proba")[:, 1]

for t in [0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15]:     # from high to low
    pred = (cv_proba >= t).astype(int)
    if recall_score(y_train, pred) >= 0.75:
        threshold = t
        precision_at_t = precision_score(y_train, pred)
        break
print(threshold, round(precision_at_t, 3))
```
hint: Loop from the highest threshold down and `break` at the first one whose recall reaches 0.75.
:::

:::exercise The final report numbers
Fit the final pipeline (`C=3`) on the training data. On the **test** set, using a threshold of **0.25**, store the recall in `test_recall`, the precision in `test_precision`, and the number of customers to call in `n_calls`.
```python starter
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
final = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))])

```
```python check
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
c = pd.read_csv("churn.csv")
X_ = c.drop(columns=["customer_id", "churned"])
a, b, cc, d = train_test_split(X_, c["churned"], test_size=0.25, random_state=0, stratify=c["churned"])
pr = ColumnTransformer([("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"])])
calls_ = (Pipeline([("prep", pr), ("model", LogisticRegression(C=3, max_iter=1000))]).fit(a, cc).predict_proba(b)[:, 1] >= 0.25).astype(int)
same(float(need("test_recall")), recall_score(d, calls_), "test_recall")
same(float(need("test_precision")), precision_score(d, calls_), "test_precision")
same(int(need("n_calls")), int(calls_.sum()), "n_calls")
```
```python solution
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score

churn = pd.read_csv("churn.csv")
X = churn.drop(columns=["customer_id", "churned"])
y = churn["churned"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
numeric = ["tenure_months", "monthly_charge", "support_calls", "age", "data_gb"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["contract", "plan"]),
])
final = Pipeline([("prep", prep), ("model", LogisticRegression(C=3, max_iter=1000))])

final.fit(X_train, y_train)
calls = (final.predict_proba(X_test)[:, 1] >= 0.25).astype(int)
test_recall = recall_score(y_test, calls)
test_precision = precision_score(y_test, calls)
n_calls = int(calls.sum())
print(round(test_recall, 3), round(test_precision, 3), n_calls)
```
hint: Fit on the training data, take `predict_proba(X_test)[:, 1]`, apply the threshold, then compute the metrics against `y_test`.
:::

:::quiz
? In the project, why choose the threshold with cross_val_predict on the training set?
+ So the test set stays unseen until the final, honest check
- Because the test set is too small
- cross_val_predict is faster
= Any choice made with the test set makes the final test score optimistic.
? Two models tie in cross-validation. Which should usually go forward?
+ The simpler, faster, easier-to-explain one
- The more complex one
- Both, averaged
= Equal performance plus simplicity wins.
? What belongs in the final report?
+ The honest test numbers in plain words, what drives the predictions, and the model's limits
- Only the AUC
- The training accuracy
= People need numbers they can plan with, the reasons, and the boundaries.
? The retention team later asks for 90% recall. What changes?
+ Lower the threshold (chosen again on validation data); expect more calls and lower precision
- Retrain with a bigger test set
- Nothing can be done
= Recall and precision trade off through the threshold.
:::
