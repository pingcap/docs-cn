---
title: TiDB 6.5.6 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.6.
---

# TiDB 6.5.6 Release Notes

Release date: December 7, 2023

TiDB version: 6.5.6

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.6#version-list)

## Compatibility changes

- Prohibit setting [`require_secure_transport`](https://docs.pingcap.com/tidb/v6.5/system-variables#require_secure_transport-new-in-v610) to `ON` in Security Enhanced Mode (SEM) to prevent potential connectivity issues for users [#47665](https://github.com/pingcap/tidb/issues/47665) @[tiancaiamao](https://github.com/tiancaiamao)
- Introduce the [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v6.5/system-variables#tidb_opt_enable_hash_join-new-in-v656) system variable to control whether the optimizer selects hash joins for tables [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)
- After further testing, the default value of the TiCDC Changefeed configuration item [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) is changed from `true` to `false`. This means that by default, table and database names in the TiCDC configuration file are case-insensitive [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- TiCDC Changefeed introduces the following new configuration items:
    - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) and [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md): enable you to set different concurrency parameters for the redo module based on specifications of different machines [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`compression`](/ticdc/ticdc-changefeed-config.md): enables you to configure the compression behavior of redo log files [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md): enables you to set the automatic cleanup of historical data when replicating data to object storage [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Improvements

+ TiKV

    - Optimize memory usage of Resolver to prevent OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)
    - Optimize the compaction mechanism: when a Region is split, if there is no key to split, a compaction is triggered to eliminate excessive MVCC versions [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Eliminate LRUCache in Router objects to reduce memory usage and prevent OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - Add the `alive` and `leak` monitoring dimensions for the `apply_router` and `raft_router` metrics [#15357](https://github.com/tikv/tikv/issues/15357) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - Add monitoring metrics such as `Status` and `Sync Progress` for `DR Auto-Sync` on the Grafana dashboard [#6975](https://github.com/tikv/pd/issues/6975) @[disksing](https://github.com/disksing)

+ Tools

    + Backup & Restore (BR)

        - During restoring a snapshot backup, BR retries when it encounters certain network errors [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - Introduce a new integration test for Point-In-Time Recovery (PITR) in the `delete range` scenario, enhancing PITR stability  [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)
        - Support the [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v6.5/sql-statement-flashback-cluster) syntax [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
        - Enable automatic retry of Region scatter during snapshot recovery when encountering timeout failures or cancellations of Region scatter [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - BR can pause Region merging by setting the `merge-schedule-limit` configuration to `0` [#7148](https://github.com/tikv/pd/issues/7148) @[BornChanger](https://github.com/3pointer)

    + TiCDC

        - Support making TiCDC Canal-JSON content format [compatible with the content format of the official Canal output](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal) by setting `content-compatible=true` in the `sink-uri` configuration [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)
        - Optimize the execution logic of replicating the `ADD INDEX` DDL operations to avoid blocking subsequent DML statements [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)
        - Reduce the impact of TiCDC incremental scanning on upstream TiKV [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)

## Bug fixes

+ TiDB

    - Fix the issue that the chunk cannot be reused when the HashJoin operator performs probe [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that `Duplicate entry` might occur when `AUTO_ID_CACHE=1` is set [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `TIDB_INLJ` hint does not take effect when joining two sub-queries [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - Fix the issue that DDL operations might get stuck after TiDB is restarted [#46751](https://github.com/pingcap/tidb/issues/46751) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that DDL operations might get permanently blocked due to incorrect MDL handling [#46920](https://github.com/pingcap/tidb/issues/46920) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the results of `MERGE_JOIN` are incorrect [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the Sort operator might cause TiDB to crash during the spill process [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `cast(col)=range` condition causes FullScan when CAST has no precision loss [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - Fix the panic issue of `batch-client` in `client-go` [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - Prohibit split table operations on non-integer clustered indexes [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - Fix the incompatibility issue between the behavior of prepared plan cache and non-prepared plan cache during time conversion [#42439](https://github.com/pingcap/tidb/issues/42439) @[qw4990](https://github.com/qw4990)
    - Fix the issue that sometimes an index cannot be created for an empty table using ingest mode [#39641](https://github.com/pingcap/tidb/issues/39641) @[tangenta](https://github.com/tangenta)
    - Fix the issue of not being able to detect data that does not comply with partition definitions during partition exchange [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - Fix the issue that `GROUP_CONCAT` cannot parse the `ORDER BY` column [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that HashCode is repeatedly calculated for deeply nested expressions, which causes high memory usage and OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that when Aggregation is pushed down through Union in MPP execution plans, the results are incorrect [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue of incorrect memory usage estimation in `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that the zip file generated by `plan replayer` cannot be imported back into TiDB [#46474](https://github.com/pingcap/tidb/issues/46474) @[YangKeao](https://github.com/YangKeao)
    - Fix the incorrect cost estimation caused by an excessively large `N` in `LIMIT N` [#43285](https://github.com/pingcap/tidb/issues/43285) @[qw4990](https://github.com/qw4990)
    - Fix the panic issue that might occur when constructing TopN structure for statistics [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that panic might occur when `tidb_enable_ordered_result_mode` is enabled [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the optimizer mistakenly selects IndexFullScan to reduce sort introduced by window functions [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the result might be incorrect when predicates are pushed down to common table expressions [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - Fix the issue that column pruning can cause panic in specific situations [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue of possible syntax error when a common table expression (CTE) containing aggregate or window functions is referenced by other recursive CTEs [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that an exception might occur when using the `QB_NAME` hint in a prepared statement [#46817](https://github.com/pingcap/tidb/issues/46817) @[jackysp](https://github.com/jackysp)
    - Fix the issue of Goroutine leak when using `AUTO_ID_CACHE=1` [#46324](https://github.com/pingcap/tidb/issues/46324) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB might panic when shutting down [#32110](https://github.com/pingcap/tidb/issues/32110) @[july2993](https://github.com/july2993)
    - Fix the issue of not handling locks in the MVCC interface when reading schema diff commit versions from the TiDB schema cache [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue of duplicate rows in `information_schema.columns` caused by renaming a table [#47064](https://github.com/pingcap/tidb/issues/47064) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the bugs in the `LOAD DATA REPLACE INTO` statement [#47995](https://github.com/pingcap/tidb/issues/47995)) @[lance6716](https://github.com/lance6716)
    - Fix the issue of `IMPORT INTO` task failure caused by PD leader malfunction for 1 minute [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue of `ADMIN CHECK` failure caused by creating an index on a date type field [#47426](https://github.com/pingcap/tidb/issues/47426) @[tangenta](https://github.com/tangenta)
    - Fix the issue of unsorted row data returned by `TABLESAMPLE` [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)

+ TiKV

    - Fix the issue that moving a peer might cause the performance of the Follower Read to deteriorate [#15468](https://github.com/tikv/tikv/issues/15468) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the data error of continuously increasing raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that requests of the TiDB Lightning checksum coprocessor time out when there is online workload [#15565](https://github.com/tikv/tikv/issues/15565) @[lance6716](https://github.com/lance6716)
    - Fix security issues by upgrading the version of `lz4-sys` to 1.9.4  [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix security issues by upgrading the version of `tokio` to 6.5 [#15621](https://github.com/tikv/tikv/issues/15621) @[LykxSassinator](https://github.com/LykxSassinator)
    - Fix security issues by removing the `flatbuffer` [#15621](https://github.com/tikv/tikv/issues/15621) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that resolved-ts lag increases when TiKV stores are partitioned [#15679](https://github.com/tikv/tikv/issues/15679) @[hicqu](https://github.com/hicqu)
    - Fix the TiKV OOM issue that occurs when restarting TiKV and there are a large number of Raft logs that are not applied [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - Fix the issue that stale peers are retained and block resolved-ts after Regions are merged [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the scheduler command variables are incorrect in Grafana on the cloud environment [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that TiKV panics due to inconsistent metadata between Regions [#13311](https://github.com/tikv/tikv/issues/13311) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that TiKV panics when the leader is forced to exit during Online Unsafe Recovery [#15629](https://github.com/tikv/tikv/issues/15629) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that TiKV coprocessor might return stale data when removing a Raft peer [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)
    - Fix the issue that resolved-ts might be blocked for 2 hours [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Flashback might get stuck when encountering `notLeader` or `regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)

+ PD

    - Fix potential security risks of the plugin directory and files [#7094](https://github.com/tikv/pd/issues/7094) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that modified isolation levels are not synchronized to the default placement rules [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - Fix the issue that `evict-leader-scheduler` might lose configuration [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the method for counting empty Regions might cause Regions to be unbalanced during the recovery process of BR [#7148](https://github.com/tikv/pd/issues/7148) @[Cabinfever](https://github.com/CabinfeverB)
    - Fix the issue that `canSync` and `hasMajority` might be calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode when the configuration of Placement Rules is complex [#7201](https://github.com/tikv/pd/issues/7201) @[disksing](https://github.com/disksing)
    - Fix the issue that `available_stores` is calculated incorrectly for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7221](https://github.com/tikv/pd/issues/7221) @[disksing](https://github.com/disksing)
    - Fix the issue that the primary AZ cannot add TiKV nodes when the secondary AZ is down for clusters adopting the Data Replication Auto Synchronous (DR Auto-Sync) mode [#7218](https://github.com/tikv/pd/issues/7218) @[disksing](https://github.com/disksing)
    - Fix the issue that adding multiple TiKV nodes to a large cluster might cause TiKV heartbeat reporting to become slow or stuck [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - Fix the issue that PD might delete normal Peers when TiKV nodes are unavailable [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that it takes a long time to switch the leader in DR Auto-Sync mode [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)
    - Upgrade the version of Gin Web Framework from v1.8.1 to v1.9.1 to fix some security issues [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)

+ TiFlash

    - Fix the issue that the `max_snapshot_lifetime` metric is displayed incorrectly on Grafana [#7713](https://github.com/pingcap/tiflash/issues/7713) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that executing the `ALTER TABLE ... EXCHANGE PARTITION ...` statement causes panic [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the memory usage reported by MemoryTracker is inaccurate [#8128](https://github.com/pingcap/tiflash/issues/8128) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the log backup might get stuck in some scenarios when backing up large wide tables [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that frequent flushes cause log backup to get stuck [#15602](https://github.com/tikv/tikv/issues/15602) @[3pointer](https://github.com/3pointer)
        - Fix the issue that the retry after an EC2 metadata connection reset cause degraded backup and restore performance [#46750](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that running PITR multiple times within 1 minute might cause data loss [#15483](https://github.com/tikv/tikv/issues/15483) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the default values for BR SQL commands and CLI are different, which might cause OOM issues [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that log backup might panic when the PD owner is transferred [#47533](https://github.com/pingcap/tidb/issues/47533) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiCDC

        - Fix the issue that TiCDC server might panic when executing lossy DDL statements in upstream [#9739](https://github.com/pingcap/tiflow/issues/9739) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the replication task reports an error when executing `RESUME` with the redo log feature enabled [#9769](https://github.com/pingcap/tiflow/issues/9769) @[hicqu](https://github.com/hicqu)
        - Fix the issue that replication lag becomes longer when the TiKV node crashes [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the `WHERE` statement does not use the primary key as the condition when replicating data to TiDB or MySQL [#9988](https://github.com/pingcap/tiflow/issues/9988) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the workload of a replication task is not distributed evenly across TiCDC nodes [#9839](https://github.com/pingcap/tiflow/issues/9839) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the interval between replicating DDL statements is too long when redo log is enabled [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the changefeed cannot replicate DML events in bidirectional replication mode if the target table is dropped and then recreated in upstream [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the replication lag becomes longer due to too many NFS files when replicating data to an object storage service [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC accesses the invalid old address during PD scaling up and down [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that fetching wrong memory information might cause OOM issues in some operating systems [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)

    + TiDB Data Migration (DM)

        - Fix the issue that DM skips partition DDLs in optimistic mode [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM cannot properly track upstream table schemas when skipping online DDLs [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that replication lag returned by DM keeps growing when a failed DDL is skipped and no subsequent DDLs are executed [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that DM skips all DMLs when resuming a task in optimistic mode [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that data import fails when encountering the `write to tikv with no leader returned` error [#45673](https://github.com/pingcap/tidb/issues/45673) @[lance6716](https://github.com/lance6716)
        - Fix the issue that data import fails because HTTP retry requests do not use the current request content [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning gets stuck during `writeToTiKV` [#46321](https://github.com/pingcap/tidb/issues/46321) @[lance6716](https://github.com/lance6716)
        - Remove unnecessary `get_regions` calls in physical import mode [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)

    + TiDB Binlog

        - Fix the issue that Drainer exits when transporting a transaction greater than 1 GB [#28659](https://github.com/pingcap/tidb/issues/28659) @[jackysp](https://github.com/jackysp)