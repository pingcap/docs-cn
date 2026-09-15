---
title: TiDB 7.5.8 Release Notes
summary: 了解 TiDB 7.5.8 的改进和错误修复。
---

# TiDB 7.5.8 Release Notes

发版日期：2026 年 9 月 17 日

TiDB 版本：7.5.8

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://pingkai.cn/download#tidb-community)

## 改进提升

+ PD

    - 为 `pd_cluster_status` 监控指标添加 `store` 标签，使 PD 能够按 store 维度上报状态指标，便于识别受影响的 TiKV store，并在需要时聚合整个集群的指标值 [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/10060 -->

## 错误修复

+ TiDB

    - 修复由于 `UNION` 查询的清理过程与 worker goroutine 的退出过程之间存在竞争，TiDB 可能因 `SIGSEGV` 崩溃的问题 [#66391](https://github.com/pingcap/tidb/issues/66391) @[bb7133](https://github.com/bb7133) <!-- component: execution --> <!-- pr: https://github.com/pingcap/tidb/pull/67003 -->
    - 修复在某些场景下，由于开销较大的全范围检查，TiDB 在查询规划期间消耗过多 CPU 的问题 [#63235](https://github.com/pingcap/tidb/issues/63235) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/64058 --> <!-- pr: https://github.com/pingcap/tidb/pull/63813 -->
    - 修复当 `tidb_opt_objective` 设置为 `determinate` 时，TiDB 在异步加载新添加索引的统计信息期间可能发生 panic 的问题 [#64274](https://github.com/pingcap/tidb/issues/64274) @[0xPoe](https://github.com/0xPoe) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/64292 -->

+ TiKV

    - 修复由于外部 SST 导入与前台写入之间存在竞争，TiKV 可能因 `txn record found but not expected` 发生 panic 的问题 [#19891](https://github.com/tikv/tikv/issues/19891) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19914 -->
    - 修复停止日志备份任务后，BR 遗留了不再需要的 GC service safepoint，可能导致 GC 无法按预期推进的问题 [#19832](https://github.com/tikv/tikv/issues/19832) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19913 -->
    - 修复在 TiCDC 重启或网络故障后，TiKV 与 TiCDC 之间的残留连接可能无法被完全清理，导致 TiKV CDC 内存配额耗尽并使 Changefeed 卡住的问题 [#18169](https://github.com/tikv/tikv/issues/18169) [#19610](https://github.com/tikv/tikv/issues/19610) @[asddongmen](https://github.com/asddongmen) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/tikv/tikv/pull/18864 --> <!-- pr: https://github.com/tikv/tikv/pull/19689 -->
    - 修复在 TiKV 出现 I/O 阻塞时，由于与 PD 相关的工作被 I/O 操作阻塞，TiKV 吞吐量可能持续下降的问题 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/18969 -->
    - 修复在 TiDB Lightning 导入数据期间，TiKV 可能因空指针解引用而崩溃的问题 [#18671](https://github.com/tikv/tikv/issues/18671) [#18756](https://github.com/tikv/tikv/issues/18756) @[Dog-Du](https://github.com/Dog-Du) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19908 -->

+ PD

    - 修复在 TiDB Lightning 导入期间并发调用 `SetRegionLabelRule` 时，PD 可能出现 goroutine 激增并变得不稳定的问题 [#9854](https://github.com/tikv/pd/issues/9854) @[lhy1024](https://github.com/lhy1024) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/9897 -->

+ TiFlash

    - 修复执行移除列 `NOT NULL` 约束的 DDL 语句后，TiFlash 与 TiKV 之间可能出现数据不一致的问题 [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang) <!-- component: storage --> <!-- pr: https://github.com/pingcap/tiflash/pull/10690 -->

+ 工具

    + TiCDC

        - 修复 Kafka Changefeed 在 DDL 或 checkpoint 事件投递失败后重试时泄漏 Kafka client，导致内存持续增长的问题 [#12666](https://github.com/pingcap/tiflow/issues/12666) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/tiflow/pull/12678 -->
        - 修复当 admin 或 producer 初始化失败，或关闭 admin 包装器或同步 producer 包装器时，Kafka sink 可能泄漏底层 Sarama client 的问题 [#12572](https://github.com/pingcap/tiflow/issues/12572) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/tiflow/pull/12592 -->
