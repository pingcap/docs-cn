---
title: TiDB 6.5.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.2.
---

# TiDB 6.5.2 Release Notes

Release date: April 21, 2023

TiDB version: 6.5.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.2#version-list)

## Compatibility changes

- TiCDC fixes the issue of incorrect encoding of `FLOAT` data in Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    When upgrading the TiCDC cluster to v6.5.2 or a later v6.5.x version, if a table replicated using Avro contains the `FLOAT` data type, you need to manually adjust the compatibility policy of Confluent Schema Registry to `None` before upgrading so that the changefeed can successfully update the schema. Otherwise, after upgrading, the changefeed will be unable to update the schema and enter an error state.

- To fix the potential issue of data loss during replication of partitioned tables to storage services, the default value of the TiCDC [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) configuration item is changed from `false` to `true`. This means that partitions in a table are stored in separate directories by default. It is recommended that you keep the value as `true` to avoid the data loss issue. [#8724](https://github.com/pingcap/tiflow/issues/8724) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Improvements

+ TiDB

    - Support caching the execution plan for `BatchPointGet` in Prepared Plan Cache [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
    - Support more SQL formats for Index Join [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)
    - Change the log level of some Index Merge readers from `"info"` to `"debug"` [#41949](https://github.com/pingcap/tidb/issues/41949) @[yibin87](https://github.com/yibin87)
    - Optimize the `distsql_concurrency` setting for Range partitioned tables with Limit to reduce query latency [#41480](https://github.com/pingcap/tidb/issues/41480) @[you06](https://github.com/you06)

+ TiFlash

    - Reduce CPU consumption of task scheduling during TiFlash reads [#6495](https://github.com/pingcap/tiflash/issues/6495) @[JinheLin](https://github.com/JinheLin)
    - Improve performance of data import from BR and TiDB Lightning to TiFlash with default configurations [#7272](https://github.com/pingcap/tiflash/issues/7272) @[breezewish](https://github.com/breezewish)

+ Tools

    + TiCDC

        - Release TiCDC Open API v2.0 [#8743](https://github.com/pingcap/tiflow/issues/8743) @[sdojjy](https://github.com/sdojjy)
        - Introduce `gomemlimit` to prevent TiCDC from OOM issues [#8675](https://github.com/pingcap/tiflow/issues/8675) @[amyangfei](https://github.com/amyangfei)
        - Use the multi-statement approach to optimize the replication performance in scenarios involving batch execution of `UPDATE` statements [#8057](https://github.com/pingcap/tiflow/issues/8057) @[amyangfei](https://github.com/amyangfei)
        - Support splitting transactions in the redo applier to improve its throughput and reduce RTO in disaster recovery scenarios [#8318](https://github.com/pingcap/tiflow/issues/8318) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support applying DDL events in redo logs [#8361](https://github.com/pingcap/tiflow/issues/8361) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - Support importing CSV data files with BOM headers [#40744](https://github.com/pingcap/tidb/issues/40744) @[dsdashun](https://github.com/dsdashun)

## Bug fixes

+ TiDB
    - Fix the issue that after a new column is added in the cache table, the value is `NULL` instead of the default value of the column [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - Fix the issue of DDL retry caused by write conflict when executing `TRUNCATE TABLE` for partitioned tables with many partitions and TiFlash replicas [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - Fix the issue of missing table names in the `ADMIN SHOW DDL JOBS` result when a `DROP TABLE` operation is being executed [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB server cannot start due to an error in reading the cgroup information with the error message "can't read file memory.stat from cgroup v1: open /sys/memory.stat no such file or directory" [#42659](https://github.com/pingcap/tidb/issues/42659) @[hawkingrei](https://github.com/hawkingrei)
    - Fix frequent write conflicts in transactions when performing DDL data backfill [#24427](https://github.com/pingcap/tidb/issues/24427) @[mjonss](https://github.com/mjonss)
    - Fix the issue that TiDB panic occurs due to inconsistent InfoSchema being obtained when generating the execution plan [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that when modifying the floating-point type using DDL to keep the length unchanged and reduce the decimal places, the old data still remains the same [#41281](https://github.com/pingcap/tidb/issues/41281) @[zimulala](https://github.com/zimulala)
    - Fix the issue that after executing `PointUpdate` within a transaction, TiDB returns incorrect results for the `SELECT` statement [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - Fix the issue that, when using Cursor Fetch and running other statements among Execute, Fetch, and Close, the Fetch and Close commands might return incorrect results or cause TiDB to panic [#40094](https://github.com/pingcap/tidb/issues/40094) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that `INSERT IGNORE` and `REPLACE` statements do not lock keys that do not modify values [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)
    - Fix the issue that TiFlash reports an error for generated columns during execution [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB might produce incorrect results when different partitioned tables appear in a single SQL statement [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - Fix the issue that full index scans might cause errors when prepared plan cache is enabled [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that IndexMerge might produce incorrect results when prepare plan cache is enabled [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the configuration of `max_prepared_stmt_count` does not take effect [#39735](https://github.com/pingcap/tidb/issues/39735) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that IndexMerge might produce incorrect results when prepare plan cache is enabled [#41828](https://github.com/pingcap/tidb/issues/41828) @[qw4990](https://github.com/qw4990) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that Index Join might cause panic in dynamic trimming mode of partition tables [#40596](https://github.com/pingcap/tidb/issues/40596) @[tiancaiamao](https://github.com/tiancaiamao)

+ TiKV

    - Fix the issue that TiKV does not correctly parse the `:` character when processing the cgroup path [#14538](https://github.com/tikv/tikv/issues/14538) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ PD

    - Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that switching placement rule might cause uneven distribution of leaders [#6195](https://github.com/tikv/pd/issues/6195) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - Fix the issue that TiFlash cannot recognize generated columns [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that Decimal division does not round up the last digit in certain cases [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that Decimal cast rounds up incorrectly in certain cases [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - Fix the issue that TopN/Sort operators produce incorrect results after enabling the new collation [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue of TiFlash process failures due to TiCDC incompatibility [#7212](https://github.com/pingcap/tiflash/issues/7212) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - Fix the issue of insufficient wait time for splitting Region retry during the PITR recovery process [#42001](https://github.com/pingcap/tidb/issues/42001) @[joccau](https://github.com/joccau)

    + TiCDC

        - Fix the issue that the partition separator does not work when TiCDC replicates data to object storage [#8581](https://github.com/pingcap/tiflow/issues/8581) @[CharlesCheung96](https://github.com/CharlesCheung96) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that table scheduling might cause data loss when TiCDC replicates data to object storage [#8256](https://github.com/pingcap/tiflow/issues/8256) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - Fix the issue that the replication gets stuck due to non-reentrant DDL statements [#8662](https://github.com/pingcap/tiflow/issues/8662) @[hicqu](https://github.com/hicqu)
        - Fix the issue that TiCDC scaling might cause data loss when TiCDC replicates data to object storage [#8666](https://github.com/pingcap/tiflow/issues/8666) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the memory usage of `db sorter` is not controlled by `cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - Fix the issue that data loss might occur in special cases during the apply of Redo log [#8591](https://github.com/pingcap/tiflow/issues/8591) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the memory usage of `db sorter` is not controlled by `cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - Fix the issue that the disorder of `UPDATE` and `INSERT` statements during data replication might cause the `Duplicate entry` error [#8597](https://github.com/pingcap/tiflow/issues/8597) @[sdojjy](https://github.com/sdojjy)
        - Fix the abnormal exit issue of the TiCDC service caused by network isolation between PD and TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @[overvenus](https://github.com/overvenus)
        - Fix the issue that graceful upgrade for TiCDC clusters fails on Kubernetes [#8484](https://github.com/pingcap/tiflow/issues/8484) @[overvenus](https://github.com/overvenus)
        - Fix the issue that the TiCDC server panics when all downstream Kafka servers are unavailable [#8523](https://github.com/pingcap/tiflow/issues/8523) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that restarting the changefeed might cause data loss or that the checkpoint cannot advance [#8242](https://github.com/pingcap/tiflow/issues/8242) @[overvenus](https://github.com/overvenus)
