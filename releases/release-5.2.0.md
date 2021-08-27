---
title: TiDB 5.2 Release Notes
---

# Release date: August 27, 2021

Release date: August 27, 2021

TiDB version: 5.2.0

In v5.2, the key new features and improvements are as follows:

- Support expression index to greatly improve query performance
- Improve the accuracy of optimizer cardinality estimation to help to select optimal execution plans
- Announce the general availability (GA) for the Lock View feature to observe transaction locking events and troubleshoot deadlock problems
- Add the TiFlash I/O traffic limit feature to improve the stability of read and write for TiFlash
- Optimize TiKV reserving space management to improve the stability of storage
- TiKV introduces a new flow control mechanism to replace the previous RocksDB write stall mechanism to improve the stability of TiKV flow control
- Simplify the operation and maintenance of Data Migration (DM) to reduce the management cost.
- TiCDC supports HTTP protocol OpenAPI to manage TiCDC tasks. It provides a more user-friendly operation method for both Kubernetes and on-premises environments. (Experimental feature)

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v5.2, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Note](/releases/release-notes.md) for the corresponding version.

### System variables

| Variable name    |  Change type    |  Description  |
| :---------- | :----------- | :----------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) | Newly added | Sets the authentication method that the server advertises. The default value is `mysql_native_password`.  |
| [`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated) | Newly added | Determines whether to include the `AUTO_INCREMENT` columns when creating a generated column or an expression index. The default value is `OFF`.  |
| [`tidb_opt_enable_correlation_adjustment`](/system-variables.md#tidb_opt_enable_correlation_adjustment) | Newly added | Controls whether the optimizer estimates the number of rows based on column order correlation. The default value is `ON`.  |
| [`tidb_opt_limit_push_down_threshold`](/system-variables.md#tidb_opt_limit_push_down_threshold) | Newly added | Sets the threshold that determines whether to push the Limit or TopN operator down to TiKV. The default value is `100`.  |
| [`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) | Modified | Sets the maximum number of statements that the statement summary tables store in memory. The default value is changed from `200` to `3000`.  |
| `tidb_enable_streaming` | Deprecated | The system variable `enable-streaming` is deprecated and it is not recommended to use it any more.  |

### Configuration file parameters

| Configuration file    |  Configuration item    |  Change type    |  Description    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB configuration file  | [`pessimistic-txn.deadlock-history-collect-retryable`](/tidb-configuration-file.md#deadlock-history-collect-retryable) |  Newly added  | Controls whether the [`INFORMATION\_SCHEMA.DEADLOCKS`](/information-schema/information-schema-deadlocks.md) table collects retryable deadlock error messages or not.  |
| TiDB configuration file  | [`security.auto-tls`](/tidb-configuration-file.md#auto-tls) |  Newly added  | Determines whether to automatically generate the TLS certificates on startup. The default value is `false`.  |
| TiDB configuration file  | [`stmt-summary.max-stmt-count`](/tidb-configuration-file.md#max-stmt-count) | Modified | Indicates the maximum number of SQL categories allowed to be saved in the statement summary tables. The default value is changed from `200` to `3000`.  |
| TiDB configuration file  | `experimental.allow-expression-index`  | Deprecated | The `allow-expression-index` configuration in the TiDB configuration file is deprecated.  |
| TiKV configuration file  | [`raftstore.cmd-batch`](/tikv-configuration-file.md#cmd-batch)  |  Newly added  | Controls whether to enable batch processing of the requests. When it is enabled, the write performance is significantly improved. The default value is `true`.  |
| TiKV configuration file  | [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)  |  Newly added  | At a certain interval, TiKV inspects the latency of the Raftstore component. This configuration item specifies the interval of the inspection. The default value is `500ms`.  |
| TiKV configuration file  | [`raftstore.max-peer-down-duration`](/tikv-configuration-file.md#max-peer-down-duration)  | Modified | Indicates the longest inactive duration allowed for a peer. A peer with timeout is marked as `down`, and PD tries to delete it later. The default value is changed from `5m` to `10m`.  |
| TiKV configuration file  | [`server.raft-client-queue-size`](/tikv-configuration-file.md#raft-client-queue-size)  |  Newly added  | Specifies the queue size of the Raft messages in TiKV. The default value is `8192`.  |
| TiKV configuration file  | [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)  |  Newly added  | Determines whether to enable the flow control mechanism. The default value is `true`.  |
| TiKV configuration file  | [`storage.flow-control.memtables-threshold`](/tikv-configuration-file.md#memtables-threshold)  |  Newly added  | When the number of kvDB memtables reaches this threshold, the flow control mechanism starts to work. The default value is `5`.  |
| TiKV configuration file  | [`storage.flow-control.l0-files-threshold`](/tikv-configuration-file.md#l0-files-threshold)  |  Newly added  | When the number of kvDB L0 files reaches this threshold, the flow control mechanism starts to work. The default value is `9`.  |
| TiKV configuration file  | [`storage.flow-control.soft-pending-compaction-bytes-limit`](/tikv-configuration-file.md#soft-pending-compaction-bytes-limit)  |  Newly added  | When the pending compaction bytes in KvDB reach this threshold, the flow control mechanism starts to reject some write requests and reports the `ServerIsBusy` error. The default value is "192GB".  |
| TiKV configuration file  | [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)  |  Newly added  | When the pending compaction bytes in KvDB reach this threshold, the flow control mechanism rejects all write requests and reports the `ServerIsBusy` error. The default value is "1024GB".  |

### Others

- Before the upgrade, check whether the value of the [`tidb_evolve_plan_baselines`](/system-variables.md#tidb_evolve_plan_baselines-new-in-v40) system variable is `ON`. If the value is `ON`, set it to `OFF`; otherwise, the upgrade will fail.
- For TiDB clusters upgraded from v4.0 to v5.2, the default value of [`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) changes from `WARN` to `OFF`.
- Before the upgrade, check the value of the TiDB configuration [`feedback-probability`](/tidb-configuration-file.md#feedback-probability). If the value is not `0`, the "panic in the recoverable goroutine" error will occur after the upgrade, but this error does not affect the upgrade.
- TiDB is now compatible with MySQL 5.7's noop variable `innodb_default_row_format`. Setting this variable has no effect. [#23541](https://github.com/pingcap/tidb/issues/23541)
- Starting from TiDB 5.2, to improve system security, it is recommended (but not mandatory) to encrypt the transport layer for connections from clients. TiDB provides the Auto TLS feature to automatically configure and enable encryption in TiDB. To use the Auto TLS feature, before the TiDB upgrade, set [`security.auto-tls`](/tidb-configuration-file.md#auto-tls) in the TiDB configuration file to `true`.

## New features

### SQL

- **Support expression index**

    The expression index is a type of special index that can be created on an expression. After an expression index is created, TiDB supports expression-based queries, which greatly improves query performance.

    [User document](/sql-statements/sql-statement-create-index.md), [#25150](https://github.com/pingcap/tidb/issues/25150)

- **Support the `translate` function in Oracle**

    The `translate` function replaces all occurrences of characters by other characters in a string. In TiDB, this function does not treat empty strings as `NULL` as Oracle does.

    [User document](/functions-and-operators/string-functions.md)

- **Support spilling HashAgg**

    Support spilling HashAgg into disk. When a SQL statement that includes an HashAgg operator causes out of memory (OOM), you can try to set the concurrency of this operator to `1` to trigger disk spill, which alleviates memory stress.

    [User document](/configure-memory-usage.md#other-memory-control-behaviors-of-tidb-server), [#25882](https://github.com/pingcap/tidb/issues/25882)

- **Improve the accuracy of optimizer cardinality estimation**

    - Improve the accuracy of TiDB's estimation of TopN/Limit. For example, for pagination queries on a large table that contain the `order by col limit x` condition, TiDB can more easily select the right index and reduce query response time.
    - Improve the accuracy of out-of-range estimation. For example, even if the statistics for a day have not been updated, TiDB can accurately select the corresponding index for a query that contains `where date=Now()`.
    - Introduce the `tidb_opt_limit_push_down_threshold` variable to control the optimizer's behavior of pushing down Limit/TopN, which resolves the issue that Limit/TopN cannot be pushed down in some situations due to wrong estimation.

    [User document](/system-variables.md#tidb_opt_limit_push_down_threshold), [#26085](https://github.com/pingcap/tidb/issues/26085)

- **Improve index selection of the optimizer**

    Add pruning rules for index selection. Before using the statistics for comparison, TiDB uses these rules to narrow down the scope of possible indexes to be selected, which reduces the possibility of selecting non-optimal indexes.

    [User document](/choose-index.md)

### Transaction

- **General availability (GA) for Lock View**

    The Lock View feature provides more information about lock conflicts and lock waits of pessimistic locks, which helps DBAs to observe transaction locking events and troubleshoot deadlock problems.

    In v5.2, the following enhancements are made to Lock View:

    - In addition to the SQL digest column in the Lock View-related tables, add a column to these tables that shows the corresponding normalized SQL text. You do not have to manually query the statement corresponding to a SQL digest.
    - Add the `TIDB_DECODE_SQL_DIGESTS` function to query the normalized SQL statements (a form without formats and arguments) corresponding to a set of SQL digests in the cluster. This simplifies the operation of querying the statements that have been historically executed by a transaction.
    - Add a column in the `DATA_LOCK_WAITS` and `DEADLOCKS` system tables to show the table name, row ID, index value, and other key information interpreted from a key. This simplifies the operations such as locating the table to which a key belongs and interpreting the key information.
    - Support collecting the information of retryable deadlock errors in the `DEADLOCKS` table, which makes it easier to troubleshoot issues caused by such errors. The error collection is disabled by default and can be enabled using the `pessimistic-txn.deadlock-history-collect-retryable` configuration.
    - Support distinguishing query-executing transactions from idle transactions on the `TIDB_TRX` system table. The `Normal` state is now divided into `Running` and `Idle` states.

   User documents:

    - View the pessimistic lock-waiting events that are occurring on all TiKV nodes in the cluster: [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)
    - View the deadlock errors recently occurred on a TiDB node: [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)
    - View the executing transaction on a TiDB node: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

- Optimize the user scenarios of adding indexes on tables with the `AUTO_RANDOM` or `SHARD_ROW_ID_BITS` attribute.

### Stability

- **Add TiFlash I/O traffic limit**

    This new feature is suitable for cloud storage with disk bandwidth of a small and specific size. It is disabled by default.

    TiFlash I/O Rate Limiter provides a new mechanism to avoid excessive race for I/O resources between read and write tasks. It balances the responses to read and write tasks, and limits the rate automatically according to read/write workload.

    [User document](/tiflash/tiflash-configuration.md)

- **Improve stability of TiKV flow control**

    TiKV introduces a new flow control mechanism to replace the previous RocksDB write stall mechanism. Compared with the write stall mechanism, this new mechanism reduces the impact on the stability of foreground write.

    In specific, when the stress of RocksDB compaction accumulates, flow control is performed at the TiKV scheduler layer instead of the RocksDB layer, to avoid the following issues:

    - Raftstore is stuck, which is caused by RocksDB write stall.
    - Raft election times out, and the node leader is transferred as a result.

    This new mechanism improves the flow control algorithm to mitigate QPS decrease when the write traffic is high.

    [User document](/tikv-configuration-file.md#storageflow-control), [#10137](https://github.com/tikv/tikv/issues/10137)

- **Detect and recover automatically from impact caused by a single slow TiKV node in a cluster**

    TiKV introduces the slow node detection mechanism. This mechanism calculates a score by inspecting the rate of TiKV Raftstore, and then reports the score to PD through store heartbeats. Meanwhile, it adds the `evict-slow-store-scheduler` scheduler on PD to automatically evict the leader on a single slow TiKV node. In this way, the impact on the whole cluster is mitigated. At the same time, more alert items about slow nodes are introduced to help you quickly pinpoint and solve problems.

[User document]( /tikv-configuration-file.md#inspect-interval), [#10539](https://github.com/tikv/tikv/issues/10539)

### Data Migration

- **Simplify operations of Data Migration (DM)**

    DM v2.0.6 can automatically identify the change event (failover or plan change) of the data source using VIP, and can automatically connect to a new data source instance, to reduce data replication latency and simplify operation procedures.

- TiDB Lightning supports customized line terminators in the CSV data, and is compatible with the MySQL LOAD DATA CSV data formats. You can then use TiDB Lightning directly in your data flow architecture.

    [#1297](https://github.com/pingcap/br/pull/1297)

### TiDB data share subscription

TiCDC supports using the HTTP protocol (OpenAPI) to manage TiCDC tasks, which is a more user-friendly operation method for both Kubernetes and on-premises environments. (Experimental feature)

[#2411](https://github.com/pingcap/ticdc/issues/2411)

### Deployment and operations

Support running the `tiup playground` command on Mac computers with Apple M1 chips.

## Feature Enhancements

+ Tools

    + TiCDC

        - Add the binary MQ format designed for TiDB. It is more compact than the open protocols based on JSON [#1621](https://github.com/pingcap/ticdc/pull/1621)
        - Remove support for file sorter [#2114](https://github.com/pingcap/ticdc/pull/2114)
        - Support log rotation configurations [#2182](https://github.com/pingcap/ticdc/pull/2182)

    + TiDB Lightning

        - Support customized line terminators (except `\r` and `\n`) [#1297](https://github.com/pingcap/br/pull/1297)
        - Support expression index and the index that depends on virtual generated columns [#1407](https://github.com/pingcap/br/pull/1407)

    + Dumpling

        - Support backing up MySQL compatible databases but does not support `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` or`SHOW CREATE TABLE` [#311](https://github.com/pingcap/dumpling/pull/311)

## Improvements

+ TiDB

    - Support pushing down the built-in function `json_unquote()` to TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)
    - Support removing the `union` branch from the dual table [#25614](https://github.com/pingcap/tidb/pull/25614)
    - Optimize the aggregate operator's cost factor [#25241](https://github.com/pingcap/tidb/pull/25241)
    - Allow the MPP outer join to choose the build table based on the table row count [#25142](https://github.com/pingcap/tidb/pull/25142)
    - Support balancing the MPP query workload among different TiFlash nodes based on Regions [#24724](https://github.com/pingcap/tidb/pull/24724)
    - Support invalidating stale Regions in the cache after the MPP query is executed [#24432](https://github.com/pingcap/tidb/pull/24432)
    - Improve the MySQL compatibility of the built-in function`str_to_date` for the format specifiers `%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)
    - Fix the issue that inconsistent binding caches might be created in multiple TiDB after recreating different bindings for the same query [#26015](https://github.com/pingcap/tidb/pull/26015)
    - Fix the issue that the existing bindings cannot be loaded into cache after upgrade [#23295](https://github.com/pingcap/tidb/pull/23295)
    - Support ordering the result of `SHOW BINDINGS` by (`original_sql`, `update_time`) [#26139](https://github.com/pingcap/tidb/pull/26139)
    - Improve the logic of query optimization when bindings exist, and reduce optimization times of a query [#26141](https://github.com/pingcap/tidb/pull/26141)
    - Support completing the garbage collection automatically for the bindings in the "deleted" status [#26206](https://github.com/pingcap/tidb/pull/26206)
    - Support showing whether a binding is used for query optimization in the result of `EXPLAIN VERBOSE` [#26930](https://github.com/pingcap/tidb/pull/26930)
    - Add a new status variation `last_plan_binding_update_time` to view the timestamp corresponding to the binding cache in the current TiDB instance [#26340](https://github.com/pingcap/tidb/pull/26340)
    - Support reporting an error when starting binding evolution or running `admin evolve bindings` to ban the baseline evolution (currently disabled in the on-premises TiDB version because it is an experimental feature) affecting other features [#26333](https://github.com/pingcap/tidb/pull/26333)

+ PD

    - Add more QPS dimensions for hot Region scheduling, and support adjusting the priority of the scheduling [#3869](https://github.com/tikv/pd/issues/3869)
    - Support hot Region balance scheduling for the write hotspot of TiFlash [#3900](https://github.com/tikv/pd/pull/3900)

+ TiFlash

    - Add operators: `MOD / %`, `LIKE`
    - Add string functions: `ASCII()`, `COALESCE()`, `LENGTH()`, `POSITION()`, `TRIM()`
    - Add mathematical functions: `CONV()`, `CRC32()`, `DEGREES()`, `EXP()`, `LN()`, `LOG()`, `LOG10()`, `LOG2()`, `POW()`, `RADIANS()`, `ROUND(decimal)`, `SIN()`, `MOD()`
    - Add date functions: `ADDDATE(string, real)`, `DATE_ADD(string, real)`, `DATE()`
    - Add other functions: `INET_NTOA()`, `INET_ATON()`, `INET6_ATON`, `INET6_NTOA()`
    - Support Shuffled Hash Join calculation and Shuffled Hash Aggregation calculation in the MPP mode when a new collation is enabled
    - Optimize basic code to improve MPP performance
    - Support casting the `STRING` type to the `DOUBLE` type
    - Optimize the non-joined data in right outer join using multiple threads
    - Support automatically invalidating stale Regions in MPP queries

+ Tools

    + TiCDC

        - Add the concurrency limit to the incremental scan of kv client [#1899](https://github.com/pingcap/ticdc/pull/1899)
        - TiCDC can always pull the old value internally [#2271](https://github.com/pingcap/ticdc/pull/2271)
        - TiCDC can fail and exit fast when unrecoverable DML errors occur [#1928](https://github.com/pingcap/ticdc/pull/1928)
        - `resolve lock` cannot be run immediately after a Region is initialized [#2235](https://github.com/pingcap/ticdc/pull/2235)
        - Optimize workerpool to reduce the number of goroutines under high concurrency [#2201](https://github.com/pingcap/ticdc/pull/2201)

    + Dumpling

        - Support always splitting TiDB v3.x tables through `tidb_rowid` to save TiDB memory [#301](https://github.com/pingcap/dumpling/pull/301)
        - Reduce access of Dumpling to the `information_schema` to improve stability [#305](https://github.com/pingcap/dumpling/pull/305)

## Bug Fixes

+ TiDB

    - Fix the issue that an incorrect result is returned when using merge join on the `SET` type column [#25669](https://github.com/pingcap/tidb/issues/25669)
    - Fix the data corruption issue in the `IN` expression's arguments [#25591](https://github.com/pingcap/tidb/issues/25591)
    - Avoid the sessions of GC being affected by global variables [#24976](https://github.com/pingcap/tidb/issues/24976)
    - Fix the panic issue that occurs when using `limit` in the window function queries [#25344](https://github.com/pingcap/tidb/issues/25344)
    - Fix the wrong value returned when querying a partitioned table using `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)
    - Fix the issue that `IFNULL` does not correctly take effect on the `ENUM` or `SET` type column [#24944](https://github.com/pingcap/tidb/issues/24944)
    - Fix the wrong results caused by changing the `count` in the join subqueries to `first_row` [#24865](https://github.com/pingcap/tidb/issues/24865)
    - Fix the query hang issue that occurs when `ParallelApply` is used under the `TopN` operator [#24930](https://github.com/pingcap/tidb/issues/24930)
    - Fix the issue that more results than expected are returned when executing SQL statements using multi-column prefix indexes [#24356](https://github.com/pingcap/tidb/issues/24356)
    - Fix the issue that the `<=>` operator cannot correctly take effect [#24477](https://github.com/pingcap/tidb/issues/24477)
    - Fix the data race issue of the parallel `Apply` operator [#23280](https://github.com/pingcap/tidb/issues/23280)
    - Fix the issue that the `index out of range` error is reported when sorting the IndexMerge results of the PartitionUnion operator [#23919](https://github.com/pingcap/tidb/issues/23919)
    - Fix the issue that setting the `tidb_snapshot` variable to an unexpectedly large value might damage the transaction isolation [#25680](https://github.com/pingcap/tidb/issues/25680)
    - Fix the issue that the ODBC-styled constant (for example, `{d '2020-01-01'}`) cannot be used as the expression [#25531](https://github.com/pingcap/tidb/issues/25531)
    - Fix the issue that `SELECT DISTINCT` converted to `Batch Get` causes incorrect results [#25320](https://github.com/pingcap/tidb/issues/25320)
    - Fix the issue that backing off queries from TiFlash to TiKV cannot be triggered [#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    - Fix the `index-out-of-range` error that occurs when checking `only_full_group_by` [#23839](https://github.com/pingcap/tidb/issues/23839))
    - Fix the issue that the result of index join in correlated subqueries is wrong [#25799](https://github.com/pingcap/tidb/issues/25799)

+ TiKV

    - Fix the wrong `tikv_raftstore_hibernated_peer_state` metric [#10330](https://github.com/tikv/tikv/issues/10330)
    - Fix the wrong arguments type of the `json_unquote()` function in the coprocessor [#10176](https://github.com/tikv/tikv/issues/10176)
    - Skip clearing callback during graceful shutdown to avoid breaking ACID in some cases [#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    - Fix a bug that the read index is shared for replica reads on a Leader [#10347](https://github.com/tikv/tikv/issues/10347)
    - Fix the wrong function that casts `DOUBLE` to `DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)

+ PD

    - Fix the issue that the expected scheduling cannot be generated due to scheduling conflicts among multiple schedulers [#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)

+ TiFlash

    - Fix the issue that TiFlash keeps restarting because of the split failure
    - Fix the potential issue that TiFlash cannot delete the delta data
    - Fix a bug that TiFlash adds wrong padding for non-binary characters in the `CAST` function
    - Fix the issue of incorrect results when handling aggregation queries with complex `GROUP BY` columns
    - Fix the TiFlash panic issue that occurs under heavy write pressure
    - Fix the panic that occurs when the right jon key is not nullable and the left join key is nullable
    - Fix the potential issue that the `read-index` requests take a long time
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the panic issue that might occur when the `Date_Format` function is called with the `STRING` type argument and `NULL` values

+ Tools

    + TiCDC

        - Fix a bug that TiCDC owner exits abnormally when refreshing the checkpoint [#1902](https://github.com/pingcap/ticdc/issues/1902)
        - Fix a bug that changefeed fails immediately after its successful creation [#2113](https://github.com/pingcap/ticdc/issues/2113)
        - Fix a bug that changefeed fails due to the invalid format of rules filter [#1625](https://github.com/pingcap/ticdc/issues/1625)
        - Fix the potential DDL loss issue when the TiCDC owner panics [#1260](https://github.com/pingcap/ticdc/issues/1260)
        - Fix the CLI compatibility issue with 4.0.x clusters on the default sort-engine option [#2373](https://github.com/pingcap/ticdc/issues/2373)
        - Fix a bug that changefeed might be reset unexpectedly when TiCDC gets the `ErrSchemaStorageTableMiss` error [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - Fix a bug that changefeed cannot be removed when TiCDC gets the `ErrGCTTLExceeded` error [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - Fix a bug that TiCDC fails to synchronize large tables to cdclog [#1259](https://github.com/pingcap/ticdc/issues/1259) [#2424](https://github.com/pingcap/ticdc/issues/2424)
        - Fix a bug that multiple processors might write data to the same table when TiCDC is rescheduling the table [#2230](https://github.com/pingcap/ticdc/issues/2230)

    + Backup & Restore (BR)

        - Fix a bug that BR skips restoring all system tables during the restore [#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        - Fix a bug that BR misses DDL operations when restoring cdclog [#870](https://github.com/pingcap/br/issues/870)

    + TiDB Lightning

        - Fix a bug that TiDB Lightning fails to parse the `DECIMAL` data type in Parquet file [#1272](https://github.com/pingcap/br/pull/1272)
        - Fix a bug that TiDB Lightning reports the "Error 9007: Write conflict" error when restoring table schemas [#1290](https://github.com/pingcap/br/issues/1290)
        - Fix a bug that TiDB Lightning fails to import data due to the overflow of int handle [#1291](https://github.com/pingcap/br/issues/1291)
        - Fix a bug that TiDB Lightning might get a checksum mismatching error due to data loss in the local backend mode [#1403](https://github.com/pingcap/br/issues/1403)
        - Fix the Lighting incompatibility issue with clustered index when TiDB Lightning is restoring table schemas [#1362](https://github.com/pingcap/br/issues/1362)

    + Dumpling

        - Fix a bug that the data export fails because the Dumpling GC safepoint is set too late [#290](https://github.com/pingcap/dumpling/pull/290)
        - Fix the Dumpling getting stuck issue when exporting table names from the upstream database in certain MySQL versions [#322](https://github.com/pingcap/dumpling/issues/322)
