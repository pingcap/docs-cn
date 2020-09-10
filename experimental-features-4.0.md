---
title: TiDB 4.0 实验特性
summary: 了解 TiDB 4.0 版本的实验特性。
aliases: ['/docs-cn/stable/experimental-features-4.0/','/docs-cn/v4.0/experimental-features-4.0/']
---

# TiDB 4.0 实验特性

本文档介绍 TiDB 4.0 版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 调度功能

+ Cascading Placement Rules 是一套副本规则系统，用于指导 PD 针对不同类型的数据生成对应的调度。通过组合不同的调度规则，用户可以精细地控制任何一段连续数据的副本数量、存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft leader 等属性。详情参阅：[Cascading Placement Rules](/configure-placement-rules.md)。
+ 弹性调度功能，结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。

## SQL 功能

- 支持表达式索引 (Expression Index) 功能，表达式索引也叫函数索引，在创建索引时索引的字段不一定要是一个具体的列，而可以由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。

## 服务级别功能

+ TiDB 实例支持以 Region 为单位缓存算子下推到 TiKV 的的返回结果，提升 SQL 语句完全一致、SQL 语句包含一个变化条件且仅限于表主键或分区主键，其他部分一致和 SQL 语句包含多个变化的条件且条件完全匹配一个复合索引列，其他部分一致场景时 SQL 执行的效率。详情参阅：[缓存查询结果](/coprocessor-cache.md)。
+ 支持将配置参数持久化存储到 PD 中，支持动态修改配置项功能，提升产品易用性。
