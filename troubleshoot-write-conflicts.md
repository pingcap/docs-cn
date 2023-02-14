---
title: Troubleshoot Write Conflicts in Optimistic Transactions
summary: Learn about the reason of and solutions to write conflicts in optimistic transactions.
---

# Troubleshoot Write Conflicts in Optimistic Transactions

This document introduces the reason of and solutions to write conflicts in optimistic transactions.

Before TiDB v3.0.8, TiDB uses the optimistic transaction model by default. In this model, TiDB does not check conflicts during transaction execution. Instead, while the transaction is finally committed, the two-phase commit (2PC) is triggered and TiDB checks write conflicts. If a write conflict exists and the auto-retry mechanism is enabled, then TiDB retries the transaction within limited times. If the retry succeeds or has reached the upper limit on retry times, TiDB returns the result of transaction execution to the client. Therefore, if a lot of write conflicts exist in the TiDB cluster, the duration can be longer.

## The reason of write conflicts

TiDB implements its transactions by using the [Percolator](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf) transaction model. `percolator` is generally an implementation of 2PC. For the detailed 2PC process, see [TiDB Optimistic Transaction Model](/optimistic-transaction.md).

After the client sends a `COMMIT` request to TiDB, TiDB starts the 2PC process:

1. TiDB chooses one key from all keys in the transaction as the primary key of the transaction.
2. TiDB sends the `prewrite` request to all the TiKV Regions involved in this commit. TiKV judges whether all keys can preview successfully.
3. TiDB receives the result that all `prewrite` requests are successful.
4. TiDB gets the `commit_ts` from PD.
5. TiDB sends the `commit` request to the TiKV Region that contains the primary key of the transaction. After TiKV receives the `commit` request, it checks the validity of the data and clears the locks left in the `prewrite` stage.
6. After the `commit` request returns successfully, TiDB returns success to the client.

The write conflict occurs in the `prewrite` stage. When the transaction finds that another transaction is writing the current key (`data.commit_ts` > `txn.start_ts`), a write conflict occurs.

## Detect write conflicts

In the TiDB Grafana panel, check the following monitoring metrics under **KV Errors**:

* **KV Backoff OPS** indicates the count of error messages per second returned by TiKV.

    ![kv-backoff-ops](/media/troubleshooting-write-conflict-kv-backoff-ops.png)

    The `txnlock` metric indicates the write-write conflict. The `txnLockFast` metric indicates the read-write conflict.

* **Lock Resolve OPS** indicates the count of items related to transaction conflicts per second:

    ![lock-resolve-ops](/media/troubleshooting-write-conflict-lock-resolve-ops.png)

    - `not_expired` indicates the TTL of the lock was not expired. The conflict transaction cannot resolve locks until the TTL is expired.
    - `wait_expired` indicates that the transaction needs to wait the lock to expire.
    - `expired` indicates the TTL of the lock was expired. Then the conflict transaction can resolve this lock.

* **KV Retry Duration** indicates the duration of re-sends the KV request:

     ![kv-retry-duration](/media/troubleshooting-write-conflict-kv-retry-duration.png)

You can also use `[kv:9007]Write conflict` as the keywords to search in the TiDB log. The keywords also indicate the write conflict exists in the cluster.

## Resolve write conflicts

If many write conflicts exist in the cluster, it is recommended to find out the write conflict key and the reason, and then try to change the application logic to avoid write conflicts. When the write conflict exists in the cluster, you can see the log similar to the following one in the TiDB log file:

```log
[2020/05/12 15:17:01.568 +08:00] [WARN] [session.go:446] ["commit failed"] [conn=3] ["finished txn"="Txn{state=invalid}"] [error="[kv:9007]Write conflict, txnStartTS=416617006551793665, conflictStartTS=416617018650001409, conflictCommitTS=416617023093080065, key={tableID=47, indexID=1, indexValues={string, }} primary={tableID=47, indexID=1, indexValues={string, }} [try again later]"]
```

The explanation of the log above is as follows:

* `[kv:9007]Write conflict`: indicates the write-write conflict.
* `txnStartTS=416617006551793665`: indicates the `start_ts` of the current transaction. You can use the `pd-ctl` tool to convert `start_ts` to physical time.
* `conflictStartTS=416617018650001409`: indicates the `start_ts` of the write conflict transaction.
* `conflictCommitTS=416617023093080065`: indicates the `commit_ts` of the write conflict transaction.
* `key={tableID=47, indexID=1, indexValues={string, }}`: indicates the write conflict key. `tableID` indicates the ID of the write conflict table. `indexID` indicates the ID of write conflict index. If the write conflict key is a record key, the log prints `handle=x`, indicating which record(row) has a conflict. `indexValues` indicates the value of the index that has a conflict.
* `primary={tableID=47, indexID=1, indexValues={string, }}`: indicates the primary key information of the current transaction.

You can use the `pd-ctl` tool to convert the timestamp to readable time:

{{< copyable "" >}}

```shell
tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 tso {TIMESTAMP}
```

You can use `tableID` to find the name of the related table:

{{< copyable "" >}}

```shell
curl http://{TiDBIP}:10080/db-table/{tableID}
```

You can use `indexID` and the table name to find the name of the related index:

{{< copyable "sql" >}}

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE TABLE_SCHEMA='{db_name}' AND TABLE_NAME='{table_name}' AND INDEX_ID={indexID};
```

In addition, in TiDB v3.0.8 and later versions, the pessimistic transaction becomes the default mode. The pessimistic transaction mode can avoid write conflicts during the transaction prewrite stage, so you do not need to modify the application any more. In the pessimistic transaction mode, each DML statement writes a pessimistic lock to the related keys during execution. This pessimistic lock can prevent other transactions from modifying the same keys, thus ensuring no write conflicts exist in the `prewrite` stage of the transaction 2PC.
