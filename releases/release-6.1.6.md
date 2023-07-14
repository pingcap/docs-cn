---
title: TiDB 6.1.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.6.
---

# TiDB 6.1.6 Release Notes

Release date: April 12, 2023

TiDB version: 6.1.6

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.6#version-list)

## Compatibility changes

- TiCDC fixes the issue of incorrect encoding of FLOAT data in Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    When upgrading the TiCDC cluster to v6.1.6 or a later v6.1.x version, if a table replicated using Avro contains the `FLOAT` data type, you need to manually adjust the compatibility policy of Confluent Schema Registry to `None` before upgrading so that the changefeed can successfully update the schema. Otherwise, after upgrading, the changefeed will be unable to update the schema and enter an error state.

## Improvements

+ TiDB

    - Supports caching the execution plan for `BatchPointGet` in Prepared Plan Cache [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
    - Support more SQL formats for Index Join [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)

+ TiKV

    - Support starting TiKV on a CPU with less than 1 core [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db) @[andreid-db](https://github.com/andreid-db)

## Bug fixes

+ TiDB

    - Fix the issue that the `ignore_plan_cache` hint might not work for `INSERT` statements [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB might panic after `indexMerge` encounters an error [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - Fix the issue that incorrect results might be returned when TopN operators with virtual columns are mistakenly pushing down to TiKV or TiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - Fix the PD OOM issue when there is a large number of Regions but the table ID cannot be pushed down when querying some virtual tables using `Prepare` or `Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - Fix the issue that Plan Cache might cache FullScan plans when processing `int_col in (decimal...)` conditions [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - Fix the issue that IndexMerge plans might generate incorrect ranges on the SET type columns [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue of potential wrong results when comparing unsigned `TINYINT`/`SMALLINT`/`INT` values with `DECIMAL`/`FLOAT`/`DOUBLE` values smaller than `0` [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that the TiDB server might run out of memory when the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table is queried. This issue can be triggered when you check slow queries on the Grafana dashboard [#33893](https://github.com/pingcap/tidb/issues/33893) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that range partitions allow multiple `MAXVALUE` partitions [#36329](https://github.com/pingcap/tidb/issues/36329) @[u5surf](https://github.com/u5surf)
    - Fix the issue that Plan Cache might cache Shuffle operators and return incorrect results [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - Fix the issue that data race in time zone might cause data-index inconsistency [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that goroutine leak might occur in `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that, when using Cursor Fetch and running other statements among Execute, Fetch, and Close, the Fetch and Close commands might return incorrect results or cause TiDB to panic [#40094](https://github.com/pingcap/tidb/issues/40094) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when modifying the floating-point type using DDL to keep the length unchanged and reduce the decimal places, the old data still remains the same [#41281](https://github.com/pingcap/tidb/issues/41281) @[zimulala](https://github.com/zimulala)
    - Fix the issue that joining the `information_schema.columns` table causes TiDB to panic [#32459](https://github.com/pingcap/tidb/issues/32459) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB panic occurs due to inconsistent InfoSchema being obtained when generating the execution plan [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiFlash reports an error for generated columns during execution [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB might produce incorrect results when different partitioned tables appear in a single SQL statement [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - Fix the issue that Plan Cache might cache Shuffle operators and return incorrect results [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that using Index Merge to read a table containing the `SET` type column might lead to incorrect results [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that full index scans might cause errors when prepared plan cache is enabled [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that SQL statements using `PointGet` to read a table during the execution of a DDL statement might throw a panic [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that after executing `PointUpdate` within a transaction, TiDB returns incorrect results for the `SELECT` statement [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - Clear expired region cache regularly to avoid memory leak and performance degradation [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf) @[zyguan](https://github.com/zyguan)
    - Fix the issue that `INSERT IGNORE` and `REPLACE` statements do not lock keys that do not modify values [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)

+ TiKV

    - Fix an error that occurs when casting the `const Enum` type to other types [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue of CPU quota limitation [#13084](https://github.com/tikv/tikv/issues/13084) @[BornChanger](https://github.com/BornChanger)
    - Fix the issue of incorrect snapshot last index [#12618](https://github.com/tikv/tikv/issues/12618) @[LintianShi](https://github.com/LintianShi)

+ PD

    - Fix the issue that the Region Scatter might cause uneven distribution of leader [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that the timeout mechanism of Online Unsafe Recovery does not work [#6107](https://github.com/tikv/pd/issues/6107) @[v01dstar](https://github.com/v01dstar)

+ TiFlash

    - Fix the issue that semi-joins use excessive memory when calculating Cartesian products [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiFlash log search is too slow [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - Fix the issue that TopN/Sort operators produce incorrect results after enabling the new collation [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that Decimal cast rounds up incorrectly in certain cases [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TiFlash cannot recognize generated columns [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that Decimal division does not round up the last digit in certain cases [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + TiCDC

        - Fix the issue that the disorder of `UPDATE` and `INSERT` statements during data replication might cause the `Duplicate entry` error [#8597](https://github.com/pingcap/tiflow/issues/8597) @[sdojjy](https://github.com/sdojjy)
        - Fix the abnormal exit issue of the TiCDC service caused by network isolation between PD and TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @[overvenus](https://github.com/overvenus)
        - Fix the data inconsistency that occurs when replicating data to a TiDB or MySQL sink and when `CHARACTER SET` is specified on the column that has the non-null unique index without a primary key [#8420](https://github.com/pingcap/tiflow/issues/8420) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - Fix the issue that the memory usage of `db sorter` is not controlled by `cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - Optimize the error message of `cdc cli` for invalid input [#7903](https://github.com/pingcap/tiflow/issues/7903) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue of insufficient duration that redo log can tolerate for S3 storage failure [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that pausing a changefeed when PD is abnormal results in incorrect status [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)

    + TiDB Lightning

        - Fix the issue that the conflict resolution logic (`duplicate-resolution`) might lead to inconsistent checksums [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - Fix the issue that TiDB Lightning panics in the split-region phase [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - Fix the issue that when importing data in Local Backend mode, the target columns do not automatically generate data if the compound primary key of the imported target table has an `auto_random` column and no value for the column is specified in the source data [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that TiDB Lightning might incorrectly skip conflict resolution when all but the last TiDB Lightning instance encounters a local duplicate record during a parallel import [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
