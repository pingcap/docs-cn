---
title: TiDB 5.0.2 Release Notes
---

# TiDB 5.0.2 Release Notes

发版日期：2021 年 6 月 9 日

TiDB 版本：5.0.2

## 兼容性更改

## 新功能

## 提升改进

+ TiDB

    - 优化了统计信息读取过程。如果缓存的统计数据是最新的，则跳过读取 mysql.stats_histograms 表，来避免频繁的数据读取 [#24317](https://github.com/pingcap/tidb/pull/24317)

+ TiFlash

    - 优化 apply region snapshots 操作的内存占用
    - 优化锁操作以避免 DDL 和读数据相互阻塞
    - 支持 integer 和 real 类型转化为 real 类型

## Bug 修复

+ TiDB

    - 修复了在某些情况下，使用前缀索引和 Index Join 导致的 Panic 的问题 [#24824](https://github.com/pingcap/tidb/pull/24824)
    - 修复了 point get 的 prepare plan cache 被事务中的 point get 语句不正确使用的问题 [#24765](https://github.com/pingcap/tidb/pull/24765)
    - 修复了当 collation 为 ascii_bin/latin1_bin 时，写入错误前缀索引的值的问题 [#24680](https://github.com/pingcap/tidb/pull/24680)
    - 修复了正在执行的事务被 gc worker 中断的问题 [#24652](https://github.com/pingcap/tidb/pull/24652)
    - 修复了当 `new-collation` 开启且 `new-row-format` 关闭的情况下，点查在聚簇索引下可能出错的问题 [#24611](https://github.com/pingcap/tidb/pull/24611)
    - Refactor converting partition keys for shuffle hash join [#24490](https://github.com/pingcap/tidb/pull/24490)
    - 修复了当查询包含 HAVING 子句时，在构建计划的过程中 Panic 的问题 [#24489](https://github.com/pingcap/tidb/pull/24489)
    - 修复了列裁剪优化导致 Apply 算子和 Join 算子执行结果错误的问题 [#24437](https://github.com/pingcap/tidb/pull/24437)
    - 修复了 `async commit` 回退导致的主锁无法清除的问题 [#24397](https://github.com/pingcap/tidb/pull/24397)
    - 修复了统计信息 GC 的一个问题，曾导致 fm-sketch 会有重复的记录 [#24357](https://github.com/pingcap/tidb/pull/24357)
    - 当悲观锁事务收到 ErrKeyExists 错误时，避免不必要的悲观事务回滚 [#23800](https://github.com/pingcap/tidb/pull/23800)
    - 修复了当 sql_mode 包含 `ANSI_QUOTES` 时，数值字面值无法被识别的问题 [#25015](https://github.com/pingcap/tidb/pull/25015)
    - 不再允许形如 `INSERT INTO table PARTITION (<partitions>) ... ON DUPLICATE KEY UPDATE` 的语句从 non-listed partitions 读取数据 [#25000](https://github.com/pingcap/tidb/pull/25000)
    - 修复了当 SQL 语句包含 group by 以及 union 时，可能会出现的 index out of range 的问题 [#24551](https://github.com/pingcap/tidb/pull/24551)
    - 修复了 concat 函数错误的 collation 处理 [#24301](https://github.com/pingcap/tidb/pull/24301)
    - 修复了全局变量 `collation_server` 对新会话无法生效的问题 [#24156](https://github.com/pingcap/tidb/pull/24156)

+ TiFlash

    - 修复并发复制共享 delta 索引导致结果错误的问题
    - 修复当存在数据缺失的情况下 TiFlash 无法启动的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 TiFlash 与 `compaction filter` 特性的兼容性问题
    - 修复 `ExchangeSender` 可能传输重复数据的问题
    - 修复 TiFlash 与 `async commit` 的兼容性问题
    - 修复当 timezone 类型转换结果包含 timestamp 类型时返回错误结果的问题
    - 修复 TiFlash 在 Segment Split 期间异常退出的问题
    - 修复非根节点 MPP 任务的执行信息显示不正确的问题
