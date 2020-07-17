---
title: Transactions
summary: Learn transactions in TiDB.
aliases: ['/docs/dev/transaction-overview/','/docs/dev/reference/transactions/overview/']
---

# Transactions

TiDB supports complete distributed transactions. Both [optimistic transaction model](/optimistic-transaction.md) and [pessimistic transaction model](/pessimistic-transaction.md)(introduced in TiDB 3.0) are available. This document introduces commonly used transaction-related statements, explicit and implicit transactions, isolation levels, lazy check for constraints, and transaction sizes.

The common variables include [`autocommit`](#autocommit), [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry), [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit), and [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode).

## Common syntax

### `BEGIN`, `START TRANSACTION` and `START TRANSACTION WITH CONSISTENT SNAPSHOT`

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

All of the above three statements are used to start a transaction with the same effect. You can explicitly start a new transaction by executing one of these statements. If the current session is in the process of a transaction when one of these statements is executed, TiDB automatically commits the current transaction before starting a new transaction.

> **Note:**
>
> Unlike MySQL, TiDB takes a snapshot of the current database after executing the statements above. MySQL's `BEGIN` and `START TRANSACTION` take a snapshot after executing the first `SELECT` statement (not `SELECT FOR UPDATE`) that reads data from InnoDB after a transaction is started. `START TRANSACTION WITH CONSISTENT SNAPSHOT` takes a snapshot during the execution of the statement. As a result, `BEGIN`, `START TRANSACTION`, and `START TRANSACTION WITH CONSISTENT SNAPSHOT` are equivalent to `START TRANSACTION WITH CONSISTENT SNAPSHOT` in MySQL.

### `COMMIT`

Syntax:

{{< copyable "sql" >}}

```sql
COMMIT;
```

You can use this statement to commit the current transaction, including all updates between `[BEGIN|START TRANSACTION]` and `COMMIT`.

### `ROLLBACK`

Syntax:

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

You can use this statement to roll back the current transaction and cancels all updates between `[BEGIN | START TRANSACTION]` and `ROLLBACK`.

## Autocommit

Syntax:

{{< copyable "sql" >}}

```sql
SET autocommit = {0 | 1}
```

When `autocommit = 1` (default), the status of the current session is autocommit. That is, statements are automatically committed immediately following their execution.

When `autocommit = 0`, the status of the current session is non-autocommit. That is, statements are only committed when you manually execute the `COMMIT` statement.

> **Note:**
>
> Some statements are committed implicitly. For example, executing `[BEGIN|START TRANSACTION]` implicitly commits the last transaction and starts a new transaction. This behavior is required for MySQL compatibility. Refer to [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) for more details.

`autocommit` is also a system variable. You can update the current session or the Global value using the following variable assignment statement:

{{< copyable "sql" >}}

```sql
SET @@SESSION.autocommit = {0 | 1};
```

{{< copyable "sql" >}}

```sql
SET @@GLOBAL.autocommit = {0 | 1};
```

## Explicit and implicit transaction

TiDB supports explicit transactions (use `[BEGIN|START TRANSACTION]` and `COMMIT` to define the start and end of the transaction) and implicit transactions (`SET autocommit = 1`).

If you set the value of `autocommit` to `1` and start a new transaction through the `[BEGIN|START TRANSACTION]` statement, the autocommit is disabled before `COMMIT` or `ROLLBACK` which makes the transaction becomes explicit.

For DDL statements, the transaction is committed automatically and does not support rollback. If you run the DDL statement while the current session is in the process of a transaction, the DDL statement is executed after the current transaction is committed.

## Lazy check of constraints

**Lazy check** means that by default TiDB will not check [primary key](/constraints.md#primary-key) or [unique constraints](/constraints.md#unique-key) when an `INSERT` statement is executed, but instead checks when the transaction is committed. In TiDB, the lazy check is performed for values written by ordinary `INSERT` statements.

For example:

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
START TRANSACTION;
INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
INSERT INTO t1 VALUES (2);
COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
```

The lazy check is important because if you perform a unique constraint check on every `INSERT` statement in a transaction, it can cause high network overhead. A batch check when the transaction is committed can greatly improve performance.

> **Note:**
>
> + This optimization only takes effect in optimistic transactions.
> + This optimization does not take effect for `INSERT IGNORE` and `INSERT ON DUPLICATE KEY UPDATE`, but only for normal `INSERT` statements. The behavior can also be disabled by setting `tidb_constraint_check_in_place=TRUE`.

## Statement rollback

TiDB supports atomic rollback after statement execution failure. If you execute a statement within a transaction, the statement does not take effect when an error occurs.

```sql
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
commit;
```

In the above example, the second `insert` statement fails, while the other two `insert` statements (1 & 3) can be successfully committed.

```sql
begin;
insert into test values (1);
insert into tset values (2);  // This statement does not take effect because "test" is misspelled as "tset".
insert into test values (3);
rollback;
```

In the above example, the second `insert` statement fails, and this transaction does not insert any data into the database because `rollback` is called.

## Transaction size limit

Due to the limitations of the underlying storage engine, TiDB requires a single row to be no more than 6 MB. All columns of a row are converted to bytes according to their data types and summed up to estimate the size of a single row.

TiDB supports both optimistic and pessimistic transactions, and optimistic transactions are the basis for pessimistic transactions. Because optimistic transactions first cache the changes in private memory, TiDB limits the size of a single transaction.

By default, TiDB sets the total size of a single transaction to no more than 100 MB. You can modify this default value via `txn-total-size-limit` in the configuration file. The maximum value of `txn-total-size-limit` is 10 GB.

The actual individual transaction size limit also depends on the amount of remaining memory available to the server, because when a transaction is executed, the memory usage of the TiDB process is approximately six times the size of the transaction.

Before v4.0, TiDB restricts the total number of key-value pairs for a single transaction to no more than 300,000. This limitation is removed since v4.0.

> **Note:**
>
> Usually, TiDB Binlog is enabled to replicate data to the downstream. In some scenarios, message middleware such as Kafka is used to consume binlogs that are replicated to the downstream.
>
> Taking Kafka as an example, the upper limit of Kafka's single message processing capability is 1 GB. Therefore, when `txn-total-size-limit` is set to more than 1 GB, it might happen that the transaction is successfully executed in TiDB, but the downstream Kafka reports an error. To avoid this situation, you need to decide the actual value of `txn-total-size-limit` according to the limit of the end consumer. For example, if Kafka is used downstream, `txn-total-size-limit` must not exceed 1 GB.
