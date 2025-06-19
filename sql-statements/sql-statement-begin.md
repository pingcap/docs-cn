---
title: BEGIN | TiDB SQL 语句参考
summary: TiDB 数据库中 BEGIN 的使用概览。
---

# BEGIN

此语句在 TiDB 中开启一个新的事务。它类似于 `START TRANSACTION` 和 `SET autocommit=0` 语句。

在没有 `BEGIN` 语句的情况下，每个语句默认会在自己的事务中自动提交。这种行为确保了与 MySQL 的兼容性。

## 语法

```ebnf+diagram
BeginTransactionStmt ::=
    'BEGIN' ( 'PESSIMISTIC' | 'OPTIMISTIC' )?
|   'START' 'TRANSACTION' ( 'READ' ( 'WRITE' | 'ONLY' ( 'WITH' 'TIMESTAMP' 'BOUND' TimestampBound )? ) | 'WITH' 'CONSISTENT' 'SNAPSHOT' )?
```

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

TiDB 支持 `BEGIN PESSIMISTIC` 或 `BEGIN OPTIMISTIC` 的语法扩展。这使你可以为你的事务覆盖默认的事务模型。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)
