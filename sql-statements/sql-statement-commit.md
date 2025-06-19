---
title: COMMIT | TiDB SQL 语句参考
summary: TiDB 数据库中 COMMIT 的使用概述。
---

# COMMIT

此语句用于在 TiDB 服务器中提交事务。

在没有 `BEGIN` 或 `START TRANSACTION` 语句的情况下，TiDB 的默认行为是每个语句都将是其自己的事务并自动提交。这种行为确保了与 MySQL 的兼容性。

## 语法

```ebnf+diagram
CommitStmt ::=
    'COMMIT' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

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

* 目前，TiDB 默认使用元数据锁（MDL）来防止 DDL 语句修改事务中使用的表。TiDB 和 MySQL 之间的元数据锁行为有所不同。更多详情，请参见[元数据锁](/metadata-lock.md)。
* 默认情况下，TiDB 3.0.8 及更高版本使用[悲观锁定](/pessimistic-transaction.md)。在使用[乐观锁定](/optimistic-transaction.md)时，需要注意 `COMMIT` 语句可能会因为行被其他事务修改而失败。
* 当启用乐观锁定时，`UNIQUE` 和 `PRIMARY KEY` 约束检查会延迟到语句提交时进行。这会导致 `COMMIT` 语句可能失败的额外情况。可以通过设置 `tidb_constraint_check_in_place=ON` 来改变这种行为。
* TiDB 解析但忽略 `ROLLBACK AND [NO] RELEASE` 语法。在 MySQL 中，此功能用于在提交事务后立即断开客户端会话。在 TiDB 中，建议改用客户端驱动程序的 `mysql_close()` 功能。
* TiDB 解析但忽略 `ROLLBACK AND [NO] CHAIN` 语法。在 MySQL 中，此功能用于在当前事务提交时立即以相同的隔离级别启动新事务。在 TiDB 中，建议直接启动新事务。

## 另请参阅

* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [约束的延迟检查](/transaction-overview.md#lazy-check-of-constraints)
