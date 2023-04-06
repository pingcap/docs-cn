---
title: TiDB 6.1.6 Release Notes
summary: 了解 TiDB 6.1.6 版本的兼容性变更、改进提升，以及错误修复。
---

# TiDB 6.1.6 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：6.1.6

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v6.1.6#version-list)

## 兼容性变更

- 兼容性变更 1

## 提升改进

+ TiDB
	- Prepare Plan Cache 可以缓存 BatchPointGet 计划 [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
	- Index Join 支持更多的模式 [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)

+ TiKV

    - (dup): release-6.6.0.md > 提升改进> TiKV - 支持在小于 1 core 的 CPU 下启动 TiKV [#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Binlog

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

## Bug 修复

+ TiDB

    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复 `ignore_plan_cache` hint 对 INSERT 语句可能不生效的问题 [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复了 `indexMerge` 遇到错误后可能会导致 TiDB 崩溃的问题 [#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复错误下推包含虚拟列的 TopN 算子到 TiKV 或 TiFlash 导致结果错误的问题 [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - (dup): release-6.6.0.md > Bug 修复> TiDB - 修复了使用 `Prepare` 或 `Execute` 查询某些虚拟表时无法将表 ID 下推，导致在大量 Region 的情况下 PD OOM 的问题 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复 Plan Cache 处理 `int_col in (decimal...)` 条件时可能缓存 FullScan 计划的问题 [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复 IndexMerge 计划在 SET 类型列上可能生成错误区间的问题 [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复了无符号的 `TINYINT`/`SMALLINT`/`INT` 和小于 `0` 的 `DECIMAL`/`FLOAT`/`DOUBLE` 类型比较时，结果可能出错的问题 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - (dup): release-5.4.1.md > Bug 修复> TiDB - 修复了查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表导致 TiDB 服务器 OOM 的问题，在 Grafana dashboard 中查看慢查询记录的时候可能会触发该问题 [#33893](https://github.com/pingcap/tidb/issues/33893)
    - (dup): release-5.1.5.md > Bug 修复> TiDB - 修复 Range 分区允许多个 `MAXVALUE` 分区的问题 [#36329](https://github.com/pingcap/tidb/issues/36329)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复 Plan Cache 可能缓存 Shuffle 算子导致返回错误结果的问题 [#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复了时区中的数据争用可能导致数据和索引不一致问题 [#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - (dup): release-6.5.1.md > Bug 修复> TiDB - 修复了 `indexMerge` 中可能会出现 goroutine 泄露的问题 [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复在使用 Cursor Fetch 且在 Execute、Fetch、Close 之间运行其它语句后，Fetch 与 Close 命令可能会返回错误结果或造成 TiDB Panic 的问题 [#40094](https://github.com/pingcap/tidb/issues/40094) [@YangKeao](https://github.com/YangKeao)
    - 修复了 DDL 在修改浮点类型，保持长度不变且减少小数位时旧数据仍然保持原样的问题 [#41281](https://github.com/pingcap/tidb/issues/41281) [@zimulala](https://github.com/zimulala)
    - 修复了 Join `information_schema.columns` 表会造成 TiDB panic 的问题 [#32459](https://github.com/pingcap/tidb/issues/32459) [@tangenta](https://github.com/tangenta)
    - 修复了生成执行计划过程中，因为获取的 Info Schema 不一致而导致的 TiDB panic [#41622](https://github.com/pingcap/tidb/issues/41622) [@tiancaiamao](https://github.com/tiancaiamao)
    - 修复有虚拟生成列的表在使用 TiFlash 副本读取时，可能会抛出错误的问题 [#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复读取 LIST PARTITION 的表时可能抛出错误的问题 [#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - 修复 prepare plan cache 开启时，包含 Window Function 的 SQL 执行结果可能错误的问题 [#38335](https://github.com/pingcap/tidb/issues/38335) @[fzzf678](https://github.com/fzzf678)
    - 修复使用 Index Merge 的方式读取包含 SET 类型的列的表时，结果可能出错的问题 [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - 修复 prepare plan cache 开启时，使用 Index 扫全表的 SQL 在执行时可能会抛出 panic 的问题 [#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - 修复当 DDL 执行过程中，使用 PointGet 读取表的 SQL 可能会在执行时抛出 panic 的问题 [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)

+ TiKV

    - (dup): release-6.6.0.md > Bug 修复> TiKV - 修复转换 `const Enum` 类型到其他类型时报错的问题 [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)

+ PD

    - (dup): release-6.5.1.md > Bug 修复> PD - 修复 Region Scatter 接口可能导致 leader 分布不均匀的问题 [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    - 修复 Online recovery 超时不生效的问题 @[v01dstar](https://github.com/v01dstar)

+ TiFlash

    - (dup): release-6.6.0.md > Bug 修复> TiFlash - 修复半连接在计算笛卡尔积时，使用内存过量的问题 [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - (dup): release-6.5.1.md > Bug 修复> TiFlash - 修复 TiFlash 日志搜索过慢的问题 [#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - 修复 `CI Collation` 下聚合函数结果不正确的问题 [#7002](https://github.com/pingcap/tiflash/pull/7002) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 `Decimal Cast` 结果不正确的问题 [#7026](https://github.com/pingcap/tiflash/pull/7026) @[windtalker](https://github.com/windtalker)
    - 修复不能识别生成列的问题 [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复 `Decimal` 的舍入问题 [#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)

+ Tools

    + Backup & Restore (BR)

    + TiCDC
        - 修复同步数据时由于 `Update` 和 `Insert` 语句乱序可能导致的 `Duplicate entry` 错误问题 [#8635](https://github.com/pingcap/tiflow/pull/8635) @[sdojjy](https://github.com/sojjy)
        - 修复 `float32` 类型解析错误导致的浮点数精度丢失问题 [#8519](https://github.com/pingcap/tiflow/pull/8519) @[3AceShowHand](https://github.com/3AceShowHand)
        - 修复由 PD 和 TiCDC 之间网络隔离引起的 TiCDC 程序异常退出的问题 [#8462](https://github.com/pingcap/tiflow/pull/8642) @[overvenus](https://github.com/overvenus)
        - 修复在同步没有主键且包含非空唯一索引的表时，可能导致的数据丢失问题 [#8420](https://github.com/pingcap/tiflow/issues/8420) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - 修复 `db sorter` 使用内存没有正确受到 `cgroup memory limit` 限制的问题 [#8623](https://github.com/pingcap/tiflow/pull/8623) @[amyangfei](https://github.com/amyangfei)
        - 优化 `cdc cli` 在遇到非法输入时的错误提示。 [#8442](https://github.com/pingcap/tiflow/pull/8442) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.6.0.md > Bug 修复> Tools> TiCDC - 修复 redo log 容忍 S3 存储故障的时间过短的问题 [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - (dup): release-6.5.1.md > Bug 修复> Tools> TiCDC - 修复在 PD 异常时，暂停一个 changefeed 会错误设置状态的问题 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)

    + TiDB Binlog

    + TiDB Data Migration (DM)

    + TiDB Lightning

        - (dup): release-6.6.0.md > Bug 修复> Tools> TiDB Lightning - 修复冲突处理逻辑 (`duplicate-resolution`) 可能导致 checksum 不一致的问题 [#40657](https://github.com/pingcap/tidb/issues/40657) @[gozssky](https://github.com/gozssky)
        - (dup): release-6.6.0.md > Bug 修复> Tools> TiDB Lightning - 修复 TiDB Lightning 在 split-region 阶段发生 panic 的问题 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - (dup): release-6.5.1.md > Bug 修复> Tools> TiDB Lightning - 修复了在使用 Local Backend 模式导入数据时，当导入目标表的复合主键中存在 `auto_random` 列，且源数据中没有指定该列的值时，相关列没有自动生成数据的问题 [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - (dup): release-6.6.0.md > Bug 修复> Tools> TiDB Lightning - 修复在并行导入时，当除最后一个 TiDB Lightning 实例外的其他实例都遇到本地重复记录时，TiDB Lightning 可能会错误地跳过冲突处理的问题 [#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)

    + Dumpling
