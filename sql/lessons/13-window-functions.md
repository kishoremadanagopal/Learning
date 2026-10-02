# Lesson 13: Window functions

**You'll learn:** `OVER`, `PARTITION BY`, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, running totals, and `LAG`/`LEAD`.

## Key terms

- **Window function:** a function that calculates across a set of related rows but, unlike `GROUP BY`, **keeps every row** in the result.
- **Window:** the set of rows a window function looks at for each row.
- **Partition:** a group of rows inside the window, set with `PARTITION BY` (like `GROUP BY`, without collapsing).
- **Running total:** a sum that grows row by row.

## Syntax

```sql
function_name(...) OVER (
  PARTITION BY column      -- optional: restart for each group
  ORDER BY column          -- optional: order within each group
)
```

| Function | Gives |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4… (no ties) |
| `RANK()` | 1, 2, 2, 4… (ties share, then skip) |
| `DENSE_RANK()` | 1, 2, 2, 3… (ties share, no skip) |
| `SUM/AVG/COUNT/MIN/MAX(x)` | the aggregate over the window |
| `LAG(x)` / `LEAD(x)` | the value from the previous / next row |

## GROUP BY vs window functions

`GROUP BY` squashes each department into one row. A window function keeps all 8 employees and adds the group value next to each one:

```sql
SELECT name, department, salary,
  AVG(salary) OVER (PARTITION BY department) AS dept_avg
FROM employees;
```

| name  | department  | salary | dept_avg |
|-------|-------------|--------|----------|
| Bob   | Engineering | 95000  | 96000    |
| Dev   | Engineering | 105000 | 96000    |
| Frank | Engineering | 88000  | 96000    |
| Emma  | Marketing   | 70000  | 66000    |
| …     | …           | …      | …        |

This makes "compare each row to its group" questions easy. `salary - dept_avg` is how far each person is from their department's average.

## Ranking within groups

```sql
SELECT name, department, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS salary_rank
FROM employees;
```

Dev is 1 in Engineering, Emma is 1 in Marketing, Hank is 1 in Sales. `PARTITION BY` restarts the numbering for each department.

## Top N per group

This is one of the most common real-world queries: "the top earner in each department." Number the rows, then keep number 1:

```sql
WITH ranked AS (
  SELECT name, department, salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
)
SELECT name, department, salary
FROM ranked
WHERE rn = 1;
```

**Window functions can't go in `WHERE`**, because they're calculated after the rows are filtered. That's why this pattern always uses a CTE (or subquery) first, then filters.

Use `ROW_NUMBER` for exactly one per group, or `RANK` to include ties.

## Running totals

With `ORDER BY` inside `OVER`, `SUM` adds up row by row:

```sql
SELECT order_date, amount,
  SUM(amount) OVER (ORDER BY order_date, order_id) AS running_total
FROM orders;
```

| order_date | amount | running_total |
|------------|--------|---------------|
| 2025-11-20 | 1200   | 1200          |
| 2025-12-02 | 25     | 1225          |
| 2026-01-10 | 300    | 1525          |
| …          | …      | …             |
| 2026-03-03 | 45     | 2200          |

Two orders share 2026-02-14, so `order_id` is added to the `ORDER BY` to give every row a unique position. Without it, rows with the same date get the same running total.

## LAG and LEAD: looking at neighbours

```sql
SELECT product, order_date,
  LAG(order_date) OVER (ORDER BY order_date, order_id) AS previous_date
FROM orders;
```

The first row's `previous_date` is `NULL`, because there's nothing before it. `LEAD` looks at the next row instead.

## Where they work

Window functions work in MSSQL, Oracle, PostgreSQL, MySQL 8+, and SQLite 3.25+, with the same syntax everywhere.

## Common mistakes

- **Filtering on a window function in `WHERE`.** Put it in a CTE first, then filter.
- **Forgetting `PARTITION BY`.** Without it, the whole table is one big window, so you get one ranking across all departments.
- **`ORDER BY` inside `OVER` vs at the end.** The one inside `OVER` controls the calculation; the one at the end of the query controls how results are displayed. They're independent.
- **Ties in running totals.** Add a unique column (like an id) to the window's `ORDER BY`.

## Exercises

1. Each employee's name, department, salary, and rank within their department (highest = 1), using `RANK`.
2. The top earner in each department, using `ROW_NUMBER`.
3. Each order's date, amount, and running total (by order_date then order_id).
4. Each employee's name, department, salary, and their department's average salary.
5. Each order's product, date, and the date of the order before it, using `LAG`.
6. Each employee's name, department, salary, and how far below their department's highest salary they are.

**In the sandbox:** exercises 59–64.

<details>
<summary>Answers</summary>

```sql
-- 1, 2, 3, 4, 5: see the examples above

-- 6  → Bob 10000, Dev 0, Frank 17000, Emma 0, Grace 8000, …
SELECT name, department, salary,
  MAX(salary) OVER (PARTITION BY department) - salary AS below_top
FROM employees;
```
</details>

---
Previous: [Lesson 12](12-ctes.md) · Next: [Lesson 14: UNION](14-union.md)
