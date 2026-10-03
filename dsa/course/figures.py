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



# ---------------------------------------------------------------- Part 4: linked lists, stacks, queues

def lnode(ax, x, y, val, color=BLUE, w=0.95, h=0.6, fontsize=11):
    """A linked-list node: value cell plus a small pointer cell with a dot. Returns (left, right, mid_y)."""
    sbox(ax, x, y, w * 0.66, h, str(val), color=color, mono=True, fontsize=fontsize)
    sbox(ax, x + w * 0.66, y, w * 0.34, h, "", color=color)
    ax.add_patch(Circle((x + w * 0.83, y + h / 2), 0.05, color=INK, zorder=5))
    return x, x + w, y + h / 2


def chain(ax, x, y, vals, colors=None, gap=0.5, w=0.95, end="None"):
    colors = colors or {}
    lefts = []
    for i, v in enumerate(vals):
        left, right, my = lnode(ax, x, y, v, color=colors.get(i, BLUE), w=w)
        lefts.append(left)
        nxt = x + w + gap
        if i < len(vals) - 1:
            arrow(ax, right - w * 0.17, my, nxt - 0.02, my, lw=1.3)
        elif end:
            arrow(ax, right - w * 0.17, my, nxt - 0.02, my, lw=1.3)
            label(ax, nxt + 0.25, my, end, mono=True, size=10, color=MUTED, ha="left")
        x = nxt
    return lefts


@fig("linked-list")
def linked_list_fig():
    f, ax = diag.canvas(10, 3.4)
    label(ax, 0.2, 3.05, "A singly linked list", bold=True, ha="left", size=11)
    lefts = chain(ax, 1.4, 2.0, [3, 7, 1, 9])
    label(ax, 0.55, 2.3, "head", bold=True, size=10)
    arrow(ax, 0.85, 2.3, 1.38, 2.3, lw=1.3)
    label(ax, 0.2, 1.3, "push_front(5): O(1)", bold=True, ha="left", size=11)
    chain(ax, 1.4, 0.25, [5, 3, 7, 1, 9], colors={0: ORANGE})
    label(ax, 0.55, 0.55, "head", bold=True, size=10)
    arrow(ax, 0.85, 0.55, 1.38, 0.55, lw=1.3)
    label(ax, 7.6, 1.32, "one new node, one pointer change:\nnothing shifts", size=9.5, color=MUTED, ha="left")
    return f


@fig("doubly-linked")
def doubly_linked():
    f, ax = diag.canvas(10, 3.6)

    def row(y, vals, faded=None):
        xs = [0.3 + i * 1.75 for i in range(len(vals))]
        for i, (x, v) in enumerate(zip(xs, vals)):
            sent = v in ("head", "tail")
            sbox(ax, x, y, 1.05, 0.6, v, color=GREY if sent else (GREY if faded == i else BLUE), mono=not sent, fontsize=10 if sent else 11)
        for a, b in zip(xs, xs[1:]):
            arrow(ax, a + 1.07, y + 0.42, b - 0.02, y + 0.42, lw=1.2)
            arrow(ax, b - 0.02, y + 0.18, a + 1.07, y + 0.18, lw=1.2, color=MUTED)
        return xs

    label(ax, 0.3, 3.3, "next →  (top arrows)      ← prev  (bottom arrows, grey)", ha="left", size=9.5, color=MUTED)
    row(2.2, ["head", "a", "b", "c", "tail"])
    label(ax, 0.3, 1.45, "remove(b): b.prev.next = b.next;  b.next.prev = b.prev   (O(1))", ha="left", size=10, mono=True)
    row(0.3, ["head", "a", "c", "tail"])
    return f


@fig("reverse-list")
def reverse_list_fig():
    f, ax = diag.canvas(10.5, 4.6)
    states = [
        ("start", [], [1, 2, 3], "prev = None, cur = 1"),
        ("step 1", [1], [2, 3], "1 now points back to None"),
        ("step 2", [2, 1], [3], "2 points back to 1"),
        ("step 3", [3, 2, 1], [], "prev = 3 is the new head"),
    ]
    for r, (title, done, rest, note) in enumerate(states):
        y = 3.75 - r * 1.15
        label(ax, 0.1, y + 0.3, title, ha="left", bold=True, size=10)
        x = 1.2
        if done:
            for i, v in enumerate(done):
                lnode(ax, x, y, v, color=TEAL)
                if i < len(done) - 1:
                    arrow(ax, x + 0.8, y + 0.3, x + 1.43, y + 0.3, lw=1.2)
                x += 1.45
            label(ax, x - 0.5 + 0.35, y + 0.3, "→ None", mono=True, size=9.5, color=MUTED, ha="left")
            x += 0.9
        else:
            label(ax, x + 0.2, y + 0.3, "None", mono=True, size=9.5, color=MUTED)
            x += 0.9
        if rest:
            chain(ax, x, y, rest, colors={0: ORANGE}, gap=0.45, w=0.95)
        label(ax, 10.4, y + 0.3, note, ha="right", size=9.5, color=MUTED)
    label(ax, 1.2, 0.05, "teal = already reversed (read left to right: head of the reversed part first)   orange = cur", ha="left", size=9, color=MUTED)
    return f


@fig("fast-slow")
def fast_slow():
    f, ax = diag.canvas(10.5, 4.1)
    xs = [0.4 + i * 1.6 for i in range(6)]
    y = 1.9
    for i, (x, v) in enumerate(zip(xs, range(1, 7))):
        col = ORANGE if v == 3 else (CRIMSON if v == 5 else BLUE)
        lnode(ax, x, y, v, color=col)
        if i < 5:
            arrow(ax, x + 0.8, y + 0.3, xs[i + 1] - 0.02, y + 0.3, lw=1.2)
    ax.add_patch(FancyArrowPatch((xs[5] + 0.8, y + 0.62), (xs[2] + 0.4, y + 0.64), connectionstyle="arc3,rad=0.35",
                                 arrowstyle="-|>", mutation_scale=14, color=INK, linewidth=1.3))
    label(ax, 9.9, 3.75, "6 links back to 3: a cycle", size=9.5, color=MUTED, ha="right")
    label(ax, xs[4] + 0.47, y - 0.3, "slow and fast\nmeet at 5", size=9.5, color=INK)
    label(ax, xs[2] + 0.47, y - 0.3, "cycle start", size=9.5, color=INK)
    rows = [("slow (1 step):", "1 → 2 → 3 → 4 → 5"), ("fast (2 steps):", "1 → 3 → 5 → 3 → 5"),
            ("then from head and from 5, 1 step each:", "1 → 2 → 3  and  5 → 6 → 3: meet at the start")]
    for k, (a, b) in enumerate(rows):
        label(ax, 0.4, 0.95 - k * 0.38, a, ha="left", size=9.5, bold=True)
        label(ax, 4.6 if k == 2 else 2.2, 0.95 - k * 0.38, b, ha="left", size=9.5, mono=True)
    return f


@fig("stack-queue")
def stack_queue():
    f, ax = diag.canvas(10.5, 4.0)
    label(ax, 1.9, 3.75, "Stack: last in, first out", bold=True, size=11)
    for i, v in enumerate(["a", "b", "c"]):
        sbox(ax, 1.2, 0.4 + i * 0.75, 1.4, 0.65, v, color=ORANGE if v == "c" else BLUE, mono=True)
    arrow(ax, 3.3, 3.25, 2.7, 2.55, color=INK, lw=1.3)
    label(ax, 3.45, 3.3, "push", ha="left", size=10)
    arrow(ax, 2.7, 2.15, 3.3, 1.55, color=INK, lw=1.3)
    label(ax, 3.45, 1.5, "pop (c first)", ha="left", size=10)
    label(ax, 1.9, 0.1, "top = end of a Python list", size=9.5, color=MUTED)
    ax.plot([5.0, 5.0], [0.2, 3.8], color="#d0d6dd", linewidth=1)
    label(ax, 7.8, 3.75, "Queue: first in, first out", bold=True, size=11)
    for i, v in enumerate(["a", "b", "c"]):
        sbox(ax, 6.5 + i * 1.05, 1.6, 0.95, 0.65, v, color=ORANGE if v == "a" else BLUE, mono=True)
    arrow(ax, 6.4, 1.92, 5.6, 1.92, color=INK, lw=1.3)
    label(ax, 6.0, 1.25, "leaves\nfirst: a", size=9.5)
    arrow(ax, 10.3, 1.92, 9.7, 1.92, color=INK, lw=1.3)
    label(ax, 10.0, 1.25, "joins\nhere", size=9.5)
    label(ax, 7.9, 0.4, "use collections.deque: append + popleft", size=9.5, color=MUTED)
    return f


@fig("monotonic-stack")
def monotonic_stack_fig():
    f, ax = diag.canvas(11, 4.3)
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    cells(ax, 0.6, 3.2, temps, w=0.8, color=GREY, highlight={5: ORANGE, 3: TEAL, 4: TEAL, 2: BLUE}, idx="auto")
    label(ax, 0.1, 3.5, "day", ha="left", size=9, color=MUTED)
    label(ax, 7.4, 3.5, "temperatures", ha="left", size=9.5, color=MUTED)

    def stack(x, items, title, colors):
        label(ax, x + 0.55, 2.55, title, bold=True, size=10)
        for i, (d, t) in enumerate(items):
            sbox(ax, x, 0.35 + i * 0.6, 1.1, 0.52, f"{t} (d{d})", color=colors[i], mono=True, fontsize=9.5)
        label(ax, x + 0.55, 0.1, "bottom", size=8.5, color=MUTED)

    stack(0.8, [(2, 75), (3, 71), (4, 69)], "before day 5", [BLUE, TEAL, TEAL])
    arrow(ax, 2.3, 1.2, 3.4, 1.2, text="72 arrives", fontsize=9.5)
    label(ax, 5.9, 1.95, "pops 69 (day 4): answer 5 − 4 = 1 day", ha="left", size=9.5)
    label(ax, 5.9, 1.55, "pops 71 (day 3): answer 5 − 3 = 2 days", ha="left", size=9.5)
    label(ax, 5.9, 1.15, "stops at 75: warmer than 72", ha="left", size=9.5)
    label(ax, 5.9, 0.75, "pushes 72 (day 5)", ha="left", size=9.5)
    stack(3.7, [(2, 75), (5, 72)], "after", [BLUE, ORANGE])
    label(ax, 5.9, 0.3, "values always decrease from bottom to top", ha="left", size=9, color=MUTED)
    return f


@fig("circular-buffer")
def circular_buffer():
    f, ax = diag.canvas(9.0, 5.0)
    cx, cy, r = 3.0, 2.45, 1.7
    vals = {0: "4", 1: "5", 2: "·", 3: "·", 4: "2", 5: "3"}
    for i in range(6):
        ang = math.radians(90 - i * 60)
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        col = ORANGE if i == 4 else (TEAL if vals[i] != "·" else GREY)
        sbox(ax, x - 0.4, y - 0.3, 0.8, 0.6, vals[i], color=col, mono=True)
        label(ax, cx + (r + 0.75) * math.cos(ang), cy + (r + 0.75) * math.sin(ang), f"[{i}]", size=9, color=MUTED, mono=True)
    ax.add_patch(FancyArrowPatch((cx + 0.5, cy + 0.9), (cx + 0.9, cy - 0.5), connectionstyle="arc3,rad=-0.4",
                                 arrowstyle="-|>", mutation_scale=14, color=MUTED, linewidth=1.3))
    label(ax, cx, cy, "items move\nclockwise", size=9, color=MUTED)
    label(ax, 5.9, 4.1, "capacity 6, holding 2, 3, 4, 5", ha="left", size=9.5)
    label(ax, 5.9, 3.6, "head = 4 (oldest: 2)", ha="left", size=9.5)
    label(ax, 5.9, 3.1, "tail = (4 + 4) % 6 = 2", ha="left", size=9.5)
    label(ax, 5.9, 2.6, "4 and 5 wrapped round", ha="left", size=9.5)
    label(ax, 5.9, 2.1, "to slots 0 and 1", ha="left", size=9.5)
    return f


@fig("sliding-max")
def sliding_max():
    from collections import deque
    f, ax = diag.canvas(11, 4.6)
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    cells(ax, 0.3, 3.75, nums, w=0.8, color=GREY, idx="auto", idx_y=3.55 + 0.9)
    k, dq, row = 3, deque(), 0
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            y = 3.05 - row * 0.5
            ax.add_patch(Rectangle((0.3 + (i - k + 1) * 0.8 - 0.03, y), k * 0.8 - 0.03, 0.36, facecolor=SOFT[BLUE], edgecolor=BLUE, linewidth=1))
            label(ax, 0.3 + (i - k + 1) * 0.8 + k * 0.4, y + 0.18, "window", size=8, color=MUTED)
            label(ax, 7.0, y + 0.18, "deque: " + ", ".join(str(nums[j]) for j in dq), ha="left", size=9.5, mono=True)
            label(ax, 10.9, y + 0.18, f"max {nums[dq[0]]}", ha="right", size=9.5, bold=True)
            row += 1
    return f


@fig("lru-cache")
def lru_cache_fig():
    f, ax = diag.canvas(11.5, 4.4)
    label(ax, 0.3, 4.1, "dict: key → node", bold=True, size=10, ha="left")
    for i, k in enumerate(["a", "b", "c"]):
        sbox(ax, 0.3, 3.15 - i * 0.6, 0.6, 0.48, k, color=GREY, mono=True)
    def dll(y, order, hl):
        xs = [2.6 + i * 1.7 for i in range(len(order))]
        for x, v in zip(xs, order):
            sent = v in ("head", "tail")
            sbox(ax, x, y, 1.1, 0.55, v, color=GREY if sent else (ORANGE if v == hl else BLUE), mono=not sent, fontsize=9.5 if sent else 11)
        for a, b in zip(xs, xs[1:]):
            arrow(ax, a + 1.12, y + 0.38, b - 0.02, y + 0.38, lw=1.1)
            arrow(ax, b - 0.02, y + 0.17, a + 1.12, y + 0.17, lw=1.1, color=MUTED)
        return xs
    xs = dll(2.6, ["head", "a", "b", "c", "tail"], None)
    for i, k in enumerate(["a", "b", "c"]):
        ax.add_patch(FancyArrowPatch((0.92, 3.39 - i * 0.6), (xs[i + 1] + 0.55, 3.18), connectionstyle="arc3,rad=-0.15",
                                     arrowstyle="-|>", mutation_scale=11, color=GREY, linewidth=1))
    label(ax, xs[1] + 0.55, 2.3, "least recent\n(evicted first)", size=9, color=MUTED)
    label(ax, xs[3] + 0.55, 2.3, "most recent", size=9, color=MUTED)
    label(ax, 0.3, 1.35, "after get(a):", bold=True, size=10, ha="left")
    dll(0.75, ["head", "b", "c", "a", "tail"], "a")
    label(ax, 2.6, 0.25, "unlink a's node, re-insert it before tail: a few pointer changes, O(1)", ha="left", size=9.5, color=MUTED)
    return f



# ---------------------------------------------------------------- Part 5: recursion

@fig("call-stack")
def call_stack():
    f, ax = diag.canvas(10.5, 4.2)
    label(ax, 2.4, 3.95, "calls go down (frames pushed)", bold=True, size=10.5)
    label(ax, 8.0, 3.95, "returns come back up (frames popped)", bold=True, size=10.5)
    rows = [(4, "4 × factorial(3)", "= 4 × 6 = 24"), (3, "3 × factorial(2)", "= 3 × 2 = 6"),
            (2, "2 × factorial(1)", "= 2 × 1 = 2"), (1, "base case", "returns 1")]
    for i, (n, waiting, ret) in enumerate(rows):
        y = 3.05 - i * 0.8
        col = ORANGE if n == 1 else BLUE
        sbox(ax, 0.3 + i * 0.35, y, 3.6, 0.6, f"factorial({n}):  {waiting}", color=col, mono=True, fontsize=9.5)
        sbox(ax, 6.3, y, 3.6, 0.6, f"factorial({n}) {ret}", color=TEAL if n != 1 else ORANGE, mono=True, fontsize=9.5)
        if i < 3:
            arrow(ax, 2.1 + i * 0.35, y - 0.02, 2.1 + (i + 1) * 0.35, y - 0.18, lw=1.1, color=MUTED)
            arrow(ax, 8.1, y - 0.18, 8.1, y - 0.02, lw=1.1, color=MUTED)
    label(ax, 5.25, 0.15, "each frame waits for the answer from the frame below it", size=9.5, color=MUTED)
    return f


@fig("fib-tree")
def fib_tree():
    f, ax = diag.canvas(12, 4.6)
    pos = {}

    def leaves(n):
        return 1 if n < 2 else leaves(n - 1) + leaves(n - 2)

    def layout(n, x0, depth, path):
        width = leaves(n) * 1.45
        x = x0 + width / 2
        y = 4.0 - depth * 0.95
        pos[path] = (x, y, n)
        if n >= 2:
            layout(n - 1, x0, depth + 1, path + "L")
            layout(n - 2, x0 + leaves(n - 1) * 1.45, depth + 1, path + "R")

    layout(5, 0.2, 0, "")
    for p, (x, y, n) in pos.items():
        if p:
            px, py, _ = pos[p[:-1]]
            ax.plot([px, x], [py - 0.2, y + 0.2], color=GREY, linewidth=1, zorder=1)
    colors = {3: ORANGE, 2: CRIMSON}
    for p, (x, y, n) in pos.items():
        c = colors.get(n, BLUE if n > 1 else GREY)
        sbox(ax, x - 0.42, y - 0.2, 0.84, 0.42, f"fib({n})", color=c, mono=True, fontsize=8.5)
    label(ax, 11.8, 4.3, "orange fib(3) is computed 2 times, crimson fib(2) 3 times", ha="right", size=9.5, color=MUTED)
    return f


@fig("divide-conquer")
def divide_conquer():
    f, ax = diag.canvas(12, 5.2)
    levels_down = [[[38, 27, 43, 3, 9, 82, 10]], [[38, 27, 43, 3], [9, 82, 10]], [[38, 27], [43, 3], [9, 82], [10]],
                   [[38], [27], [43], [3], [9], [82], [10]]]
    levels_up = [[[27, 38], [3, 43], [9, 82], [10]], [[3, 27, 38, 43], [9, 10, 82]], [[3, 9, 10, 27, 38, 43, 82]]]

    def draw(level, y, color):
        total = sum(len(g) for g in level) + (len(level) - 1) * 0.8
        x = 6.0 - total * 0.36 / 1.0
        for g in level:
            for v in g:
                sbox(ax, x, y, 0.66, 0.42, str(v), color=color, mono=True, fontsize=9)
                x += 0.72
            x += 0.8 * 0.72
    for i, lv in enumerate(levels_down):
        draw(lv, 4.55 - i * 0.62, BLUE)
    for i, lv in enumerate(levels_up):
        draw(lv, 1.95 - i * 0.62, TEAL if i < 2 else ORANGE)
    label(ax, 0.2, 3.7, "divide", ha="left", bold=True, size=10.5)
    label(ax, 0.2, 1.3, "combine\n(merge)", ha="left", bold=True, size=10.5)
    return f


@fig("backtracking-tree")
def backtracking_tree():
    f, ax = diag.canvas(12, 4.5)
    nodes = {}

    def layout(i, x0, x1, path):
        x = (x0 + x1) / 2
        y = 3.9 - i * 1.15
        nodes[tuple(path)] = (x, y)
        if i < 3:
            layout(i + 1, x0, x, path + [i + 1])
            layout(i + 1, x, x1, path)

    layout(0, 0.2, 11.8, [])
    for p, (x, y) in nodes.items():
        depth = round((3.9 - y) / 1.15)
        for child_inc in (True, False):
            cp = tuple(list(p) + [depth + 1]) if child_inc else p
            key = cp
            if depth < 3:
                # find child positions by depth
                pass
    def kids(p, depth):
        return [tuple(list(p) + [depth + 1]), p]
    drawn = set()
    def walk(p, depth, x0, x1):
        x, y = (x0 + x1) / 2, 3.9 - depth * 1.15
        if depth < 3:
            xm = (x0 + x1) / 2
            for k, (cx0, cx1, txt) in enumerate([(x0, xm, f"+{depth + 1}"), (xm, x1, f"skip {depth + 1}")]):
                cx, cy = (cx0 + cx1) / 2, 3.9 - (depth + 1) * 1.15
                ax.plot([x, cx], [y - 0.2, cy + 0.2], color=GREY, linewidth=1, zorder=1)
                ax.text((x + cx) / 2 + (-0.12 if k == 0 else 0.12), (y + cy) / 2, txt, fontsize=8, color=MUTED,
                        ha="right" if k == 0 else "left", va="center")
            walk(tuple(list(p) + [depth + 1]), depth + 1, x0, xm)
            walk(p, depth + 1, xm, x1)
        txt = "[" + ", ".join(map(str, p)) + "]"
        c = TEAL if depth == 3 else BLUE
        w = max(0.62, 0.17 * len(txt) + 0.15)
        sbox(ax, x - w / 2, y - 0.2, w, 0.4, txt, color=c, mono=True, fontsize=8.5)
    walk((), 0, 0.2, 11.8)
    label(ax, 0.2, 0.05, "leaves (teal) = the 8 subsets", ha="left", size=9.5, color=MUTED)
    return f


@fig("n-queens")
def n_queens():
    f, ax = diag.canvas(5.4, 4.8)
    sol = [1, 3, 0, 2]
    q0r, q0c = 0, 1
    for r in range(4):
        for c in range(4):
            attacked = (c == q0c or r - c == q0r - q0c or r + c == q0r + q0c) and (r, c) != (q0r, q0c)
            fill = SOFT[CRIMSON] if attacked else ("#f4f5f7" if (r + c) % 2 else "white")
            ax.add_patch(Rectangle((0.4 + c * 0.95, 3.6 - r * 0.95), 0.95, 0.95, facecolor=fill, edgecolor="#cbd2d9", linewidth=1))
            if sol[r] == c:
                ax.text(0.4 + c * 0.95 + 0.475, 3.6 - r * 0.95 + 0.475, "♛", fontsize=22, ha="center", va="center", color=INK)
        label(ax, 0.15, 3.6 - r * 0.95 + 0.475, f"row {r}", size=8.5, color=MUTED, ha="right")
    for c in range(4):
        label(ax, 0.4 + c * 0.95 + 0.475, 4.75, f"col {c}", size=8.5, color=MUTED)
    label(ax, 2.3, 0.25, "shaded: squares the row-0 queen attacks", size=9, color=MUTED)
    return f



# ---------------------------------------------------------------- Part 6: searching and sorting

@fig("binary-search")
def binary_search_fig():
    f, ax = diag.canvas(11.5, 4.4)
    vals = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    steps = [(0, 9, 4, "16 < 23: low = mid + 1"), (5, 9, 7, "56 > 23: high = mid − 1"), (5, 6, 5, "23 found at index 5")]
    for r, (lo, hi, mid, note) in enumerate(steps):
        y = 3.3 - r * 1.35
        hl = {i: GREY for i in range(len(vals)) if i < lo or i > hi}
        hl.update({mid: ORANGE if r < 2 else TEAL})
        for i, v in enumerate(vals):
            c = hl.get(i, BLUE)
            sbox(ax, 0.3 + i * 0.75, y, 0.69, 0.55, str(v), color=c, mono=True, fontsize=10)
            if r == 0:
                label(ax, 0.3 + i * 0.75 + 0.345, y + 0.78, str(i), size=8.5, color=MUTED, mono=True)
        for name, idx, dy in (("lo", lo, -0.25), ("hi", hi, -0.25), ("mid", mid, -0.25)):
            if name == "mid" and idx in (lo, hi):
                continue
            label(ax, 0.3 + idx * 0.75 + 0.345, y + dy, name, size=8.5, color=INK, bold=name == "mid")
        if mid in (lo, hi):
            label(ax, 0.3 + mid * 0.75 + 0.345, y - 0.45, "mid", size=8.5, color=INK, bold=True)
        label(ax, 8.0, y + 0.27, f"step {r + 1}: {note}", ha="left", size=9.5)
    label(ax, 0.3, 0.05, "grey = ruled out; each step halves what's left", ha="left", size=9, color=MUTED)
    return f


@fig("answer-search")
def answer_search():
    f, ax = diag.canvas(11, 2.8)
    caps = list(range(10, 22))
    def days(c):
        d, load = 1, 0
        for w in range(1, 11):
            if load + w > c:
                d += 1
                load = 0
            load += w
        return d
    for i, c in enumerate(caps):
        ok = days(c) <= 5
        sbox(ax, 0.3 + i * 0.85, 1.25, 0.78, 0.6, str(c), color=TEAL if ok else CRIMSON, mono=True, fontsize=10)
        label(ax, 0.3 + i * 0.85 + 0.39, 1.0, "yes" if ok else "no", size=8.5, color=INK)
    first = next(i for i, c in enumerate(caps) if days(c) <= 5)
    arrow(ax, 0.3 + first * 0.85 + 0.39, 2.55, 0.3 + first * 0.85 + 0.39, 1.93, lw=1.3)
    label(ax, 0.3 + first * 0.85 + 0.6, 2.55, "first yes = the answer (15)", ha="left", size=10, bold=True)
    label(ax, 0.3, 2.3, "candidate capacities", ha="left", size=9.5, color=MUTED)
    label(ax, 0.3, 0.45, "test: can packages 1..10 ship within 5 days?  once yes, always yes, so binary search finds the boundary",
          ha="left", size=9.5, color=MUTED)
    return f


@fig("insertion-sort")
def insertion_sort_fig():
    f, ax = diag.canvas(9.5, 5.0)
    a = [5, 2, 4, 6, 1, 3]
    rows = [list(a)]
    for i in range(1, len(a)):
        item, j = a[i], i - 1
        while j >= 0 and a[j] > item:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = item
        rows.append((list(a), j + 1, i))
    cells(ax, 0.9, 4.25, rows[0], w=0.8, color=GREY)
    label(ax, 0.1, 4.55, "start", ha="left", size=9.5, bold=True)
    for r, (vals, placed, i) in enumerate(rows[1:]):
        y = 3.55 - r * 0.72
        hl = {k: TEAL for k in range(i + 1)}
        hl[placed] = ORANGE
        hl.update({k: GREY for k in range(i + 1, len(vals))})
        cells(ax, 0.9, y, vals, w=0.8, color=GREY, highlight=hl)
        label(ax, 0.1, y + 0.3, f"i = {i}", ha="left", size=9.5, bold=True)
        label(ax, 5.9, y + 0.3, f"insert {vals[placed]} at position {placed}", ha="left", size=9.5, color=MUTED)
    label(ax, 0.9, 0.05, "teal = sorted part, orange = the item just inserted", ha="left", size=9, color=MUTED)
    return f


@fig("quick-partition")
def quick_partition():
    f, ax = diag.canvas(10.5, 4.6)
    a = [7, 2, 1, 8, 6, 3, 5, 4]
    pivot = a[-1]
    states = [(list(a), 0, None, "start: pivot = 4 (last item), i = 0")]
    i = 0
    for j in range(len(a) - 1):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
            states.append((list(a), i, j, f"j = {j}: {a[i - 1]} < 4 → swap into the left region, i = {i}"))
    a[i], a[-1] = a[-1], a[i]
    states.append((list(a), i, None, f"finally swap the pivot into position {i}"))
    for r, (vals, iv, j, note) in enumerate(states):
        y = 3.85 - r * 0.8
        hl = {k: TEAL for k in range(iv if r < len(states) - 1 else iv)}
        if r == len(states) - 1:
            hl[iv] = ORANGE
        else:
            hl[len(vals) - 1] = ORANGE
        cells(ax, 0.3, y, vals, w=0.7, color=BLUE, highlight=hl)
        label(ax, 6.1, y + 0.3, note, ha="left", size=9)
    label(ax, 0.3, 0.05, "teal = smaller than the pivot; orange = the pivot", ha="left", size=9, color=MUTED)
    return f


@fig("counting-sort")
def counting_sort_fig():
    f, ax = diag.canvas(10, 3.8)
    nums = [4, 2, 2, 8, 3, 3, 1]
    label(ax, 0.3, 3.5, "input", ha="left", size=9.5, bold=True)
    cells(ax, 1.3, 3.2, nums, w=0.7, color=BLUE)
    counts = [nums.count(v) for v in range(9)]
    label(ax, 0.3, 2.15, "counts", ha="left", size=9.5, bold=True)
    cells(ax, 1.3, 1.85, counts, w=0.7, color=TEAL, highlight={v: GREY for v in range(9) if counts[v] == 0}, idx="auto", idx_y=2.68)
    label(ax, 7.8, 2.15, "index = value", ha="left", size=9, color=MUTED)
    label(ax, 0.3, 0.75, "output", ha="left", size=9.5, bold=True)
    cells(ax, 1.3, 0.45, sorted(nums), w=0.7, color=ORANGE)
    label(ax, 7.0, 0.75, "read the counts from 0 upward", ha="left", size=9, color=MUTED)
    return f


# ---------------------------------------------------------------- Part 7: trees and heaps

def tnode(ax, x, y, val, color=BLUE, r=0.3, lw=1.6, fontsize=11, edge=None):
    ax.add_patch(Circle((x, y), r, facecolor=SOFT.get(color, "white"), edgecolor=edge or color, linewidth=lw, zorder=3))
    ax.text(x, y, str(val), ha="center", va="center", fontsize=fontsize, color=INK, family="monospace", zorder=4)


def tedge(ax, a, b, r=0.3, color=GREY, lw=1.2, dashed=False, r2=None):
    (x1, y1), (x2, y2) = a, b
    r2 = r if r2 is None else r2
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    ax.plot([x1 + ux * r, x2 - ux * r2], [y1 + uy * r, y2 - uy * r2], color=color, linewidth=lw, zorder=1,
            linestyle="--" if dashed else "-")


def draw_tree(ax, pos, edges, colors=None, r=0.3, fontsize=11, edge_colors=None, default=BLUE, lw=None):
    """pos: {key: (x, y, label)}; edges: [(parent, child)]; colors / edge_colors / lw: per key or edge."""
    colors, edge_colors, lw = colors or {}, edge_colors or {}, lw or {}
    for a, b in edges:
        c = edge_colors.get((a, b), GREY)
        tedge(ax, pos[a][:2], pos[b][:2], r=r, color=c, lw=2.2 if c != GREY else 1.2)
    for k, (x, y, val) in pos.items():
        tnode(ax, x, y, val, color=colors.get(k, default), r=r, fontsize=fontsize, lw=lw.get(k, 1.6))


@fig("binary-tree")
def binary_tree_fig():
    f, ax = diag.canvas(9.6, 4.3)
    pos = {1: (4.0, 3.65, 1), 2: (2.4, 2.45, 2), 3: (5.6, 2.45, 3), 4: (1.6, 1.25, 4), 5: (3.2, 1.25, 5), 6: (6.4, 1.25, 6)}
    draw_tree(ax, pos, [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)], colors={1: ORANGE, 4: TEAL, 5: TEAL, 6: TEAL})
    label(ax, 3.55, 3.65, "root", ha="right", size=9.5, color=MUTED)
    label(ax, 1.95, 2.45, "parent of 4 and 5", ha="right", size=9.5, color=MUTED)
    label(ax, 4.0, 0.62, "leaves (no children): 4, 5, 6", size=9.5, color=MUTED)
    for y, d in [(3.65, 0), (2.45, 1), (1.25, 2)]:
        ax.plot([7.1, 7.6], [y, y], color="#cbd2d9", linewidth=1, linestyle=":")
        label(ax, 7.7, y, f"depth {d}", ha="left", size=9.5, color=MUTED)
    label(ax, 4.0, 0.15, "height = 2 (edges on the longest root-to-leaf path)", size=9.5, color=MUTED)
    return f


@fig("tree-diameter")
def tree_diameter_fig():
    f, ax = diag.canvas(8.4, 4.6)
    pos = {1: (4.6, 4.0, 1), 2: (3.4, 3.0, 2), 4: (2.0, 2.0, 4), 5: (4.8, 2.0, 5), 6: (1.2, 1.0, 6), 7: (5.6, 1.0, 7)}
    path = [(2, 4), (2, 5), (4, 6), (5, 7)]
    draw_tree(ax, pos, [(1, 2)] + path, colors={k: ORANGE for k in (2, 4, 5, 6, 7)}, edge_colors={e: ORANGE for e in path})
    label(ax, 5.05, 4.0, "root", ha="left", size=9.5, color=MUTED)
    label(ax, 3.4, 0.25, "diameter: 6 → 4 → 2 → 5 → 7 = 4 edges", size=10, bold=True, color=ORANGE)
    label(ax, 6.3, 2.75, "the longest path through\nthe root has only 3 edges", ha="left", size=9.5, color=MUTED)
    return f


BST_POS = {8: (4.0, 4.0), 3: (2.2, 3.0), 10: (5.8, 3.0), 1: (1.2, 2.0), 6: (3.2, 2.0), 14: (6.8, 2.0), 4: (2.6, 1.0), 7: (3.8, 1.0), 13: (6.2, 1.0)}
BST_EDGES = [(8, 3), (8, 10), (3, 1), (3, 6), (10, 14), (6, 4), (6, 7), (14, 13)]


def bst_tree(ax, dx=0.0, scale=1.0, colors=None, edge_colors=None, skip=(), r=0.3):
    pos = {k: (dx + x * scale, y, k) for k, (x, y) in BST_POS.items() if k not in skip}
    edges = [e for e in BST_EDGES if e[0] in pos and e[1] in pos]
    draw_tree(ax, pos, edges, colors=colors, edge_colors=edge_colors, r=r, fontsize=10.5)
    return pos


@fig("bst")
def bst_fig():
    f, ax = diag.canvas(10.2, 4.6)
    path = [(8, 3), (3, 6), (6, 7)]
    pos = bst_tree(ax, dx=0.2, colors={8: ORANGE, 3: ORANGE, 6: ORANGE, 7: GREEN}, edge_colors={e: ORANGE for e in path})
    for (a, b), txt in zip(path, ["7 < 8: left", "7 > 3: right", "7 > 6: right"]):
        (x1, y1, _), (x2, y2, _) = pos[a], pos[b]
        label(ax, (x1 + x2) / 2 + (0.25 if x2 > x1 else -0.25), (y1 + y2) / 2 + 0.1, txt,
              ha="left" if x2 > x1 else "right", size=9, color=ORANGE)
    label(ax, 7.6, 3.6, "search for 7:", ha="left", size=10, bold=True)
    label(ax, 7.6, 3.15, "4 nodes visited", ha="left", size=9.5, color=MUTED)
    label(ax, 7.6, 2.4, "left subtree < node", ha="left", size=9.5, color=MUTED)
    label(ax, 7.6, 2.0, "right subtree > node", ha="left", size=9.5, color=MUTED)
    label(ax, 7.6, 1.3, "inorder: 1 3 4 6 7 8 10 13 14", ha="left", size=9.5, color=MUTED, mono=True)
    return f


@fig("bst-delete")
def bst_delete_fig():
    f, ax = diag.canvas(14.0, 5.0)
    s = 0.55
    # 1. a leaf
    bst_tree(ax, dx=0.0, scale=s, colors={4: CRIMSON}, r=0.24)
    label(ax, 2.2, 4.75, "1. leaf: delete 4", bold=True, size=10.5)
    label(ax, 2.2, 0.3, "just remove it", size=9.5, color=MUTED)
    # 2. one child
    dx = 4.5
    pos = bst_tree(ax, dx=dx, scale=s, colors={10: CRIMSON, 14: TEAL}, r=0.24)
    (x8, y8, _), (x14, y14, _) = pos[8], pos[14]
    ax.add_patch(FancyArrowPatch((x8 + 0.2, y8 - 0.15), (x14 + 0.05, y14 + 0.25), arrowstyle="-|>", mutation_scale=12,
                                 color=ORANGE, linewidth=1.6, linestyle="--", connectionstyle="arc3,rad=-0.45"))
    label(ax, dx + 2.2, 4.75, "2. one child: delete 10", bold=True, size=10.5)
    label(ax, dx + 2.2, 0.3, "8 links straight to 14", size=9.5, color=MUTED)
    # 3. two children
    dx = 9.8
    pos = bst_tree(ax, dx=dx, scale=s, colors={3: CRIMSON, 4: ORANGE}, r=0.24)
    (x3, y3, _), (x4, y4, _) = pos[3], pos[4]
    ax.add_patch(FancyArrowPatch((x4 - 0.22, y4 + 0.05), (x3 - 0.22, y3 - 0.12), arrowstyle="-|>", mutation_scale=12,
                                 color=ORANGE, linewidth=1.6, connectionstyle="arc3,rad=-0.5"))
    label(ax, x4 - 0.95, (y3 + y4) / 2 - 0.05, "copy 4 up", ha="right", size=9, color=ORANGE)
    label(ax, dx + 2.2, 4.75, "3. two children: delete 3", bold=True, size=10.5)
    label(ax, dx + 2.2, 0.3, "successor 4 = leftmost of the right subtree;\ncopy it into 3's place, then delete the old 4", size=9.5, color=MUTED)
    return f


def subtree(ax, x, y, name, color=GREY, w=0.7, h=0.75):
    from matplotlib.patches import Polygon
    ax.add_patch(Polygon([(x, y), (x - w / 2, y - h), (x + w / 2, y - h)], closed=True, facecolor=SOFT.get(color, "#eef1f4"),
                         edgecolor=color, linewidth=1.4, zorder=2))
    ax.text(x, y - h * 0.62, name, ha="center", va="center", fontsize=11, color=INK, zorder=4)


@fig("rotation")
def rotation_fig():
    f, ax = diag.canvas(10.6, 4.2)
    # before
    y_, x_ = (2.6, 3.4), (1.6, 2.4)
    tedge(ax, y_, x_, r=0.32)
    for (a, b) in [((x_[0], x_[1]), (0.9, 1.45)), ((x_[0], x_[1]), (2.3, 1.45)), ((y_[0], y_[1]), (3.5, 2.45))]:
        tedge(ax, a, b, r=0.32, r2=0, color=GREY)
    tnode(ax, *y_, "y", color=ORANGE, r=0.32)
    tnode(ax, *x_, "x", color=BLUE, r=0.32)
    subtree(ax, 0.9, 1.45, "A")
    subtree(ax, 2.3, 1.45, "B", color=TEAL)
    subtree(ax, 3.5, 2.45, "C")
    label(ax, 2.2, 0.25, "before", bold=True)
    arrow(ax, 4.6, 2.5, 6.0, 2.5, color=INK, text="rotate right at y", fontsize=9.5)
    # after
    X, Y = (7.8, 3.4), (8.8, 2.4)
    tedge(ax, X, Y, r=0.32)
    for (a, b) in [(X, (7.1, 2.45)), (Y, (8.1, 1.45)), (Y, (9.5, 1.45))]:
        tedge(ax, a, b, r=0.32, r2=0, color=GREY)
    tnode(ax, *X, "x", color=BLUE, r=0.32)
    tnode(ax, *Y, "y", color=ORANGE, r=0.32)
    subtree(ax, 7.1, 2.45, "A")
    subtree(ax, 8.1, 1.45, "B", color=TEAL)
    subtree(ax, 9.5, 1.45, "C")
    label(ax, 8.4, 0.25, "after", bold=True)
    label(ax, 5.3, 1.3, "inorder stays\nA  x  B  y  C", size=9.5, color=MUTED)
    return f


@fig("heap-array")
def heap_array_fig():
    f, ax = diag.canvas(10.0, 5.2)
    vals = [1, 3, 2, 7, 4, 5, 8]
    xs = {0: 4.6, 1: 2.8, 2: 6.4, 3: 1.9, 4: 3.7, 5: 5.5, 6: 7.3}
    ys = {0: 4.45, 1: 3.55, 2: 3.55, 3: 2.65, 4: 2.65, 5: 2.65, 6: 2.65}
    pos = {i: (xs[i], ys[i], vals[i]) for i in range(7)}
    edges = [(i, c) for i in range(7) for c in (2 * i + 1, 2 * i + 2) if c < 7]
    draw_tree(ax, pos, edges, colors={1: ORANGE, 3: TEAL, 4: TEAL}, r=0.28, fontsize=10.5)
    for i in range(7):
        label(ax, xs[i] + 0.36, ys[i] + 0.25, f"[{i}]", ha="left", size=8.5, color=MUTED, mono=True)
    w, x0, y0 = 0.9, 1.45, 1.1
    cells(ax, x0, y0, vals, w=w, highlight={1: ORANGE, 3: TEAL, 4: TEAL}, idx="auto")
    cx = lambda i: x0 + i * w + (w - 0.06) / 2
    arrow(ax, cx(1), y0 - 0.05, cx(3) - 0.05, y0 - 0.05, color=TEAL, lw=1.3, rad=0.5)
    arrow(ax, cx(1) + 0.05, y0 - 0.05, cx(4), y0 - 0.05, color=TEAL, lw=1.3, rad=0.55)
    label(ax, cx(3) + 0.2, y0 - 0.85, "children of index 1: 2·1 + 1 = 3 and 2·1 + 2 = 4", ha="left", size=9.5, color=MUTED)
    label(ax, 8.2, 3.9, "every parent ≤ its children", ha="left", size=9.5, color=MUTED)
    label(ax, 8.2, 3.5, "smallest at index 0", ha="left", size=9.5, color=MUTED)
    return f


@fig("two-heaps")
def two_heaps_fig():
    f, ax = diag.canvas(9.6, 4.0)
    low = {0: (2.0, 2.9, 3), 1: (1.2, 1.9, 1), 2: (2.8, 1.9, 2)}
    high = {0: (7.6, 2.9, 5), 1: (6.8, 1.9, 8), 2: (8.4, 1.9, 9)}
    draw_tree(ax, low, [(0, 1), (0, 2)], colors={0: ORANGE}, default=BLUE)
    draw_tree(ax, high, [(0, 1), (0, 2)], colors={0: ORANGE}, default=TEAL)
    label(ax, 2.0, 3.65, "lower half: max-heap", bold=True, size=10.5)
    label(ax, 7.6, 3.65, "upper half: min-heap", bold=True, size=10.5)
    label(ax, 2.0, 1.25, "top = largest of the small numbers", size=9, color=MUTED)
    label(ax, 7.6, 1.25, "top = smallest of the big numbers", size=9, color=MUTED)
    sbox(ax, 3.4, 2.6, 2.8, 0.6, "median = (3 + 5) / 2 = 4", color=ORANGE, fontsize=9.5)
    arrow(ax, 2.35, 2.95, 3.35, 2.92, color=ORANGE, lw=1.3)
    arrow(ax, 7.25, 2.95, 6.25, 2.92, color=ORANGE, lw=1.3)
    label(ax, 4.8, 0.45, "every number in the lower half ≤ every number in the upper half; sizes differ by at most 1", size=9, color=MUTED)
    return f


@fig("trie")
def trie_fig():
    f, ax = diag.canvas(8.6, 5.0)
    pos = {"": (4.2, 4.5, "·"), "c": (2.6, 3.5, "c"), "d": (5.8, 3.5, "d"), "ca": (2.6, 2.5, "a"), "do": (5.8, 2.5, "o"),
           "car": (1.8, 1.5, "r"), "cat": (3.4, 1.5, "t"), "dog": (5.8, 1.5, "g"), "cart": (1.8, 0.5, "t")}
    edges = [("", "c"), ("", "d"), ("c", "ca"), ("d", "do"), ("ca", "car"), ("ca", "cat"), ("do", "dog"), ("car", "cart")]
    words = {"car", "cat", "cart", "do", "dog"}
    lw = {k: 3.2 for k in words}
    colors = {k: GREEN for k in words}
    colors[""] = GREY
    draw_tree(ax, pos, edges, colors=colors, lw=lw, r=0.28)
    for k in words:
        x, y, _ = pos[k]
        label(ax, x + 0.42, y, f'"{k}"', ha="left", size=9, color=MUTED, mono=True)
    label(ax, 4.62, 4.5, "root (empty string)", ha="left", size=9, color=MUTED)
    label(ax, 6.9, 0.9, "thick green border:\na word ends here", ha="left", size=9, color=GREEN)
    return f


@fig("fenwick")
def fenwick_fig():
    f, ax = diag.canvas(11.8, 5.0)
    nums = [5, 8, 6, 3, 2, 7, 2, 6]
    w, x0 = 1.25, 1.6
    label(ax, 0.2, 4.55, "nums", ha="left", size=9.5, bold=True)
    cells(ax, x0, 4.25, nums, w=w, color=BLUE, idx=list(range(1, 9)), idx_y=4.98)
    label(ax, 0.2, 4.98, "position", ha="left", size=8.5, color=MUTED)
    tree = [0] * 9
    for i in range(1, 9):
        tree[i] = sum(nums[i - (i & -i):i])
    hl = {7, 6, 4}
    for i in range(1, 9):
        low = i & -i
        level = int(math.log2(low))
        y = 3.35 - level * 0.85
        xa = x0 + (i - low) * w
        xb = x0 + i * w - 0.06
        c = ORANGE if i in hl else TEAL
        sbox(ax, xa, y, xb - xa, 0.5, f"tree[{i}] = {tree[i]}", color=c, fontsize=8.5, mono=True)
    label(ax, 0.2, 3.6, "covers 1", ha="left", size=8.5, color=MUTED)
    label(ax, 0.2, 2.75, "covers 2", ha="left", size=8.5, color=MUTED)
    label(ax, 0.2, 1.9, "covers 4", ha="left", size=8.5, color=MUTED)
    label(ax, 0.2, 1.05, "covers 8", ha="left", size=8.5, color=MUTED)
    label(ax, 5.9, 0.3, "prefix(7) = tree[7] + tree[6] + tree[4] = 2 + 9 + 22 = 33   (7 → 6 → 4 → 0: drop the lowest bit)",
          size=9.5, color=ORANGE)
    return f


@fig("segment-tree")
def segment_tree_fig():
    f, ax = diag.canvas(12.4, 4.9)
    nums = [5, 8, 6, 3, 2, 7, 2, 6]
    w, x0 = 1.45, 0.5
    hl = {(2, 3), (4, 5), (6, 6)}

    def node(lo, hi, depth):
        total = sum(nums[lo:hi + 1])
        width = (hi - lo + 1) * w - 0.12
        x = x0 + lo * w
        y = 4.0 - depth * 1.1
        c = ORANGE if (lo, hi) in hl else (BLUE if lo != hi else TEAL)
        txt = f"{total}  [{lo}]" if lo == hi else f"{total}  [{lo}–{hi}]"
        sbox(ax, x, y, width, 0.5, txt, color=c, fontsize=9.5, mono=True)
        if lo != hi:
            mid = (lo + hi) // 2
            for a, b in ((lo, mid), (mid + 1, hi)):
                cx = x0 + (a + b + 1) / 2 * w - 0.06
                ax.plot([x + width / 2, cx], [y, y - 0.6], color=GREY, linewidth=1, zorder=1)
            node(lo, mid, depth + 1)
            node(mid + 1, hi, depth + 1)
    node(0, 7, 0)
    label(ax, 6.3, 0.3, "sum of indexes 2..6 = 9 + 9 + 2 = 20: three covering nodes instead of five leaves", size=9.5, color=ORANGE)
    return f


# ---------------------------------------------------------------- Part 8: graphs

def dedge(ax, a, b, r=0.3, color=GREY, lw=1.3, rad=0.0):
    """A directed edge from circle a to circle b."""
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    ax.add_patch(FancyArrowPatch((x1 + ux * r, y1 + uy * r), (x2 - ux * r, y2 - uy * r), arrowstyle="-|>",
                                 mutation_scale=12, color=color, linewidth=lw, connectionstyle=f"arc3,rad={rad}", zorder=2))


def wlabel(ax, a, b, text, color=INK, dx=0.0, dy=0.0, size=9.5):
    ax.text((a[0] + b[0]) / 2 + dx, (a[1] + b[1]) / 2 + dy, text, ha="center", va="center", fontsize=size, color=color,
            zorder=5, bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none"))


GPOS = {0: (0.9, 2.9), 1: (2.4, 3.6), 2: (2.0, 1.6), 3: (3.9, 2.7), 4: (5.0, 1.5)}
GEDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4)]


@fig("graph-representations")
def graph_repr_fig():
    f, ax = diag.canvas(13.4, 4.6)
    for u, v in GEDGES:
        tedge(ax, GPOS[u], GPOS[v], r=0.3)
    for k, (x, y) in GPOS.items():
        tnode(ax, x, y, k)
    label(ax, 2.95, 4.35, "the graph", bold=True)
    # matrix
    x0, y0, w = 6.2, 3.6, 0.5
    label(ax, x0 + 1.25, 4.35, "adjacency matrix", bold=True)
    for i in range(5):
        label(ax, x0 + i * w + w / 2, y0 + 0.28, str(i), size=9, color=MUTED, mono=True)
        label(ax, x0 - 0.25, y0 - i * w - w / 2, str(i), size=9, color=MUTED, mono=True)
        for j in range(5):
            on = (i, j) in GEDGES or (j, i) in GEDGES
            ax.add_patch(Rectangle((x0 + j * w, y0 - (i + 1) * w), w, w, facecolor=SOFT[BLUE] if on else "white",
                                   edgecolor="#cbd2d9", linewidth=1))
            label(ax, x0 + j * w + w / 2, y0 - i * w - w / 2, "1" if on else "0", size=9.5, mono=True,
                  color=INK if on else MUTED)
    # list
    adj = {k: sorted([v for u, v in GEDGES if u == k] + [u for u, v in GEDGES if v == k]) for k in range(5)}
    label(ax, 11.4, 4.35, "adjacency list", bold=True)
    for i in range(5):
        label(ax, 9.85, 3.35 - i * 0.5, f"{i}: {adj[i]}", ha="left", size=10, mono=True)
    label(ax, 7.45, 0.55, "O(V²) space, O(1) edge check", size=9, color=MUTED)
    label(ax, 11.4, 0.55, "O(V + E) space, fast neighbour loops", size=9, color=MUTED)
    return f


@fig("bfs-dfs")
def bfs_dfs_fig():
    f, ax = diag.canvas(12.4, 4.6)
    dist = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}
    cols = {0: ORANGE, 1: BLUE, 2: BLUE, 3: TEAL, 4: PURPLE}
    for u, v in GEDGES:
        tedge(ax, GPOS[u], GPOS[v], r=0.3)
    for k, (x, y) in GPOS.items():
        tnode(ax, x, y, k, color=cols[k])
        label(ax, x, y - 0.5, f"d={dist[k]}", size=9, color=MUTED)
    label(ax, 3.0, 4.35, "BFS from 0: rings by distance", bold=True)
    dx = 6.6
    order = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}
    tree = [(0, 1), (1, 2), (1, 3), (3, 4)]
    for u, v in GEDGES:
        a, b = (GPOS[u][0] + dx, GPOS[u][1]), (GPOS[v][0] + dx, GPOS[v][1])
        if (u, v) in tree:
            dedge(ax, a, b, r=0.3, color=ORANGE, lw=1.8)
        else:
            tedge(ax, a, b, r=0.3, dashed=True)
    for k, (x, y) in GPOS.items():
        tnode(ax, x + dx, y, k)
        label(ax, x + dx, y - 0.5, f"visit #{order[k]}", size=9, color=MUTED)
    label(ax, 3.0 + dx, 4.35, "DFS from 0: dive, then back up", bold=True)
    label(ax, 3.0 + dx, 0.45, "0 → 1 → 2, back to 1, then 3 → 4", size=9.5, color=ORANGE)
    label(ax, 3.0, 0.45, "the queue holds one ring at a time", size=9.5, color=MUTED)
    return f


@fig("islands")
def islands_fig():
    f, ax = diag.canvas(6.2, 4.4)
    grid = ["11000", "11000", "00100", "00011"]
    comp = {(0, 0): BLUE, (0, 1): BLUE, (1, 0): BLUE, (1, 1): BLUE, (2, 2): ORANGE, (3, 3): TEAL, (3, 4): TEAL}
    w = 0.7
    for r in range(4):
        for c in range(5):
            col = comp.get((r, c))
            ax.add_patch(Rectangle((0.5 + c * w, 3.4 - r * w), w, w, facecolor=SOFT[col] if col else "white",
                                   edgecolor=col or "#cbd2d9", linewidth=1.6 if col else 1))
            label(ax, 0.5 + c * w + w / 2, 3.4 - r * w + w / 2, grid[r][c], mono=True, color=INK if col else MUTED)
    label(ax, 4.3, 3.6, "3 islands", bold=True, ha="left")
    label(ax, 4.3, 3.15, "1 = land, 0 = water", ha="left", size=9.5, color=MUTED)
    label(ax, 4.3, 2.2, "(1,1) and (2,2) only\ntouch diagonally:\nseparate islands", ha="left", size=9.5, color=MUTED)
    return f


@fig("multi-source")
def multi_source_fig():
    f, ax = diag.canvas(6.4, 3.4)
    d = [[0, 1, 2, 3, 2], [1, 2, 3, 2, 1], [2, 3, 2, 1, 0]]
    shade = {0: ORANGE, 1: BLUE, 2: TEAL, 3: PURPLE}
    w = 0.8
    for r in range(3):
        for c in range(5):
            col = shade[d[r][c]]
            ax.add_patch(Rectangle((0.4 + c * w, 2.5 - r * w), w, w, facecolor=SOFT[col], edgecolor=col, linewidth=1.4))
            label(ax, 0.4 + c * w + w / 2, 2.5 - r * w + w / 2, "H" if d[r][c] == 0 else str(d[r][c]), mono=True, bold=d[r][c] == 0)
    label(ax, 4.75, 3.0, "two sources (H)", ha="left", size=9.5, bold=True)
    label(ax, 4.75, 2.55, "start together\nat distance 0", ha="left", size=9.5, color=MUTED)
    label(ax, 4.75, 1.45, "each cell: distance\nto the nearer H", ha="left", size=9.5, color=MUTED)
    return f


@fig("topological")
def topological_fig():
    f, ax = diag.canvas(12.6, 5.6)
    pos = {"underwear": (1.2, 4.9), "socks": (3.6, 4.9), "shirt": (8.6, 4.9), "trousers": (2.0, 3.8), "shoes": (3.6, 2.7),
           "belt": (5.4, 3.3), "tie": (8.6, 3.8), "jacket": (7.4, 2.7)}
    edges = [("underwear", "trousers"), ("trousers", "shoes"), ("socks", "shoes"), ("shirt", "tie"), ("tie", "jacket"),
             ("trousers", "belt"), ("belt", "jacket")]
    bw, bh = 1.35, 0.42
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.add_patch(FancyArrowPatch((x1, y1 - bh / 2), (x2, y2 + bh / 2), arrowstyle="-|>", mutation_scale=12,
                                     color=GREY, linewidth=1.3, shrinkA=2, shrinkB=2, zorder=1))
    for k, (x, y) in pos.items():
        sbox(ax, x - bw / 2, y - bh / 2, bw, bh, k, color=BLUE, fontsize=9.5)
    order = ["underwear", "socks", "shirt", "trousers", "tie", "belt", "shoes", "jacket"]
    label(ax, 0.3, 1.75, "one topological order: every arrow points right", ha="left", size=10, bold=True)
    xs = {k: 0.3 + i * 1.53 for i, k in enumerate(order)}
    for k, x in xs.items():
        sbox(ax, x, 0.2, 1.35, bh, k, color=TEAL, fontsize=9.5)
    for a, b in edges:
        ax.add_patch(FancyArrowPatch((xs[a] + 0.9, 0.2 + bh), (xs[b] + 0.45, 0.2 + bh), arrowstyle="-|>", mutation_scale=10,
                                     color=ORANGE, linewidth=1.1, connectionstyle="arc3,rad=-0.35", zorder=1))
    return f


@fig("dijkstra")
def dijkstra_fig():
    f, ax = diag.canvas(8.6, 4.9)
    P = {"A": (1.0, 2.7), "B": (4.0, 4.0), "C": (4.0, 1.4), "D": (7.0, 2.7)}
    E = [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 1), ("C", "D", 5)]
    tree = {("A", "C"), ("C", "B"), ("B", "D")}
    for a, b, w in E:
        on = (a, b) in tree
        tedge(ax, P[a], P[b], r=0.33, color=ORANGE if on else GREY, lw=2.2 if on else 1.3)
        wlabel(ax, P[a], P[b], str(w), color=ORANGE if on else MUTED)
    dist = {"A": 0, "B": 3, "C": 1, "D": 4}
    step = {"A": 1, "C": 2, "B": 3, "D": 4}
    for k, (x, y) in P.items():
        tnode(ax, x, y, k, color=ORANGE if k == "A" else BLUE, r=0.33)
        oy = 0.62 if y >= 2.5 else -0.62
        label(ax, x, y + oy, f"dist {dist[k]} (settled #{step[k]})", size=9, color=MUTED)
    label(ax, 4.3, 0.1, "orange: shortest-path tree; B is reached via C (1 + 2 = 3), cheaper than A–B (4)", size=9, color=ORANGE)
    return f


@fig("union-find")
def union_find_fig():
    f, ax = diag.canvas(11.6, 4.6)
    def forest(dx, parent, title, hl=()):
        pos = {0: (1.6, 3.6), 1: (1.0, 2.6), 2: (2.4, 2.6), 3: (1.0, 1.6), 4: (1.0, 0.6), 5: (3.9, 3.6), 6: (3.9, 2.6)}
        if title.startswith("after"):
            pos = {0: (1.9, 3.6), 1: (0.6, 2.4), 2: (1.5, 2.4), 3: (2.4, 2.4), 4: (3.3, 2.4), 5: (4.6, 3.6), 6: (4.6, 2.4)}
        for c, p in parent.items():
            a, b = (pos[c][0] + dx, pos[c][1]), (pos[p][0] + dx, pos[p][1])
            dedge(ax, a, b, r=0.28, color=ORANGE if c in hl else GREY, lw=1.8 if c in hl else 1.3)
        for k, (x, y) in pos.items():
            tnode(ax, x + dx, y, k, color=TEAL if k in (0, 5) else (ORANGE if k in hl else BLUE), r=0.28)
        label(ax, dx + 2.6, 4.35, title, bold=True)
    forest(0.2, {1: 0, 2: 0, 3: 1, 4: 3, 6: 5}, "before: find(4) walks 4 → 3 → 1 → 0", hl=(4, 3, 1))
    forest(6.0, {1: 0, 2: 0, 3: 0, 4: 0, 6: 5}, "after path compression", hl=(4, 3, 1))
    label(ax, 5.8, 0.15, "teal = roots (each names a group); arrows point to the parent", size=9.5, color=MUTED)
    return f


@fig("mst")
def mst_fig():
    f, ax = diag.canvas(8.4, 4.6)
    P = {"A": (1.0, 3.6), "B": (3.4, 3.9), "C": (3.0, 1.9), "D": (5.6, 2.4), "E": (7.2, 0.9)}
    E = [("A", "B", 1), ("B", "C", 2), ("C", "D", 3), ("D", "E", 4), ("A", "C", 5), ("B", "D", 6), ("C", "E", 7)]
    for a, b, w in E:
        on = w <= 4
        tedge(ax, P[a], P[b], r=0.32, color=ORANGE if on else GREY, lw=2.4 if on else 1.2)
        wlabel(ax, P[a], P[b], str(w), color=ORANGE if on else MUTED)
    for k, (x, y) in P.items():
        tnode(ax, x, y, k, r=0.32)
    label(ax, 0.3, 0.9, "MST (orange): 1 + 2 + 3 + 4 = 10", ha="left", size=10, bold=True, color=ORANGE)
    label(ax, 0.3, 0.45, "5, 6 and 7 would each close a cycle", ha="left", size=9.5, color=MUTED)
    return f


@fig("bipartite")
def bipartite_fig():
    f, ax = diag.canvas(9.4, 4.0)
    sq = {0: (1.0, 3.0), 1: (3.0, 3.0), 2: (3.0, 1.0), 3: (1.0, 1.0)}
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        tedge(ax, sq[u], sq[v], r=0.3)
    for k, (x, y) in sq.items():
        tnode(ax, x, y, k, color=BLUE if k % 2 == 0 else ORANGE)
    label(ax, 2.0, 3.75, "square: bipartite", bold=True)
    label(ax, 2.0, 0.25, "{0, 2} and {1, 3}", size=9.5, color=MUTED)
    tri = {0: (6.0, 3.0), 1: (8.2, 3.0), 2: (7.1, 1.1)}
    for u, v in [(0, 1), (1, 2), (2, 0)]:
        tedge(ax, tri[u], tri[v], r=0.3, color=CRIMSON if 2 in (u, v) else GREY)
    tnode(ax, *tri[0], 0, color=BLUE)
    tnode(ax, *tri[1], 1, color=ORANGE)
    tnode(ax, *tri[2], "2?", color=CRIMSON, fontsize=10)
    label(ax, 7.1, 3.75, "triangle: not bipartite", bold=True)
    label(ax, 7.1, 0.25, "2 touches both colours (an odd cycle)", size=9.5, color=MUTED)
    return f


@fig("bridges")
def bridges_fig():
    f, ax = diag.canvas(9.6, 3.8)
    P = {0: (0.9, 3.0), 1: (3.0, 2.0), 2: (0.9, 1.0), 3: (6.2, 2.0), 4: (8.3, 3.0), 5: (8.3, 1.0)}
    for u, v in [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]:
        tedge(ax, P[u], P[v], r=0.3)
    tedge(ax, P[1], P[3], r=0.3, color=CRIMSON, lw=2.6)
    wlabel(ax, P[1], P[3], "bridge", color=CRIMSON, dy=0.3)
    for k, (x, y) in P.items():
        tnode(ax, x, y, k, color=ORANGE if k in (1, 3) else BLUE)
    label(ax, 4.6, 0.35, "orange: articulation points (removing either splits the graph)", size=9.5, color=MUTED)
    return f


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names or FIGS:
        save(FIGS[name](), name)
    print(len(names or FIGS), "figures")


if __name__ == "__main__":
    main(sys.argv[1:])
