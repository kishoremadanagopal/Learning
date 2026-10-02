# Lesson 17: Final project

**You'll use:** everything, including JOINs, GROUP BY, HAVING, CASE, dates, CTEs, and window functions.

## The scenario

You've just joined a small online store as its data analyst. The manager has eight business questions for you. The data is in the three [practice tables](00-the-tables.md). For each question, write one query that answers it.

These are written the way real requests arrive: in business language, not SQL language. Part of the job is turning them into clauses.

## How to approach each question

1. **Translate the question into clauses.** Jot down which phrase maps to which part:

   | Phrase | Clause |
   |---|---|
   | "each ___" / "per ___" | `GROUP BY` |
   | "only ___" about one row | `WHERE` |
   | "only ___" about a group (total, count, average) | `HAVING` |
   | "highest first", "sorted by" | `ORDER BY` |
   | "the top one", "the best" | `ORDER BY ... LIMIT 1` or `ROW_NUMBER` |
   | "each ___'s best ___" | `ROW_NUMBER() OVER (PARTITION BY ...)` |
   | "compared to their group" | window function with `PARTITION BY` |
   | "including those with none" | `LEFT JOIN` + `COALESCE` |
   | several steps | a CTE per step |

2. **Build it in steps.** Get the JOIN right and run it. Add grouping and run it. Then add filters and sorting.
3. **Check the result by hand** for one row, using the tables.
4. **Check edge cases:** customers with no orders (Sam), ties (two orders on 2026-02-14), and values exactly on a boundary.

## The questions

1. **Revenue by city.** Each customer city and its total order amount, highest first (only cities with orders).
2. **Best month.** The month in 2026 with the highest total order amount.
3. **Customer tiers.** Every customer's name, number of orders, total spent, and tier: 'No orders' if none, 'Gold' for at least 1000, 'Silver' for at least 300, otherwise 'Bronze'.
4. **Favourite purchase.** Each customer's most expensive order: name, product, and amount.
5. **Customer lifetime.** For each customer with orders, the number of days between their first and last order.
6. **Above-average earners.** Employees who earn more than their department's average: name, department, salary, and how much above the average.
7. **Revenue share.** Each customer's share of total revenue as a percentage, rounded to 1 decimal place.
8. **Repeat customers.** Names of customers who placed orders in more than one different month.

**In the sandbox:** exercises 72–79.

## Hints

<details>
<summary>Hint for question 3</summary>

Sam has no orders, so you need a `LEFT JOIN`. But careful: with a `LEFT JOIN`, `COUNT(*)` counts Sam's row as 1. Use `COUNT(o.order_id)`, which skips the `NULL`. Put the 'No orders' check first in the `CASE`.
</details>

<details>
<summary>Hint for question 4</summary>

"Each customer's best ___" is the top-N-per-group pattern from Lesson 13: `ROW_NUMBER() OVER (PARTITION BY customer ORDER BY amount DESC)` in a CTE, then `WHERE rn = 1`.
</details>

<details>
<summary>Hint for question 7</summary>

The total revenue is a subquery: `(SELECT SUM(amount) FROM orders)`. Multiply by `100.0`, not `100`, so the division keeps its decimals.
</details>

## Answers

<details>
<summary>Answers (try first!)</summary>

```sql
-- 1  → Fremont 1420, Oakland 780
SELECT c.city, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.city
ORDER BY total DESC;

-- 2  → 2026-02, 480
SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
FROM orders
WHERE strftime('%Y', order_date) = '2026'
GROUP BY strftime('%Y-%m', order_date)
ORDER BY total DESC
LIMIT 1;

-- 3  → Maya Gold, Ana Silver, Leo Silver, Priya Bronze, Sam No orders
SELECT c.name,
  COUNT(o.order_id) AS num_orders,
  COALESCE(SUM(o.amount), 0) AS total_spent,
  CASE
    WHEN COUNT(o.order_id) = 0 THEN 'No orders'
    WHEN SUM(o.amount) >= 1000 THEN 'Gold'
    WHEN SUM(o.amount) >= 300 THEN 'Silver'
    ELSE 'Bronze'
  END AS tier
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 4  → Maya Laptop 1200, Leo Desk 300, Priya Chair 150, Ana Monitor 400
WITH ranked AS (
  SELECT c.name, o.product, o.amount,
    ROW_NUMBER() OVER (PARTITION BY c.id ORDER BY o.amount DESC) AS rn
  FROM customers c
  JOIN orders o ON o.customer_id = c.id
)
SELECT name, product, amount
FROM ranked
WHERE rn = 1;

-- 5  → Maya 12, Priya 37, Leo 0, Ana 0
SELECT c.name,
  julianday(MAX(o.order_date)) - julianday(MIN(o.order_date)) AS days_between
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 6  → Dev +9000, Emma +4000, Hank +9666.67
WITH with_avg AS (
  SELECT name, department, salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg
  FROM employees
)
SELECT name, department, salary, salary - dept_avg AS above_avg
FROM with_avg
WHERE salary > dept_avg;

-- 7  → Maya 55.7, Ana 21.8, Leo 13.6, Priya 8.9
SELECT c.name,
  ROUND(100.0 * SUM(o.amount) / (SELECT SUM(amount) FROM orders), 1) AS pct_of_revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- 8  → Maya, Priya
SELECT c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING COUNT(DISTINCT strftime('%Y-%m', o.order_date)) > 1;
```
</details>

## What's next

You've finished the course. Some ways to keep going:

- **Practice on bigger data.** Sites like SQLZoo, LeetCode (Database problems), and HackerRank (SQL) have hundreds of graded exercises.
- **Install a real database.** SQL Server Express and SQL Server Management Studio (SSMS) are free, and the [Lesson 16 cheat sheet](16-mssql-transactions.md) covers the differences you'll hit.
- **Use your own data.** Import a spreadsheet you care about into a database and ask it questions.

---
Previous: [Lesson 16](16-mssql-transactions.md) · Back to the [course home](../README.md)
