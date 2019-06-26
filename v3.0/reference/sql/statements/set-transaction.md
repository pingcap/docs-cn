---
title: SET TRANSACTION | TiDB SQL Statement Reference 
summary: An overview of the usage of SET TRANSACTION for the TiDB database.
category: reference
---

# SET TRANSACTION

The `SET TRANSACTION` statement can be used to change the current isolation level on a `GLOBAL` or `SESSION` basis. This syntax is an alternative to `SET transaction_isolation='new-value'` and is included for compatibility with both MySQL, and the SQL standards.

## Synopsis

**SetStmt:**

![SetStmt](/media/sqlgram-v3.0/SetStmt.png)

**TransactionChar:**

![TransactionChar](/media/sqlgram-v3.0/TransactionChar.png)

**IsolationLevel:**

![IsolationLevel](/media/sqlgram-v3.0/IsolationLevel.png)

## Examples

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

## MySQL compatibility

* TiDB supports the ability to set a transaction as read-only in syntax only.
* The isolation levels `READ-UNCOMMITTED` and `SERIALIZABLE` are not supported.
* The isolation level `REPEATABLE-READ` is technically Snapshot Isolation. The name `REPEATABLE-READ` is used for compatibility with MySQL.

## See also

* [SET \[GLOBAL|SESSION\] <variable>](/reference/sql/statements/set-variable.md)
* [Isolation Levels](/reference/transactions/transaction-isolation.md)
