"""Draw the diagrams used in the SQL lessons (run: python sql/figures/make_figures.py)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from diag import *  # noqa: E402,F401,F403
import matplotlib.pyplot as plt  # noqa: E402


def tables_keys():
    fig, ax = canvas(9.6, 3.6, xlim=(0, 9.6), ylim=(0, 3.6))
    label(ax, 1.75, 3.45, "customers", bold=True, mono=True)
    table(ax, 0.1, 3.25, ["id", "name", "city"], [[1, "Maya", "Fremont"], [2, "Leo", "Oakland"], [3, "Priya", "Fremont"], [4, "Sam", "San Jose"], [5, "Ana", "Oakland"]],
          [0.6, 1.0, 1.6], highlight={0: TEAL})
    label(ax, 6.9, 3.45, "orders", bold=True, mono=True)
    table(ax, 4.9, 3.25, ["order_id", "customer_id", "product"], [[101, 1, "Laptop"], [102, 1, "Mouse"], [103, 2, "Desk"], [104, 3, "Chair"], [105, 5, "Monitor"]],
          [1.2, 1.6, 1.3], highlight={0: ORANGE, 1: ORANGE})
    arrow(ax, 5.7, 2.7, 0.75, 2.62, color=ORANGE, rad=0.35)
    label(ax, 3.4, 0.55, "primary key: customers.id  ·  foreign key: orders.customer_id points to it", size=10.5)
    label(ax, 3.4, 0.2, "Orders 101 and 102 belong to customer 1 (Maya). Sam (id 4) has no orders.", size=10, color=GREY)
    return fig


def group_by():
    fig, ax = canvas(10, 3.4, xlim=(0, 10), ylim=(0, 3.4))
    colors = {"Fremont": TEAL, "Oakland": ORANGE, "San Jose": BLUE}
    rows = [("Maya", "Fremont"), ("Leo", "Oakland"), ("Priya", "Fremont"), ("Sam", "San Jose"), ("Ana", "Oakland")]
    label(ax, 1.4, 3.2, "1. rows", bold=True)
    for i, (n, c) in enumerate(rows):
        box(ax, 0.2, 2.6 - i * 0.5, 2.4, 0.4, f"{n} · {c}", color=colors[c], fontsize=9.5)
    arrow(ax, 2.8, 1.7, 3.5, 1.7, text="GROUP BY\ncity", fontsize=9.5)
    label(ax, 5.0, 3.2, "2. piles", bold=True)
    y = 2.6
    for city in colors:
        members = [n for n, c in rows if c == city]
        box(ax, 3.7, y - 0.45 * (len(members) - 1), 2.6, 0.45 * len(members) - 0.05, "\n".join(members), color=colors[city], fontsize=9.5)
        y -= 0.45 * len(members) + 0.2
    arrow(ax, 6.5, 1.7, 7.2, 1.7, text="COUNT(*)", fontsize=9.5)
    label(ax, 8.55, 3.2, "3. one row per group", bold=True)
    table(ax, 7.4, 2.95, ["city", "count"], [["Fremont", 2], ["Oakland", 2], ["San Jose", 1]], [1.6, 1.0], highlight={0: TEAL, 1: ORANGE, 2: BLUE})
    return fig


def execution_order():
    fig, ax = canvas(11, 2.6, xlim=(0, 11), ylim=(0, 2.6))
    written = ["SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT"]
    run = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY", "LIMIT"]
    label(ax, 0.05, 2.15, "You write:", ha="left", bold=True)
    label(ax, 0.05, 0.75, "SQL runs:", ha="left", bold=True)
    for i, (w, r) in enumerate(zip(written, run)):
        x = 1.45 + i * 1.35
        box(ax, x, 1.9, 1.12, 0.5, w, color=GREY, fontsize=9.5, mono=True)
        col = ORANGE if r == "SELECT" else TEAL
        box(ax, x, 0.5, 1.12, 0.5, r, color=col, fontsize=9.5, mono=True, bold=r == "SELECT")
        if i:
            arrow(ax, x - 0.21, 0.75, x - 0.02, 0.75, lw=1.2)
    label(ax, 5.8, 0.18, "SELECT runs after WHERE and HAVING: that's why aliases and aggregates can't be used in WHERE", size=9.5, color=RED)
    return fig


def join_types():
    fig, ax = canvas(12.5, 2.6, xlim=(0, 12.5), ylim=(0, 2.6))
    specs = [("INNER JOIN", ("middle",)), ("LEFT JOIN", ("left", "middle")), ("RIGHT JOIN", ("middle", "right")),
             ("FULL OUTER JOIN", ("left", "middle", "right")), ("LEFT JOIN … IS NULL", ("left",))]
    for i, (t, shade) in enumerate(specs):
        venn(ax, 1.25 + i * 2.5, 1.45, r=0.6, gap=0.6, shade=shade, color=TEAL if i < 4 else ORANGE, title=t, labels=("c", "o"))
    label(ax, 6.25, 0.12, "c = customers (left table), o = orders (right table); shaded = rows kept", size=9.5, color=GREY)
    return fig


def case_bands():
    fig, ax = plt.subplots(figsize=(9, 1.9))
    ax.set_xlim(10, 70); ax.set_ylim(0, 1)
    ax.axis("off")
    for lo, hi, name, c in [(10, 30, "'Young'  (age < 30)", TEAL), (30, 50, "'Middle'  (age < 50)", ORANGE), (50, 70, "'Senior'  (ELSE)", BLUE)]:
        ax.add_patch(plt.Rectangle((lo, 0.35), hi - lo, 0.3, color=c, alpha=0.35))
        ax.text((lo + hi) / 2, 0.5, name, ha="center", va="center", fontsize=10.5, family="monospace")
    for v in (30, 50):
        ax.axvline(v, ymin=0.25, ymax=0.75, color=INK, linewidth=1.5)
        ax.text(v, 0.12, f"{v} → {'Middle' if v == 30 else 'Senior'}", ha="center", fontsize=9.5)
    for name, age in [("Sam", 19), ("Leo", 27), ("Maya", 34), ("Priya", 41), ("Ana", 52)]:
        ax.plot(age, 0.8, "o", color=INK)
        ax.text(age, 0.9, name, ha="center", fontsize=9)
    ax.set_title("CASE checks WHENs top to bottom: the first true one wins, so each boundary belongs to the next band", fontsize=11)
    return fig


def window_vs_group():
    fig, ax = canvas(11, 4.1, xlim=(0, 11), ylim=(0, 4.1))
    rows = [("Bob", "Eng", 95000), ("Dev", "Eng", 105000), ("Frank", "Eng", 88000), ("Emma", "Mkt", 70000), ("Grace", "Mkt", 62000),
            ("Alice", "Sales", 60000), ("Carla", "Sales", 55000), ("Hank", "Sales", 72000)]
    hl = {i: (BLUE if d == "Eng" else ORANGE if d == "Mkt" else TEAL) for i, (_, d, _) in enumerate(rows)}
    label(ax, 1.75, 3.95, "employees (8 rows)", bold=True)
    table(ax, 0.1, 3.75, ["name", "dept", "salary"], rows, [1.0, 0.9, 1.3], rowh=0.36, highlight=hl, fontsize=9)
    arrow(ax, 3.45, 2.9, 4.2, 3.2, text="GROUP BY", fontsize=9.5)
    label(ax, 5.6, 3.95, "GROUP BY: 3 rows", bold=True)
    table(ax, 4.4, 3.75, ["dept", "avg"], [["Eng", 96000], ["Mkt", 66000], ["Sales", 62333]], [1.0, 1.3], rowh=0.36,
          highlight={0: BLUE, 1: ORANGE, 2: TEAL}, fontsize=9)
    arrow(ax, 3.45, 1.6, 6.85, 1.6, text="AVG(salary) OVER (PARTITION BY dept)", fontsize=9.5)
    label(ax, 8.9, 3.95, "window: all 8 rows kept", bold=True)
    avg = {"Eng": 96000, "Mkt": 66000, "Sales": 62333}
    table(ax, 7.0, 3.75, ["name", "salary", "dept_avg"], [(n, s, avg[d]) for n, d, s in rows], [1.0, 1.3, 1.3], rowh=0.36, highlight=hl, fontsize=9)
    return fig


def window_frame():
    fig, ax = canvas(9.5, 3.4, xlim=(0, 9.5), ylim=(0, 3.4))
    rows = [("2025-11-20", 1200, "1200"), ("2025-12-02", 25, "612.5"), ("2026-01-10", 300, "508.3"), ("2026-01-25", 150, "158.3"),
            ("2026-02-14", 400, "283.3"), ("2026-02-14", 80, "210"), ("2026-03-03", 45, "175")]
    table(ax, 0.2, 3.2, ["order_date", "amount", "moving_avg"], rows, [1.8, 1.2, 1.5], rowh=0.36, highlight={2: ORANGE, 3: ORANGE, 4: TEAL}, fontsize=9.5)
    label(ax, 7.2, 2.3, "ROWS BETWEEN 2 PRECEDING\nAND CURRENT ROW", mono=True, size=10)
    label(ax, 7.2, 1.45, "For the teal row, the average uses\nit and the two orange rows above:\n(300 + 150 + 400) / 3 = 283.3", size=10)
    arrow(ax, 5.6, 1.45, 4.85, 1.28, color=TEAL)
    return fig


def union_vs_join():
    fig, ax = canvas(10, 3.0, xlim=(0, 10), ylim=(0, 3.0))
    label(ax, 2.3, 2.85, "JOIN: side by side (more columns)", bold=True)
    box(ax, 0.4, 0.6, 1.6, 1.9, "customers\ncolumns", color=TEAL)
    box(ax, 2.1, 0.6, 1.6, 1.9, "orders\ncolumns", color=ORANGE)
    label(ax, 2.05, 0.35, "rows matched with ON", size=9.5, color=GREY)
    label(ax, 7.4, 2.85, "UNION: stacked (more rows)", bold=True)
    box(ax, 6.4, 1.6, 2.0, 0.9, "SELECT name\nFROM customers", color=TEAL, mono=True, fontsize=9)
    box(ax, 6.4, 0.6, 2.0, 0.9, "SELECT name\nFROM employees", color=BLUE, mono=True, fontsize=9)
    label(ax, 7.4, 0.35, "same number of columns on both sides", size=9.5, color=GREY)
    return fig


def gaps_islands():
    fig, ax = plt.subplots(figsize=(9, 2.2))
    days = list(range(1, 11))
    logged = [1, 1, 1, 0, 1, 1, 0, 0, 1, 1]
    colors = {0: TEAL, 1: ORANGE, 2: BLUE}
    island, cur = [], -1
    for i, l in enumerate(logged):
        if l and (i == 0 or not logged[i - 1]):
            cur += 1
        island.append(cur if l else None)
    for d, l, isl in zip(days, logged, island):
        ax.add_patch(plt.Rectangle((d - 0.45, 0.3), 0.9, 0.5, color=colors[isl] if l else "#eef1f4"))
        ax.text(d, 0.55, f"Mar {d}", ha="center", va="center", fontsize=9, color="white" if l else GREY)
    for k, (a, b) in enumerate([(1, 3), (5, 6), (9, 10)]):
        ax.text((a + b) / 2, 1.0, f"streak of {b - a + 1}", ha="center", fontsize=10, color=colors[k], fontweight="bold")
    ax.set_xlim(0.4, 10.6); ax.set_ylim(0.1, 1.25); ax.axis("off")
    ax.set_title("Gaps and islands: within a streak, date minus ROW_NUMBER() stays the same", fontsize=11.5)
    return fig


def pivot():
    fig, ax = canvas(10.4, 3.6, xlim=(0, 10.4), ylim=(0, 3.6))
    rows = [("Bob", "Engineering", 1), ("Dev", "Engineering", 2), ("Frank", "Engineering", 3), ("Emma", "Marketing", 1),
            ("Grace", "Marketing", 2), ("Alice", "Sales", 1), ("Carla", "Sales", 2), ("Hank", "Sales", 3)]
    hl = {i: (BLUE if d == "Engineering" else ORANGE if d == "Marketing" else TEAL) for i, (_, d, _) in enumerate(rows)}
    label(ax, 2.1, 3.45, "long: one row per person", bold=True)
    table(ax, 0.1, 3.25, ["name", "department", "rn"], rows, [1.0, 2.0, 0.6], rowh=0.32, highlight=hl, fontsize=9)
    arrow(ax, 3.9, 1.9, 4.9, 1.9, text="MAX(CASE …)\nGROUP BY rn", fontsize=9)
    label(ax, 7.65, 3.45, "wide: one column per department", bold=True)
    table(ax, 5.1, 3.25, ["rn", "Engineering", "Marketing", "Sales"], [[1, "Bob", "Emma", "Alice"], [2, "Dev", "Grace", "Carla"], [3, "Frank", "NULL", "Hank"]],
          [0.5, 1.6, 1.4, 1.1], rowh=0.42, fontsize=9.5)
    return fig


def monthly_totals():
    fig, ax = plt.subplots(figsize=(7, 3))
    months = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]
    totals = [1200, 25, 450, 480, 45]
    bars = ax.bar(months, totals, color=TEAL)
    ax.bar_label(bars, padding=3)
    ax.set_ylabel("total amount")
    ax.set_title("GROUP BY strftime('%Y-%m', order_date): one bar per group", fontsize=11.5)
    ax.set_ylim(0, 1400)
    return fig


FIGS = {"tables-keys": tables_keys, "group-by": group_by, "execution-order": execution_order, "join-types": join_types,
        "case-bands": case_bands, "window-vs-group-by": window_vs_group, "window-frame": window_frame,
        "union-vs-join": union_vs_join, "gaps-and-islands": gaps_islands, "pivot": pivot, "monthly-totals": monthly_totals}

if __name__ == "__main__":
    for name, make in FIGS.items():
        save(make(), HERE / f"{name}.svg")
    print(len(FIGS), "figures")
