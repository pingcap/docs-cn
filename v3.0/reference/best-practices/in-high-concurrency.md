---
title: TiDB 高并发写入场景最佳实践
category: reference
---

# TiDB 高并发写入场景最佳实践

在 TiDB 的使用过程中，一个典型场景是高并发批量写入数据到 TiDB。本文阐述了该场景中的常见问题，旨在给出一个业务的最佳实践，帮助读者在开发业务时避免陷入 TiDB 使用的 “反模式”。

## 目标读者

本文读者应该对 TiDB 有一定的了解，推荐先阅读 TiDB 原理的三篇文章（[讲存储](https://pingcap.com/blog-cn/tidb-internal-1/)，[说计算](https://pingcap.com/blog-cn/tidb-internal-2/)，[谈调度](https://pingcap.com/blog-cn/tidb-internal-3/)），以及 [TiDB Best Practice](https://pingcap.com/blog-cn/tidb-best-practice/)。

## 高并发批量插入场景

高并发批量插入的场景，通常产生在业务系统中的批量任务中，例如清算以及结算等业务。场景存在以下特点：

- 数据量大
- 需要短时间内将历史数据入库
- 需要短时间内读取大量数据

这就对 TiDB 提出了以下挑战：

- 写入/读取能力是否可以线性水平扩展
- 随着数据持续大并发写入，数据库性能是否稳定不衰减

对于分布式数据库来说，除了本身的基础性能外，最重要的就是充分利用所有节点能力，避免让单个节点成为瓶颈。

## TiDB 数据分布原理

如果要解决以上挑战，需要从 TiDB 数据切分以及调度的原理开始讲起。这里只是作简单的说明，详情可参阅[谈调度](https://pingcap.com/blog-cn/tidb-internal-3/)。

TiDB 以 Region 为单位对数据进行切分，每个 Region 有大小限制（默认 96M）。Region 的切分方式是范围切分。每个 Region 会有多副本，每一组副本，称为一个 Raft Group。每个 Raft Group 中由 Leader 负责执行这块数据的读 & 写（TiDB 即将支持 [Follower-Read](https://zhuanlan.zhihu.com/p/78164196)）。Leader 会自动地被 PD 组件均匀调度在不同的物理节点上，用以均分读写压力。

![TiDB 数据概览](/media/high-concurrency-best-practice/tidb-data-overview.png)

只要业务的写入没有 AUTO_INCREMENT 的主键，或没有单调递增的索引（即没有业务上的写入热点，更多细节可参阅 [TiDB 正确使用方式](https://zhuanlan.zhihu.com/p/25574778)），从原理上来说，TiDB 依靠这个架构可具备线性扩展的读写能力，并且可以充分利用分布式资源。从这一点看，TiDB 尤其适合高并发批量写入场景的业务。

但理论场景和实际情况往往存在不同。以下实例说明了热点是如何产生的。

## 热点产生的实例

以下为一张示例表：

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

这个表的结构非常简单，除了 `id` 为主键以外，没有额外的二级索引。将数据写入该表的语句如下，`id` 通过随机数离散生成：

{{< copyable "sql" >}}

```sql
INSERT INTO TEST_HOTSPOT(id, age, user_name, email) values(%v, %v, '%v', '%v');
```

负载是短时间内密集地执行以上写入语句。

以上操作看似符合理论场景中的 TiDB 最佳实践，业务上没有热点产生。只要有足够的机器，就可以充分利用 TiDB 的分布式能力。要验证是否真的符合最佳实践，可以在实验环境中进行测试。

部署拓扑 2 个 TiDB 节点，3 个 PD 节点，6 个 TiKV 节点。请忽略 QPS，因为测试只是为了阐述原理，并非 benchmark。

![QPS1](/media/high-concurrency-best-practice/QPS1.png)

客户端在短时间内发起了 “密集” 的写入，TiDB 收到的请求是 3K QPS。理论上，压力应该均摊给 6 个 TiKV 节点。但是从 TiKV 节点的 CPU 使用情况上看，存在明显的写入倾斜（tikv - 3 节点是写入热点）：

![QPS2](/media/high-concurrency-best-practice/QPS2.png)

![QPS3](/media/high-concurrency-best-practice/QPS3.png)

[Raft store CPU](/v3.0/reference/key-monitoring-metrics/tikv-dashboard.md) 为 `raftstore` 线程的 CPU 使用率，通常代表写入的负载。在这个场景下 tikv-3 为 Raft Leader，tikv-0 和 tikv-1 是 Raft 的 Follower，其他的 TiKV 节点的负载几乎为空。

从 PD 的监控中也可以证明热点的产生：

![QPS4](/media/high-concurrency-best-practice/QPS4.png)

## 热点问题产生的原因

以上测试并未达到理论场景中最佳实践，因为刚创建表的时候，这个表在 TiKV 中只会对应为一个 Region，范围是：

```
[CommonPrefix + TableID, CommonPrefix + TableID + 1)
```

短时间内大量数据会持续写入到同一个 Region上。

![TiKV Region 分裂流程](/media/high-concurrency-best-practice/tikv-Region-split.png)

上图简单描述了这个过程，随着数据持续写入，TiKV 会将一个 Region 切分为多个。但因为首先发起选举的是原 Leader 所在的 Store，所以新切分好的两个 Region 的 Leader 很可能还会在原 Store 上。新切分好的 Region 2，3 上，也会重复之前发生在 Region 1 上的过程。也就是压力会密集地集中在 TiKV-Node 1 上。

在持续写入的过程中，PD 发现 Node 1 中产生了热点，会将 Leader 均分到其他的 Node 上。如果 TiKV 的节点数多于副本数的话，TiKV 会尽可能将 Region 迁移到空闲的节点上。这两个操作在数据插入的过程中，也能在 PD 监控中得到印证：

![QPS5](/media/high-concurrency-best-practice/QPS5.png)

在持续写入一段时间后，整个集群会被 PD 自动地调度成一个压力均匀的状态，到那个时候整个集群的能力才会真正被利用起来。在大多数情况下，以上热点产生的过程是没有问题的，这个阶段属于表 Region 的预热阶段。

但是对于高并发批量密集写入场景来说，应该避免这个阶段。

## 热点问题的规避方法

为了达到场景理论中的最佳性能，一种方法是跳过这个预热阶段，直接将 Region 切分为预期的数量，提前调度到集群的各个节点中。

TiDB 在 v3.0.x 以及 v2.1.13 后支持一个叫 [Split Region](/v3.0/reference/sql/statements/split-region.md) 的新特性。这个特性提供了新的语法：

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

但是 TiDB 并不自动提前完成这个切分操作。原因如下：

![Table Region Range](/media/high-concurrency-best-practice/table-Region-range.png)

从图 3 可知，Table 行数据 key 的编码中，行数据唯一可变的是行 ID (rowID)。在 TiDB 中，rowID 是一个 Int64 整形。但是用户不一定能将 Int64 整形范围均匀切分成需要的份数，然后均匀分布在不同的节点上，还需要结合实际情况。

如果行 ID 的写入是完全离散的，那么上述方式是可行的。如果行 ID 或者索引有固定的范围或者前缀（例如，只在 `[2000w, 5000w)` 的范围内离散插入数据），这种写入依然在业务上不产生热点，但是如果按上面的方式进行切分，那么有可能一开始数据仍只写入到某个 Region 上。

作为一款通用数据库，TiDB 并不对数据的分布作假设，所以开始只用一个 Region 来对应一个表。等到真实数据插入进来以后，TiDB 自动根据数据的分布来作切分。这种方式是较通用的。

所以 TiDB 提供了 Split Region 语法，专门针对短时批量写入场景作优化。基于以上案例，下面尝试用 Split Region 语法提前切散 Region，再观察负载情况。

由于测试的写入数据在正数范围内完全离散，所以用以下语句，在 Int64 空间内提前将表切分为 128 个 Region：

{{< copyable "sql" >}}

```
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

切分完成以后，可以通过 `SHOW TABLE test_hotspot REGIONS;` 语句查看打散的情况。如果 `SCATTERING` 列值全部为 `0`，代表调度成功。

也可以通过 [table-regions.py](https://github.com/pingcap/tidb-ansible/blob/dabf60baba5e740a4bee9faf95e77563d8084be1/scripts/table-regions.py) 脚本，查看 Region 的分布。目前分布已经比较均匀了：

```
[root@172.16.4.4 scripts]# python table-regions.py --host 172.16.4.3 --port 31453 test test_hotspot
[RECORD - test.test_hotspot] - Leaders Distribution:
  total leader count: 127
  store: 1, num_leaders: 21, percentage: 16.54%
  store: 4, num_leaders: 20, percentage: 15.75%
  store: 6, num_leaders: 21, percentage: 16.54%
  store: 46, num_leaders: 21, percentage: 16.54%
  store: 82, num_leaders: 23, percentage: 18.11%
  store: 62, num_leaders: 21, percentage: 16.54%
```

再重新运行写入负载：

![QPS6](/media/high-concurrency-best-practice/QPS6.png)

![QPS7](/media/high-concurrency-best-practice/QPS7.png)

![QPS8](/media/high-concurrency-best-practice/QPS8.png)

可以看到已经消除了明显的热点问题了。

本示例仅为一个简单的表，还有索引热点的问题需要考虑。读者可参阅 [Split Region](/v3.0/reference/sql/statements/split-region.md) 文档来了解如何预先切散索引相关的 Region。

### 更复杂的热点问题

如果表没有主键或者主键不是 Int 类型，而且用户也不想自己生成一个随机分布的主键 ID 的话，TiDB 内部有一个隐式的 `_tidb_rowid` 列作为行 ID。在不使用 `SHARD_ROW_ID_BITS` 的情况下，`_tidb_rowid` 列的值基本也为单调递增，此时也会有写热点存在。（参阅 [`SHARD_ROW_ID_BITS` 的详细说明](/v3.0/reference/configuration/tidb-server/tidb-specific-variables.md#shard_row_id_bits)）

要避免由 `_tidb_rowid` 带来的写入热点问题，可以在建表时，使用 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 这两个建表选项（参阅 [`PRE_SPLIT_REGIONS` 的详细说明](/v3.0/reference/sql/statements/split-region.md#pre_split_regions)）。

`SHARD_ROW_ID_BITS` 用于将 `_tidb_rowid` 列生成的行 ID 随机打散。`pre_split_regions` 用于在建完表后预先进行 Split region。

> **注意：**
>
> `pre_split_regions` 必须小于或等于 `shard_row_id_bits`。

示例：

{{< copyable "sql" >}}

```sql
create table t (a int, b int) shard_row_id_bits = 4 pre_split_regions=·3;
```

- `SHARD_ROW_ID_BITS = 4` 表示 tidb_rowid 的值会随机分布成 16 （16=2^4） 个范围区间。
- `pre_split_regions=3` 表示建完表后提前切分出 8 (2^3) 个 Region。

开始写数据进表 t 后，数据会被写入提前切分好的 8 个 Region 中，这样也避免了刚开始建表完后因为只有一个 Region 而存在的写热点问题。

## 参数配置

### 关闭 TiDB 的 Latch 机制

TiDB 2.1 版本中在 SQL 层引入了 [latch 机制](/v3.0/reference/configuration/tidb-server/configuration-file.md#txn-local-latches)，用于在写入冲突比较频繁的场景中提前发现事务冲突，减少 TiDB 和 TiKV 事务提交时写写冲突导致的重试。在多数情况下，跑批场景全部使用存量数据，所以并不存在事务的写入冲突。可以把 TiDB 的 latch 功能关闭，以减少细小内存对象的分配：

```
[txn-local-latches]
enabled = false
```
