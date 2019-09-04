---
title: SET TRANSACTION
summary: TiDB 数据库中 SET TRANSACTION 的使用概况。
category: reference
---

# SET TRANSACTION

`SET TRANSACTION` 语句用于在 `GLOBAL` 或 `SESSION` 的基础上更改当前的隔离级别，是 `SET transaction_isolation ='new-value'` 的替代语句，提供 MySQL 和 SQL 标准的兼容性。

## 语法图

**SetStmt:**

![SetStmt](/media/sqlgram/SetStmt.png)

**TransactionChar:**

![TransactionChar](/media/sqlgram/TransactionChar.png)

**IsolationLevel:**

![IsolationLevel](/media/sqlgram/IsolationLevel.png)

## 示例

```sql
mysql> SHOW SESSION VARIABLES like 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)

mysql> SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES like 'transaction_isolation';
+-----------------------+----------------+
| Variable_name         | Value          |
+-----------------------+----------------+
| transaction_isolation | READ-COMMITTED |
+-----------------------+----------------+
1 row in set (0.01 sec)

mysql> SET SESSION transaction_isolation = 'REPEATABLE-READ';
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES like 'transaction_isolation';
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
* 隔离级别 `REPEATABLE-READ` 在技术上属于快照隔离（Snapshot Isolation）。在 TiDB 中称为 `REPEATABLE-READ` 是为了和 MySQL 保持一致。

## 另请参阅

* [SET \[GLOBAL|SESSION\] <variable>](/dev/reference/sql/statements/set-variable.md)
* [Isolation Levels](/dev/reference/transactions/transaction-isolation.md)
