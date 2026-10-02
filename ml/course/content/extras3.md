@@ logistic-regression
topics: classification with probabilities, the sigmoid curve, threshold 0.5, predict_proba, reading coefficient signs, odds, more than two classes
terms:
- **Logistic regression:** a classification model that turns a weighted sum of the features into a probability with the sigmoid curve.
- **Sigmoid:** the S-shaped function that turns any number into a value between 0 and 1.
- **Probability:** a number from 0 to 1 saying how likely something is; predict_proba returns one per class.
- **Threshold:** the probability above which a classifier says "yes"; 0.5 by default.
- **Odds:** probability ÷ (1 − probability). A 20% chance is odds of 0.25.
- **Binary classification:** classification with two classes, such as yes/no.
- **Multiclass classification:** classification with more than two classes, such as three kinds of fruit.
- **ConvergenceWarning:** a warning that training stopped before settling; fix it by raising max_iter or scaling the features.
mistakes:
- Thinking logistic regression predicts numbers because of its name. It's a classifier.
- Using predict when you need a ranking or a custom threshold. Use predict_proba(X)[:, 1].
- Reading a coefficient as "adds this much to the probability". It works on the score scale, so the effect on probability varies.

@@ classification-metrics
topics: the confusion matrix, true/false positives and negatives, precision, recall, F1, classification_report, choosing a metric from the cost of mistakes
terms:
- **Confusion matrix:** a table counting true negatives, false positives, false negatives and true positives.
- **Positive class:** the class you're trying to find (fraud, spam, leaving); not necessarily a good thing.
- **True positive (TP):** a positive correctly predicted as positive.
- **False positive (FP):** a negative wrongly predicted as positive; a false alarm.
- **False negative (FN):** a positive wrongly predicted as negative; a miss.
- **True negative (TN):** a negative correctly predicted as negative.
- **Precision:** TP ÷ (TP + FP): when the model says yes, how often it's right.
- **Recall:** TP ÷ (TP + FN): of all real positives, how many the model found. Also called sensitivity or true positive rate.
- **F1 score:** the harmonic mean of precision and recall; high only when both are high.
- **Support:** the number of test rows in each class, shown in classification_report.
- **Imbalanced classes:** when one class is much rarer than the other, which makes accuracy misleading.
mistakes:
- Judging a model on imbalanced data by accuracy alone.
- Swapping the arguments: metrics take (y_true, y_pred). For precision and recall, the order changes the answer.
- Mixing up precision and recall. Precision is about the alarms raised; recall is about the real cases.

@@ thresholds-roc
topics: changing the threshold, the precision-recall trade-off, ROC curves, AUC, choosing a threshold from costs, class_weight for rare classes
terms:
- **Precision-recall trade-off:** lowering the threshold raises recall and usually lowers precision, and the reverse.
- **True positive rate:** another name for recall.
- **False positive rate:** FP ÷ (FP + TN): the share of real negatives wrongly flagged.
- **ROC curve:** true positive rate against false positive rate for every possible threshold.
- **AUC (area under the ROC curve):** one number for how well a model ranks positives above negatives; 0.5 is random, 1.0 is perfect.
- **class_weight="balanced":** makes mistakes on rare classes count more during training.
- **Ranking:** ordering rows from most to least likely positive; what AUC measures.
mistakes:
- Passing 0/1 predictions to roc_auc_score instead of probabilities.
- Choosing the threshold on the test set. Choose it on validation data, from the costs of each mistake.
- Thinking class_weight makes a model better at ranking. It mostly shifts where the line is drawn.

@@ knn
topics: nearest neighbours, Euclidean distance, choosing k, decision boundaries, why scaling matters for distances, KNeighborsRegressor
terms:
- **k-nearest neighbours (KNN):** predicts from the k closest training rows: a vote for classes, an average for numbers.
- **Distance:** how far apart two rows are; KNN usually uses straight-line (Euclidean) distance.
- **Euclidean distance:** the square root of the sum of squared differences across features.
- **Decision boundary:** the line or surface where a classifier's prediction changes from one class to another.
- **Feature scale:** the typical size of a feature's values, which depends on its units.
- **KNeighborsRegressor:** KNN for numbers: the average label of the nearest rows.
- **Lazy learner:** a model like KNN that does almost nothing in fit and all its work when predicting.
mistakes:
- Using KNN without scaling features, so the feature with the biggest units decides everything.
- Picking k=1 because it scores perfectly on the training data.
- Using KNN on very large datasets, where every prediction compares against every stored row and gets slow.

@@ decision-trees
topics: yes/no splits, root, nodes and leaves, Gini impurity, export_text, axis-aligned boundaries, max_depth and overfitting, feature_importances_
terms:
- **Decision tree:** a model that predicts by asking a series of yes/no questions about the features.
- **Root:** the first question at the top of a tree.
- **Node:** a point in the tree where a question splits the rows.
- **Leaf:** an end point of the tree that gives the prediction.
- **Depth:** the number of questions on the longest path from the root to a leaf.
- **Gini impurity:** a measure of how mixed the classes in a group are; 0 means all one class.
- **max_depth:** a limit on how deep a tree can grow; the main way to stop it overfitting.
- **min_samples_leaf:** the smallest number of training rows allowed in a leaf.
- **export_text:** prints a fitted tree as readable if/else rules.
- **Feature importance:** how much each feature helped the model; for trees, the total impurity reduction from its splits.
- **Interaction:** when one feature's effect depends on another, such as support calls mattering mostly for new customers.
mistakes:
- Growing trees without limits on noisy data and trusting the perfect training score.
- Over-trusting one tree's structure. A slightly different sample can produce a very different tree.
- Scaling features for a tree. It's harmless but pointless.

@@ ensembles
topics: ensembles, bagging and bootstrap samples, random forests, gradient boosting, HistGradientBoosting, key hyperparameters, built-in vs permutation importance, XGBoost and LightGBM
terms:
- **Ensemble:** a model that combines the predictions of many models.
- **Bootstrap sample:** a random sample of rows drawn with replacement, the same size as the original.
- **Bagging:** training each model on a different bootstrap sample and averaging their predictions.
- **Random forest:** many decision trees, each on a bootstrap sample with random features per split, averaged together.
- **Gradient boosting:** trees built one after another, each correcting the errors of the ones before; their outputs are added up.
- **n_estimators:** the number of trees in a random forest.
- **learning_rate:** in boosting, how big each tree's correction is; smaller usually needs more trees but generalises better.
- **HistGradientBoostingClassifier:** scikit-learn's fast gradient-boosting model, which bins feature values.
- **Permutation importance:** how much a model's score drops when one feature's values are shuffled.
- **XGBoost / LightGBM / CatBoost:** popular gradient-boosting libraries outside scikit-learn.
mistakes:
- Trusting built-in feature importances blindly; they favour features with many distinct values.
- Comparing an ensemble only with a single tree. Also compare with a baseline and a simple linear model.
- Reaching for a neural network first on spreadsheet-like data, where tree ensembles usually win.
