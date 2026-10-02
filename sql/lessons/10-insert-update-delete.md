# Lesson 10: Changing data with INSERT, UPDATE and DELETE

**You'll learn:** adding, changing, and removing rows, and the safety habits that go with them.

## Key terms

- **INSERT:** adds new rows.
- **UPDATE:** changes values in existing rows.
- **DELETE:** removes rows.
- **SET:** the part of `UPDATE` that says what to change.
- **Rows affected:** how many rows a change touched. Always check it.

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
```
</details>

---
Previous: [Lesson 9](09-dates.md) · Next: [Lesson 11: Building tables](11-building-tables.md)
