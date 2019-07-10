---
title: TiDB 1.1 Beta Release Notes
category: Releases
---

# TiDB 1.1 Beta Release Notes

2018 年 2 月 24 日，TiDB 发布 1.1 Beta 版。该版本在 1.1 Alpha 版的基础上，对 MySQL 兼容性、系统稳定性做了很多改进。

## TiDB

+ 添加更多监控项, 优化日志
+ 兼容更多 MySQL 语法
+ 在 `information_schema` 中支持显示建表时间
+ 提速包含 `MaxOneRow` 算子的查询
+ 控制 Join 产生的中间结果集大小，进一步减少 Join 的内存使用
+ 增加 `tidb_config` session 变量，输出当前 TiDB 配置
+ 修复 `Union` 和 `Index Join` 算子中遇到的 panic 问题
+ 修复 `Sort Merge Join` 算子在部分场景下结果错误的问题
+ 修复 `Show Index` 语句显示正在添加过程中的索引的问题
+ 修复 `Drop Stats` 语句失败的问题
+ 优化 SQL 引擎查询性能，Sysbench 的 Select/OLTP 测试结果提升 10%
+ 使用新的执行引擎提升优化器中的子查询计算速度；相比 1.0 版本，在 TPC-H 以及 TPC-DS 等测试中有显著提升

## PD

+ 增加 Drop Region 调试接口
+ 支持设置 PD leader 优先级
+ 支持配置特定 label 的节点不调度 Raft leader
+ 增加枚举各个 PD health 状态的接口
+ 添加更多 metrics
+ PD leader 尽量与 etcd leader 保持同步
+ 提高 TiKV 宕机时数据恢复优先级和恢复速度
+ 完善 `data-dir` 配置项的合法性较验
+ 优化 Region heartbeat 性能
+ 修复热点调度破坏 label 约束的问题
+ 其他稳定性问题修复

## TiKV

+ 使用 offset + limit 遍历 lock，消除潜在的 GC 问题
+ 支持批量 resolve lock，提升 GC 速度
+ 支持并行 GC，提升 GC 速度
+ 使用 RocksDB compaction listener 更新 Region Size，让 PD 更精确的进行调度
+ 使用 `DeleteFilesInRanges` 批量删除过期数据，提高 TiKV 启动速度
+ 设置 Raft snapshot max size，防止遗留文件占用太多空间
+ `tikv-ctl` 支持更多修复操作
+ 优化有序流式聚合操作
+ 完善 metrics，修复 bug
