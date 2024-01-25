---
title: TiDB 7.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.6.0.
---

# TiDB 7.6.0 Release Notes

Release date: January 25, 2024

TiDB version: 7.6.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.6.0#version-list)

7.6.0 introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">Scalability and Performance</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#cross-database-binding">Cross-database SQL binding</a></td>
    <td>When managing hundreds of databases with the same schema, it is often necessary to apply SQL bindings across these databases. For example, in SaaS or PaaS data platforms, each user typically operates separate databases with the same schema and runs similar SQL queries on them. In this case, it is impractical to bind SQL for each database one by one. TiDB v7.6.0 introduces cross-database SQL bindings that enable matching bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">Achieve up to 10 times faster for snapshot restore (experimental)</a></td>
    <td>BR v7.6.0 introduces an experimental coarse-grained Region scatter algorithm to accelerate snapshot restores for clusters. In clusters with many TiKV nodes, this algorithm significantly improves cluster resource efficiency by more evenly distributing load across nodes and better utilizing per-node network bandwidth. In several real-world cases, this improvement accelerates restore process by about up to 10 times.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/ddl-v2">Achieve up to 10 times faster for creating tables in batch (experimental)</a></td>
    <td>With the implementation of the new DDL architecture in v7.6.0, the performance of batch table creation has witnessed a remarkable improvement, up to 10 times faster. This substantial enhancement drastically reduces the time needed for creating numerous tables. This acceleration is particularly noteworthy in SaaS scenarios, where the prevalence of high volumes of tables, ranging from tens to hundreds of thousands, is a common challenge.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use Active PD Followers to enhance PD's Region information query service (experimental)</a></td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle <code>GetRegion</code> and <code>ScanRegions</code> requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on the PD leader.</td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability</td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy-overview">Support TiProxy (experimental)</a></td>
    <td>Full support for the TiProxy service, easily deployable via deployment tooling, to manage and maintain connections to TiDB so that they live through rolling restarts, upgrades, or scaling events.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/dm-compatibility-catalog">Data Migration (DM) officially supports MySQL 8.0 (GA)</a></td>
    <td>Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (experimental) [#7431](https://github.com/tikv/pd/issues/7431) @[CabinfeverB](https://github.com/CabinfeverB)

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability, TiDB v7.6.0 supports using the Active PD Follower feature to enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).

### Performance

* BR improves snapshot restore speed by up to 10 times (experimental) [#33937](https://github.com/pingcap/tidb/issues/33937) [#49886](https://github.com/pingcap/tidb/issues/49886) @[3pointer](https://github.com/3pointer)

    As a TiDB cluster scales up, it becomes increasingly crucial to quickly restore the cluster from failures to minimize business downtime. Before v7.6.0, the Region scattering algorithm is a primary bottleneck in performance restoration. In v7.6.0, BR optimizes the Region scattering algorithm, which quickly splits the restore task into a large number of small tasks and scatters them to all TiKV nodes in batches. The new parallel recovery algorithm fully utilizes the resources of each TiKV node, thereby achieving a rapid parallel recovery. In several real-world cases, the snapshot restore speed of the cluster is improved by about 10 times in large-scale Region scenarios.

    The new coarse-grained Region scatter algorithm is experimental. To use it, you can configure the `--granularity="coarse-grained"` parameter in the `br` command. You can also control the concurrency of download tasks on each TiKV node by setting the `--tikv-max-restore-concurrency` parameter. For example:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --tikv-max-restore-concurrency 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
    ```

    For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* The Titan engine is enabled by default [#16245](https://github.com/tikv/tikv/issues/16245) @[Connor1996](https://github.com/Connor1996) @[v01dstar](https://github.com/v01dstar) @[tonyxuqqi](https://github.com/tonyxuqqi)

    To better support TiDB wide table write scenarios, especially with support for JSON, starting from TiDB v7.6.0, the Titan engine is enabled by default. The Titan engine automatically segregates large values exceeding 32 KB from RocksDB's LSM Tree, and stores them separately in Titan to optimize the handling of large values. The Titan engine is completely compatible with RocksDB features utilized by TiKV. This strategic shift not only diminishes write amplification effect, but also enhances performance in write, update, and point-query scenarios involving large values. Additionally, in Range Scan scenarios, the Titan engine's optimization has resulted in performance comparable to that of RocksDB in the default configuration.

    This configuration change remains compatible with earlier versions. For existing TiDB clusters, when upgrading to TiDB v7.6.0 or a later version, the Titan engine is disabled by default. You have the flexibility to manually enable or disable the Titan engine based on your specific requirements.

    For more information, see [documentation](/storage-engine/titan-overview.md).

* Support pushing down the following string functions to TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi)

    * `LOWER()`
    * `UPPER()`

  For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support pushing down the following JSON functions to TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) [#49392](https://github.com/pingcap/tidb/issues/49392) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87)

    * `JSON_UNQUOTE()`
    * `JSON_ARRAY()`
    * `JSON_DEPTH()`
    * `JSON_VALID()`
    * `JSON_KEYS()`
    * `JSON_CONTAINS_PATH()`

  For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Improve the performance of creating tables by 10 times (experimental) [#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd)

    In previous versions, when migrating tens of thousands of tables from the upstream database to TiDB, it is time-consuming and inefficient for TiDB to create these tables. Starting from v7.6.0, TiDB introduces a new TiDB DDL V2 architecture. You can enable it by configuring the system variable [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760). Compared with previous versions, the new version of the DDL improves the performance of creating batch tables by 10 times, and significantly reduces time for creating tables.

    For more information, see [documentation](/ddl-v2.md).

* Support periodic full compaction (experimental) [#12729](https://github.com/tikv/tikv/issues/12729) [afeinberg](https://github.com/afeinberg)

    Starting from v7.6.0, TiDB supports periodic full compaction for TiKV. This feature serves as an enhancement to Garbage Collection (GC) to eliminate redundant data versions. In scenarios where application activity shows obvious peaks and valleys, you can use this feature to perform data compaction during idle periods to improve the performance during peak periods.

    You can set the specific times that TiKV initiates periodic full compaction by configuring the TiKV configuration item [`periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760) and limit the maximum CPU usage rate for TiKV periodic full compaction by configuring [`periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760). The default value of `periodic-full-compact-start-max-cpu` is 10%, which means that periodic full compaction is triggered only when the CPU utilization of TiKV is lower than 10%, thereby reducing the impact on application traffic.

    For more information, see [documentation](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760).

### Reliability

* Cross-database execution plan binding [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990)

    When running SaaS services on TiDB, it is common practice to store data for each tenant in separate databases for easier data maintenance and management. This results in hundreds of databases with the same table and index definitions, and similar SQL statements. In such scenario, when you create an execution plan binding for a SQL statement, this binding usually applies to the SQL statements in other databases as well.

    For this scenario, TiDB v7.6.0 introduces the cross-database binding feature, which supports binding the same execution plan to SQL statements with the same schema, even if they are in different databases. When creating a cross-database binding, you need to use the wildcard `*` to represent the database name, as shown in the following example. After the binding is created, regardless of which database the tables `t1` and `t2` are in, TiDB will try to use this binding to generate an execution plan for any SQL statement with the same schema, which saves your effort to create a binding for each database.

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount
        FROM *.t1, *.t2
        WHERE t1.id = t2.id;
    ```

    In addition, cross-database binding can effectively mitigate SQL performance issues caused by uneven distribution and rapid changes in user data and workload. SaaS providers can use cross-database binding to fix execution plans validated by users with large data volumes, thereby fixing execution plans for all users. For SaaS providers, this feature provides significant convenience and experience improvements.

    Due to the system overhead (less than 1%) introduced by cross-database binding, TiDB disables this feature by default. To use cross-database binding, you need to first enable the [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) system variable.

    For more information, see [documentation](/sql-plan-management.md#cross-database-binding).

### Availability

* Support the proxy component TiProxy (experimental) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox)

    TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB, making the workload of the TiDB cluster more balanced and not affecting user access to the database during maintenance operations.

    - During maintenance operations such as rolling restarts, rolling upgrades, and scaling-in in a TiDB cluster, changes occur in the TiDB servers which result in interruptions in connections between clients and the TiDB servers. By using TiProxy, connections can be smoothly migrated to other TiDB servers during these maintenance operations so that clients are not affected.
    - Client connections to a TiDB server cannot be dynamically migrated to other TiDB servers. When the workload of multiple TiDB servers is unbalanced, it might result in a situation where the overall cluster resources are sufficient, but certain TiDB servers experience resource exhaustion leading to a significant increase in latency. To address this issue, TiProxy provides dynamic migration for connection, which allows connections to be migrated from one TiDB server to another without any impact on the clients, thereby achieving load balancing for the TiDB cluster.

  TiProxy has been integrated into TiUP, TiDB Operator, and TiDB Dashboard, making it easy to configure, deploy and maintain.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* `LOAD DATA` supports explicit transactions and rollbacks [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium)

    Compared with MySQL, the transactional behavior of the `LOAD DATA` statement varies in different TiDB versions before v7.6.0, so you might need to make additional adjustments when using this statement. Specifically, before v4.0.0, `LOAD DATA` commits every 20000 rows. From v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default and also supports committing every fixed number of rows by setting the [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) system variable. Starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on `LOAD DATA` and TiDB commits all rows in one transaction.

    Starting from v7.6.0, TiDB processes `LOAD DATA` in transactions in the same way as other DML statements, especially in the same way as MySQL. The `LOAD DATA` statement in a transaction no longer automatically commits the current transaction or starts a new transaction. Moreover, you can explicitly commit or roll back the `LOAD DATA` statement in a transaction. Additionally, the `LOAD DATA` statement is affected by the TiDB transaction mode setting (optimistic or pessimistic transaction). These improvements simplify the migration process from MySQL to TiDB and offer a more unified and controllable experience for data import.

    For more information, see [documentation](/sql-statements/sql-statement-load-data.md).

### DB operations

* `FLASHBACK CLUSTER` supports specifying a precise TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger)

    In TiDB v7.6.0, the flashback feature is more powerful and precise. It not only supports rolling back a cluster to a specified historical timestamp but also enables you to specify a precise recovery [TSO](/tso.md) using `FLASHBACK CLUSTER TO TSO`, thereby increasing flexibility in data recovery. For example, you can use this feature with TiCDC. After pausing data replication and conducting pre-online read-write tests in your downstream TiDB cluster, this feature allows the cluster to gracefully and quickly roll back to the paused TSO and continue to replicate data using TiCDC. This streamlines the pre-online validation process and simplifies data management.

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

    For more information, see [documentation](/sql-statements/sql-statement-flashback-cluster.md).

* Support automatically terminating long-running idle transactions [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520)

    In scenarios where network disconnection or application failure occurs, `COMMIT`/`ROLLBACK` statements might fail to be transmitted to the database. This could lead to delayed release of database locks, causing transaction lock waits and a rapid increase in database connections. Such issues are common in test environments but can also occur occasionally in production environments, and they are sometimes difficult to diagnose promptly. To avoid these issues, TiDB v7.6.0 introduces the [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) system variable, which automatically terminates long-running idle transactions. When a user session in a transactional state remains idle for a duration exceeding the value of this variable, TiDB will terminate the database connection of the transaction and roll back it.

    For more information, see [documentation](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760).

* Simplify the syntax for creating execution plan bindings [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990)

    TiDB v7.6.0 simplifies the syntax for creating execution plan bindings. When creating an execution plan binding, you no longer need to provide the original SQL statement. TiDB identifies the original SQL statement based on the statement with hints. This improvement enhances the convenience of creating execution plan bindings. For example:

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement).

* Support dynamically modifying the size limit of a single row record in TiDB [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan)

    Before v7.6.0, the size of a single row record in a transaction is limited by the TiDB configuration item [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). If the size limit is exceeded, TiDB returns the `entry too large` error. In this case, you need to manually modify the TiDB configuration file and restart TiDB to make the modification take effect. To reduce your management overhead, TiDB v7.6.0 introduces the system variable [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760), which supports dynamically modifying the value of the `txn-entry-size-limit` configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, TiDB limits the size of a row record in transactions to the value of this variable. This improvement enhances the flexibility for you to adjust system configurations without restarting TiDB.

    For more information, see [documentation](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760).

* BR restores system tables by default, such as user data [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) [#49627](https://github.com/pingcap/tidb/issues/49627) @[Leavrth](https://github.com/Leavrth)

    Starting from v5.1.0, when you back up snapshots, BR automatically backs up system tables in the `mysql` schema, but does not restore these system tables by default. In v6.2.0, BR adds the parameter `--with-sys-table` to support restoring data in some system tables, providing more flexibility in operations.

    To further reduce your management overhead and provide more intuitive default behavior, starting from v7.6.0, BR enables the parameter `--with-sys-table` by default and supports restoring user data for the `cloud_admin` user. This means that BR restores some system tables by default during restoration, especially user account and table statistics data. This improvement makes backup and restore operations more intuitive, thereby reducing the burden of manual configuration and improving the overall operation experience.

    For more information, see [documentation](/br/br-snapshot-guide.md).

### Observability

* Enhance observability related to resource control [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch)

    As more and more users use resource groups to isolate application workloads, Resource Control provides enhanced data based on resource groups. This helps you monitor resource group workloads and settings, ensuring that you can quickly identify and accurately diagnose problems, including:

    * [Slow Queries](/identify-slow-queries.md): add the resource group name, resource unit (RU) consumption, and time for waiting for resources.
    * [Statement Summary Tables](/statement-summary-tables.md): add the resource group name, RU consumption, and time for waiting for resources.
    * In the system variable [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014), add a new entry `ru_consumption` to indicate the consumed [RU](/tidb-resource-control.md#what-is-request-unit-ru) by SQL statements. You can use this variable to get the resource consumption of the last statement in the session.
    * Add database metrics based on resource groups: QPS/TPS, execution time (P999/P99/P95), number of failures, and number of connections.
    * Add the system table [`request_unit_by_group`](/mysql-schema.md#system-tables-related-to-resource-control) to record the history records of daily consumed RUs of all resource groups.

  For more information, see [Identify Slow Queries](/identify-slow-queries.md), [Statement Summary Tables](/statement-summary-tables.md), and [Key Monitoring Metrics of Resource Control](/grafana-resource-control-dashboard.md).

### Data migration

* Data Migration (DM) support for migrating MySQL 8.0 becomes generally available (GA) [#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001)

    Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).

    For more information, see [documentation](/dm/dm-compatibility-catalog.md).

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (experimental) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen)

    Starting from v7.6.0, TiCDC supports replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC supports querying the downstream synchronization status of a changefeed [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)

    Starting from v7.6.0, TiCDC introduces a new API `GET /api/v2/changefeed/{changefeed_id}/synced` to query the downstream synchronization status of a specified replication task (changefeed). By using this API, you can determine whether the upstream data received by TiCDC has been synchronized to the downstream system completely.

    For more information, see [documentation](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed).

* TiCDC adds support for three-character delimiters with CSV output protocol [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng87](https://github.com/zhangjinpeng87)

    Starting from v7.6.0, you can specify the CSV output protocol delimiters as 1 to 3 characters long. With this change, you can configure TiCDC to generate file output using two-character delimiters (such as `||` or `$^`) or three-character delimiters (such as `|@|`) to separate fields in the output.

    For more information, see [documentation](/ticdc/ticdc-csv.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.5.0 to the current version (v7.6.0). If you are upgrading from v7.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### MySQL compatibility

* Before TiDB v7.6.0, the `LOAD DATA` operation commits all rows in a single transaction or commits transactions in a batch, which is slightly different from MySQL behaviors. Starting from v7.6.0, TiDB processes `LOAD DATA` in transactions in the same way as MySQL. The `LOAD DATA` statement in a transaction no longer automatically commits the current transaction or starts a new transaction. Moreover, you can explicitly commit or roll back the `LOAD DATA` statement in a transaction. Additionally, the `LOAD DATA` statement is affected by the TiDB transaction mode setting (optimistic or pessimistic transaction). [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium)

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | Modified | Changes the default value from `1` to `128` after further tests.  |
| [`tidb_sysproc_scan_concurrency`](/system-variables.md#tidb_sysproc_scan_concurrency-new-in-v650) | Modified  | In a large-scale cluster, the concurrency of `scan` operations can be adjusted higher to meet the needs of `ANALYZE`. Therefore, change the maximum value from `256` to `4294967295`.  |
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)       |    Newly added       |    Sets the concurrency of the `scan` operation when executing the `ANALYZE` operation. The default value is `4`.  |
| [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760)  |  Newly added  | Controls whether to enable [TiDB DDL V2](/ddl-v2.md). Set the value to `2` to enable it and `1` to disable it. The default value is `1`. When TiDB DDL V2 is enabled, DDL statements will be executed using TiDB DDL V2. The execution speed of DDL statements for creating tables is increased by 10 times compared with TiDB DDL V1. |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)  |  Newly added   | Controls whether to support creating `Global indexes` for partitioned tables. The default value is `OFF`. `Global index` is currently in the development stage. **It is not recommended to modify the value of this system variable**. |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) | Newly added | Controls the idle timeout for transactions in a user session. When a user session is in a transactional state and remains idle for a duration exceeding the value of this variable, TiDB will terminate the session. The default value `0` means unlimited. |
| [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) | Newly added | Controls whether to enable the cross-database binding feature. The default value `OFF` means cross-database binding is disabled. |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) | Newly added | Dynamically modifies the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value. |
| [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) | Newly added | Controls whether to enable the [Active PD Follower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) feature (experimental). When the value is `OFF`, TiDB only obtains Region information from the PD leader. When the value is `ON`, TiDB evenly distributes requests for Region information to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiDB | [`tls-version`](/tidb-configuration-file.md#tls-version) | Modified | The default value is "". The default supported TLS versions of TiDB are changed from `TLS1.1` or higher to `TLS1.2` or higher. |
| TiKV | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Modified | The algorithm used for compressing values in Titan, which takes value as the unit. Starting from TiDB v7.6.0, the default compression algorithm is `zstd`. |
| TiKV | [`rocksdb.defaultcf.titan.min-blob-size`](/tikv-configuration-file.md#min-blob-size) | Modified   | Starting from TiDB v7.6.0, the default value for new clusters is `32KB`. For existing clusters upgrading to v7.6.0, the default value `1KB` remains unchanged. |
| TiKV | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled) | Modified  |  Enables or disables Titan. For v7.5.0 and earlier versions, the default value is `false`. Starting from v7.6.0, the default value is `true` for only new clusters. Existing clusters upgraded to v7.6.0 or later versions will retain the original configuration. |
| TiKV | [`gc.num-threads`](/tikv-configuration-file.md#num-threads-new-in-v760) | Newly added | When `enable-compaction-filter` is set to `false`, this parameter controls the number of GC threads. The default value is `1`. |
| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760) | Newly added | Sets the specific times that TiKV initiates periodic full compaction. The default value `[]` means periodic full compaction is disabled. |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760) | Newly added | Limits the maximum CPU usage rate for TiKV periodic full compaction. The default value is `0.1`. |
| TiKV | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) |  Newly added | Specifies the `zstd` dictionary compression size. The default value is `"0KB"`, which means to disable the `zstd` dictionary compression. |
| TiFlash | [`logger.level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | Changes the default value from `"debug"` to `"INFO"` to reduce the cost of logging. |
| TiDB Lightning| [`tidb.pd-addr`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Modified  | Configures the addresses of the PD Servers. Starting from v7.6.0, TiDB supports setting multiple PD addresses. |
| TiDB Lightning | [`block-size`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | Controls the I/O block size for sorting local files in Physical Import Mode (`backend='local'`). The default value is `16KiB`. When the disk IOPS is a bottleneck, you can increase this value to improve performance. |
| BR | [`--granularity`](/br/br-snapshot-guide.md#performance-and-impact-of-snapshot-restore) | Newly added | Uses the coarse-grained Region scatter algorithm (experimental) by specifying `--granularity="coarse-grained"`. This accelerates restore speed in large-scale Region scenarios. |
| BR | [`--tikv-max-restore-concurrency`](/br/br-snapshot-guide.md#performance-and-impact-of-snapshot-restore) | Newly added | Controls the concurrency of download tasks for each TiKV node when using the coarse-grained Region scatter algorithm. |
| TiCDC | [`compression`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls the behavior to compress redo log files. |
| TiCDC | [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls the number of encoding and decoding workers in the redo module. The default value is `16`. |
| TiCDC | [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md) | Newly added | Controls the number of flushing workers in the redo module. The default value is `8`. |
| TiCDC | [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md) | Newly added | Sets the automatic cleanup of historical data when replicating data to object storage. |

### System tables

- Add a new system table [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) to display the information of all keywords supported by TiDB.
- In the system table [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md), add the following fields related to Resource Control:
    - `Resource_group`: the resource group that the statement is bound to.
    - `Request_unit_read`: the total read RUs consumed by the statement.
    - `Request_unit_write`: the total write RUs consumed by the statement.
    - `Time_queued_by_rc`: the total time that the statement waits for available resources.

## Offline package changes

Starting from v7.6.0, the `TiDB-community-server` [binary-package](/binary-package.md) now includes `tiproxy-{version}-linux-{arch}.tar.gz`, which is the installation package for the proxy component [TiProxy](/tiproxy/tiproxy-overview.md).

## Deprecated features

* Support for the TLSv1.0 and TLSv1.1 protocols is deprecated in TiDB v7.6.0 and will be removed in v8.0.0. Please upgrade to TLSv1.2 or TLSv1.3.
* The [baseline evolution](/sql-plan-management.md#baseline-evolution) feature for execution plans will be deprecated in TiDB v8.0.0. The equivalent functionality will be redesigned in the subsequent versions.
* The [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) system variable will be deprecated in TiDB v8.0.0. After that, TiDB will no longer support automatic retries of optimistic transactions.

## Improvements

+ TiDB

    - When a non-binary collation is set and the query includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - Improve the balance of Distributed eXecution Framework (DXF) tasks in the scenario where nodes are restarted [#47298](https://github.com/pingcap/tidb/issues/47298) @[ywqzzy](https://github.com/ywqzzy)
    - Support multiple accelerated `ADD INDEX` DDL tasks to be queued for execution, instead of falling back to normal `ADD INDEX` tasks [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - Improve the compatibility of `ALTER TABLE ... ROW_FORMAT` [#48754](https://github.com/pingcap/tidb/issues/48754) @[hawkingrei](https://github.com/hawkingrei)
    - Modify the `CANCEL IMPORT JOB` statement to a synchronous statement [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - Improve the speed of adding indexes to empty tables [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)
    - When the columns of a correlated subquery are not referenced by the upper-level operator, the correlated subquery can be eliminated directly [#45822](https://github.com/pingcap/tidb/issues/45822) @[King-Dylan](https://github.com/King-Dylan)
    - `EXCHANGE PARTITION` operations now trigger maintenance updates of statistics [#47354](https://github.com/pingcap/tidb/issues/47354) @[hi-rustin](https://github.com/hi-rustin)
    - TiDB supports building binary files that meet the requirements of Federal Information Processing Standards (FIPS) [#47948](https://github.com/pingcap/tidb/issues/47948) @[tiancaiamao](https://github.com/tiancaiamao)
    - Optimize the TiDB implementation when handling some type conversions and fix related issues [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - When obtaining the schema version, TiDB uses the KV timeout feature to read by default, reducing the impact of slow meta Region leader reads on schema version updates [#48125](https://github.com/pingcap/tidb/pull/48125) @[cfzjywxk](https://github.com/cfzjywxk)

+ TiKV

    - Add an API endpoint `/async_tasks` for querying asynchronous tasks [#15759](https://github.com/tikv/tikv/issues/15759) @[YuJuncen](https://github.com/YuJuncen)
    - Add priority labels to gRPC monitoring to display resource group data of different priorities [#49318](https://github.com/pingcap/tidb/issues/49318) @[bufferflies](https://github.com/bufferflies)
    - Support dynamically adjusting the value of `readpool.unified.max-tasks-per-worker`, which can calculate the number of running tasks separately based on priority [#16026](https://github.com/tikv/tikv/issues/16026) @[glorv](https://github.com/glorv)
    - Support dynamically adjusting the number of GC threads, with a default value of `1` [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - Improve the availability of PD TSO during disk jitter [#7377](https://github.com/tikv/pd/issues/7377) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Support merging identical data reading operations in a storage-compute separation architecture to improve data scanning performance under high concurrency [#6834](https://github.com/pingcap/tiflash/issues/6834) @[JinheLin](https://github.com/JinheLin)
    - Optimize the execution performance of `SEMI JOIN` and `LEFT OUTER SEMIJOIN` when only JOIN KEY equality conditions are included in `JOIN ON` [#47424](https://github.com/pingcap/tidb/issues/47424) @[gengliqi](https://github.com/gengliqi)

+ Tools

    + Backup & Restore (BR)

        - Introduce a new integration test for Point-In-Time Recovery (PITR) in the `delete range` scenario, enhancing PITR stability  [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - Refactor the BR exception handling mechanism to increase tolerance for unknown errors [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Improve the performance of TiCDC replicating data to object storage by increasing parallelism [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support making TiCDC Canal-JSON content format [compatible with the content format of the official Canal output](/ticdc/ticdc-canal-json.md#compatibility-with-the-official-canal) by setting `content-compatible=true` in the `sink-uri` configuration [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Add configurations for full data physical import to DM OpenAPI [#10193](https://github.com/pingcap/tiflow/issues/10193) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Support configuring multiple PD addresses to enhance stability [#49515](https://github.com/pingcap/tidb/issues/49515) @[mittalrishabh](https://github.com/mittalrishabh)
        - Support configuring the `block-size` parameter to control the I/O block size for sorting local files to improve performance [#45037](https://github.com/pingcap/tidb/issues/45037) @[mittalrishabh](https://github.com/mittalrishabh)

## Bug fixes

+ TiDB

    - Fix the issue that TiDB panics and reports an error `invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - Fix the issue that queries containing common table expressions (CTEs) report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue of Goroutine leak when using `AUTO_ID_CACHE=1` [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that executing `ALTER TABLE ... LAST PARTITION` fails when the partition column type is `DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that using the `_` wildcard in `LIKE` when the data contains trailing spaces can result in incorrect query results [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that the query result is incorrect when an `ENUM` type column is used as the join key [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - Fix the issue that queries containing CTEs unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the optimizer incorrectly converts TiFlash selection path to the DUAL table in specific scenarios [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that in non-strict mode (`sql_mode = ''`), truncation during executing `INSERT` still reports an error [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that `LIMIT` and `ORDER BY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that parsing invalid values of `ENUM` or `SET` types would directly cause SQL statement errors [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - Fix the issue that tables with `AUTO_ID_CACHE=1` might lead to gRPC client leaks when there are a large number of tables [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - Fix the issue that `ADMIN RECOVER INDEX` reports `ERROR 1105` when processing a table containing `CommonHandle` [#47687](https://github.com/pingcap/tidb/issues/47687) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that specifying placement rules when executing `ALTER TABLE t PARTITION BY` reports the error `ERROR 8239` [#48630](https://github.com/pingcap/tidb/issues/48630) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `START_TIME` column type in `INFORMATION_SCHEMA.CLUSTER_INFO` is not valid [#45221](https://github.com/pingcap/tidb/issues/45221) @[dveeden](https://github.com/dveeden)
    - Fix the issue that invalid `EXTRA` column type in `INFORMATION_SCHEMA.COLUMNS` leads to the error `Data Too Long, field len 30, data len 45` [#42030](https://github.com/pingcap/tidb/issues/42030) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `IN (...)` causes different plan digests in `INFORMATION_SCHEMA.STATEMENTS_SUMMARY` [#33559](https://github.com/pingcap/tidb/issues/33559) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that when converting the `TIME` type to the `YEAR` type, the returned result mixes `TIME` and the year [#48557](https://github.com/pingcap/tidb/issues/48557) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that disabling `tidb_enable_collect_execution_info` causes the coprocessor cache to panic [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - Fix the issue that TiDB crashes when `shuffleExec` quits unexpectedly [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that static `CALIBRATE RESOURCE` relies on the Prometheus data [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - Fix the issue that when adding a large interval to a date, it returns an incorrect result. After the fix, an interval with an invalid prefix or the string `true` is treated as zero, which is consistent with MySQL 8.0 [#49227](https://github.com/pingcap/tidb/issues/49227) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `ROW` function incorrectly infers the `null` type and causes an unexpected error [#49015](https://github.com/pingcap/tidb/issues/49015) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `ILIKE` function might cause data race in some scenarios [#49677](https://github.com/pingcap/tidb/issues/49677) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that encoding fails when converting bytes to `TIME` [#47346](https://github.com/pingcap/tidb/issues/47346) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the behavior of the `ENFORCED` option in the `CHECK` constraint is inconsistent with MySQL 8.0 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that DDL statements with the `CHECK` constraint are stuck [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that adding index fails for DDL statements due to out of memory [#47862](https://github.com/pingcap/tidb/issues/47862) @[GMHDBJD](https://github.com/GMHDBJD)
    - Fix the issue that upgrading the cluster during executing `ADD INDEX` might cause the data to be inconsistent with the indexes [#46306](https://github.com/pingcap/tidb/issues/46306) @[zimulala](https://github.com/zimulala)
    - Fix the issue that executing `ADMIN CHECK` after updating the `tidb_mem_quota_query` system variable returns `ERROR 8175` [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - Fix the issue that when `ALTER TABLE` modifies the type of a column referenced by a foreign key, the change in `DECIMAL` precision is not reported as an error [#49836](https://github.com/pingcap/tidb/issues/49836) @[yoshikipom](https://github.com/yoshikipom)
    - Fix the issue that when `ALTER TABLE` modifies the type of a column referenced by a foreign key, the change in `INTEGER` length is reported as an error by mistake [#47702](https://github.com/pingcap/tidb/issues/47702) @[yoshikipom](https://github.com/yoshikipom)
    - Fix the issue that in some scenarios the expression index does not detect that the divisor is 0 [#50053](https://github.com/pingcap/tidb/issues/50053) @[lcwangchao](https://github.com/lcwangchao)
    - Mitigate the issue that TiDB nodes might encounter OOM errors when dealing with a large number of tables [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - Fix the issue that DDL gets stuck in the running state during cluster rolling restart [#50073](https://github.com/pingcap/tidb/issues/50073) @[tangenta](https://github.com/tangenta)
    - Fix the issue that results might be incorrect when accessing global indexes of partitioned tables using `PointGet` or `BatchPointGet` operators [#47539](https://github.com/pingcap/tidb/issues/47539) @[L-maple](https://github.com/L-maple)
    - Fix the issue that MPP plans might not be selected when indexes on generated columns are set as visible [#47766](https://github.com/pingcap/tidb/issues/47766) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `LIMIT` might not be pushed down to the `OR` type `Index Merge` [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that duplicate built-in rows might exist in the `mysql.bind_info` table after BR import [#46527](https://github.com/pingcap/tidb/issues/46527) @[qw4990](https://github.com/qw4990)
    - Fix the issue that statistics for partitioned tables are not updated as expected after partitions are dropped [#48182](https://github.com/pingcap/tidb/issues/48182) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that errors might be returned during the concurrent merging of global statistics for partitioned tables [#48713](https://github.com/pingcap/tidb/issues/48713) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that query results might be incorrect when the `LIKE` operator is used for index range scans on a column with PADDING SPACE [#48821](https://github.com/pingcap/tidb/issues/48821) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that generated columns might trigger concurrent read and write on memory and result in data race [#44919](https://github.com/pingcap/tidb/issues/44919) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `ANALYZE TABLE` might still collect Top1 statistics even when `WITH 0 TOPN` (indicating not collecting topN statistics) is specified [#49080](https://github.com/pingcap/tidb/issues/49080) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that illegal optimizer hints might cause valid hints to be ineffective [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that statistics for Hash partitioned tables are not correspondingly updated when you add, drop, reorganize, or `TRUNCATE` partitions [#48235](https://github.com/pingcap/tidb/issues/48235) [#48233](https://github.com/pingcap/tidb/issues/48233) [#48226](https://github.com/pingcap/tidb/issues/48226) [#48231](https://github.com/pingcap/tidb/issues/48231) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that after the time window for automatic statistics updates is configured, statistics might still be updated outside that time window [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that old statistics are not automatically deleted when a partitioned table is converted to a non-partitioned table [#49547](https://github.com/pingcap/tidb/issues/49547) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that old statistics are not automatically deleted when you clear data from a non-partitioned table using `TRUNCATE TABLE` [#49663](https://github.com/pingcap/tidb/issues/49663) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that executing queries containing the `GROUP_CONCAT(ORDER BY)` syntax might return errors [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `UPDATE`, `DELETE`, and `INSERT` statements return overflow errors instead of warnings when the `SQL_MODE` is not strict [#49137](https://github.com/pingcap/tidb/issues/49137) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that data cannot be inserted when a table has a composite index consisting of multi-valued indexes and non-binary type strings [#49680](https://github.com/pingcap/tidb/issues/49680) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `LIMIT` in multi-level nested `UNION` queries might become ineffective [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that querying partitioned tables with the `BETWEEN ... AND ...` condition returns incorrect results [#49842](https://github.com/pingcap/tidb/issues/49842) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that TiDB might select the wrong partition when querying Hash partitioned tables [#50044](https://github.com/pingcap/tidb/issues/50044) @[Defined2014](https://github.com/Defined2014)
    - Fix the connection error that occurs when you use MariaDB Connector/J with compression enabled [#49845](https://github.com/pingcap/tidb/issues/49845) @[onlyacat](https://github.com/onlyacat)

+ TiKV

    - Fix the issue that the damaged SST files might spread to other TiKV nodes and cause TiKV to panic [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that Resolved TS might be blocked for two hours [#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Flashback might get stuck when encountering `notLeader` or `regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that if TiKV runs extremely slowly, it might panic after Region merge [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV cannot read in-memory pessimistic locks when GC scans expired locks [#15066](https://github.com/tikv/tikv/issues/15066) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that the blob file size in Titan monitoring is incorrect [#15971](https://github.com/tikv/tikv/issues/15971) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that replicating large tables using TiCDC might cause TiKV to OOM  [#16035](https://github.com/tikv/tikv/issues/16035) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - Fix the issue that `cast_duration_as_time` might return incorrect results [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)

+ PD

    - Fix the issue that the etcd health check in PD does not remove expired addresses [#7226](https://github.com/tikv/pd/issues/7226) @[iosmanthus](https://github.com/iosmanthus)
    - Fix the issue that when PD leader is transferred and there is a network partition between the new leader and the PD client, the PD client fails to update the information of the leader [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix some security issues by upgrading the version of Gin Web Framework from v1.8.1 to v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that some TiFlash replica data cannot be recovered through `RECOVER TABLE` or `FLASHBACK TABLE` in scenarios with frequent execution of `CREATE TABLE` and `DROP TABLE` [#1664](https://github.com/pingcap/tiflash/issues/1664) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that query results are incorrect when querying with filtering conditions like `ColumnRef in (Literal, Func...)` [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the TiFlash panic issue when TiFlash encounters conflicts during concurrent DDL execution [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might not be able to select the GC owner of object storage data under the disaggregated storage and compute architecture [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiFlash incorrectly handles `ENUM` when the `ENUM` value is 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - Fix the incompatibility issue in the `INET_NTOA()` expression [#8211](https://github.com/pingcap/tiflash/issues/8211) @[solotzg](https://github.com/solotzg)
    - Fix the potential OOM issue that might occur when scanning multiple partitioned tables during stream read [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that short queries executed successfully print excessive info logs [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiFlash might crash when it is stopped [#8550](https://github.com/pingcap/tiflash/issues/8550) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the random invalid memory access issue that might occur with `GREATEST` or `LEAST` functions containing constant string parameters [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the log backup task might encounter memory leak and fail to run properly after startup [#16070](https://github.com/tikv/tikv/issues/16070) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that inserting data into the system table `mysql.gc_delete_range` during the PITR process returns an error [#49346](https://github.com/pingcap/tidb/issues/49346) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - Fix the issue that permissions are not updated timely after user tables are recovered through snapshots in certain scenarios [#49394](https://github.com/pingcap/tidb/issues/49394) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that the `WHERE` clause does not use the primary key as a condition when replicating `DELETE` statements in certain scenarios [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - Fix the potential data race issue during `kv-client` initialization [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC mistakenly closes the connection with TiKV in certain special scenarios [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - Fix the issue that TiCDC server might panic when executing lossy DDL statements in upstream [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - Fix the issue that `checkpoint-ts` might get stuck when TiCDC replicates data to downstream MySQL [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng87](https://github.com/zhangjinpeng87)

    + TiDB Data Migration (DM)

        - Fix the issue that DM encounters "event type truncate not valid" error that causes the upgrade to fail [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the performance degradation issue when replicating data in GTID mode [#9676](https://github.com/pingcap/tiflow/issues/9676) @[feran-morgan-pingcap](https://github.com/feran-morgan-pingcap)
        - Fix the issue that a migration task error occurs when the downstream table structure contains `shard_row_id_bits` [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [0o001](https://github.com/0o001) (First-time contributor)
- [bagechengzi](https://github.com/bagechengzi) (First-time contributor)
- [feran-morgan-pingcap](https://github.com/feran-morgan-pingcap) (First-time contributor)
- [highpon](https://github.com/highpon)
- [jiyfhust](https://github.com/jiyfhust)
- [L-maple](https://github.com/L-maple)
- [lkshminarayanan](https://github.com/lkshminarayanan) (First-time contributor)
- [lyang24](https://github.com/lyang24) (First-time contributor)
- [mittalrishabh](https://github.com/mittalrishabh)
- [morgo](https://github.com/morgo)
- [nkg-](https://github.com/nkg-) (First-time contributor)
- [onlyacat](https://github.com/onlyacat)
- [shawn0915](https://github.com/shawn0915)
- [Smityz](https://github.com/Smityz)
- [szpnygo](https://github.com/szpnygo) (First-time contributor)
- [ub-3](https://github.com/ub-3) (First-time contributor)
- [xiaoyawei](https://github.com/xiaoyawei) (First-time contributor)
- [yorkhellen](https://github.com/yorkhellen)
- [yoshikipom](https://github.com/yoshikipom) (First-time contributor)
- [Zheaoli](https://github.com/Zheaoli)
