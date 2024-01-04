---
title: TiDB 7.1.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.3.
---

# TiDB 7.1.3 Release Notes

Release date: December 21, 2023

TiDB version: 7.1.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.3#version-list)

## Compatibility changes

- After further testing, the default value of the TiCDC Changefeed configuration item [`case-sensitive`](/ticdc/ticdc-changefeed-config.md) is changed from `true` to `false`. This means that by default, table and database names in the TiCDC configuration file are case-insensitive [#10047](https://github.com/pingcap/tiflow/issues/10047) @[sdojjy](https://github.com/sdojjy)
- TiCDC Changefeed introduces the following new configuration items:
    - [`sql-mode`](/ticdc/ticdc-changefeed-config.md): enables you to set the [SQL mode](/ticdc/ticdc-ddl.md#sql-mode) used by TiCDC to parse DDL statements when TiCDC replicates data [#9876](https://github.com/pingcap/tiflow/issues/9876) @[asddongmen](https://github.com/asddongmen)
    - [`encoding-worker-num`](/ticdc/ticdc-changefeed-config.md) and [`flush-worker-num`](/ticdc/ticdc-changefeed-config.md): enables you to set different concurrency parameters for the redo module based on specifications of different machines [#10048](https://github.com/pingcap/tiflow/issues/10048) @[CharlesCheung96](https://github.com/CharlesCheung96)
    - [`compression`](/ticdc/ticdc-changefeed-config.md): enables you to configure the compression behavior of redo log files [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md): enables you to set the automatic cleanup of historical data when replicating data to object storage [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Improvements

+ TiDB

    - Support the [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.1/sql-statement-flashback-cluster) syntax [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)

+ PD

    - Enhance the configuration retrieval method of the resource control client to dynamically fetch the latest configurations [#7043](https://github.com/tikv/pd/issues/7043) @[nolouch](https://github.com/nolouch)

+ Tools

    + Backup & Restore (BR)

        - Enable automatic retry of Region scatter during snapshot recovery when encountering timeout failures or cancellations of Region scatter [#47236](https://github.com/pingcap/tidb/issues/47236) @[Leavrth](https://github.com/Leavrth)
        - During restoring a snapshot backup, BR retries when it encounters certain network errors [#48528](https://github.com/pingcap/tidb/issues/48528) @[Leavrth](https://github.com/Leavrth)
        - Introduce a new integration test for Point-In-Time Recovery (PITR) in the `delete range` scenario, enhancing PITR stability  [#47738](https://github.com/pingcap/tidb/issues/47738) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Optimize the memory consumption when TiCDC nodes replicate data to TiDB [#9935](https://github.com/pingcap/tiflow/issues/9935) @[3AceShowHand](https://github.com/3AceShowHand)
        - Optimize some alarm rules [#9266](https://github.com/pingcap/tiflow/issues/9266) @[asddongmen](https://github.com/asddongmen)
        - Optimize the performance of redo log, including parallel writing data to S3 and adopting lz4 compression algorithm [#10176](https://github.com/pingcap/tiflow/issues/10176) [#10226](https://github.com/pingcap/tiflow/issues/10226) @[sdojjy](https://github.com/sdojjy)
        - Improve the performance of TiCDC replicating data to object storage by increasing parallelism [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Reduce the impact of TiCDC incremental scanning on upstream TiKV [#11390](https://github.com/tikv/tikv/issues/11390) @[hicqu](https://github.com/hicqu)
        - Support making TiCDC Canal-JSON content format [compatible with the content format of the official Canal output](https://docs.pingcap.com/tidb/v6.5/ticdc-canal-json#compatibility-with-the-official-canal) by setting `content-compatible=true` in the `sink-uri` configuration [#10106](https://github.com/pingcap/tiflow/issues/10106) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Lightning

        - Add a retry mechanism for `GetTS` failure caused by PD leader change [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB

    - Fix the issue that queries containing common table expressions (CTEs) unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that queries containing CTEs report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the query result is incorrect when an `ENUM` type column is used as the join key [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - Fix the parsing error caused by aggregate or window functions in recursive CTEs [#47711](https://github.com/pingcap/tidb/issues/47711) @[elsa0520](https://github.com/elsa0520)
    - Fix the issue that `UPDATE` statements might be incorrectly converted to PointGet [#47445](https://github.com/pingcap/tidb/issues/47445) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the OOM issue that might occur when TiDB performs garbage collection on the `stats_history` table [#48431](https://github.com/pingcap/tidb/issues/48431) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - Fix the issue that `GenJSONTableFromStats` cannot be killed when it consumes a large amount of memory [#47779](https://github.com/pingcap/tidb/issues/47779) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that the result might be incorrect when predicates are pushed down to common table expressions [#47881](https://github.com/pingcap/tidb/issues/47881) @[winoros](https://github.com/winoros)
    - Fix the issue that `Duplicate entry` might occur when `AUTO_ID_CACHE=1` is set [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - Fix the issue that tables with `AUTO_ID_CACHE=1` might lead to gRPC client leaks when there are a large number of tables [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the incorrect error message for `ErrLoadDataInvalidURI` (invalid S3 URI error) [#48164](https://github.com/pingcap/tidb/issues/48164) @[lance6716](https://github.com/lance6716)
    - Fix the issue that executing `ALTER TABLE ... LAST PARTITION` fails when the partition column type is `DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the actual error message during `IMPORT INTO` execution might be overridden by other error messages [#47992](https://github.com/pingcap/tidb/issues/47992) [#47781](https://github.com/pingcap/tidb/issues/47781) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that TiDB deployed in the cgroup v2 container cannot be detected [#48342](https://github.com/pingcap/tidb/issues/48342) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue of unsorted row data returned by `TABLESAMPLE` [#48253](https://github.com/pingcap/tidb/issues/48253) @[tangenta](https://github.com/tangenta)
    - Fix the issue that panic might occur when `tidb_enable_ordered_result_mode` is enabled [#45044](https://github.com/pingcap/tidb/issues/45044) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the optimizer mistakenly selects IndexFullScan to reduce sort introduced by window functions [#46177](https://github.com/pingcap/tidb/issues/46177) @[qw4990](https://github.com/qw4990)
    - Fix the issue of not handling locks in the MVCC interface when reading schema diff commit versions from the TiDB schema cache [#48281](https://github.com/pingcap/tidb/issues/48281) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue of incorrect memory usage estimation in `INDEX_LOOKUP_HASH_JOIN` [#47788](https://github.com/pingcap/tidb/issues/47788) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue of `IMPORT INTO` task failure caused by PD leader malfunction for 1 minute [#48307](https://github.com/pingcap/tidb/issues/48307) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the panic issue of `batch-client` in `client-go` [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that column pruning can cause panic in specific situations [#47331](https://github.com/pingcap/tidb/issues/47331) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that TiDB does not read `cgroup` resource limits when it is started with `systemd` [#47442](https://github.com/pingcap/tidb/issues/47442) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue of possible syntax error when a common table expression (CTE) containing aggregate or window functions is referenced by other recursive CTEs [#47603](https://github.com/pingcap/tidb/issues/47603) [#47711](https://github.com/pingcap/tidb/issues/47711)  @[elsa0520](https://github.com/elsa0520)
    - Fix the panic issue that might occur when constructing TopN structure for statistics [#35948](https://github.com/pingcap/tidb/issues/35948) @[hi-rustin](https://github.com/hi-rustin)
    - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the chunk cannot be reused when the HashJoin operator performs probe [#48082](https://github.com/pingcap/tidb/issues/48082) @[wshwsh12](https://github.com/wshwsh12)

+ TiKV

    - Fix the issue that if TiKV runs extremely slowly, it might panic after Region merge [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Resolved TS might be blocked for two hours [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - Fix the issue that TiKV reports the `ServerIsBusy` error because it can not append the raft log [#15800](https://github.com/tikv/tikv/issues/15800) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that snapshot restore might get stuck when BR crashes [#15684](https://github.com/tikv/tikv/issues/15684) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that Resolved TS in stale read might cause TiKV OOM issues when tracking large transactions [#14864](https://github.com/tikv/tikv/issues/14864) @[overvenus](https://github.com/overvenus)
    - Fix the issue that damaged SST files might be spreaded to other TiKV nodes [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the scheduler command variables are incorrect in Grafana on the cloud environment [#15832](https://github.com/tikv/tikv/issues/15832) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that stale peers are retained and block resolved-ts after Regions are merged [#15919](https://github.com/tikv/tikv/issues/15919) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - Fix the TiKV OOM issue that occurs when restarting TiKV and there are a large number of Raft logs that are not applied [#15770](https://github.com/tikv/tikv/issues/15770) @[overvenus](https://github.com/overvenus)
    - Fix security issues by upgrading the version of `lz4-sys` to 1.9.4  [#15621](https://github.com/tikv/tikv/issues/15621) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV coprocessor might return stale data when removing a Raft peer [#16069](https://github.com/tikv/tikv/issues/16069) @[overvenus](https://github.com/overvenus)

+ PD

    - Fix the issue that the `resource_manager_resource_unit` metric is empty in TiDB Dashboard when executing `CALIBRATE RESOURCE` [#45166](https://github.com/pingcap/tidb/issues/45166) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the Calibrate by Workload page reports an error [#48162](https://github.com/pingcap/tidb/issues/48162) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that deleting a resource group can damage DDL atomicity [#45050](https://github.com/pingcap/tidb/issues/45050) @[glorv](https://github.com/glorv)
    - Fix the issue that when PD leader is transferred and there is a network partition between the new leader and the PD client, the PD client fails to update the information of the leader [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that adding multiple TiKV nodes to a large cluster might cause TiKV heartbeat reporting to become slow or stuck [#7248](https://github.com/tikv/pd/issues/7248) @[rleungx](https://github.com/rleungx)
    - Fix the issue that TiDB Dashboard cannot read PD `trace` data correctly [#7253](https://github.com/tikv/pd/issues/7253) @[nolouch](https://github.com/nolouch)
    - Fix some security issues by upgrading the version of Gin Web Framework from v1.8.1 to v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - Fix the issue that the rule checker does not add Learners according to the configuration of Placement Rules [#7185](https://github.com/tikv/pd/issues/7185) @[nolouch](https://github.com/nolouch)
    - Fix the issue that PD might delete normal Peers when TiKV nodes are unavailable [#7249](https://github.com/tikv/pd/issues/7249) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that it takes a long time to switch the leader in DR Auto-Sync mode [#6988](https://github.com/tikv/pd/issues/6988) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - Fix the issue that executing the `ALTER TABLE ... EXCHANGE PARTITION ...` statement causes panic [#8372](https://github.com/pingcap/tiflash/issues/8372) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix incorrect display of maximum percentile time for some panels in Grafana [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that a query returns the unexpected error message "Block schema mismatch in FineGrainedShuffleWriter-V1" [#8111](https://github.com/pingcap/tiflash/issues/8111) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the default values for BR SQL commands and CLI are different, which might cause OOM issues [#48000](https://github.com/pingcap/tidb/issues/48000) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the log backup might get stuck in some scenarios when backing up large wide tables [#15714](https://github.com/tikv/tikv/issues/15714) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that the retry after an EC2 metadata connection reset causes degraded backup and restore performance [#46750](https://github.com/pingcap/tidb/issues/47650) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that the `WHERE` clause does not use the primary key as a condition when replicating `DELETE` statements in certain scenarios [#9812](https://github.com/pingcap/tiflow/issues/9812) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that replication tasks get stuck in certain special scenarios when replicating data to object storage [#10041](https://github.com/pingcap/tiflow/issues/10041) [#10044](https://github.com/pingcap/tiflow/issues/10044) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that replication tasks get stuck in certain special scenarios after enabling sync-point and redo log [#10091](https://github.com/pingcap/tiflow/issues/10091) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC mistakenly closes the connection with TiKV in certain special scenarios [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the changefeed cannot replicate DML events in bidirectional replication mode if the target table is dropped and then recreated in upstream [#10079](https://github.com/pingcap/tiflow/issues/10079) @[asddongmen](https://github.com/asddongmen)
        - Fix the performance issue caused by accessing NFS directories when replicating data to an object store sink [#10041](https://github.com/pingcap/tiflow/issues/10041) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the interval between replicating DDL statements is too long when redo log is enabled [#9960](https://github.com/pingcap/tiflow/issues/9960) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that an owner node gets stuck due to NFS failure when the redo log is enabled [#9886](https://github.com/pingcap/tiflow/issues/9886) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the issue that DM performance is degraded due to an inappropriate algorithm used for `CompareGTID` [#9676](https://github.com/pingcap/tiflow/issues/9676) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that data import fails due to the PD leader being killed or slow processing of PD requests [#46950](https://github.com/pingcap/tidb/issues/46950) [#48075](https://github.com/pingcap/tidb/issues/48075) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that TiDB Lightning gets stuck during `writeToTiKV` [#46321](https://github.com/pingcap/tidb/issues/46321) [#48352](https://github.com/pingcap/tidb/issues/48352) @[lance6716](https://github.com/lance6716)
        - Fix the issue that data import fails because HTTP retry requests do not use the current request content [#47930](https://github.com/pingcap/tidb/issues/47930) @[lance6716](https://github.com/lance6716)
        - Remove unnecessary `get_regions` calls in physical import mode [#45507](https://github.com/pingcap/tidb/issues/45507) @[mittalrishabh](https://github.com/mittalrishabh)
