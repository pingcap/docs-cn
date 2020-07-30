---
title: Troubleshoot Lock Conflicts
summary: Learn to analyze and resolve lock conflicts in TiDB.
---

# Troubleshoot Lock Conflicts
 
TiDB supports complete distributed transactions. Starting from v3.0, TiDB provides optimistic transaction mode and pessimistic transaction mode. This document introduces how to troubleshoot and resolve lock conflicts in TiDB.

## Optimistic transaction mode

Transactions in TiDB use two-phase commit (2PC) that includes the Prewrite phase and the Commit phase. The procedure is as follows:

![two-phase commit in the optimistic transaction mode](/media/troubleshooting-lock-pic-01.png)
 
For details of Percolator and TiDB's algorithm of the transactions, see [Google's Percolator](https://ai.google/research/pubs/pub36726).

### Prewrite phase (optimistic)
 
In the Prewrite phase, TiDB adds a primary lock and a secondary lock to target keys. If there are lots of requests for adding locks to the same target key, TiDB prints an error such as write conflict or `keyislocked` to the log and reports it to the client. Specifically, the following errors related to locks might occur in the Prewrite phase.
 
#### Read-write conflict (optimistic)
 
As the TiDB server receives a read request from a client, it gets a globally unique and increasing timestamp at the physical time as the start_ts of the current transaction. The transaction needs to read the latest data before start_ts, that is, the target key of the latest commit_ts that is smaller than start_ts. When the transaction finds that the target key is locked by another transaction, and it cannot know which phase the other transaction is in, a read-write conflict happens. The diagram is as follows:

![read-write conflict](/media/troubleshooting-lock-pic-04.png)

Txn0 completes the Prewrite phase and enters the Commit phase. At this time, Txn1 requests to read the same target key. Txn1 needs to read the target key of the latest commit_ts that is smaller than its start_ts. Because Txn1’s start_ts is larger than Txn0's lock_ts, Txn1 must wait for the target key's lock to be cleared, but it hasn’t been done. As a result, Txn1 cannot confirm whether Txn0 has been committed or not. Thus, a read-write conflict between Txn1 and Txn0 happens.

You can detect the read-write conflict in your TiDB cluster by the following ways:

1. Monitoring metrics and logs of the TiDB server

    * Monitoring data through Grafana

        On the `KV Errors` panel in the TiDB dashboard, there are two monitoring metrics `Lock Resolve OPS` and `KV Backoff OPS` which can be used to check read-write conflicts in the transactions. If the values of both `not_expired` and `resolve` under `Lock Resolve OPS` increase, there might be many read-write conflicts. The `not_expired` item means that the transaction's lock has not timed out. The `resolve` item means that the other transaction tries to clean up the locks. If the value of another `txnLockFast` item under `KV Backoff OPS` increases, there might also be read-write conflicts.

        ![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png)
        ![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png)

    * Logs of the TiDB server

        If there is any read-write conflict, you can see the following message in the TiDB log:

        ```log
        [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
        ```

        * txnStartTS: The start_ts of the transaction that is sending the read request. In the above log, `416643508703592451` is the start_ts.
        * backoff_types: If a read-write conflict happens, and the read request performs backoff and retry, the type of retry is `TxnLockFast`.
        * backoff_ms: The time that the read request spends in the backoff and retry, and the unit is milliseconds. In the above log, the read request spends 255 milliseconds in the backoff and retry.
        * region_id: Region ID corresponding to the target key of the read request.

2. Logs of the TiKV server

    If there is any read-write conflict, you can see the following message in the TiKV log:

    ```log
    [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
    ```

    This message indicates that a read-write conflict occurs in TiDB. The target key of the read request has been locked by another transaction. The locks are from the uncommitted optimistic transaction and the uncommitted pessimistic transaction after the prewrite phase.

    * primary_lock：Indicates that the target key is locked by the primary lock.
    * lock_version：The start_ts of the transaction that owns the lock.
    * key：The target key that is locked.
    * lock_ttl: The lock’s TTL (Time To Live)
    * txn_size：The number of keys that are in the Region of the transaction that owns the lock.

Solutions:

* A read-write conflict triggers an automatic backoff and retry. As in the above example, Txn1 has a backoff and retry. The first time of the retry is 100 ms, the longest retry is 3000 ms, and the total time is 20000 ms at maximum.

* You can use the sub-command [`decoder`](/tidb-control.md#the-decoder-command) of TiDB Control to view the table id and rowid of the row corresponding to the specified key:

    ```sh
    ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

#### KeyIsLocked error

In the Prewrite phase of a transaction, TiDB checks whether there is any write-write conflict, and then checks whether the target key has been locked by another transaction. If the key is locked, the TiKV server outputs a "KeyIsLocked" error. At present, the error message is not printed in the logs of TiDB and TiKV. Same as read-write conflicts, when "KeyIsLocked" occurs, TiDB automatically performs backoff and retry for the transaction.

You can check whether there's any "KeyIsLocked" error in the TiDB monitoring on Grafana:

The `KV Errors` panel in the TiDB dashboard has two monitoring metrics `Lock Resolve OPS` and `KV Backoff OPS` which can be used to check write-write conflicts caused by a transaction. If the `resolve` item under `Lock Resolve OPS` and the `txnLock` item under `KV Backoff OPS` have a clear upward trend, a "KeyIsLocked" error occurs. `resolve` refers to the operation that attempts to clear the lock, and `txnLock` represents a write conflict.

![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png)
![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png)

Solutions:

* If there is a small amount of txnLock in the monitoring, no need to pay too much attention. The backoff and retry is automatically performed in the background. The first time of the retry is 200 ms and the maximum time is 3000 ms for a single retry.
* If there are too many “txnLock” operations in the `KV Backoff OPS`, it is recommended that you analyze the reasons to the write conflicts from the application side.
* If your application is a write-write conflict scenario, it is strongly recommended to use the pessimistic transaction mode.

### Commit phase (optimistic)

After the Prewrite phase completes, the client obtains commit_ts, and then the transaction is going to the next phase of 2PC - the Commit phase.

#### LockNotFound error

The error log of "TxnLockNotFound" means that transaction commit time is longer than the the TTL time, and when the transaction is going to commit, its lock has been rolled back by other transactions. If the TiDB server enables transaction commit retry, this transaction is re-executed according to [tidb_retry_limit](/system-variables.md#tidb_retry_limit). (Note about the difference between explicit and implicit transactions.)

You can check whether there is any "LockNotFound" error in the following ways:

1. View the logs of the TiDB server

    If a "TxnLockNotFound" error occurs, the TiDB log message is like this:

    ```log
    [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
    ```

    * start_ts: The start_ts of the transaction that outputs the `TxnLockNotFound` error because its lock has been rolled back by other transactions. In the above log, `412720515987275779` is the start_ts.
    * commit_ts: The commit_ts of the transaction that outputs the `TxnLockNotFound` error. In the above log, `412720519984971777` is the commit_ts.

2. View the logs of the TiKV server

    If a "TxnLockNotFound" error occurs, the TiKV log message is like this:

    ```log
    Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
    ```
 
Solutions:

* By checking the time interval between start_ts and commit_ts, you can confirm whether the commit time exceeds the TTL time.

    Checking the time interval using the PD control tool:

    ```shell
    ./pd-ctl tso [start_ts]
    ./pd-ctl tso [commit_ts]
    ```

* It is recommended to check whether the write performance is slow, which might cause that the efficiency of transaction commit is poor, and thus the lock is cleared.

* In the case of disabling the TiDB transaction retry, you need to catch the exception on the application side and try again.

## Pessimistic transaction mode

Before v3.0.8, TiDB uses the optimistic transaction mode by default. In this mode, if there is a transaction conflict, the latest transaction will fail to commit. Therefore, the application needs to support retrying transactions. The pessimistic transaction mode resolves this issue, and the application does not need to modify any logic for the workaround.

The commit phase of the pessimistic transaction mode and the optimistic transaction mode in TiDB has the same logic, and both commits are in the 2PC mode. The important adaptation of pessimistic transactions is DML execution.

![TiDB pessimistic transaction commit logic](/media/troubleshooting-lock-pic-05.png)
 
The pessimistic transaction adds an `Acquire Pessimistic Lock` phase before 2PC. This phase includes the following steps:

1. (same as the optimistic transaction mode) Receive the `begin` request from the client, and the current timestamp is this transaction’s start_ts.
2. When the TiDB server receives an `update` request from the client, the TiDB server initiates a pessimistic lock request to the TiKV server, and the lock is persisted to the TiKV server.
3. (same as the optimistic transaction mode) When the client sends the commit request, TiDB starts to perform the 2PC similar to the optimistic transaction mode. 

![Pessimistic transactions in TiDB](/media/troubleshooting-lock-pic-06.png)

For details, see [Pessimistic transaction mode](/pessimistic-transaction.md).

### Prewrite phase (pessimistic)

In the transaction pessimistic mode, the commit phase is the same as the 2PC. Therefore, the read-write conflict also exists as in the optimistic transaction mode.

#### Read-write conflict (pessimistic)

Same as [Read-write conflict (optimistic)](#read-write-conflict-optimistic).

### Commit phase (pessimistic)

In the pessimistic transaction mode, there will be no `TxnLockNotFound` error. Instead, the pessimistic lock will automatically update the TTL of the transaction through `txnheartbeat` to ensure that the second transaction does not clear the lock of the first transaction.

### Other errors related to locks

#### Pessimistic lock retry limit reached

When the transaction conflict is very serious or a write conflict occurs, the optimistic transaction will be terminated directly, and the pessimistic transaction will retry the statement with the latest data from storage until there is no write conflict.

Because TiDB's locking operation is a write operation, and the process of the operation is to read first and then write, there are two RPC requests. If a write conflict occurs in the middle of a transaction, TiDB will try again to lock the target keys, and each retry will be printed to the TiDB log. The number of retries is determined by [pessimistic-txn.max-retry-count](/tidb-configuration-file.md#max-retry-count).

In the pessimistic transaction mode, if a write conflict occurs and the number of retries reaches the upper limit, an error message containing the following keywords appears in the TiDB log:

```log
err="pessimistic lock retry limit reached"
```

Solutions:

* If the above error occurs frequently, it is recommended to adjust from the application side.

#### Lock wait timeout exceeded
 
In the pessimistic transaction mode, transactions wait for locks of each other. The timeout for waiting a lock is defined by the [innodb_lock_wait_timeout](/pessimistic-transaction.md#behaviors) parameter of TiDB. This is the maximum wait lock time at the SQL statement level, which is the expectation of a SQL statement Locking, but the lock has never been acquired. After this time, TiDB will not try to lock again and will return the corresponding error message to the client.

When a wait lock timeout occurs, the following error message will be returned to the client:

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```
 
Solutions:

* If the above error occurs frequently, it is recommended to adjust the application logic.

#### TTL manager has timed out
 
The transaction execution time can not exceed the GC time limit. In addition, the TTL time of pessimistic transactions has an upper limit, whose default value is 10 minutes. Therefore, a pessimistic transaction executed for more than 10 minutes will fail to commit. This timeout threshold is controlled by the TiDB parameter [performance.max-txn-ttl](https://github.com/pingcap/tidb/blob/master/config/config.toml.example).

When the execution time of a pessimistic transaction exceeds the TTL time, the following error message occurs in the TiDB log:

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

Solutions:

* First, confirm whether the application logic can be optimized. For example, large transactions may trigger TiDB's transaction size limit, which can be split into multiple small transactions. 
* Also, you can adjust the related parameters properly to meet the application transaction logic.

#### Deadlock found when trying to get lock

Due to resource competition between two or more transactions, a deadlock occurs. If you do not handle it manually, transactions that block each other cannot be executed successfully and will wait for each other forever. To resolve dead locks, you need to manually terminate one of the transactions to resume other transaction requests.

When a pessimistic transaction has a deadlock, one of the transactions must be terminated to unlock the deadlock. The client will return the same `Error 1213` error as in MySQL, for example:

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```

Solutions:

* The application needs to adjust transaction request logic when there too many deadlocks.
