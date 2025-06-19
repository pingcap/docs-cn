---
title: ROLLBACK | TiDB SQL 语句参考
summary: TiDB 数据库中 ROLLBACK 的使用概览。
---

# ROLLBACK

此语句撤销 TiDB 中当前事务的所有更改。它是 `COMMIT` 语句的反操作。

## 语法

```ebnf+diagram
RollbackStmt ::=
    'ROLLBACK' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

## 示例

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
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

* TiDB 解析但忽略 `ROLLBACK AND [NO] RELEASE` 语法。此功能在 MySQL 中用于在回滚事务后立即断开客户端会话连接。在 TiDB 中，建议改用客户端驱动程序的 `mysql_close()` 功能。
* TiDB 解析但忽略 `ROLLBACK AND [NO] CHAIN` 语法。此功能在 MySQL 中用于在当前事务回滚时立即以相同的隔离级别启动新事务。在 TiDB 中，建议直接启动新事务。

## 另请参阅

* [SAVEPOINT](/sql-statements/sql-statement-savepoint.md)
* [COMMIT](/sql-statements/sql-statement-commit.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
