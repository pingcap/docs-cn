---
title: TiDB 7.1.2 Release Notes
summary: 了解 TiDB 7.1.2 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.1.2 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.1.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.1.2#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.5.md > 改进提升> TiDB - 添加 coprocessor 相关的 request source 信息 [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.5.md > 改进提升> TiKV - 优化数据整理检查机制，当触发 Region Split 时，如果没有可以分裂的 key，触发一次数据整理，以消除过多的 MVCC 版本 [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - (dup): release-7.4.0.md > 改进提升> TiKV - 消除 Router 对象中的 LRUCache，降低内存占用，防止 OOM [#15430](https://github.com/tikv/tikv/issues/15430) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.3.0.md > 改进提升> TiKV - 添加 `Max gap of safe-ts` 和 `Min safe ts region` 监控项以及 `tikv-ctl get_region_read_progress` 命令，用于更好地观测和诊断 resolved-ts 和 safe-ts 的状态 [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - (dup): release-6.5.4.md > 改进提升> TiKV - 在 TiKV 中暴露部分 RocksDB 配置，允许用户禁用 TTL 和定期数据整理等特性 [#14873](https://github.com/tikv/tikv/issues/14873) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-7.4.0.md > 改进提升> TiKV - 新增 PD Client 连接重试过程中的 backoff 机制。异常错误重试期间，逐步增加重试时间间隔，减小 PD 压力 [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.4.md > 改进提升> TiKV - 避免写 Titan manifest 文件时持有锁导致影响其他线程 [#15351](https://github.com/tikv/tikv/issues/15351) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.4.0.md > 改进提升> TiKV - 改进 Resolver 的内存使用，防止 OOM [#15458](https://github.com/tikv/tikv/issues/15458) @[overvenus](https://github.com/overvenus)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.3.0.md > 改进提升> PD - 减少 `GetRegions` 请求的内存占用 [#6835](https://github.com/tikv/pd/issues/6835) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.4.0.md > 改进提升> PD - 支持复用 HTTP Client 连接，降低内存占用 [#6913](https://github.com/tikv/pd/issues/6913) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 修复 Sort 算子在 Spill 时可能发生的 Crash [#47538](https://github.com/pingcap/tidb/issues/47538) @[windtalker](https://github.com/windtalker)
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 改进提升> Tools> Backup & Restore (BR) - 通过设置 HTTP 客户端 `MaxIdleConns` 和 `MaxIdleConnsPerHost` 参数，增强日志备份以及 PITR 恢复任务对连接复用的支持 [#46011](https://github.com/pingcap/tidb/issues/46011) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.4.0.md > 改进提升> Tools> Backup & Restore (BR) - 减少日志备份 `resolve lock` 的 CPU 开销 [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 改进提升> Tools> TiCDC - 优化同步 `ADD INDEX` DDL 的执行逻辑，从而不阻塞后续的 DML 语句 [#9644](https://github.com/pingcap/tiflow/issues/9644) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.4.md > 改进提升> Tools> TiCDC - 优化 TiCDC 在故障重试时的状态展示信息 [#9483](https://github.com/pingcap/tiflow/issues/9483) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.4.md > 改进提升> Tools> TiDB Data Migration (DM) - 对不兼容的 DDL 支持严格的乐观模式 [#9112](https://github.com/pingcap/tiflow/issues/9112) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 改进提升> Tools> TiDB Lightning - 优化 TiDB Lightning 在导入数据阶段对 `no leader` 错误的重试逻辑 [#46253](https://github.com/pingcap/tidb/issues/46253) @[lance6716](https://github.com/lance6716)

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

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `group_concat` 无法解析 `ORDER BY` 列的问题 [#41986](https://github.com/pingcap/tidb/issues/41986) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复某些情况下查询系统表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 返回结果错误的问题 [#45531](https://github.com/pingcap/tidb/issues/45531) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复读取元数据时间超过一个 DDL lease 导致升级 TiDB 卡住的问题 [#45176](https://github.com/pingcap/tidb/issues/45176) @[zimulala](https://github.com/zimulala)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复执行带 CTE 的 DML 会导致 panic 的问题 [#46083](https://github.com/pingcap/tidb/issues/46083) @[winoros](https://github.com/winoros)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复交换分区时，无法检测出不符合分区定义的数据的问题 [#46492](https://github.com/pingcap/tidb/issues/46492) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `MERGE_JOIN` 的结果错误的问题 [#46580](https://github.com/pingcap/tidb/issues/46580) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复无符号类型与 `Duration` 类型常量比较时产生的结果错误 [#45410](https://github.com/pingcap/tidb/issues/45410) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `AUTO_ID_CACHE=1` 时可能导致 `Duplicate entry` 的问题 [#46444](https://github.com/pingcap/tidb/issues/46444) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.3.0.md > 错误修复> TiDB - 修复 TTL 运行过程中内存泄漏的问题 [#45510](https://github.com/pingcap/tidb/issues/45510) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.4.md > 错误修复> TiDB - 修复 kill 连接之后可能会出现 go coroutine 泄露的问题 [#46034](https://github.com/pingcap/tidb/issues/46034) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 Index Join 出错可能导致查询卡住的问题 [#45716](https://github.com/pingcap/tidb/issues/45716) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `BatchPointGet` 算子在 Hash 分区表下执行结果错误的问题 [#46779](https://github.com/pingcap/tidb/issues/46779) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复在交换分区失败或被取消时，分区表的限制残留在原表上的问题 [#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复当 JOIN 两个子查询时执行 `TIDB_INLJ` Hint 不生效的问题 [#46160](https://github.com/pingcap/tidb/issues/46160) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `DATETIME` 或 `TIMESTAMP` 列与数字值比较时，行为与 MySQL 不一致的问题 [#38361](https://github.com/pingcap/tidb/issues/38361) @[yibin87](https://github.com/yibin87)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复深嵌套的表达式的 HashCode 重复计算导致的高内存占用和 OOM 问题 [#42788](https://github.com/pingcap/tidb/issues/42788) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 access path 的启发式规则会忽略 `READ_FROM_STORAGE(TIFLASH[...])` Hint 导致 `Can't find a proper physical plan` 的问题 [#40146](https://github.com/pingcap/tidb/issues/40146) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `cast(col)=range` 条件在 CAST 无精度损失的情况下会导致 FullScan 的问题 [#45199](https://github.com/pingcap/tidb/issues/45199) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `plan replayer dump explain` 会报错的问题 [#46197](https://github.com/pingcap/tidb/issues/46197) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `tmp-storage-quota` 配置无法生效的问题 [#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 TiDB parser 状态残留导致解析失败的问题 [#45898](https://github.com/pingcap/tidb/issues/45898) @[qw4990](https://github.com/qw4990)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 MPP 执行计划中通过 Union 下推 Aggregation 导致的结果错误 [#45850](https://github.com/pingcap/tidb/issues/45850) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-7.4.0.md > 错误修复> TiDB - 修复 `AUTO_ID_CACHE=1` 时 TiDB panic 后恢复过慢的问题 [#46454](https://github.com/pingcap/tidb/issues/46454) @[tiancaiamao](https://github.com/tiancaiamao)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复 `ttl-check-poll-interval` 配置项对 RawKV API V2 不生效的问题 [#15142](https://github.com/tikv/tikv/issues/15142) @[pingyu](https://github.com/pingyu)
    - (dup): release-7.4.0.md > 错误修复> TiKV - 修复 raftstore-applys 不断增长的数据错误 [#15371](https://github.com/tikv/tikv/issues/15371) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复自适应同步模式下 sync-recover 阶段 QPS 下降到 0 的问题 [#14975](https://github.com/tikv/tikv/issues/14975) @[nolouch](https://github.com/nolouch)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复当一个 TiKV 节点被隔离而另一个节点重启时，可能导致读取不一致的问题 [#15035](https://github.com/tikv/tikv/issues/15035) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.5.md > 错误修复> TiKV - 修复 Online Unsafe Recovery 时无法处理 merge abort 的问题 [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - (dup): release-6.5.5.md > 错误修复> TiKV - 修复 PD 和 TiKV 之间的网络中断可能导致 PITR 卡住的问题 [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复在执行 `FLASHBACK` 后 Region Merge 可能被阻塞的问题 [#15258](https://github.com/tikv/tikv/issues/15258) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 减少 Store 心跳重试次数，修复心跳风暴的问题 [#15184](https://github.com/tikv/tikv/issues/15184) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.4.0.md > 错误修复> TiKV - 修复 Online Unsafe Recovery 超时未中止的问题 [#15346](https://github.com/tikv/tikv/issues/15346) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.4.md > 错误修复> TiKV - 修复部分写入时加密可能导致数据损坏的问题 [#15080](https://github.com/tikv/tikv/issues/15080) @[tabokie](https://github.com/tabokie)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.4.0.md > 错误修复> PD - 修复 Scatter Peer 时未考虑 Group 的问题 [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复在 rule checker 选定 peer 时，unhealthy peer 无法被移除的问题 [#6559](https://github.com/tikv/pd/issues/6559) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复修改隔离等级时未同步到默认放置规则中的问题 [#7121](https://github.com/tikv/pd/issues/7121) @[rleungx](https://github.com/rleungx)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复因为同步 store config 慢而导致 PD Leader 切换慢的问题 [#6918](https://github.com/tikv/pd/issues/6918) @[bufferflies](https://github.com/bufferflies)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复在 Flashback 时不更新保存 Region 信息的问题 [#6912](https://github.com/tikv/pd/issues/6912) @[overvenus](https://github.com/overvenus)
    - (dup): release-7.3.0.md > 错误修复> PD - 修复当 etcd 已经启动，但 client 尚未连接上 etcd 时，调用 client 会导致 PD panic 的问题 [#6860](https://github.com/tikv/pd/issues/6860) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复 RU 消耗小于 0 导致 PD 崩溃的问题 [#6973](https://github.com/tikv/pd/issues/6973) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-7.4.0.md > 错误修复> PD - 修复在集群规模大时 client-go 周期性更新 `min-resolved-ts` 可能造成 PD OOM 的问题 [#46664](https://github.com/pingcap/tidb/issues/46664) @[HuSharp](https://github.com/HuSharp)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.4.md > 错误修复> TiFlash - 修复由于 Region 的边界的 Key 不合法导致 TiFlash 数据不一致的问题 [#7762](https://github.com/pingcap/tiflash/issues/7762) @[lidezhu](https://github.com/lidezhu)
    - (dup): release-6.5.4.md > 错误修复> TiFlash - 修复在更改 `DATETIME`、`TIMESTAMP`、`TIME` 数据类型的 `fsp` 之后查询失败的问题 [#7809](https://github.com/pingcap/tiflash/issues/7809) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.3.0.md > 错误修复> TiFlash - 修复当同一个 MPP Task 内有多个 HashAgg 算子时，可能导致 MPP Task 编译时间过长而严重影响查询性能的问题 [#7810](https://github.com/pingcap/tiflash/issues/7810) @[SeaRise](https://github.com/SeaRise)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 恢复隐式主键可能冲突的问题 [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - (dup): release-6.5.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复 GCS 上 PITR 恢复失败的问题 [#47022](https://github.com/pingcap/tidb/issues/47022) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.4.md > 错误修复> Tools> Backup & Restore (BR) - 修复 RawKV 模式下细粒度备份阶段可能出错的问题 [#37085](https://github.com/pingcap/tidb/issues/37085) @[pingyu](https://github.com/pingyu)
        - (dup): release-7.4.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PITR 恢复数据元信息 (meta-kv) 出错的问题 [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.4.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复 BR 集成测试用例出错的问题 [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - (dup): release-6.5.4.md > 错误修复> Tools> Backup & Restore (BR) - 将 BR 使用的全局参数 `TableColumnCountLimit` 和 `IndexLimit` 的默认值提升到最大值，修复恢复过程失败的问题 [#45793](https://github.com/pingcap/tidb/issues/45793) @[Leavrth](https://github.com/Leavrth)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复开启 `scale-out` 时流量在节点间分配不均匀问题 [#9665](https://github.com/pingcap/tiflow/issues/9665) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复日志中记录了用户敏感信息的问题 [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.4.md > 错误修复> Tools> TiCDC - 修复可能无法正确同步 rename DDL 操作的问题 [#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复所有 changefeed 被移除时会阻塞上游 TiDB GC 的问题 [#9633](https://github.com/pingcap/tiflow/issues/9633) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.5.md > 错误修复> Tools> TiCDC - 修复 TiCDC 同步任务在某些特殊场景可能失败的问题 [#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.5.md > 错误修复> Tools> TiCDC - 修复 PD 节点出现网络隔离时引起 TiCDC 同步延时变高的问题 [#9565](https://github.com/pingcap/tiflow/issues/9565) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复 PD 做扩缩容场景下 TiCDC 访问无效旧地址的问题 [#9584](https://github.com/pingcap/tiflow/issues/9584) @[fubinzh](https://github.com/fubinzh) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-6.5.5.md > 错误修复> Tools> TiCDC - 修复上游在 Region 非常多时，TiKV 节点出现故障导致 TiCDC 同步任务不能快速恢复的问题 [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.5.md > 错误修复> Tools> TiCDC - 修复采用 CSV 格式时将 `UPDATE` 操作错误修改为 `INSERT` 的问题 [#9658](https://github.com/pingcap/tiflow/issues/9658) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复在上游同一条 DDL 中重命名多个表的场景下同步出错的问题 [#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @[CharlesCheung96](https://github.com/CharlesCheung96) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-6.5.4.md > 错误修复> Tools> TiCDC - 修复同步到 Kafka 时重试间隔过短导致同步任务失败的问题 [#9504](https://github.com/pingcap/tiflow/issues/9504) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiCDC - 修复在上游同一个事务中修改多行唯一键场景下，TiCDC 可能导致同步写冲突的问题 [#9430](https://github.com/pingcap/tiflow/issues/9430) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.4.md > 错误修复> Tools> TiCDC - 修复下游发生短时间故障导致同步任务卡住的问题 [#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272)[#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @[hicqu](https://github.com/hicqu)
        - (dup): release-6.5.4.md > 错误修复> Tools> TiCDC - 修复下游发生故障重试时同步任务可能卡住的问题 [#9450](https://github.com/pingcap/tiflow/issues/9450) @[hicqu](https://github.com/hicqu)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在跳过失败 DDL 并且后续无 DDL 执行时显示延迟持续增长的问题 [#9605](https://github.com/pingcap/tiflow/issues/9605) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在大小写不敏感的 collation 下无法正确处理冲突的问题 [#9489](https://github.com/pingcap/tiflow/issues/9489) @[hihihuhu](https://github.com/hihihuhu)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM validator 死锁问题并增强重试 [#9257](https://github.com/pingcap/tiflow/issues/9257) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在乐观模式恢复任务时跳过所有 DML 的问题 [#9588](https://github.com/pingcap/tiflow/issues/9588) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在跳过 Online DDL 时无法正确追踪上游表结构的问题 [#9587](https://github.com/pingcap/tiflow/issues/9587) @[GMHDBJD](https://github.com/GMHDBJD)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复 DM 在乐观模式中跳过 Partition DDL 的问题 [#9788](https://github.com/pingcap/tiflow/issues/9788) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.4.md > 错误修复> Tools> TiDB Lightning - 修复保存 `NEXT_GLOBAL_ROW_ID` 时类型错误问题 [#45427](https://github.com/pingcap/tidb/issues/45427) @[lyzx2001](https://github.com/lyzx2001)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Lightning - 修复 `checksum = "optional"` 时 Checksum 阶段仍然报错的问题 [#45382](https://github.com/pingcap/tidb/issues/45382) @[lyzx2001](https://github.com/lyzx2001)
        - (dup): release-7.4.0.md > 错误修复> Tools> TiDB Lightning - 修复当 PD 集群地址变更时数据导入失败的问题 [#43436](https://github.com/pingcap/tidb/issues/43436) @[lichunzhu](https://github.com/lichunzhu)
        - (dup): release-6.5.5.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 在 PD 拓扑变更时无法启动的问题 [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.4.md > 错误修复> Tools> TiDB Lightning - 修复导入 CSV 数据时，route 可能 panic 的问题 [#43284](https://github.com/pingcap/tidb/issues/43284) @[lyzx2001](https://github.com/lyzx2001)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-4.0.16.md > Bug 修复> Tools> TiDB Binlog - 修复传输事务超过 1 GB 时 Drainer 会退出的问题 [#28659](https://github.com/pingcap/tidb/issues/28659)

## Other dup notes

- (dup): release-7.4.0.md > # 稳定性> `stats`：对应手动执行或系统自动触发的[收集统计信息](/statistics.md#统计信息的收集)任务。 * 引入系统变量控制是否选择表的哈希连接 [#46695](https://github.com/pingcap/tidb/issues/46695) @[coderplay](https://github.com/coderplay)
- (dup): release-7.3.0.md > # 稳定性 * 新增部分优化器提示 [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
- (dup): release-7.2.0.md > # 稳定性 * 增强根据历史执行计划创建绑定的能力 [#39199](https://github.com/pingcap/tidb/issues/39199) @[qw4990](https://github.com/qw4990)