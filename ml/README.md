# Machine Learning with scikit-learn

A hands-on machine-learning course for complete beginners: 24 lessons that take you from "what is a model?" to regression, classification, decision trees, random forests, gradient boosting, pipelines, cross-validation, tuning, clustering, text classification and an end-to-end project. Every idea comes with a picture and code you can run, in a sandbox that runs real Python, pandas and scikit-learn in your browser and checks your answers.

Machine learning is part of the shared core for both the **AI engineer** and the **data / AI analyst** paths: AI engineers build on these ideas every day (training, evaluation, overfitting, data leakage), and analysts use them to predict, segment and explain.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/ml/)

The sandbox runs real Python 3.14 with NumPy, pandas, scikit-learn 1.8 and matplotlib inside your browser (via [Pyodide](https://pyodide.org)). Nothing to install, no sign-up.

- every lesson, with **86 examples** you can run and change
- **48 exercises**, numbered by lesson, that check your code and tell you what's off
- **96 quiz questions**, with explanations
- **7 practice datasets** that load with one line, like `pd.read_csv("churn.csv")`
- a chart or diagram for every key idea, and charts drawn right under your code
- your progress and code saved in your own browser

**Before you start:** you should be comfortable with Python basics and pandas (loading a CSV, selecting columns, `groupby`), and it helps to know averages, spread and correlation. If not, do [Learn Python from scratch](../python/), [Python for Data](../python-data/) and [Statistics with Python](../statistics/) first. No calculus or linear algebra is needed: every idea is explained in words and pictures, then checked with code.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 24 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every machine-learning term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | every scikit-learn step, model and metric on one page, plus a "which model?" and "which metric?" table |
| 🗂️ [Datasets](https://github.com/kishoremadanagopal/learning/tree/main/ml/data) | the practice files, to download and use on your own computer |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.

## Lessons

### Part 1: Machine Learning Foundations (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [What machine learning is](lessons/01-what-is-ml.md) | rules vs learning, models, features and labels, X and y, supervised vs unsupervised, regression vs classification vs clustering, ML in 2026 | 1–2 |
| 2 | [Your first model: fit and predict](lessons/02-first-model.md) | the estimator API, create / fit / predict, LinearRegression, KNeighborsClassifier, predict_proba, coef_ and intercept_, 2-D X | 3–4 |
| 3 | [Train and test: checking on unseen data](lessons/03-train-test.md) | why test on unseen data, train_test_split, test_size, random_state, stratify, score, accuracy, memorisation and overfitting | 5–6 |
| 4 | [The ML workflow and baselines](lessons/04-workflow-and-baselines.md) | the ML workflow, framing the question, building X and y, dropping IDs and the label, DummyClassifier and DummyRegressor, comparing to a baseline | 7–8 |

### Part 2: Regression: Predicting Numbers (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 5 | [Linear regression with many features](lessons/05-linear-regression.md) | linear models with many features, coefficients and intercept, "holding others fixed", least squares, predicting new rows, predicted-vs-actual plots | 9–10 |
| 6 | [Measuring regression errors](lessons/06-regression-metrics.md) | residuals, MAE, MSE, RMSE, R², sklearn.metrics, comparing with a baseline, residual plots, choosing a metric | 11–12 |
| 7 | [Underfitting and overfitting](lessons/07-overfitting.md) | model complexity, polynomial features, underfitting, overfitting, the complexity curve, bias and variance, ways to reduce overfitting | 13–14 |
| 8 | [Regularisation: Ridge and Lasso](lessons/08-regularization.md) | penalising big coefficients, Ridge, Lasso, ElasticNet, alpha, scaling before regularising, feature selection with Lasso | 15–16 |

### Part 3: Classification: Predicting Categories (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 9 | [Logistic regression: predicting yes or no](lessons/09-logistic-regression.md) | classification with probabilities, the sigmoid curve, threshold 0.5, predict_proba, reading coefficient signs, odds, more than two classes | 17–18 |
| 10 | [Beyond accuracy: precision and recall](lessons/10-classification-metrics.md) | the confusion matrix, true/false positives and negatives, precision, recall, F1, classification_report, choosing a metric from the cost of mistakes | 19–20 |
| 11 | [Thresholds, ROC curves and AUC](lessons/11-thresholds-roc.md) | changing the threshold, the precision-recall trade-off, ROC curves, AUC, choosing a threshold from costs, class_weight for rare classes | 21–22 |
| 12 | [k-nearest neighbours and distance](lessons/12-knn.md) | nearest neighbours, Euclidean distance, choosing k, decision boundaries, why scaling matters for distances, KNeighborsRegressor | 23–24 |
| 13 | [Decision trees](lessons/13-decision-trees.md) | yes/no splits, root, nodes and leaves, Gini impurity, export_text, axis-aligned boundaries, max_depth and overfitting, feature_importances_ | 25–26 |
| 14 | [Random forests and gradient boosting](lessons/14-ensembles.md) | ensembles, bagging and bootstrap samples, random forests, gradient boosting, HistGradientBoosting, key hyperparameters, built-in vs permutation importance, XGBoost and LightGBM | 27–28 |

### Part 4: Real-World Data and Workflow (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 15 | [Scaling features](lessons/15-scaling.md) | why units matter, StandardScaler, MinMaxScaler, RobustScaler, transformers and fit / transform / fit_transform, fitting on training data only, which models need scaling | 29–30 |
| 16 | [Text categories and missing values](lessons/16-encoding-and-missing.md) | one-hot encoding, OneHotEncoder and handle_unknown, ordinal encoding with a given order, missing values, SimpleImputer strategies, add_indicator, ColumnTransformer | 31–32 |
| 17 | [Pipelines and data leakage](lessons/17-pipelines-and-leakage.md) | Pipeline and make_pipeline, named steps, predicting from raw rows, get_feature_names_out, train-test contamination, target leakage, the "too good to be true" check | 33–34 |
| 18 | [Cross-validation](lessons/18-cross-validation.md) | the luck of one split, k-fold cross-validation, cross_val_score, mean and standard deviation of scores, stratified folds, scoring names, comparing models, cross_validate, the role of the test set | 35–36 |
| 19 | [Tuning hyperparameters](lessons/19-tuning.md) | hyperparameters, validation curves, GridSearchCV, step__parameter names, best_params_ and best_score_, refit, cv_results_, C in logistic regression, RandomizedSearchCV, nested CV | 37–38 |

### Part 5: Unsupervised Learning (Intermediate)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 20 | [Clustering with k-means](lessons/20-kmeans.md) | clustering without labels, the k-means steps, centroids, fit_predict, inertia and the elbow, silhouette score, describing clusters, scaling, limits of k-means | 39–40 |
| 21 | [Dimensionality reduction with PCA](lessons/21-pca.md) | dimensionality reduction, principal components, explained variance ratio, scaling before PCA, 2-D pictures of many features, reading components_, choosing the number of components, t-SNE and UMAP | 41–42 |

### Part 6: Machine Learning in Practice (Advanced)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 22 | [Classifying text](lessons/22-text-classification.md) | bag of words, CountVectorizer, vocabulary and document-term matrix, sparse matrices, stop words and n-grams, TF-IDF, Naive Bayes, a spam filter, top words, embeddings and LLMs | 43–44 |
| 23 | [From model to product, responsibly](lessons/23-model-to-product.md) | saving and loading pipelines with joblib, version and security warnings, serving predictions, data and concept drift, monitoring, fairness per group and proxies, model cards, classic ML vs LLMs | 45–46 |
| 24 | [Final project: a churn model, start to finish](lessons/24-final-project.md) | framing a business question, choosing a success measure, splitting first, baseline, pipeline, comparing models with CV, tuning, choosing a threshold with cross_val_predict, the single final test, permutation importance on a pipeline, the final report | 47–48 |

## The practice datasets

| File | Rows | What's in it |
|---|---|---|
| [`students.csv`](data/students.csv) | 60 | 60 students: class, hours studied, attendance and exam scores. Small and simple, for your first models. |
| [`housing.csv`](data/housing.csv) | 160 | 160 homes: neighborhood, area, bedrooms, age, distance to the centre and price (in thousands). For predicting numbers. |
| [`fruit.csv`](data/fruit.csv) | 150 | 150 apples, oranges and lemons measured by width, height and weight. For seeing how classifiers draw boundaries. |
| [`churn.csv`](data/churn.csv) | 1000 | 1,000 phone and internet customers: contract, plan, tenure, monthly charge, support calls, age (a few missing), data use and whether they left. |
| [`shoppers.csv`](data/shoppers.csv) | 200 | 200 shop customers: income, spending score, age and visits per month, with no labels. For clustering. |
| [`messages.csv`](data/messages.csv) | 400 | 400 short text messages labelled spam or ham (not spam). For text classification. |
| [`energy.csv`](data/energy.csv) | 40 | 40 days of outdoor temperature and an office building's energy use. Small and curved, for seeing overfitting. |

All of the data is made up for practice, so it's safe to share and experiment with.

## Running it on your own computer

Everything in the course also works in a normal Python setup. Install Python from [python.org](https://www.python.org/), then:

```bash
pip install numpy pandas matplotlib scipy scikit-learn jupyterlab
jupyter lab
```

Download the files from [`data/`](data/) into the same folder as your notebook. The sandbox runs pandas 3, so if your computer has an older pandas, upgrade with `pip install --upgrade pandas`.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
