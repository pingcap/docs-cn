---
title: TiKV 概述
summary: TiKV 存储引擎的概述。
---

# TiKV 概述

TiKV 是一个分布式事务型键值数据库，提供符合 ACID 的事务 API。通过实现 [Raft 共识算法](https://raft.github.io/raft.pdf)并将共识状态存储在 RocksDB 中，TiKV 保证了多副本之间的数据一致性和高可用性。作为 TiDB 分布式数据库的存储层，TiKV 提供读写服务，并持久化来自应用程序的写入数据。它还存储 TiDB 集群的统计数据。

## 架构概述

TiKV 基于 Google Spanner 的设计实现了多 Raft 组副本机制。Region 是键值数据移动的基本单位，指的是 Store 中的一个数据范围。每个 Region 被复制到多个节点。这些多个副本形成一个 Raft 组。Region 的一个副本称为 Peer。通常一个 Region 有 3 个 Peer。其中一个是 Leader，提供读写服务。PD 组件自动平衡所有 Region，以确保读写吞吐量在 TiKV 集群的所有节点之间保持平衡。通过 PD 和精心设计的 Raft 组，TiKV 在水平扩展性方面表现出色，可以轻松扩展到存储超过 100 TB 的数据。

![TiKV 架构](/media/tikv-arch.png)

### Region 和 RocksDB

每个 Store 内都有一个 RocksDB 数据库，它将数据存储到本地磁盘中。所有 Region 数据都存储在每个 Store 中的同一个 RocksDB 实例中。用于 Raft 共识算法的所有日志都存储在每个 Store 中的另一个 RocksDB 实例中。这是因为顺序 I/O 的性能优于随机 I/O。通过使用不同的 RocksDB 实例存储 Raft 日志和 Region 数据，TiKV 将 Raft 日志和 TiKV Region 的所有数据写入操作合并为一个 I/O 操作，以提高性能。

### Region 和 Raft 共识算法

Region 副本之间的数据一致性由 Raft 共识算法保证。只有 Region 的 Leader 才能提供写入服务，并且只有当数据写入到 Region 的大多数副本时，写入操作才会成功。

TiKV 尝试为集群中的每个 Region 保持适当的大小。Region 大小目前默认为 96 MiB。这种机制帮助 PD 组件在 TiKV 集群的节点之间平衡 Region。当 Region 的大小超过阈值（默认为 144 MiB）时，TiKV 会将其拆分为两个或多个 Region。当 Region 的大小小于阈值（默认为 20 MiB）时，TiKV 会将两个较小的相邻 Region 合并为一个 Region。

当 PD 将副本从一个 TiKV 节点移动到另一个节点时，它首先在目标节点上添加一个 Learner 副本，当 Learner 副本中的数据与 Leader 副本中的数据几乎相同时，PD 将其更改为 Follower 副本，并移除源节点上的 Follower 副本。

将 Leader 副本从一个节点移动到另一个节点的机制类似。不同之处在于，当 Learner 副本成为 Follower 副本后，会有一个"Leader 转移"操作，其中 Follower 副本主动提出选举以选举自己为 Leader。最后，新的 Leader 移除源节点中的旧 Leader 副本。

## 分布式事务

TiKV 支持分布式事务。用户（或 TiDB）可以写入多个键值对，而不用担心它们是否属于同一个 Region。TiKV 使用两阶段提交来实现 ACID 约束。详情请参见 [TiDB 乐观事务模型](/optimistic-transaction.md)。

## TiKV Coprocessor

TiDB 将一些数据计算逻辑下推到 TiKV Coprocessor。TiKV Coprocessor 处理每个 Region 的计算。发送到 TiKV Coprocessor 的每个请求只涉及一个 Region 的数据。
