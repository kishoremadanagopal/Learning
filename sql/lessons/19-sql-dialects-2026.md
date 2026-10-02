# Lesson 19: SQL dialects in 2026

**You'll learn:** which databases people use and where, how SQLite, MySQL, PostgreSQL, MSSQL and Oracle differ, the traps that change results without an error, and what's new in each as of late 2026.

## Key terms

- **Dialect:** one database's version of SQL. The core is shared; names, functions and small rules differ.
- **ANSI / ISO SQL:** the official SQL standard every dialect follows in part.
- **RDBMS:** relational database management system, such as PostgreSQL or MSSQL.
- **Data warehouse:** a database built for analysing large amounts of data, like Snowflake or BigQuery.
- **Collation:** the rules a database uses to compare and sort text, including whether capitals matter.
- **LTS (long-term support):** a release that gets fixes for several years, the one businesses usually run.

## The big picture

About 90% of what you've learned is the same everywhere: `SELECT`, `WHERE`, `JOIN`, `GROUP BY`, `HAVING`, `ORDER BY`, subqueries, CTEs, window functions, `CASE`, `COALESCE`, `UNION`. If you can write it in SQLite, you can write it anywhere after a few spelling changes. Learn the core once, then learn each database's differences.

| Database | Where you'll meet it | Current versions (October 2026) |
|---|---|---|
| **SQLite** | inside phones, browsers, apps and this sandbox; a whole database in one file | 3.53 (the sandbox runs 3.49) |
| **MySQL** (and its cousin **MariaDB**) | websites and web apps; the usual default on HackerRank and LeetCode | 8.4 LTS and 9.7 LTS (May 2026) |
| **PostgreSQL** | modern apps, startups, analytics; the most-used database in recent developer surveys | 18 (September 2025); 19 due October 2026 |
| **MSSQL** (Microsoft SQL Server, Azure SQL) | companies built on Microsoft tools | SQL Server 2025 |
| **Oracle** | banks, governments, large enterprises | Oracle AI Database 26ai |
| **Snowflake, BigQuery, Databricks SQL, Redshift, DuckDB** | cloud analytics and data engineering | updated continuously |

## Side by side

### Rows, text and NULLs

| Task | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| first n rows | `LIMIT n` | `LIMIT n` | `LIMIT n` | `SELECT TOP n` | `FETCH FIRST n ROWS ONLY` |
| skip rows | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `LIMIT n OFFSET m` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |
| join text | `a \|\| b` | `CONCAT(a, b)` | `a \|\| b` | `a + b`, `CONCAT` | `a \|\| b` |
| length | `LENGTH` | `CHAR_LENGTH` | `LENGTH` | `LEN` | `LENGTH` |
| replace NULL | `COALESCE`, `IFNULL` | `COALESCE`, `IFNULL` | `COALESCE` | `COALESCE`, `ISNULL` | `COALESCE`, `NVL` |
| quote a column name | `"order"` | `` `order` `` | `"order"` | `[order]` or `"order"` | `"ORDER"` |
| list per group | `GROUP_CONCAT`, `STRING_AGG` | `GROUP_CONCAT` | `STRING_AGG` | `STRING_AGG` | `LISTAGG` |
| select without a table | `SELECT 1 + 1` | `SELECT 1 + 1` | `SELECT 1 + 1` | `SELECT 1 + 1` | `FROM DUAL` (optional from 23ai) |

### Numbers

| Task | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| `7 / 2` | `3` | `3.5000` | `3` | `3` | `3.5` |
| round up | `CEIL` | `CEIL`, `CEILING` | `CEIL`, `CEILING` | `CEILING` | `CEIL` |
| truncate | `CAST(x AS INTEGER)` | `TRUNCATE(x, d)` | `TRUNC(x, d)` | `ROUND(x, d, 1)` | `TRUNC(x, d)` |
| remainder | `%` | `%`, `MOD` | `%`, `MOD` | `%` | `MOD` |
| `AVG` of whole numbers | decimal | decimal | decimal | **whole number** | decimal |
| divide by zero | NULL | NULL (with a warning) | error | error | error |

### Dates

See the full table in Lesson 9. The short version: `strftime` (SQLite), `DATE_FORMAT` / `DATE_ADD` / `DATEDIFF(end, start)` (MySQL), `EXTRACT` / `DATE_TRUNC` / `INTERVAL` (PostgreSQL), `DATEADD` / `DATEDIFF(unit, start, end)` / `FORMAT` (MSSQL), `TO_CHAR` / `TRUNC` / `ADD_MONTHS` (Oracle).

### Joins, sets and changes

| Feature | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| `FULL OUTER JOIN` | ✓ (3.39+) | **✗** (use `LEFT JOIN ... UNION ... RIGHT JOIN`) | ✓ | ✓ | ✓ |
| `INTERSECT` / `EXCEPT` | ✓ | ✓ (8.0.31+) | ✓ | ✓ | ✓ (`MINUS`; `EXCEPT` from 21c) |
| upsert | `ON CONFLICT` | `ON DUPLICATE KEY UPDATE` | `ON CONFLICT`, `MERGE` | `MERGE` | `MERGE` |
| `RETURNING` | ✓ | ✗ | ✓ | `OUTPUT` | `RETURNING INTO` |
| regex | `GLOB` only (or an add-on) | `REGEXP`, `REGEXP_LIKE` | `~`, `~*`, `regexp_replace` | `REGEXP_LIKE` and friends (2025+) | `REGEXP_LIKE` |
| case-insensitive `LIKE` | default | default | `ILIKE` | default | `UPPER()`/`LOWER()` |
| `QUALIFY` | ✗ | ✗ | ✗ | ✗ | ✓ (26ai) |

## The silent traps

These don't raise errors. The query runs and gives a **different answer** when you move it to another database:

1. **Integer division.** `100 * part / total` is 0 in SQLite, PostgreSQL and MSSQL when part < total. Multiply by `100.0`.
2. **`AVG` in MSSQL.** Averages whole-number columns as whole numbers. Use `AVG(col * 1.0)`.
3. **Capital letters.** `'abc' = 'ABC'` is true in MySQL and MSSQL (their usual collations ignore case) and false in PostgreSQL, Oracle and SQLite.
4. **NULL ordering.** NULLs sort first in SQLite, MySQL and MSSQL, and last in PostgreSQL and Oracle (Lesson 2).
5. **Empty text in Oracle.** Oracle treats `''` as NULL, so `WHERE name = ''` never matches there.
6. **`GROUP BY` leniency.** SQLite (and MySQL with `ONLY_FULL_GROUP_BY` switched off) allow columns that aren't grouped or aggregated, and quietly pick a value. PostgreSQL, MSSQL and Oracle refuse. Follow the GROUP BY rule from Lesson 3 and your queries work everywhere.
7. **`DATEDIFF` argument order.** `DATEDIFF(end, start)` in MySQL, `DATEDIFF(day, start, end)` in MSSQL.
8. **Booleans.** MySQL and SQLite store true/false as 1/0, so `SUM(salary > 70000)` counts rows there; PostgreSQL needs `SUM(CASE ...)` or `COUNT(*) FILTER (WHERE ...)`.

## What's new in 2025 and 2026

- **SQLite (3.44 to 3.53):** `CONCAT`, `CONCAT_WS` and `STRING_AGG`; `ORDER BY` inside aggregates (`GROUP_CONCAT(name, ', ' ORDER BY name)`); `unixepoch()`, `timediff()`; JSON with `->` and `->>`. The sandbox was upgraded to SQLite 3.49 for this course, so all of these work in it.
- **MySQL 9.7 LTS (May 2026):** the first long-term-support release since 8.4, bringing the 9.x line's features (such as the `VECTOR` type) to LTS, plus JSON duality views. MySQL 8.0 has reached end of life, so new projects use 8.4 or 9.7.
- **PostgreSQL 18:** `uuidv7()` for time-ordered ids, virtual generated columns, and `OLD`/`NEW` in `RETURNING`. Version 19 is due in October 2026.
- **SQL Server 2025:** native regular expressions (`REGEXP_LIKE`, `REGEXP_REPLACE`, `REGEXP_SUBSTR`, `REGEXP_COUNT`…), a `VECTOR` type for AI search, and a native JSON type.
- **Oracle AI Database 26ai:** a `BOOLEAN` type; `SELECT` without `FROM DUAL`; `GROUP BY` an alias or position, and `GROUP BY ALL`; `QUALIFY`; `FILTER` on aggregates; `DATEADD` and `DATEDIFF`; `CREATE ... IF NOT EXISTS`; `UPDATE`/`DELETE` with joins; and `VALUES` lists.
- **SQL meets AI:** PostgreSQL (with `pgvector`), MySQL, MSSQL and Oracle can all store **vector embeddings** and search by similarity. This is how many AI apps find "similar documents" (retrieval for chatbots). The SQL you know still does the filtering, joining and grouping around it.

## Switching to a new database: a checklist

1. How do I limit rows? (`LIMIT`, `TOP`, `FETCH FIRST`)
2. How do I join text and handle NULL text?
3. Does `/` keep decimals?
4. Are text comparisons case-sensitive?
5. What are the date functions called?
6. How do I quote a column name that's a reserved word?
7. Is there an upsert, and what's it called?

Look these up once and keep a note; everything else you already know.

## Exercises

These are reading exercises: answer them in words or in SQL for the database named. The answers follow.

1. Rewrite `SELECT name FROM customers ORDER BY age DESC LIMIT 3;` for MSSQL and for Oracle.
2. A query `SELECT 100 * 3 / 4;` returns 75 in every database, but `SELECT 3 / 4 * 100;` doesn't. What does it return in PostgreSQL and in MySQL, and why?
3. You move a report from MySQL to PostgreSQL and `WHERE city = 'fremont'` stops matching `'Fremont'`. Why, and what are two fixes?
4. Which of these doesn't exist in MySQL: `INTERSECT`, `FULL OUTER JOIN`, window functions, CTEs?

<details>
<summary>Answers</summary>

1. MSSQL: `SELECT TOP 3 name FROM customers ORDER BY age DESC;` · Oracle: `SELECT name FROM customers ORDER BY age DESC FETCH FIRST 3 ROWS ONLY;`
2. PostgreSQL gives `0`: `3 / 4` is integer division (0), then 0 × 100 = 0. MySQL gives `75.0000`, because its `/` always keeps decimals. Write `3 * 100.0 / 4` to be safe everywhere.
3. PostgreSQL compares text case-sensitively; MySQL's default collation doesn't. Fix with `WHERE LOWER(city) = 'fremont'` or `WHERE city ILIKE 'fremont'`.
4. `FULL OUTER JOIN`. MySQL has had `INTERSECT` since 8.0.31, and window functions and CTEs since 8.0.

</details>

---
Previous: [Lesson 18](18-interview-patterns.md) · Back to the [course home](../README.md)
