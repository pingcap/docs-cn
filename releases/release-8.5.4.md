---
title: TiDB 8.5.4 Release Notes
summary: 了解 TiDB 8.5.4 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.4 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：8.5.4

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.4#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
- (dup): release-7.5.7.md > 兼容性变更 - TiKV 废弃以下配置项，并由新的 [`gc.auto-compaction`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file/#gcauto-compaction) 配置项替代，用于控制自动 compaction 行为 [#18727](https://github.com/tikv/tikv/issues/18727) @[v01dstar](https://github.com/v01dstar)

    - 废弃配置项：[`region-compact-check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-interval)、[`region-compact-check-step`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-check-step)、[`region-compact-min-tombstones`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-tombstones)、[`region-compact-tombstones-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-tombstones-percent)、[`region-compact-min-redundant-rows`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-min-redundant-rows-从-v710-版本开始引入) 和 [`region-compact-redundant-rows-percent`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#region-compact-redundant-rows-percent-从-v710-版本开始引入)。
    - 新增配置项：[`gc.auto-compaction.check-interval`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#check-interval-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-num-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#tombstone-percent-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-threshold-从-v757-版本开始引入)、[`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#redundant-rows-percent-threshold-从-v757-版本开始引入) 和 [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/zh/tidb/v7.5/tikv-configuration-file#bottommost-level-force-从-v757-版本开始引入)。

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md(beta.1) > # SQL 功能 * 支持对分区表的非唯一列创建全局索引 [#58650](https://github.com/pingcap/tidb/issues/58650) @[Defined2014](https://github.com/Defined2014) @[mjonss](https://github.com/mjonss)
    - (dup): release-9.0.0.md(beta.1) > 改进提升> TiDB - 支持由 `IN` 子查询而来的 Semi Join 使用 `semi_join_rewrite` 的 Hint [#58829](https://github.com/pingcap/tidb/issues/58829) @[qw4990](https://github.com/qw4990)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.5.7.md > 改进提升> TiKV - 优化在存在大量 SST 文件的环境中 async snapshot 和 write 的尾延迟 [#18743](https://github.com/tikv/tikv/issues/18743) @[Connor1996](https://github.com/Connor1996)

+ PD

    - 减少非必要的错误日志 [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)
    - 升级 golang 版本到 1.23.12, 同时更新相关依赖 [#9788](https://github.com/tikv/pd/issues/9788) @[JmPotato](https://github.com/JmPotato)
    - 支持按照表级别维度打散 region 数量，使其按照 scatter-role 和 engine 维度进行均衡 #[8986](https://github.com/tikv/pd/issues/8986)  @[bufferflies](https://github.com/bufferflies)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 跳过不必要读取的数据，优化 TableScan 的读取性能 [#9875](https://github.com/pingcap/tiflash/issues/9875) @[gengliqi](https://github.com/gengliqi)
    - 优化 TiFlash 在宽且稀疏的表上 TableScan 的性能 [#10361](https://github.com/pingcap/tiflash/issues/10361) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 优化当集群存在大量表时，添加向量索引时的 TiFlash CPU 开销 [#10357](https://github.com/pingcap/tiflash/issues/10357) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 减少不必要的处理 raft commands 时的日志 [#10467](https://github.com/pingcap/tiflash/issues/10467) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - 修复当 `tidb_isolation_read_engines` 设置为 "tiflash" 时，`use index` hint 无法生效的问题 [#60869](https://github.com/pingcap/tidb/issues/60869) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复了 `max_execution_time` 对 `SELECT FOR UPDATE` 语句不生效的问题. [#62960](https://github.com/pingcap/tidb/issues/62960) @[ekexium](https://github.com/ekexium)
    - (dup): release-7.5.7.md > 错误修复> TiDB - 修复估算跨月或跨年的行数时，结果可能过分偏大的问题 [#50080](https://github.com/pingcap/tidb/issues/50080) @[terry1purcell](https://github.com/terry1purcell)
    - 修复预处理语句中处理 decimal 与 mysql 不一致的问题 [#62602](https://github.com/pingcap/tidb/issues/62602) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)
    - 修复 `truncate` 函数中短路径处理错误的问题 [#57608](https://github.com/pingcap/tidb/issues/57608) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复当 `Out Of Quota For Local Temporary Space` 触发时，spill 文件可能未被全部删除的问题 [#63216](https://github.com/pingcap/tidb/issues/63216) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

+ PD

    - 修复 PD Client 重试策略没有正确初始化的问题 [#9013](https://github.com/tikv/pd/issues/9013) @[rleungx](https://github.com/rleungx)
    - 修复 /config 和 /members API 的错误输出 [#9797](https://github.com/tikv/pd/issues/9797) @[lhy1024](https://github.com/lhy1024) 
    - 修复 tso proxy 错误处理 #[9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)
    - 修复在关闭 bucket 上报后， split bucket 依然生效 #[9726](https://github.com/tikv/pd/issues/9726) @[bufferflies](https://github.com/bufferflies)
    - 修复 resource manager 错误分配 token 问题 #[9455](https://github.com/tikv/pd/issues/9455)  @[JmPotato](https://github.com/JmPotato)
    - 修复 pd leader 变更后, placement rule 不生效问题 #[9602](https://github.com/tikv/pd/issues/9602) @[okJiang](https://github.com/okJiang)
    - 修复 backoff 初始化错误问题 #[9013](https://github.com/tikv/pd/issues/9013)  @[rleungx](https://github.com/rleungx)
    - 修复 ttl 配置不生效问题 #[9343](https://github.com/tikv/pd/issues/9343) @[lhy1024](https://github.com/lhy1024) 

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - 修复当查询的列存储大量 `NULL` 值时，可能导致查询失败的问题 [#10340](https://github.com/pingcap/tiflash/issues/10340) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复 TiFlash 消耗超过预期的 RU 的问题 [#10380](https://github.com/pingcap/tiflash/issues/10380) @[JinheLin](https://github.com/JinheLin)
    - 修复存算分离架构下，在存在慢查询时 TiFlash 容易发生 OOM 的问题 [#10278](https://github.com/pingcap/tiflash/issues/10278) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复存算分离架构下，TiFlash 遇到与 S3 网络分区时可能无限重试的问题 [#10424](https://github.com/pingcap/tiflash/issues/10424) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - 修复了当参数为 `decimal` 类型时，`floor` 和 `ceil` 函数结果可能不正确的问题 [#10365](https://github.com/pingcap/tidb/issues/10365) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) 

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiCDC

        - 修复在配置包含虚拟列的 column 类型 partition 分发器时可能导致的 panic 问题 [#12241](https://github.com/pingcap/tiflow/issues/12241) @[wk989898](https://github.com/wk989898)
        - 修复在关闭 ddl puller 时可能引发的 panic 问题 [#12244](https://github.com/pingcap/tiflow/issues/12244) @[wk989898](https://github.com/wk989898)
        - 支持在 filter 中通过设置 `ignore-txn-start-ts` 来过滤不支持的 DDL 类型 [#12286](https://github.com/pingcap/tiflow/issues/12286) @[asddongmen](https://github.com/asddongmen)
        - 修复使用 Azure 下游时可能引起的卡住问题 [#12277] (https://github.com/pingcap/tiflow/issues/12277) @[zurakutsia](https://github.com/zurakutsia)
        - 修复 `drop foreign key` DDL 没有同步到下游的问题 [#12328](https://github.com/pingcap/tiflow/issues/12328) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复订阅 region 时遇到回滚和预写条目导致的 panic 问题 [#19048](https://github.com/tikv/tikv/issues/19048) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 TiKV 断言错误导致的 panic 问题 [#18498](https://github.com/tikv/tikv/issues/18498) @[tharanga](https://github.com/tharanga)
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})