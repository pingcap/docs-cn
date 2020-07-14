---
title: BEGIN | TiDB SQL Statement Reference
summary: An overview of the usage of BEGIN for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-begin/','/docs/dev/reference/sql/statements/begin/']
---

# BEGIN

This statement starts a new transaction inside of TiDB. It is similar to the statements `START TRANSACTION` and `SET autocommit=0`.

In the absence of a `BEGIN` statement, every statement will by default autocommit in its own transaction. This behavior ensures MySQL compatibility.

## Synopsis

**BeginTransactionStmt:**

![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

You can add the `PESSIMISTIC` or `OPTIMISTIC` option to the `BEGIN` statement in TiDB to indicate the type of transaction that this statement starts.

## See also

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB optimistic transaction model](/optimistic-transaction.md)
* [TiDB pessimistic transaction model](/pessimistic-transaction.md)
