---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 Release Notes

Release date: April 7, 2022

TiDB version: 6.0.0-DMR

> **Note:**
>
> The TiDB 6.0.0-DMR documentation has been [archived](https://docs-archive.pingcap.com/tidb/v6.0/). PingCAP encourages you to use [the latest LTS version](https://docs.pingcap.com/tidb/stable) of the TiDB database.

In 6.0.0-DMR, the key new features or improvements are as follows:

- Support placement rules in SQL to provide more flexible management for data placement.
- Add a consistency check between data and indexes at the kernel level, which improves system stability and robustness, with only very low resource overhead.
- Provide Top SQL, a self-serving database performance monitoring and diagnosis feature for non-experts.
- Support Continuous Profiling that collects cluster performance data all the time, reducing MTTR for technical experts.
- Cache hotspot small tables in memory, which greatly improves the access performance, improves the throughput and reduces access latency.
- Optimize in-memory pessimistic locking. Under the performance bottleneck caused by pessimistic locks, memory optimization for pessimistic locks can effectively reduce latency by 10% and increase QPS by 10%.
- Enhance prepared statements to share execution plans, which lessens CPU resource consumption and improves SQL execution efficiency.
- Improve the computing performance of the MPP engine by supporting pushing down more expressions and the general availability (GA) of the elastic thread pool.
- Add DM WebUI to facilitate managing a large number of migration tasks.
- Improve the stability and efficiency of TiCDC when replicating data in large clusters. TiCDC now supports replicating 100,000 tables simultaneously.
- Accelerate leader balancing after restarting TiKV nodes, which improves the speed of business recovery after a restart.
- Support canceling the automatic update of statistics, which reduces resource contention and limits the impact on SQL performance.
- Provide PingCAP Clinic, an automatic diagnosis service for TiDB clusters (Technical Preview version).
- Provide TiDB Enterprise Manager, an enterprise-level database management platform.

Also, as a core component of TiDB's HTAP solution, TiFlash<sup>TM</sup> is officially open source in this release. For details, see [TiFlash repository](https://github.com/pingcap/tiflash).

## Release strategy changes

Starting from TiDB v6.0.0, TiDB provides two types of releases:

- Long-Term Support Releases

    Long-Term Support (LTS) releases are released approximately every six months. An LTS release introduces new features and improvements, and accepts patch releases within its release lifecycle. For example, v6.1.0 will be an LTS release.

- Development Milestone Releases

    Development Milestone Releases (DMR) are released approximately every two months. A DMR introduces new features and improvements, but does not accept patch releases. It is not recommended for on-premises users to use DMR in production environments. For example, v6.0.0-DMR is a DMR.

TiDB v6.0.0 is a DMR, and its version is 6.0.0-DMR.

## New features

### SQL

- SQL-based placement rules for data

    TiDB is a distributed database with excellent scalability. Usually, data is deployed across multiple servers or even multiple data centers. Therefore, data scheduling management is one of the most important basic capabilities of TiDB. In most cases, users do not need to care about how to schedule and manage data. However, with the increasing application complexity, deployment changes caused by isolation and access latency have become new challenges for TiDB. Since v6.0.0, TiDB officially provides data scheduling and management capabilities based on SQL interfaces. It supports flexible scheduling and management in dimensions such as replica counts, role types, and placement locations for any data. TiDB also supports more flexible management for data placement in multi-service shared clusters and cross-AZ deployments.

    [User document](/placement-rules-in-sql.md)

- Support building TiFlash replicas by databases. To add TiFlash replicas for all tables in a database, you only need to use a single SQL statement, which greatly saves operation and maintenance costs.

    [User document](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### Transaction

- Add a check for data index consistency at the kernel level

    Add a check for data index consistency when a transaction is executed, which improves system stability and robustness, with only very low resource overhead. You can control the check behavior using the `tidb_enable_mutation_checker` and `tidb_txn_assertion_level` variables. With the default configuration, the QPS drop is controlled within 2% in most scenarios. For the error description of the consistency check, see [user document](/troubleshoot-data-inconsistency-errors.md).

### Observability

- Top SQL: Performance diagnosis for non-experts

    Top SQL is a self-serving database performance monitoring and diagnosis feature in TiDB Dashboard, for DBAs and App developers, which is now generally available in TiDB v6.0.

    Unlike existing diagnostic features for experts, Top SQL is designed for non-experts: you do not need to traverse thousands of monitoring charts to find correlations or understand TiDB internal mechanisms such as Raft Snapshot, RocksDB, MVCC, and TSO. To use Top SQL for analyzing database load quickly and improving App performance, only basic database knowledge (such as index, lock conflict, and execution plans) is needed.

    Top SQL is not enabled by default. When enabled, Top SQL provides you with the real-time CPU load of each TiKV or TiDB node. Therefore, you can spot SQL statements consuming high CPU loads at first glimpse, and quickly analyze the issues such as database hotspots and sudden load increases. For example, you can use Top SQL to pinpoint and diagnose an unusual query that consumes 90% CPU of a single TiKV node.

    [User documentation](/dashboard/top-sql.md)

- Support Continuous Profiling

    TiDB Dashboard introduces the Continuous Profiling feature, which is now generally available in TiDB v6.0. Continuous profiling is not enabled by default. When enabled, the performance data of individual TiDB, TiKV, and PD instances will be collected all the time, with negligible overhead. With history performance data, technical experts can backtrack and pinpoint the root causes of issues like high memory consumption, even when the issues are difficult to reproduce. In this way, the mean time to recovery (MTTR) can be reduced.

    [User document](/dashboard/continuous-profiling.md)

### Performance

- Cache hotspot small tables

    For user applications in scenarios where hotspot small tables are accessed, TiDB supports explicitly caching the hotspot tables in memory, which greatly improves the access performance, improves the throughput, and reduces access latency. This solution can effectively avoid introducing a third-party cache middleware, reduce the complexity of the architecture, and cut the cost of operation and maintenance. The solution is suitable for scenarios where small tables are frequently accessed but rarely updated, such as the configuration tables or exchange rate tables.

    [User document](/cached-tables.md), [#25293](https://github.com/pingcap/tidb/issues/25293)

- In-memory pessimistic locking

    Since TiDB v6.0.0, in-memory pessimistic locking is enabled by default. After enabling this feature, pessimistic transaction locks are managed in memory. This avoids persisting pessimistic locks and the Raft replication of the lock information, and greatly reduces the overhead of managing pessimistic transaction locks. Under the performance bottleneck caused by pessimistic locks, memory optimization for pessimistic locks can effectively reduce latency by 10% and increase QPS by 10%.

    [User document](/pessimistic-transaction.md#in-memory-pessimistic-lock), [#11452](https://github.com/tikv/tikv/issues/11452)

- Optimization to get TSO at the Read Committed isolation level

    To reduce query latency, when read-write conflicts are rare, TiDB adds the `tidb_rc_read_check_ts` system variable at the [Read Committed isolation level](/transaction-isolation-levels.md#read-committed-isolation-level) to get less unnecessary TSO. This variable is disabled by default. When the variable is enabled, this optimization avoids getting duplicated TSO to reduce latency in scenarios where there is no read-write conflict. However, in scenarios with frequent read-write conflicts, enabling this variable might cause a performance regression.

    [User document](/transaction-isolation-levels.md#read-committed-isolation-level), [#33159](https://github.com/pingcap/tidb/issues/33159)

- Enhance prepared statements to share execution plans

    Reusing SQL execution plans can effectively reduce the time for parsing SQL statements, lessen CPU resource consumption, and improve SQL execution efficiency. One of the important methods of SQL tuning is to reuse SQL execution plans effectively. TiDB has supported sharing execution plans with prepared statements. However, when the prepared statements are closed, TiDB automatically clears the corresponding plan cache. After that, TiDB might unnecessarily parse the repeated SQL statements, affecting the execution efficiency. Since v6.0.0, TiDB supports controlling whether to ignore the `COM_STMT_CLOSE` command through the `tidb_ignore_prepared_cache_close_stmt` parameter (disabled by default). When the parameter is enabled, TiDB ignores the command of closing prepared statements and keeps the execution plan in the cache, improving the reuse rate of the execution plan.

    [User document](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement), [#31056](https://github.com/pingcap/tidb/issues/31056)

- Improve query pushdown

    With its native architecture of separating computing from storage, TiDB supports filtering out invalid data by pushing down operators, which greatly reduces the data transmission between TiDB and TiKV and thereby improves the query efficiency. In v6.0.0, TiDB supports pushing down more expressions and the `BIT` data type to TiKV, improving the query efficiency when computing the expressions and data type.

    [User document](/functions-and-operators/expressions-pushed-down.md#add-to-the-blocklist), [#30738](https://github.com/pingcap/tidb/issues/30738)

- Optimization of hotspot index

    Writing monotonically increasing data in batches to the secondary index causes an index hotspot and affects the overall write throughput. Since v6.0.0, TiDB supports scattering the index hotspot using the `tidb_shard` function to improve the write performance. Currently, `tidb_shard` only takes effect on the unique secondary index. This application-friendly solution does not require modifying the original query conditions. You can use this solution in the scenarios of high write throughput, point queries, and batch point queries. Note that using the data that has been scattered by range queries in the application might cause a performance regression. Therefore, do not use this function in such cases without verification.

    [User document](/functions-and-operators/tidb-functions.md#tidb_shard), [#31040](https://github.com/pingcap/tidb/issues/31040)

- Support dynamic pruning mode for partitioned tables in TiFlash MPP engine (experimental)

    In this mode, TiDB can read and compute the data on partitioned tables using the MPP engine of TiFlash, which greatly improves the query performance of partitioned tables.

    [User document](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

- Improve the computing performance of the MPP engine

    - Support pushing down more functions and operators to the MPP engine

        - Logical functions: `IS`, `IS NOT`
        - String functions: `REGEXP()`, `NOT REGEXP()`
        - Mathematical functions: `GREATEST(int/real)`, `LEAST(int/real)`
        - Date functions: `DAYNAME()`, `DAYOFMONTH()`, `DAYOFWEEK()`, `DAYOFYEAR()`, `LAST_DAY()`, `MONTHNAME()`
        - Operators: Anti Left Outer Semi Join, Left Outer Semi Join

        [User document](/tiflash/tiflash-supported-pushdown-calculations.md)

    - The elastic thread pool (enabled by default) becomes GA. This feature aims to improve CPU utilization.

        [User document](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### Stability

- Enhance baseline capturing of execution plans

    Enhance the usability of baseline capturing of execution plans by adding a blocklist with such dimensions as table name, frequency, and user name. Introduce a new algorithm to optimize memory management for caching bindings. After baseline capturing is enabled, the system automatically creates bindings for most OLTP queries. Execution plans of bound statements are fixed, avoiding performance problems due to any change in the execution plans. Baseline capturing is applicable to scenarios such as major version upgrades and cluster migration, and helps reduce performance problems caused by regression of execution plans.

    [User document](/sql-plan-management.md#baseline-capturing), [#32466](https://github.com/pingcap/tidb/issues/32466)

- Support TiKV quota limiter (experimental)

    If your machine deployed with TiKV has limited resources and the foreground is burdened by an excessively large amount of requests, background CPU resources are occupied by the foreground, causing TiKV performance unstable. In TiDB v6.0.0, you can use the quota-related configuration items to limit the resources used by the foreground, including CPU and read/write bandwidth. This greatly improves stability of clusters under long-term heavy workloads.

    [User document](/tikv-configuration-file.md#quota), [#12131](https://github.com/tikv/tikv/issues/12131)

- Support the zstd compression algorithm in TiFlash

    TiFlash introduces two parameters, `profiles.default.dt_compression_method` and `profiles.default.dt_compression_level`, which allow users to select the optimal compression algorithm based on performance and capacity balance.

    [User document](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

- Enable all I/O checks (Checksum) by default

    This feature was introduced in v5.4.0 as experimental. It enhances data accuracy and security without imposing an obvious impact on users' businesses.

    Warning: Newer version of data format cannot be downgraded in place to versions earlier than v5.4.0. During such a downgrade, you need to delete TiFlash replicas and replicate data after the downgrade. Alternatively, you can perform a downgrade by referring to [dttool migrate](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

    [User document](/tiflash/tiflash-data-validation.md)

- Improve thread utilization

    TiFlash introduces asynchronous gRPC and Min-TSO scheduling mechanisms. Such mechanisms ensure more efficient use of threads and avoid system crashes caused by excessive threads.

    [User document](/tiflash/monitor-tiflash.md#coprocessor)

### Data migration

#### TiDB Data Migration (DM)

- Add WebUI (experimental)

    With the WebUI, you can easily manage a large number of migration tasks. On the WebUI, you can:

    - View migration tasks on Dashboard
    - Manage migration tasks
    - Configure upstream settings
    - Query replication status
    - View master and worker information

    WebUI is still experimental and is still under development. Therefore, it is recommended only for trial. A known issue is that problems might occur if you use WebUI and dmctl to operate the same task. This issue will be resolved in later versions.

    [User document](/dm/dm-webui-guide.md)

- Add an error handling mechanism

    More commands are introduced to address problems that interrupt a migration task. For example:

    - In case of a schema error, you can update the schema file by using the `--from-source/--from-target` parameter of the `binlog-schema update` command, instead of editing the schema file separately.
    - You can specify a binlog position to inject, replace, skip, or revert a DDL statement.

    [User document](/dm/dm-manage-schema.md)

- Support full data storage to Amazon S3

    When DM performs all or full data migration tasks, sufficient hard disk space is required for storing full data from upstream. Compared with EBS, Amazon S3 has nearly infinite storage at lower costs. Now, DM supports configuring Amazon S3 as the dump directory. That means you can use S3 to store full data when you perform all or full data migration tasks.

    [User document](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

- Support starting a migration task from specified time

    A new parameter `--start-time` is added to migration tasks. You can define time in the format of '2021-10-21 00:01:00' or '2021-10-21T00:01:00'.

    This feature is particularly useful in scenarios where you migrate and merge incremental data from shard mysql instances. Specifically, you do not need to set a binlog start point for each source in an incremental migration task. Instead, you can create an incremental migration task quickly by using the `--start-time` parameter in `safe-mode`.

    [User document](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning

- Support configuring the maximum number of tolerable errors

    Added a configuration item `lightning.max-error`. The default value is 0. When the value is greater than 0, the max-error feature is enabled. If an error occurs in a row during encoding, a record containing this row is added to `lightning_task_info.type_error_v1` in the target TiDB and this row is ignored. When rows with errors exceed the threshold, TiDB Lightning exits immediately.

    Matching the `lightning.max-error` configuration, the `lightning.task-info-schema-name` configuration item records the name of the database that reports a data saving error.

    This feature does not cover all types of errors, for example, syntax errors are not applicable.

    [User document](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDB data share subscription

- Support replicating 100,000 tables simultaneously

    By optimizing the data processing flow, TiCDC reduces the resource consumption of processing incremental data for each table, which greatly improves the replication stability and efficiency when replicating data in large clusters. The result of an internal test shows that TiCDC can stably support replicating 100,000 tables simultaneously.

### Deployment and maintenance

- Enable new collation rules by default

    Since v4.0, TiDB has supported new collation rules that behave the same way as MySQL in the case-insensitive, accent-insensitive, and padding rules. The new collation rules are controlled by the `new_collations_enabled_on_first_bootstrap` parameter, which was disabled by default. Since v6.0, TiDB enables the new collation rules by default. Note that this configuration takes effect only upon TiDB cluster initialization.

    [User documentation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

- ​​Accelerate leader balancing after restarting TiKV nodes

    After a restart of TiKV nodes, the unevenly scattered leaders must be redistributed for load balance. In large-scale clusters, leader balancing time is positively correlated with the number of Regions. For example, the leader balancing of 100K Regions can take 20-30 minutes, which is prone to performance issues and stability risks due to uneven load. TiDB v6.0.0 provides a parameter to control the balancing concurrency and enlarges the default value to 4 times of the original, which greatly shortens the leader rebalancing time and accelerates the business recovery after a restart of the TiKV nodes.

    [User documentation](/pd-control.md#scheduler-config-balance-leader-scheduler), [#4610](https://github.com/tikv/pd/issues/4610)

- Support canceling the automatic update of statistics

    Statistics are one of the most important basic data that affect SQL performance. To ensure the completeness and timeliness of statistics, TiDB automatically updates object statistics periodically in the background. However, automatic statistics updates may result in resource contention, affecting SQL performance. To address this issue, you can manually cancel the automatic update of statistics since v6.0.

    [User documentation](/statistics.md#automatic-update)

- PingCAP Clinic diagnostic service (Technical Preview version)

    PingCAP Clinic is a diagnostic service for TiDB clusters. This service helps troubleshoot cluster issues remotely and provides a quick check of cluster status locally. With PingCAP Clinic, you can ensure the stable operation of your TiDB cluster during its full life cycle, predict potential issues, reduce the probability of issues, and quickly troubleshoot cluster issues.

    When contacting PingCAP technical support for remote assistance to troubleshoot cluster issues, you can use the PingCAP Clinic service to collect and upload diagnostic data, thereby improving the troubleshooting efficiency.

    [User documentation](/clinic/clinic-introduction.md)

- An enterprise-level database management platform, TiDB Enterprise Manager

    TiDB Enterprise Manager (TiEM) is an enterprise-level database management platform based on the TiDB database, which aims to help users manage TiDB clusters in on-premises or public cloud environments.

    TiEM not only provides full lifecycle visual management for TiDB clusters, but also provides one-stop services: parameter management, version upgrades, cluster clone, active-standby cluster switching, data import and export, data replication, and data backup and restore services. TiEM can improve the efficiency of DevOps on TiDB and reduce the DevOps cost for enterprises.

    Currently, TiEM is provided in the [TiDB Enterprise](https://en.pingcap.com/tidb-enterprise/) edition only. To get TiEM, contact us via the [TiDB Enterprise](https://en.pingcap.com/tidb-enterprise/) page.

- Support customizing configurations of the monitoring components

    When you deploy a TiDB cluster using TiUP, TiUP automatically deploys monitoring components such as Prometheus, Grafana, and Alertmanager, and automatically adds new nodes into the monitoring scope after scale-out. You can customize the configurations of the monitoring components by adding configuration items to the `topology.yaml` file.

    [User document](/tiup/customized-montior-in-tiup-environment.md)

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v6.0.0, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/releases/release-notes.md) of the corresponding version.

### System variables

| Variable name | Change type | Description |
|:---|:---|:---|
| `placement_checks` | Deleted | Controls whether the DDL statement validates the placement rules specified by [Placement Rules in SQL](/placement-rules-in-sql.md). Replaced by `tidb_placement_mode`. |
| `tidb_enable_alter_placement` | Deleted | Controls whether to enable [placement rules in SQL](/placement-rules-in-sql.md). |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | Deleted | Since v5.0, these variables have been replaced by `tidb_mem_quota_query` and removed from the [system variables](/system-variables.md) document. To ensure compatibility, these variables were kept in source code. Since TiDB 6.0.0, these variables are removed from the code, too. |
| [`tidb_enable_mutation_checker`](/system-variables.md#tidb_enable_mutation_checker-new-in-v600) | Newly added | Controls whether to enable the mutation checker. The default value is `ON`. For existing clusters that upgrade from versions earlier than v6.0.0, the mutation checker is disabled by default. |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) | Newly added | Controls whether to ignore the command that closes Prepared Statement. The default value is `OFF`. |
| [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600) | Newly added | Sets the memory usage threshold for the cache holding `binding`. The default value is `67108864` (64 MiB). |
| [`tidb_placement_mode`](/system-variables.md#tidb_placement_mode-new-in-v600) | Newly added | Controls whether DDL statements ignore the placement rules specified by [Placement Rules in SQL](/placement-rules-in-sql.md). The default value is `strict`, which means that DDL statements do not ignore placement rules. |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) | Newly added | <ul><li> Optimizes read statement latency within a transaction. If read/write conflicts are more severe, turning this variable on will add additional overhead and latency, causing regressions in performance. The default value is `off`.</li><li> This variable is not yet compatible with [replica-read](/system-variables.md#tidb_replica_read-new-in-v40). If a read request has `tidb_rc_read_check_ts` on, it might not be able to use replica-read. Do not turn on both variables at the same time.</li></ul> |
| [`tidb_sysdate_is_now`](/system-variables.md#tidb_sysdate_is_now-new-in-v600) | Newly added | Controls whether the `SYSDATE` function can be replaced by the `NOW` function. This configuration item has the same effect as the MySQL option [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now). The default value is `OFF`. |
| [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600) | Newly added | Controls the lease time of [table cache](/cached-tables.md), in seconds. The default value is `3`. |
| [`tidb_top_sql_max_meta_count`](/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600) | Newly added | Controls the maximum number of SQL statement types collected by [Top SQL](/dashboard/top-sql.md) per minute. The default value is `5000`. |
| [`tidb_top_sql_max_time_series_count`](/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600) | Newly added | Controls how many SQL statements that contribute the most to the load (that is, top N) can be recorded by [Top SQL](/dashboard/top-sql.md) per minute. The default value is `100`. |
| [`tidb_txn_assertion_level`](/system-variables.md#tidb_txn_assertion_level-new-in-v600) | Newly added | Controls the assertion level. The assertion is a consistency check between data and indexes, which checks whether a key being written exists in the transaction commit process. By default, the check enables most of the check items, with almost no impact on performance. For existing clusters that upgrade from versions earlier than v6.0.0, the check is disabled by default. |

### Configuration file parameters

| Configuration file | Configuration | Change type | Description |
|:---|:---|:---|:---|
| TiDB | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | Deleted | Configuration related to the [statement summary tables](/statement-summary-tables.md). All these configuration items are removed. You need to use SQL variables to control the statement summary tables. |
| TiDB | [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) | Modified | Controls whether to enable support for the new collation. Since v6.0, the default value is changed from `false` to `true`. This configuration item only takes effect when the cluster is initialized for the first time. After the first bootstrap, you cannot enable or disable the new collation framework using this configuration item. |
| TiKV | [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) | Modified | The value range is modified to `[1, CPU]`.  |
| TiKV | [`raftstore.apply-max-batch-size`](/tikv-configuration-file.md#apply-max-batch-size) | Modified | The maximum value is changed to `10240`. |
| TiKV | [`raftstore.raft-max-size-per-msg`](/tikv-configuration-file.md#raft-max-size-per-msg) | Modified | <ul><li>The minimum value is changed from `0` to larger than `0`.</li><li>The maximum value is set to `3GB`.</li><li>The unit is changed from `MB` to <code>KB\|MB\|GB</code>.</li></ul> |
| TiKV | [`raftstore.store-max-batch-size`](/tikv-configuration-file.md#store-max-batch-size) | Modified | The maximum value is set to `10240`. |
| TiKV | [`readpool.unified.max-thread-count`](/tikv-configuration-file.md#max-thread-count) | Modified | The adjustable range is changed to `[min-thread-count, MAX(4, CPU)]`. |
| TiKV | [`rocksdb.enable-pipelined-write`](/tikv-configuration-file.md#enable-pipelined-write) | Modified | The default value is changed from `true` to `false`. When this configuration is enabled, the previous Pipelined Write is used. When this configuration is disabled, the new Pipelined Commit mechanism is used. |
| TiKV | [`rocksdb.max-background-flushes`](/tikv-configuration-file.md#max-background-flushes) | Modified | <ul><li>When the number of CPU cores is 10, the default value is `3`.</li><li>When the number of CPU cores is 8, the default value is `2`.</li></ul> |
| TiKV | [`rocksdb.max-background-jobs`](/tikv-configuration-file.md#max-background-jobs) | Modified | <ul><li>When the number of CPU cores is 10, the default value is `9`.</li><li>When the number of CPU cores is 8, the default value is `7`.</li></ul> |
| TiFlash | [`profiles.default.dt_enable_logical_split`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | Determines whether the segment of DeltaTree Storage Engine uses logical split. The default value is changed from `true` to `false`. |
| TiFlash | [`profiles.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | Controls whether to enable the elastic thread pool. The default value is changed from `false` to `true`. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | Controls the data validation feature of TiFlash. The default value is changed from `2` to `3`.<br/>When `format_version` is set to `3`, consistency check is performed on the read operations for all TiFlash data to avoid incorrect read due to hardware failure.<br/>Note that the new format version cannot be downgraded in place to versions earlier than v5.4. |
| TiDB | [`pessimistic-txn.pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600) | Newly added | Determines the transaction mode that the auto-commit transaction uses when the pessimistic transaction mode is globally enabled (`tidb_txn_mode='pessimistic'`). |
| TiKV | [`pessimistic-txn.in-memory`](/tikv-configuration-file.md#in-memory-new-in-v600) | Newly added | Controls whether to enable the in-memory pessimistic lock. With this feature enabled, pessimistic transactions store pessimistic locks in TiKV memory as much as possible, instead of writing pessimistic locks to disks or replicating to other replicas. This improves the performance of pessimistic transactions; however, there is a low probability that a pessimistic lock will be lost, which might cause the pessimistic transaction to fail to commit. The default value is `true`. |
| TiKV | [`quota`](/tikv-configuration-file.md#quota) | Newly added | Add configuration items related to Quota Limiter, which limit the resources occupied by frontend requests. Quota Limiter is an experimental feature and is disabled by default. New quota-related configuration items are `foreground-cpu-time`, `foreground-write-bandwidth`, `foreground-read-bandwidth`, and `max-delay-duration`. |
| TiFlash | [`profiles.default.dt_compression_method`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | Specifies the compression algorithm for TiFlash. The optional values are `LZ4`, `zstd` and `LZ4HC`, all case insensitive. The default value is `LZ4`. |
| TiFlash | [`profiles.default.dt_compression_level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | Specifies the compression level of TiFlash. The default value is `1`. |
| DM | [`loaders.<name>.import-mode`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | The import mode during the full import phase. Since v6.0, DM uses TiDB Lightning's TiDB-backend mode to import data during the full import phase; the previous Loader component is no longer used. This is an internal replacement and has no obvious impact on daily operations.<br/>The default value is set to `sql`, which means using `tidb-backend` mode. In some rare cases, `tidb-backend` might not be fully compatible. You can fall back to Loader mode by configuring this parameter to `loader`. |
| DM | [`loaders.<name>.on-duplicate`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | Newly added | Specifies the methods to resolve conflicts during the full import phase. The default value is `replace`, which means using the new data to replace the existing data. |
| TiCDC | [`dial-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) | Newly added | The timeout in establishing a connection with the downstream Kafka. The default value is `10s`. |
| TiCDC | [`read-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) | Newly added | The timeout in getting a response returned by the downstream Kafka. The default value is `10s`. |
| TiCDC | [`write-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) | Newly added | The timeout in sending a request to the downstream Kafka. The default value is `10s`. |

### Others

- The data placement policy has the following compatibility changes:
    - Binding is not supported. The direct placement option is removed from the syntax.
    - The `CREATE PLACEMENT POLICY` and `ALTER PLACEMENT POLICY` statements no longer support the `VOTERS` and `VOTER_CONSTRAINTS` placement options.
    - TiDB migration tools (TiDB Binlog, TiCDC, and BR) are now compatible with placement rules. The placement option is moved to a special comment in TiDB Binlog.
    - The `information_schema.placement_rules` system table is renamed to `information_schema.placement_policies`. This table now only displays information about placement policies.
    - The `placement_checks` system variable is replaced by `tidb_placement_mode`.
    - It is prohibited to add partitions with placement rules to tables that have TiFlash replicas.
    - Remove the `TIDB_DIRECT_PLACEMENT` column from the `INFORMATION_SCHEMA` table.
- The `status` value of SQL plan management (SPM) binding is modified:
    - Remove `using`.
    - Add `enabled` (available) to replace `using`.
    - Add `disabled` (unavailable).
- DM modifies the OpenAPI interface
    - Because of internal mechanism changes, the interface related to task management cannot be compatible with the previous experimental version. You need to refer to the new [DM OpenAPI documentation](/dm/dm-open-api.md) for adaptation.
- DM changes the methods to resolve conflicts during the full import phase
    - A `loader.<name>.on-duplicate` parameter is added. The default value is `replace`, which means using the new data to replace the existing data. If you want to keep the previous behavior, you can set the value to `error`. This parameter only controls the behavior during the full import phase.
- To use DM, you should use the corresponding version of `dmctl`
    - Due to internal mechanism changes, after upgrading DM to v6.0.0, you should also upgrade `dmctl` to v6.0.0.
- In v5.4 (v5.4 only), TiDB allows incorrect values for some noop system variables. Since v6.0.0, TiDB disallows setting incorrect values for system variables. [#31538](https://github.com/pingcap/tidb/issues/31538)

## Improvements

+ TiDB

    - Clear the placement rule settings of a table automatically after restoring the table using the `FLASHBACK` or `RECOVER` statement  [#31668](https://github.com/pingcap/tidb/issues/31668)
    - Add a performance overview dashboard to show core performance metrics on typical critical paths, making metrics analysis on TiDB easier [#31676](https://github.com/pingcap/tidb/issues/31676)
    - Support using the `REPLACE` keyword in the `LOAD DATA LOCAL INFILE` statement [#24515](https://github.com/pingcap/tidb/issues/24515)
    - Support partition pruning for the built-in `IN` expression in Range partition tables [#26739](https://github.com/pingcap/tidb/issues/26739)
    - Improve query efficiency by eliminating potentially redundant Exchange operations in MPP aggregation queries [#31762](https://github.com/pingcap/tidb/issues/31762)
    - Improve compatibility with MySQL by allowing duplicate partition names in the `TRUNCATE PARTITION` and `DROP PARTITION` statements [#31681](https://github.com/pingcap/tidb/issues/31681)
    - Support showing the `CREATE_TIME` information in the results of the `ADMIN SHOW DDL JOBS` statement [#23494](https://github.com/pingcap/tidb/issues/23494)
    - Support a new built-in function `CHARSET()` [#3931](https://github.com/pingcap/tidb/issues/3931)
    - Support filtering a baseline capturing blocklist by usernames [#32558](https://github.com/pingcap/tidb/issues/32558)
    - Support using wildcards in a baseline capturing blocklist [#32714](https://github.com/pingcap/tidb/issues/32714)
    - Optimize the results of the `ADMIN SHOW DDL JOBS` and `SHOW TABLE STATUS` statements by displaying the time according to the current `time_zone` [#26642](https://github.com/pingcap/tidb/issues/26642)
    - Support pushing down the `DAYNAME()` and `MONTHNAME()` functions to TiFlash [#32594](https://github.com/pingcap/tidb/issues/32594)
    - Support pushing down the `REGEXP` function to TiFlash [#32637](https://github.com/pingcap/tidb/issues/32637)
    - Support pushing down the `DAYOFMONTH()` and `LAST_DAY()` functions to TiFlash [#33012](https://github.com/pingcap/tidb/issues/33012)
    - Support pushing down the `DAYOFWEEK()` and `DAYOFYEAR()` functions to TiFlash [#33130](https://github.com/pingcap/tidb/issues/33130)
    - Support pushing down the `IS_TRUE`, `IS_FALSE`, and `IS_TRUE_WITH_NULL` functions to TiFlash [#33047](https://github.com/pingcap/tidb/issues/33047)
    - Support pushing down the `GREATEST` and `LEAST` functions to TiFlash [#32787](https://github.com/pingcap/tidb/issues/32787)
    - Support tracking the execution of the `UnionScan` operator [#32631](https://github.com/pingcap/tidb/issues/32631)
    - Support using the PointGet plan for queries that read the `_tidb_rowid` column [#31543](https://github.com/pingcap/tidb/issues/31543)
    - Support showing the original partition name in the output of the `EXPLAIN` statement without converting the name to lowercase [#32719](https://github.com/pingcap/tidb/issues/32719)
    - Enable partition pruning for RANGE COLUMNS partitionings on IN conditions and string type columns [#32626](https://github.com/pingcap/tidb/issues/32626)
    - Return an error message when a system variable is set to NULL [#32850](https://github.com/pingcap/tidb/issues/32850)
    - Remove Broadcast Join from the non-MPP mode [#31465](https://github.com/pingcap/tidb/issues/31465)
    - Support executing MPP plans on partitioned tables in dynamic pruning mode [#32347](https://github.com/pingcap/tidb/issues/32347)
    - Support pushing down predicates for common table expressions (CTEs) [#28163](https://github.com/pingcap/tidb/issues/28163)
    - Simplify the configurations of `Statement Summary` and `Capture Plan Baselines` to be available on a global basis only [#30557](https://github.com/pingcap/tidb/issues/30557)
    - Update gopsutil to v3.21.12 to address alarms reported when building binary on macOS 12 [#31607](https://github.com/pingcap/tidb/issues/31607)

+ TiKV

    - Improve the sampling accuracy of the Raftstore for batches with many key ranges [#12327](https://github.com/tikv/tikv/issues/12327)
    - Add the correct "Content-Type" for `debug/pprof/profile` to make the Profile more easily identified [#11521](https://github.com/tikv/tikv/issues/11521)
    - Renew the lease time of the leader infinitely when the Raftstore has heartbeats or handles read requests, which helps reduce latency jitter [#11579](https://github.com/tikv/tikv/issues/11579)
    - Choose the store with the least cost when switching the leader, which helps improve performance stability [#10602](https://github.com/tikv/tikv/issues/10602)
    - Fetch Raft logs asynchronously to reduce the performance jitter caused by blocking the Raftstore [#11320](https://github.com/tikv/tikv/issues/11320)
    - Support the `QUARTER` function in vector calculation [#5751](https://github.com/tikv/tikv/issues/5751)
    - Support pushing down the `BIT` data type to TiKV [#30738](https://github.com/pingcap/tidb/issues/30738)
    - Support pushing down the `MOD` function and the `SYSDATE` function to TiKV [#11916](https://github.com/tikv/tikv/issues/11916)
    - Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)
    - Support dynamically modifying `raftstore.raft-max-inflight-msgs` [#11865](https://github.com/tikv/tikv/issues/11865)
    - Support `EXTRA_PHYSICAL_TABLE_ID_COL_ID` to enable dynamic pruning mode [#11888](https://github.com/tikv/tikv/issues/11888)
    - Support calculation in buckets [#11759](https://github.com/tikv/tikv/issues/11759)
    - Encode the keys of RawKV API V2 as `user-key` + `memcomparable-padding` + `timestamp` [#11965](https://github.com/tikv/tikv/issues/11965)
    - Encode the values of RawKV API V2 as `user-value` + `ttl` + `ValueMeta` and encode `delete` in `ValueMeta` [#11965](https://github.com/tikv/tikv/issues/11965)
    - Support dynamically modifying `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)
    - Support monitoring multi-k8s in Grafana [#12014](https://github.com/tikv/tikv/issues/12014)
    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)
    - Support dynamically modifying `raftstore.apply_max_batch_size` and `raftstore.store_max_batch_size` [#11982](https://github.com/tikv/tikv/issues/11982)
    - RawKV V2 returns the latest version upon receiving the `raw_get` or `raw_scan` request [#11965](https://github.com/tikv/tikv/issues/11965)
    - Support the RCCheckTS consistency reads [#12097](https://github.com/tikv/tikv/issues/12097)
    - Support dynamically modifying `storage.scheduler-worker-pool-size`(the thread count of the Scheduler pool) [#12067](https://github.com/tikv/tikv/issues/12067)
    - Control the use of CPU and bandwidth by using the global foreground flow controller to improve the performance stability of TiKV [#11855](https://github.com/tikv/tikv/issues/11855)
    - Support dynamically modifying `readpool.unified.max-thread-count` (the thread count of the UnifyReadPool) [#11781](https://github.com/tikv/tikv/issues/11781)
    - Use the TiKV internal pipeline to replace the RocksDB pipeline and deprecate the `rocksdb.enable-multibatch-write` parameter [#12059](https://github.com/tikv/tikv/issues/12059)

+ PD

    - Support automatically selecting the fastest object for transfer when evicting the leader, which helps speed up the eviction process [#4229](https://github.com/tikv/pd/issues/4229)
    - Forbid deleting a voter from a 2-replica Raft group in case the Region becomes unavailable [#4564](https://github.com/tikv/pd/issues/4564)
    - Speed up the scheduling of the balance leader [#4652](https://github.com/tikv/pd/issues/4652)

+ TiFlash

    - Forbid the logical splitting of TiFlash files (by adjusting the default value of `profiles.default.dt_enable_logical_split` to `false`. See [user document](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) for details) and improve the space usage efficiency of the TiFlash columnar storage so that the space occupation of a table synchronized to TiFlash is similar to the space occupation of the table in TiKV
    - Optimize the cluster management and replica replication mechanism for TiFlash by integrating the previous cluster management module into TiDB, which accelerates replica creation for small tables [#29924](https://github.com/pingcap/tidb/issues/29924)

+ Tools

    + Backup & Restore (BR)

        - Improve the speed of restoring the backup data. In the simulation test when BR restores 16 TB data to a TiKV cluster with 15 nodes (each node has 16 CPU cores), the throughput reaches 2.66 GiB/s. [#27036](https://github.com/pingcap/tidb/issues/27036)

        - Support importing and exporting placement rules. Add a `--with-tidb-placement-mode` parameter to control whether to ignore the placement rules when importing data. [#32290](https://github.com/pingcap/tidb/issues/32290)

    + TiCDC

        - Add a `Lag analyze` panel in Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)
        - Support placement rules [#4846](https://github.com/pingcap/tiflow/issues/4846)
        - Synchronize HTTP API handling [#1710](https://github.com/pingcap/tiflow/issues/1710)
        - Add the exponential backoff mechanism for restarting a changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - Set the default isolation level of MySQL sink to read-committed to reduce deadlocks in MySQL [#3589](https://github.com/pingcap/tiflow/issues/3589)
        - Validate changefeed parameters upon creation and refine error messages [#1716](https://github.com/pingcap/tiflow/issues/1716) [#1718](https://github.com/pingcap/tiflow/issues/1718) [#1719](https://github.com/pingcap/tiflow/issues/1719) [#4472](https://github.com/pingcap/tiflow/issues/4472)
        - Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)

    + TiDB Data Migration (DM)

        - Support starting a task when upstream table schemas are inconsistent and in optimistic mode [#3629](https://github.com/pingcap/tiflow/issues/3629) [#3708](https://github.com/pingcap/tiflow/issues/3708) [#3786](https://github.com/pingcap/tiflow/issues/3786)
        - Support creating a task in the `stopped` state [#4484](https://github.com/pingcap/tiflow/issues/4484)
        - Support Syncer using the working directory of the DM-worker rather than `/tmp` to write internal files, and cleaning the directory after the task is stopped [#4107](https://github.com/pingcap/tiflow/issues/4107)
        - Precheck has improved. Some important checks are no longer skipped. [#3608](https://github.com/pingcap/tiflow/issues/3608)

    + TiDB Lightning

        - Add more retryable error types [#31376](https://github.com/pingcap/tidb/issues/31376)
        - Support the base64 format password string [#31194](https://github.com/pingcap/tidb/issues/31194)
        - Standardize error codes and error outputs [#32239](https://github.com/pingcap/tidb/issues/32239)

## Bug fixes

+ TiDB

    - Fix a bug that TiDB fails to create tables with placement rules when `SCHEDULE = majority_in_primary`, and `PrimaryRegion` and `Regions` are of the same value [#31271](https://github.com/pingcap/tidb/issues/31271)
    - Fix the `invalid transaction` error when executing a query using index lookup join [#30468](https://github.com/pingcap/tidb/issues/30468)
    - Fix a bug that `show grants` returns incorrect results when two or more privileges are granted [#30855](https://github.com/pingcap/tidb/issues/30855)
    - Fix a bug that `INSERT INTO t1 SET timestamp_col = DEFAULT` would set the timestamp to the zero timestamp for the field defaulted to `CURRENT_TIMESTAMP` [#29926](https://github.com/pingcap/tidb/issues/29926)
    - ​Fix errors reported in reading the results by avoiding encoding the maximum value and minimum non-null value of the string type [#31721](https://github.com/pingcap/tidb/issues/31721)
    - Fix load data panic if the data is broken at an escape character [#31589](https://github.com/pingcap/tidb/issues/31589)
    - Fix the issue that the `greatest` or `least` function with collation gets a wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    - Fix a bug that the date_add and date_sub functions might return incorrect data types [#31809](https://github.com/pingcap/tidb/issues/31809)
    - Fix possible panic when inserting data to virtually generated columns using an insert statement [#31735](https://github.com/pingcap/tidb/issues/31735)
    - Fix a bug that no error is reported when duplicate columns are present in the created list partition [#31784](https://github.com/pingcap/tidb/issues/31784)
    - Fix wrong results returned when `select for update union select` uses incorrect snapshots [#31530](https://github.com/pingcap/tidb/issues/31530)
    - Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#31034](https://github.com/pingcap/tidb/issues/31034)
    - Fix a bug that COERCIBILITY is wrong for the `json` type [#31541](https://github.com/pingcap/tidb/issues/31541)
    - Fix wrong collation of the `json` type when this type is processed using builtin-func [#31320](https://github.com/pingcap/tidb/issues/31320)
    - Fix a bug that PD rules are not deleted when the count of TiFlash replicas is set to 0 [#32190](https://github.com/pingcap/tidb/issues/32190)
    - Fix the issue that `alter column set default` wrongly updates the table schema [#31074](https://github.com/pingcap/tidb/issues/31074)
    - Fix the issue that `date_format` in TiDB handles `'\n'` in a MySQL-incompatible way [#32232](https://github.com/pingcap/tidb/issues/32232)
    - Fix a bug that errors may occur when updating partitioned tables using join [#31629](https://github.com/pingcap/tidb/issues/31629)
    - Fix wrong range calculation results for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    - Fix possible panic in `upper()` and `lower()` functions [#32488](https://github.com/pingcap/tidb/issues/32488)
    - Fix time zone problems encountered when changing the other type columns to timestamp type columns [#29585](https://github.com/pingcap/tidb/issues/29585)
    - Fix TiDB OOM when exporting data using ChunkRPC [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    - Fix a bug that sub SELECT LIMIT does not work as expected in dynamic partition pruning mode [#32516](https://github.com/pingcap/tidb/issues/32516)
    - Fix wrong or inconsistent format of bit default value in the `INFORMATION_SCHEMA.COLUMNS` table [#32655](https://github.com/pingcap/tidb/issues/32655)
    - Fix a bug that partition table pruning might not work for listing partition tables after server restart [#32416](https://github.com/pingcap/tidb/issues/32416)
    - Fix a bug that `add column` might use a wrong default timestamp after `SET timestamp` is executed [#31968](https://github.com/pingcap/tidb/issues/31968)
    - Fix a bug that connecting to a TiDB passwordless account from MySQL 5.5 or 5.6 client may fail [#32334](https://github.com/pingcap/tidb/issues/32334)
    - Fix wrong results when reading partitioned tables in dynamic mode in transactions [#29851](https://github.com/pingcap/tidb/issues/29851)
    - Fix a bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    - Fix wrong results returned when the input of the `timdiff` function contains a millisecond [#31680](https://github.com/pingcap/tidb/issues/31680)
    - Fix wrong results when explicitly reading partitions and using the IndexJoin plan [#32007](https://github.com/pingcap/tidb/issues/32007)
    - Fix a bug that renaming a column fails when changing its column type concurrently [#31075](https://github.com/pingcap/tidb/issues/31075)
    - Fix a bug that the formula for calculating net cost for TiFlash plans is not aligned with TiKV plans [#30103](https://github.com/pingcap/tidb/issues/30103)
    - Fix a bug that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix possible wrong results when querying a table with generated columns [#33038](https://github.com/pingcap/tidb/issues/33038)
    - Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    - Fix a bug that the `SUBTIME` function returns a wrong result in case of overflow [#31868](https://github.com/pingcap/tidb/issues/31868)
    - Fix a bug that the `selection` operator cannot be pushed down when an aggregation query contains the `having` condition [#33166](https://github.com/pingcap/tidb/issues/33166)
    - Fix a bug that CTE might be blocked when a query reports errors [#31302](https://github.com/pingcap/tidb/issues/31302)
    - Fix a bug that excessive length of varbinary or varchar columns when creating tables in non-strict mode might result in errors [#30328](https://github.com/pingcap/tidb/issues/30328)
    - Fix the wrong number of followers in `information_schema.placement_policies` when no follower is specified [#31702](https://github.com/pingcap/tidb/issues/31702)
    - Fix the issue that TiDB allows to specify column prefix length as 0 when an index is created [#31972](https://github.com/pingcap/tidb/issues/31972)
    - Fix the issue that TiDB allows partition names ending with spaces [#31535](https://github.com/pingcap/tidb/issues/31535)
    - Correct the error message of the `RENAME TABLE` statement [#29893](https://github.com/pingcap/tidb/issues/29893)

+ TiKV

    - Fix the panic issue caused by deleting snapshot files when the peer status is `Applying` [#11746](https://github.com/tikv/tikv/issues/11746)
    - Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)
    - Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)
    - Fix a bug that TiKV cannot delete a range of data (which means the internal command `unsafe_destroy_range` is executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    - Fix a bug that TiKV panics when the data in `StoreMeta` is accidentally deleted in some corner cases [#11852](https://github.com/tikv/tikv/issues/11852)
    - Fix a bug that TiKV panics when performing profiling on an ARM platform [#10658](https://github.com/tikv/tikv/issues/10658)
    - Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    - Fix the compilation issue on the ARM64 architecture caused by missing SSE instruction set [#12034](https://github.com/tikv/tikv/issues/12034)
    - Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    - Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    - Fix the issue that undefined behavior (UB) might occur in TsSet conversions [#12070](https://github.com/tikv/tikv/issues/12070)
    - Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    - Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - Fix the issue of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    - Fix the potential issue of mistakenly reporting TiKV panics when exiting TiKV [#12231](https://github.com/tikv/tikv/issues/12231)

+ PD

    - Fix the issue that PD generates the operator with meaningless steps of Joint Consensus [#4362](https://github.com/tikv/pd/issues/4362)
    - Fix a bug that the TSO revoking process might get stuck when closing the PD client [#4549](https://github.com/tikv/pd/issues/4549)
    - Fix the issue that the Region scatterer scheduling lost some peers [#4565](https://github.com/tikv/pd/issues/4565)
    - Fix the issue that `Duration` fields of `dr-autosync` cannot be dynamically configured [#4651](https://github.com/tikv/pd/issues/4651)

+ TiFlash

    - Fix the TiFlash panic issue that occurs when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    - Fix the issue that expired data is recycled slowly [#4146](https://github.com/pingcap/tiflash/issues/4146)
    - Fix the potential issue of TiFlash panic when `Snapshot` is applied simultaneously with multiple DDL operations [#4072](https://github.com/pingcap/tiflash/issues/4072)
    - Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    - Fix the issue that the `SQRT` function with a negative argument returns `NaN` instead of `Null` [#3598](https://github.com/pingcap/tiflash/issues/3598)
    - Fix the issue that casting `INT` to `DECIMAL` might cause overflow [#3920](https://github.com/pingcap/tiflash/issues/3920)
    - Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    - Fix the issue that the date format identifies `'\n'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    - Fix the issue that the learner-read process takes too much time under high concurrency scenarios [#3555](https://github.com/pingcap/tiflash/issues/3555)
    - Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - Fix the issue of memory leak that occurs when a query is canceled [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - Fix a bug that enabling the elastic thread pool might cause a memory leak [#4098](https://github.com/pingcap/tiflash/issues/4098)
    - Fix a bug that canceled MPP queries might cause tasks to hang forever when the local tunnel is enabled [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - Fix a bug that the failure of the HashJoin build side might cause MPP queries to hang forever [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)
        - Fix a bug that causes the restore operation to fail when the encryption information is lost during backup retry [#32423](https://github.com/pingcap/tidb/issues/32423)

    + TiCDC

        - Fix a bug that MySQL sink generates duplicated `replace` SQL statements when `batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        - Fix the error `Unknown system variable 'transaction_isolation'` for some MySQL versions [#4504](https://github.com/pingcap/tiflow/issues/4504)
        - Fix the TiCDC panic issue that might occur when `Canal-JSON` incorrectly handles `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)
        - Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)
        - Fix the TiCDC panic issue that might occur because `Canal-JSON` does not support nil [#4736](https://github.com/pingcap/tiflow/issues/4736)
        - Fix the wrong data mapping for avro codec of type `Enum/Set` and `TinyText/MediumText/Text/LongText` [#4454](https://github.com/pingcap/tiflow/issues/4454)
        - Fix a bug that Avro converts a `NOT NULL` column to a nullable field [#4818](https://github.com/pingcap/tiflow/issues/4818)
        - Fix an issue that TiCDC cannot exit [#4699](https://github.com/pingcap/tiflow/issues/4699)

    + TiDB Data Migration (DM)

        - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        - Fix the issue that execution errors of the update statement in safemode may cause the DM-worker panic [#4317](https://github.com/pingcap/tiflow/issues/4317)
        - Fix a bug that long varchars report an error `Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        - Fix the conflict issue caused by multiple DM-workers writing data from the same upstream [#3737](https://github.com/pingcap/tiflow/issues/3737)
        - Fix the issue that hundreds of "checkpoint has no change, skip sync flush checkpoint" print in the log and the replication is very slow [#4619](https://github.com/pingcap/tiflow/issues/4619)
        - Fix the DML loss issue when merging shards and replicating incremental data from upstream in the pessimistic mode [#5002](https://github.com/pingcap/tiflow/issues/5002)

    + TiDB Lightning

        - Fix a bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        - Fix the panic that occurs when the table names in the source file and in the target cluster are different [#31771](https://github.com/pingcap/tidb/issues/31771)
        - Fix the checksum error "GC life time is shorter than transaction duration" [#32733](https://github.com/pingcap/tidb/issues/32733)
        - Fix the issue that TiDB Lightning gets stuck when it fails to check empty tables [#31797](https://github.com/pingcap/tidb/issues/31797)

    + Dumpling

        - Fix the issue that the displayed progress is not accurate when running `dumpling --sql $query` [#30532](https://github.com/pingcap/tidb/issues/30532)
        - Fix the issue that Amazon S3 cannot correctly calculate the size of compressed data [#30534](https://github.com/pingcap/tidb/issues/30534)

    + TiDB Binlog

        - Fix the issue that TiDB Binlog might be skipped when large upstream write transactions are replicated to Kafka [#1136](https://github.com/pingcap/tidb-binlog/issues/1136)
