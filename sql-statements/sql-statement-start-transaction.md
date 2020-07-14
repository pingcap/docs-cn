---
title: START TRANSACTION | TiDB SQL Statement Reference
summary: An overview of the usage of START TRANSACTION for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-start-transaction/','/docs/dev/reference/sql/statements/start-transaction/']
---

# START TRANSACTION

This statement starts a new transaction inside of TiDB. It is similar to the statement `BEGIN`.

In the absence of a `START TRANSACTION` statement, every statement will by default autocommit in its own transaction. This behavior ensures MySQL compatibility.

## Synopsis

**BeginTransactionStmt:**

![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

This statement is understood to be partly compatible with MySQL.

* `START TRANSACTION` is equivalent to MySQL’s `START TRANSACTION WITH CONSISTENT SNAPSHOT`, that is, after `START TRANSACTION`, a `SELECT` statement (not `SELECT FOR UPDATE`) is executed to read data from any table in InnoDB.
* `READ ONLY` and its extended options are only syntactically compatible, and its effect is equivalent to `START TRANSACTION`.

Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
