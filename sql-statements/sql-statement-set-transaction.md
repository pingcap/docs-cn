---
title: SET TRANSACTION | TiDB SQL 语句参考
summary: TiDB 数据库中 SET TRANSACTION 的使用概述。
---

# SET TRANSACTION

`SET TRANSACTION` 语句可用于在 `GLOBAL` 或 `SESSION` 级别更改当前的隔离级别。这种语法是 `SET transaction_isolation='new-value'` 的替代方式，包含它是为了与 MySQL 和 SQL 标准保持兼容。

## 语法

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

```sql
mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)

mysql> SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+----------------+
| Variable_name         | Value          |
+-----------------------+----------------+
| transaction_isolation | READ-COMMITTED |
+-----------------------+----------------+
1 row in set (0.01 sec)

mysql> SET SESSION transaction_isolation = 'REPEATABLE-READ';
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 仅在语法上支持将事务设置为只读。
* 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别。
* `REPEATABLE-READ` 隔离级别是通过使用快照隔离技术实现的，与 MySQL 部分兼容。
* 在悲观事务中，TiDB 支持两种与 MySQL 兼容的隔离级别：`REPEATABLE-READ` 和 `READ-COMMITTED`。详细说明请参见[隔离级别](/transaction-isolation-levels.md)。

## 另请参阅

* [`SET [GLOBAL|SESSION] <variable>`](/sql-statements/sql-statement-set-variable.md)
* [隔离级别](/transaction-isolation-levels.md)
