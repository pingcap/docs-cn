---
title: TiDB Pessimistic Transaction Model
summary: Learn the pessimistic transaction model in TiDB.
aliases: ['/docs/dev/pessimistic-transaction/','/docs/dev/reference/transactions/transaction-pessimistic/']
---

# TiDB Pessimistic Transaction Model

To make the usage of TiDB closer to traditional databases and reduce the cost of migration, starting from v3.0, TiDB supports the pessimistic transaction model on top of the optimistic transaction model. This document describes the features of the TiDB pessimistic transaction model.

> **Note:**
>
> Starting from v3.0.8, newly created TiDB clusters use the pessimistic transaction model by default. However, this does not affect your existing cluster if you upgrade it from v3.0.7 or earlier to v3.0.8 or later. In other words, **only newly created clusters default to using the pessimistic transaction model**.

## Switch transaction mode

You can set the transaction mode by configuring the [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode) system variable. The following command sets all explicit transactions (that is, non-autocommit transactions) executed by newly created sessions in the cluster to the pessimistic transaction mode:

{{< copyable "sql" >}}

```sql
set @@global.tidb_txn_mode = 'pessimistic';
```

You can also explicitly enable the pessimistic transaction mode by executing the following SQL statements:

{{< copyable "sql" >}}

```sql
BEGIN PESSIMISTIC;
```

{{< copyable "sql" >}}

```sql
BEGIN /*!90000 PESSIMISTIC */;
```

The `BEGIN PESSIMISTIC;` and `BEGIN OPTIMISTIC;` statements take precedence over the `tidb_txn_mode` system variable. Transactions started with these two statements ignore the system variable and support using both the pessimistic and optimistic transaction modes.

## Behaviors

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Difference with MySQL InnoDB](#difference-with-mysql-innodb).

- When you perform the `SELECT FOR UPDATE` statement, transactions read the **lastest** committed data and apply a pessimistic lock on the data being read.

- When you perform the `UPDATE`, `DELETE` or `INSERT` statement, transactions read the **lastest** committed data to execute on them and apply a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- When multiple transactions wait for the same lock to be released, the lock is acquired in the order of the `start ts` of the transactions as much as possible; however, the order cannot be strictly guaranteed.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. The detector randomly terminates one of the transactions, and a MySQL-compatible error code `1213` is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster. You can specify either mode for transaction execution.

- TiDB sets the lock wait timeout time by the `innodb_lock_wait_timeout` variable. After the lock times out, a MySQL-compatible error code `1205` is returned.

- TiDB supports the `FOR UPDATE NOWAIT` syntax and does not block and wait for locks to be released. Instead, a MySQL-compatible error code `3572` is returned.

- If the `Point Get` and `Batch Point Get` operators do not read data, they still locks the given primary key or unique key, which blocks other transactions from locking or writing data to the same primary key or unique key.

## Difference with MySQL InnoDB

1. When TiDB executes DML or `SELECT FOR UPDATE` statements that use range in the WHERE clause, the concurrent `INSERT` statements within the range are not blocked.

    By implementing Gap Lock, InnoDB blocks the execution of concurrent `INSERT` statements within the range. It is mainly used to support statement-based binlog. Therefore, some applications lower the isolation level to Read Committed to avoid concurrency performance problems caused by Gap Lock. TiDB does not support Gap Lock, so there is no need to pay the concurrency performance cost.

2. TiDB does not support `SELECT LOCK IN SHARE MODE`.

    When `SELECT LOCK IN SHARE MODE` is executed, it has the same effect as that without the lock, so the read or write operation of other transactions is not blocked.

3. DDL may result in failure of the pessimistic transaction commit.

    When DDL is executed in MySQL, it might be blocked by the transaction that is being executed. However, in this scenario, the DDL operation is not blocked in TiDB, which leads to failure of the pessimistic transaction commit: `ERROR 1105 (HY000): Information schema is changed. [try again later]`. TiDB executes the `TRUNCATE TABLE` statement during the transaction execution, which might result in the `table dosen't exist` error.

4. After executing `START TRANSACTION WITH CONSISTENT SNAPSHOT`, MySQL can still read the tables that are created later in other transactions, while TiDB cannot.

5. The autocommit transactions do not support the pessimistic locking.

    None of the autocommit statements acquire the pessimistic lock. These statements do not display any difference in the user side, because the nature of pessimistic transactions is to turn the retry of the whole transaction into a single DML retry. The autocommit transactions automatically retry even when TiDB closes the retry, which has the same effect as pessimistic transactions.

    The autocommit `SELECT FOR UPDATE` statement does not wait for lock, either.

6. The data read by `EMBEDDED SELECT` in the statement is not locked.

## Isolation level

TiDB supports the following two isolation levels in the pessimistic transaction mode:

- [Repeatable Read](/transaction-isolation-levels.md#repeatable-read-isolation-level) by default, which is the same as MySQL.

    > **Note:**
    >
    > In this isolation level, DML operations are performed based on the latest committed data. The behavior is the same as MySQL, but differs from the optimistic transaction mode in TiDB. See [Difference between TiDB and MySQL Repeatable Read](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read).

- [Read Committed](/transaction-isolation-levels.md#read-committed-isolation-level). You can set this isolation level using the [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) statement.

## Pipelined locking process

Adding a pessimistic lock requires writing data into TiKV. The response of successfully adding a lock can only be returned to TiDB after commit and apply through Raft. Therefore, compared with optimistic transactions, the pessimistic transaction mode inevitably has higher latency.

To reduce the overhead of locking, TiKV implements the pipelined locking process: when the data meets the requirements for locking, TiKV immediately notifies TiDB to execute subsequent requests and writes into the pessimistic lock asynchronously. This process reduces most latency and significantly improves the performance of pessimistic transactions. However, there is a low probability that the asynchronous write into the pessimistic lock might fail, resulting in the commit failure of the pessimistic transaction.

![Pipelined pessimistic lock](/media/pessimistic-transaction-pipelining.png)

This feature is disabled by default. To enable it, modify the TiKV configuration:

```toml
[pessimistic-txn]
pipelined = true
```

## FAQ

1. The TiDB log shows `pessimistic write conflict, retry statement`.

    When a write conflict occurs, the optimistic transaction is terminated directly, but the pessimistic transaction retries the statement with the latest data until there is no write conflict. The log prints this entry with each retry, so there is no need for extra attention.

2. When DML is executed, an error `pessimistic lock retry limit reached` is returned.

    In the pessimistic transaction mode, every statement has a retry limit. This error is returned when the retry times of write conflict exceeds the limit. The default retry limit is `256`. To change the limit, modify the `max-retry-limit` under the `[pessimistic-txn]` category in the TiDB configuration file.

3. The execution time limit for pessimistic transactions.

    In TiDB 4.0, garbage collection (GC) does not affect the running transactions, but the execution time of pessimistic transactions cannot exceed 10 minutes by default. You can modify this limit by editing `max-txn-ttl` under `[performance]` in the TiDB configuration file.
