---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash by planning machine resources and tuning TiDB parameters.
aliases: ['/docs/dev/tiflash/tune-tiflash-performance/','/docs/dev/reference/tiflash/tune-performance/']
---

# Tune TiFlash Performance

This document introduces how to tune the performance of TiFlash by properly planning machine resources and tuning TiDB parameters. By following these methods, your TiFlash cluster can achieve optimal performance.

## Plan resources

If you want to save machine resources and have no requirement on isolation, you can use the method that combines the deployment of both TiKV and TiFlash. It is recommended that you save enough resources for TiKV and TiFlash respectively, and do not share disks.

## Tune TiDB parameters

This section describes how to improve TiFlash performance by tuning TiDB parameters, including:

- [Forcibly enable the MPP mode](#forcibly-enable-the-mpp-mode)
- [Push down aggregate functions to a position before `Join` or `Union`](#push-down-aggregate-functions-to-a-position-before-join-or-union)
- [Enable `Distinct` optimization](#enable-distinct-optimization)
- [Compact data using the `ALTER TABLE ... COMPACT` statement](#compact-data-using-the-alter-table--compact-statement)
- [Replace Shuffled Hash Join with Broadcast Hash Join](#replace-shuffled-hash-join-with-broadcast-hash-join)
- [Set a greater execution concurrency](#set-a-greater-execution-concurrency)
- [Configure `tiflash_fine_grained_shuffle_stream_count`](#configure-tiflash_fine_grained_shuffle_stream_count)

### Forcibly enable the MPP mode

MPP execution plans can fully utilize distributed computing resources, thereby significantly improving the efficiency of batch data queries. When the optimizer does not generate an MPP execution plan for a query, you can forcibly enable the MPP mode:

The variable [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51) controls whether to ignore the optimizer's cost estimation and to forcibly use TiFlash's MPP mode for query execution. To enable MPP mode forcibly, run the following command:

```sql
set @@tidb_enforce_mpp = ON;
```

### Push down aggregate functions to a position before `Join` or `Union`

By pushing down aggregate operations to the position before `Join` or `Union`, you can reduce the data to be processed in the `Join` or `Union` operation, thereby improving performance.

The variable [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) controls whether the optimizer executes the optimization operation of pushing down the aggregate function to the position before `Join` or `Union`. When the aggregate operations are quite slow in the query, you can set this variable to `ON`.

```sql
set @@tidb_opt_agg_push_down = ON;
```

### Enable `Distinct` optimization

TiFlash does not support some aggregate functions that accept the `Distinct` column, such as `Sum`. By default, the entire aggregate function is calculated in TiDB. By enabling the `Distinct` optimization, some operations can be pushed down to TiFlash, thereby improving query performance.

If the aggregate function with the `distinct` operation is slow in a query, you can enable the optimization operation of pushing down the aggregate function with `Distinct` (such as `select sum(distinct a) from t`) to Coprocessor by setting the value of the [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) variable to `ON`.

```sql
set @@tidb_opt_distinct_agg_push_down = ON;
```

### Compact data using the `ALTER TABLE ... COMPACT` statement

Executing the [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) statement can initiate compaction for a specific table or partition on a TiFlash node. During the compaction, the physical data on the node is rewritten, including cleaning up deleted rows and merging multiple versions of data caused by updates. This helps enhance access performance and reduce disk usage. The following are examples:

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

### Replace Shuffled Hash Join with Broadcast Hash Join

For `Join` operations with small tables, the Broadcast Hash Join algorithm can avoid transfering large tables, thereby improving the computing performance.

- The [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) variable controls whether to use the Broadcast Hash Join algorithm. If the table size (unit: byte) is smaller than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.

    ```sql
    set @@tidb_broadcast_join_threshold_size = 2000000;
    ```

- The [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) variable also controls whether to use the Broadcast Hash Join algorithm. If the objects of the join operation belong to a subquery, the optimizer cannot estimate the size of the subquery result set. In this situation, the size is determined by the number of rows in the result set. If the estimated number of rows for the subquery is fewer than the value of this variable, the Broadcast Hash Join algorithm is used. Otherwise, the Shuffled Hash Join algorithm is used.

    ```sql
    set @@tidb_broadcast_join_threshold_count = 100000;
    ```

### Set a greater execution concurrency

A greater execution concurrency allows TiFlash to occupy more CPU resources of the system, thereby improving query performance.

The [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) variable is used to set the maximum concurrency for TiFlash to execute a request. The unit is threads.

```sql
set @@tidb_max_tiflash_threads = 20;
```

### Configure `tiflash_fine_grained_shuffle_stream_count`

You can increase the concurrency for executing window functions by configuring [`tiflash_fine_grained_shuffle_stream_count`](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) of the Fine Grained Shuffle feature. In this way, the execution of window functions can occupy more system resources, which improves query performance.

When a window function is pushed down to TiFlash for execution, you can use this variable to control the concurrency level of the window function execution. The unit is threads.

```sql
set @@tiflash_fine_grained_shuffle_stream_count = 20;
```
