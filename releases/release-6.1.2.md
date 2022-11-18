---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 Release Notes

Release date: October 24, 2022

TiDB version: 6.1.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.2#version-list)

## Improvements

+ TiDB

    - Allow setting placement rules and TiFlash replicas at the same time in one table [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    - Support configuring the RocksDB write stall settings to a value smaller than the flow control threshold [#13467](https://github.com/tikv/tikv/issues/13467) @[tabokie](https://github.com/tabokie)

+ Tools

    + TiDB Lightning

        - Add retryable errors during checksum to improve robustness [#37690](https://github.com/pingcap/tidb/issues/37690) @[D3Hunter](https://github.com/D3Hunter)

    + TiCDC

        - Enhance the performance of the region worker by handling resolved TS in a batch [#7078](https://github.com/pingcap/tiflow/issues/7078) @[sdojjy](https://github.com/sdojjy)

## Bug fixes

+ TiDB

    - Fix the issue that database-level privileges are incorrectly cleaned up [#38363](https://github.com/pingcap/tidb/issues/38363) @[dveeden](https://github.com/dveeden)
    - Fix the incorrect output of `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
    - Fix the issue that when one PD node goes down, the query of `information_schema.TIKV_REGION_STATUS` fails due to not retrying other PD nodes [#35708](https://github.com/pingcap/tidb/issues/35708) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `UNION` operator might return unexpected empty result [#36903](https://github.com/pingcap/tidb/issues/36903) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the Region cache is not cleaned up in time when the Region is merged [#37141](https://github.com/pingcap/tidb/issues/37141) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that the KV client sends unnecessary ping messages [#36861](https://github.com/pingcap/tidb/issues/36861) @[jackysp](https://github.com/jackysp)
    - Fix the issue that the `EXPLAIN ANALYZE` statement with DML executors might return result before the transaction commit finishes [#37373](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that `GROUP CONCAT` with `ORDER BY` might fail when the `ORDER BY` clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    - Fix the issue that `Can't find column` is reported if an `UPDATE` statement contains common table expressions (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `EXECUTE` might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187) @[Reminiscent](https://github.com/Reminiscent)

+ TiKV

    - Fix the issue that the snapshot data might be incomplete caused by batch snapshot across Regions [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that causes permission denied error when TiKV gets an error from the web identity provider and fails back to the default provider [#13122](https://github.com/tikv/tikv/issues/13122) @[3pointer](https://github.com/3pointer)
    - Fix the issue that the TiKV service is unavailable for several minutes when a TiKV instance is in an isolated network environment [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)

+ PD

    - Fix the issue that the statistics of the Region tree might be inaccurate [#5318](https://github.com/tikv/pd/issues/5318) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the TiFlash learner replica might not be created [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that unhealthy Region might cause PD panic [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Fix the issue that I/O Limiter might incorrectly throttle the I/O throughput of query requests after bulk writes, which reduces the query performance [#5801](https://github.com/pingcap/tiflash/issues/5801) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that a window function might cause TiFlash to crash when the query is canceled [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
    - Fix the panic that occurs after creating the primary index with a column containing the `NULL` value [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Lightning

        - Fix panic of TiDB Lightning caused by invalid metric counters [#37338](https://github.com/pingcap/tidb/issues/37338) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Data Migration (DM)

        - Fix the issue that upstream table structure information is lost when DM tasks enter the sync unit and are interrupted [#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        - Fix large transaction errors by splitting SQL statements when saving checkpoints [#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM precheck requires the `SELECT` privilege on `INFORMATION_SCHEMA` [#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM-worker triggers a deadlock error after running DM tasks with fast/full validators [#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Fix the issue that DM reports the `Specified key was too long` error [#5315](https://github.com/pingcap/tiflow/issues/5315) @[lance6716](https://github.com/lance6716)
        - Fix the issue that latin1 data might be corrupted during replication [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiCDC

        - Fix the issue that the cdc server might panic if it receives an HTTP request before the cdc server fully starts [#6838](https://github.com/pingcap/tiflow/issues/6838) @[asddongmen](https://github.com/asddongmen)
        - Fix the log flooding issue during upgrade [#7235](https://github.com/pingcap/tiflow/issues/7235) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that changefeed's redo log files might be deleted by mistake [#6413](https://github.com/pingcap/tiflow/issues/6413) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that TiCDC might become unavailable when too many operations in an etcd transaction are committed [#7131](https://github.com/pingcap/tiflow/issues/7131) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that data inconsistency might occur when non-reentrant DDL statements in redo logs are executed twice [#6927](https://github.com/pingcap/tiflow/issues/6927) @[hicqu](https://github.com/hicqu)

    + Backup & Restore (BR)

        - Fix the issue that the regions are not balanced because the concurrency is set too large during the restoration [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - Fix the issue that might lead to backup and restoration failure if special characters exist in the authorization key of external storage [#37469](https://github.com/pingcap/tidb/issues/37469) @[MoCuishle28](https://github.com/MoCuishle28)
