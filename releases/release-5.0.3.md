---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

Release date: July 2, 2021

TiDB version: 5.0.3

## Compatibility Changes

+ TiDB

    - After a v4.0 cluster is upgraded to v5.0 or a later version (dev or v5.1), the default value of the `tidb_multi_statement_mode` variable changes from `WARN` to `OFF`
    - TiDB is now compatible with MySQL 5.7's noop variable `innodb_default_row_format`. Setting this variable will have no effect. [#23541](https://github.com/pingcap/tidb/issues/23541)

## Feature Enhancements

+ Tools

    + TiCDC

        - Add an HTTP API to get the changefeed information and the health information of the node [#1955](https://github.com/pingcap/ticdc/pull/1955)
        - Add the SASL/SCRAM support for the kafka sink [#1942](https://github.com/pingcap/ticdc/pull/1942)
        - Make TiCDC support `--data-dir` at the server level [#2070](https://github.com/pingcap/ticdc/pull/2070)

## Improvements

+ TiDB

    - Support pushing down the `TopN` operator to TiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)
    - Support pushing down the built-in function `json_unquote()` to TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)
    - Support removing the union branch from the dual table [#25614](https://github.com/pingcap/tidb/pull/25614)
    - Support pushing down the built-in function `replace()` to TiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)
    - Support pushing down the built-in functions `unix_timestamp()`, `concat()`, `year()`, `day()`, `datediff()`, `datesub()`, and `concat_ws()` to TiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)
    - Optimize the aggregate operator's cost factor [#25241](https://github.com/pingcap/tidb/pull/25241)
    - Support pushing down the `Limit` operator to TiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)
    - Support pushing down the built-in function `str_to_date` to TiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)
    - Allow the MPP outer join to choose the build table based on the table row count [#25142](https://github.com/pingcap/tidb/pull/25142)
    - Support pushing down the built-in functions `left()`, `right()`, and `abs()` to TiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)
    - Support pushing down the Broadcast Cartesian join to TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)
    - Support pushing down the `Union All` operator to TiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)
    - Support balancing the MPP query workload among different TiFlash nodes based on Regions [#24724](https://github.com/pingcap/tidb/pull/24724)
    - Support invalidating stale Regions in the cache after the MPP query is executed [#24432](https://github.com/pingcap/tidb/pull/24432)
    - Improve the MySQL compatibility of the built-in function `str_to_date` for the format specifiers `%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)

+ TiKV

    - Limit the TiCDC sink's memory consumption [#10305](https://github.com/tikv/tikv/pull/10305)
    - Add the memory-bounded upper limit for the TiCDC old value cache [#10313](https://github.com/tikv/tikv/pull/10313)

+ PD

    - Update TiDB Dashboard to v2021.06.15.1 [#3798](https://github.com/pingcap/pd/pull/3798)

+ TiFlash

    - Support casting the `STRING` type to the `DOUBLE` type
    - Support the `STR_TO_DATE()` function
    - Optimize the non-joined data in right outer join using multiple threads
    - Support the Cartesian join
    - Support the `LEFT()` and `RIGHT()` functions
    - Support automatically invalidating stale Regions in MPP queries
    - Support the `ABS()` function

+ Tools

    + TiCDC

        - Refine gRPC's reconnection logic and increase the KV client's throughput [#1586](https://github.com/pingcap/ticdc/issues/1586) [#1501](https://github.com/pingcap/ticdc/issues/1501#issuecomment-820027078) [#1682](https://github.com/pingcap/ticdc/pull/1682) [#1393](https://github.com/pingcap/ticdc/issues/1393) [#1847](https://github.com/pingcap/ticdc/pull/1847) [#1905](https://github.com/pingcap/ticdc/issues/1905) [#1904](https://github.com/pingcap/ticdc/issues/1904)
        - Make the sorter I/O errors more user-friendly

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

    - Fix the data race issue that occurs when loading TTL configurations after the scheduler is started [#3771](https://github.com/tikv/pd/issues/3771)
    - Fix a bug that the `is_learner` field of the `TIKV_REGION_PEERS` table in TiDB is incorrect [#3372](https://github.com/tikv/pd/issues/3372) [#24293](https://github.com/pingcap/tidb/issues/24293)
    - Fix the issue that when all TiKV nodes in a zone are offline or down, PD does not schedule replicas to other zones [#3705](https://github.com/tikv/pd/issues/3705)
    - Fix the issue that PD might get panic after the scatter Region scheduler is added [#3762](https://github.com/tikv/pd/pull/3762)

+ TiFlash

    - Fix the issue that TiFlash keeps restarting because of the split failure
    - Fix the potential issue that TiFlash cannot delete the delta data
    - Fix a bug that TiFlash adds wrong padding for non-binary characters in the `CAST` function
    - Fix the issue of incorrect results when handling aggregation queries with complex `GROUP BY` columns
    - Fix the TiFlash panic issue that occurs under heavy write pressure
    - Fix the panic that occurs when the right jon key is not nullalbe and the left join key is nullable
    - Fix the potential issue that the `read-index` requests take a long time
    - Fix the panic issue that occurs when the read load is heavy
    - Fix the panic issue that might occur when the `Date_Format` function is called with the `STRING` type argument and `NULL` values

+ Tools

    + TiCDC

        - Fix the issue that TiCDC owner exits when refreshing the checkpoint [#1902](https://github.com/pingcap/ticdc/issues/1902)
        - Fix a bug that some MySQL connection might leak after MySQL sink meets the error and pauses [#1946](https://github.com/pingcap/ticdc/pull/1946)
        - Fix the panic issue that occurs when TiCDC fails to read `/proc/meminfo` [#2024](https://github.com/pingcap/ticdc/pull/2024)
        - Reduce TiCDC's runtime memory consumption [#2012](https://github.com/pingcap/ticdc/pull/2012) [#1958](https://github.com/pingcap/ticdc/pull/1958)
        - Fix a bug that might cause TiCDC server panic due to the late calculation of resolved ts [#1576](https://github.com/pingcap/ticdc/issues/1576)
        - Fix the potential deadlock issue for the processor [#2142](https://github.com/pingcap/ticdc/pull/2142)

    + Backup & Restore (BR)

        - Fix a bug that all system tables are filtered during restore [#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        - Fix the issue that Backup & Restore reports the error of "file already exists" when TDE is enabled during the restore [#1179](https://github.com/pingcap/br/issues/1179)

    + TiDB Lightning

        - Fix the TiDB Lightning panic issue for some special data [#1213](https://github.com/pingcap/br/issues/1213)
        - Fix the EOF error reported when TiDB Lightning splits the imported large CSV files [#1133](https://github.com/pingcap/br/issues/1133)
        - Fix a bug that an excessively large base value is generated when TiDB Lightning imports tables with the `auto_increment` column of the `FLOAT` or `DOUBLE` type [#1186](https://github.com/pingcap/br/pull/1186)
        - Fix the issue that TiDB fails to parse the `DECIMAL` type data in Parquet files [#1277](https://github.com/pingcap/br/pull/1277)
