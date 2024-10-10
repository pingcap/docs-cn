---
title: 术语表
summary: 了解 TiDB 相关术语。
aliases: ['/docs-cn/dev/glossary/']
---

# 术语表

## A

### ACID

ACID 是指数据库管理系统在写入或更新资料的过程中，为保证事务是正确可靠的，所必须具备的四个特性：原子性 (atomicity)、一致性 (consistency)、隔离性 (isolation) 以及持久性 (durability)。

* 原子性 (atomicity) 指一个事务中的所有操作，或者全部完成，或者全部不完成，不会结束在中间某个环节。TiDB 通过 Primary Key 所在 [Region](#regionpeerraft-group) 的原子性来保证分布式事务的原子性。
* 一致性 (consistency) 指在事务开始之前和结束以后，数据库的完整性没有被破坏。TiDB 在写入数据之前，会校验数据的一致性，校验通过才会写入内存并返回成功。
* 隔离性 (isolation) 指数据库允许多个并发事务同时对其数据进行读写和修改的能力。隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致，主要用于处理并发场景。关于 TiDB 支持的隔离级别，请参考 [TiDB 事务隔离级别](/transaction-isolation-levels.md#tidb-事务隔离级别)。
* 持久性 (durability) 指事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。在 TiDB 中，事务一旦提交成功，数据全部持久化存储到 TiKV，此时即使 TiDB 服务器宕机也不会出现数据丢失。

## B

### BR

[TiDB 备份恢复功能](/br/backup-and-restore-overview.md)用户文档中的名词 **BR** 根据上下文不同有不同的解释，比较常见的指代用法：

* TiDB 备份恢复功能，包含 br CLI、TiDB Operator、TiDB Cloud 提供的备份和恢复功能集合。
* 架构中的 BR 功能组件。

名词 **br** 一般用来指代 br CLI 工具。

### Batch Create Table

批量建表 (Batch Create Table) 是在 TiDB v6.0.0 中引入的新功能，此功能默认开启。当需要恢复的数据中带有大量的表（约 50000 张）时，批量建表功能显著提升数据恢复的速度。详情参见[批量建表](/br/br-batch-create-table.md)。

### Baseline Capturing

自动捕获绑定 (Baseline Capturing) 会对符合捕获条件的查询进行捕获，为符合条件的查询生成相应的绑定。通常用于升级时的[计划回退防护](/sql-plan-management.md#升级时的计划回退防护)。

### Bucket

一个 [Region](#regionpeerraft-group) 在逻辑上划分为多个小范围，称为 bucket。TiKV 按 bucket 收集查询统计数据，并将 bucket 的情况报告给 PD。详情参见 [Bucket 设计文档](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket)。

## C

### Cached Table

缓存表 (Cached Table) 是指 TiDB 把整张表的数据加载到服务器的内存中，直接从内存中获取表数据，避免从 TiKV 获取表数据，从而提升读性能。详情参见[缓存表](/cached-tables.md)。

### Coalesce Partition

Coalesce Partition 是一种减少 Hash 分区表或 Key 分区表中分区数量的方法。详情参见[管理 Hash 分区和 Key 分区](/partitioned-table.md#管理-hash-分区和-key-分区)。

### Continuous Profiling

持续性能分析 (Continuous Profiling) 是从 TiDB v5.3 起引入的一种从系统调用层面解读资源开销的方法。引入该方法后，TiDB 可提供数据库源码级性能观测，通过火焰图的形式帮助研发、运维人员定位性能问题的根因。详情参见 [TiDB Dashboard 实例性能分析 - 持续分析页面](/dashboard/continuous-profiling.md)。

## D

### Dynamic Pruning

动态裁剪 (Dynamic Pruning) 是 TiDB 访问分区表的两种模式之一。在动态裁剪模式下，TiDB 的每个算子都支持直接访问多个分区，省略 Union 操作，提高执行效率，还避免了 Union 并发管理的问题。

## I

### Index Merge

索引合并 (Index Merge) 是在 TiDB v4.0 版本中作为实验特性引入的一种查询执行方式的优化，可以大幅提高查询在扫描多列数据时条件过滤的效率。自 v5.4 版本起，Index Merge 成为正式功能，详情参见[用 EXPLAIN 查看索引合并的 SQL 执行计划](/explain-index-merge.md)。

### In-Memory Pessimistic Lock

内存悲观锁 (In-Memory Pessimistic Lock) 是在 TiDB v6.0.0 中引入的新功能。开启内存悲观锁功能后，悲观锁通常只会被存储在 Region leader 的内存中，而不会将锁持久化到磁盘，也不会通过 Raft 协议将锁同步到其他副本，因此可以大大降低悲观事务加锁的开销，提升悲观事务的吞吐并降低延迟。

## L

### Leader/Follower/Learner

它们分别对应 [Peer](#regionpeerraft-group) 的三种角色。其中 Leader 负责响应客户端的读写请求；Follower 被动地从 Leader 同步数据，当 Leader 失效时会进行选举产生新的 Leader；Learner 是一种特殊的角色，它只参与同步 raft log 而不参与投票，在目前的实现中只短暂存在于添加副本的中间步骤。

## M

### MPP

从 v5.0 起，TiDB 通过 TiFlash 节点引入了 Massively Parallel Processing (MPP) 架构。这使得大型表连接类查询可以由不同 TiFlash 节点共同分担完成。当 MPP 模式开启后，TiDB 将会根据代价决定是否应该交由 MPP 框架进行计算。MPP 模式下，表连接将通过对 JOIN Key 进行数据计算时重分布（Exchange 操作）的方式把计算压力分摊到各个 TiFlash 执行节点，从而达到加速计算的目的。更多信息请参见[使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

## O

### Old value

Old value 特指在 TiCDC 输出的增量变更日志中的“原始值”。可以通过配置来指定 TiCDC 输出的增量变更日志是否包含“原始值”。

### Operator

Operator 是应用于一个 Region 的，服务于某个调度目的的一系列操作的集合。例如“将 Region 2 的 Leader 迁移至 Store 5”，“将 Region 2 的副本迁移到 Store 1, 4, 5”等。

Operator 可以是由 Scheduler 通过计算生成的，也可以是由外部 API 创建的。

### Operator Step

Operator Step 是 Operator 执行过程的一个步骤，一个 Operator 常常会包含多个 Operator Step。

目前 PD 可生成的 Step 包括：

- `TransferLeader`：将 Region Leader 迁移至指定 Peer
- `AddPeer`：在指定 Store 添加 Follower
- `RemovePeer`：删除一个 Region Peer
- `AddLearner`：在指定 Store 添加 Region Learner
- `PromoteLearner`：将指定 Learner 提升为 Follower
- `SplitRegion`：将指定 Region 一分为二

## P

### Partitioning

[Partitioning](/partitioned-table.md)（分区）指通过 `RANGE`、`LIST`、`HASH` 和 `KEY` 等分区方法在物理上将一张表划分为较小的分区。

### Pending/Down

Pending 和 Down 是 Peer 可能出现的两种特殊状态。其中 Pending 表示 Follower 或 Learner 的 raft log 与 Leader 有较大差距，Pending 状态的 Follower 无法被选举成 Leader。Down 是指 Leader 长时间没有收到对应 Peer 的消息，通常意味着对应节点发生了宕机或者网络隔离。

### Point get

点查 (point get) 是指通过主键或唯一索引直接读取一行的查询方式。点查的返回结果最多是一行数据。

### Predicate columns

执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如，`WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中出现的列）的统计信息，这些用到的列称为 `PREDICATE COLUMNS`。详情参见[收集部分列的统计信息](/statistics.md#收集部分列的统计信息)。

## Q

### Quota Limiter

前台限流 (Quota Limiter) 是在 TiDB v6.0.0 版本中作为实验特性引入的功能。当 TiKV 部署的机型资源有限（如 4v CPU，16 G 内存）时，如果 TiKV 前台处理的读写请求量过大，会占用 TiKV 后台处理请求所需的 CPU 资源，最终影响 TiKV 性能的稳定性。此时，开启前台限流相关的 [quota 相关配置项](/tikv-configuration-file.md#quota)可以限制前台各类请求占用的 CPU 资源。

## R

### Raft Engine

一种内置的持久化存储引擎，有着日志结构的设计，为 TiKV 提供 multi-Raft 日志存储。从 v5.4 起，TiDB 支持使用 Raft Engine 作为 TiKV 的日志存储引擎。详情参见 [Raft Engine](/tikv-configuration-file.md#raft-engine)。

### Region/Peer/Raft Group

每个 Region 负责维护集群的一段连续数据（默认配置下平均约 256 MiB），每份数据会在不同的 Store 存储多个副本（默认配置是 3 副本），每个副本称为 Peer。同一个 Region 的多个 Peer 通过 raft 协议进行数据同步，所以 Peer 也用来指代 raft 实例中的成员。TiKV 使用 multi-raft 模式来管理数据，即每个 Region 都对应一个独立运行的 raft 实例，我们也把这样的一个 raft 实例叫做一个 Raft Group。

### Region Split

TiKV 集群中的 Region 不是一开始就划分好的，而是随着数据写入逐渐分裂生成的，分裂的过程被称为 Region Split。

其机制是集群初始化时构建一个初始 Region 覆盖整个 key space，随后在运行过程中每当 Region 数据达到一定量之后就通过 Split 产生新的 Region。

### Restore

备份操作的逆过程，即利用保存的备份数据还原出原始数据的过程。

## S

### Scheduler

Scheduler（调度器）是 PD 中生成调度的组件。PD 中每个调度器是独立运行的，分别服务于不同的调度目的。常用的调度器及其调用目标有：

- `balance-leader-scheduler`：保持不同节点的 Leader 均衡。
- `balance-region-scheduler`：保持不同节点的 Peer 均衡。
- `hot-region-scheduler`：保持不同节点的读写热点 Region 均衡。
- `evict-leader-{store-id}`：驱逐某个节点的所有 Leader。（常用于滚动升级）

### Store

PD 中的 Store 指的是集群中的存储节点，也就是 tikv-server 实例。Store 与 TiKV 实例是严格一一对应的，即使在同一主机甚至同一块磁盘部署多个 TiKV 实例，这些实例也对会对应不同的 Store。

## T

### Top SQL

Top SQL 用于找到一段时间内对某个 TiDB 或 TiKV 节点消耗负载较大的 SQL 查询。详情参见 [Top SQL 用户文档](/dashboard/top-sql.md)。

### TSO

因为 TiKV 是一个分布式的储存系统，它需要一个全球性的授时服务 TSO (Timestamp Oracle)，来分配一个单调递增的时间戳。这样的功能在 TiKV 中是由 PD 提供的，在 Google 的 [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) 中是由多个原子钟和 GPS 来提供的。
