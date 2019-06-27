---
title: GC 机制简介
category: reference
---

# GC 机制简介

TiDB 的事务的实现采用了 MVCC（多版本并发控制）机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并以时间戳来区分版本。GC 的任务便是清理不再需要的旧数据。

## 整体流程

一个 TiDB 集群中会有一个 TiDB 实例被选举为 GC leader，GC 的运行由 GC leader 来控制。

GC 会被定期触发，默认情况下每 10 分钟一次。每次 GC 时，首先，TiDB 会计算一个称为 safe point 的时间戳，接下来 TiDB 会在保证 safe point 之后的快照全部拥有正确数据的前提下，删除更早的过期数据。具体而言，分为以下三个步骤:

1. Resolve Locks
2. Delete Ranges
3. Do GC

### Resolve Locks

TiDB 的事务是基于 [Google Percolator](https://ai.google/research/pubs/pub36726) 模型实现的，事务的提交是一个两阶段提交的过程。第一阶段完成时，所有涉及的 key 会加上一个锁，其中一个锁会被设定为 Primary，其余的锁（Secondary）则会指向 Primary；第二阶段会将 Primary 锁所在的 key 加上一个 Write 记录，并去除锁。这里的 Write 记录就是历史上对该 key 进行写入或删除，或者该 key 上发生事务回滚的记录。Primary 锁被替换为何种 Write 记录标志着该事务提交成功与否。接下来，所有 Secondary 锁也会被依次替换。如果替换这些 Secondary 锁的线程死掉了，锁就残留了下来。

Resolve Locks 这一步的任务即对 safe point 之前的锁进行回滚或提交，取决于其 Primary 是否被提交。如果一个 Primary 锁也残留了下来，那么该事务应当视为超时并进行回滚。这一步是必不可少的，因为如果其 Primary 的 Write 记录由于太老而被 GC 清除掉了，那么就再也无法知道该事务是否成功。如果该事务存在残留的 Secondary 锁，那么也无法知道它应当被回滚还是提交，也就无法保证一致性。

Resolve Locks 的执行方式是由 GC leader 对所有的 Region 发送请求进行处理。从 3.0 起，这个过程默认会并行地执行，并发数量默认与 TiKV 节点个数相同。

### Delete Ranges

在执行 `DROP TABLE/INDEX` 等操作时，会有大量连续的数据被删除。如果对每个 key 都进行删除操作、再对每个 key 进行 GC 的话，那么执行效率和空间回收速度都可能非常的低下。事实上，这种时候 TiDB 并不会对每个 key 进行删除操作，而是将这些待删除的区间及删除操w作的时间戳记录下来。Delete Ranges 会将这些时间戳在 safe point 之前的区间进行快速的物理删除。

### Do GC

这一步即删除所有 key 的过期版本。为了保证 safe point 之后的任何时间戳都具有一致的快照，这一步删除 safe point 之前提交的数据，但是会保留最后一次写入（除非最后一次写入是删除）。

从 3.0 起，GC leader 只需将 safe point 上传至 PD。每个 TiKV 节点都会各自从 PD 获取 safe point，当 TiKV 发现 safe point 发生更新时便会对 leader 在本机上的所有 Region 进行 GC。与此同时，GC leader 可以继续触发下一轮 GC。

通过修改配置可以采用 2.x 版本中所使用的旧的 GC 方式，即由 GC leader 向所有 Region 发送 GC 请求。
