---
title: TiDB 6.1.1 Release Notes
---

# TiDB 6.1.1 Release Notes

Release date: September 1, 2022

TiDB version: 6.1.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.1.1#version-list)

## Compatibility changes

+ TiDB

    - Make the `SHOW DATABASES LIKE …` statement case-insensitive [#34766](https://github.com/pingcap/tidb/issues/34766) @[e1ijah1](https://github.com/e1ijah1)
    - Change the default value of [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) from `1` to `0`, which disables Join Reorder's support for Outer Join by default.

+ Diagnosis

    - Disable the Continuous Profiling feature by default, which avoids the possible TiFlash crash issue that occurs when this feature is enabled. For details, see [#5687](https://github.com/pingcap/tiflash/issues/5687) @[mornyx](https://github.com/mornyx)

## Other changes

- Add the following contents in the `TiDB-community-toolkit` binary package. For details, see [TiDB Installation Packages](/binary-package.md).

    - `server-{version}-linux-amd64.tar.gz`
    - `grafana-{version}-linux-amd64.tar.gz`
    - `alertmanager-{version}-linux-amd64.tar.gz`
    - `prometheus-{version}-linux-amd64.tar.gz`
    - `blackbox_exporter-{version}-linux-amd64.tar.gz`
    - `node_exporter-{version}-linux-amd64.tar.gz`

- Introduce multi-level support for different quality standards on the combination of operating systems and CPU architectures. See [OS and platform requirements](https://docs.pingcap.com/tidb/v6.1/hardware-and-software-requirements#os-and-platform-requirements).

## Improvements

+ TiDB

    - Add a new optimizer `SEMI_JOIN_REWRITE` to improve the performance of `EXISTS` queries [#35323](https://github.com/pingcap/tidb/issues/35323) @[winoros](https://github.com/winoros)

+ TiKV

    - Support compressing the metrics response using gzip to reduce the HTTP body size [#12355](https://github.com/tikv/tikv/issues/12355) @[winoros](https://github.com/winoros)
    - Support reducing the amount of data returned for each request by filtering out some metrics using the [`server.simplify-metrics`](https://docs.pingcap.com/tidb/v6.1/tikv-configuration-file#simplify-metrics-new-in-v611) configuration item [#12355](https://github.com/tikv/tikv/issues/12355) @[glorv](https://github.com/glorv)
    - Support dynamically modifying the number of sub-compaction operations performed concurrently in RocksDB (`rocksdb.max-sub-compactions`) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)

+ PD

    - Improve the scheduling speed of Balance Region in specific stages [#4990](https://github.com/tikv/pd/issues/4990) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiDB Lightning

        - Add a retry mechanism on errors such as `stale command` to improve import success rate [#36877](https://github.com/pingcap/tidb/issues/36877) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Data Migration (DM)

        - Users can manually set the amount of concurrency for lightning loader [#5505](https://github.com/pingcap/tiflow/issues/5505) @[buchuitoudegou](https://github.com/buchuitoudegou)

    + TiCDC

        - Add a sink uri parameter `transaction-atomicity` to support splitting the large transaction in a changefeed. This can greatly reduce the latency and memory consumption of large transactions [#5231](https://github.com/pingcap/tiflow/issues/5231) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Reduce performance overhead caused by runtime context switching in multi-Region scenarios [#5610](https://github.com/pingcap/tiflow/issues/5610) @[hicqu](https://github.com/hicqu)
        - Enhance the MySQL sink to turn off the safe mode automatically [#5611](https://github.com/pingcap/tiflow/issues/5611) @[overvenus](https://github.com/overvenus)

## Bug fixes

+ TiDB

    - Fix the issue that `INL_HASH_JOIN` might hang when used with `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that TiDB might panic when executing the `UPDATE` statement [#32311](https://github.com/pingcap/tidb/issues/32311) @[Yisaer](https://github.com/Yisaer)
    - Fix a bug that TiDB might send coprocessor requests when executing the `SHOW COLUMNS` statement [#36496](https://github.com/pingcap/tidb/issues/36496) @[tangenta](https://github.com/tangenta)
    - Fix a bug that TiDB might return the `invalid memory address or nil pointer dereference` error when executing the `SHOW WARNINGS` statement [#31569](https://github.com/pingcap/tidb/issues/31569) @[zyguan](https://github.com/zyguan)
    - Fix a bug that in the static partition prune mode, SQL statements with an aggregate condition might return wrong result when the table is empty [#35295](https://github.com/pingcap/tidb/issues/35295) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the Join Reorder operation will mistakenly push down its Outer Join condition [#37238](https://github.com/pingcap/tidb/issues/37238) @[winoros](https://github.com/winoros)
    - Fix the issue that CTE-schema hash code is cloned mistakenly, which causes the `Can't find column ... in schema ...` error when CTE is referenced more than once [#35404](https://github.com/pingcap/tidb/issues/35404) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue that the wrong join reorder in some right outer join scenarios causes wrong query result [#36912](https://github.com/pingcap/tidb/issues/36912) @[winoros](https://github.com/winoros)
    - Fix the issue of incorrectly inferred null flag of the TiFlash `firstrow` aggregate function in the EqualAll case [#34584](https://github.com/pingcap/tidb/issues/34584) @[fixdb](https://github.com/fixdb)
    - Fix the issue that Plan Cache does not work when a binding is created with the `IGNORE_PLAN_CACHE` hint [#34596](https://github.com/pingcap/tidb/issues/34596) @[fzzf678](https://github.com/fzzf678)
    - Fix the issu that an `EXCHANGE` operator is missing between the hash-partition window and the single-partition window [#35990](https://github.com/pingcap/tidb/issues/35990) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that partitioned tables cannot fully use indexes to scan data in some cases [#33966](https://github.com/pingcap/tidb/issues/33966) @[mjonss](https://github.com/mjonss)
    - Fix the issue of wrong query result when a wrong default value is set for partial aggregation after the aggregation is pushed down [#35295](https://github.com/pingcap/tidb/issues/35295) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that querying partitioned tables might get the `index-out-of-range` error in some cases [#35181](https://github.com/pingcap/tidb/issues/35181) @[mjonss](https://github.com/mjonss)
    - Fix the issue that a partition is incorrectly pruned if a partition key is used in the query condition and the collate is different from the one in the query partition table [#32749](https://github.com/pingcap/tidb/issues/32749) @[mjonss](https://github.com/mjonss)
    - Fix the issue that when TiDB Binlog is enabled, executing the `ALTER SEQUENCE` statement might cause a wrong metadata version and cause Drainer to exit [#36276](https://github.com/pingcap/tidb/issues/36276) @[AilinKid](https://github.com/AilinKid)
    - Fix the issue of incorrect TiDB status that might appear on startup in some extreme cases [#36791](https://github.com/pingcap/tidb/issues/36791) @[xhebox](https://github.com/xhebox)
    - Fix the potential `UnknownPlanID` issue that occurs when querying the execution plans for partitioned tables in TiDB Dashboard [#35153](https://github.com/pingcap/tidb/issues/35153) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that the column list does not work in the LOAD DATA statement [#35198](https://github.com/pingcap/tidb/issues/35198) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Fix the issue of the `data and columnID count not match` error that occurs when inserting duplicated values with TiDB Binlog enabled [#33608](https://github.com/pingcap/tidb/issues/33608) @[zyguan](https://github.com/zyguan)
    - Remove the limitation of `tidb_gc_life_time` [#35392](https://github.com/pingcap/tidb/issues/35392) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - Fix the `LOAD DATA` statement dead loop when an empty filed terminator is used [#33298](https://github.com/pingcap/tidb/issues/33298) @[zyguan](https://github.com/zyguan)
    - Avoid sending requests to unhealthy TiKV nodes to improve availability [#34906](https://github.com/pingcap/tidb/issues/34906) @[sticnarf](https://github.com/sticnarf)

+ TiKV

    - Fix a bug that Regions might be overlapped if Raftstore is busy [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    - Fix the issue that PD does not reconnect to TiKV after the Region heartbeat is interrupted [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue of inconsistent Region size configuration between TiKV and PD [#12518](https://github.com/tikv/tikv/issues/12518) @[5kbpers](https://github.com/5kbpers)
    - Fix the issue that encryption keys are not cleaned up when Raft Engine is enabled [#12890](https://github.com/tikv/tikv/issues/12890) @[tabokie](https://github.com/tabokie)
    - Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    - Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    - Fix the issue of frequent PD client reconnection that occurs when the PD client meets an error [#12345](https://github.com/tikv/tikv/issues/12345) @[Connor1996](https://github.com/Connor1996)
    - Fix potential panic when parallel recovery is enabled for Raft Engine [#13123](https://github.com/tikv/tikv/issues/13123) @[tabokie](https://github.com/tabokie)
    - Fix the issue that the Commit Log Duration of a new Region is too high, which causes QPS to drop [#13077](https://github.com/tikv/tikv/issues/13077) @[Connor1996](https://github.com/Connor1996)
    - Fix rare panics when Raft Engine is enabled [#12698](https://github.com/tikv/tikv/issues/12698) @[tabokie](https://github.com/tabokie)
    - Avoid redundant log warnings when proc filesystem (procfs) cannot be found [#13116](https://github.com/tikv/tikv/issues/13116) @[tabokie](https://github.com/tabokie)
    - Fix the wrong expression of `Unified Read Pool CPU` in dashboard [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    - Fix the issue that when a Region is large, the default [`region-split-check-diff`](/tikv-configuration-file.md#region-split-check-diff) might be larger than the bucket size [#12598](https://github.com/tikv/tikv/issues/12598) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - Fix the issue that TiKV might panic when Apply Snapshot is aborted and Raft Engine is enabled [#12470](https://github.com/tikv/tikv/issues/12470) @[tabokie](https://github.com/tabokie)
    - Fix the issue that the PD client might cause deadlocks [#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)

+ PD

    - Fix the issue that the online progress is inaccurate when label configurations of cluster nodes are invalid [#5234](https://github.com/tikv/pd/issues/5234) @[rleungx](https://github.com/rleungx)
    - Fix PD panics caused by the issue that gRPC handles errors inappropriately when `enable-forwarding` is enabled [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that `/regions/replicated` might return a wrong status [#5095](https://github.com/tikv/pd/issues/5095) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - Fix the issue that TiFlash crashes after dropping a column of a table with clustered indexes in some situations [#5154](https://github.com/pingcap/tiflash/issues/5154) @[hongyunyan](https://github.com/hongyunyan)
    - Fix the issue that the `format` function might return a `Data truncated` error [#4891](https://github.com/pingcap/tiflash/issues/4891) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - Fix the issue that some obsolete data might persist in storage and cannot be deleted [#5659](https://github.com/pingcap/tiflash/issues/5659) @[lidezhu](https://github.com/lidezhu)
    - Fix unnecessary CPU usage in some edge cases [#5409](https://github.com/pingcap/tiflash/issues/5409) @[breezewish](https://github.com/breezewish)
    - Fix a bug that TiFlash cannot work in a cluster using IPv6 [#5247](https://github.com/pingcap/tiflash/issues/5247) @[solotzg](https://github.com/solotzg)
    - Fix a bug that TiFlash might crash due to an error in parallel aggregation [#5356](https://github.com/pingcap/tiflash/issues/5356) @[gengliqi](https://github.com/gengliqi)
    - Fix a bug that thread resources might leak in case of `MinTSOScheduler` query errors [#5556](https://github.com/pingcap/tiflash/issues/5556) @[windtalker](https://github.com/windtalker)

+ Tools

    + TiDB Lightning

        - Fix the issue that TiDB Lightning fails to connect to TiDB when TiDB uses an IPv6 host [#35880](https://github.com/pingcap/tidb/issues/35880) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the `read index not ready` error by adding a retry mechanism [#36566](https://github.com/pingcap/tidb/issues/36566) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that sensitive information in logs is printed in server mode [#36374](https://github.com/pingcap/tidb/issues/36374) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that TiDB Lightning does not support columns starting with slash, number, or non-ascii characters in Parquet files [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)
        - Fix the issue that de-duplication might cause TiDB Lightning to panic in extreme cases [#34163](https://github.com/pingcap/tidb/issues/34163) @[ForwardStar](https://github.com/ForwardStar)

    + TiDB Data Migration (DM)

        - Fix the issue that the `txn-entry-size-limit` configuration item does not take effect in DM [#6161](https://github.com/pingcap/tiflow/issues/6161) @[ForwardStar](https://github.com/ForwardStar)
        - Fix the issue that the `check-task` command cannot handle special characters [#5895](https://github.com/pingcap/tiflow/issues/5895) @[Ehco1996](https://github.com/Ehco1996)
        - Fix the issue of possible data race in `query-status` [#4811](https://github.com/pingcap/tiflow/issues/4811) @[lyzx2001](https://github.com/lyzx2001)
        - Fix the different output format for the `operate-schema` command [#5688](https://github.com/pingcap/tiflow/issues/5688) @[ForwardStar](https://github.com/ForwardStar)
        - Fix goroutine leak when relay meets an error [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM Worker might get stuck when getting DB Conn [#3733](https://github.com/pingcap/tiflow/issues/3733) @[lance6716](https://github.com/lance6716)
        - Fix the issue that DM fails to start when TiDB uses an IPv6 host [#6249](https://github.com/pingcap/tiflow/issues/6249) @[D3Hunter](https://github.com/D3Hunter)

    + TiCDC

        - Fix the wrong maximum compatible version number [#6039](https://github.com/pingcap/tiflow/issues/6039) @[hi-rustin](https://github.com/hi-rustin)
        - Fix a bug that may cause the cdc server to panic when it receives an HTTP request before it fully starts [#5639](https://github.com/pingcap/tiflow/issues/5639) @[asddongmen](https://github.com/asddongmen)
        - Fix the ddl sink panic issue when the changefeed sync-point is enabled [#4934](https://github.com/pingcap/tiflow/issues/4934) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that a changefeed is stuck in some scenarios when sync-point is enabled [#6827](https://github.com/pingcap/tiflow/issues/6827) @[hicqu](https://github.com/hicqu)
        - Fix a bug that changefeed API does not work properly after the cdc server restarts [#5837](https://github.com/pingcap/tiflow/issues/5837) @[asddongmen](https://github.com/asddongmen)
        - Fix the data race issue in the black hole sink [#6206](https://github.com/pingcap/tiflow/issues/6206) @[asddongmen](https://github.com/asddongmen)
        - Fix the TiCDC panic issue when you set `enable-old-value = false` [#6198](https://github.com/pingcap/tiflow/issues/6198) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the data consistency issue when the redo log feature is enabled [#6189](https://github.com/pingcap/tiflow/issues/6189) [#6368](https://github.com/pingcap/tiflow/issues/6368) [#6277](https://github.com/pingcap/tiflow/issues/6277) [#6456](https://github.com/pingcap/tiflow/issues/6456) [#6695](https://github.com/pingcap/tiflow/issues/6695) [#6764](https://github.com/pingcap/tiflow/issues/6764) [#6859](https://github.com/pingcap/tiflow/issues/6859) @[asddongmen](https://github.com/asddongmen)
        - Fix poor redo log performance by writing redo events asynchronously [#6011](https://github.com/pingcap/tiflow/issues/6011) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the MySQL sink cannot connect to IPv6 addresses [#6135](https://github.com/pingcap/tiflow/issues/6135) @[hi-rustin](https://github.com/hi-rustin)

    + Backup & Restore (BR)

        - Fix a bug that BR reports `ErrRestoreTableIDMismatch` in RawKV mode [#35279](https://github.com/pingcap/tidb/issues/35279) @[3pointer](https://github.com/3pointer)
        - Adjust the backup data directory structure to fix backup failure caused by S3 rate limiting in large cluster backup [#30087](https://github.com/pingcap/tidb/issues/30087) @[MoCuishle28](https://github.com/MoCuishle28)
        - Fix incorrect backup time in the summary log [#35553](https://github.com/pingcap/tidb/issues/35553) @[ixuh12](https://github.com/ixuh12)

    + Dumpling

        - Fix the issue that GetDSN does not support IPv6 [#36112](https://github.com/pingcap/tidb/issues/36112) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Binlog

        - Fix a bug that Drainer cannot send requests correctly to Pump when `compressor` is set to `gzip` [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)
