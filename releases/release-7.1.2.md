---
title: TiDB 7.1.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.2.
---

# TiDB 7.1.2 Release Notes

Release date: October 25, 2023

TiDB version: 7.1.2

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.2#version-list)

## Compatibility changes

- Introduce the [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-new-in-v712) system variable to control whether the optimizer selects hash joins for tables [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)
- Disable periodic compaction of RocksDB by default, so that the default behavior of TiKV RocksDB is now consistent with that in versions before v6.5.0. This change prevents potential performance impact caused by a significant number of compactions after upgrading. In addition, TiKV introduces two new configuration items [`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#periodic-compaction-seconds-new-in-v712) and [`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#ttl-new-in-v712), enabling you to manually configure periodic compaction of RocksDB [#15355](https://github.com/tikv/tikv/issues/15355) @[LykxSassinator](https://github.com/LykxSassinator)
- TiCDC introduces the [`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) configuration item to control the encoding method of binary data in the CSV protocol. The default value is `'base64'` [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
- TiCDC introduces the [`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) configuration item. It is empty by default, which means that the changefeed fails when the message size exceeds the limit of the Kafka topic. When this configuration is set to `"handle-key-only"`, if the message exceeds the size limit, only the handle key will be sent to reduce the message size; if the reduced message still exceeds the limit, then the changefeed fails [#9680](https://github.com/pingcap/tiflow/issues/9680) @[3AceShowHand](https://github.com/3AceShowHand)

## Improvements

+ TiDB

    - Add new optimizer hints, including [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-), [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-), [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-), [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-), and [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    - Add request source information related to the coprocessor [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)
    - Add the `/upgrade/start` and `upgrade/finish` APIs to mark the start and end of the upgrade status for TiDB nodes [#47172](https://github.com/pingcap/tidb/issues/47172) @[zimulala](https://github.com/zimulala)

+ TiKV

    - Optimize the compaction mechanism: when a Region is split, if there is no key to split, a compaction is triggered to eliminate excessive MVCC versions [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Eliminate LRUCache in Router objects to reduce memory usage and prevent OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get-region-read-progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Expose some RocksDB configurations in TiKV that allow users to disable features such as TTL and periodic compaction [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)
    - Add the backoff mechanism for the PD client in the process of connection retries, which gradually increases retry intervals during error retries to reduce PD pressure [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - Avoid holding mutex when writing Titan manifest files to prevent affecting other threads [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)
    - Optimize memory usage of Resolver to prevent OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)

+ PD

    - Optimize the backoff mechanism in the PD caller to reduce the frequency of RPC requests when a call fails [#6556](https://github.com/tikv/pd/issues/6556) @[nolouch](https://github.com/nolouch) @[rleungx](https://github.com/rleungx) @[HuSharp](https://github.com/HuSharp)
    - Introduce the cancel mechanism for the `GetRegions` interface to release CPU and memory in time when the caller is disconnected [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - Add monitoring metrics for the memory usage of index data in Grafana [#8050](https://github.com/pingcap/tiflash/issues/8050) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Enhance support for connection reuse of log backup and PITR restore tasks by setting `MaxIdleConns` and `MaxIdleConnsPerHost` parameters in the HTTP client [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - Reduce the CPU overhead of log backup `resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)
        - Add a new restore parameter `WaitTiflashReady`. When this parameter is enabled, the restore operation will be completed after TiFlash replicas are successfully replicated [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Optimize several TiCDC monitoring metrics and alarm rules [#9047](https://github.com/pingcap/tiflow/issues/9047) @[asddongmen](https://github.com/asddongmen)
        - Kafka Sink supports [sending only handle key data](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit) when a message is too large, avoiding changefeed failure caused by excessive message size [#9680](https://github.com/pingcap/tiflow/issues/9680) @[3AceShowHand](https://github.com/3AceShowHand)
        - Optimize the execution logic of replicating the `ADD INDEX` DDL operations to avoid blocking subsequent DML statements [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)
        - Refine the status message when TiCDC retries after a failure [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - Support strict optimistic mode for incompatible DDL statements [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Change the default value of `checksum-via-sql` to `false` to improve the performance of import tasks [#45368](https://github.com/pingcap/tidb/issues/45368) [#45094](https://github.com/pingcap/tidb/issues/45094) @[GMHDBJD](https://github.com/GMHDBJD)
        - Optimize the retry logic of TiDB Lightning for the `no leader` error during the data import phase [#46253](https://github.com/pingcap/tidb/issues/46253) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB

    - Fix the issue that `GROUP_CONCAT` cannot parse the `ORDER BY` column [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that querying the system table `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns incorrect results in some cases [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that upgrading TiDB gets stuck when reading metadata takes longer than one DDL lease [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    - Fix the issue that executing DML statements with CTE can cause panic [#46083](https://github.com/pingcap/tidb/issues/46083) @[winoros](https://github.com/winoros)
    - Fix the issue of not being able to detect data that does not comply with partition definitions during partition exchange [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the results of `MERGE_JOIN` are incorrect [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - Fix the incorrect result that occurs when comparing unsigned types with `Duration` type constants [#45410](https://github.com/pingcap/tidb/issues/45410) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that `Duplicate entry` might occur when `AUTO_ID_CACHE=1` is set [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the memory leak issue when TTL is running [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that killing a connection might cause go coroutine leaks [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - Fix the issue that an error in Index Join might cause the query to get stuck [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `BatchPointGet` operator returns incorrect results for hash partitioned tables [#46779](https://github.com/pingcap/tidb/issues/46779) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that restrictions on partitioned tables remain on the original table when `EXCHANGE PARTITION` fails or is canceled [#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `TIDB_INLJ` hint does not take effect when joining two sub-queries [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the behavior is inconsistent with MySQL when comparing a `DATETIME` or `TIMESTAMP` column with a number constant [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - Fix the issue that HashCode is repeatedly calculated for deeply nested expressions, which causes high memory usage and OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that access path pruning logic ignores the `READ_FROM_STORAGE(TIFLASH[...])` hint, which causes the `Can't find a proper physical plan` error [#40146](https://github.com/pingcap/tidb/issues/40146) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the `cast(col)=range` condition causes FullScan when CAST has no precision loss [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that `plan replayer dump explain` reports an error [#46197](https://github.com/pingcap/tidb/issues/46197) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the `tmp-storage-quota` configuration does not take effect [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the TiDB parser remains in a state and causes parsing failure [#45898](https://github.com/pingcap/tidb/issues/45898) @[qw4990](https://github.com/qw4990)
    - Fix the issue that when Aggregation is pushed down through Union in MPP execution plans, the results are incorrect [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that TiDB recovers slowly after a panic when `AUTO_ID_CACHE=1` is set [#46454](https://github.com/pingcap/tidb/issues/46454) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the Sort operator might cause TiDB to crash during the spill process [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - Fix the issue of duplicate primary keys when using BR to restore non-clustered index tables with `AUTO_ID_CACHE=1` [#46093](https://github.com/pingcap/tidb/issues/46093) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the query might report an error when querying partitioned tables in static pruning mode and the execution plan contains `IndexLookUp` [#45757](https://github.com/pingcap/tidb/issues/45757) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that inserting data into a partitioned table might fail after exchanging partitions between the partition table and a table with placement policies  [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - Fix the issue of encoding time fields with incorrect timezone information [#46033](https://github.com/pingcap/tidb/issues/46033) @[tangenta](https://github.com/tangenta)
    - Fix the issue that DDL statements that fast add indexes would get stuck when the `tmp` directory does not exist [#45456](https://github.com/pingcap/tidb/issues/45456) @[tangenta](https://github.com/tangenta)
    - Fix the issue that upgrading multiple TiDB instances simultaneously might block the upgrade process [#46288](https://github.com/pingcap/tidb/issues/46228) @[zimulala](https://github.com/zimulala)
    - Fix the issue of uneven Region scattering caused by incorrect parameters used in splitting Regions [#46135](https://github.com/pingcap/tidb/issues/46135) @[zimulala](https://github.com/zimulala)
    - Fix the issue that DDL operations might get stuck after TiDB is restarted [#46751](https://github.com/pingcap/tidb/issues/46751) @[wjhuang2016](https://github.com/wjhuang2016)
    - Prohibit split table operations on non-integer clustered indexes [#47350](https://github.com/pingcap/tidb/issues/47350) @[tangenta](https://github.com/tangenta)
    - Fix the issue that DDL operations might get permanently blocked due to incorrect MDL handling [#46920](https://github.com/pingcap/tidb/issues/46920) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue of duplicate rows in `information_schema.columns` caused by renaming a table [#47064](https://github.com/pingcap/tidb/issues/47064) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the panic issue of `batch-client` in `client-go` [#47691](https://github.com/pingcap/tidb/issues/47691) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that statistics collection on partitioned tables is not killed in time when its memory usage exceeds memory limits [#45706](https://github.com/pingcap/tidb/issues/45706) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that query results are inaccurate when queries contain `UNHEX` conditions [#45378](https://github.com/pingcap/tidb/issues/45378) @[qw4990](https://github.com/qw4990)
    - Fix the issue that TiDB returns `Can't find column` for queries with `GROUP_CONCAT` [#41957](https://github.com/pingcap/tidb/issues/41957) @[AilinKid](https://github.com/AilinKid)

+ TiKV

    - Fix the issue that the `ttl-check-poll-interval` configuration item does not take effect on RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Fix the data error of continuously increasing raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that the QPS drops to zero in the sync-recover phase under the Data Replication Auto Synchronous mode [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - Fix the data inconsistency issue that might occur when one TiKV node is isolated and another node is restarted [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that Region Merge might be blocked after executing `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix the issue of heartbeat storms by reducing the number of store heartbeat retries [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - Fix the issue that Online Unsafe Recovery does not abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that encryption might cause data corruption during partial write [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - Fix the TiKV panic issue caused by incorrect metadata of Region [#13311](https://github.com/tikv/tikv/issues/13311) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the issue that requests of the TiDB Lightning checksum coprocessor time out when there is online workload [#15565](https://github.com/tikv/tikv/issues/15565) @[lance6716](https://github.com/lance6716)
    - Fix the issue that moving a peer might cause the performance of the Follower Read to deteriorate [#15468](https://github.com/tikv/tikv/issues/15468) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Fix the issue that hot Regions might not be scheduled in the v2 scheduler algorithm [#6645](https://github.com/tikv/pd/issues/6645) @[lhy1024](https://github.com/lhy1024)
    - Fix the issue that the TLS handshake might cause high CPU usage in an empty cluster [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)
    - Fix the issue that injection errors between PD nodes might cause PD panic [#6858](https://github.com/tikv/pd/issues/6858) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that store information synchronization might cause the PD leader to exit and get stuck [#6918](https://github.com/tikv/pd/issues/6918) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the Region information is not updated after Flashback [#6912](https://github.com/tikv/pd/issues/6912) @[overvenus](https://github.com/overvenus)
    - Fix the issue that PD might panic during exiting [#7053](https://github.com/tikv/pd/issues/7053) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the context timeout might cause the `lease timeout` error [#6926](https://github.com/tikv/pd/issues/6926) @[rleungx](https://github.com/rleungx)
    - Fix the issue that peers are not properly scattered by group, which might cause uneven distribution of leaders [#6962](https://github.com/tikv/pd/issues/6962) @[rleungx](https://github.com/rleungx)
    - Fix the issue that the isolation level label is not synchronized when updating using pd-ctl [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - Fix the issue that `evict-leader-scheduler` might lose configuration [#6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    - Fix potential security risks of the plugin directory and files [#7094](https://github.com/tikv/pd/issues/7094) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that DDL might not guarantee atomicity after enabling resource control [#45050](https://github.com/pingcap/tidb/issues/45050) @[glorv](https://github.com/glorv)
    - Fix the issue that unhealthy peers cannot be removed when rule checker selects peers [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - Fix the issue that when etcd is already started but the client has not yet connected to it, calling the client might cause PD to panic [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that RU consumption less than 0 causes PD to crash [#6973](https://github.com/tikv/pd/issues/6973) @[CabinfeverB](https://github.com/CabinfeverB)
    - Fix the issue that the client-go regularly updating `min-resolved-ts` might cause PD OOM when the cluster is large [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - Fix the issue that the memory usage reported by MemoryTracker is inaccurate [#8128](https://github.com/pingcap/tiflash/issues/8128) @[JinheLin](https://github.com/JinheLin)
    - Fix the issue that TiFlash data is inconsistent due to invalid range keys of a region [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that queries fail after `fsp` is changed for `DATETIME`, `TIMESTAMP`, or `TIME` data type [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that when there are multiple HashAgg operators within the same MPP task, the compilation of the MPP task might take an excessively long time, severely affecting query performance [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that recovering implicit primary keys using PITR might cause conflicts [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - Fix the issue that PITR fails to recover data from GCS [#47022](https://github.com/pingcap/tidb/issues/47022) @[Leavrth](https://github.com/Leavrth)
        - Fix the potential error in fine-grained backup phase in RawKV mode [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - Fix the issue that recovering meta-kv using PITR might cause errors [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - Fix the errors in BR integration test cases [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - Fix the issue of restore failures by increasing the default values of the global parameters `TableColumnCountLimit` and `IndexLimit` used by BR to their maximum values [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the br CLI client gets stuck when scanning restored data [#45476](https://github.com/pingcap/tidb/issues/45476) @[3pointer](https://github.com/3pointer)
        - Fix the issue that PITR might skip restoring the `CREATE INDEX` DDL statement [#47482](https://github.com/pingcap/tidb/issues/47482) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that running PITR multiple times within 1 minute might cause data loss [#15483](https://github.com/tikv/tikv/issues/15483) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that a replication task in an abnormal state blocks upstream GC [#9543](https://github.com/pingcap/tiflow/issues/9543) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that replicating data to an object storage might cause data inconsistency [#9592](https://github.com/pingcap/tiflow/issues/9592) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that enabling `redo-resolved-ts` might cause changefeed to fail [#9769](https://github.com/pingcap/tiflow/issues/9769) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that fetching wrong memory information might cause OOM issues in some operating systems [#9762](https://github.com/pingcap/tiflow/issues/9762) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue of uneven distribution of write keys among nodes when `scale-out` is enabled [#9665](https://github.com/pingcap/tiflow/issues/9665) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that sensitive user information is recorded in the logs [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC might incorrectly synchronize rename DDL operations [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that upstream TiDB GC is blocked after all changefeeds are removed [#9633](https://github.com/pingcap/tiflow/issues/9633) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC replication tasks might fail in some corner cases [#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue of high TiCDC replication latency caused by network isolation of PD nodes [#9565](https://github.com/pingcap/tiflow/issues/9565) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC accesses the invalid old address during PD scaling up and down [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC cannot recover quickly from TiKV node failures when there are a lot of Regions upstream [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC incorrectly changes the `UPDATE` operation to `INSERT` when using the CSV format [#9658](https://github.com/pingcap/tiflow/issues/9658) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that a replication error occurs when multiple tables are renamed in the same DDL statement on the upstream [#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @[CharlesCheung96](https://github.com/CharlesCheung96) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the replication task fails due to short retry intervals when synchronizing to Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that replication write conflicts might occur when the unique keys for multiple rows are modified in one transaction on the upstream [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that the replication task might get stuck when the downstream encounters a short-term failure [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272) [#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the replication task might get stuck when the downstream encounters an error and retries [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - Fix the issue that replication lag returned by DM keeps growing when a failed DDL is skipped and no subsequent DDLs are executed [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that DM cannot handle conflicts correctly with case-insensitive collations [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)
        - Fix the DM validator deadlock issue and enhance retries [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that DM skips all DMLs when resuming a task in optimistic mode [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM cannot properly track upstream table schemas when skipping online DDLs [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - Fix the issue that DM skips partition DDLs in optimistic mode [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - Fix the issue that when importing a table with `AUTO_ID_CACHE=1`, a wrong `row_id` is assigned [#46100](https://github.com/pingcap/tidb/issues/46100) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that the data type is wrong when saving `NEXT_GLOBAL_ROW_ID` [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that checksum still reports errors when `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that data import fails when the PD cluster address changes [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Lightning fails to start when PD topology is changed [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - Fix the issue that route might panic when importing CSV data [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)

    + TiDB Binlog

        - Fix the issue that Drainer exits when transporting a transaction greater than 1 GB [#28659](https://github.com/pingcap/tidb/issues/28659) @[jackysp](https://github.com/jackysp)