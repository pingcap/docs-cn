---
title: START TRANSACTION | TiDB SQL 语句参考
summary: TiDB 数据库中 START TRANSACTION 的使用概述。
---

# START TRANSACTION

此语句在 TiDB 中启动一个新的事务。它类似于 `BEGIN` 语句。

在没有 `START TRANSACTION` 语句的情况下，每个语句默认会在其自己的事务中自动提交。这种行为确保了与 MySQL 的兼容性。

## 语法图

**BeginTransactionStmt:**

```ebnf+diagram
BeginTransactionStmt ::=
    'BEGIN' ( 'PESSIMISTIC' | 'OPTIMISTIC' )?
|   'START' 'TRANSACTION' ( 'READ' ( 'WRITE' | 'ONLY' ( ( 'WITH' 'TIMESTAMP' 'BOUND' TimestampBound )? | AsOfClause ) ) | 'WITH' 'CONSISTENT' 'SNAPSHOT' | 'WITH' 'CAUSAL' 'CONSISTENCY' 'ONLY' )?

AsOfClause ::=
    ( 'AS' 'OF' 'TIMESTAMP' Expression)
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

* `START TRANSACTION` 在 TiDB 中立即启动一个事务。这与 MySQL 不同，MySQL 中的 `START TRANSACTION` 会延迟创建事务。但是 TiDB 中的 `START TRANSACTION` 等同于 MySQL 的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。

* 为了与 MySQL 兼容，会解析 `START TRANSACTION READ ONLY` 语句，但仍然允许写操作。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION WITH CAUSAL CONSISTENCY ONLY](/transaction-overview.md#causal-consistency)
