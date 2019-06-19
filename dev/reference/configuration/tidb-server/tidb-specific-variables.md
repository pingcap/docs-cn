---
title: TiDB Specific System Variables
summary: Use system variables specific to TiDB to optimize performance.
category: reference
aliases: ['/docs/sql/tidb-specific/']
---

# TiDB Specific System Variables

TiDB contains a number of system variables which are specific to its usage, and **do not** apply to MySQL. These variables start with a `tidb_` prefix, and can be tuned to optimize system performance.

## System variables

Variables can be set with the `SET` statement, for example:

```
set @@tidb_distsql_scan_concurrency = 10
```

If you need to set the global variable, run:

```
set @@global.tidb_distsql_scan_concurrency = 10
```

### tidb_snapshot

- Scope: SESSION
- Default value: ""
- This variable is used to set the time point at which the data is read by the session. For example, when you set the variable to "2017-11-11 20:20:20" or a TSO number like "400036290571534337", the current session reads the data of this moment.

### tidb_import_data

- Scope: SESSION
- Default value: 0
- This variable indicates whether to import data from the dump file currently.
- To speed up importing, the unique index constraint is not checked when the variable is set to 1.
- This variable is only used by Lightning. Do not modify it.

### tidb_opt_agg_push_down

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before Join.
- When the aggregate operation is slow in query, you can set the variable value to 1.

### tidb_opt_insubquery_unfold

- Scope: SESSION
- Default value: 0
- This variable is used to set whether the optimizer executes the optimization operation of unfolding the "in-" subquery.

### tidb_auto_analyze_ratio

- Scope: GLOBAL
- Default value: 0.5
- This variable is used to set the threshold when TiDB automatically executes [`ANALYZE TABLE`](/dev/reference/sql/statements/analyze-table.md) in a background thread to update table statistics. For example, a value of 0.5 means that auto-analyze is triggered when greater than 50% of the rows in a table have been modified.  Auto-analyze can be restricted to only execute during certain hours of the day by specifying `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time`.

> **Note:**
>
> Only when the `run-auto-analyze` option is enabled in the starting configuration file of TiDB, the `auto_analyze` feature can be triggered.

### tidb_auto_analyze_start_time

- Scope: GLOBAL
- Default value: 00:00 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_auto_analyze_end_time

- Scope: GLOBAL
- Default value: 23:59 +0000
- This variable is used to restrict the time window that the automatic update of statistics is permitted. For example, to only allow automatic statistics updates between 1AM and 3AM, set `tidb_auto_analyze_start_time='01:00 +0000'` and `tidb_auto_analyze_end_time='03:00 +0000'`.

### tidb_build_stats_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the concurrency of executing the `ANALYZE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_checksum_table_concurrency

- Scope: SESSION
- Default value: 4
- This variable is used to set the scan index concurrency of executing the `ADMIN CHECKSUM TABLE` statement.
- When the variable is set to a larger value, the execution performance of other queries is affected.

### tidb_current_ts

- Scope: SESSION
- Default value: 0
- This variable is read-only. It is used to obtain the timestamp of the current transaction.

### tidb_config

- Scope: SESSION
- Default value: ""
- This variable is read-only. It is used to obtain the configuration information of the current TiDB server.

### tidb_distsql_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 15
- This variable is used to set the concurrency of the `scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.
- For OLAP scenarios, the maximum value cannot exceed the number of CPU cores of all the TiKV nodes.

### tidb_index_lookup_size

- Scope: SESSION | GLOBAL
- Default value: 20000
- This variable is used to set the batch size of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_index_lookup_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `index lookup join` algorithm.

### tidb_hash_join_concurrency

- Scope: SESSION | GLOBAL
- Default value: 5
- This variable is used to set the concurrency of the `hash join` algorithm.

### tidb_index_serial_scan_concurrency

- Scope: SESSION | GLOBAL
- Default value: 1
- This variable is used to set the concurrency of the `serial scan` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_projection_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of the `Projection` operator.

### tidb_hashagg_partial_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `partial` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_hashagg_final_concurrency

- Scope: SESSION | GLOBAL
- Default value: 4
- This variable is used to set the concurrency of executing the concurrent `hash aggregation` algorithm in the `final` phase.
- When the parameter of the aggregate function is not distinct, `HashAgg` is run concurrently and respectively in two phases - the `partial` phase and the `final` phase.

### tidb_index_join_batch_size

- Scope: SESSION | GLOBAL
- Default value: 25000
- This variable is used to set the batch size of the `index lookup join` operation.
- Use a bigger value in OLAP scenarios, and a smaller value in OLTP scenarios.

### tidb_skip_utf8_check

- Scope: SESSION | GLOBAL
- Default value: 0
- This variable is used to set whether to skip UTF-8 validation.
- Validating UTF-8 characters affects the performance. When you are sure that the input characters are valid UTF-8 characters, you can set the variable value to 1.

### tidb_batch_insert

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to divide the inserted data automatically. It is valid only when `autocommit` is enabled.
- When inserting a large amount of data, you can set the variable value to 1. Then the inserted data is automatically divided into multiple batches and each batch is inserted by a single transaction.
- This operation might lead to a loss of transaction atomicity. Therefore, it is not recommended to use this parameter in the production environment.

### tidb_batch_delete

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to divide the data for deletion automatically. It is valid only when you delete from a single table and `autocommit` is enabled. For the definition of single-table DELETE statement, see [here](https://dev.mysql.com/doc/refman/8.0/en/delete.html).
- When deleting a large amount of data, you can set the variable value to 1. Then the data for deletion is automatically divided into multiple batches and each batch is deleted by a single transaction.
- This operation might lead to a loss of transaction atomicity. Therefore, it is not recommended to use this parameter in the production environment.

### tidb_dml_batch_size

- Scope: SESSION
- Default value: 20000
- This variable is used to set the automatically divided batch size of the data for insertion/deletion. It is only valid when `tidb_batch_insert` or `tidb_batch_delete` is enabled.
- When the data size of a single row is very large, the overall data size of 20 thousand rows exceeds the size limit for a single transaction. In this case, set the variable to a smaller value.

### tidb_max_chunk_size

- Scope: SESSION | GLOBAL
- Default value: 1024
- This variable is used to set the maximum number of rows in a chunk during the execution process.

### tidb_mem_quota_query

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for a query.
- If the memory quota of a query during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_hashjoin

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `HashJoin` operator.
- If the memory quota of the `HashJoin` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_mergejoin

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `MergeJoin` operator.
- If the memory quota of the `MergeJoin` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_sort

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `Sort` operator.
- If the memory quota of the `Sort` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_topn

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `TopN` operator.
- If the memory quota of the `TopN` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_indexlookupreader

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `IndexLookupReader` operator.
- If the memory quota of the `IndexLookupReader` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_indexlookupjoin

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `IndexLookupJoin` operator.
- If the memory quota of the `IndexLookupJoin` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_mem_quota_nestedloopapply

- Scope: SESSION
- Default value: 32 GB
- This variable is used to set the threshold value of memory quota for the `NestedLoopApply` operator.
- If the memory quota of the `NestedLoopApply` operator during execution exceeds the threshold value, TiDB performs the operation designated by the OOMAction option in the configuration file.

### tidb_general_log

- Scope: SERVER
- Default value: 0
- This variable is used to set whether to record all the SQL statements in the log.

### tidb_enable_streaming

- Scope: SERVER
- Default value: 0
- This variable is used to set whether to enable Streaming.

### tidb_retry_limit

- Scope: SESSION | GLOBAL
- Default value: 10
- When a transaction encounters retriable errors (such as transaction conflicts, over slow transaction commit, or table schema changes), this transaction can be re-executed. This variable is used to set the maximum number of the retries.

### tidb_disable_txn_auto_retry

- Scope: SESSION | GLOBAL
- Default: on
- This variable is used to set whether to disable automatic retry of explicit transactions. The default value of `on` means that transactions will not automatically retry in TiDB and `COMMIT` statements might return errors that need to be handled in the application layer.

    Setting the value to `off` means that TiDB will automatically retry transactions, resulting in fewer errors from `COMMIT` statements. Be careful when making this change, because it might result in lost updates.

    This variable does not affect automatically committed implicit transactions and internally executed transactions in TiDB. The maximum retry count of these transactions is determined by the value of `tidb_retry_limit`.

    To decide whether you can enable automatic retry, see [description of optimistic transactions](/dev/reference/transactions/transaction-isolation.md#description-of-optimistic-transactions).

### tidb_back_off_weight

- Scope: SESSION | GLOBAL
- Default value: 2
- This variable is used to increase the weight of the maximum time of TiDB `back-off`, that is, the maximum retry time for sending a retry request when an internal network or other component (TiKV, PD) failure is encountered. This variable can be used to adjust the maximum retry time and the minimum value is 1.

    For example, the base timeout for TiDB to take TSO from PD is 15 seconds. When `tidb_back_off_weight = 2`, the maximum timeout for taking TSO is: *base time * 2 = 30 seconds*.

    In the case of a poor network environment, appropriately increasing the value of this variable can effectively alleviate error reporting to the application end caused by timeout. If the application end wants to receive the error information more quickly, minimize the value of this variable.

### tidb_enable_table_partition

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to enable the `TABLE PARTITION` feature.

### tidb_backoff_lock_fast

- Scope: SESSION | GLOBAL
- Default value: 100
- This variable is used to set the `backoff` time when the read request meets a lock.

### tidb_ddl_reorg_worker_cnt

- Scope: GLOBAL
- Default value: 16
- This variable is used to set the concurrency of the DDL operation in the `re-organize` phase.

### tidb_ddl_reorg_batch_size

- Scope: GLOBAL
- Default value: 1024
- This variable is used to set the batch size during the `re-organize` phase of the DDL operation. For example, when TiDB executes the `ADD INDEX` operation, the index data needs to backfilled by `tidb_ddl_reorg_worker_cnt` (the number) concurrent workers. Each worker backfills the index data in batches.
    - If many updating operations such as `UPDATE` and `REPLACE` exist during the `ADD INDEX` operation, a larger batch size indicates a larger probability of transaction conflicts. In this case, you need to adjust the batch size to a smaller value. The minimum value is 32.
    - If the transaction conflict does not exist, you can set the batch size to a large value. The maximum value is 10240. This can increase the speed of the backfilling data, but the write pressure on TiKV also becomes higher.

### tidb_ddl_reorg_priority

- Scope: SESSION | GLOBAL
- Default value: `PRIORITY_LOW`
- This variable is used to set the priority of executing the `ADD INDEX` operation in the `re-organize` phase.
- You can set the value of this variable to `PRIORITY_LOW`, `PRIORITY_NORMAL` or `PRIORITY_HIGH`.

### tidb_force_priority

- Scope: SESSION
- Default value: `NO_PRIORITY`
- This variable is used to change the default priority for statements executed on a TiDB server. A use case is to ensure that a particular user that is performing OLAP queries receives lower priority than users performing OLTP queries.
- You can set the value of this variable to `NO_PRIORITY`, `LOW_PRIORITY`, `DELAYED` or `HIGH_PRIORITY`.

### tidb_opt_write_row_id

- Scope: SESSION
- Default value: 0
- This variable is used to set whether to allow `insert`, `replace` and `update` statements to operate on the column `_tidb_rowid`. It is not allowed by default. This variable can be used only when importing data with TiDB tools.

## SHARD_ROW_ID_BITS

For the tables with non-integer PK or without PK, TiDB uses an implicit auto-increment ROW ID. When a large number of `INSERT` operations occur, the data is written into a single Region, causing a write hot spot.

To mitigate the hot spot issue, you can configure `SHARD_ROW_ID_BITS`. The ROW ID is scattered and the data is written into multiple different Regions. But setting an overlarge value might lead to an excessively large number of RPC requests, which increases the CPU and network overheads.

- `SHARD_ROW_ID_BITS = 4` indicates 16 shards
- `SHARD_ROW_ID_BITS = 6` indicates 64 shards
- `SHARD_ROW_ID_BITS = 0` indicates the default 1 shard

Usage of statements:

- `CREATE TABLE`: `CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;`
- `ALTER TABLE`: `ALTER TABLE t SHARD_ROW_ID_BITS = 4;`

## tidb_slow_log_threshold

- Scope: SESSION
- Default value: 300ms
- This variable is used to output the threshold value of the time consumed by the slow log. When the time consumed by a query is larger than this value, this query is considered as a slow log and its log is output to the slow query log.

Usage example:

```sql
set tidb_slow_log_threshold = 200
```

## tidb_query_log_max_len

- Scope: SESSION
- Default value: 2048 (bytes)
- The maximum length of the SQL statement output. When the output length of a statement is larger than the `tidb_query-log-max-len` value, the statement is truncated to output.

Usage example:

```sql
set tidb_query_log_max_len = 20
```
