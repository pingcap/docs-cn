---
title: TiDB 7.5.2 Release Notes
summary: 了解 TiDB 7.5.2 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.2 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.5.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.2#version-list)

## 兼容性变更

- note [#issue](https://github.com/pingcap/${repo-name}/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
- (dup): release-6.5.9.md > 兼容性变更 - 在 TiKV 中提供 RocksDB [`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/zh/tidb/v6.5/tikv-configuration-file#track-and-verify-wals-in-manifest-从-v659-版本开始引入) 配置，用于调查 WAL (Write Ahead Log) 可能损坏问题 [#16549](https://github.com/tikv/tikv/issues/16549) @[v01dstar](https://github.com/v01dstar)
- (dup): release-7.1.4.md > 兼容性变更 - 为减少日志打印的开销，TiFlash 配置项 `logger.level` 默认值由 `"debug"` 改为 `"info"` [#8641](https://github.com/pingcap/tiflash/issues/8641) @[JaySon-Huang](https://github.com/JaySon-Huang)

## 改进提升

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.9.md > 改进提升> TiDB - 优化 `ANALYZE` 语句卡住元数据锁的问题 [#47475](https://github.com/pingcap/tidb/issues/47475) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.1.0.md > 改进提升> TiDB - 优化表达式默认值在 `SHOW CREATE TABLE` 结果中的 MySQL 兼容性 [#52939](https://github.com/pingcap/tidb/issues/52939) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - (dup): release-8.1.0.md > 改进提升> TiDB - 增强 TiDB 对始终为 `false` 的 DNF 项的处理能力，直接忽略这种过滤条件，以避免不必要的全表扫描 [#40997](https://github.com/pingcap/tidb/issues/40997) @[hi-rustin](https://github.com/hi-rustin)
    - 优化 `EXPLAIN ANALYZE` 中 TiFlash TableScan 算子执行过程的统计信息 [#51727](https://github.com/pingcap/tidb/issues/51727) @[JinheLin](https://github.com/JinheLin)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.9.md > 改进提升> TiKV - 在 raftstore 线程中避免进行快照文件的 IO 操作，提高 TiKV 稳定性 [#16564](https://github.com/tikv/tikv/issues/16564) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-6.5.9.md > 改进提升> TiKV - 增加 peer 和 store 消息的 slow log [#16600](https://github.com/tikv/tikv/issues/16600) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.4.md > 改进提升> TiKV - 当 TiKV 检测到存在损坏的 SST 文件时，记录损坏的具体原因 [#16308](https://github.com/tikv/tikv/issues/16308) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.9.md > 改进提升> TiKV - 删除非必要的 async block 以减少内存使用 [#16540](https://github.com/tikv/tikv/issues/16540) @[overvenus](https://github.com/overvenus)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.1.5.md > 改进提升> PD - 升级 etcd 版本至 v3.4.30 [#7904](https://github.com/tikv/pd/issues/7904) @[JmPotato](https://github.com/JmPotato)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.1.0.md > 改进提升> TiFlash - 降低 TiFlash 在开启 TLS 后因更新证书而导致 panic 的概率 [#8535](https://github.com/pingcap/tiflash/issues/8535) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.1.0.md > 改进提升> Tools> Backup & Restore (BR) - BR 在恢复数据过程中，会清理空的 SST 文件 [#16005](https://github.com/tikv/tikv/issues/16005) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > 改进提升> Tools> Backup & Restore (BR) - 增加 PITR 集成测试用例，覆盖对日志备份与添加索引加速功能的兼容性测试 [#51987](https://github.com/pingcap/tidb/issues/51987) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 改进提升> Tools> Backup & Restore (BR) - 提高日志备份对 Merge 的容忍度，如果遇到合理的长时间 Merge 操作，日志备份任务不容易进入 Error 状态 [#16554](https://github.com/tikv/tikv/issues/16554) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.7.md > 改进提升> Tools> Backup & Restore (BR) - 提升了 `RESTORE` 语句在大数据量表场景下的建表性能 [#48301](https://github.com/pingcap/tidb/issues/48301) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.0.0.md > 改进提升> Tools> Backup & Restore (BR) - 支持在恢复过程中提前分配好 Table ID，从而最大限度地复用 Table ID，提升恢复性能 [#51736](https://github.com/pingcap/tidb/issues/51736) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > 改进提升> Tools> Backup & Restore (BR) - 移除日志备份启动时检查是否存在活动 DDL job 的无效检查 [#52733](https://github.com/pingcap/tidb/issues/52733) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 改进提升> Tools> Backup & Restore (BR) - 移除使用 Google Cloud Storage (GCS) 作为外部存储时一个过时的兼容性检查 [#50533](https://github.com/pingcap/tidb/issues/50533) @[lance6716](https://github.com/lance6716)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.1.0.md > 改进提升> Tools> TiCDC - 提升使用 redo log 恢复数据过程中的内存稳定性，减少 OOM 的概率 [#10900](https://github.com/pingcap/tiflow/issues/10900) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.1.0.md > 改进提升> Tools> TiCDC - 显著提升事务冲突场景中的数据同步的稳定性，性能最高提升可达 10 倍 [#10896](https://github.com/pingcap/tiflow/issues/10896) @[CharlesCheung96](https://github.com/CharlesCheung96)

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

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## 错误修复

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复添加唯一索引可能导致 TiDB panic 的问题 [#52312](https://github.com/pingcap/tidb/issues/52312) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 TiDB Server 在初始化完成之前就标记为 Health 的问题 [#51596](https://github.com/pingcap/tidb/issues/51596) @[shenqidebaozi](https://github.com/shenqidebaozi)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `IFNULL` 函数返回的类型和 MySQL 不一致的问题 [#51765](https://github.com/pingcap/tidb/issues/51765) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复并行 Apply 在表为聚簇索引时可能导致结果错误的问题 [#51372](https://github.com/pingcap/tidb/issues/51372) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复当子查询中的 `HAVING` 子句包含关联列时，查询结果可能出错的问题 [#51107](https://github.com/pingcap/tidb/issues/51107) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复查询 `TIDB_HOT_REGIONS` 表时结果返回内存表的问题 [#50810](https://github.com/pingcap/tidb/issues/50810) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复 TiDB 在统计信息初始化完成前就开始自动收集的问题 [#52346](https://github.com/pingcap/tidb/issues/52346) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复在 `AUTO_ID_CACHE=1` 时，AutoID Leader 发生变更可能造成自增列的值减少的问题 [#52600](https://github.com/pingcap/tidb/issues/52600) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复当使用 CTE（公共表达式）访问缺少统计信息的分区表时，查询结果可能出错的问题 [#51873](https://github.com/pingcap/tidb/issues/51873) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复 TiDB Dashboard 监控页面中连接数 (Connection Count) 的计算和显示错误 [#51889](https://github.com/pingcap/tidb/issues/51889) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复在恢复含有外键的表时 DDL 卡住的问题 [#51838](https://github.com/pingcap/tidb/issues/51838) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复当列的默认值被删除时，获取该列的默认值会报错的问题 [#50043](https://github.com/pingcap/tidb/issues/50043) [#51324](https://github.com/pingcap/tidb/issues/51324) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复在配置 `force-init-stats` 的情况下，TiDB 没有监听对应端口的问题 [#51473](https://github.com/pingcap/tidb/issues/51473) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `IN()` 谓词中包含 `NULL` 时，查询结果错误的问题 [#51560](https://github.com/pingcap/tidb/issues/51560) @[winoros](https://github.com/winoros)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复 TiDB 统计信息同步加载机制无限重试加载空统计信息并打印 `fail to get stats version for this histogram` 日志的问题 [#52657](https://github.com/pingcap/tidb/issues/52657) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `EXCHANGE PARTITION` 在处理外键时判断错误的问题 [#51807](https://github.com/pingcap/tidb/issues/51807) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.6.0.md > 错误修复> TiDB - 修复 `LIMIT` 可能无法推入到 `OR` 类型的 `Index Merge` 的问题 [#48588](https://github.com/pingcap/tidb/issues/48588) @[AilinKid](https://github.com/AilinKid)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复关联子查询中 TopN 算子结果不正确的问题 [#52777](https://github.com/pingcap/tidb/issues/52777) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复 `CPS by type` 监控项显示错误的问题 [#52605](https://github.com/pingcap/tidb/issues/52605) @[nolouch](https://github.com/nolouch)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复当某些列的统计信息没有完全加载时，`EXPLAIN` 语句的结果中可能会显示错误的列 ID 的问题 [#52207](https://github.com/pingcap/tidb/issues/52207) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复关闭新排序规则框架时，涉及不同排序规则的表达式可能导致查询 panic 的问题 [#52772](https://github.com/pingcap/tidb/issues/52772) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复当 SQL 语句涉及包含多值索引的表时，执行可能报错 `Can't find a proper physical plan for this query` 的问题 [#49438](https://github.com/pingcap/tidb/issues/49438) @[qw4990](https://github.com/qw4990)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 TiDB 无法正确转换表达式中系统变量类型的问题 [#43527](https://github.com/pingcap/tidb/issues/43527) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复执行 `INSERT IGNORE` 可能出现唯一索引和数据不一致的问题 [#51784](https://github.com/pingcap/tidb/issues/51784) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复自动统计信息收集在 OOM 后卡住的问题 [#51993](https://github.com/pingcap/tidb/issues/51993) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复启用 `tidb_mem_quota_analyze` 时，更新统计信息使用的内存超过限制可能导致 TiDB crash 的问题 [#52601](https://github.com/pingcap/tidb/issues/52601) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复 `max_execute_time` 多层设置相互影响的问题 [#50914](https://github.com/pingcap/tidb/issues/50914) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复使用单个 SQL 语句添加多个索引导致的索引不一致问题 [#51746](https://github.com/pingcap/tidb/issues/51746) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复窗口函数中有某些子查询时可能会 panic 的问题 [#42734](https://github.com/pingcap/tidb/issues/42734) @[hi-rustin](https://github.com/hi-rustin)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `shuffleExec` 意外退出导致 TiDB 崩溃的问题 [#48230](https://github.com/pingcap/tidb/issues/48230) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复回滚改写分区 DDL 任务时，状态卡住的问题 [#51090](https://github.com/pingcap/tidb/issues/51090) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复一些情况下查询 `BINARY` 类型的 JSON 可能会报错的问题 [#51547](https://github.com/pingcap/tidb/issues/51547) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复开启分布式执行框架后为大数据量的表添加索引不成功的问题 [#52640](https://github.com/pingcap/tidb/issues/52640) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复 TTL 功能在某些情况下因为没有正确切分数据范围而造成数据热点的问题 [#51527](https://github.com/pingcap/tidb/issues/51527) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复主键类型是 `VARCHAR` 时，执行 `ALTER TABLE ... COMPACT TIFLASH REPLICA` 可能会错误地提前结束的问题 [#51810](https://github.com/pingcap/tidb/issues/51810) @[breezewish](https://github.com/breezewish)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复添加索引期间升级集群导致数据索引不一致的问题 [#52411](https://github.com/pingcap/tidb/issues/52411) @[tangenta](https://github.com/tangenta)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复关闭 TableDual 的 Predicate 下推后，出现性能回退的问题 [#50614](https://github.com/pingcap/tidb/issues/50614) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 TiDB Server 通过 HTTP 接口添加 label 返回成功但不生效的问题 [#51427](https://github.com/pingcap/tidb/issues/51427) @[you06](https://github.com/you06)
    - (dup): release-8.1.0.md > 错误修复> TiDB - 修复 ingest 模式添加索引时，在某些特殊情况下导致数据索引不一致的问题 [#51954](https://github.com/pingcap/tidb/issues/51954) @[lance6716](https://github.com/lance6716)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复 `init-stats` 流程可能导致 TiDB panic 以及 `load stats` 流程直接退出的问题 [#51581](https://github.com/pingcap/tidb/issues/51581) @[hawkingrei](https://github.com/hawkingrei)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复当配置文件中出现不合规的配置项时，配置文件不生效的问题 [#51399](https://github.com/pingcap/tidb/issues/51399) @[Defined2014](https://github.com/Defined2014)
    - (dup): release-6.5.9.md > 错误修复> TiDB - 修复当 SQL 语句中包含 `JOIN` 且 `SELECT` 列表只包含常量时，使用 MPP 执行查询可能导致查询结果出错的问题 [#50358](https://github.com/pingcap/tidb/issues/50358) @[yibin87](https://github.com/yibin87)
    - (dup): release-8.0.0.md > 错误修复> TiDB - 修复在 `determinate` 模式下 (`tidb_opt_objective='determinate'`)，如果查询不包含谓词，可能无法加载统计信息的问题 [#48257](https://github.com/pingcap/tidb/issues/48257) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-7.1.5.md > 错误修复> TiDB - 修复某些情况下 `SHOW CREATE PLACEMENT POLICY` 语句不显示 `SURVIVAL_PREFERENCES` 属性的问题 [#51699](https://github.com/pingcap/tidb/issues/51699) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-6.5.8.md > 错误修复> TiKV - 修复巴西和埃及时区转换错误的问题 [#16220](https://github.com/tikv/tikv/issues/16220) @[overvenus](https://github.com/overvenus)
    - (dup): release-6.5.9.md > 错误修复> TiKV - 修复监控指标 `tikv_unified_read_pool_thread_count` 有时没有数据的问题 [#16629](https://github.com/tikv/tikv/issues/16629) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-6.5.9.md > 错误修复> TiKV - 修复 RocksDB 中非活跃的 WAL (Write Ahead Log) 可能损毁数据的问题 [#16705](https://github.com/tikv/tikv/issues/16705) @[Connor1996](https://github.com/Connor1996)
    - (dup): release-7.1.5.md > 错误修复> TiKV - 修复由于过时的 Region peer 忽略 GC 消息导致 resolve-ts 被阻塞的问题 [#16504](https://github.com/tikv/tikv/issues/16504) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.9.md > 错误修复> TiKV - 修复乐观事务在执行期间被其它事务发起 resolve lock 时，如果事务的 primary key 上之前有通过异步提交 (Async Commit) 或一阶段提交 (1PC) 模式提交的数据，事务的原子性可能有小概率被破坏问题 [#16620](https://github.com/tikv/tikv/issues/16620) @[MyonKeminta](https://github.com/MyonKeminta)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-7.1.5.md > 错误修复> PD - 修复写热点调度可能会违反放置策略 (placement policy) 约束的问题 [#7848](https://github.com/tikv/pd/issues/7848) @[lhy1024](https://github.com/lhy1024)
    - (dup): release-7.1.4.md > 错误修复> PD - 修复资源组 (Resource Group) 客户端中未完全删除的 slot 导致分配 token 低于给定值的问题 [#7346](https://github.com/tikv/pd/issues/7346) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.9.md > 错误修复> PD - 修复扩缩容进度显示不准确的问题 [#7726](https://github.com/tikv/pd/issues/7726) @[CabinfeverB](https://github.com/CabinfeverB)
    - (dup): release-8.1.0.md > 错误修复> PD - 修复两数据中心部署切换时 Leader 无法迁移的问题 [#7992](https://github.com/tikv/pd/issues/7992) @[TonsnakeLin](https://github.com/TonsnakeLin)
    - (dup): release-8.1.0.md > 错误修复> PD - 修复 PD 的 `Filter target` 监控指标未提供 scatter range 信息的问题 [#8125](https://github.com/tikv/pd/issues/8125) @[HuSharp](https://github.com/HuSharp)
    - (dup): release-6.5.9.md > 错误修复> PD - 修复 `SHOW CONFIG` 的查询结果包含已废弃的 `trace-region-flow` 配置项的问题 [#7917](https://github.com/tikv/pd/issues/7917) @[rleungx](https://github.com/rleungx)

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
    - (dup): release-8.1.0.md > 错误修复> TiFlash - 修复存算分离架构下，TiFlash 计算节点进程停止时可能出现 panic 的问题 [#8860](https://github.com/pingcap/tiflash/issues/8860) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.1.5.md > 错误修复> TiFlash - 修复查询生成列出错的问题 [#8787](https://github.com/pingcap/tiflash/issues/8787) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-8.1.0.md > 错误修复> TiFlash - 修复从低于 v6.5.0 的集群升级到 v6.5.0 及以上版本后，可能出现 TiFlash 元数据损坏以及进程 panic 的问题 [#9039](https://github.com/pingcap/tiflash/issues/9039) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-6.5.9.md > 错误修复> TiFlash - 修复 `ENUM` 列在 chunk encode 时可能会导致 TiFlash crash 的问题 [#8674](https://github.com/pingcap/tiflash/issues/8674) @[yibin87](https://github.com/yibin87)
    - (dup): release-7.1.5.md > 错误修复> TiFlash - 修复日志中 `local_region_num` 数值错误的问题 [#8895](https://github.com/pingcap/tiflash/issues/8895) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.0.0.md > 错误修复> TiFlash - 修复存算分离架构下，TiFlash 关闭过程中可能 panic 的问题 [#8837](https://github.com/pingcap/tiflash/issues/8837) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - (dup): release-8.1.0.md > 错误修复> TiFlash - 修复 TiFlash 在高并发读的情况下，可能返回瞬时不正确结果的问题 [#8845](https://github.com/pingcap/tiflash/issues/8845) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-8.1.0.md > 错误修复> TiFlash - 修复存算分离架构下，修改 TiFlash 计算节点 `storage.remote.cache.capacity` 配置项的值后，Grafana 中硬盘使用量监控指标 `used_size` 显示不正确的问题 [#8920](https://github.com/pingcap/tiflash/issues/8920) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-8.0.0.md > 错误修复> TiFlash - 修复存算分离架构下，出现网络隔离后查询可能会被永久阻塞的问题 [#8806](https://github.com/pingcap/tiflash/issues/8806) @[JinheLin](https://github.com/JinheLin)
    - (dup): release-6.5.9.md > 错误修复> TiFlash - 修复在非严格 `sql_mode` 下插入数据到带有异常默认值的列可能导致 TiFlash panic 的问题 [#8803](https://github.com/pingcap/tiflash/issues/8803) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复在小概率情况下，由于特殊的事件时序导致日志备份数据丢失的问题 [#16739](https://github.com/tikv/tikv/issues/16739) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-6.5.9.md > 错误修复> Tools> Backup & Restore (BR) - 修复全量备份失败时打印过多日志的问题 [#51572](https://github.com/pingcap/tidb/issues/51572) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复 PD 连接失败导致日志备份 advancer owner 所在的 TiDB 可能崩溃的问题 [#52597](https://github.com/pingcap/tidb/issues/52597) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复因 TiKV 重启，日志备份的 global checkpoint 推进提前于实际备份文件写入点，可能导致少量备份数据丢失的问题 [#16809](https://github.com/tikv/tikv/issues/16809) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-8.1.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复恢复暂停的日志备份任务时，如果与 PD 的网络连接不稳定可能导致 TiKV panic 的问题 [#17020](https://github.com/tikv/tikv/issues/17020) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.5.md > 错误修复> Tools> Backup & Restore (BR) - 修复一个不稳定的测试用例 [#52547](https://github.com/pingcap/tidb/issues/52547) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-8.1.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复在 BR 恢复数据或 TiDB Lightning 物理导入模式下导入数据时，从 PD 获取到的 Region 没有 Leader 的问题 [#51124](https://github.com/pingcap/tidb/issues/51124) [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 错误修复> Tools> Backup & Restore (BR) - 修复在某些极端情况下，全量备份因找不到 peer 导致 TiKV panic 的问题 [#16394](https://github.com/tikv/tikv/issues/16394) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-6.5.9.md > 错误修复> Tools> Backup & Restore (BR) - 修复在日志备份任务被暂停后，移除任务无法立即恢复 GC safepoint 的问题 [#52082](https://github.com/pingcap/tidb/issues/52082) @[3pointer](https://github.com/3pointer)

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复 PD 磁盘 IO 延迟较大导致 TiCDC 同步大幅延迟的问题 [#9054](https://github.com/pingcap/tiflow/issues/9054) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复调用驱逐 TiCDC owner 节点的 API (`/api/v2/owner/resign`) 导致 TiCDC 任务意外重启的问题 [#10781](https://github.com/pingcap/tiflow/issues/10781) @[sdojjy](https://github.com/sdojjy)
        - (dup): release-6.5.9.md > 错误修复> Tools> TiCDC - 修复在频繁执行 DDL 的场景中，由于错误的 BarrierTS 导致数据被写入到错误的 CSV 文件的问题 [#10668](https://github.com/pingcap/tiflow/issues/10668) @[lidezhu](https://github.com/lidezhu)
        - (dup): release-7.1.4.md > 错误修复> Tools> TiCDC - 修复 TiCDC 在开启单行数据正确性校验后由于时区不匹配导致 `TIMESTAMP` 类型 checksum 验证失败的问题 [#10573](https://github.com/pingcap/tiflow/issues/10573) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.9.md > 错误修复> Tools> TiCDC - 修复当对象存储遇到暂时故障时，启用了最终一致性功能的 changefeed 可能直接失败的问题 [#10710](https://github.com/pingcap/tiflow/issues/10710) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复没有正确同步 `DROP PRIMARY KEY` 和 `DROP UNIQUE KEY` 的问题 [#10890](https://github.com/pingcap/tiflow/issues/10890) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-6.5.9.md > 错误修复> Tools> TiCDC - 修复在调度表的同步任务时 TiCDC panic 的问题 [#10613](https://github.com/pingcap/tiflow/issues/10613) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复当下游 Pulsar 下线后，移除 changefeed 会导致 TiCDC 正常流程卡住，从而引起其他 changefeed 进度卡住的问题 [#10629](https://github.com/pingcap/tiflow/issues/10629) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复重启 PD 可能导致 TiCDC 节点报错重启的问题 [#10799](https://github.com/pingcap/tiflow/issues/10799) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-6.5.9.md > 错误修复> Tools> TiCDC - 修复 `open-protocol` 的 old value 部分错误地按照 `STRING` 类型而非真正类型输出默认值的问题 [#10803](https://github.com/pingcap/tiflow/issues/10803) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiCDC - 修复 `TIMEZONE` 类型的值没有按照正确的时区设置默认值的问题 [#10931](https://github.com/pingcap/tiflow/issues/10931) @[3AceShowHand](https://github.com/3AceShowHand)
        - (dup): release-7.1.5.md > 错误修复> Tools> TiCDC - 修复上游写入 `Exchange Partition ... With Validation` DDL 后，TiCDC 向下游执行该 DDL 时失败，导致 changefeed 卡住的问题 [#10859](https://github.com/pingcap/tiflow/issues/10859) @[hongyunyan](https://github.com/hongyunyan)
        - (dup): release-6.5.9.md > 错误修复> Tools> TiCDC - 修复 KV Client 数据争用导致 TiCDC panic 的问题 [#10718](https://github.com/pingcap/tiflow/issues/10718) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.9.md > 错误修复> Tools> TiDB Data Migration (DM) - 修复上游为 binary 类型主键时丢失数据的问题 [#10672](https://github.com/pingcap/tiflow/issues/10672) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - (dup): release-6.5.8.md > 错误修复> Tools> TiDB Lightning - 修复 EBS BR 运行时 TiDB Lightning 可能导入失败的问题 [#49517](https://github.com/pingcap/tidb/issues/49517) @[mittalrishabh](https://github.com/mittalrishabh)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 导入数据时，因源文件存在不兼容的 SQL 语句而报 `no database selected` 的问题 [#51800](https://github.com/pingcap/tidb/issues/51800) @[lance6716](https://github.com/lance6716)
        - (dup): release-8.1.0.md > 错误修复> Tools> TiDB Lightning - 修复 TiDB Lightning 导入数据时，kill PD Leader 会导致 `invalid store ID 0` 报错的问题 [#50501](https://github.com/pingcap/tidb/issues/50501) @[Leavrth](https://github.com/Leavrth)
        - (dup): release-7.1.5.md > 错误修复> Tools> TiDB Lightning - 修复导入 Parquet 格式的空表时，TiDB Lightning panic 的问题 [#52518](https://github.com/pingcap/tidb/issues/52518) @[kennytm](https://github.com/kennytm)

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

    + TiDB Binlog

        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb-binlog/issues/${issue-id}) @[贡献者 GitHub ID](https://github.com/${github-id})

## Other dup notes

- (dup): release-7.6.0.md > # 稳定性 * 跨数据库绑定执行计划 [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990)