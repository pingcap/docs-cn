---
title: TiDB 5.1.5 Release Notes
---

# TiDB 5.1.5 Release Notes

发版日期：2022 年 12 月 28 日

TiDB 版本：5.1.5

试用链接：[Quick start](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v5.1.5#version-list)

## 兼容性变更

## 提升改进

+ TiDB

+ PD

    (dup: release-6.1.0.md > Improvements> PD)- Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)

+ TiFlash

## Bug 修复

+ TiDB
    
    <!--executor owner: zanmato1984-->  
    
    (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that the window function causes TiDB to panic instead of reporting an error [#30326](https://github.com/pingcap/tidb/issues/30326)
    (dup: release-5.4.3.md > Bug fixes> TiDB)- Fix the wrong result that occurs when enabling dynamic mode in partitioned tables for TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix wrong results of `GREATEST` and `LEAST` when passing in unsigned `BIGINT` arguments [#30101](https://github.com/pingcap/tidb/issues/30101)
    (dup: release-5.4.1.md > Bug Fixes> TiDB)- Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue that the result of `concat(ifnull(time(3)))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    (dup: release-5.0.6.md > Bug fixes> TiDB)- Fix the issue that the SQL statements that contain `cast(integer as char) union string` return wrong results [#29513](https://github.com/pingcap/tidb/issues/29513)
    (dup: release-6.1.1.md > Bug fixes> TiDB)- Fix the issue that `INL_HASH_JOIN` might hang when used with `LIMIT` [#35638](https://github.com/pingcap/tidb/issues/35638) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复当有 Region 返回空数据时 `ANY_VALUE` 结果不正确的问题 [#30923](https://github.com/pingcap/tidb/issues/30923)
    (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix wrong results of index join caused by an innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494)

    <!--planner owner: winoros-->
    
        (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that a SQL operation is canceled when its JSON type column joins its `CHAR` type column [#29401](https://github.com/pingcap/tidb/issues/29401)

    <!--sql-infra and tidb owner: bb7133-->

    (dup: release-5.2.4.md > Bug fixes> TiDB)- Fix the issue that the background HTTP service of TiDB might not exit successfully and makes the cluster in an abnormal state [#30571](https://github.com/pingcap/tidb/issues/30571)
    (dup: release-5.4.0.md > Bug fixes> TiDB)- Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that `KILL TIDB` cannot take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031)
    - Fix the bug that setting any session variable will make `tidb_snapshot` unwork. [#35515](https://github.com/pingcap/tidb/issues/35515)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that the Region cache is not cleaned up in time when the Region is merged [#37141](https://github.com/pingcap/tidb/issues/37141)
    - 修复因为 kv client 中 connection data race 导致的 panic [33773](https://github.com/pingcap/tidb/issues/33773)
    (dup: release-6.1.1.md > Bug fixes> TiDB)- Fix the issue that when TiDB Binlog is enabled, executing the `ALTER SEQUENCE` statement might cause a wrong metadata version and cause Drainer to exit [#36276](https://github.com/pingcap/tidb/issues/36276) @[AilinKid](https://github.com/AilinKid)
    (dup: release-5.3.2.md > Bug Fixes> TiDB)- Fix the bug that TiDB may panic when querying statement summary tables [#35340](https://github.com/pingcap/tidb/issues/35340)
    - None [#30402](https://github.com/pingcap/tidb/issues/30402) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30587](https://github.com/pingcap/tidb/issues/30587) @[ti-srebot](https://github.com/ti-srebot)
    - None [#37414](https://github.com/pingcap/tidb/issues/37414) @[ti-srebot](https://github.com/ti-srebot)
    (dup: release-5.4.1.md > Bug Fixes> TiDB)- Fix the issue that TiDB gets the wrong result when using TiFlash to scan tables with empty range although TiFlash does not support reading tables with empty range yet [#33083](https://github.com/pingcap/tidb/issues/33083)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that the `avg()` function returns `ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.` when queried from TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that `ERROR 1105 (HY000): close of nil channel` is returned when using `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)
    - None [#30923](https://github.com/pingcap/tidb/issues/30923) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#37932](https://github.com/pingcap/tidb/issues/37932) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#30923](https://github.com/pingcap/tidb/issues/30923) @[ti-srebot](https://github.com/ti-srebot)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that `ERROR 1105 (HY000): close of nil channel` is returned when using `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that TiKV and TiFlash return different results when querying logical operations [#37258](https://github.com/pingcap/tidb/issues/37258)
    (dup: release-5.3.4.md > Bug fixes> TiDB)- Fix the issue that the `EXECUTE` statement might throw an unexpected error in specific scenarios [#37187](https://github.com/pingcap/tidb/issues/37187)
    - None [#27125](https://github.com/pingcap/tidb/issues/27125) @[ti-srebot](https://github.com/ti-srebot)
    (dup: release-5.4.2.md > Bug Fixes> TiDB)- Fix the planner wrong behaviors that occur when `tidb_opt_agg_push_down` and `tidb_enforce_mpp` are enabled [#34465](https://github.com/pingcap/tidb/issues/34465)
    (dup: release-6.1.1.md > Bug fixes> TiDB)- Fix a bug that TiDB might send coprocessor requests when executing the `SHOW COLUMNS` statement [#36496](https://github.com/pingcap/tidb/issues/36496) @[tangenta](https://github.com/tangenta)
    - Add warnings for `lock tables` and `unlock tables` when `enable-table-lock` flag is not enabled [#28967](https://github.com/pingcap/tidb/issues/28967)
    - Fix the issue that range partitions allow multiple `MAXVALUE` partitions [#36329](https://github.com/pingcap/tidb/issues/36329)

+ TiKV

    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the issue of time parsing error that occurs when the `DATETIME` values contain a fraction and `Z` [#12739](https://github.com/tikv/tikv/issues/12739)
    (dup: release-5.4.1.md > Bug Fixes> TiKV)- Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    (dup: release-6.1.1.md > Bug fixes> TiKV)- Fix a bug that Regions might be overlapped if Raftstore is busy [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    (dup: release-5.2.4.md > Bug fixes> TiKV)- Fix the TiKV panic issue that occurs when applying snapshot is aborted [#11618](https://github.com/tikv/tikv/issues/11618)
    (dup: release-5.4.1.md > Bug Fixes> TiKV)- Fix a bug that TiKV might panic if it has been running for 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    (dup: release-6.1.1.md > Bug fixes> TiKV)- Fix the panic issue that might occur when the source peer catches up logs by snapshot in the Region merge process [#12663](https://github.com/tikv/tikv/issues/12663) @[BusyJay](https://github.com/BusyJay)
    (dup: release-6.1.1.md > Bug fixes> TiKV)- Fix the issue that TiKV panics when performing type conversion for an empty string [#12673](https://github.com/tikv/tikv/issues/12673) @[wshwsh12](https://github.com/wshwsh12)
    (dup: release-5.4.1.md > Bug Fixes> TiKV)- Fix a bug that stale messages cause TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    (dup: release-6.1.1.md > Bug fixes> TiKV)- Fix the panic issue that might occur when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825) @[BusyJay](https://github.com/BusyJay)
    (dup: release-5.4.1.md > Bug Fixes> TiKV)- Fix the TiKV panic issue that occurs when the target peer is replaced with the peer that is destroyed without being initialized when merging a Region [#12048](https://github.com/tikv/tikv/issues/12048)
    (dup: release-6.1.0.md > Bug fixes> TiKV)- Fix the issue that TiKV reports the `invalid store ID 0` error when using Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)
    (dup: release-5.3.2.md > Bug Fixes> TiKV)- Fix the possible duplicate commit records in pessimistic transactions when async commit is enabled [#12615](https://github.com/tikv/tikv/issues/12615)
    (dup: release-5.4.3.md > Improvements> TiKV)- Support configuring the `unreachable_backoff` item to avoid Raftstore broadcasting too many messages after one peer becomes unreachable [#13054](https://github.com/tikv/tikv/issues/13054)

    <!--transaction owner:cfzjywxk -->

    (dup: release-5.4.1.md > Bug Fixes> TiKV)- Fix the issue that successfully committed optimistic transactions may report the `Write Conflict` error when the network is poor [#34066](https://github.com/pingcap/tidb/issues/34066)
    (dup: release-6.1.1.md > Bug fixes> TiKV)- Fix the wrong expression of `Unified Read Pool CPU` in dashboard [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)

+ PD

    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the issue that a removed tombstone store appears again after the PD leader transfer ​​[#4941](https://github.com/tikv/pd/issues/4941)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the issue that scheduling cannot start immediately after the PD leader transfer [#4769](https://github.com/tikv/pd/issues/4769)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix the wrong status code of `not leader` [#4797](https://github.com/tikv/pd/issues/4797)
    (dup: release-6.1.0.md > Improvements> PD)- Disable compiling swagger server by default [#4932](https://github.com/tikv/pd/issues/4932)
    (dup: release-5.3.4.md > Bug fixes> PD)- Fix the issue that PD cannot correctly handle dashboard proxy requests [#5321](https://github.com/tikv/pd/issues/5321)
    (dup: release-6.1.0.md > Bug fixes> PD)- Fix a bug of TSO fallback in some corner cases [#4884](https://github.com/tikv/pd/issues/4884)
    (dup: release-5.3.4.md > Bug fixes> PD)- Fix the issue that the TiFlash learner replica might not be created in specific scenarios [#5401](https://github.com/tikv/pd/issues/5401)
    (dup: release-5.4.1.md > Bug Fixes> PD)- Fix the issue that the label distribution has residual labels in the metrics [#4825](https://github.com/tikv/pd/issues/4825)
    - (dup: release-6.1.0.md > Bug fixes> PD)- Fix the issue that region checker always occupy one cpu in some corner cases.[#4920](https://github.com/tikv/pd/issues/4920) 
    (dup: release-5.4.1.md > Bug Fixes> PD)- Fix the issue that when there exists a Store with large capacity (2T for example), fully allocated small Stores cannot be detected, which results in no balance operator being generated [#4805](https://github.com/tikv/pd/issues/4805)
    (dup: release-5.3.2.md > Bug Fixes> PD)- Fix the issue that schedulers do not work when `SchedulerMaxWaitingOperator` is set to `1` [#4946](https://github.com/tikv/pd/issues/4946)

+ TiFlash

    <!--compute owner: zanmato1984 -->
  
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix incorrect `microsecond` when casting string to datetime [#3556](https://github.com/pingcap/tiflash/issues/3556)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the panic issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196)
    (dup: release-6.1.1.md > Bug fixes> TiFlash)- Fix a bug that TiFlash might crash due to an error in parallel aggregation [#5356](https://github.com/pingcap/tiflash/issues/5356) @[gengliqi](https://github.com/gengliqi)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the issue that a query containing `JOIN` might be hung if an error occurs [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - 修复 `OR` 函数计算结果错误的问题 [#5849](https://github.com/pingcap/tiflash/issues/5849) @[xzhangxian1008](https://github.com/xzhangxian1008)

    <!--storage owner: flowbehappy -->

    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the bug that invalid storage directory configurations lead to unexpected behaviors [#4093](https://github.com/pingcap/tiflash/issues/4093)
    (dup: release-6.1.0.md > Bug fixes> TiFlash)- Fix potential data inconsistency after a lot of INSERT and DELETE operations [#4956](https://github.com/pingcap/tiflash/issues/4956)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that data not matching any region range remains on a TiFlash node [#4414](https://github.com/pingcap/tiflash/issues/4414)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the potential query error after adding columns under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967)
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix repeated crashes caused by the `commit state jump backward` errors [#2576](https://github.com/pingcap/tiflash/issues/2576)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix potential errors when querying on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the issue that the date format identifies `'
'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101)
    - 修复 `Prepare Merge` 可能导致 raft 状态机元数据损坏从而引起 TiFlash 重启的问题 [#3435](https://github.com/pingcap/tiflash/issues/3435) @[solotzg](https://github.com/solotzg)
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix a bug that an MPP query might fail due to random gRPC keepalive timeout [#4662](https://github.com/pingcap/tiflash/issues/4662)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix a bug that MPP tasks might leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the issue that expired data is recycled slowly [#4146](https://github.com/pingcap/tiflash/issues/4146)
    (dup: release-5.4.1.md > Bug Fixes> TiFlash)- Fix the overflow that occurs when casting `FLOAT` to `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)
    (dup: release-5.3.4.md > Bug fixes> TiFlash)- Fix the issue that logical operators return wrong results when the argument type is UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)
    - None [#5849](https://github.com/pingcap/tiflash/issues/5849) @[ti-chi-bot](https://github.com/ti-chi-bot)
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix the potential `index out of bounds` error if calling `json_length` with empty string [#2705](https://github.com/pingcap/tiflash/issues/2705)
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix wrong decimal comparison results in corner cases [#4512](https://github.com/pingcap/tiflash/issues/4512)
    (dup: release-5.3.2.md > Bug Fixes> TiFlash)- Fix `TiFlash_schema_error` reported when `NOT NULL` columns are added [#4596](https://github.com/pingcap/tiflash/issues/4596)
    (dup: release-5.3.4.md > Bug fixes> TiFlash)- Fix the issue that TiFlash bootstrap fails when `0.0` is used as the default value for integers, for example, `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157)

+ Tools

    + TiDB-Binlog

        - Fix the bug that Drainer can't send request correctly to Pump when setting `compressor=gzip` [#1152](https://github.com/pingcap/tidb-binlog/issues/1152)

    + Backup & Restore (BR)

        (dup: release-5.4.0.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the issue that system tables cannot be restored because concurrently backing up system tables makes the table name fail to update [#29710](https://github.com/pingcap/tidb/issues/29710)

    + TiCDC

        (dup: release-6.1.0.md > Bug fixes> Tools> TiCDC)- Fix data loss that occurs in special incremental scanning scenarios [#5468](https://github.com/pingcap/tiflow/issues/5468)
        - fix no sorter metrics [#5690](https://github.com/pingcap/tiflow/issues/5690) @[asddongmen](https://github.com/asddongmen)
        (dup: release-6.1.0.md > Bug fixes> Tools> TiCDC)- Fix excessive memory usage by optimizing the way DDL schemas are buffered [#1386](https://github.com/pingcap/tiflow/issues/1386)
