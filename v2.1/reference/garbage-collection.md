---
title: TiDB Garbage Collection (GC)
summary: Use Garbage Collection (GC) to clear the obsolete data of TiDB.
category: reference
---

# TiDB Garbage Collection (GC)

TiDB uses MVCC to control concurrency. When you update or delete data, the original data is not deleted immediately but is kept for a period during which it can be read. Thus the write operation and the read operation are not mutually exclusive and it is possible to read the history versions of the data.

The data versions whose duration exceeds a specific time and that are not used any more will be cleared, otherwise they will occupy the disk space and affect TiDB's performance. TiDB uses Garbage Collection (GC) to clear the obsolete data.

## Working mechanism

GC runs periodically on TiDB. When a TiDB server is started, a `gc_worker` is enabled in the background. In each TiDB cluster, one `gc_worker` is elected to be the leader which is used to maintain the GC status and send GC commands to all the TiKV Region leaders.

## Configuration and monitor

The GC configuration and operational status are recorded in the `mysql.tidb` system table as below, which can be monitored and configured using SQL statements:

```sql
mysql> select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb;
+-----------------------+------------------------------------------------------------------------------------------------+
| VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
+-----------------------+------------------------------------------------------------------------------------------------+
| bootstrapped          | True                                                                                           |
| tidb_server_version   | 18                                                                                             |
| tikv_gc_leader_uuid   | 58accebfa7c0004                                                                                |
| tikv_gc_leader_desc   | host:ip-172-16-30-5, pid:95472, start at 2018-04-11 13:43:30.73076656 +0800 CST m=+0.068873865 |
| tikv_gc_leader_lease  | 20180418-11:02:30 +0800 CST                                                                    |
| tikv_gc_run_interval  | 10m0s                                                                                          |
| tikv_gc_life_time     | 10m0s                                                                                          |
| tikv_gc_last_run_time | 20180418-10:59:30 +0800 CST                                                                    |
| tikv_gc_safe_point    | 20180418-10:58:30 +0800 CST                                                                    |
| tikv_gc_concurrency   | 1                                                                                              |
+-----------------------+------------------------------------------------------------------------------------------------+
10 rows in set (0.02 sec)
```

In the table above, `tikv_gc_run_interval`, `tikv_gc_life_time` and `tikv_gc_concurrency` can be configured manually. Other variables with the `tikv_gc` prefix record the current status, which are automatically updated by TiDB. Do not modify these variables.

- `tikv_gc_leader_uuid`, `tikv_gc_leader_desc`, `tikv_gc_leader_lease`: the current GC leader information.

- `tikv_gc_run_interval`: the interval of GC work. The value is 10 min by default and cannot be smaller than 10 min.

- `tikv_gc_life_time`: the retention period of data versions; The value is 10 min by default and cannot be smaller than 10 min.

    When GC works, the outdated data is cleared. You can set it using the SQL statement. For example, if you want to retain the data within a day, you can execute the operation as below:

    ```sql
    update mysql.tidb set VARIABLE_VALUE = '24h' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

    The duration strings are a sequence of a number with the time unit, such as 24h, 2h30m and 2.5h. The time units you can use include "h", "m" and "s".

    > **Note:**
    >
    > When you set `tikv_gc_life_time` to a large number (like days or even months) in a scenario where data is updated frequently, some problems as follows may occur:

    - The more versions of the data, the more disk storage space is occupied.
    - A large number of history versions might slow down the query. They may affect range queries like `select count(*) from t`.
    - If `tikv_gc_life_time` is suddenly turned to a smaller value during operation, a great deal of old data may be deleted in a short time, causing I/O pressure.

- `tikv_gc_last_run_time`: the last time GC works.

- `tikv_gc_safe_point`: the time before which versions are cleared by GC and after which versions are readable.

- `tikv_gc_concurrency`: the GC concurrency. It is set to 1 by default. In this case, a single thread operates and threads send request to each Region and wait for the response one by one. You can set the variable value larger to improve the system performance, but keep the value smaller than 128.

## Implementation details

The GC implementation process is complex. When the obsolete data is cleared, data consistency is guaranteed. The process of doing GC is as below:

### 1. Resolve locks

The TiDB transaction model is inspired by Google's Percolator. It's mainly a two-phase commit protocol with some practical optimizations. When the first phase is finished, all the related keys are locked. Among these locks, one is the primary lock and the others are secondary locks which contain a pointer of the primary locks; in the secondary phase, the key with the primary lock gets a write record and its lock is removed. The write record indicates the write or delete operation in the history or the transactional rollback record of this key. Replacing the primary lock with which write record indicates whether the corresponding transaction is committed successfully. Then all the secondary locks are replaced successively. If the threads fail to replace the secondary locks, these locks are retained. During GC, the lock whose timestamp is before the safe point is replaced with the corresponding write record based on the transaction committing status.

> **Note:**
>
> This is a required step. Once GC has cleared the write record of the primary lock, you can never know whether this transaction is successful or not. As a result, data consistency cannot be guaranteed.

### 2. Delete ranges

`DeleteRanges` is usually executed after operations like `drop table`, used to delete a range which might be very large. If the `use_delete_range` option of TiKV is not enabled, TiKV deletes the keys in the range.

### 3. Do GC

Clear the data before the safe point of each key and the write record.

> **Note:**
>
> If the last record in all the write records of `Put` and `Delete` types before the safe point is `Put`, this record and its data cannot be deleted directly. Otherwise, you cannot successfully perform the read operation whose timestamp is after the safe point and before the next version of the key.
