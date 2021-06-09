---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 Release Notes

Release date: May 28, 2021

TiDB version: 4.0.13

## New Features

+ TiDB

    - Support changing an `AUTO_INCREMENT` column to an `AUTO_RANDOM` one [#24608](https://github.com/pingcap/tidb/pull/24608)
    - Add the `infoschema.client_errors_summary` tables to help users keep track of the errors that have been returned to clients [#23267](https://github.com/pingcap/tidb/pull/23267)

## Improvements

+ TiDB

    - Avoid frequently reading the `mysql.stats_histograms` table if the cached statistics is up-to-date to avoid high CPU usage [#24352](https://github.com/pingcap/tidb/pull/24352)

+ TiKV

    - Make the calculation process of `store used size` more precise [#9904](https://github.com/tikv/tikv/pull/9904)
    - Set more Regions in the `EpochNotMatch` message to reduce Region misses [#9731](https://github.com/tikv/tikv/pull/9731)
    - Speed up freeing the memory accumulated in the long-running cluster [#10035](https://github.com/tikv/tikv/pull/10035)

+ PD

    - Optimize the metrics of TSO processing time to help users determine whether the TSO processing time at the PD side is too long [#3524](https://github.com/pingcap/pd/pull/3524)
    - Update the dashboard version to v2021.03.12.1 [#3469](https://github.com/pingcap/pd/pull/3469)

+ TiFlash

    - Automatically clean archived data to free up disk space

+ Tools

    + Backup & Restore (BR)

        - Support backing up user tables created in the `mysql` schema [#1077](https://github.com/pingcap/br/pull/1077)
        - Update `checkVersion` to check the cluster data and the backup data [#1090](https://github.com/pingcap/br/pull/1090)
        - Tolerate a small number of TiKV node failures during backup [#1062](https://github.com/pingcap/br/pull/1062)

    + TiCDC

        - Implement the processor flow control to avoid memory overflow (OOM) [#1751](https://github.com/pingcap/ticdc/pull/1751)
        - Support cleaning up stale temporary files in Unified Sorter and prevent multiple `cdc server` instances from sharing the same `sort-dir` directory [#1741](https://github.com/pingcap/ticdc/pull/1741)
        - Add the HTTP handler for the failpoint [#1732](https://github.com/pingcap/ticdc/pull/1732)

## Bug Fixes

+ TiDB

    - Fix the panic issue that occurs when the `UPDATE` statement with a subquery updates the generated column [#24658](https://github.com/pingcap/tidb/pull/24658)
    - Fix the issue that causes duplicate query results when using the multi-column index for data reads [#24634](https://github.com/pingcap/tidb/pull/24634)
    - Fix the issue that causes wrong query result when using the `BIT` type constant as the divisor in the DIV expression [#24266](https://github.com/pingcap/tidb/pull/24266)
    - Fix the issue that the `NO_ZERO_IN_DATE` SQL mode does not take effect for the default column value set in DDL statements [#24185](https://github.com/pingcap/tidb/pull/24185)
    - Fix an issue which causes wrong query results when using `UNION` between a `BIT` type column and an `INTEGER` type column [#24026](https://github.com/pingcap/tidb/pull/24026)
    - Fix the issue that the `TableDual` plans are mistakenly created when comparing the `BINARY` type and the `CHAR` type [#23917](https://github.com/pingcap/tidb/pull/23917)
    - Fix the issue that the `insert ignore on duplicate` statement might unexpectedly delete table records [#23825](https://github.com/pingcap/tidb/pull/23825)
    - Fix the issue that the Audit plugin causes TiDB panic [#23819](https://github.com/pingcap/tidb/pull/23819)
    - Fix the issue that the `HashJoin` operator incorrectly processes the collation [#23812](https://github.com/pingcap/tidb/pull/23812)
    - Fix the issue of disconnection that occurs when `batch_point_get` incorrectly handles abnormal values in the pessimistic transaction [#23778](https://github.com/pingcap/tidb/pull/23778)
    - Fix the issue of inconsistent indexes that occurs when the `tidb_row_format_version` configuration value is set to `1` and the `enable_new_collation` value is set to `true` [#23772](https://github.com/pingcap/tidb/pull/23772)
    - Fix a bug that occurs when comparing the `INTEGER` type column with the `STRING` constant value [#23705](https://github.com/pingcap/tidb/pull/23705)
    - Fix the error that occurs when the `BIT` type column is passed into the `approx_percent` function [#23702](https://github.com/pingcap/tidb/pull/23702)
    - Fix a bug that causes TiDB to mistakenly report the `TiKV server timeout` error when executing TiFlash batch requests [#23700](https://github.com/pingcap/tidb/pull/23700)
    - Fix the issue that the `IndexJoin` operator returns wrong results on the prefix column index [#23691](https://github.com/pingcap/tidb/pull/23691)
    - Fix the issue which causes wrong query results because the collation on the `BINARY` type column is not properly handled [#23598](https://github.com/pingcap/tidb/pull/23598)
    - Fix the issue of query panic that occurs when the `UPDATE` statement contains the join query with the `HAVING` clause [#23575](https://github.com/pingcap/tidb/pull/23575)
    - Fix the issue that causes TiFlash to return wrong results when using the `NULL` constant in the comparison expression [#23474](https://github.com/pingcap/tidb/pull/23474)
    - Fix the issue of wrong results when comparing the `YEAR` type column with the `STRING` constant [#23335](https://github.com/pingcap/tidb/pull/23335)
    - Fix the issue that `group_concat` panics when `session.group_concat_max_len` is set too small [#23257](https://github.com/pingcap/tidb/pull/23257)
    - Fix the issue of wrong query results that occurs when using the `BETWEEN` expression for the `TIME` type column [#23233](https://github.com/pingcap/tidb/pull/23233)
    - Fix the issue of privilege check in the `DELETE` statements [#23215](https://github.com/pingcap/tidb/pull/23215)
    - Fix the issue that no error is reported when inserting invalid strings to the `DECIMAL` type column [#23196](https://github.com/pingcap/tidb/pull/23196)
    - Fix the issue of parsing error occurred when inserting data to the `DECIMAL` type columns [#23152](https://github.com/pingcap/tidb/pull/23152)
    - Fix the issue that the `USE_INDEX_MERGE` hint does not take effect [#22924](https://github.com/pingcap/tidb/pull/22924)
    - Fix a bug that the query returns wrong results when using `ENUM` or `SET` columns in the `WHERE` clause as an filter [#22814](https://github.com/pingcap/tidb/pull/22814)
    - Fix a bug that the query returns wrong results when using the clustered index and the new collation at the same time [#21408](https://github.com/pingcap/tidb/pull/21408)
    - Fix the panic that occurs when executing `ANALYZE` with `enable_new_collation` enabled [#21299](https://github.com/pingcap/tidb/pull/21299)
    - Fix the issue that SQL views does not correctly handle the default roles associated with the SQL DEFINER [#24531](https://github.com/pingcap/tidb/pull/24531)
    - Fix the issue that cancelling DDL jobs gets stuck [#24445](https://github.com/pingcap/tidb/pull/24445)
    - Fix the issue that the `concat` function incorrectly handles the collation [#24300](https://github.com/pingcap/tidb/pull/24300)
    - Fix a bug that the query returns wrong results when the `SELECT` field has an `IN` subquery and the subquery's outer side contains `NULL` tuples [#24022](https://github.com/pingcap/tidb/pull/24022)
    - Fix a bug that TiFlash is chosen wrongly by the optimizer when `TableScan` is in descending order [#23974](https://github.com/pingcap/tidb/pull/23974)
    - Fix a bug that the `point_get` plan returns the column name that is inconsistent with that of MySQL [#23970](https://github.com/pingcap/tidb/pull/23970)
    - Fix the issue that executing the `show table status` statement on a database with a upper-cased name returns wrong results [#23958](https://github.com/pingcap/tidb/pull/23958)
    - Fix a bug that the users who do not have the `INSERT` and `DELETE` privileges on a table at the same time can perform the `REPLACE` operation [#23938](https://github.com/pingcap/tidb/pull/23938)
    - Fix the issue that the results of the `concat`/`make_set`/`insert` expressions are wrong because the collation is incorrectly handled [#23878](https://github.com/pingcap/tidb/pull/23878)
    - Fix the panic that occurs when executing a query on the table that has `RANGE` partitions [#23689](https://github.com/pingcap/tidb/pull/23689)
    - Fix the issue: In the cluster of an earlier version, if the `tidb_enable_table_partition` variable is set to `false`, the tables that contain partitions are handled as non-partitioned tables. Executing `batch point get` queries on this table, when the cluster is upgraded to a later version, causes connection panic. [#23682](https://github.com/pingcap/tidb/pull/23682)
    - Fix the issue that when TiDB is configured to listen on TCP and UNIX sockets, the remote hosts over the TCP connection are not correctly validated for connection [#23513](https://github.com/pingcap/tidb/pull/23513)
    - Fix a bug that the non-default collation causes wrong query results [#22923](https://github.com/pingcap/tidb/pull/22923)
    - Fix a bug that the **Coprocessor Cache** panel of Grafana does not work [#22617](https://github.com/pingcap/tidb/pull/22617)
    - Fix the error that occurs when the optimizer accesses the statistic cache [#22565](https://github.com/pingcap/tidb/pull/22565)

+ TiKV

    - Fix a bug that TiKV cannot start if the `file_dict` file is not fully written into the disk that has been full [#9963](https://github.com/tikv/tikv/pull/9963)
    - Limit TiCDC's scan speed at 128MB/s by default [#9983](https://github.com/tikv/tikv/pull/9983)
    - Reduce the memory usage of TiCDC's initial scan [#10133](https://github.com/tikv/tikv/pull/10133)
    - Support the back pressure for TiCDC's scan speed [#10142](https://github.com/tikv/tikv/pull/10142)
    - Fix a potential OOM issue by avoiding unnecessary reads to get TiCDC old values [#10031](https://github.com/tikv/tikv/pull/10031)
    - Fix a TiCDC OOM issue caused by reading old values [#10197](https://github.com/tikv/tikv/pull/10197)
    - Add a timeout mechanism for S3 storages to avoid the client hanging without responses [#10132](https://github.com/tikv/tikv/pull/10132)

+ TiFlash

    - Fix the issue that number of `delta-merge-tasks` is not reported to Prometheus
    - Fix the TiFlash panic issue that occurs during `Segment Split`
    - Fix the issue that the `Region write Duration (write blocks)` panel in Grafana is shown in a wrong place
    - Fix the potential issue that the storage engine fails to remove data
    - Fix the issue of incorrect results when casting the `TIME` type to the `INTEGER` type
    - Fix a bug that the behavior of the `bitwise` operator is different from that of TiDB
    - Fix the issue of incorrect results when casting the `STRING` type to the `INTEGER` type
    - Fix the issue that consecutive and fast writes might make TiFlash out of memory
    - Fix the potential issue that the exception of null pointer might be raised during the table GC
    - Fix the TiFlash panic issue that occurs when writing data to dropped tables
    - Fix the TiFlash panic issue that occurs during BR restore
    - Fix a bug that the weights of some characters are wrong when using the general CI collation
    - Fix the potential issue that data will be lost in tombstoned tables
    - Fix the issue of incorrect results when comparing the string which contains zero bytes
    - Fix the issue that the logical function returns wrong results if the input column contains null constants
    - Fix the issue that the logical function only accepts the numeric type
    - Fix the issue of incorrect results that occurs when the timestamp value is `1970-01-01` and the timezone offset is negative
    - Fix the issue that hash value of `Decimal256` is not stable

+ Tools

    + TiCDC

        - Fix the deadlock issue caused by the flow control when the sorter's input channel has been blocked [#1779](https://github.com/pingcap/ticdc/pull/1779)
        - Fix the issue that the TiKV GC safe point is blocked due to the stagnation of TiCDC changefeed checkpoint [#1756](https://github.com/pingcap/ticdc/pull/1756)
        - Revert the update in `explicit_defaults_for_timestamp` which requires the `SUPER` privilege when replicating data to MySQL [#1749](https://github.com/pingcap/ticdc/pull/1749)

    + TiDB Lightning

        - Fix a bug that TiDB Lightning's TiDB-backend cannot load any data when autocommit is disabled
