---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash.
aliases: ['/docs/dev/tiflash/tune-tiflash-performance/','/docs/dev/reference/tiflash/tune-performance/']
---

# Tune TiFlash Performance

This document introduces how to tune the performance of TiFlash, including planning machine resources and tuning TiDB parameters.

## Plan resources

If you want to save machine resources and have no requirement on isolation, you can use the method that combines the deployment of both TiKV and TiFlash. It is recommended that you save enough resources for TiKV and TiFlash respectively, and do not share disks.

## Tune TiDB parameters

1. For the TiDB node dedicated to OLAP/TiFlash, it is recommended that you increase the value of the [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) configuration item for this node to `80`:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2. Enable the super batch feature:

    You can use the [`tidb_allow_batch_cop`](/system-variables.md#tidb_allow_batch_cop-new-in-v40) variable to set whether to merge Region requests when reading from TiFlash.

    When the number of Regions involved in the query is relatively large, try to set this variable to `1` (effective for coprocessor requests with `aggregation` operators that are pushed down to TiFlash), or set this variable to `2` (effective for all coprocessor requests that are pushed down to TiFlash).

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_allow_batch_cop = 1;
    ```

3. Enable the optimization of pushing down aggregate functions before TiDB operators such as `JOIN` or `UNION`:

    You can use the [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down) variable to control the optimizer to execute this optimization. When the aggregate operations are quite slow in the query, try to set this variable to `1`.

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

4. Enable the optimization of pushing down aggregate functions with `Distinct` before TiDB operators such as `JOIN` or `UNION`:

    You can use the [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down) variable to control the optimizer to execute this optimization. When the aggregate operations with `Distinct` are quite slow in the query, try to set this variable to `1`.

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_distinct_agg_push_down = 1;
    ```