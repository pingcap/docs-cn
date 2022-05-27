---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 Release Notes

Release date: January 15, 2021

TiDB version: 4.0.10

## New Features

+ PD

    - Add the `enable-redact-log` configuration item to redact user data from logs [#3266](https://github.com/pingcap/pd/pull/3266)

+ TiFlash

    - Add the `security.redact_info_log` configuration item to redact user data from logs

## Improvements

+ TiDB

    - Make the size limit of a key-value entry in transaction configurable using `txn-entry-size-limit` [#21843](https://github.com/pingcap/tidb/pull/21843)

+ PD

    - Optimize the `store-state-filter` metrics to show more information [#3100](https://github.com/tikv/pd/pull/3100)
    - Upgrade the `go.etcd.io/bbolt` dependency to v1.3.5 [#3331](https://github.com/tikv/pd/pull/3331)

+ Tools

    + TiCDC

        - Enable the old value feature for the `maxwell` protocol [#1144](https://github.com/pingcap/tiflow/pull/1144)
        - Enable the unified sorter feature by default [#1230](https://github.com/pingcap/tiflow/pull/1230)

    + Dumpling

        - Support checking unrecognized arguments and printing the current progress during dumping [#228](https://github.com/pingcap/dumpling/pull/228)

    + TiDB Lightning

        - Support retrying the error that occurs when reading from S3 [#533](https://github.com/pingcap/tidb-lightning/pull/533)

## Bug Fixes

+ TiDB

    - Fix a concurrency bug that might cause the batch client timeout [#22336](https://github.com/pingcap/tidb/pull/22336)
    - Fix the issue of duplicate bindings caused by concurrent baseline capture [#22295](https://github.com/pingcap/tidb/pull/22295)
    - Make the baseline capture bound to the SQL statement work when the log level is `'debug'` [#22293](https://github.com/pingcap/tidb/pull/22293)
    - Correctly release GC locks when Region merge occurs [#22267](https://github.com/pingcap/tidb/pull/22267)
    - Return correct values for user variables of the `datetime` type [#22143](https://github.com/pingcap/tidb/pull/22143)
    - Fix the issue of using index merge when there are multiple table filters [#22124](https://github.com/pingcap/tidb/pull/22124)
    - Fix the `wrong precision` issue in TiFlash caused by the `prepare` plan cache [#21960](https://github.com/pingcap/tidb/pull/21960)
    - Fix the issue of incorrect results caused by schema change [#21596](https://github.com/pingcap/tidb/pull/21596)
    - Avoid unnecessary column flag changes in `ALTER TABLE` [#21474](https://github.com/pingcap/tidb/pull/21474)
    - Set the database name for table aliases of query blocks used in optimizer hints [#21380](https://github.com/pingcap/tidb/pull/21380)
    - Generate the proper optimizer hint for `IndexHashJoin` and `IndexMergeJoin` [#21020](https://github.com/pingcap/tidb/pull/21020)

+ TiKV

    - Fix the wrong mapping between ready and peer [#9409](https://github.com/tikv/tikv/pull/9409)
    - Fix the issue that some logs are not redacted when `security.redact-info-log` is set to `true` [#9314](https://github.com/tikv/tikv/pull/9314)

+ PD

    - Fix the issue that the ID allocation is not monotonic [#3308](https://github.com/tikv/pd/pull/3308) [#3323](https://github.com/tikv/pd/pull/3323)
    - Fix the issue that the PD client might be blocked in some cases [#3285](https://github.com/pingcap/pd/pull/3285)

+ TiFlash

    - Fix the issue that TiFlash fails to start because TiFlash fails to process the TiDB schema of an old version
    - Fix the issue that TiFlash fails to start due to incorrect handling of `cpu_time` on the RedHat system
    - Fix the issue that TiFlash fails to start when `path_realtime_mode` is set to `true`
    - Fix an issue of incorrect results when calling the `substr` function with three parameters
    - Fix the issue that TiFlash does not support changing the `Enum` type even if the change is lossless

+ Tools

    + TiCDC

        - Fix the `maxwell` protocol issues, including the issue of `base64` data output and the issue of outputting TSO to unix timestamp [#1173](https://github.com/pingcap/tiflow/pull/1173)
        - Fix a bug that outdated metadata might cause the newly created changefeed abnormal [#1184](https://github.com/pingcap/tiflow/pull/1184)
        - Fix the issue of creating the receiver on the closed notifier [#1199](https://github.com/pingcap/tiflow/pull/1199)
        - Fix a bug that the TiCDC owner might consume too much memory in the etcd watch client [#1227](https://github.com/pingcap/tiflow/pull/1227)
        - Fix the issue that `max-batch-size` does not take effect [#1253](https://github.com/pingcap/tiflow/pull/1253)
        - Fix the issue of cleaning up stale tasks before the capture information is constructed [#1280](https://github.com/pingcap/tiflow/pull/1280)
        - Fix the issue that the recycling of db conn is block because `rollback` is not called in MySQL sink [#1285](https://github.com/pingcap/tiflow/pull/1285)

    + Dumpling

        - Avoid TiDB out of memory (OOM) by setting the default behavior of [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) [#233](https://github.com/pingcap/dumpling/pull/233)

    + Backup & Restore (BR)

        - Fix the issue that BR v4.0.9 cannot restore the files backed up using BR v4.0.8 on GCS [#688](https://github.com/pingcap/br/pull/688)
        - Fix the issue that BR panics when the GCS storage URL has no prefix [#673](https://github.com/pingcap/br/pull/673)
        - Disable backup statistics by default to avoid BR OOM [#693](https://github.com/pingcap/br/pull/693)

    + TiDB Binlog

        - Fix the issue that when the `AMEND TRANSACTION` feature is enabled, Drainer might choose the incorrect schema version to generate SQL statements [#1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    + TiDB Lightning

        - Fix a bug that the Region is not split because the Region key is incorrectly encoded [#531](https://github.com/pingcap/tidb-lightning/pull/531)
        - Fix the issue that the failure of `CREATE TABLE` might be lost when multiple tables are created [#530](https://github.com/pingcap/tidb-lightning/pull/530)
        - Fix the issue of `column count mismatch` when using the TiDB-backend [#535](https://github.com/pingcap/tidb-lightning/pull/535)
