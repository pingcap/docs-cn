---
title: ROLLBACK
summary: TiDB 数据库中 ROLLBACK 的使用概况。
aliases: ['/docs-cn/stable/reference/sql/statements/rollback/']
---

# ROLLBACK

`ROLLBACK` 语句用于还原 TiDB 内当前事务中的所有更改，作用与 `COMMIT` 语句相反。

## 语法图

**RollbackStmt:**

![RollbackStmt](/media/sqlgram/RollbackStmt.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "sql" >}}

```sql
BEGIN;
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
ROLLBACK;
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM t1;
```

```
Empty set (0.01 sec)
```

## MySQL 兼容性

`ROLLBACK` 语句与 MySQL 不完全兼容，TiDB 对任何 `CompletionTypeWithinTransaction` 仅有语法上的支持，即不支持事务回滚后，关闭连接或继续开启一个新事务的回滚选项。如有其他兼容性差异，请在 GitHub 上提交 [issue](/report-issue.md)。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
