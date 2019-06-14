---
title: BEGIN
summary: TiDB 数据库中 BEGIN 的使用概况。
category: reference
---

# BEGIN

`BEGIN` 语句用于在 TiDB 内启动一个新事务，类似于 `START TRANSACTION` 和 `SET autocommit=0` 语句。

在没有 `BEGIN` 语句的情况下，每个语句默认在各自的事务中自动提交，从而确保 MySQL 兼容性。


## 语法图

**BeginTransactionStmt:**

![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)

## 示例

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

## MySQL 兼容性

`BEGIN` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 [提交 issue](/report-issue.md)。

## 另请参阅

* [COMMIT](/dev/reference/sql/statements/commit.md)
* [ROLLBACK](/dev/reference/sql/statements/rollback.md)
* [START TRANSACTION](/dev/reference/sql/statements/start-transaction.md)