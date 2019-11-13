---
title: Follower Read
category: reference
---

# Follower Read

TiDB 3.1 新增了 follower read 功能，在强一致性读的前提下使用 region 的 follower 副本来承载数据读取的任务。提升 TiDB 集群的吞吐能力并降低 leader 负载。

## 什么是 follower read
Follower read 包含一系列将 TiKV 读取负载从 region 的 leader 副本上 offload 到 follower 副本的负载均衡机制。TiKV 的 follower read 实现可以保证单行数据读取的线性一致性，配合 TiDB Snapshot Isolation 事务隔离级别可以为用户提供强一致的数据读取能力。为了获得强一致读取的能力，在当前的实现中 follower 节点需要额外付出 read index 开销。因此目前 follower read 的主要受益是隔离集群的读写请求以及提升整体读取吞吐，从单个请求的 latency 角度看会比传统的 leader 读取多付出一次 read index raft 交互开销。在后续的演进中 follower read 将会引入一系列的优化消除与 leader read 在 latency 上的差距。

## 使用方式

要开启 TiDB 的 follower read 功能，将 SESSION 变量 `tidb_replica_read` 的值设置为 `follower` 即可：

{{< copyable "sql" >}}

```sql
set @@tidb_replica_read = 'follower';
```

作用域：SESSION

默认值：leader

该变量用于设置当前会话期待的数据读取方式。

    - 当设定为默认值 `leader` 或者空字符串时，TiDB 会维持原有行为方式，将所有的读取操作都发送给 leader 副本处理。
    - 当设置为 `follower` 时，TiDB 会选择 region 的 follower 副本完成所有的数据读取操作。

### 适用场景

当系统中存在读取热点 region 导致 leader 资源紧张成为整个系统读取瓶颈时，启用 follower read 可明显降低 leader 的负担并且通过在多个 follower 之间均衡负载, 显著的提升整体系统的吞吐能力。

## Follower read 实现机制

在 follower read 功能出现前，TiDB 采用 strong leader 策略将所有的读写操作全部提交到 region 的 leader 节点上完成。虽然 TiKV 能够很均匀的将 region 分散到多个物理节点上，但是对于每一个 region 来说，只有 leader 副本能够对外提供服务，另外两个 follower 除了时刻同步数据准备着 failover 时投票切换成为 leader 外，没有办法对 TiDB 的请求提供任何帮助。为了允许在 TiKV 的 follower 节点进行数据读取，同时又不破坏线性一致性和 Snapshot Isolation 的事务隔离，region 的 follower 节点需要使用 Raft ReadIndex 协议确保当前读请求可以读到当前 leader 上已经 commit 的最新的数据。Follower read 在 TiDB 层面的变化很容易理解，我们只需要根据负载均衡策略将对某个 region 的读取请求发送到 follower 节点。

### Follower 强一致读

TiKV follower 节点处理读取请求时首先使用 Raft ReadIndex 协议同 region 当前的 leader 进行一次交互获取当前 raft group 最新的 commit index。在获取到当前 raft group 中最新的 commit index 后，等本地 apply 到前一步获取到的 leader 最新 commit index 后开始正常的读取请求处理流程。想了解详细的实现细节可参考相关 PR: 

   - [tikv/tikv#5051](https://github.com/tikv/tikv/pull/5051) 
   - [tikv/tikv#5118](https://github.com/tikv/tikv/pull/5118)
   - [kvproto/kvproto#424](https://github.com/pingcap/kvproto/pull/424)

### Follower 副本选择策略
由于 TiKV 的 follower read 可以保证线性一致性，不会破坏 TiDB 的 Snapshot Isolation 事务隔离级别，因此 TiDB 选择 follower 的策略可以采用 round robine 的方式。虽然 TiKV 有数据一致性的保证可以选择任意的 follower 处理任意读取请求，但考虑到多个 follower 间复制速度不同，如果负载均衡的粒度过细可能导致明显的 latency 波动。目前 follower read 负载均衡策略粒度是连接级别的，对于一个 TiDB 的客户端连接在某个具体的 region 上会固定使用同一个 follower，只有在选中的 follower 故障或者因调度策略发生调整的情况才会进行切换。
