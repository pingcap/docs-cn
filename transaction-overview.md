---
title: Transactions
summary: Learn transactions in TiDB.
aliases: ['/docs/dev/transaction-overview/','/docs/dev/reference/transactions/overview/']
---

# Transactions

TiDB supports distributed transactions using either [pessimistic](/pessimistic-transaction.md) or [optimistic](/optimistic-transaction.md) transaction mode. Starting from TiDB 3.0.8, TiDB uses the pessimistic transaction mode by default.

This document introduces commonly used transaction-related statements, explicit and implicit transactions, isolation levels, lazy check for constraints, and transaction sizes.

The common variables include [`autocommit`](#autocommit), [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry), [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit), and [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode).

> **Note:**
>
> The [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) and [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) variables only apply to optimistic transactions, not to pessimistic transactions.

## Common statements

### Starting a transaction

The statements [`BEGIN`](/sql-statements/sql-statement-begin.md) and [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) can be used interchangeably to explicitly start a new transaction.

Syntax:

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

If the current session is in the process of a transaction when one of these statements is executed, TiDB automatically commits the current transaction before starting a new transaction.

> **Note:**
>
> Unlike MySQL, TiDB takes a snapshot of the current database after executing the statements above. MySQL's `BEGIN` and `START TRANSACTION` take a snapshot after executing the first `SELECT` statement (not `SELECT FOR UPDATE`) that reads data from InnoDB after a transaction is started. `START TRANSACTION WITH CONSISTENT SNAPSHOT` takes a snapshot during the execution of the statement. As a result, `BEGIN`, `START TRANSACTION`, and `START TRANSACTION WITH CONSISTENT SNAPSHOT` are equivalent to `START TRANSACTION WITH CONSISTENT SNAPSHOT` in MySQL.

### Committing a transaction

The statement [`COMMIT`](/sql-statements/sql-statement-commit.md) instructs TiDB to apply all changes made in the current transaction.

Syntax:

{{< copyable "sql" >}}

```sql
COMMIT;
```

> **Tip:**
>
> Make sure that your application correctly handles that a `COMMIT` statement could return an error before enabling [optimistic transactions](/optimistic-transaction.md). If you are unsure of how your application handles this, it is recommended to instead use the default of [pessimistic transactions](/pessimistic-transaction.md).

### Rolling back a transaction

The statement [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) rolls back and cancels all changes in the current transaction.

Syntax:

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

Transactions are also automatically rolled back if the client connection is aborted or closed.

## Autocommit

As required for MySQL compatibility, TiDB will by default _autocommit_ statements immediately following their execution.

For example:

```sql
mysql> CREATE TABLE t1 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+------+
| id | pad1 |
+----+------+
|  1 | test |
+----+------+
1 row in set (0.00 sec)
```

In the above example, the `ROLLBACK` statement has no effect. This is because the `INSERT` statement is executed in autocommit. That is, it was the equivalent of the following single-statement transaction:

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

Autocommit will not apply if a transaction has been explicitly started. In the following example, the `ROLLBACK` statement successfully reverts the `INSERT` statement:

```sql
mysql> CREATE TABLE t2 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t2 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

The [`autocommit`](/system-variables.md#autocommit) system variable [can be changed](/sql-statements/sql-statement-set-variable.md) on either a global or session basis.

For example:

{{< copyable "sql" >}}

```sql
SET autocommit = 0;
```

{{< copyable "sql" >}}

```sql
SET GLOBAL autocommit = 0;
```

## Explicit and implicit transaction

> **Note:**
>
> Some statements are committed implicitly. For example, executing `[BEGIN|START TRANSACTION]` implicitly commits the last transaction and starts a new transaction. This behavior is required for MySQL compatibility. Refer to [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) for more details.

TiDB supports explicit transactions (use `[BEGIN|START TRANSACTION]` and `COMMIT` to define the start and end of the transaction) and implicit transactions (`SET autocommit = 1`).

If you set the value of `autocommit` to `1` and start a new transaction through the `[BEGIN|START TRANSACTION]` statement, the autocommit is disabled before `COMMIT` or `ROLLBACK` which makes the transaction becomes explicit.

For DDL statements, the transaction is committed automatically and does not support rollback. If you run the DDL statement while the current session is in the process of a transaction, the DDL statement is executed after the current transaction is committed.

## Lazy check of constraints

By default, optimistic transactions will not check the [primary key](/constraints.md#primary-key) or [unique constraints](/constraints.md#unique-key) when a DML statement is executed. These checks are instead performed on transaction `COMMIT`.

For example:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
BEGIN OPTIMISTIC;
INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
INSERT INTO t1 VALUES (2);
COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
```

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> BEGIN OPTIMISTIC;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (2);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
mysql> SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

The lazy check optimization improves performance by batching constraint checks and reducing network communication. The behavior can be disabled by setting [`tidb_constraint_check_in_place=TRUE`](/system-variables.md#tidb_constraint_check_in_place).

> **Note:**
>
> + This optimization only applies to optimistic transactions.
> + This optimization does not take effect for `INSERT IGNORE` and `INSERT ON DUPLICATE KEY UPDATE`, but only for normal `INSERT` statements.

## Statement rollback

TiDB supports atomic rollback after statement execution failure. If a statement results in an error, the changes it made will not take effect. The transaction will remain open, and additional changes can be made before issuing a `COMMIT` or `ROLLBACK` statement.

{{< copyable "sql" >}}

```sql
CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
BEGIN;
INSERT INTO test VALUES (1);
INSERT INTO tset VALUES (2);  -- Statement does not take effect because "test" is misspelled as "tset".
INSERT INTO test VALUES (1),(2);  -- Entire statement does not take effect because it violates a PRIMARY KEY constraint
INSERT INTO test VALUES (3);
COMMIT;
SELECT * FROM test;
```

```sql
mysql> CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.09 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO test VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO tset VALUES (2);  -- Statement does not take effect because "test" is misspelled as "tset".
ERROR 1146 (42S02): Table 'test.tset' doesn't exist
mysql> INSERT INTO test VALUES (1),(2);  -- Entire statement does not take effect because it violates a PRIMARY KEY constraint
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
mysql> INSERT INTO test VALUES (3);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM test;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

In the above example, the transaction remains open after the failed `INSERT` statements. The final insert statement is then successful and changes are committed.

## Transaction size limit

Due to the limitations of the underlying storage engine, TiDB requires a single row to be no more than 6 MB. All columns of a row are converted to bytes according to their data types and summed up to estimate the size of a single row.

TiDB supports both optimistic and pessimistic transactions, and optimistic transactions are the basis for pessimistic transactions. Because optimistic transactions first cache the changes in private memory, TiDB limits the size of a single transaction.

By default, TiDB sets the total size of a single transaction to no more than 100 MB. You can modify this default value via `txn-total-size-limit` in the configuration file. The maximum value of `txn-total-size-limit` is 10 GB.

The actual individual transaction size limit also depends on the amount of remaining memory available to the server, because when a transaction is executed, the memory usage of the TiDB process is approximately six times the size of the transaction.

TiDB previously limited the total number of key-value pairs for a single transaction to 300,000. This restriction was removed in TiDB v4.0.

> **Note:**
>
> Usually, TiDB Binlog is enabled to replicate data to the downstream. In some scenarios, message middleware such as Kafka is used to consume binlogs that are replicated to the downstream.
>
> Taking Kafka as an example, the upper limit of Kafka's single message processing capability is 1 GB. Therefore, when `txn-total-size-limit` is set to more than 1 GB, it might happen that the transaction is successfully executed in TiDB, but the downstream Kafka reports an error. To avoid this situation, you need to decide the actual value of `txn-total-size-limit` according to the limit of the end consumer. For example, if Kafka is used downstream, `txn-total-size-limit` must not exceed 1 GB.

## Causal consistency

> **Note:**
>
> Transactions with causal consistency take effect only when the async commit and one-phase commit features are enabled. For details of the two features, see [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50) and [`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50).

TiDB supports enabling causal consistency for transactions. Transactions with causal consistency, when committed, do not need to get timestamp from PD and have lower commit latency. The syntax to enable causal consistency is as follows:

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

By default, TiDB guarantees linear consistency. In the case of linear consistency, if transaction 2 is committed after transaction 1 is committed, logically, transaction 2 should occur after transaction 1. Causal consistency is weaker than linear consistency. In the case of causal consistency, the commit order and occurrence order of two transactions can be guaranteed consistent only when the data locked or written by transaction 1 and transaction 2 have an intersection, which means that the two transactions have a causal relationship known to the database. Currently, TiDB does not support passing in external causal relationship.

Two transactions with causal consistency enabled have the following characteristics:

+ [Transactions with potential causal relationship have the consistent logical order and physical commit order](#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order)
+ [Transactions with no causal relationship do not guarantee consistent logical order and physical commit order](#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order)
+ [Reads without lock do not create causal relationship](#reads-without-lock-do-not-create-causal-relationship)

### Transactions with potential causal relationship have the consistent logical order and physical commit order

Assume that both transaction 1 and transaction 2 adopt causal consistency and have the following statements executed:

| Transaction 1 | Transaction 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE | |
| UPDATE t set v = $(x + 1) WHERE id = 2 | |
| COMMIT | |
| | UPDATE t SET v = 2 WHERE id = 1 |
| | COMMIT |

In the example above, transaction 1 locks the `id = 1` record and transaction 2 modifies the `id = 1` record. Therefore, transaction 1 and transaction 2 have a potential causal relationship. Even with the causal consistency enabled, as long as transaction 2 is committed after transaction 1 is successfully committed, logically, transaction 2 must occur after transaction 1. Therefore, it is impossible that a transaction reads transaction 2's modification on the `id = 1` record without reading transaction 1's modification on the `id = 2` record.

### Transactions with no causal relationship do not guarantee consistent logical order and physical commit order

Assume that the initial values of `id = 1` and `id = 2` are both `0`. Assume that both transaction 1 and transaction 2 adopt causal consistency and have the following statements executed:

| Transaction 1 | Transaction 2 | Transaction 3 |
|-------|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | |
| UPDATE t set v = 3 WHERE id = 2 | | |
| | UPDATE t SET v = 2 WHERE id = 1 | |
| | | BEGIN |
| COMMIT | | |
| | COMMIT | |
| | | SELECT v FROM t WHERE id IN (1, 2) |

In the example above, transaction 1 does not read the `id = 1` record, so transaction 1 and transaction 2 have no causal relationship known to the database. With causal consistency enabled for the transactions, even if transaction 2 is committed after transaction 1 is committed in terms of physical time order, TiDB does not guarantee that transaction 2 logically occurs after transaction 1.

If transaction 3 begins before transaction 1 is committed, and if transaction 3 reads the `id = 1` and `id = 2` records after transaction 2 is committed, transaction 3 might read the value of `id = 1` to be `2` but the value of `id = 2` to be `0`.

### Reads without lock do not create causal relationship

Assume that both transaction 1 and transaction 2 adopt causal consistency and have the following statements executed:

| Transaction 1 | Transaction 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1 | |
| UPDATE t set v = 3 WHERE id = 2 | |
| | COMMIT |
| COMMIT | |

In the example above, reads without lock do not create causal relationship. Transaction 1 and transaction 2 have created write skew. In this case, it would have been unreasonable if the two transactions still had causal relationship. Therefore, the two transactions with causal consistency enabled have no definite logical order.
