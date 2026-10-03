"""Draw the lesson diagrams for AI Engineering with LLMs into figures/*.svg (deterministic).

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
    "axes.facecolor": "white", "savefig.facecolor": "white", "svg.hashsalt": "ai-engineering-course",
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


# ---------------------------------------------------------------- Part 1: how LLMs work

@fig("next-token")
def next_token_fig():
    f, ax = diag.canvas(11.0, 4.2)
    sbox(ax, 0.3, 2.6, 3.4, 0.7, 'text so far: "The capital of France is"', color=BLUE, fontsize=9.5)
    sbox(ax, 4.4, 2.45, 1.8, 1.0, "LLM", color=PURPLE, fontsize=14, bold=True)
    arrow(ax, 3.75, 2.95, 4.35, 2.95, color=INK)
    probs = [(" Paris", 0.92), (" a", 0.03), (" the", 0.02), (" located", 0.01), ("…", 0.02)]
    for i, (tok, p) in enumerate(probs):
        y = 3.55 - i * 0.42
        ax.add_patch(Rectangle((7.6, y - 0.14), 2.6 * p, 0.28, facecolor=SOFT[ORANGE] if i == 0 else SOFT[GREY],
                               edgecolor=ORANGE if i == 0 else GREY, linewidth=1.2))
        label(ax, 7.5, y, repr(tok)[1:-1] if tok != "…" else "…", ha="right", size=9.5, mono=True)
        label(ax, 7.7 + 2.6 * p, y, f"{p:.0%}", ha="left", size=9, color=MUTED)
    arrow(ax, 6.25, 2.95, 6.75, 2.95, color=INK)
    label(ax, 8.6, 3.95, "next-token probabilities", size=9.5, bold=True)
    ax.add_patch(FancyArrowPatch((8.3, 1.25), (2.0, 2.55), arrowstyle="-|>", mutation_scale=14, color=ORANGE,
                                 linewidth=1.6, connectionstyle="arc3,rad=-0.35"))
    label(ax, 5.2, 0.55, 'pick one token (" Paris"), append it, and run again', size=10, color=ORANGE)
    return f


@fig("tokens")
def tokens_fig():
    f, ax = diag.canvas(10.0, 2.8)
    toks = [("Token", 3404), ("ization", 2065), (" isn", 4536), ("'t", 956), (" magic", 11204), ("!", 0)]
    cols = [BLUE, ORANGE, TEAL, CRIMSON, PURPLE, GREEN]
    x = 0.4
    for (t, i), c in zip(toks, cols):
        w = 0.32 + 0.19 * len(t)
        sbox(ax, x, 1.4, w, 0.62, t.replace(" ", "␣"), color=c, mono=True, fontsize=11)
        label(ax, x + w / 2, 1.05, str(i), size=9, color=MUTED, mono=True)
        x += w + 0.12
    label(ax, 0.4, 2.45, '"Tokenization isn\'t magic!"  →  6 tokens', ha="left", size=10.5, bold=True)
    label(ax, 0.4, 0.45, "␣ marks a space: it usually belongs to the start of the next word. Numbers below are token IDs (illustrative).",
          ha="left", size=9, color=MUTED)
    return f


@fig("embedding-space")
def embedding_space_fig():
    f, ax = plt.subplots(figsize=(7.2, 5.0))
    groups = {
        "animals": (BLUE, {"dog": (1.0, 4.0), "puppy": (1.6, 4.9), "cat": (2.4, 3.4), "kitten": (3.0, 4.3)}),
        "vehicles": (ORANGE, {"car": (7.0, 1.2), "truck": (7.8, 1.8), "bus": (6.6, 2.0)}),
        "food": (TEAL, {"pizza": (6.4, 5.2), "pasta": (7.2, 5.6), "bread": (6.9, 4.6)}),
    }
    for name, (c, pts) in groups.items():
        for w, (x, y) in pts.items():
            ax.scatter([x], [y], s=60, color=c, zorder=3)
            ax.annotate(w, (x, y), xytext=(6, 5), textcoords="offset points", fontsize=10, color=INK)
    for a, b in (("dog", "puppy"), ("cat", "kitten")):
        (x1, y1), (x2, y2) = groups["animals"][1][a], groups["animals"][1][b]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.5))
    ax.text(0.6, 0.6, 'dog → puppy and cat → kitten: the same "young version of" direction', fontsize=9, color=PURPLE)
    ax.set_xlim(0, 9); ax.set_ylim(0, 6.3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("dimension 1"); ax.set_ylabel("dimension 2")
    ax.set_title("Similar meanings sit close together")
    return f


@fig("transformer")
def transformer_fig():
    f, ax = diag.canvas(7.6, 6.4)
    sbox(ax, 1.8, 0.3, 4.0, 0.55, 'input tokens: "The cat sat"', color=GREY, fontsize=10)
    sbox(ax, 1.8, 1.2, 4.0, 0.55, "token embeddings + positions", color=BLUE, fontsize=10)
    ax.add_patch(Rectangle((1.4, 2.05), 4.8, 2.5, facecolor="none", edgecolor=PURPLE, linewidth=1.6, linestyle="--"))
    label(ax, 6.35, 3.3, "× N\nlayers", ha="left", size=10, color=PURPLE, bold=True)
    sbox(ax, 1.8, 2.35, 4.0, 0.7, "self-attention\n(tokens share information)", color=ORANGE, fontsize=9.5)
    sbox(ax, 1.8, 3.55, 4.0, 0.7, "feed-forward network\n(each token on its own)", color=TEAL, fontsize=9.5)
    sbox(ax, 1.8, 4.9, 4.0, 0.55, "output layer → logits → softmax", color=BLUE, fontsize=10)
    sbox(ax, 1.8, 5.75, 4.0, 0.5, 'next token: " on" 41%, " down" 22%, …', color=GREEN, fontsize=9.5)
    for y1, y2 in ((0.85, 1.2), (1.75, 2.35), (3.05, 3.55), (4.25, 4.9), (5.45, 5.75)):
        arrow(ax, 3.8, y1, 3.8, y2, color=INK, lw=1.2)
    return f


@fig("attention")
def attention_fig():
    import numpy as np
    toks = ["the", "animal", "was", "tired", "because", "it"]
    n = len(toks)
    w = np.zeros((n, n))
    rows = {0: [1], 1: [0.3, 0.7], 2: [0.1, 0.6, 0.3], 3: [0.05, 0.45, 0.2, 0.3], 4: [0.05, 0.2, 0.1, 0.45, 0.2],
            5: [0.03, 0.72, 0.05, 0.1, 0.05, 0.05]}
    for i, r in rows.items():
        w[i, :len(r)] = r
    masked = np.ma.masked_where(np.triu(np.ones((n, n)), k=1) == 1, w)
    f, ax = plt.subplots(figsize=(6.2, 5.2))
    cmap = matplotlib.colormaps["Purples"].copy()
    cmap.set_bad("#f4f5f7")
    ax.imshow(masked, cmap=cmap, vmin=0, vmax=1)
    for i in range(n):
        for j in range(i + 1):
            ax.text(j, i, f"{w[i, j]:.2f}", ha="center", va="center", fontsize=8.5, color="white" if w[i, j] > 0.5 else INK)
    ax.set_xticks(range(n), toks, rotation=30)
    ax.set_yticks(range(n), toks)
    ax.set_xlabel("attends to (keys)")
    ax.set_ylabel("token attending (queries)")
    ax.set_title('"it" attends mostly to "animal" (illustrative weights)')
    for s in ax.spines.values():
        s.set_visible(False)
    return f


@fig("temperature")
def temperature_fig():
    import numpy as np
    toks = ["Paris", "a", "the", "located", "beautiful"]
    logits = np.array([6.0, 2.5, 2.0, 1.5, 1.0])
    f, axes = plt.subplots(1, 3, figsize=(10.5, 3.4), sharey=True)
    for ax, t, c in zip(axes, (0.2, 1.0, 2.0), (BLUE, PURPLE, ORANGE)):
        z = logits / t
        p = np.exp(z - z.max()); p /= p.sum()
        ax.bar(range(5), p, color=c, alpha=0.85)
        ax.set_xticks(range(5), toks, rotation=35, fontsize=9)
        ax.set_title(f"temperature {t}")
        ax.set_ylim(0, 1.05)
        for i, v in enumerate(p):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=8, color=INK)
    axes[0].set_ylabel("probability")
    f.tight_layout()
    return f


def main(names):
    OUT.mkdir(exist_ok=True)
    for name in names or FIGS:
        save(FIGS[name](), name)
    print(len(names or FIGS), "figures")


if __name__ == "__main__":
    main(sys.argv[1:])
