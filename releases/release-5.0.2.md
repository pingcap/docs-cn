---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

Release date: June 10, 2021

TiDB version: 5.0.2

## Compatibility Changes

+ Tools

    + TiCDC

        - Deprecate `--sort-dir` in the `cdc cli changefeed` command. Instead, users can set `--sort-dir` in the `cdc server` command. [#1795](https://github.com/pingcap/ticdc/pull/1795)

## New Features

+ TiKV

    - Enable the Hibernate Region feature by default [#10266](https://github.com/tikv/tikv/pull/10266)

## Improvements

+ TiDB

    - Avoid frequently reading the `mysql.stats_histograms` table if the cached statistics is up-to-date to avoid high CPU usage [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiKV

    - BR now supports the S3-compatible storage using the virtual-host addressing mode [#10243](https://github.com/tikv/tikv/pull/10243)
    - Support the back pressure for TiCDC's scan speed [#10151](https://github.com/tikv/tikv/pull/10151)
    - Reduce the memory usage of TiCDC's initial scan [#10133](https://github.com/tikv/tikv/pull/10133)
    - Improve the cache hit ratio of the TiCDC's Old Value feature in the pessimistic transaction [#10089](https://github.com/tikv/tikv/pull/10089)
    - Split Regions more evenly [#10086](https://github.com/tikv/tikv/pull/10086)

+ TiFlash

    - Optimize the table lock to prevent DDL jobs and data reads from blocking each other
    - Support casting the `INTEGER` or `REAL` type to `REAL` type

+ Tools

    + TiCDC

        - Add monitoring metrics for the table memory consumption [#1885](https://github.com/pingcap/ticdc/pull/1885)
        - Optimize the memory and CPU usages during the sorting stage [#1863](https://github.com/pingcap/ticdc/pull/1863)
        - Delete some useless log information that might cause user confusion [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        - Clarify some ambiguous error messages [#1132](https://github.com/pingcap/br/pull/1132)
        - Support checking the cluster version of a backup [#1091](https://github.com/pingcap/br/pull/1091)
        - Support backing up and restoring system tables in the `mysql` schema [#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)

    + Dumpling

        - Fix the issue that no error is output when a backup operation fails [#280](https://github.com/pingcap/dumpling/pull/280)

## Bug Fixes

+ TiDB

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
    - Fix the issue that numeric literals cannot be recognized when the sql_mode contains `ANSI_QUOTES` [#24522](https://github.com/pingcap/tidb/pull/24522)
    - Forbid statements such as `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` to read data from non-listed partitions [#24746](https://github.com/pingcap/tidb/issues/24746)
    - Fix the potential `index out of range` error when a SQL statement contains both `GROUP BY` and `UNION` [#24281](https://github.com/pingcap/tidb/issues/24281)
    - Fix the issue that the `CONCAT` function incorrectly handles the collation [#24296](https://github.com/pingcap/tidb/issues/24296)
    - Fix the issue that the `collation_server` global variable does not take effect in new sessions [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiKV

    - Fix a TiCDC OOM issue caused by reading old values [#9996](https://github.com/tikv/tikv/issues/9996) [#9981](https://github.com/tikv/tikv/issues/9981)
    - Fix the issue of empty value in the secondary index for the clustered primary key column when collation is `latin1_bin` [#24548](https://github.com/pingcap/tidb/issues/24548)
    - Add the `abort-on-panic` configuration, which allows TiKV to generate the core dump file when panic occurs. Users still need to correctly configure the environment to enable core dump [#10216](https://github.com/tikv/tikv/pull/10216)
    - Fix the performance regression issue of `point get` queries that occurs when TiKV is not busy [#10046](https://github.com/tikv/tikv/issues/10046)

+ PD

    - Fix the issue that the PD Leader re-election is slow when there are many stores [#3697](https://github.com/tikv/pd/issues/3697)
    - Fix the panic issue that occurs when removing the evict leader scheduler from a non-existent store [#3660](https://github.com/tikv/pd/issues/3660)
    - Fix the issue that the statistics are not updated after offline peers are merged [#3611](https://github.com/tikv/pd/issues/3611)

+ TiFlash

    - Fix the issue of incorrect results when cloning shared delta index concurrently
    - Fix the potential issue that TiFlash fails to restart with incomplete data
    - Fix the issue that old dm files are not removed automatically
    - Fix the potential panic that occurs when the Compaction Filter feature is enabled
    - Fix the potential issue that `ExchangeSender` sends duplicated data
    - Fix the issue that TiFlash cannot resolve the lock fallen back from async commit
    - Fix the issue of incorrect results returned when the casted result of the `TIMEZONE` type contains the `TIMESTAMP` type
    - Fix the TiFlash panic issue that occurs during Segment Split
    - Fix the issue that the execution information about the non-root MPP task is not accurate

+ Tools

    + TiCDC

        - Fix the issue that the time zone information is lost in the Avro output [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - Support cleaning up stale temporary files in Unified Sorter and forbid sharing the `sort-dir` directory [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - Fix a deadlock bug in the KV client that occurs when many stale Regions exist [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - Fix the wrong help information in the `--cert-allowed-cn` flag [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - Revert the update for `explicit_defaults_for_timestamp` which requires the `SUPER` privilege when replicating data to MySQL [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - Support the sink flow control to reduce the risk of memory overflow [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - Fix a bug that the replication task might stop when moving a table [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - Fix the issue that the TiKV GC safe point is blocked due to the stagnation of TiCDC changefeed checkpoint [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        - Fix the issue that the `DELETE` events are lost during the log restore [#1063](https://github.com/pingcap/br/issues/1063)
        - Fix a bug that causes BR to send too many useless RPC requests to TiKV [#1037](https://github.com/pingcap/br/pull/1037)
        - Fix the issue that no error is output when a backup operation fails [#1043](https://github.com/pingcap/br/pull/1043)

    + TiDB Lightning

        - Fix the issue of TiDB Lightning panic that occurs when generating KV data [#1127](https://github.com/pingcap/br/pull/1127)
        - Fix the issue that TiDB Lightning in the TiDB-backend mode cannot load any data when the autocommit is disabled [#1104](https://github.com/pingcap/br/issues/1104)
        - Fix a bug that the batch split Region fails due to the total key size exceeding the raft entry limit during the data import [#969](https://github.com/pingcap/br/issues/969)
