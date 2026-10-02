# Learn Python for Data: NumPy, pandas and charts

A hands-on course that takes you from "I know a little Python" to cleaning, analysing and charting real data: 1 lessons on NumPy, pandas and matplotlib, with a practice sandbox that runs real pandas in your browser and checks your answers.

This is the shared core for both the **AI engineer** and the **data / AI analyst** paths: every one of those jobs loads, cleans, summarises and charts data first.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/python-data/)

The sandbox runs real Python 3.14 with NumPy, pandas and matplotlib inside your browser (via [Pyodide](https://pyodide.org)). Nothing to install, no sign-up.

- every lesson, with **3 examples** you can run and change
- **2 exercises**, numbered by lesson, that check your code and tell you what's off
- **1 quiz questions**, with explanations
- **7 practice datasets** that load with one line, like `pd.read_csv("sales.csv")`
- charts drawn right under your code
- your progress and code saved in your own browser

**Before you start:** you should know Python basics: variables, lists, dictionaries, loops, `if` and functions. If you don't yet, do lessons 1 to 20 of [Learn Python from scratch](../python/) first.

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 1 lessons, each with key terms, examples, common mistakes, exercises, answers and a quiz |
| 📖 [Glossary](glossary.md) | every data term used in the course, defined in plain English |
| 🧾 [Cheat sheet](cheatsheet.md) | NumPy, pandas and matplotlib on one page, with lesson numbers |
| 🗂️ [Datasets](https://github.com/kishoremadanagopal/learning/tree/main/python-data/data) | the practice files, to download and use on your own computer |

## How to use this course

1. Read a lesson, here on GitHub or in the sandbox. Start with its **Key terms**.
2. Run the examples in the sandbox and change them to see what happens.
3. Do the lesson's exercises in the sandbox and press **Check**.
4. Only then open the **Answers** section at the bottom of the lesson.

## Lessons

### Part 0: Smoke (Beginner)

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 1 | [Smoke test](lessons/01-smoke.md) | test | 1–2 |

## The practice datasets

| File | Rows | What's in it |
|---|---|---|
| [`sales.csv`](data/sales.csv) | 600 | 600 orders from 2025: date, customer, region, product, units and price. |
| [`customers.csv`](data/customers.csv) | 120 | 120 customers: name, city, segment, age and signup date. |
| [`products.csv`](data/products.csv) | 8 | 8 products with category, price, cost and supplier. |
| [`employees_messy.csv`](data/employees_messy.csv) | 40 | An HR export full of problems to clean: stray spaces, mixed capitals, text salaries, gaps and duplicates. |
| [`weather.csv`](data/weather.csv) | 1095 | Daily temperature and rain for London, Mumbai and New York in 2025. |
| [`students.csv`](data/students.csv) | 60 | 60 students: class, hours studied, attendance and exam scores. |
| [`movies.json`](data/movies.json) | 40 | 40 (made-up) films: year, genre, runtime, rating and box office. |

All of the data is made up for practice, so it's safe to share and experiment with.

## Running it on your own computer

Everything in the course also works in a normal Python setup. Install Python from [python.org](https://www.python.org/), then:

```bash
pip install numpy pandas matplotlib jupyterlab
jupyter lab
```

Download the files from [`data/`](data/) into the same folder as your notebook. The sandbox runs pandas 3, so if your computer has an older pandas, upgrade with `pip install --upgrade pandas`.

## Editing the course

Lessons are generated from the Markdown sources in [`course/`](course/). See [course/README.md](course/README.md).
