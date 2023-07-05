---
title: TiDB 7.0.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.0.0.
---

# TiDB 7.0.0 Release Notes

Release date: March 30, 2023

TiDB version: 7.0.0-[DMR](/releases/versioning.md#development-milestone-releases)

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.0/quick-start-with-tidb) | [Installation package](https://www.pingcap.com/download/?version=v7.0.0#version-list)

In v7.0.0-DMR, the key new features and improvements are as follows:

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
    <td rowspan="2">Scalability and Performance<br/></td>
    <td>Session level <a href="https://docs.pingcap.com/tidb/v7.0/sql-non-prepared-plan-cache" target="_blank">non-prepared SQL plan cache</a> (experimental)</td>
    <td>Support automatically reusing plan cache at the session level to reduce compilation and shorten the query time for the same SQL patterns without manually setting prepare statements in advance.</td>
  </tr>
  <tr>
    <td>TiFlash supports the <a href="https://docs.pingcap.com/tidb/v7.0/tiflash-disaggregated-and-s3" target="_blank">disaggregated storage and compute architecture and S3 shared storage</a> (experimental)</td>
    <td>TiFlash introduces a cloud-native architecture as an option:
      <ul>
        <li>Disaggregates TiFlash's compute and storage, which is a milestone for elastic HTAP resource utilization.</li>
        <li>Introduces S3-based storage engine, which can provide shared storage at a lower cost.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability<br/></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.0/tidb-resource-control" target="_blank">Resource control enhancement</a> (experimental) </td>
    <td>Support using resource groups to allocate and isolate resources for various applications or workloads within one cluster. In this release, TiDB adds support for different resource binding modes (user, session, and statement levels) and user-defined priorities. Additionally, you can also use commands to perform resource calibration (estimation for the whole resource amount).</td>
  </tr>
  <tr>
    <td>TiFlash supports <a href="https://docs.pingcap.com/tidb/v7.0/tiflash-spill-disk" target="_blank">spill to disk</a></td>
    <td>TiFlash supports intermediate result spill to disk to mitigate OOMs in data-intensive operations such as aggregations, sorts, and hash joins.</td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.0/time-to-live" target="_blank">Row-level TTL</a> (GA)</td>
    <td>Support managing database size and improve performance by automatically expiring data of a certain age.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.0/partitioned-table#reorganize-partitions" target="_blank">Reorganize <code>LIST</code>/<code>RANGE</code> partition</a></td>
    <td>The <code>REORGANIZE PARTITION</code> statement can be used for merging adjacent partitions or splitting one partition into many, which provides better usability of partitioned tables.</td>
  </tr>
  <tr>
    <td rowspan="2">DB Operations and Observability<br/></td>
    <td>TiDB enhances the functionalities of <a href="https://docs.pingcap.com/tidb/v7.0/sql-statement-load-data" target="_blank"><code>LOAD DATA</code> statements</a> (experimental)</td>
    <td>TiDB enhances the functionalities of <code>LOAD DATA</code> SQL statements, such as supporting data import from S3/GCS.<br/></td>
  </tr>
  <tr>
    <td>TiCDC supports <a href="https://docs.pingcap.com/tidb/v7.0/ticdc-sink-to-cloud-storage" target="_blank">object storage sink</a> (GA)</td>
    <td>TiCDC supports replicating row change events to object storage services, including Amazon S3, GCS, Azure Blob Storage, and NFS.<br/></td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* TiFlash supports the disaggregated storage and compute architecture and supports object storage in this architecture (experimental) [#6882](https://github.com/pingcap/tiflash/issues/6882) @[flowbehappy](https://github.com/flowbehappy)

    Before v7.0.0, TiFlash only supports the coupled storage and compute architecture. In this architecture, each TiFlash node acts as both storage and compute node, and its computing and storage capabilities cannot be independently expanded. In addition, TiFlash nodes can only use local storage.

    Starting from v7.0.0, TiFlash also supports the disaggregated storage and compute architecture. In this architecture, TiFlash nodes are divided into two types (Compute Nodes and Write Nodes) and support object storage that is compatible with S3 API. Both types of nodes can be independently scaled for computing or storage capacities. The **disaggregated storage and compute architecture** and  **coupled storage and compute architecture** cannot be used in the same cluster or converted to each other. You can configure which architecture to use when you deploy TiFlash.

    For more information, see [documentation](/tiflash/tiflash-disaggregated-and-s3.md).

### Performance

* Achieve compatibility between Fast Online DDL and PITR [#38045](https://github.com/pingcap/tidb/issues/38045) @[Leavrth](https://github.com/Leavrth)

    In TiDB v6.5.0, [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is not fully compatible with [PITR](/br/backup-and-restore-overview.md). To ensure a full data backup, it is recommended to first stop the PITR background backup task, quickly add indexes using Fast Online DDL, and then resume the PITR backup task.

    Starting from TiDB v7.0.0, Fast Online DDL and PITR are fully compatible. When restoring cluster data through PITR, the index operations added via Fast Online DDL during log backup will be automatically replayed to achieve compatibility.

    For more information, see [documentation](/ddl-introduction.md).

* TiFlash supports null-aware semi join and null-aware anti semi join operators [#6674](https://github.com/pingcap/tiflash/issues/6674) @[gengliqi](https://github.com/gengliqi)

    When using `IN`, `NOT IN`, `= ANY`, or `!= ALL` operators in correlated subqueries, TiDB optimizes the computing performance by converting them to semi join or anti semi join. If the join key column might be `NULL`, a null-aware join algorithm is required, such as [Null-aware semi join](/explain-subqueries.md#null-aware-semi-join-in-and--any-subqueries) and [Null-aware anti semi join](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries).

    Before v7.0.0, TiFlash does not support null-aware semi join and null-aware anti semi join operators, preventing these subqueries from being directly pushed down to TiFlash. Starting from v7.0.0, TiFlash supports null-aware semi join and null-aware anti semi join operators. If a SQL statement contains these correlated subqueries, the tables in the query have TiFlash replicas, and [MPP mode](/tiflash/use-tiflash-mpp-mode.md) is enabled, the optimizer automatically determines whether to push down null-aware semi join and null-aware anti semi join operators to TiFlash to improve overall performance.

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* TiFlash supports using FastScan (GA) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    Starting from v6.3.0, TiFlash introduces FastScan as an experimental feature. In v7.0.0, this feature becomes generally available. You can enable FastScan using the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630). By sacrificing strong consistency, this feature significantly improves table scan performance. If the corresponding table only involves `INSERT` operations without any `UPDATE`/`DELETE` operations, FastScan can keep strong consistency and improve the scan performance.

    For more information, see [documentation](/tiflash/use-fastscan.md).

* TiFlash supports late materialization (experimental) [#5829](https://github.com/pingcap/tiflash/issues/5829) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

    When processing a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query by default, and then filters and aggregates the data based on the query conditions. Late materialization is an optimization method that supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

    The TiFlash late materialization feature is not enabled by default. You can enable it by setting the `tidb_opt_enable_late_materialization` system variable to `OFF`. When the feature is enabled, the TiDB optimizer will determine which filter conditions to be pushed down based on statistics and filter conditions.

    For more information, see [documentation](/tiflash/tiflash-late-materialization.md).

* Support caching execution plans for non-prepared statements (experimental) [#36598](https://github.com/pingcap/tidb/issues/36598) @[qw4990](https://github.com/qw4990)

    The execution plan cache is important for improving the load capacity of concurrent OLTP and TiDB already supports [Prepared execution plan cache](/sql-prepared-plan-cache.md). In v7.0.0, TiDB can also cache execution plans for non-Prepare statements, expanding the scope of execution plan cache and improving the concurrent processing capacity of TiDB.

    This feature is disabled by default. You can enable it by setting the system variable [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) to `ON`. For stability reasons, TiDB v7.0.0 allocates a new area for caching non-prepared execution plans and you can set the cache size using the system variable [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size). Additionally, this feature has certain restrictions on SQL statements. For more information, see [Restrictions](/sql-non-prepared-plan-cache.md#restrictions).

    For more information, see [documentation](/sql-non-prepared-plan-cache.md).

* TiDB removes the execution plan cache constraint for subqueries [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    TiDB v7.0.0 removes the execution plan cache constraint for subqueries. This means that the execution plan of SQL statements with subqueries can now be cached, such as `SELECT * FROM t WHERE a > (SELECT ...)`. This feature further expands the application scope of execution plan cache and improves the execution efficiency of SQL queries.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* TiKV supports automatically generating empty log files for log recycling [#14371](https://github.com/tikv/tikv/issues/14371) @[LykxSassinator](https://github.com/LykxSassinator)

    In v6.3.0, TiKV introduced the [Raft log recycling](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) feature to reduce long-tail latency caused by write load. However, log recycling can only take effect when the number of Raft log files reaches a certain threshold, making it difficult for users to directly experience the throughput improvement brought by this feature.

    In v7.0.0, a new configuration item called `raft-engine.prefill-for-recycle` was introduced to improve user experience. This item controls whether empty log files are generated for recycling when the process starts. When this configuration is enabled, TiKV automatically fills a batch of empty log files during initialization, ensuring that log recycling takes effect immediately after initialization.

    For more information, see [documentation](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700).

* Support deriving the TopN or Limit operator from [window functions](/functions-and-operators/expressions-pushed-down.md) to improve window function performance [#13936](https://github.com/tikv/tikv/issues/13936) @[windtalker](https://github.com/windtalker)

    This feature is disabled by default. To enable it, you can set the session variable [tidb_opt_derive_topn](/system-variables.md#tidb_opt_derive_topn-new-in-v700) to `ON`.

    For more information, see [documentation](/derive-topn-from-window.md).

* Support creating unique indexes through Fast Online DDL [#40730](https://github.com/pingcap/tidb/issues/40730) @[tangenta](https://github.com/tangenta)

    TiDB v6.5.0 supports creating ordinary secondary indexes via Fast Online DDL. TiDB v7.0.0 supports creating unique indexes via Fast Online DDL. Compared to v6.1.0, adding unique indexes to large tables is expected to be several times faster with improved performance.

    For more information, see [documentation](/ddl-introduction.md).

### Reliability

* Enhance the resource control feature (experimental) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    TiDB enhances the resource control feature based on resource groups. This feature significantly improves the resource utilization efficiency and performance of TiDB clusters. The introduction of the resource control feature is a milestone for TiDB. You can divide a distributed database cluster into multiple logical units, map different database users to corresponding resource groups, and set the quota for each resource group as needed. When the cluster resources are limited, all resources used by sessions in the same resource group are limited to the quota. In this way, even if a resource group is over-consumed, the sessions in other resource groups are not affected.

    With this feature, you can combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set quotas, so as to achieve the maximum utilization of resources. In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

    This feature provides a built-in Resource Control Dashboard for the actual usage of resources in Grafana, assisting you to allocate resources more rationally. It also supports dynamic resource management capabilities based on both session and statement levels (Hint). The introduction of this feature will help you gain more precise control over the resource usage of your TiDB cluster, and dynamically adjust quotas based on actual needs.

    In TiDB v7.0.0, you can set the absolute scheduling priority (`PRIORITY`) for resource groups to guarantee that important services can get resources. It also extends the way to set resource groups.

    You can use resource groups in the following ways:

    - User level. Bind a user using the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statements to a specific resource group. After binding a resource group to a user, sessions newly created by the user are automatically bound to the corresponding resource group.
    - Session level. Set the resource group used by the current session via [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md).
    - Statement level. Set the resource group used by the current statement via [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name).

  For more information, see [documentation](/tidb-resource-control.md).

* Support a checkpoint mechanism for Fast Online DDL, improving fault tolerance and automatic recovery capability [#42164](https://github.com/pingcap/tidb/issues/42164) @[tangenta](https://github.com/tangenta)

    TiDB v7.0.0 introduces a checkpoint mechanism for [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630), which significantly improves its fault tolerance and automatic recovery capabilities. By periodically recording and synchronizing the DDL progress, ongoing DDL operations can continue to be executed in Fast Online DDL mode even if there is a TiDB DDL Owner failure or switch. This makes the execution of DDL more stable and efficient.

    For more information, see [documentation](/ddl-introduction.md).

* TiFlash supports spilling to disk [#6528](https://github.com/pingcap/tiflash/issues/6528) @[windtalker](https://github.com/windtalker)

    To improve execution performance, TiFlash runs data entirely in memory as much as possible. When the amount of data exceeds the total size of memory, TiFlash terminates the query to avoid system crashes caused by running out of memory. Therefore, the amount of data that TiFlash can handle is limited by the available memory.

    Starting from v7.0.0, TiFlash supports spilling to disk. By adjusting the threshold of memory usage for operators ([`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700), [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700), and [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)), you can control the maximum amount of memory that an operator can use. When the memory used by the operator exceeds the threshold, it automatically writes data to disk. This sacrifices some performance but allows for processing of more data.

    For more information, see [documentation](/tiflash/tiflash-spill-disk.md).

* Improve the efficiency of collecting statistics [#41930](https://github.com/pingcap/tidb/issues/41930) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    In v7.0.0, TiDB further optimizes the logic of collecting statistics, reducing the collection time by about 25%. This optimization improves the operational efficiency and stability of large database clusters, reducing the impact of statistics collection on cluster performance.

* Add new optimizer hints for MPP optimization [#39710](https://github.com/pingcap/tidb/issues/39710) @[Reminiscent](https://github.com/Reminiscent)

    In v7.0.0, TiDB adds a series of optimizer hints to influence the generation of MPP execution plans.

    - [`SHUFFLE_JOIN()`](/optimizer-hints.md#shuffle_joint1_name--tl_name-): takes effect on MPP. It hints the optimizer to use the Shuffle Join algorithm for the specified table.
    - [`BROADCAST_JOIN()`](/optimizer-hints.md#broadcast_joint1_name--tl_name-): takes effect on MPP. It hints the optimizer to use the Broadcast Join algorithm for the specified table.
    - [`MPP_1PHASE_AGG()`](/optimizer-hints.md#mpp_1phase_agg): takes effect on MPP. It hints the optimizer to use the one-phase aggregation algorithm for all aggregate functions in the specified query block.
    - [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg): takes effect on MPP. It hints the optimizer to use the two-phase aggregation algorithm for all aggregate functions in the specified query block.

  MPP optimizer hints can help you intervene in HTAP queries, improving performance and stability for HTAP workloads.

  For more information, see [documentation](/optimizer-hints.md).

* Optimizer hints support specifying join methods and join orders [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)

    In v7.0.0, the optimizer hint [`LEADING()`](/optimizer-hints.md#leadingt1_name--tl_name-) can be used in conjunction with hints that affect the join method, and their behaviors are compatible. In the case of multi-table joins, you can effectively specify the optimal join method and join order, thereby enhancing the control of optimizer hints over execution plans.

    The new hint behavior has minor changes. To ensure forward compatibility, TiDB introduces the system variable [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700). When this variable is set to `OFF`, the optimizer hint behavior is compatible with earlier versions. When you upgrade your cluster from earlier versions to v7.0.0 or later versions, this variable will be set to `OFF`. To obtain more flexible hint behavior, after you confirm that the behavior does not cause a performance regression, it is strongly recommended to set this variable to `ON`.

    For more information, see [documentation](/optimizer-hints.md).

### Availability

* Support the `prefer-leader` option, which provides higher availability for read operations and reduces response latency in unstable network conditions [#40905](https://github.com/pingcap/tidb/issues/40905) @[LykxSassinator](https://github.com/LykxSassinator)

    You can control TiDB's data reading behavior through the system variable [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40). In v7.0.0, this variable adds the `prefer-leader` option. When the variable is set to `prefer-leader`, TiDB prioritizes selecting the leader replica to perform read operations. When the processing speed of the leader replica slows down significantly, such as due to disk or network performance fluctuations, TiDB selects other available follower replicas to perform read operations, providing higher availability and reducing response latency.

    For more information, see [documentation](/develop/dev-guide-use-follower-read.md).

### SQL

* Time to live (TTL) is generally available [#39262](https://github.com/pingcap/tidb/issues/39262) @[lcwangchao](https://github.com/lcwangchao) @[YangKeao](https://github.com/YangKeao)

    TTL provides row-level lifecycle control policies. In TiDB, tables with TTL attributes set automatically check and delete expired row data based on the configuration. The goal of TTL is to help users periodically clean up unnecessary data in time while minimizing the impact on cluster workloads.

    For more information, see [documentation](/time-to-live.md).

* Support `ALTER TABLE…REORGANIZE PARTITION` [#15000](https://github.com/pingcap/tidb/issues/15000) @[mjonss](https://github.com/mjonss)

    TiDB supports the `ALTER TABLE...REORGANIZE PARTITION` syntax. Using this syntax, you can reorganize some or all of the partitions of a table, including merging, splitting, or other modifications, without losing data.

    For more information, see [documentation](/partitioned-table.md#reorganize-partitions).

* Support Key partitioning [#41364](https://github.com/pingcap/tidb/issues/41364) @[TonsnakeLin](https://github.com/TonsnakeLin)

    Now TiDB supports Key partitioning. Both Key partitioning and Hash partitioning can evenly distribute data into a certain number of partitions. The difference is that Hash partitioning only supports distributing data based on a specified integer expression or an integer column, while Key partitioning supports distributing data based on a column list, and partitioning columns of Key partitioning are not limited to the integer type.

    For more information, see [documentation](/partitioned-table.md#key-partitioning).

### DB operations

* TiCDC supports replicating change data to storage services (GA) [#6797](https://github.com/pingcap/tiflow/issues/6797) @[zhaoxinyu](https://github.com/zhaoxinyu)

    TiCDC supports replicating changed data to Amazon S3, GCS, Azure Blob Storage, NFS, and other S3-compatible storage services. Storage services are reasonably priced and easy to use. If you are not using Kafka, you can use storage services. TiCDC saves the changed logs to a file and then sends it to the storage services instead. From the storage services, your own consumer program can read the newly generated changed log files periodically. Currently, TiCDC supports replicating changed logs in canal-json and CSV formats to the storage service.

    For more information, see [documentation](/ticdc/ticdc-sink-to-cloud-storage.md).

* TiCDC OpenAPI v2 [#8019](https://github.com/pingcap/tiflow/issues/8019) @[sdojjy](https://github.com/sdojjy)

    TiCDC provides OpenAPI v2. Compared with OpenAPI v1, OpenAPI v2 provides more comprehensive support for replication tasks. The features provided by TiCDC OpenAPI are a subset of the [`cdc cli` tool](/ticdc/ticdc-manage-changefeed.md). You can query and operate TiCDC clusters via OpenAPI v2, such as getting TiCDC node status, checking cluster health status, and managing replication tasks.

    For more information, see [documentation](/ticdc/ticdc-open-api-v2.md).

* [DBeaver](https://dbeaver.io/) v23.0.1 supports TiDB by default [#17396](https://github.com/dbeaver/dbeaver/issues/17396) @[Icemap](https://github.com/Icemap)

    - Provides an independent TiDB module, icon, and logo.
    - The default configuration supports [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless), making it easier to connect to TiDB Serverless.
    - Supports identifying TiDB versions to display or hide foreign key tabs.
    - Supports visualizing SQL execution plans in `EXPLAIN` results.
    - Supports highlighting TiDB keywords such as `PESSIMISTIC`, `OPTIMISTIC`, `AUTO_RANDOM`, `PLACEMENT`, `POLICY`, `REORGANIZE`, `EXCHANGE`, `CACHE`, `NONCLUSTERED`, and `CLUSTERED`.
    - Supports highlighting TiDB functions such as  `TIDB_BOUNDED_STALENESS`, `TIDB_DECODE_KEY`, `TIDB_DECODE_PLAN`, `TIDB_IS_DDL_OWNER`, `TIDB_PARSE_TSO`, `TIDB_VERSION`, `TIDB_DECODE_SQL_DIGESTS`, and `TIDB_SHARD`.

  For more information, see [DBeaver documentation](https://github.com/dbeaver/dbeaver/wiki).

### Data migration

* Enhance the functionalities of `LOAD DATA` statements and support importing data from cloud storage (experimental) [#40499](https://github.com/pingcap/tidb/issues/40499) @[lance6716](https://github.com/lance6716)

    Before TiDB v7.0.0, the `LOAD DATA` statement could only import data files from the client side. If you wanted to import data from cloud storage, you had to rely on TiDB Lightning. However, deploying TiDB Lightning separately would bring additional deployment and management costs. In v7.0.0, you can directly import data from cloud storage using the `LOAD DATA` statement. Some examples of the feature are as follows:

    - Supports importing data from Amazon S3 and Google Cloud Storage to TiDB. Supports importing multiple source files to TiDB in one go with wildcards.
    - Support using `DEFINED NULL BY` to define null.
    - Support source files in CSV and TSV formats.

  For more information, see [documentation](/sql-statements/sql-statement-load-data.md).

* TiDB Lightning supports enabling compressed transfers when sending key-value pairs to TiKV (GA) [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky)

    Starting from v6.6.0, TiDB Lightning supports compressing locally encoded and sorted key-value pairs for network transfer when sending them to TiKV, thus reducing the amount of data transferred over the network and lowering the network bandwidth overhead. In the earlier TiDB versions before this feature is supported, TiDB Lightning requires relatively high network bandwidth and incurs high traffic charges in case of large data volumes.

    In v7.0.0, this feature becomes GA and is disabled by default. To enable it, you can set the `compress-kv-pairs` configuration item of TiDB Lightning to `"gzip"` or `"gz"`.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v6.6.0 to the current version (v7.0.0). If you are upgrading from v6.5.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

* TiDB removes the constraint that the auto-increment column must be an index [#40580](https://github.com/pingcap/tidb/issues/40580) @[tiancaiamao](https://github.com/tiancaiamao)

    Before v7.0.0, TiDB's behavior is consistent with MySQL, requiring the auto-increment column to be an index or index prefix. Starting from v7.0.0, TiDB removes the constraint that the auto-increment column must be an index or index prefix. Now you can define the primary key of a table more flexibly and use the auto-increment column to implement sorting and pagination more conveniently. This also avoids the write hotspot problem caused by the auto-increment column and improves query performance by using the table with clustered indexes. With the new release, you can create a table using the following syntax:

    ```sql
    CREATE TABLE test1 (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `k` int(11) NOT NULL DEFAULT '0',
        `c` char(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        PRIMARY KEY(`k`, `id`)
    );
    ```

    This feature does not affect TiCDC data replication.

    For more information, see [documentation](/mysql-compatibility.md#auto-increment-id).

* TiDB supports Key partitions, as shown in the following example:

    ```sql
    CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT) PARTITION BY KEY(store_id) PARTITIONS 4;
    ```

    Starting from v7.0.0, TiDB supports Key partitions and can parse the MySQL `PARTITION BY LINEAR KEY` syntax. However, TiDB ignores the `LINEAR` keyword and uses a non-linear hash algorithm instead. Currently, the `KEY` partition type does not support partition statements with an empty partition column list.

    For more information, see [documentation](/partitioned-table.md#key-partitioning).

### Behavior changes

* TiCDC fixes the issue of incorrect encoding of `FLOAT` data in Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    When upgrading the TiCDC cluster to v7.0.0, if a table replicated using Avro contains the `FLOAT` data type, you need to manually adjust the compatibility policy of Confluent Schema Registry to `None` before upgrading so that the changefeed can successfully update the schema. Otherwise, after upgrading, the changefeed will be unable to update the schema and enter an error state.

* Starting from v7.0.0, [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) system variable no longer takes effect on the [`LOAD DATA` statement](/sql-statements/sql-statement-load-data.md).

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| `tidb_pessimistic_txn_aggressive_locking` | Deleted | This variable is renamed to [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700). |
| [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) | Modified | Takes effect starting from v7.0.0 and controls whether to enable the [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) feature. |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630) | Modified | Changes the default value from `OFF` to `ON` after further tests, meaning that TiDB applies Null-Aware Hash Join when Anti Join is generated by subqueries led by special set operators `NOT IN` and `!= ALL` by default. |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) | Modified | Changes the default value from `OFF` to `ON`, meaning that the cluster isolates resources by resource group by default. Resource Control is enabled by default in v7.0.0, so that you can use this feature whenever you want. |
| [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size) | Modified | Takes effect starting from v7.0.0 and controls the maximum number of execution plans that can be cached by [Non-prepared plan cache](/sql-non-prepared-plan-cache.md). |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) | Modified | Starting from v7.0.0, this variable is no longer effective for cursor fetch read in the prepared statement protocol. |
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-new-in-v700) | Newly added | This variable controls whether Index Join is supported when the inner table has `Selection` or `Projection` operators on it. |
| [`tidb_enable_plan_cache_for_subquery`](/system-variables.md#tidb_enable_plan_cache_for_subquery-new-in-v700) | Newly added | This variable controls whether Prepared Plan Cache caches queries that contain subqueries. |
| [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700) | Newly added | This variable controls whether to enable the [`PLAN REPLAYER CONTINUOUS CAPTURE`](/sql-plan-replayer.md#use-plan-replayer-continuous-capture) feature. The default value `OFF` means to disable the feature. |
| [`tidb_load_based_replica_read_threshold`](/system-variables.md#tidb_load_based_replica_read_threshold-new-in-v700) | Newly added | This variable sets the threshold for triggering load-based replica read. The feature controlled by this variable is not fully functional in TiDB v7.0.0. Do not change the default value. |
| [`tidb_opt_advanced_join_hint`](/system-variables.md#tidb_opt_advanced_join_hint-new-in-v700) | Newly added | This variable controls whether the join method hint influences the optimization of join reorder. The default value is `ON`, which means the new compatible control mode is used. The value `OFF` means the behavior before v7.0.0 is used. For forward compatibility, the value of this variable is set to `OFF` when the cluster is upgraded from an earlier version to v7.0.0 or later. |
| [`tidb_opt_derive_topn`](/system-variables.md#tidb_opt_derive_topn-new-in-v700) | Newly added | This variable controls whether to enable the [Derive TopN or Limit from Window Functions](/derive-topn-from-window.md) optimization rule. The default value is `OFF`, which means the optimization rule is not enabled. |
| [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) | Newly added | This variable controls whether to enable the [TiFlash Late Materialization](/tiflash/tiflash-late-materialization.md) feature. The default value is `OFF`, which means the feature is not enabled. |
| [`tidb_opt_ordering_index_selectivity_threshold`](/system-variables.md#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) | Newly added | This variable controls how the optimizer selects indexes when the SQL statement contains `ORDER BY` and `LIMIT` clauses and has filtering conditions. |
| [`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700) | Newly added | Controls whether to enable the enhanced pessimistic lock-waking model to reduce the tail latency of transactions under single-row conflict scenarios. The default value is `ON`. When the cluster is upgraded from an earlier version to v7.0.0 or later, the value of this variable is set to `OFF`. |
| [`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700) | Newly added | This variable is used to limit the concurrency of TTL tasks across the entire cluster. The default value `-1` means that the TTL tasks are the same as the number of TiKV nodes. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | `server.snap-max-write-bytes-per-sec` | Deleted | This parameter is renamed to [`server.snap-io-max-bytes-per-sec`](/tikv-configuration-file.md#snap-io-max-bytes-per-sec). |
| TiKV | [`raft-engine.enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) | Modified | The default value changes from `false` to `true`. |
| TiKV | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval) | Modified | The default value changes from `"1s"` to `"20s"`. This modification can increase the interval of the regular advancement of Resolved TS and reduce the traffic consumption between TiKV nodes. |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | Modified | The default value changes from `false` to `true`. |
| TiKV | [`raft-engine.prefill-for-recycle`](/tikv-configuration-file.md#prefill-for-recycle-new-in-v700) | Newly added | Controls whether to generate empty log files for log recycling in Raft Engine. The default value is `false`. |
| PD | [`degraded-mode-wait-duration`](/pd-configuration-file.md#degraded-mode-wait-duration) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the waiting time for triggering the degraded mode. The default value is `0s`. |
| PD | [`read-base-cost`](/pd-configuration-file.md#read-base-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the basis factor for conversion from a read request to RU. The default value is `0.25`. |
| PD | [`read-cost-per-byte`](/pd-configuration-file.md#read-cost-per-byte) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the basis factor for conversion from read flow to RU. The default value is `1/ (64 * 1024)`. |
| PD | [`read-cpu-ms-cost`](/pd-configuration-file.md#read-cpu-ms-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the basis factor for conversion from CPU to RU. The default value is `1/3`. |
| PD | [`write-base-cost`](/pd-configuration-file.md#write-base-cost) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the basis factor for conversion from a write request to RU. The default value is `1`. |
| PD | [`write-cost-per-byte`](/pd-configuration-file.md#write-cost-per-byte) | Newly added | A [Resource Control](/tidb-resource-control.md)-related configuration item. It controls the basis factor for conversion from write flow to RU. The default value is `1/1024`. |
| TiFlash | [`flash.disaggregated_mode`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | In the disaggregated architecture of TiFlash, it indicates whether this TiFlash node is a write node or a compute node. The value can be `tiflash_write` or `tiflash_compute`. |
| TiFlash | [`storage.s3.endpoint`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The endpoint to connect to S3. |
| TiFlash | [`storage.s3.bucket`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The bucket where TiFlash stores all data. |
| TiFlash | [`storage.s3.root`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The root directory of data storage in S3 bucket. |
| TiFlash | [`storage.s3.access_key_id`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | `ACCESS_KEY_ID` for accessing S3. |
| TiFlash | [`storage.s3.secret_access_key`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | `SECRET_ACCESS_KEY` for accessing S3. |
| TiFlash | [`storage.remote.cache.dir`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The local data cache directory of TiFlash compute node. |
| TiFlash | [`storage.remote.cache.capacity`](/tiflash/tiflash-disaggregated-and-s3.md) | Newly added | The size of the local data cache directory of TiFlash compute node. |
| TiDB Lightning | [`add-index-by-sql`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls whether to use SQL to add indexes in physical import mode. The default value is `false`, which means that TiDB Lightning will encode both row data and index data into KV pairs and import them into TiKV together. The advantage of adding indexes using SQL is to separate the import of data and the import of indexes, which can quickly import data. Even if the index creation fails after the data is imported, the data consistency is not affected. |
| TiCDC | [`enable-table-across-nodes`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Determines whether to divide a table into multiple sync ranges according to the number of Regions. These ranges can be replicated by multiple TiCDC nodes. |
| TiCDC      | [`region-threshold`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | When `enable-table-across-nodes` is enabled, this feature only takes effect on tables with more than `region-threshold` Regions.      |
| DM | [`analyze`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)  | Newly added | Controls whether to execute the `ANALYZE TABLE <table>` operation on each table after CHECKSUM is completed. It can be configured as `"required"`/`"optional"`/`"off"`. The default value is `"optional"`. |
| DM | [`range-concurrency`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)  | Newly added | Controls the concurrency of dm-worker writing KV data to TiKV. |
| DM | [`compress-kv-pairs`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)  | Newly added | Controls whether to enable compression when dm-worker sends KV data to TiKV. Currently, only gzip is supported. The default value is empty, which means no compression. |
| DM | [`pd-addr`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)  | Newly added | Controls the address of the downstream PD server in the Physical Import mode. You can fill in either one or more PD servers. If this configuration item is empty, use the PD address information from the TiDB query by default. |

## Improvements

+ TiDB

    - Introduce the `EXPAND` operator to optimize the performance of SQL queries with multiple `DISTINCT` in a single `SELECT` statement [#16581](https://github.com/pingcap/tidb/issues/16581) @[AilinKid](https://github.com/AilinKid)
    - Support more SQL formats for Index Join [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    - Avoid globally sorting partitioned table data in TiDB in some cases [#26166](https://github.com/pingcap/tidb/issues/26166) @[Defined2014](https://github.com/Defined2014)
    - Support using `fair lock mode` and `lock only if exists` at the same time [#42068](https://github.com/pingcap/tidb/issues/42068) @[MyonKeminta](https://github.com/MyonKeminta)
    - Support printing transaction slow logs and transaction internal events [#41863](https://github.com/pingcap/tidb/issues/41863) @[ekexium](https://github.com/ekexium)
    - Support the `ILIKE` operator [#40943](https://github.com/pingcap/tidb/issues/40943) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ PD

    - Add a new monitoring metric for scheduling failures due to the store limit [#6043](https://github.com/tikv/pd/issues/6043) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Reduce TiFlash's memory usage on write path [#7144](https://github.com/pingcap/tiflash/issues/7144) @[hongyunyan](https://github.com/hongyunyan)
    - Reduce TiFlash's restart time in scenarios with many tables [#7146](https://github.com/pingcap/tiflash/issues/7146) @[hongyunyan](https://github.com/hongyunyan)
    - Support pushing down the `ILIKE` operator [#6740](https://github.com/pingcap/tiflash/issues/6740) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + TiCDC

        - Support distributing data changes of a single large table to multiple TiCDC nodes in scenarios where Kafka is the downstream, thus solving the scalability issue of single tables in data integration scenarios of large-scale TiDB clusters [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)

            You can enable this feature by setting the TiCDC configuration item `enable_table_across_nodes` to `true`. You can use `region_threshold` to specify that when the number of Regions for a table exceeds this threshold, TiCDC starts distributing data changes of the corresponding table to multiple TiCDC nodes.

        - Support splitting transactions in the redo applier to improve its throughput and reduce RTO in disaster recovery scenarios [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Improve the table scheduling to split a single table more evenly across various TiCDC nodes [#8247](https://github.com/pingcap/tiflow/issues/8247) @[overvenus](https://github.com/overvenus)
        - Add the Large Row monitoring metrics in MQ sink [#8286](https://github.com/pingcap/tiflow/issues/8286) @[hi-rustin](https://github.com/hi-rustin)
        - Reduce network traffic between TiKV and TiCDC nodes in scenarios where a Region contains data of multiple tables [#6346](https://github.com/pingcap/tiflow/issues/6346) @[overvenus](https://github.com/overvenus)
        - Move the P99 metrics panel of Checkpoint TS and Resolved TS to the Lag analyze panel [#8524](https://github.com/pingcap/tiflow/issues/8524) @[hi-rustin](https://github.com/hi-rustin)
        - Support applying DDL events in redo logs [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support splitting and scheduling tables to TiCDC nodes based on upstream write throughput [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    + TiDB Lightning

        - TiDB Lightning Physical Import Mode supports separating data import and index import to improve import speed and stability [#42132](https://github.com/pingcap/tidb/issues/42132) @[gozssky](https://github.com/gozssky)

           Add the `add-index-by-sql` parameter. The default value is `false`, which means that TiDB Lightning encodes both row data and index data into KV pairs and import them into TiKV together. If you set it to `true`, it means that TiDB Lightning adds indexes via the `ADD INDEX` SQL statement after importing the row data to improve import speed and stability.

        - Add the `tikv-importer.keyspace-name` parameter. The default value is an empty string, which means TiDB Lightning automatically gets the key space name of the corresponding tenant to import data. If you specify a value, the specified key space name will be used to import data. This parameter provides flexibility in the configuration of TiDB Lightning when you import data to a multi-tenant TiDB cluster. [#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## Bug fixes

+ TiDB

    - Fix the issue of missing updates when upgrading TiDB from v6.5.1 to a later version [#41502](https://github.com/pingcap/tidb/issues/41502) @[chrysan](https://github.com/chrysan)
    - Fix the issue that the default values of some system variables are not modified after upgrading [#41423](https://github.com/pingcap/tidb/issues/41423) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that Coprocessor request types related to adding indexes are displayed as unknown [#41400](https://github.com/pingcap/tidb/issues/41400) @[tangenta](https://github.com/tangenta)
    - Fix the issue of returning "PessimisticLockNotFound" when adding an index [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    - Fix the issue of mistakenly returning `found duplicate key` when adding a unique index [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    - Fix the panic issue when adding an index [#41880](https://github.com/pingcap/tidb/issues/41880) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiFlash reports an error for generated columns during execution [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB might not be able to obtain statistics correctly when there is a time type [#41938](https://github.com/pingcap/tidb/issues/41938) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that full index scans might cause errors when prepared plan cache is enabled [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that `IFNULL(NOT NULL COLUMN, ...)` might return incorrect results [#41734](https://github.com/pingcap/tidb/issues/41734) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that TiDB might produce incorrect results when all data in a partitioned table is in a single Region [#41801](https://github.com/pingcap/tidb/issues/41801) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that TiDB might produce incorrect results when different partitioned tables appear in a single SQL statement [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - Fix the issue that statistics auto-collection might not trigger correctly on a partitioned table after adding a new index to the partitioned table [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that TiDB might read incorrect column statistics information after collecting statistics twice in a row [#42073](https://github.com/pingcap/tidb/issues/42073) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that IndexMerge might produce incorrect results when prepare plan cache is enabled [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    - Fix the issue that IndexMerge might have goroutine leakage [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that non-BIGINT unsigned integers might produce incorrect results when compared with strings/decimals [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that killing a previous `ANALYZE` statement due to memory over-limit might cause the current `ANALYZE` statement in the same session to be killed [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that data race might occur during the information collection process of the batch coprocessor [#41412](https://github.com/pingcap/tidb/issues/41412) @[you06](https://github.com/you06)
    - Fix the issue that an assertion error prevents printing MVCC information for partitioned tables [#40629](https://github.com/pingcap/tidb/issues/40629) @[ekexium](https://github.com/ekexium)
    - Fix the issue that fair lock mode adds locking to non-existent keys [#41527](https://github.com/pingcap/tidb/issues/41527) @[ekexium](https://github.com/ekexium)
    - Fix the issue that `INSERT IGNORE` and `REPLACE` statements do not lock keys that do not modify values [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)

+ PD

    - Fix the issue that the Region Scatter operation might cause uneven distribution of leaders [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that data race might occur when getting PD members during startup [#6069](https://github.com/tikv/pd/issues/6069) @[rleungx](https://github.com/rleungx)
    - Fix the issue that data race might occur when collecting hotspot statistics [#6069](https://github.com/tikv/pd/issues/6069) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that switching placement rule might cause uneven distribution of leaders [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue that Decimal division does not round up the last digit in certain cases [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that Decimal cast rounds up incorrectly in certain cases [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TopN/Sort operators produce incorrect results after enabling the new collation [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that TiFlash reports an error when aggregating a result set larger than 12 million rows on a single TiFlash node [#6993](https://github.com/pingcap/tiflash/issues/6993) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue of insufficient wait time for splitting Region retry during the PITR recovery process [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)
        - Fix the issue of recovery failures due to `memory is limited` error encountered during the PITR recovery process [#41983](https://github.com/pingcap/tidb/issues/41983) @[joccau](https://github.com/joccau)
        - Fix the issue that PITR log backup progress does not advance when a PD node is down [#14184](https://github.com/tikv/tikv/issues/14184) @[YuJuncen](https://github.com/YuJuncen)
        - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that restarting the changefeed might cause data loss or that the checkpoint cannot advance [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)
        - Fix the data race issue in DDL sink [#8238](https://github.com/pingcap/tiflow/issues/8238) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the changefeed in the `stopped` status might restart automatically [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the TiCDC server panics when all downstream Kafka servers are unavailable [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that data might be lost when the downstream is MySQL and the executed statement is incompatible with TiDB [#8453](https://github.com/pingcap/tiflow/issues/8453) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that rolling upgrade might cause TiCDC OOM or that the checkpoint gets stuck [#8329](https://github.com/pingcap/tiflow/issues/8329) @[overvenus](https://github.com/overvenus)
        - Fix the issue that graceful upgrade for TiCDC clusters fails on Kubernetes [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)

    + TiDB Data Migration (DM)

        - Fix the issue that when a DM worker node uses Google Cloud Storage, due to too frequent breakpoints, the request frequency limit of Google Cloud Storage is reached and the DM worker cannot write the data into Google Cloud Storage, thus causing the full data to fail to load [#8482](https://github.com/pingcap/tiflow/issues/8482) @[maxshuang](https://github.com/maxshuang)
        - Fix the issue that when multiple DM tasks replicate the same downstream data at the same time and all use the downstream metadata table to record the breakpoint information, the breakpoint information of all tasks is written to the same metadata table and uses the same task ID [#8500](https://github.com/pingcap/tiflow/issues/8500) @[maxshuang](https://github.com/maxshuang)

    + TiDB Lightning

        - Fix the issue that when Physical Import Mode is used for importing data, if there is an `auto_random` column in the composite primary key of the target table, but the value of the column is not specified in the source data, TiDB Lightning does not generate data for the `auto_random` column automatically [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that when Logical Import Mode is used for importing data, the import fails due to lack of the `CONFIG` permission for the target cluster [#41915](https://github.com/pingcap/tidb/issues/41915) @[lichunzhu](https://github.com/lichunzhu)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [AntiTopQuark](https://github.com/AntiTopQuark)
- [blacktear23](https://github.com/blacktear23)
- [BornChanger](https://github.com/BornChanger)
- [Dousir9](https://github.com/Dousir9)
- [erwadba](https://github.com/erwadba)
- [HappyUncle](https://github.com/HappyUncle)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [liumengya94](https://github.com/liumengya94)
- [woofyzhao](https://github.com/woofyzhao)
- [xiaguan](https://github.com/xiaguan)
