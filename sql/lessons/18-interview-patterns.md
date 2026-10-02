# Lesson 18: Interview and HackerRank patterns

**You'll learn:** the query patterns that come up again and again on HackerRank, LeetCode and in SQL interviews: the Nth highest value, duplicates, pivoting rows into columns, the median, growth from one period to the next, consecutive streaks ("gaps and islands"), "every" questions, and how to read the rounding words in a question.

## Key terms

- **Nth highest:** the value in position N when sorted from largest, counting ties once.
- **Pivot:** turning the values of one column into separate columns.
- **Conditional aggregation:** an aggregate over a `CASE`, like `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` or `MAX(CASE WHEN ... THEN name END)`.
- **Median:** the middle value when sorted (the average of the middle two for an even count).
- **Gaps and islands:** finding runs of consecutive values (islands) and the breaks between them (gaps).
- **Relational division:** "find the X that have **all** of Y", such as customers who bought every product.

## How to approach a puzzle question

1. **Read the sample output first.** It tells you the columns, their order, and how numbers are rounded.
2. **Write the inner step on its own and run it.** Build the query in steps (CTEs, Lesson 12).
3. **Check the edge cases:** ties, NULLs, an empty result, and integer division.
4. **Pick the right dialect.** HackerRank offers MySQL, Oracle, MSSQL and DB2; LeetCode offers MySQL, MSSQL, Oracle and PostgreSQL. Lesson 19 lists the differences. MySQL is the safest choice for most practice questions.

## The words that decide the function

Puzzle sites are strict about formatting, so the wording matters:

| The question says | Use | Example |
|---|---|---|
| "rounded to 2 decimal places" | `ROUND(x, 2)` | 62333.333 → 62333.33 |
| "rounded down", "floor", "greatest integer ≤" | `FLOOR(x)` | 4.9 → 4 |
| "rounded up", "ceiling", "smallest integer ≥" | `CEIL(x)` / `CEILING(x)` | 4.1 → 5 |
| "truncate to 4 decimal places" | `TRUNCATE(x, 4)` MySQL · `TRUNC(x, 4)` Oracle | 3.14159 → 3.1415 |
| "nearest integer" | `ROUND(x)` | 4.5 → 5 |
| "absolute difference" | `ABS(a - b)` | |
| "as a percentage" | `100.0 * part / total` | not `100 * part / total` |

## 1. The Nth highest value

"The second-highest salary" is the most-asked SQL interview question. Three ways:

```sql
-- a) the biggest salary below the maximum
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);         -- 95000

-- b) skip one distinct value (wrapped so it returns NULL, not nothing, if there's no 2nd)
SELECT (SELECT DISTINCT salary FROM employees
        ORDER BY salary DESC LIMIT 1 OFFSET 1) AS second_highest;

-- c) DENSE_RANK: works for any N, and per group with PARTITION BY
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT DISTINCT salary FROM ranked WHERE rnk = 3;            -- 88000, the 3rd highest
```

Why `DENSE_RANK`? With salaries 100, 100, 90, the "second highest" is 90. `ROW_NUMBER` would say 100 and `RANK` would skip to 3; only `DENSE_RANK` gives 90 rank 2. `DISTINCT` in (b) does the same job for `OFFSET`.

## 2. Duplicates

Find the values that appear more than once:

```sql
SELECT order_date, COUNT(*) AS num_orders
FROM orders
GROUP BY order_date
HAVING COUNT(*) > 1;                     -- 2026-02-14, 2
```

See the **whole rows** involved, with a window count:

```sql
WITH counted AS (
  SELECT o.*, COUNT(*) OVER (PARTITION BY order_date) AS same_day
  FROM orders o
)
SELECT * FROM counted WHERE same_day > 1;      -- Monitor and Keyboard
```

Delete repeats but keep one copy of each (the lowest id):

```sql
DELETE FROM people
WHERE id NOT IN (
  SELECT MIN(id) FROM people GROUP BY email     -- one survivor per email
);
```

## 3. Pivot: rows into columns

**Counts as columns** use conditional aggregation:

```sql
SELECT department,
  SUM(CASE WHEN years >= 5 THEN 1 ELSE 0 END) AS veterans,
  SUM(CASE WHEN years <  5 THEN 1 ELSE 0 END) AS newer
FROM employees
GROUP BY department;            -- Engineering 2 1, Marketing 1 1, Sales 1 2
```

PostgreSQL, SQLite and Oracle 26ai also accept `COUNT(*) FILTER (WHERE years >= 5)`, the SQL-standard spelling.

**Names as columns** (HackerRank's *Occupations*): number the names within each group, then put one group in each column with `MAX(CASE ...)`, one row per number:

```sql
WITH numbered AS (
  SELECT name, department,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY name) AS rn
  FROM employees
)
SELECT
  MAX(CASE WHEN department = 'Engineering' THEN name END) AS Engineering,
  MAX(CASE WHEN department = 'Marketing'   THEN name END) AS Marketing,
  MAX(CASE WHEN department = 'Sales'       THEN name END) AS Sales
FROM numbered
GROUP BY rn
ORDER BY rn;
```

| Engineering | Marketing | Sales |
|---|---|---|
| Bob | Emma | Alice |
| Dev | Grace | Carla |
| Frank | NULL | Hank |

`MAX` is only there because `GROUP BY` needs an aggregate: each cell has at most one name, and `MAX` of one value is that value. MSSQL and Oracle also have a `PIVOT` keyword, but the `CASE` version works everywhere.

## 4. The median

Only some databases have `MEDIAN()` (Oracle, DuckDB, Snowflake) or `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` (PostgreSQL and Oracle; MSSQL only as a window function, with `OVER ()` added). MySQL and standard SQLite have neither. (This sandbox's SQLite happens to include a `median()` add-on, but most SQLite builds don't, so don't rely on it.) The portable way numbers the rows and averages the middle one or two:

```sql
WITH ordered AS (
  SELECT salary,
    ROW_NUMBER() OVER (ORDER BY salary) AS rn,
    COUNT(*) OVER () AS n
  FROM employees
)
SELECT AVG(salary) AS median_salary
FROM ordered
WHERE rn IN ((n + 1) / 2, (n + 2) / 2);      -- 71000: the average of 70000 and 72000
```

With 8 rows, `(n + 1) / 2` and `(n + 2) / 2` are 4 and 5 (integer division). With 7 rows, both are 4, the single middle row. This is one place where integer division is exactly what you want; in MySQL and Oracle, where `/` gives decimals, write `FLOOR((n + 1) / 2)` and `FLOOR((n + 2) / 2)`.

## 5. Growth from one period to the next

Totals per month in a CTE, then `LAG` for the previous month:

```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, total,
  total - LAG(total) OVER (ORDER BY month) AS change,
  ROUND(100.0 * (total - LAG(total) OVER (ORDER BY month))
        / LAG(total) OVER (ORDER BY month), 1) AS pct_change
FROM monthly
ORDER BY month;
```

| month | total | change | pct_change |
|---|---|---|---|
| 2025-11 | 1200 | NULL | NULL |
| 2025-12 | 25 | -1175 | -97.9 |
| 2026-01 | 450 | 425 | 1700.0 |
| 2026-02 | 480 | 30 | 6.7 |

## 6. Consecutive days: gaps and islands

"Users who logged in on 3 or more consecutive days" is a favourite hard question. The trick: within a run of consecutive dates, **the date minus its row number is the same** for every row. That constant labels each run (island):

```sql
WITH logins(user_id, day) AS (
  VALUES (1, '2026-03-01'), (1, '2026-03-02'), (1, '2026-03-03'), (1, '2026-03-05'),
         (2, '2026-03-01'), (2, '2026-03-03'), (2, '2026-03-04')
),
grp AS (
  SELECT user_id, day,
    julianday(day) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS island
  FROM logins
)
SELECT user_id, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS days
FROM grp
GROUP BY user_id, island
ORDER BY user_id, start_day;
```

| user_id | start_day | end_day | days |
|---|---|---|---|
| 1 | 2026-03-01 | 2026-03-03 | 3 |
| 1 | 2026-03-05 | 2026-03-05 | 1 |
| 2 | 2026-03-01 | 2026-03-01 | 1 |
| 2 | 2026-03-03 | 2026-03-04 | 2 |

Add `HAVING COUNT(*) >= 3` to keep only the long streaks. In other databases, replace `julianday(day) - ROW_NUMBER()` with a date minus that many days (`DATE_SUB(day, INTERVAL rn DAY)` in MySQL, `day - rn` in PostgreSQL and Oracle, `DATEADD(day, -rn, day)` in MSSQL). HackerRank's *SQL Project Planning* is this pattern.

## 7. "Every" and "all" questions

"Customers whose **every** order is under 500" means "their **largest** order is under 500":

```sql
SELECT c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING MAX(o.amount) < 500;              -- Ana, Leo, Priya
```

"Customers who bought **all** the products" (relational division) compares counts:

```sql
SELECT customer_id
FROM purchases
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products);
```

## 8. Top N per group and running totals

Both are in Lesson 13: `ROW_NUMBER()` in a CTE then `WHERE rn <= N`, and `SUM(...) OVER (ORDER BY ...)`. Use `DENSE_RANK` instead of `ROW_NUMBER` when ties should all be included.

## Common mistakes

- **Returning nothing instead of NULL.** "If there is no second-highest salary, return NULL" needs the value wrapped in an outer `SELECT (...)` or an aggregate like `MAX`; a bare `LIMIT ... OFFSET` returns zero rows.
- **Using `ROW_NUMBER` when ties matter.** Nth-highest questions almost always mean distinct values: `DENSE_RANK`.
- **Forgetting the order the site wants.** Many checkers compare rows in order, so add the `ORDER BY` the question describes.
- **Integer division in percentages and averages.** Multiply by `100.0` or `1.0` first.
- **Printing extra columns.** Return exactly the columns the question asks for, in that order.

## Exercises

1. The second-highest salary in the company, as one value.
2. The third-highest distinct salary, using `DENSE_RANK`.
3. Order dates that appear more than once, with the number of orders that day.
4. Pivot: employee names in three columns (Engineering, Marketing, Sales), each sorted alphabetically.
5. The median salary, without a `MEDIAN` function.
6. Each month, its total, and the change from the previous month.
7. Customers who have orders and whose every order is under 500.

**In the sandbox:** exercises 107–113.

<details>
<summary>Answers</summary>

```sql
-- 1  → 95000
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- 2  → 88000
WITH ranked AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT DISTINCT salary FROM ranked WHERE rnk = 3;

-- 3  → 2026-02-14, 2
SELECT order_date, COUNT(*) AS num_orders
FROM orders
GROUP BY order_date
HAVING COUNT(*) > 1;

-- 4  (see section 3)
WITH numbered AS (
  SELECT name, department,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY name) AS rn
  FROM employees
)
SELECT
  MAX(CASE WHEN department = 'Engineering' THEN name END) AS Engineering,
  MAX(CASE WHEN department = 'Marketing'   THEN name END) AS Marketing,
  MAX(CASE WHEN department = 'Sales'       THEN name END) AS Sales
FROM numbered
GROUP BY rn
ORDER BY rn;

-- 5  → 71000
WITH ordered AS (
  SELECT salary,
    ROW_NUMBER() OVER (ORDER BY salary) AS rn,
    COUNT(*) OVER () AS n
  FROM employees
)
SELECT AVG(salary) AS median_salary
FROM ordered
WHERE rn IN ((n + 1) / 2, (n + 2) / 2);

-- 6  → 2025-11 1200 NULL, 2025-12 25 -1175, 2026-01 450 425, 2026-02 480 30, 2026-03 45 -435
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, total,
  total - LAG(total) OVER (ORDER BY month) AS change
FROM monthly
ORDER BY month;

-- 7  → Ana, Leo, Priya
SELECT c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING MAX(o.amount) < 500;
```
</details>

---
Previous: [Lesson 17](17-final-project.md) · Next: [Lesson 19: SQL dialects in 2026](19-sql-dialects-2026.md)
