# Editing the course

Everything in the repository root (the sandbox, `lessons/`, `glossary.md`, `cheatsheet.md` and `README.md`) is generated from the files in this folder. Edit the sources here, then rebuild.

```bash
pip install markdown
python course/build.py --test
```

`--test` runs every example and every exercise solution with your local Python, and fails if anything is broken.

| File | What it is |
|---|---|
| `content/part1.md` … `part7.md` | lesson text, examples, exercises and quizzes |
| `content/extras.md` | each lesson's topics, key terms and common mistakes |
| `content/cheatsheet.md` | the syntax cheat sheet |
| `page.html`, `app.js` | the sandbox page and its logic |
| `playground.html` | the standalone playground |
| `figures.py` | draws the lesson diagrams in `figures/` (run it after changing a diagram) |
| `build.py` | builds everything and tests the lesson code |

## Lesson format

````text
@@@ lesson
id: my-lesson
title: My lesson
minutes: 10
summary: One sentence shown under the title.
---
Normal **Markdown** text. Use ### for section headings.

```python
print("A runnable example")
```

```python stdin=Ada|36 error
# stdin= fills the Input box (| separates lines); error marks an example meant to fail
```

:::exercise Exercise title
What the learner should do.
```python starter
# code the learner starts with
```
```python check
assert something, "message shown when the check fails"
# __output__ holds what the learner's code printed; __source__ holds their code
```
```python solution
# a correct answer
```
hint: A nudge in the right direction.
:::

:::quiz
? Question text?
- wrong answer
+ right answer
= Explanation shown after answering.
:::
````

Each lesson also needs an entry in `content/extras.md`:

```text
@@ my-lesson
topics: short list of topics for the README table
terms:
- **Term:** definition
mistakes:
- A common mistake and how to avoid it.
```
