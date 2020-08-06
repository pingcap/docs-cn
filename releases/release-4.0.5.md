---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 Release Notes

发版日期：2020 年 8 月 11 日

TiDB 版本：4.0.5

## 兼容性变化

+ TiDB

    - 

## 新功能

+ TiFlash

    - 支持与 TiDB 统一的 log 格式。[#977](https://github.com/pingcap/tics/pull/977), [#978](https://github.com/pingcap/tics/pull/978)


+ Tools

    - TiCDC

        - 支持加密 Kafka 链接 [#764](https://github.com/pingcap/ticdc/pull/764)
        - 支持输出 old value [#708](https://github.com/pingcap/ticdc/pull/708)
        - 添加列的特征的标识 [#796](https://github.com/pingcap/ticdc/pull/796)
        - 支持输出上一版本的 DDL 和表结构 [#799](https://github.com/pingcap/ticdc/pull/799)


## 优化提升

+ TiDB

    - 优化 `Union` 场景下 `DecodePlan` 的开销 [#18941](https://github.com/pingcap/tidb/pull/18941)
    - 减少 GC 在遇到 region miss 时 scan lock 的次数 [#18876](https://github.com/pingcap/tidb/pull/18876)
    - 减少统计信息 feedback 对集群性能的影响 [#18772](https://github.com/pingcap/tidb/pull/18772)
    - 支持在 RPC 请求返回结果前取消操作. [#18580](https://github.com/pingcap/tidb/pull/18580)
    - 支持使用 HTTP API 生成带有相关监控项名称的 profile. [#18531](https://github.com/pingcap/tidb/pull/18531)
    - 支持分区表的预打散功能. [#17863](https://github.com/pingcap/tidb/pull/17863)
    - 在监控面板中显示每个实例的内存使用详情.
    - 在 `EXPLAIN` 中显示 `BatchPointGet` 算子的详细运行信息 [#18892](https://github.com/pingcap/tidb/pull/18892)
    - 在 `EXPLAIN` 中显示 `PointGet` 算子的详细运行信息 [#18817](https://github.com/pingcap/tidb/pull/18817)
    - 解决 `MemTracker` 潜在的死锁问题 [#18395](https://github.com/pingcap/tidb/pull/18395)
    - 提高字符串转换为整数类型和小数类型的兼容性，支持将 json 转换为时间日期类型. [#18159](https://github.com/pingcap/tidb/pull/18159)
    - 支持限制 `TableReader` 算子内存使用. [#18392](https://github.com/pingcap/tidb/pull/18392)
    - 在 `batch cop` 请求重试时避免多次 backoff [#18999](https://github.com/pingcap/tidb/pull/18999)

+ PD

    - 支持打散特殊存储引擎节点（例如 TiFlash）上的 Region [#2706](https://github.com/pingcap/pd/pull/2706)
    - 支持通过 API 指定某范围内的 Region 优先进行调度 [#2687](https://github.com/pingcap/pd/pull/2687)
    - 优化 Region 打散操作，使得 Leader 分布更均匀 [#2684](https://github.com/pingcap/pd/pull/2684)
    - 针对 TSO 请求添加更多测试和日志 [#2678](https://github.com/pingcap/pd/pull/2678)
    - 避免 Region Leader 变化时可能产生的不必要的缓存更新 [#2672](https://github.com/pingcap/pd/pull/2672)

+ TiKV

    - 

+ TiFlash

    - 添加更多的 Grafana 监控面板，比如 CPU/IO/RAM 使用量，以及存储引擎的各项指标等。[#965](https://github.com/pingcap/tics/pull/965)
    - 通过优化 Raft logs 的处理逻辑，减少 IO 操作。[#960](https://github.com/pingcap/tics/pull/960)
    - 加快 add partition ddl 之后 region 的调度性能。[#959](https://github.com/pingcap/tics/pull/959)
    - 优化 DeltaTree 引擎中 delta 数据的整理，减少读写放大。[#952](https://github.com/pingcap/tics/pull/952)
    - 通过使用多线程对 region snapshot 进行预处理，优化 apply 性能。[#944](https://github.com/pingcap/tics/pull/944)

+ Tools

    + TiCDC

        - 减少了取时间戳的频率 [#801](https://github.com/pingcap/ticdc/pull/801)

    + Backup & Restore (BR)

        - 优化了日志 [#428](https://github.com/pingcap/br/pull/428)

    + Dumpling

        - 减少导出 MySQL 时持锁的时间 [#121](https://github.com/pingcap/dumpling/pull/121)

    + TiDB Lightning

        - 优化了日志 [#352](https://github.com/pingcap/tidb-lightning/pull/352)


## Bug 修复

+ TiDB

    - 修复 `builtinCastRealAsDecimalSig` 函数中未正确处理 `ErrTruncate/Overflow` 错误导致报 "should ensure all columns have the same length" 错误的问题. [#18967](https://github.com/pingcap/tidb/pull/18967)
    - 修复 `pre_split_regions` 对分区表不生效的问题. [#18837](https://github.com/pingcap/tidb/pull/18837)
    - 修复大事务提前终止的问题. [#18813](https://github.com/pingcap/tidb/pull/18813)
    - 修复使用 `collation` 相关函数查询结果错误的问题. [#18735](https://github.com/pingcap/tidb/pull/18735)
    - 修复 `getAutoIncrementID()` 函数逻辑错误导致导出工具报 'table not exist' 错误的问题. [#18692](https://github.com/pingcap/tidb/pull/18692)
    - 修复 `select a from t having t.a` 报 `unknown column error` 的问题.  [#18434](https://github.com/pingcap/tidb/pull/18434)
    - 修复 hash 分区表分区键为整数类型时，写入64位无符号类型导致溢出 panic 的问题. [#18186](https://github.com/pingcap/tidb/pull/18186)
    - 修复 `char` 函数行为错误的问题. [#18122](https://github.com/pingcap/tidb/pull/18122)
    - 修复 `ADMIN REPAIR TABLE` 无法解析 range 分区表表达式中整数的问题 [#17988](https://github.com/pingcap/tidb/pull/17988)
    - 修复 `SET CHARSET` 行为不正确的问题 [#17289](https://github.com/pingcap/tidb/pull/17289)
    - 修复由于错误的设置 collation 导致 `collation` 函数返回错误结果的问题 [#17231](https://github.com/pingcap/tidb/pull/17231)
    - 修复 `STR_TO_DATE` 和 MySQL 行为不一致的问题 [#18727](https://github.com/pingcap/tidb/pull/18727)
    - 修复 `cluster_info` 表中，TiDB 版本和 PD/TiKV 不一致的问题. [#18413](https://github.com/pingcap/tidb/pull/18413)
    - 修复悲观事务未能检查出重复数据导致可以重复写入冲突数据的问题. [#19004](https://github.com/pingcap/tidb/pull/19004)
    - 修复 `union select for update` 存在并发竞态的问题 . [#19006](https://github.com/pingcap/tidb/pull/19006)

+ PD

    - 修复 PD leader 切换时可能导致一段时间内 TSO 不可用的问题 [#2666](https://github.com/pingcap/pd/pull/2666)
    - 修复开启 Placement Rule 时，某些情况下 Region 无法调度至最佳状态的问题 [#2720](https://github.com/pingcap/pd/pull/2720)

+ TiKV

    - 

+ TiFlash

    - 

+ Tools

    + TiCDC

        - 解决了同步任务不能被移除的问题 [#782](https://github.com/pingcap/ticdc/pull/782)
        - 修正了错误的删除事件 [#787](https://github.com/pingcap/ticdc/pull/787)
        - 解决了已停止的同步任务会卡住 GC 的问题 [#797](https://github.com/pingcap/ticdc/pull/797)
        - 解决了网络阻塞导致同步任务不能退出的问题 [#825](https://github.com/pingcap/ticdc/pull/825)

    + TiDB Lightning

        - 解决了 TiDB backend 遇到空 binary/hex 的时候出现语法错误的问题 [#357](https://github.com/pingcap/tidb-lightning/pull/357)
