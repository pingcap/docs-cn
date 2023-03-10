---
title: TiDB 6.5.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.1.
---

# TiDB 6.5.1 Release Notes

Release date: March 10, 2023

TiDB version: 6.5.1

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.1#version-list)

## Compatibility changes

- Starting from February 20, 2023, the [telemetry feature](/telemetry.md) is disabled by default in new versions of TiDB and TiDB Dashboard, including v6.5.1, and usage information is not collected and shared with PingCAP. Before upgrading to these versions, if the cluster uses the default telemetry configuration, the telemetry feature is disabled after the upgrade. See [TiDB Release Timeline](/releases/release-timeline.md) for specific versions.

    - The default value of the [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402) system variable is changed from `ON` to `OFF`.
    - The default value of the TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402) configuration item is changed from `true` to `false`.
    - The default value of the PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry) configuration item is changed from `true` to `false`.

- Starting from v1.11.3, the telemetry feature is disabled by default in newly deployed TiUP, and usage information is not collected. If you upgrade from a TiUP version earlier than v1.11.3 to v1.11.3 or a later version, the telemetry feature keeps the same status as before the upgrade.

- No longer support modifying column types on partitioned tables because of potential correctness issues. [#40620](https://github.com/pingcap/tidb/issues/40620) @[mjonss](https://github.com/mjonss)

- The default value of the TiKV [`advance-ts-interval`](/tikv-configuration-file.md#advance-ts-interval) configuration item is changed from `1s` to `20s`. You can modify this configuration item to reduce the latency and improve the timeliness of the Stale Read data. See [Reduce Stale Read latency](/stale-read.md#reduce-stale-read-latency) for details.

## Improvements

+ TiDB

    - Starting from v6.5.1, the TiDB cluster deployed by TiDB Operator v1.4.3 or higher supports IPv6 addresses. This means that TiDB can support a larger address space and bring you better security and network performance.

        - Full support for IPv6 addressing: TiDB supports using IPv6 addresses for all network connections, including client connections, internal communication between nodes, and communication with external systems.
        - Dual-stack support: If you are not ready to fully switch to IPv6 yet, TiDB also supports dual-stack networks. This means that you can use both IPv4 and IPv6 addresses in the same TiDB cluster and choose a network deployment mode that prioritizes IPv6 by configuration.

      For more information on IPv6 deployment, see [TiDB on Kubernetes documentation](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#ipv6-support).

    - Support specifying the SQL script executed upon TiDB cluster initialization [#35624](https://github.com/pingcap/tidb/issues/35624) @[morgo](https://github.com/morgo)

        TiDB v6.5.1 adds a new configuration item [`initialize-sql-file`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651). When you start a TiDB cluster for the first time, you can specify the SQL script to be executed by configuring the command line parameter `--initialize-sql-file`. You can use this feature when you need to perform such operations as modifying the value of a system variable, creating a user, or granting privileges. For more information, see [documentation](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#initialize-sql-file-new-in-v651).

    - Clear expired region cache regularly to avoid memory leak and performance degradation [#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf)
    - Add a new configuration item `--proxy-protocol-fallbackable` to control whether to enable PROXY protocol fallback mode. When this parameter is set to `true`, TiDB accepts PROXY client connections and client connections without any PROXY protocol header [#41409](https://github.com/pingcap/tidb/issues/41409) @[blacktear23](https://github.com/blacktear23)
    - Improve the accuracy of Memory Tracker [#40900](https://github.com/pingcap/tidb/issues/40900) [#40500](https://github.com/pingcap/tidb/issues/40500) @[wshwsh12](https://github.com/wshwsh12)
    - When the plan cache fails to take effect, the system returns the reason as a warning [#40210](https://github.com/pingcap/tidb/pull/40210) @[qw4990](https://github.com/qw4990)
    - Improve the optimizer strategy for out-of-range estimation [#39008](https://github.com/pingcap/tidb/issues/39008) @[time-and-fate](https://github.com/time-and-fate)

+ TiKV

    - Support starting TiKV on a CPU with less than 1 core [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)
    - Increase the thread limit of the Unified Read Pool (`readpool.unified.max-thread-count`) to 10 times the CPU quota, to better handle high-concurrency queries [#13690](https://github.com/tikv/tikv/issues/13690) @[v01dstar](https://github.com/v01dstar)
    - Change the the default value of `resolved-ts.advance-ts-interval` from `"1s"` to `"20s"`, to reduce cross-region traffic [#14100](https://github.com/tikv/tikv/issues/14100) @[overvenus](https://github.com/overvenus)

+ TiFlash

    - Accelerate TiFlash startup greatly when the data volume is large [#6395](https://github.com/pingcap/tiflash/issues/6395) @[hehechen](https://github.com/hehechen)

+ Tools

    + Backup & Restore (BR)

        - Optimize the concurrency of downloading log backup files on the TiKV side to improve the performance of PITR in regular scenarios [#14206](https://github.com/tikv/tikv/issues/14206) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Support batch `UPDATE` statements to improve TiCDC replication performance [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)
        - Enable pull-based sink to optimize system throughput [#8232](https://github.com/pingcap/tiflow/issues/8232) @[hi-rustin](https://github.com/hi-rustin)
        - Support storing redo logs to GCS-compatible or Azure-compatible object storage [#7987](https://github.com/pingcap/tiflow/issues/7987) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Implement MQ sink and MySQL sink in the asynchronous mode to improve the sink throughput [#5928](https://github.com/pingcap/tiflow/issues/5928) @[amyangfei](https://github.com/amyangfei) @[CharlesCheung96](https://github.com/CharlesCheung96)

## Bug fixes

+ TiDB

    - Fix the issue that the [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600) configuration item does not take effect for point-get queries [#39928](https://github.com/pingcap/tidb/issues/39928) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the `INSERT` or `REPLACE` statements might panic in long session connections [#40351](https://github.com/pingcap/tidb/issues/40351) @[winoros](https://github.com/winoros)
    - Fix the issue that `auto analyze` causes graceful shutdown to take a long time [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that data race might occur during DDL ingestion [#40970](https://github.com/pingcap/tidb/issues/40970) @[tangenta](https://github.com/tangenta)
    - Fix the issue that data race might occur when an index is added [#40879](https://github.com/pingcap/tidb/issues/40879) @[tangenta](https://github.com/tangenta)
    - Fix the issue that the adding index operation is inefficient due to invalid Region cache when there are many Regions in a table [#38436](https://github.com/pingcap/tidb/issues/38436) @[tangenta](https://github.com/tangenta)
    - Fix the issue that TiDB might deadlock during initialization [#40408](https://github.com/pingcap/tidb/issues/40408) @[Defined2014](https://github.com/Defined2014)
    - Fix the issue that unexpected data is read because TiDB improperly handles `NULL` values when constructing key ranges [#40158](https://github.com/pingcap/tidb/issues/40158) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix the issue that the value of system variables might be incorrectly modified in some cases due to memory reuse [#40979](https://github.com/pingcap/tidb/issues/40979) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that a TTL task fails if the primary key of the table contains an `ENUM` column [#40456](https://github.com/pingcap/tidb/issues/40456) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that TiDB panics when adding a unique index [#40592](https://github.com/pingcap/tidb/issues/40592) @[tangenta](https://github.com/tangenta)
    - Fix the issue that some truncate operations cannot be blocked by MDL when truncating the same table concurrently [#40484](https://github.com/pingcap/tidb/issues/40484) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that TiDB cannot restart after global bindings are created for partition tables in dynamic trimming mode [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - Fix the issue that reading data using the "cursor read" method might return an error because of GC [#39447](https://github.com/pingcap/tidb/issues/39447) @[zyguan](https://github.com/zyguan)
    - Fix the issue that the `EXECUTE` information is null in the result of `SHOW PROCESSLIST` [#41156](https://github.com/pingcap/tidb/issues/41156) @[YangKeao](https://github.com/YangKeao)
    - Fix the issue that when `globalMemoryControl` is killing a query, the `KILL` operation might not end [#41057](https://github.com/pingcap/tidb/issues/41057) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that TiDB might panic after `indexMerge` encounters an error [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - Fix the issue that the `ANALYZE` statement might be terminated by `KILL` [#41825](https://github.com/pingcap/tidb/issues/41825) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - Fix the issue that goroutine leak might occur in `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue of potential wrong results when comparing unsigned `TINYINT`/`SMALLINT`/`INT` values with `DECIMAL`/`FLOAT`/`DOUBLE` values smaller than `0` [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - Fix the issue that enabling `tidb_enable_reuse_chunk` might lead to memory leak [#40987](https://github.com/pingcap/tidb/issues/40987) @[guo-shaoge](https://github.com/guo-shaoge)
    - Fix the issue that data race in time zone might cause data-index inconsistency [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - Fix the issue that the scan detail information during the execution of `batch cop` might be inaccurate [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06)
    - Fix the issue that the upper concurrency of `cop` is not limited [#41134](https://github.com/pingcap/tidb/issues/41134) @[you06](https://github.com/you06)
    - Fix the issue that the `statement context` in `cursor read` is mistakenly cached [#39998](https://github.com/pingcap/tidb/issues/39998) @[zyguan](https://github.com/zyguan)
    - Periodically clean up stale Region cache to avoid memory leak and performance degradation [#40355](https://github.com/pingcap/tidb/issues/40355) @[sticnarf](https://github.com/sticnarf)
    - Fix the issue that using plan cache on queries that contain `year <cmp> const` might get a wrong result [#41626](https://github.com/pingcap/tidb/issues/41626) @[qw4990](https://github.com/qw4990)
    - Fix the issue of large estimation errors when querying with a large range and a large amount of data modification [#39593](https://github.com/pingcap/tidb/issues/39593) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that some conditions cannot be pushed down through Join operators when using Plan Cache [#40093](https://github.com/pingcap/tidb/issues/40093) [#38205](https://github.com/pingcap/tidb/issues/38205) @[qw4990](https://github.com/qw4990)
    - Fix the issue that IndexMerge plans might generate incorrect ranges on the SET type columns [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that Plan Cache might cache FullScan plans when processing `int_col <cmp> decimal` conditions [#40679](https://github.com/pingcap/tidb/issues/40679) [#41032](https://github.com/pingcap/tidb/issues/41032) @[qw4990](https://github.com/qw4990)
    - Fix the issue that Plan Cache might cache FullScan plans when processing `int_col in (decimal...)` conditions [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - Fix the issue that the `ignore_plan_cache` hint might not work for `INSERT` statements [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717)  @[qw4990](https://github.com/qw4990)
    - Fix the issue that Auto Analyze might hinder TiDB from exiting [#40038](https://github.com/pingcap/tidb/issues/40038) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - Fix the issue that incorrect access intervals might be constructed on Unsigned Primary Keys in partitioned tables [#40309](https://github.com/pingcap/tidb/issues/40309) @[winoros](https://github.com/winoros)
    - Fix the issue that Plan Cache might cache Shuffle operators and return incorrect results [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - Fix the issue that creating Global Binding on partitioned tables might cause TiDB to fail to start [#40368](https://github.com/pingcap/tidb/issues/40368) @[Yisaer](https://github.com/Yisaer)
    - Fix the issue that query plan operators might be missing in slow logs [#41458](https://github.com/pingcap/tidb/issues/41458) @[time-and-fate](https://github.com/time-and-fate)
    - Fix the issue that incorrect results might be returned when TopN operators with virtual columns are mistakenly pushing down to TiKV or TiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - Fix the issue of inconsistent data when adding indexes [#40698](https://github.com/pingcap/tidb/issues/40698) [#40730](https://github.com/pingcap/tidb/issues/40730) [#41459](https://github.com/pingcap/tidb/issues/41459) [#40464](https://github.com/pingcap/tidb/issues/40464) [#40217](https://github.com/pingcap/tidb/issues/40217) @[tangenta](https://github.com/tangenta)
    - Fix the issue of getting the `Pessimistic lock not found` error when adding indexes [#41515](https://github.com/pingcap/tidb/issues/41515) @[tangenta](https://github.com/tangenta)
    - Fix the issue of misreported duplicate key errors when adding unique indexes [#41630](https://github.com/pingcap/tidb/issues/41630) @[tangenta](https://github.com/tangenta)
    - Fix the issue of performance degradation when using `paging` in TiDB [#40741](https://github.com/pingcap/tidb/issues/40741) @[solotzg](https://github.com/solotzg)

+ TiKV

    - Fix the issue that Resolved TS causes higher network traffic [#14092](https://github.com/tikv/tikv/issues/14092) @[overvenus](https://github.com/overvenus)
    - Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [#14038](https://github.com/tikv/tikv/issues/14038) @[MyonKeminta](https://github.com/MyonKeminta)
    - Fix an error that occurs when casting the `const Enum` type to other types [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - Fix the issue that the paging in a cop task is inaccurate [#14254](https://github.com/tikv/tikv/issues/14254)  @[you06](https://github.com/you06)
    - Fix the issue that the `scan_detail` field is inaccurate in `batch_cop` mode [#14109](https://github.com/tikv/tikv/issues/14109) @[you06](https://github.com/you06)
    - Fix a potential error in the Raft Engine that might cause TiKV to detect Raft data corruption and fail to restart [#14338](https://github.com/tikv/tikv/issues/14338) @[tonyxuqqi](https://github.com/tonyxuqqi)

+ PD

    - Fix the issue that the execution `replace-down-peer` slows down under certain conditions [#5788](https://github.com/tikv/pd/issues/5788) @[HundunDM](https://github.com/HunDunDM)
    - Fix the issue that PD might unexpectedly add multiple Learners to a Region [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - Fix the issue that the Region Scatter task generates redundant replicas unexpectedly [#5909](https://github.com/tikv/pd/issues/5909) @[HundunDM](https://github.com/HunDunDM)
    - Fix the PD OOM issue that occurs when the calls of `ReportMinResolvedTS` are too frequent [#5965](https://github.com/tikv/pd/issues/5965) @[HundunDM](https://github.com/HunDunDM)
    - Fix the issue that the Region Scatter might cause uneven distribution of leader [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)

+ TiFlash

    - Fix the issue that semi-joins use excessive memory when calculating Cartesian products [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that TiFlash log search is too slow [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - Fix the issue that TiFlash cannot start because files are mistakenly deleted after repeated restarts [#6486](https://github.com/pingcap/tiflash/issues/6486) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash might report an error when performing a query after adding a new column [#6726](https://github.com/pingcap/tiflash/issues/6726) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that TiFlash does not support IPv6 configuration [#6734](https://github.com/pingcap/tiflash/issues/6734) @[ywqzzy](https://github.com/ywqzzy)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that the connection failure between PD and tidb-server causes PITR backup progress not to advance [#41082](https://github.com/pingcap/tidb/issues/41082) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that TiKV cannot listen to PITR tasks due to the connection failure between PD and TiKV [#14159](https://github.com/tikv/tikv/issues/14159) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that PITR does not support configuration changes for PD clusters [#14165](https://github.com/tikv/tikv/issues/14165) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the PITR feature does not support CA-bundles [#38775](https://github.com/pingcap/tidb/issues/38775) @[3pointer](https://github.com/3pointer)
        - Fix the issue that when a PITR backup task is deleted, the residual backup data causes data inconsistency in new tasks [#40403](https://github.com/pingcap/tidb/issues/40403) @[joccau](https://github.com/joccau)
        - Fix the issue that causes panic when BR parses the `backupmeta` file [#40878](https://github.com/pingcap/tidb/issues/40878) @[MoCuishle28](https://github.com/MoCuishle28)
        - Fix the issue that restore is interrupted due to failure in getting the Region size [#36053](https://github.com/pingcap/tidb/issues/36053) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that the frequency of `resolve lock` is too high when there is no PITR backup task in the TiDB cluster [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - Fix the issue that restoring data to a cluster on which the log backup is running causes the log backup file unable to be restored [#40797](https://github.com/pingcap/tidb/issues/40797) @[Leavrth](https://github.com/Leavrth)
        - Fix the panic issue that occurs when attempting to resume backup from a checkpoint after a full backup failure [#40704](https://github.com/pingcap/tidb/issues/40704) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that PITR errors are overwritten [#40576](https://github.com/pingcap/tidb/issues/40576)@[Leavrth](https://github.com/Leavrth)
        - Fix the issue that checkpoints do not advance in PITR backup tasks when the advance owner and gc owner are different [#41806](https://github.com/pingcap/tidb/issues/41806) @[joccau](https://github.com/joccau)

    + TiCDC

        - Fix the issue that changefeed might get stuck in special scenarios such as when scaling in or scaling out TiKV or TiCDC nodes [#8174](https://github.com/pingcap/tiflow/issues/8174) @[hicqu](https://github.com/hicqu)
        - Fix the issue that precheck is not performed on the storage path of redo log [#6335](https://github.com/pingcap/tiflow/issues/6335) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue of insufficient duration that redo log can tolerate for S3 storage failure [#8089](https://github.com/pingcap/tiflow/issues/8089)  @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that `transaction_atomicity` and `protocol` cannot be updated via the configuration file [#7935](https://github.com/pingcap/tiflow/issues/7935) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the checkpoint cannot advance when TiCDC replicates an excessively large number of tables [#8004](https://github.com/pingcap/tiflow/issues/8004) @[overvenus](https://github.com/overvenus)
        - Fix the issue that applying redo log might cause OOM when the replication lag is excessively high [#8085](https://github.com/pingcap/tiflow/issues/8085) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that the performance degrades when redo log is enabled to write meta [#8074](https://github.com/pingcap/tiflow/issues/8074) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix a bug that the context deadline is exceeded when TiCDC replicates data without splitting large transactions [#7982](https://github.com/pingcap/tiflow/issues/7982) @[hi-rustin](https://github.com/hi-rustin)
        - Fix the issue that pausing a changefeed when PD is abnormal results in incorrect status [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)
        - Fix the data inconsistency that occurs when replicating data to a TiDB or MySQL sink and when `CHARACTER SET` is specified on the column that has the non-null unique index without a primary key [#8420](https://github.com/pingcap/tiflow/issues/8420) @[asddongmen](https://github.com/asddongmen)
        - Fix the panic issue in table scheduling and blackhole sink [#8024](https://github.com/pingcap/tiflow/issues/8024) [#8142](https://github.com/pingcap/tiflow/issues/8142) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - Fix the issue that the `binlog-schema delete` command fails to execute [#7373](https://github.com/pingcap/tiflow/issues/7373) @[liumengya94](https://github.com/liumengya94)
        - Fix the issue that the checkpoint does not advance when the last binlog is a skipped DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @[D3Hunter](https://github.com/D3Hunter)
        - Fix a bug that when the expression filters of both "update" and "non-update" types are specified in one table, all `UPDATE` statements are skipped [#7831](https://github.com/pingcap/tiflow/issues/7831) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - Fix the issue that TiDB Lightning prechecks cannot find dirty data left by previously failed imports [#39477](https://github.com/pingcap/tidb/issues/39477) @[dsdashun](https://github.com/dsdashun)
        - Fix the issue that TiDB Lightning panics in the split-region phase [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - Fix the issue that the conflict resolution logic (`duplicate-resolution`) might lead to inconsistent checksums [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - Fix the issue that TiDB Lightning might incorrectly skip conflict resolution when all but the last TiDB Lightning instance encounters a local duplicate record during a parallel import [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
        - Fix the issue that when importing data in Local Backend mode, the target columns do not automatically generate data if the compound primary key of the imported target table has an `auto_random` column and no value for the column is specified in the source data [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
