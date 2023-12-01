---
title: TiDB 7.5.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.5.0.
---

# TiDB 7.5.0 Release Notes

Release date: December 1, 2023

TiDB version: 7.5.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.5.0#version-list)

TiDB 7.5.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 7.1.0, 7.5.0 includes new features, improvements, and bug fixes released in [7.2.0-DMR](/releases/release-7.2.0.md), [7.3.0-DMR](/releases/release-7.3.0.md), and [7.4.0-DMR](/releases/release-7.4.0.md). When you upgrade from 7.1.x to 7.5.0, you can download the [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v7.2-to-v7.5-en-release-notes.pdf) to view all release notes between the two LTS versions. The following table lists some highlights from 7.2.0 to 7.5.0:

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
    <td>Support running multiple <code>ADD INDEX</code> statements in parallel</td>
    <td>This feature allows for concurrent jobs to add multiple indexes for a single table. Previously, it would take the time of X plus the time of Y to execute two <code>ADD INDEX</code> statements simultaneously (X and Y). With this feature, adding two indexes X and Y in one SQL can be concurrently executed, and the total execution time of DDL is significantly reduced. Especially in scenarios with wide tables, internal test data shows that performance can be improved by up to 94%.</td>
  </tr>
  <tr>
    <td rowspan="3">Reliability and Availability</td>
    <td>Optimize <a href="https://docs.pingcap.com/tidb/v7.5/tidb-global-sort" target="_blank">Global Sort</a> (experimental, introduced in v7.4.0)</td>
    <td>TiDB v7.2.0 introduced the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed execution framework</a>. For tasks that take advantage of this framework, v7.4 introduces global sorting to eliminate the unnecessary I/O, CPU, and memory spikes caused by temporarily out-of-order data during data re-organization tasks. The global sorting takes advantage of external shared object storage (Amazon S3 in this first iteration) to store intermediary files during the job, adding flexibility and cost savings. Operations like <code>ADD INDEX</code> and <code>IMPORT INTO</code> will be faster, more resilient, more stable, more flexible, and cost less to run.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-background-tasks" target="_blank">Resource control for background tasks</a> (experimental, introduced in v7.4.0)</td>
    <td>In v7.1.0, the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">Resource Control</a> feature was introduced to mitigate resource and storage access interference between workloads. TiDB v7.4.0 applied this control to the priority of background tasks as well. In v7.4.0, Resource Control now identifies and manages the priority of background task execution, such as auto-analyze, Backup & Restore, bulk load with TiDB Lightning, and online DDL. In future releases, this control will eventually apply to all background tasks.</td>
  </tr>
  <tr>
    <td>Resource control for <a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control#manage-queries-that-consume-more-resources-than-expected-runaway-queries"> managing runaway queries</a> (experimental, introduced in v7.2.0)</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.5/tidb-resource-control" target="_blank">Resource Control</a> is a framework for resource-isolating workloads by Resource Groups, but it makes no calls on how individual queries affect work inside of each group. TiDB v7.2.0 introduces "runaway queries control" to let you control how TiDB identifies and treats these queries per Resource Group. Depending on needs, long running queries might be terminated or throttled, and the queries can be identified by exact SQL text, SQL digests or their plan digests, for better generalization. In v7.3.0, TiDB enables you to proactively watch for known bad queries, similar to a SQL blocklist at the database level.</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td>MySQL 8.0 compatibility (introduced in v7.4.0)</td>
    <td>In MySQL 8.0, the default character set is utf8mb4, and the default collation of utf8mb4 is <code>utf8mb4_0900_ai_ci</code>. TiDB v7.4.0 adding support for this enhances compatibility with MySQL 8.0 so that migrations and replications from MySQL 8.0 databases with the default collation are now much smoother.</td>
  </tr>
  <tr>
    <td rowspan="4">DB Operations and Observability</td>
    <td>TiDB Lightning's physical import mode integrated into TiDB with <a href="https://docs.pingcap.com/tidb/v7.5/sql-statement-import-into"><code>IMPORT INTO</code></a> (GA)</td>
    <td>Before v7.2.0, to import data based on the file system, you needed to install <a href="https://docs.pingcap.com/tidb/v7.5/tidb-lightning-overview">TiDB Lightning</a> and used its physical import mode. Now, the same capability is integrated into the <code>IMPORT INTO</code> statement so you can use this statement to quickly import data without installing any additional tool. This statement also supports the <a href="https://docs.pingcap.com/tidb/v7.5/tidb-distributed-execution-framework" target="_blank">distributed execution framework</a> for parallel import, which improves import efficiency during large-scale imports.</td>
  </tr>
  <tr>
    <td>Specify <a href="https://docs.pingcap.com/tidb/v7.5/system-variables#tidb_service_scope-new-in-v740" target="_blank">the respective TiDB nodes</a> to execute the <code>ADD INDEX</code> and <code>IMPORT INTO</code> SQL statements (GA)</td>
    <td>You have the flexibility to specify whether to execute <code>ADD INDEX</code> or <code>IMPORT INTO</code> SQL statements on some of the existing TiDB nodes or newly added TiDB nodes. This approach enables resource isolation from the rest of the TiDB nodes, preventing any impact on business operations while ensuring optimal performance for executing the preceding SQL statements. In v7.5.0, this feature becomes generally available (GA).</td>
  </tr>
  <tr>
    <td>DDL supports <a href="https://docs.pingcap.com/tidb/v7.5/ddl-introduction#ddl-related-commands">pause and resume operations</a> (GA)</td>
    <td>Adding indexes can be big resource consumers and can affect online traffic. Even when throttled in a Resource Group or isolated to labeled nodes, there may still be a need to suspend these jobs in emergencies. As of v7.2.0, TiDB now natively supports suspending any number of these background jobs at once, freeing up needed resources while avoiding having to cancel and restart the jobs.</td>
  </tr>
  <tr>
    <td>TiDB Dashboard supports heap profiling for TiKV<a href="https://docs.pingcap.com/tidb/v7.5/dashboard-profiling" target="_blank"></a></td>
    <td>Previously, addressing TiKV OOM or high memory usage issues typically required manual execution of <code>jeprof</code> to generate a heap profile in the instance environment. Starting from v7.5.0, TiKV enables remote processing of heap profiles. You can now directly access the flame graph and call graph of heap profile. This feature provides the same simple and easy-to-use experience as Go heap profiling.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Support designating and isolating TiDB nodes to distributedly execute `ADD INDEX` or `IMPORT INTO` tasks when the distributed execution framework is enabled [#46258](https://github.com/pingcap/tidb/issues/46258) @[ywqzzy](https://github.com/ywqzzy)

    Executing `ADD INDEX` or `IMPORT INTO` tasks in parallel in a resource-intensive cluster can consume a large amount of TiDB node resources, which can lead to cluster performance degradation. To avoid performance impact on existing services, v7.4.0 introduces the system variable [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) as an experimental feature to control the service scope of each TiDB node under the [TiDB backend task distributed execution framework](/tidb-distributed-execution-framework.md). You can select several existing TiDB nodes or set the TiDB service scope for new TiDB nodes, and all distributedly executed `ADD INDEX` and `IMPORT INTO` tasks only run on these nodes. In v7.5.0, this feature becomes generally available (GA).

    For more information, see [documentation](/system-variables.md#tidb_service_scope-new-in-v740).

### Performance

* The TiDB backend task distributed execution framework becomes generally available (GA), improving the performance and stability of `ADD INDEX` and `IMPORT INTO` tasks in parallel execution [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016)

    The backend task distributed execution framework introduced in v6.6.0 has become GA. In versions before TiDB v7.1.0, only one TiDB node can execute DDL tasks at the same time. Starting from v7.1.0, multiple TiDB nodes can execute the same DDL task in parallel under the backend task distributed execution framework. Starting from v7.2.0, the backend task distributed execution framework supports multiple TiDB nodes to execute the same `IMPORT INTO` task in parallel, thereby better utilizing the resources of the TiDB cluster and significantly improving the performance of DDL and `IMPORT INTO` tasks. In addition, you can also increase TiDB nodes to linearly improve the performance of these tasks.

    To use the backend task distributed execution framework, set [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) value to `ON`.

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    For more information, see [documentation](/tidb-global-sort.md).

* Improve the performance of adding multiple indexes in a single SQL statement [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta)

    Before v7.5.0, when you add multiple indexes (`ADD INDEX`) in a single SQL statement, the performance was similar to adding multiple indexes using separate SQL statements. Starting from v7.5.0, the performance of adding multiple indexes in a single SQL statement is significantly improved. Especially in scenarios with wide tables, internal test data shows that performance can be improved by up to 94%.

### DB operations

* DDL jobs support pause and resume operations (GA) [#18015](https://github.com/pingcap/tidb/issues/18015) @[godouxm](https://github.com/godouxm)

    The pause and resume operations for DDL jobs introduced in v7.2.0 become generally available (GA). These operations let you pause resource-intensive DDL jobs (such as creating indexes) to save resources and minimize the impact on online traffic. When resources permit, you can seamlessly resume DDL jobs without canceling and restarting them. This feature improves resource utilization, enhances user experience, and simplifies the schema change process.

    You can pause and resume multiple DDL jobs using `ADMIN PAUSE DDL JOBS` or `ADMIN RESUME DDL JOBS`:

    ```sql
    ADMIN PAUSE DDL JOBS 1,2;
    ADMIN RESUME DDL JOBS 1,2;
    ```

    For more information, see [documentation](/ddl-introduction.md#ddl-related-commands).

* BR supports backing up and restoring statistics [#48008](https://github.com/pingcap/tidb/issues/48008) @[Leavrth](https://github.com/Leavrth)

    Starting from TiDB v7.5.0, the br command-line tool introduces the `--ignore-stats` parameter to back up and restore database statistics. When you set this parameter to `false`, the br command-line tool supports backing up and restoring statistics of columns, indexes, and tables. In this case, you do not need to manually run the statistics collection task for the TiDB database restored from the backup, or wait for the completion of automatic collection tasks. This feature simplifies database maintenance work and improves query performance.

    For more information, see [documentation](/br/br-snapshot-manual.md#back-up-statistics).

### Observability

* TiDB Dashboard supports heap profiling for TiKV [#15927](https://github.com/tikv/tikv/issues/15927) @[Connor1996](https://github.com/Connor1996)

    Previously, addressing TiKV OOM or high memory usage issues typically required manual execution of `jeprof` to generate a heap profile in the instance environment. Starting from v7.5.0, TiKV enables remote processing of heap profiles. You can now directly access the flame graph and call graph of heap profile. This feature provides the same simple and easy-to-use experience as Go heap profiling.

    For more information, see [documentation](/dashboard/dashboard-profiling.md).

### Data migration

* Support the `IMPORT INTO` SQL statement (GA) [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)

    In v7.5.0, the `IMPORT INTO` SQL statement becomes generally available (GA). This statement integrates the [Physical Import Mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) capability of TiDB Lightning and allows you to quickly import data in formats such as CSV, SQL, and PARQUET into an empty table in TiDB. This import method eliminates the need for a separate deployment and management of TiDB Lightning, thereby reducing the complexity of data import and greatly improving import efficiency.

    For more information, see [documentation](/sql-statements/sql-statement-import-into.md).

* Data Migration (DM) supports blocking incompatible (data-consistency-corrupting) DDL changes [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD)

    Before v7.5.0, the DM Binlog Filter feature can only migrate or filter specified events, and the granularity is relatively coarse. For example, it can only filter large granularity of DDL events such as `ALTER`. This method is limited in some scenarios. For example, the application allows `ADD COLUMN` but not `DROP COLUMN`, but they are both filtered by `ALTER` events in the earlier DM versions.

    To address such issues, v7.5.0 refines the granularity of the supported DDL events, such as support filtering `MODIFY COLUMN` (modify the column data type), `DROP COLUMN`, and other fine-grained DDL events that lead to data loss, truncation of data, and loss of precision. You can configure it as needed. This feature also supports blocking incompatible DDL changes and reporting errors for such changes, so that you can intervene manually in time to avoid impacting downstream application data.

    For more information, see [documentation](/dm/dm-binlog-event-filter.md#parameter-descriptions).

* Support real-time checkpoint updates for continuous data validation [#8463](https://github.com/pingcap/tiflow/issues/8463) @[lichunzhu](https://github.com/lichunzhu)

    Before v7.5.0, the [continuous data validation feature](/dm/dm-continuous-data-validation.md) ensures the data consistency during replication from DM to downstream. This serves as the basis for cutting over business traffic from the upstream database to TiDB. However, due to various factors such as replication delay and waiting for re-validation of inconsistent data, the continuous validation checkpoint must be refreshed every few minutes. This is unacceptable for some business scenarios where the cutover time is limited to tens of seconds.

    With the introduction of real-time updating of checkpoint for continuous data validation, you can now provide the binlog position from the upstream database. Once the continuous validation program detects this binlog position in memory, it immediately refreshes the checkpoint instead of refreshing it every few minutes. Therefore, you can quickly perform cut-off operations based on this immediately updated checkpoint.

    For more information, see [documentation](/dm/dm-continuous-data-validation.md#set-the-cutover-point-for-continuous-data-validation).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.4.0 to the current version (v7.5.0). If you are upgrading from v7.3.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### System variables

| Variable name  | Change type    |  Description |
|--------|------------------------------|------|
| [`tidb_enable_fast_analyze`](/system-variables.md#tidb_enable_fast_analyze) | Deprecated | Controls whether to enable the statistics `Fast Analyze` feature. This feature is deprecated in v7.5.0. |
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) |  Modified | Changes the default value from `1` to `2` after further tests. |
| [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency) | Modified | Changes the default value from `4` to `2` after further tests. |
| [`tidb_merge_partition_stats_concurrency`](/system-variables.md#tidb_merge_partition_stats_concurrency)    |  Modified | This system variable takes effect starting from v7.5.0. It specifies the concurrency of merging statistics for a partitioned table when TiDB analyzes the partitioned table. |
| [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) | Newly added | Controls the sampling concurrency of the `ANALYZE` process. |
| [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) | Newly added | This variable is used by TiDB to merge statistics asynchronously to avoid OOM issues. |
| [`tidb_gogc_tuner_max_value`](/system-variables.md#tidb_gogc_tuner_max_value-new-in-v750) | Newly added | Controls the maximum value of GOGC that the GOGC Tuner can adjust. |
| [`tidb_gogc_tuner_min_value`](/system-variables.md#tidb_gogc_tuner_min_value-new-in-v750) | Newly added | Controls the minimum value of GOGC that the GOGC Tuner can adjust.|

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`raftstore.region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) | Modified | Sets the number of redundant MVCC rows required to trigger RocksDB compaction. Starting from v7.5.0, this configuration item takes effect for the `"raft-kv"` storage engine. |
| TiKV | [`raftstore.region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | Modified | Sets the percentage of redundant MVCC rows required to trigger RocksDB compaction. Starting from v7.5.0, this configuration item takes effect for the `"raft-kv"` storage engine. |
| TiKV | [`raftstore.evict-cache-on-memory-ratio`](/tikv-configuration-file.md#evict-cache-on-memory-ratio-new-in-v750) | Newly added | When the memory usage of TiKV exceeds 90% of the system available memory, and the memory occupied by Raft entry cache exceeds the `evict-cache-on-memory-ratio` of used memory, TiKV evicts the Raft entry cache. |
| TiKV | [`memory.enable-heap-profiling`](/tikv-configuration-file.md#enable-heap-profiling-new-in-v750) | Newly added | Controls whether to enable Heap Profiling to track the memory usage of TiKV. |
| TiKV | [`memory.profiling-sample-per-bytes`](/tikv-configuration-file.md#profiling-sample-per-bytes-new-in-v750) | Newly added | Specifies the amount of data sampled by Heap Profiling each time, rounding up to the nearest power of 2. |
| BR | [`--ignore-stats`](/br/br-snapshot-manual.md#back-up-statistics) | Newly added | Controls whether to back up and restore database statistics. When you set this parameter to `false`, the br command-line tool supports backing up and restoring statistics of columns, indexes, and tables. |
| TiCDC | [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) | Modified | Changes the default value from `true` to `false` after further tests, which means that the table names and database names in the TiCDC configuration file are case-insensitive by default. |
| TiCDC | [`sink.dispatchers.partition`](/ticdc/ticdc-changefeed-config.md) | Modified | Controls how TiCDC dispatches incremental data to Kafka partitions. v7.5.0 introduces a new value option `columns`, which uses the explicitly specified column values to calculate the partition number. |
| TiCDC | [`sink.column-selectors`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls the specified columns of data change events that TiCDC sends to Kafka when dispatching incremental data. |
| TiCDC | [`sql-mode`](/ticdc/ticdc-changefeed-config.md) | Newly added | Specifies the SQL mode used by TiCDC when parsing DDL statements. The default value is the same as the default SQL mode of TiDB. |
| TiDB Lightning | `--importer` | Deleted | Specifies the address of TiKV-importer, which is deprecated in v7.5.0. |

## Offline package changes

Starting from v7.5.0, the following contents are removed from the `TiDB-community-toolkit` [binary package](/binary-package.md):

- `tikv-importer-{version}-linux-{arch}.tar.gz`
- `mydumper`
- `spark-{version}-any-any.tar.gz`
- `tispark-{version}-any-any.tar.gz`

## Deprecated features

* [Mydumper](https://docs.pingcap.com/tidb/v4.0/mydumper-overview) is deprecated in v7.5.0 and most of its features have been replaced by [Dumpling](/dumpling-overview.md). It is strongly recommended that you use Dumpling instead of Mydumper.

* TiKV-importer is deprecated in v7.5.0. It is strongly recommended that you use the [Physical Import Mode of TiDB Lightning](/tidb-lightning/tidb-lightning-physical-import-mode.md) as an alternative.

* Starting from TiDB v7.5.0, technical support for the data replication feature of [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is no longer provided. It is strongly recommended to use [TiCDC](/ticdc/ticdc-overview.md) as an alternative solution for data replication. Although TiDB Binlog v7.5.0 still supports the Point-in-Time Recovery (PITR) scenario, this component will be completely deprecated in future versions. It is recommended to use [PITR](/br/br-pitr-guide.md) as an alternative solution for data recovery.

* The [`Fast Analyze`](/system-variables.md#tidb_enable_fast_analyze) feature (experimental) for statistics is deprecated in v7.5.0.

* The [incremental collection](https://docs.pingcap.com/tidb/v7.4/statistics#incremental-collection) feature (experimental) for statistics is deprecated in v7.5.0.

## Improvements

+ TiDB

    - Optimize the concurrency model of merging GlobalStats: introduce [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-new-in-v750) to enable simultaneous loading and merging of statistics, which speeds up the generation of GlobalStats on partitioned tables. Optimize the memory usage of merging GlobalStats to avoid OOM and reduce memory allocations. [#47219](https://github.com/pingcap/tidb/issues/47219) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the `ANALYZE` process: introduce [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750) to better control the `ANALYZE` concurrency to reduce resource consumption. Optimize the memory usage of `ANALYZE` to reduce memory allocation and avoid frequent GC by reusing some intermediate results. [#47275](https://github.com/pingcap/tidb/issues/47275) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize the use of placement policies: support configuring the range of a policy to global and improve the syntax support for common scenarios. [#45384](https://github.com/pingcap/tidb/issues/45384) @[nolouch](https://github.com/nolouch)
    - Improve the performance of adding indexes with `tidb_ddl_enable_fast_reorg` enabled. In internal tests, v7.5.0 improves the performance by up to 62.5% compared with v6.5.0. [#47757](https://github.com/pingcap/tidb/issues/47757) @[tangenta](https://github.com/tangenta)

+ TiKV

    - Avoid holding mutex when writing Titan manifest files to prevent affecting other threads [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)

+ PD

    - Improve the stability and usability of the `evict-slow-trend` scheduler [#7156](https://github.com/tikv/pd/issues/7156) @[LykxSassinato](https://github.com/LykxSassinator)

+ Tools

    + Backup & Restore (BR)

        - Add a new inter-table backup parameter `table-concurrency` for snapshot backups. This parameter is used to control the inter-table concurrency of meta information such as statistics backup and data validation [#48571](https://github.com/pingcap/tidb/issues/48571) @[3pointer](https://github.com/3pointer)
        - During restoring a snapshot backup, BR retries when it encounters certain network errors [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)

## Bug fixes

+ TiDB

    - Prohibit split table operations on non-integer clustered indexes [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - Fix the issue of encoding time fields with incorrect timezone information [#46033](https://github.com/pingcap/tidb/issues/46033) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the Sort operator might cause TiDB to crash during the spill process [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiDB returns `Can't find column` for queries with `GROUP_CONCAT` [#41957](https://github.com/pingcap/tidb/issues/41957) @[AilinKid](https://github.com/AilinKid)
    - Fix the panic issue of `batch-client` in `client-go` [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue of incorrect memory usage estimation in `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue of uneven workload caused by the rejoining of a TiFlash node that has been offline for a long time [#35418](https://github.com/pingcap/tidb/issues/35418) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the chunk cannot be reused when the HashJoin operator performs probe [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `COALESCE()` function returns incorrect result type for `DATE` type parameters [#46475](https://github.com/pingcap/tidb/issues/46475) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that `UPDATE` statements with subqueries are incorrectly converted to PointGet [#48171](https://github.com/pingcap/tidb/issues/48171) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that incorrect results are returned when the cached execution plans contain the comparison between date types and `unix_timestamp` [#48165](https://github.com/pingcap/tidb/issues/48165) @[qw4990](https://github.com/qw4990)
    - Fix the issue that an error is reported when default inline common table expressions (CTEs) with aggregate functions or window functions are referenced by recursive CTEs [#47881](https://github.com/pingcap/tidb/issues/47881) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that the optimizer mistakenly selects IndexFullScan to reduce sort introduced by window functions [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - Fix the issue that multiple references to CTEs result in incorrect results due to condition pushdown of CTEs [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - Fix the issue that the MySQL compression protocol cannot handle large loads of data (>=16M) [#47152](https://github.com/pingcap/tidb/issues/47152) [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @[dveeden](https://github.com/dveeden)
    - Fix the issue that TiDB does not read `cgroup` resource limits when it is started with `systemd` [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV

    - Fix the issue that retrying prewrite requests in the pessimistic transaction mode might cause the risk of data inconsistency in rare cases [#11187](https://github.com/tikv/tikv/issues/11187) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue that `evict-leader-scheduler` might lose configuration [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that after a store goes offline, the monitoring metric of its statistics is not deleted [#7180](https://github.com/tikv/pd/issues/7180) @[rleungx](https://github.com/rleungx)
    - Fix the issue that `canSync` and `hasMajority` might be calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode when the configuration of Placement Rules is complex [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - Fix the issue that the rule checker does not add Learners according to the configuration of Placement Rules [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - Fix the issue that TiDB Dashboard cannot read PD `trace` data correctly [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - Fix the issue that PD might panic due to empty Regions obtained internally [#7261](https://github.com/tikv/pd/issues/7261) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that `available_stores` is calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - Fix the issue that PD might delete normal Peers when TiKV nodes are unavailable [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that adding multiple TiKV nodes to a large cluster might cause TiKV heartbeat reporting to become slow or stuck [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that the `UPPER()` and `LOWER()` functions return inconsistent results between TiDB and TiFlash [#7695](https://github.com/pingcap/tiflash/issues/7695) @[windtalker](https://github.com/windtalker)
    - Fix the issue that executing queries on empty partitions causes query failure [#8220](https://github.com/pingcap/tiflash/issues/8220) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the panic issue caused by table creation failure when replicating TiFlash replicas [#8217](https://github.com/pingcap/tiflash/issues/8217) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that PITR might skip restoring the `CREATE INDEX` DDL statement [#47482](https://github.com/pingcap/tidb/issues/47482) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the log backup might get stuck in some scenarios when backing up large wide tables [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the performance issue caused by accessing NFS directories when replicating data to an object store sink [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the storage path is misspelled when `claim-check` is enabled [#10036](https://github.com/pingcap/tiflow/issues/10036) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC scheduling is not balanced in some cases [#9845](https://github.com/pingcap/tiflow/issues/9845) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might get stuck when replicating data to Kafka [#9855](https://github.com/pingcap/tiflow/issues/9855) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the TiCDC processor might panic in some cases [#9849](https://github.com/pingcap/tiflow/issues/9849) [#9915](https://github.com/pingcap/tiflow/issues/9915) @[hicqu](https://github.com/hicqu) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that enabling `kv-client.enable-multiplexing` causes replication tasks to get stuck [#9673](https://github.com/pingcap/tiflow/issues/9673) @[fubinzh](https://github.com/fubinzh)
        - Fix the issue that an owner node gets stuck due to NFS failure when the redo log is enabled [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

## Performance test

To learn about the performance of TiDB v7.5.0, you can refer to the [TPC-C performance test report](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc) and [Sysbench performance test report](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench) of the TiDB Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community:

- [jgrande](https://github.com/jgrande) (First-time contributor)
- [shawn0915](https://github.com/shawn0915)
