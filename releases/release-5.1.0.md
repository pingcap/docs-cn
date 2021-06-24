---
title: TiDB 5.1 Release Notes
---

# TiDB 5.1 Release Notes

Release date: June 24, 2021

TiDB version: 5.1.0

In v5.1, the key new features or improvements are as follows:

- Support the Common Table Expression (CTE) feature of MySQL 8.0 to improve the readability and execution efficiency of SQL statements.
- Support changing column types online to improve code development flexibility.
- Introduce a new statistics type to improve query stability, which is enabled as an experimental feature by default.
- Support the dynamic privilege feature of MySQL 8.0 to implement more fine-grained control over certain operations.
- Support directly reading data from the local replica using the Stale Read feature to reduce read latency and improve query performance (Experimental).
- Add the Lock View feature to facilitate database administrators (DBAs) to observe transaction locking events and troubleshoot deadlock problems (Experimental).
- Add TiKV write rate limiter for background tasks to ensure that the latency of read and write requests is stable.

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v5.1, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/releases/release-notes.md) for the corresponding version. 

### System variables

| Variable name   | Change type   | Description   |
|:----------|:-----------|:-----------|
| [`cte_max_recursion_depth`](/system-variables.md#cte_max_recursion_depth)  | Newly added | Controls the maximum recursion depth in Common Table Expressions. |
| [`init_connect`](/system-variables.md#init_connect)  | Newly added | Controls the initial connection to a TiDB server. |
| [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)  | Newly added | Controls how TiDB collects statistics. The default value of this variable is `2`. This is an experimental feature. |
| [`tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security) | Newly added | Indicates whether the TiDB server you are connected to has the Security Enhanced Mode (SEM) enabled. This variable setting cannot be changed without restarting the TiDB server. |
| [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51) | Newly added | Controls whether to ignore the optimizer's cost estimation and to forcibly use the MPP mode for query execution. The data type of this variable is `BOOL` and the default value is `false`. |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51) | Newly added | Specifies whether to enable dynamic prune mode for partitioned tables. This feature is experimental. The default value of this variable is `static`, which means the dynamic mode for partitioned tables is disabled by default.  |

### Configuration file parameters

| Configuration file | Configuration item | Change type   | Description   |
|:----------|:-----------|:-----------|:-----------|
| TiDB configuration file | [`security.enable-sem`](/tidb-configuration-file.md#enable-sem)  | Newly added  | Controls whether to enable the Security Enhanced Mode (SEM). The default value of this configuration item is `false`, which means the SEM is disabled. |
| TiDB configuration file | [`performance.committer-concurrency`](/tidb-configuration-file.md#committer-concurrency)  | Modified  | Controls the concurrency number for requests related to commit operations in the commit phase of a single transaction. The default value is changed from `16` to `128`. |
| TiDB configuration file | [`performance.tcp-no-delay`](/tidb-configuration-file.md#tcp-no-delay)  | Newly added  | Determines whether to enable TCP_NODELAY at the TCP layer. The default value is `true`, which means TCP_NODELAY is enabled. |
| TiDB configuration file | [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)  | Newly added  | Controls whether TiDB ignores cost estimates of Optimizer at the instance level and enforces the MPP mode. The default value is `false`. |
| TiDB configuration file | [`pessimistic-txn.deadlock-history-capacity`](/tidb-configuration-file.md#deadlock-history-capacity)  | Newly added  | Sets the maximum number of deadlock events that can be recorded in the [`INFORMATION_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) table of a single TiDB server. The default value is `10`. |
| TiKV configuration file | [`abort-on-panic`](/tikv-configuration-file.md#abort-on-panic)  | Newly added  | Sets whether the `abort` process allows the system to generate core dump files when TiKV panics. The default value is `false`, which means it is not allowed to generate core dump files. |
| TiKV configuration file | [`hibernate-regions`](/tikv-configuration-file.md#hibernate-regions)  | Modified  | The default value is changed from `false` to `true`. If a Region is idle for a long time, it is automatically set as hibernated. |
| TiKV configuration file | [`old-value-cache-memory-quota`](/tikv-configuration-file.md#old-value-cache-memory-quota)  | Newly added  | Sets the upper limit of memory usage by TiCDC old values. The default value is `512MB`. |
| TiKV configuration file | [`sink-memory-quota`](/tikv-configuration-file.md#sink-memory-quota)  | Newly added  | Sets the upper limit of memory usage by TiCDC data change events. The default value is `512MB`. |
| TiKV configuration file | [`incremental-scan-threads`](/tikv-configuration-file.md#incremental-scan-threads)  | Newly added  | Sets the number of threads for the task of incrementally scanning historical data. The default value is `4`, which means there are four threads for the task.  |
| TiKV configuration file | [`incremental-scan-concurrency`](/tikv-configuration-file.md#incremental-scan-concurrency)  | Newly added  | Sets the maximum number of concurrent executions for the tasks of incrementally scanning historical data. The default value is `6`, which means that six tasks can be concurrently executed at most. |
| TiKV configuration file | [`soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)  | Modified  | The soft limit on the pending compaction bytes. The default value is changed from `"64GB"` to `"192GB"`. |
| TiKV configuration file | [`storage.io-rate-limit`](/tikv-configuration-file.md#storageio-rate-limit)  | Newly added  | Controls the I/O rate of TiKV writes. The default value of `storage.io-rate-limit.max-bytes-per-sec` is `"0MB"`. |
| TiKV configuration file | [`resolved-ts.enable`](/tikv-configuration-file.md#enable)  | Newly added  | Determines whether to maintain the `resolved-ts` for all Region leaders. The default value is `true`. |
| TiKV configuration file | [`resolved-ts.advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval)  | Newly added  | The interval at which the `resolved-ts` is forwarded. The default value is `"1s"`. You can change the value dynamically. |
| TiKV configuration file | [`resolved-ts.scan-lock-pool-size`](/tikv-configuration-file.md#scan-lock-pool-size)  | Newly added  | The number of threads that TiKV uses to scan the MVCC (multi-version concurrency control) lock data when initializing the `resolved-ts`. The default value is `2`. |

### Others

- Upgrade the Go compiler version of TiDB from go1.13.7 to go1.16.4, which improves the TiDB performance. If you are a TiDB developer, upgrade your Go compiler version to ensure a smooth compilation. 
- Avoid creating tables with clustered indexes in the cluster that uses TiDB Binlog during the TiDB rolling upgrade.
- Avoid executing statements like `alter table ... modify column` or `alter table ... change column` during the TiDB rolling upgrade.
- Since v5.1, setting the replica of system tables, when building TiFlash replicas for each table, is no longer supported. Before upgrading the cluster, you need to clear the relevant system table replicas; otherwise, the upgrade will fail.
- Deprecate the `--sort-dir` parameter in the `cdc cli changefeed` command of TiCDC. Instead, you can set `--sort-dir` in the `cdc server` command. [#1795](https://github.com/pingcap/ticdc/pull/1795)

## New features

### SQL

- Support the Common Table Expression (CTE) feature of MySQL 8.0, which empowers TiDB with the capability of querying hierarchical data recursively or non-recursively. 

    This feature meets the needs of using tree queries to implement application logics in multiple sectors such as human resources, manufacturing, financial markets, and education. 
[User document](/sql-statements/sql-statement-with.md), [#17472](https://github.com/pingcap/tidb/issues/17472)

- Support the dynamic privilege feature of MySQL 8.0. 

    Dynamic privileges are used to limit the `SUPER` privilege and provide TiDB with more flexible privilege configuration for more fine-grained access control. For example, you can use dynamic privileges to create a user account that can only perform `BACKUP` and `RESTORE` operations.

    The supported dynamic privileges are as follows:

    - `BACKUP_ADMIN`
    - `RESTORE_ADMIN`
    - `ROLE_ADMIN`
    - `CONNECTION_ADMIN`
    - `SYSTEM_VARIABLES_ADMIN`

    You can also use plugins to add new privileges. To check out all supported privileges, execute the `SHOW PRIVILEGES` statement. [User document](/privilege-management.md)

- Add a new configuration item for the Security Enhanced Mode (SEM), which divides the TiDB administrator privileges in a finer-grained way. 

    The Security Enhanced Mode is disabled by default. To enable it, see the [user document](/system-variables.md#tidb_enable_enhanced_security).

- Enhance the capability of changing column types online. Support changing the column type online using the `ALTER TABLE` statement, including but not limited to:

    - Changing `VARCHAR` to `BIGINT`
    - Modifying the `DECIMAL` precision
    - Compressing the length of `VARCHAR(10)` to `VARCHAR(5)`

    [User document](/sql-statements/sql-statement-modify-column.md)

- Introduce a new SQL syntax `AS OF TIMESTAMP` to perform Stale Read, a new experimental feature used to read historical data from a specified point in time or from a specified time range.

    [User document](/stale-read.md), [#21094](https://github.com/pingcap/tidb/issues/21094)

    The examples of `AS OF TIMESTAMP` are as follows:

    ```sql
    SELECT * FROM t AS OF TIMESTAMP  '2020-09-06 00:00:00';
    START TRANSACTION READ ONLY AS OF TIMESTAMP '2020-09-06 00:00:00';
    SET TRANSACTION READ ONLY as of timestamp '2020-09-06 00:00:00';
    ```

- Introduce a new statistics type `tidb_analyze_version = 2` (Experimental).

    `tidb_analyze_version` is set to `2` by default, which avoids the large errors that might occur in the large data volume caused by hash conflicts in Version 1 and maintains the estimation accuracy in most scenarios.

    [User document](/statistics.md)

### Transaction

+ Support the Lock View feature (Experimental)

    The Lock View feature provides more information about lock conflicts and lock waits of pessimistic locks, which helps DBAs to observe transaction locking conditions and troubleshoot deadlock problems. [#24199](https://github.com/pingcap/tidb/issues/24199)

    User document:

    - View the pessimistic locks and other locks that currently occur on all TiKV nodes in the clusters: [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    - View several deadlock errors that recently occurred on the TiDB nodes: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    - View the transaction information executed currently on the TiDB nodes: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### Performance

+ Stale read of data replicas (Experimental)

    Read local replicas data directly to reduce read latency and improve the query performance
    [User document](/stale-read.md), [#21094](https://github.com/pingcap/tidb/issues/21094)

+ Enable the Hibernate Region feature by default.

    If a Region is in an inactive state for a long time, it is automatically set to a silent state, which reduces the system overhead of the heartbeat information between the Leader and the Follower.
    [User document](/tikv-configuration-file.md#hibernate-regions)，[#10266](https://github.com/tikv/tikv/pull/10266)

### Stability

+ Solve the replication stability issue of TiCDC

    - Improve TiCDC memory usage to avoid OOM in the following scenarios
    - If large amounts of data is accumulated during the replication interruption, exceeding 1TB, the re-replication causes OOM problems.
    - Large amounts of data writes cause OOM problems in TiCDC.
    - Reduce the possibility of  TiCDC replication interruption in the following scenarios:
        [project#11](https://github.com/pingcap/ticdc/projects/11)
       
        - Replication interruption when the network is unstable
        - Replication interruption when some TiKV/PD/TiCDC nodes are down

+ TiFlash storage memory control

    Optimize the speed and memory usage of Region snapshot generation and reduce the possibility of OOM

+ Add a write rate limiter for TiKV background tasks (TiKV Write Rate Limiter)

    To ensure the duration stability of read and write requests, TiKV Write Rate Limiter smoothes the write traffic of TiKV background tasks such as GC and Compaction. The default value of TiKV background task write rate limiter is "0MB". It is recommended to set this value to the optimal I/O bandwidth of the disk, such as the maximum I/O bandwidth specified by the cloud disk manufacturer.
    [User document](/tikv-configuration-file.md#storageio-rate-limit), [#9156](https://github.com/tikv/tikv/issues/9156)

+ Solve scheduling stability issues when multiple scaling tasks are performed at the same time

### Telemetry

TiDB adds the running status of TiDB cluster requests in telemetry, including execution status, failure status, etc.

To learn more about the information and how to disable this behavior, refer to [Telemetry](https://docs.pingcap.com/zh/tidb/stable/telemetry).

## Improvements

+ TiDB

    - Support the built-in function `VITESS_HASH()` [#23915](https://github.com/pingcap/tidb/pull/23915)
    - Support pushing down data of the enumerated type to TiKV to improve performance when using enumerated types in `WHERE` clauses [#23619](https://github.com/pingcap/tidb/issues/23619)
    - Optimize the calculation of Window Function to solve TiDB OOM problems when paging data with ROW_NUMBER() [#23807](https://github.com/pingcap/tidb/issues/23807)
    - Optimize the calculation of `UNION ALL` to solve the TiDB OOM problems when using `UNION ALL` to join a large number of `SELECT` statements [#21441](https://github.com/pingcap/tidb/issues/21441)
    - Optimize the dynamic mode of partitioned tables to improve performance and stability [#24150](https://github.com/pingcap/tidb/issues/24150)
    - Fix the `Region is Unavailable` issue that occurs in multiple scenarios [project#62](https://github.com/pingcap/tidb/projects/62)
    - Fix multiple `Region is Unavailable` issues that might occur in frequent scheduling situations
    - Fix `Region is Unavailable` issue that might occur in some high stress write situations
    - Avoid frequently reading the `mysql.stats_histograms` table if the cached statistics is up-to-date to avoid high CPU usage [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiKV

    - Use `zstd` to compress Region snapshots, preventing large space differences between nodes in case of heavy scheduling or scaling [#10005](https://github.com/tikv/tikv/pull/10005)
    - Solve OOM issues in multiple cases [#10183](https://github.com/tikv/tikv/issues/10183)

        - Add memory usage tracking for each module
        - Solve the OOM issue caused by oversized Raft entries cache
        - Solve the OOM issue caused by stacked GC tasks
        - Solve the OOM issue caused by fetching too many Raft entries from the Raft log to memory at one time

    - Split Regions more evenly to mitigate the issue that the growth of Region size exceeds the splitting speed when there are hotspot writes [#9785](https://github.com/tikv/tikv/issues/9785)

+ TiFlash

    - Support `Union All`, `TopN`, and `Limit` functions
    - Support the Cartesian product including left outer join and semi anti join in MPP mode
    - Optimize lock operations to avoid that running DDL statements and read operations are blocked by each other
    - Optimize cleanup of expired data by TiFlash 
    - Support further filtering of query filters on `timestamp` columns at the TiFlash storage level
    - Improve the startup and scalability speed of TiFlash when a large number of tables are in a cluster
    - Improve TiFlash compatibility when running on unknown CPUs

+ PD

    - Avoid unexpected statistics after adding the `scatter region` scheduler [#3602](https://github.com/pingcap/pd/pull/3602)
    - Solve multiple scheduling issues in the scaling process

        - Optimize the generation process of replica snapshots to solve slow scheduling issues during scaling [#3563](https://github.com/tikv/pd/issues/3563) [#10059](https://github.com/tikv/tikv/pull/10059) [#10001](https://github.com/tikv/tikv/pull/10001)
        - Solve slow scheduling issues caused by heartbeat pressure due to traffic changes [#3693](https://github.com/tikv/pd/issues/3693) [#3739](https://github.com/tikv/pd/issues/3739) [#3728](https://github.com/tikv/pd/issues/3728) [#3751](https://github.com/tikv/pd/issues/3751)
        - Reduce the space discrepancies of large clusters due to scheduling, and optimize the scheduling formula to prevent the bursting issue (which is similar to heterogeneous space clusters) caused by large compression rate discrepancies [#3592](https://github.com/tikv/pd/issues/3592) [#10005](https://github.com/tikv/tikv/pull/10005)

+ Tools

    + Backup & Restore (BR)

        - Support backing up and restoring system tables in the `mysql` schema [#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)
        - Support the S3-compatible storage that is based on the virtual-host addressing mode [#10243](https://github.com/tikv/tikv/pull/10243)
        - Optimize the format of backupmeta to reduce memory usage [#1171](https://github.com/pingcap/br/pull/1171)

    + TiCDC

        - Improve the descriptions of some log messages to be clearer and more useful for diagnosing problems [#1759](https://github.com/pingcap/ticdc/pull/1759)
        - Support the back pressure feature to allow the TiCDC scanning speed to sense the downstream processing capacity [#10151](https://github.com/tikv/tikv/pull/10151)
        - Reduce memory usage when TiCDC performs the initial scan  [#10133](https://github.com/tikv/tikv/pull/10133)
        - Improve the cache hit rate for the TiCDC Old Value in pessimistic transactions [#10089](https://github.com/tikv/tikv/pull/10089)

    + Dumpling

        - Improve the logic of exporting data from TiDB v4.0 to avoid TiDB becoming out of memory (OOM) [#273](https://github.com/pingcap/dumpling/pull/273)

        - Fix the issue that no error is output when a backup operation fails [#280](https://github.com/pingcap/dumpling/pull/280)

    + TiDB Lightning

        - Improve data importing speed. The optimization results show that the speed of importing TPC-C data is increased by 30%, and the speed of importing large tables (2TB+) with more indexes (5 indexes) is increased by more than 50%. [#753](https://github.com/pingcap/br/pull/753)
        - Add a pre-check on the data to be imported and also on the target cluster before importing, and report errors to reject the import process if it does not meet the import requirements [#999](https://github.com/pingcap/br/pull/999)
        - Optimize the timing of checkpoint updates on the Local backend to improve performance of restarting from breakpoints[#1080](https://github.com/pingcap/br/pull/1080)

## Bug Fixes

+ TiDB

    - Fix the issue that the execution result of project elimination might be wrong when the projection result is empty [#23887](https://github.com/pingcap/tidb/issues/23887)
    - Fix the issue of wrong query results when a column contains `NULL` values in some cases [#23891](https://github.com/pingcap/tidb/issues/23891)
    - Forbid generating MPP plans when the scan contains virtual columns [#23886](https://github.com/pingcap/tidb/issues/23886)
    - Fix the wrong reuse of `PointGet` and `TableDual` in Plan Cache [#23187](https://github.com/pingcap/tidb/issues/23187) [#23144](https://github.com/pingcap/tidb/issues/23144) [#23304](https://github.com/pingcap/tidb/issues/23304) [#23290](https://github.com/pingcap/tidb/issues/23290)
    - Fix the error that occurs when the optimizer builds the `IndexMerge` plan for clustered indexes [#23906](https://github.com/pingcap/tidb/issues/23906)
    - Fix the type inference of the BIT-type errors [#23832](https://github.com/pingcap/tidb/issues/23832)
    - Fix the issue that some optimizer hints do not take effect when the `PointGet` operator exists [#23570](https://github.com/pingcap/tidb/issues/23570)
    - Fix the issue that DDL operations might fail when rolling back due to an error [#23893](https://github.com/pingcap/tidb/issues/23893)
    - Fix the issue that the index range of the binary literal constant is incorrectly built [#23672](https://github.com/pingcap/tidb/issues/23672)
    - Fix the potential wrong results of the `IN` clause in some cases [#23889](https://github.com/pingcap/tidb/issues/23889)
    - Fix the wrong results of some string functions [#23759](https://github.com/pingcap/tidb/issues/23759)
    - Users now need both `INSERT` and `DELETE` privileges on a table to perform `REPLACE` operations [#23909](https://github.com/pingcap/tidb/issues/23909)
    - Users now need both `INSERT` and `DELETE` privileges on a table to perform `REPLACE` operations [#24070](https://github.com/pingcap/tidb/pull/24070)
    - Fix the wrong `TableDual` plans caused by incorrectly comparing binaries and bytes[#23846](https://github.com/pingcap/tidb/issues/23846)
    - Fix the panic issue caused by using the prefix index and index join in some cases [#24547](https://github.com/pingcap/tidb/issues/24547) [#24716](https://github.com/pingcap/tidb/issues/24716) [#24717](https://github.com/pingcap/tidb/issues/24717)
    - Fix the issue that the prepared plan cache of `point get` is incorrectly used by the `point get` statement in the transaction [#24741](https://github.com/pingcap/tidb/issues/24741)
    - Fix the issue of writing the wrong prefix index value when the collation is `ascii_bin` or `latin1_bin` [#24569](https://github.com/pingcap/tidb/issues/24569)
    - Fix the issue that the ongoing transaction might be interrupted by the GC worker [#24591](https://github.com/pingcap/tidb/issues/24591)
    - Fix a bug that the point query might get wrong on the clustered index when `new-collation` is enabled but `new-row-format` is disabled [#24541](https://github.com/pingcap/tidb/issues/24541)
    - Refactor the conversion of partition keys for shuffle hash join [#24490](https://github.com/pingcap/tidb/pull/24490)
    - Fix the panic issue that occurs when building the plan for queries that contain the `HAVING` clause [#24045](https://github.com/pingcap/tidb/issues/24045)
    - Fix the issue that the column pruning improvement causes the `Apply` and `Join` operators' results to go wrong [#23887](https://github.com/pingcap/tidb/issues/23887)
    - Fix a bug that the primary lock fallen back from async commit cannot be resolved [#24384](https://github.com/pingcap/tidb/issues/24384)
    - Fix a GC issue of statistics that might cause duplicated fm-sketch records [#24357](https://github.com/pingcap/tidb/pull/24357)
    - Avoid unnecessary pessimistic rollback when the pessimistic locking receives the `ErrKeyExists` error [#23799](https://github.com/pingcap/tidb/issues/23799)
    - Fix the issue that numeric literals cannot be recognized when the sql_mode contains `ANSI_QUOTES` [#24429](https://github.com/pingcap/tidb/issues/24429)
    - Forbid statements such as `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` to read data from non-listed partitions [#24746](https://github.com/pingcap/tidb/issues/24746)
    - Fix the potential `index out of range` error when a SQL statement contains both `GROUP BY` and `UNION` [#24281](https://github.com/pingcap/tidb/issues/24281)
    - Fix the issue that the `CONCAT` function incorrectly handles the collation [#24296](https://github.com/pingcap/tidb/issues/24296)
    - Fix the issue that the `collation_server` global variable does not take effect in new sessions [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiKV

    - Fix the issue that the coprocessor fails to properly handle the signed or unsigned integer types in the `IN` expression [#9821](https://github.com/tikv/tikv/issues/9821)
    - Fix the issue of many empty Regions after batch ingesting SST files [#964](https://github.com/pingcap/br/issues/964)
    - Fix a bug that TiKV cannot start up after the file dictionary file is damaged [#9886](https://github.com/tikv/tikv/issues/9886)
    - Fix a TiCDC OOM issue caused by reading old values [#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    - Fix the issue of empty value in the secondary index for the clustered primary key column when collation is `latin1_bin` [#24548](https://github.com/pingcap/tidb/issues/24548)
    - Add the `abort-on-panic` configuration, which allows TiKV to generate the core dump file when panic occurs. Users still need to correctly configure the environment to enable core dump [#10216](https://github.com/tikv/tikv/pull/10216)
    - Fix the performance regression issue of `point get` queries that occurs when TiKV is not busy [#10046](https://github.com/tikv/tikv/issues/10046)

+ PD

    - Fix the issue that the PD Leader re-election is slow when there are many stores [#3697](https://github.com/tikv/pd/issues/3697)

    - Fix the panic issue that occurs when removing the evict leader scheduler from a non-existent store [#3660](https://github.com/tikv/pd/issues/3660)
    - Fix the issue that the statistics are not updated after offline peers are merged [#3611](https://github.com/tikv/pd/issues/3611)

+ TiFlash

    - Fix the issue of incorrect results when casting the time type to the integer type
    - Fix a bug that the `receiver` cannot find corresponding tasks within 10 seconds
    - Fix the issue that there might be invalid iterators in `cancelMPPQuery`
    - Fix a bug that the behavior of the `bitwise` operator is different from that of TiDB
    - Fix the alert issue caused by overlapping ranges when using the `prefix key`
    - Fix the issue of incorrect results when casting the string type to the integer type
    - Fix the issue that consecutive and fast writes might make TiFlash out of memory
    - Fix the potential issue that the exception of null pointer might be raised during the table GC
    - Fix the TiFlash panic issue that occurs when writing data to dropped tables
    - Fix the issue that TiFlash might panic during BR restore
    - Fix the issue of incorrect results when cloning shared delta index concurrently
    - Fix the potential panic that occurs when the Compaction Filter feature is enabled
    - Fix the issue that TiFlash cannot resolve the lock fallen back from async commit
    - Fix the issue of incorrect results returned when the casted result of the `TIMEZONE` type contains the `TIMESTAMP` type
    - Fix the TiFlash panic issue that occurs during Segment Split

+ Tools

    + TiDB Lightning

        - Fix the issue of TiDB Lightning panic that occurs when generating KV data [#1127](https://github.com/pingcap/br/pull/1127)
        - Fix a bug that the batch split Region fails due to the total key size exceeding the raft entry limit during the data import [#969](https://github.com/pingcap/br/issues/969)
        - Fix the issue that when importing CSV files, if the last line of the file does not contain line break characters (`\r\n`), an error will be reported [#1133](https://github.com/pingcap/br/issues/1133)
        - Fix the issue that if a table to be imported includes an auto-increment column of the double type, the auto_increment value becomes abnormal [#1178](https://github.com/pingcap/br/pull/1178)

    + Backup & Restore (BR)
        - Fix the issue of backup interruption caused by the failure of a few TiKV nodes [#980](https://github.com/pingcap/br/issues/980)

    + TiCDC

        - Fix the concurrency issue in Unified Sorter and filter the unhelpful error messages [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - Fix a bug that the creation of redundant directories might interrupt the replication with MinIO [#1463](https://github.com/pingcap/ticdc/issues/1463)
        - Set the default value of the `explicit_defaults_for_timestamp` session variable to ON to make the MySQL 5.7 downstream keep the same behavior with the upstream TiDB [#1585](https://github.com/pingcap/ticdc/issues/1585)
        - Fix the issue that the incorrect handling of `io.EOF` might cause replication interruption [#1633](https://github.com/pingcap/ticdc/issues/1633)
        - Correct the TiKV CDC endpoint CPU metric in the TiCDC dashboard [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - Increase `defaultBufferChanSize` to avoid replication blocking in some cases [#1259](https://github.com/pingcap/ticdc/issues/1259)
        - Fix the issue that the time zone information is lost in the Avro output [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - Support cleaning up stale temporary files in Unified Sorter and forbid sharing the `sort-dir` directory [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - Fix a deadlock bug in the KV client that occurs when many stale Regions exist [#1599](https://github.com/pingcap/ticdc/issues/1599)
        - Fix the wrong help information in the `--cert-allowed-cn` flag [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - Revert the update for `explicit_defaults_for_timestamp` which requires the SUPER privilege when replicating data to MySQL [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - Support the sink flow control to reduce the risk of memory overflow [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - Fix a bug that the replication task might stop when moving a table [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - Fix the issue that the TiKV GC safe point is blocked due to the stagnation of TiCDC changefeed checkpoint [#1759](https://github.com/pingcap/ticdc/pull/1759)
