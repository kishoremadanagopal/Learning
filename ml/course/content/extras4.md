@@ scaling
topics: why units matter, StandardScaler, MinMaxScaler, RobustScaler, transformers and fit / transform / fit_transform, fitting on training data only, which models need scaling
terms:
- **Scaling:** changing features to comparable ranges so no feature dominates just because of its units.
- **Transformer:** a scikit-learn object with fit and transform that changes data instead of predicting.
- **transform:** applies what a transformer learned in fit to some data.
- **fit_transform:** fit and transform in one step; use it on training data only.
- **Standardisation:** subtracting the mean and dividing by the standard deviation, giving z-scores.
- **MinMaxScaler:** rescales each feature to the range 0 to 1.
- **RobustScaler:** scales with the median and interquartile range, so outliers barely affect it.
- **Outlier:** a value far from the rest, which can drag the mean and standard deviation.
mistakes:
- Fitting the scaler on all the data, or on the test set. Fit on training data; only transform the test data.
- Calling fit_transform on the test set, which refits the scaler to it.
- Scaling for trees and expecting a difference. It only matters for distance- and penalty-based models.

@@ encoding-and-missing
topics: one-hot encoding, OneHotEncoder and handle_unknown, ordinal encoding with a given order, missing values, SimpleImputer strategies, add_indicator, ColumnTransformer
terms:
- **Encoding:** turning categories (text) into numbers a model can use.
- **One-hot encoding:** one 0/1 column per category, with a single 1 in each row.
- **OneHotEncoder:** scikit-learn's one-hot transformer; remembers the categories it saw in training.
- **handle_unknown="ignore":** makes OneHotEncoder encode a category it never saw as all zeros instead of failing.
- **Ordinal encoding:** one column of numbers for categories with a real order, like basic < standard < premium.
- **OrdinalEncoder:** scikit-learn's ordinal transformer; pass categories= to set the order.
- **Missing value:** an empty cell, shown as NaN in pandas.
- **Imputation:** filling missing values with a sensible guess.
- **SimpleImputer:** fills gaps with the mean, median, most frequent value or a constant, learned from training data.
- **Missing indicator:** a 0/1 column saying whether a value was missing (add_indicator=True).
- **ColumnTransformer:** applies different transformers to different columns and joins the results.
- **Sparse matrix:** a compact format that stores only the non-zero values; OneHotEncoder's default output.
- **passthrough:** in a ColumnTransformer, keeps the listed columns unchanged.
mistakes:
- Numbering unordered categories (0, 1, 2), which invents an order that isn't there.
- Using OrdinalEncoder without categories=, so the order is alphabetical instead of the real one.
- Forgetting handle_unknown="ignore", so the model crashes on the first new category.
- Filling gaps with statistics computed on all the data instead of the training data.

@@ pipelines-and-leakage
topics: Pipeline and make_pipeline, named steps, predicting from raw rows, get_feature_names_out, train-test contamination, target leakage, the "too good to be true" check
terms:
- **Pipeline:** a chain of transformers ending in a model that fits, predicts and scores as one object.
- **named_steps:** a pipeline's steps by name, such as pipe.named_steps["model"].
- **Data leakage:** information that won't be available at prediction time getting into training, making scores look better than reality.
- **Train-test contamination:** a learned step (scaling, imputing, selecting features) seeing test or validation rows.
- **Target leakage:** a feature that is only known after the outcome, or is caused by it.
- **SelectKBest:** a step that keeps the k features most related to the label.
- **get_feature_names_out:** returns the names of the columns a transformer produces.
mistakes:
- Preparing the data before splitting it, so test-set information leaks into training.
- Choosing features with the whole dataset, then evaluating on part of it.
- Keeping a feature you wouldn't have at prediction time, like a closing date or a refund.
- Celebrating a near-perfect score instead of hunting for the leak.

@@ cross-validation
topics: the luck of one split, k-fold cross-validation, cross_val_score, mean and standard deviation of scores, stratified folds, scoring names, comparing models, cross_validate, the role of the test set
terms:
- **Cross-validation (CV):** scoring a model on several different train/validation splits and averaging.
- **Fold:** one of the equal parts the data is cut into for cross-validation.
- **Validation fold:** the fold held out to score the model in one round of CV.
- **Validation set:** data used to compare and choose models; separate from the final test set.
- **k-fold:** cross-validation with k folds, each used once for validation.
- **StratifiedKFold:** k-fold that keeps the class mix the same in every fold; the default for classifiers.
- **KFold:** plain k-fold; pass shuffle=True when rows are in some order.
- **cross_val_score:** returns one score per fold.
- **cross_validate:** like cross_val_score, but with several metrics, fit times and optional training scores.
- **scoring:** the metric name used in CV and search, such as "roc_auc" or "neg_mean_absolute_error".
mistakes:
- Comparing models on one split and trusting a difference smaller than the scores' wobble.
- Doing preprocessing outside the pipeline, so each fold's validation rows leak into training.
- Using the test set to choose between models. That's the validation folds' job.
- Forgetting that neg_ metrics are negative, and picking the "smallest" when higher is better.

@@ tuning
topics: hyperparameters, validation curves, GridSearchCV, step__parameter names, best_params_ and best_score_, refit, cv_results_, C in logistic regression, RandomizedSearchCV, nested CV
terms:
- **Tuning:** searching for the hyperparameter values that give the best validation score.
- **Validation curve:** training and validation scores plotted against one hyperparameter.
- **GridSearchCV:** tries every combination of the listed hyperparameter values with cross-validation.
- **RandomizedSearchCV:** tries a fixed number of random combinations; faster for big search spaces.
- **Parameter grid:** a dictionary of hyperparameter names and the values to try.
- **best_params_:** the winning hyperparameter values of a search.
- **best_score_:** the winning mean cross-validation score.
- **best_estimator_:** the model refitted on all the training data with the best settings.
- **refit:** retraining the best setting on the whole training set after the search (on by default).
- **C:** logistic regression's regularisation setting: smaller C means a stronger penalty.
- **Nested cross-validation:** a search inside each round of an outer CV, for an honest estimate of the whole tuning process.
mistakes:
- Tuning on the test set, then reporting the test score as if it were unseen.
- Writing parameter names without the step prefix in a pipeline grid (use "model__C", not "C").
- Making grids so large the search takes hours; use RandomizedSearchCV or a coarse grid first.
- Reading C like alpha. They work in opposite directions.
