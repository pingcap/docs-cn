---
title: COMMIT
summary: TiDB 数据库中 COMMIT 的使用概况。
---

# COMMIT

`COMMIT` 语句用于在 TiDB 服务器内部提交事务。

在不使用 `BEGIN` 或 `START TRANSACTION` 语句的情况下，TiDB 中每一个查询语句本身也会默认作为事务处理，自动提交，确保了与 MySQL 的兼容。

## 语法图

```ebnf+diagram
CommitStmt ::=
    'COMMIT' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

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

* TiDB 3.0.8 及更新版本默认使用[悲观事务模型](/pessimistic-transaction.md)。在[乐观事务模型](/optimistic-transaction.md)下，需要考虑到修改的行已被另一个事务修改，导致 `COMMIT` 语句可能执行失败的情况。
* 启用乐观事务模型后，`UNIQUE` 和 `PRIMARY KEY` 约束检查将延迟直至语句提交。当 `COMMIT` 语句失败时，这可能导致其他问题。可通过设置 `tidb_constraint_check_in_place=TRUE` 来改变该行为。
* TiDB 解析但忽略 `ROLLBACK AND [NO] RELEASE` 语法。在 MySQL 中，使用该语法可在提交事务后立即断开客户端会话。在 TiDB 中，建议使用客户端程序的 `mysql_close()` 来实现该功能。
* TiDB 解析但忽略 `ROLLBACK AND [NO] CHAIN` 语法。在 MySQL 中，使用该语法可在提交当前事务时立即以相同的隔离级别开启新事务。在 TiDB 中，推荐直接开启新事务。

## 另请参阅

* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [事务的惰性检查](/transaction-overview.md#惰性检查)
