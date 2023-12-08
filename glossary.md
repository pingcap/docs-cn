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
* 隔离性 (isolation) 指数据库允许多个并发事务同时对其数据进行读写和修改的能力。隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致，主要用于处理并发场景。TiDB 目前只支持一种隔离级别，即可重复读。
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

### Binlog

在 TiDB 中，Binlog 指由 TiDB、MySQL 或 MariaDB 生成的一种二进制日志 (binary log)，用于记录 TiDB 或上下游的数据库表结构变更（例如 `CREATE`、`ALTER TABLE` 语句等）和表数据修改（例如 `INSERT`、`DELETE`、`UPDATE` 语句等）。

### Bucket

一个 [Region](#regionpeerraft-group) 在逻辑上划分为多个小范围，称为 bucket。TiKV 按 bucket 收集查询统计数据，并将 bucket 的情况报告给 PD。详情参见 [Bucket 设计文档](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket)。

## C

### Cached Table

缓存表 (Cached Table) 是指 TiDB 把整张表的数据加载到服务器的内存中，直接从内存中获取表数据，避免从 TiKV 获取表数据，从而提升读性能。详情参见[缓存表](/cached-tables.md)。

### Cluster

TiDB 数据库以及各组件的集合，部署在多节点服务器上，每个节点上运行实例，向客户端提供服务。

### Coalesce Partition

Coalesce Partition 是一种减少 Hash 分区表或 Key 分区表中分区数量的方法。详情参见[管理 Hash 分区和 Key 分区](/partitioned-table.md#管理-hash-分区和-key-分区)。

### Common table expression (CTE)

公共表表达式 (CTE) 是一个临时的中间结果集，能够在 SQL 语句中引用多次，提高 SQL 语句的可读性与执行效率。在 TiDB 中可以通过 `WITH` 语句使用公共表表达式。公共表表达式分为非递归和递归两种类型。

详情参见[公共表表达式 (CTE)](/develop/dev-guide-use-common-table-expression.md)。

### Continuous Profiling

持续性能分析 (Continuous Profiling) 是从 TiDB v5.3 起引入的一种从系统调用层面解读资源开销的方法。引入该方法后，TiDB 可提供数据库源码级性能观测，通过火焰图的形式帮助研发、运维人员定位性能问题的根因。详情参见 [TiDB Dashboard 实例性能分析 - 持续分析页面](/dashboard/continuous-profiling.md)。

### Coprocessor

一种替 TiDB 分担计算的协处理机制。位于存储层（TiKV 或 TiFlash），以 Region 为单位协同处理从 TiDB 下推的计算。

## D

### Dumpling

Dumpling 是一款数据导出工具，用于将存储在 TiDB 或 MySQL 中的数据导出为 SQL 或 CSV 格式，用于逻辑全量备份。Dumpling 也支持将数据导出到 Amazon S3 中。详情参见[使用 Dumpling 导出数据](/dumpling-overview.md)。

### Dynamic Pruning

动态裁剪 (Dynamic Pruning) 是 TiDB 访问分区表的两种模式之一。在动态裁剪模式下，TiDB 的每个算子都支持直接访问多个分区，省略 Union 操作，提高执行效率，还避免了 Union 并发管理的问题。

## E

### Expression index

表达式索引 (expression index) 是一种特殊的索引，能将索引建立于表达式上。在创建了表达式索引后，基于表达式的查询便可以使用上索引，极大提升查询的性能。

详情参见 [CREATE INDEX - 表达式索引](/sql-statements/sql-statement-create-index.md#表达式索引)。

## G

### GC (Garbage Collection)

垃圾回收（GC 或 Garbage collection）是 TiDB 中的内存资源管理机制。当不再需要动态内存里的旧数据时，便予以清理，让出内存。详情参见 [GC 机制](/garbage-collection-overview.md)。

## H

### Hotspot

热点 (Hotspot) 指 TiKV 的读写负载集中于某一个或几个 Region 或节点的现象，此时可能会造成性能瓶颈，使性能无法达到最佳。要解决热点问题，可参考 [TiDB 热点问题处理](/troubleshoot-hot-spot-issues.md)。

### HTAP

全称为 "Hybrid Transactional and Analytical Processing"，即在线事务与在线分析处理。TiDB HTAP 可以满足企业海量数据的增长需求、降低运维的风险成本、与现有的大数据栈无缝缝合，从而实现数据资产价值的实时变现。在 TiDB 中，面向在线事务处理的行存储引擎 TiKV 与面向实时分析场景的列存储引擎 TiFlash 同时存在，自动同步，保持强一致性。

详情参见 [HTAP 快速上手指南](/quick-start-with-htap.md)和 [HTAP 深入探索指南](/explore-htap.md)。

## I

### Index Merge

索引合并 (Index Merge) 是在 TiDB v4.0 版本中作为实验特性引入的一种查询执行方式的优化，可以大幅提高查询在扫描多列数据时条件过滤的效率。自 v5.4 版本起，Index Merge 成为正式功能，详情参见[用 EXPLAIN 查看索引合并的 SQL 执行计划](/explain-index-merge.md)。

### In-Memory Pessimistic Lock

内存悲观锁 (In-Memory Pessimistic Lock) 是在 TiDB v6.0.0 中引入的新功能。开启内存悲观锁功能后，悲观锁通常只会被存储在 Region leader 的内存中，而不会将锁持久化到磁盘，也不会通过 Raft 协议将锁同步到其他副本，因此可以大大降低悲观事务加锁的开销，提升悲观事务的吞吐并降低延迟。

## L

### Leader/Follower/Learner

它们分别对应 [Peer](#regionpeerraft-group) 的三种角色。其中 Leader 负责响应客户端的读写请求；Follower 被动地从 Leader 同步数据，当 Leader 失效时会进行选举产生新的 Leader；Learner 是一种特殊的角色，它只参与同步 raft log 而不参与投票，在目前的实现中只短暂存在于添加副本的中间步骤。

### Lock View

Lock View 特性用于提供关于悲观锁的锁冲突和锁等待的更多信息，方便 DBA 通过锁视图功能来观察事务加锁情况以及排查死锁问题。

详情参见系统表文档 [TIDB_TRX](/information-schema/information-schema-tidb-trx.md)、[DATA_LOCK_WAITS](/information-schema/information-schema-data-lock-waits.md) 和 [DEADLOCKS](/information-schema/information-schema-deadlocks.md)。

## M

### MPP

从 v5.0 起，TiDB 通过 TiFlash 节点引入了 Massively Parallel Processing (MPP) 架构。这使得大型表连接类查询可以由不同 TiFlash 节点共同分担完成。当 MPP 模式开启后，TiDB 将会根据代价决定是否应该交由 MPP 框架进行计算。MPP 模式下，表连接将通过对 JOIN Key 进行数据计算时重分布（Exchange 操作）的方式把计算压力分摊到各个 TiFlash 执行节点，从而达到加速计算的目的。更多信息请参见[使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

详情参见[使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### Multi-version concurrency control (MVCC)

TiDB 中的并发控制机制，对事务内读取到的内存做处理，实现对 TiDB 的并发访问，避免并发读写冲突造成的阻塞。

## O

### Old value

Old value 特指在 TiCDC 输出的增量变更日志中的“原始值”。可以通过配置来指定 TiCDC 输出的增量变更日志是否包含“原始值”。

### Online transactional processing (OLTP)

全称为在线事务处理，即使用计算机系统来处理事务数据。

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

### Optimistic transaction

使用乐观并发控制的事务，在并发环境中，外界对数据的操作一般不会造成冲突。开启乐观事务后，TiDB 只在事务最终提交时才会检测冲突。乐观事务模式适合读多写少的并发场景，能提高 TiDB 性能。

自 v3.0.8 开始，TiDB 集群默认使用悲观事务模式。但如果从 3.0.7 及之前版本创建的集群升级到 3.0.8 及之后的版本，不会改变默认事务模式，即只有新创建的集群才会默认使用悲观事务模式。详情参见 [TiDB 乐观事务模型](/optimistic-transaction.md)。

## P

### Partitioning

[Partitioning](/partitioned-table.md)（分区）指通过 `RANGE`、`LIST`、`HASH` 和 `KEY` 等分区方法在物理上将一张表划分为较小的分区。这些较小的分区为分区表 (Partitioned Table)。

### PD Control (pd-ctl)

PD Control（或 pd-ctl）是 PD 的命令行工具，用于获取集群状态信息和调整集群。详情参见 [PD Control 使用说明](/pd-control.md)。

### Pending/Down

Pending 和 Down 是 Peer 可能出现的两种特殊状态。其中 Pending 表示 Follower 或 Learner 的 raft log 与 Leader 有较大差距，Pending 状态的 Follower 无法被选举成 Leader。Down 是指 Leader 长时间没有收到对应 Peer 的消息，通常意味着对应节点发生了宕机或者网络隔离。

### Placement Rules

Placement Rules 特性用于通过 SQL 接口配置数据在 TiKV 集群中的放置位置。通过该功能，用户可以将表和分区指定部署至不同的地域、机房、机柜、主机。适用场景包括低成本优化数据高可用策略、保证本地的数据副本可用于本地 Stale Read 读取、遵守数据本地要求等。

详情参见 [Placement Rules in SQL](/placement-rules-in-sql.md)。

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

每个 Region 负责维护集群的一段连续数据（默认配置下平均约 96 MiB），每份数据会在不同的 Store 存储多个副本（默认配置是 3 副本），每个副本称为 Peer。同一个 Region 的多个 Peer 通过 raft 协议进行数据同步，所以 Peer 也用来指代 raft 实例中的成员。TiKV 使用 multi-raft 模式来管理数据，即每个 Region 都对应一个独立运行的 raft 实例，我们也把这样的一个 raft 实例叫做一个 Raft Group。

### Region Split

TiKV 集群中的 Region 不是一开始就划分好的，而是随着数据写入逐渐分裂生成的，分裂的过程被称为 Region Split。

其机制是集群初始化时构建一个初始 Region 覆盖整个 key space，随后在运行过程中每当 Region 数据达到一定量之后就通过 Split 产生新的 Region。

### Restore

备份操作的逆过程，即利用保存的备份数据还原出原始数据的过程。

### RocksDB

一款提供键值存储与读写功能的 LSM-tree 架构引擎，由 Facebook 基于 LevelDB 开发。RocksDB 是 TiKV 的核心存储引擎，用于存储 Raft 日志以及用户数据。

## S

### Scheduler

Scheduler（调度器）是 PD 中生成调度的组件。PD 中每个调度器是独立运行的，分别服务于不同的调度目的。常用的调度器及其调用目标有：

- `balance-leader-scheduler`：保持不同节点的 Leader 均衡。
- `balance-region-scheduler`：保持不同节点的 Peer 均衡。
- `hot-region-scheduler`：保持不同节点的读写热点 Region 均衡。
- `evict-leader-{store-id}`：驱逐某个节点的所有 Leader。（常用于滚动升级）

### Security Enhanced Mode

即安全增强模式，用于对 TiDB 管理员进行更细粒度的权限划分。安全增强模式受[安全增强式 Linux](https://zh.wikipedia.org/wiki/安全增强式Linux) 等系统设计的启发，削减拥有 MySQL `SUPER` 权限的用户能力，转而使用细粒度的 `RESTRICTED` 权限作为替代。

详情参见[系统变量文档 - `tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)。

### Stale Read

Stale Read 是一种读取历史数据版本的机制，读取 TiDB 中存储的历史数据版本。通过 Stale Read 功能，你能从指定时间点或时间范围内读取对应的历史数据，从而避免数据同步带来延迟。当使用 Stale Read 时，TiDB 默认会随机选择一个副本来读取数据，因此能利用所有副本。

详情参见 [Stale Read](/stale-read.md)。

### Store

PD 中的 Store 指的是集群中的存储节点，也就是 tikv-server 实例。Store 与 TiKV 实例是严格一一对应的，即使在同一主机甚至同一块磁盘部署多个 TiKV 实例，这些实例也对会对应不同的 Store。

## T

### Temporary table

临时表 (temporary table) 解决了业务中间计算结果的临时存储问题，让用户免于频繁地建表和删表等操作。用户可将业务上的中间计算数据存入临时表，用完数据后 TiDB 自动清理回收临时表。这避免了用户业务过于复杂，减少了表管理开销，并提升了性能。

详情参见[临时表](/temporary-tables.md)。

### TiCDC

[TiCDC](/ticdc/ticdc-overview.md) 是一款 TiDB 增量数据同步工具，通过拉取上游 TiKV 的数据变更日志，TiCDC 可以将数据解析为有序的行级变更数据输出到下游。更多关于 TiCDC 的概念和术语，参见 [TiCDC 术语表](/ticdc/ticdc-glossary.md)。

### TiDB Data Migration (DM)

[TiDB Data Migration (DM)](/dm/dm-overview.md) 是一款便捷的数据迁移工具，支持从与 MySQL 协议兼容的数据库（MySQL、MariaDB、Aurora MySQL）到 TiDB 的全量数据迁移和增量数据同步。使用 DM 工具有利于简化数据迁移过程，降低数据迁移运维成本。

更多关于 DM 的概念和术语，参见 [TiDB Data Migration 术语表](/dm/dm-glossary.md)。

### TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是一款数据导入工具，用于从静态文件导入 TB 级数据到 TiDB 集群，常用于 TiDB 集群的初始化数据导入。

更多关于 TiDB Lightning 的概念和术语，参见 [TiDB Lightning 术语表](/tidb-lightning/tidb-lightning-glossary.md)。

### TiFlash

[TiFlash](/tiflash/tiflash-overview.md) 是 TiDB HTAP 形态的关键组件，它是 TiKV 的列存扩展，在提供良好隔离性的同时，也兼顾了强一致性。列存副本通过 Raft Learner 协议异步复制，但是在读取的时候通过 Raft 校对索引配合 MVCC 的方式获得 Snapshot Isolation 的一致性隔离级别。这个架构很好地解决了 HTAP 场景的隔离性以及列存同步的问题。

### TiUP

[TiUP](/tiup/tiup-overview.md) 是 TiDB 于 v4.0 版本引入的包管理工具，用于 TiDB 集群的部署、升级、管理，管理着 TiDB 生态下众多的组件，如 TiDB、PD、TiKV 等。用户想要运行 TiDB 生态中任何组件时，只需要执行 TiUP 一行命令即可，相比以前，大大降低了管理难度。

### Top SQL

Top SQL 用于找到一段时间内对某个 TiDB 或 TiKV 节点消耗负载较大的 SQL 查询。详情参见 [Top SQL 用户文档](/dashboard/top-sql.md)。

### TSO

因为 TiKV 是一个分布式的储存系统，它需要一个全球性的授时服务 TSO (Timestamp Oracle)，来分配一个单调递增的时间戳。这样的功能在 TiKV 中是由 PD 提供的，在 Google 的 [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) 中是由多个原子钟和 GPS 来提供的。

### TTL

[Time to Live (TTL)](/time-to-live.md) 提供了行级别的生命周期控制策略。通过为表设置 TTL 属性，TiDB 可以周期性地自动检查并清理表中的过期数据。
