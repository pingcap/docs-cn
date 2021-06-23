---
title: START TRANSACTION | TiDB SQL Statement Reference
summary: An overview of the usage of START TRANSACTION for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-start-transaction/','/docs/dev/reference/sql/statements/start-transaction/']
---

# START TRANSACTION

This statement starts a new transaction inside of TiDB. It is similar to the statement `BEGIN`.

In the absence of a `START TRANSACTION` statement, every statement will by default autocommit in its own transaction. This behavior ensures MySQL compatibility.

## Synopsis

**BeginTransactionStmt:**

```ebnf+diagram
BeginTransactionStmt ::=
    'BEGIN' ( 'PESSIMISTIC' | 'OPTIMISTIC' )?
|   'START' 'TRANSACTION' ( 'READ' ( 'WRITE' | 'ONLY' ( ( 'WITH' 'TIMESTAMP' 'BOUND' TimestampBound )? | AsOfClause ) ) | 'WITH' 'CONSISTENT' 'SNAPSHOT' | 'WITH' 'CAUSAL' 'CONSISTENCY' 'ONLY' )?

AsOfClause ::=
    ( 'AS' 'OF' 'TIMESTAMP' Expression)
```

## Examples

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

## MySQL compatibility

* `START TRANSACTION` immediately starts a transaction inside TiDB. This differs from MySQL, where `START TRANSACTION` lazily creates a transaction. But `START TRANSACTION` in TiDB is equivalent to MySQL's `START TRANSACTION WITH CONSISTENT SNAPSHOT`.

* The statement `START TRANSACTION READ ONLY` is parsed for compatibility with MySQL, but still allows write operations.

## See also

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [BEGIN](/sql-statements/sql-statement-begin.md)
* [START TRANSACTION WITH CAUSAL CONSISTENCY ONLY](/transaction-overview.md#causal-consistency)
