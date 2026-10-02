"""Draw the lesson charts for Statistics with Python into figures/*.svg (deterministic).

Run: python figures.py
Each chart illustrates one idea; lessons include them with ![alt text](figures/name.svg).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
DATA = ROOT / "data"

TEAL, ORANGE, BLUE, RED, GREY, INK = "#0f766e", "#e8730c", "#2c679c", "#c2410c", "#9aa5b1", "#1f2933"
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"], "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold",
    "axes.titlesize": 12.5, "axes.edgecolor": "#52606d", "axes.labelcolor": INK,
    "xtick.color": "#52606d", "ytick.color": "#52606d", "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white", "svg.hashsalt": "statistics-course",
})
FIGS = {}


def fig(name):
    def deco(f):
        FIGS[name] = f
        return f
    return deco


def save(f, name):
    f.tight_layout()
    f.savefig(OUT / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(f)


# ---------------------------------------------------------------- Part 1: describing data

@fig("population-sample")
def _():
    rng = np.random.default_rng(3)
    f, ax = plt.subplots(figsize=(7, 3.2))
    xy = rng.random((400, 2)) * [10, 4]
    pick = rng.choice(400, 30, replace=False)
    ax.scatter(xy[:, 0], xy[:, 1], s=18, color=GREY, alpha=0.6, label="population: everyone (400)")
    ax.scatter(xy[pick, 0], xy[pick, 1], s=46, color=ORANGE, edgecolor=INK, linewidth=0.6, label="sample: the 30 you measure")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("We measure a sample to learn about the population")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, frameon=False)
    return f


@fig("mean-median-skew")
def _():
    rng = np.random.default_rng(5)
    incomes = np.concatenate([rng.lognormal(10.6, 0.45, 950), rng.lognormal(12.3, 0.4, 50)]) / 1000
    f, ax = plt.subplots(figsize=(7, 3.4))
    ax.hist(incomes, bins=60, range=(0, 250), color=TEAL, alpha=0.8, edgecolor="white")
    med, mean = np.median(incomes), incomes.mean()
    ax.axvline(med, color=INK, linewidth=2, label=f"median ≈ {med:.0f}k")
    ax.axvline(mean, color=ORANGE, linewidth=2, linestyle="--", label=f"mean ≈ {mean:.0f}k")
    ax.set_title("A few huge incomes pull the mean to the right of the median")
    ax.set_xlabel("Yearly income (thousands)"); ax.set_ylabel("People")
    ax.legend(frameon=False)
    return f


@fig("same-mean-different-spread")
def _():
    x = np.linspace(20, 100, 400)
    f, ax = plt.subplots(figsize=(7, 3.2))
    for sd, c, lab in [(5, TEAL, "class A: std 5 (consistent)"), (15, ORANGE, "class B: std 15 (spread out)")]:
        ax.plot(x, stats.norm.pdf(x, 60, sd), color=c, linewidth=2.5, label=lab)
        ax.fill_between(x, stats.norm.pdf(x, 60, sd), color=c, alpha=0.15)
    ax.axvline(60, color=INK, linestyle=":", label="both have mean 60")
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Exam score"); ax.set_title("Same average, very different spread")
    ax.legend(frameon=False, loc="upper right")
    return f


@fig("boxplot-anatomy")
def _():
    rng = np.random.default_rng(8)
    data = np.concatenate([rng.normal(60, 10, 200), [98, 104, 18]])
    q1, med, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1
    lo = data[data >= q1 - 1.5 * iqr].min(); hi = data[data <= q3 + 1.5 * iqr].max()
    f, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.boxplot(data, orientation="horizontal", widths=0.5, patch_artist=True,
               boxprops=dict(facecolor="#dcf1ee", edgecolor=TEAL, linewidth=1.8),
               medianprops=dict(color=ORANGE, linewidth=2.5), whiskerprops=dict(color=TEAL, linewidth=1.5),
               capprops=dict(color=TEAL, linewidth=1.5), flierprops=dict(marker="o", markerfacecolor=RED, markeredgecolor=RED))
    labels = [(q1, "Q1 (25%)", 1.27, "right"), (med, "median", 1.38, "center"), (q3, "Q3 (75%)", 1.27, "left"),
              (lo, "lowest typical", 1.27, "center"), (hi, "highest typical", 1.27, "center")]
    for v, t, yy, ha in labels:
        ax.annotate(t, (v, yy), ha=ha, fontsize=10, color=INK)
    ax.annotate("outliers", (data.max(), 0.72), ha="center", color=RED, fontsize=10)
    ax.annotate("", xy=(q1, 0.62), xytext=(q3, 0.62), arrowprops=dict(arrowstyle="<->", color=INK))
    ax.text((q1 + q3) / 2, 0.52, "IQR: the middle 50%", ha="center", fontsize=10)
    ax.set_ylim(0.4, 1.5); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Value"); ax.set_title("How to read a box plot")
    return f


@fig("distribution-shapes")
def _():
    rng = np.random.default_rng(2)
    sets = [("Symmetric", rng.normal(50, 10, 3000), TEAL), ("Right-skewed (long right tail)", rng.gamma(2, 8, 3000), ORANGE),
            ("Left-skewed (long left tail)", 100 - rng.gamma(2, 8, 3000), BLUE)]
    f, axes = plt.subplots(1, 3, figsize=(10, 2.9))
    for ax, (t, d, c) in zip(axes, sets):
        ax.hist(d, bins=35, color=c, alpha=0.85, edgecolor="white")
        ax.axvline(np.mean(d), color=INK, linestyle="--", linewidth=1.5)
        ax.axvline(np.median(d), color=INK, linewidth=1.5)
        ax.set_title(t, fontsize=11); ax.set_yticks([])
    axes[0].text(0.02, 0.92, "solid = median\ndashed = mean", transform=axes[0].transAxes, fontsize=9, va="top")
    return f


@fig("z-scores")
def _():
    x = np.linspace(-3.6, 3.6, 400)
    f, ax = plt.subplots(figsize=(7, 3.0))
    ax.plot(x, stats.norm.pdf(x), color=TEAL, linewidth=2.5)
    for z, lab, dx in [(-2, "z = -2\nunusually low", -0.55), (0, "z = 0\nexactly average", 0), (1.5, "z = 1.5\n1.5 std above", 0.75)]:
        ax.vlines(z, 0, stats.norm.pdf(z), color=ORANGE, linewidth=2)
        ax.annotate(lab, (z + dx, stats.norm.pdf(z) + 0.03), ha="center", fontsize=10)
    ax.set_xticks(range(-3, 4)); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_ylim(0, 0.52)
    ax.set_xlabel("z-score: how many standard deviations from the mean")
    ax.set_title("A z-score puts any value on a common scale")
    return f


@fig("bar-vs-pie")
def _():
    labels = ["Consumer", "Business", "Student"]
    vals = [55, 30, 15]
    f, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.3))
    a1.pie(vals, labels=labels, colors=[TEAL, ORANGE, BLUE], startangle=90, wedgeprops=dict(edgecolor="white"),
           autopct="%d%%", textprops=dict(color="white", fontsize=10))
    for t in a1.texts[::2]:
        t.set_color(INK)
    a1.set_title("Pie: fine for 2-3 parts of a whole")
    a2.barh(labels[::-1], vals[::-1], color=[BLUE, ORANGE, TEAL])
    for i, v in enumerate(vals[::-1]):
        a2.text(v + 1, i, f"{v}%", va="center")
    a2.set_xlim(0, 65); a2.set_title("Bar: easier to compare exactly")
    a2.set_xlabel("Share of customers (%)")
    return f


@fig("stacked-bar")
def _():
    c = pd.read_csv(DATA / "customers.csv")
    t = pd.crosstab(c["city"], c["segment"], normalize="index") * 100
    t = t.loc[t["Business"].sort_values().index]
    f, ax = plt.subplots(figsize=(7, 3.4))
    left = np.zeros(len(t))
    for col, colr in zip(["Business", "Consumer", "Student"], [ORANGE, TEAL, BLUE]):
        ax.barh(t.index, t[col], left=left, color=colr, label=col, edgecolor="white")
        left += t[col].values
    ax.set_xlabel("Share of each city's customers (%)"); ax.set_xlim(0, 100)
    ax.set_title("A two-way table as a 100% stacked bar")
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    return f


# ---------------------------------------------------------------- Part 2: probability

@fig("law-of-large-numbers")
def _():
    rng = np.random.default_rng(11)
    f, ax = plt.subplots(figsize=(7, 3.3))
    for k, c in zip(range(3), [TEAL, ORANGE, BLUE]):
        flips = rng.integers(0, 2, 2000)
        ax.plot(np.arange(1, 2001), flips.cumsum() / np.arange(1, 2001), color=c, linewidth=1.6, alpha=0.9)
    ax.axhline(0.5, color=INK, linestyle="--", label="true probability 0.5")
    ax.set_xscale("log"); ax.set_ylim(0, 1)
    ax.set_xlabel("Number of coin flips (log scale)"); ax.set_ylabel("Share of heads so far")
    ax.set_title("With more tries, the share settles on the true probability")
    ax.legend(frameon=False)
    return f


@fig("medical-test")
def _():
    f, ax = plt.subplots(figsize=(7, 3.6))
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.99, color="#e4e7eb"))
    ax.add_patch(plt.Rectangle((0, 0.99), 1, 0.01 * 6, color=RED))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.08)
    ax.axis("off")
    ax.text(0.5, 0.5, "9,900 healthy people\n5% test positive anyway → 495 false alarms", ha="center", va="center", fontsize=11)
    ax.text(0.5, 1.02, "100 sick people: 90 test positive", ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    ax.set_title("10,000 people, 1% sick. A positive test is right only 90 / (90 + 495) ≈ 15% of the time", fontsize=11)
    return f


@fig("binomial")
def _():
    f, axes = plt.subplots(1, 2, figsize=(9, 3.0), sharey=True)
    k = np.arange(0, 11)
    for ax, p, c in [(axes[0], 0.5, TEAL), (axes[1], 0.2, ORANGE)]:
        ax.bar(k, stats.binom.pmf(k, 10, p), color=c, edgecolor="white")
        ax.set_title(f"Heads in 10 flips, p = {p}"); ax.set_xticks(k); ax.set_xlabel("successes")
    axes[0].set_ylabel("probability")
    return f


@fig("poisson")
def _():
    k = np.arange(0, 16)
    f, ax = plt.subplots(figsize=(7, 3.0))
    ax.bar(k, stats.poisson.pmf(k, 4), color=BLUE, edgecolor="white")
    ax.set_xticks(k); ax.set_xlabel("customers arriving in one hour"); ax.set_ylabel("probability")
    ax.set_title("Poisson: counts of events when 4 happen on average")
    return f


@fig("normal-68-95")
def _():
    x = np.linspace(-4, 4, 600)
    y = stats.norm.pdf(x)
    f, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.plot(x, y, color=INK, linewidth=2)
    for k, c, a in [(3, BLUE, 0.15), (2, ORANGE, 0.25), (1, TEAL, 0.45)]:
        m = (x >= -k) & (x <= k)
        ax.fill_between(x[m], y[m], color=c, alpha=a)
    for k, pct, h in [(1, "68%", 0.27), (2, "95%", 0.16), (3, "99.7%", 0.05)]:
        ax.annotate("", xy=(-k, h), xytext=(k, h), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
        ax.text(0, h + 0.012, pct, ha="center", fontsize=10.5, fontweight="bold")
    ax.set_xticks(range(-3, 4)); ax.set_xticklabels(["-3σ", "-2σ", "-1σ", "mean", "+1σ", "+2σ", "+3σ"])
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_title("The normal curve: 68% within 1 std, 95% within 2, 99.7% within 3")
    return f


@fig("normal-cdf")
def _():
    x = np.linspace(130, 210, 500)
    y = stats.norm.pdf(x, 170, 8)
    f, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(x, y, color=INK, linewidth=2)
    m = x <= 180
    ax.fill_between(x[m], y[m], color=TEAL, alpha=0.4)
    ax.text(142, 0.028, f"P(height ≤ 180)\n= norm.cdf(180, 170, 8)\n= {stats.norm.cdf(180, 170, 8):.3f}", ha="center", va="bottom", fontsize=10)
    ax.annotate("", xy=(163, 0.02), xytext=(150, 0.027), arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
    ax.axvline(180, color=ORANGE, linewidth=2)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Height (cm), mean 170, std 8")
    ax.set_title("cdf = the area to the left of a value")
    return f


# ---------------------------------------------------------------- Part 3: sampling and estimation

@fig("sampling-bias")
def _():
    rng = np.random.default_rng(4)
    true = 34
    random_means = [rng.normal(true, 6, 25).mean() for _ in range(40)]
    biased_means = [rng.normal(true + 7, 4, 25).mean() for _ in range(40)]
    f, ax = plt.subplots(figsize=(7, 2.8))
    ax.scatter(random_means, np.full(40, 1) + rng.normal(0, 0.05, 40), color=TEAL, alpha=0.8, label="random samples")
    ax.scatter(biased_means, np.full(40, 0) + rng.normal(0, 0.05, 40), color=ORANGE, alpha=0.8, label="biased samples (e.g. only online)")
    ax.axvline(true, color=INK, linestyle="--")
    ax.text(true + 0.15, 1.45, "true average", ha="left")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["biased", "random"]); ax.set_ylim(-0.5, 1.7)
    ax.set_xlabel("average age found by each sample of 25")
    ax.set_title("A biased sample misses in the same direction every time")
    return f


@fig("clt")
def _():
    rng = np.random.default_rng(9)
    pop = rng.exponential(10, 200_000)
    f, axes = plt.subplots(1, 4, figsize=(11, 2.8))
    axes[0].hist(pop, bins=60, range=(0, 60), color=GREY, edgecolor="white")
    axes[0].set_title("Population (skewed)", fontsize=10.5)
    for ax, n, c in zip(axes[1:], [2, 10, 40], [ORANGE, BLUE, TEAL]):
        means = rng.choice(pop, (5000, n)).mean(axis=1)
        ax.hist(means, bins=40, color=c, edgecolor="white")
        ax.set_title(f"Averages of samples of {n}", fontsize=10.5)
        ax.set_xlim(0, 30)
    for ax in axes:
        ax.set_yticks([])
    f.suptitle("Central limit theorem: sample averages become bell-shaped", fontweight="bold", fontsize=12)
    return f


@fig("confidence-intervals")
def _():
    rng = np.random.default_rng(21)
    true, sd, n = 50, 12, 30
    f, ax = plt.subplots(figsize=(7, 4.2))
    misses = 0
    for i in range(50):
        s = rng.normal(true, sd, n)
        lo, hi = stats.t.interval(0.95, n - 1, loc=s.mean(), scale=stats.sem(s))
        hit = lo <= true <= hi
        misses += not hit
        ax.plot([lo, hi], [i, i], color=TEAL if hit else RED, linewidth=2 if hit else 2.8)
        ax.plot(s.mean(), i, "o", color=TEAL if hit else RED, markersize=3)
    ax.axvline(true, color=INK, linestyle="--")
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("95% confidence interval for the mean, from 50 different samples")
    ax.set_title(f"About 95% of intervals catch the true mean ({50 - misses} of 50 here)")
    return f


@fig("bootstrap")
def _():
    s = pd.read_csv(DATA / "students.csv")["math"].to_numpy()
    rng = np.random.default_rng(1)
    boots = np.array([rng.choice(s, len(s)).mean() for _ in range(5000)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    f, ax = plt.subplots(figsize=(7, 3.2))
    ax.hist(boots, bins=50, color=TEAL, alpha=0.8, edgecolor="white")
    for v in (lo, hi):
        ax.axvline(v, color=ORANGE, linewidth=2)
    top = ax.get_ylim()[1]
    ax.set_ylim(0, top * 1.25)
    ax.text((lo + hi) / 2, top * 1.08, f"95% interval: {lo:.1f} to {hi:.1f}", ha="center", color=ORANGE, fontweight="bold")
    ax.set_xlabel("average math score in each of 5,000 resamples"); ax.set_yticks([])
    ax.set_title("Bootstrap: resample your own data to see how much the mean wobbles")
    return f


# ---------------------------------------------------------------- Part 4: testing

@fig("p-value")
def _():
    x = np.linspace(-4, 4, 600)
    y = stats.norm.pdf(x)
    obs = 2.1
    f, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.plot(x, y, color=INK, linewidth=2)
    for m in (x >= obs, x <= -obs):
        ax.fill_between(x[m], y[m], color=RED, alpha=0.5)
    ax.axvline(obs, color=ORANGE, linewidth=2)
    ax.text(obs + 0.1, 0.25, "what we\nobserved", color=ORANGE)
    ax.text(0, 0.12, "results we'd expect\nif nothing is going on\n(the null hypothesis)", ha="center", fontsize=10)
    ax.text(3.0, 0.05, f"p = {2 * stats.norm.sf(obs):.3f}\n(both red tails)", ha="center", color=RED)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xlabel("test statistic")
    ax.set_title("The p-value: how surprising our result is if the null is true")
    return f


@fig("before-after")
def _():
    t = pd.read_csv(DATA / "training.csv")
    f, ax = plt.subplots(figsize=(5.5, 3.8))
    for _, r in t.iterrows():
        c = TEAL if r["after"] > r["before"] else (RED if r["after"] < r["before"] else GREY)
        ax.plot([0, 1], [r["before"], r["after"]], color=c, alpha=0.7, marker="o", markersize=4)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["before training", "after training"]); ax.set_xlim(-0.3, 1.3)
    ax.set_ylabel("test score")
    ax.set_title("Paired data: each line is one person")
    return f


@fig("t-vs-normal")
def _():
    x = np.linspace(-4.5, 4.5, 500)
    f, ax = plt.subplots(figsize=(7, 3.0))
    ax.plot(x, stats.norm.pdf(x), color=INK, linewidth=2, label="normal")
    for d, c in [(2, ORANGE), (5, BLUE), (30, TEAL)]:
        ax.plot(x, stats.t.pdf(x, d), color=c, linewidth=1.8, linestyle="--", label=f"t, {d} degrees of freedom")
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_title("Small samples use the t distribution: fatter tails, more caution")
    ax.legend(frameon=False, fontsize=9.5)
    return f


@fig("errors-power")
def _():
    x = np.linspace(-4, 7, 700)
    h0, h1 = stats.norm.pdf(x, 0, 1), stats.norm.pdf(x, 2.5, 1)
    crit = stats.norm.ppf(0.95)
    f, ax = plt.subplots(figsize=(7.6, 3.4))
    ax.plot(x, h0, color=INK, linewidth=2, label="if there's no effect (null)")
    ax.plot(x, h1, color=TEAL, linewidth=2, label="if the effect is real")
    ax.fill_between(x[x >= crit], h0[x >= crit], color=RED, alpha=0.5, label="α: false alarm (Type I)")
    ax.fill_between(x[x <= crit], h1[x <= crit], color=GREY, alpha=0.5, label="β: missed effect (Type II)")
    ax.fill_between(x[x >= crit], h1[x >= crit], color=TEAL, alpha=0.18, label=f"power = {stats.norm.sf(crit, 2.5):.0%}")
    ax.axvline(crit, color=ORANGE, linewidth=2)
    ax.text(crit + 0.05, 0.42, "decision line", color=ORANGE)
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 0.47)
    ax.set_title("Two ways to be wrong, and power: the chance of catching a real effect")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    return f


@fig("observed-expected")
def _():
    sides = ["1", "2", "3", "4", "5", "6"]
    obs = [8, 9, 10, 7, 9, 17]
    exp = [sum(obs) / 6] * 6
    xi = np.arange(6)
    f, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(xi - 0.2, obs, width=0.4, color=TEAL, label="observed")
    ax.bar(xi + 0.2, exp, width=0.4, color=GREY, label="expected if fair")
    ax.set_xticks(xi); ax.set_xticklabels(sides); ax.set_xlabel("dice face"); ax.set_ylabel("rolls")
    ax.set_title("Chi-square compares observed counts with expected counts")
    ax.legend(frameon=False)
    return f


@fig("anova-classes")
def _():
    s = pd.read_csv(DATA / "students.csv")
    groups = [s.loc[s["class"] == c, "math"] for c in "ABC"]
    f, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.boxplot(groups, tick_labels=["Class A", "Class B", "Class C"], widths=0.45, patch_artist=True,
               boxprops=dict(facecolor="#dcf1ee", edgecolor=TEAL), medianprops=dict(color=ORANGE, linewidth=2))
    rng = np.random.default_rng(0)
    for i, g in enumerate(groups, start=1):
        ax.scatter(i + rng.normal(0, 0.06, len(g)), g, s=12, color=INK, alpha=0.5)
    ax.axhline(s["math"].mean(), color=GREY, linestyle="--", label="overall mean")
    ax.set_ylabel("math score"); ax.legend(frameon=False)
    ax.set_title("ANOVA: are the group means further apart than the spread inside groups?", fontsize=11)
    return f


# ---------------------------------------------------------------- Part 5: relationships

@fig("correlation-gallery")
def _():
    rng = np.random.default_rng(6)
    f, axes = plt.subplots(1, 5, figsize=(11.5, 2.5))
    for ax, r in zip(axes[:4], [-0.9, -0.4, 0.4, 0.9]):
        xy = rng.multivariate_normal([0, 0], [[1, r], [r, 1]], 150)
        ax.scatter(xy[:, 0], xy[:, 1], s=8, color=TEAL if r > 0 else ORANGE, alpha=0.7)
        ax.set_title(f"r = {r}", fontsize=11)
    x = np.linspace(-2, 2, 150)
    y = x ** 2 + rng.normal(0, 0.25, 150)
    axes[4].scatter(x, y, s=8, color=RED, alpha=0.7)
    axes[4].set_title(f"r ≈ {np.corrcoef(x, y)[0, 1]:.1f}, yet related!", fontsize=11)
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
    f.suptitle("Correlation measures straight-line relationships only", fontweight="bold", fontsize=12)
    return f


@fig("regression-line")
def _():
    s = pd.read_csv(DATA / "students.csv")
    res = stats.linregress(s["hours_studied"], s["math"])
    f, ax = plt.subplots(figsize=(7, 3.8))
    pred = res.intercept + res.slope * s["hours_studied"]
    for x, y, p in zip(s["hours_studied"], s["math"], pred):
        ax.plot([x, x], [y, p], color=GREY, linewidth=1)
    ax.scatter(s["hours_studied"], s["math"], color=TEAL, s=22, zorder=3, label="students")
    xs = np.linspace(0, 14, 50)
    ax.plot(xs, res.intercept + res.slope * xs, color=ORANGE, linewidth=2.5,
            label=f"math ≈ {res.intercept:.1f} + {res.slope:.2f} × hours")
    ax.set_xlabel("hours studied per week"); ax.set_ylabel("math score")
    ax.set_title("Least squares: the line that makes the grey gaps (residuals) smallest")
    ax.legend(frameon=False, loc="upper left")
    return f


@fig("residual-plot")
def _():
    import statsmodels.formula.api as smf
    h = pd.read_csv(DATA / "housing.csv")
    m = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=h).fit()
    f, ax = plt.subplots(figsize=(7, 3.2))
    ax.scatter(m.fittedvalues, m.resid, color=TEAL, s=16, alpha=0.8)
    ax.axhline(0, color=ORANGE, linewidth=2)
    ax.set_xlabel("predicted price (thousands)"); ax.set_ylabel("residual (actual − predicted)")
    ax.set_title("A healthy residual plot: a shapeless cloud around zero")
    return f


@fig("coefficients")
def _():
    import statsmodels.formula.api as smf
    h = pd.read_csv(DATA / "housing.csv")
    m = smf.ols("price_k ~ area_sqm + bedrooms + age_years + distance_km + C(neighborhood)", data=h).fit()
    ci = m.conf_int().drop("Intercept")
    est = m.params.drop("Intercept")
    names = {"C(neighborhood)[T.Hillside]": "Hillside (vs Central)", "C(neighborhood)[T.Riverside]": "Riverside (vs Central)",
             "area_sqm": "per extra m²", "bedrooms": "per extra bedroom", "age_years": "per year of age", "distance_km": "per km from centre"}
    order = est.sort_values().index
    f, ax = plt.subplots(figsize=(7, 3.4))
    yi = np.arange(len(order))
    ax.errorbar(est[order], yi, xerr=[est[order] - ci.loc[order, 0], ci.loc[order, 1] - est[order]], fmt="o",
                color=TEAL, ecolor=TEAL, capsize=4)
    ax.axvline(0, color=GREY, linestyle="--")
    ax.set_yticks(yi); ax.set_yticklabels([names[k] for k in order])
    ax.set_xlabel("change in price (thousands), with 95% confidence interval")
    ax.set_title("Each coefficient: the effect of one thing, holding the others fixed", fontsize=11.5)
    return f


# ---------------------------------------------------------------- Part 6: at work

@fig("ab-test-result")
def _():
    a = pd.read_csv(DATA / "ab_test.csv")
    g = a.groupby("group")["converted"].agg(["mean", "count"])
    se = np.sqrt(g["mean"] * (1 - g["mean"]) / g["count"])
    f, ax = plt.subplots(figsize=(5.8, 3.4))
    ax.bar(g.index, g["mean"] * 100, color=[GREY, TEAL], width=0.55)
    ax.errorbar(g.index, g["mean"] * 100, yerr=1.96 * se * 100, fmt="none", ecolor=INK, capsize=8, linewidth=1.5)
    for i, v in enumerate(g["mean"] * 100):
        ax.text(i, v / 2, f"{v:.1f}%", ha="center", color="white", fontweight="bold")
    ax.set_ylabel("conversion rate (%)"); ax.set_xticks([0, 1]); ax.set_xticklabels(["page A (old)", "page B (new)"])
    ax.set_title("A/B test: rates with 95% intervals")
    return f


def main():
    OUT.mkdir(exist_ok=True)
    for name, make in FIGS.items():
        save(make(), name)
    print(f"{len(FIGS)} figures written to {OUT}")


if __name__ == "__main__":
    main()
