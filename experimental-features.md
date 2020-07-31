---
title: 实验特性
summary: 了解 TiDB 4.0 版本的实验特性。
---

# 实验特性

本文档介绍 TiDB 4.0 版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 核心特性

### 调度功能

+ Cascading Placement Rules 是一套副本规则系统，用于指导 PD 针对不同类型的数据生成对应的调度。通过组合不同的调度规则，用户可以精细地控制任何一段连续数据的副本数量、存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft leader 等属性。详情参阅：[Cascading Placement Rules](/configure-placement-rules.md)。
+ 弹性调度功能，结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。

### SQL 功能

- 支持表达式索引 (Expression Index) 功能，表达式索引也叫函数索引，在创建索引时索引的字段不一定要是一个具体的列，而可以由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。
- 支持 AutoRandom Key 作为 TiDB 在列属性上的扩展语法，AutoRandom 被设计用于解决自增主键列的写热点问题，为使用自增主键列的用户提供最低成本的 MySQL 迁移方案。详情参阅：[AutoRandom Key](/auto-random.md)。

### 服务级别功能

+ TiDB 实例支持以 Region 为单位缓存算子下推到 TiKV 的的返回结果，提升 SQL 语句完全一致、SQL 语句包含一个变化条件且仅限于表主键或分区主键，其他部分一致和 SQL 语句包含多个变化的条件且条件完全匹配一个复合索引列，其他部分一致场景时 SQL 执行的效率。详情参阅：[缓存查询结果](/coprocessor-cache.md)。
+ 支持将配置参数持久化存储到 PD 中，支持动态修改配置项功能，提升产品易用性。

### TiCDC

TiCDC 支持通过拉取 TiKV 变更日志实现 TiDB 集群之间数据同步，支持数据的高可靠、服务的高可用能力，确保数据不会丢失。用户可以通过订阅的方式订阅数据的变更信息，系统会自动将数据推送到下游系统，当前仅支持 MySQL 协议的数据库（例如：MySQL、TiDB)及 Kafka 作为 TiCDC 的下游，同时用户也可以通过 TiCDC 提供的[开放数据协议](/ticdc/ticdc-open-protocol.md)自行扩展支持的下游系统。详情参阅：[TiCDC](/ticdc//ticdc-overview.md)。
