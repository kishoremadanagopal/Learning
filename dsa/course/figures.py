"""Draw the lesson diagrams for Data Structures and Algorithms in Python into figures/*.svg (deterministic).

Run: python figures.py            (all figures)
     python figures.py kmp          (one figure)
Palette (validated for colour-blind separation): blue, orange, teal, crimson, purple; text stays in ink.
"""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
sys.path.insert(0, str(ROOT.parents[1] / "tools"))
import diag  # noqa: E402
from diag import arrow, box, label  # noqa: E402

GREEN, BLUE, ORANGE, TEAL, CRIMSON, PURPLE = "#2e7d32", "#1f6fb2", "#e07b00", "#159a7f", "#b42357", "#7a5ac8"
GREY, INK, MUTED = "#9aa5b1", "#1f2933", "#52606d"
SOFT = {GREEN: "#e3f2e4", BLUE: "#e3eef8", ORANGE: "#fdecd6", TEAL: "#dcf3ee", CRIMSON: "#f8e1e8", PURPLE: "#ece6f8", GREY: "#eef1f4", INK: "#eef1f4"}

plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"], "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold",
    "axes.titlesize": 12.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white", "svg.hashsalt": "dsa-course",
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


def sbox(ax, x, y, w, h, text="", color=GREEN, **kw):
    box(ax, x, y, w, h, text, color=color, fill=SOFT.get(color, "white"), **kw)


def cells(ax, x, y, values, w=0.7, h=0.6, color=BLUE, highlight=None, mono=True, fontsize=11, idx=None, idx_y=None):
    """A row of boxes with optional index labels above; highlight: {i: color}."""
    highlight = highlight or {}
    for i, v in enumerate(values):
        c = highlight.get(i, color)
        sbox(ax, x + i * w, y, w - 0.06, h, str(v), color=c, mono=mono, fontsize=fontsize)
        if idx is not None:
            label(ax, x + i * w + (w - 0.06) / 2, idx_y if idx_y is not None else y + h + 0.22, str(idx[i] if idx != "auto" else i), size=9.5, color=MUTED, mono=True)


# ---------------------------------------------------------------- Part 1

@fig("structures-overview")
def structures_overview():
    f, ax = diag.canvas(14, 3.1)
    # array
    for i in range(4):
        sbox(ax, 0.2 + i * 0.42, 1.4, 0.4, 0.45, str(i), color=BLUE, fontsize=9)
    label(ax, 1.05, 0.55, "array", bold=True)
    # linked list
    for i in range(3):
        sbox(ax, 2.35 + i * 0.75, 1.4, 0.45, 0.45, "", color=TEAL)
        if i < 2:
            arrow(ax, 2.82 + i * 0.75, 1.62, 3.08 + i * 0.75, 1.62, lw=1.2)
    label(ax, 3.3, 0.55, "linked list", bold=True)
    # stack
    for i in range(4):
        sbox(ax, 4.8, 0.95 + i * 0.32, 0.9, 0.28, "", color=ORANGE)
    arrow(ax, 6.0, 2.45, 6.0, 2.0, lw=1.2, text=None)
    label(ax, 6.35, 2.3, "push\n/ pop", size=8.5, color=MUTED)
    label(ax, 5.25, 0.55, "stack", bold=True)
    # queue
    for i in range(4):
        sbox(ax, 7.1 + i * 0.42, 1.4, 0.38, 0.45, "", color=PURPLE)
    arrow(ax, 6.75, 1.62, 7.05, 1.62, lw=1.2)
    arrow(ax, 8.8, 1.62, 9.1, 1.62, lw=1.2)
    label(ax, 6.85, 2.1, "in", size=8.5, color=MUTED)
    label(ax, 8.95, 2.1, "out", size=8.5, color=MUTED)
    label(ax, 7.9, 0.55, "queue", bold=True)
    # hash table
    for i in range(4):
        sbox(ax, 9.75, 0.95 + i * 0.36, 0.38, 0.32, str(i), color=CRIMSON, fontsize=8)
    sbox(ax, 10.35, 1.67, 0.75, 0.3, "\"cat\"", color=CRIMSON, fontsize=8, mono=True)
    arrow(ax, 10.14, 1.82, 10.33, 1.82, lw=1.0)
    label(ax, 10.45, 0.55, "hash table", bold=True)
    # tree
    pts = {"r": (12.0, 2.45), "a": (11.55, 1.75), "b": (12.45, 1.75), "c": (11.3, 1.05), "d": (11.8, 1.05)}
    for p, q in [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d")]:
        ax.plot([pts[p][0], pts[q][0]], [pts[p][1], pts[q][1]], color=MUTED, linewidth=1.3, zorder=1)
    for x, y in pts.values():
        ax.add_patch(Circle((x, y), 0.17, facecolor=SOFT[GREEN], edgecolor=GREEN, linewidth=1.5, zorder=3))
    label(ax, 11.95, 0.55, "tree", bold=True)
    # graph
    g = [(13.0, 2.3), (13.75, 2.5), (13.5, 1.6), (12.95, 1.15), (13.85, 1.05)]
    for a, b in [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)]:
        ax.plot([g[a][0], g[b][0]], [g[a][1], g[b][1]], color=MUTED, linewidth=1.3, zorder=1)
    for x, y in g:
        ax.add_patch(Circle((x, y), 0.14, facecolor=SOFT[BLUE], edgecolor=BLUE, linewidth=1.5, zorder=3))
    label(ax, 13.4, 0.55, "graph", bold=True)
    return f


@fig("six-steps")
def six_steps():
    f, ax = diag.canvas(13, 2.7)
    steps = [("1. Understand", "inputs, outputs,\nlimits"), ("2. Examples", "work 2–3 by hand,\nincl. edge cases"),
             ("3. Brute force", "simplest correct way\nand its Big-O"), ("4. Spot the pattern", "clue words, where\nis work wasted?"),
             ("5. Plan", "steps in plain\nwords"), ("6. Code & test", "run examples,\nstate the cost")]
    cols = [GREY, GREY, ORANGE, GREEN, BLUE, TEAL]
    for i, ((t, sub), c) in enumerate(zip(steps, cols)):
        x = 0.1 + i * 2.15
        sbox(ax, x, 1.0, 1.85, 1.15, "", color=c)
        label(ax, x + 0.925, 1.85, t, bold=True, size=10)
        label(ax, x + 0.925, 1.35, sub, size=8.5, color=MUTED)
        if i < 5:
            arrow(ax, x + 1.87, 1.57, x + 2.13, 1.57)
    arrow(ax, 0.1 + 5 * 2.15 + 0.9, 0.97, 0.1 + 4 * 2.15 + 0.9, 0.97, color=MUTED, rad=-0.45, lw=1.3)
    label(ax, 0.1 + 4.5 * 2.15 + 0.9, 0.18, "a test fails? fix the plan", size=9, color=MUTED)
    return f


@fig("big-o-growth")
def big_o_growth():
    import numpy as np
    n = np.linspace(1, 20, 400)
    f, ax = plt.subplots(figsize=(8.4, 4.4))
    curves = [("O(2ⁿ)", 2 ** n, CRIMSON, "-"), ("O(n²)", n ** 2, ORANGE, "-"), ("O(n log n)", n * np.log2(n), PURPLE, "--"),
              ("O(n)", n, BLUE, "-"), ("O(log n)", np.log2(n), TEAL, "--"), ("O(1)", np.ones_like(n), GREEN, "-")]
    ends = {"O(2ⁿ)": (7.3, 101), "O(n²)": (11.0, 104), "O(n log n)": (20.3, 86), "O(n)": (20.3, 20), "O(log n)": (20.3, 7.5), "O(1)": (20.3, 1.5)}
    for name, y, c, ls in curves:
        ax.plot(n, y, color=c, linewidth=2.3, linestyle=ls)
        x0, y0 = ends[name]
        ax.text(x0, y0, name, fontsize=10.5, fontweight="bold", color=INK, va="center", ha="left" if x0 > 20 else "left")
    ax.set_ylim(0, 110); ax.set_xlim(1, 23.5)
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_xlabel("n (input size)"); ax.set_ylabel("steps")
    ax.set_title("How the number of steps grows with the input")
    return f


@fig("amortized-append")
def amortized_append():
    # CPython's list growth rule (3.12+): new_allocated = (newsize + (newsize >> 3) + 6) & ~3
    cap, sizes, caps, resized = 0, [], [], []
    for size in range(1, 41):
        if size > cap:
            cap = (size + (size >> 3) + 6) & ~3
            resized.append(size)
        sizes.append(size); caps.append(cap)
    f, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.step(sizes, caps, where="post", color=BLUE, linewidth=2.2, label="capacity (slots reserved)")
    ax.plot(sizes, sizes, color=GREY, linewidth=1.8, linestyle="--", label="items stored")
    ax.scatter(resized, [caps[s - 1] for s in resized], s=55, color=ORANGE, zorder=4, edgecolor="white", linewidth=0.8,
               label="full: copy everything into a bigger block (O(n))")
    ax.set_xlabel("number of appends"); ax.set_ylabel("slots")
    ax.set_xlim(0, 41); ax.set_ylim(0, 50)
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_title("Most appends are cheap; occasional copies average out to O(1)")
    return f


@fig("list-vs-set")
def list_vs_set():
    f, ax = diag.canvas(12, 3.4)
    label(ax, 2.9, 3.15, "list: check one by one, O(n)", bold=True, size=11)
    vals = [8, 3, 5, 1, 9, 7, 4]
    for i, v in enumerate(vals):
        c = ORANGE if v == 7 else BLUE
        sbox(ax, 0.2 + i * 0.8, 1.6, 0.7, 0.6, str(v), color=c, mono=True)
        if i < 5:
            arrow(ax, 0.55 + i * 0.8, 1.45, 1.35 + i * 0.8, 1.45, color=MUTED, lw=1.0, rad=0.4)
    label(ax, 2.9, 0.75, "is 7 in the list? → 6 comparisons", size=10, color=MUTED)
    ax.plot([6.3, 6.3], [0.4, 3.2], color="#d0d6dd", linewidth=1)
    label(ax, 9.2, 3.15, "set / dict: jump straight there, O(1)", bold=True, size=11)
    sbox(ax, 6.6, 1.65, 0.7, 0.5, "7", color=ORANGE, mono=True)
    arrow(ax, 7.35, 1.9, 7.85, 1.9)
    sbox(ax, 7.9, 1.55, 1.25, 0.7, "hash(7)\n% 8 = 7", color=GREY, fontsize=9, mono=True)
    for i in range(8):
        c = ORANGE if i == 7 else PURPLE
        sbox(ax, 9.55 + 0.03, 2.6 - i * 0.3, 0.45, 0.26, str(i), color=c, fontsize=8, mono=True)
    arrow(ax, 9.2, 1.85, 9.55, 0.53, color=ORANGE, lw=1.6)
    label(ax, 10.75, 0.55, "bucket 7", size=9.5, color=MUTED, ha="left")
    return f


# ---------------------------------------------------------------- Part 2

@fig("array-memory")
def array_memory():
    f, ax = diag.canvas(10.2, 3.6)
    vals = [12, 7, 30, 4, 18, 25, 9, 3]
    cells(ax, 0.3, 2.0, vals, w=0.75, color=BLUE, highlight={5: ORANGE}, idx="auto")
    label(ax, 0.3, 3.3, "a[5]: start + 5 × slot size → one step, O(1)", ha="left", size=10.5, bold=True)
    arrow(ax, 4.3, 3.12, 4.06, 2.66, color=ORANGE, lw=1.6)
    label(ax, 7.4, 1.25, "insert 99 at index 2:", ha="left", size=10.5, bold=True)
    after = [12, 7, 99, 30, 4, 18, 25, 9, 3]
    cells(ax, 0.3, 0.2, after, w=0.75, color=BLUE, highlight={2: ORANGE}, fontsize=10)
    for i in range(3, 9):
        arrow(ax, 0.3 + (i - 1) * 0.75 + 0.35, 1.95, 0.3 + i * 0.75 + 0.35, 0.86, color=MUTED, lw=1.0)
    label(ax, 7.4, 0.5, "every later item\nshifts right: O(n)", ha="left", size=10, color=MUTED)
    return f


@fig("two-pointers")
def two_pointers():
    f, ax = diag.canvas(12.2, 3.6)
    label(ax, 2.7, 3.35, "Opposite ends (sorted data)", bold=True, size=11)
    vals = [1, 3, 4, 6, 8, 11]
    cells(ax, 0.3, 1.7, vals, w=0.8, color=BLUE, highlight={0: ORANGE, 5: ORANGE}, idx="auto")
    label(ax, 0.66, 1.25, "L →", bold=True, size=11)
    label(ax, 4.36, 1.25, "← R", bold=True, size=11)
    label(ax, 2.7, 0.6, "sum too small: L moves right\nsum too big: R moves left", size=9.5, color=MUTED)
    ax.plot([5.55, 5.55], [0.3, 3.4], color="#d0d6dd", linewidth=1)
    label(ax, 8.9, 3.35, "Same direction (read / write)", bold=True, size=11)
    vals2 = [1, 3, 12, 0, 0, 12]
    cells(ax, 6.0, 1.7, [1, 3, 12, "·", "·", "·"], w=0.8, color=TEAL, highlight={3: ORANGE}, idx="auto")
    label(ax, 8.76, 1.25, "W", bold=True, size=11)
    label(ax, 10.36, 1.25, "R →", bold=True, size=11)
    label(ax, 8.9, 0.6, "R reads every item; W marks where\nthe next kept item is written", size=9.5, color=MUTED)
    return f


@fig("sliding-window")
def sliding_window():
    f, ax = diag.canvas(11, 3.7)
    vals = [2, 1, 5, 1, 3, 2]
    for row, (start, title) in enumerate([(1, "window [1, 5, 1]: sum 7"), (2, "slide right: 7 − 1 + 3 = 9")]):
        y = 2.25 - row * 1.6
        hl = {i: GREEN for i in range(start, start + 3)}
        if row == 1:
            hl[1] = CRIMSON
            hl[4] = ORANGE
        cells(ax, 0.3, y, vals, w=0.8, color=GREY, highlight=hl)
        ax.add_patch(Rectangle((0.3 + start * 0.8 - 0.06, y - 0.08), 3 * 0.8 + 0.06, 0.76, fill=False, edgecolor=GREEN, linewidth=2.2, zorder=5))
        label(ax, 5.4, y + 0.3, title, ha="left", size=10.5, bold=row == 1)
    label(ax, 5.4, 0.3, "one number leaves (crimson), one joins (orange)", ha="left", size=9.5, color=MUTED)
    return f


@fig("prefix-sums")
def prefix_sums():
    f, ax = diag.canvas(11, 3.7)
    nums = [3, 1, 4, 1, 5, 9]
    prefix = [0, 3, 4, 8, 9, 14, 23]
    label(ax, 0.1, 2.75, "nums", ha="left", bold=True, mono=True)
    cells(ax, 1.5, 2.45, nums, w=0.8, color=BLUE, highlight={2: ORANGE, 3: ORANGE, 4: ORANGE}, idx="auto")
    label(ax, 0.1, 1.15, "prefix", ha="left", bold=True, mono=True)
    cells(ax, 1.1, 0.85, prefix, w=0.8, color=TEAL, highlight={2: CRIMSON, 5: CRIMSON}, idx="auto", idx_y=0.55)
    label(ax, 7.4, 2.75, "4 + 1 + 5 = 10", ha="left", size=11)
    label(ax, 7.4, 1.15, "prefix[5] − prefix[2]\n= 14 − 4 = 10", ha="left", size=11, bold=True)
    return f


@fig("grid-neighbours")
def grid_neighbours():
    f, ax = diag.canvas(8, 4.0)
    rows, cols = 3, 4
    x0, y0, s = 1.2, 0.5, 0.8
    for r in range(rows):
        for c in range(cols):
            colr = ORANGE if (r, c) == (1, 2) else (TEAL if (r, c) in [(0, 2), (2, 2), (1, 1), (1, 3)] else GREY)
            sbox(ax, x0 + c * s, y0 + (rows - 1 - r) * s, s - 0.06, s - 0.06, f"{r},{c}", color=colr, fontsize=9, mono=True)
    for c in range(cols):
        label(ax, x0 + c * s + 0.37, y0 + rows * s + 0.2, f"col {c}", size=9, color=MUTED)
    for r in range(rows):
        label(ax, x0 - 0.45, y0 + (rows - 1 - r) * s + 0.37, f"row {r}", size=9, color=MUTED)
    label(ax, 5.0, 2.55, "grid[1][2]", ha="left", bold=True, mono=True)
    label(ax, 5.0, 2.05, "neighbours:", ha="left", size=10)
    label(ax, 5.0, 1.6, "(r−1, c) (r+1, c)\n(r, c−1) (r, c+1)", ha="left", size=9.5, mono=True)
    label(ax, 5.0, 0.85, "check 0 ≤ r < rows\nand 0 ≤ c < cols", ha="left", size=9.5, color=MUTED)
    return f


@fig("kmp")
def kmp():
    f, ax = diag.canvas(12, 4.6)
    p = "ababaca"
    lps = [0, 0, 1, 2, 3, 0, 1]
    label(ax, 0.1, 4.2, "pattern", ha="left", bold=True, size=10)
    cells(ax, 1.4, 3.95, list(p), w=0.6, h=0.5, color=BLUE)
    label(ax, 0.1, 3.5, "LPS", ha="left", bold=True, size=10)
    cells(ax, 1.4, 3.25, lps, w=0.6, h=0.5, color=TEAL)
    label(ax, 6.0, 3.85, "LPS[4] = 3: \"aba\" is both a prefix\nand a suffix of \"ababa\"", ha="left", size=9.5, color=MUTED)
    label(ax, 0.1, 2.3, "text", ha="left", bold=True, size=10)
    cells(ax, 1.4, 2.05, list("ababab"), w=0.6, h=0.5, color=GREY, highlight={5: CRIMSON})
    label(ax, 0.1, 1.45, "before", ha="left", size=9, color=MUTED)
    cells(ax, 1.4, 1.25, list("ababa"), w=0.6, h=0.42, color=BLUE, fontsize=9.5)
    label(ax, 4.6, 1.46, "next pattern char 'c' ≠ text 'b': mismatch after 5 matches", ha="left", size=9, color=MUTED)
    label(ax, 0.1, 0.6, "after", ha="left", size=9, color=MUTED)
    cells(ax, 1.4 + 2 * 0.6, 0.4, list("aba"), w=0.6, h=0.42, color=GREEN, fontsize=9.5)
    label(ax, 4.6, 0.61, "slide so \"aba\" (LPS = 3) stays matched;\nthe text pointer never moves back", ha="left", size=9, color=MUTED)
    return f


# ---------------------------------------------------------------- Part 3

@fig("hash-table")
def hash_table():
    f, ax = diag.canvas(11.5, 4.2)
    keys = [("\"cat\"", 3.3), ("\"dog\"", 2.1), ("\"owl\"", 0.9)]
    for k, y in keys:
        sbox(ax, 0.2, y, 1.1, 0.5, k, color=ORANGE, mono=True, fontsize=10)
        arrow(ax, 1.35, y + 0.25, 1.95, y + 0.25, lw=1.2)
    sbox(ax, 2.0, 0.8, 1.8, 3.1, "", color=GREY)
    label(ax, 2.9, 2.6, "hash(key)\n% 8", mono=True, size=10)
    bucket_y = {i: 3.9 - i * 0.45 for i in range(8)}
    for i in range(8):
        sbox(ax, 5.0, bucket_y[i] - 0.36, 0.55, 0.36, str(i), color=PURPLE, mono=True, fontsize=9)
    for src_y, b in [(3.55, 3), (2.35, 6), (1.15, 3)]:
        arrow(ax, 3.85, src_y, 4.97, bucket_y[b] - 0.18, color=MUTED, lw=1.1)
    sbox(ax, 5.95, bucket_y[3] - 0.38, 1.6, 0.4, "cat → 4", color=BLUE, mono=True, fontsize=9)
    arrow(ax, 5.58, bucket_y[3] - 0.18, 5.92, bucket_y[3] - 0.18, lw=1.1)
    sbox(ax, 7.95, bucket_y[3] - 0.38, 1.6, 0.4, "owl → 2", color=BLUE, mono=True, fontsize=9)
    arrow(ax, 7.58, bucket_y[3] - 0.18, 7.92, bucket_y[3] - 0.18, lw=1.1)
    sbox(ax, 5.95, bucket_y[6] - 0.38, 1.6, 0.4, "dog → 7", color=BLUE, mono=True, fontsize=9)
    arrow(ax, 5.58, bucket_y[6] - 0.18, 5.92, bucket_y[6] - 0.18, lw=1.1)
    label(ax, 9.8, bucket_y[3] - 0.18, "collision:\na short chain", ha="left", size=9.5, color=MUTED)
    label(ax, 5.3, 0.15, "buckets", size=9.5, color=MUTED)
    return f


@fig("two-sum")
def two_sum():
    f, ax = diag.canvas(11.5, 3.9)
    nums = [2, 7, 11, 15]
    label(ax, 0.1, 3.5, "nums = [2, 7, 11, 15], target = 9", ha="left", bold=True, mono=True, size=10.5)
    rows = [("i = 0, x = 2", "need 7: not seen", "seen = {2: 0}", GREY),
            ("i = 1, x = 7", "need 2: seen at index 0!", "answer [0, 1]", GREEN)]
    for k, (a, b, c, col) in enumerate(rows):
        y = 2.5 - k * 1.1
        cells(ax, 0.2, y, nums, w=0.65, h=0.5, color=GREY, highlight={k: ORANGE}, fontsize=10)
        label(ax, 3.1, y + 0.25, a, ha="left", mono=True, size=10)
        label(ax, 5.3, y + 0.25, b, ha="left", size=10)
        sbox(ax, 8.6, y, 2.6, 0.5, c, color=col, mono=True, fontsize=9.5)
    label(ax, 5.75, 0.45, "for each x, look up target − x in a dict of the values already seen: O(1) per check", size=9.5, color=MUTED)
    return f


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names or FIGS:
        save(FIGS[name](), name)
    print(len(names or FIGS), "figures")


if __name__ == "__main__":
    main(sys.argv[1:])
