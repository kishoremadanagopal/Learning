# Lesson 11: Building tables

**You'll learn:** `CREATE TABLE`, data types, constraints (primary key, foreign key, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`), `ALTER TABLE`, and `DROP TABLE`.

## Key terms

- **Schema:** the structure of the database: tables, columns, types, rules.
- **Data type:** the kind of value a column holds.
- **Constraint:** a rule the database enforces (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, `REFERENCES`).
- **Foreign key:** a column whose values must exist in another table's key column.
- **DDL (Data Definition Language):** the statements that define structure: `CREATE`, `ALTER`, `DROP`.

## Syntax

```sql
CREATE TABLE table_name (
  column1 TYPE PRIMARY KEY,
  column2 TYPE NOT NULL,
  column3 TYPE UNIQUE,
  column4 TYPE DEFAULT value,
  column5 TYPE CHECK (condition),
  column6 TYPE REFERENCES other_table(column)
);
ALTER TABLE table_name ADD COLUMN column TYPE;
DROP TABLE table_name;
```

## CREATE TABLE

```sql
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  price      REAL
);
```

Each line is **column name, data type, then any rules**, separated by commas, with no comma after the last line.

## Data types

| Kind | SQLite | MSSQL | Example |
|---|---|---|---|
| whole number | `INTEGER` | `INT` | 34 |
| decimal number | `REAL` | `DECIMAL(10,2)` | 4.25 |
| text | `TEXT` | `VARCHAR(50)` / `NVARCHAR(50)` | 'Maya' |
| date | `TEXT` ('YYYY-MM-DD') | `DATE` | '2026-01-10' |
| true/false | `INTEGER` (0/1) | `BIT` | 1 |

- `VARCHAR(50)` = text up to 50 characters. `DECIMAL(10,2)` = up to 10 digits, 2 after the point. **Use `DECIMAL` for money**, since it stores exact values.
- SQLite accepts MSSQL-style types too, so you can practice them in the sandbox.

## Constraints: rules the database enforces

| Rule | Means |
|---|---|
| `PRIMARY KEY` | each row's unique id |
| `NOT NULL` | a value is required |
| `UNIQUE` | no two rows can share a value |
| `DEFAULT x` | use x when no value is given |
| `CHECK (...)` | the value must pass a test |
| `REFERENCES table(col)` | the value must exist in another table (**foreign key**) |

```sql
CREATE TABLE reviews (
  review_id   INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  rating      INTEGER CHECK (rating BETWEEN 1 AND 5),
  review_date TEXT DEFAULT '2026-01-01'
);
```

Now the database refuses bad data by itself: a rating of 7 fails the `CHECK`, and a `customer_id` of 99 fails the foreign key. Bad data gets stopped at the door instead of being caught by hand later.

**Primary key vs foreign key** is the idea behind every JOIN: `customers.id` identifies each customer; `orders.customer_id` points to one.

## Changing and removing tables

```sql
ALTER TABLE customers ADD COLUMN email TEXT;   -- existing rows get NULL
DROP TABLE reviews;                            -- structure and data, gone
```

⚠️ `DROP TABLE` is even more final than a `DELETE` without `WHERE`.

## In MSSQL

| SQLite | MSSQL |
|---|---|
| `INTEGER PRIMARY KEY` (auto-numbers if you skip the id) | `INT IDENTITY(1,1) PRIMARY KEY` |
| `ALTER TABLE t ADD COLUMN email TEXT` | `ALTER TABLE t ADD email VARCHAR(100)` |
| foreign keys need `PRAGMA foreign_keys = ON` (the sandbox has it on) | always enforced |

## Data types and auto-numbering in every database

| Kind | SQLite | MySQL | PostgreSQL | MSSQL | Oracle |
|---|---|---|---|---|---|
| whole number | `INTEGER` | `INT`, `BIGINT` | `INTEGER`, `BIGINT` | `INT`, `BIGINT` | `NUMBER(10)` |
| exact decimal (money) | `REAL` (approximate!) | `DECIMAL(10,2)` | `NUMERIC(10,2)` | `DECIMAL(10,2)` | `NUMBER(10,2)` |
| text | `TEXT` | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)`, `NVARCHAR(n)` | `VARCHAR2(n)` |
| date / date and time | `TEXT` | `DATE`, `DATETIME` | `DATE`, `TIMESTAMP` | `DATE`, `DATETIME2` | `DATE` (includes time), `TIMESTAMP` |
| true/false | `INTEGER` 0/1 | `BOOLEAN` (stored as 0/1) | `BOOLEAN` | `BIT` | `BOOLEAN` (26ai), `NUMBER(1)` before |
| auto-numbered id | `INTEGER PRIMARY KEY` | `INT AUTO_INCREMENT PRIMARY KEY` | `INT GENERATED ALWAYS AS IDENTITY` (older: `SERIAL`) | `INT IDENTITY(1,1)` | `NUMBER GENERATED ALWAYS AS IDENTITY` |

- `CREATE TABLE IF NOT EXISTS` and `DROP TABLE IF EXISTS` avoid errors when you re-run a script. They work in SQLite, MySQL and PostgreSQL, in MSSQL 2016+ (`DROP ... IF EXISTS` only) and in Oracle from 23ai.
- SQLite normally lets you store text in an `INTEGER` column. Add `STRICT` after the closing bracket (`CREATE TABLE t (...) STRICT;`, SQLite 3.37+) to make it reject the wrong type, as other databases do.
- `GENERATED ALWAYS AS IDENTITY` is the SQL-standard way to auto-number, and the one to learn for PostgreSQL and Oracle today.

## Exercises

1. Create a table `products`: `product_id` (integer, primary key), `name` (text, required), `price` (decimal number).
2. Create `products` again, then add two products: 1 Pen 1.50, and 2 Notebook 4.25.
3. Add a column `email` (text) to `customers`.
4. Create `reviews`: `review_id` (primary key), `customer_id` (linked to `customers.id`), and `rating` (integer between 1 and 5).
5. Create `departments`: `dept_id` (primary key) and `dept_name` (text, required, no duplicates). Then add 1 Sales, 2 Engineering, 3 Marketing.

**In the sandbox:** exercises 50–54. After building `reviews` in free practice, try inserting a rating of 7 or a customer_id of 99 to see the constraints at work.

<details>
<summary>Answers</summary>

```sql
-- 1
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price REAL
);

-- 2
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  price REAL
);
INSERT INTO products (product_id, name, price)
VALUES (1, 'Pen', 1.50),
       (2, 'Notebook', 4.25);

-- 3
ALTER TABLE customers ADD COLUMN email TEXT;

-- 4
CREATE TABLE reviews (
  review_id INTEGER PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  rating INTEGER CHECK (rating BETWEEN 1 AND 5)
);

-- 5
CREATE TABLE departments (
  dept_id INTEGER PRIMARY KEY,
  dept_name TEXT NOT NULL UNIQUE
);
INSERT INTO departments (dept_id, dept_name)
VALUES (1, 'Sales'), (2, 'Engineering'), (3, 'Marketing');
```
</details>

---
Previous: [Lesson 10](10-insert-update-delete.md) · Next: [Lesson 12: CTEs](12-ctes.md)
