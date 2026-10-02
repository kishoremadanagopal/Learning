# Machine learning cheat sheet

Every step, model and metric from the course on one page. The number in brackets is the lesson.

## The pattern [2–4]

```python
from sklearn.model_selection import train_test_split
X = df.drop(columns=["id", "target"])          # features: a table (2-D)          [1, 4]
y = df["target"]                               # label: one column                 [1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)   # stratify for classification [3]

model = SomeModel(hyperparameter=value)        # 1. create                         [2]
model.fit(X_train, y_train)                    # 2. fit (train)                    [2]
model.predict(X_test)                          # 3. predict                        [2]
model.predict_proba(X_test)[:, 1]              # probability of class 1            [2, 9]
model.score(X_test, y_test)                    # accuracy (classifier) or R² (regressor)  [3]
model.coef_, model.intercept_                  # learned things end with _         [2]
```

**Always compare with a baseline:** `DummyClassifier()` (most common class) or `DummyRegressor()` (training mean). [4]

## Which kind of problem? [1]

| The label is… | Problem | Example |
|---|---|---|
| a number | regression | price, temperature, minutes |
| a category (yes/no, A/B/C) | classification | spam, churn, fruit type |
| missing (no labels) | clustering / dimensionality reduction | customer segments, 2-D map |

## Which model? [2, 5, 8, 9, 12–14, 20–22]

| Model | Import | Type | Scale features? | Notes |
|---|---|---|---|---|
| Linear regression | `sklearn.linear_model.LinearRegression` | regression | no | simple, explainable baseline [5] |
| Ridge / Lasso | `sklearn.linear_model.Ridge`, `Lasso` | regression | **yes** | `alpha` = penalty; Lasso zeroes features [8] |
| Logistic regression | `sklearn.linear_model.LogisticRegression` | classification | **yes** | `C` = 1/penalty (small C = simpler) [9, 19] |
| k-nearest neighbours | `sklearn.neighbors.KNeighborsClassifier` / `Regressor` | both | **yes** | `n_neighbors`: small = overfit [12] |
| Decision tree | `sklearn.tree.DecisionTreeClassifier` / `Regressor` | both | no | `max_depth`, `min_samples_leaf` [13] |
| Random forest | `sklearn.ensemble.RandomForestClassifier` / `Regressor` | both | no | `n_estimators`, `min_samples_leaf` [14] |
| Gradient boosting | `sklearn.ensemble.HistGradientBoostingClassifier` / `Regressor` | both | no | `learning_rate`, `max_iter`, `max_depth`; handles NaN [14] |
| Naive Bayes (text) | `sklearn.naive_bayes.MultinomialNB` | classification | no | fast for word counts [22] |
| k-means | `sklearn.cluster.KMeans` | clustering | **yes** | `n_clusters`, `n_init`, `random_state` [20] |
| PCA | `sklearn.decomposition.PCA` | dimensionality reduction | **yes** | `n_components` (int or share like 0.95) [21] |

**For a new table problem:** baseline → logistic/linear regression → random forest or gradient boosting, compared with cross-validation.

## Regression metrics [6]

| Metric | Function | Read as |
|---|---|---|
| MAE | `mean_absolute_error(y_true, y_pred)` | typical error, in y's units |
| RMSE | `root_mean_squared_error(y_true, y_pred)` | like MAE, big misses count more |
| R² | `r2_score(y_true, y_pred)` or `model.score` | share of variation explained; 1 perfect, 0 = baseline, < 0 worse |

## Classification metrics [10, 11]

```
                    predicted 0       predicted 1
actually 0          TN                FP (false alarm)
actually 1          FN (missed)       TP (caught)
```

| Metric | Formula | Function | Focus on it when |
|---|---|---|---|
| accuracy | (TP + TN) / all | `accuracy_score` | classes are balanced |
| precision | TP / (TP + FP) | `precision_score` | false alarms are costly (spam filter) |
| recall | TP / (TP + FN) | `recall_score` | misses are costly (fraud, disease, churn) |
| F1 | 2PR / (P + R) | `f1_score` | you need one balanced number |
| AUC | area under ROC curve | `roc_auc_score(y_true, proba)` | comparing models' ranking, any threshold |

```python
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, RocCurveDisplay
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()                     # [10]
print(classification_report(y_test, pred))                                  # [10]
pred = (model.predict_proba(X_test)[:, 1] >= 0.3).astype(int)               # custom threshold [11]
LogisticRegression(class_weight="balanced")                                 # rare classes [11]
```

## Preparing data [15–17]

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder, OrdinalEncoder, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline

scaler.fit(X_train); scaler.transform(X_test)          # fit on TRAIN only            [15]
OneHotEncoder(handle_unknown="ignore")                 # unordered categories         [16]
OrdinalEncoder(categories=[["small", "medium", "large"]])   # ordered categories     [16]
SimpleImputer(strategy="median")                       # "mean", "most_frequent", "constant"  [16]

prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
])                                                                                    # [16]
pipe = Pipeline([("prep", prep), ("model", LogisticRegression())])                    # [17]
pipe.fit(X_train, y_train); pipe.predict_proba(raw_new_rows)                          # [17]
pipe.named_steps["model"], pipe[-1]                     # reach a step                [17]
pipe.named_steps["prep"].get_feature_names_out()        # column names after prep     [17]
```

**Data leakage checklist** [17]: every learned step inside the pipeline · split before exploring · no feature that's only known after the outcome · results too good to be true → hunt for the leak.

## Validating and tuning [18, 19]

```python
from sklearn.model_selection import cross_val_score, cross_validate, cross_val_predict, KFold, GridSearchCV, RandomizedSearchCV, validation_curve

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="roc_auc")    # mean ± std  [18]
cross_validate(model, X, y, cv=5, scoring=["accuracy", "roc_auc"], return_train_score=True)  [18]
KFold(5, shuffle=True, random_state=0)                  # shuffled folds for regression  [18]
search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]}, cv=5, scoring="roc_auc")     [19]
search.fit(X_train, y_train); search.best_params_; search.best_score_; search.predict(X_test)  [19]
RandomizedSearchCV(model, space, n_iter=20, cv=5, random_state=0)            # big spaces   [19]
proba = cross_val_predict(pipe, X_train, y_train, cv=5, method="predict_proba")[:, 1]   # choose thresholds [24]
```

Scoring names: `"accuracy"`, `"f1"`, `"precision"`, `"recall"`, `"roc_auc"`, `"r2"`, `"neg_mean_absolute_error"`, `"neg_root_mean_squared_error"` (neg = negated: flip the sign).

| Data | Used for |
|---|---|
| training folds | fitting |
| validation folds (CV) | comparing models, tuning, picking a threshold |
| test set | one final, honest score |

## Overfitting at a glance [3, 7]

| Training score | Test / CV score | Diagnosis | Try |
|---|---|---|---|
| low | low | underfitting | more complex model, better features |
| high | much lower | overfitting | simpler model, regularisation, more data, limit depth |
| good | close to training | good fit | ship it (after the final test) |

Complexity knobs: polynomial `degree`, `n_neighbors` (small = complex), `max_depth`, `alpha` / `C`, number of features.

## Unsupervised [20, 21]

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
labels = make_pipeline(StandardScaler(), KMeans(n_clusters=5, n_init=10, random_state=0)).fit_predict(X)  # [20]
km.inertia_                                   # lower = tighter; look for the elbow        [20]
silhouette_score(X_scaled, labels)            # -1 to 1, higher is better                  [20]
df.groupby(labels)[cols].mean()               # describe each cluster                      [20]

from sklearn.decomposition import PCA
pca = make_pipeline(StandardScaler(), PCA(n_components=2)).fit(X)                          # [21]
pca[-1].explained_variance_ratio_             # share of variation per component           [21]
pca[-1].components_                           # each component's feature weights           [21]
```

## Text [22]

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression())
model.fit(df["text"], df["label"])            # one column of strings, single brackets
model.predict(["a new message"])              # a list of texts
```

## Explaining, saving, monitoring [14, 23]

```python
from sklearn.inspection import permutation_importance
r = permutation_importance(model, X_test, y_test, scoring="roc_auc", n_repeats=10, random_state=0)  # [14]
pd.Series(r.importances_mean, index=X_test.columns).sort_values()

import joblib
joblib.dump(pipe, "model.joblib"); pipe = joblib.load("model.joblib")    # same sklearn version; trusted files only  [23]
```

Before going live [23]: compare live data with training data (drift) · track predictions and accuracy · check metrics per group, with counts · write a model card (intended use, data, performance, limits, version) · plan retraining.

## Common errors [2, 16]

| Error message contains | Fix |
|---|---|
| `Expected a 2-dimensional container` / `Expected 2D array` | X must be a table: `df[["col"]]` |
| `could not convert string to float` | encode text columns (OneHotEncoder) |
| `Input X contains NaN` | impute (SimpleImputer) or use HistGradientBoosting |
| `is not fitted yet` | call `.fit(...)` first |
| `X has N features, but … is expecting M features` | predict with the same columns as training |
| `ConvergenceWarning` | scale features, or raise `max_iter` |
