---
title: START TRANSACTION
summary: TiDB 数据库中 START TRANSACTION 的使用概况。
category: reference
---

# START TRANSACTION

`START TRANSACTION` 语句用于在 TiDB 内部启动新事务。它类似于语句 `BEGIN` 和 `SET autocommit = 0`。

在没有 `START TRANSACTION` 语句的情况下，每个语句都会在各自的事务中自动提交，这样可确保 MySQL 兼容性。

## 总览

**BeginTransactionStmt:**

![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)

## 实例

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

## MySQL 兼容性

`START TRANSACTION` 语句可视为与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [COMMIT](/dev/reference/sql/statements/commit.md)
* [ROLLBACK](/dev/reference/sql/statements/rollback.md)
* [BEGIN](/dev/reference/sql/statements/begin.md)