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
+ [Cost Model Version 2](/cost-model.md#cost-model-version-2)（v6.2.0 实验特性）
+ [FastScan](/develop/dev-guide-use-fastscan.md)（v6.2.0 实验特性）
+ [随机采样约 10000 行数据来快速构建统计信息](/system-variables.md#tidb_enable_fast_analyze)（v3.0 实验特性）

## 稳定性

+ 提升优化器选择索引的稳定性：扩展统计信息功能，收集多列顺序依赖性信息，帮助优化器选择相对较优的索引（v5.0 实验特性）
+ [后台限流](/tikv-configuration-file.md#后台限流)（v6.2.0 实验特性）

    你可以使用后台限流相关的 quota 配置项以限制后台各类请求占用的 CPU 资源。触发该限制的请求会被强制等待一段时间以让出 CPU 资源。

## 调度功能

弹性调度功能。结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。（v4.0 实验特性）

## SQL 功能

+ 表达式索引 (Expression Index) 功能。表达式索引也叫函数索引，在创建索引时索引的字段不一定是一个具体的列，也可以是由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。（v4.0 实验特性）
+ [生成列](/generated-columns.md#生成列)。（v2.1 实验特性）
+ [自定义变量](/user-defined-variables.md#用户自定义变量)。（v2.1 实验特性）
+ [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner)：基于 Cascades 框架的自顶向下查询优化器。（v3.0 实验特性）
+ [元数据锁](/metadata-lock.md) （v6.3.0 实验特性）
+ [Range INTERVAL 分区](/partitioned-table.md#range-interval-分区)（v6.3.0 实验特性）
+ [添加索引加速](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)（v6.3.0 实验特性）

## 存储

+ [Titan Level Merge 功能](/storage-engine/titan-configuration.md#level-merge实验功能)。（v4.0 实验特性）
+ 将 Region 划分为更小的区间 bucket，并且[以 bucket 作为并发查询单位](/tune-region-performance.md#使用-bucket-增加并发)，以提高扫描数据的并发度。（v6.1.0 实验特性）
+ TiKV 引入 [API v2](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)。（v6.1.0 实验特性）

## 数据迁移

+ [使用 WebUI](/dm/dm-webui-guide.md) 管理 DM 迁移任务。（v6.0 实验特性）
+ 为 TiDB Lightning 设置[磁盘资源配额](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#磁盘资源配额-从-v620-版本开始引入)（v6.2.0 实验特性）
+ [DM 增量数据校验](/dm/dm-continuous-data-validation.md)（v6.2.0 实验特性）

## 数据共享订阅

+ [RawKV 跨集群复制](/tikv-configuration-file.md#api-version-从-v610-版本开始引入)（v6.2.0 实验特性）

## 垃圾回收

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)。（v5.0 实验特性）

## 问题诊断

+ [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)。（v4.0 实验特性）
+ [集群诊断](/dashboard/dashboard-diagnostics-access.md)。（v4.0 实验特性）
+ [TiKV-FastTune 监控面板](/grafana-tikv-dashboard.md#tikv-fasttune-面板)。（v4.0 实验特性）
