---
title: START TRANSACTION
summary: TiDB 数据库中 START TRANSACTION 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-start-transaction/','/docs-cn/dev/reference/sql/statements/start-transaction/']
---

# START TRANSACTION

`START TRANSACTION` 语句用于在 TiDB 内部启动新事务。它类似于语句 `BEGIN`。

在没有 `START TRANSACTION` 语句的情况下，每个语句都会在各自的事务中自动提交，这样可确保 MySQL 兼容性。

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

* 执行 `START TRANSACTION` 在 TiDB 中开启事务并立即生成快照。而在 MySQL 中，执行 `START TRANSACTION` 会开启事务但不会立即生成快照。TiDB 中的 `START TRANSACTION` 等同于 MySQL 中的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。
* 为与 MySQL 兼容，TiDB 会解析 `START TRANSACTION READ ONLY` 语句，但解析后 TiDB 仍允许写入操作。

## 另请参阅

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION WITH CAUSAL CONSISTENCY ONLY](/transaction-overview.md#因果一致性事务)
