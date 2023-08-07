---
title: Partitioned Raft KV
summary: 了解 TiKV 的 Partitioned Raft KV 特性。
---

# Partitioned Raft KV

> **警告：**
>
> Partitioned Raft KV 目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

v6.6.0 之前，基于 Raft 的存储引擎，TiKV 使用单个 RocksDB 实例存储该 TiKV 实例所有 Region 的数据。

为了更平稳地支持更大的集群，从 v6.6.0 开始，TiDB 引入了一个全新的 TiKV 存储引擎，该引擎使用多个 RocksDB 实例来存储 TiKV 的 Region 数据，每个 Region 的数据都独立存储在单个 RocksDB 实例中。

新的 TiKV 引擎能够更好地控制 RocksDB 实例的文件数和层级，并实现了 Region 间数据操作的物理隔离，避免相互影响。同时，该引擎支持平稳管理更多的数据。你可以理解为，TiKV 通过分区管理多个 RocksDB 实例，这也是该特性 Partitioned Raft KV 名字的由来。

## 使用场景

如果你的 TiKV 集群有以下特点，可以考虑使用该功能：

* 需要在单个 TiKV 实例支持更多的数据。
* 具有大量写入吞吐。
* 需要频繁地扩缩容。
* 负载有较为严重的读写放大。
* TiKV 内存尚有富余。

该功能的主要优势在于，提高写入性能，加快扩缩容速度，以及在相同硬件下支持更多数据和更大的集群。

## 使用方法

要启用 Partitioned Raft KV，需要在创建集群时将配置项 [`storage.engine`](/tikv-configuration-file.md#engine-从-v660-版本开始引入) 设为 `"partitioned-raft-kv"`。同时，在使用 Partitioned Raft KV 特性时，可以通过配置项 [`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-从-v660-版本开始引入) 和 [`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-从-v660-版本开始引入) 来控制 RocksDB 的内存使用。

## 使用限制

由于该功能为实验特性，目前有以下限制：

* 暂不支持基于 EBS 的快照备份
* 暂不支持 Online Unsafe Recovery 和 Titan
* 不支持 tikv-ctl 命令行管理工具中的以下子命令：
    * `unsafe-recover`
    * `raw-scan`
    * `remove-fail-stores`
    * `recreate-region`
    * `reset-to-version`
* 暂不兼容 TiFlash
* 初始化以后不支持开启或者关闭
