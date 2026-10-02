@@ correlation
topics: scatter plots, Pearson's r, testing a correlation with `pearsonr`, Spearman's rank correlation, correlation matrices and heatmaps, confounders, correlation vs causation
terms:
- **Scatter plot:** a chart with one dot per row, placed by two numerical variables.
- **Correlation:** a measure of how two variables move together.
- **Pearson's r:** the strength and direction of a straight-line relationship, from −1 to +1.
- **Spearman's ρ (rho):** a correlation computed on ranks, measuring any steadily rising or falling relationship.
- **Correlation matrix:** a table of the correlations between every pair of variables.
- **Heatmap:** a grid of coloured cells, often used to show a correlation matrix.
- **Confounder:** a third variable that influences both variables in a relationship.
- **Causation:** one variable directly changing another.
mistakes:
- Computing r without looking at the scatter plot. Curves and outliers fool it.
- Saying a correlation proves cause and effect.
- Reading r = 0.3 as "30% related". Square it for the share of variation explained (here 9%).

@@ linear-regression
topics: the regression line, least squares, slope and intercept, `stats.linregress`, prediction and extrapolation, R², residuals and residual plots, testing the slope, regression to the mean
terms:
- **Linear regression:** fitting a straight line to predict an outcome from a predictor.
- **Outcome (dependent variable):** the variable being predicted, y.
- **Predictor (independent variable):** the variable used to predict, x.
- **Slope:** the average change in y for a one-unit increase in x.
- **Intercept:** the predicted y when x is 0.
- **Residual:** actual y minus predicted y.
- **Least squares:** choosing the line that minimises the sum of squared residuals.
- **R² (coefficient of determination):** the share of the variation in y explained by the model.
- **Extrapolation:** predicting outside the range of the data.
- **Regression to the mean:** extreme results tend to be followed by less extreme ones.
mistakes:
- Interpreting the intercept when x = 0 is impossible or far from the data.
- Extrapolating far beyond the data.
- Trusting R² without looking at the residual plot.

@@ multiple-regression
topics: multiple regression, statsmodels formulas, coefficients "holding others fixed", p-values and intervals for coefficients, dummy variables with `C()`, adjusted R², prediction, residual checks, multicollinearity and VIF
terms:
- **Multiple regression:** regression with several predictors.
- **Coefficient:** the estimated effect of one predictor, holding the others fixed.
- **OLS (ordinary least squares):** the standard way of fitting a linear regression.
- **statsmodels:** a Python library for statistical models and tests.
- **Formula:** text like `"price ~ area + C(neighborhood)"` describing a model.
- **Dummy variable:** a 0/1 column representing one category.
- **Reference category:** the category the dummy variables are compared with.
- **Adjusted R²:** R² penalised for the number of predictors.
- **Multicollinearity:** strong correlation between predictors.
- **VIF (variance inflation factor):** a measure of how much multicollinearity inflates a coefficient's uncertainty.
mistakes:
- Reading a coefficient as the effect "on its own" rather than "holding the others fixed".
- Forgetting `C()` around a numeric code that's really a category (like a store number).
- Keeping two near-duplicate predictors and trusting their individual coefficients.
