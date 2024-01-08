---
title: Titan 配置
aliases: ['/docs-cn/dev/storage-engine/titan-configuration/','/docs-cn/dev/reference/titan/configuration/','/docs-cn/dev/titan-configuration/']
---

# Titan 配置

本文档介绍如何通过 [Titan](/storage-engine/titan-overview.md) 配置项来开启、关闭 Titan、相关参数以及 Level Merge 功能。

## 开启 Titan

Titan 对 RocksDB 兼容，也就是说，使用 RocksDB 存储引擎的现有 TiKV 实例可以直接开启 Titan。

+ 方法一：如果使用 TiUP 部署的集群，开启的方法是执行 `tiup cluster edit-config ${cluster-name}` 命令，再编辑 TiKV 的配置文件。编辑 TiKV 配置文件示例如下：

    {{< copyable "shell-regular" >}}

    ```shell
      tikv:
        rocksdb.titan.enabled: true
    ```

    重新加载配置，同时也会在线滚动重启 TiKV：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    具体命令，可参考[通过 TiUP 修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)。

+ 方法二：直接编辑 TiKV 配置文件开启 Titan（生产环境不推荐）。

    {{< copyable "" >}}

    ``` toml
    [rocksdb.titan]
    enabled = true
    ```

开启 Titan 以后，原有的数据并不会马上移入 Titan 引擎，而是随着前台写入和 RocksDB compaction 的进行，逐步进行 key-value 分离并写入 Titan。同样，全量、增量恢复或者 TiDB Lightning 导入的 SST 都是 RocksDB 格式，数据不会直接导入 Titan。随着 Compaction 的进行，被处理过的 SST 中的大 value 会分离到 Titan 中。可以通过观察 **TiKV Details** - **Titan kv** - **blob file size** 监控面版确认数据保存在 Titan 中部分的大小。

如果需要加速数据移入 Titan，可以通过 tikv-ctl 执行一次全量 compaction，请参考[手动 compact](/tikv-control.md#手动-compact-整个-tikv-集群的数据)。由于 RocksDB 有 Block Cache，且转成 Titan 时的数据访问是连续的，因此 Block Cache 能有很好的命中率。在测试中，TiKV 节点上 670 GiB 的数据，通过 tikv-ctl 全量 compaction 转成 Titan，只需 1 小时。

> **注意：**
>
> 在 v7.6.0 开始，新建集群默认打开 Titan。已有集群升级到 v7.6.0 则会维持原有的配置，如果没有显式配置 Titan，则仍然会使用 RocksDB。

> **警告：**
>
> 在不开启 Titan 功能的情况下，RocksDB 无法读取已经迁移到 Titan 的数据。如果在打开过 Titan 的 TiKV 实例上错误地关闭了 Titan（误设置 `rocksdb.titan.enabled = false`），启动 TiKV 会失败，TiKV log 中出现 `You have disabled titan when its data directory is not empty` 错误。如需要关闭 Titan，参考[关闭 Titan](#关闭-titan) 一节。

## 相关参数介绍

使用 TiUP 调整参数，请参考[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)。

+ Titan GC 线程数。

    当从 **TiKV Details** - **Thread CPU** - **RocksDB CPU** 监控中观察到 Titan GC 线程长期处于满负荷状态时，应该考虑增加 Titan GC 线程池大小。

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    max-background-gc = 1
    ```

+ value 的大小阈值。

    当写入的 value 小于这个值时，value 会保存在 RocksDB 中，反之则保存在 Titan 的 blob file 中。根据 value 大小的分布，增大这个值可以使更多 value 保存在 RocksDB，读取这些小 value 的性能会稍好一些；减少这个值可以使更多 value 保存在 Titan 中，进一步减少 RocksDB compaction。经过[测试](/storage-engine/titan-overview.md#min-blob-size-的选择及其性能影响)，1 KB是一个比较折中的值。如果发现系统磁盘占用过大可以进一步调高这个值。

    ```toml
    [rocksdb.defaultcf.titan]
    min-blob-size = "1KB"
    ```

+ Titan 中 value 所使用的压缩算法。从 v7.6.0 开始，默认采用 `zstd` 压缩算法。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-file-compression = "zstd"
    ```

+ 默认情况下，`zstd-dict-size` 为 `0KB`，表示 Titan 中压缩的是单个 value 值，而 RocksDB 压缩以 Block（默认值为 `32KB`）为单位。因此当 value 平均小于 32KB 时，Titan 的压缩率低于 RocksDB。以 JSON 内容为例，Titan 的 store size 可能比 RocksDB 高 30% 至 50%。实际压缩率还取决于 value 内容是否适合压缩，以及不同 value 之间的相似性。你可以通过设置 `zstd-dict-size`（比如 `16KB` ）启用 zstd 字典压缩以大幅提高压缩率（实际 Store Size 可以低于 RocksDB）。但 zstd 字典压缩在有些负载下会有 10% 左右的性能损失。
  
    ```toml
    [rocksdb.defaultcf.titan]
    zstd-dict-size = "16KB"
    ``` 

+ Titan 中 value 的缓存大小。

    更大的缓存能提高 Titan 读性能，但过大的缓存会造成 OOM。建议在数据库稳定运行后，根据监控把 RocksDB block cache (`storage.block-cache.capacity`) 设置为 store size 减去 blob file size 的大小，`blob-cache-size` 设置为 `内存大小 * 50% 再减去 block cache 的大小`。这是为了保证 block cache 足够缓存整个 RocksDB 的前提下，blob cache 尽量大。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-cache-size = 0
    ```

+ 当一个 blob file 中无用数据（相应的 key 已经被更新或删除）比例超过以下阈值时，将会触发 Titan GC。

    ```toml
    discardable-ratio = 0.5
    ```

    将此文件有用的数据重写到另一个文件。这个值可以估算 Titan 的写放大和空间放大的上界（假设关闭压缩）。公式是：

    写放大上界 = 1 / discardable_ratio

    空间放大上界 = 1 / (1 - discardable_ratio)

    可以看到，减少这个阈值可以减少空间放大，但是会造成 Titan 更频繁 GC；增加这个值可以减少 Titan GC，减少相应的 I/O 带宽和 CPU 消耗，但是会增加磁盘空间占用。

+ 以下选项限制 RocksDB compaction 的 I/O 速率，以达到在流量高峰时，限制 RocksDB compaction 减少其 I/O 带宽和 CPU 消耗对前台读写性能的影响。

    当开启 Titan 时，该选项限制 RocksDB compaction 和 Titan GC 的 I/O 速率总和。当发现在流量高峰时 RocksDB compaction 和 Titan GC 的 I/O 和/或 CPU 消耗过大，可以根据磁盘 I/O 带宽和实际写入流量适当配置这个选项。

    ```toml
    [rocksdb]
    rate-bytes-per-sec = 0
    ```

## 关闭 Titan

通过设置 `rocksdb.defaultcf.titan.blob-run-mode` 参数可以关闭 Titan。`blob-run-mode` 可以设置为以下几个值之一：

- 当设置为 `normal` 时，Titan 处于正常读写的状态。
- 当设置为 `read-only` 时，新写入的 value 不论大小均会写入 RocksDB。
- 当设置为 `fallback` 时，新写入的 value 不论大小均会写入 RocksDB，并且当 RocksDB 进行 compaction 时，会自动把所碰到的存储在 Titan blob file 中的 value 移回 RocksDB。

如果现有数据和未来数据均不再需要 Titan，可执行以下步骤完全关闭 Titan。一般情况下，只需要执行以下步骤 1 和步骤 3、步骤 4 即可。步骤 2 虽然可以加快数据迁移速度，但会严重影响用户 SQL 的性能。事实上，即使跳过步骤 2，由于在 Compaction 过程中会将数据从 Titan 迁移到 RocksDB，会占用额外的 I/O 和 CPU 资源，因此仍然可以观察到一定的性能损失，在资源紧张的情况下吞吐可以下降 50% 以上。

1. 更新需要关闭 Titan 的 TiKV 节点的配置。你可以通过以下两种方式之一更新 TiKV 配置：

    - 执行 `tiup cluster edit-config`，编辑配置文件，再执行 `tiup cluster reload -R tikv`。
    - 手动修改 TiKV 配置文件，然后重启 TiKV。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-run-mode = "fallback"
    discardable-ratio = 1.0
    ```

    > **注意：**
    >
    > `discardable-ratio` 在磁盘空间不足以同时保持 Titan 和 RocksDB 数据时应该维持默认值。一般来说，如果磁盘可用空间小于 50% 时，推荐使用默认值。因为当 `discardable-ratio = 1.0` 时，RocksDB 数据一方面在不断增加，同时 Titan 原有的 blob 文件回收需要该文件所有数据都迁移至 RocksDB 才会发生，这个过程会比较缓慢。`discardable-ratio = 1.0` 带来的好处是减小 compaction 过程中 Blob 文件自身的 GC，节省了带宽。
 
2. [可选] 使用 `tikv-ctl` 执行全量数据整理 (Compaction)。这一步骤将消耗大量 I/O 和 CPU 资源。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3. 等待数据整理结束，通过 **TiKV-Details**/**Titan - kv** 监控面板确认 **Blob file count** 指标降为 0。

4. 更新 TiKV 节点的配置，关闭 Titan。

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

### Titan 转 RocksDB 速度

由于 Titan Blob 文件中的 Value 是不连续的，而且 Titan 的 Cache 是 Value 级别，因此 Blob Cache 无法帮助 compaction。从 Titan 转到 RocksDB 速度相比 RocksDB 转 Titan 会慢一个数量级。在测试中，TiKV 节点上 800 GiB 的  Titan 数据，通过 tikv-ctl 做全量 compaction 转成 RocksDB，需要 12 个小时。

## Level Merge（实验功能）

TiKV 4.0 中 Titan 提供新的算法提升范围查询性能并降低 Titan GC 对前台写入性能的影响。这个新的算法称为 [Level Merge](/storage-engine/titan-overview.md#level-merge)。Level Merge 可以通过以下选项开启：

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

开启 Level Merge 的好处如下：

- 大幅提升 Titan 的范围查询性能。
- 减少了 Titan GC 对前台写入性能的影响，提升写入性能。
- 减少 Titan 空间放大，减少磁盘空间占用（默认配置下的比较）。

相应地，Level Merge 的写放大会比 Titan 稍高，但依然低于原生的 RocksDB。
