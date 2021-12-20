---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 Release Notes

Release Date: September 27, 2021

TiDB version: 5.1.2

## Compatibility changes

+ TiDB

    + The following bug fixes change execution results, which might cause upgrade incompatibilities:

        - Fix the issue that `greatest(datetime) union null` returns empty string [#26532](https://github.com/pingcap/tidb/issues/26532)
        - Fix the issue that the `having` clause might not work correctly [#26496](https://github.com/pingcap/tidb/issues/26496)
        - Fix the wrong execution results that occur when the collations around the `between` expression are different [#27146](https://github.com/pingcap/tidb/issues/27146)
        - Fix the wrong execution results that occur when the column in the `group_concat` function has a non-bin collation [#27429](https://github.com/pingcap/tidb/issues/27429)
        - Fix an issue that using a `count(distinct)` expression on multiple columns returns wrong result when the new collation is enabled [#27091](https://github.com/pingcap/tidb/issues/27091)
        - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
        - Fix the issue that inserting an invalid date does not report an error when the `SQL_MODE` is 'STRICT_TRANS_TABLES' [#26762](https://github.com/pingcap/tidb/issues/26762)
        - Fix the issue that using an invalid default date does not report an error when the `SQL_MODE` is 'NO_ZERO_IN_DATE' [#26766](https://github.com/pingcap/tidb/issues/26766)

+ Tools

    + TiCDC

        - Set the compatible version from `5.1.0-alpha` to `5.2.0-alpha` [#2659](https://github.com/pingcap/tiflow/pull/2659)

## Improvements

+ TiDB

    - Trigger auto-analyze by histogram row count and increase the accuracy of this trigger action  [#24237](https://github.com/pingcap/tidb/issues/24237)

+ TiKV

    - Support dynamically modifying TiCDC configurations [#10645](https://github.com/tikv/tikv/issues/10645)
    - Reduce the size of Resolved TS message to save network bandwidth [#2448](https://github.com/pingcap/tiflow/issues/2448)
    - Limit the counts of peer stats in the heartbeat message reported by a single store [#10621](https://github.com/tikv/tikv/pull/10621)

+ PD

    - Allow empty Regions to be scheduled and use a separate tolerance configuration in scatter range scheduler [#4117](https://github.com/tikv/pd/pull/4117)
    - Improve the performance of synchronizing Region information between PDs [#3933](https://github.com/tikv/pd/pull/3933)
    - Support dynamically adjusting the retry limit of a store based on the generated operator [#3744](https://github.com/tikv/pd/issues/3744)

+ TiFlash

    - Support the `DATE()` function
    - Add Grafana panels for write throughput per instance
    - Optimize the performance of the `leader-read` process
    - Accelerate the process of canceling MPP tasks

+ Tools

    + TiCDC

        - Optimize memory management when the Unified Sorter is using memory to sort data [#2553](https://github.com/pingcap/tiflow/issues/2553)
        - Optimize workerpool for fewer goroutines when concurrency is high  [#2211](https://github.com/pingcap/tiflow/issues/2211)
        - Reduce goroutine usage when a table's Region transfer away from a TiKV node [#2284](https://github.com/pingcap/tiflow/issues/2284)
        - Add a global gRPC connection pool and share gRPC connections among KV clients [#2534](https://github.com/pingcap/tiflow/pull/2534)
        - Prohibit operating TiCDC clusters across major and minor versions [#2599](https://github.com/pingcap/tiflow/pull/2599)

    + Dumpling

        - Support backing up MySQL-compatible databases that do not support `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` and `SHOW CREATE TABLE` [#309](https://github.com/pingcap/dumpling/issues/309)

## Bug fixes

+ TiDB

    - Fix the potential wrong results of index hash join when the hash column is the `ENUM` type [#27893](https://github.com/pingcap/tidb/issues/27893)
    - Fix a batch client bug that recycle idle connection might block sending requests in some rare cases [#27678](https://github.com/pingcap/tidb/pull/27678)
    - Fix the issue that the overflow check of the `FLOAT64` type is different with that of MySQL [#23897](https://github.com/pingcap/tidb/issues/23897)
    - Fix the issue that TiDB returns an `unknow` error while it should return the `pd is timeout` error [#26147](https://github.com/pingcap/tidb/issues/26147)
    - Fix the wrong character set and collation for the `case when` expression [#26662](https://github.com/pingcap/tidb/issues/26662)
    - Fix the potential `can not found column in Schema column` error for MPP queries [#28148](https://github.com/pingcap/tidb/pull/28148)
    - Fix a bug that TiDB might panic when TiFlash is shutting down [#28096](https://github.com/pingcap/tidb/issues/28096)
    - Fix the issue of wrong range caused by using `enum like 'x%'` [#27130](https://github.com/pingcap/tidb/issues/27130)
    - Fix the Common Table Expression (CTE) dead lock issue when used with IndexLookupJoin [#27410](https://github.com/pingcap/tidb/issues/27410)
    - Fix a bug that retryable deadlocks are incorrectly recorded into the `INFORMATION_SCHEMA.DEADLOCKS` table [#27400](https://github.com/pingcap/tidb/issues/27400)
    - Fix the issue that the `TABLESAMPLE` query result from partitioned tables is not sorted as expected [#27349](https://github.com/pingcap/tidb/issues/27349)
    - Remove the unused `/debug/sub-optimal-plan` HTTP API  [#27265](https://github.com/pingcap/tidb/pull/27265)
    - Fix a bug that the query might return wrong results when the hash partitioned table deals with unsigned data [#26569](https://github.com/pingcap/tidb/issues/26569)
    - Fix a bug that creating partition fails if `NO_UNSIGNED_SUBTRACTION` is set [#26765](https://github.com/pingcap/tidb/issues/26765)
    - Fix the issue that the `distinct` flag is missing when `Apply` is converted to `Join` [#26958](https://github.com/pingcap/tidb/issues/26958)
    - Set a block duration for the newly recovered TiFlash node to avoid blocking queries during this time [#26897](https://github.com/pingcap/tidb/pull/26897)
    - Fix a bug that might occur when the CTE is referenced more than once [#26212](https://github.com/pingcap/tidb/issues/26212)
    - Fix a CTE bug when MergeJoin is used [#25474](https://github.com/pingcap/tidb/issues/25474)
    - Fix a bug that the `SELECT FOR UPDATE` statement does not correctly lock the data when a normal table joins a partitioned table [#26251](https://github.com/pingcap/tidb/issues/26251)
    - Fix the issue that the `SELECT FOR UPDATE` statement returns an error when a normal table joins a partitioned table [#26250](https://github.com/pingcap/tidb/issues/26250)
    - Fix the issue that `PointGet` does not use the lite version of resolving lock [#26562](https://github.com/pingcap/tidb/pull/26562)

+ TiKV

    - Fix a panic issue that occurs after TiKV is upgraded from v3.x to later versions [#10902](https://github.com/tikv/tikv/issues/10902)
    - Fix the potential disk full issue caused by corrupted snapshot files [#10813](https://github.com/tikv/tikv/issues/10813)
    - Make the slow log of TiKV coprocessor only consider the time spent on processing requests [#10841](https://github.com/tikv/tikv/issues/10841)
    - Drop log instead of blocking threads when the slogger thread is overloaded and the queue is filled up [#10841](https://github.com/tikv/tikv/issues/10841)
    - Fix a panic issue that occurs when processing Coprocessor requests times out [#10852](https://github.com/tikv/tikv/issues/10852)
    - Fix the TiKV panic issue that occurs when upgrading from a pre-5.0 version with Titan enabled [#10842](https://github.com/tikv/tikv/pull/10842)
    - Fix the issue that TiKV of a newer version cannot be rolled back to v5.0.x [#10842](https://github.com/tikv/tikv/pull/10842)
    - Fix the issue that TiKV might delete files before ingesting data to RocksDB [#10438](https://github.com/tikv/tikv/issues/10438)
    - Fix the parsing failure caused by the left pessimistic locks [#26404](https://github.com/pingcap/tidb/issues/26404)

+ PD

    - Fix the issue that PD does not fix the down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix the issue that the replica count of the default placement rules stays constant after `replication.max-replicas` is updated [#3886](https://github.com/tikv/pd/issues/3886)
    - Fix a bug that PD might panic when scaling out TiKV [#3868](https://github.com/tikv/pd/issues/3868)
    - Fix a bug that the hot Region scheduler cannot work when the cluster has the evict leader scheduler [#3697](https://github.com/tikv/pd/issues/3697)

+ TiFlash

    - Fix the issue of unexpected results when TiFlash fails to establish MPP connections
    - Fix the potential issue of data inconsistency that occurs when TiFlash is deployed on multiple disks
    - Fix a bug that MPP queries get wrong results when TiFlash server is under high load
    - Fix a potential bug that MPP queries hang forever
    - Fix the panic issue when operating store initialization and DDL simultaneously
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT`, `<`, `<=`, `>`, `>=`, or `COLUMN`
    - Fix the potential panic issue when `Snapshot` is applied simultaneously with multiple DDL operations
    - Fix the issue that the store size in metrics is inaccurate under heavy writing
    - Fix the potential issue that TiFlash cannot garbage-collect the delta data after running for a long time
    - Fix the issue of wrong results when the new collation is enabled
    - Fix the potential panic issue that occurs when resolving locks
    - Fix a potential bug that metrics display wrong values

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the average speed is not accurate during data backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + Dumpling

        - Fix the issue that Dumpling is pending when `show table status` returns incorrect results in some MySQL versions (8.0.3 and 8.0.23) [#322](https://github.com/pingcap/dumpling/issues/322)
        - Fix the CLI compatibility issue with 4.0.x clusters on the default `sort-engine` option [#2373](https://github.com/pingcap/tiflow/issues/2373)

    + TiCDC

        - Fix a bug that the JSON encoding might cause panic when processing a string type value that is `string` or `[]byte` [#2758](https://github.com/pingcap/tiflow/issues/2758)
        - Reduce gRPC window size to avoid OOM [#2673](https://github.com/pingcap/tiflow/issues/2673)
        - Fix a gRPC `keepalive` error under high memory pressure [#2202](https://github.com/pingcap/tiflow/issues/2202)
        - Fix a bug that an unsigned `tinyint` causes TiCDC to panic [#2648](https://github.com/pingcap/tiflow/issues/2648)
        - Fix an empty value issue in TiCDC Open Protocol. An empty value is no longer output when there is no change in one transaction. [#2612](https://github.com/pingcap/tiflow/issues/2612)
        - Fix a bug in DDL handling during manual restarts [#2603](https://github.com/pingcap/tiflow/issues/2603)
        - Fix the issue that `EtcdWorker`'s snapshot isolation might be wrongly violated when managing the metadata [#2559](https://github.com/pingcap/tiflow/pull/2559)
        - Fix a bug that multiple processors might write data to the same table when TiCDC is rescheduling the table [#2230](https://github.com/pingcap/tiflow/issues/2230)
        - Fix a bug that changefeed might be reset unexpectedly when TiCDC gets the `ErrSchemaStorageTableMiss` error [#2422](https://github.com/pingcap/tiflow/issues/2422)
        - Fix a bug that changefeed cannot be removed when TiCDC gets the `ErrGCTTLExceeded` error [#2391](https://github.com/pingcap/tiflow/issues/2391)
        - Fix a bug that TiCDC fails to synchronize large tables to cdclog [#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
