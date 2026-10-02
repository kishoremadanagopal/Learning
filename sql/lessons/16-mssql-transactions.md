# Lesson 16: MSSQL (T-SQL) differences and transactions

**You'll learn:** everything that changes when you move from SQLite to Microsoft SQL Server, and how transactions give you an undo button.

## Key terms

- **Dialect:** a database's own version of SQL. SQLite, MySQL, PostgreSQL, MSSQL, and Oracle share a core but differ in details.
- **T-SQL (Transact-SQL):** Microsoft SQL Server's dialect.
- **Transaction:** a group of changes that succeed or fail together.
- **COMMIT:** make a transaction's changes permanent.
- **ROLLBACK:** undo every change in the transaction.
- **ACID:** the guarantees a transaction gives: Atomic (all or nothing), Consistent, Isolated (others don't see half-done work), Durable (committed changes survive a crash).

## Syntax

```sql
BEGIN TRANSACTION;
  -- changes
COMMIT;        -- keep them
-- or
ROLLBACK;      -- undo them
```

## Part 1: SQLite → MSSQL cheat sheet

### Queries

| Task | SQLite | MSSQL |
|---|---|---|
| Top N rows | `... ORDER BY x LIMIT 5` | `SELECT TOP 5 ... ORDER BY x` |
| Skip rows (paging) | `LIMIT 10 OFFSET 20` | `ORDER BY x OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` |
| Alias in `GROUP BY` / `HAVING` | allowed | ❌ repeat the expression |
| Plain column after `GROUP BY` | runs (random value) | ❌ error |
| Text comparison | case-sensitive | case-insensitive (by default) |

### Text

| Task | SQLite | MSSQL |
|---|---|---|
| Join text | `a \|\| b` | `a + b` or `CONCAT(a, b)` |
| Length | `LENGTH(x)` | `LEN(x)` |
| Replace NULL | `COALESCE(x, 0)` / `IFNULL` | `COALESCE(x, 0)` / `ISNULL(x, 0)` |
| Part of text | `SUBSTR(x, 1, 3)` | `SUBSTRING(x, 1, 3)` |

### Numbers

| Task | SQLite | MSSQL |
|---|---|---|
| Average of whole numbers | `AVG(salary)` → 62333.33 | `AVG(salary)` → **62333** (use `AVG(salary * 1.0)`) |
| Integer division | `7 / 2` → 3 | `7 / 2` → 3 (both! use `7.0 / 2`) |
| Convert type | `CAST(x AS INTEGER)` | `CAST(x AS INT)` or `CONVERT(INT, x)` |

### Dates

| Task | SQLite | MSSQL |
|---|---|---|
| Today | `date('now')` | `GETDATE()` or `CAST(GETDATE() AS DATE)` |
| Year / month | `strftime('%Y', d)` (text) | `YEAR(d)`, `MONTH(d)` (numbers) |
| Year-month | `strftime('%Y-%m', d)` | `FORMAT(d, 'yyyy-MM')` |
| Days between | `julianday(b) - julianday(a)` | `DATEDIFF(day, a, b)` |
| Add days | `date(d, '+30 days')` | `DATEADD(day, 30, d)` |

### Changing data and tables

| Task | SQLite | MSSQL |
|---|---|---|
| Add to a value | `SET x = x + 5` | `SET x = x + 5` or `SET x += 5` |
| Auto-numbering id | `INTEGER PRIMARY KEY` | `INT IDENTITY(1,1) PRIMARY KEY` |
| Add a column | `ALTER TABLE t ADD COLUMN c TEXT` | `ALTER TABLE t ADD c VARCHAR(100)` |
| Text type | `TEXT` | `VARCHAR(n)` / `NVARCHAR(n)` (N = any language) |
| Money | `REAL` | `DECIMAL(10,2)` |
| Foreign keys | need `PRAGMA foreign_keys = ON` | always enforced |

### Habits that work in every database

1. Single quotes for text: `'Fremont'`.
2. Table aliases without `AS`: `FROM customers c`.
3. `COALESCE` instead of `ISNULL` / `IFNULL` / `NVL`.
4. Repeat aggregates in `HAVING` instead of using aliases.
5. Follow the GROUP BY rule strictly.
6. End every statement with `;`.

## Part 2: Transactions

Remember from Lesson 10: there's no undo after an `UPDATE` or `DELETE`. **Transactions are the undo button.**

```sql
BEGIN TRANSACTION;

DELETE FROM orders WHERE amount < 50;

SELECT * FROM orders;     -- check the result

ROLLBACK;                 -- not happy? undo everything since BEGIN
-- COMMIT;                -- happy? make it permanent
```

Until you `COMMIT`, the changes aren't final. `ROLLBACK` puts everything back exactly as it was at `BEGIN`.

### All or nothing

Transactions also keep related changes together. Moving money between two accounts takes two `UPDATE`s. If the first succeeds and the second fails, money disappears. In a transaction, either both happen or neither does:

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### A safe routine for risky changes (MSSQL)

```sql
BEGIN TRANSACTION;

UPDATE employees SET salary = salary + 5000 WHERE department = 'Marketing';
-- MSSQL shows "(2 rows affected)". Is 2 what you expected?

SELECT name, salary FROM employees WHERE department = 'Marketing';

-- then run ONE of these:
COMMIT;
-- ROLLBACK;
```

⚠️ Don't leave a transaction open. Until you `COMMIT` or `ROLLBACK`, other people may be blocked from using those rows.

## Common mistakes

- **Forgetting `COMMIT`.** In MSSQL the changes seem done in your window, but other users don't see them, and the rows stay locked.
- **Expecting `ROLLBACK` to undo a committed change.** Once committed, it's permanent.
- **Using `LIMIT` in MSSQL.** It's `TOP`.
- **Getting whole numbers from `AVG` in MSSQL.** Multiply by `1.0`.

## Exercises

Translate each SQLite query to MSSQL. (No sandbox for these, since the sandbox runs SQLite. Check against the answers.)

1. `SELECT name FROM customers ORDER BY age LIMIT 1;`
2. `SELECT name || ' - ' || city FROM customers;`
3. `SELECT product FROM orders WHERE strftime('%Y', order_date) = '2025';`
4. `SELECT department, AVG(salary) FROM employees GROUP BY department;` (keep the decimals)
5. `SELECT product, julianday('2026-03-31') - julianday(order_date) FROM orders;`

And one to run in the sandbox:

6. Inside a transaction, delete every order, then undo it with `ROLLBACK`. (**Sandbox exercise 71.**)

<details>
<summary>Answers</summary>

```sql
-- 1
SELECT TOP 1 name FROM customers ORDER BY age;

-- 2
SELECT name + ' - ' + city FROM customers;
-- or
SELECT CONCAT(name, ' - ', city) FROM customers;

-- 3
SELECT product FROM orders WHERE YEAR(order_date) = 2025;

-- 4
SELECT department, AVG(salary * 1.0) FROM employees GROUP BY department;

-- 5
SELECT product, DATEDIFF(day, order_date, '2026-03-31') FROM orders;

-- 6 (SQLite)
BEGIN TRANSACTION;
DELETE FROM orders;
ROLLBACK;
```
</details>

---
Previous: [Lesson 15](15-views-indexes.md) · Next: [Lesson 17: Final project](17-final-project.md)
