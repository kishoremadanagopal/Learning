"""Draw the lesson charts and diagrams for Machine Learning with scikit-learn into figures/*.svg (deterministic).

Run: python figures.py            (all figures)
     python figures.py sigmoid     (one figure)
Each picture illustrates one idea; lessons include them with ![alt text](figures/name.svg).
Palette (validated for colour-blind separation): blue, orange, teal, crimson, purple; text stays in ink.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.colors import ListedColormap

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT.parents[1] / "tools"))
import diag  # noqa: E402
from diag import arrow, box, label, table  # noqa: E402

BLUE, ORANGE, TEAL, CRIMSON, PURPLE = "#1f6fb2", "#e07b00", "#159a7f", "#b42357", "#7a5ac8"
GREY, INK, MUTED = "#9aa5b1", "#1f2933", "#52606d"
SOFT = {BLUE: "#e3eef8", ORANGE: "#fdecd6", TEAL: "#dcf3ee", CRIMSON: "#f8e1e8", PURPLE: "#ece6f8", GREY: "#eef1f4", INK: "#eef1f4"}
FRUIT = {"apple": (CRIMSON, "o"), "orange": (ORANGE, "s"), "lemon": (BLUE, "^")}

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"], "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold",
    "axes.titlesize": 12.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white", "svg.hashsalt": "ml-course",
    "legend.frameon": False,
})
FIGS = {}


def fig(name):
    def deco(f):
        FIGS[name] = f
        return f
    return deco


def save(f, name):
    f.savefig(OUT / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(f)


def sbox(ax, x, y, w, h, text, color=BLUE, **kw):
    """A box filled with the soft version of its colour."""
    box(ax, x, y, w, h, text, color=color, fill=SOFT.get(color, "white"), **kw)


def read(name):
    return pd.read_csv(DATA / name)


def churn_split(cols=("tenure_months", "monthly_charge", "support_calls"), rs=0):
    from sklearn.model_selection import train_test_split
    c = read("churn.csv")
    return train_test_split(c[list(cols)], c["churned"], test_size=0.25, random_state=rs, stratify=c["churned"])


def fruit_scatter(ax, f, x="width_cm", y="height_cm", s=26, legend=True):
    for kind, (col, mk) in FRUIT.items():
        rows = f[f["fruit"] == kind]
        ax.scatter(rows[x], rows[y], s=s, color=col, marker=mk, edgecolor="white", linewidth=0.6, label=kind, zorder=3)
    if legend:
        ax.legend(loc="upper right", fontsize=9.5, handletextpad=0.3)


# ---------------------------------------------------------------- Part 1

@fig("rules-vs-learning")
def rules_vs_learning():
    f, ax = diag.canvas(10, 3.6)
    for y, title, ins, mid, out, mcol in [
        (2.55, "Traditional programming", ("rules", "data"), "program", "answers", GREY),
        (0.75, "Machine learning", ("data", "answers"), "training", "rules\n(a model)", BLUE),
    ]:
        label(ax, 0.1, y + 0.72, title, ha="left", bold=True, size=11.5)
        sbox(ax, 0.2, y - 0.05, 1.5, 0.5, ins[0], color=GREY)
        label(ax, 1.95, y + 0.2, "+", size=14, bold=True)
        sbox(ax, 2.2, y - 0.05, 1.5, 0.5, ins[1], color=ORANGE if ins[1] == "answers" else GREY)
        arrow(ax, 3.85, y + 0.2, 4.75, y + 0.2)
        sbox(ax, 4.85, y - 0.1, 1.9, 0.6, mid, color=mcol, bold=True)
        arrow(ax, 6.9, y + 0.2, 7.8, y + 0.2)
        sbox(ax, 7.9, y - 0.15, 1.9, 0.7, out, color=BLUE if mid == "training" else GREY, bold=mid == "training")
    label(ax, 5.0, 0.12, "You give examples with the right answers; training works out the rule.", size=10, color=MUTED)
    return f


@fig("ml-types")
def ml_types():
    f, ax = diag.canvas(10, 3.9)
    sbox(ax, 3.9, 3.2, 2.2, 0.55, "Machine learning", color=INK, bold=True)
    sbox(ax, 0.9, 2.0, 3.0, 0.65, "Supervised\n(examples come with answers)", color=BLUE, fontsize=10)
    sbox(ax, 6.1, 2.0, 3.0, 0.65, "Unsupervised\n(no answers)", color=TEAL, fontsize=10)
    for x1, x2 in [(5.0, 2.4), (5.0, 7.6)]:
        arrow(ax, x1, 3.2, x2, 2.68, color=MUTED, lw=1.3)
    leaves = [(0.2, "Regression", "predicts a number\nprice, temperature", BLUE),
              (2.55, "Classification", "predicts a category\nspam? which fruit?", BLUE),
              (5.4, "Clustering", "finds groups\ncustomer segments", TEAL),
              (7.75, "Dim. reduction", "many columns → few\na 2-D map of data", TEAL)]
    for x, t, sub, c in leaves:
        sbox(ax, x, 0.45, 2.1, 1.0, "", color=c)
        label(ax, x + 1.05, 1.18, t, bold=True, size=10.5)
        label(ax, x + 1.05, 0.78, sub, size=9, color=MUTED)
    for x1, x2 in [(2.1, 1.25), (2.7, 3.6), (7.3, 6.45), (7.9, 8.8)]:
        arrow(ax, x1, 2.0, x2, 1.48, color=MUTED, lw=1.3)
    return f


@fig("fit-predict")
def fit_predict():
    f, ax = diag.canvas(10, 2.4)
    steps = [("1. create", "model = LinearRegression()", "an empty model", GREY),
             ("2. fit", "model.fit(X, y)", "learns the rule from examples", BLUE),
             ("3. predict", "model.predict(new_X)", "uses the rule on new rows", TEAL)]
    for i, (t, code, sub, c) in enumerate(steps):
        x = 0.1 + i * 3.4
        sbox(ax, x, 0.55, 2.9, 1.45, "", color=c)
        label(ax, x + 1.45, 1.68, t, bold=True, size=11.5)
        label(ax, x + 1.45, 1.22, code, mono=True, size=9.5)
        label(ax, x + 1.45, 0.82, sub, size=9.5, color=MUTED)
        if i < 2:
            arrow(ax, x + 2.95, 1.27, x + 3.35, 1.27)
    label(ax, 5.0, 0.18, "Every scikit-learn model works this way.", size=10, color=MUTED)
    return f


@fig("train-test-split")
def train_test_split_fig():
    f, ax = diag.canvas(10, 2.0)
    ax.add_patch(Rectangle((0.2, 0.85), 7.2, 0.75, facecolor=SOFT[BLUE], edgecolor=BLUE, linewidth=1.6))
    ax.add_patch(Rectangle((7.45, 0.85), 2.35, 0.75, facecolor=SOFT[ORANGE], edgecolor=ORANGE, linewidth=1.6))
    label(ax, 3.8, 1.22, "training set: 112 rows (75%)", bold=True)
    label(ax, 8.62, 1.22, "test set\n38 rows (25%)", bold=True, size=10)
    label(ax, 3.8, 0.55, "the model learns from these: fit()", size=10, color=MUTED)
    label(ax, 8.62, 0.55, "hidden until the end: score()", size=10, color=MUTED)
    label(ax, 5.0, 1.85, "150 fruits, shuffled, then cut in two", size=10.5)
    return f


@fig("ml-workflow")
def ml_workflow():
    f, ax = diag.canvas(12.6, 2.6)
    steps = ["1. Define\nthe question", "2. Get the\ndata", "3. Split\ntrain / test", "4. Prepare\nfeatures",
             "5. Train\nmodels", "6. Evaluate\non unseen data", "7. Deploy\nand monitor"]
    cols = [GREY, GREY, ORANGE, BLUE, BLUE, TEAL, PURPLE]
    for i, (s, c) in enumerate(zip(steps, cols)):
        x = 0.1 + i * 1.8
        sbox(ax, x, 0.9, 1.5, 0.9, s, color=c, fontsize=9.5)
        if i < 6:
            arrow(ax, x + 1.52, 1.35, x + 1.78, 1.35)
    arrow(ax, 0.1 + 5 * 1.8 + 0.75, 0.88, 0.1 + 3 * 1.8 + 0.75, 0.88, color=MUTED, rad=-0.3, lw=1.3)
    label(ax, 0.1 + 4 * 1.8 + 0.75, 0.05, "improve and try again", size=9.5, color=MUTED)
    return f


# ---------------------------------------------------------------- Part 2

def housing_split(rs=5):
    from sklearn.model_selection import train_test_split
    h = read("housing.csv")
    return train_test_split(h[["area_sqm", "bedrooms", "age_years", "distance_km"]], h["price_k"], test_size=0.25, random_state=rs)


@fig("predicted-vs-actual")
def predicted_vs_actual():
    from sklearn.linear_model import LinearRegression
    a, b, c, d = housing_split()
    p = LinearRegression().fit(a, c).predict(b)
    f, ax = plt.subplots(figsize=(5.6, 5.0))
    lo, hi = 150, 650
    ax.plot([lo, hi], [lo, hi], linestyle="--", color=GREY, linewidth=1.5, zorder=1)
    ax.scatter(d, p, s=40, color=BLUE, edgecolor="white", linewidth=0.8, zorder=3)
    ax.text(250, 560, "above the line:\npredicted too high", fontsize=9.5, color=MUTED)
    ax.text(470, 210, "below the line:\npredicted too low", fontsize=9.5, color=MUTED)
    ax.text(590, 625, "perfect", fontsize=9.5, color=MUTED, ha="right")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect("equal")
    ax.set_xlabel("actual price (thousands)"); ax.set_ylabel("predicted price (thousands)")
    ax.set_title("40 test homes: predicted vs actual")
    return f


@fig("residuals")
def residuals():
    rng = np.random.default_rng(4)
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = 2 + 1.1 * x + rng.normal(0, 1.4, 8)
    m, c0 = np.polyfit(x, y, 1)
    f, ax = plt.subplots(figsize=(7, 3.6))
    xs = np.linspace(0.5, 8.5, 2)
    ax.plot(xs, c0 + m * xs, color=ORANGE, linewidth=2.2, label="model's predictions")
    for xi, yi in zip(x, y):
        ax.plot([xi, xi], [yi, c0 + m * xi], color=MUTED, linewidth=1.6, zorder=2)
    ax.scatter(x, y, s=50, color=BLUE, zorder=3, edgecolor="white", label="actual values")
    i = int(np.argmax(np.abs(y - (c0 + m * x))))
    ax.annotate("an error (residual):\nactual − predicted", xy=(x[i] + 0.05, (y[i] + c0 + m * x[i]) / 2), xytext=(x[i] + 0.6, (y[i] + c0 + m * x[i]) / 2 + 2.2),
                fontsize=9.5, arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("feature"); ax.set_ylabel("label")
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_title("MAE averages the lengths of the grey lines; RMSE squares them first")
    return f


def energy_split(rs=1):
    from sklearn.model_selection import train_test_split
    e = read("energy.csv")
    return train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=rs)


def poly(degree, final=None):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from sklearn.linear_model import LinearRegression
    return make_pipeline(PolynomialFeatures(degree), StandardScaler(), final if final is not None else LinearRegression())


@fig("under-over-fit")
def under_over_fit():
    a, b, c, d = energy_split()
    grid = pd.DataFrame({"temperature_c": np.linspace(a["temperature_c"].min(), a["temperature_c"].max(), 400)})
    f, axes = plt.subplots(1, 3, figsize=(12, 3.7), sharey=True)
    for ax, (deg, t) in zip(axes, [(1, "Degree 1: underfit"), (2, "Degree 2: good fit"), (15, "Degree 15: overfit")]):
        m = poly(deg).fit(a, c)
        ax.scatter(a["temperature_c"], c, s=30, color=BLUE, edgecolor="white", zorder=3, label="training days")
        ax.plot(grid["temperature_c"], m.predict(grid), color=ORANGE, linewidth=2.2, label="model")
        ax.set_ylim(150, 600)
        ax.set_title(t)
        ax.set_xlabel("temperature (°C)")
    axes[0].set_ylabel("energy (kWh)")
    axes[0].legend(loc="upper center", fontsize=9)
    f.tight_layout()
    return f


@fig("complexity-curve")
def complexity_curve():
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import root_mean_squared_error
    e = read("energy.csv")
    degrees = list(range(1, 16))
    tr, te = {d: [] for d in degrees}, {d: [] for d in degrees}
    for seed in range(40):
        a, b, c, d = train_test_split(e[["temperature_c"]], e["energy_kwh"], test_size=0.3, random_state=seed)
        for deg in degrees:
            m = poly(deg).fit(a, c)
            tr[deg].append(root_mean_squared_error(c, m.predict(a)))
            te[deg].append(root_mean_squared_error(d, m.predict(b)))
    trm = [np.median(tr[d]) for d in degrees]
    tem = [np.median(te[d]) for d in degrees]
    f, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(degrees, trm, color=BLUE, linewidth=2.2, marker="o", markersize=5, label="training error")
    ax.plot(degrees, tem, color=ORANGE, linewidth=2.2, marker="s", markersize=5, label="test error")
    best = degrees[int(np.argmin(tem))]
    ax.axvline(best, color=GREY, linestyle=":", linewidth=1.5)
    top = min(max(tem) * 1.05, 75)
    ax.set_ylim(0, top)
    ax.text(best + 0.2, top * 0.93, "sweet spot", fontsize=10, color=INK)
    ax.text(1.2, top * 0.08, "underfitting", fontsize=10, color=MUTED)
    ax.text(12.3, top * 0.08, "overfitting", fontsize=10, color=MUTED)
    ax.set_xlabel("model complexity (polynomial degree)")
    ax.set_ylabel("RMSE (median of 40 splits)")
    ax.set_xticks(degrees)
    ax.legend(loc="upper center", fontsize=10)
    ax.set_title("Training error keeps falling; test error turns back up")
    return f


@fig("regularization")
def regularization():
    from sklearn.linear_model import Ridge, LinearRegression, Lasso
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    a, b, c, d = energy_split()
    grid = pd.DataFrame({"temperature_c": np.linspace(a["temperature_c"].min(), a["temperature_c"].max(), 400)})
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
    ax1.scatter(a["temperature_c"], c, s=28, color=GREY, edgecolor="white", zorder=3, label="training days")
    for model, lab, col, ls in [(LinearRegression(), "no penalty", CRIMSON, "-"), (Ridge(alpha=0.1), "Ridge, alpha = 0.1", BLUE, "-"),
                                (Ridge(alpha=100), "Ridge, alpha = 100", ORANGE, "--")]:
        ax1.plot(grid["temperature_c"], poly(15, model).fit(a, c).predict(grid), color=col, linewidth=2.2, linestyle=ls, label=lab)
    ax1.set_ylim(150, 600)
    ax1.set_xlabel("temperature (°C)"); ax1.set_ylabel("energy (kWh)")
    ax1.set_title("Ridge smooths a degree-15 curve")
    ax1.legend(fontsize=9, loc="upper center")
    h = read("housing.csv")
    X = h[["area_sqm", "bedrooms", "age_years", "distance_km"]].copy()
    rng = np.random.default_rng(0)
    for i in range(5):
        X[f"noise_{i}"] = rng.normal(size=len(X)).round(2)
    from sklearn.model_selection import train_test_split
    Xa, _, ya, _ = train_test_split(X, h["price_k"], test_size=0.25, random_state=5)
    alphas = np.logspace(-1, 2, 60)
    coefs = np.array([make_pipeline(StandardScaler(), Lasso(alpha=al)).fit(Xa, ya)[-1].coef_ for al in alphas])
    real = {"area_sqm": BLUE, "bedrooms": TEAL, "age_years": ORANGE, "distance_km": CRIMSON}
    for j, col in enumerate(X.columns):
        if col in real:
            ax2.plot(alphas, coefs[:, j], color=real[col], linewidth=2.2, label=col)
        else:
            ax2.plot(alphas, coefs[:, j], color=GREY, linewidth=1.3, label="5 noise columns" if col == "noise_0" else None)
    ax2.legend(fontsize=9, loc="center left", bbox_to_anchor=(0.02, 0.6))
    ax2.axhline(0, color=INK, linewidth=0.8)
    ax2.set_xscale("log")
    ax2.set_xlabel("Lasso alpha (log scale)"); ax2.set_ylabel("coefficient (scaled features)")
    ax2.set_title("Lasso drops the useless features to 0")
    f.tight_layout()
    return f


# ---------------------------------------------------------------- Part 3

@fig("sigmoid")
def sigmoid():
    from sklearn.linear_model import LogisticRegression
    a, b, c, d = churn_split()
    m = LogisticRegression().fit(a, c)
    t = np.linspace(0, 72, 300)
    grid = pd.DataFrame({"tenure_months": t, "monthly_charge": 50.0, "support_calls": 1})
    p = m.predict_proba(grid)[:, 1]
    rng = np.random.default_rng(0)
    f, ax = plt.subplots(figsize=(8, 4.2))
    ax.scatter(a["tenure_months"], c + rng.uniform(-0.03, 0.03, len(c)), s=9, color=GREY, alpha=0.5, zorder=2, label="real customers (0 = stayed, 1 = left)")
    ax.plot(t, p, color=BLUE, linewidth=2.4, zorder=3, label="model: P(leaves)")
    ax.axhline(0.5, color=ORANGE, linestyle="--", linewidth=1.5)
    ax.text(71, 0.53, "threshold 0.5", ha="right", fontsize=9.5, color=INK)
    ax.set_ylim(-0.08, 1.08)
    ax.set_xlabel("tenure (months as a customer)")
    ax.set_ylabel("probability of leaving")
    ax.set_title("Logistic regression: a score squeezed into a probability")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=9.5)
    return f


@fig("confusion-matrix")
def confusion_matrix_fig():
    f, ax = diag.canvas(7.6, 4.4)
    cells = [((2.2, 1.9), "True negative", "167", "stayed, predicted stay", TEAL),
             ((4.9, 1.9), "False positive", "14", "stayed, predicted leave\n(false alarm)", ORANGE),
             ((2.2, 0.2), "False negative", "46", "left, predicted stay\n(missed)", CRIMSON),
             ((4.9, 0.2), "True positive", "23", "left, predicted leave\n(caught)", BLUE)]
    for (x, y), t, n, sub, col in cells:
        sbox(ax, x, y, 2.6, 1.6, "", color=col)
        label(ax, x + 1.3, y + 1.32, t, bold=True, size=10.5)
        label(ax, x + 1.3, y + 0.85, n, bold=True, size=18)
        label(ax, x + 1.3, y + 0.35, sub, size=9, color=MUTED)
    label(ax, 3.5, 3.75, "predicted: stay (0)", bold=True, size=10)
    label(ax, 6.2, 3.75, "predicted: leave (1)", bold=True, size=10)
    label(ax, 1.95, 2.7, "really\nstayed (0)", bold=True, size=10, ha="right")
    label(ax, 1.95, 1.0, "really\nleft (1)", bold=True, size=10, ha="right")
    return f


@fig("threshold-tradeoff")
def threshold_tradeoff():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import precision_score, recall_score
    a, b, c, d = churn_split()
    pr = LogisticRegression().fit(a, c).predict_proba(b)[:, 1]
    ts = np.round(np.arange(0.05, 0.81, 0.01), 2)
    rec = [recall_score(d, (pr >= t).astype(int)) for t in ts]
    pre = [precision_score(d, (pr >= t).astype(int), zero_division=np.nan) for t in ts]
    f, ax = plt.subplots(figsize=(8, 4.0))
    ax.plot(ts, rec, color=BLUE, linewidth=2.2, label="recall (leavers caught)")
    ax.plot(ts, pre, color=ORANGE, linewidth=2.2, linestyle="--", label="precision (calls that were right)")
    for t, txt in [(0.5, "default 0.5"), (0.3, "0.3")]:
        ax.axvline(t, color=GREY, linestyle=":", linewidth=1.4)
        ax.text(t + 0.01, 1.02, txt, fontsize=9.5, color=INK)
    ax.set_ylim(0, 1.08); ax.set_xlim(0.05, 0.8)
    ax.set_xlabel("threshold: flag a customer if P(leaves) ≥ this")
    ax.set_ylabel("score")
    ax.legend(loc="lower left", fontsize=9.5)
    ax.set_title("Lower threshold: more leavers caught, more false alarms")
    return f


@fig("roc-curve")
def roc_curve_fig():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_curve, roc_auc_score
    a, b, c, d = churn_split()
    pr = LogisticRegression().fit(a, c).predict_proba(b)[:, 1]
    fpr, tpr, _ = roc_curve(d, pr)
    f, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.plot([0, 1], [0, 1], linestyle="--", color=GREY, linewidth=1.5)
    ax.fill_between(fpr, tpr, step="post", color=SOFT[BLUE], zorder=1)
    ax.plot(fpr, tpr, color=BLUE, linewidth=2.2, drawstyle="steps-post", zorder=3)
    ax.text(0.45, 0.32, f"AUC = {roc_auc_score(d, pr):.2f}\n(shaded area)", fontsize=10.5, color=INK)
    ax.text(0.62, 0.52, "random guessing", fontsize=9.5, color=MUTED, rotation=38)
    ax.scatter([0], [1], s=60, color=TEAL, zorder=4, clip_on=False)
    ax.text(0.04, 0.96, "perfect model", fontsize=9.5, color=INK, va="top")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.01); ax.set_aspect("equal")
    ax.set_xlabel("false positive rate (stayers flagged)")
    ax.set_ylabel("true positive rate (leavers caught)")
    ax.set_title("ROC curve of the churn model")
    return f


def fruit_regions(ax, model, f, step=0.02):
    from sklearn.preprocessing import LabelEncoder
    X = f[["width_cm", "height_cm"]]
    model.fit(X, f["fruit"])
    xx, yy = np.meshgrid(np.arange(4.8, 9.8, step), np.arange(5.4, 10.4, step))
    grid = pd.DataFrame({"width_cm": xx.ravel(), "height_cm": yy.ravel()})
    order = list(FRUIT)
    z = pd.Series(model.predict(grid)).map({k: i for i, k in enumerate(order)}).to_numpy().reshape(xx.shape)
    ax.contourf(xx, yy, z, levels=[-0.5, 0.5, 1.5, 2.5], colors=[SOFT[FRUIT[k][0]] for k in order])
    fruit_scatter(ax, f, s=20, legend=False)
    ax.set_xlim(4.8, 9.8); ax.set_ylim(5.4, 10.4)
    ax.set_xlabel("width (cm)")


@fig("knn-neighbours")
def knn_neighbours():
    f_ = read("fruit.csv")
    new = np.array([7.6, 7.3])
    dist = np.sqrt(((f_[["width_cm", "height_cm"]].to_numpy() - new) ** 2).sum(axis=1))
    r = np.sort(dist)[4]
    f, ax = plt.subplots(figsize=(5.8, 5.4))
    fruit_scatter(ax, f_, s=30)
    ax.add_patch(Circle(tuple(new), r + 0.02, fill=False, edgecolor=INK, linewidth=1.5, linestyle="--", zorder=4))
    ax.scatter([new[0]], [new[1]], s=140, color="white", edgecolor=INK, linewidth=2, zorder=5, marker="*")
    near = f_.iloc[np.argsort(dist)[:5]]["fruit"].value_counts()
    txt = ", ".join(f"{n} {k}{'s' if n > 1 else ''}" for k, n in near.items())
    ax.annotate(f"new fruit\n5 nearest: {txt}", xy=(new[0] + 0.1, new[1] + 0.1), xytext=(8.15, 9.25), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.set_xlim(4.8, 9.8); ax.set_ylim(5.4, 10.4); ax.set_aspect("equal")
    ax.set_xlabel("width (cm)"); ax.set_ylabel("height (cm)")
    ax.set_title("k = 5: the five closest fruits vote")
    return f


@fig("knn-boundaries")
def knn_boundaries():
    from sklearn.neighbors import KNeighborsClassifier
    f_ = read("fruit.csv")
    f, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, k in zip(axes, [1, 15]):
        fruit_regions(ax, KNeighborsClassifier(k), f_)
        ax.set_title(f"k = {k}: " + ("jagged, follows single points" if k == 1 else "smooth boundaries"))
        ax.set_aspect("equal")
    axes[0].set_ylabel("height (cm)")
    axes[1].legend(*axes[0].get_legend_handles_labels(), loc="upper right", fontsize=9.5)
    f.tight_layout()
    return f


@fig("decision-tree")
def decision_tree_fig():
    from sklearn.tree import DecisionTreeClassifier
    cols = ["tenure_months", "monthly_charge", "support_calls", "data_gb"]
    a, b, c, d = churn_split(cols)
    t = DecisionTreeClassifier(max_depth=2, random_state=0).fit(a, c).tree_
    names = {0: "tenure", 1: "charge", 2: "support calls", 3: "data"}

    def info(n):
        v = t.value[n][0]
        share = v[1] / v.sum()
        return int(t.n_node_samples[n]), share

    f, ax = diag.canvas(10.5, 4.2)
    L, R = t.children_left[0], t.children_right[0]
    pos = {0: (5.25, 3.3), L: (2.6, 2.05), R: (7.9, 2.05)}
    for node, (x, y) in pos.items():
        n, s = info(node)
        q = f"{names[t.feature[node]]} ≤ {t.threshold[node]:.1f}?"
        sbox(ax, x - 1.35, y - 0.35, 2.7, 0.8, "", color=GREY)
        label(ax, x, y + 0.2, q, bold=True, size=10)
        label(ax, x, y - 0.12, f"{n} customers, {s:.0%} left", size=9, color=MUTED)
    kids = {0: (L, R), L: (t.children_left[L], t.children_right[L]), R: (t.children_left[R], t.children_right[R])}
    leaf_x = {t.children_left[L]: 1.35, t.children_right[L]: 3.85, t.children_left[R]: 6.65, t.children_right[R]: 9.15}
    for node, x in leaf_x.items():
        n, s = info(node)
        col = CRIMSON if s >= 0.5 else TEAL
        sbox(ax, x - 1.05, 0.25, 2.1, 0.8, "", color=col)
        label(ax, x, 0.82, "leaves" if s >= 0.5 else "stays", bold=True, size=10.5)
        label(ax, x, 0.48, f"{n} customers, {s:.0%} left", size=8.5, color=MUTED)
    for parent in (0, L, R):
        px, py = pos[parent]
        for side, child in zip(("yes", "no"), kids[parent]):
            cx, cy = (pos[child] if child in pos else (leaf_x[child], 0.25 + 0.8))
            ty = cy + 0.45 if child in pos else cy
            arrow(ax, px + (-0.6 if side == "yes" else 0.6), py - 0.36, cx, ty, color=MUTED, lw=1.2)
            ax.text((px + cx) / 2 + (-0.25 if side == "yes" else 0.25), (py - 0.36 + ty) / 2, side, fontsize=9, color=INK, ha="center")
    label(ax, 0.1, 3.85, "root", ha="left", size=9.5, color=MUTED, italic=True)
    label(ax, 0.1, 0.05, "leaves", ha="left", size=9.5, color=MUTED, italic=True)
    return f


@fig("tree-boundary")
def tree_boundary():
    from sklearn.tree import DecisionTreeClassifier
    f_ = read("fruit.csv")
    f, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, depth in zip(axes, [3, None]):
        fruit_regions(ax, DecisionTreeClassifier(max_depth=depth, random_state=0), f_, step=0.01)
        ax.set_title("max_depth = 3: a few rectangles" if depth else "no depth limit: tiny boxes around single fruits")
        ax.set_aspect("equal")
    axes[0].set_ylabel("height (cm)")
    axes[1].legend(*axes[0].get_legend_handles_labels(), loc="upper right", fontsize=9.5)
    f.tight_layout()
    return f


def tree_icon(ax, x, y, col, s=0.32):
    """A tiny tree glyph: three nodes in a V."""
    for (x1, y1), (x2, y2) in [((x, y + s), (x - s, y - s * 0.4)), ((x, y + s), (x + s, y - s * 0.4))]:
        ax.plot([x1, x2], [y1, y2], color=col, linewidth=1.5, zorder=3)
    for px, py in [(x, y + s), (x - s, y - s * 0.4), (x + s, y - s * 0.4)]:
        ax.add_patch(Circle((px, py), 0.09, facecolor=col, edgecolor="white", linewidth=0.8, zorder=4))


@fig("ensembles")
def ensembles():
    f, ax = diag.canvas(12, 4.4)
    label(ax, 2.9, 4.15, "Random forest: many trees, averaged", bold=True, size=11.5)
    sbox(ax, 0.2, 1.75, 1.4, 0.8, "training\ndata", color=GREY, fontsize=9.5)
    for i, y in enumerate([3.1, 2.0, 0.9]):
        arrow(ax, 1.65, 2.15, 2.25, y + 0.25, color=MUTED, lw=1.2)
        sbox(ax, 2.3, y, 1.35, 0.5, f"sample {i + 1}", color=GREY, fontsize=9)
        arrow(ax, 3.7, y + 0.25, 4.05, y + 0.25, color=MUTED, lw=1.2)
        tree_icon(ax, 4.45, y + 0.22, BLUE)
        arrow(ax, 4.9, y + 0.25, 5.45, 2.15, color=MUTED, lw=1.2)
    sbox(ax, 5.5, 1.75, 0.9, 0.8, "vote /\naverage", color=BLUE, fontsize=9)
    label(ax, 2.95, 0.45, "each tree sees different rows\nand random features", size=9, color=MUTED)
    ax.plot([6.75, 6.75], [0.3, 4.0], color="#d0d6dd", linewidth=1)
    label(ax, 9.4, 4.15, "Gradient boosting: trees fix earlier mistakes", bold=True, size=11.5)
    xs = [7.25, 8.85, 10.45]
    for i, x in enumerate(xs):
        tree_icon(ax, x + 0.35, 2.85, ORANGE)
        label(ax, x + 0.35, 2.2, f"tree {i + 1}", size=9.5)
        label(ax, x + 0.35, 1.8, ["learns the data", "learns tree 1's\nerrors", "learns what's\nstill wrong"][i], size=8.5, color=MUTED)
        if i < 2:
            arrow(ax, x + 0.8, 2.85, x + 1.5, 2.85, color=MUTED, lw=1.2, text="errors", fontsize=8.5)
    sbox(ax, 8.1, 0.45, 2.6, 0.6, "prediction = tree 1 + tree 2 + tree 3 …", color=ORANGE, fontsize=8.5)
    return f


@fig("feature-importance")
def feature_importance():
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.inspection import permutation_importance
    c = read("churn.csv")
    X = pd.get_dummies(c.drop(columns=["customer_id", "churned"]), dtype=int)
    a, b, cc, d = train_test_split(X, c["churned"], test_size=0.25, random_state=0, stratify=c["churned"])
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0).fit(a, cc)
    pi = permutation_importance(rf, b, d, scoring="roc_auc", n_repeats=10, random_state=0).importances_mean
    df = pd.DataFrame({"built-in": rf.feature_importances_, "permutation": pi}, index=X.columns).sort_values("permutation")
    f, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, col, colour, t in [(axes[0], "built-in", GREY, "Built-in (impurity) importance"), (axes[1], "permutation", BLUE, "Permutation importance on the test set")]:
        ax.barh(df.index, df[col], color=colour, height=0.65)
        ax.set_title(t, fontsize=11.5)
        ax.axvline(0, color=INK, linewidth=0.8)
    axes[0].set_xlabel("share of impurity reduction")
    axes[1].set_xlabel("drop in AUC when shuffled")
    f.tight_layout()
    return f


# ---------------------------------------------------------------- Part 4

@fig("scaling")
def scaling():
    from sklearn.preprocessing import StandardScaler
    f_ = read("fruit.csv")
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
    fruit_scatter(ax1, f_, x="width_cm", y="weight_g", s=18, legend=False)
    ax1.set_xlim(0, 250); ax1.set_ylim(0, 250); ax1.set_aspect("equal")
    ax1.set_xlabel("width (cm)"); ax1.set_ylabel("weight (g)")
    ax1.set_title("Raw units, drawn to the same scale")
    ax1.annotate("all the width\ndifferences fit\nin this sliver", xy=(9, 120), xytext=(60, 40), fontsize=9.5,
                 arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    z = pd.DataFrame(StandardScaler().fit_transform(f_[["width_cm", "weight_g"]]), columns=["width_cm", "weight_g"])
    z["fruit"] = f_["fruit"]
    fruit_scatter(ax2, z, x="width_cm", y="weight_g", s=22)
    ax2.set_xlim(-3.2, 3.2); ax2.set_ylim(-3.2, 3.2); ax2.set_aspect("equal")
    ax2.axhline(0, color="#d0d6dd", linewidth=0.8, zorder=1); ax2.axvline(0, color="#d0d6dd", linewidth=0.8, zorder=1)
    ax2.set_xlabel("width (standardised)"); ax2.set_ylabel("weight (standardised)")
    ax2.set_title("After StandardScaler: both matter equally")
    f.tight_layout()
    return f


@fig("one-hot")
def one_hot():
    f, ax = diag.canvas(10.5, 2.6)
    vals = ["month-to-month", "one-year", "two-year", "month-to-month"]
    table(ax, 0.2, 2.35, ["contract"], [[v] for v in vals], [2.3], rowh=0.4, color=BLUE, fontsize=9.5)
    arrow(ax, 2.75, 1.35, 3.65, 1.35, text="OneHotEncoder", fontsize=9.5)
    cats = ["month-to-month", "one-year", "two-year"]
    rows = [["1" if v == c else "0" for c in cats] for v in vals]
    table(ax, 3.9, 2.35, ["contract_month-to-month", "contract_one-year", "contract_two-year"], rows, [2.45, 1.95, 1.95], rowh=0.4, color=TEAL, fontsize=9)
    for r, v in enumerate(vals):
        cidx = cats.index(v)
        x0 = 3.9 + [0, 2.45, 4.4][cidx]
        w = [2.45, 1.95, 1.95][cidx]
        ax.add_patch(Rectangle((x0 + 0.03, 2.35 - 0.4 * (r + 2) + 0.03), w - 0.06, 0.34, facecolor="none", edgecolor=ORANGE, linewidth=1.8, zorder=5))
    return f


@fig("pipeline")
def pipeline_fig():
    f, ax = diag.canvas(12, 3.6)
    sbox(ax, 0.1, 1.2, 1.9, 1.1, "raw rows\ntext, gaps,\nmixed units", color=GREY, fontsize=9.5)
    arrow(ax, 2.05, 1.75, 2.55, 1.75)
    sbox(ax, 2.6, 0.45, 4.4, 2.6, "", color=BLUE)
    label(ax, 4.8, 2.8, "ColumnTransformer (\"prep\")", bold=True, size=10)
    sbox(ax, 2.85, 1.55, 3.9, 0.9, "numeric columns:\nSimpleImputer → StandardScaler", color=TEAL, fontsize=9)
    sbox(ax, 2.85, 0.6, 3.9, 0.75, "text columns: OneHotEncoder", color=ORANGE, fontsize=9)
    arrow(ax, 7.05, 1.75, 7.55, 1.75)
    sbox(ax, 7.6, 1.25, 2.2, 1.0, "LogisticRegression\n(\"model\")", color=PURPLE, fontsize=9.5)
    arrow(ax, 9.85, 1.75, 10.35, 1.75)
    sbox(ax, 10.4, 1.3, 1.5, 0.9, "churn\nprobabilities", color=GREY, fontsize=9)
    label(ax, 6.0, 0.08, "pipe.fit(X_train, y_train): every step learns from training rows only  ·  pipe.predict(new_rows): same steps, then predict", size=9.5, color=MUTED)
    return f


@fig("leakage")
def leakage():
    f, ax = diag.canvas(12, 3.6)
    label(ax, 2.9, 3.4, "Train-test contamination", bold=True, size=11.5)
    ax.add_patch(Rectangle((0.3, 2.2), 4.0, 0.5, facecolor=SOFT[BLUE], edgecolor=BLUE, linewidth=1.4))
    ax.add_patch(Rectangle((4.3, 2.2), 1.3, 0.5, facecolor=SOFT[ORANGE], edgecolor=ORANGE, linewidth=1.4))
    label(ax, 2.3, 2.45, "training rows", size=9.5)
    label(ax, 4.95, 2.45, "test rows", size=9.5)
    sbox(ax, 1.6, 0.95, 2.8, 0.6, "scaler / feature selector", color=CRIMSON, fontsize=9.5)
    arrow(ax, 2.3, 2.18, 2.6, 1.6, color=MUTED, lw=1.2)
    arrow(ax, 4.95, 2.18, 3.7, 1.6, color=CRIMSON, lw=1.6)
    label(ax, 2.9, 0.45, "fitted on ALL rows: the test set\nis no longer unseen", size=9.5, color=MUTED)
    ax.plot([6.1, 6.1], [0.2, 3.5], color="#d0d6dd", linewidth=1)
    label(ax, 9.1, 3.4, "Target leakage", bold=True, size=11.5)
    table(ax, 6.6, 3.0, ["tenure", "calls", "cancel_fee_paid", "churned"], [["3", "4", "1", "1"], ["40", "0", "0", "0"], ["7", "2", "1", "1"]],
          [0.9, 0.85, 1.75, 1.0], rowh=0.4, color=BLUE, fontsize=9)
    ax.add_patch(Rectangle((6.6 + 1.75, 3.0 - 1.6), 1.75, 1.6, facecolor="none", edgecolor=CRIMSON, linewidth=2, zorder=5))
    label(ax, 9.1, 0.75, "only known AFTER the customer leaves:\nit gives the answer away", size=9.5, color=MUTED)
    return f


@fig("kfold")
def kfold():
    f, ax = diag.canvas(10.5, 3.6)
    for r in range(5):
        y = 2.9 - r * 0.6
        label(ax, 0.6, y + 0.2, f"round {r + 1}", size=9.5)
        for k in range(5):
            val = k == r
            col = ORANGE if val else BLUE
            ax.add_patch(Rectangle((1.3 + k * 1.3, y), 1.22, 0.42, facecolor=SOFT[col], edgecolor=col, linewidth=1.3))
            label(ax, 1.3 + k * 1.3 + 0.61, y + 0.21, "validate" if val else "train", size=8.5)
        arrow(ax, 7.85, y + 0.21, 8.35, y + 0.21, color=MUTED, lw=1.1)
        label(ax, 8.85, y + 0.21, f"score {r + 1}", size=9.5)
    sbox(ax, 9.4, 1.1, 1.0, 1.2, "mean\n± std", color=TEAL, fontsize=9.5)
    label(ax, 4.5, 0.15, "every row is used for validation exactly once", size=9.5, color=MUTED)
    return f


@fig("validation-curve")
def validation_curve_fig():
    from sklearn.model_selection import validation_curve
    from sklearn.tree import DecisionTreeClassifier
    c = read("churn.csv")
    X = c[["tenure_months", "monthly_charge", "support_calls", "data_gb"]]
    depths = list(range(1, 16))
    tr, va = validation_curve(DecisionTreeClassifier(random_state=0), X, c["churned"], param_name="max_depth",
                              param_range=depths, cv=5, scoring="roc_auc")
    f, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(depths, tr.mean(axis=1), color=BLUE, linewidth=2.2, marker="o", markersize=5, label="training AUC")
    ax.plot(depths, va.mean(axis=1), color=ORANGE, linewidth=2.2, marker="s", markersize=5, label="cross-validated AUC")
    sd = va.std(axis=1)
    ax.fill_between(depths, va.mean(axis=1) - sd, va.mean(axis=1) + sd, color=SOFT[ORANGE], zorder=0)
    best = depths[int(np.argmax(va.mean(axis=1)))]
    ax.axvline(best, color=GREY, linestyle=":", linewidth=1.5)
    ax.text(best + 0.2, 0.52, f"best depth = {best}", fontsize=10)
    ax.set_ylim(0.5, 1.02)
    ax.set_xticks(depths)
    ax.set_xlabel("max_depth"); ax.set_ylabel("AUC")
    ax.legend(loc="upper left", fontsize=10)
    ax.set_title("Validation curve: deeper trees overfit")
    return f


# ---------------------------------------------------------------- Part 5

@fig("kmeans-steps")
def kmeans_steps():
    rng = np.random.default_rng(11)
    centres = np.array([[2, 2], [6, 3], [4, 6.5]])
    pts = np.vstack([rng.normal(c, 0.8, (25, 2)) for c in centres])
    cols = [BLUE, ORANGE, TEAL]
    mk = ["o", "s", "^"]
    start = np.array([[0.8, 7.8], [3.2, 0.6], [7.6, 6.2]])
    f, axes = plt.subplots(1, 4, figsize=(14, 3.7), sharey=True)

    def assign(c):
        return np.argmin(((pts[:, None, :] - c[None]) ** 2).sum(axis=2), axis=1)

    cur = start.copy()
    lab = assign(cur)
    panels = [("1. random starting centres", None, cur.copy()), ("2. assign to nearest centre", lab.copy(), cur.copy())]
    moved = np.array([pts[lab == k].mean(axis=0) for k in range(3)])
    panels.append(("3. move centres to the middle", lab.copy(), moved.copy()))
    cur = moved
    for _ in range(10):
        lab = assign(cur)
        cur = np.array([pts[lab == k].mean(axis=0) for k in range(3)])
    panels.append(("4. repeat until settled", assign(cur), cur))
    for ax, (t, l, c) in zip(axes, panels):
        if l is None:
            ax.scatter(pts[:, 0], pts[:, 1], s=18, color=GREY, edgecolor="white", linewidth=0.5)
        else:
            for k in range(3):
                ax.scatter(pts[l == k, 0], pts[l == k, 1], s=18, color=cols[k], marker=mk[k], edgecolor="white", linewidth=0.5)
        for k in range(3):
            ax.scatter(c[k, 0], c[k, 1], s=190, marker="X", color=cols[k], edgecolor=INK, linewidth=1.2, zorder=5)
        ax.set_title(t, fontsize=10.5)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.5, 9)
    f.tight_layout()
    return f


@fig("elbow-silhouette")
def elbow_silhouette():
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    s = read("shoppers.csv")
    X = s[["annual_income_k", "spending_score"]]
    ks = list(range(2, 9))
    inertia, sil = [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
        inertia.append(km.inertia_ / 1000)
        sil.append(silhouette_score(X, km.labels_))
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.8))
    ax1.plot(ks, inertia, color=BLUE, linewidth=2.2, marker="o")
    ax1.annotate("elbow", xy=(5, inertia[3]), xytext=(6, inertia[3] + 45), fontsize=10, arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax1.set_xlabel("number of clusters k"); ax1.set_ylabel("inertia (thousands)")
    ax1.set_title("Inertia always falls: look for the elbow")
    ax2.plot(ks, sil, color=ORANGE, linewidth=2.2, marker="s")
    ax2.annotate("highest", xy=(5, sil[3]), xytext=(6.2, sil[3] - 0.03), fontsize=10, arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax2.set_xlabel("number of clusters k"); ax2.set_ylabel("silhouette score")
    ax2.set_title("Silhouette: higher is better")
    for ax in (ax1, ax2):
        ax.set_xticks(ks)
    f.tight_layout()
    return f


@fig("pca-idea")
def pca_idea():
    from sklearn.decomposition import PCA
    rng = np.random.default_rng(5)
    x = rng.normal(0, 1.6, 120)
    y = 0.75 * x + rng.normal(0, 0.45, 120)
    P = np.column_stack([x, y])
    pca = PCA().fit(P)
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    ax1.scatter(x, y, s=18, color=BLUE, edgecolor="white", linewidth=0.5)
    for comp, var, name, col in zip(pca.components_, pca.explained_variance_, ["PC1", "PC2"], [ORANGE, CRIMSON]):
        v = comp * 2.2 * np.sqrt(var)
        ax1.add_patch(FancyArrowPatch((0, 0), tuple(v), arrowstyle="-|>", mutation_scale=16, color=col, linewidth=2.4, zorder=4))
        ax1.text(v[0] * 1.12, v[1] * 1.12 + (0.25 if name == "PC2" else 0), name, fontsize=11, fontweight="bold", color=INK, ha="center")
    ax1.set_xlim(-5, 5); ax1.set_ylim(-5, 5); ax1.set_aspect("equal")
    ax1.set_xlabel("feature 1"); ax1.set_ylabel("feature 2")
    ax1.set_title("PC1 follows the biggest spread")
    Z = pca.transform(P)
    ax2.scatter(Z[:, 0], Z[:, 1], s=18, color=BLUE, edgecolor="white", linewidth=0.5)
    ax2.axhline(0, color="#d0d6dd", linewidth=0.8, zorder=0)
    ax2.set_xlim(-5, 5); ax2.set_ylim(-5, 5); ax2.set_aspect("equal")
    r = pca.explained_variance_ratio_
    ax2.set_xlabel(f"PC1 ({r[0]:.0%} of the variation)"); ax2.set_ylabel(f"PC2 ({r[1]:.0%})")
    ax2.set_title("Redrawn on the new axes")
    f.tight_layout()
    return f


# ---------------------------------------------------------------- Part 6

@fig("bag-of-words")
def bag_of_words():
    from sklearn.feature_extraction.text import CountVectorizer
    msgs = ["Win a free prize now", "Are you free for lunch tomorrow?", "Call now to claim your free prize"]
    v = CountVectorizer().fit(msgs)
    words = list(v.get_feature_names_out())
    m = v.transform(msgs).toarray()
    f, ax = diag.canvas(13.2, 2.4)
    for i, t in enumerate(msgs):
        label(ax, 0.1, 1.53 - i * 0.42, f"“{t}”", ha="left", size=9.5)
    arrow(ax, 3.35, 1.1, 3.85, 1.1)
    colw = [0.7] * len(words)
    rows = [[str(n) for n in r] for r in m]
    table(ax, 3.95, 1.95, words, rows, colw, rowh=0.42, color=BLUE, fontsize=8.5)
    for i, r in enumerate(m):
        for j, n in enumerate(r):
            if n:
                ax.add_patch(Rectangle((3.95 + j * 0.7 + 0.04, 1.95 - 0.42 * (i + 2) + 0.04), 0.62, 0.34, facecolor=SOFT[ORANGE], edgecolor="none", zorder=1))
    label(ax, 8.5, 0.1, "one row per message, one column per word: counts, word order thrown away", size=9.5, color=MUTED)
    return f


@fig("lifecycle")
def lifecycle():
    f, ax = diag.canvas(11, 3.4)
    steps = [("data", GREY), ("train &\nevaluate", BLUE), ("save the\npipeline", TEAL), ("serve\npredictions", ORANGE), ("monitor: drift,\nfairness, accuracy", PURPLE)]
    for i, (s, c) in enumerate(steps):
        x = 0.2 + i * 2.2
        sbox(ax, x, 1.6, 1.75, 1.0, s, color=c, fontsize=9.5)
        if i < 4:
            arrow(ax, x + 1.78, 2.1, x + 2.17, 2.1)
    arrow(ax, 0.2 + 4 * 2.2 + 0.9, 1.55, 0.2 + 0.9, 1.55, color=MUTED, rad=-0.25, lw=1.4)
    label(ax, 5.5, 0.35, "retrain on fresh data", size=10, color=MUTED)
    return f


@fig("project-steps")
def project_steps():
    f, ax = diag.canvas(12, 3.0)
    steps = ["1. question &\nsuccess measure", "2. split off\na test set", "3. baseline", "4. pipeline", "5. compare\nmodels (CV)",
             "6. tune the\nwinner (CV)", "7. threshold from\nCV predictions", "8. test\nonce", "9. explain\n& report"]
    cols = [GREY, ORANGE, GREY, BLUE, BLUE, BLUE, BLUE, ORANGE, TEAL]
    for i, (s, c) in enumerate(zip(steps, cols)):
        row, k = divmod(i, 5)
        x = 0.1 + k * 2.4
        y = 1.75 - row * 1.35
        sbox(ax, x, y, 2.0, 0.9, s, color=c, fontsize=9)
        if k < 4 and i < 8:
            arrow(ax, x + 2.02, y + 0.45, x + 2.38, y + 0.45)
    arrow(ax, 0.1 + 4 * 2.4 + 1.0, 1.73, 0.1 + 1.0, 1.32, color=MUTED, lw=1.2, rad=0.0)
    return f


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names or FIGS:
        save(FIGS[name](), name)
    print(len(names or FIGS), "figures")


if __name__ == "__main__":
    main(sys.argv[1:])
