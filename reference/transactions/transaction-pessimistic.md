---
title: TiDB Pessimistic Transaction Model
summary: Learn the pessimistic transaction model in TiDB.
category: reference
---

# TiDB Pessimistic Transaction Model

In versions before 3.0.8, TiDB implements the optimistic transaction mode by default, in which the transaction commit might fail because of transaction conflict. To make sure that the commit succeeds, you need to modify the application and add an automatic retry mechanism. You can avoid this issue by using the pessimistic transaction mode of TiDB.

## Usage

To apply the pessimistic transaction mode, choose any of the following three methods that suits your needs:

- Execute the `BEGIN PESSIMISTIC;` statement to allow the transaction to apply the pessimistic transaction mode. You can write it in comment style as `BEGIN /*!90000 PESSIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute the `set @@tidb_txn_mode = 'pessimistic';` statement to allow all the explicit transactions (namely non-autocommit transactions) processed in this session to apply the pessimistic transaction mode.

- Execute the `set @@global.tidb_txn_mode = 'pessimistic';` statement to allow all newly created sessions of the entire cluster to apply the pessimistic transaction mode to execute explicit transactions.

After you set `global.tidb_txn_mode` to `pessimistic`, the pessimistic transaction mode is applied by default. To apply the optimistic transaction mode to the transaction, you can use any of the following three methods:

- Execute the `BEGIN OPTIMISTIC;` statement to allow the transaction to apply the optimistic transaction mode. You can write it in comment style as `BEGIN /*!90000 OPTIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute the `set @@tidb_txn_mode = 'optimistic';` statement to allow all the transactions processed in this session to apply the optimistic transaction mode.

- Execute the `set @@global.tidb_txn_mode = 'optimistic;'` or `set @@global.tidb_txn_mode = '';` to allow all newly created sessions of the entire cluster to apply the optimistic transaction mode to the transactions.

The `BEGIN PESSIMISTIC;` and `BEGIN OPTIMISTIC;` statements take precedence over the `tidb_txn_mode` system variable. Transactions started with these two statements ignore the system variable and support using both the pessimistic and optimistic transaction modes.

To disable the pessimistic transaction mode, modify the configuration file and add `enable = false` to the `[pessimistic-txn]` category.

## Behaviors

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Difference with MySQL InnoDB](#difference-with-mysql-innoDB).

- When you perform the `SELECT FOR UPDATE` statement, transactions read the last committed data and apply a pessimistic lock on the data being read.

- When you perform the `UPDATE`, `DELETE` or `INSERT` statement, transactions read the last committed data to execute on them and apply a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- When multiple transactions wait for the same lock to be released, the lock is acquired in the order of the `start ts` of the transactions as much as possible; however, the order cannot be strictly guaranteed.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. The detector randomly terminates one of the transactions, and a MySQL-compatible error code `1213` is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster. You can specify either mode for transaction execution.

- TiDB sets the lock wait timeout time by the `innodb_lock_wait_timeout` variable. After the lock times out, a MySQL-compatible error code `1205` is returned.

- TiDB supports the `FOR UPDATE NOWAIT` syntax and does not block and wait for locks to be released. Instead, a MySQL-compatible error code `3572` is returned.

## Difference with MySQL InnoDB

1. When TiDB executes DML or `SELECT FOR UPDATE` statements that use range in the WHERE clause, the concurrent `INSERT` statements within the range are not blocked.

    By implementing Gap Lock, InnoDB blocks the execution of concurrent `INSERT` statements within the range. It is mainly used to support statement-based binlog. Therefore, some applications lower the isolation level to READ COMMITTED to avoid concurrency performance problems caused by Gap Lock. TiDB does not support Gap Lock, so there is no need to pay the concurrency performance cost.

2. TiDB does not support `SELECT LOCK IN SHARE MODE`.

    When `SELECT LOCK IN SHARE MODE` is executed, it has the same effect as that without the lock, so the read or write operation of other transactions is not blocked.

3. DDL may result in failure of the pessimistic transaction commit.

    When DDL is executed in MySQL, it might be blocked by the transaction that is being executed. However, in this scenario, the DDL operation is not blocked in TiDB, which leads to failure of the pessimistic transaction commit: `ERROR 1105 (HY000): Information schema is changed. [try again later]`.

4. After executing `START TRANSACTION WITH CONSISTENT SNAPSHOT`, MySQL can still read the tables that are created later in other transactions, while TiDB cannot.

5. The autocommit transactions do not support the pessimistic locking.

    None of the autocommit statements acquire the pessimistic lock. These statements do not display any difference in the user side, because the nature of pessimistic transactions is to turn the retry of the whole transaction into a single DML retry. The autocommit transactions automatically retry even when TiDB closes the retry, which has the same effect as pessimistic transactions.

    The autocommit `SELECT FOR UPDATE` statement does not wait for lock, either.

## FAQ

1. The TiDB log shows `pessimistic write conflict, retry statement`.

    When a write conflict occurs, the optimistic transaction is terminated directly, but the pessimistic transaction retries the statement with the latest data until there is no write conflict. The log prints this entry with each retry, so there is no need for extra attention.

2. When DML is executed, an error `pessimistic lock retry limit reached` is returned.

    In the pessimistic transaction mode, every statement has a retry limit. This error is returned when the retry times of write conflict exceeds the limit. The default retry limit is `256`. To change the limit, modify the `max-retry-limit` under the `[pessimistic-txn]` category in the TiDB configuration file.

3. The execution time limit for pessimistic transactions.

    The execution time of transactions cannot exceed the limit of `tikv_gc_life_time`. In addition, the pessimistic transactions have a TTL (Time to Live) limit of 10 minutes, so the pessimistic transactions that execute over 10 minutes might fail to commit.
