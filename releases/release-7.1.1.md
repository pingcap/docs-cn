---
title: TiDB 7.1.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.1.
---

# TiDB 7.1.1 Release Notes

Release date: July 24, 2023

TiDB version: 7.1.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v7.1.1#version-list)

## Compatibility changes

- TiDB introduces a new system variable `tidb_lock_unchanged_keys` to control whether to lock unchanged keys [#44714](https://github.com/pingcap/tidb/issues/44714) @[ekexium](https://github.com/ekexium)

## Improvements

+ TiDB

    - Plan Cache supports queries with more than 200 parameters [#44823](https://github.com/pingcap/tidb/issues/44823) @[qw4990](https://github.com/qw4990)
    - Optimize the performance of reading the dumped chunks from disk [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)
    - Optimize the logic of constructing index scan range so that it supports converting complex conditions into index scan range [#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - When the retry leader of stale read encounters a lock, TiDB forcibly retries with the leader after resolving the lock, which avoids unnecessary overhead [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)

+ PD

    - PD blocks Swagger API by default when the Swagger server is disabled [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiCDC

        - Optimize the encoding format of binary fields when TiCDC replicates data to object storage services [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support the OAUTHBEARER authentication in the scenario of replication to Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/hi-rustin)

    + TiDB Lightning

        - Improve the retry logic of TiDB Lightning for the PD `ClientTSOStreamClosed` error during the checksum phase [#45301](https://github.com/pingcap/tidb/issues/45301) @[lance6716](https://github.com/lance6716)
        - Verify checksum through SQL after the import to improve stability of verification [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD)

    + Dumpling

        - Dumpling avoids executing table queries when the `--sql` parameter is used, thereby reducing the export overhead [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

    + TiDB Binlog

        - Optimize the method of retrieving table information to reduce the initialization time and memory usage of Drainer [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## Bug fixes

+ TiDB

    - Fix the issue that the GC Resolve Locks step might miss some pessimistic locks [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that Stats Collector might cause deadlock when a new session is created [#44502](https://github.com/pingcap/tidb/issues/44502) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the potential memory leak issue in memory tracker [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that batch coprocessor retry might generate incorrect Region information that causes query failure [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - Fix the potential data race issue in index scan [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that query results in MPP mode are incorrect when `tidb_enable_parallel_apply` is enabled [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - Fix the hang-up issue that occurs when queries with `indexMerge` are killed [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that excessive memory consumption of SQL execution details in statistics causes TiDB OOM in extreme cases [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the `FormatSQL()` method cannot properly truncate extremely long SQL statements in input [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that DDL operations get stuck during cluster upgrade, which causes upgrade failure [#44158](https://github.com/pingcap/tidb/issues/44158) @[zimulala](https://github.com/zimulala)
    - Fix the issue that other TiDB nodes do not take over TTL tasks after failures in one TiDB node [#45022](https://github.com/pingcap/tidb/issues/45022) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that when the MySQL Cursor Fetch protocol is used, the memory consumption of result sets might exceed the `tidb_mem_quota_query` limit and causes TiDB OOM. After the fix, TiDB will automatically write result sets to the disk to release memory [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that users can view information in the `INFORMATION_SCHEMA.TIFLASH_REPLICA` table even without permissions [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that `ROW_COUNT` returned by the `ADMIN SHOW DDL JOBS` statement is inaccurate [#44044](https://github.com/pingcap/tidb/issues/44044) @[tangenta](https://github.com/tangenta)
    - Fix the issue that querying a Range COLUMNS partitioned table might get an error [#43459](https://github.com/pingcap/tidb/issues/43459) @[mjonss](https://github.com/mjonss)
    - Fix the issue that resuming a paused DDL task fails [#44217](https://github.com/pingcap/tidb/issues/44217) @[dhysum](https://github.com/dhysum)
    - Fix the issue that in-memory pessimistic locks cause `FLASHBACK` failures and data inconsistency [#44292](https://github.com/pingcap/tidb/issues/44292) @[JmPotato](https://github.com/JmPotato)
    - Fix the issue that deleted tables can still be read from `INFORMATION_SCHEMA` [#43714](https://github.com/pingcap/tidb/issues/43714) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the cluster upgrade fails when there are paused DDL operations before the upgrade [#44225](https://github.com/pingcap/tidb/issues/44225) @[zimulala](https://github.com/zimulala)
    - Fix the `duplicate entry` error that occurs when restoring a table with `AUTO_ID_CACHE=1` using BR [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the data index inconsistency issue triggered by multiple switches of DDL owner [#44619](https://github.com/pingcap/tidb/issues/44619) @[tangenta](https://github.com/tangenta)
    - Fix the issue that canceling an `ADD INDEX` DDL task in the `none` status might cause memory leak because this task is not removed from the backend task queue [#44205](https://github.com/pingcap/tidb/issues/44205) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the proxy protocol reports the `Header read timeout` error when processing certain erroneous data [#43205](https://github.com/pingcap/tidb/issues/43205) @[blacktear23](https://github.com/blacktear23)
    - Fix the issue that PD isolation might block the running DDL [#44267](https://github.com/pingcap/tidb/issues/44267) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the query result of the `SELECT CAST(n AS CHAR)` statement is incorrect when `n` in the statement is a negative number [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - Fix the issue of excessive memory usage after creating a large number of empty partitioned tables [#44308](https://github.com/pingcap/tidb/issues/44308) @[hawkingrei](https://github.com/hawkingrei)
    - Fix the issue that Join Reorder might cause incorrect outer join results [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that queries containing Common Table Expressions (CTEs) might cause insufficient disk space [#44477](https://github.com/pingcap/tidb/issues/44477) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that dropping a database causes slow GC progress [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that adding an index fails in the ingest mode [#44137](https://github.com/pingcap/tidb/issues/44137) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the `SELECT` statement returns an error for a partitioned table if the table partition definition uses the `FLOOR()` function to round a partitioned column [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - Fix the issue that follower read does not handle flashback errors before retrying, which causes query errors [#43673](https://github.com/pingcap/tidb/issues/43673) @[you06](https://github.com/you06)
    - Fix the issue that using `memTracker` with cursor fetch causes memory leaks [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the `SHOW PROCESSLIST` statement cannot display the TxnStart of the transaction of the statement with a long subquery time [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that the `LEADING` hint does not support querying block aliases [#44645](https://github.com/pingcap/tidb/issues/44645) @[qw4990](https://github.com/qw4990)
    - Fix the issue that `PREPARE stmt FROM "ANALYZE TABLE xxx"` might be killed by `tidb_mem_quota_query` [#44320](https://github.com/pingcap/tidb/issues/44320) @[chrysan](https://github.com/chrysan)
    - Fix the panic issue caused by empty `processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - Fix the issue that data and indexes are inconsistent when the `ON UPDATE` statement does not correctly update the primary key [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan)
    - Fix the issue that queries might return incorrect results when `tidb_opt_agg_push_down` is enabled [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that using CTEs and correlated subqueries simultaneously might result in incorrect query results or panic [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that canceling a DDL task in the rollback state causes errors in related metadata [#44143](https://github.com/pingcap/tidb/issues/44143) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that executing the `UPDATE` statement causes errors due to checking foreign key constraints [#44848](https://github.com/pingcap/tidb/issues/44848) @[crazycs520](https://github.com/crazycs520)

+ PD

    - Fix the issue that Resource Manager repeatedly initializes the default resource group [#6787](https://github.com/tikv/pd/issues/6787) @[glorv](https://github.com/glorv)
    - Fix the issue that in some cases, the `location-labels` set in the Placement Rules in SQL does not schedule as expected [#6662](https://github.com/tikv/pd/issues/6662) @[rleungx](https://github.com/rleungx)
    - Fix the issue that redundant replicas cannot be automatically repaired in some corner cases [#6573](https://github.com/tikv/pd/issues/6573) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - Fix the issue that in the disaggregated storage and compute architecture mode, the TiFlash compute node fetches inaccurate CPU core information [#7436](https://github.com/pingcap/tiflash/issues/7436) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiFlash takes too long to restart after using Online Unsafe Recovery [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that `checksum mismatch` is falsely reported in some cases [#44472](https://github.com/pingcap/tidb/issues/44472) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - Fix the issue that a PD exception might cause the replication task to get stuck [#8808](https://github.com/pingcap/tiflow/issues/8808) [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen) @[fubinzh](https://github.com/fubinzh)
        - Fix the issue of excessive memory consumption when replicating to an object storage service [#8894](https://github.com/pingcap/tiflow/issues/8894) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the replication task might get stuck when the redo log is enabled and there is an exception downstream [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC keeps retrying when there is a downstream failure, which causes the retry time to be too long [#9272](https://github.com/pingcap/tiflow/issues/9272) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of excessive downstream pressure caused by reading downstream metadata too frequently when replicating data to Kafka [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the OOM issue caused by excessive memory usage of the sorter component in some special scenarios [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu)
        - Fix the issue that the `UPDATE` operation cannot output old values when the Avro or CSV protocol is used [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that when replicating data to storage services, the JSON file corresponding to downstream DDL statements does not record the default values of table fields [#9066](https://github.com/pingcap/tiflow/issues/9066) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue of too many downstream logs caused by frequently setting the downstream bidirectional replication-related variables when replicating data to TiDB or MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that when a replication error occurs due to an oversized Kafka message, the message body is recorded in the log [#9031](https://github.com/pingcap/tiflow/issues/9031) @[darraes](https://github.com/darraes)
        - Fix the issue that TiCDC gets stuck when PD fails such as network isolation or PD Owner node reboot [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that Avro protocol incorrectly identifies `Enum` type values [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - Fix the issue that DM-master exits abnormally when a unique index contains empty columns in the table to be migrated [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that the failed connection between TiDB Lightning and PD cannot be retried, improving the import success rate [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Lightning does not correctly display the error message when writing data to TiKV returns an out of space error [#44733](https://github.com/pingcap/tidb/issues/44733) @[lance6716](https://github.com/lance6716)
        - Fix the issue that the `Region is unavailable` error is reported during checksum operation [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the TiDB Lightning panic issue when `experimental.allow-expression-index` is enabled and the default value is UUID [#44497](https://github.com/pingcap/tidb/issues/44497) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that disk quota might be inaccurate due to competing conditions [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that in Logical Import Mode, deleting tables downstream during import might cause TiDB Lightning metadata not to be updated in time [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)

    + Dumpling

        - Fix the issue that Dumpling exits abnormally when the query result set of `--sql` is empty [#45200](https://github.com/pingcap/tidb/issues/45200) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - Fix the issue that TiDB cannot correctly query Binlog node status via `SHOW PUMP STATUS` or `SHOW DRAINER STATUS` after a complete change of the PD address [#42643](https://github.com/pingcap/tidb/issues/42643) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB cannot write binlogs after a complete change of the PD address [#42643](https://github.com/pingcap/tidb/issues/42643) @[lance6716](https://github.com/lance6716)
        - Fix the issue that the etcd client does not automatically synchronize the latest node information during initialization [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)
