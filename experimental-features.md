---
title: TiDB 实验特性
summary: 了解 TiDB 各版本的实验特性。
aliases: ['/docs-cn/dev/experimental-features-4.0/','/zh/tidb/dev/experimental-features-4.0/']
---

# TiDB 实验特性

本文介绍 TiDB 各版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 性能

+ [支持收集部分列的统计信息](/statistics.md#收集部分列的统计信息)（v5.4 实验特性）
+ [支持统计信息的同步加载](/statistics.md#统计信息的加载)（v5.4 实验特性）
+ [限制 ANALYZE 的内存使用量](/statistics.md#统计信息收集的内存限制) (v6.1.0 实验特性)
+ [随机采样约 10000 行数据来快速构建统计信息](/system-variables.md#tidb_enable_fast_analyze)（v3.0 实验特性）

## 稳定性

+ 提升优化器选择索引的稳定性：扩展统计信息功能，收集多列顺序依赖性信息，帮助优化器选择相对较优的索引。（v5.0 实验特性）
+ 当 TiKV 部署的机型资源有限时，如果 TiKV 前台处理的读写请求量过大，会占用 TiKV 后台处理请求所需的 CPU 资源，最终影响 TiKV 性能的稳定性。此时，你可以使用[前台限流](/tikv-configuration-file.md#quota)以限制前台各类请求占用的 CPU 资源。（v6.0 实验特性）

## 调度功能

弹性调度功能。结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。（v4.0 实验特性）

## SQL 功能

+ 表达式索引 (Expression Index) 功能。表达式索引也叫函数索引，在创建索引时索引的字段不一定是一个具体的列，也可以是由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。（v4.0 实验特性）
+ [生成列](/generated-columns.md#生成列)。（v2.1 实验特性）
+ [自定义变量](/user-defined-variables.md#用户自定义变量)。（v2.1 实验特性）
+ [JSON 数据类型](/data-type-json.md)及 [JSON 函数](/functions-and-operators/json-functions.md)。（v2.1 实验特性）
+ [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner)：基于 Cascades 框架的自顶向下查询优化器。（v3.0 实验特性）
+ [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。（v6.1.0 实验特性）

## 存储

+ [关闭 Titan 功能](/storage-engine/titan-configuration.md#关闭-titan实验功能)。（v4.0 实验特性）
+ [Titan Level Merge 功能](/storage-engine/titan-configuration.md#level-merge实验功能)。（v4.0 实验特性）
+ 将 Region 划分为更小的区间 bucket，并且[以 bucket 作为并发查询单位](/tune-region-performance.md#使用-bucket-增加并发)，以提高扫描数据的并发度。（v6.1.0 实验特性）
+ TiKV 引入 [API v2](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。（v6.1.0 实验特性）

## 备份与恢复

+ [RawKV 备份和恢复](/br/rawkv-backup-and-restore.md)。（v3.1 实验特性）

## 数据迁移

+ [使用 WebUI](/dm/dm-webui-guide.md) 管理 DM 迁移任务。（v6.0 实验特性）

## 垃圾回收

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)。（v5.0 实验特性）

## 问题诊断

+ [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)。（v4.0 实验特性）
+ [集群诊断](/dashboard/dashboard-diagnostics-access.md)。（v4.0 实验特性）
