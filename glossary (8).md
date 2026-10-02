# SQL glossary

Every term used in the course, A to Z. The number in brackets is the lesson where it's introduced.

| Term | Meaning |
|---|---|
| **ACID** | The guarantees of a transaction: Atomic (all or nothing), Consistent, Isolated, Durable. [16] |
| **Aggregate function** | A function that turns many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. [3] |
| **Alias** | A temporary name given with `AS`, for a column (`AVG(age) AS average_age`) or a table (`FROM customers c`). [3, 5] |
| **ALTER TABLE** | Changes an existing table's structure, e.g. adds a column. [11] |
| **AND / OR** | Combine conditions: `AND` needs both true, `OR` needs either. [2] |
| **ASC / DESC** | Sort direction in `ORDER BY`: ascending (A→Z, 1→9, the default) or descending. [2] |
| **BETWEEN** | Inclusive range test: `rating BETWEEN 1 AND 5`. [9, 11] |
| **CASE** | If/then logic that produces a value: `CASE WHEN ... THEN ... ELSE ... END`. [7] |
| **CHECK** | A constraint requiring each value to pass a test. [11] |
| **Clause** | One part of a statement, like `WHERE ...` or `ORDER BY ...`. [1] |
| **COALESCE** | Returns the first value that isn't NULL: `COALESCE(x, 0)`. [8] |
| **Column (field)** | One attribute that every row of a table has. [0] |
| **COMMIT** | Makes a transaction's changes permanent. [16] |
| **Constraint** | A rule the database enforces on data: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, foreign key. [11] |
| **CREATE TABLE** | Defines a new table. [11] |
| **CROSS JOIN** | Pairs every row of one table with every row of another. [5] |
| **CTE (Common Table Expression)** | A named temporary result defined with `WITH`, used by the query that follows. [12] |
| **Data type** | The kind of value a column holds: integer, decimal, text, date… [11] |
| **Database** | An organized collection of data. [0] |
| **DBMS** | The software that manages a database (SQLite, MySQL, PostgreSQL, SQL Server, Oracle). [0] |
| **DEFAULT** | A constraint giving a column's value when none is supplied. [11] |
| **DELETE** | Removes rows: `DELETE FROM table WHERE ...`. [10] |
| **DENSE_RANK** | Window function that ranks with ties and no gaps (1, 2, 2, 3). [13] |
| **Dialect** | A DBMS's own version of SQL. [0] |
| **DISTINCT** | Removes duplicate rows from a result. [8] |
| **DROP** | Deletes a whole table, view, or index. [11, 15] |
| **EXCEPT (MINUS)** | Rows in the first query's result but not the second's. [14] |
| **Execution order** | The order SQL actually runs clauses: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT. [4] |
| **Foreign key** | A column that points to another table's primary key. [5, 11] |
| **FULL OUTER JOIN** | A join that keeps unmatched rows from both tables. [5] |
| **GROUP BY** | Splits rows into groups so aggregates are calculated per group. [3] |
| **HAVING** | Filters groups after `GROUP BY`; may use aggregates. [4] |
| **IN / NOT IN** | Tests whether a value is (or isn't) in a list or subquery result. [2, 6] |
| **Index** | A lookup structure that speeds up finding rows. [15] |
| **INNER JOIN (JOIN)** | Combines rows from two tables where they match; unmatched rows are dropped. [5] |
| **INSERT** | Adds rows: `INSERT INTO table (cols) VALUES (...)`. [10] |
| **INTERSECT** | Rows present in both queries' results. [14] |
| **IS NULL / IS NOT NULL** | The only correct way to test for NULL. [5] |
| **LAG / LEAD** | Window functions returning a value from the previous / next row. [13] |
| **LEFT JOIN** | A join that keeps every row of the first (left) table. [5] |
| **LIKE** | Pattern matching on text with `%` (any characters) and `_` (one character). [8] |
| **LIMIT / TOP / FETCH FIRST** | Caps the number of rows returned (SQLite and MySQL / MSSQL / Oracle). [2] |
| **NOT NULL** | A constraint requiring a value. [11] |
| **NULL** | A marker for "no value / unknown". Not zero, not empty text. [5] |
| **ORDER BY** | Sorts the result. [2] |
| **OVER** | Turns a function into a window function and defines its window. [13] |
| **PARTITION BY** | Splits a window into groups, like `GROUP BY` without collapsing rows. [13] |
| **Primary key** | A column that uniquely identifies each row. [0, 11] |
| **Query** | A request for data, written in SQL. [0] |
| **Query plan** | The database's plan for running a query; see it with `EXPLAIN QUERY PLAN`. [15] |
| **RANK** | Window function that ranks with ties and gaps (1, 2, 2, 4). [13] |
| **Relational database** | A database of linked tables. [0] |
| **Result set** | The rows a query returns. [0] |
| **RIGHT JOIN** | A join that keeps every row of the second (right) table. [5] |
| **ROLLBACK** | Undoes every change in the current transaction. [16] |
| **Row (record)** | One item in a table. [0] |
| **ROW_NUMBER** | Window function numbering rows 1, 2, 3… with no ties. [13] |
| **Running total** | A cumulative sum, row by row: `SUM(x) OVER (ORDER BY ...)`. [13] |
| **Schema** | The structure of a database: tables, columns, links. [0] |
| **SELECT** | The statement that reads data. [1] |
| **SET** | The part of `UPDATE` that says what to change. [10] |
| **SQL** | Structured Query Language, the language of relational databases. [0] |
| **Statement** | One complete SQL command, ending with `;`. [1] |
| **Subquery** | A query in parentheses inside another query. [6] |
| **Table** | Data about one kind of thing, in rows and columns. [0] |
| **Transaction** | A group of changes that succeed or fail together. [16] |
| **T-SQL** | Transact-SQL, Microsoft SQL Server's dialect. [16] |
| **UNION / UNION ALL** | Stack two results; `UNION` removes duplicates, `UNION ALL` keeps them. [14] |
| **UNIQUE** | A constraint forbidding duplicate values in a column. [11] |
| **UPDATE** | Changes existing rows: `UPDATE table SET ... WHERE ...`. [10] |
| **View** | A saved query you can use like a table. [15] |
| **WHERE** | Filters individual rows. [1] |
| **Wildcard** | A pattern character in `LIKE`: `%` or `_`. [8] |
| **Window function** | A function over related rows that keeps every row in the result. [13] |
| **WITH** | Starts one or more CTEs. [12] |
