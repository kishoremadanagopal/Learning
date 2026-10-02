# Editing the Java course

Everything in `java/` (the sandbox, the game data, `lessons/`, `glossary.md`, `cheatsheet.md` and `README.md`) is generated from the files in this folder. Edit the sources here, then rebuild.

```bash
pip install markdown
python course/build.py --test
```

`--test` needs a JDK (17 or newer). It compiles and runs every example, checks every exercise solution against its tests, and confirms every Java Quest answer compiles. It fails if anything is broken.

| File | What it is |
|---|---|
| `content/part1.md` … `part7.md` | lesson text, examples, exercises and quizzes |
| `content/extras.md` | each lesson's topics, key terms and common mistakes |
| `content/cheatsheet.md` | the syntax cheat sheet |
| `content/game.md` | Java Quest challenges |
| `page.html`, `app.js` | the sandbox page and its logic |
| `game.html` | the Java Quest game |
| `runner/` | the Java program that compiles, runs and checks code in the browser |
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

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("A runnable example");
    }
}
```

```java stdin=Ada|36 error
// stdin= fills the Input box (| separates lines); error marks an example meant to fail
```

:::exercise Exercise title
What the learner should do.
```java starter
// code the learner starts with
```
```java check
eq(10, call("twice", 5), "twice(5)");   // statements; see runner/src/course/T.java for helpers
outputIs("expected output");
```
```java solution
// a correct answer
```
hint: A nudge in the right direction.
:::
````
