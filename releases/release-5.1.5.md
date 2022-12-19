---
title: TiDB 5.1.5 Release Notes
---

# TiDB 5.1.5 Release Notes

发版日期：2022 年 12 月 28 日

TiDB 版本：5.1.5

试用链接：[Quick start](https://docs.pingcap.com/tidb/v5.1/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v5.1.5#version-list)

## 提升改进

+ TiDB

    - Optimize the performance of the region cache after merging many regions. [#37141](https://github.com/pingcap/tidb/issues/37141) @[sticnarf](https://github.com/sticnarf)
    - None [#36496](https://github.com/pingcap/tidb/issues/36496) @[ti-srebot](https://github.com/ti-srebot)

+ PD

    - server: disable swagger server [#4932](https://github.com/tikv/pd/issues/4932) @[ti-chi-bot](https://github.com/ti-chi-bot)

+ TiFlash

    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101) @[ti-chi-bot](https://github.com/ti-chi-bot)

## Bug 修复

+ TiDB

    - executor: fix pipelined window invalid memory address [#30326](https://github.com/pingcap/tidb/issues/30326) @[ti-srebot](https://github.com/ti-srebot)
    - Fix wrong result when enabling dynamic mode in partition table for tiflash [#37254](https://github.com/pingcap/tidb/issues/37254) @[ti-srebot](https://github.com/ti-srebot)
    - Fix wrong result of greatest/least Function. [#30101](https://github.com/pingcap/tidb/issues/30101) @[ti-srebot](https://github.com/ti-srebot)
    - executor: fix wrong result of delete multiple tables using left join [#31321](https://github.com/pingcap/tidb/issues/31321) @[ti-srebot](https://github.com/ti-srebot)
    - bugfix: concat(ifnull(time(3)) returns different results from MySQL [#29498](https://github.com/pingcap/tidb/issues/29498) @[ti-srebot](https://github.com/ti-srebot)
    - Fix wrong flen for CastAsString funtion [#29513](https://github.com/pingcap/tidb/issues/29513) @[ti-srebot](https://github.com/ti-srebot)
    - executor: fix index_lookup_hash_join hang when used with limit [#35638](https://github.com/pingcap/tidb/issues/35638) @[ti-srebot](https://github.com/ti-srebot)
    - Fix wrong `any_value` result when there are regions returning empty result [#30923](https://github.com/pingcap/tidb/issues/30923) @[ti-srebot](https://github.com/ti-srebot)
    - Fix index join bug caused by innerWorker panic [#31494](https://github.com/pingcap/tidb/issues/31494) @[ti-srebot](https://github.com/ti-srebot)
    - Fix the bug that sql got cancel if including json column joins char column. [#29401](https://github.com/pingcap/tidb/issues/29401) @[ti-srebot](https://github.com/ti-srebot)
    - Fix some connections and goroutines leak caused by not closed HTTP response body [#30571](https://github.com/pingcap/tidb/issues/30571) @[tiancaiamao](https://github.com/tiancaiamao)
    - Fix concurrent column type changes(with changing data) that cause schema and data inconsistencies. [#31048](https://github.com/pingcap/tidb/issues/31048) @[ti-srebot](https://github.com/ti-srebot)
    - fix the issue that `KILL TIDB` doesn't take effect immediately on idle connections [#24031](https://github.com/pingcap/tidb/issues/24031) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the bug that setting any session variable will make `tidb_snapshot` unwork. [#35515](https://github.com/pingcap/tidb/issues/35515) @[ti-srebot](https://github.com/ti-srebot)
    - Optimize the performance of the region cache after merging many regions. [#37141](https://github.com/pingcap/tidb/issues/37141) @[sticnarf](https://github.com/sticnarf)
    - Fix the data race issue of the connection array. [#33773](https://github.com/pingcap/tidb/issues/33773) @[ystaticy](https://github.com/ystaticy)
    - ddl: fix alter sequence will generate schemaVer=0 when alter options are the same as the old [#36276](https://github.com/pingcap/tidb/issues/36276) @[ti-srebot](https://github.com/ti-srebot)
    - None [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#35340](https://github.com/pingcap/tidb/issues/35340) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30402](https://github.com/pingcap/tidb/issues/30402) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30587](https://github.com/pingcap/tidb/issues/30587) @[ti-srebot](https://github.com/ti-srebot)
    - None [#37414](https://github.com/pingcap/tidb/issues/37414) @[ti-srebot](https://github.com/ti-srebot)
    - None [#33083](https://github.com/pingcap/tidb/issues/33083) @[ti-srebot](https://github.com/ti-srebot)
    - None [#29952](https://github.com/pingcap/tidb/issues/29952) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30289](https://github.com/pingcap/tidb/issues/30289) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30923](https://github.com/pingcap/tidb/issues/30923) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#37932](https://github.com/pingcap/tidb/issues/37932) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#30923](https://github.com/pingcap/tidb/issues/30923) @[ti-srebot](https://github.com/ti-srebot)
    - None [#30289](https://github.com/pingcap/tidb/issues/30289) @[ti-srebot](https://github.com/ti-srebot)
    - None [#37258](https://github.com/pingcap/tidb/issues/37258) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#37187](https://github.com/pingcap/tidb/issues/37187) @[fzzf678](https://github.com/fzzf678)
    - None [#27125](https://github.com/pingcap/tidb/issues/27125) @[ti-srebot](https://github.com/ti-srebot)
    - None [#34465](https://github.com/pingcap/tidb/issues/34465) @[ti-srebot](https://github.com/ti-srebot)
    - None [#36496](https://github.com/pingcap/tidb/issues/36496) @[ti-srebot](https://github.com/ti-srebot)
    - None [#28967](https://github.com/pingcap/tidb/issues/28967) @[ti-srebot](https://github.com/ti-srebot)
    - None [#36329](https://github.com/pingcap/tidb/issues/36329) @[ti-srebot](https://github.com/ti-srebot)

+ TiKV

    - Fix a wrong check in datetime when the datetime has a fraction and 'Z' [#12739](https://github.com/tikv/tikv/issues/12739) @[ti-srebot](https://github.com/ti-srebot)
    - Fix potential linearizability violation in replica reads. [#12109](https://github.com/tikv/tikv/issues/12109) @[ti-srebot](https://github.com/ti-srebot)
    - Fix a bug that regions may be overlapped if raftstore is too busy [#13160](https://github.com/tikv/tikv/issues/13160) @[ti-srebot](https://github.com/ti-srebot)
    - Fix  #11618.  Skip on_raft_base_tick when snapshot is aborted to avoid a potential panic. [#11618](https://github.com/tikv/tikv/issues/11618) @[YuJuncen](https://github.com/YuJuncen)
    - Fixes the bug that TiKV keep running over 2 years may panic. [#11940](https://github.com/tikv/tikv/issues/11940) @[ti-srebot](https://github.com/ti-srebot)
    - Fix possible panic when source peer catch up logs by snapshot in merge [#12663](https://github.com/tikv/tikv/issues/12663) @[YangKeao](https://github.com/YangKeao)
    - Fix tikv crash when conv empty string [#12673](https://github.com/tikv/tikv/issues/12673) @[YuJuncen](https://github.com/YuJuncen)
    - Fix stale message cause panic [#12023](https://github.com/tikv/tikv/issues/12023) @[ti-srebot](https://github.com/ti-srebot)
    - Fix potential panic when a peer is being split and destroyed at the same time [#12825](https://github.com/tikv/tikv/issues/12825) @[v01dstar](https://github.com/v01dstar)
    - fix panic when target peer is replaced with an destroyed uninitialized peer during merge [#12048](https://github.com/tikv/tikv/issues/12048) @[ti-srebot](https://github.com/ti-srebot)
    - Fix a bug that sometimes generates a message with zero store id when doing follower read [#12478](https://github.com/tikv/tikv/issues/12478) @[v01dstar](https://github.com/v01dstar)
    - Fix possible duplicate commit record in async-commit pessimistic transactions. [#12615](https://github.com/tikv/tikv/issues/12615) @[ti-srebot](https://github.com/ti-srebot)
    - Add a new option to make unreachable_backoff of raftstore configurable. [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    - Fixes that successfully committed optimistic transactions may report false WriteConflict on network errors. [#34066](https://github.com/pingcap/tidb/issues/34066) @[ti-srebot](https://github.com/ti-srebot)
    - None [#13086](https://github.com/tikv/tikv/issues/13086) @[ti-srebot](https://github.com/ti-srebot)
    - None [#13147](https://github.com/tikv/tikv/issues/13147) @[ti-srebot](https://github.com/ti-srebot)

+ PD

    - Fix the issue that the removed tombstone store shows again after transferring the PD leader [#4941](https://github.com/tikv/pd/issues/4941) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that scheduling cannot immediately start after PD leader transfers [#4769](https://github.com/tikv/pd/issues/4769) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that the status code of `not leader` is sometimes wrong [#4797](https://github.com/tikv/pd/issues/4797) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - server: disable swagger server [#4932](https://github.com/tikv/pd/issues/4932) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix a bug that could not handle dashboard proxy requests correctly. [#5321](https://github.com/tikv/pd/issues/5321) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the corner case that may cause TSO fallback. [#4884](https://github.com/tikv/pd/issues/4884) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fixed the bug where the Learner Peer of TiFlash Replica might not be created. [#5401](https://github.com/tikv/pd/issues/5401) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that the label distribution has residual labels [#4825](https://github.com/tikv/pd/issues/4825) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#4920](https://github.com/tikv/pd/issues/4920) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None. [#4805](https://github.com/tikv/pd/issues/4805) @[rleungx](https://github.com/rleungx)
    - None. [#4946](https://github.com/tikv/pd/issues/4946) @[ti-chi-bot](https://github.com/ti-chi-bot)

+ TiFlash

    - Fix str_to_date() function incorrectly handles leading zeros when parsing Microseconds [#3556](https://github.com/pingcap/tiflash/issues/3556) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the potential crash issue that occurs when TLS is enabled [#4196](https://github.com/pingcap/tiflash/issues/4196) @[LittleFall](https://github.com/LittleFall)
    - Fix a panic issue in parallel aggregation when an exception is thrown. [#5356](https://github.com/pingcap/tiflash/issues/5356) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the issue that a query containing `JOIN` could be hung if an error was encountered [#4195](https://github.com/pingcap/tiflash/issues/4195) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the bug that invalid storage dir configurations lead to unexpected behavior [#4093](https://github.com/pingcap/tiflash/issues/4093) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix potential wrong result after a lot of insert and delete operations [#4956](https://github.com/pingcap/tiflash/issues/4956) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Avoid leaving data on tiflash node which doesn't corresponding to any region range [#4414](https://github.com/pingcap/tiflash/issues/4414) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix potential query error after add column under heavy read workload [#3967](https://github.com/pingcap/tiflash/issues/3967) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#2576](https://github.com/pingcap/tiflash/issues/2576) @[solotzg](https://github.com/solotzg)
    - Fix potential query error when select on a table with many delete operations [#4747](https://github.com/pingcap/tiflash/issues/4747) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - fix date format identifies '\n' as invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix cast datetime to decimal wrong result bug [#4151](https://github.com/pingcap/tiflash/issues/4151) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the bug that some exceptions are not handled properly [#4101](https://github.com/pingcap/tiflash/issues/4101) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix the metadata corruption issue when `Prepare Merge` is triggered after a new election is finished but the isolated peer is not informed [#3435](https://github.com/pingcap/tiflash/issues/3435) @[solotzg](https://github.com/solotzg)
    - Fix bug that TiFlash query will meet keepalive timeout error randomly. [#4662](https://github.com/pingcap/tiflash/issues/4662) @[windtalker](https://github.com/windtalker)
    - fix error result for function `in` [#4016](https://github.com/pingcap/tiflash/issues/4016) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix a bug that MPP tasks may leak threads forever [#4238](https://github.com/pingcap/tiflash/issues/4238) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - fix the problem that expired data was not recycled timely due to slow gc speed [#4146](https://github.com/pingcap/tiflash/issues/4146) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - Fix wrong result of cast(float as decimal) when overflow happens [#3998](https://github.com/pingcap/tiflash/issues/3998) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#6127](https://github.com/pingcap/tiflash/issues/6127) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#5849](https://github.com/pingcap/tiflash/issues/5849) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#2705](https://github.com/pingcap/tiflash/issues/2705) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#4512](https://github.com/pingcap/tiflash/issues/4512) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#4596](https://github.com/pingcap/tiflash/issues/4596) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - [#4091](https://github.com/pingcap/tiflash/issues/4091) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#5979](https://github.com/pingcap/tiflash/issues/5979) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#4091](https://github.com/pingcap/tiflash/issues/4091) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - [#4091](https://github.com/pingcap/tiflash/issues/4091) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#5385](https://github.com/pingcap/tiflash/issues/5385) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#4405](https://github.com/pingcap/tiflash/issues/4405) @[ti-chi-bot](https://github.com/ti-chi-bot)
    - None [#3157](https://github.com/pingcap/tiflash/issues/3157) @[ti-chi-bot](https://github.com/ti-chi-bot)

+ Tools

    + Backup & Restore (BR)

        - None [#29710](https://github.com/pingcap/tidb/issues/29710) @[joccau](https://github.com/joccau)

    + TiCDC

        - Fix data loss when upstream transaction conflicts during cdc reconnection [#5468](https://github.com/pingcap/tiflow/issues/5468) @[ti-chi-bot](https://github.com/ti-chi-bot)
        - fix no sorter metrics [#5690](https://github.com/pingcap/tiflow/issues/5690) @[asddongmen](https://github.com/asddongmen)
        - None [#1386](https://github.com/pingcap/tiflow/issues/1386) @[hicqu](https://github.com/hicqu)