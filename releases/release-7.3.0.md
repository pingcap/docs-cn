---
title: TiDB 7.3.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.3.0.
---

# TiDB 7.3.0 Release Notes

Release date: August 14, 2023

TiDB version: 7.3.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.3/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.3.0#version-list)

7.3.0 introduces the following major features. In addition to that, 7.3.0 also includes a series of enhancements (described in the [Feature details](#feature-details) section) to query stability in TiDB server and TiFlash. These enhancements are more miscellaneous in nature and not user-facing so they are not included in the following table.

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
    <td>Scalability and Performance</td>
    <td>TiDB Lightning supports <a href="https://docs.pingcap.com/tidb/v7.3/partitioned-raft-kv">Partitioned Raft KV</a> (experimental)</td>
    <td>TiDB Lightning now supports the new Partitioned Raft KV architecture, as part of the near-term GA of the architecture.
    </td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-lightning-physical-import-mode-usage#conflict-detection">Add automatic conflict detection and resolution on data imports</a></td>
    <td>The TiDB Lightning Physical Import Mode supports a new version of conflict detection, which implements the semantics of replacing (<code>replace</code>) or ignoring (<code>ignore</code>) conflict data when encountering conflicts. It automatically handles conflict data for you while improving the performance of conflict resolution.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/tidb-resource-control#query-watch-parameters">Manual management of runaway queries </a>(experimental)</td>
    <td>Queries might take longer than you expect. With the new watch list of resource groups, you can now manage queries more effectively and either deprioritize or kill them. Allowing operators to mark target queries by exact SQL text, SQL digest, or plan digest and deal with the queries at a resource group level, this feature gives you much more control over the potential impact of unexpected large queries on a cluster.</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/optimizer-hints">Enhance operator control over query stability by adding more optimizer hints to the query planner</a></td>
    <td>Added hints: <code>NO_INDEX_JOIN()</code>, <code>NO_MERGE_JOIN()</code>, <code>NO_INDEX_MERGE_JOIN()</code>, <code>NO_HASH_JOIN()</code>, <code>NO_INDEX_HASH_JOIN()</code>
    </td>
  </tr>
  <tr>
    <td>DB Operations and Observability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.3/sql-statement-show-analyze-status">Show the progress of statistics collection tasks</a></td>
    <td>Support viewing the progress of <code>ANALYZE</code> tasks using the <code>SHOW ANALYZE STATUS</code> statement or through the <code>mysql.analyze_jobs</code> system table.</td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

* TiFlash supports the replica selection strategy [#44106](https://github.com/pingcap/tidb/issues/44106) @[XuHuaiyu](https://github.com/XuHuaiyu)

    Before v7.3.0, TiFlash uses replicas from all its nodes for data scanning and MPP calculations to maximize performance. Starting from v7.3.0, TiFlash introduces the replica selection strategy and lets you configure it using the [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730) system variable. This strategy supports selecting specific replicas based on the [zone attributes](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb) of nodes and scheduling specific nodes for data scanning and MPP calculations.

    For a cluster that is deployed in multiple data centers and each data center has complete TiFlash data replicas, you can configure this strategy to only select TiFlash replicas from the current data center. This means data scanning and MPP calculations are performed only on TiFlash nodes in the current data center, which avoids excessive network data transmission across data centers.

    For more information, see [documentation](/system-variables.md#tiflash_replica_read-new-in-v730).

* TiFlash supports Runtime Filter within nodes [#40220](https://github.com/pingcap/tidb/issues/40220) @[elsa0520](https://github.com/elsa0520)

    Runtime Filter is a **dynamic predicate** generated during the query planning phase. In the process of table joining, these dynamic predicates can effectively filter out rows that do not meet the join conditions, reducing scan time and network overhead, and improving the efficiency of table joining. Starting from v7.3.0, TiFlash supports Runtime Filter within nodes, improving the overall performance of analytical queries. In some TPC-DS workloads, the performance can be improved by 10% to 50%.

    This feature is disabled by default in v7.3.0. To enable this feature, set the system variable [`tidb_runtime_filter_mode`](/system-variables.md#tidb_runtime_filter_mode-new-in-v720) to `LOCAL`.

    For more information, see [documentation](/runtime-filter.md).

* TiFlash supports executing common table expressions (CTEs) (experimental) [#43333](https://github.com/pingcap/tidb/issues/43333) @[winoros](https://github.com/winoros)

    Before v7.3.0, the MPP engine of TiFlash cannot execute queries that contain CTEs by default. To achieve the best execution performance within the MPP framework, you need to use the system variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) to enforce inlining CTE.

    Starting from v7.3.0, TiFlash's MPP engine supports executing queries with CTEs without inlining them, allowing for optimal query execution within the MPP framework. In TPC-DS benchmark tests, compared with inlining CTEs, this feature has shown a 20% improvement in overall query execution speed for queries containing CTE.

    This feature is experimental and is disabled by default. It is controlled by the system variable [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720).

### Reliability

* Add new optimizer hints [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)

    In v7.3.0, TiDB introduces several new optimizer hints to control the join methods between tables, including:

    - [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) selects join methods other than merge join.
    - [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-) selects join methods other than index nested loop join.
    - [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-) selects join methods other than index nested loop merge join.
    - [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) selects join methods other than hash join.
    - [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) selects join methods other than [index nested loop hash join](/optimizer-hints.md#inl_hash_join).

  For more information, see [documentation](/optimizer-hints.md).

* Manually mark queries that use resources more than expected (experimental) [#43691](https://github.com/pingcap/tidb/issues/43691) @[Connor1996](https://github.com/Connor1996) @[CabinfeverB](https://github.com/CabinfeverB)

    In v7.2.0, TiDB automatically manages queries that use resources more than expected (Runaway Query) by automatically downgrading or canceling runaway queries. In actual practice, rules alone cannot cover all cases. Therefore, TiDB v7.3.0 introduces the ability to manually mark runaway queries. With the new command [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md), you can mark runaway queries based on SQL text, SQL Digest, or execution plan, and the marked runaway queries can be downgraded or cancelled.

    This feature provides an effective intervention method for sudden performance issues in the database. For performance issues caused by queries, before identifying the root cause, this feature can quickly alleviate its impact on overall performance, thereby improving system service quality.

    For more information, see [documentation](/tidb-resource-control.md#query-watch-parameters).

### SQL

* List and List COLUMNS partitioned tables support default partitions [#20679](https://github.com/pingcap/tidb/issues/20679) @[mjonss](https://github.com/mjonss) @[bb7133](https://github.com/bb7133)

    Before v7.3.0, when you use the `INSERT` statement to insert data into a List or List COLUMNS partitioned table, the data needs to meet the specified partitioning conditions of the table. If the data to be inserted does not meet any of these conditions, either the execution of the statement will fail or the non-compliant data will be ignored.

   Starting from v7.3.0, List and List COLUMNS partitioned tables support default partitions. After a default partition is created, if the data to be inserted does not meet any partitioning condition, it will be written to the default partition. This feature improves the usability of List and List COLUMNS partitioning, avoiding the execution failure of the `INSERT` statement or data being ignored due to data that does not meet partitioning conditions.

    Note that this feature is a TiDB extension to MySQL syntax. For a partitioned table with a default partition, the data in the table cannot be directly replicated to MySQL.

    For more information, see [documentation](/partitioned-table.md#list-partitioning).

### Observability

* Show the progress of collecting statistics [#44033](https://github.com/pingcap/tidb/issues/44033) @[hawkingrei](https://github.com/hawkingrei)

    Collecting statistics for large tables often takes a long time. In previous versions, you cannot see the progress of collecting statistics, and therefore cannot predict the completion time. TiDB v7.3.0 introduces a feature to show the progress of collecting statistics. You can view the overall workload, current progress, and estimated completion time for each subtask using the system table `mysql.analyze_jobs` or `SHOW ANALYZE STATUS`. In scenarios such as large-scale data import and SQL performance optimization, this feature helps you understand the overall task progress and improves the user experience.

    For more information, see [documentation](/sql-statements/sql-statement-show-analyze-status.md).

* Plan Replayer supports exporting historical statistics [#45038](https://github.com/pingcap/tidb/issues/45038) @[time-and-fate](https://github.com/time-and-fate)

    Starting from v7.3.0, with the newly added [`dump with stats as of timestamp`](/sql-plan-replayer.md) clause, you can use Plan Replayer to export the statistics of specified SQL-related objects at a specific point in time. During the diagnosis of execution plan issues, accurately capturing historical statistics can help analyze more precisely how the execution plan was generated at the time when the issue occurred. This helps identify the root cause of the issue and greatly improves efficiency in diagnosing execution plan issues.

    For more information, see [documentation](/sql-plan-replayer.md).

### Data migration

* TiDB Lightning introduces a new version of conflict data detection and handling strategy [#41629](https://github.com/pingcap/tidb/issues/41629) @[lance6716](https://github.com/lance6716)

    In previous versions, TiDB Lightning uses different conflict detection and handling methods for Logical Import Mode and Physical Import Mode, which are complex to configure and not easy for users to understand. In addition, Physical Import Mode cannot handle conflicts using the `replace` or `ignore` strategy. Starting from v7.3.0, TiDB Lightning introduces a unified conflict detection and handling strategy for both Logical Import Mode and Physical Import Mode. You can choose to report an error (`error`), replace (`replace`) or ignore (`ignore`) conflicting data when encountering conflicts. You can limit the number of conflict records, such as the task is interrupted and terminated after processing a specified number of conflict records. Furthermore, the system can record conflicting data for troubleshooting.

    For import data with many conflicts, it is recommended to use the new version of the conflict detection and handling strategy for better performance. In the lab environment, the new version strategy can improve the performance of conflict detection and handling up to three times faster than the old version. This performance value is for reference only. The actual performance might vary depending on your configuration, table structure, and the percentage of conflicting data. Note that the new version and the old version of the conflict strategy cannot be used at the same time. The old conflict detection and handling strategy will be deprecated in the future.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#conflict-detection).

* TiDB Lightning supports Partitioned Raft KV (experimental) [#14916](https://github.com/tikv/tikv/issues/14916) @[GMHDBJD](https://github.com/GMHDBJD)

    TiDB Lightning now supports Partitioned Raft KV. This feature helps improve the data import performance of TiDB Lightning.

* TiDB Lightning introduces a new parameter `enable-diagnose-log` to enhance troubleshooting by printing more diagnostic logs [#45497](https://github.com/pingcap/tidb/issues/45497) @[D3Hunter](https://github.com/D3Hunter)

    By default, this feature is disabled and TiDB Lightning only prints logs containing `lightning/main`. When enabled, TiDB Lightning prints logs for all packages (including `client-go` and `tidb`) to help diagnose issues related to `client-go` and `tidb`.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.2.0 to the current version (v7.3.0). If you are upgrading from v7.1.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* Backup & Restore (BR)

    - BR adds an empty cluster check before performing a full data restoration. By default, restoring data to a non-empty cluster is not allowed. If you want to force the restoration, you can use the `--filter` option to specify the corresponding table name to restore data to.

* TiDB Lightning

    - `tikv-importer.on-duplicate` is deprecated and replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).
    - The `max-error` parameter, which controls the maximum number of non-fatal errors that TiDB Lightning can tolerate before stopping the migration task, no longer limits import data conflicts. The [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) parameter now controls the maximum number of conflicting records that can be tolerated.

* TiCDC

    - When Kafka sink uses Avro protocol, if the `force-replicate` parameter is set to `true`, TiCDC reports an error when creating a changefeed.
    - Due to incompatibility between `delete-only-output-handle-key-columns` and `force-replicate` parameters, when both parameters are enabled, TiCDC reports an error when creating a changefeed.
    - When the output protocol is Open Protocol, the `UPDATE` events only output the changed columns.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_opt_enable_mpp_shared_cte_execution`](/system-variables.md#tidb_opt_enable_mpp_shared_cte_execution-new-in-v720) | Modified | This system variable takes effect starting from v7.3.0. It controls whether non-recursive Common Table Expressions (CTEs) can be executed in TiFlash MPP. |
| [`tidb_lock_unchanged_keys`](/system-variables.md#tidb_lock_unchanged_keys-new-in-v711-and-v730) | Newly added | This variable is used to control in certain scenarios whether to lock the keys that are involved but not modified in a transaction. |
| [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) | Newly added | Controls whether the `EXPLAIN` statement disables the execution of constant subqueries that can be expanded at the optimization stage.  |
| [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730) | Newly added | This variable controls the generation of GlobalStats when partition statistics are missing. |
| [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730) | Newly added | Controls the strategy for selecting TiFlash replicas when a query requires the TiFlash engine. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) | Newly added | Controls whether to enable the 32-bit connection ID feature. |
| TiDB | [`in-mem-slow-query-recent-num`](/tidb-configuration-file.md#in-mem-slow-query-recent-num-new-in-v730) | Newly added | Controls the number of recently used slow queries that are cached in memory. |
| TiDB | [`in-mem-slow-query-topn-num`](/tidb-configuration-file.md#in-mem-slow-query-topn-num-new-in-v730) | Newly added | Controls the number of slowest queries that are cached in memory. |
| TiKV | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610) | Modified | Changes the default value from `96MiB` to `50MiB`. |
| TiKV | [`raft-engine.format-version`](/tikv-configuration-file.md#format-version-new-in-v630) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), Ribbon filter is used. Therefore, TiKV changes the default value from `2` to `5`. |
| TiKV | [`raftdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size-1) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV skips writing WAL. Therefore, TiKV changes the default value from `"4GB"` to `1`, meaning that WAL is disabled. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].compaction-guard-min-output-file-size</code>](/tikv-configuration-file.md#compaction-guard-min-output-file-size) | Modified | Changes the default value from `"1MB"` to `"8MB"` to resolve the issue that compaction speed cannot keep up with the write speed during large data writes. |
| TiKV | [<code>rocksdb.\[defaultcf\|writecf\|lockcf\].format-version</code>](/tikv-configuration-file.md#format-version-new-in-v620) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), Ribbon filter is used. Therefore, TiKV changes the default value from `2` to `5`. |
| TiKV | [`rocksdb.lockcf.write-buffer-size`](/tikv-configuration-file.md#write-buffer-size) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to speed up compaction on lockcf, TiKV changes the default value from `"32MB"` to `"4MB"`. |
| TiKV | [`rocksdb.max-total-wal-size`](/tikv-configuration-file.md#max-total-wal-size) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV skips writing WAL. Therefore, TiKV changes the default value from `"4GB"` to `1`, meaning that WAL is disabled. |
| TiKV | [`rocksdb.stats-dump-period`](/tikv-configuration-file.md#stats-dump-period) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to disable redundant log printing, changes the default value from `"10m"` to `"0"`. |
| TiKV | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660) | Modified | To reduce the memory overhead of memtables, when `storage.engine="raft-kv"`, TiKV changes the default value from 25% of the memory of the machine to `0`, which means no limit. When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), TiKV changes the default value from 25% to 20% of the memory of the machine. |
| TiKV | [`storage.block-cache.capacity`](/tikv-configuration-file.md#capacity) | Modified | When using Partitioned Raft KV (`storage.engine="partitioned-raft-kv"`), to compensate for the memory overhead of memtables, TiKV changes the default value from 45% to 30% of the size of total system memory. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | Modified | Introduces a new DTFile format `format_version = 5` to reduce the number of physical files by merging smaller files. Note that this format is experimental and not enabled by default. |
| TiDB Lightning  | `tikv-importer.incremental-import` | Deleted | TiDB Lightning parallel import parameter. Because it could easily be mistaken as an incremental import parameter, this parameter is now renamed to `tikv-importer.parallel-import`. If a user passes in the old parameter name, it will be automatically converted to the new one. |
| TiDB Lightning  | `tikv-importer.on-duplicate` | Deprecated | Controls action to do when trying to insert a conflicting record in the logical import mode. Starting from v7.3.0, this parameter is replaced by [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). |
| TiDB Lightning | [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | The new version of strategy to handle conflicting data. It controls the maximum number of rows in the `conflict_records` table. The default value is 100. |
| TiDB Lightning  | [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | The new version of strategy to handle conflicting data. It includes the following options: "" (TiDB Lightning does not detect and process conflicting data), `error` (terminate the import and report an error if a primary or unique key conflict is detected in the imported data), `replace` (when encountering data with conflicting primary or unique keys, the new data is retained and the old data is overwritten.), `ignore` (when encountering data with conflicting primary or unique keys, the old data is retained and the new data is ignored.). The default value is "", that is, TiDB Lightning does not detect and process conflicting data. |
| TiDB Lightning  | [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls the upper limit of the conflicting data. When `conflict.strategy="error"`, the default value is `0`. When `conflict.strategy="replace"` or `conflict.strategy="ignore"`, you can set it as a maxint. |
| TiDB Lightning  | [`enable-diagnose-logs`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls whether to enable the diagnostic logs. The default value is `false`, that is, only the logs related to the import are output, and the logs of other dependent components are not output. When you set it to `true`, logs from both the import process and other dependent components are output, and GRPC debugging is enabled, which can be used for diagnosis. |
|TiDB Lightning  | [`tikv-importer.parallel-import`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | TiDB Lightning parallel import parameter. It replaces the existing `tikv-importer.incremental-import` parameter, which could be mistaken as an incremental import parameter and misused. |
|BR  | `azblob.encryption-scope` | Newly added | BR provides encryption scope support for Azure Blob Storage. |
|BR  | `azblob.encryption-key` | Newly added | BR provides encryption key support for Azure Blob Storage. |
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) | Newly added | Empty by default, which means that when the message size exceeds the limit of Kafka topic, the changefeed fails. When this configuration is set to `"handle-key-only"`, if the message exceeds the size limit, only the handle key will be sent to reduce the message size; if the reduced message still exceeds the limit, then the changefeed fails. |
| TiCDC | [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | The encoding method of binary data, which can be `'base64'` or `'hex'`. The default value is `'base64'`. |

### System tables

- Add a new system table `mysql.tidb_timers` to store the metadata of internal timers.

## Deprecated features

* TiDB

    - The [`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze) feature (experimental) for statistics will be deprecated in v7.5.0.
    - The [incremental collection](/statistics.md#incremental-collection) feature for statistics will be deprecated in v7.5.0.

## Improvements

+ TiDB

    - Introduce a new system variable [`tidb_opt_enable_non_eval_scalar_subquery`](/system-variables.md#tidb_opt_enable_non_eval_scalar_subquery-new-in-v730) to control whether the `EXPLAIN` statement executes subqueries in advance during the optimization phase [#22076](https://github.com/pingcap/tidb/issues/22076) @[winoros](https://github.com/winoros)
    - When [Global Kill](/tidb-configuration-file.md#enable-global-kill-new-in-v610) is enabled, you can terminate the current session by pressing <kbd>Control+C</kbd> [#8854](https://github.com/pingcap/tidb/issues/8854) @[pingyu](https://github.com/pingyu)
    - Support the `IS_FREE_LOCK()` and `IS_USED_LOCK()` locking functions [#44493](https://github.com/pingcap/tidb/issues/44493) @[dveeden](https://github.com/dveeden)
    - Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - Optimize the overestimation issue of the inner table of Index Join by using Optimizer Fix Controls [#44855](https://github.com/pingcap/tidb/issues/44855) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get-region-read-progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ PD

    - Support blocking the Swagger API by default when the Swagger server is not enabled [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    - Improve the high availability of etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    - Reduce the memory consumption of `GetRegions` requests [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Support a new DTFile format version [`storage.format_version = 5`](/tiflash/tiflash-configuration.md) to reduce the number of physical files (experimental) [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - When backing up data to Azure Blob Storage using BR, you can specify either an encryption scope or an encryption key for server-side encryption [#45025](https://github.com/pingcap/tidb/issues/45025) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Optimize the message size of the Open Protocol output to make it include only the updated column values when sending `UPDATE` events [#9336](https://github.com/pingcap/tiflow/issues/9336) @[3AceShowHand](https://github.com/3AceShowHand)
        - Storage Sink now supports hexadecimal encoding for HEX formatted data, making it compatible with AWS DMS format specifications [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Kafka Sink supports [sending only handle key data](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) when the message is too large, reducing the size of the message [#9382](https://github.com/pingcap/tiflow/issues/9382) @[3AceShowHand](https://github.com/3AceShowHand)

## Bug fixes

+ TiDB

    - Fix the issue that when the MySQL Cursor Fetch protocol is used, the memory consumption of result sets might exceed the `tidb_mem_quota_query` limit and causes TiDB OOM. After the fix, TiDB will automatically write result sets to the disk to release memory [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - Fix the TiDB panic issue caused by data race [#45561](https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)
    - Fix the hang-up issue that occurs when queries with `indexMerge` are killed [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that query results in MPP mode are incorrect when `tidb_enable_parallel_apply` is enabled [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - Fix the issue that `resolve lock` might hang when there is a sudden change in PD time [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the GC Resolve Locks step might miss some pessimistic locks [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the query with `ORDER BY` returns incorrect results in dynamic pruning mode [#45007](https://github.com/pingcap/tidb/issues/45007) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `AUTO_INCREMENT` can be specified on the same column with the `DEFAULT` column value [#45136](https://github.com/pingcap/tidb/issues/45136) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that querying the system table `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns incorrect results in some cases [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue of incorrect partition table pruning in some cases [#42273](https://github.com/pingcap/tidb/issues/42273) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that global indexes are not cleared when truncating partition of a partitioned table [#42435](https://github.com/pingcap/tidb/issues/42435) @[L-maple](https://github.com/L-maple)
    - Fix the issue that other TiDB nodes do not take over TTL tasks after failures in one TiDB node [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the memory leak issue when TTL is running [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue of inaccurate error messages when inserting data into partitioned tables [#44966](https://github.com/pingcap/tidb/issues/44966) @[lilinghai](https://github.com/lilinghai)
    - Fix the read permission issue on the `INFORMATION_SCHEMA.TIFLASH_REPLICA` table [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that an error occurs when using a wrong partition table name [#44967](https://github.com/pingcap/tidb/issues/44967) @[River2000i](https://github.com/River2000i)
    - Fix the issue that creating indexes gets stuck when `tidb_enable_dist_task` is enabled in some cases [#44440](https://github.com/pingcap/tidb/issues/44440) @[tangenta](https://github.com/tangenta)
    - Fix the `duplicate entry` error that occurs when restoring a table with `AUTO_ID_CACHE=1` using BR [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the time consumed for executing `TRUNCATE TABLE` is inconsistent with the task execution time shown in `ADMIN SHOW DDL JOBS` [#44785](https://github.com/pingcap/tidb/issues/44785) @[tangenta](https://github.com/tangenta)
    - Fix the issue that upgrading TiDB gets stuck when reading metadata takes longer than one DDL lease [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the query result of the `SELECT CAST(n AS CHAR)` statement is incorrect when `n` in the statement is a negative number [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - Fix the issue that queries might return incorrect results when `tidb_opt_agg_push_down` is enabled [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue of wrong results that occurs when a query with `current_date()` uses plan cache [#45086](https://github.com/pingcap/tidb/issues/45086) @[qw4990](https://github.com/qw4990)

+ TiKV

    - Fix the issue that reading data during GC might cause TiKV panic in some rare cases [#15109](https://github.com/tikv/tikv/issues/15109) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue that restarting PD might cause the `default` resource group to be reinitialized [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    - Fix the issue that when etcd is already started but the client has not yet connected to it, calling the client might cause PD to panic [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the `health-check` output of a Region is inconsistent with the Region information returned by querying the Region ID [#6560](https://github.com/tikv/pd/issues/6560) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that failed learner peers in `unsafe recovery` are ignored in `auto-detect` mode [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that Placement Rules select TiFlash learners that do not meet the rules [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    - Fix the issue that unhealthy peers cannot be removed when rule checker selects peers [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Fix the issue that TiFlash cannot replicate partitioned tables successfully due to deadlocks [#7758](https://github.com/pingcap/tiflash/issues/7758) @[hongyunyan](https://github.com/hongyunyan)
    - Fix the issue that the `INFORMATION_SCHEMA.TIFLASH_REPLICA` system table contains tables that users do not have privileges to access [#7795](https://github.com/pingcap/tiflash/issues/7795) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that when there are multiple HashAgg operators within the same MPP task, the compilation of the MPP task might take an excessively long time, severely affecting query performance [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + TiCDC

        - Fix the issue that changefeeds would fail due to the temporary unavailability of PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - Fix the data inconsistency issue that might occur when some TiCDC nodes are isolated from the network [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that when Kafka Sink encounters errors it might indefinitely block changefeed progress [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - Fix the panic issue that might occur when the TiCDC node status changes [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - Fix the encoding error for the default `ENUM` values [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - Fix the issue that executing checksum after TiDB Lightning completes import might get SSL errors [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that in Logical Import Mode, deleting tables downstream during import might cause TiDB Lightning metadata not to be updated in time [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [charleszheng44](https://github.com/charleszheng44)
- [dhysum](https://github.com/dhysum)
- [haiyux](https://github.com/haiyux)
- [Jiang-Hua](https://github.com/Jiang-Hua)
- [Jille](https://github.com/Jille)
- [jiyfhust](https://github.com/jiyfhust)
- [krishnaduttPanchagnula](https://github.com/krishnaduttPanchagnula)
- [L-maple](https://github.com/L-maple)
- [pingandb](https://github.com/pingandb)
- [testwill](https://github.com/testwill)
- [tisonkun](https://github.com/tisonkun)
- [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
- [yumchina](https://github.com/yumchina)
