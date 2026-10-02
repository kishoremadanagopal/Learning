"""Small drawing helpers for the course diagrams (boxes, arrows, tables, Venn circles), drawn with matplotlib."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

TEAL, ORANGE, BLUE, RED, GREY, INK, PURPLE, GREEN = "#0f766e", "#e8730c", "#2c679c", "#c2410c", "#9aa5b1", "#1f2933", "#6d4fc2", "#2f7a45"
SOFT = {TEAL: "#dcf1ee", ORANGE: "#fde8d6", BLUE: "#e3edf7", RED: "#fbe4dc", GREY: "#eef1f4", PURPLE: "#ece7fa", GREEN: "#e2f2e6", INK: "#eef1f4"}

plt.rcParams.update({
    "svg.fonttype": "none", "svg.hashsalt": "learning-diagrams", "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"], "font.size": 11,
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 12.5,
})


def canvas(w, h, title=None, xlim=None, ylim=None):
    """A blank drawing area w x h inches, with data coordinates 0..w by 0..h unless given."""
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*(xlim or (0, w)))
    ax.set_ylim(*(ylim or (0, h)))
    ax.axis("off")
    ax.set_aspect("equal")
    if title:
        ax.set_title(title)
    return fig, ax


def _keep_spaces(text):
    """SVG collapses runs of spaces, so use non-breaking spaces where the spacing matters."""
    text = str(text)
    return text.replace(" ", "\u00a0") if ("  " in text or "\n " in text or text.startswith(" ")) else text


def box(ax, x, y, w, h, text="", color=TEAL, fill=None, fontsize=11, bold=False, mono=False, round_=0.08, textcolor=None, lw=1.6):
    """A rounded box with its lower-left corner at (x, y)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={round_}",
                                linewidth=lw, edgecolor=color, facecolor=fill if fill is not None else SOFT.get(color, "white")))
    if text:
        ax.text(x + w / 2, y + h / 2, _keep_spaces(text), ha="center", va="center", fontsize=fontsize,
                fontweight="bold" if bold else "normal", family="monospace" if mono else None, color=textcolor or INK)


def arrow(ax, x1, y1, x2, y2, color=INK, text=None, lw=1.6, style="-|>", fontsize=10, rad=0.0, text_offset=(0, 0.12)):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14, color=color, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x1 + x2) / 2 + text_offset[0], (y1 + y2) / 2 + text_offset[1], text, ha="center", va="bottom", fontsize=fontsize, color=color)


def label(ax, x, y, text, size=10.5, color=INK, ha="center", va="center", bold=False, mono=False, italic=False):
    ax.text(x, y, _keep_spaces(text), ha=ha, va=va, fontsize=size, color=color, fontweight="bold" if bold else "normal",
            family="monospace" if mono else None, style="italic" if italic else "normal")


def table(ax, x, y, header, rows, colw, rowh=0.36, color=TEAL, highlight=None, header_fill=None, fontsize=10, mono=True, dim=None):
    """Draw a table with its top-left corner at (x, y). highlight: {row_index: color}; dim: set of row indexes to grey out."""
    highlight = highlight or {}
    dim = dim or set()
    total_w = sum(colw)
    ax.add_patch(Rectangle((x, y - rowh), total_w, rowh, facecolor=header_fill or color, edgecolor=color, linewidth=1.2))
    cx = x
    for h, w in zip(header, colw):
        ax.text(cx + w / 2, y - rowh / 2, h, ha="center", va="center", color="white", fontsize=fontsize, fontweight="bold",
                family="monospace" if mono else None)
        cx += w
    for r, row in enumerate(rows):
        top = y - rowh * (r + 1)
        fc = SOFT.get(highlight[r], highlight[r]) if r in highlight else "white"
        ax.add_patch(Rectangle((x, top - rowh), total_w, rowh, facecolor=fc, edgecolor="#cbd2d9", linewidth=0.8))
        cx = x
        for v, w in zip(row, colw):
            ax.text(cx + w / 2, top - rowh / 2, _keep_spaces(v), ha="center", va="center", fontsize=fontsize,
                    color=GREY if r in dim else INK, family="monospace" if mono else None)
            cx += w
    return x + total_w, y - rowh * (len(rows) + 1)


def venn(ax, cx, cy, r=0.55, gap=0.55, shade=("left", "middle", "right"), color=TEAL, title=None, labels=("A", "B")):
    """Two overlapping circles; shade any of left-only, middle (overlap) and right-only."""
    import numpy as np
    xs = np.linspace(cx - gap - r, cx + gap + r, 400)
    ys = np.linspace(cy - r, cy + r, 200)
    X, Y = np.meshgrid(xs, ys)
    in_l = (X - (cx - gap / 2)) ** 2 + (Y - cy) ** 2 <= r ** 2
    in_r = (X - (cx + gap / 2)) ** 2 + (Y - cy) ** 2 <= r ** 2
    mask = np.zeros_like(X, dtype=bool)
    if "left" in shade:
        mask |= in_l & ~in_r
    if "middle" in shade:
        mask |= in_l & in_r
    if "right" in shade:
        mask |= in_r & ~in_l
    from matplotlib.colors import ListedColormap
    ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5], colors=[color], alpha=0.55)
    for dx in (-gap / 2, gap / 2):
        ax.add_patch(Circle((cx + dx, cy), r, fill=False, edgecolor=INK, linewidth=1.4))
    ax.text(cx - gap / 2 - r * 0.45, cy, labels[0], ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(cx + gap / 2 + r * 0.45, cy, labels[1], ha="center", va="center", fontsize=10.5, fontweight="bold")
    if title:
        ax.text(cx, cy - r - 0.28, title, ha="center", va="center", fontsize=11, fontweight="bold", family="monospace")


def save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
