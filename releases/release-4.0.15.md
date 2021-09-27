---
title: TiDB 4.0.15 Release Notes
---

# TiDB 4.0.15 Release Notes

Release Date: September 27, 2021

TiDB version: 4.0.15

## Compatibility changes

+ TiDB

    - Fix the issue that executing `SHOW VARIABLES` in a new session is slow. This fix reverts some changes made in [#21045](https://github.com/pingcap/tidb/pull/21045) and might cause compatibility issues. [#24326](https://github.com/pingcap/tidb/issues/24326)
    + The following bug fixes change execution results, which might cause upgrade incompatibilities:
        - Fix the issue that `greatest(datetime) union null` returns empty string [#26532](https://github.com/pingcap/tidb/issues/26532)
        - Fix the issue that the `having` clause might not work correctly [#26496](https://github.com/pingcap/tidb/issues/26496)
        - Fix the wrong execution results that occur when the collations around the `between` expression are different [#27146](https://github.com/pingcap/tidb/issues/27146)
        - Fix the result wrong that occurs when the argument of the `extract` function is a negative duration [#27236](https://github.com/pingcap/tidb/issues/27236)
        - Fix the wrong execution results that occur when the column in the `group_concat` function has a non-bin collation [#27429](https://github.com/pingcap/tidb/issues/27429)
        - Fix the issue of wrong character set and collation for the `case when` expression [#26662](https://github.com/pingcap/tidb/issues/26662)
        - Fix the issue that column information is missed when converting the `Apply` operator to `Join` [#27233](https://github.com/pingcap/tidb/issues/27233)
        - Fix the issue of unexpected behavior when casting the invalid string to `DATE` [#26762](https://github.com/pingcap/tidb/issues/26762)
        - Fix a bug that the `count distinct` result on multiple columns is wrong when the new collation is enabled [#27091](https://github.com/pingcap/tidb/issues/27091)

## Feature enhancement

+ TiKV

    - Support changing TiCDC configurations dynamically [#10645](https://github.com/tikv/tikv/issues/10645)

## Improvements

+ TiDB

    - Trigger auto-analyze based on the histogram row count [#24237](https://github.com/pingcap/tidb/issues/24237)

+ TiKV

    - Handle read ready and write ready separately to reduce read latency [#10475](https://github.com/tikv/tikv/issues/10475)
    - The slow log of TiKV coprocessor only considers the time spent on processing requests. [#10841](https://github.com/tikv/tikv/issues/10841)
    - Drop log instead of blocking threads when the slogger thread is overloaded and the queue is filled up [#10841](https://github.com/tikv/tikv/issues/10841)
    - Reduce the size of Resolved TS messages to save network bandwidth [#2448](https://github.com/pingcap/ticdc/issues/2448)

+ PD

    - Improve the performance of synchronizing Region information between PDs [#3932](https://github.com/tikv/pd/pull/3932)

+ Tools

    + Backup & Restore (BR)

        - Split and scatter Regions concurrently to improve restore speed [#1363](https://github.com/pingcap/br/pull/1363)
        - Retry BR tasks when encountering the PD request error or the TiKV I/O timeout error [#27787](https://github.com/pingcap/tidb/issues/27787)
        - Reduce empty Regions when restoring many small tables to avoid affecting cluster operations after the restore [#1374](https://github.com/pingcap/br/issues/1374)
        - Perform the `rebase auto id` operation while creating tables, which saves the separate `rebase auto id` DDL operation and speeds up restore [#1424](https://github.com/pingcap/br/pull/1424)

    + Dumpling

        - Filter the skipped databases before getting the table information to improve the filtering efficiency of `SHOW TABLE STATUS` [#337](https://github.com/pingcap/dumpling/pull/337)
        - Use `SHOW FULL TABLES` to get table information for tables to be exported, because `SHOW TABLE STATUS` cannot work properly in some MySQL versions [#322](https://github.com/pingcap/dumpling/issues/322)
        - Support backing up MySQL-compatible databases that do not support the `START TRANSACTION ... WITH CONSISTENT SNAPSHOT` or the `SHOW CREATE TABLE` syntax [#309](https://github.com/pingcap/dumpling/issues/309)
        - Refine the Dumpling warning log to avoid the misleading information that a dump fails [#340](https://github.com/pingcap/dumpling/pull/340)

    + TiDB Lightning

        - Support importing data into tables that have expression index or the index that depends on virtual generated columns [#1404](https://github.com/pingcap/br/issues/1404)

    + TiCDC

        - Always pulls old values from TiKV internally to improve usability [#2397](https://github.com/pingcap/ticdc/pull/2397)
        - Reduce the goroutine usage when a table's Regions are all transferred away from a TiKV node [#2284](https://github.com/pingcap/ticdc/issues/2284)
        - Optimize workerpool for fewer goroutines when concurrency is high [#2211](https://github.com/pingcap/ticdc/issues/2211)
        - Execute DDL statements asynchronously to avoid affecting other changefeeds [#2295](https://github.com/pingcap/ticdc/issues/2295)
        - Add a global gRPC connection pool and share gRPC connections among KV clients [#2531](https://github.com/pingcap/ticdc/pull/2531)
        - Fail fast for unrecoverable DML errors [#1724](https://github.com/pingcap/ticdc/issues/1724)
        - Optimize memory management when the Unified Sorter is using memory to sort data [#2553](https://github.com/pingcap/ticdc/issues/2553)
        - Add Prometheus metrics for DDL executions [#2595](https://github.com/pingcap/ticdc/issues/2595) [#2669](https://github.com/pingcap/ticdc/issues/2669)
        - Prohibit operating TiCDC clusters across major or minor versions [#2601](https://github.com/pingcap/ticdc/pull/2601)
        - Remove `file sorter` [#2325](https://github.com/pingcap/ticdc/pull/2325)
        - Clean up changefeed metrics when a changefeed is removed, and clean up processor metrics when a processor exits [#2156](https://github.com/pingcap/ticdc/issues/2156)
        - Optimize the lock-resolving algorithm after a Region is initialized [#2188](https://github.com/pingcap/ticdc/issues/2188)

## Bug fixes

+ TiDB

    - Fix a bug that collation is incorrectly set for binary literals when building ranges [#23672](https://github.com/pingcap/tidb/issues/23672)

    - Fix the "index out of range" error that occurs when a query includes both `GROUP BY` and `UNION` [#26553](https://github.com/pingcap/tidb/pull/26553)
    - Fix the issue that TiDB might fail to send requests if TiKV has tombstone stores [#23676](https://github.com/pingcap/tidb/issues/23676) [#24648](https://github.com/pingcap/tidb/issues/24648)
    - Remove the undocumented `/debug/sub-optimal-plan` HTTP API [#27264](https://github.com/pingcap/tidb/pull/27264)

+ TiKV

    - Fix the issue that BR reports the "file already exists" error when TDE is enabled during data restore [#1179](https://github.com/pingcap/br/issues/1179)
    - Fix the potential disk full issue caused by corrupted snapshot files [#10813](https://github.com/tikv/tikv/issues/10813)
    - Fix the issue that TiKV deletes stale Regions too frequently [#10680](https://github.com/tikv/tikv/issues/10680)
    - Fix the issue that TiKV frequently reconnects the PD client [#9690](https://github.com/tikv/tikv/issues/9690)
    - Check stale file information from the encryption file dictionary [#9115](https://github.com/tikv/tikv/issues/9115)

+ PD

    - Fix the issue that PD does not fix the down peers in time [#4077](https://github.com/tikv/pd/issues/4077)
    - Fix a bug that PD might panic when scaling out TiKV [#3868](https://github.com/tikv/pd/issues/3868)

+ TiFlash

    - Fix the potential issue of data inconsistency that occurs when TiFlash is deployed on multiple disks
    - Fix a bug of incorrect results that occurs when queries contain filters like `CONSTANT`, `<`, `<=`, `>`, `>=`, or `COLUMN`
    - Fix the issue that the store size in metrics is inaccurate under heavy writing
    - Fix a potential bug that TiFlash cannot restore data when deployed on multiple disks
    - Fix the potential issue that TiFlash cannot garbage-collect the delta data after running for a long time

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that the average speed is inaccurately calculated for backup and restore [#1405](https://github.com/pingcap/br/issues/1405)

    + TiCDC

        - Fix the `ErrSchemaStorageTableMiss` error that occurs when the DDL Job duplication is encountered in the integrated test [#2422](https://github.com/pingcap/ticdc/issues/2422)
        - Fix a bug that a changefeed cannot be removed if the `ErrGCTTLExceeded` error occurs [#2391](https://github.com/pingcap/ticdc/issues/2391)
        - Fix the issue that outdated capture might appear in the output of the `capture list` command [#2388](https://github.com/pingcap/ticdc/issues/2388)
        - Fix the deadlock issue in the TiCDC processor [#2017](https://github.com/pingcap/ticdc/pull/2017)
        - Fix a data inconsistency issue that occurs because multiple processors might write data to the same table when this table is being re-scheduled [#2230](https://github.com/pingcap/ticdc/issues/2230)
        - Fix a bug that the `EtcdWorker` snapshot isolation is violated in metadata management [#2557](https://github.com/pingcap/ticdc/pull/2557)
        - Fix the issue that the changefeed cannot be stopped due to the DDL sink error [#2552](https://github.com/pingcap/ticdc/issues/2552)
        - Fix the issue of TiCDC Open Protocol: TiCDC outputs an empty value when there is no change in a transaction [#2612](https://github.com/pingcap/ticdc/issues/2612)
        - Fix a bug that causes TiCDC to panic on the unsigned `TINYINT` type [#2648](https://github.com/pingcap/ticdc/issues/2648)
        - Decrease the gRPC window size to avoid the OOM that occurs when TiCDC captures too many Regions [#2202](https://github.com/pingcap/ticdc/issues/2202)
        - Fix the OOM issue that occurs when TiCDC captures too many Regions [#2673](https://github.com/pingcap/ticdc/issues/2673)
        - Fix the issue of process panic that occurs when encoding the data types such as `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar` into JSON [#2758](https://github.com/pingcap/ticdc/issues/2758)
        - Fix the a memory leak issue that might occur when creating a new changefeed [#2389](https://github.com/pingcap/ticdc/issues/2389)
        - Fix a bug that DDL handling fails when a changefeed starts at the finish TS of a schema change [#2603](https://github.com/pingcap/ticdc/issues/2603)
        - Fix the issue of potential DDL loss when the owner crashes when executing DDL statements [#1260](https://github.com/pingcap/ticdc/issues/1260)
        - Fix the issue of insecure concurrent access to the map in `SinkManager` [#2298](https://github.com/pingcap/ticdc/pull/2298)
