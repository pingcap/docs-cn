---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash.
category: reference
aliases: ['/docs/dev/reference/tiflash/tune-performance/']
---

# Tune TiFlash Performance

This document introduces how to tune the performance of TiFlash, including planning machine resources and tuning TiDB parameters.

## Plan resources

If you want to save machine resources and have no requirement on isolation, you can use the method that combines the deployment of both TiKV and TiFlash. It is recommended that you save enough resources for TiKV and TiFlash respectively, and do not share disks.

## Tune TiDB parameters

1. For the TiDB node dedicated to OLAP/TiFlash, it is recommended that you increase the value of the [`tidb_distsql_scan_concurrency`](/tidb-specific-system-variables.md#tidb_distsql_scan_concurrency) configuration item for this node to `80`:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2. Enable the optimization for TiDB Operator such as the aggregate pushdown of `JOIN` or `UNION`:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```
