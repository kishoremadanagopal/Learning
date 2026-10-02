@@ probability-basics
topics: probability as a fraction and a long-run share, law of large numbers, complement, addition and multiplication rules, independence, counting
terms:
- **Probability:** a number from 0 (impossible) to 1 (certain) for how likely something is.
- **Outcome:** one possible result of a random process, like rolling a 4.
- **Event:** a set of outcomes, like "an even number".
- **Law of large numbers:** with more repetitions, the observed share gets closer to the true probability.
- **Complement:** "not A"; P(not A) = 1 − P(A).
- **Independent events:** events where one happening doesn't change the chance of the other.
- **Simulation:** estimating a probability by imitating the random process many times.
- **Combination / permutation:** the number of ways to choose items without order / to arrange them in order.
mistakes:
- Multiplying probabilities of events that aren't independent.
- Adding probabilities for "A or B" without subtracting the overlap.
- The gambler's fallacy: thinking heads is "due" after many tails. Independent flips have no memory.

@@ conditional-probability
topics: P(A | B), conditioning by filtering, independence, P(A | B) vs P(B | A), Bayes' rule, base rates, false positives
terms:
- **Conditional probability:** the probability of A given that B happened, written P(A | B).
- **Joint probability:** the probability that A and B both happen.
- **Bayes' rule:** P(A | B) = P(B | A) × P(A) / P(B), used to reverse a conditional probability.
- **Prior (base rate):** the probability before seeing new evidence, like how common a disease is.
- **Posterior:** the updated probability after seeing the evidence.
- **False positive:** a test or model saying "yes" when the truth is "no".
- **False negative:** saying "no" when the truth is "yes".
- **Precision:** of everything flagged as positive, the share that really is.
mistakes:
- Confusing P(A | B) with P(B | A), the "prosecutor's fallacy".
- Ignoring the base rate. A 95%-accurate test for a rare condition still gives mostly false alarms.
- Dividing by the wrong total: "given B" means divide by the count of B.

@@ discrete-distributions
topics: random variables, expected value, the binomial distribution, pmf, cdf and sf, the Poisson distribution, simulating with rvs
terms:
- **Random variable:** a number produced by a random process.
- **Discrete:** taking separate, countable values like 0, 1, 2.
- **Expected value:** the long-run average of a random variable: each value times its probability, summed.
- **Binomial distribution:** the number of successes in n independent tries with success probability p.
- **Poisson distribution:** the number of events in a fixed interval when they happen at a steady average rate λ.
- **pmf (probability mass function):** P(X = k) for a discrete variable.
- **cdf (cumulative distribution function):** P(X ≤ k).
- **sf (survival function):** P(X > k) = 1 − cdf.
mistakes:
- Off-by-one errors: "at least 30" is `sf(29)`, not `sf(30)`, because `sf(k)` means "more than k".
- Using the binomial when tries aren't independent or the probability changes between them.
- Expecting the expected value to be a possible outcome (a dice's is 3.5).

@@ normal-distribution
topics: the bell curve, μ and σ, the 68-95-99.7 rule, areas with `norm.cdf` and `norm.sf`, percentiles with `norm.ppf`, the standard normal, checking normality
terms:
- **Normal distribution:** the symmetric bell-shaped distribution set by its mean μ and standard deviation σ.
- **Continuous:** able to take any value in a range.
- **pdf (probability density function):** the height of the curve; probabilities are areas under it.
- **68-95-99.7 rule:** the share of normal values within 1, 2 and 3 standard deviations of the mean.
- **Standard normal:** the normal distribution with mean 0 and std 1.
- **ppf (percent point function):** the value with a given area to its left; the inverse of the cdf.
- **1.96:** the z-value with 2.5% of the standard normal beyond it; ±1.96 holds the middle 95%.
- **Normality test:** a test (like Shapiro-Wilk) of whether data could come from a normal distribution.
mistakes:
- Assuming everything is normal. Incomes, waiting times and counts usually aren't; look at a histogram.
- Using `cdf` for "greater than". The right tail is `sf` (or 1 − cdf).
- Passing the variance instead of the standard deviation to `stats.norm`.
