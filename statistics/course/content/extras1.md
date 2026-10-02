@@ what-is-statistics
topics: populations and samples, statistics and parameters, descriptive vs inferential, kinds of variables
terms:
- **Statistics:** learning about a whole group from data about part of it, and saying how sure you are.
- **Population:** everything or everyone you want to draw conclusions about.
- **Sample:** the part of the population you actually measure.
- **Parameter:** a true number for the whole population, like the average height of every adult.
- **Statistic:** a number calculated from a sample, used to estimate a parameter.
- **Descriptive statistics:** summarising the data you have.
- **Inferential statistics:** drawing conclusions about the population from a sample, with a measure of uncertainty.
- **Variable:** something recorded about each row, such as a score or a city.
- **Categorical variable:** a variable whose values are labels, like city or product.
- **Numerical variable:** a variable whose values are numbers you can do maths with.
- **Ordinal variable:** categories with a natural order, like small, medium, large.
mistakes:
- Treating a sample's number as the exact truth. A different sample gives a slightly different answer; statistics measures how different.
- Averaging codes that are really categories, like store IDs or postcodes.
- Generalising from a sample that doesn't represent the population (more on this in Part 3).

@@ center
topics: mean, median, mode, outliers, skew, choosing a "typical" value, weighted mean
terms:
- **Mean:** the sum of the values divided by how many there are; the "average".
- **Median:** the middle value when the values are sorted.
- **Mode:** the most common value.
- **Outlier:** a value far from the others.
- **Skewed:** having a long tail on one side.
- **Robust:** not much affected by outliers. The median is robust; the mean is not.
- **Weighted mean:** an average where some values count more than others.
mistakes:
- Reporting the mean for skewed data like incomes, waiting times or order values. Check the median too.
- Forgetting that `mode()` can return several values. Use `mode()[0]` for one.
- Comparing means of groups without looking at how many rows each group has.

@@ spread
topics: range, quartiles, IQR, variance, standard deviation, `n - 1`, box plots, coefficient of variation
terms:
- **Spread (variability):** how far values are spread out.
- **Range:** the largest value minus the smallest.
- **Quartiles:** the values that split sorted data into four equal parts: Q1, the median and Q3.
- **IQR (interquartile range):** Q3 minus Q1, the spread of the middle 50%.
- **Deviation:** a value's distance from the mean.
- **Variance:** the average squared deviation (dividing by n − 1 for a sample).
- **Standard deviation (std):** the square root of the variance: the typical distance from the mean.
- **Box plot:** a chart of the quartiles, whiskers and outliers.
- **Coefficient of variation (CV):** the standard deviation divided by the mean.
mistakes:
- Mixing up variance and standard deviation. Variance is in squared units; report the std.
- Getting slightly different answers from NumPy and pandas. `np.std` divides by n; pandas divides by n − 1. Use `ddof=1` in NumPy for samples.
- Describing data with an average alone. Always add a measure of spread.

@@ shape-and-outliers
topics: histograms and bins, symmetric and skewed shapes, `skew()`, log transform, z-scores, outlier rules
terms:
- **Distribution:** how the values of a variable are spread across possible values.
- **Histogram:** bars counting how many values fall into each range (bin).
- **Bin:** one range of values in a histogram.
- **Right-skewed:** a long tail of large values; the mean is above the median.
- **Left-skewed:** a long tail of small values; the mean is below the median.
- **Bimodal:** having two peaks, often two groups mixed together.
- **z-score:** (value − mean) / std: how many standard deviations a value is from the mean.
- **Standardising:** converting values to z-scores so different variables share one scale.
- **Log transform:** analysing log(x) instead of x to pull in a long right tail.
mistakes:
- Trusting one histogram. Try a few bin counts; the shape can change.
- Using the z-score rule on strongly skewed data, where the mean and std are themselves distorted.
- Deleting outliers automatically. Investigate first.

@@ categorical-data
topics: counts and proportions, the mean of 0/1 data, bar vs pie charts, two-way tables, row percentages
terms:
- **Frequency:** how many times a value occurs.
- **Proportion:** a count divided by the total, between 0 and 1.
- **Relative frequency:** another name for proportion.
- **Binary variable:** a variable with two values, often coded 1 (yes) and 0 (no).
- **Rate:** a proportion of a group, like the conversion rate.
- **Two-way (contingency) table:** counts for every combination of two categorical variables.
- **Row percentages:** each row of a two-way table divided by its row total.
mistakes:
- Comparing raw counts between groups of different sizes. Compare percentages.
- Using a pie chart with many slices or close values. Use a sorted bar chart.
- Normalising the wrong direction. Ask "percent of what?" before choosing `normalize="index"` or `"columns"`.
