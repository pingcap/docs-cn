---
title: TiDB 5.4.2 Release Notes
---

# TiDB 5.4.2 Release Notes

Release Date: July 8, 2022

TiDB version: 5.4.2

> **Warning:**
>
> It is not recommended to use v5.4.2, because this version has a known bug. For details, see [#12934](https://github.com/tikv/tikv/issues/12934). This bug is planned to be fixed in the upcoming v5.4.3.

## Improvements

+ TiDB

    - Avoid sending requests to unhealthy TiKV nodes to improve availability [#34906](https://github.com/pingcap/tidb/issues/34906)

+ TiKV

    - Reload TLS certificate automatically for each update to improve availability [#12546](https://github.com/tikv/tikv/issues/12546)
    - Improve the health check to detect unavailable Raftstore, so that the TiKV client can update Region Cache in time [#12398](https://github.com/tikv/tikv/issues/12398)
    - Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)

+ PD

    - Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)

+ Tools

    + TiDB Lightning

        - Optimize Scatter Region to batch mode to improve the stability of the Scatter Region process [#33618](https://github.com/pingcap/tidb/issues/33618)

## Bug Fixes

+ TiDB

    - Fix the issue of wrong TableDual plans cached in binary protocol [#34690](https://github.com/pingcap/tidb/issues/34690) [#34678](https://github.com/pingcap/tidb/issues/34678)
    - Fix the issue of incorrectly inferred null flag of the TiFlash `firstrow` aggregate function in the EqualAll case [#34584](https://github.com/pingcap/tidb/issues/34584)
    - Fix the issue that the planner generates wrong 2-phase aggregate plan for TiFlash [#34682](https://github.com/pingcap/tidb/issues/34682)
    - Fix the planner wrong behaviors that occur when `tidb_opt_agg_push_down` and `tidb_enforce_mpp` are enabled [#34465](https://github.com/pingcap/tidb/issues/34465)
    - Fix the wrong memory-usage value used when Plan Cache is evicted [#34613](https://github.com/pingcap/tidb/issues/34613)
    - Fix the issue that the column list does not work in the `LOAD DATA` statement [#35198](https://github.com/pingcap/tidb/issues/35198)
    - Avoid reporting `WriteConflict` errors in pessimistic transactions [#11612](https://github.com/tikv/tikv/issues/11612)
    - Fix the issue that the prewrite requests are not idempotency when Region errors and network issues occur [#34875](https://github.com/pingcap/tidb/issues/34875)
    - Fix the issue that the async commit transactions being rolled back might not meet atomicity [#33641](https://github.com/pingcap/tidb/issues/33641)
    - Previously, when a network connectivity issue occurred, TiDB did not always correctly free the resources held by the disconnected session. This issue has been fixed so that open transactions can be rolled back and other associated resources can be released. [#34722](https://github.com/pingcap/tidb/issues/34722)
    - Fix the issue that the `references invalid table` error might be incorrectly reported when TiDB queries views with CTE [#33965](https://github.com/pingcap/tidb/issues/33965)
    - Fix the panic issue caused by the `fatal error: concurrent map read and map write` error [#35340](https://github.com/pingcap/tidb/issues/35340)

+ TiKV

    - Fix the panic issue caused by analyzing statistics when `max_sample_size` is set to `0` [#11192](https://github.com/tikv/tikv/issues/11192)
    - Fix the potential issue of mistakenly reporting TiKV panics when exiting TiKV [#12231](https://github.com/tikv/tikv/issues/12231)
    - Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663)
    - Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825)
    - Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345)
    - Fix the issue of time parsing error that occurs when the `DATETIME` values contain a fraction and `Z` [#12739](https://github.com/tikv/tikv/issues/12739)
    - Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673)
    - Fix the possible duplicate commit records in pessimistic transactions when async commit is enabled [#12615](https://github.com/tikv/tikv/issues/12615)
    - Fix the issue that TiKV reports the `invalid store ID 0` error when using Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)
    - Fix the issue of TiKV panic caused by the race between destroying peers and batch splitting Regions [#12368](https://github.com/tikv/tikv/issues/12368)
    - Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12329](https://github.com/tikv/tikv/issues/12329)
    - Fix the issue of failing to start TiKV on AUFS [#12543](https://github.com/tikv/tikv/issues/12543)

+ PD

    - Fix the wrong status code of `not leader` [#4797](https://github.com/tikv/pd/issues/4797)
    - Fix the PD panic that occurs when a hot region has no leader [#5005](https://github.com/tikv/pd/issues/5005)
    - Fix the issue that scheduling cannot start immediately after the PD leader transfer [#4769](https://github.com/tikv/pd/issues/4769)
    - Fix a bug of TSO fallback in some corner cases [#4884](https://github.com/tikv/pd/issues/4884)

+ TiFlash

    - Fix the issue that TiFlash crashes after dropping a column of a table with clustered indexes in some situations [#5154](https://github.com/pingcap/tiflash/issues/5154)
    - Fix potential data inconsistency after a lot of INSERT and DELETE operations [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - Fix wrong decimal comparison results in corner cases [#4512](https://github.com/pingcap/tiflash/issues/4512)

+ Tools

    + Backup & Restore (BR)

        - Fix a bug that BR reports `ErrRestoreTableIDMismatch` in RawKV mode [#35279](https://github.com/pingcap/tidb/issues/35279)
        - Fix a bug that BR does not retry when an error occurs in saving files [#34865](https://github.com/pingcap/tidb/issues/34865)
        - Fix a panic issue when BR is running [#34956](https://github.com/pingcap/tidb/issues/34956)
        - Fix the issue that BR cannot handle S3 internal errors [#34350](https://github.com/pingcap/tidb/issues/34350)
        - Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)

    + TiCDC

        - Fix data loss that occurs in special incremental scanning scenarios [#5468](https://github.com/pingcap/tiflow/issues/5468)
        - Fix a bug that the redo log manager flushes logs before writing logs [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix a bug that the resolved ts moves too fast when some tables are not maintained by the redo writer [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix the issue that file name conflicts may cause data loss [#5486](https://github.com/pingcap/tiflow/issues/5486)
        - Fix replication interruption that occurs when Region leader is missing and the retry exceeds the limit [#5230](https://github.com/pingcap/tiflow/issues/5230)
        - Fix the bug that MySQL Sink may save a wrong checkpointTs [#5107](https://github.com/pingcap/tiflow/issues/5107)
        - Fix a bug that may cause goroutine leak in the HTTP server [#5303](https://github.com/pingcap/tiflow/issues/5303)
        - Fix the issue that changes in meta Region can lead to latency increase [#4756](https://github.com/pingcap/tiflow/issues/4756) [#4762](https://github.com/pingcap/tiflow/issues/4762)

    + TiDB Data Migration (DM)

        - Fix the issue that DM occupies more disk space after a task automatically resumes [#5344](https://github.com/pingcap/tiflow/issues/5344)
        - Fix the issue that the uppercase table cannot be replicated when `case-sensitive: true` is not set [#5255](https://github.com/pingcap/tiflow/issues/5255)
