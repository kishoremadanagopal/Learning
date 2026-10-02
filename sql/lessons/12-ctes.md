# Lesson 12: CTEs, breaking big queries into steps

**You'll learn:** `WITH`, chaining several CTEs, when a CTE beats a subquery, and recursive CTEs that generate rows (number lists, calendars, hierarchies).

## Key terms

- **CTE (Common Table Expression):** a named, temporary result set defined at the start of a query with `WITH`. It exists only while that one query runs.
- **Intermediate result:** a step's output that a later step builds on.
- **Recursive CTE:** a CTE that refers to itself, adding rows step by step until a condition stops it.

## Syntax

```sql
WITH step_name AS (
  SELECT ...
)
SELECT ...
FROM step_name;
```

Several CTEs, separated by commas (only one `WITH`):

```sql
WITH first_step AS (
  SELECT ...
),
second_step AS (
  SELECT ... FROM first_step
)
SELECT ... FROM second_step;
```

## Why CTEs

Some questions take several steps: "total spent per customer, then only the big spenders." You could nest subqueries, but they read inside-out. A CTE lets you write the steps top to bottom, each with a name.

```sql
WITH customer_totals AS (
  SELECT c.name, SUM(o.amount) AS total_spent
  FROM customers c
  JOIN orders o ON o.customer_id = c.id
  GROUP BY c.name
)
SELECT name, total_spent
FROM customer_totals
WHERE total_spent > 400;
```

| name | total_spent |
|------|-------------|
| Maya | 1225        |
| Ana  | 480         |

Notice the last step filters with `WHERE`, not `HAVING`. Inside the CTE the totals were group results; outside, they're just a normal column of a normal (temporary) table.

## CTEs fix the "repeat the CASE" problem

In Lesson 7, counting customers per age group meant writing the whole `CASE` twice (in `SELECT` and `GROUP BY`) so it would work in MSSQL. With a CTE you write it once:

```sql
WITH labeled AS (
  SELECT CASE
    WHEN age < 30 THEN 'Young'
    WHEN age < 50 THEN 'Middle'
    ELSE 'Senior'
  END AS age_group
  FROM customers
)
SELECT age_group, COUNT(*) AS num_customers
FROM labeled
GROUP BY age_group;
```

`GROUP BY age_group` works here in every database, because `age_group` is a real column of `labeled`, not an alias from the same `SELECT`.

## Chaining CTEs

```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
),
best AS (
  SELECT MAX(total) AS top_total FROM monthly
)
SELECT m.month, m.total
FROM monthly m
JOIN best b ON m.total = b.top_total;
```

Each CTE can use the ones above it.

## How to build one

1. Write the first step as a normal query and run it. Check the result.
2. Wrap it: `WITH step AS ( ...your query... )`.
3. Write the next step underneath, selecting `FROM step`.
4. Run the whole thing.

## CTE or subquery?

They can often do the same job. Use a CTE when:
- the query has more than one step
- you'd otherwise repeat the same subquery twice
- someone else (or future you) needs to read it

## Recursive CTEs: generating rows

A **recursive** CTE refers to itself. It starts with an **anchor** row, then a second query keeps adding rows based on the previous ones, until its `WHERE` stops it:

```sql
WITH RECURSIVE nums(n) AS (
  SELECT 1                              -- anchor: the first row
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 10   -- recursive step: the next row, until 10
)
SELECT n FROM nums;                     -- 1, 2, 3, ..., 10
```

How it runs: start with `1`; apply the step to get `2`; apply it to `2` to get `3`; … at `10`, `n < 10` is false, so no new row appears and it stops. **Always include the stopping condition**, or it runs forever (most databases cap it and raise an error).

### A calendar that fills the gaps

`GROUP BY month` only shows months that have orders. To show every month, including empty ones, generate the months first and `LEFT JOIN` the data onto them:

```sql
WITH RECURSIVE months(m) AS (
  SELECT '2025-10-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM months WHERE m < '2026-03-01'
)
SELECT strftime('%Y-%m', m) AS month, COALESCE(SUM(o.amount), 0) AS total
FROM months
LEFT JOIN orders o ON strftime('%Y-%m', o.order_date) = strftime('%Y-%m', m)
GROUP BY m
ORDER BY m;                             -- 2025-10 now appears, with 0
```

### Hierarchies

The other classic use is walking a tree, such as an org chart where each employee has a `manager_id`: the anchor selects the boss (`WHERE manager_id IS NULL`), and the recursive step joins each level's employees to the previous level (`JOIN chain c ON e.manager_id = c.id`), adding `level + 1` as it goes.

### In other databases

`WITH RECURSIVE` works in SQLite, MySQL 8+ and PostgreSQL. MSSQL and Oracle write just `WITH` (no `RECURSIVE`), and MSSQL stops after 100 levels unless you add `OPTION (MAXRECURSION 1000)`. PostgreSQL also has `generate_series(1, 10)`, which makes number and date lists without recursion.

## In MSSQL

CTEs work the same way. One catch: if the statement before `WITH` doesn't end with a semicolon, MSSQL gets confused. That's why you often see `;WITH` in MSSQL code. Ending every statement with `;` avoids it.

## Common mistakes

- **A comma after the last CTE.** `WITH a AS (...), b AS (...), SELECT ...` → no comma before the final `SELECT`.
- **Writing `WITH` twice.** Only the first CTE starts with `WITH`; the rest are separated by commas.
- **Using the CTE in a later, separate query.** A CTE disappears when its query ends. (For something reusable, see views in Lesson 15.)

## Exercises

1. Using a CTE named `customer_totals`, show the customers who spent more than 400.
2. Using a CTE, show the departments whose average salary is above the company-wide average.
3. Using a CTE that labels each customer Young/Middle/Senior, count the customers in each group.
4. Using a CTE of monthly totals, show the single month with the highest total.

**In the sandbox:** exercises 55–58.

### More practice

5. The numbers 1 to 10, one per row, in a column called `n`, using a recursive CTE.
6. Every month from 2025-10 to 2026-03 with its total order amount, showing 0 for months with no orders, in month order.

**In the sandbox:** exercises 101–102.

<details>
<summary>Answers</summary>

```sql
-- 1  → Maya 1225, Ana 480  (see above)

-- 2  → Engineering  (company average 75875)
WITH dept_avg AS (
  SELECT department, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department
)
SELECT department
FROM dept_avg
WHERE avg_salary > (SELECT AVG(salary) FROM employees);

-- 3  → Middle 2, Senior 1, Young 2  (see above)

-- 4  → 2025-11, 1200
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, total
FROM monthly
ORDER BY total DESC
LIMIT 1;

-- 5  → 1 to 10
WITH RECURSIVE nums(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums;

-- 6  → 2025-10 0, 2025-11 1200, 2025-12 25, 2026-01 450, 2026-02 480, 2026-03 45
WITH RECURSIVE months(m) AS (
  SELECT '2025-10-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM months WHERE m < '2026-03-01'
)
SELECT strftime('%Y-%m', m) AS month, COALESCE(SUM(o.amount), 0) AS total
FROM months
LEFT JOIN orders o ON strftime('%Y-%m', o.order_date) = strftime('%Y-%m', m)
GROUP BY m
ORDER BY m;
```
</details>

---
Previous: [Lesson 11](11-building-tables.md) · Next: [Lesson 13: Window functions](13-window-functions.md)
