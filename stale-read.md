---
title: Stale Read 功能使用场景介绍
aliases: ['/docs-cn/dev/stale-read/']
---

# Stale Read 功能介绍

Stale Read 是 TiDB 提供快速读取数据的一种机制。Stale Read 功能允许用户通过指定时间点或时间范围的方式读取一定程度上的历史数据（使用 [AS OF TIMESTAMP 语法](/as-of-timestamp.md)）。通过 Stale Read，TiDB 可以从任意一个副本上读取到所给定时间点或时间范围内尽可能新的数据，并在这个过程中始终保证数据的一致性约束。

# 使用场景

在一些跨数据中心部署的场景中，上层应用或业务所请求的大部分事务类型都是只读事务，只存在部分只写事务或读写事务。对于读写事务或者只写事务，业务应用可以容忍一定程度的延迟代价，但是对只读事务来说，其对延迟和 QPS 都有较高的要求。在达到延迟与 QPS 要求的基础上，此类只读事务往往也能够容忍读到一定程度的旧数据，即偏斜的数据（Stale Data）。在 Stale Read 功能中，TiDB 通过牺牲*只读事务*所能读到数据的实效性，并允许从更近距离的副本中读取数据，来在数据跨中心的部署场景中提供更好的读性能。由于 TiDB 使用了 Raft 来作为集群内的副本一致性共识算法，传统的读请求需要由多个副本中的 Leader 角色提供，即便引入了 [Follower Read](/follower-read.md) 功能来减少 Leader 对读请求的处理压力，但为了保证一致性读（Consistent Read）————即在 Follower 上读到的数据在 Leader 上也一定能读到，反之亦然————副本中的 Follower 角色需要在处理读请求之前与 Leader 进行通信，确保自身的数据同步进度至少与 Leader 一样才可以对外提供读请求的处理服务。在跨中心部署的场景下，延迟对上述过程所带来的影响会变得显著，从而降低集群对读请求的处理能力。Stale Read 通过引入类似安全时间节点的机制，达成一致性读的同时减少副本间的进度同步开销，并结合从地理位置更近的副本中读取，在多区域部署中带来更好的延迟表现。

# 使用方式

如前所述，TiDB 提供两种 Stale Read 的方式，分别是指定一个精确的时间点和一个时间范围，两者的区别如下：

- 精确时间点：通过指定一个时间戳，确保读到该指定时间点下保证全局事务记录一致性的数据，不破坏隔离级别，但可能读到旧数据。该功能通过 [AS OF TIMESTAMP 语法](/as-of-timestamp.md#语法方式)提供。
- 时间范围：通过指定一个时间范围，确保读到在该时间范围内尽可能新的数据，不破坏隔离级别，但可能读到旧数据。该功能通过 [AS OF TIMESTAMP 语法](/as-of-timestamp.md#语法方式) 和 [TIDB_BOUNDED_STALENESS 函数](/as-of-timestamp.md#语法方式)实现。

除了语法的使用，Stale Read 通常需要配合 TiDB 的 Geo-Partition 部署来进一步在跨中心部署场景中获得更好的性能表现，具体可见[Geo-Partition 使用文档](/configure-geo-partition.md)。