---
title: TiDB 7.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.1.0.
---

# TiDB 7.1.0 Release Notes

Release date: May 31, 2023

TiDB version: 7.1.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.0#version-list)

TiDB 7.1.0 is a Long-Term Support Release (LTS).

Compared with the previous LTS 6.5.0, 7.1.0 not only includes new features, improvements, and bug fixes released in [6.6.0-DMR](/releases/release-6.6.0.md), [7.0.0-DMR](/releases/release-7.0.0.md), but also introduces the following key features and improvements:

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
    <td rowspan="4">Scalability and Performance</td>
    <td>TiFlash supports the <a href="https://docs.pingcap.com/tidb/v7.1/tiflash-disaggregated-and-s3" target="_blank">disaggregated storage and compute architecture and S3 shared storage</a> (experimental, introduced in v7.0.0)</td>
    <td>TiFlash introduces a cloud-native architecture as an option:
      <ul>
        <li>Disaggregates TiFlash's compute and storage, which is a milestone for elastic HTAP resource utilization.</li>
        <li>Introduces S3-based storage engine, which can provide shared storage at a lower cost.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>TiKV supports <a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_store_batch_size" target="_blank">batch aggregating data requests</a> (introduced in v6.6.0) </td>
    <td>This enhancement significantly reduces total RPCs in TiKV batch-get operations. In situations where data is highly dispersed and the gRPC thread pool has insufficient resources, batching coprocessor requests can improve performance by more than 50%.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/troubleshoot-hot-spot-issues#scatter-read-hotspots" target="_blank">Load-based replica read</a></td>
    <td>In a read hotspot scenario, TiDB can redirect read requests for a hotspot TiKV node to its replicas. This feature efficiently scatters read hotspots and optimizes the use of cluster resources. To control the threshold for triggering load-based replica read, you can adjust the system variable <a href="https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_load_based_replica_read_threshold-new-in-v700" target="_blank"><code>tidb_load_based_replica_read_threshold</code></a>.</td>
  </tr>
  <tr>
      <td>TiKV supports<a href="https://docs.pingcap.com/tidb/v7.1/partitioned-raft-kv" target="_blank"> partitioned Raft KV storage engine </a> (experimental)</td>
    <td>TiKV introduces a new generation of storage engine, the partitioned Raft KV. By allowing each data Region to have a dedicated RocksDB instance, it can expand the cluster's storage capacity from TB-level to PB-level and provide more stable write latency and stronger scalability.</td>
    </tr>
  <tr>
    <td rowspan="2">Reliability and availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/tidb-resource-control" target="_blank">Resource control by resource groups</a> (GA)</td>
   <td>Support resource management based on resource groups, which allocates and isolates resources for different workloads in the same cluster. This feature significantly enhances the stability of multi-application clusters and lays the foundation for multi-tenancy. In v7.1.0, this feature introduces the ability to estimate system capacity based on actual workload or hardware deployment.</td>
  </tr>
  <tr>
    <td>TiFlash supports <a href="https://docs.pingcap.com/tidb/v7.1/tiflash-spill-disk" target="_blank">spill to disk</a> (introduced in v7.0.0)</td>
    <td>TiFlash supports intermediate result spill to disk to mitigate OOMs in data-intensive operations such as aggregations, sorts, and hash joins.</td>
  </tr>
  <tr>
    <td rowspan="3">SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/sql-statement-create-index#multi-valued-indexes" target="_blank">Multi-valued indexes</a> (GA)</td>
    <td>Support MySQL-compatible multi-valued indexes and enhance the JSON type to improve compatibility with MySQL 8.0. This feature improves the efficiency of membership checks on multi-valued columns.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/time-to-live" target="_blank">Row-level TTL</a> (GA in v7.0.0)</td>
    <td>Support managing database size and improve performance by automatically expiring data of a certain age.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/generated-columns" target="_blank">Generated columns</a> (GA)</td>
    <td>Values in a generated column are calculated by a SQL expression in the column definition in real time. This feature pushes some application logic to the database level, thus improving query efficiency.</td>
  </tr>
  <tr>
    <td rowspan="2">Security</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.1/security-compatibility-with-mysql" target="_blank">LDAP authentication</a></td>
    <td>TiDB supports LDAP authentication, which is compatible with <a href="https://dev.mysql.com/doc/refman/8.0/en/ldap-pluggable-authentication.html" target="_blank">MySQL 8.0</a>.</td>
  </tr>
  <tr>
    <td> Audit log enhancement (<a href="https://www.pingcap.com/tidb-enterprise" target="_blank">Enterprise Edition</a> only)</td>
    <td>TiDB Enterprise Edition enhances the database auditing feature. It significantly improves the system auditing capacity by providing more fine-grained event filtering controls, more user-friendly filter settings, a new file output format in JSON, and lifecycle management of audit logs.</td>
  </tr>
</tbody>
</table>

## Feature details

### Performance

* Enhance the Partitioned Raft KV storage engine (experimental) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)

    TiDB v6.6.0 introduces the Partitioned Raft KV storage engine as an experimental feature, which uses multiple RocksDB instances to store TiKV Region data, and the data of each Region is independently stored in a separate RocksDB instance. The new storage engine can better control the number and level of files in the RocksDB instance, achieve physical isolation of data operations between Regions, and support stably managing more data. Compared with the original TiKV storage engine, using the Partitioned Raft KV storage engine can achieve about twice the write throughput and reduce the elastic scaling time by about 4/5 under the same hardware conditions and mixed read and write scenarios.

    In TiDB v7.1.0, the Partitioned Raft KV storage engine supports tools such as TiDB Lightning, BR, and TiCDC.

    Currently, this feature is experimental and not recommended for use in production environments. You can only use this engine in a newly created cluster and you cannot directly upgrade from the original TiKV storage engine.

    For more information, see [documentation](/partitioned-raft-kv.md).

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

* Enhance the capability of caching execution plans for non-prepared statements (experimental) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    TiDB v7.0.0 introduces non-prepared plan cache as an experimental feature to improve the load capacity of concurrent OLTP. In v7.1.0, TiDB enhances this feature and supports caching more SQL statements.

    To improve memory utilization, TiDB v7.1.0 merges the cache pools of non-prepared and prepared plan caches. You can control the cache size using the system variable [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710). The [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) and [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) system variables are deprecated.

    To maintain forward compatibility, when you upgrade from an earlier version to v7.1.0 or later versions, the cache size `tidb_session_plan_cache_size` remains the same value as `tidb_prepared_plan_cache_size`, and [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) remains the setting before the upgrade. After sufficient performance testing, you can enable non-prepared plan cache using `tidb_enable_non_prepared_plan_cache`. For a newly created cluster, non-prepared plan cache is enabled by default.

    Non-prepared plan cache does not support DML statements by default. To remove this restriction, you can set the [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710) system variable to `ON`.

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

* Support the DDL distributed parallel execution framework (experimental) [#41495](https://github.com/pingcap/tidb/issues/41495) @[benjamin2037](https://github.com/benjamin2037)

    Before TiDB v7.1.0, only one TiDB node can serve as the DDL owner and execute DDL tasks at the same time. Starting from TiDB v7.1.0, in the new distributed parallel execution framework, multiple TiDB nodes can execute the same DDL task in parallel, thus better utilizing the resources of the TiDB cluster and significantly improving the performance of DDL. In addition, you can linearly improve the performance of DDL by adding more TiDB nodes. Note that this feature is currently experimental and only supports `ADD INDEX` operations.

    To use the distributed framework, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    For more information, see [documentation](/tidb-distributed-execution-framework.md).

### Reliability

* Resource Control becomes generally available (GA) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB enhances the resource control feature based on resource groups, which becomes GA in v7.1.0. This feature significantly improves the resource utilization efficiency and performance of TiDB clusters. The introduction of the resource control feature is a milestone for TiDB. You can divide a distributed database cluster into multiple logical units, map different database users to corresponding resource groups, and set the quota for each resource group as needed. When the cluster resources are limited, all resources used by sessions in the same resource group are limited to the quota. In this way, even if a resource group is over-consumed, the sessions in other resource groups are not affected.

    With this feature, you can combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set quotas, which can achieve the maximum utilization of resources. In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

    In TiDB v7.1.0, this feature introduces the ability to estimate system capacity based on actual workload or hardware deployment. The estimation ability provides you with a more accurate reference for capacity planning and assists you in better managing TiDB resource allocation to meet the stability needs of enterprise-level scenarios.

    To improve user experience, TiDB Dashboard provides the [Resource Manager page](/dashboard/dashboard-resource-manager.md). You can view the resource group configuration on this page and estimate cluster capacity in a visual way to facilitate reasonable resource allocation.

    For more information, see [documentation](/tidb-resource-control.md).

* Support the checkpoint mechanism for Fast Online DDL to improve fault tolerance and automatic recovery capability [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.1.0 introduces a checkpoint mechanism for [Fast Online DDL](/ddl-introduction.md), which significantly improves the fault tolerance and automatic recovery capability of Fast Online DDL. Even if the TiDB owner node is restarted or changed due to failures, TiDB can still recover progress from checkpoints that are automatically updated on a regular basis, making the DDL execution more stable and efficient.

    For more information, see [documentation](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630).

* Backup & Restore supports checkpoint restore [#42339](https://github.com/pingcap/tidb/issues/42339) @[Leavrth](https://github.com/Leavrth)

    Snapshot restore or log restore might be interrupted due to recoverable errors, such as disk exhaustion and node crash. Before TiDB v7.1.0, the recovery progress before the interruption would be invalidated even after the error is addressed, and you need to start the restore from scratch. For large clusters, this incurs considerable extra cost.

    Starting from TiDB v7.1.0, Backup & Restore (BR) introduces the checkpoint restore feature, which enables you to continue an interrupted restore. This feature can retain most recovery progress of the interrupted restore.

    For more information, see [documentation](/br/br-checkpoint-restore.md).

* Optimize the strategy of loading statistics [#42160](https://github.com/pingcap/tidb/issues/42160) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

   TiDB v7.1.0 introduces lightweight statistics initialization as an experimental feature. Lightweight statistics initialization can significantly reduce the number of statistics that must be loaded during startup, thus improving the speed of loading statistics. This feature increases the stability of TiDB in complex runtime environments and reduces the impact on the overall service when TiDB nodes restart. You can set the parameter [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) to `true` to enable this feature.

    During TiDB startup, SQL statements executed before the initial statistics are fully loaded might have suboptimal execution plans, thus causing performance issues. To avoid such issues, TiDB v7.1.0 introduces the configuration parameter [`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710). With this option, you can control whether TiDB provides services only after statistics initialization has been finished during startup. This parameter is disabled by default.

    For more information, see [documentation](/statistics.md#load-statistics).

* TiCDC supports the data integrity validation feature for single-row data [#8718](https://github.com/pingcap/tiflow/issues/8718) [#42747](https://github.com/pingcap/tidb/issues/42747) @[3AceShowHand](https://github.com/3AceShowHand) @[zyguan](https://github.com/zyguan)

    Starting from v7.1.0, TiCDC introduces the data integrity validation feature, which uses a checksum algorithm to validate the integrity of single-row data. This feature helps verify whether any error occurs in the process of writing data from TiDB, replicating it through TiCDC, and then writing it to a Kafka cluster. The data integrity validation feature only supports changefeeds that use Kafka as the downstream and currently supports the Avro protocol.

    For more information, see [documentation](/ticdc/ticdc-integrity-check.md).

* TiCDC optimizes DDL replication operations [#8686](https://github.com/pingcap/tiflow/issues/8686) @[hi-rustin](https://github.com/hi-rustin)

    Before v7.1.0, when you perform a DDL operation that affects all rows on a large table (such as adding or deleting a column), the replication latency of TiCDC would significantly increase. Starting from v7.1.0, TiCDC optimizes this replication operation and mitigates the impact of DDL operations on downstream latency.

    For more information, see [documentation](/ticdc/ticdc-faq.md#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream).

* Improve the stability of TiDB Lightning when importing TiB-level data [#43510](https://github.com/pingcap/tidb/issues/43510) [#43657](https://github.com/pingcap/tidb/issues/43657) @[D3Hunter](https://github.com/D3Hunter) @[lance6716](https://github.com/lance6716)

    Starting from v7.1.0, TiDB Lightning has added four configuration items to improve stability when importing TiB-level data.

    - `tikv-importer.region-split-batch-size` controls the number of Regions when splitting Regions in a batch. The default value is `4096`.
    - `tikv-importer.region-split-concurrency` controls the concurrency when splitting Regions. The default value is the number of CPU cores.
    - `tikv-importer.region-check-backoff-limit` controls the number of retries to wait for the Region to come online after the split and scatter operations. The default value is `1800` and the maximum retry interval is two seconds. The number of retries is not increased if any Region becomes online between retries.
    - `tikv-importer.pause-pd-scheduler-scope` controls the scope in which TiDB Lightning pauses PD scheduling. Value options are `"table"` and `"global"`. The default value is `"table"`. For TiDB versions earlier than v6.1.0, you can only configure the `"global"` option, which pauses global scheduling during data import. Starting from v6.1.0, the `"table"` option is supported, which means that scheduling is only paused for the Region that stores the target table data. It is recommended to set this configuration item to `"global"` in scenarios with large data volumes to improve stability.

  For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md).

### SQL

* Support saving TiFlash query results using the `INSERT INTO SELECT` statement (GA) [#37515](https://github.com/pingcap/tidb/issues/37515) @[gengliqi](https://github.com/gengliqi)

    Starting from v6.5.0, TiDB supports pushing down the `SELECT` clause (analytical query) of the `INSERT INTO SELECT` statement to TiFlash. In this way, you can easily save the TiFlash query result to a TiDB table specified by `INSERT INTO` for further analysis, which takes effect as result caching (that is, result materialization).

    In v7.1.0, this feature is generally available. During the execution of the `SELECT` clause in the `INSERT INTO SELECT` statement, the optimizer can intelligently decide whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. Therefore, the `tidb_enable_tiflash_read_for_write_stmt` system variable introduced during the experimental phase is now deprecated. Note that the computation rules of `INSERT INTO SELECT` statements for TiFlash do not meet the `STRICT SQL Mode` requirement, so TiDB allows the `SELECT` clause in the `INSERT INTO SELECT` statement to be pushed down to TiFlash only when the [SQL mode](/sql-mode.md) of the current session is not strict, which means that the `sql_mode` value does not contain `STRICT_TRANS_TABLES` and `STRICT_ALL_TABLES`.

    For more information, see [documentation](/tiflash/tiflash-results-materialization.md).

* MySQL-compatible multi-valued indexes become generally available (GA) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990) @[YangKeao](https://github.com/YangKeao)

    Filtering the values of an array in a JSON column is a common operation, but normal indexes cannot help speed up such an operation. Creating a multi-valued index on an array can greatly improve filtering performance. If an array in the JSON column has a multi-valued index, you can use the multi-valued index to filter retrieval conditions in `MEMBER OF()`, `JSON_CONTAINS()`, and `JSON_OVERLAPS()` functions, thereby reducing I/O consumption and improving operation speed.

    In v7.1.0, the multi-valued indexes feature becomes generally available (GA). It supports more complete data types and is compatible with TiDB tools. You can use multi-valued indexes to speed up the search operations on JSON arrays in production environments.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).

* Improve the partition management for Hash and Key partitioned tables [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    Before v7.1.0, Hash and Key partitioned tables in TiDB only support the `TRUNCATE PARTITION` partition management statement. Starting from v7.1.0, Hash and Key partitioned tables also support `ADD PARTITION` and `COALESCE PARTITION` partition management statements. Therefore, you can flexibly adjust the number of partitions in Hash and Key partitioned tables as needed. For example, you can increase the number of partitions with the `ADD PARTITION` statement, or decrease the number of partitions with the `COALESCE PARTITION` statement.

    For more information, see [documentation](/partitioned-table.md#manage-hash-and-key-partitions).

* The syntax of Range INTERVAL partitioning becomes generally available (GA) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    The syntax of Range INTERVAL partitioning (introduced in v6.3.0) becomes GA. With this syntax, you can define Range partitioning by a desired interval without enumerating all partitions, which drastically reduces the length of Range partitioning DDL statements. The syntax is equivalent to that of the original Range partitioning.

    For more information, see [documentation](/partitioned-table.md#range-interval-partitioning).

* Generated columns become generally available (GA) @[bb7133](https://github.com/bb7133)

    Generated columns are a valuable feature for a database. When creating a table, you can define that the value of a column is calculated based on the values of other columns in the table, rather than being explicitly inserted or updated by users. This generated column can be either a virtual column or a stored column. TiDB has supported MySQL-compatible generated columns since earlier versions, and this feature becomes GA in v7.1.0.

    Using generated columns can improve MySQL compatibility for TiDB, simplifying the process of migrating from MySQL. It also reduces data maintenance complexity and improves data consistency and query efficiency.

    For more information, see [documentation](/generated-columns.md).

### DB operations

* Support smooth cluster upgrade without manually canceling DDL operations (experimental) [#39751](https://github.com/pingcap/tidb/issues/39751) @[zimulala](https://github.com/zimulala)

    Before TiDB v7.1.0, to upgrade a cluster, you must manually cancel its running or queued DDL tasks before the upgrade and then add them back after the upgrade.

    To provide a smoother upgrade experience, TiDB v7.1.0 supports automatically pausing and resuming DDL tasks. Starting from v7.1.0, you can upgrade your clusters without manually canceling DDL tasks in advance. TiDB will automatically pause any running or queued user DDL tasks before the upgrade and resume these tasks after the rolling upgrade, making it easier for you to upgrade your TiDB clusters.

    For more information, see [documentation](/smooth-upgrade-tidb.md).

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

* Support LDAP authentication [#43580](https://github.com/pingcap/tidb/issues/43580) @[YangKeao](https://github.com/YangKeao)

    Starting from v7.1.0, TiDB supports LDAP authentication and provides two authentication plugins: `authentication_ldap_sasl` and `authentication_ldap_simple`.

    For more information, see [documentation](/security-compatibility-with-mysql.md).

* Enhance the database auditing feature (Enterprise Edition)

    In v7.1.0, TiDB Enterprise Edition enhances the database auditing feature, which significantly expands its capacity and improves the user experience to meet the needs of enterprises for database security compliance:

    - Introduce the concepts of "Filter" and "Rule" for more granular audit event definitions and more fine-grained audit settings.
    - Support defining rules in JSON format, providing a more user-friendly configuration method.
    - Add automatic log rotation and space management functions, and support configuring log rotation in two dimensions: retention time and log size.
    - Support outputting audit logs in both TEXT and JSON formats, facilitating easier integration with third-party tools.
    - Support audit log redaction. You can replace all literals to enhance security.

  Database auditing is an important feature in TiDB Enterprise Edition. This feature provides a powerful monitoring and auditing tool for enterprises to ensure data security and compliance. It can help enterprise managers in tracking the source and impact of database operations to prevent illegal data theft or tampering. Furthermore, database auditing can also help enterprises meet various regulatory and compliance requirements, ensuring legal and ethical compliance. This feature has important application value for enterprise information security.

    This feature is included in TiDB Enterprise Edition. To use this feature and its documentation, navigate to the [TiDB Enterprise](https://www.pingcap.com/tidb-enterprise) page.

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.0.0 to the current version (v7.1.0). If you are upgrading from v6.6.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* To improve security, TiFlash deprecates the HTTP service port (default `8123`) and uses the gRPC port as a replacement

    If you have upgraded TiFlash to v7.1.0, then during the TiDB upgrade to v7.1.0, TiDB cannot read the TiFlash system tables ([`INFORMATION_SCHEMA.TIFLASH_TABLES`](/information-schema/information-schema-tiflash-tables.md) and [`INFORMATION_SCHEMA.TIFLASH_SEGMENTS`](/information-schema/information-schema-tiflash-segments.md)).

* TiDB Lightning in TiDB versions from v6.2.0 to v7.0.0 decides whether to pause global scheduling based on the TiDB cluster version. When TiDB cluster version >= v6.1.0, scheduling is only paused for the Region that stores the target table data and is resumed after the target table import is complete. While for other versions, TiDB Lightning pauses global scheduling. Starting from TiDB v7.1.0, you can control whether to pause global scheduling by configuring [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md). By default, TiDB Lightning pauses scheduling for the Region that stores the target table data. If the target cluster version is earlier than v6.1.0, an error occurs. In this case, you can change the value of the parameter to `"global"` and try again.

* When you use [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) in TiDB v7.1.0, some Regions might remain in the FLASHBACK process even after the completion of the FLASHBACK operation. It is recommended to avoid using this feature in v7.1.0. For more information, see issue [#44292](https://github.com/pingcap/tidb/issues/44292). If you have encountered this issue, you can use the [TiDB snapshot backup and restore](/br/br-snapshot-guide.md) feature to restore data.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) | Deprecated | Changes the default value from `OFF` to `ON`. When [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50), the optimizer intelligently decides whether to push a query down to TiFlash based on the [SQL mode](/sql-mode.md) and the cost estimates of the TiFlash replica. |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | Deprecated | Starting from v7.1.0, this system variable is deprecated. You can use [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) to control the maximum number of plans that can be cached. |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610) | Deprecated | Starting from v7.1.0, this system variable is deprecated. You can use [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) to control the maximum number of plans that can be cached. |
| `tidb_ddl_distribute_reorg` | Deleted | This variable is renamed to [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710). |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | Modified | Introduces two new value options: `authentication_ldap_sasl` and `authentication_ldap_simple`. |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) | Modified | Takes effect starting from v7.1.0 and controls the threshold for triggering load-based replica read. Changes the default value from `"0s"` to `"1s"` after further tests. |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) | Modified | Changes the default value from `OFF` to `ON`, meaning that the TiFlash late materialization feature is enabled by default. |
| [`authentication_ldap_sasl_auth_method_name`](/system-variables.md#authentication_ldap_sasl_auth_method_name-new-in-v710) | Newly added | Specifies the authentication method name in LDAP SASL authentication. |
| [`authentication_ldap_sasl_bind_base_dn`](/system-variables.md#authentication_ldap_sasl_bind_base_dn-new-in-v710) | Newly added | Limits the search scope within the search tree in LDAP SASL authentication. If a user is created without `AS ...` clause, TiDB automatically searches the `dn` in LDAP server according to the user name. |
| [`authentication_ldap_sasl_bind_root_dn`](/system-variables.md#authentication_ldap_sasl_bind_root_dn-new-in-v710) | Newly added | Specifies the `dn` used to login to the LDAP server to search users in LDAP SASL authentication. |
| [`authentication_ldap_sasl_bind_root_pwd`](/system-variables.md#authentication_ldap_sasl_bind_root_pwd-new-in-v710) | Newly added | Specifies the password used to login to the LDAP server to search users in LDAP SASL authentication. |
| [`authentication_ldap_sasl_ca_path`](/system-variables.md#authentication_ldap_sasl_ca_path-new-in-v710) | Newly added | Specifies the absolute path of the certificate authority file for StartTLS connections in LDAP SASL authentication. |
| [`authentication_ldap_sasl_init_pool_size`](/system-variables.md#authentication_ldap_sasl_init_pool_size-new-in-v710) | Newly added | Specifies the initial connections in the connection pool to the LDAP server in LDAP SASL authentication. |
| [`authentication_ldap_sasl_max_pool_size`](/system-variables.md#authentication_ldap_sasl_max_pool_size-new-in-v710) | Newly added | Specifies the maximum connections in the connection pool to the LDAP server in LDAP SASL authentication. |
| [`authentication_ldap_sasl_server_host`](/system-variables.md#authentication_ldap_sasl_server_host-new-in-v710) | Newly added | Specifies the LDAP server host in LDAP SASL authentication. |
| [`authentication_ldap_sasl_server_port`](/system-variables.md#authentication_ldap_sasl_server_port-new-in-v710) | Newly added | Specifies the LDAP server TCP/IP port number in LDAP SASL authentication. |
| [`authentication_ldap_sasl_tls`](/system-variables.md#authentication_ldap_sasl_tls-new-in-v710) | Newly added | Specifies whether connections by the plugin to the LDAP server are protected with StartTLS in LDAP SASL authentication. |
| [`authentication_ldap_simple_auth_method_name`](/system-variables.md#authentication_ldap_simple_auth_method_name-new-in-v710) | Newly added | Specifies the authentication method name in LDAP simple authentication. It only supports `SIMPLE`. |
| [`authentication_ldap_simple_bind_base_dn`](/system-variables.md#authentication_ldap_simple_bind_base_dn-new-in-v710) | Newly added | Limits the search scope within the search tree in LDAP simple authentication. If a user is created without `AS ...` clause, TiDB will automatically search the `dn` in LDAP server according to the user name. |
| [`authentication_ldap_simple_bind_root_dn`](/system-variables.md#authentication_ldap_simple_bind_root_dn-new-in-v710) | Newly added | Specifies the `dn` used to login to the LDAP server to search users in LDAP simple authentication. |
| [`authentication_ldap_simple_bind_root_pwd`](/system-variables.md#authentication_ldap_simple_bind_root_pwd-new-in-v710) | Newly added | Specifies the password used to login to the LDAP server to search users in LDAP simple authentication. |
| [`authentication_ldap_simple_ca_path`](/system-variables.md#authentication_ldap_simple_ca_path-new-in-v710) | Newly added | Specifies the absolute path of the certificate authority file for StartTLS connections in LDAP simple authentication. |
| [`authentication_ldap_simple_init_pool_size`](/system-variables.md#authentication_ldap_simple_init_pool_size-new-in-v710) | Newly added | Specifies the initial connections in the connection pool to the LDAP server in LDAP simple authentication. |
| [`authentication_ldap_simple_max_pool_size`](/system-variables.md#authentication_ldap_simple_max_pool_size-new-in-v710) | Newly added | Specifies the maximum connections in the connection pool to the LDAP server in LDAP simple authentication. |
| [`authentication_ldap_simple_server_host`](/system-variables.md#authentication_ldap_simple_server_host-new-in-v710) | Newly added | Specifies the LDAP server host in LDAP simple authentication. |
| [`authentication_ldap_simple_server_port`](/system-variables.md#authentication_ldap_simple_server_port-new-in-v710) | Newly added | Specifies the LDAP server TCP/IP port number in LDAP simple authentication. |
| [`authentication_ldap_simple_tls`](/system-variables.md#authentication_ldap_simple_tls-new-in-v710) | Newly added | Specifies whether connections by the plugin to the LDAP server are protected with StartTLS in LDAP simple authentication. |
| [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) | Newly added | Controls whether to enable the distributed execution framework. After enabling distributed execution, DDL, import, and other supported backend tasks will be jointly completed by multiple TiDB nodes in the cluster. This variable was renamed from `tidb_ddl_distribute_reorg`. |
| [`tidb_enable_non_prepared_plan_cache_for_dml`](/system-variables.md#tidb_enable_non_prepared_plan_cache_for_dml-new-in-v710) | Newly added | Controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature for DML statements. |
| [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) | Newly added | Controls whether to enable the TiCDC data integrity validation for single-row data feature.|
| [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710) | Newly added | This variable provides more fine-grained control over the optimizer and helps to prevent performance regression after upgrading caused by behavior changes in the optimizer. |
| [`tidb_plan_cache_invalidation_on_fresh_stats`](/system-variables.md#tidb_plan_cache_invalidation_on_fresh_stats-new-in-v710) | Newly added | Controls whether to invalidate the plan cache automatically when statistics on related tables are updated. |
| [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) | Newly added | Controls the maximum size of a plan that can be cached in prepared or non-prepared plan cache. |
| [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) | Newly added | Controls whether to use the algorithm with the minimum overhead of network transmission. If this variable is enabled, TiDB estimates the size of the data to be exchanged in the network using `Broadcast Hash Join` and `Shuffled Hash Join` respectively, and then chooses the one with the smaller size. [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) and [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) will not take effect after this variable is enabled. |
| [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) | Newly added | Controls the maximum number of plans that can be cached. Prepared plan cache and non-prepared plan cache share the same cache. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`performance.force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710) | Newly added | Controls whether to wait for statistics initialization to finish before providing services during TiDB startup. |
| TiDB | [`performance.lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) | Newly added | Controls whether to use lightweight statistics initialization during TiDB startup. |
| TiDB | [`log.timeout`](/tidb-configuration-file.md#timeout-new-in-v710) | Newly added | Sets the timeout for log-writing operations in TiDB. In case of a disk failure that prevents logs from being written, this configuration item can trigger the TiDB process to panic instead of hang. The default value is `0`, which means no timeout is set. |
| TiKV | [`region-compact-min-redundant-rows`](/tikv-configuration-file.md#region-compact-min-redundant-rows-new-in-v710) | Newly added | Sets the number of redundant MVCC rows required to trigger RocksDB compaction. The default value is `50000`. |
| TiKV | [`region-compact-redundant-rows-percent`](/tikv-configuration-file.md#region-compact-redundant-rows-percent-new-in-v710) | Newly added | Sets the percentage of redundant MVCC rows required to trigger RocksDB compaction. The default value is `20`. |
| TiKV | [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50) | Modified | Changes the default value from `30MiB` to `100MiB` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| TiKV | [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) | Modified | Changes the default value from `3000` to `7000` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| TiKV | [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620) | Modified | Changes the default value from `0.25` to `0.75` when [`region-split-size`](/tikv-configuration-file.md#region-split-size) is greater than or equal to 4 GB. |
| TiKV | [`region-compact-check-step`](/tikv-configuration-file.md#region-compact-check-step) | Modified | Changes the default value from `100` to `5` when Partitioned Raft KV is enabled (`storage.engine="partitioned-raft-kv"`). |
| PD | [`store-limit-version`](/pd-configuration-file.md#store-limit-version-new-in-v710) | Newly added | Controls the mode of store limit. Value options are `"v1"` and `"v2"`. |
| PD | [`schedule.enable-diagnostic`](/pd-configuration-file.md#enable-diagnostic-new-in-v630) | Modified | Changes the default value from `false` to `true`, meaning that the diagnostic feature of scheduler is enabled by default. |
| TiFlash | `http_port` | Deleted | Deprecates the HTTP service port (default `8123`). |
| TiDB Lightning | [`tikv-importer.pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls the scope in which TiDB Lightning pauses PD scheduling. The default value is `"table"` and value options are `"global"` and `"table"`. |
| TiDB Lightning | [`tikv-importer.region-check-backoff-limit`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls the number of retries to wait for the Region to come online after the split and scatter operations. The default value is `1800`. The maximum retry interval is two seconds. The number of retries is not increased if any Region becomes online between retries.|
| TiDB Lightning | [`tikv-importer.region-split-batch-size`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls the number of Regions when splitting Regions in a batch. The default value is `4096`. |
| TiDB Lightning | [`tikv-importer.region-split-concurrency`](/tidb-lightning/tidb-lightning-configuration.md) | Newly added | Controls the concurrency when splitting Regions. The default value is the number of CPU cores. |
| TiCDC | [`insecure-skip-verify`](/ticdc/ticdc-sink-to-kafka.md) | Newly added | Controls whether the authentication algorithm is set when TLS is enabled in the scenario of replicating data to Kafka. |
| TiCDC | [`integrity.corruption-handle-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | Newly added | Specifies the log level of the Changefeed when the checksum validation for single-row data fails. The default value is `"warn"`. Value options are `"warn"` and `"error"`. |
| TiCDC | [`integrity.integrity-check-level`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | Newly added | Controls whether to enable the checksum validation for single-row data. The default value is `"none"`, which means to disable the feature. |
| TiCDC | [`sink.only-output-updated-columns`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | Newly added | Controls whether to only output the updated columns. The default value is `false`. |
| TiCDC | [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#cli-and-configuration-parameters-of-ticdc-changefeeds) | Modified | Changes the default value from `false` to `true` after further tests, meaning that partitions in a table are stored in separate directories by default. It is recommended that you keep the value as `true` to avoid the potential issue of data loss during replication of partitioned tables to storage services. |

## Improvements

+ TiDB

    - Display the number of distinct values for the corresponding column in the Cardinality column of the `SHOW INDEX` result [#42227](https://github.com/pingcap/tidb/issues/42227) @[winoros](https://github.com/winoros)
    - Use `SQL_NO_CACHE` to prevent TTL Scan queries from impacting the TiKV block cache [#43206](https://github.com/pingcap/tidb/issues/43206) @[lcwangchao](https://github.com/lcwangchao)
    - Improve an error message related to `MAX_EXECUTION_TIME` to make it compatible with MySQL [#43031](https://github.com/pingcap/tidb/issues/43031) @[dveeden](https://github.com/dveeden)
    - Support using the MergeSort operator on partitioned tables in IndexLookUp [#26166](https://github.com/pingcap/tidb/issues/26166) @[Defined2014](https://github.com/Defined2014)
    - Enhance `caching_sha2_password` to make it compatible with MySQL [#43576](https://github.com/pingcap/tidb/issues/43576) @[asjdf](https://github.com/asjdf)

+ TiKV

    - Reduce the impact of split operations on write QPS when using partitioned Raft KV [#14447](https://github.com/tikv/tikv/issues/14447) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Optimize the space occupied by snapshots when using partitioned Raft KV [#14581](https://github.com/tikv/tikv/issues/14581) @[bufferflies](https://github.com/bufferflies)
    - Provide more detailed time information for each stage of processing requests in TiKV [#12362](https://github.com/tikv/tikv/issues/12362) @[cfzjywxk](https://github.com/cfzjywxk)
    - Use PD as metastore in log backup [#13867](https://github.com/tikv/tikv/issues/13867) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Add a controller that automatically adjusts the size of the store limit based on the execution details of the snapshot. To enable this controller, set `store-limit-version` to `v2`. Once enabled, you do not need to manually adjust the `store limit` configuration to control the speed of scaling in or scaling out [#6147](https://github.com/tikv/pd/issues/6147) @[bufferflies](https://github.com/bufferflies)
    - Add historical load information to avoid frequent scheduling of Regions with unstable loads by the hotspot scheduler when the storage engine is raft-kv2 [#6297](https://github.com/tikv/pd/issues/6297) @[bufferflies](https://github.com/bufferflies)
    - Add a leader health check mechanism. When the PD server where the etcd leader is located cannot be elected as the leader, PD actively switches the etcd leader to ensure that the PD leader is available [#6403](https://github.com/tikv/pd/issues/6403) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Improve TiFlash performance and stability in the disaggregated storage and compute architecture [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[breezewish](https://github.com/breezewish) @[JinheLin](https://github.com/JinheLin)
    - Support optimizing query performance in Semi Join or Anti Semi Join by selecting the smaller table as the build side [#7280](https://github.com/pingcap/tiflash/issues/7280) @[yibin87](https://github.com/yibin87)
    - Improve performance of data import from BR and TiDB Lightning to TiFlash with default configurations [#7272](https://github.com/pingcap/tiflash/issues/7272) @[breezewish](https://github.com/breezewish)

+ Tools

    + Backup & Restore (BR)

        - Support modifying the TiKV configuration item `log-backup.max-flush-interval` during log backup [#14433](https://github.com/tikv/tikv/issues/14433) @[joccau](https://github.com/joccau)

    + TiCDC

        - Optimize the directory structure when DDL events occur in the scenario of replicating data to object storage [#8890](https://github.com/pingcap/tiflow/issues/8890) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Optimize the method of setting GC TLS for the upstream when the TiCDC replication task fails [#8403](https://github.com/pingcap/tiflow/issues/8403) @[charleszheng44](https://github.com/charleszheng44)
        - Support replicating data to the Kafka-on-Pulsar downstream [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)
        - Support using the open-protocol protocol to only replicate the changed columns after an update occurs when replicating data to Kafka [#8706](https://github.com/pingcap/tiflow/issues/8706) @[sdojjy](https://github.com/sdojjy)
        - Optimize the error handling of TiCDC in the downstream failures or other scenarios [#8657](https://github.com/pingcap/tiflow/issues/8657) @[hicqu](https://github.com/hicqu)
        - Add a configuration item `insecure-skip-verify` to control whether to set the authentication algorithm in the scenario of enabling TLS [#8867](https://github.com/pingcap/tiflow/issues/8867) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Lightning

        - Change the severity level of the precheck item related to uneven Region distribution from `Critical` to `Warn` to avoid blocking users from importing data [#42836](https://github.com/pingcap/tidb/issues/42836) @[okJiang](https://github.com/okJiang)
        - Add a retry mechanism when encountering an `unknown RPC` error during data import [#43291](https://github.com/pingcap/tidb/issues/43291) @[D3Hunter](https://github.com/D3Hunter)
        - Enhance the retry mechanism for Region jobs [#43682](https://github.com/pingcap/tidb/issues/43682) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB

    - Fix the issue that there is no prompt about manually executing `ANALYZE TABLE` after reorganizing partitions [#42183](https://github.com/pingcap/tidb/issues/42183) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue of missing table names in the `ADMIN SHOW DDL JOBS` result when a `DROP TABLE` operation is being executed [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that `Ignore Event Per Minute` and `Stats Cache LRU Cost` charts might not be displayed normally in the Grafana monitoring panel [#42562](https://github.com/pingcap/tidb/issues/42562) @[pingandb](https://github.com/pingandb)
    - Fix the issue that the `ORDINAL_POSITION` column returns incorrect results when querying the `INFORMATION_SCHEMA.COLUMNS` table [#43379](https://github.com/pingcap/tidb/issues/43379) @[bb7133](https://github.com/bb7133)
    - Fix the case sensitivity issue in some columns of the permission table [#41048](https://github.com/pingcap/tidb/issues/41048) @[bb7133](https://github.com/bb7133)
    - Fix the issue that after a new column is added in the cache table, the value is `NULL` instead of the default value of the column [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - Fix the issue that CTE results are incorrect when pushing down predicates [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - Fix the issue of DDL retry caused by write conflict when executing `TRUNCATE TABLE` for partitioned tables with many partitions and TiFlash replicas [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - Fix the issue that there is no warning when using `SUBPARTITION` in creating partitioned tables [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - Fix the incompatibility issue with MySQL when dealing with value overflow issues in generated columns [#40066](https://github.com/pingcap/tidb/issues/40066) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that `REORGANIZE PARTITION` cannot be concurrently executed with other DDL operations [#42442](https://github.com/pingcap/tidb/issues/42442) @[bb7133](https://github.com/bb7133)
    - Fix the issue that canceling the partition reorganization task in DDL might cause subsequent DDL operations to fail [#42448](https://github.com/pingcap/tidb/issues/42448) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that assertions on delete operations are incorrect under certain conditions [#42426](https://github.com/pingcap/tidb/issues/42426) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB server cannot start due to an error in reading the cgroup information with the error message "can't read file memory.stat from cgroup v1: open /sys/memory.stat no such file or directory" [#42659](https://github.com/pingcap/tidb/issues/42659) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the `Duplicate Key` issue that occurs when updating the partition key of a row on a partitioned table with a global index [#42312](https://github.com/pingcap/tidb/issues/42312) @[L-maple](https://github.com/L-maple)
    - Fix the issue that the `Scan Worker Time By Phase` chart in the TTL monitoring panel does not display data [#42515](https://github.com/pingcap/tidb/issues/42515) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that some queries on partitioned tables with a global index return incorrect results [#41991](https://github.com/pingcap/tidb/issues/41991) [#42065](https://github.com/pingcap/tidb/issues/42065) @[L-maple](https://github.com/L-maple)
    - Fix the issue of displaying some error logs during the process of reorganizing a partitioned table [#42180](https://github.com/pingcap/tidb/issues/42180) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the data length in the `QUERY` column of the `INFORMATION_SCHEMA.DDL_JOBS` table might exceed the column definition [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `INFORMATION_SCHEMA.CLUSTER_HARDWARE` table might display incorrect values in containers [#42851](https://github.com/pingcap/tidb/issues/42851) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that an incorrect result is returned when you query a partitioned table using `ORDER BY` + `LIMIT` [#43158](https://github.com/pingcap/tidb/issues/43158) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue of multiple DDL tasks running simultaneously using the ingest method [#42903](https://github.com/pingcap/tidb/issues/42903) @[tangenta](https://github.com/tangenta)
    - Fix the wrong value returned when querying a partitioned table using `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)
    - Fix the issue of displaying the incorrect TiDB address in IPv6 environment [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - Fix the issue of displaying incorrect values for system variables `tidb_enable_tiflash_read_for_write_stmt` and `tidb_enable_exchange_partition` [#43281](https://github.com/pingcap/tidb/issues/43281) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that when `tidb_scatter_region` is enabled, Region does not automatically split after a partition is truncated [#43174](https://github.com/pingcap/tidb/issues/43174) [#43028](https://github.com/pingcap/tidb/issues/43028) @[jiyfhust](https://github.com/jiyfhust)
    - Add checks on the tables with generated columns and report errors for unsupported DDL operations on these columns [#38988](https://github.com/pingcap/tidb/issues/38988) [#24321](https://github.com/pingcap/tidb/issues/24321) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the error message is incorrect in certain type conversion errors [#41730](https://github.com/pingcap/tidb/issues/41730) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that after a TiDB node is normally shutdown, DDL tasks triggered on this node will be canceled [#43854](https://github.com/pingcap/tidb/issues/43854) @[zimulala](https://github.com/zimulala)
    - Fix the issue that when the PD member address changes, allocating ID for the `AUTO_INCREMENT` column will be blocked for a long time [#42643](https://github.com/pingcap/tidb/issues/42643) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of reporting the `GC lifetime is shorter than transaction duration` error during DDL execution [#40074](https://github.com/pingcap/tidb/issues/40074) @[tangenta](https://github.com/tangenta)
    - Fix the issue that metadata locks unexpectedly block the DDL execution [#43755](https://github.com/pingcap/tidb/issues/43755) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the cluster cannot query some system views in IPv6 environment [#43286](https://github.com/pingcap/tidb/issues/43286) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue of not finding the partition during inner join in dynamic pruning mode [#43686](https://github.com/pingcap/tidb/issues/43686) @[mjonss](https://github.com/mjonss)
    - Fix the issue that TiDB reports syntax errors when analyzing tables [#43392](https://github.com/pingcap/tidb/issues/43392) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiCDC might lose some row changes during table renaming [#43338](https://github.com/pingcap/tidb/issues/43338) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB server crashes when the client uses cursor reads [#38116](https://github.com/pingcap/tidb/issues/38116) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `ADMIN SHOW DDL JOBS LIMIT` returns incorrect results [#42298](https://github.com/pingcap/tidb/issues/42298) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the TiDB panic issue that occurs when querying union views and temporary tables with `UNION` [#42563](https://github.com/pingcap/tidb/issues/42563) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that renaming tables does not take effect when committing multiple statements in a transaction [#39664](https://github.com/pingcap/tidb/issues/39664) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the incompatibility issue between the behavior of prepared plan cache and non-prepared plan cache during time conversion [#42439](https://github.com/pingcap/tidb/issues/42439) @[qw4990](https://github.com/qw4990)
    - Fix the wrong results caused by plan cache for Decimal type [#43311](https://github.com/pingcap/tidb/issues/43311) @[qw4990](https://github.com/qw4990)
    - Fix the TiDB panic issue in null-aware anti join (NAAJ) due to the wrong field type check [#42459](https://github.com/pingcap/tidb/issues/42459) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that DML execution failures in pessimistic transactions at the RC isolation level might cause inconsistency between data and indexes [#43294](https://github.com/pingcap/tidb/issues/43294) @[ekexium](https://github.com/ekexium)
    - Fix the issue that in some extreme cases, when the first statement of a pessimistic transaction is retried, resolving locks on this transaction might affect transaction correctness [#42937](https://github.com/pingcap/tidb/issues/42937) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that in some rare cases, residual pessimistic locks of pessimistic transactions might affect data correctness when GC resolves locks [#43243](https://github.com/pingcap/tidb/issues/43243) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the `LOCK` to `PUT` optimization leads to duplicate data being returned in specific queries [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - Fix the issue that when data is changed, the locking behavior of the unique index is not consistent with that when the data is unchanged [#36438](https://github.com/pingcap/tidb/issues/36438) @[zyguan](https://github.com/zyguan)

+ TiKV

    - Fix the issue that when you enable `tidb_pessimistic_txn_fair_locking`, in some extreme cases, expired requests caused by failed RPC retries might affect data correctness during the resolve lock operation [#14551](https://github.com/tikv/tikv/issues/14551) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that when you enable `tidb_pessimistic_txn_fair_locking`, in some extreme cases, expired requests caused by failed RPC retries might cause transaction conflicts to be ignored, thus affecting transaction consistency [#14311](https://github.com/tikv/tikv/issues/14311) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that encryption key ID conflict might cause the deletion of the old keys [#14585](https://github.com/tikv/tikv/issues/14585) @[tabokie](https://github.com/tabokie)
    - Fix the performance degradation issue caused by accumulated lock records when a cluster is upgraded from a previous version to v6.5 or later versions [#14780](https://github.com/tikv/tikv/issues/14780) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the `raft entry is too large` error occurs during the PITR recovery process [#14313](https://github.com/tikv/tikv/issues/14313) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV panics during the PITR recovery process due to `log_batch` exceeding 2 GB [#13848](https://github.com/tikv/tikv/issues/13848) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Fix the issue that the number of `low space store` in the PD monitoring panel is abnormal after TiKV panics [#6252](https://github.com/tikv/pd/issues/6252) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that Region Health monitoring data is deleted after PD leader switch [#6366](https://github.com/tikv/pd/issues/6366) @[iosmanthus](https://github.com/iosmanthus)
    - Fix the issue that the rule checker cannot repair unhealthy Regions with the `schedule=deny` label [#6426](https://github.com/tikv/pd/issues/6426) @[nolouch](https://github.com/nolouch)
    - Fix the issue that some existing labels are lost after TiKV or TiFlash restarts [#6467](https://github.com/tikv/pd/issues/6467) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that the replication status cannot be switched when there are learner nodes in the replication mode [#14704](https://github.com/tikv/tikv/issues/14704) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Fix the issue that querying data in the `TIMESTAMP` or `TIME` type returns errors after enabling late materialization [#7455](https://github.com/pingcap/tiflash/issues/7455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that large update transactions might cause TiFlash to repeatedly report errors and restart [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue of backup slowdown when a TiKV node crashes in a cluster [#42973](https://github.com/pingcap/tidb/issues/42973) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue of inaccurate error messages caused by a backup failure in some cases [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue of TiCDC time zone setting [#8798](https://github.com/pingcap/tiflow/issues/8798) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that TiCDC cannot automatically recover when PD address or leader fails [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that checkpoint lag increases when one of the upstream TiKV nodes crashes [#8858](https://github.com/pingcap/tiflow/issues/8858) @[hicqu](https://github.com/hicqu)
        - Fix the issue that when replicating data to object storage, the `EXCHANGE PARTITION` operation in the upstream cannot be properly replicated to the downstream [#8914](https://github.com/pingcap/tiflow/issues/8914) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the OOM issue caused by excessive memory usage of the sorter component in some special scenarios [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu)
        - Fix the TiCDC node panic that occurs when the downstream Kafka sinks are rolling restarted [#9023](https://github.com/pingcap/tiflow/issues/9023) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiDB Dumpling

        - Fix the issue that the `UNSIGNED INTEGER` type primary key cannot be used for splitting chunks [#42620](https://github.com/pingcap/tidb/issues/42620) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Dumpling might panic when `--output-file-template` is incorrectly set [#42391](https://github.com/pingcap/tidb/issues/42391) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Binlog

        - Fix the issue that an error might occur when encountering a failed DDL statement [#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @[okJiang](https://github.com/okJiang)

    + TiDB Lightning

        - Fix the performance degradation issue during data import [#42456](https://github.com/pingcap/tidb/issues/42456) @[lance6716](https://github.com/lance6716)
        - Fix the issue of `write to tikv with no leader returned` when importing a large amount of data [#43055](https://github.com/pingcap/tidb/issues/43055) @[lance6716](https://github.com/lance6716)
        - Fix the issue of excessive `keys within region is empty, skip doIngest` logs during data import [#43197](https://github.com/pingcap/tidb/issues/43197) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that panic might occur during partial write [#43363](https://github.com/pingcap/tidb/issues/43363) @[lance6716](https://github.com/lance6716)
        - Fix the issue that OOM might occur when importing a wide table [#43728](https://github.com/pingcap/tidb/issues/43728) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue of missing data in the TiDB Lightning Grafana dashboard [#43357](https://github.com/pingcap/tidb/issues/43357) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the import failure due to incorrect setting of `keyspace-name` [#43684](https://github.com/pingcap/tidb/issues/43684) @[zeminzhou](https://github.com/zeminzhou)
        - Fix the issue that data import might be skipped during range partial write in some cases [#43768](https://github.com/pingcap/tidb/issues/43768) @[lance6716](https://github.com/lance6716)

## Performance test

To learn about the performance of TiDB v7.1.0, you can refer to the [TPC-C performance test report](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-tpcc) and [Sysbench performance test report](https://docs.pingcap.com/tidbcloud/v7.1.0-performance-benchmarking-with-sysbench) of the TiDB Dedicated cluster.

## Contributors

We would like to thank the following contributors from the TiDB community:

- [blacktear23](https://github.com/blacktear23)
- [ethercflow](https://github.com/ethercflow)
- [hihihuhu](https://github.com/hihihuhu)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lqs](https://github.com/lqs)
- [pingandb](https://github.com/pingandb)
- [yorkhellen](https://github.com/yorkhellen)
- [yujiarista](https://github.com/yujiarista) (First-time contributor)
