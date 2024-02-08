---
title: TiDB 6.5.7 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.7.
---

# TiDB 6.5.7 Release Notes

Release date: January 8, 2024

TiDB version: 6.5.7

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.7#version-list)

## Compatibility changes

+ Introduce the TiDB configuration item [`performance.force-init-stats`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#force-init-stats-new-in-v657) to control whether TiDB needs to wait for statistics initialization to finish before providing services during TiDB startup [#43385](https://github.com/pingcap/tidb/issues/43385) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
+ To reduce the overhead of log printing, TiFlash changes the default value of `logger.level` from `"debug"` to `"info"` [#8568](https://github.com/pingcap/tiflash/issues/8568) @[xzhangxian1008](https://github.com/xzhangxian1008)

## Improvements

+ TiDB

    - Optimize memory usage and performance for `ANALYZE` operations on partitioned tables [#47071](https://github.com/pingcap/tidb/issues/47071) [#47104](https://github.com/pingcap/tidb/issues/47104) [#46804](https://github.com/pingcap/tidb/issues/46804) @[hawkingrei](https://github.com/hawkingrei)
    - Support Plan Cache to cache execution plans with the `PointGet` operator generated during physical optimization using Optimizer Fix Controls [#44830](https://github.com/pingcap/tidb/issues/44830) @[qw4990](https://github.com/qw4990)
    - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)

+ TiFlash

    - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - Resolve compatibility issues between EBS-based snapshot backups and TiDB Lightning imports [#46850](https://github.com/pingcap/tidb/issues/46850) @[YuJuncen](https://github.com/YuJuncen)
        - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - When the downstream is Kafka, the topic expression allows `schema` to be optional and supports specifying a topic name directly [#9763](https://github.com/pingcap/tiflow/issues/9763) @[3AceShowHand](https://github.com/3AceShowHand)

## Bug fixes

+ TiDB

    - Fix the issue that `stats_meta` is not created following table creation [#38189](https://github.com/pingcap/tidb/issues/38189) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the incorrect error message for `ErrLoadDataInvalidURI` (invalid S3 URI error) [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that queries containing common table expressions (CTEs) unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that queries containing CTEs report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - Fix the issue of possible statistics data errors when importing statistics exported from early versions of TiDB [#42931](https://github.com/pingcap/tidb/issues/42931) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the optimizer incorrectly converts TiFlash selection path to the DUAL table in specific scenarios [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that parsing invalid values of `ENUM` or `SET` types would directly cause SQL statement errors [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - Fix the issue that using the `_` wildcard in `LIKE` when the data contains trailing spaces can result in incorrect query results [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that in non-strict mode (`sql_mode = ''`), truncation during executing `INSERT` still reports an error [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB panics and reports an error `invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the completion times of two DDL tasks with dependencies are incorrectly sequenced [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)

+ TiKV

    - Fix the issue that damaged SST files might be spread to other TiKV nodes [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Resolved TS in stale read might cause TiKV OOM issues when tracking large transactions [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV reports the `ServerIsBusy` error because it cannot append the raft log [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - Fix the issue that the `location-labels` set by Placement Rules in SQL are not scheduled as expected under specific conditions [#6637](https://github.com/tikv/pd/issues/6637) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - Fix incorrect display of maximum percentile time for some panels in Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that `checkpoint-ts` might get stuck when TiCDC replicates data to downstream MySQL [#10334](https://github.com/pingcap/tiflow/issues/10334) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987)
        - Fix the potential data race issue during `kv-client` initialization [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)
