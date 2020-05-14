---
title: TiDB Optimistic Transaction Model
summary: Learn the optimistic transaction model in TiDB.
category: reference
aliases: ['/docs/dev/reference/transactions/transaction-model/']
---

# TiDB Optimistic Transaction Model

This document introduces the principles of TiDB's optimistic transaction model. This document assumes that you have a basic understanding of [TiDB architecture](/architecture.md), [Percolator](https://ai.google/research/pubs/pub36726), and the [ACID](/glossary.md#acid) properties of transactions.

In TiDB's optimistic transaction model, the two-phase commit begins right after the client executes the `COMMIT` statement. Therefore, the write-write conflict can be observed before the transactions are actually committed.

> **Note:**
>
> Starting from v3.0.8, TiDB uses the [pessimistic transaction model](/pessimistic-transaction.md) by default. However, this does not affect your clusters if you upgrading from v3.0.7 or earlier to v3.0.8 (and later). In other words, **only newly created clusters default to using the pessimistic transaction model**.

## Principles of optimistic transactions

TiDB adopts Google's Percolator transaction model, a variant of two-phase commit (2PC) to ensure the correct completion of a distributed transaction. The procedure is as follows:

![2PC in TiDB](/media/2pc-in-tidb.png)

1. The client begins a transaction.

    TiDB receives the start version number (monotonically increasing in time and globally unique) from PD and mark it as `start_ts`.

2. The client issues a read request.
    1. TiDB receives routing information (how data is distributed among TiKV nodes) from PD.
    2. TiDB receives the data of the `start_ts` version from TiKV.

3. The client issues a write request.

    TiDB checks whether the written data satisfies consistency constraints (to ensure the data types are correct and the unique index is met etc.) **Valid data is stored in the memory**.

4. The client issues a commit request.

5. TiDB begins 2PC to ensure the atomicity of distributed transactions and persist data in store.

    1. TiDB selects a Primary Key from the data to be written.
    2. TiDB receives the information of Region distribution from PD, and groups all keys by Region accordingly.
    3. TiDB sends prewrite requests to all TiKV nodes involved. Then, TiKV checks whether there are conflict or expired versions. Valid data is locked.
    4. TiDB receives all requests in the prewrite phase and the prewrite is successful.
    5. TiDB receives a commit version number from PD and marks it as `commit_ts`.
    6. TiDB initiates the second commit to the TiKV node where Primary Key is located. TiKV checks the data, and clean the locks left in the prewrite phase.
    7. TiDB receives the message that reports the second phase is successfully finished.

6. TiDB returns a message to inform the client that the transaction is successfully committed.

7. TiDB asynchronously cleans the locks left in this transaction.

## Advantages and disadvantages

From the process of transactions in TiDB above, it is clear that TiDB transactions have the following advantages:

* Simple to understand
* Implement cross-node transaction based on single-row transaction
* Decentralized lock management

However, TiDB transactions also have the following disadvantages:

* Transaction latency due to 2PC
* In need of a centralized version manager
* OOM (out of memory) when extensive data is written in the memory

To avoid potential problems in application, refer to [transaction sizes](/transaction-overview.md#transaction-size) to see more details.

## Transaction retries

TiDB uses optimistic concurrency control by default whereas MySQL applies pessimistic concurrency control. This means that MySQL checks for conflicts during the execution of SQL statements, so there are few errors reported in heavy contention scenarios. For the convenience of MySQL users, TiDB provides a retry function that runs inside a transaction.

### Automatic retry

If there is a conflict, TiDB retries the write operations automatically. You can set `tidb_disable_txn_auto_retry` and `tidb_retry_limit` to enable or disable this default function:

```toml
# Whether to disable automatic retry. ("on" by default)
tidb_disable_txn_auto_retry = off
# Set the maximum number of the retires. ("10" by default)
# When “tidb_retry_limit = 0”, automatic retry is completely disabled.
tidb_retry_limit = 10
```

You can enable the automatic retry in either session level or global level:

1. Session level:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_disable_txn_auto_retry = off;
    ```

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_retry_limit = 10;
    ```

2. Global level:

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_disable_txn_auto_retry = off;
    ```

    {{< copyable "sql" >}}

    ```sql
    set @@global.tidb_retry_limit = 10;
    ```

> **Note:**
>
> The `tidb_retry_limit` variable decides the maximum number of retries. When this variable is set to `0`, none of the transactions automatically retries, including the implicit single statement transactions that are automatically committed. This is the way to completely disable the automatic retry mechanism in TiDB. After the automatic retry is disabled, all conflicting transactions report failures (includes the `try again later` string) to the application layer in the fastest way.

### Limits of retry

By default, TiDB will not retry transactions because this might lead to lost updates and damaged [`REPEATABLE READ` isolation](/transaction-isolation-levels.md).

The reason can be observed from the procedures of retry:

1. Allocate a new timestamp and mark it as `start_ts`.
2. Retry the SQL statements that contain write operations.
3. Implement the two-phase commit.

In Step 2, TiDB only retries SQL statements that contain write operations. However, during retrying, TiDB receives a new version number to mark the beginning of the transaction. This means that TiDB retries SQL statements with the data in the new `start_ts` version. In this case, if the transaction updates data using other query results, the results might be inconsistent because the `REPEATABLE READ` isolation is violated.

If your application can tolerate lost updates, and does not require `REPEATABLE READ` isolation consistency, you can enable this feature by setting `tidb_disable_txn_auto_retry = off`.

## Conflict detection

For the optimistic transaction, it is important to detect whether there are write-write conflicts in the underlying data. Although TiKV reads data for detection **in the prewrite phase**, a conflict pre-detection is also performed in the TiDB clusters to improve the efficiency.

Because TiDB is a distributed database, the conflict detection in the memory is performed in two layers:

* The TiDB layer. If a write-write conflict in the instance is observed after the primary write is issued, it is unnecessary to issue the subsequent writes to the TiKV layer.
* The TiKV layer. TiDB instances are unaware of each other, which means they cannot confirm whether there are conflicts or not. Therefore, the conflict detection is mainly performed in the TiKV layer.

The conflict detection in the TiDB layer is disabled by default. The specific configuration items are as follows:

```toml
[txn-local-latches]
# Whether to enable the latches for transactions. Recommended
# to use latches when there are many local transaction conflicts.
# ("false" by default)
enabled = false
# Controls the number of slots corresponding to Hash. ("204800" by default)
# It automatically adjusts upward to an exponential multiple of 2.
# Each slot occupies 32 Bytes of memory. If set too small,
# it might result in slower running speed and poor performance
# when data writing covers a relatively large range.
capacity = 2048000
```

The value of the `capacity` configuration item mainly affects the accuracy of conflict detection. During conflict detection, only the hash value of each key is stored in the memory. Because the probability of collision when hashing is closely related to the probability of misdetection, you can configure `capacity` to controls the number of slots and enhance the accuracy of conflict detection.

* The smaller the value of `capacity`, the smaller the occupied memory and the greater the probability of misdetection.
* The larger the value of `capacity`, the larger the occupied memory and the smaller the probability of misdetection.

When you confirm that there is no write-write conflict in the upcoming transactions (such as importing data), it is recommended to disable the function of conflict detection.

TiKV also uses a similar mechanism to detect conflicts, but the conflict detection in the TiKV layer cannot be disabled. You can only configure `scheduler-concurrency` to control the number of slots that defined by the modulo operation:

```toml
# Controls the number of slots. ("2048000" by default）
scheduler-concurrency = 2048000
```

In addition, TiKV supports monitoring the time spent on waiting latches in scheduler.

![Scheduler latch wait duration](/media/optimistic-transaction-metric.png)

When `Scheduler latch wait duration` is high and there is no slow writes, it can be safely concluded that there are many write conflicts at this time.
