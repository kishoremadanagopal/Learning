# Lesson 0: What databases and SQL are

**You'll learn:** what a database is, how data is organized in tables, what keys are, and why there are several "flavors" of SQL.

## Key terms

- **Data:** facts stored for later use: names, prices, dates.
- **Database:** an organized collection of data, stored so it can be searched and updated quickly and safely.
- **DBMS (Database Management System):** the software that runs a database and answers your requests, like SQLite, MySQL, PostgreSQL, Microsoft SQL Server, or Oracle.
- **Relational database:** a database that stores data in tables that are linked to each other. Every database in this course is relational.
- **Table:** a set of data about one kind of thing (customers, orders), arranged in rows and columns.
- **Row (record):** one item in a table, like one customer.
- **Column (field):** one attribute every row has, like `city`.
- **Value (cell):** what's stored where a row and column meet, like `'Fremont'`.
- **Schema:** the design of a database: which tables exist, their columns, and how they link.
- **Primary key:** a column whose value uniquely identifies each row, like `customers.id`.
- **Foreign key:** a column that points to the primary key of another table, like `orders.customer_id`.
- **NULL:** a special marker meaning "no value" or "unknown." It isn't zero and isn't empty text.
- **Query:** a request to the database, written in SQL.
- **Result set:** the table of rows a query returns.
- **SQL (Structured Query Language):** the standard language for working with relational databases. Pronounced "S-Q-L" or "sequel."
- **Dialect:** a DBMS's own version of SQL. The core is the same everywhere, with small differences in the details.

## Why not just use a spreadsheet?

Spreadsheets are great for small, personal data. Databases take over when:

- the data is **large** (millions of rows)
- **many people or apps** use it at the same time
- the data must stay **correct** (no order for a customer who doesn't exist)
- you need to **combine** data from many tables quickly

## How data is organized

A relational database splits data into tables so each fact is stored **once**. Customer details live in `customers`; each order lives in `orders` and points back to its customer:

```
customers                    orders
┌────┬───────┐              ┌──────────┬─────────────┬─────────┐
│ id │ name  │              │ order_id │ customer_id │ product │
├────┼───────┤              ├──────────┼─────────────┼─────────┤
│ 1  │ Maya  │◄─────────────│ 101      │ 1           │ Laptop  │
│    │       │◄─────────────│ 102      │ 1           │ Mouse   │
│ 2  │ Leo   │◄─────────────│ 103      │ 2           │ Desk    │
└────┴───────┘              └──────────┴─────────────┴─────────┘
 primary key                              foreign key
```

If Maya changes her name, it changes in one place, and every order still points to her.

## What SQL can do

| Kind of task | Statements | Lessons |
|---|---|---|
| **Read** data (queries) | `SELECT` | 1–9, 12–14 |
| **Change** data | `INSERT`, `UPDATE`, `DELETE` | 10 |
| **Define** structure | `CREATE`, `ALTER`, `DROP` | 11, 15 |
| **Control** changes | `BEGIN`, `COMMIT`, `ROLLBACK` | 16 |

Most of your time with SQL is spent reading data, so that's most of the course.

## SQL is declarative

You describe **what** you want ("names of customers in Fremont"), not **how** to find it. The database works out the fastest way. That's why SQL reads almost like English:

```sql
SELECT name FROM customers WHERE city = 'Fremont';
```

## Dialects

| DBMS | Made by | Typical use |
|---|---|---|
| SQLite | open source | apps, phones, browsers, learning (this course's sandbox) |
| MySQL | Oracle (open source) | websites |
| PostgreSQL | open source | websites, analytics |
| Microsoft SQL Server | Microsoft | businesses; its dialect is called **T-SQL** |
| Oracle Database | Oracle | large enterprises |

About 90% of what you learn works in all of them. Each lesson notes the differences, and [Lesson 16](16-mssql-transactions.md) collects them.

## How to write SQL well

- Put keywords in capitals (`SELECT`, `WHERE`) and names in lowercase. SQL doesn't require it, but it's easier to read.
- Put each clause on its own line.
- End each statement with a semicolon `;`.
- Comments start with `--` and run to the end of the line:

```sql
-- Customers who live in Fremont
SELECT name
FROM customers
WHERE city = 'Fremont';
```

---
Next: [The practice tables](00-the-tables.md) · [Lesson 1: First queries](01-first-queries.md)
