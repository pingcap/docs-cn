---
title: TiDB 6.1.6 Release Notes
summary: 了解 TiDB 6.1.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.1.6 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.1.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.6#version-list)

## 兼容性变更

- 兼容性变更 1

## 提升改进

+ TiDB

+ TiKV

    - (dup): release-6.6.0.md > Improvements> TiKV - Support starting TiKV on a CPU with less than 1 core [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Binlog

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

## Bug 修复

+ TiDB

    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that the `ignore_plan_cache` hint might not work for `INSERT` statements [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717)  @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that TiDB might panic after `indexMerge` encounters an error [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that incorrect results might be returned when TopN operators with virtual columns are mistakenly pushing down to TiKV or TiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - (dup): release-6.6.0.md > Bug fixes> TiDB - Fix the PD OOM issue when there is a large number of Regions but the table ID cannot be pushed down when querying some virtual tables using `Prepare` or `Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that Plan Cache might cache FullScan plans when processing `int_col in (decimal...)` conditions [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that IndexMerge plans might generate incorrect ranges on the SET type columns [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue of potential wrong results when comparing unsigned `TINYINT`/`SMALLINT`/`INT` values with `DECIMAL`/`FLOAT`/`DOUBLE` values smaller than `0` [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - (dup): release-5.4.1.md > Bug Fixes> TiDB - Fix the issue that the TiDB server might run out of memory when the `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` table is queried. This issue can be triggered when you check slow queries on the Grafana dashboard [#33893](https://github.com/pingcap/tidb/issues/33893)
    - (dup): release-6.1.5.md > Bug fixes> TiDB - Fix the issue that data race might cause TiDB to restart [#27725](https://github.com/pingcap/tidb/issues/27725) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-5.1.5.md > Bug fixes> TiDB - Fix the issue that range partitions allow multiple `MAXVALUE` partitions [#36329](https://github.com/pingcap/tidb/issues/36329)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that Plan Cache might cache Shuffle operators and return incorrect results [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that data race in time zone might cause data-index inconsistency [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-6.5.1.md > Bug fixes> TiDB - Fix the issue that goroutine leak might occur in `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)

+ TiKV

    - (dup): release-6.6.0.md > Bug fixes> TiKV - Fix an error that occurs when casting the `const Enum` type to other types [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)

+ PD

    - (dup): release-6.5.1.md > Bug fixes> PD - Fix the issue that the Region Scatter might cause uneven distribution of leader [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - (dup): release-6.6.0.md > Bug fixes> TiFlash - Fix the issue that semi-joins use excessive memory when calculating Cartesian products [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-6.5.1.md > Bug fixes> TiFlash - Fix the issue that TiFlash log search is too slow [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)

+ Tools

    + Backup & Restore (BR)

    + TiCDC

        - (dup): release-6.6.0.md > Bug fixes> Tools> TiCDC - Fix the issue of insufficient duration that redo log can tolerate for S3 storage failure [#8089](https://github.com/pingcap/tiflow/issues/8089)  @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.1.md > Bug fixes> Tools> TiCDC - Fix the issue that pausing a changefeed when PD is abnormal results in incorrect status [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)

    + TiDB Binlog

    + TiDB Data Migration (DM)

    + TiDB Lightning

        - (dup): release-6.6.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that the conflict resolution logic (`duplicate-resolution`) might lead to inconsistent checksums [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - (dup): release-6.6.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning panics in the split-region phase [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.1.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that when importing data in Local Backend mode, the target columns do not automatically generate data if the compound primary key of the imported target table has an `auto_random` column and no value for the column is specified in the source data [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-6.6.0.md > Bug fixes> Tools> TiDB Lightning - Fix the issue that TiDB Lightning might incorrectly skip conflict resolution when all but the last TiDB Lightning instance encounters a local duplicate record during a parallel import [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)

    + Dumpling
