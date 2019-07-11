---
title: TiDB RC4 Release Notes
category: Releases
---

# TiDB RC4 Release Notes

2017 年 8 月 4 日，TiDB 正式发布 RC4 版。该版本对 MySQL 兼容性、SQL 优化器、系统稳定性、性能做了大量的工作。性能方面重点优化了写入速度，计算任务调度支持优先级，避免分析型大事务影响在线事务。SQL 优化器全新改版，查询代价估算更加准确，且能够自动选择 Join 物理算子。功能方面进一步 MySQL 兼容性。
同时为了更好的支持 OLAP 业务，开源了 TiSpark 项目，可以通过 Spark 读取和分析 TiKV 中的数据。

## TiDB

+ SQL 查询优化器重构
    - 更好的支持 TopN 查询
    - 支持 Join 算子根据代价自动选择
    - 更完善的 Projection Elimination
+ Schema 版本检查区分 Table，避免 DDL 干扰其他正在执行的事务
+ 支持 BatchIndexJoin
+ 完善 Explain 语句
+ 提升 Index Scan 性能
+ 大量 MySQL 兼容性相关功能
+ 支持 Json 类型及其操作
+ 支持查询优先级、隔离级别的设置

## PD

+ 支持通过 PD 设置 TiKV location labels
+ 调度优化
    - 支持 PD 主动向 TiKV 下发调度命令
    - 加快 region heartbeat 响应速度
    - 优化 balance 算法
+ 优化数据加载，加快 failover 速度

## TiKV

+ 支持查询优先级设置
+ 支持 RC 隔离级别
+ 完善 Jepsen，提升稳定性
+ 支持 Document Store
+ Coprocessor 支持更多下推函数
+ 提升性能，提升稳定性

## TiSpark Beta Release

+ 支持谓词下推
+ 支持聚合下推
+ 支持范围裁剪
+ 通过 TPC-H 测试 (除去一个需要 View 的 Query)