# Editing the course

Everything in the folder above (the sandbox, `lessons/`, `data/`, `glossary.md`, `cheatsheet.md` and `README.md`) is generated from the files here. Edit the sources, then rebuild.

```bash
pip install markdown numpy pandas==3.0.2 matplotlib scipy statsmodels
python course/build.py --test
```

`--test` runs every example and exercise with the same `runner.py` the browser sandbox uses, and fails if a solution doesn't pass, a starter already passes, or an example's error flag is wrong. `--show <lesson-id>` prints each example's output so you can check the lesson text matches it.

| File | What it is |
|---|---|
| `content/part1.md` … | lesson text, examples, exercises and quizzes |
| `content/extras*.md` | each lesson's topics, key terms and common mistakes |
| `content/cheatsheet.md` | the cheat sheet |
| `datasets.py` | generates the extra practice data in `data/` (deterministic) |
| `figures.py` | draws the lesson charts in `figures/` |
| `runner.py` | runs code and checks, in the browser (Pyodide) and in tests |
| `page.html`, `app.js`, `worker.js` | the sandbox page, its logic, and the Web Worker that runs Python |
| `build.py` | builds everything and tests the lesson code |

## Exercise checks

Check code runs after the learner's code, in the same namespace, with these helpers:

| Helper | Use |
|---|---|
| `need("name", pd.DataFrame)` | the learner's variable, or a friendly "create a variable called…" failure |
| `same(actual, expected, "what")` | compares numbers, arrays, Series and DataFrames (`ignore_index=`, `ignore_order=`) |
| `printed("text")` | the learner printed this text |
| `uses("groupby(")` | the learner's code contains this (comments ignored) |
| `chart()` | the Axes of the chart they drew |
| `__output__`, `__source__` | everything printed, and the learner's code |
