---
title: COMMIT
summary: TiDB 数据库中 COMMIT 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/commit/']
---

# COMMIT

`COMMIT` 语句用于在 TiDB 服务器内部提交事务。

在不使用 `BEGIN` 或 `START TRANSACTION` 语句的情况下，TiDB 中每一个查询语句本身也会默认作为事务处理，自动提交，确保了与 MySQL 的兼容。

## 语法图

**CommitStmt:**

![CommitStmt](/media/sqlgram/CommitStmt.png)

**CompletionTypeWithinTransaction:**

![CompletionTypeWithinTransaction](/media/sqlgram/CompletionTypeWithinTransaction.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 VALUES (1);
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
COMMIT;
```

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

* 对于 `COMMIT` 语句中 `CompletionTypeWithinTransaction` 选项，目前只在语法上支持。

## 另请参阅

* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [事务的惰性检查](/transaction-overview.md#事务的惰性检查)
