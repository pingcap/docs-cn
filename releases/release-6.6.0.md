---
title: TiDB 6.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.6.0.
---

# TiDB 6.6.0 Release Notes

Release date: February 20, 2023

TiDB version: 6.6.0-[DMR](/releases/versioning.md#development-milestone-releases)

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.6/quick-start-with-tidb) | [Installation package](https://www.pingcap.com/download/?version=v6.6.0#version-list)

In v6.6.0-DMR, the key new features and improvements are as follows:

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
    <td rowspan="3">Scalability and Performance<br /></td>
    <td>TiKV supports <a href="https://docs.pingcap.com/tidb/v6.6/partitioned-raft-kv" target="_blank">Partitioned Raft KV storage engine</a> (experimental)</td>
    <td>TiKV introduces the Partitioned Raft KV storage engine, and each Region uses an independent RocksDB instance, which can easily expand the storage capacity of the cluster from TB to PB and provide more stable write latency and stronger scalability.</td>
  </tr>
  <tr>
    <td>TiKV supports <a href="https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_store_batch_size" target="_blank">batch aggregating data requests</a></td>
    <td>This enhancement significantly reduces total RPCs in TiKV batch-get operations. In situations where data is highly dispersed and the gRPC thread pool has insufficient resources, batching coprocessor requests can improve performance by more than 50%.</td>
  </tr>
  <tr>
    <td>TiFlash supports <a href="https://docs.pingcap.com/tidb/v6.6/stale-read" target="_blank">Stale Read</a> and <a href="https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression" target="_blank">compression exchange</a></td>
    <td>TiFlash supports the stale read feature, which can improve query performance in scenarios where real-time requirements are not restricted. TiFlash supports data compression to improve the efficiency of parallel data exchange, and the overall TPC-H performance improves by 10%, which can save more than 50% of the network usage.</td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and availability<br /></td>
    <td><a href="https://docs.pingcap.com/tidb/v6.6/tidb-resource-control" target="_blank">Resource control</a> (experimental)</td>
    <td>Support resource management based on resource groups, which maps database users to the corresponding resource groups and sets quotas for each resource group based on actual needs.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v6.6/sql-plan-management#create-a-binding-according-to-a-historical-execution-plan" target="_blank">Historical SQL binding</a></td>
    <td>Support binding historical execution plans and quickly binding execution plans on TiDB Dashboard.</td>
  </tr>
  <tr>
    <td rowspan="2">SQL functionalities<br /></td>
    <td><a href="https://docs.pingcap.com/tidb/v6.6/foreign-key" target="_blank">Foreign key</a></td>
    <td>Support MySQL-compatible foreign key constraints to maintain data consistency and improve data quality.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v6.6/sql-statement-create-index/#multi-valued-index" target="_blank">Multi-valued index</a> (experimental)</td>
    <td>Introduce MySQL-compatible multi-valued indexes and enhance the JSON type to improve TiDB's compatibility with MySQL 8.0.</td>
  </tr>
  <tr>
    <td>DB operations and observability<br /></td>
    <td><a href="https://docs.pingcap.com/tidb/v6.6/dm-precheck#check-items-for-physical-import" target="_blank">DM supports physical import</a> (experimental)</td>
    <td>TiDB Data Migration (DM) integrates TiDB Lightning's physical import mode to improve the performance of full data migration, with performance being up to 10 times faster.</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Support Partitioned Raft KV storage engine (experimental) [#11515](https://github.com/tikv/tikv/issues/11515) [#12842](https://github.com/tikv/tikv/issues/12842) @[busyjay](https://github.com/busyjay) @[tonyxuqqi](https://github.com/tonyxuqqi) @[tabokie](https://github.com/tabokie) @[bufferflies](https://github.com/bufferflies) @[5kbpers](https://github.com/5kbpers) @[SpadeA-Tang](https://github.com/SpadeA-Tang) @[nolouch](https://github.com/nolouch)

    Before TiDB v6.6.0, TiKV's Raft-based storage engine used a single RocksDB instance to store the data of all 'Regions' of the TiKV instance. To support larger clusters more stably, starting from TiDB v6.6.0, a new TiKV storage engine is introduced, which uses multiple RocksDB instances to store TiKV Region data, and the data of each Region is independently stored in a separate RocksDB instance. The new engine can better control the number and level of files in the RocksDB instance, achieve physical isolation of data operations between Regions, and support stably managing more data. You can see it as TiKV managing multiple RocksDB instances through partitioning, which is why the feature is named Partitioned-Raft-KV. The main advantage of this feature is better write performance, faster scaling, and larger volume of data supported with the same hardware. It can also support larger cluster scales.

    Currently, this feature is experimental and not recommended for use in production environments.

    For more information, see [documentation](/partitioned-raft-kv.md).

* Support the distributed parallel execution framework for DDL operations (experimental) [#37125](https://github.com/pingcap/tidb/issues/37125) @[zimulala](https://github.com/zimulala)

    In previous versions, only one TiDB instance in the entire TiDB cluster was allowed to handle schema change tasks as a DDL owner. To further improve DDL concurrency for large table's DDL operations, TiDB v6.6.0 introduces the distributed parallel execution framework for DDL, through which all TiDB instances in the cluster can concurrently execute the `StateWriteReorganization` phase of the same task to speed up DDL execution. This feature is controlled by the system variable [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) and is currently only supported for `Add Index` operations.

### Performance

* Support a stable wake-up model for pessimistic lock queues [#13298](https://github.com/tikv/tikv/issues/13298) @[MyonKeminta](https://github.com/MyonKeminta)

    If an application encounters frequent single-point pessimistic lock conflicts, the existing wake-up mechanism cannot guarantee the time for transactions to acquire locks, which causes high long-tail latency and even lock acquisition timeout. Starting from v6.6.0, you can enable a stable wake-up model for pessimistic locks by setting the value of the system variable [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660) to `ON`. In this wake-up model, the wake-up sequence of a queue can be strictly controlled to avoid the waste of resources caused by invalid wake-ups. In scenarios with serious lock conflicts, the stable wake-up model can reduce long-tail latency and the P99 response time.

    Tests indicate this reduces tail latency 40-60%.

    For more information, see [documentation](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660).

* Batch aggregate data requests [#39361](https://github.com/pingcap/tidb/issues/39361) @[cfzjywxk](https://github.com/cfzjywxk) @[you06](https://github.com/you06)

    When TiDB sends a data request to TiKV, TiDB compiles the request into different sub-tasks according to the Region where the data is located, and each sub-task only processes the request of a single Region. When the data to be accessed is highly dispersed, even if the size of the data is not large, many sub-tasks will be generated, which in turn will generate many RPC requests and consume extra time. Starting from v6.6.0, TiDB supports partially merging data requests that are sent to the same TiKV instance, which reduces the number of sub-tasks and the overhead of RPC requests. In the case of high data dispersion and insufficient gRPC thread pool resources, batching requests can improve performance by more than 50%.

    This feature is enabled by default. You can set the batch size of requests using the system variable [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size).

* Remove the limit on `LIMIT` clauses [#40219](https://github.com/pingcap/tidb/issues/40219) @[fzzf678](https://github.com/fzzf678)

    Starting from v6.6.0, TiDB plan cache supports caching execution plans with a variable as the `LIMIT` parameter, such as `LIMIT ?` or `LIMIT 10, ?`. This feature allows more SQL statements to benefit from plan cache, thus improving execution efficiency.

    For more information, see [documentation](/sql-prepared-plan-cache.md).

* TiFlash supports data exchange with compression [#6620](https://github.com/pingcap/tiflash/issues/6620) @[solotzg](https://github.com/solotzg)

    To cooperate with multiple nodes for computing, the TiFlash engine needs to exchange data among different nodes. When the size of the data to be exchanged is very large, the performance of data exchange might affect the overall computing efficiency. In v6.6.0, the TiFlash engine introduces a compression mechanism to compress the data that needs to be exchanged when necessary, and then to perform the exchange, thereby improving the efficiency of data exchange.

    For more information, see [documentation](/explain-mpp.md#mpp-version-and-exchange-data-compression).

* TiFlash supports the Stale Read feature [#4483](https://github.com/pingcap/tiflash/issues/4483) @[hehechen](https://github.com/hehechen)

   The Stale Read feature has been generally available (GA) since v5.1.1, which allows you to read historical data at a specific timestamp or within a specified time range. Stale read can reduce read latency and improve query performance by reading data from local TiKV replicas directly. Before v6.6.0, TiFlash does not support Stale Read. Even if a table has TiFlash replicas, Stale Read can only read its TiKV replicas.

   Starting from v6.6.0, TiFlash supports the Stale Read feature. When you query the historical data of a table using the [`AS OF TIMESTAMP`](/as-of-timestamp.md) syntax or the [`tidb_read_staleness`](/tidb-read-staleness.md) system variable, if the table has a TiFlash replica, the optimizer now can choose to read the corresponding data from the TiFlash replica, thus further improving query performance.

    For more information, see [documentation](/stale-read.md).

* Support pushing down the `regexp_replace` string function to TiFlash [#6115](https://github.com/pingcap/tiflash/issues/6115) @[xzhangxian1008](https://github.com/xzhangxian1008)

### Reliability

* Support resource control based on resource groups (experimental) [#38825](https://github.com/pingcap/tidb/issues/38825) @[nolouch](https://github.com/nolouch) @[BornChanger](https://github.com/BornChanger) @[glorv](https://github.com/glorv) @[tiancaiamao](https://github.com/tiancaiamao) @[Connor1996](https://github.com/Connor1996) @[JmPotato](https://github.com/JmPotato) @[hnes](https://github.com/hnes) @[CabinfeverB](https://github.com/CabinfeverB) @[HuSharp](https://github.com/HuSharp)

    Now you can create resource groups for a TiDB cluster, bind different database users to corresponding resource groups, and set quotas for each resource group according to actual needs. When the cluster resources are limited, all resources used by sessions in the same resource group will be limited to the quota. In this way, even if a resource group is over-consumed, the sessions in other resource groups are not affected. TiDB provides a built-in view of the actual usage of resources on Grafana dashboards, assisting you to allocate resources more rationally.

    The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

    With this feature, you can:

    - Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
    - Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.

  In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

  In v6.6, you need to enable both TiDB's global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) and the TiKV configuration item [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to enable resource control. Currently, the supported quota method is based on "[Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)". RU is TiDB's unified abstraction unit for system resources such as CPU and IO.

  For more information, see [documentation](/tidb-resource-control.md).

* Binding historical execution plans is GA [#39199](https://github.com/pingcap/tidb/issues/39199) @[fzzf678](https://github.com/fzzf678)

    In v6.5.0, TiDB extends the binding targets in the [`CREATE [GLOBAL | SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md) statements and supports creating bindings according to historical execution plans. In v6.6.0, this feature is GA. The selection of execution plans is not limited to the current TiDB node. Any historical execution plan generated by any TiDB node can be selected as the target of [SQL binding](/sql-statements/sql-statement-create-binding.md), which further improves the feature usability.

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan).

* Add several optimizer hints [#39964](https://github.com/pingcap/tidb/issues/39964) @[Reminiscent](https://github.com/Reminiscent)

    TiDB adds several optimizer hints in v6.6.0 to control the execution plan selection of `LIMIT` operations.

    - [`ORDER_INDEX()`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-): tells the optimizer to use the specified index, to keep the order of the index when reading data, and generates plans similar to `Limit + IndexScan(keep order: true)`.
    - [`NO_ORDER_INDEX()`](/optimizer-hints.md#no_order_indext1_name-idx1_name--idx2_name-): tells the optimizer to use the specified index, not to keep the order of the index when reading data, and generates plans similar to `TopN + IndexScan(keep order: false)`.

  Continuously introducing optimizer hints provides users with more intervention methods, helps solve SQL performance issues, and improves the stability of overall performance.

* Support dynamically managing the resource usage of DDL operations (experimental) [#38025](https://github.com/pingcap/tidb/issues/38025) @[hawkingrei](https://github.com/hawkingrei)

    TiDB v6.6.0 introduces resource management for DDL operations to reduce the impact of DDL changes on online applications by automatically controlling the CPU usage of these operations. This feature is effective only after the [DDL distributed parallel execution framework](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) is enabled.

### Availability

* Support configuring `SURVIVAL_PREFERENCE` for [placement rules in SQL](/placement-rules-in-sql.md) [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)

    `SURVIVAL_PREFERENCES` provides data survival preference settings to increase the disaster survivability of data. By specifying `SURVIVAL_PREFERENCE`, you can control the following:

    - For TiDB clusters deployed across cloud regions, when a cloud region fails, the specified databases or tables can survive in another cloud region.
    - For TiDB clusters deployed in a single cloud region, when an availability zone fails, the specified databases or tables can survive in another availability zone.

  For more information, see [documentation](/placement-rules-in-sql.md#survival-preferences).

* Support rolling back DDL operations via the `FLASHBACK CLUSTER TO TIMESTAMP` statement [#14088](https://github.com/tikv/tikv/pull/14088) @[Defined2014](https://github.com/Defined2014) @[JmPotato](https://github.com/JmPotato)

    The [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) statement supports restoring the entire cluster to a specified point in time within the Garbage Collection (GC) lifetime. In TiDB v6.6.0, this feature adds support for rolling back DDL operations. This can be used to quickly undo a DML or DDL misoperation on a cluster, roll back a cluster within minutes, and roll back a cluster multiple times on the timeline to determine when specific data changes occurred.

    For more information, see [documentation](/sql-statements/sql-statement-flashback-to-timestamp.md).

### SQL

* Support MySQL-compatible foreign key constraints [#18209](https://github.com/pingcap/tidb/issues/18209) [@crazycs520](https://github.com/crazycs520)

    TiDB v6.6.0 introduces the foreign key constraints feature, which is compatible with MySQL. This feature supports referencing within a table or between tables, constraints validation, and cascade operations. This feature helps to migrate applications to TiDB, maintain data consistency, improve data quality, and facilitate data modeling.

    For more information, see [documentation](/foreign-key.md).

* Support the MySQL-compatible multi-valued index (experimental) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990)

    TiDB introduces the MySQL-compatible multi-valued index in v6.6.0. Filtering the values of an array in a JSON column is a common operation, but normal indexes cannot help speed up such an operation. Creating a multi-valued index on an array can greatly improve filtering performance. If an array in the JSON column has a multi-valued index, you can use the multi-value index to filter the retrieval conditions with `MEMBER OF()`, `JSON_CONTAINS()`, `JSON_OVERLAPS()` functions, thereby reducing much I/O consumption and improving operation speed.

    Introducing multi-valued indexes further enhances TiDB's support for the JSON data type and also improves TiDB's compatibility with MySQL 8.0.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index).

### DB operations

* Support configuring read-only storage nodes for resource-consuming tasks @[v01dstar](https://github.com/v01dstar)

    In production environments, some read-only operations might consume a large number of resources regularly and affect the performance of the entire cluster, such as backups and large-scale data reading and analysis. TiDB v6.6.0 supports configuring read-only storage nodes for resource-consuming read-only tasks to reduce the impact on the online application. Currently, TiDB, TiSpark, and BR support reading data from read-only storage nodes. You can configure read-only storage nodes according to [steps](/best-practices/readonly-nodes.md#procedures) and specify where data is read through the system variable `tidb_replica_read`, the TiSpark configuration item `spark.tispark.replica_read`, or the br command line argument `--replica-read-label`, to ensure the stability of cluster performance.

    For more information, see [documentation](/best-practices/readonly-nodes.md).

* Support dynamically modifying `store-io-pool-size` [#13964](https://github.com/tikv/tikv/issues/13964) @[LykxSassinator](https://github.com/LykxSassinator)

    The TiKV configuration item [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) specifies the allowable number of threads that process Raft I/O tasks, which can be adjusted when tuning TiKV performance. Before v6.6.0, this configuration item cannot be modified dynamically. Starting from v6.6.0, you can modify this configuration without restarting the server, which means more flexible performance tuning.

    For more information, see [documentation](/dynamic-config.md).

* Support specifying the SQL script executed upon TiDB cluster initialization [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

    When you start a TiDB cluster for the first time, you can specify the SQL script to be executed by configuring the command line parameter `--initialize-sql-file`. You can use this feature when you need to perform such operations as modifying the value of a system variable, creating a user, or granting privileges.

    For more information, see [documentation](/tidb-configuration-file.md#initialize-sql-file-new-in-v660).

* TiDB Data Migration (DM) integrates with TiDB Lightning's physical import mode for up to a 10x performance boost for full migration (experimental) @[lance6716](https://github.com/lance6716)

    In v6.6.0, DM full migration capability integrates with physical import mode of TiDB Lightning, which enables DM to improve the performance of full data migration by up to 10 times, greatly reducing the migration time in large data volume scenarios.

    Before v6.6.0, for large data volume scenarios, you were required to configure physical import tasks in TiDB Lightning separately for fast full data migration, and then use DM for incremental data migration, which was a complex configuration. Starting from v6.6.0, you can migrate large data volumes without the need to configure TiDB Lightning tasks; one DM task can accomplish the migration.

    For more information, see [documentation](/dm/dm-precheck.md#check-items-for-physical-import).

* TiDB Lightning adds a new configuration parameter `"header-schema-match"` to address the issue of mismatched column names between the source file and the target table @[dsdashun](https://github.com/dsdashun)

    In v6.6.0, TiDB Lightning adds a new profile parameter `"header-schema-match"`. The default value is `true`, which means the first row of the source CSV file is treated as the column name, and consistent with that in the target table. If the field name in the CSV table header does not match the column name of the target table, you can set this configuration to `false`. TiDB Lightning will ignore the error and continue to import the data in the order of the columns in the target table.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

* TiDB Lightning supports enabling compressed transfers when sending key-value pairs to TiKV [#41163](https://github.com/pingcap/tidb/issues/41163) @[gozssky](https://github.com/gozssky)

    Starting from v6.6.0, TiDB Lightning supports compressing locally encoded and sorted key-value pairs for network transfer when sending them to TiKV, thus reducing the amount of data transferred over the network and lowering the network bandwidth overhead. In the earlier TiDB versions before this feature is supported, TiDB Lightning requires relatively high network bandwidth and incurs high traffic charges in case of large data volumes.

    This feature is disabled by default. To enable it, you can set the `compress-kv-pairs` configuration item of TiDB Lightning to `"gzip"` or `"gz"`.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task).

* The TiKV-CDC tool is now GA and supports subscribing to data changes of RawKV [#48](https://github.com/tikv/migration/issues/48) @[zeminzhou](https://github.com/zeminzhou) @[haojinming](https://github.com/haojinming) @[pingyu](https://github.com/pingyu)

    TiKV-CDC is a CDC (Change Data Capture) tool for TiKV clusters. TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. TiKV-CDC supports subscribing to data changes of RawKV and replicating them to a downstream TiKV cluster in real time, thus enabling cross-cluster replication of RawKV.

    For more information, see [documentation](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc/).

* TiCDC supports scaling out a single table on Kafka changefeeds and distributing the changefeed to multiple TiCDC nodes (experimental) [#7720](https://github.com/pingcap/tiflow/issues/7720) @[overvenus](https://github.com/overvenus)

    Before v6.6.0, when a table in the upstream accepts a large amount of writes, the replication capability of this table cannot be scaled out, resulting in an increase in the replication latency. Starting from TiCDC v6.6.0. the changefeed of an upstream table can be distributed to multiple TiCDC nodes in a Kafka sink, which means the replication capability of a single table is scaled out.

    For more information, see [documentation](/ticdc/ticdc-sink-to-kafka.md#scale-out-the-load-of-a-single-large-table-to-multiple-ticdc-nodes).

* [GORM](https://github.com/go-gorm/gorm) adds TiDB integration tests. Now TiDB is the default database supported by GORM. [#6014](https://github.com/go-gorm/gorm/pull/6014) @[Icemap](https://github.com/Icemap)

    - In v1.4.6, [GORM MySQL driver](https://github.com/go-gorm/mysql) adapts to the `AUTO_RANDOM` attribute of TiDB [#104](https://github.com/go-gorm/mysql/pull/104)
    - In v1.4.6, [GORM MySQL driver](https://github.com/go-gorm/mysql) fixes the issue that when connecting to TiDB, the `Unique` attribute of the `Unique` field cannot be modified during `AutoMigrate` [#105](https://github.com/go-gorm/mysql/pull/105)
    - [GORM documentation](https://github.com/go-gorm/gorm.io) mentions TiDB as the default database [#638](https://github.com/go-gorm/gorm.io/pull/638)

    For more information, see [GORM documentation](https://gorm.io/docs/index.html).

### Observability

* Support quickly creating SQL binding on TiDB Dashboard [#781](https://github.com/pingcap/tidb-dashboard/issues/781) @[YiniXu9506](https://github.com/YiniXu9506)

    TiDB v6.6.0 supports creating SQL binding from statement history, which allows you to quickly bind a SQL statement to a specific plan on TiDB Dashboard.

    By providing a user-friendly interface, this feature simplifies the process of binding plans in TiDB, reduces the operation complexity, and improves the efficiency and user experience of the plan binding process.

    For more information, see [documentation](/dashboard/dashboard-statement-details.md#fast-plan-binding).

* Add warning for caching execution plans @[qw4990](https://github.com/qw4990)

    When an execution plan cannot be cached, TiDB indicates the reason in warning to make diagnostics easier. For example:

    ```sql
    mysql> PREPARE st FROM 'SELECT * FROM t WHERE a<?';
    Query OK, 0 rows affected (0.00 sec)

    mysql> SET @a='1';
    Query OK, 0 rows affected (0.00 sec)

    mysql> EXECUTE st USING @a;
    Empty set, 1 warning (0.01 sec)

    mysql> SHOW WARNINGS;
    +---------+------+----------------------------------------------+
    | Level   | Code | Message                                      |
    +---------+------+----------------------------------------------+
    | Warning | 1105 | skip plan-cache: '1' may be converted to INT |
    +---------+------+----------------------------------------------+
    ```

    In the preceding example, the optimizer converts a non-INT type to an INT type, and the execution plan might change with the change of the parameter, so TiDB does not cache the plan.

    For more information, see [documentation](/sql-prepared-plan-cache.md#diagnostics-of-prepared-plan-cache).

* Add a `Warnings` field to the slow query log [#39893](https://github.com/pingcap/tidb/issues/39893) @[time-and-fate](https://github.com/time-and-fate)

    TiDB v6.6.0 adds a `Warnings` field to the slow query log to help diagnose performance issues. This field records warnings generated during the execution of a slow query. You can also view the warnings on the slow query page of TiDB Dashboard.

    For more information, see [documentation](/identify-slow-queries.md).

* Automatically capture the generation of SQL execution plans [#38779](https://github.com/pingcap/tidb/issues/38779) @[Yisaer](https://github.com/Yisaer)

    In the process of troubleshooting execution plan issues, `PLAN REPLAYER` can help preserve the scene and improve the efficiency of diagnosis. However, in some scenarios, the generation of some execution plans cannot be reproduced freely, which makes the diagnosis work more difficult.

    To address such issues, in TiDB v6.6.0, `PLAN REPLAYER` extends the capability of automatic capture. With the `PLAN REPLAYER CAPTURE` command, you can register the target SQL statement in advance and also specify the target execution plan at the same time. When TiDB detects the SQL statement or the execution plan that matches the registered target, it automatically generates and packages the `PLAN REPLAYER` information. When the execution plan is unstable, this feature can improve diagnostic efficiency.

    To use this feature, set the value of [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) to `ON`.

    For more information, see [documentation](/sql-plan-replayer.md#use-plan-replayer-capture).

* Support persisting statements summary (experimental) [#40812](https://github.com/pingcap/tidb/issues/40812) @[mornyx](https://github.com/mornyx)

    Before v6.6.0, statements summary data is kept in memory and would be lost upon a TiDB server restart. Starting from v6.6.0, TiDB supports enabling statements summary persistence, which allows historical data to be written to disks on a regular basis. In the meantime, the result of queries on system tables will derive from disks, instead of memory. After TiDB restarts, all historical data remains available.

    For more information, see [documentation](/statement-summary-tables.md#persist-statements-summary).

### Security

* TiFlash supports automatic rotations of TLS certificates [#5503](https://github.com/pingcap/tiflash/issues/5503) @[ywqzzy](https://github.com/ywqzzy)

    In v6.6.0, TiDB supports automatic rotations of TiFlash TLS certificates. For a TiDB cluster with encrypted data transmission between components enabled, when a TLS certificate of TiFlash expires and needs to be reissued with a new one, the new TiFlash TLS certificate can be automatically loaded without restarting the TiDB cluster. In addition, the rotation of a TLS certificate between components within a TiDB cluster does not affect the use of the TiDB cluster, which ensures high availability of the cluster.

    For more information, see [documentation](/enable-tls-between-components.md).

* TiDB Lightning supports accessing Amazon S3 data via AWS IAM role keys and session tokens [#4075](https://github.com/pingcap/tidb/issues/40750) @[okJiang](https://github.com/okJiang)

    Before v6.6.0, TiDB Lightning only supports accessing S3 data via AWS IAM **user's access keys** (each access key consists of an access key ID and a secret access key) so you cannot use a temporary session token to access S3 data. Starting from v6.6.0, TiDB Lightning supports accessing S3 data via AWS IAM **role's access keys + session tokens** as well to improve the data security.

    For more information, see [documentation](/tidb-lightning/tidb-lightning-data-source.md#import-data-from-amazon-s3).

### Telemetry

- Starting from February 20, 2023, the [telemetry feature](/telemetry.md) is disabled by default in new versions of TiDB and TiDB Dashboard (including v6.6.0). If you upgrade from a previous version that uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. For the specific versions, see [TiDB Release Timeline](/releases/release-timeline.md).
- Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP. If you upgrade from a previous version of TiUP to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v6.5.0 to the current version (v6.6.0). If you are upgrading from v6.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

* Support MySQL-compatible foreign key constraints [#18209](https://github.com/pingcap/tidb/issues/18209) @[crazycs520](https://github.com/crazycs520)

    For more information, see the [SQL](#sql) section in this document and [documentation](/foreign-key.md).

* Support the MySQL-compatible multi-valued index (experimental) [#39592](https://github.com/pingcap/tidb/issues/39592) @[xiongjiwei](https://github.com/xiongjiwei) @[qw4990](https://github.com/qw4990)

    For more information, see the [SQL](#sql) section in this document and [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-index).

### System variables

| Variable name  | Change type    | Description |
|--------|------------------------------|------|
| `tidb_enable_amend_pessimistic_txn` | Deleted | Starting from v6.5.0, this variable is deprecated. Starting from v6.6.0, this variable and the `AMEND TRANSACTION` feature are deleted. TiDB will use [meta lock](/metadata-lock.md) to avoid the `Information schema is changed` error. |
| `tidb_enable_concurrent_ddl` | Deleted | This variable controls whether to allow TiDB to use concurrent DDL statements. When this variable is disabled, TiDB uses the old DDL execution framework, which provides limited support for concurrent DDL execution. Starting from v6.6.0, this variable is deleted and TiDB no longer supports the old DDL execution framework. |
| `tidb_ttl_job_run_interval` | Deleted | This variable is used to control the scheduling interval of TTL jobs in the background. Starting from v6.6.0, this variable is deleted, because TiDB provides the `TTL_JOB_INTERVAL` attribute for every table to control the TTL runtime, which is more flexible than `tidb_ttl_job_run_interval`. |
| [`foreign_key_checks`](/system-variables.md#foreign_key_checks) | Modified | This variable controls whether to enable the foreign key constraint check. The default value changes from `OFF` to `ON`, which means enabling the foreign key check by default. |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630) | Modified | This variable controls whether to enable the foreign key feature. The default value changes from `OFF` to `ON`, which means enabling foreign key by default. |
| `tidb_enable_general_plan_cache` | Modified | This variable controls whether to enable General Plan Cache. Starting from v6.6.0, this variable is renamed to [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache). |
| [`tidb_enable_historical_stats`](/system-variables.md#tidb_enable_historical_stats) | Modified | This variable controls whether to enable historical statistics. The default value changes from `OFF` to `ON`, which means that historical statistics are enabled by default. |
| [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) | Modified | The default value changes from `ON` to `OFF`, which means that telemetry is disabled by default in TiDB. |
| `tidb_general_plan_cache_size` | Modified | This variable controls the maximum number of execution plans that can be cached by General Plan Cache. Starting from v6.6.0, this variable is renamed to [`tidb_non_prepared_plan_cache_size`](/system-variables.md#tidb_non_prepared_plan_cache_size). |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) | Modified | A new value option `learner` is added for this variable to specify the learner replicas with which TiDB reads data from read-only nodes. |
| [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) | Modified | A new value option `prefer-leader` is added for this variable to improve the overall read availability of TiDB clusters. When this option is set, TiDB prefers to read from the leader replica. When the performance of the leader replica significantly decreases, TiDB automatically reads from follower replicas. |
| [`tidb_store_batch_size`](/system-variables.md#tidb_store_batch_size) | Modified | This variable controls the batch size of the Coprocessor Tasks of the `IndexLookUp` operator. `0` means to disable batch. Starting from v6.6.0, the default value is changed from `0` to `4`, which means 4 Coprocessor tasks will be batched into one task for each batch of requests. |
| [`mpp_exchange_compression_mode`](/system-variables.md#mpp_exchange_compression_mode-new-in-v660)  | Newly added |  This variable specifies the data compression mode of the MPP Exchange operator. It takes effect when TiDB selects the MPP execution plan with the version number `1`. The default value `UNSPECIFIED` means that TiDB automatically selects the `FAST` compression mode. |
| [`mpp_version`](/system-variables.md#mpp_version-new-in-v660)  | Newly added |  This variable specifies the version of the MPP execution plan. After a version is specified, TiDB selects the specified version of the MPP execution plan. The default value `UNSPECIFIED` means that TiDB automatically selects the latest version `1`. |
| [`tidb_ddl_distribute_reorg`](/system-variables.md#tidb_ddl_distribute_reorg-new-in-v660) | Newly added | This variable controls whether to enable distributed execution of the DDL reorg phase to accelerate this phase. The default value `OFF` means not to enable distributed execution of the DDL reorg phase by default. Currently, this variable takes effect only for `ADD INDEX`. |
| [`tidb_enable_historical_stats_for_capture`](/system-variables.md#tidb_enable_historical_stats_for_capture) | Newly added | This variable controls whether the information captured by `PLAN REPLAYER CAPTURE` includes historical statistics by default. The default value `OFF` means that historical statistics are not included by default. |
| [`tidb_enable_plan_cache_for_param_limit`](/system-variables.md#tidb_enable_plan_cache_for_param_limit-new-in-v660) | Newly added | This variable controls whether Prepared Plan Cache caches execution plans that contain `COUNT` after `Limit`. The default value is `ON`, which means Prepared Plan Cache supports caching such execution plans. Note that Prepared Plan Cache does not support caching execution plans with a `COUNT` condition that counts a number greater than 10000. |
| [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) | Newly added | This variable controls whether to enable the [`PLAN REPLAYER CAPTURE` feature](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans). The default value `OFF` means to disable the `PLAN REPLAYER CAPTURE` feature. |
| [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) | Newly added  | This variable controls whether to enable the resource control feature. The default value is `OFF`. When this variable is set to `ON`, the TiDB cluster supports resource isolation of applications based on resource groups. |
| [`tidb_historical_stats_duration`](/system-variables.md#tidb_historical_stats_duration-new-in-v660) | Newly added | This variable controls how long the historical statistics are retained in storage. The default value is 7 days. |
| [`tidb_index_join_double_read_penalty_cost_rate`](/system-variables.md#tidb_index_join_double_read_penalty_cost_rate-new-in-v660) | Newly added | This variable controls whether to add some penalty cost to the selection of index join. The default value `0` means that this feature is disabled by default. |
| [`tidb_pessimistic_txn_aggressive_locking`](/system-variables.md#tidb_pessimistic_txn_aggressive_locking-new-in-v660) | Newly added | This variable controls whether to use enhanced pessimistic locking wake-up model for pessimistic transactions. The default value `OFF` means not to use such a wake-up model for pessimistic transactions by default. |
| [`tidb_stmt_summary_enable_persistent`](/system-variables.md#tidb_stmt_summary_enable_persistent-new-in-v660) | Newly added | This variable is read-only. It controls whether to enable [statements summary persistence](/statement-summary-tables.md#persist-statements-summary). The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660). |
| [`tidb_stmt_summary_filename`](/system-variables.md#tidb_stmt_summary_filename-new-in-v660) | Newly added | This variable is read-only. It specifies the file to which persistent data is written when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled. The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660). |
| [`tidb_stmt_summary_file_max_backups`](/system-variables.md#tidb_stmt_summary_file_max_backups-new-in-v660) | Newly added | This variable is read-only. It specifies the maximum number of data files that can be persisted when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled. The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660). |
| [`tidb_stmt_summary_file_max_days`](/system-variables.md#tidb_stmt_summary_file_max_days-new-in-v660) | Newly added | This variable is read-only. It specifies the maximum number of days to keep persistent data files when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled. The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660). |
| [`tidb_stmt_summary_file_max_size`](/system-variables.md#tidb_stmt_summary_file_max_size-new-in-v660) | Newly added | This variable is read-only. It specifies the maximum size of a persistent data file when [statements summary persistence](/statement-summary-tables.md#persist-statements-summary) is enabled. The value of this variable is the same as that of the configuration item [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660). |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV  | `enable-statistics` | Deleted | This configuration item specifies whether to enable RocksDB statistics. Starting from v6.6.0, this item is deleted. RocksDB statistics are enabled for all clusters by default to help diagnostics. For details, see [#13942](https://github.com/tikv/tikv/pull/13942). |
| TiKV | `storage.block-cache.shared` | Deleted | Starting from v6.6.0, this configuration item is deleted, and the block cache is enabled by default and cannot be disabled. For details, see [#12936](https://github.com/tikv/tikv/issues/12936). |
| DM | `on-duplicate` |  Deleted | This configuration item controls the methods to resolve conflicts during the full import phase. In v6.6.0, new configuration items `on-duplicate-logical` and `on-duplicate-physical` are introduced to replace `on-duplicate`. |
| TiDB | [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) | Modified | Starting from v6.6.0, the default value changes from `true` to `false`, which means that telemetry is disabled by default in TiDB. |
| TiKV  | [`rocksdb.defaultcf.block-size`](/tikv-configuration-file.md#block-size) and [`rocksdb.writecf.block-size`](/tikv-configuration-file.md#block-size)  |  Modified  |   The default values change from `64K` to `32K`.  |
| TiKV | [`rocksdb.defaultcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size), [`rocksdb.writecf.block-cache-size`](/tikv-configuration-file.md#block-cache-size), [`rocksdb.lockcf.block-cache-size`](/tikv-configuration-file.md#block-cache-size) | Deprecated | Starting from v6.6.0, these configuration items are deprecated. For details, see [#12936](https://github.com/tikv/tikv/issues/12936). |
| PD | [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) | Modified | Starting from v6.6.0, the default value changes from `true` to `false`, which means that telemetry is disabled by default in TiDB Dashboard. |
| DM | [`import-mode`](/dm/task-configuration-file-full.md) |  Modified | The possible values of this configuration item are changed from `"sql"` and `"loader"` to `"logical"` and `"physical"`. The default value is `"logical"`, which means using TiDB Lightning's logical import mode to import data. |
| TiFlash |  [`profile.default.max_memory_usage_for_all_queries`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)  |  Modified  |  Specifies the memory usage limit for the generated intermediate data in all queries. Starting from v6.6.0, the default value changes from `0` to `0.8`, which means the limit is 80% of the total memory. |
| TiCDC  | [`consistent.storage`](/ticdc/ticdc-sink-to-mysql.md#prerequisites)  |  Modified  | This configuration item specifies the path under which redo log backup is stored. Two more value options are added for `scheme`, GCS, and Azure. |
| TiDB | [`initialize-sql-file`](/tidb-configuration-file.md#initialize-sql-file-new-in-v660) | Newly added | This configuration item specifies the SQL script to be executed when the TiDB cluster is started for the first time. The default value is empty. |
| TiDB | [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660) | Newly added | This configuration item controls whether to enable statements summary persistence. The default value is `false`, which means this feature is not enabled by default. |
| TiDB | [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum number of data files that can be persisted. `0` means no limit on the number of files. |
| TiDB | [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum number of days to keep persistent data files. |
| TiDB | [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the maximum size of a persistent data file (in MiB). |
| TiDB | [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660) | Newly added | When statements summary persistence is enabled, this configuration specifies the file to which persistent data is written. |
| TiKV | [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) | Newly added | Whether to enable scheduling for user foreground read/write requests according to the Request Unit (RU) of the corresponding resource groups. The default value is `false`, which means to disable scheduling according to the RU of the corresponding resource groups. |
| TiKV | [`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660) | Newly added | This configuration item specifies the type of the storage engine. Value options are `"raft-kv"` and `"partitioned-raft-kv"`. This configuration item can only be specified when creating a cluster and cannot be modified once being specified. |
| TiKV | [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660) | Newly added | This configuration item specifies the flush strategy used when the memory usage of `memtable` of the current RocksDB reaches the threshold.  |
| TiKV | [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660) | Newly added | This configuration item specifies the limit on total memory used by `memtable` of all RocksDB instances in a single TiKV. The default value is 25% of the total machine memory.  |
| PD  | [`pd-server.enable-gogc-tuner`](/pd-configuration-file.md#enable-gogc-tuner-new-in-v660) | Newly added | This configuration item controls whether to enable the GOGC tuner, which is disabled by default. |
| PD  | [`pd-server.gc-tuner-threshold`](/pd-configuration-file.md#gc-tuner-threshold-new-in-v660) | Newly added | This configuration item specifies the maximum memory threshold ratio for tuning GOGC. The default value is `0.6`. |
| PD  | [`pd-server.server-memory-limit-gc-trigger`](/pd-configuration-file.md#server-memory-limit-gc-trigger-new-in-v660) | Newly added | This configuration item specifies the threshold ratio at which PD tries to trigger GC. The default value is `0.7`. |
| PD  | [`pd-server.server-memory-limit`](/pd-configuration-file.md#server-memory-limit-new-in-v660) | Newly added | This configuration item specifies the memory limit ratio for a PD instance. The value `0` means no memory limit. |
| TiCDC | [`scheduler.region-per-span`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | This configuration item controls whether to split a table into multiple replication ranges based on the number of Regions, and these ranges can be replicated by multiple TiCDC nodes. The default value is `50000`. |
| TiDB Lightning | [`compress-kv-pairs`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | This configuration item controls whether to enable compression when sending KV pairs to TiKV in the physical import mode. The default value is empty, meaning that the compression is not enabled. |
| DM | [`checksum-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls whether DM performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after the import. The default value is `"required"`, which performs admin checksum after the import. If checksum fails, DM pauses the task and you need to manually handle the failure. |
| DM | [`disk-quota-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item sets the disk quota. It corresponds to the [`disk-quota` configuration](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) of TiDB Lightning. |
| DM | [`on-duplicate-logical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls how DM resolves conflicting data in the logical import mode. The default value is `"replace"`, which means using the new data to replace the existing data. |
| DM | [`on-duplicate-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item controls how DM resolves conflicting data in the physical import mode. The default value is `"none"`, which means not resolving conflicting data. `"none"` has the best performance, but might lead to inconsistent data in the downstream database. |
| DM | [`sorting-dir-physical`](/dm/task-configuration-file-full.md) | Newly added | This configuration item specifies the directory used for local KV sorting in the physical import mode. The default value is the same as the `dir` configuration. |
| sync-diff-inspector | [`skip-non-existing-table`](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description) | Newly added | This configuration item controls whether to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream.  |
| TiSpark | [`spark.tispark.replica_read`](/tispark-overview.md#tispark-configurations) | Newly added | This configuration item controls the type of replicas to be read. The value options are `leader`, `follower`, and `learner`. |
| TiSpark | [`spark.tispark.replica_read.label`](/tispark-overview.md#tispark-configurations) | Newly added | This configuration item is used to set labels for the target TiKV node. |

### Others

- Support dynamically modifying [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530). This facilitates more flexible TiKV performance tuning.
- Remove the limit on `LIMIT` clauses, thus improving the execution performance.
- Starting from v6.6.0, BR does not support restoring data to clusters earlier than v6.1.0.
- Starting from v6.6.0, TiDB no longer supports modifying column types on partitioned tables because of potential correctness issues.

## Improvements

+ TiDB

    - Improve the scheduling mechanism of TTL background cleaning tasks to allow the cleaning task of a single table to be split into several sub-tasks and scheduled to run on multiple TiDB nodes simultaneously [#40361](https://github.com/pingcap/tidb/issues/40361) @[YangKeao](https://github.com/YangKeao)
    - Optimize the column name display of the result returned by running multi-statements after setting a non-default delimiter [#39662](https://github.com/pingcap/tidb/issues/39662) @[mjonss](https://github.com/mjonss)
    - Optimize the execution efficiency of statements after warning messages are generated [#39702](https://github.com/pingcap/tidb/issues/39702) @[tiancaiamao](https://github.com/tiancaiamao)
    - Support distributed data backfill for `ADD INDEX` (experimental) [#37119](https://github.com/pingcap/tidb/issues/37119) @[zimulala](https://github.com/zimulala)
    - Support using `CURDATE()` as the default value of a column [#38356](https://github.com/pingcap/tidb/issues/38356) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - `partial order prop push down` now supports the LIST-type partitioned tables [#40273](https://github.com/pingcap/tidb/issues/40273) @[winoros](https://github.com/winoros)
    - Add error messages for conflicts between optimizer hints and execution plan bindings [#40910](https://github.com/pingcap/tidb/issues/40910) @[Reminiscent](https://github.com/Reminiscent)
    - Optimize the plan cache strategy to avoid non-optimal plans when using plan cache in some scenarios [#40312](https://github.com/pingcap/tidb/pull/40312) [#40218](https://github.com/pingcap/tidb/pull/40218) [#40280](https://github.com/pingcap/tidb/pull/40280) [#41136](https://github.com/pingcap/tidb/pull/41136) [#40686](https://github.com/pingcap/tidb/pull/40686) @[qw4990](https://github.com/qw4990)
    - Clear expired region cache regularly to avoid memory leak and performance degradation [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - `MODIFY COLUMN` is not supported on partitioned tables [#39915](https://github.com/pingcap/tidb/issues/39915) @[wjhuang2016](https://github.com/wjhuang2016)
    - Disable renaming of columns that partition tables depend on [#40150](https://github.com/pingcap/tidb/issues/40150) @[mjonss](https://github.com/mjonss)
    - Refine the error message reported when a column that a partitioned table depends on is deleted [#38739](https://github.com/pingcap/tidb/issues/38739) @[jiyfhust](https://github.com/jiyfhust)
    - Add a mechanism that `FLASHBACK CLUSTER` retries when it fails to check the `min-resolved-ts` [#39836](https://github.com/pingcap/tidb/issues/39836) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - Optimize the default values of some parameters in partitioned-raft-kv mode: the default value of the TiKV configuration item `storage.block-cache.capacity` is adjusted from 45% to 30%, and the default value of `region-split-size` is adjusted from `96MiB` adjusted to `10GiB`. When using raft-kv mode and `enable-region-bucket` is `true`, `region-split-size` is adjusted to 1 GiB by default. [#12842](https://github.com/tikv/tikv/issues/12842) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Support priority scheduling in Raftstore asynchronous writes [#13730](https://github.com/tikv/tikv/issues/13730) @[Connor1996](https://github.com/Connor1996)
    - Support starting TiKV on a CPU with less than 1 core [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - Optimize the new detection mechanism of Raftstore slow score and add `evict-slow-trend-scheduler` [#14131](https://github.com/tikv/tikv/issues/14131) @[innerr](https://github.com/innerr)
    - Force the block cache of RocksDB to be shared and no longer support setting the block cache separately according to CF [#12936](https://github.com/tikv/tikv/issues/12936) @[busyjay](https://github.com/busyjay)

+ PD

    - Support managing the global memory threshold to alleviate the OOM problem (experimental) [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    - Add the GC Tuner to alleviate the GC pressure (experimental) [#5827](https://github.com/tikv/pd/issues/5827) @[hnes](https://github.com/hnes)
    - Add the `evict-slow-trend-scheduler` scheduler to detect and schedule abnormal nodes [#5808](https://github.com/tikv/pd/pull/5808) @[innerr](https://github.com/innerr)
    - Add the keyspace manager to manage keyspace [#5293](https://github.com/tikv/pd/issues/5293) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)

+ TiFlash

    - Support an independent MVCC bitmap filter that decouples the MVCC filtering operations in the TiFlash data scanning process, which provides the foundation for future optimization of the data scanning process [#6296](https://github.com/pingcap/tiflash/issues/6296) @[JinheLin](https://github.com/JinheLin)
    - Reduce the memory usage of TiFlash by up to 30% when there is no query [#6589](https://github.com/pingcap/tiflash/pull/6589) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Optimize the concurrency of downloading log backup files on the TiKV side to improve the performance of PITR recovery in regular scenarios [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Support batch `UPDATE` DML statements to improve TiCDC replication performance [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        - Implement MQ sink and MySQL sink in the asynchronous mode to improve the sink throughput [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - Optimize DM alert rules and content [#7376](https://github.com/pingcap/tiflow/issues/7376) @[D3Hunter](https://github.com/D3Hunter)

             Previously, alerts similar to "DM_XXX_process_exits_with_error" were raised whenever a related error occurred. But some alerts are caused by idle database connections, which can be recovered after reconnecting. To reduce these kinds of alerts, DM divides errors into two types: automatically recoverable errors and unrecoverable errors:

            - For an error that is automatically recoverable, DM reports the alert only if the error occurs more than 3 times within 2 minutes.
            - For an error that is not automatically recoverable, DM maintains the original behavior and reports the alert immediately.

        - Optimize relay performance by adding the async/batch relay writer [#4287](https://github.com/pingcap/tiflow/issues/4287) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Physical Import Mode supports keyspace [#40531](https://github.com/pingcap/tidb/issues/40531) @[iosmanthus](https://github.com/iosmanthus)
        - Support setting the maximum number of conflicts by `lightning.max-error` [#40743](https://github.com/pingcap/tidb/issues/40743) @[dsdashun](https://github.com/dsdashun)
        - Support importing CSV data files with BOM headers [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)
        - Optimize the processing logic when encountering TiKV flow-limiting errors and try other available regions instead [#40205](https://github.com/pingcap/tidb/issues/40205) @[lance6716](https://github.com/lance6716)
        - Disable checking the table foreign keys during import [#40027](https://github.com/pingcap/tidb/issues/40027) @[gozssky](https://github.com/gozssky)

    + Dumpling

        - Support exporting settings for foreign keys [#39913](https://github.com/pingcap/tidb/issues/39913) @[lichunzhu](https://github.com/lichunzhu)

    + sync-diff-inspector

        - Add a new parameter `skip-non-existing-table` to control whether to skip checking upstream and downstream data consistency when tables in the downstream do not exist in the upstream [#692](https://github.com/pingcap/tidb-tools/issues/692) @[lichunzhu](https://github.com/lichunzhu) @[liumengya94](https://github.com/liumengya94)

## Bug fixes

+ TiDB

    - Fix the issue that a statistics collection task fails due to an incorrect `datetime` value [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that `stats_meta` is not created following table creation [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix frequent write conflicts in transactions when performing DDL data backfill [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    - Fix the issue that sometimes an index cannot be created for an empty table using ingest mode [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `wait_ts` in the slow query log is the same for different SQL statements within the same transaction [#39713](https://github.com/pingcap/tidb/issues/39713) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - Fix the issue that the `Assertion Failed` error is reported when adding a column during the process of deleting a row record [#39570](https://github.com/pingcap/tidb/issues/39570) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the `not a DDL owner` error is reported when modifying a column type [#39643](https://github.com/pingcap/tidb/issues/39643) @[zimulala](https://github.com/zimulala)
    - Fix the issue that no error is reported when inserting a row after exhaustion of the auto-increment values of the `AUTO_INCREMENT` column [#38950](https://github.com/pingcap/tidb/issues/38950) @[Dousir9](https://github.com/Dousir9)
    - Fix the issue that the `Unknown column` error is reported when creating an expression index [#39784](https://github.com/pingcap/tidb/issues/39784) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that data cannot be inserted into a renamed table when the generated expression includes the name of this table [#39826](https://github.com/pingcap/tidb/issues/39826) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the `INSERT ignore` statement cannot fill in default values when the column is write-only [#40192](https://github.com/pingcap/tidb/issues/40192) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that resources are not released when disabling the resource management module [#40546](https://github.com/pingcap/tidb/issues/40546) @[zimulala](https://github.com/zimulala)
    - Fix the issue that TTL tasks cannot trigger statistics updates in time [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that unexpected data is read because TiDB improperly handles `NULL` values when constructing key ranges [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that illegal values are written to a table when the `MODIFT COLUMN` statement also changes the default value of a column [#40164](https://github.com/pingcap/tidb/issues/40164) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the adding index operation is inefficient due to invalid Region cache when there are many Regions in a table [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - Fix data race occurred in allocating auto-increment IDs [#40584](https://github.com/pingcap/tidb/issues/40584) @[Dousir9](https://github.com/Dousir9)
    - Fix the issue that the implementation of the not operator in JSON is incompatible with the implementation in MySQL [#40683](https://github.com/pingcap/tidb/issues/40683) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that concurrent view might cause DDL operations to be blocked [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - Fix data inconsistency caused by concurrently executing DDL statements to modify columns of partitioned tables [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss) @[mjonss](https://github.com/mjonss)
    - Fix the issue that "Malformed packet" is reported when using `caching_sha2_password` for authentication without specifying a password [#40831](https://github.com/pingcap/tidb/issues/40831) @[dveeden](https://github.com/dveeden)
    - Fix the issue that a TTL task fails if the primary key of the table contains an `ENUM` column [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that some DDL operations blocked by MDL cannot be queried in `mysql.tidb_mdl_view` [#40838](https://github.com/pingcap/tidb/issues/40838) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that data race might occur during DDL ingestion [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TTL tasks might delete some data incorrectly after the time zone changes [#41043](https://github.com/pingcap/tidb/issues/41043) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that `JSON_OBJECT` might report an error in some cases [#39806](https://github.com/pingcap/tidb/issues/39806) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TiDB might deadlock during initialization [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that the value of system variables might be incorrectly modified in some cases due to memory reuse [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that data might be inconsistent with the index when a unique index is created in the ingest mode [#40464](https://github.com/pingcap/tidb/issues/40464) @[tangenta](https://github.com/tangenta)
    - Fix the issue that some truncate operations cannot be blocked by MDL when truncating the same table concurrently [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the `SHOW PRIVILEGES` statement returns an incomplete privilege list [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that TiDB panics when adding a unique index [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - Fix the issue that executing the `ADMIN RECOVER` statement might cause the index data to be corrupted [#40430](https://github.com/pingcap/tidb/issues/40430) @[xiongjiwei](https://github.com/xiongjiwei)
    - Fix the issue that a query might fail when the queried table contains a `CAST` expression in the expression index [#40130](https://github.com/pingcap/tidb/issues/40130) @[xiongjiwei](https://github.com/xiongjiwei)
    - Fix the issue that a unique index might still produce duplicate data in some cases [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    - Fix the PD OOM issue when there is a large number of Regions but the table ID cannot be pushed down when querying some virtual tables using `Prepare` or `Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - Fix the issue that data race might occur when an index is added [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - Fix the `can't find proper physical plan` issue caused by virtual columns [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that TiDB cannot restart after global bindings are created for partition tables in dynamic trimming mode [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - Fix the issue that `auto analyze` causes graceful shutdown to take a long time [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the panic of the TiDB server when the IndexMerge operator triggers memory limiting behaviors [#41036](https://github.com/pingcap/tidb/pull/41036) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the `SELECT * FROM table_name LIMIT 1` query on partitioned tables is slow [#40741](https://github.com/pingcap/tidb/pull/40741) @[solotzg](https://github.com/solotzg)

+ TiKV

    - Fix an error that occurs when casting the `const Enum` type to other types [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that Resolved TS causes higher network traffic [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - Fix the issue that the Region Scatter task generates redundant replicas unexpectedly [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - Fix the issue that the Online Unsafe Recovery feature would get stuck and time out in `auto-detect` mode [#5753](https://github.com/tikv/pd/issues/5753) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the execution `replace-down-peer` slows down under certain conditions [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - Fix the PD OOM issue that occurs when the calls of `ReportMinResolvedTS` are too frequent [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)

+ TiFlash

    - Fix the issue that querying TiFlash-related system tables might get stuck [#6745](https://github.com/pingcap/tiflash/pull/6745) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that semi-joins use excessive memory when calculating Cartesian products [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the result of the division operation on the DECIMAL data type is not rounded [#6393](https://github.com/pingcap/tiflash/issues/6393) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that when restoring log backup, hot Regions cause the restore to fail [#37207](https://github.com/pingcap/tidb/issues/37207) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that restoring data to a cluster on which the log backup is running causes the log backup file to be unrecoverable [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the PITR feature does not support CA-bundles [#38775](https://github.com/pingcap/tidb/issues/38775) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the panic issue caused by duplicate temporary tables during recovery [#40797](https://github.com/pingcap/tidb/issues/40797) @[joccau](https://github.com/joccau)
        - Fix the issue that PITR does not support configuration changes for PD clusters [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the connection failure between PD and tidb-server causes PITR backup progress not to advance [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiKV cannot listen to PITR tasks due to the connection failure between PD and TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - Fix the issue that when a PITR backup task is deleted, the residual backup data causes data inconsistency in new tasks [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)

    + TiCDC

        - Fix the issue that `transaction_atomicity` and `protocol` cannot be updated via the configuration file [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that precheck is not performed on the storage path of redo log [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue of insufficient duration that redo log can tolerate for S3 storage failure [#8089](https://github.com/pingcap/tiflow/issues/8089)  @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that changefeed might get stuck in special scenarios such as when scaling in or scaling out TiKV or TiCDC nodes [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - Fix the issue of too high traffic among TiKV nodes [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
        - Fix the performance issues of TiCDC in terms of CPU usage, memory control, and throughput when the pull-based sink is enabled [#8142](https://github.com/pingcap/tiflow/issues/8142) [#8157](https://github.com/pingcap/tiflow/issues/8157) [#8001](https://github.com/pingcap/tiflow/issues/8001) [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Data Migration (DM)

        - Fix the issue that the `binlog-schema delete` command fails to execute [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that the checkpoint does not advance when the last binlog is a skipped DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - Fix a bug that when the expression filters of both "update" and "non-update" types are specified in one table, all `UPDATE` statements are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)
        - Fix a bug that when only one of `update-old-value-expr` or `update-new-value-expr` is set for a table, the filter rule does not take effect or DM panics [#7774](https://github.com/pingcap/tiflow/issues/7774) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning timeout hangs due to TiDB restart in some scenarios [#33714](https://github.com/pingcap/tidb/issues/33714) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Lightning might incorrectly skip conflict resolution when all but the last TiDB Lightning instance encounters a local duplicate record during a parallel import [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that precheck cannot accurately detect the presence of a running TiCDC in the target cluster [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning panics in the split-region phase [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - Fix the issue that the conflict resolution logic (`duplicate-resolution`) might lead to inconsistent checksums [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - Fix a possible OOM problem when there is an unclosed delimiter in the data file [#40400](https://github.com/pingcap/tidb/issues/40400) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Fix the issue that the file offset in the error report exceeds the file size [#40034](https://github.com/pingcap/tidb/issues/40034) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Fix an issue with the new version of PDClient that might cause parallel import to fail [#40493](https://github.com/pingcap/tidb/issues/40493) @[AmoebaProtozoa](https://github.com/AmoebaProtozoa)
        - Fix the issue that TiDB Lightning prechecks cannot find dirty data left by previously failed imports [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [morgo](https://github.com/morgo)
- [jiyfhust](https://github.com/jiyfhust)
- [b41sh](https://github.com/b41sh)
- [sourcelliu](https://github.com/sourcelliu)
- [songzhibin97](https://github.com/songzhibin97)
- [mamil](https://github.com/mamil)
- [Dousir9](https://github.com/Dousir9)
- [hihihuhu](https://github.com/hihihuhu)
- [mychoxin](https://github.com/mychoxin)
- [xuning97](https://github.com/xuning97)
- [andreid-db](https://github.com/andreid-db)
