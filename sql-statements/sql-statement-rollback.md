---
title: ROLLBACK | TiDB SQL Statement Reference
summary: An overview of the usage of ROLLBACK for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-rollback/','/docs/dev/reference/sql/statements/rollback/']
---

# ROLLBACK

This statement reverts all changes in the current transaction inside of TIDB.  It is the opposite of a `COMMIT` statement.

## Synopsis

**RollbackStmt:**

![RollbackStmt](/media/sqlgram/RollbackStmt.png)

## Examples

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
Empty set (0.01 sec)
```

## MySQL compatibility

This statement is partly compatible with MySQL. TiDB only has syntactic support for `CompletionTypeWithinTransaction`. Closing the connection or continuing to open a new transaction after the transaction is rolled back is not supported. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
