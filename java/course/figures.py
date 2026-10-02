"""Draw the lesson diagrams into figures/ as SVG files.  Run:  python figures.py"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))

import matplotlib.pyplot as plt
from diag import TEAL, ORANGE, BLUE, RED, GREY, INK, PURPLE, GREEN, SOFT, canvas, box, arrow, label, save

# The Python course draws the same Big-O chart and recursion stack; reuse them.
_spec = importlib.util.spec_from_file_location("pyfigs", HERE.parents[1] / "python" / "course" / "figures.py")
pyfigs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pyfigs)

OUT = HERE / "figures"


def cells(ax, x, y, values, w=0.62, h=0.55, fills=None, color=TEAL, fontsize=11):
    for i, v in enumerate(values):
        box(ax, x + i * w, y, w - 0.04, h, str(v), color=fills[i] if fills else color, round_=0.02, fontsize=fontsize, mono=True)


def compile_run():
    fig, ax = canvas(11, 2.9)
    box(ax, 0.1, 1.2, 1.9, 0.9, "Main.java\nsource code", color=GREY, mono=True, fontsize=9.5)
    arrow(ax, 2.05, 1.65, 2.65, 1.65)
    box(ax, 2.7, 1.2, 1.7, 0.9, "javac\ncompiler", color=ORANGE, mono=True, fontsize=10, bold=True)
    arrow(ax, 4.45, 1.65, 5.05, 1.65)
    box(ax, 5.1, 1.2, 1.9, 0.9, "Main.class\nbytecode", color=BLUE, mono=True, fontsize=9.5)
    arrow(ax, 7.05, 1.65, 7.65, 1.65)
    box(ax, 7.7, 1.2, 1.5, 0.9, "JVM\nruns it", color=TEAL, mono=True, fontsize=10, bold=True)
    arrow(ax, 9.25, 1.65, 9.65, 1.65)
    box(ax, 9.7, 1.2, 1.1, 0.9, "Hello", color=PURPLE, mono=True)
    label(ax, 1.05, 2.4, "step 1: compile", size=10, bold=True, color=ORANGE)
    ax.plot([0.1, 7.0], [2.25, 2.25], color=ORANGE, linewidth=1)
    label(ax, 8.6, 2.4, "step 2: run", size=10, bold=True, color=TEAL)
    ax.plot([7.7, 10.8], [2.25, 2.25], color=TEAL, linewidth=1)
    label(ax, 3.55, 0.75, "compile errors (a missing ;)\nare caught here, before running", size=9, color=RED)
    label(ax, 8.45, 0.75, "runtime exceptions (like 1 / 0)\nhappen here, while running", size=9, color=RED)
    label(ax, 6.05, 0.75, "same file runs on Windows,\nmacOS, Linux, a browser", size=9, color=BLUE)
    return fig


def string_index():
    fig, ax = canvas(9.4, 2.6)
    s = "Hello, World"
    x0 = 0.6
    w = 0.68
    fills = [TEAL] * 5 + [GREY, GREY] + [ORANGE] * 5
    cells(ax, x0, 1.0, [c if c != " " else "␣" for c in s], w=w, h=0.6, fills=fills)
    for i in range(len(s)):
        label(ax, x0 + w / 2 - 0.02 + i * w, 1.85, str(i), size=10, mono=True)
    label(ax, x0 + 2.5 * w, 0.6, 's.substring(0, 5) → "Hello"', size=10, mono=True, color=TEAL)
    label(ax, x0 + 9.5 * w, 0.6, 's.substring(7) → "World"', size=10, mono=True, color=ORANGE)
    label(ax, 4.7, 0.15, "end is not included: substring(0, 5) stops before index 5", size=9.5, color=GREY)
    label(ax, 4.7, 2.35, 's.length() is 12, so the last index is 11', size=9.5, color=GREY)
    return fig


def array_boxes():
    fig, ax = canvas(7.5, 2.3)
    label(ax, 1.2, 1.32, "scores", mono=True, bold=True, ha="right")
    arrow(ax, 1.3, 1.32, 1.75, 1.32)
    cells(ax, 1.8, 1.05, [90, 72, 85], w=0.9, h=0.55, color=TEAL, fontsize=12)
    for i in range(3):
        label(ax, 2.23 + i * 0.9, 1.85, f"[{i}]", size=10, mono=True, color=GREY)
    label(ax, 3.15, 0.65, "scores.length is 3   ·   scores[3] is out of bounds", size=9.5, mono=True)
    label(ax, 6.0, 1.32, "fixed size,\none type (int)", size=9.5, color=GREY, ha="left")
    return fig


def grid_2d():
    fig, ax = canvas(7.5, 2.9)
    vals = [[1, 2, 3], [4, 5, 6]]
    for r in range(2):
        label(ax, 1.55, 1.82 - r * 0.7, f"row {r}", size=9.5, color=GREY, ha="right")
        for c in range(3):
            hit = (r, c) == (1, 2)
            box(ax, 1.7 + c * 0.8, 1.55 - r * 0.7, 0.74, 0.6, str(vals[r][c]), color=ORANGE if hit else TEAL, round_=0.02, mono=True, fontsize=12,
                bold=hit)
    for c in range(3):
        label(ax, 2.07 + c * 0.8, 2.45, f"col {c}", size=9.5, color=GREY)
    label(ax, 6.3, 1.25, "grid[1][2] is 6\nrow first, then column", size=10, color=ORANGE, ha="center")
    label(ax, 3.3, 0.35, "grid.length = 2 rows   ·   grid[0].length = 3 columns", size=9.5, mono=True)
    return fig


def references():
    fig, ax = canvas(9, 3.0)
    label(ax, 1.9, 2.75, "the variables", size=10, bold=True, color=GREY)
    label(ax, 6.6, 2.75, "the objects", size=10, bold=True, color=GREY)
    box(ax, 0.6, 1.75, 2.6, 0.55, "int count = 5", color=BLUE, mono=True, fontsize=10)
    label(ax, 3.4, 2.02, "← a primitive holds the value itself", size=9, color=BLUE, ha="left")
    for i, n in enumerate(["first", "second"]):
        y = 0.95 - i * 0.7
        box(ax, 0.6, y, 2.6, 0.55, f"Box {n}", color=GREY, mono=True, fontsize=10)
        arrow(ax, 3.25, y + 0.27, 5.55, 0.55, color=INK)
    box(ax, 5.6, 0.2, 2.4, 0.8, "a Box object\nvalue = 99", color=ORANGE, mono=True, fontsize=10)
    label(ax, 6.8, 1.35, "one object, two arrows:\nsecond = first copies the arrow", size=9, color=ORANGE)
    return fig


def inheritance_tree():
    fig, ax = canvas(8.5, 4.2)
    box(ax, 3.2, 3.35, 2.1, 0.55, "Object", color=GREY, mono=True, bold=True)
    label(ax, 5.5, 3.62, "every class extends Object", size=9, color=GREY, ha="left")
    arrow(ax, 4.25, 2.95, 4.25, 3.3, color=GREY)
    box(ax, 2.6, 1.9, 3.3, 1.0, "", color=ORANGE)
    label(ax, 4.25, 2.62, "Animal", mono=True, bold=True)
    label(ax, 4.25, 2.3, 'name   speak() → "..."', mono=True, size=9.5)
    label(ax, 4.25, 2.05, "introduce()", mono=True, size=9.5)
    for i, (n, s) in enumerate([("Dog", '"Woof"'), ("Cat", '"Meow"')]):
        x = 0.4 + i * 4.7
        box(ax, x, 0.45, 3.0, 0.85, "", color=TEAL)
        label(ax, x + 1.5, 1.05, f"{n} extends Animal", mono=True, bold=True, size=10)
        label(ax, x + 1.5, 0.7, f"@Override speak() → {s}", mono=True, size=9)
        arrow(ax, x + 1.5, 1.35, 4.25, 1.85, color=INK)
    label(ax, 4.25, 0.1, "arrows point from child to parent: a Dog is an Animal", size=9.5, color=GREY)
    return fig


def try_catch():
    fig, ax = canvas(10, 3.6)
    box(ax, 0.2, 1.45, 2.3, 0.75, "try {\n  parse and divide }", color=BLUE, mono=True, fontsize=9.5)
    rows = [("no exception\nreturn the answer", TEAL, 2.7), ('NumberFormatException\ncatch: "Not a number"', RED, 1.45),
            ("ArithmeticException\ncatch: \"Can't divide by zero\"", ORANGE, 0.2)]
    for text, c, y in rows:
        arrow(ax, 2.55, 1.82, 3.75, y + 0.37, color=c)
        box(ax, 3.8, y, 3.5, 0.75, text, color=c, mono=True, fontsize=9)
        arrow(ax, 7.35, y + 0.37, 7.85, 1.82, color=c)
    box(ax, 7.9, 1.45, 1.9, 0.75, "finally {\n  always runs }", color=PURPLE, mono=True, fontsize=9.5)
    return fig


def exception_tree():
    fig, ax = canvas(11.2, 4.0)
    def node(x, y, w, text, c, note=None):
        box(ax, x, y, w, 0.48, text, color=c, mono=True, fontsize=9.5)
        if note:
            label(ax, x + w + 0.15, y + 0.24, note, size=8.5, color=c, ha="left")
    node(3.4, 3.4, 2.0, "Throwable", GREY)
    node(0.6, 2.5, 1.6, "Error", RED, "JVM trouble:\ndon't catch")
    node(5.2, 2.5, 1.8, "Exception", BLUE)
    node(2.8, 1.5, 2.2, "IOException ...", BLUE, None)
    node(6.6, 1.5, 2.5, "RuntimeException", ORANGE)
    arrow(ax, 1.4, 2.98, 4.0, 3.38, color=GREY, style="-")
    arrow(ax, 6.1, 2.98, 4.8, 3.38, color=GREY, style="-")
    arrow(ax, 3.9, 1.98, 5.6, 2.48, color=GREY, style="-")
    arrow(ax, 7.85, 1.98, 6.6, 2.48, color=GREY, style="-")
    label(ax, 3.9, 1.2, "checked: must catch\nor declare with throws", size=8.5, color=BLUE)
    kids = ["NullPointer", "IllegalArgument", "IndexOutOfBounds", "Arithmetic"]
    for i, k in enumerate(kids):
        x = 4.3 + i * 1.72
        box(ax, x, 0.2, 1.64, 0.6, k + "\nException", color=ORANGE, mono=True, fontsize=8)
        arrow(ax, x + 0.82, 0.82, 7.85, 1.48, color=GREY, style="-", lw=1)
    label(ax, 2.3, 0.5, "unchecked (orange):\nusually bugs in the code", size=8.5, color=ORANGE)
    return fig


def collections_map():
    fig, ax = canvas(11, 3.6)
    box(ax, 2.55, 2.75, 2.2, 0.55, "Collection", color=GREY, mono=True, bold=True)
    for x, name, c, kids, note in [(0.2, "List", TEAL, ["ArrayList", "LinkedList"], "ordered, duplicates ok"),
                                   (3.9, "Set", BLUE, ["HashSet", "TreeSet"], "no duplicates")]:
        box(ax, x + 0.8, 1.7, 1.6, 0.55, name, color=c, mono=True, bold=True)
        arrow(ax, x + 1.6, 2.28, 3.65, 2.72, color=GREY, style="-")
        label(ax, x + 1.6 + (-0.9 if name == "List" else 0.9), 2.42, note, size=8.5, color=c)
        for j, k in enumerate(kids):
            box(ax, x + j * 1.65, 0.6, 1.55, 0.55, k, color=c, mono=True, fontsize=9.5)
            arrow(ax, x + j * 1.65 + 0.77, 1.18, x + 1.6, 1.67, color=GREY, style="-")
    box(ax, 8.2, 1.7, 1.6, 0.55, "Map", color=ORANGE, mono=True, bold=True)
    label(ax, 9.0, 2.6, "key → value pairs\n(not a Collection)", size=8.5, color=ORANGE)
    for j, k in enumerate(["HashMap", "TreeMap"]):
        box(ax, 7.4 + j * 1.65, 0.6, 1.55, 0.55, k, color=ORANGE, mono=True, fontsize=9.5)
        arrow(ax, 7.4 + j * 1.65 + 0.77, 1.18, 9.0, 1.67, color=GREY, style="-")
    label(ax, 5.5, 0.15, "Hash… versions are fastest; Tree… versions keep things sorted", size=9.5, color=GREY)
    return fig


def stream_pipeline():
    fig, ax = canvas(12, 3.2)
    stages = [("nums.stream()", [5, 12, 7, 20, 3, 18], GREY), (".filter(n -> n > 6)", [12, 7, 20, 18], TEAL),
              (".map(n -> n * 2)", [24, 14, 40, 36], ORANGE), (".sorted()", [14, 24, 36, 40], PURPLE)]
    x = 0.1
    centres = []
    for i, (op, vals, c) in enumerate(stages):
        w = 0.42 * len(vals)
        centres.append(x + w / 2)
        label(ax, x + w / 2, 2.75, op, mono=True, size=9.5, color=c, bold=True)
        for j, v in enumerate(vals):
            box(ax, x + j * 0.42, 1.9, 0.38, 0.5, str(v), color=c, round_=0.02, mono=True, fontsize=9)
        arrow(ax, x + w + 0.03, 2.15, x + w + 0.67, 2.15)
        x += w + 0.72
    box(ax, x, 1.9, 1.0, 0.5, "List", color=BLUE, mono=True, fontsize=9.5)
    label(ax, x + 0.5, 2.75, ".toList()", mono=True, size=9.5, bold=True, color=BLUE)
    label(ax, centres[0], 1.45, "source", size=9.5, color=GREY)
    ax.plot([centres[1] - 0.8, centres[3] + 0.8], [1.6, 1.6], color=GREY, linewidth=1)
    label(ax, centres[2], 1.35, "intermediate operations (lazy: nothing runs yet)", size=9.5)
    label(ax, x + 0.5, 1.45, "terminal:\nruns it all", size=9.5, color=BLUE, va="top")
    return fig


def recursion_stack():
    return pyfigs.recursion_stack()


def big_o():
    return pyfigs.big_o()


FIGS = {"compile-and-run": compile_run, "string-index": string_index, "array": array_boxes, "two-d-array": grid_2d,
        "references": references, "inheritance-tree": inheritance_tree, "try-catch-finally": try_catch,
        "exception-hierarchy": exception_tree, "collections": collections_map, "stream-pipeline": stream_pipeline,
        "recursion-stack": recursion_stack, "big-o": big_o}

if __name__ == "__main__":
    for name, fn in FIGS.items():
        save(fn(), OUT / f"{name}.svg")
    print(len(FIGS), "figures")
