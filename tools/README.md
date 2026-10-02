# Shared tools

| File | What it does |
|---|---|
| `diag.py` | small matplotlib helpers (boxes, arrows, tables, Venn circles) used to draw the lesson diagrams as SVG |
| `place_figures.py` | inserts `![alt](figures/name.svg)` lines into a course's `content/part*.md` files |

Each course draws its own diagrams with `course/figures.py` (SQL: `sql/figures/make_figures.py`), then `course/build.py` copies them into the published site.
