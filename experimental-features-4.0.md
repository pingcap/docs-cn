---
title: TiDB 实验特性
summary: 了解 TiDB 所有版本的实验特性。
aliases: ['/docs-cn/dev/experimental-features-4.0/']
---

# TiDB 实验特性

本文档介绍 TiDB 所有版本中的实验特性。**不建议**在生产环境中使用实验特性。

## 性能

+ TiDB 实例支持以 Region 为单位缓存算子下推到 TiKV 的的返回结果，提升 SQL 语句完全一致、SQL 语句包含一个变化条件且仅限于表主键或分区主键，其他部分一致和 SQL 语句包含多个变化的条件且条件完全匹配一个复合索引列，其他部分一致场景时 SQL 执行的效率。详情参阅：[缓存查询结果](/coprocessor-cache.md)。(v4.0)

## 稳定性

### TiFlash 限制压缩或整理数据占用 I/O 资源，缓解后台任务与前端的数据读写对 I/O 资源的争抢(v5.0)

TiFlash 压缩或者整理数据会占用大量 I/O 资源，系统通过限制压缩或整理数据占用的 I/O 量缓解资源争抢。此特性为实验性特性，系统默认关闭此特性，你可以通过 `bg_task_io_rate_limit` 配置项开启限制压缩或整理数据 I/O 资源。

## 调度功能

+ Cascading Placement Rules 是一套副本规则系统，用于指导 PD 针对不同类型的数据生成对应的调度。通过组合不同的调度规则，用户可以精细地控制任何一段连续数据的副本数量、存放位置、主机类型、是否参与 Raft 投票、是否可以担任 Raft leader 等属性。详情参阅：[Cascading Placement Rules](/configure-placement-rules.md)。(v4.0)
+ 弹性调度功能，结合 Kubernetes，可根据实时负载状态，动态扩缩节点，能够有效地缓解业务高峰的压力并且节约不必要的成本开销。详情参阅：[启用 TidbCluster 弹性伸缩](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling)。(v4.0)

## SQL 功能

- 支持表达式索引 (Expression Index) 功能，表达式索引也叫函数索引，在创建索引时索引的字段不一定要是一个具体的列，而可以由一个或者多个列计算出来的表达式。对于快速访问那些基于计算结果的表非常有用。详情参阅：[表达式索引](/sql-statements/sql-statement-create-index.md)。(v4.0)

#### List 分区表 （List Partition）(v5.0)

[用户文档](/partitioned-table#List 分区)

采用 List 分区表后，你可以高效地查询、维护有大量数据的表。

List 分区表会按照 `PARTITION BY LIST(expr) PARTITION part_name VALUES IN (...)` 表达式来定义分区，定义如何将数据划分到不同的分区中。分区表的数据集合最多支持 1024 个值，值的类型只支持整数型，不能有重复的值。可通过 PARTITION ... VALUES IN (...) 子句对值进行定义。

你可以设置 session 变量 `tidb_enable_list_partition` 的值为 `ON` ，开启 List 分区表实验功能。

#### List Column 分区表 （List Column Partition）（v5.0）

[用户文档](/partitioned-table#List 分区)

List Column 分区表是 List 分区表的变体，主要的区别是分区键可以由多个列组成，列的类型不再局限于整数类型，可以是字符串、DATE 和  DATETIME 等。

你可以设置session 变量 `tidb_enable_list_partition` 的值为 `ON` 开启 List Column 分区表实验功能。

## 配置管理

+ 支持将配置参数持久化存储到 PD 中，支持动态修改配置项功能，提升产品易用性。(v4.0)

## TiDB 数据共享订阅

### TiCDC 集成第三方生态 Kafka Connect (Confluent Platform)  (v5.0)

[用户文档](/integrate-confluent-using-ticdc#tidb-集成-confluent-platform-快速上手指南)，[TiCDC#660](https://github.com/pingcap/ticdc/issues/660)

为满足将 TiDB 的数据流转到其他系统以支持相关的业务需求，该功能可以把 TiDB 数据流转到 Kafka、Hadoop、 Oracle 等系统，实现业务所需的数据流转架构。

Confluent 平台提供的 kafka connectors 协议支持向不同协议关系型或非关系型数据库传输数据，在社区被广泛使用。 TiDB 通过 TiCDC 集成到 Confluent 平台的 Kafka Connect 扩展 TiDB 数据流转到其他异构数据库或者系统的能力。

### TiCDC 支持 TiDB 集群之间环形同步 (v5.0)

[用户文档](/ticdc/manage-ticdc.md#环形同步)，[TiCDC#471](https://github.com/pingcap/ticdc/issues/471)

由于地理位置差异导致的通讯延迟等问题，存在以下场景：
用户部署多套 TiDB 集群到不同的地理区域来支撑其当地的业务，然后通过各个 TiDB 相互复制，或者汇总复制数据到一个中心 TiDB hub，来完成诸如分析、结算等业务。

TiCDC 支持在多个独立的 TiDB 集群间同步数据。比如有三个 TiDB 集群 A、B 和 C，它们都有一个数据表 test.user_data，并且各自对它有数据写入。环形同步功能可以将 A、B 和 C 对 test.user_data 的写入同步到其它集群上，使三个集群上的 test.user_data 达到最终一致。

该功能可以用于以下场景： 

+ 多套 TiDB 集群相互进行数据备份，灾难发生时业务切换到正常的 TiDB 集群
+ 跨地域部署多套 TiDB 集群支撑当地业务，TiDB 集群之间的同一业务表之间数据需要相互复制

限制与约束：

+ 无法支持业务在不同集群写入使用自增 ID 的业务表，数据复制会导致业务数据相互覆盖而造成数据丢失
+ 无法支持业务在不同集群写入相同业务表的相同数据，数据复制会导致业务数据相互覆盖而造成数据丢失
