---
title: TiDB 3.0.15 Release Notes
aliases: ['/docs-cn/dev/releases/release-3.0.15/']
---

# TiDB 3.0.15 Release Notes

发版日期：2020 年 6 月 5 日

TiDB 版本：3.0.15

## 新功能

+ TiDB

    - 禁止分区表上的查询使用 plan cache 功能 [#16759](https://github.com/pingcap/tidb/pull/16759)
    - 分区表支持 `admin recover index`、`admin check index` 语句 [#17315](https://github.com/pingcap/tidb/pull/17315) [#17390](https://github.com/pingcap/tidb/pull/17390)
    - Range 类型分区表支持按 `in` 查询条件进行分区裁剪 [#17318](https://github.com/pingcap/tidb/pull/17318)
    - 优化 `SHOW CREATE TABLE` 的输出结果，在分区名称上添加了引号 [#16315](https://github.com/pingcap/tidb/pull/16315)
    - `GROUP_CONCAT` 支持 `ORDER BY` 子句 [#16988](https://github.com/pingcap/tidb/pull/16988)
    - 优化统计信息 `CMSketch` 的内存分配机制，减少垃圾回收导致的性能影响 [#17543](https://github.com/pingcap/tidb/pull/17543)

+ PD

    - 新增按照 Leader 个数调度的策略 [#2479](https://github.com/pingcap/pd/pull/2479)

## Bug 修复

+ TiDB

    - Hash 聚合函数中，采用深拷贝的方式拷贝 `enum` 和 `set` 类型数据，且修复一处正确性问题 [#16890](https://github.com/pingcap/tidb/pull/16890)
    - 修复点查因整数溢出处理逻辑不正确导致输出结果不正确的问题 [#16753](https://github.com/pingcap/tidb/pull/16753)
    - 修复 `CHAR()` 函数作为查询的谓词条件时因处理逻辑不正确导致输出的结果不正确的问题 [#16557](https://github.com/pingcap/tidb/pull/16557)
    - 修复 `IsTrue` 和 `IsFalse` 函数存储层和计算层计算结果不一致的问题[#16627](https://github.com/pingcap/tidb/pull/16627)
    - 修复部分表达式（例如 `case when`）中，`Not Null` 标记设置不正确的问题 [#16993](https://github.com/pingcap/tidb/pull/16993)
    - 修复部分场景中优化器无法为 `TableDual` 找到物理计划的问题 [#17014](https://github.com/pingcap/tidb/pull/17014)
    - 修复 Hash 分区表中分区选择的语法没有正确生效的问题 [#17051](https://github.com/pingcap/tidb/pull/17051)
    - 修复 `XOR` 作用于浮点数时，结果与 MySQL 不一致的问题 [#16976](https://github.com/pingcap/tidb/pull/16976)
    - 修复 prepare 方式执行 DDL 语句出错的问题 [#17415](https://github.com/pingcap/tidb/pull/17415)
    - 修复 ID 分配器中计算 Batch 大小的逻辑处理不正确的问题 [#17548](https://github.com/pingcap/tidb/pull/17548)
    - 修复 `MAX_EXEC_TIME` 的 SQL Hint 在超过 expensive 阈值后不生效的问题 [#17534](https://github.com/pingcap/tidb/pull/17534)

+ TiKV

    - 修复长时间运行后由于处理逻辑不正确导致碎片整理不再有效的问题 [#7790](https://github.com/tikv/tikv/pull/7790)
    - 修复系统意外重启后错误地删除 snapshot 文件导致系统 panic 的问题 [#7925](https://github.com/tikv/tikv/pull/7925)
    - 修复因消息包过大导致 gRPC 连接断开的问题 [#7822](https://github.com/tikv/tikv/pull/7822)
