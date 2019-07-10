---
title: COMMIT
summary: TiDB 数据库中 COMMIT 的使用概况。
category: reference
---

# COMMIT

`COMMIT` 语句用于在 TiDB 服务器内部提交事务。

在不使用 `BEGIN` 或 `START TRANSACTION` 语句的情况下，TiDB 中每一个查询语句本身也会默认作为事务处理，自动提交，确保了与 MySQL 的兼容。

## 语法图

**CommitStmt:**

![CommitStmt](/media/sqlgram/CommitStmt.png)

## 示例

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

* 在 MySQL 中，除了有多个 primary 的群组复制以外，`COMMIT` 语句通常不会导致错误。相比之下，TiDB 使用乐观并发控制，冲突可能导致 `COMMIT` 返回错误。
* 默认情况下，`UNIQUE` 和 `PRIMARY KEY` 约束检查将延迟直至语句提交。可通过设置 `tidb_constraint_check_in_place=TRUE` 来改变该行为。

## 另请参阅

* [START TRANSACTION](/reference/sql/statements/start-transaction.md)
* [ROLLBACK](/reference/sql/statements/rollback.md)
* [BEGIN](/reference/sql/statements/begin.md)
* [事务的惰性检查](/reference/transactions/overview.md#事务的惰性检查)
