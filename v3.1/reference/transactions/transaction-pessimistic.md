---
title: TiDB Pessimistic Transaction Mode
summary: Learn about the pessimistic transaction mode of TiDB.
category: reference
---

# TiDB Pessimistic Transaction Mode

By default, TiDB implements the optimistic transaction mode, where the transaction commit might fail because of transaction conflicts. To make sure that the commit succeeds, you need to modify the application and add an automatic retry mechanism. You can avoid this issue by using the pessimistic transaction mode of TiDB.

## Behaviors of the pessimistic transaction mode

Pessimistic transactions in TiDB behave similarly to those in MySQL. See the minor differences in [Known restrictions](#known-restrictions).

- When you perform the `SELECT FOR UPDATE` statement, transactions read the last committed data and apply a pessimistic lock on the data being read.

- When you perform the `UPDATE/DELETE/INSERT` statement, transactions read the last committed data to execute on them and apply a pessimistic lock on the modified data.

- When a pessimistic lock is applied on a row of data, other write transactions attempting to modify the data are blocked and have to wait for the lock to be released.

- When a pessimistic lock is applied on a row of data, other transactions attempting to read the data are not blocked and can read the committed data.

- All the locks are released when the transaction is committed or rolled back.

- Deadlocks in concurrent transactions can be detected by the deadlock detector. A DEADLOCK error which is the same as that in MySQL is returned.

- TiDB supports both the optimistic transaction mode and pessimistic transaction mode in the same cluster. You can specify either mode for transaction execution.

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

## Configuration parameter

The related configuration parameters are under the `[pessimistic-txn]` category. Besides `enable`, you can also configure the following parameters:

- `ttl`

    ```
    ttl = "40s"
    ```

    `ttl` is the timeout for pessimistic transaction locking. Its default value is "40s" (40 seconds). You must set it to a value between 15~120 seconds, and a value out of this range can result in an error.

    A transaction fails when its execution time exceeds `ttl`. If the value of `ttl` is set too high, the remaining pessimistic lock might block the write transaction for a long time when `tidb-server` is down. If set too low, the transaction might be rolled back by other transactions before it can finish execution.

- `max-retry-count`

    ```
    max-retry-count = 256
    ```

    A pessimistic transaction can automatically retry a single statement. You can specify the maximum retrying times by setting the `max-retry-count` parameter to avoid retrying a statement endlessly in some extreme cases. Normally, you do not need to modify this configuration.

## Known restrictions

- TiDB does not support GAP Lock or Next Key Lock. When multiple rows of data are updated through range conditions in a pessimistic transaction, other transactions can insert data without being blocked in this range.

- TiDB does not support `SELECT LOCK IN SHARE MODE`.
