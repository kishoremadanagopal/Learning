# Lesson 15: Views and indexes

**You'll learn:** saving a query as a view, and making queries faster with indexes.

## Key terms

- **View:** a saved query that you can use like a table. It stores the query, not the data, so it always shows current data.
- **Index:** a lookup structure that lets the database find rows quickly without reading the whole table, like the index at the back of a book.
- **Full table scan:** reading every row to find matches. Fine for 8 rows, slow for 8 million.
- **Query plan:** the database's step-by-step plan for running a query.

## Syntax

```sql
CREATE VIEW view_name AS
SELECT ...;

DROP VIEW view_name;

CREATE INDEX index_name ON table_name (column);
CREATE UNIQUE INDEX index_name ON table_name (column);

DROP INDEX index_name;
```

## Views

A CTE disappears when its query ends. A view is saved in the database, so everyone can reuse it:

```sql
CREATE VIEW customer_spending AS
SELECT c.name, COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;
```

Now it works like a table:

```sql
SELECT * FROM customer_spending WHERE total_spent > 400;
```

**Why views are useful:**
- **Reuse:** write a complicated JOIN once and query it simply.
- **Consistency:** everyone uses the same definition of "total spent."
- **Security:** give people access to a view that shows only some columns (say, no salaries) instead of the whole table.

**A view doesn't store data.** Add a new order and `customer_spending` shows the new total immediately, because the query runs each time you use the view.

## Indexes

Without an index, `WHERE customer_id = 3` makes the database read every row of `orders`. With one, it jumps straight to the matching rows:

```sql
CREATE INDEX idx_orders_customer
ON orders (customer_id);
```

**Good columns to index:**
- columns you often filter on in `WHERE`
- columns used to `JOIN` (like foreign keys: `orders.customer_id`)
- columns you often sort by

**Primary keys and `UNIQUE` columns are indexed automatically.**

**The trade-off:** indexes make reading faster but writing slower, because every `INSERT`, `UPDATE`, and `DELETE` has to update the index too. They also take up space. So index the columns you actually search on, not every column.

## Seeing whether an index is used

```sql
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 3;
```

In SQLite this shows `SEARCH orders USING INDEX idx_orders_customer` when the index is used, or `SCAN orders` for a full table scan. In MSSQL, use **Display Estimated Execution Plan** in SQL Server Management Studio.

## In MSSQL

- `CREATE VIEW` and `CREATE INDEX` work the same way.
- MSSQL has **clustered** indexes (the table is physically stored in that order; one per table, usually the primary key) and **non-clustered** indexes (a separate lookup structure; many per table). `CREATE INDEX` creates a non-clustered one.
- To change a view: `CREATE OR ALTER VIEW` (MSSQL 2016 SP1+) or `ALTER VIEW`.

## Common mistakes

- **`ORDER BY` inside a view.** MSSQL doesn't allow it without `TOP`, and it's not guaranteed anyway. Sort when you query the view.
- **Expecting a view to be faster.** A normal view runs its query every time, so it's about convenience, not speed.
- **Indexing everything.** Each index slows down writes.

## Exercises

1. Create a view `customer_spending` showing every customer's name and total spent (0 for no orders).
2. Create a view `big_orders` showing product, amount, and customer name for orders over 300.
3. Create an index `idx_orders_customer` on the `customer_id` column of `orders`.

**In the sandbox:** exercises 68–70. In free practice, try `EXPLAIN QUERY PLAN` before and after creating the index.

<details>
<summary>Answers</summary>

```sql
-- 1: see above

-- 2  → Laptop 1200 Maya, Monitor 400 Ana
CREATE VIEW big_orders AS
SELECT o.product, o.amount, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.amount > 300;

-- 3: see above
```
</details>

---
Previous: [Lesson 14](14-union.md) · Next: [Lesson 16: MSSQL and transactions](16-mssql-transactions.md)
