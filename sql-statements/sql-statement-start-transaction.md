---
title: START TRANSACTION
summary: TiDB 数据库中 START TRANSACTION 的使用概况。
aliases: ['/docs-cn/v3.1/sql-statements/sql-statement-start-transaction/','/docs-cn/v3.1/reference/sql/statements/start-transaction/']
---

# START TRANSACTION

`START TRANSACTION` 语句用于在 TiDB 内部启动新事务。它类似于语句 `BEGIN` 和 `SET autocommit = 0`。

在没有 `START TRANSACTION` 语句的情况下，每个语句都会在各自的事务中自动提交，这样可确保 MySQL 兼容性。

## 语法图

**BeginTransactionStmt:**

![BeginTransactionStmt](/media/sqlgram/BeginTransactionStmt.png)

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

`START TRANSACTION` 语句与 MySQL 不完全兼容。

* `START TRANSACTION` 相当于 MySQL 的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`，即 `START TRANSACTION` 后执行了一个从 InnoDB 任意表读数据的 `SELECT` 语句（非 `SELECT FOR UPDATE`）。
* `READ ONLY` 及其扩展选项都都只是语法兼容，其效果等同于 `START TRANSACTION`。

如发现任何其他兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
