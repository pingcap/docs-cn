---
title: COMMIT | TiDB SQL Statement Reference
summary: An overview of the usage of COMMIT for the TiDB database.
category: reference
---

# COMMIT

This statement commits a transaction inside of the TIDB server.

In the absense of a `BEGIN` or `START TRANSACTION` statement, the default behavior of TiDB is that every statement will be its own transaction and autocommit. This behavior ensures MySQL compatibility.

## Synopsis

**CommitStmt:**

![CommitStmt](/media/sqlgram-v3.0/CommitStmt.png)

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

* In MySQL, with the exception of Group Replication with multiple primaries, it is not typical that a `COMMIT` statement could result in an error. By contrast, TiDB uses optimistic concurrency control and conflicts may result in `COMMIT` returning an error.
* Be default, `UNIQUE` and `PRIMARY KEY` constraint checks are deffered until statement commit. This behavior can be changed by setting `tidb_constraint_check_in_place=TRUE`.

## See also

* [START TRANSACTION](/reference/sql/statements/start-transaction.md)
* [ROLLBACK](/reference/sql/statements/rollback.md)
* [BEGIN](/reference/sql/statements/begin.md)
* [Lazy checking of constraints](/reference/transactions/overview.md#lazy-check-of-constraints)
