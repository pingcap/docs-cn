---
title: TiDB 大规模读取优化
summary: 了解 TiDB 优化大规模读取场景的技术细节。
aliases: ['/docs-cn/dev/distsql-read/','/docs-cn/dev/reference/distsql-read/']
---

# TiDB 大规模读取优化

针对大规模读取的场景，TiDB 进行了优化。TiDB 是一个使用全局索引的数据库，全局索引的性能优势在于索引键是连续的，仅读取索引时速度较快。此外，批处理和副本读取也是优化的关键。通过副本读取，可以避免远程读取的延迟和流量，提高读取性能。

## 索引

### 局部索引

分布式数据库有两种类型：局部索引和全局索引。局部索引类似于普通数据库，最终结果是多个节点的结果重叠在一起。如下图所示，此查询需要从三个节点中获取信息，才能得出完整的结果。

![local-index](/media/reference/distsql-read/local-index.png)

### 全局索引

全局索引的分布式数据库可能更为复杂，但效率可能更高。如下图所示，此查询和 `(r4, r5)` 无关的节点。当有许多这样的不相关节点时，全局索引的性能优势就会显现出来。

![global-index](/media/reference/distsql-read/global-index.png)

例子中查询加点线框的部分被称为 Table Lookup。全局索引的优势在于索引键是连续的，几乎在同一节点上，读取速度较快，因此这个表查找可能会降低性能，原因有三个：

- 表查找的 Key 通常不连续，这会导致引擎扫描速度变慢，在RocksDB中，Seek的成本高于Next。
- 图中的数据库节点在 TiDB 中的概念是 Region，如果涉及到的 Region 过多，编解码的开销会不可忽视。
- Table Lookup 的负载可能会严重倾斜，此时即使集群具有非常多的资源，Table Lookup 的性能也可能很差。

TiDB 针对第二个和第三个问题做了优化。

## 一致性的优点

一致性意味着读取的快照 index 和 row 是一对一的关系。在上面的例子中，`i100->r0->value0` 和 `i150->r2->value2` 是一对一的关系。由于这个优点，Table Lookup 的大小在发送请求之前就已知道了。当有许多小的 Table Lookup 请求时，可以增加执行并法度。

## 批处理

一种优化 Table Lookup 的方法是批处理。为了读取远程分片的数据，需要通过 RPC。但是，此 RPC 的编码和解码开销很大，会影响处理速度。

![non-batch](/media/reference/distsql-read/non-batch.png)

在图中，数据库分片具有副本，包括领导者副本分片和跟随者副本分片。绿色分片是 leader，黄色分片是 follower。除了 Table Lookup 之外的解释在图中省略。

![batch](/media/reference/distsql-read/batch.png)

在图中，批处理是 RPC 上下文的节约。以 `r1->value1` 和 `r3->value3` 为例，原本需要执行两个RPC 的查询，但现在可以使用一个 RPC 解决（其中 r5 的分片不是 leader，需要进行重试）。

TiDB 通过设置 `tidb_store_batch_size` 来控制 batch RPC 的大小。

## 副本读取

通常，要获取最新数据，查询必须在 leader 上执行。但是，由于某些查询的平衡不良，如果所有查询都在领导者上执行，则该领导者的资源利用率将增加，而其他节点的资源将无法使用。如果用户看到这种情况，他们会困惑：“虽然集群资源仍然存在，但为什么查询变慢？”使用副本读取功能，可以通过读取接近的副本数据来避免远程读取的延迟和流量。

TiDB 支持 follower read 特性，简单地说，TiDB 可以从副本节点读取最新数据，但是必须确认安全的读取范围（applied index）。

![load-based-replica-read](/media/reference/distsql-read/load-based-replica-read.png)

要使用副本读取，节点需要估计自己读取任务的排队时间（[ewma](https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average)时间），如果查询等待时间太长（`ewma > busy threshold`），节点会直接返回“busy”，然后客户端会重试。在重试时，将选择 ewma 最低的节点。

这种设计的巧妙之处在于，一个节点可以拥有多个领导者分片，并且这些领导者分片的跟随者分散在许多地方。例如，在10个节点的集群中，即使一个节点很忙，最佳情况下也可以从9个节点获得支持。

TiDB 通过设置 `tidb_load_based_replica_read_threshold` 来控制 batch RPC 的大小。
