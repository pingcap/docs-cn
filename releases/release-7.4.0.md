---
title: TiDB 7.4.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.4.0.
---

# TiDB 7.4.0 Release Notes

Release date: October 12, 2023

TiDB version: 7.4.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.4/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.4.0#version-list)

7.4.0 introduces the following key features and improvements:

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
    <td>Enhance the performance of adding multiple indexes for a table in a single <code>ADD INDEX</code> statement (experimental) </td>
    <td>Since v6.2.0, you can add multiple indexes for a table in a single <code>ADD INDEX</code> statement. However, the performance is the same as running multiple <code>ADD INDEX</code> statements. After optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.</td>
  </tr>
  <tr>
    <td rowspan="3">Reliability and Availability</td>
    <td>Improve the performance and stability of <code>IMPORT INTO</code> and <code>ADD INDEX</code> operations via <a href="https://docs.pingcap.com/tidb/v7.4/tidb-global-sort" target="_blank">global sort</a></td>
    <td>Before v7.4.0, tasks such as <code>ADD INDEX</code> or <code>IMPORT INTO</code> using the <a href="https://docs.pingcap.com/tidb/v7.4/tidb-distributed-execution-framework" target="_blank">distributed execution framework</a> meant localized and partial sorting, which ultimately led to TiKV doing a lot of extra work to make up for the partial sorting. These jobs also required TiDB nodes to allocate local disk space for sorting, before loading to TiKV.<br/>With the introduction of the Global Sorting feature in v7.4.0, data is temporarily stored in external shared storage (S3 in this version) for global sorting before being loaded into TiKV. This eliminates the need for TiKV to consume extra resources and significantly improves the performance and stability of operations like <code>ADD INDEX</code> and <code>IMPORT INTO</code>.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#manage-background-tasks" target="_blank">Resource control</a> for background tasks (experimental)</td>
    <td>In v7.1.0, the <a href="https://docs.pingcap.com/tidb/v7.4/tidb-resource-control#use-resource-control-to-achieve-resource-isolation" target="_blank">Resource Control</a> feature was introduced to mitigate resource and storage access interference between workloads. TiDB v7.4.0 applies this control to background tasks as well. In v7.4.0, Resource Control now identifies and manages the resources produced by background tasks, such as auto-analyze, Backup & Restore, bulk load with TiDB Lightning, and online DDL. This will eventually apply to all background tasks.</td>
  </tr>
  <tr>
    <td>TiFlash supports <a href="https://docs.pingcap.com/tidb/v7.4/tiflash-disaggregated-and-s3" target="_blank">storage-computing separation and S3</a> (GA) </td>
    <td>TiFlash disaggregated storage and compute architecture and S3 shared storage become generally available:
      <ul>
        <li>Disaggregates TiFlash's compute and storage, which is a milestone for elastic HTAP resource utilization.</li>
        <li>Supports using S3-based storage engine, which can provide shared storage at a lower cost.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td>TiDB supports <a href="https://docs.pingcap.com/tidb/v7.4/partitioned-table#convert-a-partitioned-table-to-a-non-partitioned-table" target="_blank">partition type management</a> </td>
    <td>Before v7.4.0, Range/List partitioned tables support partition management operations such as <code>TRUNCATE</code>, <code>EXCHANGE</code>, <code>ADD</code>, <code>DROP</code>, and <code>REORGANIZE</code>, and Hash/Key partitioned tables support partition management operations such as <code>ADD</code> and <code>COALESCE</code>.
    <p>Now TiDB also supports the following partition type management operations:</p>
      <ul>
        <li>Convert partitioned tables to non-partitioned tables</li>
        <li>Partition existing non-partitioned tables</li>
        <li>Modify partition types for existing tables</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>MySQL 8.0 compatibility: support<a href="https://docs.pingcap.com/tidb/v7.4/character-set-and-collation#character-sets-and-collations-supported-by-tidb" target="_blank"> collation <code>utf8mb4_0900_ai_ci</code></a></td>
    <td>One notable change in MySQL 8.0 is that the default character set is utf8mb4, and the default collation of utf8mb4 is <code>utf8mb4_0900_ai_ci</code>. TiDB v7.4.0 adding support for this enhances compatibility with MySQL 8.0 so that migrations and replications from MySQL 8.0 databases with the default collation are now much smoother.</td>
  </tr>
  <tr>
    <td>DB Operations and Observability</td>
    <td>Specify<a href="https://docs.pingcap.com/tidb/v7.4/system-variables#tidb_service_scope-new-in-v740" target="_blank"> the respective TiDB nodes</a> to execute the <code>IMPORT INTO</code> and <code>ADD INDEX</code> SQL statements (experimental)</td>
    <td>You have the flexibility to specify whether to execute <code>IMPORT INTO</code> or <code>ADD INDEX</code> SQL statements on some of the existing TiDB nodes or newly added TiDB nodes. This approach enables resource isolation from the rest of the TiDB nodes, preventing any impact on business operations while ensuring optimal performance for executing the preceding SQL statements.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Support selecting the TiDB nodes to parallelly execute the backend `ADD INDEX` or `IMPORT INTO` tasks of the distributed execution framework (experimental) [#46453](https://github.com/pingcap/tidb/pull/46453) @[ywqzzy](https://github.com/ywqzzy)

    Executing `ADD INDEX` or `IMPORT INTO` tasks in parallel in a resource-intensive cluster can consume a large amount of TiDB node resources, which can lead to cluster performance degradation. Starting from v7.4.0, you can use the system variable [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) to control the service scope of each TiDB node under the [TiDB Backend Task Distributed Execution Framework](/tidb-distributed-execution-framework.md). You can select several existing TiDB nodes or set the TiDB service scope for new TiDB nodes, and all parallel `ADD INDEX` and `IMPORT INTO` tasks only run on these nodes. This mechanism can avoid performance impact on existing services.

    For more information, see [documentation](/system-variables.md#tidb_service_scope-new-in-v740).

* Enhance the Partitioned Raft KV storage engine (experimental) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)

    TiDB v6.6.0 introduces the Partitioned Raft KV storage engine as an experimental feature, which uses multiple RocksDB instances to store TiKV Region data, and the data of each Region is independently stored in a separate RocksDB instance.

    In v7.4.0, TiDB further improves the compatibility and stability of the Partitioned Raft KV storage engine. Through large-scale data testing, the compatibility with TiDB ecosystem tools and features such as DM, Dumpling, TiDB Lightning, TiCDC, BR, and PITR is ensured. Additionally, the Partitioned Raft KV storage engine provides more stable performance under mixed read and write workloads, making it especially suitable for write-heavy scenarios. Furthermore, each TiKV node now supports 8 core CPUs and can be configured with 8 TB data storage, and 64 GB memory.

    For more information, see [documentation](/partitioned-raft-kv.md).

* TiFlash supports the disaggregated storage and compute architecture (GA) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[JaySon-Huang](https://github.com/JaySon-Huang) @[JinheLin](https://github.com/JinheLin) @[breezewish](https://github.com/breezewish) @[lidezhu](https://github.com/lidezhu) @[CalvinNeo](https://github.com/CalvinNeo) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    In v7.0.0, TiFlash introduces the disaggregated storage and compute architecture as an experimental feature. With a series of improvements, the disaggregated storage and compute architecture for TiFlash becomes GA starting from v7.4.0.

    In this architecture, TiFlash nodes are divided into two types (Compute Nodes and Write Nodes) and support object storage that is compatible with S3 API. Both types of nodes can be independently scaled for computing or storage capacities. In the disaggregated storage and compute architecture, you can use TiFlash in the same way as the coupled storage and compute architecture, such as creating TiFlash replicas, querying data, and specifying optimizer hints.

    Note that the TiFlash **disaggregated storage and compute architecture** and **coupled storage and compute architecture** cannot be used in the same cluster or converted to each other. You can configure which architecture to use when you deploy TiFlash.

    For more information, see [documentation](/tiflash/tiflash-disaggregated-and-s3.md).

### Performance

* Support pushing down the JSON operator `MEMBER OF` to TiKV [#46307](https://github.com/pingcap/tidb/issues/46307) @[wshwsh12](https://github.com/wshwsh12)

    * `value MEMBER OF(json_array)`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support pushing down window functions with any frame definition type to TiFlash [#7376](https://github.com/pingcap/tiflash/issues/7376) @[xzhangxian1008](https://github.com/xzhangxian1008)

    Before v7.4.0, TiFlash does not support window functions containing `PRECEDING` or `FOLLOWING`, and all window functions containing such frame definitions cannot be pushed down to TiFlash. Starting from v7.4.0, TiFlash supports frame definitions of all window functions. This feature is enabled automatically, and window functions containing frame definitions will be automatically pushed down to TiFlash for execution when the related requirements are met.

* Introduce cloud storage-based global sort capability to improve the performance and stability of `ADD INDEX` and `IMPORT INTO` tasks in parallel execution [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016)

    Before v7.4.0, when executing tasks like `ADD INDEX` or `IMPORT INTO` in the distributed parallel execution framework, each TiDB node needs to allocate a significant amount of local disk space for sorting encoded index KV pairs and table data KV pairs. However, due to the lack of global sorting capability, there might be overlapping data between different TiDB nodes and within each individual node during the process. As a result, TiKV has to constantly perform compaction operations while importing these KV pairs into its storage engine, which impacts the performance and stability of `ADD INDEX` and `IMPORT INTO`.

    In v7.4.0, TiDB introduces the [Global Sort](/tidb-global-sort.md) feature. Instead of writing the encoded data locally and sorting it there, the data is now written to cloud storage for global sorting. Once sorted, both the indexed data and table data are imported into TiKV in parallel, thereby improving performance and stability.

    For more information, see [documentation](/tidb-global-sort.md).

* Improve the performance of adding multiple indexes in a single SQL statement by optimizing parallel multi schema change [#41602](https://github.com/pingcap/tidb/issues/41602) @[tangenta](https://github.com/tangenta) @[Defined2014](https://github.com/Defined2014)

    Before v7.4.0, when you use parallel multi schema change to commit multiple `ADD INDEX` operations in a single SQL statement, the performance is the same as using multiple independent SQL statements for `ADD INDEX` operations. However, after optimization in v7.4.0, the performance of adding multiple indexes in a single SQL statement has been greatly improved.

* Support caching execution plans for non-prepared statements (GA) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    TiDB v7.0.0 introduces non-prepared plan cache as an experimental feature to improve the load capacity of concurrent OLTP. In v7.4.0, this feature becomes GA. The execution plan cache will be applied to more scenarios, thereby improving the concurrent processing capacity of TiDB.

    Enabling the non-prepared plan cache might incur additional memory and CPU overhead and might not be suitable for all situations. Starting from v7.4.0, this feature is disabled by default. You can enable it using [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) and control the cache size using [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710).

    Additionally, this feature does not support DML statements by default and has certain restrictions on SQL statements. For more details, see [Restrictions](/sql-non-prepared-plan-cache.md#restrictions).

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

### Reliability

* TiFlash supports query-level data spilling [#7738](https://github.com/pingcap/tiflash/issues/7738) @[windtalker](https://github.com/windtalker)

    Starting from v7.0.0, TiFlash supports controlling data spilling for three operators: `GROUP BY`, `ORDER BY`, and `JOIN`. This feature prevents issues such as query termination or system crashes when the data size exceeds the available memory. However, managing spilling for each operator individually can be cumbersome and ineffective for overall resource control.

    In v7.4.0, TiFlash introduces the query-level data spilling. By setting the memory limit for a query on a TiFlash node using [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) and the memory ratio that triggers data spilling using [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740), you can conveniently manage the memory usage of a query and have better control over TiFlash memory resources.

    For more information, see [documentation](/tiflash/tiflash-spill-disk.md).

* Support user-defined TiKV read timeout [#45380](https://github.com/pingcap/tidb/issues/45380) @[crazycs520](https://github.com/crazycs520)

    Normally, TiKV processes requests very quickly, in a matter of milliseconds. However, when a TiKV node encounters disk I/O jitter or network latency, the request processing time can increase significantly. In versions earlier than v7.4.0, the timeout limit for TiKV requests is fixed and unadjustable. Hence, TiDB has to wait for a fixed-duration timeout response when a TiKV node encounters issues, which results in a noticeable impact on application query performance during jitter.

    TiDB v7.4.0 introduces a new system variable [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740), which lets you customize the timeout for RPC read requests that TiDB sends to TiKV in a query. It means that when the request sent to a TiKV node is delayed due to disk or network issues, TiDB can time out faster and resend the request to other TiKV nodes, thus reducing query latency. If timeouts occur for all TiKV nodes, TiDB will retry using the default timeout. Additionally, you can also use the optimizer hint `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` in a query to set the timeout for TiDB to send a TiKV RPC read request. This enhancement gives TiDB the flexibility to adapt to unstable network or storage environments, improving query performance and enhancing the user experience.

    For more information, see [documentation](/system-variables.md#tikv_client_read_timeout-new-in-v740).

* Support temporarily modifying some system variable values using an optimizer hint [#45892](https://github.com/pingcap/tidb/issues/45892) @[winoros](https://github.com/winoros)

    TiDB v7.4.0 introduces the optimizer hint `SET_VAR()`, which is similar to that of MySQL 8.0. By including the hint `SET_VAR()` in SQL statements, you can temporarily modify the value of system variables during statement execution. This helps you set the environment for different statements. For example, you can actively increase the parallelism of resource-intensive SQL statements or change the optimizer behavior through variables.

    You can find the system variables that can be modified using the hint `SET_VAR()` in [system variables](/system-variables.md). It is strongly recommended not to modify variables that are not explicitly supported, as this might cause unpredictable behavior.

    For more information, see [documentation](/optimizer-hints.md).

* TiFlash supports resource control [#7660](https://github.com/pingcap/tiflash/issues/7660) @[guo-shaoge](https://github.com/guo-shaoge)

    In TiDB v7.1.0, the resource control feature becomes generally available and provides resource management capabilities for TiDB and TiKV. In v7.4.0, TiFlash supports the resource control feature, improving the overall resource management capabilities of TiDB. The resource control of TiFlash is fully compatible with the existing TiDB resource control feature, and the existing resource groups will manage the resources of TiDB, TiKV, and TiFlash at the same time.

    To control whether to enable the TiFlash resource control feature, you can configure the TiFlash parameter `enable_resource_control`. After enabling this feature, TiFlash performs resource scheduling and management based on the resource group configuration of TiDB, ensuring the reasonable allocation and use of overall resources.

    For more information, see [documentation](/tidb-resource-control.md).

* TiFlash supports the pipeline execution model (GA) [#6518](https://github.com/pingcap/tiflash/issues/6518) @[SeaRise](https://github.com/SeaRise)

    Starting from v7.2.0, TiFlash introduces a pipeline execution model. This model centrally manages all thread resources and schedules task execution uniformly, maximizing the utilization of thread resources while avoiding resource overuse. In v7.4.0, TiFlash improves the statistics of thread resource usage, and the pipeline execution model becomes a GA feature and is enabled by default. Since this feature is mutually dependent with the TiFlash resource control feature, TiDB v7.4.0 removes the variable `tidb_enable_tiflash_pipeline_model` used to control whether to enable the pipeline execution model in previous versions. Instead, you can enable or disable the pipeline execution model and the TiFlash resource control feature by configuring the TiFlash parameter `tidb_enable_resource_control`.

    For more information, see [documentation](/tiflash/tiflash-pipeline-model.md).

* Add the option of optimizer mode [#46080](https://github.com/pingcap/tidb/issues/46080) @[time-and-fate](https://github.com/time-and-fate)

    In v7.4.0, TiDB introduces a new system variable [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740), which controls the estimation method used by the optimizer. The default value `moderate` maintains the previous behavior of the optimizer, where it uses runtime statistics to adjust estimations based on data changes. If this variable is set to `determinate`, the optimizer generates execution plans solely based on statistics without considering runtime corrections.

    For long-term stable OLTP applications or situations where you are confident in the existing execution plans, it is recommended to switch to `determinate` mode after testing. This reduces potential plan changes.

    For more information, see [documentation](/system-variables.md#tidb_opt_objective-new-in-v740).

* TiDB resource control supports managing background tasks (experimental) [#44517](https://github.com/pingcap/tidb/issues/44517) @[glorv](https://github.com/glorv)

    Background tasks, such as data backup and automatic statistics collection, are low-priority but consume many resources. These tasks are usually triggered periodically or irregularly. During execution, they consume a lot of resources, thus affecting the performance of online high-priority tasks. Starting from v7.4.0, the TiDB resource control feature supports managing background tasks. This feature reduces the performance impact of low-priority tasks on online applications, enabling rational resource allocation, and greatly improving cluster stability.

    TiDB supports the following types of background tasks:

    - `lightning`: perform import tasks using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) or [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md).
    - `br`: perform backup and restore tasks using [BR](/br/backup-and-restore-overview.md). PITR is not supported.
    - `ddl`: control the resource usage during the batch data write back phase of Reorg DDLs.
    - `stats`: the [collect statistics](/statistics.md#collect-statistics) tasks that are manually executed or automatically triggered by TiDB.

  By default, the task types that are marked as background tasks are empty, and the management of background tasks is disabled. This default behavior is the same as that of versions prior to TiDB v7.4.0. To manage background tasks, you need to manually modify the background task types of the `default` resource group.

    For more information, see [documentation](/tidb-resource-control.md#manage-background-tasks).

* Enhance the ability to lock statistics [#46351](https://github.com/pingcap/tidb/issues/46351) @[hi-rustin](https://github.com/hi-rustin)

    In v7.4.0, TiDB has enhanced the ability to [lock statistics](/statistics.md#lock-statistics). Now, to ensure operational security, locking and unlocking statistics require the same privileges as collecting statistics. In addition, TiDB supports locking and unlocking statistics for specific partitions, providing greater flexibility. If you are confident in queries and execution plans in the database and want to prevent any changes from occurring, you can lock statistics to enhance stability.

    For more information, see [documentation](/statistics.md#lock-statistics).

* Introduce a system variable to control whether to select hash joins for tables [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)

     MySQL 8.0 introduces hash joins for tables as a new feature. This feature is primarily used to join two relatively large tables and result sets. However, for transactional workloads, or some applications running on MySQL 5.7, hash joins for tables might pose a performance risk. MySQL provides the [`optimizer_switch`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_block-nested-loop) to control whether to select hash joins at the global or session level.

    Starting from v7.4.0, TiDB introduces the system variable [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740) to have control over hash joins for tables. It is enabled by default (`ON`). If you are sure that you do not need to select hash joins between tables in your execution plan, you can modify the variable to `OFF` to reduce the possibility of execution plan rollbacks and improve system stability.

    For more information, see [documentation](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740).

### SQL

* TiDB supports partition type management [#42728](https://github.com/pingcap/tidb/issues/42728) @[mjonss](https://github.com/mjonss)

    Before v7.4.0, partition types of partitioned tables in TiDB cannot be modified. Starting from v7.4.0, TiDB supports modifying partitioned tables to non-partitioned tables or non-partitioned tables to partitioned tables, and supports changing partition types. Hence, now you can flexibly adjust the partition type and number for a partitioned table. For example, you can use the `ALTER TABLE t PARTITION BY ...` statement to modify the partition type.

    For more information, see [documentation](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table).

* TiDB supports using the `ROLLUP` modifier and the `GROUPING` function [#44487](https://github.com/pingcap/tidb/issues/44487) @[AilinKid](https://github.com/AilinKid)

    The `WITH ROLLUP` modifier and `GROUPING` function are commonly used in data analysis for multi-dimensional data summarization. Starting from v7.4.0, you can use the `WITH ROLLUP` modifier and `GROUPING` function in the `GROUP BY` clause. For example, you can use the `WITH ROLLUP` modifier in the `SELECT ... FROM ... GROUP BY ... WITH ROLLUP` syntax.

   For more information, see [documentation](/functions-and-operators/group-by-modifier.md).

### DB operations

* Support collation `utf8mb4_0900_ai_ci` and `utf8mb4_0900_bin` [#37566](https://github.com/pingcap/tidb/issues/37566) @[YangKeao](https://github.com/YangKeao) @[zimulala](https://github.com/zimulala) @[bb7133](https://github.com/bb7133)

    TiDB v7.4.0 enhances the support for migrating data from MySQL 8.0 and adds two collations: `utf8mb4_0900_ai_ci` and `utf8mb4_0900_bin`. `utf8mb4_0900_ai_ci` is the default collation in MySQL 8.0.

    TiDB v7.4.0 also introduces the system variable `default_collation_for_utf8mb4` which is compatible with MySQL 8.0. This enables you to specify the default collation for the utf8mb4 character set and provides compatibility with migration or data replication from MySQL 5.7 or earlier versions.

    For more information, see [documentation](/character-set-and-collation.md#character-sets-and-collations-supported-by-tidb).

### Observability

* Support adding session connection IDs and session aliases to logs [#46071](https://github.com/pingcap/tidb/issues/46071) @[lcwangchao](https://github.com/lcwangchao)

     When you troubleshoot a SQL execution problem, it is often necessary to correlate the contents of TiDB component logs to pinpoint the root cause. Starting from v7.4.0, TiDB can write session connection IDs (`CONNECTION_ID`) to session-related logs, including TiDB logs, slow query logs, and slow logs from the coprocessor on TiKV. You can correlate the contents of several types of logs based on session connection IDs to improve troubleshooting and diagnostic efficiency.

     In addition, by setting the session-level system variable [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740), you can add custom identifiers to the logs mentioned above. With this ability to inject your application identification information into the logs, you can correlate the contents of the logs with the application, build the link from the application to the logs, and reduce the difficulty of diagnosis.

* TiDB Dashboard supports displaying execution plans in a table view [#1589](https://github.com/pingcap/tidb-dashboard/issues/1589) @[baurine](https://github.com/baurine)

    In v7.4.0, TiDB Dashboard supports displaying execution plans on the **Slow Query** and **SQL Statement** pages in a table view to improve the diagnosis experience.

    For more information, see [documentation](/dashboard/dashboard-statement-details.md).

### Data migration

* Enhance the `IMPORT INTO` feature [#46704](https://github.com/pingcap/tidb/issues/46704) @[D3Hunter](https://github.com/D3Hunter)

    Starting from v7.4.0, you can add the `CLOUD_STORAGE_URI` option in the `IMPORT INTO` statement to enable the [global sorting](/tidb-global-sort.md) feature (experimental), which helps boost import performance and stability. In the `CLOUD_STORAGE_URI` option, you can specify a cloud storage address for the encoded data.

    In addition, in v7.4.0, the `IMPORT INTO` feature introduces the following functionalities:

    - Support configuring the `Split_File` option, which allows you to split a large CSV file into multiple 256 MiB small CSV files for parallel processing, improving import performance.
    - Support importing compressed CSV and SQL files. The supported compression formats include `.gzip`, `.gz`, `.zstd`, `.zst`, and `.snappy`.

  For more information, see [documentation](/sql-statements/sql-statement-import-into.md).

* Dumpling supports the user-defined terminator when exporting data to CSV files [#46982](https://github.com/pingcap/tidb/issues/46982) @[GMHDBJD](https://github.com/GMHDBJD)

    Before v7.4.0, Dumpling uses `"\r\n"` as the line terminator when exporting data to a CSV file. As a result, certain downstream systems that only recognize `"\n"` as the terminator cannot parse the exported CSV file, or have to use a third-party tool for conversion before parsing the file.

    Starting from v7.4.0, Dumpling introduces a new parameter `--csv-line-terminator`. This parameter allows you to specify a desired terminator when you export data to a CSV file. This parameter supports `"\r\n"` and `"\n"`. The default terminator is `"\r\n"` to keep consistent with earlier versions.

    For more information, see [documentation](/dumpling-overview.md#option-list-of-dumpling).

* TiCDC supports replicating data to Pulsar [#9413](https://github.com/pingcap/tiflow/issues/9413) @[yumchina](https://github.com/yumchina) @[asddongmen](https://github.com/asddongmen)

    Pulsar is a cloud-native and distributed message streaming platform that significantly enhances your real-time data streaming experience. Starting from v7.4.0, TiCDC supports replicating change data to Pulsar in `canal-json` format to achieve seamless integration with Pulsar. With this feature, TiCDC provides you with the ability to easily capture and replicate TiDB changes to Pulsar, offering new possibilities for data processing and analytics capabilities. You can develop your own consumer applications that read and process newly generated change data from Pulsar to meet specific business needs.

    For more information, see [documentation](/ticdc/ticdc-sink-to-pulsar.md).

- TiCDC improves large message handling with claim-check pattern [#9153](https://github.com/pingcap/tiflow/issues/9153) @[3AceShowHand](https://github.com/3AceShowHand)

    Before v7.4.0, TiCDC is unable to send large messages exceeding the maximum message size (`max.message.bytes`) of Kafka to downstream. Starting from v7.4.0, when configuring a changefeed with Kafka as the downstream, you can specify an external storage location for storing the large message, and send a reference message containing the address of the large message in the external storage to Kafka. When consumers receive this reference message, they can retrieve the message content from the external storage address.

    For more information, see [documentation](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.3.0 to the current version (v7.4.0). If you are upgrading from v7.2.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

* Starting with v7.4.0, TiDB is compatible with core features of MySQL 8.0, and `version()` returns the version prefixed with `8.0.11`.

* After TiFlash is upgraded to v7.4.0 from an earlier version, in-place downgrading to the original version is not supported. This is because, starting from v7.4, TiFlash optimizes the data compaction logic of PageStorage V3 to reduce the read and write amplification generated during data compaction, which leads to changes to some of the underlying storage file names.

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| `tidb_enable_tiflash_pipeline_model` | Deleted | This variable was used to control whether to enable the TiFlash pipeline execution model. Starting from v7.4.0, the TiFlash pipeline execution model is automatically enabled when the TiFlash resource control feature is enabled. |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified |  Changes the default value from `ON` to `OFF` after further tests, meaning that non-prepared execution plan cache is disabled. |
| [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740) | Newly added | Controls the default collation for the `utf8mb4` character set. The default value is `utf8mb4_bin`. |
| [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) | Newly added | Specifies the cloud storage URI to enable [Global Sort](/tidb-global-sort.md). |
| [`tidb_opt_enable_hash_join`](/system-variables.md#tidb_opt_enable_hash_join-new-in-v740) | Newly added | Controls whether the optimizer will select hash joins for tables. The value is `ON` by default. If set to `OFF`, the optimizer avoids selecting a hash join of a table unless there is no other execution plan available. |
| [`tidb_opt_objective`](/system-variables.md#tidb_opt_objective-new-in-v740) | Newly added | This variable controls the objective of the optimizer. `moderate` maintains the default behavior in versions prior to TiDB v7.4.0, where the optimizer tries to use more information to generate better execution plans. `determinate` mode tends to be more conservative and makes the execution plan more stable. |
| [`tidb_schema_version_cache_limit`](/system-variables.md#tidb_schema_version_cache_limit-new-in-v740) | Newly added | This variable limits how many historical schema versions can be cached in a TiDB instance. The default value is `16`, which means that TiDB caches 16 historical schema versions by default. |
| [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) | Newly added | This variable is an instance-level system variable. You can use it to control the service scope of TiDB nodes under the [TiDB distributed execution framework](/tidb-distributed-execution-framework.md). When you set `tidb_service_scope` of a TiDB node to `background`, the TiDB distributed execution framework schedules that TiDB node to execute background tasks, such as [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md). |
| [`tidb_session_alias`](/system-variables.md#tidb_session_alias-new-in-v740) |  Newly added | Controls the value of the `session_alias` column in the logs related to the current session. |
| [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) | Newly added | Limits the maximum memory usage for a query on a TiFlash node. When the memory usage of a query exceeds this limit, TiFlash returns an error and terminates the query. The default value is `0`, which means no limit.|
| [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) | Newly added | Controls the threshold for TiFlash [query-level spilling](/tiflash/tiflash-spill-disk.md#query-level-spilling). The default value is `0.7`. |
| [`tikv_client_read_timeout`](/system-variables.md#tikv_client_read_timeout-new-in-v740) | Newly added | Controls the timeout for TiDB to send a TiKV RPC read request in a query. The default value `0` indicates that the default timeout (usually 40 seconds) is used. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610) | Modified | The default value is changed from `false` to `true`, which means the memory limit for caching TiDB statistics is enabled by default. |
| TiFlash | [`flash.compact_log_min_gap`](/tiflash/tiflash-configuration.md) | Newly added | When the gap between the `applied_index` advanced by the current Raft state machine and the `applied_index` at the last disk spilling exceeds `compact_log_min_gap`, TiFlash executes the `CompactLog` command from TiKV and spills data to disk. |
| TiFlash | [`profiles.default.enable_resource_control`](/tiflash/tiflash-configuration.md) | Newly added | Controls whether to enable the TiFlash resource control feature. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | Modified | Change the default value from `4` to `5`. The new format can reduce the number of physical files by merging smaller files. |
| Dumpling  | [`--csv-line-terminator`](/dumpling-overview.md#option-list-of-dumpling) | Newly added | Specifies the desired terminator of CSV files . This option supports `"\r\n"` and `"\n"`. The default value is `"\r\n"`, which is consistent with the earlier versions. |
| TiCDC | [`claim-check-storage-uri`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage) | Newly added | When `large-message-handle-option` is set to `claim-check`, `claim-check-storage-uri` must be set to a valid external storage address. Otherwise, creating a changefeed results in an error. |
| TiCDC | [`large-message-handle-compression`](/ticdc/ticdc-sink-to-kafka.md#ticdc-data-compression) | Newly added | Controls whether to enable compression during encoding. The default value is empty, which means not enabled. |
| TiCDC | [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#send-large-messages-to-external-storage) | Modified | This configuration item adds a new value `claim-check`. When it is set to `claim-check`, TiCDC Kafka sink supports sending the message to external storage when the message size exceeds the limit and sends a message to Kafka containing the address of this large message in external storage. |

## Improvements

+ TiDB

    - Optimize memory usage and performance for `ANALYZE` operations on partitioned tables [#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @[hawkingrei](https://github.com/hawkingrei)
    - Optimize memory usage and performance for statistics garbage collection [#31778](https://github.com/pingcap/tidb/issues/31778) @[winoros](https://github.com/winoros)
    - Optimize the pushdown of `limit` for index merge intersections to improve query performance [#46863](https://github.com/pingcap/tidb/issues/46863) @[AilinKid](https://github.com/AilinKid)
    - Improve the cost model to minimize the chances of mistakenly choosing a full table scan when `IndexLookup` involves many table retrieval tasks [#45132](https://github.com/pingcap/tidb/issues/45132) @[qw4990](https://github.com/qw4990)
    - Optimize the join elimination rule to improve the query performance of `join on unique keys` [#46248](https://github.com/pingcap/tidb/issues/46248) @[fixdb](https://github.com/fixdb)
    - Change the collation of multi-valued index columns to `binary` to avoid execution failure [#46717](https://github.com/pingcap/tidb/issues/46717) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Optimize memory usage of Resolver to prevent OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
    - Eliminate LRUCache in Router objects to reduce memory usage and prevent OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - Reduce memory usage of TiCDC Resolver [#15412](https://github.com/tikv/tikv/issues/15412) @[overvenus](https://github.com/overvenus)
    - Reduce memory fluctuations caused by RocksDB compaction [#15324](https://github.com/tikv/tikv/issues/15324) @[overvenus](https://github.com/overvenus)
    - Reduce memory consumption in the flow control module of Partitioned Raft KV [#15269](https://github.com/tikv/tikv/issues/15269) @[overvenus](https://github.com/overvenus)
    - Add the backoff mechanism for the PD client in the process of connection retries, which gradually increases retry intervals during error retries to reduce PD pressure [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - Support dynamically adjusting `background_compaction` of RocksDB [#15424](https://github.com/tikv/tikv/issues/15424) @[glorv](https://github.com/glorv)

+ PD

    - Optimize TSO tracing information for easier investigation of TSO-related issues [#6856](https://github.com/tikv/pd/pull/6856) @[tiancaiamao](https://github.com/tiancaiamao)
    - Support reusing HTTP Client connections to reduce memory usage [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - Improve the speed of PD automatically updating cluster status when the backup cluster is disconnected [#6883](https://github.com/tikv/pd/issues/6883) @[disksing](https://github.com/disksing)
    - Enhance the configuration retrieval method of the resource control client to dynamically fetch the latest configurations [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Improve write performance during random write workloads by optimizing the spilling policy of the TiFlash write process [#7564](https://github.com/pingcap/tiflash/issues/7564) @[CalvinNeo](https://github.com/CalvinNeo)
    - Add more metrics about the Raft replication process for TiFlash [#8068](https://github.com/pingcap/tiflash/issues/8068) @[CalvinNeo](https://github.com/CalvinNeo)
    - Reduce the number of small files to avoid potential exhaustion of file system inodes [#7595](https://github.com/pingcap/tiflash/issues/7595) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
        - Enhance support for connection reuse of log backup and PITR restore tasks by setting `MaxIdleConns` and `MaxIdleConnsPerHost` parameters in the HTTP client [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - Improve fault tolerance of BR when it fails to connect to PD or external S3 storage [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - Add a new restore parameter `WaitTiflashReady`. When this parameter is enabled, the restore operation will be completed after TiFlash replicas are successfully replicated [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)
        - Reduce the CPU overhead of log backup `resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Optimize the execution logic of replicating the `ADD INDEX` DDL operations to avoid blocking subsequent DML statements [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)

    + TiDB Lightning

        - Optimize the retry logic of TiDB Lightning during the Region scatter phase [#46203](https://github.com/pingcap/tidb/issues/46203) @[mittalrishabh](https://github.com/mittalrishabh)
        - Optimize the retry logic of TiDB Lightning for the `no leader` error during the data import phase [#46253](https://github.com/pingcap/tidb/issues/46253) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB

    - Fix the issue that the `BatchPointGet` operator returns incorrect results for tables that are not hash partitioned [#45889](https://github.com/pingcap/tidb/issues/45889) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `BatchPointGet` operator returns incorrect results for hash partitioned tables [#46779](https://github.com/pingcap/tidb/issues/46779) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the TiDB parser remains in a state and causes parsing failure [#45898](https://github.com/pingcap/tidb/issues/45898) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `EXCHANGE PARTITION` does not check constraints [#45922](https://github.com/pingcap/tidb/issues/45922) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `tidb_enforce_mpp` system variable cannot be correctly restored [#46214](https://github.com/pingcap/tidb/issues/46214) @[djshow832](https://github.com/djshow832)
    - Fix the issue that the `_` in the `LIKE` clause is incorrectly handled [#46287](https://github.com/pingcap/tidb/issues/46287) [#46618](https://github.com/pingcap/tidb/issues/46618) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `schemaTs` is set to 0 when TiDB fails to obtain the schema [#46325](https://github.com/pingcap/tidb/issues/46325) @[hihihuhu](https://github.com/hihihuhu)
    - Fix the issue that `Duplicate entry` might occur when `AUTO_ID_CACHE=1` is set [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB recovers slowly after a panic when `AUTO_ID_CACHE=1` is set [#46454](https://github.com/pingcap/tidb/issues/46454) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `next_row_id` in `SHOW CREATE TABLE` is incorrect when `AUTO_ID_CACHE=1` is set [#46545](https://github.com/pingcap/tidb/issues/46545) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the panic issue that occurs during parsing when using CTE in subqueries [#45838](https://github.com/pingcap/tidb/issues/45838) @[djshow832](https://github.com/djshow832)
    - Fix the issue that restrictions on partitioned tables remain on the original table when `EXCHANGE PARTITION` fails or is canceled [#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the definition of List partitions does not support using both `NULL` and empty strings [#45694](https://github.com/pingcap/tidb/issues/45694) @[mjonss](https://github.com/mjonss)
    - Fix the issue of not being able to detect data that does not comply with partition definitions during partition exchange [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `tmp-storage-quota` configuration does not take effect [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `WEIGHT_STRING()` function does not match the collation [#45725](https://github.com/pingcap/tidb/issues/45725) @[dveeden](https://github.com/dveeden)
    - Fix the issue that an error in Index Join might cause the query to get stuck [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the behavior is inconsistent with MySQL when comparing a `DATETIME` or `TIMESTAMP` column with a number constant [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - Fix the incorrect result that occurs when comparing unsigned types with `Duration` type constants [#45410](https://github.com/pingcap/tidb/issues/45410) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that access path pruning logic ignores the `READ_FROM_STORAGE(TIFLASH[...])` hint, which causes the `Can't find a proper physical plan` error [#40146](https://github.com/pingcap/tidb/issues/40146) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `GROUP_CONCAT` cannot parse the `ORDER BY` column [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that HashCode is repeatedly calculated for deeply nested expressions, which causes high memory usage and OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `cast(col)=range` condition causes FullScan when CAST has no precision loss [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that when Aggregation is pushed down through Union in MPP execution plans, the results are incorrect [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that bindings with `in (?)` cannot match `in (?, ... ?)` [#44298](https://github.com/pingcap/tidb/issues/44298) @[qw4990](https://github.com/qw4990)
    - Fix the error caused by not considering the connection collation when `non-prep plan cache` reuses the execution plan [#47008](https://github.com/pingcap/tidb/issues/47008) @[qw4990](https://github.com/qw4990)
    - Fix the issue that no warning is reported when an executed plan does not hit the plan cache [#46159](https://github.com/pingcap/tidb/issues/46159) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `plan replayer dump explain` reports an error [#46197](https://github.com/pingcap/tidb/issues/46197) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that executing DML statements with CTE can cause panic [#46083](https://github.com/pingcap/tidb/issues/46083) @[winoros](https://github.com/winoros)
    - Fix the issue that the `TIDB_INLJ` hint does not take effect when joining two sub-queries [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the results of `MERGE_JOIN` are incorrect [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)

+ TiKV

    - Fix the issue that TiKV fails to start when Titan is enabled and the `Blob file deleted twice` error occurs [#15454](https://github.com/tikv/tikv/issues/15454) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue of no data in the Thread Voluntary and Thread Nonvoluntary monitoring panels [#15413](https://github.com/tikv/tikv/issues/15413) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the data error of continuously increasing raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - Fix the TiKV panic issue caused by incorrect metadata of Region [#13311](https://github.com/tikv/tikv/issues/13311) @[zyguan](https://github.com/zyguan)
    - Fix the issue of QPS dropping to 0 after switching from `sync_recovery` to `sync` [#15366](https://github.com/tikv/tikv/issues/15366) @[nolouch](https://github.com/nolouch)
    - Fix the issue that Online Unsafe Recovery does not abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the potential memory leak issue caused by CpuRecord [#15304](https://github.com/tikv/tikv/issues/15304) @[overvenus](https://github.com/overvenus)
    - Fix the issue that `"Error 9002: TiKV server timeout"` occurs when the backup cluster is down and the primary cluster is queried [#12914](https://github.com/tikv/tikv/issues/12914) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the backup TiKV gets stuck when TiKV restarts after the primary cluster recovers [#12320](https://github.com/tikv/tikv/issues/12320) @[disksing](https://github.com/disksing)

+ PD

    - Fix the issue that the Region information is not updated and saved during Flashback [#6912](https://github.com/tikv/pd/issues/6912) @[overvenus](https://github.com/overvenus)
    - Fix the issue of slow switching of PD Leaders due to slow synchronization of store config [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that the groups are not considered in Scatter Peers [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that RU consumption less than 0 causes PD to crash [#6973](https://github.com/tikv/pd/issues/6973) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that modified isolation levels are not synchronized to the default placement rules [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the client-go regularly updating `min-resolved-ts` might cause PD OOM when the cluster is large [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - Fix the issue that the `max_snapshot_lifetime` metric is displayed incorrectly on Grafana [#7713](https://github.com/pingcap/tiflash/issues/7713) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that some metrics about the maximum duration are not correct [#8076](https://github.com/pingcap/tiflash/issues/8076) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that TiDB incorrectly reports that an MPP task has failed [#7177](https://github.com/pingcap/tiflash/issues/7177) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - Fix an issue that the misleading error message `resolve lock timeout` covers up the actual error when backup fails [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that recovering implicit primary keys using PITR might cause conflicts [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - Fix the issue that recovering meta-kv using PITR might cause errors [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - Fix the errors in BR integration test cases [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)

    + TiCDC

        - Fix the issue that TiCDC accesses the invalid old address during PD scaling up and down [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that changefeed fails in some scenarios [#9309](https://github.com/pingcap/tiflow/issues/9309) [#9450](https://github.com/pingcap/tiflow/issues/9450) [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9685](https://github.com/pingcap/tiflow/issues/9685) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96) 
        - Fix the issue that replication write conflicts might occur when the unique keys for multiple rows are modified in one transaction on the upstream [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that a replication error occurs when multiple tables are renamed in the same DDL statement on the upstream [#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @[CharlesCheung96](https://github.com/CharlesCheung96) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that Chinese characters are not validated in CSV files [#9609](https://github.com/pingcap/tiflow/issues/9609) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that upstream TiDB GC is blocked after all changefeeds are removed [#9633](https://github.com/pingcap/tiflow/issues/9633) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue of uneven distribution of write keys among nodes when `scale-out` is enabled [#9665](https://github.com/pingcap/tiflow/issues/9665) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that sensitive user information is recorded in the logs [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - Fix the issue that DM cannot handle conflicts correctly with case-insensitive collations [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)
        - Fix the DM validator deadlock issue and enhance retries [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that replication lag returned by DM keeps growing when a failed DDL is skipped and no subsequent DDLs are executed [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that DM cannot properly track upstream table schemas when skipping online DDLs [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM skips all DMLs when resuming a task in optimistic mode [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM skips partition DDLs in optimistic mode [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that inserting data returns an error after TiDB Lightning imports the `NONCLUSTERED auto_increment` and `AUTO_ID_CACHE=1` tables [#46100](https://github.com/pingcap/tidb/issues/46100) @[tiancaiamao](https://github.com/tiancaiamao)
        - Fix the issue that checksum still reports errors when `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that data import fails when the PD cluster address changes [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [aidendou](https://github.com/aidendou)
- [coderplay](https://github.com/coderplay)
- [fatelei](https://github.com/fatelei)
- [highpon](https://github.com/highpon)
- [hihihuhu](https://github.com/hihihuhu) (First-time contributor)
- [isabella0428](https://github.com/isabella0428)
- [jiyfhust](https://github.com/jiyfhust)
- [JK1Zhang](https://github.com/JK1Zhang)
- [joker53-1](https://github.com/joker53-1) (First-time contributor)
- [L-maple](https://github.com/L-maple)
- [mittalrishabh](https://github.com/mittalrishabh)
- [paveyry](https://github.com/paveyry)
- [shawn0915](https://github.com/shawn0915)
- [tedyu](https://github.com/tedyu)
- [yumchina](https://github.com/yumchina)
- [ZhuohaoHe](https://github.com/ZhuohaoHe)
