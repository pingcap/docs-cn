---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

发版日期：2021 年 6 月 9 日

TiDB 版本：5.0.2

## 兼容性更改

+ Tools

    + TiCDC

        - 在 `cdc cli changefeed` 命令中废弃 `--sort-dir` 参数，用户需在 `cdc server` 命令中设定 `--sort-dir` [#1795](https://github.com/pingcap/ticdc/pull/1795)

## 新功能

## 提升改进

+ TiDB

    - 当内存中的统计信息缓存是最新的时，避免后台作业频繁读取 `mysql.stats_histograms` 表造成高 CPU 使用率 [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiFlash

    - 通过摄取文件来进行 Apply Region snapshots 操作以减少内存占用
    - 优化锁操作以避免 DDL 语句和读数据相互阻塞
    - 支持 `INTEGER` 和 `REAL` 类型转化为 `REAL` 类型

+ Tools

    + TiCDC

        - 添加关于数据表内存使用情况的监控 [#1885](https://github.com/pingcap/ticdc/pull/1885)
        - 优化排序阶段的内存和 CPU 使用 [#1863](https://github.com/pingcap/ticdc/pull/1863)
        - 删除了一些可能让用户困惑的日志信息 [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        - 优化了一些含糊的报错信息使其更清晰 [#1132](https://github.com/pingcap/br/pull/1132)
        - 支持检查备份的版本信息 [#1091](https://github.com/pingcap/br/pull/1091)
        - 支持备份和恢复 `mysql` schema 下的系统表 [#1143](https://github.com/pingcap/br/pull/1143) [#1078](https://github.com/pingcap/br/pull/1078)

    + Dumpling

        - 修复备份失败却没有错误输出的问题 [#280](https://github.com/pingcap/dumpling/pull/280)

## Bug 修复

+ TiDB

    - 修复了在某些情况下，使用前缀索引和 Index Join 导致的 panic 的问题 [#24824](https://github.com/pingcap/tidb/pull/24824)
    - 修复了 `point get` 的 prepare plan cache 被事务中的 `point get` 语句不正确使用的问题 [#24765](https://github.com/pingcap/tidb/pull/24765)
    - 修复了当排序规则为 `ascii_bin` 或 `latin1_bin` 时，写入错误的前缀索引值的问题 [#24680](https://github.com/pingcap/tidb/pull/24680)
    - 修复了正在执行的事务被 GC worker 中断的问题 [#24652](https://github.com/pingcap/tidb/pull/24652)
    - 修复了当 `new-collation` 开启且 `new-row-format` 关闭的情况下，点查在聚簇索引下可能出错的问题 [#24611](https://github.com/pingcap/tidb/pull/24611)
    - 为 Shuffle Hash Join 重构分区键的转换功能 [#24490](https://github.com/pingcap/tidb/pull/24490)
    - 修复了当查询包含 `HAVING` 子句时，在构建计划的过程中 panic 的问题 [#24489](https://github.com/pingcap/tidb/pull/24489)
    - 修复了列裁剪优化导致 Apply 算子和 Join 算子执行结果错误的问题 [#24437](https://github.com/pingcap/tidb/pull/24437)
    - 修复了 Async Commit 回退导致的主锁无法清除的问题 [#24397](https://github.com/pingcap/tidb/pull/24397)
    - 修复了统计信息 GC 的一个问题，该问题可能导致重复的 fm-sketch 记录 [#24357](https://github.com/pingcap/tidb/pull/24357)
    - 当悲观锁事务收到 `ErrKeyExists` 错误时，避免不必要的悲观事务回滚 [#23800](https://github.com/pingcap/tidb/pull/23800)
    - 修复了当 sql_mode 包含 `ANSI_QUOTES` 时，数值字面值无法被识别的问题 [#25015](https://github.com/pingcap/tidb/pull/25015)
    - 禁止如 `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` 的语句从 non-listed partitions 读取数据 [#25000](https://github.com/pingcap/tidb/pull/25000)
    - 修复了当 SQL 语句包含 `GROUP BY` 以及 `UNION` 时，可能会出现的 `index out of range` 的问题 [#24551](https://github.com/pingcap/tidb/pull/24551)
    - 修复了 `CONCAT` 函数错误处理排序规则的问题 [#24301](https://github.com/pingcap/tidb/pull/24301)
    - 修复了全局变量 `collation_server` 对新会话无法生效的问题 [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiFlash

    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复当存在数据缺失的情况下 TiFlash 无法启动的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 TiFlash 在 Compaction Filter 特性开启时可能崩溃的问题
    - 修复 `ExchangeSender` 可能传输重复数据的问题
    ?- 修复 TiFlash 无法清除 Async Commit 回退的锁的问题
    - 修复当 `TIMEZONE` 类型的转换结果包含 `TIMESTAMP` 类型时返回错误结果的问题
    - 修复 TiFlash 在 Segment Split 期间异常退出的问题
    - 修复非根节点 MPP 任务的执行信息显示不正确的问题

+ Tools

    + TiCDC

        - 修复 Avro 输出中丢失时区信息的问题 [#1712](https://github.com/pingcap/ticdc/pull/1712)
        - 支持清理 Unified Sorter 过期的文件并禁止共享 `sort-dir` 目录 [#1742](https://github.com/pingcap/ticdc/pull/1742)
        - 修复存在大量过期 Region 信息时 KV 客户端可能锁死的问题 [#1801](https://github.com/pingcap/ticdc/pull/1801)
        - 修复 `--cert-allowed-cn` 参数中错误的帮助消息 [#1697](https://github.com/pingcap/ticdc/pull/1697)
        - 修复因更新 `explicit_defaults_for_timestamp` 而需要 MySQL `SUPER` 权限的问题 [#1750](https://github.com/pingcap/ticdc/pull/1750)
        - 添加 sink 流控以降低内存溢出的风险 [#1840](https://github.com/pingcap/ticdc/pull/1840)
        - 修复调度数据表时可能发生的同步终止问题 [#1828](https://github.com/pingcap/ticdc/pull/1828)
        - 修复 TiCDC changefeed 断点卡住导致 TiKV GC safe point 不推进的问题 [#1759](https://github.com/pingcap/ticdc/pull/1759)

    + Backup & Restore (BR)

        ?- 修复 log restore 为删除事件的问题 [#1083](https://github.com/pingcap/br/pull/1083)
        - 修复 BR 发送过多无用 RPC 请求到 TiKV 的问题 [#1037](https://github.com/pingcap/br/pull/1037)
        - 修复备份失败却没有错误输出的问题 [#1043](https://github.com/pingcap/br/pull/1043)

    + TiDB Lightning

        - 修复在生成 KV 数据时可能发生的 panic 问题 [#5739](https://github.com/pingcap/br/pull/5739)
        - 修复 TiDB-backend 模式下因没有开启 autocommit 而无法加载数据的问题 [#1125](https://github.com/pingcap/br/pull/1125)
        - 修复数据导入期间 batch split region 因键的总大小超过 Raft 条目限制而可能失败的问题 [#1065](https://github.com/pingcap/br/pull/1065)
