---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 Release Notes

Release date: February 26, 2021

TiDB version: 4.0.11

## New Features

+ TiDB

    - Support the `utf8_unicode_ci` and `utf8mb4_unicode_ci` collations [#22558](https://github.com/pingcap/tidb/pull/22558)

+ TiKV

    - Support the `utf8mb4_unicode_ci` collation [#9577](https://github.com/tikv/tikv/pull/9577)
    - Support the `cast_year_as_time` collation [#9299](https://github.com/tikv/tikv/pull/9299)

+ TiFlash

    - Add a Coprocessor thread pool to queue Coprocessor requests for execution, which avoids out of memory (OOM) in some cases, and add the `cop_pool_size` and `batch_cop_pool_size` configuration items with the default values of `NumOfPhysicalCores * 2`

## Improvements

+ TiDB

    - Reorder inner joins that are simplified from outer joins [#22402](https://github.com/pingcap/tidb/pull/22402)
    - Support multiple clusters in Grafana dashboards [#22534](https://github.com/pingcap/tidb/pull/22534)
    - Add a workaround for the issue of multiple statements [#22468](https://github.com/pingcap/tidb/pull/22468)
    - Divide the metrics of slow query into `internal` and `general` [#22405](https://github.com/pingcap/tidb/pull/22405)
    - Add interface for `utf8_unicode_ci` and `utf8mb4_unicode_ci` collations [#22099](https://github.com/pingcap/tidb/pull/22099)

+ TiKV

    - Add metrics of server information for DBaaS [#9591](https://github.com/tikv/tikv/pull/9591)
    - Support multiple clusters in Grafana dashboards [#9572](https://github.com/tikv/tikv/pull/9572)
    - Report RocksDB metrics to TiDB [#9316](https://github.com/tikv/tikv/pull/9316)
    - Record the suspension time for Coprocessor tasks [#9277](https://github.com/tikv/tikv/pull/9277)
    - Add thresholds of key counts and key size for Load Base Split [#9354](https://github.com/tikv/tikv/pull/9354)
    - Check whether the file exists before data import [#9544](https://github.com/tikv/tikv/pull/9544)
    - Improve Fast Tune panels [#9180](https://github.com/tikv/tikv/pull/9180)

+ PD

    - Support multiple clusters in Grafana dashboards [#3398](https://github.com/pingcap/pd/pull/3398)

+ TiFlash

    - Optimize the performance of the `date_format` function
    - Optimize the memory consumption of handling ingest SST
    - Optimize the retrying logic in Batch Coprocessor to reduce the probability of Region error

+ Tools

    + TiCDC

        - Add the version information in the `capture` metadata and add the CLI version of a `changefeed` in the `changefeed` metadata [#1342](https://github.com/pingcap/tiflow/pull/1342)

    + TiDB Lightning

        - Create tables in parallel to improve import performance [#502](https://github.com/pingcap/tidb-lightning/pull/502)
        - Skip splitting Regions to improve import performance if the engine's total size is smaller than the Region size [#524](https://github.com/pingcap/tidb-lightning/pull/524)
        - Add a import progress bar and optimize the accuracy of restore progress [#506](https://github.com/pingcap/tidb-lightning/pull/506)

## Bug Fixes

+ TiDB

    - Fix the issue of abnormal `unicode_ci` constant propagation [#22614](https://github.com/pingcap/tidb/pull/22614)
    - Fix the issue that might cause wrong collation and coercibility [#22602](https://github.com/pingcap/tidb/pull/22602)
    - Fix the issue that might cause wrong collation results [#22599](https://github.com/pingcap/tidb/pull/22599)
    - Fix the issue of constant substitution for different collations [#22582](https://github.com/pingcap/tidb/pull/22582)
    - Fix a bug that the `like` function might return wrong result when using collation [#22531](https://github.com/pingcap/tidb/pull/22531)
    - Fix the issue of incorrect `duration` type inference in `least` and `greatest` functions [#22580](https://github.com/pingcap/tidb/pull/22580)
    - Fix a bug that occurs when the `like` function handles a single character wildcard (`_`) followed by a multiple character wildcard (`%`) [#22575](https://github.com/pingcap/tidb/pull/22575)
    - Fix the type inference error of the TiDB's built-in functions (`least` and `greatest`) [#22562](https://github.com/pingcap/tidb/pull/22562)
    - Fix a bug that makes the `like` function get the wrong result if the pattern string is a unicode string [#22529](https://github.com/pingcap/tidb/pull/22529)
    - Fix a bug that the point get query does not get the snapshot data when the `@@tidb_snapshot` variable is set [#22527](https://github.com/pingcap/tidb/pull/22527)
    - Fix the potential panic that occurs when generating hints from joins [#22518](https://github.com/pingcap/tidb/pull/22518)
    - Fix the issue that strings are incorrectly converted to the `BIT` type [#22420](https://github.com/pingcap/tidb/pull/22420)
    - Fix the `index out of range` error that occurs when inserting values to the `tidb_rowid` column [#22359](https://github.com/pingcap/tidb/pull/22359)
    - Fix a bug that the cached plan is incorrectly used [#22353](https://github.com/pingcap/tidb/pull/22353)
    - Fix the runtime panic in the `WEIGHT_STRING` function when the length of the binary/char string is too large [#22332](https://github.com/pingcap/tidb/pull/22332)
    - Forbid using the generated column when the number of function parameters is invalid [#22174](https://github.com/pingcap/tidb/pull/22174)
    - Correctly set the process information before building the execution plan [#22148](https://github.com/pingcap/tidb/pull/22148)
    - Fix the issue of inaccurate runtime statistics of `IndexLookUp` [#22136](https://github.com/pingcap/tidb/pull/22136)
    - Add cache for the memory usage information when the cluster is deployed in a container [#22116](https://github.com/pingcap/tidb/pull/22116)
    - Fix the issue of the decoding plan errors [#22022](https://github.com/pingcap/tidb/pull/22022)
    - Report errors for using invalid window specifications [#21976](https://github.com/pingcap/tidb/pull/21976)
    - Report errors when the `PREPARE` statement is nested with `EXECUTE`, `DEALLOCATE` or `PREPARE` [#21972](https://github.com/pingcap/tidb/pull/21972)
    - Fix the issue that no error is reported when the `INSERT IGNORE` statement is used on a non-existing partition [#21971](https://github.com/pingcap/tidb/pull/21971)
    - Unify the encoding of `EXPLAIN` results and slow log [#21964](https://github.com/pingcap/tidb/pull/21964)
    - Fix the issue of unknown columns in join when using the aggregate operator [#21957](https://github.com/pingcap/tidb/pull/21957)
    - Fix the wrong type inference in the `ceiling` function [#21936](https://github.com/pingcap/tidb/pull/21936)
    - Fix the issue that the `Double` type column ignores its decimal [#21916](https://github.com/pingcap/tidb/pull/21916)
    - Fix the issue that the correlated aggregation is calculated in subqueries [#21877](https://github.com/pingcap/tidb/pull/21877)
    - Report errors for the JSON object with key length >= 65536 [#21870](https://github.com/pingcap/tidb/pull/21870)
    - Fix the issue that the `dyname` function is incompatible with MySQL [#21850](https://github.com/pingcap/tidb/pull/21850)
    - Fix the issue that the `to_base64` function returns `NULL` when the input data is too long [#21813](https://github.com/pingcap/tidb/pull/21813)
    - Fix the failure of comparing multiple fields in the subquery [#21808](https://github.com/pingcap/tidb/pull/21808)
    - Fix the issue that occurs when comparing the float type in JSON [#21785](https://github.com/pingcap/tidb/pull/21785)
    - Fix the issue that occurs when comparing the types of JSON objects [#21718](https://github.com/pingcap/tidb/pull/21718)
    - Fix the issue that the coercibility value of the `cast` function is incorrectly set [#21714](https://github.com/pingcap/tidb/pull/21714)
    - Fix an unexpected panic when using the `IF` function [#21711](https://github.com/pingcap/tidb/pull/21711)
    - Fix the issue that the `NULL` result returned from JSON search is incompatible with MySQL [#21700](https://github.com/pingcap/tidb/pull/21700)
    - Fix the issue that occurs when checking the `only_full_group_by` mode using `ORDER BY` and `HAVING` [#21697](https://github.com/pingcap/tidb/pull/21697)
    - Fix the issue that the units of `Day` and `Time` are incompatible with MySQL [#21676](https://github.com/pingcap/tidb/pull/21676)
    - Fix the issue that the default values of `LEAD` and `LAG` cannot adapt to the field type [#21665](https://github.com/pingcap/tidb/pull/21665)
    - Perform a check to ensure that the `LOAD DATA` statement can only load data into base tables [#21638](https://github.com/pingcap/tidb/pull/21638)
    - Fix the issue that occurs when `addtime` and `subtime` functions handle invalid arguments [#21635](https://github.com/pingcap/tidb/pull/21635)
    - Change the round rule for approximate values to "round to the nearest even number" [#21628](https://github.com/pingcap/tidb/pull/21628)
    - Fix the issue that `WEEK()` does not recognize `@@GLOBAL.default_week_format` until it has been explicitly read [#21623](https://github.com/pingcap/tidb/pull/21623)

+ TiKV

    - Fix the issue that TiKV is failed to build with `PROST=1` [#9604](https://github.com/tikv/tikv/pull/9604)
    - Fix the unmatched memory diagnostics [#9589](https://github.com/tikv/tikv/pull/9589)
    - Fix the issue that the end key of a partial RawKV-restore range is inclusive [#9583](https://github.com/tikv/tikv/pull/9583)
    - Fix the issue of TiKV panic that occurs when loading the old value of a key of a rolled-back transaction during TiCDC's incremental scan [#9569](https://github.com/tikv/tikv/pull/9569)
    - Fix the configuration glitch of old values when changefeeds with different settings connect to one Region [#9565](https://github.com/tikv/tikv/pull/9565)
    - Fix a crash issue that occurs when running a TiKV cluster on a machine with a network interface that lacks the MAC address (introduced in v4.0.9) [#9516](https://github.com/tikv/tikv/pull/9516)
    - Fix the issue of TiKV OOM when backing up a huge Region [#9448](https://github.com/tikv/tikv/pull/9448)
    - Fix the issue that `region-split-check-diff` cannot be customized [#9530](https://github.com/tikv/tikv/pull/9530)
    - Fix the issue of TiKV panic when the system time goes back [#9542](https://github.com/tikv/tikv/pull/9542)

+ PD

    - Fix the issue that member health metrics are incorrectly displayed [#3368](https://github.com/pingcap/pd/pull/3368)
    - Forbid removing the tombstone store that still has peers [#3352](https://github.com/pingcap/pd/pull/3352)
    - Fix the issue that the store limit cannot be persisted [#3403](https://github.com/pingcap/pd/pull/3403)
    - Fix the limit constriction of the scatter range scheduler [#3401](https://github.com/pingcap/pd/pull/3401)

+ TiFlash

    - Fix a bug that the `min`/`max` result is wrong for the decimal type
    - Fix a bug that TiFlash might crash when reading data
    - Fix the issue that some data written after DDL operations might be lost after data compaction
    - Fix the issue that TiFlash incorrectly handles decimal constants in Coprocessor
    - Fix the potential crash during the learner read process
    - Fix the inconsistent behaviors of division by `0` or `NULL` between TiDB and TiFlash

+ Tools

    + TiCDC

        - Fix a bug that the TiCDC service might unexpectedly exit when `ErrTaskStatusNotExists` and the closing of `capture` session occur at the same time [#1240](https://github.com/pingcap/tiflow/pull/1240)
        - Fix the old value switch issue that a `changefeed` might be affected by another `changefeed` [#1347](https://github.com/pingcap/tiflow/pull/1347)
        - Fix a bug that the TiCDC service might hang when processing a new `changefeed` with the invalid `sort-engine` parameter [#1309](https://github.com/pingcap/tiflow/pull/1309)
        - Fix the issue of panic that occurs when getting the debugging information on non-owner nodes [#1349](https://github.com/pingcap/tiflow/pull/1349)
        - Fix the issue that the `ticdc_processor_num_of_tables` and `ticdc_processor_table_resolved_ts` metrics are not properly updated when adding or removing tables [#1351](https://github.com/pingcap/tiflow/pull/1351)
        - Fix the issue of potential data loss if a processor crashes when adding a table [#1363](https://github.com/pingcap/tiflow/pull/1363)
        - Fix a bug that the owner might lead to abnormal TiCDC server exits during table migrations [#1352](https://github.com/pingcap/tiflow/pull/1352)
        - Fix a bug that TiCDC does not exit in time after the service GC safepoint is lost [#1367](https://github.com/pingcap/tiflow/pull/1367)
        - Fix a bug that the KV client might skip creating the event feed [#1336](https://github.com/pingcap/tiflow/pull/1336)
        - Fix a bug that the atomicity of transactions is broken when the transactions are replicated to the downstream [#1375](https://github.com/pingcap/tiflow/pull/1375)

    + Backup & Restore (BR)

        - Fix the issue that TiKV might be caused to generate a big Region after BR restores the backup [#702](https://github.com/pingcap/br/pull/702)
        - Fix the issue that BR restores a table's Auto ID even if the table does not have Auto ID [#720](https://github.com/pingcap/br/pull/720)

    + TiDB Lightning

        - Fix a bug that `column count mismatch` might be triggered when using the TiDB-backend [#535](https://github.com/pingcap/tidb-lightning/pull/535)
        - Fix a bug that TiDB-backend panics if the column count of the source file and the column count of the target table mismatch [#528](https://github.com/pingcap/tidb-lightning/pull/528)
        - Fix a bug that TiKV might unexpectedly panic during TiDB Lightning's data import [#554](https://github.com/pingcap/tidb-lightning/pull/554)
