---
title: Titan 配置
category: reference
---

# Titan 配置

Titan 是基于 RocksDB 开发的存储引擎插件，通过把 key 和 value 分离存储，以在 value 较大的场景下，降低 RocksDB 后台 compaction 对 IO 带宽和 CPU 的占用，同时提高 SSD 寿命。

## 适用场景

Titan 适合在以下场景中使用：

- 前台写入量较大，RocksDB 大量触发 compaction 消耗大量 IO 带宽或者 CPU 资源，造成 TiKV 前台读写性能较差。
- 前台写入量较大，由于 IO 带宽瓶颈或 CPU 瓶颈的限制，RocksDB compaction 进度落后较多频繁造成 write stall。
- 前台写入量较大，RocksDB 大量触发 compaction 造成 IO 写入量较大，影响 SSD 盘的寿命。

开启 Titan 需要考虑以下前提条件：

- Value 较大。即 value 平均大小比较大，或者数据中大 value 的数据总大小占比比较大。目前 Titan 默认 1kb 以上大小的 value 是大 value，根据实际情况 512b 以上大小的 value 也可以看作是大 value。
- 没有范围查询或者对范围查询性能不敏感。Titan 存储数据的顺序性较差，所以相比 RocksDB 范围查询的性能较差，尤其是大范围查询。在测试中 Titan 范围查询性能相比 RocksDB 下降 40% 到数倍不等。
- 磁盘剩余空间足够。Titan 降低写放大是通过牺牲空间放大达到的。另外由于 Titan 逐个压缩 value，压缩率比 RocksDB（逐个压缩 block）要差。这两个因素一起造成 Titan 占用磁盘空间比 RocksDB 要多，这是正常现象。根据实际情况和不同的配置，Titan 磁盘空间占用可能会比 RocksDB 多一倍。

## 开启 Titan

### 直接开启 Titan

Titan 对 RocksDB 兼容，也就是说，现有使用 RocksDB 存储引擎的 TiKV 实例可以直接开启 Titan。开启的方法是修改 TiKV 配置并重启 TiKV：

{{< copyable "" >}}

``` toml
[rocksdb.titan]
enabled = true
```

开启 Titan 以后，原有的数据并不会马上移入 Titan 引擎，而是随着前台写入和 RocksDB compaction 的进行，逐步进行 key-value 分离并写入 Titan。可以通过观察 **TiKV Details** - **Titan kv** - **blob file size** 监控面版确认数据保存在 Titan 中部分的大小。

如果需要加速数据移入 Titan，可以通过 tikv-ctl 执行一次全量 compaction。请参看 tikv-ctl 文档。

注意 RocksDB 无法读取 Titan 的数据，但用 RocksDB 打开 Titan 数据也不会造成数据损坏。如果在打开过 Titan 的 TiKV 实例上错误地关闭了 Titan （误设置 rocksdb.titan.enabled = false），启动 TiKV 会失败，TiKV log 中出现 “You have disabled titan when its data directory is not empty” 错误。请参看“关闭 Titan”一节。

### 滚动开启 Titan（实验性）

也可以在集群中一个或多个 TiKV 节点中打开 Titan 作为实验，待调整稳定以后再在整个集群开启 Titan。由于 Titan 写入性能和存储方式跟 RocksDB 存在差异，滚动开启 Titan 的过程中可能造成 leader 分布不均匀，可以通过 PD 监控查看是否开启 Titan 的实例 leader count 较高，如果写负载有明显不均可以通过 pd-ctl store weight 降低 Titan 实例的 leader weight 以使 leader count 均衡。

## 参数调整

```toml
[rocksdb.titan]
max-background-gc = 1
```

Titan GC 线程数。当从 **TiKV Details** - **Thread CPU** - **RocksDB CPU** 监控中观察到 Titan GC 线程长期处于满负荷状态时，应该考虑增加 Titan GC 线程池大小。

```toml
[rocksdb.defaultcf.titan]
min-blob-size = "1KB"
```

大 value 的大小阈值。当写入的 value 小于这个值时，value 会保存在 RocksDB 中，反之则保存在 Titan 的 blob file 中。根据 value 大小的分布，增大这个值可以使更多 value 保存在 RocksDB，读取这些小 value 的性能会稍好一些；减少这个值可以使更多 value 保存在 Titan 中，进一步减少 RocksDB compaction。

```toml
[rocksdb.defaultcf.titan]
blob-file-compression = "lz4"
```

Titan 中 value 所使用的压缩算法。Titan 中压缩是以 value 为单元的。

```toml
[rocksdb.defaultcf.titan]
blob-cache-size = 0
```

Titan 中 value 的缓存大小。更大的缓存能提高 Titan 读性能，但过大的缓存会造成 OOM。建议在数据库稳定运行后，根据监控把 RocksDB block cache (storage.block-cache.capacity) 设置为 store size 减去 blob file size 的大小，`blob-cache-size` 设置为`内存大小 * 50% 再减去 block cache 的大小`。这是为了保证 block cache 足够缓存整个 RocksDB 的前提下，blob cache 尽量大。

```toml
discardable-ratio = 0.5
```

当一个 blob file 中无用数据（相应的 key 已经被更新或删除）比例超过这一阈值时，将会触发 Titan GC ，将此文件有用的数据重写到另一个文件。这个值可以估算 Titan 的写放大和空间放大的上界（假设关闭压缩）。公式是：
写放大上界 = 1 / discardable_ratio
空间放大上界 = 1 / ( 1 - discarable_ratio )
可以看到，减少这个阈值可以减少空间放大，但是会造成 Titan 更频繁 GC；增加这个值可以减少 Titan GC，减少相应的 IO 带宽和 CPU 消耗，但是会增加磁盘空间占用。

```toml
[rocksdb]
rate-bytes-per-sec = 0
```

该选项并不是 Titan 独有的设置。该选项限制 RocksDB compaction 的 IO 速率，以达到在流量高峰时，限制 RocksDB compaction 减少其 IO 带宽和 CPU 消耗对前台读写性能的影响。当开启 Titan 时，该选项限制 RocksDB compaction 和 Titan GC 的 IO 速率总和。当发现在流量高峰时 RocksDB compaction 和 Titan GC 的 IO 和/或 CPU 消耗过大，可以根据磁盘 IO 带宽和实际写入流量适当配置这个选项。

## 关闭 Titan（实验性）

通过设置 rocksdb.defaultcf.titan.blob-run-mode 可以关闭 Titan。blob-run-mode 可以设置为以下几个值之一：

- 当设置为 “kNormal” 时，Titan 处于正常读写的状态。
- 当设置为 “kReadnly” 时，新写入的 value 不论大小均会写入 RocksDB。
- 当设置为 “kFallback” 时，新写入的 value 不论大小均会写入 RocksDB，并且当 RocksDB 进行 compaction 时，会自动把所碰到的存储在 Titan blob file 中的 value 移回 RocksDB。

当需要关闭 Titan 时，可以设置 blob-run-mode = “kFallback”，并通过 tikv-ctl 执行全量 compaction。此后通过监控确认 blob file size 降到 0 以后，可以更改 rocksdb.titan.enabled = false 并重启 TiKV。

关闭 Titan 是实验性功能，非必要不建议使用。

## Level Merge：提升范围查询性能（实验性）

TiKV 4.0 中 Titan 提供新的算法提升范围查询性能并降低 Titan GC 对前台写入性能的影响。这个新的算法称为 level merge。Level merge 可以通过以下选项开启：

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

开启 level merge 的好处包括：

- 大幅提升 Titan 的范围查询性能。
- 减少了 Titan GC 对前台写入性能的影响，提升写入性能。
- 减少 Titan 空间放大，减少磁盘空间占用（默认配置下的比较）。

相应地，level mege 写放大会比 Titan 稍高，但依然低于原生的 RocksDB。
