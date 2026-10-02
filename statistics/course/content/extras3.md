@@ sampling-and-bias
topics: simple random, stratified, cluster and convenience samples, selection, non-response, survivorship and measurement bias, sampling variability, standard error
terms:
- **Simple random sample:** a sample where every member of the population has the same chance of being chosen.
- **Stratified sample:** random samples taken separately from each group (stratum), so every group is represented.
- **Cluster sample:** randomly chosen whole groups, with everyone in them measured.
- **Convenience sample:** whoever is easiest to reach; usually biased.
- **Bias:** a systematic error that pushes results in one direction.
- **Selection bias:** bias from who ends up in the sample.
- **Non-response bias:** bias because people who respond differ from those who don't.
- **Survivorship bias:** bias from looking only at the cases that "survived" some filter.
- **Sampling variability:** the natural difference between one random sample and another.
- **Standard error (SE):** the standard deviation of a statistic across samples; for a mean, s / √n.
mistakes:
- Believing a large sample can't be biased. Size reduces random error, not bias.
- Confusing the standard deviation (spread of the data) with the standard error (uncertainty of an average).
- Forgetting `random_state=` and getting a different sample each time, so results can't be reproduced.

@@ central-limit-theorem
topics: the distribution of sample averages, the central limit theorem, σ / √n, how large n must be, proportions
terms:
- **Sampling distribution:** the distribution of a statistic (like the mean) over many samples.
- **Central limit theorem (CLT):** for large enough samples, sample averages are approximately normal, centred on the population mean, with standard deviation σ / √n.
- **σ (sigma):** the population standard deviation.
- **√n:** the square root of the sample size; why precision grows slowly with more data.
- **Standard error of a proportion:** √(p(1 − p) / n).
mistakes:
- Thinking the CLT makes the data normal. It's the averages that become normal.
- Applying it to tiny samples from very skewed data. Strong skew needs bigger n.
- Expecting it to fix bias or non-random samples.

@@ confidence-intervals
topics: estimate ± critical value × standard error, the t distribution, degrees of freedom, `stats.t.interval`, interpreting 95%, interval width, intervals for proportions, margin of error
terms:
- **Point estimate:** a single best guess, like the sample mean.
- **Confidence interval:** a range of plausible values for a population number, built so that a stated share of such ranges contain it.
- **Confidence level:** the long-run share of intervals that contain the true value, usually 95%.
- **Critical value:** how many standard errors to go out on each side (about 1.96 for 95% with the normal distribution).
- **t distribution:** a bell-shaped distribution with fatter tails than the normal, used when the std is estimated from the sample.
- **Degrees of freedom:** a number that sets the t distribution's shape; n − 1 for one mean.
- **Margin of error:** the "±" part of a confidence interval.
mistakes:
- Saying "95% of the data is in the interval". The interval is about the mean, not individual values.
- Using 1.96 with very small samples. Use the t distribution for means.
- Comparing two groups by checking whether their intervals overlap. Overlapping intervals can still hide a real difference; test the difference directly.

@@ bootstrap
topics: resampling with replacement, bootstrap percentile intervals, intervals for medians and correlations, `scipy.stats.bootstrap`, differences between groups, limits
terms:
- **Bootstrap:** estimating uncertainty by recomputing a statistic on many resamples of your data.
- **Resample:** a sample drawn from your own data, with replacement, the same size as the original.
- **With replacement:** each draw can pick a row that was already picked.
- **Bootstrap distribution:** the statistic's values across all resamples.
- **Percentile interval:** the middle 95% of the bootstrap distribution (2.5th to 97.5th percentiles).
- **BCa interval:** a more accurate bootstrap interval that corrects for bias and skew; SciPy's default.
mistakes:
- Resampling x and y separately when they're pairs. Pick row positions and use them for both.
- Resampling without replacement, which just returns the same data shuffled.
- Expecting the bootstrap to rescue a tiny or biased sample.
