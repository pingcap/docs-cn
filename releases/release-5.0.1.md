---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 Release Notes

Release date: April 24, 2021

TiDB version: 5.0.1

## Compatibility change

- The default value of the [`committer-concurrency`](/tidb-configuration-file.md#committer-concurrency) configuration item is changed from `16` to `128`.

## Improvements

+ TiDB

    - Support the built-in function `VITESS_HASH()` [#23915](https://github.com/pingcap/tidb/pull/23915)

+ TiKV

    - Use `zstd` to compress the Region snapshot [#10005](https://github.com/tikv/tikv/pull/10005)

+ PD

    - Modify the Region score calculator to better satisfy isomerous stores [#3605](https://github.com/pingcap/pd/pull/3605)
    - Avoid unexpected statistics after adding the `scatter region` scheduler [#3602](https://github.com/pingcap/pd/pull/3602)

+ Tools

    + Backup & Restore (BR)

        - Remove some misleading information from the summary log [#1009](https://github.com/pingcap/br/pull/1009)

## Bug Fixes

+ TiDB

    - Fix the issue that the execution result of project elimination might be wrong when the projection result is empty [#24093](https://github.com/pingcap/tidb/pull/24093)
    - Fix the issue of wrong query results when a column contains `NULL` values in some cases [#24063](https://github.com/pingcap/tidb/pull/24063)
    - Forbid generating MPP plans when the scan contains virtual columns [#24058](https://github.com/pingcap/tidb/pull/24058)
    - Fix the wrong reuse of `PointGet` and `TableDual` in Plan Cache [#24043](https://github.com/pingcap/tidb/pull/24043)
    - Fix the error that occurs when the optimizer builds the `IndexMerge` plan for clustered indexes [#24042](https://github.com/pingcap/tidb/pull/24042)
    - Fix the type inference of the BIT-type errors [#24027](https://github.com/pingcap/tidb/pull/24027)
    - Fix the issue that some optimizer hints do not take effect when the `PointGet` operator exists [#23685](https://github.com/pingcap/tidb/pull/23685)
    - Fix the issue that DDL operations might fail when rolling back due to an error [#24080](https://github.com/pingcap/tidb/pull/24080)
    - Fix the issue that the index range of the binary literal constant is incorrectly built [#24041](https://github.com/pingcap/tidb/pull/24041)
    - Fix the potential wrong results of the `IN` clause in some cases [#24023](https://github.com/pingcap/tidb/pull/24023)
    - Fix the wrong results of some string functions  [#23879](https://github.com/pingcap/tidb/pull/23879)
    - Users now need both `INSERT` and `DELETE` privileges on a table to perform `REPLACE` operations [#23939](https://github.com/pingcap/tidb/pull/23939)
    - Fix the performance regression when executing the point query [#24070](https://github.com/pingcap/tidb/pull/24070)
    - Fix the wrong `TableDual` plans caused by incorrectly comparing binaries and bytes [#23918](https://github.com/pingcap/tidb/pull/23918)

+ TiKV

    - Fix the issue that the coprocessor fails to properly handle the signed or unsigned integer types in the `IN` expression [#10018](https://github.com/tikv/tikv/pull/10018)
    - Fix the issue of many empty Regions after batch ingesting SST files [#10015](https://github.com/tikv/tikv/pull/10015)
    - Fix the potential panic that occurs when the input of `cast_string_as_time` is invalid UTF-8 bytes [#9995](https://github.com/tikv/tikv/pull/9995)
    - Fix a bug that TiKV cannot start up after the file dictionary file is damaged [#9992](https://github.com/tikv/tikv/pull/9992)

+ TiFlash

    - Fix the issue that the storage engine fails to remove the data of some ranges
    - Fix the issue of incorrect results when casting the time type to the integer type
    - Fix a bug that the `receiver` cannot find corresponding tasks within 10 seconds
    - Fix the issue that there might be invalid iterators in `cancelMPPQuery`
    - Fix a bug that the behavior of the `bitwise` operator is different from that of TiDB
    - Fix the alert issue caused by overlapping ranges when using the `prefix key`
    - Fix the issue of incorrect results when casting the string type to the integer type
    - Fix the issue that consecutive and fast writes might make TiFlash out of memory
    - Fix the issue that duplicated column names will make TiFlash raise errors
    - Fix the issue that TiFlash fails to parse MPP plans
    - Fix the potential issue that the exception of null pointer might be raised during the table GC
    - Fix the TiFlash panic issue that occurs when writing data to dropped tables
    - Fix the issue that TiFlash might panic during BR restore

+ Tools

    + TiDB Lightning

        - Fix the issue of the inaccurate table count in the progress log during the import [#1005](https://github.com/pingcap/br/pull/1005)

    + Backup & Restore (BR)

        - Fix a bug that the actual backup speed exceeds the `--ratelimit` limit [#1026](https://github.com/pingcap/br/pull/1026)
        - Fix the issue of backup interruption caused by the failure of a few TiKV nodes [#1019](https://github.com/pingcap/br/pull/1019)
        - Fix the issue of the inaccurate table count in the progress log during TiDB Lightning's import [#1005](https://github.com/pingcap/br/pull/1005)

    + TiCDC

        - Fix the concurrency issue in Unified Sorter and filter the unhelpful error messages [#1678](https://github.com/pingcap/ticdc/pull/1678)
        - Fix a bug that the creation of redundant directories might interrupt the replication with MinIO [#1672](https://github.com/pingcap/ticdc/pull/1672)
        - Set the default value of the `explicit_defaults_for_timestamp` session variable to `ON` to make the MySQL 5.7 downstream keep the same behavior with the upstream TiDB [#1659](https://github.com/pingcap/ticdc/pull/1659)
        - Fix the issue that the incorrect handling of `io.EOF` might cause replication interruption [#1648](https://github.com/pingcap/ticdc/pull/1648)
        - Correct the TiKV CDC endpoint CPU metric in the TiCDC dashboard [#1645](https://github.com/pingcap/ticdc/pull/1645)
        - Increase `defaultBufferChanSize` to avoid replication blocking in some cases [#1632](https://github.com/pingcap/ticdc/pull/1632)
