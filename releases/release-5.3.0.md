---
title: TiDB 5.3 Release Notes
---

# TiDB 5.3 Release Notes

Release date: November 30, 2021

TiDB version: 5.3.0

In v5.3, the key new features or improvements are as follows:

+ Introduce temporary tables to simplify your application logic and improve performance
+ Support setting attributes for tables and partitions
+ Support creating users with the least privileges on TiDB Dashboard to enhance system security
+ Optimize the timestamp processing flow in TiDB to improve the overall performance
+ Enhance the performance of TiDB Data Migration (DM) so that data is migrated from MySQL to TiDB with lower latency
+ Support parallel import using multiple TiDB Lightning instances to improve the efficiency of full data migration
+ Support saving and restoring the on-site information of a cluster with a single SQL statement, which helps improve the efficiency of troubleshooting issues relating to execution plans
+ Support the continuous profiling experimental feature to improve the observability of database performance
+ Continue optimizing the storage and computing engines to improve the system performance and stability

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v5.3.0, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/releases/release-notes.md) of the corresponding version.

### System variables

|  Variable name    |  Change type    |  Description    |
| :---------- | :----------- | :----------- |
| [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40) | Modified |  Temporary tables are now supported by TiDB so `CREATE TEMPORARY TABLE` and `DROP TEMPORARY TABLE` no longer require enabling `tidb_enable_noop_functions`. |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | Newly added | Controls the behavior of the optimizer when the statistics on a table expire. The default value is `ON`. When the number of modified rows in the table is greater than 80% of the total rows (This ratio can be adjusted by the configuration [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)), the optimizer considers that the statistics other than the total number of rows are no longer reliable and use pseudo statistics instead. When you set the value as `OFF`, even if the statistics expire, the optimizer still uses them. |
|[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v53) | Newly added  | Determines whether to enable or disable the TSO Follower Proxy feature. The default value is `OFF`, which means the TSO Follower Proxy feature is disabled. At this time, TiDB only gets TSO from PD leader. When this feature is enabled, TiDB evenly sends the requests to all PD nodes when acquiring TSO. The PD follower then forwards the TSO requests to reduce the CPU pressure of PD leader. |
|[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v53) | Newly added |  Sets the maximum waiting time for a batch saving operation when TiDB requests TSO from PD. The default value is `0`, which means no additional waiting. |
| [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530) | Newly added  | Limits the maximum size of a single [temporary table](/temporary-tables.md). If the temporary table exceeds this size, an error will occur. |

### Configuration file parameters

|  Configuration file    |  Configuration item  | Change type |  Description  |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`prepared-plan-cache.capacity`](/tidb-configuration-file.md#capacity)  | Modified | Controls the number of cached statements. The default value is changed from `100` to `1000`.|
| TiKV | [`storage.reserve-space`](/tikv-configuration-file.md#reserve-space) | Modified | Controls space reserved for disk protection when TiKV is started. Starting from v5.3.0, 80% of the reserved space is used as the extra disk space required for operations and maintenance when the disk space is insufficient, and the other 20% is used to store temporary files. |
| TiKV | `memory-usage-limit` | Modified  | This configuration item is new in TiDB v5.3.0 and its value is calculated based on storage.block-cache.capacity. |
| TiKV | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) | Newly added | The allowable number of threads that process Raft I/O tasks, which is the size of the StoreWriter thread pool. When you modify the size of this thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools). |
| TiKV | [`raftstore.raft-write-size-limit`](/tikv-configuration-file.md#raft-write-size-limit-new-in-v530) | Newly added | Determines the threshold at which Raft data is written into the disk. If the data size is larger than the value of this configuration item, the data is written to the disk. When the value of `raftstore.store-io-pool-size` is `0`, this configuration item does not take effect. |
| TiKV | [`raftstore.raft-msg-flush-interval`](/tikv-configuration-file.md#raft-msg-flush-interval-new-in-v530) | Newly added | Determines the interval at which Raft messages are sent in batches. The Raft messages in batches are sent at every interval specified by this configuration item. When the value of `raftstore.store-io-pool-size` is `0`, this configuration item does not take effect. |
| TiKV | `raftstore.raft-reject-transfer-leader-duration`  | Deleted | Determines the smallest duration that a Leader is transferred to a newly added node. |
| PD | [`log.file.max-days`](/pd-configuration-file.md#max-days) | Modified | Controls the maximum number of days that logs are retained for. The default value is changed from `1` to `0`. |
| PD | [`log.file.max-backups`](/pd-configuration-file.md#max-backups) | Modified | Controls the maximum number of logs that are retained for. The default value is changed from `7` to `0`.  |
| PD | [`patrol-region-interval`](/pd-configuration-file.md#patrol-region-interval) | Modified | Controls the running frequency at which replicaChecker checks the health state of a Region. The smaller this value is, the faster replicaChecker runs. Normally, you do not need to adjust this parameter. The default value is changed from `100ms` to `10ms`. |
| PD | [`max-snapshot-count`](/pd-configuration-file.md#max-snapshot-count) | Modified | Controls the maximum number of snapshots that a single store receives or sends at the same time. PD schedulers depend on this configuration to prevent the resources used for normal traffic from being preempted. The default value is changed from `3` to `64`. |
| PD | [`max-pending-peer-count`](/pd-configuration-file.md#max-pending-peer-count) | Modified | Controls the maximum number of pending peers in a single store. PD schedulers depend on this configuration to prevent too many Regions with outdated logs from being generated on some nodes. The default value is changed from `16` to `64`. |

### Others

- Temporary tables:

    - If you have created local temporary tables in a TiDB cluster earlier than v5.3.0, these tables are actually ordinary tables, and handled as ordinary tables after the cluster is upgraded to v5.3.0 or a later version. If you have created global temporary tables in a TiDB cluster of v5.3.0 or a later version, when the cluster is downgraded to a version earlier than v5.3.0, these tables are handled as ordinary tables and cause a data error.
    - Since v5.3.0, TiCDC and BR support [global temporary tables](/temporary-tables.md#global-temporary-tables). If you use TiCDC and BR of a version earlier than v5.3.0 to replicate global temporary tables to the downstream, a table definition error occurs.
    - The following clusters are expected to be v5.3.0 or later; otherwise, data error is reported when you create a global temporary table:

        - the cluster to be imported using TiDB ecosystem tools
        - the cluster restored using TiDB ecosystem tools
        - the downstream cluster in a replication task using TiDB ecosystem tools
    - For the compatibility information of temporary tables, refer to [Compatibility with MySQL temporary tables](/temporary-tables.md#compatibility-with-mysql-temporary-tables) and [Compatibility restrictions with other TiDB features](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features).

- For releases earlier than v5.3.0, TiDB reports an error when a system variable is set to an illegal value. For v5.3.0 and later releases, TiDB returns success with a warning such as "|Warning | 1292 | Truncated incorrect xxx: 'xx'" when a system variable is set to an illegal value.
- Fix the issue that the `SHOW VIEW` permission is not required to execute `SHOW CREATE VIEW`. Now you are expected to have the `SHOW VIEW` permission to execute the `SHOW CREATE VIEW` statement.
- The system variable `sql_auto_is_null` is added to the noop functions. When `tidb_enable_noop_functions = 0/OFF`, modifying this variable value causes an error.
- The `GRANT ALL ON performance_schema.*` syntax is no longer permitted. If you execute this statement in TiDB, an error occurs.
- Fix the issue that auto-analyze is unexpectedly triggered outside the specified time period when new indexes are added before v5.3.0. In v5.3.0, after you set the time period through the `tidb_auto_analyze_start_time` and `tidb_auto_analyze_end_time` variables, auto-analyze is triggered only during this time period.
- The default storage directory for plugins is changed from "" to /data/deploy/plugin.
- The DM code is migrated to [the folder "dm" in TiCDC code repository](https://github.com/pingcap/ticdc/tree/master/dm). Now DM follows TiDB in version numbers. Next to v2.0.x, the new DM version is v5.3.0, and you can upgrade from v2.0.x to v5.3.0 without any risk.

## New features

### SQL

- **Use SQL interface to set placement rules for data (experimental feature)**

    Support the `[CREATE | ALTER] PLACEMENT POLICY` syntax that provides a SQL interface to set placement rules for data. Using this feature, you can specify tables and partitions to be scheduled to specific regions, data centers, racks, hosts, or replica count rules. This meets your application demands for lower cost and higher flexibility. The typical user scenarios are as follows:

    - Merge multiple databases of different applications to reduce the cost on database maintenance, and achieve application resource isolation through the rule configuration
    - Increase replica count for important data to improve the application availability and data reliability
    - Store new data into SSDs and store old data into HHDs to lower the cost on data archiving and storage
    - Schedule the leaders of hotspot data to high-performance TiKV instances
    - Separate cold data to lower-cost storage mediums to improve cost efficiency

    [User document](/placement-rules-in-sql.md), [#18030](https://github.com/pingcap/tidb/issues/18030)

- **Temporary tables**

    Support the `CREATE [GLOBAL] TEMPORARY TABLE` statement to create temporary tables. Using this feature, you can easily manage the temporary data generated in the calculation process of an application. Temporary data is stored in memory and you can use the `tidb_tmp_table_max_size` variable to limit the size of a temporary table. TiDB supports the following types of temporary tables:

    - Global temporary tables
        - Visible to all sessions in the cluster, and table schemas are persistent.
        - Provides transaction-level data isolation. The temporary data is effective only in the transaction. After the transaction finishes, the data is automatically dropped.
    - Local temporary tables
        - Visible only to the current session, and tables schemas are not persistent.
        - Supports duplicated table names. You do not need to design complicated naming rules for your application.
        - Provides session-level data isolation, which enables you to design a simpler application logic. After the transaction finishes, the temporary tables are dropped.

        [User document](/temporary-tables.md), [#24169](https://github.com/pingcap/tidb/issues/24169)

- **Support the `FOR UPDATE OF TABLES` syntax**

    For a SQL statement that joins multiple tables, TiDB supports acquiring pessimistic locks on the rows correlated to the tables that are included in `OF TABLES`.

    [User document](/sql-statements/sql-statement-select.md), [#28689](https://github.com/pingcap/tidb/issues/28689)

- **Table attributes**

    Support the `ALTER TABLE [PARTITION] ATTRIBUTES` statement that allows you to set attributes for a table or partition. Currently, TiDB only supports setting the `merge_option` attribute. By adding this attribute, you can explicitly control the Region merge behavior.

    User scenarios: When you perform the `SPLIT TABLE` operation, if no data is inserted after a certain period of time, the empty Regions are automatically merged by default. In this case, you can set the table attribute to `merge_option=deny` to avoid the automatic merging of Regions.

    [User document](/table-attributes.md), [#3839](https://github.com/tikv/pd/issues/3839)

### Security

- **Support creating users with the least privileges on TiDB Dashboard**

The account system of TiDB Dashboard is consistent with that of TiDB SQL. Users accessing TiDB Dashboard are authenticated and authorized based on TiDB SQL users' privileges. Therefore, TiDB Dashboard requires limited privileges, or merely the read-only privilege. You can configure users to access TiDB Dashboard based on the principle of least privilege, thus avoiding access of high-privileged users.

It is recommended that you create a least-privileged SQL user to access and sign in with TiDB Dashboard. This avoids access of high-privileged users and improves security.

[User document](/dashboard/dashboard-user.md)

### Performance

- **Optimize the timestamp processing flow of PD**

    TiDB optimizes its timestamp processing flow and reduces the timestamp processing load of PD by enabling PD Follower Proxy and modifying the batch waiting time required when the PD client requests TSO in batches. This helps improve the overall scalability of the system.

    - Support enabling or disabling PD Follower Proxy through the system variable [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v53). Suppose that the TSO requests load of PD is too high. In this case, enabling PD follower proxy can batch forward the TSO requests collected during the request cycle on followers to the leader nodes. This solution can effectively reduce the number of direct interactions between clients and leaders, reduce the pressure of the load on leaders, and improve the overall performance of TiDB. 

    > **Note:**
    >
    > When the number of clients is small and the PD leader CPU load is not full, it is NOT recommended to enable PD Follower Proxy.

    - Support using the system variable [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v53) to set the maximum waiting time needed for the PD client to batch request TSO. The unit of this time is milliseconds. In case that PD has a high TSO requests load, you can reduce the load and improve the throughput by increasing the waiting time to get a larger batch size.

    > **Note:**
    >
    > When the TSO request load is not high, it is NOT recommended to modify this variable value.

    [User document](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v53), [#3149](https://github.com/tikv/pd/issues/3149)

### Stability

- **Support Online Unsafe Recovery after some stores are permanently damaged (experimental feature)**

    Support the `unsafe remove-failed-stores` command that performs online data unsafe recovery. Suppose that the majority of data replicas encounter issues like permanent damage (such as disk damage), and these issues cause the data ranges in an application to be unreadable or unwritable. In this case, you can use the Online Unsafe Recovery feature implemented in PD to recover the data, so that the data is readable or writable again.

    It is recommended to perform the feature-related operations with the support of the TiDB team.

[User document](/online-unsafe-recovery.md), [#10483](https://github.com/tikv/tikv/issues/10483)

### Data migration

- **DM replication performance enhanced**

    Supports the following features to ensure lower-latency data replication from MySQL to TiDB:

    - Compact multiple updates on a single row into one statement
    - Merge batch updates of multiple rows into one statement

- **Add DM OpenAPI to better maintain DM clusters (experimental feature)**

    DM provides the OpenAPI feature for querying and operating the DM cluster. It is similar to the feature of [dmctl tools](https://docs.pingcap.com/zh/tidb-data-migration/stable/dmctl-introduction).

    Currently, DM OpenAPI is an experimental feature and disabled by default. It is not recommended to use it in a production environment.

    [User Document](https://docs.pingcap.com/zh/tidb-data-migration/stable/open-api)

- **TiDB Lightning Parallel Import**

    TiDB Lightning provides parallel import capability to extend the original feature. It allows you to deploy multiple Lightning instances at the same time to import single tables or multiple tables to downstream TiDB in parallel. Without changing the way customers use it, it greatly improves the data migration ability, allowing you to migrate data in a more real-time way to further process, integrate and analyze them. It improves the efficiency of enterprise data management.

    In our test, using 10 TiDB Lightning instances, a total of 20 TiB MySQL data can be imported to TiDB within 8 hours. The performance of multiple table import is also improved. A single TiDB Lightning instance can support importing at 250 GB/s, and the overall migration is 8 times faster than the original performance.

    [User Document](/tidb-lightning/tidb-lightning-distributed-import.md)

- **TiDB Lightning Prechecks**

    TiDB Lightning provides the ability to check the configuration before running a migration task. It is enabled by default. This feature automatically performs some routine checks for disk space and execution configuration. The main purpose is to ensure that the whole subsequent import process goes smoothly.

    [User Document](/tidb-lightning/tidb-lightning-prechecks.md)

- **TiDB Lightning supports importing files of GBK character set**

    You can specify the character set of the source data file. TiDB Lightning will convert the source file from the specified character set to UTF-8 encoding during the import process.

    [User Document](/tidb-lightning/tidb-lightning-configuration.md)

- **Sync-diff-inspector improvement**

    - Improve the comparison speed from 375 MB/s to 700 MB/s
    - Reduce the memory consumption of TiDB nodes by nearly half during comparison
    - Optimize the user interface and display the progress bar during comparison

    [User Document](/sync-diff-inspector/sync-diff-inspector-overview.md)

### Diagnostic efficiency

- **Save and restore the on-site information of a cluster**

    When you locate and troubleshoot the issues of a TiDB cluster, you often need to provide information on the system and the query plan. To help you get the information and troubleshoot cluster issues in a more convenient and efficient way, the `PLAN REPLAY` command is introduced in TiDB v5.3.0. This command enables you to easily save and restore the on-site information of a cluster, improves the efficiency of troubleshooting, and helps you more easily archive the issues for management.

    The features of `PLAN REPLAYER` are as follows:

    - Exports the information of a TiDB cluster at an on-site troubleshooting to a ZIP-formatted file for storage.
    - Imports into a cluster the ZIP-formatted file exported from another TiDB cluster. This file contains the information of the latter TiDB cluster at an on-site troubleshooting.

    [User document](/sql-plan-replayer.md), [#26325](https://github.com/pingcap/tidb/issues/26325)

### TiDB data share subscription

- **TiCDC Eventually Consistent Replication**

    TiCDC provides the eventually consistent replication capability in disaster scenarios. When a disaster occurs in the primary TiDB cluster and the service cannot be resumed in a short period of time, TiCDC needs to provide the ability to ensure the consistency of data in the secondary cluster. Meanwhile, TiCDC needs to allow the business to quickly switch the traffic to the secondary cluster to avoid the database being unavailable for a long time and affecting the business.

    This feature supports TiCDC to replicate incremental data from a TiDB cluster to the secondary relational database TiDB/Aurora/MySQL/MariaDB. In case the primary cluster crashes, TiCDC can recover the secondary cluster to a certain snapshot in the primary cluster within 5 minutes, given the condition that before disaster the replication status of TiCDC is normal and replication lag is small. It allows data loss of less than 30 minutes, that is, RTO <= 5min, and RPO <= 30min.

    [User Document](/ticdc/manage-ticdc.md)

- **TiCDC supports the HTTP protocol OpenAPI for managing TiCDC tasks**

    Since TiDB v5.3.0, TiCDC OpenAPI becomes an General Availability (GA) feature. You can query and operate TiCDC clusters using OpenAPI in the production environment.

### Deployment and maintenance

- **Continuous Profiling (experimental feature)**

    TiDB Dashboard supports the Continuous Profiling feature, which stores instance performance analysis results automatically in real time when TiDB clusters are running. You can check the performance analysis result in a flame graph, which is more observable and shortens troubleshooting time.

    This feature is disabled by default and needs to be enabled on the **Continuous Profile** page of TiDB Dashboard.

    This feature is only available for clusters upgraded or installed using TiUP v1.7.0 or above.

    [User document](/dashboard/continuous-profiling.md)

## Telemetry

TiDB adds the information to the telemetry report about whether or not the TEMPORARY TABLE feature is used. This does not include table names or table data.

To learn more about telemetry and how to disable this behavior, refer to [Telemetry](/telemetry.md).

## Removed feature

Starting from TiCDC v5.3.0, the cyclic replication feature between TiDB clusters (an experimental feature in v5.0.0) has been removed. If you have already used this feature to replicate data before upgrading TiCDC, the related data is not affected after the upgrade.

## Improvements

+ TiDB

    - Show the affected SQL statements in the debug log when the coprocessor encounters a lock, which is helpful in diagnosing problems [#27718](https://github.com/pingcap/tidb/issues/27718)
    - Support showing the size of the backup and restore data when backing up and restoring data in the SQL logical layer [#27247](https://github.com/pingcap/tidb/issues/27247)
    - Improve the default collection logic of ANALYZE when `tidb_analyze_version` is `2`, which accelerates collection and reduces resource overhead
    - Introduce the `ANALYZE TABLE table_name COLUMNS col_1, col_2, ... , col_n` syntax. The syntax allows collecting statistics only on a portion of the columns in wide tables, which improves the speed of statistics collection

+ TiKV

    - Enhance disk space protection to improve storage stability

        To solve the issue that TiKV might panic in case of a disk fully-written error, TiKV introduces a two-level threshold defense mechanism to protect the disk remaining space from being exhausted by excess traffic. Additionally, the mechanism provides the ability to reclaim space when the threshold is triggered. When the remaining space threshold is triggered, some write operations will fail and TiKV will return a disk full error as well as a list of disk full nodes. In this case, to recover the space and restore the service, you can execute `Drop/Truncate Table` or scale out the nodes.

    - Simplify the algorithm of L0 flow control [#10879](https://github.com/tikv/tikv/issues/10879)
    - Improve the error log report in the raft client module [#10944](https://github.com/tikv/tikv/pull/10944)
    - Improve logging threads to avoid them becoming a performance bottleneck [#10841](https://github.com/tikv/tikv/issues/10841)
    - Add more statistics types of write queries [#10507](https://github.com/tikv/tikv/issues/10507)

+ PD

    - Add more types of write queries to QPS dimensions in the hotspot scheduler [#3869](https://github.com/tikv/pd/issues/3869)
    - Support dynamically adjusting the retry limit of the balance region scheduler to improve the performance of the scheduler [#3744](https://github.com/tikv/pd/issues/3744)
    - Update TiDB Dashboard to v2021.10.08.1 [#4070](https://github.com/tikv/pd/pull/4070)
    - Support that the evict leader scheduler can schedule regions with unhealthy peers [#4093](https://github.com/tikv/pd/issues/4093)
    - Speed up the exit process of schedulers [#4146](https://github.com/tikv/pd/issues/4146)

+ TiFlash

    - Improve the execution efficiency of the TableScan operator greatly
    - Improve the execution efficiency of the Exchange operator
    - Reduce write amplification and memory usage during GC of the storage engine (experimental feature)
    - Improve the stability and availability of TiFlash when TiFlash restarts, which reduces possible query failures following the restart
    - Support pushing down multiple new String and Time functions to the MPP engine

        - String functions: LIKE pattern, FORMAT(), LOWER(), LTRIM(), RTRIM(), SUBSTRING_INDEX(), TRIM(), UCASE(), UPPER()
        - Mathematical functions: ROUND (decimal, int)
        - Date and time functions: HOUR(), MICROSECOND(), MINUTE(), SECOND(), SYSDATE()
        - Type conversion function: CAST(time, real)
        - Aggregation functions: GROUP_CONCAT(), SUM(enum)

    - Support 512-bit SIMD
    - Enhance the cleanup algorithm for outdated data to reduce disk usage and read files more efficiently
    - Fix the issue that dashboard does not display memory or CPU information in some non-Linux systems
    - Unify the naming style of TiFlash log files (keep the naming style consistent with that of TiKV) and support dynamic modification of logger.count and logger.size
    - Improve the data validation capability of column-based files (checksums, experimental feature)

+ Tools

    + TiCDC

        - Reduce the default value of the Kafka sink configuration item `MaxMessageBytes` from 64 MB to 1 MB to fix the issue that large messages are rejected by the Kafka Broker [#3104](https://github.com/pingcap/ticdc/pull/3104)
        - Reduce memory usage in the replication pipeline [#2553](https://github.com/pingcap/ticdc/issues/2553)[#3037](https://github.com/pingcap/ticdc/pull/3037) [#2726](https://github.com/pingcap/ticdc/pull/2726)
        - Optimize monitoring items and alert rules to improve observability of synchronous links, memory GC, and stock data scanning processes [#2735](https://github.com/pingcap/ticdc/pull/2735) [#1606](https://github.com/pingcap/ticdc/issues/1606) [#3000](https://github.com/pingcap/ticdc/pull/3000) [#2985](https://github.com/pingcap/ticdc/issues/2985) [#2156](https://github.com/pingcap/ticdc/issues/2156)
        - When the sync task status is normal, no more historical error messages are displayed to avoid misleading users [#2242](https://github.com/pingcap/ticdc/issues/2242)

## Bug Fixes

+ TiDB

    - Fix an error that occurs during execution caused by the wrong execution plan. The wrong execution plan is caused by the shallow copy of schema columns when pushing down the aggregation operators on partitioned tables. [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)
    - Fix the issue that plan-cache cannot detect changes of unsigned flags [#28254](https://github.com/pingcap/tidb/issues/28254)
    - Fix the wrong partition pruning when the partition function is out of range [#28233](https://github.com/pingcap/tidb/issues/28233)
    - Fix the issue that planner might cache invalid plans for `join` in some cases [#28087](https://github.com/pingcap/tidb/issues/28087)
    - Fix wrong index hash join when hash column type is enum [#27893](https://github.com/pingcap/tidb/issues/27893)
    - Fix a batch client bug that recycling idle connection might block sending requests in some rare cases [#27688](https://github.com/pingcap/tidb/pull/27688)
    - Fix the TiDB Lightning panic issue when it fails to perform checksum on a target cluster [#27686](https://github.com/pingcap/tidb/pull/27686)
    - Fix wrong results of the `date_add` and `date_sub` functions in some cases [#27232](https://github.com/pingcap/tidb/issues/27232)
    - Fix wrong results of the `hour` function in vectorized expression [#28643](https://github.com/pingcap/tidb/issues/28643)
    - Fix the authenticating issue when connecting to MySQL 5.1 or an older client version  [#27855](https://github.com/pingcap/tidb/issues/27855)
    - Fix the issue that auto analyze might be triggered out of the specified time when a new index is added [#28698](https://github.com/pingcap/tidb/issues/28698)
    - Fix a bug that setting any session variable invalidates `tidb_snapshot` [#28683](https://github.com/pingcap/tidb/pull/28683)
    - Fix a bug that BR is not working for clusters with many missing-peer regions [#27534](https://github.com/pingcap/tidb/issues/27534)
    - Fix  the unexpected error like `tidb_cast to Int32 is not supported` when the unsupported `cast` is pushed down to TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)
    - Fix the issue that `DECIMAL overflow` is missing in the `%s value is out of range in '%s'`error message  [#27964](https://github.com/pingcap/tidb/issues/27964)
    - Fix a bug that the availability detection of MPP node does not work in some corner cases [#3118](https://github.com/pingcap/tics/issues/3118)
    - Fix the `DATA RACE` issue when assigning `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)
    - Fix the `INDEX OUT OF RANGE` error for a MPP query after deleting an empty `dual table`. [#28250](https://github.com/pingcap/tidb/issues/28250)
    - Fix the issue of false positive error log `invalid cop task execution summaries length` for MPP queries [#1791](https://github.com/pingcap/tics/issues/1791)
    - Fix the issue of error log `cannot found column in Schema column` for MPP queries [#28149](https://github.com/pingcap/tidb/pull/28149)
    - Fix the issue that TiDB might panic when TiFlash is shuting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Remove the support for insecure 3DES (Triple Data Encryption Algorithm) based TLS cipher suites [#27859](https://github.com/pingcap/tidb/pull/27859)
    - Fix the issue that Lightning connects to offline TiKV nodes during pre-check and causes import failures [#27826](https://github.com/pingcap/tidb/pull/27826)
    - Fix the issue that pre-check cost too much time when importing many files to tables [#27605](https://github.com/pingcap/tidb/issues/27605)
    - Fix the issue that rewriting expressions makes `between` infer wrong collation [#27146](https://github.com/pingcap/tidb/issues/27146)
    - Fix the issue that `group_concat` function did not consider the collation [#27429](https://github.com/pingcap/tidb/issues/27429)
    - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
    - Fix the issue that creating partition fails if `NO_UNSIGNED_SUBTRACTION` is set [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Avoid expressions with side effects in column pruning and aggregation pushdown [#27106](https://github.com/pingcap/tidb/issues/27106)
    - Remove useless gRPC logs [#24190](https://github.com/pingcap/tidb/issues/24190)
    - Limit the valid decimal length to fix precision-related issues [#3091](https://github.com/pingcap/tics/issues/3091)
    - Fix the issue of a wrong way to check for overflow in `plus` expression [#26977](https://github.com/pingcap/tidb/issues/26977)
    - Fix the issue of `data too long` error when dumping statistics from the table with `new collation` data [#27024](https://github.com/pingcap/tidb/issues/27024)
    - Fix the issue that the retried transactions' statements are not included in `TIDB_TRX` [#28670](https://github.com/pingcap/tidb/pull/28670)
    - Fix the wrong default value of the `plugin_dir` configuration [28084](https://github.com/pingcap/tidb/issues/28084)

+ TiKV

    - Fix the issue of unavailable TiKV caused by Raftstore deadlock when migrating Regions. The workaround is to disable the scheduling and restart the unavailable TiKV. [#10909](https://github.com/tikv/tikv/issues/10909)
    - Fix the issue that CDC adds scan retries frequently due to the Congest error [#11082](https://github.com/tikv/tikv/issues/11082)
    - Fix the issue that the Raft connection is broken when the channel is full [#11047](https://github.com/tikv/tikv/issues/11047)
    - Fix the issue that batch messages are too large in Raft client implementation [#9714](https://github.com/tikv/tikv/issues/9714)
    - Fix the issue that some coroutines leak in `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)
    - Fix a panic issue that occurs to the coprocessor when the size of response exceeds 4 GiB [#9012](https://github.com/tikv/tikv/issues/9012)
    - Fix the issue that snapshot Garbage Collection (GC) misses GC snapshot files when snapshot files cannot be garbage collected [#10813](https://github.com/tikv/tikv/issues/10813)
    - Fix a panic issue caused by timeout when processing Coprocessor requests [#10852](https://github.com/tikv/tikv/issues/10852)
    - Fix a memory leak caused by monitoring data of statistics threads [#11195](https://github.com/tikv/tikv/issues/11195)
    - Fix a panic issue caused by getting the cgroup information from some platforms [#10980](https://github.com/tikv/tikv/pull/10980)
    - Fix the issue of poor scan performance because MVCC Deletion versions are not dropped by compaction filter GC [#11248](https://github.com/tikv/tikv/pull/11248)

+ PD

    - Fix the issue that PD incorrectly delete the peers with data and in pending status because the number of peers exceeds the number of configured peers [#4045](https://github.com/tikv/pd/issues/4045)
    - Fix the issue that PD does not fix down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the issue that the scatter range scheduler cannot schedule empty regions [#4118](https://github.com/tikv/pd/pull/4118)
    - Fix the issue that the key manager cost too much CPU [#4071](https://github.com/tikv/pd/issues/4071)
    - Fix the data race issue that might occur when setting configurations of hot region scheduler [#4159](https://github.com/tikv/pd/issues/4159)
    - Fix slow leader election caused by stucked region syncer[#3936](https://github.com/tikv/pd/issues/3936)

+ TiFlash

    - Fix the issue of inaccurate TiFlash Store Size statistics
    - Fix the issue that TiFlash fails to start up on some platforms due to the absence of library `nsl`
    - Block the infinite wait of `wait index` when writing pressure is heavy (a default timeout of 5 minutes is added), which prevents TiFlash from waiting too long for data replication to provide services
    - Fix the slow and no result issues of the log search when the log volume is large
    - Fix the issue that only the most recent logs can be searched when searching old historical logs
    - Fix the possible wrong result when a new collation is enabled
    - Fix the possible parsing errors when an SQL statement contains extremely long nested expressions
    - Fix the possible `Block schema mismatch` error of the Exchange operator
    - Fix the possible `Can't compare` error when comparing Decimal types
    - Fix the `3rd arguments of function substringUTF8 must be constants` error of the `left/substring` function

+ Tools

    + TiCDC

        - Fix the issue that TiCDC replication task might terminate when the upstream TiDB instance unexpectedly exits [#3061](https://github.com/pingcap/ticdc/issues/3061)
        - Fix the issue that TiCDC process might panic when TiKV sends duplicate requests to the same Region [#2386](https://github.com/pingcap/ticdc/issues/2386)
        - Fix unnecessary CPU consumption when verifying downstream TiDB/MySQL availability [#3073](https://github.com/pingcap/ticdc/issues/3073)
        - Fix the issue that the volume of Kafka messages generated by TiCDC is not constrained by `max-message-size` [#2962](https://github.com/pingcap/ticdc/issues/2962)
        - Fix the issue that TiCDC sync task might pause when an error occurs during writing a Kafka message [#2978](https://github.com/pingcap/ticdc/issues/2978)
        - Fix the issue that some partitioned tables without valid indexes might be ignored when `force-replicate` is enabled [#2834](https://github.com/pingcap/ticdc/issues/2834)
        - Fix the issue that scanning stock data might fail due to TiKV performing GC when scanning stock data takes too long [#2470](https://github.com/pingcap/ticdc/issues/2470)
        - Fix a possible panic issue when encoding some types of columns into Open Protocol format [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - Fix a possible panic issue when encoding some types of columns into Avro format [#2648](https://github.com/pingcap/ticdc/issues/2648)

    + TiDB Binlog

        - Fix the issue that when most tables are filtered out, checkpoint can not be updated under some special load [#1075](https://github.com/pingcap/tidb-binlog/pull/1075)
