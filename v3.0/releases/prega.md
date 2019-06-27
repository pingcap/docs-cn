---
title: TiDB Pre-GA Release Notes
category: Releases
aliases: ['/docs-cn/releases/prega/']
---

# TiDB Pre-GA Release Notes

2017 年 8 月 30 日，TiDB 发布 Pre-GA 版。该版本对 MySQL 兼容性、SQL 优化器、系统稳定性、性能做了大量的工作。

## TiDB:

+ SQL 查询优化器
    - 调整代价模型
    - 优化索引选择，支持不同类型字段比较的索引选择
    - 支持基于贪心算法的 Join Reorder
+ 大量 MySQL 兼容性相关功能
+ 支持 Natural Join
+ 完成 JSON 类型支持 (Experimental)，包括对 JSON 中的字段查询、更新、建索引
+ 裁剪无用数据，减小执行器内存消耗
+ 支持在 SQL 语句中设置优先级，并根据查询类型自动设置部分语句的优先级
+ 完成表达式重构，执行速度提升 30% 左右 

## PD:

+ 支持手动切换 PD 集群 Leader

## TiKV:

+ Raft Log 使用独立的 RocksDB 实例
+ 使用 DeleteRange 加快删除副本速度
+ Coprocessor 支持更多运算符下推
+ 提升性能，提升稳定性

## TiSpark Beta Release:

+ 支持谓词下推
+ 支持聚合下推
+ 支持范围裁剪
+ 通过 TPC-H 测试 (除去一个需要 View 的 Query)
