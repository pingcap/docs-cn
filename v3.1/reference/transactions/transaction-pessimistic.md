---
title: TiDB Pessimistic Transaction Mode
summary: Learn about the pessimistic transaction mode of TiDB.
category: reference
---

# TiDB Pessimistic Transaction Mode

By default, TiDB implements the optimistic transaction mode, where the transaction commit might fail because of transaction conflicts. To make sure that the commit succeeds, you need to modify the application and add an automatic retry mechanism. You can avoid this issue by using the pessimistic transaction mode of TiDB.

## Behaviors of the pessimistic transaction mode

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Difference with MySQL InnoDB](#difference-with-mysql-innoDB).

- When you perform the `SELECT FOR UPDATE` statement, transactions read the last committed data and apply a pessimistic lock on the data being read.

- When you perform the `UPDATE`, `DELETE` or `INSERT` statement, transactions read the last committed data to execute on them and apply a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. A MySQL-compatible error code `1213` is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster. You can specify either mode for transaction execution.

- TiDB sets the lock wait timeout time by the `innodb_wait_timeout` variable. After the lock times out, a MySQL-compatible error code `1205` is returned.

- TiDB supports the `FOR UPDATE NOWAIT` syntax and does not block and wait for locks to be released. Instead, a MySQL-compatible error code `3572` is returned.

## Usage of pessimistic transaction mode

To apply the pessimistic transaction mode, choose any of the following three methods that suits your needs:

- Execute the `BEGIN PESSIMISTIC;` statement to allow the transaction to apply the pessimistic transaction mode. You can write it in comment style as `BEGIN /*!90000 PESSIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute the `set @@tidb_txn_mode = 'pessimistic';` statement to allow all the explicit transactions (namely non-autocommit transactions) processed in this session to apply the pessimistic transaction mode.

- Execute the `set @@global.tidb_txn_mode = 'pessimistic';` statement to allow all newly created sessions of the entire cluster to apply the pessimistic transaction mode to execute explicit transactions.

After you set `global.tidb_txn_mode` to `pessimistic`, the pessimistic transaction mode is applied by default; but you can use either of the following two methods to apply the optimistic transaction mode for the transaction:

- Execute the `BEGIN OPTIMISTIC;` statement to allow the transaction to apply the optimistic transaction mode. You can write it in comment style as `BEGIN /*!90000 OPTIMISTIC */;` to make it compatible with the MySQL syntax.

- Execute the `set @@tidb_txn_mode = 'optimistic';` statement to allow all the transactions processed in this session to apply the optimistic transaction mode.

The `BEGIN PESSIMISTIC;` and `BEGIN OPTIMISTIC;` statements take precedence over the `tidb_txn_mode` system variable. Transactions that are started with these two statements will ignore system variables.

To disable the pessimistic transaction mode, modify the configuration file and add `enable = false` to the `[pessimistic-txn]` category.

## Difference with MySQL InnoDB

1. When TiDB executing DML or `SELECT FOR UPDATE` statements that use range in the WHERE clause, the concurrent `INSERT` statements within the range are not blocked.

    By implementing Gap Lock, InnoDB blocks the execution of concurrent `INSERT` statements within the range. It is mainly used to support statement-based binlog. Therefore, some applications set the isolation level to READ COMMITTED to avoid concurrency performance problems caused by Gap Lock. TiDB does not support Gap Lock, so there is no need to pay the concurrency performance cost.

2. TiDB does not support `SELECT LOCK IN SHARE MODE`.

    When `SELECT LOCK IN SHARE MODE` is specified in a statement, it has the same effect as that without the lock, so the read or write of other transactions is not blocked.