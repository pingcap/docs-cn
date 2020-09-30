---
title: ROLLBACK
summary: TiDB 数据库中 ROLLBACK 的使用概况。
aliases: ['/docs-cn/v2.1/sql-statements/sql-statement-rollback/','/docs-cn/v2.1/reference/sql/statements/rollback/']
---

# ROLLBACK

`ROLLBACK` 语句用于还原 TiDB 内当前事务中的所有更改，作用与 `COMMIT` 语句相反。

## 语法图

**Statement:**

![Statement](/media/sqlgram/Statement.png)

## 示例

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
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

## MySQL 兼容性

TiDB 不支持 `ROLLBACK TO SAVEPOINT` 语句。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
