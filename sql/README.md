# Learn SQL from scratch

A complete, hands-on SQL course for beginners: 20 lessons from "what is a database" to window functions, a final project, interview patterns and the differences between today's databases, with a practice sandbox that runs your queries in the browser and checks your answers.

## ▶ [Open the practice sandbox](https://kishoremadanagopal.github.io/learning/sql/)

The sandbox runs a real SQLite database in your browser. Nothing to install, no sign-up.

- the three practice tables (`customers`, `employees`, `orders`)
- **113 exercises**, grouped by lesson, that check your answer and tell you what's off
- plain-English hints for common error messages
- **Reset data** to undo any changes you make
- your progress and correct answers saved in your own browser

## Course materials

| | |
|---|---|
| 📘 [Lessons](#lessons) | 20 lessons, each with key terms, syntax, examples, common mistakes, exercises and answers |
| 📖 [Glossary](glossary.md) | every SQL term used in the course, defined in plain English |
| 🧾 [Syntax cheat sheet](cheatsheet.md) | every statement and clause on one page, SQLite and MSSQL side by side |
| 🗂️ [The practice tables](lessons/00-the-tables.md) | the data every lesson uses |

## How to use this course

1. Read a lesson. Start with its **Key terms** and **Syntax** sections.
2. Try its exercises yourself in the sandbox's free practice mode.
3. Do the matching sandbox exercises and press **Check answer**.
4. Only then open the **Answers** section at the bottom of the lesson.

Each lesson has a **Common mistakes** section. They're real mistakes made while working through this course, so read them. You'll probably make some of the same ones.

## Lessons

### Part 1: Basics

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 0 | [What databases and SQL are](lessons/00-introduction.md) | tables, rows, keys, dialects | — |
| 1 | [First queries](lessons/01-first-queries.md) | `SELECT`, `FROM`, `WHERE` | 1 |
| 2 | [Filtering, sorting and limiting](lessons/02-filtering-sorting.md) | `AND`/`OR`/`IN`/`BETWEEN`, `ORDER BY` (ties, expressions, NULLs), `LIMIT`/`OFFSET` | 2, 5, 80–82 |
| 3 | [Aggregates and GROUP BY](lessons/03-aggregates-group-by.md) | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY` | 3, 6 |
| 4 | [HAVING](lessons/04-having.md) | `WHERE` vs `HAVING`, execution order | 4, 7–10 |

### Part 2: Combining data

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 5 | [JOINs](lessons/05-joins.md) | `JOIN`, `LEFT JOIN`, `NULL`, outer and cross joins, self joins, range joins | 11–16, 83–84 |
| 6 | [Subqueries](lessons/06-subqueries.md) | `IN` / `NOT IN` and the NULL trap, correlated subqueries, `EXISTS`, derived tables | 17–20, 85–87 |

### Part 3: Transforming data

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 7 | [CASE](lessons/07-case.md) | if/then labels, `SUM(CASE ...)`, boundaries | 21–30 |
| 8 | [Handy functions](lessons/08-functions.md) | `DISTINCT`, `LIKE`, `ROUND`/`FLOOR`/`CEIL`/`ABS`/`%`, integer division, `CAST`, `SUBSTR`/`INSTR`/`REPLACE`, `COALESCE`/`NULLIF`, `GROUP_CONCAT` | 31–37, 88–96 |
| 9 | [Dates](lessons/09-dates.md) | date filters, year/month/weekday, start of month, date math, every database side by side | 38–43, 97–98 |

### Part 4: Changing data and structure

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 10 | [Changing data](lessons/10-insert-update-delete.md) | `INSERT`, `UPDATE`, `DELETE`, safety habits, `INSERT ... SELECT`, upsert, `RETURNING`, `TRUNCATE` | 44–49, 99–100 |
| 11 | [Building tables](lessons/11-building-tables.md) | `CREATE TABLE`, data types in every database, keys, constraints, auto-numbering | 50–54 |

### Part 5: Intermediate SQL

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 12 | [CTEs](lessons/12-ctes.md) | `WITH`, multi-step queries, recursive CTEs | 55–58, 101–102 |
| 13 | [Window functions](lessons/13-window-functions.md) | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, running totals, moving averages, `LAG`, `FIRST_VALUE`, `QUALIFY` | 59–64, 103–106 |
| 14 | [UNION](lessons/14-union.md) | `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT` | 65–67 |
| 15 | [Views and indexes](lessons/15-views-indexes.md) | `CREATE VIEW`, `CREATE INDEX`, query plans | 68–70 |

### Part 6: Putting it together

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 16 | [MSSQL and transactions](lessons/16-mssql-transactions.md) | T-SQL differences, `BEGIN`/`COMMIT`/`ROLLBACK` | 71 |
| 17 | [Final project](lessons/17-final-project.md) | eight business questions using everything | 72–79 |

### Part 7: Interviews and the real world

| # | Lesson | Topics | Sandbox |
|---|---|---|---|
| 18 | [Interview and HackerRank patterns](lessons/18-interview-patterns.md) | Nth highest, duplicates, pivots, median, growth, gaps and islands, rounding words | 107–113 |
| 19 | [SQL dialects in 2026](lessons/19-sql-dialects-2026.md) | SQLite, MySQL, PostgreSQL, MSSQL and Oracle side by side, silent traps, what's new | — |

## Which database is this?

The sandbox uses **SQLite** (version 3.49). Everything in these lessons also works in MySQL, PostgreSQL, Microsoft SQL Server (MSSQL) and Oracle, apart from the differences each lesson points out. [Lesson 19](lessons/19-sql-dialects-2026.md), [Lesson 16](lessons/16-mssql-transactions.md) and the [cheat sheet](cheatsheet.md) collect them all.

SQLite is more forgiving than MSSQL and Oracle in a few places (aliases in `HAVING`, plain columns after `GROUP BY`), so the lessons teach the stricter habits that work everywhere.

## Five habits that prevent most bugs

1. Check every table and column name against the real table (`customers`, not `customer`).
2. One-row condition → `WHERE`. Group condition → `HAVING`.
3. After `GROUP BY`, every other column goes inside `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`.
4. Read the word before each number: "over" is `>`, "at least" is `>=`.
5. Before any `UPDATE` or `DELETE`, run a `SELECT` with the same `WHERE`.
