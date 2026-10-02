# Lesson 10: Changing data with INSERT, UPDATE and DELETE

**You'll learn:** adding, changing, and removing rows, the safety habits that go with them, copying rows with `INSERT ... SELECT`, "insert or update" (upsert), `RETURNING`, and `DELETE` vs `TRUNCATE` vs `DROP`.

## Key terms

- **INSERT:** adds new rows.
- **UPDATE:** changes values in existing rows.
- **DELETE:** removes rows.
- **SET:** the part of `UPDATE` that says what to change.
- **Rows affected:** how many rows a change touched. Always check it.
- **Upsert:** insert a row, or update it if it already exists.
- **TRUNCATE:** empties a whole table in one fast step.

## Syntax

```sql
INSERT INTO table (col1, col2) VALUES (value1, value2);
UPDATE table SET col1 = value1, col2 = value2 WHERE condition;
DELETE FROM table WHERE condition;
```

## The three shapes

| Statement | Shape |
|---|---|
| `INSERT` | `INSERT INTO table (columns) VALUES (values);` |
| `UPDATE` | `UPDATE table SET column = value WHERE ...;` |
| `DELETE` | `DELETE FROM table WHERE ...;` |

Each has its own keyword before the table name: `INSERT INTO`, `UPDATE`, `DELETE FROM`. Only `DELETE` uses `FROM`. `UPDATE` never does.

## INSERT

```sql
INSERT INTO customers (id, name, city, age)
VALUES (6, 'Zoe', 'Oakland', 23);
```

Several rows at once:

```sql
INSERT INTO customers (id, name, city, age)
VALUES (6, 'Zoe', 'Oakland', 23),
       (7, 'Raj', 'Fremont', 38);
```

**Always list the columns.** It's clearer and keeps working if a column is added to the table later.

## UPDATE

```sql
UPDATE customers
SET city = 'Fremont'
WHERE name = 'Leo';
```

- The **column name** goes on the left of `SET`: `SET name = 'Notebook'`, not `SET Motebook = 'Notebook'`.
- To change a value relative to itself, name the column on both sides:

```sql
UPDATE employees
SET salary = salary + 5000
WHERE department = 'Marketing';
```

⚠️ `SET salary = + 5000` (or `= '5000'`) **replaces** the salary with 5000. It runs with no error. MSSQL has a shortcut `SET salary += 5000`; SQLite doesn't.

## DELETE

```sql
DELETE FROM orders
WHERE order_id = 107;
```

Double-check **which table** you're deleting from: `order_id` lives in `orders`, not `employees`.

## ⚠️ The most important rule

**`UPDATE` and `DELETE` without `WHERE` affect every row in the table.**

```sql
UPDATE customers SET city = 'Fremont';   -- everyone now lives in Fremont
DELETE FROM orders;                      -- every order is gone
```

There's no "are you sure?" and no undo. The professional habit:

1. Write a `SELECT` with the **same `WHERE`**: `SELECT * FROM orders WHERE amount < 50;`
2. Check it shows **exactly** the rows you mean.
3. Then swap `SELECT *` for `DELETE` (or `UPDATE ... SET ...`), keeping the `WHERE` identical.

To check an `UPDATE`'s new values first:

```sql
SELECT name, salary, salary + 5000 AS new_salary
FROM employees
WHERE department = 'Marketing';
```

Target rows by their **id** when you can (`WHERE order_id = 107`), since names can repeat.

## INSERT ... SELECT: copy rows from a query

Instead of `VALUES`, an `INSERT` can take the rows a `SELECT` returns. It's how you fill summary tables, archive old rows or copy data between tables:

```sql
CREATE TABLE fremont_customers (id INTEGER PRIMARY KEY, name TEXT);

INSERT INTO fremont_customers (id, name)
SELECT id, name FROM customers WHERE city = 'Fremont';      -- Maya, Priya
```

The `SELECT` must return the same number of columns, in the same order, as the column list.

## Upsert: insert, or update if it's already there

Inserting a row whose primary key already exists fails with a UNIQUE error. An **upsert** says what to do instead:

```sql
INSERT INTO customers (id, name, city, age)
VALUES (2, 'Leo', 'Berkeley', 28)
ON CONFLICT (id) DO UPDATE
SET city = excluded.city, age = excluded.age;      -- Leo exists, so he's updated
```

`excluded` means "the row you tried to insert". `ON CONFLICT (id) DO NOTHING` skips the row instead. Every database has a version:

| Database | Upsert |
|---|---|
| SQLite, PostgreSQL | `INSERT ... ON CONFLICT (id) DO UPDATE SET col = excluded.col` |
| MySQL | `INSERT ... ON DUPLICATE KEY UPDATE col = VALUES(col)` (8.0.20+: `AS new ... col = new.col`) |
| MSSQL, Oracle (also PostgreSQL 15+) | `MERGE INTO target USING source ON (...) WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...` |

## RETURNING: see what you changed

`RETURNING` makes an `INSERT`, `UPDATE` or `DELETE` hand back the rows it touched, so you don't need a second `SELECT`:

```sql
UPDATE employees SET salary = salary + 5000
WHERE department = 'Marketing'
RETURNING name, salary;                 -- Emma 75000, Grace 67000
```

It works in SQLite, PostgreSQL and MariaDB; Oracle uses `RETURNING ... INTO`, and MSSQL uses `OUTPUT inserted.col` (or `deleted.col`). MySQL doesn't have it.

## Changing rows based on another table

Use a subquery in the `WHERE` (this works everywhere):

```sql
-- give a raise to employees whose department's average is under 65000
UPDATE employees
SET salary = salary + 1000
WHERE department IN (
  SELECT department FROM employees GROUP BY department HAVING AVG(salary) < 65000
);
```

Most databases also allow a join in the update itself, but the spelling differs: `UPDATE ... FROM other WHERE ...` (SQLite 3.33+, PostgreSQL, MSSQL, Oracle 26ai), `UPDATE t JOIN other ON ... SET ...` (MySQL).

## DELETE vs TRUNCATE vs DROP

| Statement | Removes | Can use `WHERE` | Notes |
|---|---|---|---|
| `DELETE FROM t WHERE ...` | the matching rows | yes | slowest; can be rolled back |
| `TRUNCATE TABLE t` | every row, keeps the table | no | fast; resets auto-numbering; not in SQLite (use `DELETE FROM t`) |
| `DROP TABLE t` | the table itself, structure and all | no | Lesson 11 |

## In MSSQL

- MSSQL reports **"(N rows affected)"** after each change. Always glance at that number.
- MSSQL and Oracle accept `DELETE orders WHERE ...` without `FROM`. `DELETE FROM` works everywhere, so keep that habit.
- MSSQL supports transactions as an undo button: `BEGIN TRANSACTION`, check the result, then `ROLLBACK` (undo) or `COMMIT` (keep).

## Exercises

1. Add a new customer: id 6, name Zoe, city Oakland, age 23.
2. Add an order for Sam (customer id 4): order_id 108, product Headphones, amount 90, date 2026-03-15.
3. Leo has moved. Change his city to Fremont.
4. Give everyone in Marketing a raise of 5000.
5. Delete the Lamp order (order_id 107).
6. Delete every order with an amount under 50.

**In the sandbox:** exercises 44–49. These are checked on a fresh copy of the data, so you can check as often as you like. In free practice your changes are real; press **Reset data** to undo them.

### More practice

7. Upsert: add customer id 2 as Leo, Berkeley, 28, or update his city and age if id 2 already exists. Use `INSERT ... ON CONFLICT`.
8. Create a table `fremont_customers (id INTEGER PRIMARY KEY, name TEXT)` and fill it with the Fremont customers using `INSERT INTO ... SELECT`.

**In the sandbox:** exercises 99–100.

<details>
<summary>Answers</summary>

```sql
-- 1
INSERT INTO customers (id, name, city, age)
VALUES (6, 'Zoe', 'Oakland', 23);

-- 2
INSERT INTO orders (order_id, customer_id, product, amount, order_date)
VALUES (108, 4, 'Headphones', 90, '2026-03-15');

-- 3
UPDATE customers SET city = 'Fremont' WHERE name = 'Leo';

-- 4  → Emma 75000, Grace 67000
UPDATE employees SET salary = salary + 5000 WHERE department = 'Marketing';

-- 5
DELETE FROM orders WHERE order_id = 107;

-- 6  → removes Mouse (25) and Lamp (45)
DELETE FROM orders WHERE amount < 50;

-- 7  → Leo now lives in Berkeley and is 28; no new row
INSERT INTO customers (id, name, city, age)
VALUES (2, 'Leo', 'Berkeley', 28)
ON CONFLICT (id) DO UPDATE
SET city = excluded.city, age = excluded.age;

-- 8  → Maya, Priya
CREATE TABLE fremont_customers (id INTEGER PRIMARY KEY, name TEXT);

INSERT INTO fremont_customers (id, name)
SELECT id, name FROM customers WHERE city = 'Fremont';
```
</details>

---
Previous: [Lesson 9](09-dates.md) · Next: [Lesson 11: Building tables](11-building-tables.md)
