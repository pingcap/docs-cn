---
title: SAVEPOINT
summary: TiDB 数据库中 SAVEPOINT 的使用概况。
---

# SAVEPOINT

`SAVEPOINT` 是 TiDB 从 v6.2.0 开始支持的特性，语法如下：

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **警告：**
>
> `SAVEPOINT` 特性不支持在关闭 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-从-v630-版本开始引入) 的悲观事务中使用。

- `SAVEPOINT` 语句用于在当前事务中，设置一个指定名字保存点。如果已经存在相同名字的保存点，就删除已有的保存点并设置新的保存点。

- `ROLLBACK TO SAVEPOINT` 语句将事务回滚到指定名称的事务保存点，而不终止该事务。当前事务在设置保存点后，对表数据所做的修改将在回滚中撤销，且删除事务保存点之后的所有保存点。在悲观事务中，对于已经持有的悲观锁不会回滚，而是在事务结束时才释放。

    如果 `ROLLBACK TO SAVEPOINT` 语句中指定名称的保存点不存在，则会返回以下错误信息：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

- `RELEASE SAVEPOINT` 语句将从当前事务中删除指定名称及之后的**_所有_**保存点，而不会提交或回滚当前事务。如果指定名称的保存点不存在，则会返回以下错误信息：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

    当事务提交或者回滚后，事务中所有保存点都会被删除。

## 语法图

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
CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
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

向表中再次插入数据并设置保存点 `sp2`：

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

回滚至保存点 `sp1`：

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

提交事务并查询表格，发现表中仅有 `sp1` 前插入的数据：

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

使用 `ROLLBACK TO SAVEPOINT` 语句将事物回滚到指定保存点时，MySQL 会释放该保存点之后才持有的锁，但在 TiDB 悲观事务中，不会立即释放该保存点之后才持有的锁，而是等到事务提交或者回滚时，才释放全部持有的锁。

TiDB 不支持 MySQL 中的 `ROLLBACK WORK TO SAVEPOINT ...` 语法。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)
