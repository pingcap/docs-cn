---
title: TiDB 8.5.1 Release Notes
summary: 了解 TiDB 8.5.1 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.1 Release Notes

发版日期：2025 年 x 月 x 日

TiDB 版本：8.5.1

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.1#version-list)

## 操作系统支持变更

- 从 v8.5.1 起，TiDB 重新提供了对 CentOS Linux 7 的支持。如果你需要在 CentOS 7 上部署 TiDB 8.5 版本或将集群升级到 TiDB 8.5 版本，请部署或升级至 TiDB 8.5.1 或以上版本。
    - 根据 [CentOS Linux EOL](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)，CentOS Linux 7 的上游支持已于 2024 年 6 月 30 日终止。在 v8.4.0 DMR 和 v8.5.0 版本中，TiDB 暂停了对 CentOS 7 的支持，建议使用 Rocky Linux 9.1 及以上的版本。如果在使用 CentOS Linux 7 的情况下将 TiDB 升级到 v8.4.0 DMR 或 v8.5.0 版本，将导致集群不可用的风险。
    - 尽管 TiDB v8.5.1 及以上版本支持 CentOS Linux 7，但由于 CentOS Linux 7 已经达到其生命周期的终止（EOL），强烈建议用户参考该系统的[官方声明和安全建议](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)，考虑尽快迁移到 [TiDB 支持的操作系统版本](/hardware-and-software-requirements.md#操作系统及平台要求)，如 Rocky Linux 9.1 及以上版本。

## 改进提升

+ TiDB <!--tw@Oreoxmt: 5 notes-->

    - 支持将只读的用户变量折叠为常量 [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    - 将具有 nulleq 条件的笛卡尔积 Semi Join 转换为具有相等条件的 Semi Join [#57583](https://github.com/pingcap/tidb/issues/57583) @[hawkingrei](https://github.com/hawkingrei)
    - 统计信息内存缓存的默认阈值为总内存的 20% [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)

+ TiKV <!--tw@Oreoxmt: 1 note-->

    - 增加了对非法 max-ts 更新的检测机制 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)

+ TiFlash

    - (dup): release-7.5.5.md > 改进提升> TiFlash - 优化在存算分离架构下，读节点从 S3 下载文件异常时的重试策略 [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

+ Tools

    + TiCDC <!--tw@qiancai: 1 note-->

        - 减少 TiCDC 在做 Initial Scan 时对与 TiKV 中 cache hit rate 的影响 [#17877](https://github.com/tikv/tikv/issues/17877) @[hicqu](https://github.com/hicqu)

## 错误修复

+ TiDB <!--tw@lilin90: the following 9 notes-->

    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复查询 TiFlash 系统表中默认超时时间过短的问题 [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复设置 `tidb_gogc_tuner_max_value` 和 `tidb_gogc_tuner_min_value` 时，由于最大值为空导致出现错误的 warning 信息的问题 [#57889](https://github.com/pingcap/tidb/issues/57889) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复添加索引期间，计划缓存使用了错误的 schema 导致数据索引不一致的问题 [#56733](https://github.com/pingcap/tidb/issues/56733) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-7.5.5.md > 错误修复> TiDB - 修复 Grafana 中 **Stats Healthy Distribution** 面板的数据可能错误的问题 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    - 修复没有收集过统计信息的表的上次 ANALYZE 时间可能不为 NULL 的问题 [#57735](https://github.com/pingcap/tidb/issues/57735) @[winoros](https://github.com/winoros)
    - 正确处理取统计信息的异常，防止后台任务超时时内存内的统计信息被误删除的问题 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    - 修复执行 DROP DATABASE 语句后统计信息未被清理的问题  [#57230](https://github.com/pingcap/tidb/issues/57230) @[Rustin170506](https://github.com/Rustin170506)
    - 修复在构造 IndexMerge 时可能丢失部分谓词的问题 [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    - 修复在超过 3000 维向量类型的列上创建向量搜索索引会失败的问题 [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    - 修复 REORGANIZE PARTITION 操作未正确移除被替换的全局索引以及处理非聚簇表唯一索引的问题。[#56822](https://github.com/pingcap/tidb/issues/56822) @[mjonss](https://github.com/mjonss)
    - 修复分区表 Range INTERVAL 语法糖不支持使用 `MINUTE` 做间隔的问题。[#57698](https://github.com/pingcap/tidb/issues/57698) @[mjonss](https://github.com/mjonss)
    - 修复查询慢日志时，由于时区导致的时间范围错误的问题 [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在缩减 TTL 扫描任务工作线程时，任务取消失败可能导致扫描任务泄漏的问题。 [#57708](https://github.com/pingcap/tidb/issues/57708) @[YangKeao](https://github.com/YangKeao) <!--tw@hfxsd: the following 10 notes-->
    - 修复在丢失心跳后，若 TTL 表被删除或禁用，TTL 作业仍继续运行的问题 [#57702](https://github.com/pingcap/tidb/issues/57702) @[YangKeao](https://github.com/YangKeao)
    - 修复 TTL 作业被取消后，last_job_finish_time 显示不正确的问题 [#58109](https://github.com/pingcap/tidb/issues/58109) @[YangKeao](https://github.com/YangKeao)
    - 修复 TiDB 丢失心跳时，TTL 任务无法被取消的问题 [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    - 修复某个 TTL 任务丢失心跳会阻塞其他任务获取心跳的问题 [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    - 修复缩减 TTL 工作线程时，部分过期行未被删除的问题。 [#57990](https://github.com/pingcap/tidb/issues/57990) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当 TTL 删除速率限制器被中断时，剩余行未重试的问题。[#58205](https://github.com/pingcap/tidb/issues/58205) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在某些情况下，TTL 可能生成大量警告日志的问题。[#58305](https://github.com/pingcap/tidb/issues/58305) @[lcwangchao](https://github.com/lcwangchao)
    - 修复在修改 tidb_ttl_delete_rate_limit 时，部分 TTL 任务可能挂起的问题。[#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    - 修复执行 REORGANIZE PARTITION 时，数据回填可能导致并发更新被回滚的问题。[#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    - 修复查询 cluster_slow_query 表时使用 order by 可能导致结果乱序的问题。[#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)

+ TiKV <!--tw@Oreoxmt: 2 notes-->

    - 修复了处理 GBK/GB18030 编码数据时的编码问题 [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 修复了因 In-memory Engine 预加载尚未初始化的副本导致的 panic 问题 [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus]([https://github.com/overvenus]
    - (dup): release-8.1.2.md > 错误修复> TiKV - 修复 Region Split 后可能无法快速选出 Leader 的问题 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    - (dup): release-8.1.2.md > 错误修复> TiKV - 修复磁盘卡住时，TiKV 无法向 PD 上报心跳的问题 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)

+ PD <!--tw@Oreoxmt: 1 note-->

    - 修复 PD 在启用 `@@tidb_enable_tso_follower_proxy` 变量后可能出现的 Panic 问题 [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    - (dup): release-7.5.5.md > 错误修复> PD - 修复 `evict-leader-scheduler` 在使用相同 Store ID 重复创建后无法正常工作的问题 [#8756](https://github.com/tikv/pd/issues/8756) @[okJiang](https://github.com/okJiang)

+ TiFlash <!--tw@qiancai: 2 notes-->

    - (dup): release-7.5.5.md > 错误修复> TiFlash - 修复在存算分离架构下，对新增的列进行查询可能返回错误结果的问题 [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)
    - 修复 TiFlash 可能在内存占用不高的情况下，发生意外拒绝处理 Raft 消息的行为 [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复 TiFlash `Position` 函数不支持 Collation 的问题 [#9377](https://github.com/pingcap/tiflash/issues/9377) @[xzhangxian1008](https://github.com/xzhangxian1008)

+ Tools

    + Backup & Restore (BR) <!--tw@qiancai: 1 note-->

        - 修复了 PiTR 无法恢复大 Index 的问题。 [#58433](https://github.com/pingcap/tidb/pull/58433) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC <!--tw@qiancai: 5 notes-->

        - 修复在扩容出新的 TiKV 节点后 Changefeed 可能会卡住的问题 [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        - 修复 event filter 在处理 rename table DDL 时错误的使用新的表名而不是旧的表名来进行过滤的问题 [#11946](https://github.com/pingcap/tiflow/issues/11946) @[kennytm](https://github.com/kennytm)
        - 修复在删除 changefeed 后 goroutine 泄漏的问题 [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        - 修复由于 Sarama 客户端乱序重发消息导致 kafka 消息乱序的问题 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复 Debezium 协议中 not null timestamp 类型的默认值不正确的问题 [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)