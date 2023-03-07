---
title: TiDB 6.2.0 Release Notes
---

# TiDB 6.2.0 Release Notes

Release date: August 23, 2022

TiDB version: 6.2.0-DMR

> **Note:**
>
> The TiDB 6.2.0-DMR documentation has been [archived](https://docs-archive.pingcap.com/tidb/v6.2/). PingCAP encourages you to use [the latest LTS version](https://docs.pingcap.com/tidb/stable) of the TiDB database.

In v6.2.0-DMR, the key new features and improvements are as follows:

* TiDB Dashboard supports [visual execution plans](/dashboard/dashboard-slow-query.md#visual-execution-plans), allowing more intuitive display of execution plans.
* Add a [Monitoring page](/dashboard/dashboard-monitoring.md) in TiDB Dashboard to make the performance analysis and tuning more efficient.
* The [Lock View](/information-schema/information-schema-data-lock-waits.md) of TiDB feature supports showing the waiting information of optimistic transactions, facilitating quick locating of lock conflicts.
* TiFlash supports [a newer version of storage format](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file), enhancing stability and performance.
* The [Fine Grained Shuffle feature](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) allows parallel execution of window functions in multiple threads.
* A new concurrent DDL framework: Less DDL statements blocked and higher execution efficiency.
* TiKV supports [automatically tuning the CPU usage](/tikv-configuration-file.md#background-quota-limiter), thus ensuring stable and efficient database operations.
* [Point-in-time recovery (PITR)](/br/backup-and-restore-overview.md) is introduced to restore a snapshot of a TiDB cluster to a new cluster from any given time point in the past.
* TiDB Lightning supports [pausing the scheduling on the table level](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#pause-scheduling-on-the-table-level) in the physical import mode, instead of on the cluster level.
* BR supports [restoring user and privilege data](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema), making backup and restore smoother.
* TiCDC unlocks more data replication scenarios by supporting [filtering specific types of DDL events](/ticdc/ticdc-filter.md).
* The [`SAVEPOINT` mechanism](/sql-statements/sql-statement-savepoint.md) is supported, with which you can flexibly control the rollback points within a transaction.
* TiDB supports [adding, dropping, and modifying multiple columns or indexes with only one `ALTER TABLE` statement](/sql-statements/sql-statement-alter-table.md).
* [Cross-cluster RawKV replication](/tikv-configuration-file.md#api-version-new-in-v610) is now supported.

## New features

### SQL

* The physical data compaction feature is GA

    The TiFlash backend automatically compacts physical data based on specific conditions to reduce the backlog of useless data and optimize the data storage structure.

    There is often a certain amount of useless data in TiFlash tables before data compaction is automatically triggered. This feature lets you choose the right timing and manually execute SQL statements to immediately compact the physical data in TiFlash, thus reducing storage space usage and improving query performance. This feature is experimental in TiDB v6.1, and now is in General Availability (GA) in TiDB v6.2.0.

    [User document](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact) [#4145](https://github.com/pingcap/tiflash/issues/4145) @[breezewish](https://github.com/breezewish)

### Observability

* Split TiDB Dashboard from PD

    TiDB Dashboard is moved from PD to the monitoring node. This reduces the impact of TiDB Dashboard on PD and makes PD more stable.

    @[Hawkson-jee](https://github.com/Hawkson-jee)

* TiDB Dashboard adds a Monitoring page

    The new Monitoring page shows key indicators required for performance tuning, based on which you can analyze and tune performance with reference to [Performance tuning by database time](/performance-tuning-methods.md).

    Specifically, you can analyze user response time and database time from a global and top-down perspective, to confirm whether the bottleneck in user response time is caused by database issues. If the bottleneck is in the database, you can use the database time overview and SQL latency breakdowns to identify the bottleneck and tune performance.

    [User document](/dashboard/dashboard-monitoring.md) [#1381](https://github.com/pingcap/tidb-dashboard/issues/1381) @[YiniXu9506](https://github.com/YiniXu9506)

* TiDB Dashboard supports visual execution plans

    TiDB Dashboard provides visual execution plans and basic diagnosis service through the SQL Statements and Monitoring pages. This feature offers a fresh new perspective for you to identify each step of a query plan. Therefore, you can learn all traces of query execution plans more intuitively.

    This feature is particularly useful when you are trying to learn the execution of complex and large queries. Meanwhile, for each query execution plan, TiDB Dashboard automatically analyzes the execution details, spots potential problems, and provides optimization suggestions to reduce the time required for executing specific query plans.

    [User document](/dashboard/dashboard-slow-query.md#visual-execution-plans) [#1224](https://github.com/pingcap/tidb-dashboard/issues/1224) @[time-and-fate](https://github.com/time-and-fate)

* Lock View supports showing the waiting information of optimistic transactions

    Too many lock conflicts might cause serious performance problems, and detecting the lock conflicts is a necessary way to troubleshoot such problems. Before v6.2.0, TiDB supported viewing the lock conflict relationships using the `INFORMATION_SCHEMA.DATA_LOCK_WAITS` system view, but it does not show the waiting information of optimistic transactions. TiDB v6.2.0 extends the `DATA_LOCK_WAITS` view and lists the optimistic transactions blocked by pessimistic locks in the view. This feature helps users detect lock conflicts quickly, and provides a basis for improving the application, thus reducing the frequency of lock conflicts and improving the overall performance.

    [User document](/information-schema/information-schema-data-lock-waits.md) [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangsong](https://github.com/longfangsong)

### Performance

* Improve the `LEADING` optimizer hint to support outer join ordering

    In v6.1.0, the optimizer hint `LEADING` was introduced to modify the join order of tables. But this hint was not applicable to queries that contain outer joins. For more information, see [`LEADING` document](/optimizer-hints.md#leadingt1_name--tl_name-). In v6.2.0, TiDB lifts this restriction. In a query that contains outer join, now you can use this hint to specify the join order of tables to get better SQL execution performance and to avoid the sudden change of execution plans.

    [User document](/optimizer-hints.md#leadingt1_name--tl_name-) [#29932](https://github.com/pingcap/tidb/issues/29932) @[Reminiscent](https://github.com/Reminiscent)

* Add a new optimizer `SEMI_JOIN_REWRITE` to improve the performance of `EXISTS` queries

    In some scenarios, queries with `EXISTS` cannot have the optimal execution plan and might be executed for too long. In v6.2.0, the optimizer adds rewriting rules for such scenarios, and you can use `SEMI_JOIN_REWRITE` in queries to forcibly make the optimizer rewrite the query and get better query performance.

    [User document](/optimizer-hints.md#semi_join_rewrite) [#35323](https://github.com/pingcap/tidb/issues/35323) @[winoros](https://github.com/winoros)

* Add a new optimizer hint `MERGE` to improve the performance of analytical queries

    Common table expression (CTE) is an effective way to simplify the query logic. It is widely used to write complex queries. Before v6.2.0, CTE cannot be automatically expanded in TiFlash environments, which, to some extent, limits the execution efficiency of MPP. In v6.2.0, a MySQL-compatible optimizer hint `MERGE` is introduced. With this hint, the optimizer now allows CTE inlines to be expanded, so that the consumers of the CTE query results can concurrently execute the query in TiFlash, which improves the performance of some analytical queries.

    [User document](/optimizer-hints.md#merge) [#36122](https://github.com/pingcap/tidb/issues/36122) @[dayicklp](https://github.com/dayicklp)

* Optimize the performance of aggregation operations in some analytical scenarios

    When you use TiFlash to perform aggregation operations on a column in an OLAP scenario, if serious data skew exists due to uneven distribution of the aggregated column, and if the aggregated column has many different values, the execution efficiency of `COUNT(DISTINCT)` queries on the column is low. In v6.2.0, new rewriting rules are introduced to improve the performance of `COUNT(DISTINCT)` queries on a single column.

    [User document](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) [#36169](https://github.com/pingcap/tidb/issues/36169) @[fixdb](https://github.com/fixdb)

* TiDB supports concurrent DDL operations

    TiDB v6.2.0 introduces a new concurrent DDL framework, which enables DDL statements to be concurrently executed on different table objects and fixes the issue that DDL operations are blocked by DDL operations on other tables. In addition, TiDB supports concurrent DDL execution when adding an index on multiple tables or changing a column type. This improves the efficiency of DDL execution.

    [#32031](https://github.com/pingcap/tidb/issues/32031) @[wjhuang2016](https://github.com/wjhuang2016)

* Optimizer enhances the estimation of string matching

    In the string matching scenario, if the optimizer cannot accurately estimate the number of rows, it affects the generation of the optimal execution plan. For example, the condition is `like '%xyz'` or using a regular expression `regex ()`. To improve the estimation accuracy in such scenarios, TiDB v6.2.0 enhances the estimation method. The new method combines the TopN information of statistics and system variables to improve the accuracy and makes it possible to modify the match selectivity manually, thus improving the SQL performance.

    [User document](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) [#36209](https://github.com/pingcap/tidb/issues/36209) @[time-and-fate](https://github.com/time-and-fate)

* Window functions pushed down to TiFlash can be executed in multiple threads

    After the Fine Grained Shuffle feature is enabled, window functions can be executed in multiple threads, instead of in a single thread. This feature reduces the query response time significantly without changing user behavior. You can control the granularity of the shuffle by adjusting the value of the variables.

    [User document](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) [#4631](https://github.com/pingcap/tiflash/issues/4631) @[guo-shaoge](https://github.com/guo-shaoge)

* TiFlash supports a newer version of storage format

    The new storage format relieves high CPU usage caused by GC in high-concurrency and heavy workload scenarios. This significantly reduces IO traffic of background tasks, thereby boosting stability under high concurrencies and heavy workloads. At the same time, space amplification and disk waste can be significantly reduced.

    In TiDB v6.2.0, data is stored in the new storage format by default. Note that if TiFlash is upgraded from earlier versions to v6.2.0, you cannot perform in-place downgrade on TiFlash, because earlier TiFlash versions cannot recognize the new storage format.

    For more information about upgrading TiFlash, see [TiFlash v6.2.0 Upgrade Guide](/tiflash-620-upgrade-guide.md).

    [User document](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#3594](https://github.com/pingcap/tiflash/issues/3594) @[JaySon-Huang](https://github.com/JaySon-Huang) @[lidezhu](https://github.com/lidezhu) @[jiaqizho](https://github.com/jiaqizho)

* TiFlash optimizes data scanning performance in multiple concurrency scenarios (experimental)

    TiFlash reduces duplicate reads of the same data by merging read operations of the same data, and optimizes the resource overhead in the case of multiple concurrent tasks to improve data scanning performance. It avoids the situation where the same data has to be read separately in each task, or even the same data may be read multiple times at the same time, if the same data is involved in multiple concurrent tasks.

    [User document](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

* TiFlash adds FastScan for data scanning to increase read and write speed by sacrificing data consistency (experimental)

    TiDB introduces FastScan in v6.2.0. It supports skipping consistency checks to increase the speed significantly. FastScan is suitable for scenarios that do not require high accuracy and consistency of data such as offline analysis tasks. Previously, to ensure data consistency, TiFlash needed to perform data consistency checks during the data scanning process to find the required data from multiple different versions.

    When you upgrade from an earlier version to TiDB v6.2.0, FastScan is not enabled by default for all tables, which ensures data consistency. You can enable FastScan for each table independently. If the table is set to FastScan in TiDB v6.2.0, it will be disabled when you downgrade to a lower version, but this does not affect the normal data read. In this case, it is equivalent to strong consistency read.

    [User document](/develop/dev-guide-use-fastscan.md) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

### Stability

* TiKV supports automatically tuning the CPU usage (experimental)

    Databases usually have background processes to perform internal operations. Statistical information can be collected to help identify performance problems, generate better execution plans, and improve the stability and performance of the database. However, how to more efficiently collect information, and how to balance the resource overhead of background operations and foreground operations without affecting the daily use have always been one of the headaches in the database industry.

    Starting from v6.2.0, TiDB supports setting the CPU usage rate of background requests using the TiKV configuration file, thereby limiting the CPU usage ratio of background operations such as automatically collecting statistics in TiKV, and avoiding the resource preemption of user operations by background operations in extreme cases. This ensures that the operations of the database are stable and efficient.

    At the same time, TiDB also supports automatically adjusting CPU usage. Then, TiKV will adaptively adjust the CPU resources occupied by background requests according to the CPU usage of the instance. This feature is disabled by default.

    [User document](/tikv-configuration-file.md#background-quota-limiter) [#12503](https://github.com/tikv/tikv/issues/12503) @[BornChanger](https://github.com/BornChanger)

### Ease of use

* TiKV supports listing detailed configuration information using command-line flags

    The TiKV configuration file can be used to manage TiKV instances. However, for instances that run for a long time and are managed by different users, it is difficult to know which configuration item has been modified and what the default value is. This might cause confusion when you upgrade the cluster or migrate data. Since TiDB v6.2.0, tikv-server supports a new command-line flag [`—-config-info`](/command-line-flags-for-tikv-configuration.md#--config-info-format) that lists default and current values of all TiKV configuration items, helps users to quickly verify the startup parameters of the TiKV process, and improves usability.

    [User document](/command-line-flags-for-tikv-configuration.md#--config-info-format) [#12492](https://github.com/tikv/tikv/issues/12492) @[glorv](https://github.com/glorv)

### MySQL compatibility

* TiDB supports modifying multiple columns or indexes in a single `ALTER TABLE` statement

    Before v6.2.0, TiDB only supports single DDL changes, which leads to incompatible DDL operations when migrating heterogeneous databases, and it takes extra effort to modify a complex DDL statement into multiple TiDB-supported simple DDL statements. In addition, some users rely on the ORM framework to create assembly in SQL, thus causing SQL incompatibility. Since v6.2.0, TiDB supports modifying multiple schema objects in a single SQL statement, which is convenient for users to implement SQL and improves usability.

    [User document](/sql-statements/sql-statement-alter-table.md) [#14766](https://github.com/pingcap/tidb/issues/14766) @[tangenta](https://github.com/tangenta)

* Support setting savepoints in transactions

    A transaction is a logical collection of a series of consecutive operations with which the database guarantees ACID properties. In some complex application scenarios, you might need to manage many operations in a transaction, and sometimes you might need to roll back some operations in the transaction. "Savepoint" is a nameable mechanism for the internal implementation of transactions. With this mechanism, you can flexibly control the rollback points within a transaction, thereby managing the more complex transactions and having more freedom in designing diverse applications.

    [User document](/sql-statements/sql-statement-savepoint.md) [#6840](https://github.com/pingcap/tidb/issues/6840) @[crazycs520](https://github.com/crazycs520)

### Data migration

* BR supports restoring user and privilege data

    BR supports restoring user and privilege data when it performs a normal restoration. You do not need any additional restoration plan to restore user and privilege data. To enable this feature, specify the `--with-sys-table` parameter when you use BR to restore data.

    [User document](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema) [#35395](https://github.com/pingcap/tidb/issues/35395) @[D3Hunter](https://github.com/D3Hunter)

* Support point-in-time recovery (PITR) based on backup and restoration of log and snapshot

    PITR is implemented based on the backup and restoration of log and snapshot. It allows you to restore the snapshots of a cluster at any point in history to a new cluster. This feature satisfies the following needs:

    - Reduce the RPO in disaster recovery to less than 20 minutes.
    - Handle the cases of incorrect writes from applications by, for example, rolling back data to before the error event.
    - Perform history data auditing to meet the requirements of laws and regulations.

    This feature has usage limitations. For details, refer to the user document.

    [User document](/br/backup-and-restore-overview.md) [#29501](https://github.com/pingcap/tidb/issues/29501) @[joccau](https://github.com/joccau)

* DM supports continuous data validation (experimental)

    Continuous data validation is used to continuously compare the upstream binlog with the data written into the downstream during data migration. The validator identifies data exceptions, such as inconsistent data and missing records.

    This feature solves the issues of lagging validation and excessive resource consumption in common full data validation schemes.

    [User document](/dm/dm-continuous-data-validation.md) [#4426](https://github.com/pingcap/tiflow/issues/4426) @[D3Hunter](https://github.com/D3Hunter) @[buchuitoudegou](https://github.com/buchuitoudegou)

* Automatically identify the region of Amazon S3 buckets

    Data migration tasks can automatically identify the region of Amazon S3 buckets. You do not need to explicitly pass the region parameter.

    [#34275](https://github.com/pingcap/tidb/issues/34275) @[WangLe1321](https://github.com/WangLe1321)

* Support configuring disk quota for TiDB Lightning (experimental)

    When TiDB Lightning imports data in the physical import mode (backend='local'), sorted-kv-dir must have enough space to store the source data. Insufficient disk space might cause the import task to fail. Now you can use the new `disk_quota` configuration to limit the total amount of disk space used by TiDB Lightning, so that the import task can be completed normally even when sorted-kv-dir does not have enough storage space.

    [User document](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) [#446](https://github.com/pingcap/tidb-lightning/issues/446) @[buchuitoudegou](https://github.com/buchuitoudegou)

* TiDB Lightning supports importing data to production clusters in the physical import mode

    Previously, the physical import mode of TiDB Lightning (backend='local') had a significant impact on the target cluster. For example, during the migration, PD global scheduling is paused. Therefore, the previous physical import mode is only suitable for initial data import.

    TiDB Lightning improves the existing physical import mode. By allowing pausing the scheduling of tables, the impact of import is reduced from cluster level to table level. That is, you can read and write tables that are not being imported.

    This feature does not need manual configuration. If your TiDB cluster is v6.1.0 or later versions and TiDB Lightning is v6.2.0 or later versions, the new physical import mode takes effect automatically.

    [User document](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#pause-scheduling-on-the-table-level) [#35148](https://github.com/pingcap/tidb/issues/35148) @[gozssky](https://github.com/gozssky)

* Refactor the [user documentation of TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to make its structure more reasonable and clear. The terms for "backend" is also modified to lower the understanding barrier for new users:

    - Replace "local backend" with "physical import mode".
    - Replace "tidb backend" with "logical import mode".

### TiDB data share subscription

* Support cross-cluster RawKV replication (experimental)

    Support subscribing to the data change of RawKV and replicating the data change to a downstream TiKV cluster in real-time using a new component TiKV-CDC, which makes the cross-cluster replication possible.

    [User document](/tikv-configuration-file.md#api-version-new-in-v610) [#11965](https://github.com/tikv/tikv/issues/11965) @[pingyu](https://github.com/pingyu)

* Support filtering DDL and DML events

    In some special occasions, you might want to set filter rules for incremental data change logs. For example, filtering high risk DDL events such as DROP TABLE. Starting from v6.2.0, TiCDC supports filtering DDL events of specified types and filtering DML events based on SQL expressions. This makes TiCDC applicable to more data replication scenarios.

    [User document](/ticdc/ticdc-filter.md) [#6160](https://github.com/pingcap/tiflow/issues/6160) @[asddongmen](https://github.com/asddongmen)

## Compatibility changes

### System variables

| Variable name | Change type | Description |
| --- | --- | --- |
| [tidb_enable_new_cost_interface](/system-variables.md#tidb_enable_new_cost_interface-new-in-v620) | Newly added | This variable controls whether to enable the [refactored Cost Model implementation](/cost-model.md#cost-model-version-2). |
| [tidb_cost_model_version](/system-variables.md#tidb_cost_model_version-new-in-v620) | Newly added | TiDB uses a cost model to choose an index and operator during physical optimization. This variable is used to select the cost model version. TiDB v6.2.0 introduces the Cost Model Version 2, which is more accurate than the previous version in internal tests. |
| tidb_enable_concurrent_ddl | Newly added | This variable controls whether to allow TiDB to use concurrent DDL statements. DO NOT modify this variable. The risk of disabling this variable is unknown and might corrupt the metadata of the cluster. |
| [tiflash_fine_grained_shuffle_stream_count](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620) | Newly added | This variable controls the concurrency level of the window function execution When the window function is pushed down to TiFlash for execution. |
| [tiflash_fine_grained_shuffle_batch_size](/system-variables.md#tiflash_fine_grained_shuffle_batch_size-new-in-v620) | Newly added | When Fine Grained Shuffle is enabled, the window function pushed down to TiFlash can be executed in parallel. This variable controls the batch size of the data sent by the sender. The sender will send data once the cumulative number of rows exceeds this value. |
| [tidb_default_string_match_selectivity](/system-variables.md#tidb_default_string_match_selectivity-new-in-v620) | Newly added | This variable is used to set the default selectivity of `like`, `rlike`, and `regexp` functions in the filter condition when estimating the number of rows. This variable also controls whether to enable TopN to help estimate these functions. |
| [tidb_enable_analyze_snapshot](/system-variables.md#tidb_enable_analyze_snapshot-new-in-v620) | Newly added | This variable controls whether to read historical data or the latest data when performing `ANALYZE`. |
| [tidb_generate_binary_plan](/system-variables.md#tidb_generate_binary_plan-new-in-v620) | Newly added | This variable controls whether to generate binary-encoded execution plans in slow logs and statement summaries. |
| [tidb_opt_skew_distinct_agg](/system-variables.md#tidb_opt_skew_distinct_agg-new-in-v620) | Newly added | This variable sets whether the optimizer rewrites the aggregate functions with `DISTINCT` to the two-level aggregate functions, such as rewriting `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b` to `SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`. |
| [tidb_enable_noop_variables](/system-variables.md#tidb_enable_noop_variables-new-in-v620) | Newly added | This variable controls whether to show `noop` variables in the result of `SHOW [GLOBAL] VARIABLES`. |
| [tidb_min_paging_size](/system-variables.md#tidb_min_paging_size-new-in-v620) | Newly added | This variable is used to set the maximum number of rows during the coprocessor paging request process. |
| [tidb_txn_commit_batch_size](/system-variables.md#tidb_txn_commit_batch_size-new-in-v620) | Newly added | This variable is used to control the batch size of transaction commit requests that TiDB sends to TiKV. |
| tidb_enable_change_multi_schema | Deleted | This variable is used to control whether multiple columns or indexes can be altered in one `ALTER TABLE` statement. |
| [tidb_enable_outer_join_reorder](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) | Modified | This variable controls whether the Join Reorder algorithm of TiDB supports Outer Join. In v6.1.0, the default value is `ON`, which means the Join Reorder's support for Outer Join is enabled by default. From v6.2.0, the default value is `OFF`, which means the support is disabled by default. |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
| --- | --- | --- | --- |
| TiDB | feedback-probability | Deleted | This configuration is no longer effective and is not recommended. |
| TiDB | query-feedback-limit | Deleted | This configuration is no longer effective and is not recommended. |
| TiKV | [server.simplify-metrics](/tikv-configuration-file.md#simplify-metrics-new-in-v620) | Newly added | This configuration specifies whether to simplify the returned monitoring metrics. |
| TiKV | [quota.background-cpu-time](/tikv-configuration-file.md#background-cpu-time-new-in-v620) | Newly added | This configuration specifies the soft limit on the CPU resources used by TiKV background to process read and write requests. |
| TiKV | [quota.background-write-bandwidth](/tikv-configuration-file.md#background-write-bandwidth-new-in-v620) | Newly added | This configuration specifies the soft limit on the bandwidth with which background transactions write data (not effective currently). |
| TiKV | [quota.background-read-bandwidth](/tikv-configuration-file.md#background-read-bandwidth-new-in-v620) | Newly added | This configuration specifies the soft limit on the bandwidth with which background transactions and the Coprocessor read data (not effective currently). |
| TiKV | [quota.enable-auto-tune](/tikv-configuration-file.md#enable-auto-tune-new-in-v620) | Newly added | This configuration specifies whether to enable the auto-tuning of quota. If this configuration item is enabled, TiKV dynamically adjusts the quota for the background requests based on the load of TiKV instances. |
| TiKV | rocksdb.enable-pipelined-commit | Deleted | This configuration is no longer effective. |
| TiKV | gc-merge-rewrite | Deleted | This configuration is no longer effective. |
| TiKV | [log-backup.enable](/tikv-configuration-file.md#enable-new-in-v620) | Newly added | This configuration controls whether to enable log backup on TiKV. |
| TiKV | [log-backup.file-size-limit](/tikv-configuration-file.md#file-size-limit-new-in-v620) | Newly added | This configuration specifies the size limit on log backup data. Once this limit is reached, data is automatically flushed to external storage. |
| TiKV | [log-backup.initial-scan-pending-memory-quota](/tikv-configuration-file.md#initial-scan-pending-memory-quota-new-in-v620) | Newly added | This configuration specifies the quota of cache used for storing incremental scan data. |
| TiKV | [log-backup.max-flush-interval](/tikv-configuration-file.md#max-flush-interval-new-in-v620) | Newly added | This configuration specifies the maximum interval for writing backup data to external storage in log backup. |
| TiKV | [log-backup.initial-scan-rate-limit](/tikv-configuration-file.md#initial-scan-rate-limit-new-in-v620) | Newly added | This configuration specifies the rate limit on throughput in an incremental data scan in log backup. |
| TiKV | [log-backup.num-threads](/tikv-configuration-file.md#num-threads-new-in-v620) | Newly added | This configuration specifies the number of threads used in log backup. |
| TiKV | [log-backup.temp-path](/tikv-configuration-file.md#temp-path-new-in-v620) | Newly added | This configuration specifies temporary path to which log files are written before being flushed to external storage. |
| PD | replication-mode.dr-auto-sync.wait-async-timeout | Deleted | This configuration does not take effect and is deleted. |
| PD | replication-mode.dr-auto-sync.wait-sync-timeout | Deleted | This configuration does not take effect and is deleted. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | The default value of `format_version` changes to `4`, the default format for v6.2.0 and later versions, which reduces write amplification and background task resource consumption. |
| TiFlash | [profiles.default.dt_enable_read_thread](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | This configuration controls whether to use the thread pool to handle read requests from the storage engine. The default value is `false`. |
| TiFlash | [profiles.default.dt_page_gc_threshold](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | This configuration specifies the minimum ratio of valid data in a PageStorage data file. |
| TiCDC | [--overwrite-checkpoint-ts](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task) | Newly added | This configuration is added to the `cdc cli changefeed resume` sub-command. |
| TiCDC | [--no-confirm](/ticdc/ticdc-manage-changefeed.md#resume-a-replication-task) | Newly added | This configuration is added to the `cdc cli changefeed resume` sub-command.|
| DM | [mode](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | This configuration is a validator parameter. Optional values are `full`, `fast`, and `none`. The default value is `none`, which does not validate the data. |
| DM | [worker-count](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | This configuration is a validator parameter and specifies the number of validation workers in the background. The default value is `4`. |
| DM | [row-error-delay](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | This configuration is a validator parameter. If a row is not validated within the specified time, it will be marked as an error row. The default value is 30m, which means 30 minutes. |
| TiDB Lightning | [tikv-importer.store-write-bwlimit](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task) | Newly added | This configuration determines the write bandwidth when TiDB Lightning writes data to each TiKV Store. The default value is `0`, indicating the bandwidth is not limited. |
| TiDB Lightning | [tikv-importer.disk-quota](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#configure-disk-quota-new-in-v620) | Newly added | This configuration limits the storage space used by TiDB Lightning. |

### Others

- TiFlash `format_version` cannot be downgraded from `4` to `3`. For details, see [TiFlash v6.2.0 Upgrade Guide](/tiflash-620-upgrade-guide.md).
- In v6.2.0 and later versions, it is strongly recommended to keep the default value `false` of `dt_enable_logical_split` and not to change it to `true`. For details, see known issue [#5576](https://github.com/pingcap/tiflash/issues/5576).
- If the backup cluster has a TiFlash replica, after you perform PITR, the restoration cluster does not contain the data in the TiFlash replica. To restore data from the TiFlash replica, you need to manually configure TiFlash replicas. Executing the `exchange partition` DDL statement might result in a failure of PITR. If the upstream database uses TiDB Lightning's physical import mode to import data, the data cannot be backed up in log backup. It is recommended to perform a full backup after the data import. For other compatibility issues of PITR, see [PITR limitations](/br/backup-and-restore-overview.md#before-you-use).
- Since TiDB v6.2.0, you can restore table in `mysql` schema by specifying the parameter `--with-sys-table=true` when restoring data.
- When you execute the `ALTER TABLE` statement to add, drop, or modify multiple columns or indexes, TiDB checks table consistency by comparing the table before and after statement execution, regardless of the change in the same DDL statement. The execution order of the DDLs is not fully compatible with MySQL in some scenarios.
- If the TiDB component is v6.2.0 or later, the TiKV component should not be earlier than v6.2.0.
- TiKV adds a configuration item `split.region-cpu-overload-threshold-ratio` that supports [dynamic configuration](/dynamic-config.md#modify-tikv-configuration-dynamically).
- Slow query logs, `information_schema.statements_summary`, and `information_schema.slow_query`can export `binary_plan`, or execution plans encoded in the binary format.
- Two columns are added to the `SHOW TABLE ... REGIONS` statement: `SCHEDULING_CONSTRAINTS` and `SCHEDULING_STATE`, which respectively indicate Region scheduling constraints in Placement in SQL and the current scheduling state.
- Since TiDB v6.2.0, you can capture data changes of RawKV via [TiKV-CDC](https://github.com/tikv/migration/tree/main/cdc).
- When `ROLLBACK TO SAVEPOINT` is used to roll back a transaction to a specified savepoint, MySQL releases the locks held only after the specified savepoint, while in TiDB pessimistic transaction, TiDB does not immediately release the locks held after the specified savepoint. Instead, TiDB releases all locks when the transaction is committed or rolled back.
- Since TiDB v6.2.0, the `SELECT tidb_version()` statement also returns Store type (tikv or unistore).
- TiDB no longer has hidden system variables.
- TiDB v6.2.0 introduces two new system tables:
    - `INFORMATION_SCHEMA.VARIABLES_INFO`: used for viewing information about TiDB system variables.
    - `PERFORMANCE_SCHEMA.SESSION_VARIABLES`: used for viewing information about TiDB session-level system variables.

## Removed feature

Since TiDB v6.2.0, backing up and restoring RawKV using BR is deprecated.

## Improvements

+ TiDB

    - Support the `SHOW COUNT(*) WARNINGS` and `SHOW COUNT(*) ERRORS` statements [#25068](https://github.com/pingcap/tidb/issues/25068) @[likzn](https://github.com/likzn)
    - Add validation check for some system variables [#35048](https://github.com/pingcap/tidb/issues/35048) @[morgo](https://github.com/morgo)
    - Optimize the error messages for some type conversions [#32447](https://github.com/pingcap/tidb/issues/32744) @[fanrenhoo](https://github.com/fanrenhoo)
    - The `KILL` command now supports DDL operations [#24144](https://github.com/pingcap/tidb/issues/24144) @[morgo](https://github.com/morgo)
    - Make the output of `SHOW TABLES/DATABASES LIKE …` more MySQL-compatible. The column names in the output contain the `LIKE` value [#35116](https://github.com/pingcap/tidb/issues/35116) @[likzn](https://github.com/likzn)
    - Improve the performance of JSON-related functions [#35859](https://github.com/pingcap/tidb/issues/35859) @[wjhuang2016](https://github.com/wjhuang2016)
    - Improve the verification speed of password login using SHA-2 [#35998](https://github.com/pingcap/tidb/issues/35998) @[virusdefender](https://github.com/virusdefender)
    - Simplify some log outputs [#36011](https://github.com/pingcap/tidb/issues/36011) @[dveeden](https://github.com/dveeden)
    - Optimize the Coprocessor communication protocol. This can greatly reduce the memory consumption of the TiDB processes when reading data, and further alleviate the OOM issue in the scenario of scanning tables and exporting data by Dumpling. The system variable `tidb_enable_paging` is introduced to control whether to enable this communication protocol (with the scope of SESSION or GLOBAL). This protocol is disabled by default. To enable it, set the variable value to `true` [#35633](https://github.com/pingcap/tidb/issues/35633) @[tiancaiama](https://github.com/tiancaiamao) @[wshwsh12](https://github.com/wshwsh12)
    - Optimize the accuracy of memory tracking for some operators (HashJoin, HashAgg, Update, Delete) ([#35634](https://github.com/pingcap/tidb/issues/35634), [#35631](https://github.com/pingcap/tidb/issues/35631), [#35635](https://github.com/pingcap/tidb/issues/35635) @[wshwsh12](https://github.com/wshwsh12)) ([#34096](https://github.com/pingcap/tidb/issues/34096) @[ekexium](https://github.com/ekexium))

    - The system table `INFORMATION_SCHEMA.DATA_LOCK_WAIT` supports recording the locking information of optimistic transactions [#34609](https://github.com/pingcap/tidb/issues/34609) @[longfangson](https://github.com/longfangsong)
    - Add some monitoring metrics for transactions [#34456](https://github.com/pingcap/tidb/issues/34456) @[longfangsong](https://github.com/longfangsong)

+ TiKV

    - Support compressing the metrics response using gzip to reduce the HTTP body size [#12355](https://github.com/tikv/tikv/issues/12355) @[glorv](https://github.com/glorv)
    - Improve the readability of the TiKV panel in Grafana Dashboard [#12007](https://github.com/tikv/tikv/issues/12007) @[kevin-xianliu](https://github.com/kevin-xianliu)
    - Optimize the commit pipeline performance of the Apply operator [#12898](https://github.com/tikv/tikv/issues/12898) @[ethercflow](https://github.com/ethercflow)
    - Support dynamically modifying the number of sub-compaction operations performed concurrently in RocksDB (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)

+ PD

    - Support the statistical dimension of CPU usage of a Region and enhance the usage scenarios of Load Base Split [#12063](https://github.com/tikv/tikv/issues/12063) @[Jmpotato](https://github.com/JmPotato)

+ TiFlash

    - Refine error handling of the TiFlash MPP engine, thereby enhancing stability [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker) @[yibin87](https://github.com/yibin87)

    - Optimize the comparison and sorting of UTF8_BIN and UTF8MB4_BIN collations [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)

+ Tools

    - Backup & Restore (BR)

        - Adjust the backup data directory structure to fix backup failure caused by S3 rate limiting in large cluster backup [#30087](https://github.com/pingcap/tidb/issues/30087) @[MoCuishle28](https://github.com/MoCuishle28)

    - TiCDC

        - Reduce performance overhead caused by runtime context switching in multi-Region scenarios [#5610](https://github.com/pingcap/tiflow/issues/5610) @[hicqu](https://github.com/hicqu)

        - Optimize redo log performance, and fix meta and data inconsistency problems ([#6011](https://github.com/pingcap/tiflow/issues/6011) @[CharlesCheung96](https://github.com/CharlesCheung96)) ([#5924](https://github.com/pingcap/tiflow/issues/5924) @[zhaoxinyu](https://github.com/zhaoxinyu)) ([#6277](https://github.com/pingcap/tiflow/issues/6277) @[hicqu](https://github.com/hicqu))

    - TiDB Lightning

        - Add more retryable errors, including EOF, Read index not ready, and Coprocessor timeout [#36674](https://github.com/pingcap/tidb/issues/36674), [#36566](https://github.com/pingcap/tidb/issues/36566) @[D3Hunter](https://github.com/D3Hunter)

    - TiUP

        - When a new cluster is deployed using TiUP, node-exporter will use the [1.3.1](https://github.com/prometheus/node_exporter/releases/tag/v1.3.1) version, and blackbox-exporter will use the [0.21.1](https://github.com/prometheus/blackbox_exporter/releases/tag/v0.21.1) version, which ensures successful deployment in different systems and environments

## Bug fixes

+ TiDB

    - Fix the issue that a partition is incorrectly pruned if a partition key is used in the query condition and the collate is different from the one in the query partition table [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - Fix the issue that `SET ROLE` cannot match the granted role if there are capital letters in the host [#33061](https://github.com/pingcap/tidb/issues/33061) @[morgo](https://github.com/morgo)
    - Fix the issue that columns with `auto_increment` cannot be dropped [#34891](https://github.com/pingcap/tidb/issues/34891) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `SHOW CONFIG` shows some configuration items that have been removed [#34867](https://github.com/pingcap/tidb/issues/34867) @[morgo](https://github.com/morgo)
    - Fix the issue that `SHOW DATABASES LIKE …` is case-sensitive [#34766](https://github.com/pingcap/tidb/issues/34766) @[e1ijah1](https://github.com/e1ijah1)
    - Fix the issue that `SHOW TABLE STATUS LIKE ...` is case-sensitive [#7518](https://github.com/pingcap/tidb/issues/7518) @[likzn](https://github.com/likzn)
    - Fix the issue that `max-index-length` still reports an error in non-strict mode [#34931](https://github.com/pingcap/tidb/issues/34931) @[e1ijah1](https://github.com/e1ijah1)
    - Fix the issue that `ALTER COLUMN ... DROP DEFAULT` does not work [#35018](https://github.com/pingcap/tidb/issues/35018) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that when you create a table, the default value and the type of a column are not consistent and are not automatically corrected [#34881](https://github.com/pingcap/tidb/issues/34881) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that data in the `mysql.columns_priv` table is not deleted synchronously after you run `DROP USER` [#35059](https://github.com/pingcap/tidb/issues/35059) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue of DDL jam by disallowing creating tables within the schemas of some systems [#35205](https://github.com/pingcap/tidb/issues/35205) @[tangenta](https://github.com/tangenta)
    - Fix the issue that querying partitioned tables might report "index-out-of-range" and "non used index" errors in some cases [#35181](https://github.com/pingcap/tidb/issues/35181) @[mjonss](https://github.com/mjonss)
    - Fix the issue that `INTERVAL expr unit + expr` might report an error [#30253](https://github.com/pingcap/tidb/issues/30253) @[mjonss](https://github.com/mjonss)
    - Fix a bug that a temporary table cannot be found after being created in a transaction [#35644](https://github.com/pingcap/tidb/issues/35644) @[djshow832](https://github.com/djshow832)
    - Fix the panic issue that occurs when setting collation to the `ENUM` column [#31637](https://github.com/pingcap/tidb/issues/31637) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that when one PD node goes down, the query of `information_schema.TIKV_REGION_STATUS` fails due to not retrying other PD nodes [#35708](https://github.com/pingcap/tidb/issues/35708) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `SHOW CREATE TABLE …` cannot correctly display set or `ENUM` columns after `SET character_set_results = GBK` [#31338](https://github.com/pingcap/tidb/issues/31338) @[tangenta](https://github.com/tangenta)
    - Fix the incorrect scope of the system variables `tidb_log_file_max_days` and `tidb_config` [#35190](https://github.com/pingcap/tidb/issues/35190) @[morgo](https://github.com/morgo)
    - Fix the issue that the output of `SHOW CREATE TABLE` is not compatible with MySQL for the `ENUM` or `SET` column [#36317](https://github.com/pingcap/tidb/issues/36317) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that when creating a table, the behavior of a `LONG BYTE` column is not compatible with MySQL [#36239](https://github.com/pingcap/tidb/issues/36239) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that `auto_increment = x` does not take effect on temporary tables [#36224](https://github.com/pingcap/tidb/issues/36224) @[djshow832](https://github.com/djshow832)
    - Fix the wrong default value when modifying columns concurrently [#35846](https://github.com/pingcap/tidb/issues/35846) @[wjhuang2016](https://github.com/wjhuang2016)
    - Avoid sending requests to unhealthy TiKV nodes to improve availability [#34906](https://github.com/pingcap/tidb/issues/34906) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that the column list does not work in the LOAD DATA statement [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that in some scenarios the pessimistic lock is incorrectly added to the non-unique secondary index [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

+ TiKV

    - Avoid reporting `WriteConflict` errors in pessimistic transactions [#11612](https://github.com/tikv/tikv/issues/11612) @[sticnarf](https://github.com/sticnarf)
    - Fix the possible duplicate commit records in pessimistic transactions when async commit is enabled [#12615](https://github.com/tikv/tikv/issues/12615) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that TiKV panics when modifying the `storage.api-version` from `1` to `2` [#12600](https://github.com/tikv/tikv/issues/12600) @[pingyu](https://github.com/pingyu)
    - Fix the issue of inconsistent Region size configuration between TiKV and PD [#12518](https://github.com/tikv/tikv/issues/12518) @[5kbpers](https://github.com/5kbpers)
    - Fix the issue that TiKV keeps reconnecting PD clients [#12506](https://github.com/tikv/tikv/issues/12506), [#12827](https://github.com/tikv/tikv/issues/12827) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue of time parsing error that occurs when the `DATETIME` values contain a fraction and `Z` [#12739](https://github.com/tikv/tikv/issues/12739) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the perf context written by the Apply operator to TiKV RocksDB is coarse-grained [#11044](https://github.com/tikv/tikv/issues/11044) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that TiKV fails to start when the configuration of [backup](/tikv-configuration-file.md#backup)/[import](/tikv-configuration-file.md#import)/[cdc](/tikv-configuration-file.md#cdc) is invalid [#12771](https://github.com/tikv/tikv/issues/12771) @[3pointer](https://github.com/3pointer)
    - Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    - Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    - Fix the panic issue caused by analyzing statistics when `max_sample_size` is set to `0` [#11192](https://github.com/tikv/tikv/issues/11192) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix the issue that encryption keys are not cleaned up when Raft Engine is enabled [#12890](https://github.com/tikv/tikv/issues/12890) @[tabokie](https://github.com/tabokie)
    - Fix the issue that the `get_valid_int_prefix` function is incompatible with TiDB. For example, the `FLOAT` type was incorrectly converted to `INT` [#13045](https://github.com/tikv/tikv/issues/13045) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the Commit Log Duration of a new Region is too high, which causes QPS to drop [#13077](https://github.com/tikv/tikv/issues/13077) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that BR does not reset the rate limit after finishing a rate-limited backup task [#31722](https://github.com/pingcap/tidb/issues/31722) @[MoCuishle28](https://github.com/MoCuishle28)

## Contributors

We would like to thank the following contributors from the TiDB community:

- [e1ijah1](https://github.com/e1ijah1)
- [PrajwalBorkar](https://github.com/PrajwalBorkar)
- [likzn](https://github.com/likzn)
- [rahulk789](https://github.com/rahulk789)
- [virusdefender](https://github.com/virusdefender)
- [joycse06](https://github.com/joycse06)
- [morgo](https://github.com/morgo)
- [ixuh12](https://github.com/ixuh12)
- [blacktear23](https://github.com/blacktear23)
- [johnhaxx7](https://github.com/johnhaxx7)
- [GoGim1](https://github.com/GoGim1)
- [renbaoshuo](https://github.com/renbaoshuo)
- [Zheaoli](https://github.com/Zheaoli)
- [fanrenhoo](https://github.com/fanrenhoo)
- [njuwelkin](https://github.com/njuwelkin)
- [wirybeaver](https://github.com/wirybeaver)
- [hey-kong](https://github.com/hey-kong)
- [fatelei](https://github.com/fatelei)
- [eastfisher](https://github.com/eastfisher): First-time contributor
- [Juneezee](https://github.com/Juneezee): First-time contributor
