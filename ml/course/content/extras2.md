@@ linear-regression
topics: linear models with many features, coefficients and intercept, "holding others fixed", least squares, predicting new rows, predicted-vs-actual plots
terms:
- **Linear regression:** a model whose prediction is the intercept plus a coefficient times each feature, added up.
- **Least squares:** choosing coefficients so the sum of squared training errors is as small as possible.
- **Coefficient:** the change in the prediction for one more unit of a feature, with the other features unchanged.
- **Intercept:** the model's prediction when every feature is 0.
- **Holding other features fixed:** comparing rows that differ in only one feature; what a coefficient describes.
- **Predicted-vs-actual plot:** a scatter of predictions against the real values; a perfect model puts every point on the diagonal.
mistakes:
- Comparing raw coefficients to rank features. Their sizes depend on units; standardise first.
- Reading a coefficient as cause and effect. A model learns patterns in data, not what happens if you change something.
- Building the new row with columns in a different order, or missing one, from the training data.

@@ regression-metrics
topics: residuals, MAE, MSE, RMSE, R², sklearn.metrics, comparing with a baseline, residual plots, choosing a metric
terms:
- **Residual:** actual minus predicted for one row; the model's error on that row.
- **MAE (mean absolute error):** the average size of the errors, in the label's units.
- **MSE (mean squared error):** the average of the squared errors.
- **RMSE (root mean squared error):** the square root of MSE, back in the label's units; big errors count extra.
- **R² (coefficient of determination):** the share of the variation in the label that the model explains, compared with always predicting the average. 1 is perfect, 0 is no better than the average, below 0 is worse.
- **Residual plot:** residuals plotted against predictions; a healthy model shows a shapeless cloud around 0.
- **sklearn.metrics:** the scikit-learn module with metric functions such as mean_absolute_error and r2_score.
mistakes:
- Computing metrics on the training data and reporting them as the model's quality.
- Reporting only R². People understand "typically off by 41,000" (MAE) much better.
- Forgetting that R² can be negative. It doesn't run from 0 to 1 on test data.
- Passing predictions first to metric functions. The habit is metric(y_true, y_pred).

@@ overfitting
topics: model complexity, polynomial features, underfitting, overfitting, the complexity curve, bias and variance, ways to reduce overfitting
terms:
- **Underfitting:** a model too simple for the pattern; it does badly on both training and test data.
- **Overfitting:** a model so flexible it learns the training data's noise; good on training data, worse on new data.
- **Model complexity:** how flexible a model is, set by knobs like polynomial degree, n_neighbors or tree depth.
- **Polynomial features:** extra columns made from powers of a feature (x², x³…) so a linear model can draw curves.
- **Degree:** the highest power in polynomial features.
- **Complexity curve:** training and test error plotted against complexity; the test error is lowest at the sweet spot.
- **Bias:** error from a model's too-rigid assumptions; high bias causes underfitting.
- **Variance:** how much a model changes with different training rows; high variance causes overfitting.
- **make_pipeline:** joins several steps into one model that runs them in order.
- **PolynomialFeatures:** the scikit-learn step that adds powers of the features.
mistakes:
- Choosing the most complex model because its training error is lowest.
- Believing a perfect training score means a perfect model. It usually means memorising.
- Thinking overfitting only happens with fancy models. Even linear regression overfits with too many features and too few rows.

@@ regularization
topics: penalising big coefficients, Ridge, Lasso, ElasticNet, alpha, scaling before regularising, feature selection with Lasso
terms:
- **Regularisation:** adding a penalty for big coefficients to the training goal, to reduce overfitting.
- **alpha:** the strength of the penalty in Ridge and Lasso; 0 means none, larger means simpler.
- **Ridge:** linear regression with a penalty on squared coefficients; shrinks them all smoothly.
- **Lasso:** linear regression with a penalty on absolute coefficients; can set some exactly to 0.
- **ElasticNet:** linear regression with a mix of the Ridge and Lasso penalties.
- **Feature selection:** keeping only the features that help; Lasso does it automatically.
- **StandardScaler:** a step that rescales each feature to mean 0 and standard deviation 1.
- **Standardised coefficient:** a coefficient on scaled features: the effect of one standard deviation of the feature, comparable across features.
mistakes:
- Regularising without scaling, so features in small units get punished unfairly.
- Using alpha that's far too big and wondering why the model is no better than the average.
- Picking alpha by the training score. Like any hyperparameter, choose it on unseen data.
