# Editing the course

Everything in the folder above (the sandbox, `lessons/`, `glossary.md`, `cheatsheet.md` and `README.md`) is generated from the files here. Edit the sources, then rebuild.

```bash
pip install markdown matplotlib
NODE_BIN=/path/to/node26 python course/build.py --test
```

`--test` runs every example and exercise with the same `runner.js` the browser sandbox uses (in Node.js 26 or newer, each run in a worker thread with a time limit), and fails if a solution doesn't pass its hidden tests, a starter already passes, an exercise has no hint or walkthrough, or an example's error flag is wrong. `--show <lesson-id>` prints each example's output so you can check the lesson text matches it.

| File | What it is |
|---|---|
| `content/part1.md` … | lesson text, examples, exercises and quizzes |
| `content/extras*.md` | each lesson's topics, key terms and common mistakes |
| `content/cheatsheet.md` | the cheat sheet |
| `figures.py` | draws the lesson diagrams in `figures/` |
| `runner.js` | runs code and checks, in the browser (Web Worker) and in tests (Node.js) |
| `harness.mjs` | the Node.js test harness |
| `page.html`, `app.js`, `worker.js` | the sandbox page, its logic, and the Web Worker that runs the code |
| `build.py` | builds everything and tests the lesson code |

## Exercise checks

Check code runs after the learner's code (as an async function), with these helpers:

| Helper | Use |
|---|---|
| `need("name", "function")` | the learner's variable or function, or a friendly "create a … called" failure |
| `same(actual, expected, "what")` | deep comparison (arrays, objects, Map, Set, Date; floats within a tiny tolerance) |
| `printed("text")` | the learner printed this text |
| `uses("reduce(")` | the learner's code contains this (comments ignored) |
| `test("fn", [[args, expected, "label"], ...], {valid, key, show})` | hidden test cases (async functions are awaited); reports the first failing input |
| `__output__`, `__source__` | everything printed, and the learner's code |
