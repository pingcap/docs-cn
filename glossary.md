---
title: 术语表
summary: 了解 TiDB 相关术语。
---

# 术语表

本术语表提供了 TiDB 中的关键术语定义。

此外，你还可以参考以下术语表：

- [TiDB Data Migration 术语表](/dm/dm-glossary.md)
- [TiCDC 术语表](/ticdc/ticdc-glossary.md)
- [TiDB Lightning 术语表](/tidb-lightning/tidb-lightning-glossary.md)

## A

### ACID

ACID 是指数据库管理系统在写入或更新资料的过程中，为保证事务是正确可靠的，所必须具备的四个特性：原子性 (atomicity)、一致性 (consistency)、隔离性 (isolation) 以及持久性 (durability)。

* 原子性 (atomicity) 指一个事务中的所有操作，或者全部完成，或者全部不完成，不会结束在中间某个环节。TiDB 通过 Primary Key 所在 [Region](#regionpeerraft-group) 的原子性来保证分布式事务的原子性。
* 一致性 (consistency) 指在事务开始之前和结束以后，数据库的完整性没有被破坏。TiDB 在写入数据之前，会校验数据的一致性，校验通过才会写入内存并返回成功。
* 隔离性 (isolation) 指数据库允许多个并发事务同时对其数据进行读写和修改的能力。隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致，主要用于处理并发场景。关于 TiDB 支持的隔离级别，请参考 [TiDB 事务隔离级别](/transaction-isolation-levels.md#tidb-事务隔离级别)。
* 持久性 (durability) 指事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。在 TiDB 中，事务一旦提交成功，数据全部持久化存储到 TiKV，此时即使 TiDB 服务器宕机也不会出现数据丢失。

## B

### Backup & Restore (BR)

**Backup & Restore** 或 **BR** 指代 [TiDB 备份恢复功能](/br/backup-and-restore-overview.md)。

`br` 指代进行 TiDB 备份或恢复时使用的 [br 命令行工具](/br/use-br-command-line-tool.md)。

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

### Column Family (CF)

在 RocksDB 和 TiKV 中，Column Family (CF，列族) 表示数据库中键值对的逻辑分组。

### 公共表表达式 (CTE)

公共表表达式 (Common Table Expression, CTE) 用于定义一个临时结果集，能够在 SQL 语句中通过 [`WITH`](/sql-statements/sql-statement-with.md) 子句多次引用。更多信息，请参见[公共表表达式](/develop/dev-guide-use-common-table-expression.md)。

### Continuous Profiling

持续性能分析 (Continuous Profiling) 是从 TiDB v5.3 起引入的一种从系统调用层面解读资源开销的方法。引入该方法后，TiDB 可提供数据库源码级性能观测，通过火焰图的形式帮助研发、运维人员定位性能问题的根因。详情参见 [TiDB Dashboard 实例性能分析 - 持续分析页面](/dashboard/continuous-profiling.md)。

## D

### Data Definition Language (DDL)

数据定义语言 (Data Definition Language, DDL) 是 SQL 标准的一部分，用于创建、修改和删除表及其他对象。更多信息，请参见 [DDL 语句的执行原理及最佳实践](/ddl-introduction.md)。

### Data Migration (DM)

Data Migration (DM) 是 TiDB 提供的一款数据迁移工具，用于将数据从 MySQL 兼容的数据库迁移到 TiDB。DM 会从 MySQL 兼容的数据库实例读取数据，然后将其应用到 TiDB 目标实例中。更多信息，请参见 [TiDB Data Migration 简介](/dm/dm-overview.md)。

### Data Modification Language (DML)

数据操作语言 (Data Modification Language, DML) 是 SQL 标准的一部分，用于插入、更新和删除表中的行数据。

### Development Milestone Release (DMR)

TiDB 会在开发里程碑版本 (Development Milestone Release, DMR) 中引入新的功能，但 DMR 不提供长期支持。更多信息，请参见 [TiDB 版本规则](/releases/versioning.md)。

### 容灾 (DR)

容灾 (Disaster Recovery, DR) 是在未来灾难发生时恢复数据和服务的解决方案。TiDB 提供了多种容灾方案，例如备份和复制数据到备用集群。更多信息，请参见 [TiDB 容灾方案概述](/dr-solution-introduction.md)。

### 分布式执行框架 (DXF)

分布式执行框架 (Distributed eXecution Framework, DXF) 允许 TiDB 在处理特定任务（例如创建索引或导入数据）时对这些任务进行统一调度和分布式执行。该框架旨在高效利用集群资源执行任务，控制资源使用，以减少对核心业务事务的影响。更多信息，请参见 [TiDB 分布式执行框架](/tidb-distributed-execution-framework.md)。

### Dynamic Pruning

动态裁剪 (Dynamic Pruning) 是 TiDB 访问分区表的两种模式之一。在动态裁剪模式下，TiDB 的每个算子都支持直接访问多个分区，省略 Union 操作，提高执行效率，还避免了 Union 并发管理的问题。

## G

### Garbage Collection (GC)

垃圾回收 (Garbage Collection, GC) 指清理不再需要的旧数据以释放资源的过程。关于 TiKV 垃圾回收过程的详情，请参见[垃圾回收概述](/garbage-collection-overview.md)。

### General Availability (GA)

一个功能 GA (General Availability) 意味着该功能已进行充分测试并可在生产环境中使用。根据每个功能的开发情况不同，TiDB 中的新功能可能会在[开发里程碑版本 (DMR)](#development-milestone-release-dmr) 中 GA，也可能会在[长期支持版本 (LTS)](#long-term-support-lts) 中 GA 。由于 TiDB 不提供基于 DMR 的补丁版本，在生产环境中建议使用 LTS 版本。

### Global Transaction Identifiers (GTIDs)

全局事务标识符 (Global Transaction Identifiers, GTIDs) 是在 MySQL 二进制日志中跟踪已复制事务的唯一标识符。[Data Migration (DM)](/dm/dm-overview.md) 在迁移数据时会使用这些标识符确保复制的一致性。

## H

### Hybrid Transactional and Analytical Processing (HTAP)

混合型在线事务与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 功能支持在同一数据库中同时处理 OLTP（联机事务处理）和 OLAP（联机分析处理）工作负载。在 TiDB 中，HTAP 是通过使用 TiKV 进行行存以及使用进行 TiFlash 进行列存来实现的。更多信息，请参见 [Gartner 网站上的 HTAP 定义](https://www.gartner.com/en/information-technology/glossary/htap-enabling-memory-computing-technologies)。

## I

### In-Memory Pessimistic Lock

内存悲观锁 (In-Memory Pessimistic Lock) 是在 TiDB v6.0.0 中引入的新功能。开启内存悲观锁功能后，悲观锁通常只会被存储在 Region leader 的内存中，而不会将锁持久化到磁盘，也不会通过 Raft 协议将锁同步到其他副本，因此可以大大降低悲观事务加锁的开销，提升悲观事务的吞吐并降低延迟。

### Index Merge

索引合并 (Index Merge) 是在 TiDB v4.0 版本中作为实验特性引入的一种查询执行方式的优化，可以大幅提高查询在扫描多列数据时条件过滤的效率。自 v5.4 版本起，Index Merge 成为正式功能，详情参见[用 EXPLAIN 查看索引合并的 SQL 执行计划](/explain-index-merge.md)。

## K

### Key Management Service (KMS)

密钥管理服务 (Key Management Service, KMS) 提供了一种存储和检索密钥的安全方式。常见的 KMS 包括 AWS KMS、Google Cloud KMS 和 HashiCorp Vault。TiDB 中的多个组件都支持通过 KMS 管理用于存储加密和相关服务的密钥。

### Key-Value (KV)

键值 (Key-Value, KV) 是一种通过唯一键来关联值并存储信息的数据结构，它能够实现快速的数据检索。TiDB 通过 TiKV 将表和索引映射为键值对，从而实现数据库中的高效数据存储和访问。

## L

### Leader/Follower/Learner

它们分别对应 [Peer](#regionpeerraft-group) 的三种角色。其中 Leader 负责响应客户端的读写请求；Follower 被动地从 Leader 同步数据，当 Leader 失效时会进行选举产生新的 Leader；Learner 是一种特殊的角色，它只参与同步 raft log 而不参与投票，在目前的实现中只短暂存在于添加副本的中间步骤。

### Lightweight Directory Access Protocol (LDAP)

轻量级目录访问协议 (Lightweight Directory Access Protocol, LDAP) 是一种标准化的目录信息访问方式，通常用于账户和用户数据的管理。TiDB 对 LDAP 的支持是通过 [LDAP 身份验证插件](/security-compatibility-with-mysql.md#可用的身份验证插件)实现的。

### Long Term Support (LTS)

长期支持 (Long Term Support, LTS) 版本指经过充分测试并在较长时间内维护的软件版本。更多信息，请参见 [TiDB 版本规则](/releases/versioning.md)。

## M

### Massively Parallel Processing (MPP)

从 v5.0 起，TiDB 通过 TiFlash 节点引入了 Massively Parallel Processing (MPP) 架构。这使得大型表连接类查询可以由不同 TiFlash 节点共同分担完成。当 MPP 模式开启后，TiDB 将会根据代价决定是否应该交由 MPP 框架进行计算。MPP 模式下，表连接将通过对 JOIN Key 进行数据计算时重分布（Exchange 操作）的方式把计算压力分摊到各个 TiFlash 执行节点，从而达到加速计算的目的。更多信息请参见[使用 MPP 模式](/tiflash/use-tiflash-mpp-mode.md)。

### Multi-version concurrency control (MVCC)

[MVCC](https://zh.wikipedia.org/wiki/多版本并发控制)（多版本并发控制）是 TiDB 和其他数据库中的一种并发控制机制。它处理事务的内存读取，以实现对 TiDB 的并发访问，从而避免由并发读写冲突引起的阻塞。

## O

### Old value

Old value 特指在 TiCDC 输出的增量变更日志中的“原始值”。可以通过配置来指定 TiCDC 输出的增量变更日志是否包含“原始值”。

### Online Analytical Processing (OLAP)

在线分析处理 (Online Analytical Processing, OLAP) 指的是以分析任务为主的数据库工作负载，例如数据报告和复杂查询。OLAP 的特点是涉及大量行数据的读密集型查询。

### Online Transaction Processing (OLTP)

在线事务处理 (Online Transaction Processing, OLTP) 指的是以事务性任务为主的数据库工作负载，例如读取、插入、更新和删除少量记录。

### Out of Memory (OOM)

内存不足 (Out of Memory, OOM) 指的是系统由于内存不足而引起失败的情况。更多信息，请参见 [TiDB OOM 故障排查](/troubleshoot-tidb-oom.md)。

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

### Placement Driver (PD)

PD 是 [TiDB 架构](/tidb-architecture.md) 中的核心组件之一，负责存储元数据，为事务时间戳分配[时间戳服务 (TSO)](/tso.md)，协调 TiKV 上的数据分布，并运行 [TiDB Dashboard](/dashboard/dashboard-overview.md)。更多信息，请参见 [TiDB 调度](/tidb-scheduling.md)。

### Point get

点查 (point get) 是指通过主键或唯一索引直接读取一行的查询方式。点查的返回结果最多是一行数据。

### Point in Time Recovery (PITR)

PITR 用于将数据恢复到特定时间点（例如，在意外执行了 `DELETE` 语句之前的时间点）。更多信息，请参见 [TiDB 日志备份与 PITR 功能架构](/br/br-log-architecture.md)。

### Predicate columns

执行 SQL 语句时，优化器在大多数情况下只会用到部分列（例如，`WHERE`、`JOIN`、`ORDER BY`、`GROUP BY` 子句中出现的列）的统计信息，这些用到的列称为 `PREDICATE COLUMNS`。详情参见[收集部分列的统计信息](/statistics.md#收集部分列的统计信息)。

## Q

### Queries Per Second (QPS)

每秒查询数 (Queries Per Second, QPS) 指的是数据库服务每秒处理的查询数量。它是衡量数据库吞吐量的重要性能指标。

### Quota Limiter

前台限流 (Quota Limiter) 是在 TiDB v6.0.0 版本中作为实验特性引入的功能。当 TiKV 部署的机型资源有限（如 4v CPU，16 G 内存）时，如果 TiKV 前台处理的读写请求量过大，会占用 TiKV 后台处理请求所需的 CPU 资源，最终影响 TiKV 性能的稳定性。此时，开启前台限流相关的 [quota 相关配置项](/tikv-configuration-file.md#quota)可以限制前台各类请求占用的 CPU 资源。

## R

### Raft Engine

一种内置的持久化存储引擎，有着日志结构的设计，为 TiKV 提供 multi-Raft 日志存储。从 v5.4 起，TiDB 支持使用 Raft Engine 作为 TiKV 的日志存储引擎。详情参见 [Raft Engine](/tikv-configuration-file.md#raft-engine)。

### Region Split

TiKV 集群中的 Region 不是一开始就划分好的，而是随着数据写入逐渐分裂生成的，分裂的过程被称为 Region Split。

其机制是集群初始化时构建一个初始 Region 覆盖整个 key space，随后在运行过程中每当 Region 大小或 Key 数量达到阈值之后就通过 Split 产生新的 Region。

### Region/Peer/Raft Group

每个 Region 负责维护集群的一段连续数据（默认配置下平均约 256 MiB），每份数据会在不同的 Store 存储多个副本（默认配置是 3 副本），每个副本称为 Peer。同一个 Region 的多个 Peer 通过 raft 协议进行数据同步，所以 Peer 也用来指代 raft 实例中的成员。TiKV 使用 multi-raft 模式来管理数据，即每个 Region 都对应一个独立运行的 raft 实例，我们也把这样的一个 raft 实例叫做一个 Raft Group。

### Remote Procedure Call (RPC)

RPC（远程过程调用）是软件组件之间的一种通信方式。在 TiDB 集群中，不同组件（例如 TiDB、TiKV 和 TiFlash）之间使用 gRPC 标准进行通信。

### Request Unit (RU)

RU 是 TiDB 中资源使用的统一抽象单位，用于在[资源管控](/tidb-resource-control.md)功能中衡量资源的使用情况。

### Restore

备份操作的逆过程，即利用保存的备份数据还原出原始数据的过程。

## S

### Scheduler

Scheduler（调度器）是 PD 中生成调度的组件。PD 中每个调度器是独立运行的，分别服务于不同的调度目的。常用的调度器及其调用目标有：

- `balance-leader-scheduler`：保持不同节点的 Leader 均衡。
- `balance-region-scheduler`：保持不同节点的 Peer 均衡。
- `hot-region-scheduler`：保持不同节点的读写热点 Region 均衡。
- `evict-leader-{store-id}`：驱逐某个节点的所有 Leader。（常用于滚动升级）

### Static Sorted Table / Sorted String Table (SST)

SST 是 RocksDB 使用的文件存储格式。RocksDB 是 [TiKV](/storage-engine/rocksdb-overview.md) 的一种存储引擎。

### Store

PD 中的 Store 指的是集群中的存储节点，也就是 tikv-server 实例。Store 与 TiKV 实例是严格一一对应的，即使在同一主机甚至同一块磁盘部署多个 TiKV 实例，这些实例也对会对应不同的 Store。

## T

### Timestamp Oracle (TSO)

因为 TiKV 是一个分布式的储存系统，它需要一个全球性的授时服务 TSO (Timestamp Oracle)，来分配一个单调递增的时间戳。这样的功能在 TiKV 中是由 PD 提供的，在 Google 的 [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) 中是由多个原子钟和 GPS 来提供的。详见 [TSO 文档](/tso.md)。

### Top SQL

Top SQL 用于找到一段时间内对某个 TiDB 或 TiKV 节点消耗负载较大的 SQL 查询。详见 [Top SQL 文档](/dashboard/top-sql.md)。

### Transactions Per Second (TPS)

每秒事务数 (Transactions Per Second, TPS) 指的是数据库每秒处理的事务数量。它是衡量数据库性能和吞吐量的关键指标。

## U

### Uniform Resource Identifier (URI)

统一资源标识符 (Uniform Resource Identifier, URI) 是用于标识资源的一种标准化格式。更多信息，请参见维基百科的[统一资源标识符](https://zh.wikipedia.org/wiki/统一资源标识符)页面。

### Universally Unique Identifier (UUID)

通用唯一标识符 (Universally Unique Identifier, UUID) 是一种 128 位（16 字节）的生成 ID，用于在数据库中唯一地标识记录。更多信息，请参见 [UUID](/best-practices/uuid.md)。