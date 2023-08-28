---
title: TiDB 6.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.4.
---

# TiDB 6.5.4 Release Notes

Release date: August 28, 2023

TiDB version: 6.5.4

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.4#version-list)

## Compatibility changes

- To fix the issue that TiDB consumes too much memory when using `Cursor Fetch` to fetch a large result set, TiDB automatically writes the result set to the disk to release memory [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)

## Improvements

+ TiDB 

    - Optimize the performance of `LOAD DATA` statements that contain assignment expressions [#46081](https://github.com/pingcap/tidb/issues/46081) @[gengliqi](https://github.com/gengliqi)
    - Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - Add a `halt-scheduling` configuration item to suspend PD scheduling [#6493](https://github.com/tikv/pd/issues/6493) @[JmPotato](https://github.com/JmPotato)
    
+ TiKV

    - Use gzip compression for `check_leader` requests to reduce traffic [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - Add the `Max gap of safe-ts` and `Min safe ts region` metrics and introduce the `tikv-ctl get_region_read_progress` command to better observe and diagnose the status of resolved-ts and safe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Expose some RocksDB configurations in TiKV that allow users to disable features such as TTL and periodic compaction [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD 

    - Support blocking the Swagger API by default when the Swagger server is not enabled [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)
    - Improve the high availability of etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @[lhy1024](https://github.com/lhy1024)
    - Reduce the memory consumption of `GetRegions` requests [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - Support reusing HTTP connections [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)

+ TiFlash 

    - Improve TiFlash write performance through IO batch optimization [#7735](https://github.com/pingcap/tiflash/issues/7735) @[lidezhu](https://github.com/lidezhu)
    - Improve TiFlash write performance by removing unnecessary fsync operations [#7736](https://github.com/pingcap/tiflash/issues/7736) @[lidezhu](https://github.com/lidezhu)
    - Limit the maximum length of the TiFlash coprocessor task queue to avoid excessive queuing of coprocessor tasks, which impacts TiFlash's service availability [#7747](https://github.com/pingcap/tiflash/issues/7747) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR) 

        - Enhance support for connection reuse by setting `MaxIdleConns` and `MaxIdleConnsPerHost` parameters in the HTTP client [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - Improve fault tolerance of BR when it fails to connect to PD or external S3 storage [#42909](https://github.com/pingcap/tidb/issues/42909) @[Leavrth](https://github.com/Leavrth)
        - Add a new restore parameter `WaitTiflashReady`. When this parameter is enabled, the restore operation will be completed after TiFlash replicas are successfully replicated [#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - Refine the status message when TiCDC retries after a failure [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)
        - Optimize the way TiCDC handles messages that exceed the limit when synchronizing to Kafka by supporting only sending the primary key to the downstream [#9574](https://github.com/pingcap/tiflow/issues/9574) @[3AceShowHand](https://github.com/3AceShowHand)
        - Storage Sink now supports hexadecimal encoding for HEX formatted data, making it compatible with AWS DMS format specifications [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM) 
    
        - Support strict optimistic mode for incompatible DDL statements [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + Dumpling 

        - Reduce export overhead by skipping querying all databases and tables when exporting data with the `-sql` parameter [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

## Bug fixes

+ TiDB 

    - Fix the issue that the `index out of range` error might be reported when pushing down the `STREAM_AGG()` operator [#40857](https://github.com/pingcap/tidb/issues/40857) @[Dousir9](https://github.com/Dousir9)
    - Fix the issue that TiDB ignores all partition information and creates a non-partitioned table when the `CREATE TABLE` statement contains sub-partition definitions [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - Fix the issue that incorrect `stale_read_ts` setting might cause `PREPARE stmt` to read data incorrectly [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06) 
    - Fix the issue of possible data race in ActivateTxn [#42092](https://github.com/pingcap/tidb/issues/42092) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that a batch client does not reconnect timely [#44431](https://github.com/pingcap/tidb/issues/44431) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that SQL compile error logs are not redacted [#41831](https://github.com/pingcap/tidb/issues/41831) @[lance6716](https://github.com/lance6716)
    - Fix the issue that using CTEs and correlated subqueries simultaneously might result in incorrect query results or panic [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TTL tasks cannot trigger statistics updates in time [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the GC Resolve Locks step might miss some pessimistic locks [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the potential memory leak issue in memory tracker [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the data length in the `QUERY` column of the `INFORMATION_SCHEMA.DDL_JOBS` table might exceed the column definition [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the PD OOM issue when there is a large number of Regions but the table ID cannot be pushed down when querying some virtual tables using `Prepare` or `Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - Fix the issue that statistics auto-collection might not trigger correctly on a partitioned table after adding a new index to the partitioned table [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that excessive memory consumption of SQL execution details in statistics causes TiDB OOM in extreme cases [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that batch coprocessor retry might generate incorrect Region information that causes query failure [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - Fix the hang-up issue that occurs when queries with `indexMerge` are killed [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that querying the system table `INFORMATION_SCHEMA.TIKV_REGION_STATUS` returns incorrect results in some cases [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that query results in MPP mode are incorrect when `tidb_enable_parallel_apply` is enabled [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - Fix the issue that queries might return incorrect results when `tidb_opt_agg_push_down` is enabled [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - Fix the can't find proper physical plan issue caused by virtual columns [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - Fix the panic issue caused by empty `processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - Fix the issue that the query result of the `SELECT CAST(n AS CHAR)` statement is incorrect when `n` in the statement is a negative number [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - Fix the issue that when the MySQL Cursor Fetch protocol is used, the memory consumption of result sets might exceed the `tidb_mem_quota_query` limit and causes TiDB OOM. After the fix, TiDB will automatically write result sets to the disk to release memory [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - Fix the `duplicate entry` error that occurs when restoring a table with `AUTO_ID_CACHE=1` using BR [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `SELECT` statement returns an error for a partitioned table if the table partition definition uses the `FLOOR()` function to round a partitioned column [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that concurrent view might cause DDL operations to be blocked [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - Fix the issue that a statistics collection task fails due to an incorrect `datetime` value [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that some DDL statements might be stuck for a period after the PD node of a cluster is replaced [#33908](https://github.com/pingcap/tidb/issues/33908)
    - Fix the issue that `resolve lock` might hang when there is a sudden change in PD time [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - Fix the potential data race issue in index scan [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `FormatSQL()` method cannot properly truncate extremely long SQL statements in input [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that users can view information in the `INFORMATION_SCHEMA.TIFLASH_REPLICA` table even without permissions [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that the behavior is inconsistent with MySQL when comparing a `DATETIME` or `TIMESTAMP` column with a number constant [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - Fix the issue that an error in Index Join might cause the query to get stuck [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that killing a connection might cause go coroutine leaks [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - Fix the issue that the `tmp-storage-quota` configuration does not take effect [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that TiFlash replicas might be unavailable when a TiFlash node is down in the cluster [#38484](https://github.com/pingcap/tidb/issues/38484) @[hehechen](https://github.com/hehechen)
    - Fix the issue that TiDB crashes due to possible data race when reading and writing `Config.Lables` concurrently [#45561](https://github.com/pingcap/tidb/issues/45561) @[genliqi](https://github.com/gengliqi)

+ TiKV

    - Fix the issue that the `ttl-check-poll-interval` configuration item does not take effect on RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Fix the issue that Online Unsafe Recovery does not abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Region Merge might be blocked after executing `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix the data inconsistency issue that might occur when one TiKV node is isolated and another node is restarted [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - Fix the issue that the QPS drops to zero in the sync-recover phase under the Data Replication Auto Synchronous mode [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - Fix the issue that encryption might cause data corruption during partial write [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - Fix the issue of heartbeat storms by reducing the number of store heartbeat retries [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - Fix the issue that traffic control might not work when there is a high amount of pending compaction bytes [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that TiKV might consume more memory when the Old Value feature in TiCDC is enabled [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Fix the issue that when etcd is already started but the client has not yet connected to it, calling the client might cause PD to panic [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that a leader cannot exit for a long time [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that when the placement rule uses `LOCATION_LABLES`, SQL and the Rule Checker are not compatible [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)
    - Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that unhealthy peers cannot be removed when rule checker selects peers [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - Fix the issue that failed learner peers in `unsafe recovery` are ignored in `auto-detect` mode [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)

+ TiFlash 

    - Fix the issue that queries fail after `fsp` is changed for `DATETIME`, `TIMESTAMP`, or `TIME` data type [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash data is inconsistent due to invalid range keys of a region [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - Fix the issue that when there are multiple HashAgg operators within the same MPP task, the compilation of the MPP task might take an excessively long time, severely affecting query performance [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)
    - Fix the issue that TiFlash takes too long to restart after using Online Unsafe Recovery [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)
    - Fix the issue that TiFlash rounds the `DECIMAL` result incorrectly when doing division [#6462](https://github.com/pingcap/tiflash/issues/6462) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue of restore failures by increasing the default values of the global parameters `TableColumnCountLimit` and `IndexLimit` used by BR to their maximum values [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of rewrite failures when processing DDL meta information in PITR [#43184](https://github.com/pingcap/tidb/issues/43184) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of panic caused by not checking function returns during PITR execution [#45853](https://github.com/pingcap/tidb/issues/45853) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue of obtaining invalid region ID when using S3-compatible storage other than Amazon S3 [#41916](https://github.com/pingcap/tidb/issues/41916) [#42033](https://github.com/pingcap/tidb/issues/42033) @[3pointer](https://github.com/3pointer)
        - Fix the potential error in fine-grained backup phase in RawKV mode [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue that the replication task might get stuck when the downstream encounters an error and retries [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the replication task fails due to short retry intervals when synchronizing to Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that TiCDC might cause synchronization write conflicts when modifying multiple unique key rows in one transaction on the upstream [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC might incorrectly synchronize rename DDL operations [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that the replication task might get stuck when the downstream encounters a short-term failure [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - Fix the panic issue that might occur when the TiCDC node status changes [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that when Kafka Sink encounters errors it might indefinitely block changefeed progress [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the data inconsistency issue that might occur when some TiCDC nodes are isolated from the network [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the replication task might get stuck when the redo log is enabled and there is an exception downstream [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that changefeeds would fail due to the temporary unavailability of PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of too many downstream logs caused by frequently setting the downstream bidirectional replication-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that Avro protocol incorrectly identifies `Enum` type values [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the panic issue when the unique key column name is null [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)
        - Fix the deadlock issue that might occur when the validator handles errors incorrectly, and optimize the retry mechanism [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that collation is not considered when calculating the causality key [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)

    + TiDB Lightning

        - Fix the issue that the disk quota check might block when an engine is importing data [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that checksum reports an error `Region is unavailable` when SSL is enabled on the target cluster [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that encoding errors cannot be logged correctly [#44321](https://github.com/pingcap/tidb/issues/44321) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that route might panic when importing CSV data [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that importing table A in logical import mode might mistakenly report that table B does not exist [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that the data type is wrong when saving `NEXT_GLOBAL_ROW_ID` [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that checksum still reports errors when `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the issue that data import fails when the PD cluster address changes [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that data import fails when some PD nodes fail [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that when a table with auto-incremental columns sets `AUTO_ID_CACHE=1`, the base value of the ID allocator is incorrect [#46100](https://github.com/pingcap/tidb/issues/46100) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - Fix the issue that the exported file is lost due to unprocessed file writer closing error when exporting to Amazon S3 [#45353](https://github.com/pingcap/tidb/issues/45353) @[lichunzhu](https://github.com/lichunzhu)

    + TiDB Binlog

        - Fix the issue that the etcd client does not automatically synchronize the latest node information during initialization [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
