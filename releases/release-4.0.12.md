---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 Release Notes

Release date: April 2, 2021

TiDB version: 4.0.12

## New Features

+ TiFlash

    - Add tools to check the status of `tiflash replica` for online rolling updates

## Improvements

+ TiDB

    - Refine the output information of the `EXPLAIN` statement for the `batch cop` mode [#23164](https://github.com/pingcap/tidb/pull/23164)
    - Add the warning information for expressions that cannot be pushed to the storage layer in the output of the `EXPLAIN` statement [#23020](https://github.com/pingcap/tidb/pull/23020)
    - Migrate a part of the DDL package code from `Execute`/`ExecRestricted` to the safe API (2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    - Migrate a part of the DDL package code from `Execute`/`ExecRestricted` to the safe API (1) [#22929](https://github.com/pingcap/tidb/pull/22929)
    - Add `optimization-time` and `wait-TS-time` into the slow log [#22918](https://github.com/pingcap/tidb/pull/22918)
    - Support querying `partition_id` from the `infoschema.partitions` table [#22489](https://github.com/pingcap/tidb/pull/22489)
    - Add `last_plan_from_binding` to help the users know whether a SQL statement's execution plan is matched with the hints in the binding [#21430](https://github.com/pingcap/tidb/pull/21430)
    - Scatter truncated tables without the `pre-split` option [#22872](https://github.com/pingcap/tidb/pull/22872)
    - Add three format specifiers for the `str_to_date` expression [#22812](https://github.com/pingcap/tidb/pull/22812)
    - Record the `PREPARE` execution failure as `Failed Query OPM` in the metrics monitor [#22672](https://github.com/pingcap/tidb/pull/22672)
    - Do not report errors for the `PREPARE` execution if `tidb_snapshot` is set [#22641](https://github.com/pingcap/tidb/pull/22641)

+ TiKV

    - Prevent a large number of reconnections in a short period of time [#9879](https://github.com/tikv/tikv/pull/9879)
    - Optimize the write operations and Batch Get in the scenarios of many tombstones [#9729](https://github.com/tikv/tikv/pull/9729)
    - Change the default value of `leader-transfer-max-log-lag` to `128` to increase the success rate of leader transfer [#9605](https://github.com/tikv/tikv/pull/9605)

+ PD

    - Update the Region cache only when `pending-peers` or `down-peers` changes, which reduces the pressure of updating heartbeats [#3471](https://github.com/pingcap/pd/pull/3471)
    - Prevent the Regions in `split-cache` from becoming the target of merge [#3459](https://github.com/pingcap/pd/pull/3459)

+ TiFlash

    - Optimize the configuration file and remove useless items
    - Reduce the size of TiFlash binary files
    - Use an adaptive aggressive GC strategy to reduce memory usage

+ Tools

    + TiCDC

        - Add a double confirmation when users create or resume the changefeed with the `start-ts` or `checkpoint-ts` 1 day before the current timestamp [#1497](https://github.com/pingcap/ticdc/pull/1497)
        - Add Grafana panels for the Old Value feature [#1571](https://github.com/pingcap/ticdc/pull/1571)

    + Backup & Restore (BR)

        - Log the `HTTP_PROXY` and `HTTPS_PROXY` environmental variables [#827](https://github.com/pingcap/br/pull/827)
        - Improve the backup performance when there are many tables [#745](https://github.com/pingcap/br/pull/745)
        - Report errors if the service safe point check fails [#826](https://github.com/pingcap/br/pull/826)
        - Add the `cluster_version` and `br_version` information in `backupmeta` [#803](https://github.com/pingcap/br/pull/803)
        - Add retry for external storage errors to increase the success rate of backup [#851](https://github.com/pingcap/br/pull/851)
        - Reduce memory usage during backup [#886](https://github.com/pingcap/br/pull/886)

    + TiDB Lightning

        - Check the TiDB cluster version before running TiDB Lightning to avoid unexpected errors [#787](https://github.com/pingcap/br/pull/787)
        - Fail fast when TiDB Lightning meets the `cancel` error [#867](https://github.com/pingcap/br/pull/867)
        - Add `tikv-importer.engine-mem-cache-size` and `tikv-importer.local-writer-mem-cache-size` configuration items to balance between memory usage and performance [#866](https://github.com/pingcap/br/pull/866)
        - Run `batch split region` in parallel for TiDB Lightning's Local-backend to increase the import speed [#868](https://github.com/pingcap/br/pull/868)
        - When using TiDB Lightning to import data from a S3 storage, TiDB Lightning no longer requires the `s3:ListBucket` permission [#919](https://github.com/pingcap/br/pull/919)
        - When resuming from a checkpoint, TiDB Lightning keeps using the original engine [#924](https://github.com/pingcap/br/pull/924)

## Bug Fixes

+ TiDB

    - Fix the issue that the `get` variable expression goes wrong when the session variable is hexadecimal literals[#23372](https://github.com/pingcap/tidb/pull/23372)
    - Fix the issue that wrong collation is used when creating the fast execution plan for the `Enum` or `Set` type [#23292](https://github.com/pingcap/tidb/pull/23292)
    - Fix the possible wrong result of the `nullif` expression when it is used with `is-null` [#23279](https://github.com/pingcap/tidb/pull/23279)
    - Fix the issue that the auto-analysis is triggered outside its time range [#23219](https://github.com/pingcap/tidb/pull/23219)
    - Fix the issue that the `CAST` function might ignore errors for the `point get` plan [#23211](https://github.com/pingcap/tidb/pull/23211)
    - Fix a bug that prevents SPM from taking effect when `CurrentDB` is empty [#23209](https://github.com/pingcap/tidb/pull/23209)
    - Fix the issue of possible wrong table filters for the IndexMerge plan [#23165](https://github.com/pingcap/tidb/pull/23165)
    - Fix the issue of unexpected `NotNullFlag` in the returning types of the `NULL` constant [#23135](https://github.com/pingcap/tidb/pull/23135)
    - Fix a bug that collation might not be handled by the text type [#23092](https://github.com/pingcap/tidb/pull/23092)
    - Fix the issue that the range partition might incorrectly handle the `IN` expression [#23074](https://github.com/pingcap/tidb/pull/23074)
    - Fix the issue that after marking a TiKV store as tombstone, starting new TiKV stores with different StoreIDs with the same IP address and port keeps returning the `StoreNotMatch` error [#23071](https://github.com/pingcap/tidb/pull/23071)
    - Do not adjust the `INT` type when it is `NULL` and compared with `YEAR` [#22844](https://github.com/pingcap/tidb/pull/22844)
    - Fix the issue of lost connection when loading data on tables with the `auto_random` column [#22736](https://github.com/pingcap/tidb/pull/22736)
    - Fix the issue of DDL hangover when the DDL operation meets panic in the cancelling path [#23297](https://github.com/pingcap/tidb/pull/23297)
    - Fix the wrong key range of index scan when comparing the `YEAR` column with `NULL` [#23104](https://github.com/pingcap/tidb/pull/23104)
    - Fix the issue that a successfully created view is failed to use [#23083](https://github.com/pingcap/tidb/pull/23083)

+ TiKV

    - Fix the issue that the `IN` expression does not properly handle unsigned/signed integers [#9850](https://github.com/tikv/tikv/pull/9850)
    - Fix the issue that the ingest operation is not re-entrant [#9779](https://github.com/tikv/tikv/pull/9779)
    - Fix the issue that the space is missed when converting JSON to string in TiKV coprocessor [#9666](https://github.com/tikv/tikv/pull/9666)

+ PD

    - Fix a bug that the isolation level is wrong when the store lacks the label [#3474](https://github.com/pingcap/pd/pull/3474)

+ TiFlash

    - Fix the issue of incorrect execution results when the default value of the `binary` type column contains leading or tailing zero bytes
    - Fix a bug that TiFlash fails to synchronize schema if the name of the database contains special characters
    - Fix the issue of incorrect results when handling the `IN` expression with decimal values
    - Fix a bug that the metric for the opened file count shown in Grafana is high
    - Fix a bug that TiFlash does not support the `Timestamp` literal
    - Fix the potential not responding issue while handling the `FROM_UNIXTIME` expression
    - Fix the issue of incorrect results when casting string as integer
    - Fix a bug that the `like` function might return wrong results

+ Tools

    + TiCDC

        - Fix a disorder issue of the `resolved ts` event [#1464](https://github.com/pingcap/ticdc/pull/1464)
        - Fix a data loss issue caused by wrong table scheduling due to the network problem [#1508](https://github.com/pingcap/ticdc/pull/1508)
        - Fix a bug of untimely release of resources after a processor is stopped [#1547](https://github.com/pingcap/ticdc/pull/1547)
        - Fix a bug that the transaction counter is not correctly updated, which might cause database connection leak [#1524](https://github.com/pingcap/ticdc/pull/1524)
        - Fix the issue that multiple owners can co-exist when PD has jitter, which might lead to table missing [#1540](https://github.com/pingcap/ticdc/pull/1540)

    + Backup & Restore (BR)

        - Fix a bug that `WalkDir` for the s3 storage returns `nil` if the target path is bucket name [#733](https://github.com/pingcap/br/pull/733)
        - Fix a bug that the `status` port is not served with TLS [#839](https://github.com/pingcap/br/pull/839)

    + TiDB Lightning

        - Fix the error that TiKV Importer might ignore that the file has already existed [#848](https://github.com/pingcap/br/pull/848)
        - Fix a bug that the TiDB Lightning might use the wrong timestamp and read the wrong data [#850](https://github.com/pingcap/br/pull/850)
        - Fix a bug that TiDB Lightning's unexpected exit might cause damaged checkpoint file [#889](https://github.com/pingcap/br/pull/889)
        - Fix the issue of possible data error that occurs because the `cancel` error is ignored [#874](https://github.com/pingcap/br/pull/874)
