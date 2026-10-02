"""Draw the lesson diagrams into figures/ as SVG files.  Run:  python figures.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch
from diag import (TEAL, ORANGE, BLUE, RED, GREY, INK, PURPLE, GREEN, SOFT,
                  canvas, box, arrow, label, venn, save)

OUT = HERE / "figures"


def diamond(ax, cx, cy, w, h, text, color=ORANGE, fontsize=9.5):
    ax.add_patch(Polygon([(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)],
                         closed=True, facecolor=SOFT[color], edgecolor=color, linewidth=1.6))
    label(ax, cx, cy, text, size=fontsize, mono=True)


def cells(ax, x, y, values, w=0.62, h=0.55, color=TEAL, fills=None, fontsize=11):
    for i, v in enumerate(values):
        c = fills[i] if fills else color
        box(ax, x + i * w, y, w - 0.04, h, str(v), color=c, round_=0.02, fontsize=fontsize, mono=True)


def run_stages():
    fig, ax = canvas(11, 2.6)
    steps = [("your code", 'print("Hi")', GREY), ("1. Tokens", 'print ( "Hi" )', BLUE), ("2. AST", "a tree of the\nprogram", PURPLE),
             ("3. Compile", "bytecode\n(or JavaScript)", ORANGE), ("4. Run", "Hi", TEAL)]
    for i, (title, body, c) in enumerate(steps):
        x = 0.15 + i * 2.2
        label(ax, x + 0.85, 2.3, title, bold=True, color=c)
        box(ax, x, 1.1, 1.7, 0.95, body, color=c, mono=True, fontsize=9.5)
        if i < len(steps) - 1:
            arrow(ax, x + 1.75, 1.57, x + 2.15, 1.57)
    label(ax, 4.95, 0.75, "syntax errors (typos)\nare caught here", size=9, color=RED)
    label(ax, 9.65, 0.75, "runtime errors (like 1 / 0)\nare found here", size=9, color=RED)
    return fig


def variables():
    fig, ax = canvas(7.5, 2.4)
    for i, (name, val, typ, c) in enumerate([("name", '"Ada"', "str", TEAL), ("age", "36", "int", ORANGE)]):
        y = 1.5 - i * 1.0
        box(ax, 0.3, y, 1.2, 0.55, name, color=GREY, mono=True, bold=True)
        arrow(ax, 1.55, y + 0.27, 3.0, y + 0.27, color=INK)
        box(ax, 3.05, y, 1.4, 0.55, val, color=c, mono=True, fontsize=11.5)
        label(ax, 4.65, y + 0.27, f"type: {typ}", size=9.5, color=c, ha="left")
    label(ax, 0.9, 2.25, "names", size=9.5, color=GREY)
    label(ax, 3.75, 2.25, "values", size=9.5, color=GREY)
    label(ax, 2.25, 2.25, "=", size=13, bold=True)
    return fig


def string_index():
    fig, ax = canvas(6.2, 2.3)
    word = "Python"
    x0 = 1.2
    cells(ax, x0, 0.9, list(word), w=0.65, h=0.6, fills=[ORANGE] + [TEAL] * 4 + [PURPLE])
    for i in range(6):
        label(ax, x0 + 0.305 + i * 0.65, 1.75, str(i), size=10.5, mono=True, color=INK)
        label(ax, x0 + 0.305 + i * 0.65, 0.62, str(i - 6), size=10.5, mono=True, color=GREY)
    label(ax, 1.05, 1.75, "index", size=9.5, ha="right")
    label(ax, 1.05, 0.62, "from the end", size=9.5, ha="right", color=GREY)
    label(ax, 3.1, 0.15, 'word[0] is "P"     word[-1] is "n"', size=10, mono=True)
    return fig


def string_slice():
    fig, ax = canvas(7.2, 2.6)
    word = "Python"
    x0 = 1.0
    w = 0.75
    cells(ax, x0, 1.0, list(word), w=w, h=0.6, fills=[TEAL, TEAL] + [GREY] * 4)
    for i in range(7):
        x = x0 + i * w - 0.02
        ax.plot([x, x], [0.85, 1.75], color=ORANGE if i in (0, 2) else GREY, linewidth=2 if i in (0, 2) else 1)
        label(ax, x, 1.98, str(i), size=10.5, mono=True, color=ORANGE if i in (0, 2) else INK)
    label(ax, 3.2, 2.4, "slice positions sit between the characters", size=10, color=GREY)
    label(ax, 3.2, 0.45, 'word[0:2] cuts at 0 and 2 → "Py"', size=10.5, mono=True, color=TEAL)
    label(ax, 3.2, 0.1, "start is included, stop is not", size=9.5, color=GREY)
    return fig


def if_elif():
    fig, ax = canvas(8.5, 4.4)
    label(ax, 1.8, 4.2, "score = 82", mono=True, bold=True)
    checks = [("score >= 90", 'grade = "A"', False), ("score >= 80", 'grade = "B"', True), ("score >= 70", 'grade = "C"', None)]
    for i, (cond, act, taken) in enumerate(checks):
        cy = 3.45 - i * 1.0
        diamond(ax, 1.8, cy, 2.6, 0.75, cond, color=ORANGE if taken is not None else GREY)
        col = TEAL if taken else GREY
        arrow(ax, 3.12, cy, 4.6, cy, color=col, text="yes", fontsize=9.5, lw=2.4 if taken else 1.3)
        box(ax, 4.65, cy - 0.27, 1.9, 0.54, act, color=col, mono=True, fontsize=9.5)
        if i < 2:
            arrow(ax, 1.8, cy - 0.38, 1.8, cy - 0.62, color=ORANGE if i == 0 else GREY, lw=2.4 if i == 0 else 1.3)
            label(ax, 1.95, cy - 0.5, "no", size=9.5, ha="left", color=ORANGE if i == 0 else GREY)
    arrow(ax, 1.8, 1.07, 1.8, 0.72, color=GREY)
    label(ax, 1.95, 0.9, "no", size=9.5, ha="left", color=GREY)
    box(ax, 0.85, 0.2, 1.9, 0.5, 'else: grade = "F"', color=GREY, mono=True, fontsize=9.5)
    label(ax, 6.75, 2.45, "82 fails the first test,\npasses the second,\nso grade is B.\nThe rest are skipped.", size=9.5, color=TEAL, ha="left")
    return fig


def for_loop():
    fig, ax = canvas(10, 2.9)
    items = ["apple", "banana", "cherry"]
    label(ax, 4.95, 2.65, 'for fruit in ["apple", "banana", "cherry"]:', mono=True, size=10.5)
    for i, it in enumerate(items):
        x = 0.4 + i * 3.1
        box(ax, x, 1.35, 2.4, 0.9, "", color=[TEAL, ORANGE, PURPLE][i])
        label(ax, x + 1.2, 2.0, f"round {i + 1}", size=9, color=GREY)
        label(ax, x + 1.2, 1.62, f'fruit = "{it}"', mono=True, size=10)
        label(ax, x + 1.2, 0.85, f"I like {it}", mono=True, size=10, color=[TEAL, ORANGE, PURPLE][i])
        arrow(ax, x + 1.2, 1.3, x + 1.2, 1.05, color=GREY)
        if i < 2:
            arrow(ax, x + 2.45, 1.8, x + 3.05, 1.8, color=INK, text="next")
    label(ax, 5.0, 0.3, "the body runs once per item, then the loop ends when the list runs out", size=9.5, color=GREY)
    return fig


def list_refs():
    fig, ax = canvas(8.5, 3.0)
    label(ax, 2.2, 2.8, "b = a   (same list, two names)", bold=True, size=10.5)
    for i, n in enumerate(["a", "b"]):
        y = 1.95 - i * 0.75
        box(ax, 0.2, y, 0.6, 0.48, n, color=GREY, mono=True, bold=True)
        arrow(ax, 0.85, y + 0.24, 1.75, 1.6, color=INK)
    cells(ax, 1.8, 1.33, [1, 2, 3, 4], w=0.6, h=0.55, fills=[TEAL] * 3 + [ORANGE])
    label(ax, 3.0, 0.9, "b.append(4) changes it for a too", size=9.5, color=ORANGE)
    label(ax, 6.4, 2.8, "c = a.copy()   (a new list)", bold=True, size=10.5)
    box(ax, 4.6, 1.33, 0.6, 0.48, "c", color=GREY, mono=True, bold=True)
    arrow(ax, 5.25, 1.57, 5.6, 1.6, color=INK)
    cells(ax, 5.65, 1.33, [1, 2, 3, 4, 5], w=0.55, h=0.55, fills=[BLUE] * 4 + [ORANGE])
    label(ax, 7.0, 0.9, "c.append(5) leaves a alone", size=9.5, color=BLUE)
    return fig


def dict_keys():
    fig, ax = canvas(7.5, 2.9)
    label(ax, 1.25, 2.7, "keys", bold=True, color=PURPLE)
    label(ax, 4.6, 2.7, "values", bold=True, color=TEAL)
    pairs = [('"name"', '"Ada"'), ('"age"', "36"), ('"languages"', '["English", "French"]')]
    for i, (k, v) in enumerate(pairs):
        y = 1.95 - i * 0.75
        box(ax, 0.3, y, 1.9, 0.5, k, color=PURPLE, mono=True, fontsize=10)
        arrow(ax, 2.25, y + 0.25, 2.95, y + 0.25)
        box(ax, 3.0, y, 3.2 if i == 2 else 1.4, 0.5, v, color=TEAL, mono=True, fontsize=10)
    label(ax, 3.75, 0.1, 'person["name"] looks up the key and gives back "Ada"', size=9.5, color=GREY)
    return fig


def set_ops():
    fig, ax = canvas(11, 2.6, xlim=(0, 11), ylim=(0, 2.6))
    ops = [("a | b", "union", ("left", "middle", "right")), ("a & b", "intersection", ("middle",)),
           ("a - b", "difference", ("left",)), ("a ^ b", "symmetric difference", ("left", "right"))]
    for i, (sym, name, shade) in enumerate(ops):
        cx = 1.35 + i * 2.75
        venn(ax, cx, 1.45, r=0.62, gap=0.62, shade=shade, color=TEAL, labels=("Ana\nCy", "Dee"))
        label(ax, cx, 1.45, "Ben", size=10.5, bold=True)
        label(ax, cx, 0.5, sym, mono=True, bold=True)
        label(ax, cx, 0.18, name, size=9.5, color=GREY)
    label(ax, 5.5, 2.45, "a = python_devs = {Ana, Ben, Cy}      b = java_devs = {Ben, Dee}      shaded = the result", size=9.5)
    return fig


def comprehension():
    fig, ax = canvas(9, 3.0)
    parts = [("[", INK), ("n * n", TEAL), (" for n in range(1, 6)", ORANGE), ("]", INK)]
    full = "".join(t for t, _ in parts)
    r = fig.canvas.get_renderer()
    t = ax.text(4.0, 2.55, full.replace(" ", "\u00a0"), family="monospace", fontsize=13, va="center", ha="center", fontweight="bold", color="none")
    bb = t.get_window_extent(r).transformed(ax.transData.inverted())
    cw = (bb.x1 - bb.x0) / len(full)
    i = 0
    mids = []
    for text, c in parts:
        ax.text(bb.x0 + i * cw, 2.55, text.replace(" ", "\u00a0"), family="monospace", fontsize=13, va="center", ha="left", fontweight="bold", color=c)
        mids.append(bb.x0 + (i + len(text) / 2) * cw)
        i += len(text)
    label(ax, mids[1], 2.05, "what to keep", size=9.5, color=TEAL)
    label(ax, mids[2] + 0.3, 2.05, "where the values come from", size=9.5, color=ORANGE)
    cells(ax, 1.2, 1.0, [1, 2, 3, 4, 5], w=0.62, h=0.5, color=ORANGE)
    label(ax, 0.95, 1.25, "n", mono=True, ha="right")
    for i in range(5):
        arrow(ax, 1.49 + i * 0.62, 0.95, 1.49 + i * 0.62, 0.72, color=GREY, lw=1.1)
    cells(ax, 1.2, 0.15, [1, 4, 9, 16, 25], w=0.62, h=0.5, color=TEAL)
    label(ax, 0.95, 0.4, "n * n", mono=True, ha="right")
    label(ax, 6.0, 0.75, "one new list, built in a\nsingle line instead of\na loop with .append()", size=9.5, color=GREY, ha="left")
    return fig


def function_machine():
    fig, ax = canvas(9, 2.3)
    label(ax, 1.0, 1.9, "argument", size=9.5, color=GREY)
    box(ax, 0.3, 1.0, 1.4, 0.6, '"Ada"', color=ORANGE, mono=True)
    arrow(ax, 1.75, 1.3, 2.6, 1.3)
    box(ax, 2.65, 0.55, 3.0, 1.5, "", color=TEAL)
    label(ax, 4.15, 1.75, "greet(name)", mono=True, bold=True)
    label(ax, 4.15, 1.2, 'name = "Ada"', mono=True, size=9.5, color=GREY)
    label(ax, 4.15, 0.85, 'return f"Hello, {name}!"', mono=True, size=9)
    arrow(ax, 5.7, 1.3, 6.5, 1.3)
    label(ax, 7.6, 1.9, "return value", size=9.5, color=GREY)
    box(ax, 6.55, 1.0, 2.1, 0.6, '"Hello, Ada!"', color=PURPLE, mono=True)
    label(ax, 4.5, 0.15, "values go in as arguments; one value comes back out with return", size=9.5, color=GREY)
    return fig


def legb():
    fig, ax = canvas(8.5, 4.0)
    layers = [("B  built-in", "print, len, range ...", GREY), ("G  global (module)", 'x = "global"', BLUE),
              ("E  enclosing: outer()", 'x = "enclosing"', ORANGE), ("L  local: inner()", 'x = "local"', TEAL)]
    for i, (name, body, c) in enumerate(layers):
        x, y = 0.2 + 0.35 * i, 0.2 + 0.22 * i
        w, h = 5.8 - 0.7 * i, 3.6 - 0.72 * i
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.1", facecolor=SOFT[c], edgecolor=c, linewidth=1.6))
        label(ax, x + 0.15, y + h - 0.2, name, size=9.5, bold=True, color=c, ha="left")
        label(ax, x + w - 0.15, y + h - 0.2, body, size=9, mono=True, ha="right")
    label(ax, 3.1, 1.2, 'print(x) inside inner()\nshows "local"', size=9.5, mono=True, color=TEAL)
    arrow(ax, 6.4, 1.6, 6.4, 3.3, color=INK)
    label(ax, 6.6, 2.45, "Python looks for a\nname from the inside\nout: L → E → G → B\nand stops at the\nfirst match", size=9.5, ha="left")
    return fig


def recursion_stack():
    fig, ax = canvas(9.5, 3.6)
    calls = ["factorial(4)", "factorial(3)", "factorial(2)", "factorial(1)"]
    rets = ["4 * 6 = 24", "3 * 2 = 6", "2 * 1 = 2", "1   (base case)"]
    for i, (c, r) in enumerate(zip(calls, rets)):
        y = 2.8 - i * 0.75
        x = 0.3 + i * 0.55
        box(ax, x, y, 2.0, 0.5, c, color=ORANGE if i < 3 else PURPLE, mono=True, fontsize=10)
        box(ax, 5.6 + (3 - i) * 0.0, y, 2.6, 0.5, r, color=TEAL if i < 3 else PURPLE, mono=True, fontsize=10)
        arrow(ax, x + 2.05, y + 0.25, 5.55, y + 0.25, color=GREY, lw=1.0, style="-")
        if i < 3:
            arrow(ax, x + 1.0, y - 0.02, x + 1.55, y - 0.23, color=ORANGE)
            arrow(ax, 6.9, y - 0.23, 6.9, y - 0.02, color=TEAL)
    label(ax, 1.3, 3.45, "calls go down ↓", size=10, color=ORANGE, bold=True)
    label(ax, 6.9, 3.45, "answers come back up ↑", size=10, color=TEAL, bold=True)
    label(ax, 4.75, 0.2, "each call waits for the one below it; the base case stops the chain", size=9.5, color=GREY)
    return fig


def try_flow():
    fig, ax = canvas(9.5, 3.4)
    box(ax, 0.2, 1.35, 1.8, 0.7, "try:\nrisky code", color=BLUE, mono=True, fontsize=10)
    box(ax, 3.3, 2.3, 2.2, 0.7, "else:\nonly if no error", color=TEAL, mono=True, fontsize=9.5)
    box(ax, 3.3, 0.4, 2.2, 0.7, "except Error:\nhandle it", color=RED, mono=True, fontsize=9.5)
    box(ax, 6.9, 1.35, 2.3, 0.7, "finally:\nalways runs", color=PURPLE, mono=True, fontsize=9.5)
    arrow(ax, 2.05, 1.85, 3.25, 2.6, color=TEAL, text="no error", text_offset=(-0.35, 0.08))
    arrow(ax, 2.05, 1.55, 3.25, 0.8, color=RED, text="error", text_offset=(-0.3, -0.38))
    arrow(ax, 5.55, 2.6, 6.85, 1.85, color=TEAL)
    arrow(ax, 5.55, 0.8, 6.85, 1.55, color=RED)
    label(ax, 4.75, 3.25, "safe_divide(10, 4) takes the top path; safe_divide(1, 0) the bottom", size=9.5, color=GREY)
    return fig


def class_objects():
    fig, ax = canvas(9, 3.2)
    box(ax, 0.3, 0.6, 2.8, 2.1, "", color=ORANGE)
    label(ax, 1.7, 2.4, "class Dog", mono=True, bold=True)
    label(ax, 1.7, 1.85, "name", mono=True, size=10)
    label(ax, 1.7, 1.5, "age", mono=True, size=10)
    label(ax, 1.7, 1.05, "bark()", mono=True, size=10, color=ORANGE)
    label(ax, 1.7, 0.3, "the blueprint", size=9.5, color=GREY)
    for i, (n, nm, age) in enumerate([("rex", "Rex", 3), ("fido", "Fido", 7)]):
        y = 1.75 - i * 1.25
        arrow(ax, 3.15, 1.65, 4.6, y + 0.4, color=GREY)
        label(ax, 3.75 if i == 0 else 4.0, 2.3 if i == 0 else 0.8, f'Dog("{nm}", {age})', size=9, mono=True, color=GREY)
        box(ax, 4.65, y, 3.2, 0.85, "", color=TEAL)
        label(ax, 5.0, y + 0.6, n, mono=True, bold=True, ha="left")
        label(ax, 5.0, y + 0.25, f'name="{nm}"   age={age}', mono=True, size=9.5, ha="left")
    label(ax, 6.25, 0.1, "objects: each keeps its own values", size=9.5, color=GREY)
    return fig


def inheritance_tree():
    fig, ax = canvas(8.5, 3.3)
    box(ax, 2.6, 2.0, 3.3, 1.05, "", color=ORANGE)
    label(ax, 4.25, 2.8, "Animal", mono=True, bold=True)
    label(ax, 4.25, 2.4, 'name   speak() → "..."', mono=True, size=9.5)
    label(ax, 4.25, 2.15, "introduce()", mono=True, size=9.5)
    for i, (n, s) in enumerate([("Dog", '"Woof"'), ("Cat", '"Meow"')]):
        x = 0.6 + i * 4.3
        box(ax, x, 0.45, 3.0, 0.85, "", color=TEAL)
        label(ax, x + 1.5, 1.05, f"{n}(Animal)", mono=True, bold=True)
        label(ax, x + 1.5, 0.7, f"speak() → {s}", mono=True, size=9.5)
        arrow(ax, x + 1.5, 1.35, 4.25, 1.95, color=INK)
    label(ax, 4.25, 0.1, "children inherit name and introduce(), and replace speak() with their own", size=9.5, color=GREY)
    label(ax, 2.75, 1.85, "is an", size=9.5, color=GREY, italic=True)
    return fig


def big_o():
    n = np.linspace(1, 32, 200)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    curves = [("O(n²)", n ** 2, RED), ("O(n log n)", n * np.log2(n), ORANGE), ("O(n)", n, BLUE),
              ("O(log n)", np.log2(n), TEAL), ("O(1)", np.ones_like(n), GREEN)]
    where = {"O(n²)": (11.4, 112), "O(n log n)": (25.5, 100), "O(n)": (32.6, 32), "O(log n)": (32.6, 14), "O(1)": (32.6, 4)}
    for name, y, c in curves:
        ax.plot(n, y, color=c, linewidth=2.2)
        ax.text(*where[name], name, color=c, va="center", fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, 120)
    ax.set_xlim(1, 38)
    ax.set_xlabel("n (number of items)")
    ax.set_ylabel("steps")
    ax.set_title("How the work grows as the input grows")
    return fig


FIGS = {"run-stages": run_stages, "variables": variables, "string-index": string_index, "string-slice": string_slice,
        "if-elif": if_elif, "for-loop": for_loop, "list-references": list_refs, "dict-keys-values": dict_keys,
        "set-operations": set_ops, "comprehension": comprehension, "function-machine": function_machine,
        "legb": legb, "recursion-stack": recursion_stack, "try-except-flow": try_flow,
        "class-objects": class_objects, "inheritance-tree": inheritance_tree, "big-o": big_o}

if __name__ == "__main__":
    for name, fn in FIGS.items():
        # coloured pieces of one line of code must line up exactly, so draw that text as shapes
        with plt.rc_context({"svg.fonttype": "path"} if name == "comprehension" else {}):
            save(fn(), OUT / f"{name}.svg")
    print(len(FIGS), "figures")
