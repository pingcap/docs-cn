---
title: TiDB 7.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.1.0.
---

# TiDB 7.1.0 Release Notes

TiDB version: 7.1.0 (upcoming)

> **Note:**
>
> TiDB v7.1.0 is not yet available. This release note is a preview version to provide insights into upcoming features and is subject to change. The features outlined here are not guaranteed to be included in the final release.

In v7.1.0, the key new features and improvements are as follows:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="2">Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/sql-non-prepared-plan-cache" target="_blank">Session-level plan cache for non-prepared statements</a> (GA)</td>
    <td>Support automatically reusing plan cache at the session level to remove query planning time, reducing query time for repeat SQL patterns without manually setting prepare statements in advance.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#scatter-read-hotspots" target="_blank">Load-based replica read</a></td>
    <td>In a read hotspot scenario, TiDB can redirect read requests for a hotspot TiKV node to its replicas. This feature efficiently scatters read hotspots and optimizes the use of cluster resources. To control the threshold for triggering load-based replica read, you can adjust the system variable <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_load_based_replica_read_threshold-new-in-v700" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a>.</td>
  </tr>
  <tr>
    <td rowspan="1">Reliability and availability</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/tidb-resource-control" target="_blank">Resource control by resource groups</a> (GA)</td>
   <td>Support resource management based on resource groups, which maps database users to the corresponding resource groups and sets quotas for each resource group based on actual needs.</td>
 </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/dev/sql-statement-create-index#multi-valued-index" target="_blank">Multi-valued index</a> (GA)</td>
    <td>Support MySQL-compatible multi-valued indexes and enhance the JSON type to improve compatibility with MySQL 8.0. This feature improves the efficiency of membership checks on multi-valued columns.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/dev/generated-columns" target="_blank">Generated columns</a> (GA)</td>
    <td>Values in a generated column are calculated by a SQL expression in the column definition in real time. This feature pushes some application logic to the database level, thus improving query efficiency.</td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

* TiFlash supports late materialization (GA) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

     In v7.0.0, late materialization was introduced in TiFlash as an experimental feature for optimizing query performance. This feature is disabled by default (the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable defaults to `OFF`). When processing a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query, and then filters and aggregates the data based on the query conditions. When Late materialization is enabled, TiDB supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down to the TableScan operator, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

    Starting from v7.1.0, the TiFlash late materialization feature is generally available and enabled by default (the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable defaults to `ON`). The TiDB optimizer decides which filters to be pushed down to the TableScan operator based on the statistics and the filter conditions of the query.

    For more information, see [documentation](/tiflash/tiflash-late-materialization.md).

* TiFlash supports automatically choosing an MPP Join algorithm according to the overhead of network transmission [#7084](https://github.com/pingcap/tiflash/issues/7084) @[solotzg](https://github.com/solotzg)

    The TiFlash MPP mode supports multiple Join algorithms. Before v7.1.0, TiDB determines whether the MPP mode uses the Broadcast Hash Join algorithm based on the [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) variables and the actual data volume.

    In v7.1.0, TiDB introduces the [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) variable, which controls whether to choose the MPP Join algorithm based on the minimum overhead of network transmission. This variable is disabled by default, indicating that the default algorithm selection method remains the same as that before v7.1.0. You can set the variable to `ON` to enable it. When it is enabled, you no longer need to manually adjust the [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) variables (both variables does not take effect at this time), TiDB automatically estimates the threshold of network transmission by different Join algorithms, and then chooses the algorithm with the smallest overhead overall, thus reducing network traffic and improving MPP query performance.

    For more information, see [documentation](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode).

* Support load-based replica read to mitigate read hotspots [#14151](https://github.com/tikv/tikv/issues/14151) @[sticnarf](https://github.com/sticnarf) @[you06](https://github.com/you06)

    In a read hotspot scenario, the hotspot TiKV node cannot process read requests in time, resulting in the read requests queuing. However, not all TiKV resources are exhausted at this time. To reduce latency, TiDB v7.1.0 introduces the load-based replica read feature, which allows TiDB to read data from other TiKV nodes without queuing on the hotspot TiKV node. You can control the queue length of read requests using the [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) system variable. When the estimated queue time of the leader node exceeds this threshold, TiDB prioritizes reading data from follower nodes. This feature can improve read throughput by 70% to 200% in a read hotspot scenario compared to not scattering read hotspots.

    For more information, see [documentation](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots).

* Support caching execution plans for non-prepared statements (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    TiDB v7.0.0 introduces non-prepared plan cache as an experimental feature to improve the load capacity of concurrent OLTP. In v7.1.0, this feature is generally available, enabled by default, and supports caching more SQL statements.

    To improve memory utilization, TiDB v7.1.0 merges the cache pools of non-prepared and prepared plan caches. You can control the cache size using the system variable [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710). The [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) and [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) system variables are deprecated.

    To maintain forward compatibility, when you upgrade from an earlier version to v7.1.0 or later versions, the cache size `tidb_session_plan_cache_size` remains the same value as `tidb_prepared_plan_cache_size`, and [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) remains the setting before the upgrade. After sufficient performance testing, you can enable non-prepared plan cache using `tidb_enable_non_prepared_plan_cache`. For a newly created cluster, non-prepared plan cache is enabled by default.

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

### Reliability

* Resource Control becomes generally available (GA) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB enhances the resource control feature based on resource groups, which becomes GA in v7.1.0. This feature significantly improves the resource utilization efficiency and performance of TiDB clusters. The introduction of the resource control feature is a milestone for TiDB. You can divide a distributed database cluster into multiple logical units, map different database users to corresponding resource groups, and set the quota for each resource group as needed. When the cluster resources are limited, all resources used by sessions in the same resource group are limited to the quota. In this way, even if a resource group is over-consumed, the sessions in other resource groups are not affected.

    With this feature, you can combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set quotas, which can achieve the maximum utilization of resources. In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

    In TiDB v7.1.0, this feature introduces the ability to estimate system capacity based on actual workload or hardware deployment. The estimation ability provides you with a more accurate reference for capacity planning and assists you in better managing TiDB resource allocation to meet the stability needs of enterprise-level scenarios.

    For more information, see [documentation](/tidb-resource-control.md).

* Support the checkpoint mechanism for Fast Online DDL to improve fault tolerance and automatic recovery capability [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.1.0 introduces a checkpoint mechanism for [Fast Online DDL](/ddl-introduction.md), which significantly improves the fault tolerance and automatic recovery capability of Fast Online DDL. Even if the TiDB owner node is restarted or changed due to failures, TiDB can still recover progress from checkpoints that are automatically updated on a regular basis, making the DDL execution more stable and efficient.

    For more information, see [documentation](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630).

* Backup & Restore supports checkpoint restore [#42339](https://github.com/pingcap/tidb/issues/42339) @[Leavrth](https://github.com/Leavrth)

    Snapshot restore or log restore might be interrupted due to recoverable errors, such as disk exhaustion and node crash. Before TiDB v7.1.0, the recovery progress before the interruption would be invalidated even after the error is addressed, and you need to start the restore from scratch. For large clusters, this incurs considerable extra cost.

    Starting from TiDB v7.1.0, Backup & Restore (BR) introduces the checkpoint restore feature, which enables you to continue an interrupted restore. This feature can retain most recovery progress of the interrupted restore.

    For more information, see [documentation](/br/br-checkpoint-restore.md).

* Optimize the strategy of loading statistics [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    Enabling synchronous loading of statistics can significantly reduce the number of statistics that must be loaded during startup, thus improving the speed of loading statistics. This feature increases the stability of TiDB in complex runtime environments and reduces the impact of individual TiDB nodes restart on the overall service.

    For more information, see [documentation](/statistics.md#load-statistics).

### SQL

* Support saving TiFlash query results using the `INSERT INTO SELECT` statement (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    Starting from v6.5.0, TiDB supports pushing down the `SELECT` clause (analytical query) of the `INSERT INTO SELECT` statement to TiFlash. In this way, you can easily save the TiFlash query result to a TiDB table specified by `INSERT INTO` for further analysis, which takes effect as result caching (that is, result materialization).

    In v7.1.0, this feature is generally available. During the execution of the `SELECT` clause in the `INSERT INTO SELECT` statement, the optimizer can intelligently decide whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. Therefore, the `tidb_enable_tiflash_read_for_write_stmt` system variable introduced during the experimental phase is now deprecated. Note that the computation rules of `INSERT INTO SELECT` statements for TiFlash do not meet the `STRICT SQL Mode` requirement, so TiDB allows the `SELECT` clause in the `INSERT INTO SELECT` statement to be pushed down to TiFlash only when the [SQL mode](/sql-mode.md) of the current session is not strict, which means that the `sql_mode` value does not contain `STRICT_TRANS_TABLES` and `STRICT_ALL_TABLES`.

    For more information, see [documentation](/tiflash/tiflash-results-materialization.md).

* MySQL-compatible multi-valued indexes become generally available (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao)

    Filtering the values of an array in a JSON column is a common operation, but normal indexes cannot help speed up such an operation. Creating a multi-valued index on an array can greatly improve filtering performance. If an array in the JSON column has a multi-valued index, you can use the multi-valued index to filter retrieval conditions in `MEMBER OF()`, `JSON_CONTAINS()`, and `JSON_OVERLAPS()` functions, thereby reducing I/O consumption and improving operation speed.

    In v7.1.0, the multi-valued index feature becomes generally available (GA). It supports more complete data types and is compatible with TiDB tools. You can use multi-valued indexes to speed up the search operations on JSON arrays in production environments.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index).

* Improve the partition management for Hash and Key partitioned tables [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    Before v7.1.0, Hash and Key partitioned tables in TiDB only support the `TRUNCATE PARTITION` partition management statement. Starting from v7.1.0, Hash and Key partitioned tables also support `ADD PARTITION` and `COALESCE PARTITION` partition management statements. Therefore, you can flexibly adjust the number of partitions in Hash and Key partitioned tables as needed. For example, you can increase the number of partitions with the `ADD PARTITION` statement, or decrease the number of partitions with the `COALESCE PARTITION` statement.

    For more information, see [documentation](/partitioned-table.md#manage-hash-and-key-partitions).

* The syntax of Range INTERVAL partitioning becomes generally available (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    The syntax of Range INTERVAL partitioning (introduced in v6.3.0) becomes GA. With this syntax, you can define Range partitioning by a desired interval without enumerating all partitions, which drastically reduces the length of Range partitioning DDL statements. The syntax is equivalent to that of the original Range partitioning.

    For more information, see [documentation](/partitioned-table.md#range-interval-partitioning).

* Generated columns become generally available (GA) @[bb7133](https://github.com/bb7133)

    Generated columns are a valuable feature for database. When creating a table, you can define that the value of a column is calculated based on the values of other columns in the table, rather than being explicitly inserted or updated by users. This generated column can be either a virtual column or a stored column. TiDB has supported MySQL-compatible generated columns since earlier versions, and this feature becomes GA in v7.1.0.

    Using generated columns can improve MySQL compatibility for TiDB, simplifying the process of migrating from MySQL. It also reduces data maintenance complexity and improves data consistency and query efficiency.

    For more information, see [documentation](/generated-columns.md).

### Observability

* Enhance optimizer diagnostic information [#43122](https://github.com/pingcap/tidb/issues/43122) @[time-and-fate](https://github.com/time-and-fate)

    Obtaining sufficient information is the key to SQL performance diagnostics. In v7.1.0, TiDB continues to add optimizer runtime information to various diagnostic tools, providing better insights into how execution plans are selected and assisting in troubleshooting SQL performance issues. The new information includes:

    * `debug_trace.json` in the output of [`PLAN REPLAYER`](/sql-plan-replayer.md).
    * Partial statistics details for `operator info` in the output of [`EXPLAIN`](/explain-walkthrough.md).
    * Partial statistics details in the `Stats` field of [slow queries](/identify-slow-queries.md).

  For more information, see [Use `PLAN REPLAYER` to save and restore the on-site information of a cluster](/sql-plan-replayer.md), [`EXPLAIN` walkthrough](/explain-walkthrough.md), and [Identify slow queries](/identify-slow-queries.md).

### Security

* Replace the interface used for querying TiFlash system table information [#6941](https://github.com/pingcap/tiflash/issues/6941) @[flowbehappy](https://github.com/flowbehappy)

    Starting from v7.1.0, when providing the query service of [`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) and [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md) system tables for TiDB, TiFlash uses the gRPC port instead of the HTTP port, which avoids the security risks of the HTTP service.

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.0.0 to the current version (v7.1.0). If you are upgrading from v6.6.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* To improve security, TiFlash deprecates the HTTP service port (default `8123`) and uses the gRPC port as a replacement

    If you have upgraded TiFlash to v7.1.0, then during the TiDB upgrade to v7.1.0, TiDB cannot read the TiFlash system tables ([`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) and [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)).

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) | Deprecated | Changes the default value from `OFF` to `ON`. When [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50), the optimizer intelligently decides whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | Deprecated | Starting from v7.1.0, this system variable is deprecated. You can use [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) to control the maximum number of plans that can be cached. |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) | Deprecated | Starting from v7.1.0, this system variable is deprecated. You can use [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) to control the maximum number of plans that can be cached. |
| `tidb_ddl_distribute_reorg` | Deleted | This variable is renamed to [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710). |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that non-prepared plan cache is enabled by default. |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) | Modified | Takes effect starting from v7.1.0 and controls the threshold for triggering load-based replica read. Changes the default value from `"0s"` to `"1s"` after further tests. |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) | Modified | Changes the default value from `OFF` to `ON`, meaning that the TiFlash late materialization feature is enabled by default. |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) | Newly added | Controls whether to enable the distributed execution framework. After enabling distributed execution, DDL, Import and other supported backend tasks will be jointly completed by multiple TiDB nodes in the cluster. This variable was renamed from `tidb_ddl_distribute_reorg`. |
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710) | Newly added | Controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature for DML statements. |
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) | Newly added | This variable provides a more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer. |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-new-in-v710) | Newly added | Controls whether to invalidate the plan cache automatically when statistics on related tables are updated. |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) | Newly added | Controls the maximum size of a plan that can be cached in prepared or non-prepared plan cache. |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) | Newly added | Controls whether to use the algorithm with the minimum overhead of network transmission. If this variable is enabled, TiDB estimates the size of the data to be exchanged in the network using `Broadcast Hash Join` and `Shuffled Hash Join` respectively, and then chooses the one with the smaller size. [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) will not take effect after this variable is enabled. |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) | Newly added | Controls the maximum number of plans that can be cached. Prepared plan cache and non-prepared plan cache share the same cache. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710) | Newly added | Controls whether to wait for statistics initialization to finish before providing services during TiDB startup. |
| TiDB | [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) | Newly added | Controls whether to use lightweight statistics initialization during TiDB startup. |
| TiDB | [`timeout`](/tidb-configuration-file.md#timeout-new-in-v710) | Newly added | Sets the timeout for log-writing operations in TiDB. In case of a disk failure that prevents logs from being written, this configuration item can trigger the TiDB process to panic instead of hang. The default value is `0`, which means no timeout is set. |
| TiKV | [`optimize-filters-for-memory`](/tikv-configuration-file.md#optimize-filters-for-memory-new-in-v710) | Newly added | Controls whether to generate Bloom/Ribbon filters that minimize memory internal fragmentation. |
| TiKV | [`ribbon-filter-above-level`](/tikv-configuration-file.md#ribbon-filter-above-level-new-in-v710) | Newly added | Controls whether to use Ribbon filters for levels greater than or equal to this value and use non-block-based bloom filters for levels less than this value. |
| TiKV | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50) | Modified | Changes the default value from `30MiB` to `100MiB` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| TiKV | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) | Modified | Changes the default value from `3000` to `7000` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| TiKV | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620) | Modified | Changes the default value from `0.25` to `0.75` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| PD | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710) | Newly added | Controls the mode of store limit. Value options are `"v1"` and `"v2"`. |
| PD | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630) | Modified | Changes the default value from `false` to `true`, meaning that the diagnostic feature of scheduler is enabled by default. |
| TiFlash | `http_port` | Deleted | Deprecates the HTTP service port (default `8123`). |
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | Modified | Changes the default value from `false` to `true` after further tests, meaning that partitions in a table are stored in separate directories by default. It is recommended that you keep the value as `true` to avoid the potential issue of data loss during replication of partitioned tables to storage services. |

## Improvements

+ TiFlash

    - Improve TiFlash performance and stability in the disaggregated storage and compute architecture [#6882](https://github.com/pingcap/tiflash/issues/6882)  @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin)
    - Support optimizing query performance in Semi Join or Anti Semi Join by selecting the smaller table as the build side [#7280](https://github.com/pingcap/tiflash/issues/7280) @[yibin87](https://github.com/yibin87)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [ethercflow](https://github.com/ethercflow)
- [hihihuhu](https://github.com/hihihuhu)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lqs](https://github.com/lqs)
- [pingandb](https://github.com/pingandb)
- [yorkhellen](https://github.com/yorkhellen)
- [yujiarista](https://github.com/yujiarista)
