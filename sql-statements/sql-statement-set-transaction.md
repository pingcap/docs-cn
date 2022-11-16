---
title: SET TRANSACTION
summary: TiDB 数据库中 SET TRANSACTION 的使用概况。
---

# SET TRANSACTION

`SET TRANSACTION` 语句用于在 `GLOBAL` 或 `SESSION` 的基础上更改当前的隔离级别，是 `SET transaction_isolation ='new-value'` 的替代语句，提供 MySQL 和 SQL 标准的兼容性。

## 语法图

```ebnf+diagram

SetStmt ::=
    'SET' ( VariableAssignmentList | 
    'PASSWORD' ('FOR' Username)? '=' PasswordOpt | 
    ( 'GLOBAL'| 'SESSION' )? 'TRANSACTION' TransactionChars | 
    'CONFIG' ( Identifier | stringLit) ConfigItemName EqOrAssignmentEq SetExpr )

TransactionChars ::=
    ( 'ISOLATION' 'LEVEL' IsolationLevel | 'READ' 'WRITE' | 'READ' 'ONLY' AsOfClause? )

IsolationLevel ::=
    ( 'REPEATABLE' 'READ' | 'READ' ( 'COMMITTED' | 'UNCOMMITTED' ) | 'SERIALIZABLE' )

AsOfClause ::=
    ( 'AS' 'OF' 'TIMESTAMP' Expression)
```

## 示例

{{< copyable "sql" >}}

```sql
SHOW SESSION VARIABLES LIKE 'transaction_isolation';
```

```
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW SESSION VARIABLES LIKE 'transaction_isolation';
```

```
+-----------------------+----------------+
| Variable_name         | Value          |
+-----------------------+----------------+
| transaction_isolation | READ-COMMITTED |
+-----------------------+----------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SET SESSION transaction_isolation = 'REPEATABLE-READ';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW SESSION VARIABLES LIKE 'transaction_isolation';
```

```
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 支持仅在语法中将事务设置为只读的功能。
* 不支持隔离级别 `READ-UNCOMMITTED` 和 `SERIALIZABLE`。
* 通过快照隔离 (Snapshot Isolation) 技术，实现乐观事务的 `REPEATABLE-READ` 隔离级别，和 MySQL 兼容。
* 在悲观事务中，TiDB 支持与 MySQL 兼容的 `REPEATABLE-READ` 和 `READ-COMMITTED` 两种隔离级别。具体描述详见 [Isolation Levels](/transaction-isolation-levels.md)。

## 另请参阅

* [`SET \[GLOBAL|SESSION\] <variable>`](/sql-statements/sql-statement-set-variable.md)
* [Isolation Levels](/transaction-isolation-levels.md)
