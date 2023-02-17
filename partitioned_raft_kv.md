---
title: 分区raft kv
aliases: ['/docs-cn/dev/partitioned-raft-kv/']
---

# 分区raft kv

本文介绍 TiKV 的分区raft kv。

## 介绍
TiDB v6.6.0 之前，TiKV 基于 Raft 的存储引擎使用一个单一的 RocksDB 实例存储该 TiKV 实例所有 Region 的数据。
为了更平稳的支持更大的集群，从 TiDB v6.6.0 开始，我们引入了一个全新的 TiKV 存储引擎，该引擎使用多个 RocksDB 实例来存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单独的 RocksDB 实例中。新引擎能够更好的控制 RocksDB 实例的文件数和层级，并实现了 Region 间数据操作的物理隔离，避免互相影响，支持平稳管理更多的数据。可以理解为 TiKV 通过分区管理多个 RocksDB 实例，这也是该特性分区 Raft KV 名字的由来。该功能目前是实验特性，不推荐在生产环境中使用。
该功能的主要优势在于更好的写入性能，更快的扩缩容，相同硬件下可以支持更大的数据，也能支持更大的集群规模。

## 相关配置
### storage.engine
设置engine类型。该配置只能在创建新集群时指定，且后续无法更改。**实验特性**
* `raft-kv`: raft-kv是 TiDB v6.6.0 之前的默认存储引擎
* `partitioned-raft-kv`: partitioned-raft-kv是6.6新引入的Engine类型。

### rocksdb.write-buffer-limit
设置单个TiKV中所有RocksDB中使用的memtable的内存上限,默认值为本机内存的25%, 推荐不低于5GB。该选项只作用于`partitioned-raft-kv`.**实验特性**
* 默认值: 25%可用内存
* 单位: KB|MB|GB

### rocksdb.write-buffer-flush-oldest-first
设置当RocksDB当前memtable内存占用达到阈值之后的Flush策略。**实验特性**
* false，是默认值，表明Flush的策略是优先选择数据量大的memtable落盘到SST。
* true，表明Flush的策略是优先选择最老的memtable落盘到SST。该策略用于有明显冷热数据的场景，可以把冷数据的memtable清除。

## 该功能的使用场景
* 需要在单个TiKV支持更大的数据
* 有大量写入吞吐
* 频繁做扩缩容
* 读、写放大比较严重的负载
* TiKV内存尚有富余

## 该功能的限制
由于该功能处于实验特性，以下功能仍然在开发中，目前不支持。
* lightning导入, TiCDC, BR, dumping, Tikv-ctl等工具均不支持
* 不支持和TiFlash共同使用
* 一旦启用该功能后无法回退到6.5或者以前的版本。
