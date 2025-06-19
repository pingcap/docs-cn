---
title: RocksDB 概述
summary: 了解 RocksDB 的基本概念和工作原理。
category: reference
---

# RocksDB 概述

[RocksDB](https://github.com/facebook/rocksdb) 是一个提供键值存储和读写功能的 LSM-tree 存储引擎。它由 Facebook 开发，基于 LevelDB。用户写入的键值对首先被插入到预写日志（Write Ahead Log，WAL）中，然后写入内存中的跳表（SkipList，一种称为 MemTable 的数据结构）。LSM-tree 引擎将随机修改（插入）转换为对 WAL 文件的顺序写入，因此它们提供比 B-tree 引擎更好的写入吞吐量。

一旦内存中的数据达到一定大小，RocksDB 就会将内容刷新到磁盘上的排序字符串表（Sorted String Table，SST）文件中。SST 文件组织在多个层级中（默认最多 6 层）。当某一层的总大小达到阈值时，RocksDB 会选择部分 SST 文件并将它们合并到下一层。每个后续层的大小是前一层的 10 倍，因此 90% 的数据存储在最后一层。

RocksDB 允许用户创建多个列族（Column Families，CFs）。CFs 有自己的 SkipList 和 SST 文件，并且它们共享同一个 WAL 文件。这样，不同的 CFs 可以根据应用特性有不同的设置。同时它不会增加对 WAL 的写入次数。

## TiKV 架构

TiKV 的架构如下图所示：

![TiKV RocksDB](/media/tikv-rocksdb.png)

作为 TiKV 的存储引擎，RocksDB 用于存储 Raft 日志和用户数据。TiKV 节点中的所有数据共享两个 RocksDB 实例。一个用于 Raft 日志（通常称为 raftdb），另一个用于用户数据和 MVCC 元数据（通常称为 kvdb）。kvdb 中有四个 CFs：raft、lock、default 和 write：

* raft CF：存储每个 Region 的元数据。它只占用很少的空间，用户不需要关心。
* lock CF：存储悲观事务的悲观锁和分布式事务的预写锁。事务提交后，lock CF 中的相应数据会被快速删除。因此，lock CF 中的数据大小通常很小（小于 1 GB）。如果 lock CF 中的数据大量增加，这意味着大量事务正在等待提交，系统可能遇到了 bug 或故障。
* write CF：存储用户的实际写入数据和 MVCC 元数据（数据所属事务的开始时间戳和提交时间戳）。当用户写入一行数据时，如果数据长度小于或等于 255 字节，则存储在 write CF 中。否则，存储在 default CF 中。在 TiDB 中，二级索引只占用 write CF 的空间，因为非唯一索引存储的值为空，而唯一索引存储的值是主键索引。
* default CF：存储长度超过 255 字节的数据。

## RocksDB 内存使用

为了提高读取性能并减少对磁盘的读取操作，RocksDB 根据一定大小（默认为 64 KB）将存储在磁盘上的文件分成块。读取块时，首先检查数据是否已存在于内存中的 BlockCache 中。如果是，则可以直接从内存中读取数据，而无需访问磁盘。

BlockCache 根据 LRU 算法丢弃最近最少使用的数据。默认情况下，TiKV 将系统内存的 45% 用于 BlockCache。用户也可以自行修改 `storage.block-cache.capacity` 配置为适当的值。但不建议超过系统总内存的 60%。

写入 RocksDB 的数据首先写入 MemTable。当 MemTable 的大小超过 128 MB 时，它会切换到一个新的 MemTable。TiKV 中有 2 个 RocksDB 实例，共 4 个 CFs。每个 CF 的单个 MemTable 大小限制为 128 MB。同时最多可以存在 5 个 MemTable，否则前台写入会被阻塞。这部分占用的内存最多为 2.5 GB（4 x 5 x 128 MB）。由于内存消耗较少，不建议更改此限制。

## RocksDB 空间使用

* 多版本：由于 RocksDB 是具有 LSM-tree 结构的键值存储引擎，MemTable 中的数据首先刷新到 L0。由于文件按生成顺序排列，L0 中的 SST 范围可能会重叠。因此，同一个键在 L0 中可能有多个版本。当文件从 L0 合并到 L1 时，它会被切割成特定大小的多个文件（默认为 8 MB）。同一层上每个文件的键范围不会相互重叠，因此在 L1 和后续层级中每个键只有一个版本。
* 空间放大：每一层文件的总大小是前一层的 x 倍（默认为 10），因此 90% 的数据存储在最后一层。这也意味着 RocksDB 的空间放大不超过 1.11（L0 数据较少，可以忽略）。
* TiKV 的空间放大：TiKV 有自己的 MVCC 策略。当用户写入一个键时，实际写入 RocksDB 的是 key + commit_ts，也就是说，更新和删除也会向 RocksDB 写入一个新键。TiKV 会定期删除旧版本的数据（通过 RocksDB 的 Delete 接口），因此可以认为用户在 TiKV 上存储的数据实际空间被放大到 1.11 加上最近 10 分钟写入的数据（假设 TiKV 及时清理旧数据）。

## RocksDB 后台线程和压缩

在 RocksDB 中，将 MemTable 转换为 SST 文件以及合并各层 SST 文件等操作都在后台线程池中执行。后台线程池的默认大小为 8。当机器的 CPU 数量小于或等于 8 时，后台线程池的默认大小为 CPU 数量减一。

通常情况下，用户不需要更改此配置。如果用户在一台机器上部署多个 TiKV 实例，或者机器的读取负载相对较高而写入负载较低，可以适当将 `rocksdb/max-background-jobs` 调整为 3 或 4。

## WriteStall

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节适用于 TiDB，不适用于 TiDB Cloud。

</CustomContent>

RocksDB 的 L0 与其他层不同。L0 的 SST 按生成顺序排列，SST 之间的键范围可能重叠。因此，执行查询时必须依次查询 L0 中的每个 SST。为了不影响查询性能，当 L0 中的文件过多时，会触发 WriteStall 来阻塞写入。

当遇到写入延迟突然大幅增加时，可以首先查看 Grafana RocksDB KV 面板上的 **WriteStall Reason** 指标。如果是由于 L0 文件过多导致的 WriteStall，可以将以下配置调整为 64。

```
rocksdb.defaultcf.level0-slowdown-writes-trigger
rocksdb.writecf.level0-slowdown-writes-trigger
rocksdb.lockcf.level0-slowdown-writes-trigger
rocksdb.defaultcf.level0-stop-writes-trigger
rocksdb.writecf.level0-stop-writes-trigger
rocksdb.lockcf.level0-stop-writes-trigger
```
