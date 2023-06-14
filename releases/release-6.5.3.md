---
title: TiDB 6.5.3 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.3.
---

# TiDB 6.5.3 Release Notes

Release date: June 14, 2023

TiDB version: 6.5.3

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.3#version-list)

## Improvements

+ TiDB

    - Improve the performance of `TRUNCATE` on partitioned tables with Placement Rules [#43070](https://github.com/pingcap/tidb/issues/43070) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Avoid invalid Stale Read retries after resolving locks [#43659](https://github.com/pingcap/tidb/issues/43659) @[you06](https://github.com/you06)
    - Reduce latency by using leader read when Stale Read encounters the `DataIsNotReady` error [#765](https://github.com/tikv/client-go/pull/765) @[Tema](https://github.com/Tema)
    - Add `Stale Read OPS` and `Stale Read MBps` metrics to track hit rate and traffic when using Stale Read [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)

+ TiKV

    - Reduce traffic by using gzip to compress `check_leader` requests [#14839](https://github.com/tikv/tikv/issues/14839) @[cfzjywxk](https://github.com/cfzjywxk)

+ PD

    - Use a separate gRPC connection for PD leader election to prevent the impact of other requests [#6403](https://github.com/tikv/pd/issues/6403) @[rleungx](https://github.com/rleungx)

+ Tools

    + TiCDC

        - Optimize the way TiCDC handles DDLs so that DDLs do not block the use of other unrelated DML Events, and reduce memory usage [#8106](https://github.com/pingcap/tiflow/issues/8106) @[asddongmen](https://github.com/asddongmen)
        - Optimize the Decoder interface and add a new method `AddKeyValue` [#8861](https://github.com/pingcap/tiflow/issues/8861) @[3AceShowHand](https://github.com/3AceShowHand)
        - Optimize the directory structure when DDL events occur in the scenario of replicating data to object storage [#8890](https://github.com/pingcap/tiflow/issues/8890) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Support replicating data to the Kafka-on-Pulsar downstream [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)
        - Support using the OAuth protocol for validation when replicating data to Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @[hi-rustin](https://github.com/hi-rustin)
        - Optimize the way TiCDC handles the `UPDATE` statement during data replication using the Avro or CSV protocol, by splitting `UPDATE` into `DELETE` and `INSERT` statements, so that you can get the old value from the `DELETE` statement [#9086](https://github.com/pingcap/tiflow/issues/9086) @[3AceShowHand](https://github.com/3AceShowHand)
        - Add a configuration item `insecure-skip-verify` to control whether to set the authentication algorithm in the scenario of enabling TLS [#8867](https://github.com/pingcap/tiflow/issues/8867) @[hi-rustin](https://github.com/hi-rustin)
        - Optimize DDL replication operations to mitigate the impact of DDL operations on downstream latency [#8686](https://github.com/pingcap/tiflow/issues/8686) @[hi-rustin](https://github.com/hi-rustin)
        - Optimize the method of setting GC TLS for the upstream when the TiCDC replication task fails [#8403](https://github.com/pingcap/tiflow/issues/8403) @[charleszheng44](https://github.com/charleszheng44)

    + TiDB Binlog

        - Optimize the method of retrieving table information to reduce the initialization time and memory usage of Drainer [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## Bug fixes

+ TiDB

    - Fix the issue that the `min, max` query result is incorrect [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue of incorrect execution plans when pushing down window functions to TiFlash [#43922](https://github.com/pingcap/tidb/issues/43922) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the query with CTE causes TiDB to hang [#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that the SQL statement reports the `runtime error: index out of range` error when using the `AES_DECRYPT` expression [#43063](https://github.com/pingcap/tidb/issues/43063) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the `SHOW PROCESSLIST` statement cannot display the TxnStart of the transaction of the statement with a long subquery time [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - Fix the issue that PD isolation might block the running DDL [#44014](https://github.com/pingcap/tidb/issues/44014) [#43755](https://github.com/pingcap/tidb/issues/43755) [#44267](https://github.com/pingcap/tidb/issues/44267) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the TiDB panic issue that occurs when querying union views and temporary tables with `UNION` [#42563](https://github.com/pingcap/tidb/issues/42563) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the behavior issue of Placement Rules in partitioned tables, so that the Placement Rules in deleted partitions can be correctly set and recycled [#44116](https://github.com/pingcap/tidb/issues/44116) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that truncating a partition of a partitioned table might cause the Placement Rule of the partition to become invalid [#44031](https://github.com/pingcap/tidb/issues/44031) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TiCDC might lose some row changes during table renaming [#43338](https://github.com/pingcap/tidb/issues/43338) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the DDL job history is lost after importing a table using BR [#43725](https://github.com/pingcap/tidb/issues/43725) @[tangenta](https://github.com/tangenta)
    - Fix the issue that `JSON_OBJECT` might report an error in some cases [#39806](https://github.com/pingcap/tidb/issues/39806) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that the cluster cannot query some system views in IPv6 environment [#43286](https://github.com/pingcap/tidb/issues/43286) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that when the PD member address changes, allocating ID for the `AUTO_INCREMENT` column will be blocked for a long time [#42643](https://github.com/pingcap/tidb/issues/42643) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that TiDB sends duplicate requests to PD during placement rules recycling, causing numerous `full config reset` entries in the PD log [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the `SHOW PRIVILEGES` statement returns an incomplete privilege list [#40591](https://github.com/pingcap/tidb/issues/40591) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that `ADMIN SHOW DDL JOBS LIMIT` returns incorrect results [#42298](https://github.com/pingcap/tidb/issues/42298) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue that the `tidb_auth_token` user fails to be created when the password complexity check is enabled [#44098](https://github.com/pingcap/tidb/issues/44098) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - Fix the issue of not finding the partition during inner join in dynamic pruning mode [#43686](https://github.com/pingcap/tidb/issues/43686) @[mjonss](https://github.com/mjonss)
    - Fix the issue that the `Data Truncated` warning occurs when executing `MODIFY COLUMN` on a partitioned table [#41118](https://github.com/pingcap/tidb/issues/41118) @[mjonss](https://github.com/mjonss)
    - Fix the issue of displaying the incorrect TiDB address in IPv6 environment [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - Fix the issue that CTE results are incorrect when pushing down predicates [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - Fix the issue that incorrect results might be returned when using a common table expression (CTE) in statements with non-correlated subqueries [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    - Fix the issue that Join Reorder might cause incorrect outer join results [#44314](https://github.com/pingcap/tidb/issues/44314) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that in some extreme cases, when the first statement of a pessimistic transaction is retried, resolving locks on this transaction might affect transaction correctness [#42937](https://github.com/pingcap/tidb/issues/42937) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that in some rare cases, residual pessimistic locks of pessimistic transactions might affect data correctness when GC resolves locks [#43243](https://github.com/pingcap/tidb/issues/43243) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that the scan detail information during the execution of `batch cop` might be inaccurate [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - Fix the issue that TiDB cannot read data updates when Stale Read and `PREPARE` statements are used at the same time [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06)
    - Fix the issue that an `assertion failed` error might be mistakenly reported when executing the `LOAD DATA` statement [#43849](https://github.com/pingcap/tidb/issues/43849) @[you06](https://github.com/you06)
    - Fix the issue that the coprocessor cannot fall back to the leader when a `region data not ready` error occurs during the use of Stale Read [#43365](https://github.com/pingcap/tidb/issues/43365) @[you06](https://github.com/you06)

+ TiKV

    - Fix the issue of file handle leakage in Continuous Profiling [#14224](https://github.com/tikv/tikv/issues/14224) @[tabokie](https://github.com/tabokie)
    - Fix the issue that PD crash might cause PITR to fail to proceed [#14184](https://github.com/tikv/tikv/issues/14184) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the issue that encryption key ID conflict might cause the deletion of the old keys [#14585](https://github.com/tikv/tikv/issues/14585) @[tabokie](https://github.com/tabokie)
    - Fix the issue that autocommit and point get replica read might break linearizability [#14715](https://github.com/tikv/tikv/issues/14715) @[cfzjywxk](https://github.com/cfzjywxk)
    - Fix the performance degradation issue caused by accumulated lock records when a cluster is upgraded from a previous version to v6.5 or later versions [#14780](https://github.com/tikv/tikv/issues/14780) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix the issue that TiDB Lightning might cause SST file leakage [#14745](https://github.com/tikv/tikv/issues/14745) @[YuJuncen](https://github.com/YuJuncen)
    - Fix the potential conflict between the encryption key and raft log file deletion that might cause TiKV to fail to start [#14761](https://github.com/tikv/tikv/issues/14761) @[Connor1996](https://github.com/Connor1996)

+ TiFlash

    - Fix the performance degradation issue of the partition TableScan operator during Region transfer [#7519](https://github.com/pingcap/tiflash/issues/7519) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that a TiFlash query might report an error if the `GENERATED` type field is present along with the `TIMESTAMP` or `TIME` type [#7468](https://github.com/pingcap/tiflash/issues/7468) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - Fix the issue that large update transactions might cause TiFlash to repeatedly report errors and restart [#7316](https://github.com/pingcap/tiflash/issues/7316) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the error "Truncate error cast decimal as decimal" occurs when reading data from TiFlash with the `INSERT SELECT` statement [#7348](https://github.com/pingcap/tiflash/issues/7348) @[windtalker](https://github.com/windtalker)
    - Fix the issue that queries might consume more memory than needed when the data on the Join build side is very large and contains many small string type columns [#7416](https://github.com/pingcap/tiflash/issues/7416) @[yibin87](https://github.com/yibin87)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the error message "resolve lock timeout" of BR is misleading when a backup fails, which hides the actual error information [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix an OOM issue that might occur when there are as many as 50,000 tables [#7872](https://github.com/pingcap/tiflow/issues/7872) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC gets stuck when an OOM occurs in upstream TiDB [#8561](https://github.com/pingcap/tiflow/issues/8561) @[overvenus](https://github.com/overvenus)
        - Fix the issue that TiCDC gets stuck when PD fails such as network isolation or PD Owner node reboot [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue of TiCDC time zone setting [#8798](https://github.com/pingcap/tiflow/issues/8798) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that checkpoint lag increases when one of the upstream TiKV nodes crashes [#8858](https://github.com/pingcap/tiflow/issues/8858) @[hicqu](https://github.com/hicqu)
        - Fix the issue that when replicating data to downstream MySQL, a replication error occurs after the `FLASHBACK CLUSTER TO TIMESTAMP` statement is executed in the upstream TiDB [#8040](https://github.com/pingcap/tiflow/issues/8040) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that when replicating data to object storage, the `EXCHANGE PARTITION` operation in the upstream cannot be properly replicated to the downstream [#8914](https://github.com/pingcap/tiflow/issues/8914) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the OOM issue caused by excessive memory usage of the sorter component in some special scenarios [#8974](https://github.com/pingcap/tiflow/issues/8974) @[hicqu](https://github.com/hicqu)
        - Fix the issue that when the downstream is Kafka, TiCDC queries the downstream metadata too frequently and causes excessive workload in the downstream [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that when a replication error occurs due to an oversized Kafka message, the message body is recorded in the log [#9031](https://github.com/pingcap/tiflow/issues/9031) @[darraes](https://github.com/darraes)
        - Fix the TiCDC node panic that occurs when the downstream Kafka sinks are rolling restarted [#9023](https://github.com/pingcap/tiflow/issues/9023) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that when replicating data to storage services, the JSON file corresponding to downstream DDL statements does not record the default values of table fields [#9066](https://github.com/pingcap/tiflow/issues/9066) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Lightning

        - Fix the issue that OOM might occur when importing a wide table [#43728](https://github.com/pingcap/tidb/issues/43728) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue of `write to tikv with no leader returned` when importing a large amount of data [#43055](https://github.com/pingcap/tidb/issues/43055) @[lance6716](https://github.com/lance6716)
        - Fix a possible OOM problem when there is an unclosed delimiter in the data file [#40400](https://github.com/pingcap/tidb/issues/40400) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - Add a retry mechanism when encountering an `unknown RPC` error during data import [#43291](https://github.com/pingcap/tidb/issues/43291) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - Fix the issue that TiDB Binlog reports an error when encountering a `CANCELED` DDL statement [#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @[okJiang](https://github.com/okJiang)
