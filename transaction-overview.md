---
title: Transactions
summary: Learn transactions in TiDB.
category: reference
aliases: ['/docs/dev/reference/transactions/overview/']
---

# Transactions

TiDB supports complete distributed transactions. Both [optimistic transaction model](/optimistic-transaction.md) and [pessimistic transaction model](/pessimistic-transaction.md)(introduced in TiDB 3.0) are available. This document introduces transaction-related statements, explicit and implicit transactions, isolation levels, lazy check for constraints, and transaction sizes.

The common variables include [`autocommit`](#autocommit), [`tidb_disable_txn_auto_retry`](/tidb-specific-system-variables.md#tidb_disable_txn_auto_retry), and [`tidb_retry_limit`](/tidb-specific-system-variables.md#tidb_retry_limit).

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

## Transaction isolation level

TiDB **only supports** `SNAPSHOT ISOLATION`. You can set the isolation level of the current session to `READ COMMITTED` using the following statement. However, TiDB is only compatible with the `READ COMMITTED` isolation level in syntax and transactions are still executed at the `SNAPSHOT ISOLATION` level.

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Lazy check of constraints

**Lazy check** means that by default TiDB will not check [primary key](/constraints.md#primary-key) or [unique constraints](/constraints.md#unique) when an `INSERT` statement is executed, but instead checks when the transaction is committed. In TiDB, the lazy check is performed for values written by ordinary `INSERT` statements.

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
> This optimization does not take effect for `INSERT IGNORE` and `INSERT ON DUPLICATE KEY UPDATE`, only for normal `INSERT` statements. The behavior can also be disabled by setting `tidb_constraint_check_in_place=TRUE`.

## Statement rollback

If you execute a statement within a transaction, the statement does not take effect when an error occurs.

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

## Transaction sizes

In TiDB, a transaction either too small or too large can impair the overall performance.

### Small transactions

TiDB uses the default autocommit setting (that is, `autocommit = 1`), which automatically issues a commit when executing each SQL statement. Therefore, each of the following three statements is treated as a transaction:

```sql
UPDATE my_table SET a = 'new_value' WHERE id = 1;
UPDATE my_table SET a = 'newer_value' WHERE id = 2;
UPDATE my_table SET a = 'newest_value' WHERE id = 3;
```

In this case, the latency is increased because each statement, as a transaction, uses the two-phase commit which consumes more execution time.

To improve the execution efficiency, you can use an explicit transaction instead, that is, to execute the above three statements within a transaction:

```sql
START TRANSACTION;
UPDATE my_table SET a = 'new_value' WHERE id = 1;
UPDATE my_table SET a = 'newer_value' WHERE id = 2;
UPDATE my_table SET a = 'newest_value' WHERE id = 3;
COMMIT;
```

Similarly, it is recommended to execute `INSERT` statements within an explicit transaction.

> **Note:**
>
> The single-threaded workloads in TiDB might not fully use TiDB's distributed resources, so the performance of TiDB is lower than that of a single-instance deployment of MySQL. This difference is similar to the case of transactions with higher latency in TiDB.

### Large transaction

Due to the requirement of the two-phase commit, a large transaction can lead to the following issues:

* OOM (Out of Memory) when excessive data is written in the memory
* More conflicts in the prewrite phase
* Long duration before transactions are actually committed

Therefore, TiDB intentionally imposes some limits on transaction sizes:

* The total number of SQL statements in a transaction is no more than 5,000 (default)
* Each key-value pair is no more than 6 MB

For each transaction, it is recommended to keep the number of SQL statements between 100 to 500 to achieve an optimal performance.

TiDB sets a default limit of 100 MB for the total size of key-value pairs, which can be modified by the `txn-total-size-limit` configuration item in the configuration file. The maximum value of `txn-total-size-limit` is 10 GB. The actual size limit of one transaction also depends on the memory capacity. When executing large transactions, the memory usage of the TiDB process is approximately 6 times larger than the total size of transactions.

In versions earlier than 4.0, TiDB limits the total number of key-value pairs for a single transaction to no more than 300,000. This limitation is removed since v4.0.
