---
title: TiDB 6.3.0 Release Notes
---

# TiDB 6.3.0 Release Notes

Release date: September 30, 2022

TiDB version: 6.3.0-DMR

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v6.3.0#version-list)

In v6.3.0-DMR, the key new features and improvements are as follows:

- TiKV supports encryption at rest using the SM4 algorithm.
- TiDB supports authentication using the SM3 algorithm.
- The `CREATE USER` and `ALTER USER` statements support the `ACCOUNT LOCK/UNLOCK` option.
- JSON data type and functions become generally available (GA).
- TiDB supports null-aware anti join.
- TiDB provides execution time metrics at a finer granularity.
- A new syntactic sugar is added to simplify Range partition definitions.
- Range COLUMNS partitioning supports defining multiple columns.
- The performance of adding indexes is tripled.
- Reduce the impact of resource-consuming queries on the response time of lightweight queries by more than 50%.

## New features

### SQL

* Add a new syntactic sugar (Range INTERVAL partitioning) to simplify Range partition definitions (experimental) [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    TiDB provides [INTERVAL partitioning](/partitioned-table.md#range-interval-partitioning) as a new way of defining Range partitions. You do not need to enumerate all partitions, which drastically reduces the length of Range partitioning DDL statements. The syntax is equivalent to that of the original Range partitioning.

* Range COLUMNS partitioning supports defining multiple columns [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    TiDB supports [PARTITION BY RANGE COLUMNS (column_list)](/partitioned-table.md#range-columns-partitioning). `column_list` is no longer limited to a single column. The basic feature is the same as MySQL.

* [EXCHANGE PARTITION](/partitioned-table.md#partition-management) becomes GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)

* Support pushdown of two more [window functions](/tiflash/tiflash-supported-pushdown-calculations.md) to TiFlash [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise)

    * `LEAD()`
    * `LAG()`

* Provide lightweight metadata lock to improve the DML success rate during DDL change (experimental) [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

    TiDB uses the online asynchronous schema change algorithm to support changing metadata objects. When a transaction is executed, it obtains the corresponding metadata snapshot at the transaction start. If the metadata is changed during a transaction, to ensure data consistency, TiDB returns an `Information schema is changed` error and the transaction fails to commit. To solve the problem, TiDB v6.3.0 introduces [metadata lock](/metadata-lock.md) into the online DDL algorithm. To avoid DML errors whenever possible, TiDB coordinates the priority of DMLs and DDLs during table metadata change, and makes executing DDLs wait for the DMLs with old metadata to commit.

* Improve the performance of adding indexes and reduce its impact on DML transactions (experimental) [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037)

    To improve the speed of backfilling when creating an index, TiDB v6.3.0 accelerates the `ADD INDEX` and `CREATE INDEX` DDL operations when the [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) system variable is enabled. When the feature is enabled, the performance of adding indexes is about tripled.

### Security

* TiKV supports the SM4 algorithm for encryption at rest [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    Add the [SM4 algorithm](/encryption-at-rest.md) for TiKV encryption at rest. When you configure encryption at rest, you can enable the SM4 encryption capacity by setting the value of the `data-encryption-method` configuration to `sm4-ctr`.

* TiDB supports authentication with the SM3 algorithm [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB adds an authentication plugin [`tidb_sm3_password`](/security-compatibility-with-mysql.md) based on the SM3 algorithm. When this plugin is enabled, the user password is encrypted and validated using the SM3 algorithm.

* TiDB JDBC supports authentication with the SM3 algorithm [#25](https://github.com/pingcap/mysql-connector-j/issues/25) @[lastincisor](https://github.com/lastincisor)

    Authenticating the user password needs client-side support. Now because [JDBC supports the SM3 algorithm](/develop/dev-guide-choose-driver-or-orm.md#java-drivers), you can connect to TiDB using SM3 authentication via TiDB-JDBC.

### Observability

* TiDB provides fine-grained metrics of SQL query execution time [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 provides fine-grained data metrics for [detailed observation of execution time](/latency-breakdown.md). Through the complete and segmented metrics, you can clearly understand the main time consumption of SQL queries, and then quickly find key problems and save time in troubleshooting.

* Enhanced output for slow logs and `TRACE` statements [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 enhances the output of slow logs and `TRACE`. You can observe the [full-link duration](/latency-breakdown.md) of SQL queries from TiDB parsing to KV RocksDB writing to disk, which further enhances the diagnostic capabilities.

* TiDB Dashboard provides deadlock history information [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    From v6.3.0, TiDB Dashboard provides deadlock history. If you check the slow log in TiDB Dashboard and find the lock waiting time of some SQL statements to be excessively long, you can check the deadlock history to locate the root cause, which makes your diagnosis easier.

### Performance

* TiFlash changes the way of using FastScan (experimental) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    In v6.2.0, TiFlash introduces the FastScan feature, which brings expected performance improvements but lacks flexibility in use. Therefore, in v6.3.0, TiFlash changes [the way of using FastScan](/develop/dev-guide-use-fastscan.md): the `ALTER TABLE ... SET TIFLASH MODE ...` syntax to enable or disable FastScan is deprecated. Instead, you can use the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) to easily control whether to enable FastScan.

    When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. You need to set the variable `tiflash_fastscan`. When you upgrade from v6.2.0 or an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistency.

* TiFlash optimizes data scanning performance in scenarios of multiple concurrency tasks [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash reduces duplicate reads of the same data by combining read operations of the same data. It optimizes the resource overhead and [improves the performance of data scanning in the case of concurrent tasks](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). For multiple concurrent tasks, it avoids the situation where each task needs to read the same data separately, and avoids the possibility of multiple reads of the same data at the same time.

    This feature is experimental in v6.2.0, and becomes GA in v6.3.0.

* TiFlash improves performance of data replication [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

    TiFlash uses the Raft protocol for data replication from TiKV. Prior to v6.3.0, it often took a long time to replicate large amounts of replica data. TiDB v6.3.0 optimizes the TiFlash data replication mechanism and significantly improves the replication speed. When you use BR to recover data, use TiDB Lightning to import data, or add new TiFlash replicas, the TiFlash replicas can be replicated more quickly. You can query with TiFlash in a more timely manner. In addition, TiFlash replicas will also reach a secure and balanced state faster when you scale up, scale down, or modify the number of TiFlash replicas.

* TiFlash supports three-stage aggregation of individual `COUNT(DISTINCT)` [#37202](https://github.com/pingcap/tidb/issues/37202) @[fixdb](https://github.com/fixdb)

     TiFlash supports rewriting queries containing only one `COUNT(DISTINCT)` into a [three-stage aggregation](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630). This improves concurrency and performance.

* TiKV supports log recycling [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV supports [recycling log files](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) in Raft Engine. This reduces the long tail latency in network disks during Raft log appending and improves performance under write workloads.

* TiDB supports null-aware anti join [#37525](https://github.com/pingcap/tidb/issues/37525) @[Arenatlx](https://github.com/Arenatlx)

    TiDB v6.3.0 introduces a new join type [Null-aware anti join (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries). NAAJ can be aware of whether the collection is empty or `NULL` when processing collection operations. This optimizes the execution efficiency of operations such as `IN` and `= ANY` and improves SQL performance.

* Add optimizer hints to control the build end of Hash Join [#35439](https://github.com/pingcap/tidb/issues/35439) @[Reminiscent](https://github.com/Reminiscent)

    In v6.3.0, the TiDB optimizer introduces 2 hints, `HASH_JOIN_BUILD()` and `HASH_JOIN_PROBE()`, to specify the Hash Join, its probe end, and its build end. When the optimizer fails to select the optimal execution plan, you can use these hints to intervene with the plan.

* Support session-level common table expressions (CTE) inline [#36514](https://github.com/pingcap/tidb/issues/36514) @[elsa0520](https://github.com/elsa0520)

    TiDB v6.2.0 introduced the `MERGE` hint in optimizers to allow CTE inline, so that the consumers of a CTE query result can execute it in parallel in TiFlash. In v6.3.0, a session variable [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) is introduced to allow CTE inline in sessions. This can greatly improve the ease of use.

### Transactions

* Support deferring checks of unique constraints in pessimistic transactions [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium)

    You can use the [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) system variable to control when TiDB checks [unique constraints](/constraints.md#pessimistic-transactions) in pessimistic transactions. This variable is disabled by default. When the variable is enabled (set to `ON`), TiDB will defer locking operations and unique constraint checks in pessimistic transactions until necessary, thus improving the performance of bulk DML operations.

* Optimize the way of fetching TSO in the Read-Committed isolation level [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin)

    In the Read-Committed isolation level, the system variable [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) is introduced to control how TSO is fetched. In the case of Plan Cache hit, TiDB improves the execution efficiency of batch DML statements by reducing the frequency of fetching TSO, and reduces the execution time of running tasks in batch.

### Stability

* Reduce the impact of resource-consuming queries on the response time of lightweight queries [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

    When resource-consuming queries and lightweight queries are executed at the same time, the response time of lightweight queries is affected. In this case, to ensure the quality of transactional services, lightweight queries are expected to be processed by TiDB first. In v6.3.0, TiKV optimizes the scheduling mechanism of read requests, so that the execution time of resource-consuming queries in each round can meet expectations. This drastically reduces the impact of resource-consuming queries on the response time of lightweight queries and reduces P99 latency by more than 50% for mixed workload scenarios.

* Modify the default policy of loading statistics when statistics become outdated [#27601](https://github.com/pingcap/tidb/issues/27601) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    In v5.3.0, TiDB introduced the system variable [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) to control how the optimizer behaves when the statistics become outdated. The default value is `ON`, which means keeping the behavior of the old version: When the statistics on objects that are involved in a SQL statement are outdated, the optimizer considers that statistics (other than the total number of rows on the table) are no longer reliable and uses pseudo statistics instead. After tests and analyses of actual user scenarios, the default value of `tidb_enable_pseudo_for_outdated_stats` is changed to `OFF` since v6.3.0. Even if the statistics become outdated, the optimizer will still use the statistics on the table, which makes the execution plan more stable.

* Disabling Titan becomes GA @[tabokie](https://github.com/tabokie)

    You can [disable Titan](/storage-engine/titan-configuration.md#disable-titan) for online TiKV nodes.

* Use `static` partition pruning when GlobalStats are not ready [#37535](https://github.com/pingcap/tidb/issues/37535) @[Yisaer](https://github.com/Yisaer)

    When [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode) is enabled, the optimizer selects execution plans based on [GlobalStats](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode). Before GlobalStats are fully collected, using pseudo statistics might cause performance regression. In v6.3.0, this issue is addressed by maintaining the `static` mode if you enable dynamic pruning before GlobalStats are collected. TiDB remains in the `static` mode until GlobalStats are collected. This ensures performance stability when you change the partition pruning settings.

### Ease of use

* Address the conflict between SQL-based data Placement Rules and TiFlash replicas [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

    TiDB v6.0.0 provides SQL-based data Placement Rules. But this feature conflicts with TiFlash replicas due to implementation issues. TiDB v6.3.0 optimizes the implementation mechanisms, and [resolves the conflict between SQL-based data Placement Rules and TiFlash](/placement-rules-in-sql.md#known-limitations).

### MySQL compatibility

* Improve MySQL 8.0 compatibility by adding support for four regular expression functions: `REGEXP_INSTR()`, `REGEXP_LIKE()`, `REGEXP_REPLACE()`, and `REGEXP_SUBSTR()` [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker)

    For more details about the compatibility with MySQL, see [Regular expression compatibility with MySQL](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql).

* The `CREATE USER` and `ALTER USER` statements support the `ACCOUNT LOCK/UNLOCK` option [#37051](https://github.com/pingcap/tidb/issues/37051) @[CbcWestwolf](https://github.com/CbcWestwolf)

    When you create a user using the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) statement, you can specify whether the created user is locked using the `ACCOUNT LOCK/UNLOCK` option. A locked user cannot log in to the database.

    You can modify the lock state of an existing user using the `ACCOUNT LOCK/UNLOCK` option in the [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) statement.

* JSON data type and JSON functions become GA [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei)

    JSON is a popular data format adopted by a large number of programs. TiDB has introduced the [JSON support](/data-type-json.md) as an experimental feature since an earlier version, compatible with MySQL's JSON data type and some JSON functions.

    In TiDB v6.3.0, the JSON data type and functions become GA, which enriches TiDB’s data types, supports using JSON functions in [expression indexes](/sql-statements/sql-statement-create-index.md#expression-index) and [generated-columns](/generated-columns.md), and further improves TiDB’s compatibility with MySQL.

### Backup and restore

* PITR supports [GCS and Azure Blob Storage](/br/backup-and-restore-storages.md) as backup storages @[joccau](https://github.com/joccau)

    If your TiDB cluster is deployed on GCP or Azure, you can use the PITR feature after upgrading your cluster to v6.3.0.

* BR supports AWS S3 Object Lock [#13442](https://github.com/tikv/tikv/issues/13442) @[3pointer](https://github.com/3pointer)

    You can protect backup data on AWS from being tampered with or deleted by enabling [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html).

### Data migration

* TiDB Lightning supports [importing Parquet files exported by Apache Hive into TiDB](/tidb-lightning/tidb-lightning-data-source.md#parquet) [#37536](https://github.com/pingcap/tidb/issues/37536) @[buchuitoudegou](https://github.com/buchuitoudegou)

* DM adds a new configuration item `safe-mode-duration` [#6224](https://github.com/pingcap/tiflow/issues/6224) @[okJiang](https://github.com/okJiang)

    This configuration item is added to the [task configuration file](/dm/task-configuration-file-full.md). You can adjust the automatic safe mode duration after DM exits abnormally. The default value is 60 seconds. If `safe-mode-duration` is set to `"0s"`, an error is reported when DM tries to enter safe mode after an abnormal restart.

### TiDB data share subscription

* TiCDC supports a deployment topology that can replicate data from multiple geo-distributed data sources [#5301](https://github.com/pingcap/tiflow/issues/5301) @[sdojjy](https://github.com/sdojjy)

    To support replicating data from a single TiDB cluster to multiple geo-distributed data systems, starting from v6.3.0, [you can deploy TiCDC in multiple IDCs](/ticdc/deploy-ticdc.md) to replicate data for each IDC. This feature helps deliver the capability of geo-distributed data replication and deployment topology.

* TiCDC supports keeping the snapshots consistent between the upstream and the downstream (sync point) [#6977](https://github.com/pingcap/tiflow/issues/6977) @[asddongmen](https://github.com/asddongmen)

    In the scenarios of data replication for disaster recovery, TiCDC supports [periodically maintaining a downstream data snapshot](/sync-diff-inspector/upstream-downstream-diff.md#data-check-for-tidb-upstream-and-downstream-clusters) so that the downstream snapshot is consistent with the upstream snapshot. With this feature, TiCDC can better support the scenarios where reads and writes are separate, and help you lower the cost.

* TiCDC supports graceful upgrade [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus) @[3AceShowHand](https://github.com/3AceShowHand)

    When TiCDC is deployed using [TiUP](/ticdc/deploy-ticdc.md#upgrade-cautions) (>=v1.11.0) or [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (>=v1.3.8), you can gracefully upgrade the TiCDC cluster. During the upgrade, data replication latency is kept as low as 30 seconds. This improves stability, empowering TiCDC to better support latency-sensitive applications.

## Compatibility changes

### System variables

| Variable name | Change type | Description |
| --- | --- | --- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | Modified | Adds a new option `tidb_sm3_password`. When this variable is set to `tidb_sm3_password`, SM3 is used as the encryption algorithm. |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630)   | Newly added  | Controls whether to enforce the requirement that a table has a primary key. After this variable is enabled, attempting to create or alter a table without a primary key will produce an error.  |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630) | Newly added | Controls the threshold at which the TiDB server prefers to send read requests to the replica in the same region as the TiDB server when [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40) is set to `closest-adaptive`.  |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | Newly added | Controls when TiDB checks [unique constraints](/constraints.md#pessimistic-transactions) in pessimistic transactions. |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630) | Newly added |  Takes effect only when [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) is enabled. It sets the usage limit of local storage during backfilling when creating an index.  |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) | Newly added | Controls whether to enable the acceleration of `ADD INDEX` and `CREATE INDEX` DDL operations to improve the speed of backfilling when creating an index. |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630) | Newly added |  Controls the concurrency of `flashback cluster`. The feature controlled by this variable is not fully functional in TiDB v6.3.0. Do not change the default value.  |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition) | Deprecated |  Controls whether to enable the [`exchange partitions with tables`](/partitioned-table.md#partition-management) feature. The default value is `ON`, that is, `exchange partitions with tables` is enabled by default.  |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630) | Newly added |  Controls whether to enable the `FOREIGN KEY` feature. The feature controlled by this variable is not fully functional in TiDB v6.3.0. Do not change the default value.  |
| `tidb_enable_general_plan_cache` | Newly added |  Controls whether to enable the General Plan Cache feature. The feature controlled by this variable is not fully functional in TiDB v6.3.0. Do not change the default value.  |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)| Newly added | Specifies whether to enable the [Metadata lock](/metadata-lock.md) feature. |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630) | Newly added |  Controls whether TiDB applies Null-Aware Hash Join when Anti Join is generated by subqueries led by special set operators `NOT IN` and `!= ALL`. |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | Modified | Controls the behavior of the optimizer on using statistics of a table when the statistics are outdated. The default value changes from `ON` to `OFF`, which means the optimizer still keeps using the statistics of the table even if the statistics of this table are outdated. |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) | Modified | Controls whether to enable the dynamic memory control feature for the operator that reads data. When this variable is set to `ON`, the memory usage might not be under the control of [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query). Therefore, the default value is changed from `ON` to `OFF`. |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) | Newly added |  Controls whether read requests in SQL write statements are pushed down to TiFlash. The feature controlled by this variable is not fully functional in TiDB v6.3.0. Do not change the default value.  |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) | Newly added | Controls whether to replace expressions with generated columns in an unsafe way. |
| `tidb_general_plan_cache_size` | Newly added | Controls the maximum number of execution plans that can be cached by General Plan Cache. The feature controlled by this variable is not fully functional in TiDB v6.3.0. Do not change the default value.  |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630) | Newly added | Read-only and used to obtain the result of the last `PLAN REPLAYER DUMP` execution in the current session. |
| [tidb_max_paging_size](/system-variables.md#tidb_max_paging_size-new-in-v630) | Newly added | This variable is used to set the minimum number of rows during the coprocessor paging request process. |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630) | Newly added | Controls whether common table expressions (CTEs) in the entire session are inlined or not. The default value is `OFF`, which means that inlining CTE is not enforced by default. |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630) | Newly added | Specifies whether to rewrite a `COUNT(DISTINCT)` aggregation into a three-stage aggregation in MPP mode. The default value is `ON`. |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | Modified | Specifies whether to enable dynamic pruning. Since v6.3.0, the default value changes to `dynamic`. |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) | Modified | Used for optimizing the timestamp acquisition, which is suitable for scenarios with read-committed isolation level where read-write conflicts are rare. This feature is oriented to specific service workloads and might cause performance regression in other scenarios. For this reason, since v6.3.0, the scope of this variable changes from `GLOBAL \| SESSION` to `INSTANCE`. That means you can enable this feature for specific TiDB instances. |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)  | Newly added | Used for optimizing the acquisition of timestamps and is suitable for scenarios with few point-write conflicts in RC isolation level of pessimistic transactions. Enabling this variable can avoid the latency and overhead brought by obtaining the global timestamps during the execution of point-write statements |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) | Newly added | Controls whether to enable FastScan. If [FastScan](/develop/dev-guide-use-fastscan.md) is enabled (set to `ON`), TiFlash provides more efficient query performance, but does not guarantee the accuracy of the query results or data consistency. |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
| --- | --- | --- | --- |
| TiDB | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) | Newly added | Specifies the file system location used by TiDB to store temporary data. If a feature requires local storage in TiDB nodes, TiDB stores the corresponding temporary data in this location. The default value is `/tmp/tidb`. |
| TiKV | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630) | Newly added | Controls whether to automatically adjust the thread pool size. When it is enabled, the read performance of TiKV is optimized by automatically adjusting the UnifyReadPool thread pool size based on the current CPU usage.|
| TiKV | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method) | Modified | Introduces a new value option `sm4-ctr`. When this configuration item is set to `sm4-ctr`, data is encrypted using SM4 before being stored. |
| TiKV | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630) | Newly added | Determines whether to recycle stale log files in Raft Engine. When it is enabled, logically purged log files will be reserved for recycling. This reduces the long tail latency on write workloads. This configuration item is only available when [format-version](/tikv-configuration-file.md#format-version-new-in-v630) is >= 2. |
| TiKV | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630) | Newly added | Specifies the version of log files in Raft Engine. The default log file version is `1` for TiKV earlier than v6.3.0. The log files can be read by TiKV >= v6.1.0. The default log file version is `2` for TiKV v6.3.0 and later. TiKV v6.3.0 and later can read the log files. |
| TiKV | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620) | Modified | Since v6.3.0, the default value changes from `false` to `true`. |
| TiKV | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620) | Modified | Since v6.3.0, the default value changes from `5min` to `3min`. |
| PD | [enable-diagnostic](/pd-configuration-file.md#enable-diagnostic-new-in-v630) | Newly added | Controls whether to enable the diagnostic feature. The default value is `false`. |
| TiFlash | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Deprecated | Since v6.3.0, this configuration item is deprecated. The thread pool is used to handle read requests from the storage engine by default and cannot be disabled. |
| DM | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Specifies the duration of the automatic safe mode. |
| TiCDC | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Specifies whether to enable the Syncpoint feature. |
| TiCDC | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots. |
| TiCDC | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) | Newly added | Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up. |
| TiCDC | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters) | Deprecated | The `memory` sorting is deprecated. It is not recommended to use it in any situation. |

### Others

* Log backup supports GCS and Azure Blob Storage as backup storage.
* Log backup is now compatible with the `exchange partition` DDL.
* The SQL statement `ALTER TABLE ...SET TiFLASH MODE ...` previously used for enabling [fastscan](/develop/dev-guide-use-fastscan.md) is deprecated, and replaced by the system variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630). When you upgrade from v6.2.0 to v6.3.0, all FastScan settings in v6.2.0 will become invalid, but will not affect the normal reading of data. In this case, you need to configure the variable [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) to enable or disable FastScan. When you upgrade from an earlier version to v6.3.0, the FastScan feature is not enabled by default for all sessions to keep data consistent.
* To deploy TiFlash under the Linux AMD64 architecture, the CPU must support the AVX2 instruction set. Ensure that `cat /proc/cpuinfo | grep avx2` has output. To deploy TiFlash under the Linux ARM64 architecture, the CPU must support the ARMv8 instruction set architecture. Ensure that `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'` has output. By using the instruction set extensions, TiFlash's vectorization engine can deliver better performance.
* The minimum version of HAProxy that works with TiDB is now v1.5. HAProxy versions between v1.5 and v2.1 now require the `post-41` configuration option to be set in `mysql-check`. It is recommended to use HAProxy v2.2 or newer.

## Removed feature

Since v6.3.0, TiCDC no longer supports configuring Pulsar sink. [kop](https://github.com/streamnative/kop) provided by StreamNative can be used as an alternative.

## Improvements

+ TiDB

    - TiDB is now case-insensitive to the target table name when checking the table existence [#34610](https://github.com/pingcap/tidb/issues/34610) @[tiancaiamao](https://github.com/tiancaiamao)
    - Improve MySQL compatibility by adding a parsing check when setting the value of `init_connect` [#35324](https://github.com/pingcap/tidb/issues/35324) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Improve the log warning generated for new connections [#34964](https://github.com/pingcap/tidb/issues/34964) @[xiongjiwei](https://github.com/xiongjiwei)
    - Optimize the HTTP API for querying DDL history jobs, and add support for the `start_job_id` parameter [#35838](https://github.com/pingcap/tidb/issues/35838) @[tiancaiamao](https://github.com/tiancaiamao)
    - Report errors when the JSON path has wrong syntax [#22525](https://github.com/pingcap/tidb/issues/22525) [#34959](https://github.com/pingcap/tidb/issues/34959) @[xiongjiwei](https://github.com/xiongjiwei)
    - Improve the performance of Join operations by fixing a false sharing issue [#37641](https://github.com/pingcap/tidb/issues/37641) @[gengliqi](https://github.com/gengliqi)
    - Support exporting the execution plan information of multiple SQL statements at a time using [`PLAN REPLAYER`](/sql-plan-replayer.md), which makes troubleshooting more efficient [#37798](https://github.com/pingcap/tidb/issues/37798) @[Yisaer](https://github.com/Yisaer)

+ TiKV

    - Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    - Improve the fault tolerance of TSO service [#12794](https://github.com/tikv/tikv/issues/12794) @[pingyu](https://github.com/pingyu)
    - Support dynamically modifying the number of sub-compaction operations performed concurrently in RocksDB (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)
    - Optimize the performance of merging empty Regions [#12421](https://github.com/tikv/tikv/issues/12421) @[tabokie](https://github.com/tabokie)
    - Support more regular expression functions [#13483](https://github.com/tikv/tikv/issues/13483) @[gengliqi](https://github.com/gengliqi)
    - Support automatically adjusting the thread pool size based on the CPU usage [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

+ PD

    - Improve the query of the TiKV IO MBps metric in TiDB Dashboard [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)
    - Modify the URL in TiDB Dashboard from `metrics` to `monitoring` [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)

+ TiFlash

    - Support pushing down the `elt` function to TiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @[Willendless](https://github.com/Willendless)
    - Support pushing down the `leftShift` function to TiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @[AnnieoftheStars](https://github.com/AnnieoftheStars)
    - Support pushing down the `castTimeAsDuration` function to TiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)
    - Support pushing down the `HexIntArg/HexStrArg` function to TiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107) @[YangKeao](https://github.com/YangKeao)
    - Refactor TiFlash's interpreter, and support the new interpreter Planner [#4739](https://github.com/pingcap/tiflash/issues/4739) @[SeaRise](https://github.com/SeaRise)
    - Improve the accuracy of memory tracker in TiFlash [#5609](https://github.com/pingcap/tiflash/issues/5609) @[bestwoody](https://github.com/bestwoody)
    - Improve the performance of string columns with the `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN` collations [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    - Calculate the I/O throughput in background in ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401), [#5091](https://github.com/pingcap/tiflash/issues/5091) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + Backup & Restore (BR)

        - PITR can merge small files generated in log backup, which greatly reduces the number of backup files [#13232](https://github.com/tikv/tikv/issues/13232) @[Leavrth](https://github.com/Leavrth)
        - PITR supports automatically configuring the number of TiFlash replicas based on the upstream cluster configuration after the restoration [#37208](https://github.com/pingcap/tidb/issues/37208) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Improve TiCDC's compatibility with the concurrent DDL framework introduced in the upstream TiDB [#6506](https://github.com/pingcap/tiflow/issues/6506) @[lance6716](https://github.com/lance6716)
        - Support logging `start ts` of DML statements when MySQL sink gets an error [#6460](https://github.com/pingcap/tiflow/issues/6460) @[overvenus](https://github.com/overvenus)
        - Enhance the `api/v1/health` API to return a more accurate health state of a TiCDC cluster [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus)
        - Implement MQ sink and MySQL sink in the asynchronous mode to improve the sink throughput [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu) @[hi-rustin](https://github.com/hi-rustin)
        - Delete the deprecated pulsar sink [#7087](https://github.com/pingcap/tiflow/issues/7087) @[hi-rustin](https://github.com/hi-rustin)
        - Improve replication performance by discarding DDL statements that are irrelevant to a changefeed [#6447](https://github.com/pingcap/tiflow/issues/6447) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Improve compatibility with MySQL 8.0 as data source [#6448](https://github.com/pingcap/tiflow/issues/6448) @[lance6716](https://github.com/lance6716)
        - Optimize DDL by executing DDL asynchronously when encounter "invalid connection" [#4689](https://github.com/pingcap/tiflow/issues/4689) @[lyzx2001](https://github.com/lyzx2001)

    + TiDB Lightning

        - Add query parameters for S3 external storage URL to support accessing the S3 data in another account by assuming a given role [#36891](https://github.com/pingcap/tidb/issues/36891) @[dsdashun](https://github.com/dsdashun)

## Bug fixes

+ TiDB

    - Fix the issue that the privilege check is skipped for `PREPARE` statements [#35784](https://github.com/pingcap/tidb/issues/35784) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the system variable `tidb_enable_noop_variable` can be set to `WARN` [#36647](https://github.com/pingcap/tidb/issues/36647) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that when an expression index is defined, the `ORDINAL_POSITION` column of the `INFORMAITON_SCHEMA.COLUMNS` table might be incorrect [#31200](https://github.com/pingcap/tidb/issues/31200) @[bb7133](https://github.com/bb7133)
    - Fix the issue that TiDB does not report an error when the timestamp is larger than `MAXINT32` [#31585](https://github.com/pingcap/tidb/issues/31585) @[bb7133](https://github.com/bb7133)
    - Fix the issue that TiDB server cannot be started when the enterprise plugin is used [#37319](https://github.com/pingcap/tidb/issues/37319) @[xhebox](https://github.com/xhebox)
    - Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
    - Fix the unexpected `EXCHANGE PARTITION` behaviors with temporary tables [#37201](https://github.com/pingcap/tidb/issues/37201) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that querying `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns an incorrect result @[zimulala](https://github.com/zimulala)
    - Fix the issue that the `EXPLAIN` query on views does not check privileges [#34326](https://github.com/pingcap/tidb/issues/34326) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that JSON `null` cannot be updated to `NULL` [#37852](https://github.com/pingcap/tidb/issues/37852) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `row_count` of DDL jobs is inaccurate [#25968](https://github.com/pingcap/tidb/issues/25968) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `FLASHBACK TABLE` does not work properly [#37386](https://github.com/pingcap/tidb/issues/37386) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue of failing to handle `prepared` statement flags in the typical MySQL protocol [#36731](https://github.com/pingcap/tidb/issues/36731) @[dveeden](https://github.com/dveeden)
    - Fix the issue of incorrect TiDB status that might appear on startup in some extreme cases [#36791](https://github.com/pingcap/tidb/issues/36791) @[xhebox](https://github.com/xhebox)
    - Fix the issue that `INFORMATION_SCHEMA.VARIABLES_INFO` does not comply with security enhanced mode (SEM) [#37586](https://github.com/pingcap/tidb/issues/37586) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that casting string to string goes wrong in queries with `UNION` [#31678](https://github.com/pingcap/tidb/issues/31678) @[cbcwestwolf](https://github.com/cbcwestwolf)
    - Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the cast and comparison between binary strings and JSON in TiDB are incompatible with MySQL [#31918](https://github.com/pingcap/tidb/issues/31918) [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `JSON_OBJECTAGG` and `JSON_ARRAYAGG` in TiDB are not compatible with MySQL on binary values [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the comparison between JSON opaque values causes panic [#37315](https://github.com/pingcap/tidb/issues/37315) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the single precision float cannot be used in JSON aggregation funtions [#37287](https://github.com/pingcap/tidb/issues/37287) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the result of the `castRealAsTime` expression is inconsistent with MySQL [#37462](https://github.com/pingcap/tidb/issues/37462) @[mengxin9014](https://github.com/mengxin9014)
    - Fix the issue that pessimistic DML operations lock non-unique index keys [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)
    - Fix the issue that `auto-commit` change affects transaction commit behaviours [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that the UPDATE statements incorrectly eliminate the projection in some cases, which causes the `Can't find column` error  [#37568](https://github.com/pingcap/tidb/issues/37568) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the Join Reorder operation will mistakenly push down its Outer Join condition [#37238](https://github.com/pingcap/tidb/issues/37238) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `IN` and `NOT IN` subqueries in some patterns report the `Can't find column` error [#37032](https://github.com/pingcap/tidb/issues/37032) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `Can't find column` is reported if an `UPDATE` statement contains common table expressions (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)
    - Fix incorrect `PromQL` [#35856](https://github.com/pingcap/tidb/issues/35856) @[Defined2014](https://github.com/Defined2014)

+ TiKV

    - Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that Regions might be overlapped if Raftstore is busy [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    - Fix the issue that the PD client might cause deadlocks [#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)
    - Fix the issue that TiKV might panic when encryption is disabled [#13081](https://github.com/tikv/tikv/issues/13081) @[jiayang-zheng](https://github.com/jiayang-zheng)
    - Fix the wrong expression of `Unified Read Pool CPU` in Dashboard [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    - Fix the issue that the TiKV service is unavailable for several minutes when a TiKV instance is in an isolated network environment [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)
    - Fix the issue that TiKV mistakenly reports a `PessimisticLockNotFound` error [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that PITR might cause data loss in some situations [#13281](https://github.com/tikv/tikv/issues/13281) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that causes checkpoint not advanced when there are some long pessimistic transactions [#13304](https://github.com/tikv/tikv/issues/13304) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV does not distinguish the datetime type (`DATETIME`, `DATE`, `TIMESTAMP` and `TIME`) and `STRING` type in JSON [#13417](https://github.com/tikv/tikv/issues/13417) @[YangKeao](https://github.com/YangKeao)
    - Fix incompatibility with MySQL of comparison between JSON bool and other JSON value [#13386](https://github.com/tikv/tikv/issues/13386) [#37481](https://github.com/pingcap/tidb/issues/37481) @[YangKeao](https://github.com/YangKeao)

+ PD

    - Fix PD panics caused by the issue that gRPC handles errors inappropriately when `enable-forwarding` is enabled [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that unhealthy Region might cause PD panic [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)
    - Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - Fix the issue that a window function might cause TiFlash to crash when the query is canceled [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that wrong data input for `CAST(value AS DATETIME)` causing high TiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that the result of `CAST(Real/Decimal AS time)` is inconsistent with MySQL [#3779](https://github.com/pingcap/tiflash/issues/3779) @[mengxin9014](https://github.com/mengxin9014)
    - Fix the issue that some obsolete data in storage cannot be deleted [#5570](https://github.com/pingcap/tiflash/issues/5570) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that page GC might block creating tables [#5697](https://github.com/pingcap/tiflash/issues/5697) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that might cause the information of the checkpoint being stale [#36423](https://github.com/pingcap/tidb/issues/36423) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - Fix the issue that might cause log backup checkpoint TS stuck when TiCDC exists in the cluster [#37822](https://github.com/pingcap/tidb/issues/37822) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469) [@MoCuishle28](https://github.com/MoCuishle28)

    + TiCDC

        - Fix the issue that TiCDC returns an inaccurate error for a wrong PD address with a grpc service [#6458](https://github.com/pingcap/tiflow/issues/6458) @[crelax](https://github.com/crelax)
        - Fix the issue that the `cdc cause cli changefeed list` command does not return failed changefeeds [#6334](https://github.com/pingcap/tiflow/issues/6334) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC is unavailable when changefeed initialization fails [#6859](https://github.com/pingcap/tiflow/issues/6859) @[asddongmen](https://github.com/asddongmen)

    + TiDB Binlog

        - Fix the issue that Drainer cannot send requests correctly to Pump when compressor is set to gzip [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Data Migration (DM)

        - Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315) @[lance6716](https://github.com/lance6716)
        - Fix goroutine leak when relay meets an error [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        - Fix the issue that when `collation_compatible` is set to `"strict"`, DM might generate SQL with duplicated collations [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        - Reduce the appearance of the warning message "found error when get timezone from binlog status_vars" in DM-worker log [#6628](https://github.com/pingcap/tiflow/issues/6628) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning does not support columns starting with slash, number, or non-ascii characters in Parquet files [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)

## Contributors

We would like to thank the following contributors from the TiDB community:

- @[An-DJ](https://github.com/An-DJ)
- @[AnnieoftheStars](https://github.com/AnnieoftheStars)
- @[AntiTopQuark](https://github.com/AntiTopQuark)
- @[blacktear23](https://github.com/blacktear23)
- @[BurtonQin](https://github.com/BurtonQin) (First-time contributor)
- @[crelax](https://github.com/crelax)
- @[eltociear](https://github.com/eltociear)
- @[fuzhe1989](https://github.com/fuzhe1989)
- @[erwadba](https://github.com/erwadba)
- @[jianzhiyao](https://github.com/jianzhiyao)
- @[joycse06](https://github.com/joycse06)
- @[morgo](https://github.com/morgo)
- @[onlyacat](https://github.com/onlyacat)
- @[peakji](https://github.com/peakji)
- @[rzrymiak](https://github.com/rzrymiak)
- @[tisonkun](https://github.com/tisonkun)
- @[whitekeepwork](https://github.com/whitekeepwork)
- @[Ziy1-Tan](https://github.com/Ziy1-Tan)
