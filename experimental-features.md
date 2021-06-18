---
title: TiDB 实验特性
summary: 了解 TiDB 各版本的实验特性。
aliases: ['/docs-cn/dev/experimental-features-4.0/','/zh/tidb/dev/experimental-features-4.0/']
---

# TiDB 实验特性

本文介绍 TiDB 各版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 稳定性

+ TiFlash 限制压缩或整理数据占用 I/O 资源，缓解后台任务与前端的数据读写对 I/O 资源的争抢（v5.0 实验特性）
+ 提升优化器选择索引的稳定性（v5.0 实验特性）
    + 扩展统计信息功能，收集多列顺序依赖性信息，帮助优化器选择相对较优的索引。
    + 重构统计信息模块，帮助优化器选择相对较优的索引，包括从 `CMSKetch` 和直方图中删除 `TopN` 值，为索引的直方图维护 Bucket NDV。

## 调度功能

+ Cascading Placement Rules 是一套副本规则系统，用于指导 PD 针对不同类型的数据生成对应的调度。通过组合不同的调度规则，用户可以精细地控制任何一段连续数据的副本数量、存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft leader 等属性。详情参阅：[Cascading Placement Rules](/configure-placement-rules.md)。（v4.0 实验特性）
+ 弹性调度功能。结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。（v4.0 实验特性）

## SQL 功能

+ List 分区表 （List Partition）。（v5.0 实验特性）
+ List Column 分区表 （List Column Partition)。（v5.0 实验特性）
+ [分区表动态模式](/partitioned-table.md#动态模式)。（v5.1 实验特性）
+ 表达式索引 (Expression Index) 功能。表达式索引也叫函数索引，在创建索引时索引的字段不一定是一个具体的列，也可以是由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。（v4.0 实验特性）
+ [生成列](/generated-columns.md#生成列)。
+ [自定义变量](/user-defined-variables.md#用户自定义变量)。
+ [JSON 数据类型](/data-type-json.md) 及 [JSON 函数](/functions-and-operators/json-functions.md)。
+ [View](/information-schema/information-schema-views.md)。

## 配置管理

+ 将配置参数持久化存储到 PD 中，并且可以动态修改配置项的功能。（v4.0 实验特性）
+ [SHOW CONFIG](/sql-statements/sql-statement-show-config.md)。（v4.0 实验特性）

## TiDB 数据共享订阅

+ TiCDC 集成第三方生态 [Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md)（v5.0 实验特性）
+ TiCDC [支持 TiDB 集群之间环形同步](/ticdc/manage-ticdc.md#环形同步)。（v5.0 实验特性）

## 存储

+ [关闭 Titan 功能](/storage-engine/titan-configuration.md#关闭-titan实验功能)。
+ [Titan Level Merge 功能](/storage-engine/titan-configuration.md#level-merge实验功能)。
+ TiFlash 支持将存储引擎的新数据分布在多个硬盘上，分摊 I/O 压力。（v4.0 实验特性）

## 备份与恢复

+ [Raw KV 备份](/br/use-br-command-line-tool.md#raw-kv-备份实验性功能)。

## 垃圾回收

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-从-v50-版本开始引入)。

## 问题诊断

+ [SQL 诊断](/information-schema/information-schema-sql-diagnostics.md)。
+ [集群诊断](/dashboard/dashboard-diagnostics-access.md)。
