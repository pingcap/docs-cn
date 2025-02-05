---
title: TiDB 数据库的存储
summary: 了解 TiDB 数据库的存储层。
aliases: ['/docs-cn/dev/tidb-storage/']
---

# TiDB 数据库的存储

本文主要介绍 [TiKV](https://github.com/tikv/tikv) 的一些设计思想和关键概念。

![storage-architecture](/media/tidb-storage-architecture-1.png)

## Key-Value Pairs（键值对）

作为数据保存系统，首先要决定数据的存储模型，即数据的保存形式。TiKV 选择使用 Key-Value 模型，并提供有序遍历方法。

TiKV 数据存储的两个关键点：

- TiKV 实现了一个巨大的 Map（类似于 C++ 的 std::map），用于存储 Key-Value Pairs（键值对）。
- Map 中的键值对按照键的二进制顺序排序，可以通过 Seek 方法定位某个键，然后使用 Next 方法以递增顺序获取更大的键值对。

注意，TiKV 的 KV 存储模型与 SQL 中的表无关。本文不讨论 SQL 概念，专注于 TiKV 的高性能、高可靠性和分布式键值存储的实现。

## 本地存储 (RocksDB)

任何持久化的存储引擎，数据终归要保存在磁盘上，TiKV 也不例外。但是 TiKV 没有选择直接向磁盘上写数据，而是把数据保存在 RocksDB 中，具体的数据落地由 RocksDB 负责。这个选择的原因是开发一个单机存储引擎工作量很大，特别是要做一个高性能的单机引擎，需要做各种细致的优化，而 RocksDB 是由 Facebook 开源的一个非常优秀的单机 KV 存储引擎，可以满足 TiKV 对单机引擎的各种要求。这里可以简单的认为 RocksDB 是一个单机的持久化 Key-Value Map。

## Raft 协议

接下来 TiKV 的实现面临一件更难的事情：如何保证单机失效的情况下，数据不丢失，不出错？

简单来说，需要想办法把数据复制到多台机器上，这样一台机器无法服务了，其他的机器上的副本还能提供服务；复杂来说，还需要这个数据复制方案是可靠和高效的，并且能处理副本失效的情况。TiKV 选择了 Raft 算法。Raft 是一个一致性协议，本文只会对 Raft 做一个简要的介绍，细节问题可以参考它的[论文](https://raft.github.io/raft.pdf)。Raft 提供几个重要的功能：

- Leader（主副本）选举
- 成员变更（如添加副本、删除副本、转移 Leader 等操作）
- 日志复制

TiKV 利用 Raft 来做数据复制，每个数据变更都会落地为一条 Raft 日志，通过 Raft 的日志复制功能，将数据安全可靠地同步到复制组的每一个节点中。不过在实际写入中，根据 Raft 的协议，只需要同步复制到多数节点，即可安全地认为数据写入成功。

![Raft in TiDB](/media/tidb-storage-1.png)

总结一下，通过单机的 RocksDB，TiKV 可以将数据快速地存储在磁盘上；通过 Raft，将数据复制到多台机器上，以防单机失效。数据的写入是通过 Raft 这一层的接口写入，而不是直接写 RocksDB。通过实现 Raft，TiKV 变成了一个分布式的 Key-Value 存储，少数几台机器宕机也能通过原生的 Raft 协议自动把副本补全，可以做到对业务无感知。

## Region

首先，为了便于理解，在此节，假设所有的数据都只有一个副本。前面提到，TiKV 可以看做是一个巨大的有序的 KV Map，那么为了实现存储的水平扩展，数据将被分散在多台机器上。对于一个 KV 系统，将数据分散在多台机器上有两种比较典型的方案：

* Hash：按照 Key 做 Hash，根据 Hash 值选择对应的存储节点。
* Range：按照 Key 分 Range，某一段连续的 Key 都保存在一个存储节点上。

TiKV 选择了第二种方式，将整个 Key-Value 空间分成很多段，每一段是一系列连续的 Key，将每一段叫做一个 Region，可以用 [StartKey，EndKey) 这样一个左闭右开区间来描述。每个 Region 中保存的数据量默认维持在 256 MiB 左右（可以通过配置修改）。

![Region in TiDB](/media/tidb-storage-2.png)

注意，这里的 Region 还是和 SQL 中的表没什么关系。 这里的讨论依然不涉及 SQL，只和 KV 有关。

将数据划分成 Region 后，TiKV 执行两项重要操作：

- 按 Region 将数据分散到集群中的所有节点，并尽量保证每个节点上的 Region 数量大致相同。
- 以 Region 为单位进行 Raft 的复制和成员管理。

以下两点非常关键：

- 数据按 Key 切分成多个 Region，每个 Region 的数据仅保存在一个节点上（暂不考虑多副本）。TiDB 系统中的 [PD 组件](/tidb-architecture.md)负责将 Region 尽可能均匀地分布在集群节点上，实现存储容量的水平扩展（增加新节点后，会自动调度其他节点上的 Region）和负载均衡（避免某节点存储过多数据而其他节点存储较少）。为了确保上层客户端能访问所需数据，PD 组件会记录 Region 的分布情况，可通过任意 Key 查询其所在的 Region 及其对应的节点（即 Key 的位置路由信息）。

- TiKV 以 Region 为单位进行数据复制，一个 Region 的数据会保存多个副本，称为 Replica。Replica 之间通过 Raft 保持数据一致性，构成一个 Raft Group，其中一个 Replica 作为 Leader，其他作为 Follower。默认情况下，所有读写操作均通过 Leader 进行，读操作在 Leader 上即可完成，而写操作由 Leader 复制给 Follower。

大家理解了 Region 之后，应该可以理解下面这张图：

![TiDB Storage](/media/tidb-storage-3.png)

以 Region 为单位做数据的分散和复制，TiKV 就成为了一个分布式的具备一定容灾能力的 KeyValue 系统，不用再担心数据存不下，或者是磁盘故障丢失数据的问题。

## MVCC

TiKV 支持多版本并发控制 (Multi-Version Concurrency Control, MVCC)。假设有这样一种场景：某客户端 A 在写一个 Key，另一个客户端 B 同时在对这个 Key 进行读操作。如果没有数据的多版本控制机制，那么这里的读写操作必然互斥。在分布式场景下，这种情况可能会导致性能问题和死锁问题。有了 MVCC，只要客户端 B 执行的读操作的逻辑时间早于客户端 A，那么客户端 B 就可以在客户端 A 写入的同时正确地读原有的值。即使该 Key 被多个写操作修改过多次，客户端 B 也可以按照其逻辑时间读到旧的值。

TiKV 的 MVCC 是通过在 Key 后面添加版本号来实现的。没有 MVCC 时，可以把 TiKV 看作如下的 Key-Value 对：

```
Key1 -> Value
Key2 -> Value
……
KeyN -> Value
```

有了 MVCC 之后，TiKV 的 Key-Value 排列如下：

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

注意，对于同一个 Key 的多个版本，版本号较大的会被放在前面，版本号小的会被放在后面（见 [Key-Value](#key-value-pairs键值对) 一节，Key 是有序的排列），这样当用户通过一个 Key + Version 来获取 Value 的时候，可以通过 Key 和 Version 构造出 MVCC 的 Key，也就是 Key_Version。然后可以直接通过 RocksDB 的 SeekPrefix(Key_Version) API，定位到第一个大于等于这个 Key_Version 的位置。

## 分布式 ACID 事务

TiKV 的事务采用的是 Google 在 BigTable 中使用的事务模型：[Percolator](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)，TiKV 根据这篇论文实现，并做了大量的优化。详细介绍参见[事务概览](/transaction-overview.md)。
