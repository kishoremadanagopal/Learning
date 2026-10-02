@@ hypothesis-testing
topics: null and alternative hypotheses, test statistics, null distributions, permutation tests, p-values, α, one- vs two-sided tests, reading p-values correctly
terms:
- **Hypothesis test:** a method for judging whether data gives evidence against a "no effect" explanation.
- **Null hypothesis (H₀):** the default claim of no effect or no difference.
- **Alternative hypothesis (H₁):** the claim that there is an effect or difference.
- **Test statistic:** a number that measures how far the data is from what H₀ predicts.
- **Null distribution:** the values the test statistic would take if H₀ were true.
- **p-value:** the probability of a result at least as extreme as the one observed, if H₀ were true.
- **Significance level (α):** the cut-off for calling a result significant, usually 0.05.
- **Statistically significant:** p below α; evidence against H₀, not necessarily an important effect.
- **Permutation test:** a test that builds the null distribution by shuffling group labels.
- **Two-sided test:** a test that counts extreme results in both directions.
- **Effect size:** how big a difference or relationship is, separate from whether it's significant.
mistakes:
- Reading p as "the probability H₀ is true" or "the probability the result is due to chance".
- Treating "not significant" as proof of no effect. It means not enough evidence.
- Choosing one-sided tests or changing α after seeing the data.

@@ t-tests
topics: the t statistic, one-sample, Welch's two-sample and paired t-tests, confidence intervals for differences, Cohen's d, assumptions, Mann-Whitney and Wilcoxon
terms:
- **t-test:** a test comparing means using the t distribution.
- **t statistic:** a difference divided by its standard error.
- **One-sample t-test:** compares one group's mean with a fixed value.
- **Welch's t-test:** compares two independent groups without assuming equal spreads.
- **Paired t-test:** compares two measurements on the same subjects, using each subject's difference.
- **Cohen's d:** a difference between means measured in standard deviations.
- **Mann-Whitney U test:** a rank-based alternative to the two-sample t-test.
- **Wilcoxon signed-rank test:** a rank-based alternative to the paired t-test.
mistakes:
- Using an unpaired test on paired data, which wastes the pairing and loses power.
- Reporting only the p-value. Give the difference and its confidence interval too.
- Using t-tests on tiny, very skewed samples. Switch to a rank-based test.

@@ errors-and-power
topics: Type I and II errors, α and β, power, simulating false alarms and power, sample size calculations, multiple testing, Bonferroni
terms:
- **Type I error:** a false alarm: rejecting H₀ when it's true.
- **Type II error:** a miss: failing to reject H₀ when there is a real effect.
- **β (beta):** the probability of a Type II error.
- **Power:** the probability of detecting a real effect, 1 − β; 80% is a common target.
- **Minimum detectable effect:** the smallest effect a study is designed to detect.
- **Multiple testing:** running many tests, which makes some false alarms likely.
- **p-hacking:** trying analyses until something comes out significant.
- **Bonferroni correction:** dividing α by the number of tests.
mistakes:
- Running a study without working out the sample size, then calling a missed effect "no effect".
- Testing many slices of the data and reporting only the significant one.
- Stopping an experiment the moment p dips below 0.05, which inflates false alarms.

@@ chi-square
topics: observed vs expected counts, the χ² statistic, goodness-of-fit tests, tests of independence, expected frequencies, Cramér's V, Fisher's exact test
terms:
- **Chi-square (χ²) test:** a test comparing observed counts with the counts expected under H₀.
- **Observed count:** how many cases actually fell in a category.
- **Expected count:** how many would fall there if H₀ were true.
- **Goodness-of-fit test:** tests whether counts match a claimed distribution.
- **Test of independence:** tests whether two categorical variables are related.
- **Degrees of freedom (chi-square):** (rows − 1) × (columns − 1) for a two-way table.
- **Cramér's V:** the strength of association between two categorical variables, from 0 to 1.
- **Fisher's exact test:** an exact test for 2 × 2 tables with small counts.
mistakes:
- Feeding percentages instead of counts into the test.
- Ignoring small expected counts (below about 5).
- Reading a significant result as a strong relationship. Check Cramér's V.

@@ anova
topics: one-way ANOVA, between- and within-group variation, the F statistic, `f_oneway`, Tukey's HSD, Kruskal-Wallis, eta squared
terms:
- **ANOVA (analysis of variance):** a test of whether three or more group means are all equal.
- **Between-group variation:** how far the group means are from the overall mean.
- **Within-group variation:** how spread out values are inside each group.
- **F statistic:** the ratio of between-group to within-group variation.
- **Post-hoc test:** a follow-up test that finds which groups differ.
- **Tukey's HSD:** a post-hoc test comparing every pair while controlling false alarms.
- **Kruskal-Wallis test:** a rank-based alternative to one-way ANOVA.
- **Eta squared (η²):** the share of total variation explained by the groups.
mistakes:
- Running every pairwise t-test instead of ANOVA plus a post-hoc test.
- Concluding all groups differ from a significant ANOVA.
- Using ANOVA on strongly skewed data with small groups. Use Kruskal-Wallis.
