"""Draw the diagrams and charts used in the Python for Data lessons into figures/*.svg.

Run: python course/figures.py   (uses the shared helpers in tools/diag.py)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from diag import *  # noqa: E402,F401,F403
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

OUT = HERE / "figures"
DATA = HERE / "data"


def workflow():
    fig, ax = canvas(11, 1.9, xlim=(0, 11), ylim=(0, 1.9))
    steps = [("1. Ask", "a clear question"), ("2. Load", "files, databases"), ("3. Clean", "gaps, types, typos"),
             ("4. Analyse", "filter, group, join"), ("5. Show", "charts"), ("6. Share", "results, report")]
    cols = [GREY, BLUE, ORANGE, TEAL, PURPLE, GREEN]
    for i, ((t, sub), c) in enumerate(zip(steps, cols)):
        x = 0.1 + i * 1.82
        box(ax, x, 0.55, 1.5, 0.95, "", color=c)
        label(ax, x + 0.75, 1.18, t, bold=True)
        label(ax, x + 0.75, 0.82, sub, size=9.5)
        if i < 5:
            arrow(ax, x + 1.52, 1.02, x + 1.8, 1.02)
    label(ax, 5.5, 0.2, "Cleaning usually takes the most time. Every step is in this course.", size=9.5, color=GREY)
    return fig


def csv_vs_json():
    fig, ax = canvas(10.2, 3.3, xlim=(0, 10.2), ylim=(0, 3.3))
    label(ax, 2.3, 3.15, "CSV: a flat table", bold=True)
    table(ax, 0.2, 2.9, ["title", "year", "genre"], [["Broken Station", 2006, "Comedy"], ["Last River", 2022, "Thriller"], ["Silent River", 2022, "Sci-Fi"]],
          [1.9, 0.8, 1.2], rowh=0.42, fontsize=9.5)
    label(ax, 7.4, 3.15, "JSON: values inside values", bold=True)
    box(ax, 5.3, 0.25, 4.6, 2.65, "", color=ORANGE)
    lines = ['{', '  "order_id": 1042,', '  "customer": {', '    "name": "Priya",', '    "city": "Leeds" },',
             '  "items": [', '    {"product": "Notebook", "units": 3},', '    {"product": "Lamp", "units": 1} ]', '}']
    for i, l in enumerate(lines):
        ax.text(5.45, 2.68 - i * 0.27, l.replace(' ', '\u00a0'), fontsize=9, family="monospace", va="center")
    return fig


def array_shapes():
    fig, ax = canvas(10, 3.2, xlim=(0, 10), ylim=(0, 3.2))
    label(ax, 1.9, 3.0, "1-D array: shape (5,)", bold=True)
    for i, v in enumerate([4.5, 6.0, 35.0, 59.0, 79.0]):
        box(ax, 0.2 + i * 0.7, 2.0, 0.65, 0.6, str(v), color=TEAL, round_=0.02, fontsize=9.5, mono=True)
        label(ax, 0.52 + i * 0.7, 1.75, f"[{i}]", size=9, color=GREY, mono=True)
    label(ax, 7.0, 3.0, "2-D array: shape (3, 4)", bold=True)
    vals = np.arange(1, 13).reshape(3, 4)
    for r in range(3):
        for c in range(4):
            box(ax, 5.6 + c * 0.7, 2.2 - r * 0.62, 0.65, 0.57, str(vals[r, c]), color=BLUE, round_=0.02, fontsize=9.5, mono=True)
    arrow(ax, 5.3, 2.45, 5.3, 1.05, color=ORANGE, text=None)
    label(ax, 5.05, 1.75, "axis 0\n(rows)", size=9, color=ORANGE, ha="right")
    arrow(ax, 5.6, 0.75, 8.35, 0.75, color=PURPLE)
    label(ax, 7.0, 0.45, "axis 1 (columns)", size=9, color=PURPLE)
    return fig


def boolean_mask():
    fig, ax = canvas(10, 2.6, xlim=(0, 10), ylim=(0, 2.6))
    temps = [3.1, 4.8, 7.2, 10.5, 14.0, 17.3, 19.6]
    rows = [("temps", [str(t) for t in temps], [GREY] * 7),
            ("temps > 10", ["True" if t > 10 else "False" for t in temps], [TEAL if t > 10 else GREY for t in temps])]
    for r, (name, vals, cols) in enumerate(rows):
        y = 1.9 - r * 0.75
        label(ax, 1.55, y + 0.27, name, mono=True, ha="right", size=10)
        for i, (v, c) in enumerate(zip(vals, cols)):
            box(ax, 1.7 + i * 0.8, y, 0.75, 0.55, v, color=c, round_=0.02, fontsize=9, mono=True)
    label(ax, 1.55, 0.67, "temps[temps > 10]", mono=True, ha="right", size=10)
    for i, t in enumerate([t for t in temps if t > 10]):
        box(ax, 1.7 + i * 0.8, 0.4, 0.75, 0.55, str(t), color=TEAL, round_=0.02, fontsize=9, mono=True)
    label(ax, 7.9, 0.67, "only the True positions are kept", size=9.5, color=GREY, ha="left")
    return fig


def broadcasting():
    fig, ax = canvas(10.5, 2.9, xlim=(0, 10.5), ylim=(0, 2.9))
    units = np.array([[5, 2, 0, 7], [3, 8, 1, 4], [6, 1, 2, 2]])
    prices = [10, 25, 40, 5]
    label(ax, 1.5, 2.7, "units (3, 4)", bold=True)
    for r in range(3):
        for c in range(4):
            box(ax, 0.1 + c * 0.72, 1.9 - r * 0.6, 0.66, 0.54, str(units[r, c]), color=BLUE, round_=0.02, fontsize=9.5, mono=True)
    label(ax, 3.3, 1.35, "×", size=18)
    label(ax, 5.15, 2.7, "prices (4,) stretched to (3, 4)", bold=True)
    for r in range(3):
        for c in range(4):
            box(ax, 3.7 + c * 0.72, 1.9 - r * 0.6, 0.66, 0.54, str(prices[c]), color=ORANGE if r == 0 else GREY, round_=0.02, fontsize=9.5, mono=True)
    label(ax, 6.85, 1.35, "=", size=18)
    label(ax, 8.65, 2.7, "revenue (3, 4)", bold=True)
    for r in range(3):
        for c in range(4):
            box(ax, 7.2 + c * 0.82, 1.9 - r * 0.6, 0.76, 0.54, str(units[r, c] * prices[c]), color=TEAL, round_=0.02, fontsize=9.5, mono=True)
    label(ax, 5.25, 0.35, "the one row of prices is reused for every store (grey copies are never actually made)", size=9.5, color=GREY)
    return fig


def axis_sums():
    fig, ax = canvas(9.5, 3.3, xlim=(0, 9.5), ylim=(0, 3.3))
    s = np.array([[72, 85, 90], [64, 70, 58], [88, 91, 79], [55, 62, 71]])
    for r in range(4):
        for c in range(3):
            box(ax, 2.5 + c * 0.9, 2.6 - r * 0.55, 0.85, 0.5, str(s[r, c]), color=BLUE, round_=0.02, fontsize=9.5, mono=True)
    for c, name in enumerate(["math", "sci", "eng"]):
        label(ax, 2.92 + c * 0.9, 3.2, name, size=9, color=GREY)
    for c in range(3):
        box(ax, 2.5 + c * 0.9, 0.25, 0.85, 0.5, f"{s[:, c].mean():.1f}", color=ORANGE, round_=0.02, fontsize=9, mono=True)
    arrow(ax, 3.85, 0.95, 3.85, 0.8, color=ORANGE)
    label(ax, 2.35, 0.5, "mean(axis=0)\none per column", size=9.5, color=ORANGE, ha="right")
    for r in range(4):
        box(ax, 5.4, 2.6 - r * 0.55, 0.9, 0.5, f"{s[r].mean():.1f}", color=PURPLE, round_=0.02, fontsize=9, mono=True)
    label(ax, 6.5, 1.85, "mean(axis=1)\none per row", size=9.5, color=PURPLE, ha="left")
    return fig


def dataframe_anatomy():
    fig, ax = canvas(10, 3.4, xlim=(0, 10), ylim=(0, 3.4))
    rows = [[1001, "2025-01-01", "West", "Headphones", 1], [1002, "2025-01-04", "North", "Desk Lamp", 3], [1003, "2025-01-06", "East", "Pen Pack", 7]]
    table(ax, 1.2, 2.6, ["order_id", "order_date", "region", "product", "units"], rows, [1.2, 1.5, 1.0, 1.5, 0.9], rowh=0.45, highlight={}, fontsize=9.5)
    for i in range(3):
        box(ax, 0.6, 2.15 - i * 0.45 - 0.45, 0.55, 0.43, str(i), color=GREY, round_=0.02, fontsize=9.5, mono=True)
    label(ax, 0.88, 2.35, "index", size=9.5, color=GREY)
    ax.add_patch(plt.Rectangle((4.9, 0.72), 1.5, 1.93, fill=False, edgecolor=ORANGE, linewidth=2.2))
    label(ax, 5.65, 0.45, 'sales["product"] is a Series', size=9.5, color=ORANGE)
    label(ax, 4.2, 3.1, "columns (names)", size=9.5, color=TEAL)
    arrow(ax, 4.2, 2.98, 4.2, 2.62, color=TEAL)
    return fig


def missing_map():
    e = pd.read_csv(DATA / "employees_messy.csv")
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.imshow(e.isna().T.to_numpy(), aspect="auto", cmap="Oranges", vmin=0, vmax=1.3, interpolation="nearest")
    ax.set_yticks(range(len(e.columns)), e.columns)
    ax.set_xlabel("row number")
    ax.set_title("Where are the gaps? Orange = missing (employees_messy.csv)")
    ax.spines[["left", "bottom"]].set_visible(False)
    return fig


def split_apply_combine():
    fig, ax = canvas(11, 3.6, xlim=(0, 11), ylim=(0, 3.6))
    rows = [("North", 120), ("South", 95), ("North", 80), ("East", 60), ("South", 40), ("East", 30), ("North", 50)]
    col = {"North": TEAL, "South": ORANGE, "East": BLUE}
    label(ax, 1.25, 3.45, "rows", bold=True)
    table(ax, 0.1, 3.25, ["region", "revenue"], rows, [1.2, 1.1], rowh=0.37, highlight={i: col[r] for i, (r, _) in enumerate(rows)}, fontsize=9.5)
    arrow(ax, 2.5, 1.9, 3.3, 1.9, text="split", fontsize=10)
    label(ax, 4.6, 3.45, "groups", bold=True)
    y = 3.15
    for reg in ["East", "North", "South"]:
        vals = [v for r, v in rows if r == reg]
        h = 0.37 * len(vals)
        box(ax, 3.45, y - h, 2.4, h - 0.05, f"{reg}: " + " + ".join(map(str, vals)), color=col[reg], fontsize=9.5)
        y -= h + 0.15
    arrow(ax, 6.0, 1.9, 7.1, 1.9, text="apply sum", fontsize=10)
    label(ax, 8.6, 3.45, "combine", bold=True)
    table(ax, 7.4, 3.0, ["region", "revenue"], [["East", 90], ["North", 250], ["South", 135]], [1.4, 1.2], rowh=0.42,
          highlight={0: BLUE, 1: TEAL, 2: ORANGE}, fontsize=9.5)
    label(ax, 8.6, 0.9, 'sales.groupby("region")["revenue"].sum()', mono=True, size=9)
    return fig


def merge_joins():
    fig, ax = canvas(9, 2.5, xlim=(0, 9), ylim=(0, 2.5))
    for i, (how, shade) in enumerate([("inner", ("middle",)), ("left", ("left", "middle")), ("right", ("middle", "right")), ("outer", ("left", "middle", "right"))]):
        venn(ax, 1.1 + i * 2.25, 1.4, r=0.6, gap=0.6, shade=shade, color=PURPLE, title=f'how="{how}"', labels=("left", "right"))
    return fig


def wide_long():
    fig, ax = canvas(10, 3.0, xlim=(0, 10), ylim=(0, 3.0))
    label(ax, 1.75, 2.85, "wide", bold=True)
    table(ax, 0.2, 2.6, ["student", "math", "science"], [["Ana", 72, 85], ["Ben", 64, 70]], [1.2, 0.9, 1.1], rowh=0.42, fontsize=9.5)
    arrow(ax, 3.6, 2.05, 5.0, 2.05, text="melt", fontsize=10, color=TEAL)
    arrow(ax, 5.0, 1.35, 3.6, 1.35, text="pivot", fontsize=10, color=ORANGE, text_offset=(0, -0.38))
    label(ax, 7.2, 2.85, "long (tidy)", bold=True)
    table(ax, 5.4, 2.6, ["student", "subject", "score"], [["Ana", "math", 72], ["Ana", "science", 85], ["Ben", "math", 64], ["Ben", "science", 70]],
          [1.2, 1.3, 0.9], rowh=0.42, fontsize=9.5, highlight={0: TEAL, 1: TEAL, 2: ORANGE, 3: ORANGE})
    return fig


def bins():
    fig, ax = plt.subplots(figsize=(8.5, 1.9))
    edges = [0, 40, 60, 80, 100]
    names = ["D", "C", "B", "A"]
    cols = [RED, ORANGE, BLUE, TEAL]
    for lo, hi, n, c in zip(edges, edges[1:], names, cols):
        ax.add_patch(plt.Rectangle((lo, 0.35), hi - lo, 0.3, color=c, alpha=0.35))
        ax.text((lo + hi) / 2, 0.5, f"{n}: ({lo}, {hi}]", ha="center", va="center", family="monospace", fontsize=10)
    for e in edges:
        ax.text(e, 0.12, str(e), ha="center", fontsize=9.5)
    ax.plot(60, 0.8, "o", color=INK)
    ax.text(60, 0.9, "60 → C (right edge included)", ha="center", fontsize=9.5)
    ax.set_xlim(-2, 102); ax.set_ylim(0, 1.05); ax.axis("off")
    ax.set_title('pd.cut(scores, bins=[0, 40, 60, 80, 100], labels=["D", "C", "B", "A"])', fontsize=10.5, family="monospace")
    return fig


def rolling():
    w = pd.read_csv(DATA / "weather.csv", parse_dates=["date"])
    lon = w[w["city"] == "London"].set_index("date")["temp_c"]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(lon.index, lon, color=GREY, linewidth=0.8, label="daily")
    ax.plot(lon.index, lon.rolling(7).mean(), color=TEAL, linewidth=2, label="7-day average")
    ax.plot(lon.index, lon.rolling(30).mean(), color=ORANGE, linewidth=2.2, label="30-day average")
    ax.set_ylabel("°C"); ax.legend(frameon=False)
    ax.set_title("Rolling averages smooth out day-to-day noise (London, 2025)")
    return fig


def chart_chooser():
    rng = np.random.default_rng(1)
    fig, axes = plt.subplots(1, 5, figsize=(12, 2.6))
    axes[0].plot(range(12), np.cumsum(rng.normal(1, 2, 12)) + 20, color=TEAL, marker="o", markersize=3)
    axes[0].set_title("Line\nchange over time", fontsize=10.5)
    axes[1].barh(["C", "B", "A"], [3, 5, 8], color=ORANGE)
    axes[1].set_title("Bar\ncompare categories", fontsize=10.5)
    axes[2].hist(rng.normal(60, 12, 400), bins=20, color=BLUE)
    axes[2].set_title("Histogram\nhow values spread", fontsize=10.5)
    x = rng.uniform(0, 10, 60)
    axes[3].scatter(x, 30 + 4 * x + rng.normal(0, 6, 60), s=10, color=PURPLE)
    axes[3].set_title("Scatter\nare two things related?", fontsize=10.5)
    axes[4].boxplot([rng.normal(m, 8, 80) for m in (50, 58, 54)], widths=0.5)
    axes[4].set_title("Box plot\ncompare spreads", fontsize=10.5)
    for a in axes:
        a.set_xticks([]); a.set_yticks([])
    return fig


FIGS = {"workflow": workflow, "csv-vs-json": csv_vs_json, "array-shapes": array_shapes, "boolean-mask": boolean_mask,
        "broadcasting": broadcasting, "axis": axis_sums, "dataframe-anatomy": dataframe_anatomy, "missing-map": missing_map,
        "split-apply-combine": split_apply_combine, "merge-joins": merge_joins, "wide-long": wide_long, "cut-bins": bins,
        "rolling-average": rolling, "chart-chooser": chart_chooser}

if __name__ == "__main__":
    for name, make in FIGS.items():
        save(make(), OUT / f"{name}.svg")
    print(len(FIGS), "figures")
