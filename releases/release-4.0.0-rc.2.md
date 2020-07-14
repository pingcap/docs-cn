---
title: TiDB 4.0 RC.2 Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-rc.2/']
---

# TiDB 4.0 RC.2 Release Notes

Release date: May 15, 2020

TiDB version: 4.0.0-rc.2

## Compatibility Changes

+ TiDB

    - Remove the size limit for a single transaction (100 MB) when TiDB Binlog is enabled. Now the size limit for a transaction is 10 GB. However, if TiDB Binlog is enabled and the downstream is Kafka, configure the `txn-total-size-limit` parameter according to the message size limit of 1 GB in Kafka [#16941](https://github.com/pingcap/tidb/pull/16941)
    - Change the behavior from querying the default time range to returning an error and requesting a specified time range if the time range is not specified when querying the `CLUSTER_LOG` table [#17003](https://github.com/pingcap/tidb/pull/17003)
    - If the unsupported `sub-partition` or `linear hash` option is specified when creating the partitioned table using the `CREATE TABLE` statement, the normal table is created rather than the partitioned table with the options ignored [#17197](https://github.com/pingcap/tidb/pull/17197)

+ TiKV

    - Move the encryption-related configuration to the security-related configuration, which means changing `[encryption]` in the TiKV configuration file to `[security.encryption]` [#7810](https://github.com/tikv/tikv/pull/7810)

+ Tools

    - TiDB Lightning

        - Change the default SQL mode to `ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER` when importing data to improve compatibility [#316](https://github.com/pingcap/tidb-lightning/pull/316)
        - Disallow accessing the PD or TiKV port in the tidb-backend mode [#312](https://github.com/pingcap/tidb-lightning/pull/312)
        - Print the log information to the tmp file by default, and print the path of the tmp file when TiDB Lightning is started [#313](https://github.com/pingcap/tidb-lightning/pull/313)

## Important Bug Fixes

+ TiDB

    - Fix the issue that the wrong partition is chosen when the `WHERE` clause has only one equivalent condition [#17054](https://github.com/pingcap/tidb/pull/17054)
    - Fix the issue of wrong results caused by building the incorrect Index range when the `WHERE` clause only contains the string column [#16660](https://github.com/pingcap/tidb/pull/16660)
    - Fix the panic issue that occurs when executing the `PointGet` query in the transaction after the `DELETE` operation [#16991](https://github.com/pingcap/tidb/pull/16991)
    - Fix the issue that the GC worker might encounter the deadlock when an error occurs [#16915](https://github.com/pingcap/tidb/pull/16915)
    - Avoid the unnecessary RegionMiss retry when the TiKV response is slow but not down [#16956](https://github.com/pingcap/tidb/pull/16956)
    - Change the log level in the client in the handshake phase of the MySQL protocol to `DEBUG` to solve the problem that interferes with log output [#16881](https://github.com/pingcap/tidb/pull/16881)
    - Fix the issue that the Region is not pre-split according to the `PRE_SPLIT_REGIONS` information defined by the table after the `TRUNCATE` operation [#16776](https://github.com/pingcap/tidb/pull/16776)
    - Fix the issue of soaring goroutine caused by retry when TiKV is unavailable during the second phase of the two-phase commit [#16876](https://github.com/pingcap/tidb/pull/16876)
    - Fix the panic issue of statement execution when some expressions cannot be pushed down [#16869](https://github.com/pingcap/tidb/pull/16869)
    - Fix the wrong execution result of the IndexMerge operation on the partitioned table [#17124](https://github.com/pingcap/tidb/pull/17124)
    - Fix the performance reduction of `wide_table` caused by the mutex contention of Memory Trackers [#17234](https://github.com/pingcap/tidb/pull/17234)

+ TiFlash

    - Fix the issue that the system cannot start normally after the upgrade if the name of the database or table contains special characters

## New Features

+ TiDB

    - Add support for the `BACKUP` and `RESTORE` commands to back up and restore data [#16960](https://github.com/pingcap/tidb/pull/16960)
    - Support pre-checking the data volume in a single Region before commit and pre-splitting the Region when the data volume exceeds the threshold [#16959](https://github.com/pingcap/tidb/pull/16959)
    - Add the new `LAST_PLAN_FROM_CACHE` variable with a `Session` scope to indicate whether the last executed statement hits the plan cache [#16830](https://github.com/pingcap/tidb/pull/16830)
    - Support recording the `Cop_time` information in slow log and the `SLOW_LOG` table [#16904](https://github.com/pingcap/tidb/pull/16904)
    - Add in Grafana more metrics that monitor the memory status of Go Runtime [#16928](https://github.com/pingcap/tidb/pull/16928)
    - Support outputting the `forUpdateTS` and `Read Consistency` isolation level information in General Log [#16946](https://github.com/pingcap/tidb/pull/16946)
    - Support collapsing duplicate requests of resolving locks in TiKV Region [#16925](https://github.com/pingcap/tidb/pull/16925)
    - Support using the `SET CONFIG` statement to modify the configuration of PD/TiKV nodes [#16853](https://github.com/pingcap/tidb/pull/16853)
    - Support the `auto_random` option in the `CREATE TABLE` statement [#16813](https://github.com/pingcap/tidb/pull/16813)
    - Allocate TaskID for the DistSQL request to help TiKV better schedule and process requests [#17155](https://github.com/pingcap/tidb/pull/17155)
    - Support displaying the version information of the TiDB server after logging into the MySQL client [#17187](https://github.com/pingcap/tidb/pull/17187)
    - Support the `ORDER BY` clause in the `GROUP_CONCAT` function [#16990](https://github.com/pingcap/tidb/pull/16990)
    - Support displaying the `Plan_from_cache` information in slow log to indicate whether the statement hits plan cache [#17121](https://github.com/pingcap/tidb/pull/17121)
    - Add the feature that TiDB Dashboard can display the capacity information of TiFlash multi-disk deployment
    - Add the feature of querying the TiFlash log using SQL statements in Dashboard

+ TiKV

    - Support encryption debugging for tikv-ctl, so that tikv-ctl can be used to operate and manage the cluster when the encryption storage is enabled [#7698](https://github.com/tikv/tikv/pull/7698)
    - Support encrypting the lock column family in snapshots [#7712](https://github.com/tikv/tikv/pull/7712)
    - Use the heatmap in the Grafana dashboard for Raftstore latency summary to better diagnose the jitter issue [#7717](https://github.com/tikv/tikv/pull/7717)
    - Support setting the upper limit for the size of the gRPC message [#7824](https://github.com/tikv/tikv/pull/7824)
    - Add in Grafana dashboard the encryption-related monitoring metrics [#7827](https://github.com/tikv/tikv/pull/7827)
    - Support Application-Layer Protocol Negotiation (ALPN) [#7825](https://github.com/tikv/tikv/pull/7825)
    - Add more statistics about Titan [#7818](https://github.com/tikv/tikv/pull/7818)
    - Support using the task ID provided by the client as the identifier in the unified read pool to avoid that the priority of a task is lowered by another task in the same transaction [#7814](https://github.com/tikv/tikv/pull/7814)
    - Improve the performance of the `batch insert` request [#7718](https://github.com/tikv/tikv/pull/7718)

+ PD

    - Eliminate the speed limit of removing peers when making a node offline [#2372](https://github.com/pingcap/pd/pull/2372)

+ TiFlash

    - Change the name of the Count graph of **Read Index** in Grafana to **Ops**
    - Optimize the data for opening file descriptors when the system load is low to reduce system resource consumption
    - Add the capacity-related configuration parameter to limit the the data storage capacity

+ Tools

    - TiDB Lightning

        - Add the `fetch-mode` sub-command in tidb-lightning-ctl to print the TiKV cluster mode [#287](https://github.com/pingcap/tidb-lightning/pull/287)

    - TiCDC

        - Support managing the replication task by using `cdc cli` (changefeed) [#546](https://github.com/pingcap/ticdc/pull/546)

    - Backup & Restore (BR)

        - Support automatically adjusting GC time during backup [#257](https://github.com/pingcap/br/pull/257)
        - Adjust PD parameters when restoring data to speed up the restoration [#198](https://github.com/pingcap/br/pull/198)

## Bug Fixes

+ TiDB

    - Improve the logic that determines whether to use vectorization for expression execution in multiple operators [#16383](https://github.com/pingcap/tidb/pull/16383)
    - Fix the issue that the `IndexMerge` hint fails to check the database name correctly [#16932](https://github.com/pingcap/tidb/pull/16932)
    - Forbid truncating the sequence object [#17037](https://github.com/pingcap/tidb/pull/17037)
    - Fix the issue that the `INSERT`/`UPDATE`/`ANALYZE`/`DELETE` statements can be performed on a sequence object [#16957](https://github.com/pingcap/tidb/pull/16957)
    - Fix the issue that the internal SQL statements in the bootstrap phase are not correctly marked as internal queries in the Statement Summary table [#17062](https://github.com/pingcap/tidb/pull/17062)
    - Fix the error that occurs when a filter condition supported by TiFlash but not by TiKV is pushed down to the `IndexLookupJoin` operator [#17036](https://github.com/pingcap/tidb/pull/17036)
    - Fix the concurrency issue of the `LIKE` expression that might occur after the collation is enabled [#16997](https://github.com/pingcap/tidb/pull/16997)
    - Fix the issue that the `LIKE` function cannot correctly build the `Range` query index after the collation is enabled [#16783](https://github.com/pingcap/tidb/pull/16783)
    - Fix the issue that a wrong value is returned when executing `@@LAST_PLAN_FROM_CACHE` after the `Plan Cache` statement is triggered [#16831](https://github.com/pingcap/tidb/pull/16831)
    - Fix the issue that `TableFilter` on the index is missed when calculating candidate paths for `IndexMerge` [#16947](https://github.com/pingcap/tidb/pull/16947)
    - Fix the issue that a physical query plan cannot be generated when using the `MergeJoin` hint and the `TableDual` operator exists [#17016](https://github.com/pingcap/tidb/pull/17016)
    - Fix the wrong capitalization of the values in the `Stmt_Type` column of the Statement Summary table [#17018](https://github.com/pingcap/tidb/pull/17018)
    - Fix the issue that the `Permission Denied` error is reported because the service cannot be started when different users use the same `tmp-storage-path` [#16996](https://github.com/pingcap/tidb/pull/16996)
    - Fix the issue that the `NotNullFlag` result type is incorrectly set for an expression whose result type is determined by multiple input columns, such as `CASE WHEN` [#16995](https://github.com/pingcap/tidb/pull/16995)
    - Fix the issue that the green GC might leave unresolved locks when dirty stores exist [#16949](https://github.com/pingcap/tidb/pull/16949)
    - Fix the issue that the green GC might leave unresolved locks when encountering a single key with multiple different locks [#16948](https://github.com/pingcap/tidb/pull/16948)
    - Fix the issue of inserting a wrong value in the `INSERT VALUE` statement because a sub-query refers to a parent query column [#16952](https://github.com/pingcap/tidb/pull/16952)
    - Fix the issue of incorrect results when using the `AND` operator on the `Float` value [#16666](https://github.com/pingcap/tidb/pull/16666)
    - Fix the wrong information of the `WAIT_TIME` field in the expensive log [#16907](https://github.com/pingcap/tidb/pull/16907)
    - Fix the issue that the `SELECT FOR UPDATE` statement cannot be recorded in the slow log in the pessimistic transaction mode [#16897](https://github.com/pingcap/tidb/pull/16897)
    - Fix the wrong result that occurs when executing `SELECT DISTINCT` on a column of the `Enum` or `Set` type [#16892](https://github.com/pingcap/tidb/pull/16892)
    - Fix the display error of `auto_random_base` in the `SHOW CREATE  TABLE` statement [#16864](https://github.com/pingcap/tidb/pull/16864)
    - Fix the incorrect value of `string_value` in the `WHERE` clause [#16559](https://github.com/pingcap/tidb/pull/16559)
    - Fix the issue that the error message of the `GROUP BY` window function is inconsistent with that of MySQL [#16165](https://github.com/pingcap/tidb/pull/16165)
    - Fix the issue that the `FLASH TABLE` statement fails to execute when the database name contains the uppercase letter [#17167](https://github.com/pingcap/tidb/pull/17167)
    - Fix the inaccurate memory tracing of the Projection executor [#17118](https://github.com/pingcap/tidb/pull/17118)
    - Fix the issue of incorrect time filtering of the `SLOW_QUERY` table in different time zones [#17164](https://github.com/pingcap/tidb/pull/17164)
    - Fix the panic issue that occurs when `IndexMerge` is used with the virtual generated column [#17126](https://github.com/pingcap/tidb/pull/17126)
    - Fix the capitalization issue of the `INSTR` and `LOCATE` function [#17068](https://github.com/pingcap/tidb/pull/17068)
    - Fix the issue that the `tikv server timeout` error is reported frequently after the `tidb_allow_batch_cop` configuration is enabled [#17161](https://github.com/pingcap/tidb/pull/17161)
    - Fix the issue that the result of performing `XOR` operation on the Float type is inconsistent with that of MySQL 8.0 [#16978](https://github.com/pingcap/tidb/pull/16978)
    - Fix the issue that no error is reported when the unsupported `ALTER TABLE REORGANIZE PARTITION` statement is executed [#17178](https://github.com/pingcap/tidb/pull/17178)
    - Fix the issue that an error is reported when `EXPLAIN FORMAT="dot"  FOR CONNECTION ID` encounters an unsupported plan [#17160](https://github.com/pingcap/tidb/pull/17160)
    - Fix the record issue of the prepared statement in the `EXEC_COUNT` column of the Statement Summary table [#17086](https://github.com/pingcap/tidb/pull/17086)
    - Fix the issue that the value is not validated when setting the Statement Summary system variable [#17129](https://github.com/pingcap/tidb/pull/17129)
    - Fix the issue that an error is reported if an overflow value is used to query the `UNSIGNED BIGINT` primary key when the plan cache is enabled [#17120](https://github.com/pingcap/tidb/pull/17120)
    - Fix the incorrect QPS display by the machine instance and request type on the Grafana **TiDB Summary** dashboard [#17105](https://github.com/pingcap/tidb/pull/17105)

+ TiKV

    - Fix the issue that many empty Regions are generated after restoration [#7632](https://github.com/tikv/tikv/pull/7632)
    - Fix the panic issue of Raftstore when receiving out-of-order read index responses [#7370](https://github.com/tikv/tikv/pull/7370)
    - Fix the issue that an invalid storage or coprocessor read pool configuration might not be rejected when the unified thread pool is enabled [#7513](https://github.com/tikv/tikv/pull/7513)
    - Fix the panic issue of the `join` operation when the TiKV server is shut down [#7713](https://github.com/tikv/tikv/pull/7713)
    - Fix the issue that no result is returned when searching TiKV slow logs via diagnostics API [#7776](https://github.com/tikv/tikv/pull/7776)
    - Fix the issue that notable memory fragmentation is generated when the TiKV node is running for a long time [#7556](https://github.com/tikv/tikv/pull/7556)
    - Fix the issue that the SQL statement fails to execute when an invalid date is stored [#7268](https://github.com/tikv/tikv/pull/7268)
    - Fix the issue that the backup data cannot be restored from GCS [#7739](https://github.com/tikv/tikv/pull/7739)
    - Fix the issue that KMS key ID is not validated during encryption at rest [#7719](https://github.com/tikv/tikv/pull/7719)
    - Fix the underlying correctness issue of the Coprocessor in compilers of different architecture  [#7714](https://github.com/tikv/tikv/pull/7714) [#7730](https://github.com/tikv/tikv/pull/7730)
    - Fix the `snapshot ingestion` error when encrytion is enabled [#7815](https://github.com/tikv/tikv/pull/7815)
    - Fix the `Invalid cross-device link` error when rewriting the configuration file [#7817](https://github.com/tikv/tikv/pull/7817)
    - Fix the issue of wrong toml format when writing the configuration file to an empty file [#7817](https://github.com/tikv/tikv/pull/7817)
    - Fix the issue that a destroyed peer in Raftstore can still process requests [#7836](https://github.com/tikv/tikv/pull/7836)

+ PD

    - Fix the `404` issue that occurs when using the `region key` command in pd-ctl [#2399](https://github.com/pingcap/pd/pull/2399)
    - Fix the issue that the monitor metrics of TSO and ID allocation are missing from the Grafana dashboard [#2405](https://github.com/pingcap/pd/pull/2405)
    - Fix the issue that pd-recover is not included in the Docker image [#2406](https://github.com/pingcap/pd/pull/2406)
    - Parse the path of data directory to an absolute path to fix the issue that TiDB Dashboard might not correctly display PD information [#2420](https://github.com/pingcap/pd/pull/2420)
    - Fix the issue that there is no default output when using the `scheduler config shuffle-region-scheduler` command in pd-ctl [#2416](https://github.com/pingcap/pd/pull/2416)

+ TiFlash

    - Fix the issue that the wrong information of used capacity is report in some scenarios

+ Tools

    - TiDB Binlog

        - Fix the issue that data of the `mediumint` type is not processed when the downstream is Kafka [#962](https://github.com/pingcap/tidb-binlog/pull/962)
        - Fix the issue that the reparo fails to parse the DDL statement when the database name in DDL is a keyword [#961](https://github.com/pingcap/tidb-binlog/pull/961)

    - TiCDC

        - Fix the issue of using the wrong time zone when the `TZ` environment variable is not set [#512](https://github.com/pingcap/ticdc/pull/512)
        - Fix the issue that the owner does not clean up the resources when the server exits because some errors are not handled correctly [#528](https://github.com/pingcap/ticdc/pull/528)
        - Fix the issue that TiCDC might be stuck when reconnecting to TiKV [#531](https://github.com/pingcap/ticdc/pull/531)
        - Optimize the memory usage when initializing the table schema [#534](https://github.com/pingcap/ticdc/pull/534)
        - Use the `watch` mode to monitor the replication status changes and perform quasi-real-time updates to reduce replication delay [#481](https://github.com/pingcap/ticdc/pull/481)

    + Backup & Restore (BR)

        - Fix the issue that inserting data might trigger the `duplicate entry` error after BR restores a table with the `auto_random` attribute [#241](https://github.com/pingcap/br/issues/241)
