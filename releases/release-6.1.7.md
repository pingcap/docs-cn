---
title: TiDB 6.1.7 Release Notes
summary: 了解 TiDB 6.1.7 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.1.7 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.1.7

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.7#version-list)

## 兼容性变更

- note [#issue](链接) @[贡献者 GitHub ID](链接)

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - (dup): release-6.6.0.md > 改进提升> Tools> TiCDC - 支持 Batch UPDATE DML 语句，提升 TiCDC 的同步性能 [#8084](https://github.com/pingcap/tiflow/issues/8084) @[amyangfei](https://github.com/amyangfei)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - (dup): release-7.2.0.md > 改进提升> Tools> TiDB Lightning - 数据导入完成后使用 SQL 方式校验 checksum，提升数据校验的稳定性 [#41941](https://github.com/pingcap/tidb/issues/41941) @[GMHDBJD](https://github.com/GMHDBJD)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - 修复包含 CTE 的查询可能导致的磁盘可用空间不足的问题 [#44477](https://github.com/pingcap/tidb/issues/44477) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复某些情况下 CTE 查询结果出错的问题 [#44649](https://github.com/pingcap/tidb/issues/44649) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 select cast(n as char)，当 n 为负数时，查询结果出错的问题 [#44786](https://github.com/pingcap/tidb/issues/44786) @[xhebox](https://github.com/xhebox)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - (dup): release-6.5.2.md > 错误修复> TiDB - 修复缓存表执行新增列操作后，新增列值为 `NULL` 而非列的默认值的问题 [#42928](https://github.com/pingcap/tidb/issues/42928) @[lqs](https://github.com/lqs)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复分区表在 Index Join 的 probe 阶段找不到对应行而报错的问题 [#43686](https://github.com/pingcap/tidb/issues/43686) @[AilinKid](https://github.com/AilinKid) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复删除数据库导致 GC 推进慢的问题 [#33069](https://github.com/pingcap/tidb/issues/33069) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复 `ON UPDATE` 语句没有正确更新主键导致数据索引不一致的问题 [#44565](https://github.com/pingcap/tidb/issues/44565) @[zyguan](https://github.com/zyguan)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复在重命名表期间 TiCDC 可能丢失部分行变更的问题 [#43338](https://github.com/pingcap/tidb/issues/43338) @[tangenta](https://github.com/tangenta)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复 Placement Rule 在分区表下的行为问题，使得删除的分区 Placement Rule 可以被正确设置并回收 [#44116](https://github.com/pingcap/tidb/issues/44116) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复当 `tidb_scatter_region` 变量设置为开启时，对某个分区进行 TRUNCATE 操作后没有自动分裂 Region 的问题 [#43174](https://github.com/pingcap/tidb/issues/43174) [#43028](https://github.com/pingcap/tidb/issues/43028) @[jiyfhust](https://github.com/jiyfhust)
    - (dup): release-6.5.2.md > 错误修复> TiDB - 修复分区特别多并且带有 TiFlash 副本的分区表在执行 `TRUNCATE TABLE` 时，出现写冲突导致 DDL 重试的问题 [#42940](https://github.com/pingcap/tidb/issues/42940) @[mjonss](https://github.com/mjonss)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复窗口函数计算下推到 TiFlash 时执行计划构造错误的问题 [#43922](https://github.com/pingcap/tidb/issues/43922) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复在带有非关联子查询的语句中使用公共表表达式 (CTE) 可能导致结果错误的问题 [#44051](https://github.com/pingcap/tidb/issues/44051) @[winoros](https://github.com/winoros)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复 `memTracker` 配合 cursor fetch 使用导致内存泄漏的问题 [#44254](https://github.com/pingcap/tidb/issues/44254) @[YangKeao](https://github.com/YangKeao)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复 `INFORMATION_SCHEMA.DDL_JOBS` 表中 `QUERY` 列的数据长度可能超出列定义的问题 [#42440](https://github.com/pingcap/tidb/issues/42440) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复 `min, max` 查询结果出错的问题 [#43805](https://github.com/pingcap/tidb/issues/43805) @[wshwsh12](https://github.com/wshwsh12)
    - (dup): release-7.1.0.md > 错误修复> TiDB - 修复 analyze 表时报语法错误的问题 [#43392](https://github.com/pingcap/tidb/issues/43392) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复 `SHOW PROCESSLIST` 语句无法显示子查询时间较长语句的事务的 TxnStart 的问题 [#40851](https://github.com/pingcap/tidb/issues/40851) @[crazycs520](https://github.com/crazycs520)
    - (dup): release-6.5.2.md > 错误修复> TiDB - 修复对于执行中的 `DROP TABLE` 操作，`ADMIN SHOW DDL JOBS` 的结果中缺少表名的问题 [#42268](https://github.com/pingcap/tidb/issues/42268) @[tiancaiamao](https://github.com/tiancaiamao)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复 IPv6 环境下显示错误的 TiDB 地址的问题 [#43260](https://github.com/pingcap/tidb/issues/43260) @[nexustar](https://github.com/nexustar)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复在使用 `AES_DECRYPT` 表达式时，SQL 报错 `runtime error: index out of range` 的问题 [#43063](https://github.com/pingcap/tidb/issues/43063) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复在创建分区表时使用 `SUBPARTITION` 没有警告提醒的问题 [#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @[mjonss](https://github.com/mjonss)
    - (dup): release-7.2.0.md > 错误修复> TiDB - 修复使用 CTE 的查询导致 TiDB 卡住的问题 [#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @[guo-shaoge](https://github.com/guo-shaoge)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复在 TRUNCATE 分区表的某个分区时可能造成分区的 Placement Rule 失效的问题 [#44031](https://github.com/pingcap/tidb/issues/44031) @[lcwangchao](https://github.com/lcwangchao)
    - (dup): release-6.5.3.md > 错误修复> TiDB - 修复在谓词下推的情况下 CTE 结果错误的问题 [#43645](https://github.com/pingcap/tidb/issues/43645) @[winoros](https://github.com/winoros)
    - (dup): release-6.3.0.md > 错误修复> TiDB>- 修复与自动提交 (auto-commit) 模式更改相关的事务提交行为 [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - (dup): release-6.5.3.md > 错误修复> TiKV - 修复 TiDB Lightning 可能导致 SST 文件泄露的问题 [#14745](https://github.com/tikv/tikv/issues/14745) @[YuJuncen](https://github.com/YuJuncen)
    - (dup): release-6.5.3.md > 错误修复> TiKV - 修复加密 Key ID 冲突会导致旧 Key 被删除的问题 [#14585](https://github.com/tikv/tikv/issues/14585) @[tabokie](https://github.com/tabokie)
    - (dup): release-6.5.3.md > 错误修复> TiKV - 修复 Continuous Profiling 中的文件句柄泄露的问题 [#14224](https://github.com/tikv/tikv/issues/14224) @[tabokie](https://github.com/tabokie)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - (dup): release-7.2.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复某些情况下误报 `resolved lock timeout` 的问题 [#43236](https://github.com/pingcap/tidb/issues/43236) @[YuJuncen](https://github.com/YuJuncen)
        - (dup): release-7.1.0.md > 错误修复> Tools> Backup & Restore (BR) - 修复集群中 TiKV 出现宕机导致备份速度降低的问题 [#42973](https://github.com/pingcap/tidb/issues/42973) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - (dup): release-7.2.0.md > 错误修复> Tools> TiCDC - 修复 TiCDC 同步到 Kafka-on-Pulsar 时不能正确建立连接的问题 [#8892](https://github.com/pingcap/tiflow/issues/8892) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): release-7.1.0.md > 错误修复> Tools> TiCDC - 修复 PD 地址或 leader 出现故障时 TiCDC 不能自动恢复的问题 [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)
        - (dup): release-6.5.3.md > 错误修复> Tools> TiCDC - 修复当下游为 Kafka 时，TiCDC 查询下游的元信息频率过高导致下游负载过大的问题 [#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @[hi-rustin](https://github.com/hi-rustin)
        - (dup): release-6.5.3.md > 错误修复> Tools> TiCDC - 修复 PD 出现网络隔离或 PD Owner 节点重启等故障时 TiCDC 卡住问题 [#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @[asddongmen](https://github.com/asddongmen)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - (dup): release-6.5.3.md > 错误修复> Tools> TiDB Lightning - 修复宽表导入时可能出现 OOM 的问题 [#43728](https://github.com/pingcap/tidb/issues/43728) @[D3Hunter](https://github.com/D3Hunter)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Binlog

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)
