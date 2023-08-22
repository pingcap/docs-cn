---
title: TiDB 6.5.4 Release Notes
summary: 了解 TiDB 6.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.5.4 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.5.4#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - 新增 stale read traffice 相关指标和监控面板 [#43325](https://github.com/pingcap/tidb/issues/43325) @[you06](https://github.com/you06)
    - (dup): release-7.3.0.md > 改进提升> TiDB - 优化与落盘相关的 chunk 读取的性能 [#45125](https://github.com/pingcap/tidb/issues/45125) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Add get_region_read_progress command in tikv-ctl [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Compress traffic of check_leader requests. [#14839](https://github.com/tikv/tikv/issues/14839) @[you06](https://github.com/you06)
    - rawkv: fix ttl_checker for RawKV API v2. [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - Make the checkpoint lag of PITR more stable when there are some leadership transforming. [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
    - Add safe-ts related logs and Grafana panels. [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Fix occasional panic during shutdown [#13926](https://github.com/tikv/tikv/issues/13926) @[BusyJay](https://github.com/BusyJay)
    - Make online unsafe recovery abort on timeout [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - 为 check leader 请求添加 gzip 压缩降低跨 tikv 节点之间相关流量开销 [#14553](https://github.com/tikv/tikv/issues/14553) @[you06](https://github.com/you06)
    - 新增 min_safe_ts, min_safe_ts_region 和 min_safe_ts_gap 监控指标，用于诊断 resolved-ts 相关问题 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)   
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.3.0.md > 改进提升> TiKV - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get_region_read_progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.3.0.md > 改进提升> PD - 减少 `GetRegions` 请求的内存占用 [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.3.0.md > 改进提升> PD - 未开启 Swagger server 时，PD 默认屏蔽 Swagger API [#6786](https://github.com/tikv/pd/issues/6786) @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - 使用 IO 攒批优化提高了 TiFlash 的数据写入性能 [#7735](https://github.com/pingcap/tiflash/issues/7735) @[lidezhu](https://github.com/lidezhu)
    - 通过去掉不必要的文件 fsync 操作提高了 TiFlash 的数据写入性能 [#7736](https://github.com/pingcap/tiflash/issues/7736) @[lidezhu](https://github.com/lidezhu)
    - 
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.3.0.md > 改进提升> Tools> TiCDC - Storage Sink 支持对 HEX 格式的数据进行十六进制编码输出，使其兼容 AWS DMS 的格式规范 [#9373](https://github.com/pingcap/tiflow/issues/9373) @[CharlesCheung96](https://github.com/CharlesCheung96)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.1.md > 改进提升> Tools> Dumpling - 避免 Dumpling 在使用 `--sql` 参数时执行表查询语句，从而减少导出开销 [#45239](https://github.com/pingcap/tidb/issues/45239) @[lance6716](https://github.com/lance6716)

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.1.md > 改进提升> Tools> TiDB Binlog - 优化表信息的获取方式，降低 Drainer 的初始化时间和内存占用 [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @[lichunzhu](https://github.com/lichunzhu)

## 错误修复

+ TiDB

    - 修复 load data assertion 报错问题 [#43849](https://github.com/pingcap/tidb/issues/43849) @[you06](https://github.com/you06) 
    - 修复 stale read ts 设置不正确可能导致 prepare statement 读数据不正确的问题 [#43044](https://github.com/pingcap/tidb/issues/43044) @[you06](https://github.com/you06) 
    - 修复activate txn 可能存在的 data race [#42092](https://github.com/pingcap/tidb/issues/42092) @[hawkingrei](https://github.com/hawkingrei)
    - 修复 coprocessor 请求 scan details 处理不准确的问题 [#41582](https://github.com/pingcap/tidb/issues/41582) @[you06](https://github.com/you06) 
    - 修复 batch client 重连不及时的问题 [#44431](https://github.com/pingcap/tidb/issues/44431) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.1.7.md > 错误修复> TiDB - 修复 SQL compile 报错的日志未脱敏的问题 [#41831](https://github.com/pingcap/tidb/issues/41831) @[lance6716](https://github.com/lance6716)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复同时使用 CTE 和关联子查询可能导致查询结果出错或者 panic 的问题 [#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @[winoros](https://github.com/winoros) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了 TTL 任务不能及时触发统计信息更新的问题 [#40109](https://github.com/pingcap/tidb/issues/40109) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 GC resolve lock 可能错过一些悲观锁的问题 [#45134](https://github.com/pingcap/tidb/issues/45134) @[MyonKeminta](https://github.com/MyonKeminta)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 memory tracker 潜在的泄露问题 [#44612](https://github.com/pingcap/tidb/issues/44612) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.DDL_JOBS` 表中 `QUERY` 列的数据长度可能超出列定义的问题 [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了使用 `Prepare` 或 `Execute` 查询某些虚拟表时无法将表 ID 下推，导致在大量 Region 的情况下 PD OOM 的问题 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - (dup): release-7.0.0.md > 错误修复> TiDB - 修复在为分区表添加新的索引之后，该分区表可能无法正确触发统计信息的自动收集的问题 [#41638](https://github.com/pingcap/tidb/issues/41638) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复极端情况下，统计 SQL execution detail 的信息占用太多内存导致 TiDB OOM 的问题 [#44047](https://github.com/pingcap/tidb/issues/44047) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 batch coprocessor 重试时可能会生成错误 Region 信息导致查询失败的问题 [#44622](https://github.com/pingcap/tidb/issues/44622) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复带 `indexMerge` 的查询被 kill 时可能会卡住的问题 [#45279](https://github.com/pingcap/tidb/issues/45279) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复在创建分区表时使用 `SUBPARTITION` 没有警告提醒的问题 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复当开启 `tidb_enable_parallel_apply` 时，MPP 模式下的查询结果出错的问题 [#45299](https://github.com/pingcap/tidb/issues/45299) @[windtalker](https://github.com/windtalker)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复开启 `tidb_opt_agg_push_down` 时查询可能返回错误结果的问题 [#44795](https://github.com/pingcap/tidb/issues/44795) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了由虚拟列引发的 `can't find proper physical plan` 问题 [#41014](https://github.com/pingcap/tidb/issues/41014) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-6.1.7.md > 错误修复> TiDB - 修复某些情况下 TiDB 查询 panic 的问题 [#40857](https://github.com/pingcap/tidb/issues/40857) @[Dousir9](https://github.com/Dousir9)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 `processInfo` 为空导致的 panic 问题 [#43829](https://github.com/pingcap/tidb/issues/43829) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 `SELECT CAST(n AS CHAR)` 语句中的 `n` 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复当使用 MySQL 的 Cursor Fetch 协议时，结果集占用的内存超过 `tidb_mem_quota_query` 的限制导致 TiDB OOM 的问题。修复后，TiDB 会自动将结果集写入磁盘以释放内存资源 [#43233](https://github.com/pingcap/tidb/issues/43233) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复通过 BR 恢复 `AUTO_ID_CACHE=1` 的表时，会遇到 `duplicate entry` 报错的问题 [#44716](https://github.com/pingcap/tidb/issues/44716) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复当分区表定义中使用了 `FLOOR()` 函数对分区列进行取整时 `SELECT` 语句返回错误的问题 [#42323](https://github.com/pingcap/tidb/issues/42323) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了并发视图模式可能会造成 DDL 操作卡住的问题 [#40352](https://github.com/pingcap/tidb/issues/40352) @[zeminzhou](https://github.com/zeminzhou)
    - (dup): release-6.6.0.md > 错误修复> TiDB - 修复了收集统计信息任务因为错误的 `datetime` 值而失败的问题 [#39336](https://github.com/pingcap/tidb/issues/39336) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    - (dup): release-6.1.0.md > 错误修复> TiDB - 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 resolve lock 在 PD 时间跳变的情况下可能卡住的问题 [#44822](https://github.com/pingcap/tidb/issues/44822) @[zyguan](https://github.com/zyguan)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复 index scan 中可能存在的数据竞争问题 [#45126](https://github.com/pingcap/tidb/issues/45126) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复对于过长的 SQL 输入，`FormatSQL()` 方法无法正常截断的问题 [#44542](https://github.com/pingcap/tidb/issues/44542) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.1.md > 错误修复> TiDB - 修复即使用户没有权限，也能查看 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表信息的问题 [#45320](https://github.com/pingcap/tidb/issues/45320) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ TiKV

    - Fix an issue that Region merge may be blocked after flashback [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - Fix an issue that may cause inconsistent reads when a TiKV node is isolated while another node restarts [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - Fix the QPS drop to zero in dr SyncRecovery phase in DR mode [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - Fix offset inconsistency between crypter and file that could cause data corruption when file I/O is interrupted. [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)
    - rust-rocks: expose ColumnFamilyOptions's ttl and periodic_compaction_seconds setting in tikv. They're disabled by default. [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)
    - pd_client: reduce store heartbeat retires to prevent heartbeat storm [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - Fix the issue that flow control may not work when pending compaction bytes is high [#14392](https://github.com/tikv/tikv/issues/14392) @[Connor1996](https://github.com/Connor1996)
    - Fixed a bug that may cause PITR get stuck when the network between PD and TiKV is cut down. [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - Fixed a bug that may cause TiKV use more memory than excepted when TiCDC and old value enabled. [#14815](https://github.com/tikv/tikv/issues/14815) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.1.4.md > Bug 修复> PD - 修复 PD 可能会非预期地向 Region 添加多个 Learner 的问题 [#5786](https://github.com/tikv/pd/issues/5786) @[HunDunDM](https://github.com/HunDunDM)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复 `unsafe recovery` 中失败的 learner peer 在 `auto-detect` 模式中被忽略的问题 [#6690](https://github.com/tikv/pd/issues/6690) @[v01dstar](https://github.com/v01dstar)

+ TiFlash

    - 修复在更改 `DATETIME`、`TIMESTAMP`、`TIME` 数据类型的 `fsp` 之后查询失败的问题 [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复由于 Region 的边界的 Key 不合法导致 TiFlash 数据不一致的问题 [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.3.0.md > 错误修复> TiFlash - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)
    - (dup): release-7.1.1.md > 错误修复> TiFlash - 修复 TiFlash 在使用 Online Unsafe Recovery 之后重启时间过长的问题 [#7671](https://github.com/pingcap/tiflash/issues/7671) @[hongyunyan](https://github.com/hongyunyan)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.6.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复当 TiDB 集群不存在 PITR 备份任务时，`resolve lock` 频率过高的问题 [#40759](https://github.com/pingcap/tidb/issues/40759) @[joccau](https://github.com/joccau)
        - (dup): release-7.0.0.md > 错误修复> Tools> Backup & Restore (BR) - 缓解了 Region leadership 迁移导致 PITR 日志备份进度延迟变高的问题 [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - 修复在下游发生故障重试时可能导致同步任务卡住 [#9450](https://github.com/pingcap/tiflow/issues/9450) 
        - 优化 TiCDC 因为故障重试时对外展示状态的方式 [#9483](https://github.com/pingcap/tiflow/issues/9483) 
        - 修复同步到 kafka 时重试时间间隔过短导致同步任务失败的问题 [#9504](https://github.com/pingcap/tiflow/issues/9504) 
        -  修复在上游同一个事务中修改多行 UK 场景下，CDC 可能导致同步写冲突的问题 [#9430](https://github.com/pingcap/tiflow/issues/9430) 
        -  修复同步 rename ddl 存在可能不能正确同步的问题 [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531)
        - 修复下游发生短时间故障导致同步任务卡住的问题 [#9542](https://github.com/pingcap/tiflow/issues/9542)[#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582)[#9592](https://github.com/pingcap/tiflow/issues/9592)
        - 优化同步到 kafka 时消息过大超过限制的处理方式，允许只发送 PK 到下游 [#9574](https://github.com/pingcap/tiflow/issues/9574)
        - 修复CDC 节点在发生网络隔离时可能导致数据不一致的问题[#9344](https://github.com/pingcap/tiflow/issues/9344)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.3.0.md > 错误修复> Tools> TiCDC - 修复在 TiCDC 节点状态发生改变时可能引发的 panic 问题 [#9354](https://github.com/pingcap/tiflow/issues/9354) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiCDC - 修复当 Kafka Sink 遇到错误时可能会无限阻塞同步任务推进的问题 [#9309](https://github.com/pingcap/tiflow/issues/9309) @[hicqu](https://github.com/hicqu)
        - (dup): release-7.1.1.md > 错误修复> Tools> TiCDC - 修复当下游为 Kafka 时，TiCDC 查询下游的元信息频率过高导致下游负载过大的问题 [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiCDC - 修复 TiCDC 部分节点发生网络隔离时可能引发的数据不一致问题 [#9344](https://github.com/pingcap/tiflow/issues/9344) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.1.1.md > 错误修复> Tools> TiCDC - 修复在打开 redo log 且下游出现异常时可能会导致同步任务卡住的问题 [#9172](https://github.com/pingcap/tiflow/issues/9172) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiCDC - 修复由于 PD 短暂不可用而导致同步任务报错的问题 [#9294](https://github.com/pingcap/tiflow/issues/9294) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.2.0.md > 错误修复> Tools> TiCDC - 修复同步到 TiDB 或 MySQL 场景下，频繁设置下游双向复制相关变量导致下游日志过多的问题 [#9180](https://github.com/pingcap/tiflow/issues/9180) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiCDC - 修复对默认 `ENUM` 值编码错误的问题 [#9259](https://github.com/pingcap/tiflow/issues/9259) @[3AceShowHand](https://github.com/3AceShowHand)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.1.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM-master 在迁移唯一索引包含空列的表时异常退出的问题 [#9247](https://github.com/pingcap/tiflow/issues/9247) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.1.md > 错误修复> Tools> TiDB Lightning - 修复竞态条件可能导致磁盘配额 (disk quota) 不准确的问题 [#44867](https://github.com/pingcap/tidb/issues/44867) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 导入完成后执行 checksum 可能遇到 SSL 错误的问题 [#45462](https://github.com/pingcap/tidb/issues/45462) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-7.3.0.md > 错误修复> Tools> TiDB Lightning - 修复逻辑导入模式下，导入期间下游删除表可能导致 TiDB Lightning 元信息未及时更新的问题 [#44614](https://github.com/pingcap/tidb/issues/44614) @[dsdashun](https://github.com/dsdashun)
        - (dup): release-7.1.1.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 连接 PD 失败无法重试的问题，提高导入成功率 [#43400](https://github.com/pingcap/tidb/issues/43400) @[lichunzhu](https://github.com/lichunzhu)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.1.md > 错误修复> Tools> TiDB Binlog - 修复 etcd client 初始化时没有自动同步最新节点信息的问题 [#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @[lichunzhu](https://github.com/lichunzhu)

## Other dup notes

- (dup): release-7.3.0.md > # 稳定性 * 新增部分优化器提示 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
- (dup): release-7.0.0.md > # 稳定性> [`MPP_2PHASE_AGG()`](/optimizer-hints.md#mpp_2phase_agg)：针对 MPP 生效。提示优化器对指定查询块中所有聚合函数使用二阶段聚合算法。 * 优化器 Hint 可兼容指定连接方式与连接顺序 [#36600](https://github.com/pingcap/tidb/issues/36600) @[Reminiscent](https://github.com/Reminiscent)
- (dup): release-6.6.0.md > # 高可用 * [Placement Rules in SQL](/placement-rules-in-sql.md) 支持指定 `SURVIVAL_PREFERENCE` [#38605](https://github.com/pingcap/tidb/issues/38605) @[nolouch](https://github.com/nolouch)
