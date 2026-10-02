# Machine learning glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **Accuracy** | The share of predictions that are correct; what score returns for a classifier. [3] |
| **alpha** | The strength of the penalty in Ridge and Lasso; 0 means none, larger means simpler. [8] |
| **AUC (area under the ROC curve)** | One number for how well a model ranks positives above negatives; 0.5 is random, 1.0 is perfect. [11] |
| **Bagging** | Training each model on a different bootstrap sample and averaging their predictions. [14] |
| **Bag of words** | Representing a text by how many times each word appears, ignoring the order. [22] |
| **Baseline** | The score of the simplest sensible guess, which any real model must beat. [4] |
| **best_estimator_** | The model refitted on all the training data with the best settings. [19] |
| **best_params_** | The winning hyperparameter values of a search. [19] |
| **best_score_** | The winning mean cross-validation score. [19] |
| **Bias** | Error from a model's too-rigid assumptions; high bias causes underfitting. [7] |
| **Binary classification** | Classification with two classes, such as yes/no. [9] |
| **Bootstrap sample** | A random sample of rows drawn with replacement, the same size as the original. [14] |
| **C** | Logistic regression's regularisation setting: smaller C means a stronger penalty. [19] |
| **Centroid** | The centre of a cluster: the average of its rows. [20] |
| **classes_** | The list of categories a classifier learned, in the order predict_proba uses. [2] |
| **Classification** | Supervised learning that predicts a category. [1] |
| **class_weight="balanced"** | Makes mistakes on rare classes count more during training. [11] |
| **Clustering** | Unsupervised learning that puts similar rows into groups. [1, 20] |
| **Cluster profile** | The average of each feature within each cluster, used to describe what the cluster means. [20] |
| **Coefficient** | A number a linear model learned for a feature: how much the prediction changes per unit of that feature. Stored in coef_. [2, 5] |
| **ColumnTransformer** | Applies different transformers to different columns and joins the results. [16] |
| **Complexity curve** | Training and test error plotted against complexity; the test error is lowest at the sweet spot. [7] |
| **components_** | The weights each component gives to the original features. [21] |
| **Concept drift** | A change in the relationship between features and the label. [23] |
| **Confusion matrix** | A table counting true negatives, false positives, false negatives and true positives. [10] |
| **ConvergenceWarning** | A warning that training stopped before settling; fix it by raising max_iter or scaling the features. [9] |
| **CountVectorizer** | Turns texts into word counts. [22] |
| **cross_validate** | Like cross_val_score, but with several metrics, fit times and optional training scores. [18] |
| **Cross-validation (CV)** | Scoring a model on several different train/validation splits and averaging. [18] |
| **cross_val_predict** | Returns, for every training row, the prediction from the CV round in which that row was held out. [24] |
| **cross_val_score** | Returns one score per fold. [18] |
| **Customer segmentation** | Clustering customers into groups that behave alike, so each can be treated differently. [20] |
| **Data drift** | A change in the input data compared with the training data. [23] |
| **Data leakage** | Information that won't be available at prediction time getting into training, making scores look better than reality. [17] |
| **DBSCAN** | A clustering method that finds groups of any shape and can leave odd points unassigned. [20] |
| **Decision boundary** | The line or surface where a classifier's prediction changes from one class to another. [12] |
| **Decision tree** | A model that predicts by asking a series of yes/no questions about the features. [13] |
| **Degree** | The highest power in polynomial features. [7] |
| **Deliverable** | What the project hands over: the model, its honest numbers, explanations and limits. [24] |
| **Depth** | The number of questions on the longest path from the root to a leaf. [13] |
| **Dimension** | A column (feature) of the data; 3 features means 3-dimensional data. [21] |
| **Dimensionality reduction** | Summarising many columns with a few new ones. [1, 21] |
| **Distance** | How far apart two rows are; KNN usually uses straight-line (Euclidean) distance. [12] |
| **Document-term matrix** | A table with one row per text and one column per word, holding counts or weights. [22] |
| **DummyClassifier** | A baseline classifier that always predicts the most common class. [4] |
| **DummyRegressor** | A baseline regressor that always predicts the average of the training labels. [4] |
| **ElasticNet** | Linear regression with a mix of the Ridge and Lasso penalties. [8] |
| **Elbow method** | Choosing k where adding more clusters stops reducing inertia much. [20] |
| **Embedding** | A list of numbers produced by a language model that captures a text's meaning; similar meanings get similar numbers. [22] |
| **Encoding** | Turning categories (text) into numbers a model can use. [16] |
| **Ensemble** | A model that combines the predictions of many models. [14] |
| **Estimator** | Any scikit-learn model object; they all have fit and either predict or transform. [2] |
| **EU AI Act** | The European Union's law setting rules for AI systems according to their risk. [23] |
| **Euclidean distance** | The square root of the sum of squared differences across features. [12] |
| **Evals** | Tests that measure how well an AI system (such as an LLM) performs, using held-out labelled examples. [22] |
| **Explained variance ratio** | The share of the total variation each component captures. [21] |
| **export_text** | Prints a fitted tree as readable if/else rules. [13] |
| **F1 score** | The harmonic mean of precision and recall; high only when both are high. [10] |
| **Fairness** | A model working comparably well for different groups of people. [23] |
| **False negative (FN)** | A positive wrongly predicted as negative; a miss. [10] |
| **False positive (FP)** | A negative wrongly predicted as positive; a false alarm. [10] |
| **False positive rate** | FP ÷ (FP + TN): the share of real negatives wrongly flagged. [11] |
| **FastAPI** | A popular Python library for building web APIs, often used to serve models. [23] |
| **Feature** | A column the model uses as a clue, such as a fruit's width. All features together are called X. [1] |
| **Feature importance** | How much each feature helped the model; for trees, the total impurity reduction from its splits. [13] |
| **Feature scale** | The typical size of a feature's values, which depends on its units. [12] |
| **Feature selection** | Keeping only the features that help; Lasso does it automatically. [8] |
| **Final test** | The single, last evaluation on the untouched test set. [24] |
| **fit** | The method that trains a model: model.fit(X, y). [2] |
| **fit_predict** | Fits a clustering model and returns each row's cluster number. [20] |
| **fit_transform** | Fit and transform in one step; use it on training data only. [15] |
| **Fold** | One of the equal parts the data is cut into for cross-validation. [18] |
| **Generalisation** | How well a model works on data it didn't train on. [3] |
| **get_feature_names_out** | Returns the names of the columns a transformer produces. [17] |
| **Gini impurity** | A measure of how mixed the classes in a group are; 0 means all one class. [13] |
| **Gradient boosting** | Trees built one after another, each correcting the errors of the ones before; their outputs are added up. [14] |
| **GridSearchCV** | Tries every combination of the listed hyperparameter values with cross-validation. [19] |
| **handle_unknown="ignore"** | Makes OneHotEncoder encode a category it never saw as all zeros instead of failing. [16] |
| **HistGradientBoostingClassifier** | Scikit-learn's fast gradient-boosting model, which bins feature values. [14] |
| **Holding other features fixed** | Comparing rows that differ in only one feature; what a coefficient describes. [5] |
| **Hyperparameter** | A setting you choose before training, like n_neighbors. [2] |
| **Identifier (ID)** | A column that names each row, such as customer_id; not a real feature. [4] |
| **Imbalanced classes** | When one class is much rarer than the other, which makes accuracy misleading. [10] |
| **Imputation** | Filling missing values with a sensible guess. [16] |
| **Inertia** | The total squared distance from each row to its cluster centre; lower means tighter clusters. [20] |
| **Interaction** | When one feature's effect depends on another, such as support calls mattering mostly for new customers. [13] |
| **Intercept** | The prediction when every feature is 0. Stored in intercept_. [2, 5] |
| **joblib** | A library that saves Python objects, such as fitted pipelines, to files and loads them back. [23] |
| **k-fold** | Cross-validation with k folds, each used once for validation. [18] |
| **KFold** | Plain k-fold; pass shuffle=True when rows are in some order. [18] |
| **k-means** | A clustering method that alternates between assigning rows to the nearest centre and moving each centre to the average of its rows. [20] |
| **k-nearest neighbours (KNN)** | A model that predicts from the k most similar training rows, by vote or average. [2, 12] |
| **KNeighborsRegressor** | KNN for numbers: the average label of the nearest rows. [12] |
| **Label** | The answer the model should learn to predict, such as the kind of fruit. Also called the target, and called y in code. [1] |
| **Large language model (LLM)** | A very large model trained on text that can follow instructions, such as labelling a message. [22] |
| **Lasso** | Linear regression with a penalty on absolute coefficients; can set some exactly to 0. [8] |
| **Lazy learner** | A model like KNN that does almost nothing in fit and all its work when predicting. [12] |
| **Leaf** | An end point of the tree that gives the prediction. [13] |
| **learning_rate** | In boosting, how big each tree's correction is; smaller usually needs more trees but generalises better. [14] |
| **Least squares** | Choosing coefficients so the sum of squared training errors is as small as possible. [5] |
| **Linear regression** | A model that fits the best straight line (or flat surface) through the data and predicts from it. [2, 5] |
| **Logistic regression** | A classification model that turns a weighted sum of the features into a probability with the sigmoid curve. [9] |
| **Machine learning (ML)** | Getting a computer to learn rules from examples, instead of writing the rules by hand. [1] |
| **MAE (mean absolute error)** | The average size of the errors, in the label's units. [6] |
| **Majority class** | The most common category in the labels. [4] |
| **make_pipeline** | Joins several steps into one model that runs them in order. [7] |
| **max_depth** | A limit on how deep a tree can grow; the main way to stop it overfitting. [13] |
| **MinMaxScaler** | Rescales each feature to the range 0 to 1. [15] |
| **min_samples_leaf** | The smallest number of training rows allowed in a leaf. [13] |
| **Missing indicator** | A 0/1 column saying whether a value was missing (add_indicator=True). [16] |
| **Missing value** | An empty cell, shown as NaN in pandas. [16] |
| **ML workflow** | The steps of a project: question, data, split, prepare, train, evaluate, deploy and monitor. [4] |
| **Model** | The rule a computer learned from data; it turns features into a prediction. [1] |
| **Model card** | A short document describing a model's intended use, data, performance, groups checked and limits. [23] |
| **Model complexity** | How flexible a model is, set by knobs like polynomial degree, n_neighbors or tree depth. [7] |
| **Monitoring** | Tracking a live model's inputs, predictions and accuracy over time. [23] |
| **MSE (mean squared error)** | The average of the squared errors. [6] |
| **Multiclass classification** | Classification with more than two classes, such as three kinds of fruit. [9] |
| **Naive Bayes** | A fast probabilistic classifier that combines how likely each word is in each class. [22] |
| **named_steps** | A pipeline's steps by name, such as pipe.named_steps["model"]. [17] |
| **n_components** | How many components to keep, or (between 0 and 1) what share of variation to keep. [21] |
| **Nested cross-validation** | A search inside each round of an outer CV, for an honest estimate of the whole tuning process. [19] |
| **n_estimators** | The number of trees in a random forest. [14] |
| **n-gram** | A run of n neighbouring words, such as "free prize" (a 2-gram, or bigram). [22] |
| **n_init** | How many random starts k-means tries, keeping the best. [20] |
| **Node** | A point in the tree where a question splits the rows. [13] |
| **Odds** | Probability ÷ (1 − probability). A 20% chance is odds of 0.25. [9] |
| **OneHotEncoder** | Scikit-learn's one-hot transformer; remembers the categories it saw in training. [16] |
| **One-hot encoding** | One 0/1 column per category, with a single 1 in each row. [16] |
| **OrdinalEncoder** | Scikit-learn's ordinal transformer; pass categories= to set the order. [16] |
| **Ordinal encoding** | One column of numbers for categories with a real order, like basic < standard < premium. [16] |
| **Outlier** | A value far from the rest, which can drag the mean and standard deviation. [15] |
| **Out-of-fold prediction** | A prediction for a row made by a model that didn't train on it. [24] |
| **Overfitting** | Learning the training data's noise so well that the model does worse on new data. [3, 7] |
| **Parameter** | Something the model learns during training, like a coefficient. [2] |
| **Parameter grid** | A dictionary of hyperparameter names and the values to try. [19] |
| **passthrough** | In a ColumnTransformer, keeps the listed columns unchanged. [16] |
| **PCA (principal component analysis)** | Finds new axes (principal components) along which the data varies most. [21] |
| **Permutation importance** | How much a model's score drops when one feature's values are shuffled. [14] |
| **Pipeline** | A chain of transformers ending in a model that fits, predicts and scores as one object. [17] |
| **Polynomial features** | Extra columns made from powers of a feature (x², x³…) so a linear model can draw curves. [7] |
| **PolynomialFeatures** | The scikit-learn step that adds powers of the features. [7] |
| **Positive class** | The class you're trying to find (fraud, spam, leaving); not necessarily a good thing. [10] |
| **Precision** | TP ÷ (TP + FP): when the model says yes, how often it's right. [10] |
| **Precision-recall trade-off** | Lowering the threshold raises recall and usually lowers precision, and the reverse. [11] |
| **predict** | The method that returns the model's answers for new rows. [2] |
| **Predicted-vs-actual plot** | A scatter of predictions against the real values; a perfect model puts every point on the diagonal. [5] |
| **Prediction** | The model's answer for an example, often one it has never seen. [1] |
| **predict_proba** | For classifiers, the model's probability for each class, in the order of model.classes_. [2] |
| **Principal component** | A new column made as a weighted mix of the original features; PC1 holds the most variation. [21] |
| **Probability** | A number from 0 to 1 saying how likely something is; predict_proba returns one per class. [9] |
| **Proxy** | A feature that indirectly reveals another one, such as a postcode standing in for ethnicity or income. [23] |
| **Random forest** | Many decision trees, each on a bootstrap sample with random features per split, averaged together. [14] |
| **RandomizedSearchCV** | Tries a fixed number of random combinations; faster for big search spaces. [19] |
| **random_state** | A seed that fixes a random process, so results are the same every run. [3] |
| **Ranking** | Ordering rows from most to least likely positive; what AUC measures. [11] |
| **R² (coefficient of determination)** | The share of the variation in the label that the model explains, compared with always predicting the average. 1 is perfect, 0 is no better than the average, below 0 is worse. [6] |
| **Recall** | TP ÷ (TP + FN): of all real positives, how many the model found. Also called sensitivity or true positive rate. [10] |
| **refit** | Retraining the best setting on the whole training set after the search (on by default). [19] |
| **Regression** | Supervised learning that predicts a number. [1] |
| **Regularisation** | Adding a penalty for big coefficients to the training goal, to reduce overfitting. [8] |
| **Residual** | Actual minus predicted for one row; the model's error on that row. [6] |
| **Residual plot** | Residuals plotted against predictions; a healthy model shows a shapeless cloud around 0. [6] |
| **Retraining** | Fitting the model again on fresher data. [23] |
| **Ridge** | Linear regression with a penalty on squared coefficients; shrinks them all smoothly. [8] |
| **RMSE (root mean squared error)** | The square root of MSE, back in the label's units; big errors count extra. [6] |
| **RobustScaler** | Scales with the median and interquartile range, so outliers barely affect it. [15] |
| **ROC curve** | True positive rate against false positive rate for every possible threshold. [11] |
| **Root** | The first question at the top of a tree. [13] |
| **Scaling** | Changing features to comparable ranges so no feature dominates just because of its units. [15] |
| **scikit-learn** | The standard Python library for machine learning on tables; imported as sklearn. [1] |
| **score** | A model's built-in measure: accuracy for classifiers, R² for regressors. [3] |
| **scoring** | The metric name used in CV and search, such as "roc_auc" or "neg_mean_absolute_error". [18] |
| **SelectKBest** | A step that keeps the k features most related to the label. [17] |
| **Serialisation** | Saving an object to a file or bytes so it can be loaded later. [23] |
| **Serving** | Making a model's predictions available to other software, often as a web API. [23] |
| **Sigmoid** | The S-shaped function that turns any number into a value between 0 and 1. [9] |
| **Silhouette score** | From −1 to 1, how much closer rows are to their own cluster than to the nearest other one. [20] |
| **SimpleImputer** | Fills gaps with the mean, median, most frequent value or a constant, learned from training data. [16] |
| **sklearn.metrics** | The scikit-learn module with metric functions such as mean_absolute_error and r2_score. [6] |
| **Sparse matrix** | A compact format that stores only the non-zero values; OneHotEncoder's default output. [16] |
| **Standardisation** | Subtracting the mean and dividing by the standard deviation, giving z-scores. [15] |
| **Standardised coefficient** | A coefficient on scaled features: the effect of one standard deviation of the feature, comparable across features. [8] |
| **StandardScaler** | A step that rescales each feature to mean 0 and standard deviation 1. [8] |
| **Stop words** | Very common words (the, a, to) often removed because they carry little meaning. [22] |
| **StratifiedKFold** | K-fold that keeps the class mix the same in every fold; the default for classifiers. [18] |
| **Stratify** | Splitting so that each part keeps the same mix of classes as the full data. [3] |
| **Success measure** | The metric and target agreed before modelling, such as recall of at least 0.7. [24] |
| **Supervised learning** | Learning from examples that come with the right answers. [1] |
| **Support** | The number of test rows in each class, shown in classification_report. [10] |
| **Target** | Another name for the label. [1] |
| **Target leakage** | A feature that is only known after the outcome, or is caused by it. [17] |
| **Test set** | Rows held back and used only to measure the finished model; it plays the part of new, unseen data. [3] |
| **test_size** | The share of rows kept for testing, such as 0.25. [3] |
| **TF-IDF** | Term frequency × inverse document frequency: a word's count, scaled down if it appears in many texts. [22] |
| **TfidfVectorizer** | Turns texts into TF-IDF weights. [22] |
| **Threshold** | The probability above which a classifier says "yes"; 0.5 by default. [9] |
| **Training** | Letting a model learn from examples with known answers. [1] |
| **Training set** | The rows the model learns from. [3] |
| **Train-test contamination** | A learned step (scaling, imputing, selecting features) seeing test or validation rows. [17] |
| **train_test_split** | The scikit-learn function that shuffles rows and splits them into X_train, X_test, y_train, y_test. [3] |
| **transform** | Applies what a transformer learned in fit to some data. [15] |
| **Transformer** | A scikit-learn object with fit and transform that changes data instead of predicting. [15] |
| **True negative (TN)** | A negative correctly predicted as negative. [10] |
| **True positive rate** | Another name for recall. [11] |
| **True positive (TP)** | A positive correctly predicted as positive. [10] |
| **t-SNE / UMAP** | Non-linear methods for drawing complex data in 2-D; good for pictures, with axes that have no meaning. [21] |
| **Tuning** | Searching for the hyperparameter values that give the best validation score. [19] |
| **Underfitting** | A model too simple for the pattern; it does badly on both training and test data. [7] |
| **Unsupervised learning** | Finding structure, such as groups, in data with no answers. [1] |
| **Validation curve** | Training and validation scores plotted against one hyperparameter. [19] |
| **Validation fold** | The fold held out to score the model in one round of CV. [18] |
| **Validation set** | Data used to compare and choose models; separate from the final test set. [18] |
| **Variance** | How much a model changes with different training rows; high variance causes overfitting. [7] |
| **Vocabulary** | All the distinct words a vectorizer learned from the training texts. [22] |
| **X** | The table of features, one row per example. [1] |
| **XGBoost / LightGBM / CatBoost** | Popular gradient-boosting libraries outside scikit-learn. [14] |
| **y** | The column of labels, one per row of X. [1] |
