---
title: TiDB 7.5.1 Release Notes
summary: 了解 TiDB 7.5.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.1 Release Notes

发版日期：2024 年 x 月 x 日

TiDB 版本：v7.5.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.1#version-list)

## 兼容性变更

<!-- tw:@Oreoxmt (2) -->

- 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)
- (dup): release-6.5.8.md > Compatibility changes - Introduce the TiKV configuration item [`gc.num-threads`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#num-threads-new-in-v658) to set the number of GC threads when `enable-compaction-filter` is `false`  [#16101](https://github.com/tikv/tikv/issues/16101) @[tonyxuqqi](https://github.com/tonyxuqqi)
- TiCDC Changefeed 新增以下配置项：
    - [`compression`](/ticdc/ticdc-changefeed-config.md)：你可以设置 redo log 文件的压缩行为 [#10176](https://github.com/pingcap/tiflow/issues/10176) @[sdojjy](https://github.com/sdojjy)
    - [`sink.cloud-storage-config`](/ticdc/ticdc-changefeed-config.md)：你可以设置同步数据到对象存储时自动清理历史数据的功能 [#10109](https://github.com/pingcap/tiflow/issues/10109) @[CharlesCheung96](https://github.com/CharlesCheung96)

## 改进提升

+ TiDB
    <!-- tw:@hfxsd (1) -->
    - 在 ddl schema reload 中使用 kv timeout 特性降低 meta region leader 读不可用对于集群影响 [#48124](https://github.com/pingcap/tidb/issues/48124) @[cfzjywxk](https://github.com/cfzjywxk)
    - (dup): release-7.6.0.md > # Observability * Enhance observability related to resource control [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch)

        随着越来越多用户利用资源组对业务应用进行隔离，资源管控提供了更丰富的基于资源组的数据，协助你观测资源组负载、资源组设置，确保出现问题时能够快速发现并精准诊断。其中包括：

        * [慢查询日志](/identify-slow-queries.md)增加资源组名称、RU 消耗、以及等待资源耗时。
        * [Statement Summary Tables](/statement-summary-tables.md) 增加资源组名称、RU 消耗、以及等待资源耗时。
        * 在变量 [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-从-v4014-版本开始引入) 中增加了 SQL 的 [RU](/tidb-resource-control.md#什么是-request-unit-ru) 消耗信息 `ru_consumption`，你可以利用此变量获取会话中上一条语句的资源消耗。
        * 增加基于[资源组的数据库指标](/grafana-resource-control-dashboard.md)：QPS/TPS、执行时间 (P999/P99/P95)、失败次数、连接数。

    - (dup): release-7.6.0.md > Improvements> TiDB - Modify the `CANCEL IMPORT JOB` statement to a synchronous statement [#48736](https://github.com/pingcap/tidb/issues/48736) @[D3Hunter](https://github.com/D3Hunter)
    - (dup): release-7.1.3.md > Improvements> TiDB - Support the [`FLASHBACK CLUSTER TO TSO`](https://docs.pingcap.com/tidb/v7.1/sql-statement-flashback-cluster) syntax [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger)
    - (dup): release-7.6.0.md > Improvements> TiDB - Optimize the TiDB implementation when handling some type conversions and fix related issues [#47945](https://github.com/pingcap/tidb/issues/47945) [#47864](https://github.com/pingcap/tidb/issues/47864) [#47829](https://github.com/pingcap/tidb/issues/47829) [#47816](https://github.com/pingcap/tidb/issues/47816) @[YangKeao](https://github.com/YangKeao) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.6.0.md > Improvements> TiDB - When a non-binary collation is set and the query includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) [#49138](https://github.com/pingcap/tidb/issues/49138) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.7.md > Improvements> TiDB - Enhance the ability to convert `OUTER JOIN` to `INNER JOIN` in specific scenarios [#49616](https://github.com/pingcap/tidb/issues/49616) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.6.0.md > Improvements> TiDB - Support multiple accelerated `ADD INDEX` DDL tasks to be queued for execution, instead of falling back to normal `ADD INDEX` tasks [#47758](https://github.com/pingcap/tidb/issues/47758) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.6.0.md > Improvements> TiDB - Improve the speed of adding indexes to empty tables [#49682](https://github.com/pingcap/tidb/issues/49682) @[zimulala](https://github.com/zimulala)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ TiFlash
    <!-- tw:@hfxsd (1) -->
    - 改进 RU 计算，使得 RU 值更稳定 [#8391](https://github.com/pingcap/tiflash/issues/8391) @[guo-shaoge(https://github.com/guo-shaoge)
    - (dup): release-6.5.7.md > Improvements> TiFlash - Reduce the impact of disk performance jitter on read latency [#8583](https://github.com/pingcap/tiflash/issues/8583) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.8.md > Improvements> TiFlash - Reduce the impact of background GC tasks on read and write task latency [#8650](https://github.com/pingcap/tiflash/issues/8650) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)
        <!-- tw:@hfxsd (1) -->
        - 使用更优的算法, 提升 restore 过程中 sst 文件合并的速度 [#50613](https://github.com/pingcap/tidb/issues/50613) @[Leavrth](https://github.com/Leavrth)
        - 在 restore 过程中批量创建 database [#50767](https://github.com/pingcap/tidb/issues/50767) @[Leavrth](https://github.com/Leavrth)
        - 在 restore 过程中批量 ingest sst 文件 [#16267](https://github.com/tikv/tikv/issues/16267) @[3pointer](https://github.com/3pointer)
        - 在日志备份中, 在日志和 metrics 中, 增加打印拖慢 global checkpoint 推进的最慢的 region 的信息 [#51046](https://github.com/pingcap/tidb/issues/51046) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.7.md > Improvements> Tools> Backup & Restore (BR) - Improve the table creation performance of the `RESTORE` statement in scenarios with large datasets [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.6.md > Improvements> Tools> Backup & Restore (BR) - BR can pause Region merging by setting the `merge-schedule-limit` configuration to `0` [#7148](https://github.com/tikv/pd/issues/7148) @[BornChanger](https://github.com/3pointer)
        - (dup): release-7.6.0.md > Improvements> Tools> Backup & Restore (BR) - Refactor the BR exception handling mechanism to increase tolerance for unknown errors [#47656](https://github.com/pingcap/tidb/issues/47656) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.8.md > Improvements> Tools> TiCDC - Support [querying the downstream synchronization status of a changefeed](https://docs.pingcap.com/tidb/v6.5/ticdc-open-api-v2#query-whether-a-specific-replication-task-is-completed), which helps you determine whether the upstream data changes received by TiCDC have been synchronized to the downstream system completely [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan)
        - (dup): release-7.1.3.md > Improvements> Tools> TiCDC - Improve the performance of TiCDC replicating data to object storage by increasing parallelism [#10098](https://github.com/pingcap/tiflow/issues/10098) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.8.md > Improvements> Tools> TiDB Lightning - Improve the performance of `ALTER TABLE` when importing a large number of small tables [#50105](https://github.com/pingcap/tidb/issues/50105) @[D3Hunter](https://github.com/D3Hunter)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB
    <!-- tw:@qiancai (8) -->
    - 修复设置全局变量 `tidb_service_scope` 后配置失效的问题 [#49245](https://github.com/pingcap/tidb/issues/49245) @[ywqzzy](https://github.com/ywqzzy)
    - 修复开启压缩时，通讯协议无法处理大于等于 16M 的报文 [#47157](https://github.com/pingcap/tidb/issues/47157) [#47161](https://github.com/pingcap/tidb/issues/47161) @[dveeden](https://github.com/dveeden)
    - 修复 `approx_percentile` 函数可能导致 TiDB panic 的问题 [#40463](https://github.com/pingcap/tidb/issues/40463) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 TiDB 在字符串函数参数为 `null` 常量时可能会隐式插入 `from_binary` 函数导致无法下推给 TiFlash 的问题 [#49526](https://github.com/pingcap/tidb/issues/49526) @[YangKeao](https://github.com/YangKeao)
    - 修复 goroutine 在 hash join spill 失败时可能会泄露的问题 [#50841](https://github.com/pingcap/tidb/issues/50841) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 bit 类型在参与一些函数计算时可能会因为 decode 失败导致 query 出错的问题 [#49566](https://github.com/pingcap/tidb/issues/49566), [#50850](https://github.com/pingcap/tidb/issues/50850), [#50855](https://github.com/pingcap/tidb/issues/50855) @[jiyfhust](https://github.com/jiyfhust)
    - 修复 CTE query 内存超限时可能会导致 goroutine 泄露的问题 [#50337](https://github.com/pingcap/tidb/issues/50337) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在 TiFlash 延迟物化在有关联列时结果可能出错的问题 [#49241](https://github.com/pingcap/tidb/issues/49241), [#51204](https://github.com/pingcap/tidb/issues/51204) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that high CPU usage of TiDB occurs due to long-term memory pressure caused by `tidb_server_memory_limit` [#48741](https://github.com/pingcap/tidb/issues/48741) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that the completion times of two DDL tasks with dependencies are incorrectly sequenced [#49498](https://github.com/pingcap/tidb/issues/49498) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that illegal optimizer hints might cause valid hints to be ineffective [#49308](https://github.com/pingcap/tidb/issues/49308) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that DDL statements with the `CHECK` constraint are stuck [#47632](https://github.com/pingcap/tidb/issues/47632) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that the behavior of the `ENFORCED` option in the `CHECK` constraint is inconsistent with MySQL 8.0 [#47567](https://github.com/pingcap/tidb/issues/47567) [#47631](https://github.com/pingcap/tidb/issues/47631) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that CTE queries might report an error `type assertion for CTEStorageMap failed` during the retry process [#46522](https://github.com/pingcap/tidb/issues/46522) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that the `DELETE` and `UPDATE` statements using index lookup might report an error when `tidb_multi_statement_mode` mode is enabled [#50012](https://github.com/pingcap/tidb/issues/50012) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that `UPDATE` or `DELETE` statements containing `WITH RECURSIVE` CTEs might produce incorrect results [#48969](https://github.com/pingcap/tidb/issues/48969) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that the optimizer incorrectly converts TiFlash selection path to the DUAL table in specific scenarios [#49285](https://github.com/pingcap/tidb/issues/49285) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that the same query plan has different `PLAN_DIGEST` values in some cases [#47634](https://github.com/pingcap/tidb/issues/47634) @[King-Dylan](https://github.com/King-Dylan)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that after the time window for automatic statistics updates is configured, statistics might still be updated outside that time window [#49552](https://github.com/pingcap/tidb/issues/49552) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the issue that the query result is incorrect when an `ENUM` type column is used as the join key [#48991](https://github.com/pingcap/tidb/issues/48991) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that executing `UNIQUE` index lookup with an `ORDER BY` clause might cause an error [#49920](https://github.com/pingcap/tidb/issues/49920) @[jackysp](https://github.com/jackysp)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that `LIMIT` in multi-level nested `UNION` queries might become ineffective [#49874](https://github.com/pingcap/tidb/issues/49874) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the issue that the result of `COUNT(INT)` calculated by MPP might be incorrect [#48643](https://github.com/pingcap/tidb/issues/48643) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that parsing invalid values of `ENUM` or `SET` types would directly cause SQL statement errors [#49487](https://github.com/pingcap/tidb/issues/49487) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that TiDB panics and reports an error `invalid memory address or nil pointer dereference` [#42739](https://github.com/pingcap/tidb/issues/42739) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the issue that executing `UNION ALL` with the DUAL table as the first subnode might cause an error [#48755](https://github.com/pingcap/tidb/issues/48755) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that common hints do not take effect in `UNION ALL` statements [#50068](https://github.com/pingcap/tidb/issues/50068) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that TiDB server might panic during graceful shutdown [#36793](https://github.com/pingcap/tidb/issues/36793) @[bb7133](https://github.com/bb7133)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that Daylight Saving Time is displayed incorrectly in some time zones [#49586](https://github.com/pingcap/tidb/issues/49586) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that static `CALIBRATE RESOURCE` relies on the Prometheus data [#49174](https://github.com/pingcap/tidb/issues/49174) @[glorv](https://github.com/glorv)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that hints cannot be used in `REPLACE INTO` statements [#34325](https://github.com/pingcap/tidb/issues/34325) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that executing queries containing the `GROUP_CONCAT(ORDER BY)` syntax might return errors [#49986](https://github.com/pingcap/tidb/issues/49986) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that TiDB server might consume a significant amount of resources when the enterprise plugin for audit logging is used [#49273](https://github.com/pingcap/tidb/issues/49273) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that using old interfaces might cause inconsistent metadata for tables [#49751](https://github.com/pingcap/tidb/issues/49751) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that disabling `tidb_enable_collect_execution_info` causes the coprocessor cache to panic [#48212](https://github.com/pingcap/tidb/issues/48212) @[you06](https://github.com/you06)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the issue that executing `ALTER TABLE ... LAST PARTITION` fails when the partition column type is `DATETIME` [#48814](https://github.com/pingcap/tidb/issues/48814) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that the `COMMIT` or `ROLLBACK` operation executed through `COM_STMT_EXECUTE` fails to terminate transactions that have timed out [#49151](https://github.com/pingcap/tidb/issues/49151) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that histogram statistics might not be parsed into readable strings when the histogram boundary contains `NULL` [#49823](https://github.com/pingcap/tidb/issues/49823) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that queries containing common table expressions (CTEs) unexpectedly get stuck when the memory limit is exceeded [#49096](https://github.com/pingcap/tidb/issues/49096) @[AilinKid](https://github.com/AilinKid})
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that data is inconsistent under the TiDB Distributed eXecution Framework (DXF) when executing `ADD INDEX` after the DDL Owner is network isolated [#49773](https://github.com/pingcap/tidb/issues/49773) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that the auto-increment ID allocation reports an error due to concurrent conflicts when using an auto-increment column with `AUTO_ID_CACHE=1` [#50519](https://github.com/pingcap/tidb/issues/50519) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that TiDB might panic when a query contains the Apply operator and the `fatal error: concurrent map writes` error occurs [#50347](https://github.com/pingcap/tidb/issues/50347) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the TiDB node panic issue that occurs when DDL `jobID` is restored to 0 [#46296](https://github.com/pingcap/tidb/issues/46296) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that query results are incorrect due to `STREAM_AGG()` incorrectly handling CI [#49902](https://github.com/pingcap/tidb/issues/49902) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Mitigate the issue that TiDB nodes might encounter OOM errors when dealing with a large number of tables or partitions [#50077](https://github.com/pingcap/tidb/issues/50077) @[zimulala](https://github.com/zimulala)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that the `LEADING` hint does not take effect in `UNION ALL` statements [#50067](https://github.com/pingcap/tidb/issues/50067) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that `LIMIT` and `OPRDERBY` might be invalid in nested `UNION` queries [#49377](https://github.com/pingcap/tidb/issues/49377) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that a query containing the IndexHashJoin operator gets stuck when memory exceeds `tidb_mem_quota_query` [#49033](https://github.com/pingcap/tidb/issues/49033) @[XuHuaiyu](https://github.com/XuHuaiyu)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that TiDB returns wrong query results when processing `ENUM` or `SET` types by constant propagation [#49440](https://github.com/pingcap/tidb/issues/49440) @[winoros](https://github.com/winoros)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that executing `SELECT INTO OUTFILE` using the `PREPARE` method incorrectly returns a success message instead of an error [#49166](https://github.com/pingcap/tidb/issues/49166) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.8.md > Bug fixes> TiDB - Fix the issue that enforced sorting might become ineffective when a query uses optimizer hints (such as `STREAM_AGG()`) that enforce sorting and its execution plan contains `IndexMerge` [#49605](https://github.com/pingcap/tidb/issues/49605) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.1.3.md > Bug fixes> TiDB - Fix the issue that tables with `AUTO_ID_CACHE=1` might lead to gRPC client leaks when there are a large number of tables [#48869](https://github.com/pingcap/tidb/issues/48869) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that in non-strict mode (`sql_mode = ''`), truncation during executing `INSERT` still reports an error [#49369](https://github.com/pingcap/tidb/issues/49369) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that using the `_` wildcard in `LIKE` when the data contains trailing spaces can result in incorrect query results [#48983](https://github.com/pingcap/tidb/issues/48983) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-7.6.0.md > Bug fixes> TiDB - Fix the issue that executing `ADMIN CHECK` after updating the `tidb_mem_quota_query` system variable returns `ERROR 8175` [#49258](https://github.com/pingcap/tidb/issues/49258) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue of excessive statistical error in constructing statistics caused by Golang's implicit conversion algorithm [#49801](https://github.com/pingcap/tidb/issues/49801) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.7.md > Bug fixes> TiDB - Fix the issue that queries containing CTEs report `runtime error: index out of range [32] with length 32` when `tidb_max_chunk_size` is set to a small value [#48808](https://github.com/pingcap/tidb/issues/48808) @[guo-shaoge](https://github.com/guo-shaoge)

+ TiKV
    <!-- tw:@hfxsd (1) -->
    - 修复开启 checksum 可能导致 TiKV panic 的问题 [#16371](https://github.com/tikv/tikv/issues/16371) @[cfzjywxk](github.com/cfzjywxk)
    - (dup): release-6.5.8.md > Bug fixes> TiKV - Fix the issue that TiKV might panic when gRPC threads are checking `is_shutdown` [#16236](https://github.com/tikv/tikv/issues/16236) @[pingyu](https://github.com/pingyu)
    - (dup): release-6.5.8.md > Bug fixes> TiKV - Fix the issue that TiKV converts the time zone incorrectly for Brazil and Egypt [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > Bug fixes> TiKV - Fix the issue that `blob-run-mode` in Titan cannot be updated online [#15978](https://github.com/tikv/tikv/issues/15978) @[tonyxuqqi](https://github.com/tonyxuqqi)
    - (dup): release-6.5.8.md > Bug fixes> TiKV - Fix the issue that TiDB and TiKV might produce inconsistent results when processing `DECIMAL` arithmetic multiplication truncation [#16268](https://github.com/tikv/tikv/issues/16268) @[solotzg](https://github.com/solotzg)
    - (dup): release-6.5.6.md > Bug fixes> TiKV - Fix the issue that Flashback might get stuck when encountering `notLeader` or `regionNotFound` [#15712](https://github.com/tikv/tikv/issues/15712) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-6.5.7.md > Bug fixes> TiKV - Fix the issue that damaged SST files might be spread to other TiKV nodes [#15986](https://github.com/tikv/tikv/issues/15986) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.3.md > Bug fixes> TiKV - Fix the issue that if TiKV runs extremely slowly, it might panic after Region merge [#16111](https://github.com/tikv/tikv/issues/16111) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.1.3.md > Bug fixes> TiKV - Fix the issue that the joint state of DR Auto-Sync might time out when scaling out [#15817](https://github.com/tikv/tikv/issues/15817) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.3.md > Bug fixes> TiKV - Fix the issue that Resolved TS might be blocked for two hours [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.6.0.md > Bug fixes> TiKV - Fix the issue that Resolved TS might be blocked for two hours [#11847](https://github.com/tikv/tikv/issues/11847) [#15520](https://github.com/tikv/tikv/issues/15520) [#39130](https://github.com/pingcap/tidb/issues/39130) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.6.0.md > Bug fixes> TiKV - Fix the issue that `cast_duration_as_time` might return incorrect results [#16211](https://github.com/tikv/tikv/issues/16211) @[gengliqi](https://github.com/gengliqi)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.1.3.md > Bug fixes> PD - Fix the issue that when PD leader is transferred and there is a network partition between the new leader and the PD client, the PD client fails to update the information of the leader [#7416](https://github.com/tikv/pd/issues/7416) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.1.3.md > Bug fixes> PD - Fix some security issues by upgrading the version of Gin Web Framework from v1.8.1 to v1.9.1 [#7438](https://github.com/tikv/pd/issues/7438) @[niubell](https://github.com/niubell)
    - (dup): release-6.5.7.md > Bug fixes> PD - Fix the issue that the orphan peer is deleted when the number of replicas does not meet the requirements [#7584](https://github.com/tikv/pd/issues/7584) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-6.5.8.md > Bug fixes> PD - Fix the issue that querying a Region without a leader using `pd-ctl` might cause PD to panic [#7630](https://github.com/tikv/pd/issues/7630) @[rleungx](https://github.com/rleungx)

+ TiFlash
    <!-- tw:@Oreoxmt (5) -->
    - 修复在发生副本迁移时因 TiFlash 与 PD 之间网络链接不稳定可能导致 TiFlash panic 的问题 [#8323](https://github.com/pingcap/tiflash/issues/8323) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复去除 TiFlash 副本后重新添加，可能导致 TiFlash 数据损坏的问题 [#8695](https://github.com/pingcap/tiflash/issues/8695) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复在插入数据后马上进行 `DROP TABLE` 以及 `FLASHBACK TABLE` 或 `RECOVER TABLE` 操作后，部分 TiFlash 副本数据无法恢复的潜在问题 [#8395](https://github.com/pingcap/tiflash/issues/8395) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 Grafana 中部分面板的最大分位数耗时显示不正确的问题 [#8076](https://github.com/pingcap/tiflash/issues/8076) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复 TiFlash 发生 remote 读时可能会 crash 的问题 [#8685](https://github.com/pingcap/tiflash/issues/8685) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the issue that TiFlash incorrectly handles `ENUM` when the `ENUM` value is 0 [#8311](https://github.com/pingcap/tiflash/issues/8311) @[solotzg](https://github.com/solotzg)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the issue that short queries executed successfully print excessive info logs [#8592](https://github.com/pingcap/tiflash/issues/8592) @[windtalker](https://github.com/windtalker)
    - (dup): release-6.5.7.md > Bug fixes> TiFlash - Fix the issue that the memory usage increases significantly due to slow queries [#8564](https://github.com/pingcap/tiflash/issues/8564) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.8.md > Bug fixes> TiFlash - Fix the issue that the `lowerUTF8` and `upperUTF8` functions do not allow characters in different cases to occupy different bytes [#8484](https://github.com/pingcap/tiflash/issues/8484) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the potential OOM issue that might occur when scanning multiple partitioned tables during stream read [#8505](https://github.com/pingcap/tiflash/issues/8505) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-6.5.7.md > Bug fixes> TiFlash - Fix the issue of memory leak when TiFlash encounters memory limitation during query [#8447](https://github.com/pingcap/tiflash/issues/8447) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the TiFlash panic issue when TiFlash encounters conflicts during concurrent DDL execution [#8578](https://github.com/pingcap/tiflash/issues/8578) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.8.md > Bug fixes> TiFlash - Fix the issue that TiFlash panics after executing `ALTER TABLE ... MODIFY COLUMN ... NOT NULL`, which changes nullable columns to non-nullable [#8419](https://github.com/pingcap/tiflash/issues/8419) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the issue that query results are incorrect when querying with filtering conditions like `ColumnRef in (Literal, Func...)` [#8631](https://github.com/pingcap/tiflash/issues/8631) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - (dup): release-6.5.7.md > Bug fixes> TiFlash - Fix the issue that data of TiFlash replicas would still be garbage collected after executing `FLASHBACK DATABASE` [#8450](https://github.com/pingcap/tiflash/issues/8450) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the issue that TiFlash might not be able to select the GC owner of object storage data under the disaggregated storage and compute architecture [#8519](https://github.com/pingcap/tiflash/issues/8519) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.6.0.md > Bug fixes> TiFlash - Fix the random invalid memory access issue that might occur with `GREATEST` or `LEAST` functions containing constant string parameters [#8604](https://github.com/pingcap/tiflash/issues/8604) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)
        <!-- tw:@hfxsd (4) -->
        - 修复因为某个 tikv 节点没有 leader 拖慢 restore 的问题 [#50566](https://github.com/pingcap/tidb/issues/50566) @[Leavrth](https://github.com/Leavrth)
        - 全量恢复指定 --filter 选项后, 不必强制要求目标集群是空的 [#51009](https://github.com/pingcap/tidb/issues/51009) @[3pointer](https://github.com/3pointer)
        - 修复一个 restore 过程中检查集群是否为空的问题 [#50232](https://github.com/pingcap/tidb/issues/50232) @[Leavrth](https://github.com/Leavrth)
        - 修复一个停止 log backup 作业导致 tidb crash 的问题 [#50839](https://github.com/pingcap/tidb/issues/50839) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.8.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the `Unsupported collation` error is reported when you restore data from backups of an old version [#49466](https://github.com/pingcap/tidb/issues/49466) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.7.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that the log backup task can start but does not work properly if failing to connect to PD during task initialization [#16056](https://github.com/tikv/tikv/issues/16056) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.3.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR generates incorrect URIs for external storage files [#48452](https://github.com/pingcap/tidb/issues/48452) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.8.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that log backup gets stuck after changing the TiKV IP address on the same node [#50445](https://github.com/pingcap/tidb/issues/50445) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.8.md > Bug fixes> Tools> Backup & Restore (BR) - Fix the issue that BR cannot retry when encountering an error while reading file content from S3 [#49942](https://github.com/pingcap/tidb/issues/49942) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.8.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC returns the `ErrChangeFeedAlreadyExists` error when concurrently creating multiple changefeeds [#10430](https://github.com/pingcap/tiflow/issues/10430) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.8.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed `resolved ts` does not advance in extreme cases [#10157](https://github.com/pingcap/tiflow/issues/10157) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.1.3.md > Bug fixes> Tools> TiCDC - Fix the issue that TiCDC mistakenly closes the connection with TiKV in certain special scenarios [#10239](https://github.com/pingcap/tiflow/issues/10239) @[hicqu](https://github.com/hicqu)
        - (dup): release-7.1.3.md > Bug fixes> Tools> TiCDC - Fix the issue that the TiCDC server might panic when replicating data to an object storage service [#10137](https://github.com/pingcap/tiflow/issues/10137) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.8.md > Bug fixes> Tools> TiCDC - Fix the issue that the changefeed reports an error after `TRUNCATE PARTITION` is executed on the upstream table [#10522](https://github.com/pingcap/tiflow/issues/10522) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.8.md > Bug fixes> Tools> TiCDC - Fix the issue that after filtering out `add table partition` events is configured in `ignore-event`, TiCDC does not replicate other types of DML changes for related partitions to the downstream [#10524](https://github.com/pingcap/tiflow/issues/10524) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.7.md > Bug fixes> Tools> TiCDC - Fix the potential data race issue during `kv-client` initialization [#10095](https://github.com/pingcap/tiflow/issues/10095) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.6.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that a migration task error occurs when the downstream table structure contains `shard_row_id_bits` [#10308](https://github.com/pingcap/tiflow/issues/10308) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.6.0.md > Bug fixes> Tools> TiDB Data Migration (DM) - Fix the issue that DM encounters "event type truncate not valid" error that causes the upgrade to fail [#10282](https://github.com/pingcap/tiflow/issues/10282) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
