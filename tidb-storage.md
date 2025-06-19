---
title: TiDB 存储
summary: 了解 TiDB 数据库的存储层。
---

# TiDB 存储

本文介绍 [TiKV](https://github.com/tikv/tikv) 的一些设计理念和关键概念。

![storage-architecture](/media/tidb-storage-architecture-1.png)

## 键值对

对于数据存储系统来说，首先要决定的是数据存储模型，即以什么形式保存数据。TiKV 选择了键值（Key-Value）模型，并提供有序遍历方法。TiKV 数据存储模型有两个关键点：

+ 这是一个巨大的 Map（类似于 C++ 中的 `std::Map`），用于存储键值对。
+ Map 中的键值对按照键的二进制顺序排序，这意味着你可以定位到特定键的位置，然后调用 Next 方法按递增顺序获取大于该键的键值对。

注意，本文描述的 TiKV 的 KV 存储模型与 SQL 表无关。本文不讨论任何与 SQL 相关的概念，仅关注如何实现一个高性能、高可靠性的分布式键值存储系统（如 TiKV）。

## 本地存储（RocksDB）

对于任何持久化存储引擎，数据最终都要保存在磁盘上，TiKV 也不例外。TiKV 不直接写入数据到磁盘，而是将数据存储在 RocksDB 中，由 RocksDB 负责数据存储。这是因为开发一个独立的存储引擎需要付出巨大的成本，特别是一个需要仔细优化的高性能独立引擎。

RocksDB 是 Facebook 开源的一个优秀的独立存储引擎。这个引擎可以满足 TiKV 对单个引擎的各种要求。在这里，你可以简单地将 RocksDB 视为一个单一的持久化键值 Map。

## Raft 协议

此外，TiKV 的实现面临着一个更困难的问题：如何在单机故障的情况下确保数据安全。

一个简单的方法是将数据复制到多台机器上，这样即使一台机器故障，其他机器上的副本仍然可用。换句话说，你需要一个可靠、高效，并且能够处理副本故障情况的数据复制方案。所有这些都可以通过 Raft 算法来实现。

Raft 是一个共识算法。本文只简要介绍 Raft。更多详细信息，你可以参考 [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf)。Raft 有几个重要特性：

- Leader 选举
- 成员变更（如添加副本、删除副本和转移 Leader）
- 日志复制

TiKV 使用 Raft 来执行数据复制。每个数据变更都会被记录为一条 Raft 日志。通过 Raft 日志复制，数据被安全可靠地复制到 Raft 组的多个节点上。但是，根据 Raft 协议，只要数据被复制到大多数节点上，写入就可以被认为是成功的。

![Raft in TiDB](/media/tidb-storage-1.png)

总的来说，TiKV 可以通过单机 RocksDB 快速地将数据存储在磁盘上，并通过 Raft 将数据复制到多台机器上以应对机器故障。数据是通过 Raft 接口而不是直接写入 RocksDB。通过实现 Raft，TiKV 成为了一个分布式键值存储系统。即使发生少数机器故障，TiKV 也可以通过原生 Raft 协议自动完成副本复制，不会影响应用。

## Region

为了便于理解，让我们假设所有数据只有一个副本。如前所述，TiKV 可以被视为一个大型的、有序的 KV Map，因此数据分布在多台机器上以实现水平扩展。对于 KV 系统，有两种典型的方案来将数据分布到多台机器上：

* Hash：通过键创建 Hash，根据 Hash 值选择对应的存储节点。
* Range：按键划分范围，将一段连续的键存储在一个节点上。

TiKV 选择了第二种方案，将整个键值空间划分为一系列连续的键段。每个段称为一个 Region。每个 Region 可以用 `[StartKey, EndKey)` 来描述，这是一个左闭右开的区间。每个 Region 的默认大小限制为 96 MiB，这个大小是可配置的。

![Region in TiDB](/media/tidb-storage-2.png)

注意，这里的 Region 与 SQL 表无关。在本文中，暂时忘记 SQL，只关注 KV。将数据划分为 Region 后，TiKV 将执行两个重要任务：

* 将数据分布到集群中的所有节点上，并以 Region 为基本单位。尽量确保每个节点上的 Region 数量大致相似。
* 在 Region 内执行 Raft 复制和成员管理。

这两个任务非常重要，让我们逐一介绍。

* 首先，数据按键被划分为许多 Region，每个 Region 的数据只存储在一个节点上（忽略多个副本）。TiDB 系统有一个 PD 组件，负责尽可能均匀地将 Region 分布在集群中的所有节点上。这样，一方面实现了存储容量的水平扩展（其他节点上的 Region 会自动调度到新添加的节点）；另一方面实现了负载均衡（避免出现一个节点数据很多而其他节点数据很少的情况）。

    同时，为了确保上层客户端能够访问所需的数据，系统中有一个组件（PD）记录 Region 在节点上的分布情况，即通过任何键都能知道这个键属于哪个 Region 以及该 Region 位于哪个节点。

* 对于第二个任务，TiKV 在 Region 内复制数据，这意味着一个 Region 的数据会有多个副本，称为"Replica"。一个 Region 的多个副本存储在不同的节点上，形成一个 Raft Group，通过 Raft 算法保持一致性。

    其中一个副本作为该组的 Leader，其他作为 Follower。默认情况下，所有的读写操作都通过 Leader 处理，其中读操作在 Leader 上执行，写操作则复制到 Follower。下图展示了关于 Region 和 Raft Group 的完整图景。

![TiDB Storage](/media/tidb-storage-3.png)

通过在 Region 中分布和复制数据，我们得到了一个在某种程度上具有容灾能力的分布式键值系统。你不再需要担心容量问题，也不用担心磁盘故障和数据丢失。

## MVCC

TiKV 支持多版本并发控制（MVCC）。考虑一个场景，客户端 A 正在写入一个键的同时，客户端 B 正在读取同一个键。如果没有 MVCC 机制，这些读写操作将互相排斥，在分布式场景下会带来性能问题和死锁。然而，有了 MVCC，只要客户端 B 在客户端 A 写入操作的逻辑时间之前执行读操作，那么在客户端 A 执行写入操作的同时，客户端 B 就可以正确读取原始值。即使这个键被多个写操作修改多次，客户端 B 仍然可以根据其逻辑时间读取旧值。

TiKV 的 MVCC 是通过在键后面附加版本号来实现的。没有 MVCC 时，TiKV 的键值对如下：

```
Key1 -> Value
Key2 -> Value
……
KeyN -> Value
```

有了 MVCC 后，TiKV 的键值对如下：

```
Key1_Version3 -> Value
Key1_Version2 -> Value
Key1_Version1 -> Value
……
Key2_Version4 -> Value
Key2_Version3 -> Value
Key2_Version2 -> Value
Key2_Version1 -> Value
……
KeyN_Version2 -> Value
KeyN_Version1 -> Value
……
```

注意，对于同一个键的多个版本，版本号较大的会被放在前面（参见[键值对](#键值对)部分，键是按顺序排列的），这样当你通过 Key + Version 获取 Value 时，MVCC 的键可以用 Key 和 Version 构造出来，即 `Key_Version`。然后可以直接通过 RocksDB 的 `SeekPrefix(Key_Version)` API 定位到大于或等于这个 `Key_Version` 的第一个位置。

## 分布式 ACID 事务

TiKV 的事务采用了 Google 在 BigTable 中使用的模型：[Percolator](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)。TiKV 的实现受到这篇论文的启发，并进行了大量优化。详情请参见[事务概览](/transaction-overview.md)。
