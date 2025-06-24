---
title: SAVEPOINT | TiDB SQL 语句参考
summary: TiDB 数据库中 SAVEPOINT 的使用概述。
---

# SAVEPOINT

`SAVEPOINT` 是 TiDB v6.2.0 引入的功能。语法如下：

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **警告：**
>
> - 启用 TiDB Binlog 时不能使用 `SAVEPOINT`。
> - 当 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 被禁用时，不能在悲观事务中使用 `SAVEPOINT`。

- `SAVEPOINT` 用于在当前事务中设置指定名称的保存点。如果已存在同名的保存点，它将被删除，并设置一个同名的新保存点。

- `ROLLBACK TO SAVEPOINT` 将事务回滚到指定名称的保存点，且不会终止事务。保存点之后对表数据所做的更改将在回滚中被撤销，该保存点之后的所有保存点都将被删除。在悲观事务中，事务持有的锁不会被回滚。相反，这些锁将在事务结束时释放。

    如果 `ROLLBACK TO SAVEPOINT` 语句中指定的保存点不存在，该语句将返回以下错误：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

- `RELEASE SAVEPOINT` 语句从当前事务中删除指定名称的保存点以及该保存点之后的**所有保存点**，而不会提交或回滚当前事务。如果指定名称的保存点不存在，将返回以下错误：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

    事务提交或回滚后，事务中的所有保存点都将被删除。

## 语法概要

```ebnf+diagram
SavepointStmt ::=
    "SAVEPOINT" Identifier

RollbackToStmt ::=
    "ROLLBACK" "TO" "SAVEPOINT"? Identifier

ReleaseSavepointStmt ::=
    "RELEASE" "SAVEPOINT" Identifier
```

## 示例

创建表 `t1`：

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

开始当前事务：

```sql
BEGIN;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

向表中插入数据并设置保存点 `sp1`：

```sql
INSERT INTO t1 VALUES (1);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

再次向表中插入数据并设置保存点 `sp2`：

```sql
INSERT INTO t1 VALUES (2);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

释放保存点 `sp2`：

```sql
RELEASE SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

回滚到保存点 `sp1`：

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

提交事务并查询表。只返回 `sp1` 之前插入的数据。

```sql
COMMIT;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
SELECT * FROM t1;
```

```sql
+---+
| a |
+---+
| 1 |
+---+
1 row in set
```

## MySQL 兼容性

当使用 `ROLLBACK TO SAVEPOINT` 将事务回滚到指定保存点时，MySQL 会立即释放仅在指定保存点之后持有的锁，而在 TiDB 悲观事务中，TiDB 不会立即释放指定保存点之后持有的锁。相反，TiDB 会在事务提交或回滚时释放所有锁。

TiDB 不支持 MySQL 的 `ROLLBACK WORK TO SAVEPOINT ...` 语法。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB 乐观事务模式](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)
