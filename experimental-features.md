---
title: TiDB 实验特性
summary: 了解 TiDB 各版本的实验特性。
---

# TiDB 实验特性

本文介绍 TiDB 各版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 性能

+ [随机采样约 10000 行数据来快速构建统计信息](/system-variables.md#tidb_enable_fast_analyze)（v3.0 实验特性）

## 稳定性

+ 提升优化器选择索引的稳定性（v5.0 实验特性）
    + 扩展统计信息功能，收集多列顺序依赖性信息，帮助优化器选择相对较优的索引。
    + 重构统计信息模块，帮助优化器选择相对较优的索引，包括从 `CMSKetch` 和直方图中删除 `TopN` 值，为索引的直方图维护 Bucket NDV。详情参阅[统计信息简介 - `tidb_analyze_version = 2` 的介绍](/statistics.md)。

## 调度功能

弹性调度功能。结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。（v4.0 实验特性）

## SQL 功能

+ [使用 SQL 接口设置数据放置规则](/placement-rules-in-sql.md)。(v5.3 实验特性)
+ List 分区表 (List Partition)。（v5.0 实验特性）
+ List Column 分区表 (List Column Partition)。（v5.0 实验特性）
+ [分区表动态裁剪模式](/partitioned-table.md#动态裁剪模式)。（v5.1 实验特性）
+ 表达式索引 (Expression Index) 功能。表达式索引也叫函数索引，在创建索引时索引的字段不一定是一个具体的列，也可以是由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。（v4.0 实验特性）
+ [生成列](/generated-columns.md#生成列)。（v2.1 实验特性）
+ [自定义变量](/user-defined-variables.md#用户自定义变量)。（v2.1 实验特性）
+ [JSON 数据类型](/data-type-json.md)及 [JSON 函数](/functions-and-operators/json-functions.md)。（v2.1 实验特性）
+ [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner)：基于 Cascades 框架的自顶向下查询优化器。（v3.0 实验特性）
+ [使用 `ALTER TABLE` 修改多个列或索引](/system-variables.md#tidb_enable_change_multi_schema)。（v5.0.0 实验特性）

## 配置管理

+ 将配置参数持久化存储到 PD 中，并且可以动态修改配置项的功能。（v4.0 实验特性）

## TiDB 数据共享订阅

+ TiCDC 集成第三方生态 [Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md)（v5.0 实验特性）
+ [表级锁 (Table Lock)](/tidb-configuration-file.md#enable-table-lock-从-v400-版本开始引入)（v4.0.0 实验特性）

## 存储

+ [关闭 Titan 功能](/storage-engine/titan-configuration.md#关闭-titan实验功能)。（v4.0 实验特性）
+ [Titan Level Merge 功能](/storage-engine/titan-configuration.md#level-merge实验功能)。（v4.0 实验特性）

## 数据迁移

+ [DM 的 OpenAPI 功能](https://docs.pingcap.com/zh/tidb-data-migration/stable/open-api)。 （v5.3 实验特性）

## 备份与恢复

+ [Raw KV 备份](/br/use-br-command-line-tool.md#raw-kv-备份实验性功能)。（v3.1 实验特性）

## 垃圾回收

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)。（v5.0 实验特性）

## 问题诊断

+ [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)。（v4.0 实验特性）
+ [集群诊断](/dashboard/dashboard-diagnostics-access.md)。（v4.0 实验特性）
+ [在线有损恢复](/online-unsafe-recovery.md)。（v5.3 实验特性）
+ [持续性能分析](/dashboard/continuous-profiling.md)。（v5.3 实验特性）
