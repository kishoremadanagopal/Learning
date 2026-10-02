@@ what-is-ml
topics: rules vs learning, models, features and labels, X and y, supervised vs unsupervised, regression vs classification vs clustering, ML in 2026
terms:
- **Machine learning (ML):** getting a computer to learn rules from examples, instead of writing the rules by hand.
- **Model:** the rule a computer learned from data; it turns features into a prediction.
- **Prediction:** the model's answer for an example, often one it has never seen.
- **Feature:** a column the model uses as a clue, such as a fruit's width. All features together are called X.
- **Label:** the answer the model should learn to predict, such as the kind of fruit. Also called the target, and called y in code.
- **Target:** another name for the label.
- **X:** the table of features, one row per example.
- **y:** the column of labels, one per row of X.
- **Training:** letting a model learn from examples with known answers.
- **Supervised learning:** learning from examples that come with the right answers.
- **Unsupervised learning:** finding structure, such as groups, in data with no answers.
- **Regression:** supervised learning that predicts a number.
- **Classification:** supervised learning that predicts a category.
- **Clustering:** unsupervised learning that puts similar rows into groups.
- **Dimensionality reduction:** summarising many columns with a few new ones.
- **scikit-learn:** the standard Python library for machine learning on tables; imported as sklearn.
mistakes:
- Calling a 0/1 or yes/no label "regression" because it's stored as numbers. If it's a category, it's classification.
- Putting the label column inside X. The model then just copies the answer and looks perfect until it meets real data.
- Expecting a model to be right every time. A model gives its best guess from patterns in past examples.

@@ first-model
topics: the estimator API, create / fit / predict, LinearRegression, KNeighborsClassifier, predict_proba, coef_ and intercept_, 2-D X
terms:
- **Estimator:** any scikit-learn model object; they all have fit and either predict or transform.
- **fit:** the method that trains a model: model.fit(X, y).
- **predict:** the method that returns the model's answers for new rows.
- **predict_proba:** for classifiers, the model's probability for each class, in the order of model.classes_.
- **Linear regression:** a model that fits the best straight line (or flat surface) through the data and predicts from it.
- **Coefficient:** a number a linear model learned for a feature: how much the prediction changes per unit of that feature. Stored in coef_.
- **Intercept:** the prediction when every feature is 0. Stored in intercept_.
- **k-nearest neighbours (KNN):** a model that predicts from the k most similar training rows, by vote or average.
- **Hyperparameter:** a setting you choose before training, like n_neighbors.
- **Parameter:** something the model learns during training, like a coefficient.
- **classes_:** the list of categories a classifier learned, in the order predict_proba uses.
mistakes:
- Passing one feature as df["col"] (1-D). X must be a table: df[["col"]].
- Calling predict before fit. The model hasn't learned anything yet, so scikit-learn raises NotFittedError.
- Predicting with different columns, or a different column order, from the ones used in fit.
- Reading too much into one prediction. Check how sure the model is with predict_proba.

@@ train-test
topics: why test on unseen data, train_test_split, test_size, random_state, stratify, score, accuracy, memorisation and overfitting
terms:
- **Training set:** the rows the model learns from.
- **Test set:** rows held back and used only to measure the finished model; it plays the part of new, unseen data.
- **train_test_split:** the scikit-learn function that shuffles rows and splits them into X_train, X_test, y_train, y_test.
- **test_size:** the share of rows kept for testing, such as 0.25.
- **random_state:** a seed that fixes a random process, so results are the same every run.
- **Stratify:** splitting so that each part keeps the same mix of classes as the full data.
- **Accuracy:** the share of predictions that are correct; what score returns for a classifier.
- **score:** a model's built-in measure: accuracy for classifiers, R² for regressors.
- **Generalisation:** how well a model works on data it didn't train on.
- **Overfitting:** learning the training data's noise so well that the model does worse on new data.
mistakes:
- Judging a model by its score on the training data.
- Mixing up the order of the four results. It's always X_train, X_test, y_train, y_test.
- Leaving out random_state and then wondering why the score changes every run.
- Training on the test set "just once". After that it's no longer unseen.

@@ workflow-and-baselines
topics: the ML workflow, framing the question, building X and y, dropping IDs and the label, DummyClassifier and DummyRegressor, comparing to a baseline
terms:
- **ML workflow:** the steps of a project: question, data, split, prepare, train, evaluate, deploy and monitor.
- **Baseline:** the score of the simplest sensible guess, which any real model must beat.
- **DummyClassifier:** a baseline classifier that always predicts the most common class.
- **DummyRegressor:** a baseline regressor that always predicts the average of the training labels.
- **Majority class:** the most common category in the labels.
- **Identifier (ID):** a column that names each row, such as customer_id; not a real feature.
mistakes:
- Reporting "85% accuracy" without the baseline. If 85% of rows are one class, that's no better than guessing.
- Keeping ID columns as features. The model can find meaningless patterns in them.
- Starting to model before the question is clear: what is predicted, for whom, and what action follows.
