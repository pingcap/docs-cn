---
title: Titan 配置
summary: Titan 配置介绍了如何开启、关闭 Titan、数据迁移原理、相关参数以及 Level Merge 功能。从 TiDB v7.6.0 开始，默认启用 Titan，支持宽表写入场景和 JSON。开启 Titan 方法包括使用 TiUP 部署集群、直接编辑 TiKV 配置文件、编辑 TiDB Operator 配置文件。数据迁移是逐步进行的，可以通过全量 Compaction 提高迁移速度。常用配置参数包括 `min-blob-size`、`blob-file-compression`、`blob-cache-size` 等。关闭 Titan 可通过设置 `blob-run-mode` 参数。Level Merge 是实验功能，可提升范围查询性能并降低 Titan GC 对前台写入性能的影响。
---

# Titan 配置

本文档介绍如何通过 [Titan](/storage-engine/titan-overview.md) 配置项来开启、关闭 Titan、数据迁移原理、相关参数以及 Level Merge 功能。

## 开启 Titan

> **注意：**
>
> - 从 TiDB v7.6.0 开始，新集群将默认启用 Titan，以更好地支持 TiDB 宽表写入场景和 JSON。阈值 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 的默认值也由之前的 `1KB` 调整为 `32KB`。
> - 如果集群在升级到 TiDB v7.6.0 或更高版本之前未启用 Titan，则升级后将保持原有配置，继续使用 RocksDB。
> - 如果集群在升级到 TiDB v7.6.0 或更高版本之前已经启用了 Titan，则升级后将维持原有配置，保持启用 Titan，并保留升级前 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 的配置。如果升级前没有显式配置该值，则升级后仍然保持老版本的默认值 `1KB`，以确保升级后集群配置的稳定性。

Titan 对 RocksDB 兼容，也就是说，使用 RocksDB 存储引擎的现有 TiKV 实例可以直接开启 Titan。

开启 Titan 的方法如下。

+ 方法一：如果使用 TiUP 部署的集群，开启的方法是执行 `tiup cluster edit-config ${cluster-name}` 命令，再编辑 TiKV 的配置文件。编辑 TiKV 配置文件示例如下：

    ```shell
    tikv:
      rocksdb.titan.enabled: true
    ```

    重新加载配置，同时也会在线滚动重启 TiKV：

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    具体命令，可参考[通过 TiUP 修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)。

+ 方法二：直接编辑 TiKV 配置文件开启 Titan（不建议在生产环境中使用）。

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

+ 方法三：编辑 TiDB Operator 的 `${cluster_name}/tidb-cluster.yaml` 配置文件，编辑示例如下：

    ```yaml
    spec:
      tikv:
        ## Base image of the component
        baseImage: pingcap/tikv
        ## tikv-server configuration
        ## Ref: https://docs.pingcap.com/zh/tidb/stable/tikv-configuration-file
        config: |
          log-level = "info"
          [rocksdb]
            [rocksdb.titan]
              enabled = true
    ```

    应用配置时，触发在线滚动重启 TiDB 集群让配置生效：

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    更多信息请参考[在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster)。

## 数据迁移

> **警告：**
>
> 在关闭 Titan 功能的情况下，RocksDB 无法读取已经迁移到 Titan 的数据。如果在打开过 Titan 的 TiKV 实例上错误地关闭了 Titan（误设置 `rocksdb.titan.enabled = false`），启动 TiKV 会失败，TiKV log 中出现 `You have disabled titan when its data directory is not empty` 的错误。如需要关闭 Titan，请参考[关闭 Titan](#关闭-titan) 。

开启 Titan 以后，原有的数据并不会马上迁移到 Titan 引擎，而是随着前台写入和 RocksDB Compaction 的进行，**逐步进行 key-value 分离并写入 Titan**。同样的，无论是通过 [BR](/br/backup-and-restore-overview.md) 快照或日志恢复的数据或扩缩容过程中产生的数据搬迁，还是通过 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 物理导入模式导入的数据，都会首先写入 RocksDB。然后，随着 RocksDB Compaction 的进行，超过 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 默认值 `32KB` 的大 value 会逐步分离到 Titan 中。你可以通过观察 **TiKV Details** > **Titan kv** > **blob file size** 监控面板中文件的大小来确认存储在 Titan 中的数据大小。

为了更快地将数据转移到 Titan，建议使用 tikv-ctl 工具执行一次全量 Compaction，以提高迁移速度。具体操作步骤请参考[手动 compact](/tikv-control.md#手动-compact-整个-tikv-集群的数据)。由于 RocksDB 具备 Block Cache，并且在将数据从 RocksDB 迁移到 Titan 时，数据访问是连续的，这使得在迁移过程中 Block Cache 能够更有效地提升迁移速度。在我们的测试中，通过 tikv-ctl 在单个 TiKV 节点上执行全量 Compaction，仅需 1 小时就能将 670 GiB 的数据迁移到 Titan。

需要注意的是，由于 Titan Blob 文件中的 Value 并非连续的，而且 Titan 的缓存是基于 Value 级别的，因此 Blob Cache 无法在 Compaction 过程中提供帮助。相较于从 RocksDB 转向 Titan 的速度，从 Titan 转回 RocksDB 的速度则会慢一个数量级。在测试中，通过 tikv-ctl 将 TiKV 节点上的 800 GiB Titan 数据进行全量 Compaction 转为 RocksDB，需要花费 12 个小时。

## 常用配置参数

通过合理配置 Titan 参数，可以有效提升数据库性能和资源利用率。本节介绍了一些常见的参数。

### `min-blob-size`

你可以通过设置 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) 来调整 value 的大小阈值，决定哪些数据保存在 RocksDB 中，哪些数据保存在 Titan 的 blob file 中。`32KB` 是个折中的值，它能确保 Titan 的性能相对 RocksDB 没有回退。但在很多场景中，该值并不是最佳值。建议参考 [`min-blob-size` 对性能的影响](/storage-engine/titan-overview.md#min-blob-size-对性能的影响)来选择合适的值。如果你想进一步提升写性能，并能接受扫描性能的下降，你可以将该值最低调整为 `1KB`。

### `blob-file-compression` 和 `zstd-dict-size`

可以使用 [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) 参数指定 Titan 中 value 所使用的压缩算法，也可以配置 [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) 启用 `zstd` 字典压缩来提高压缩率。

### `blob-cache-size`

可以使用 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) 控制 Titan 中 value 的缓存大小。更大的缓存能提高 Titan 读性能，但过大的缓存会造成 OOM。

建议在数据库稳定运行后，根据监控把 RocksDB block cache (`storage.block-cache.capacity`) 设置为 store size 减去 blob file size 的大小，`blob-cache-size` 设置为内存大小 * 50% 减去 block cache 的大小。这是为了保证 block cache 足够缓存整个 RocksDB 的前提下，blob cache 尽量大。

### `discardable-ratio` 和 `max-background-gc`

[`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 和 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) 的设置对于 Titan 的读性能和垃圾回收过程都有重要影响。

当一个 blob file 中无用数据（相应的 key 已经被更新或删除）比例超过 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 设置的阈值时，将会触发 Titan GC。减少这个阈值可以减少空间放大，但是会造成 Titan 更频繁 GC；增加这个值可以减少 Titan GC，减少相应的 I/O 带宽和 CPU 消耗，但是会增加磁盘空间占用。

若果你通过**TiKV Details** - **Thread CPU** - **RocksDB CPU** 监控中观察到 Titan GC 线程长期处于满负荷状态时，应该考虑调整 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) 增加 Titan GC 线程池大小。

### `rate-bytes-per-sec`

通过调整 [`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec)，你可以限制 RocksDB compaction 的 I/O 速率，从而在高流量时减少对前台读写性能的影响。

### `shared-blob-cache`（从 v8.0.0 版本开始引入）

你可以通过 [`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache从-v800-版本开始引入) 控制是否启用 Titan Blob 文件和 RocksDB Block 文件的共享缓存，默认值为 `true`。当开启共享缓存时，Block 文件具有更高的优先级，TiKV 将优先满足 Block 文件的缓存需求，然后将剩余的缓存用于 Blob 文件。

### Titan 配置文件示例

下面是一个 Titan 配置文件的样例，更多的参数说明，请参考 [TiKV 配置文件描述](/tikv-configuration-file.md)。你可以使用 TiUP [修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)，也可以通过[在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/configure-a-tidb-cluster)修改配置参数。

```toml
[rocksdb]
rate-bytes-per-sec = 0

[rocksdb.titan]
enabled = true
max-background-gc = 1

[rocksdb.defaultcf.titan]
min-blob-size = "32KB"
blob-file-compression = "zstd"
zstd-dict-size = "16KB"
discardable-ratio = 0.5
blob-run-mode = "normal"
level-merge = false
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
    > 在磁盘空间不足以同时保持 Titan 和 RocksDB 数据时，应该使用 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) 的默认值 `0.5`。一般来说，如果磁盘可用空间小于 50% 时，推荐使用默认值。因为当 `discardable-ratio = 1.0` 时，RocksDB 数据一方面在不断增加，同时 Titan 原有的 blob 文件回收需要该文件所有数据都迁移至 RocksDB 才会发生，这个过程会比较缓慢。如果磁盘空间足够大，设置 `discardable-ratio = 1.0` 可以减小 compaction 过程中 Blob 文件自身的 GC，从而节省带宽。

2. （可选）使用 `tikv-ctl` 执行全量数据整理 (Compaction)。这一步骤将消耗大量 I/O 和 CPU 资源。

    > **警告：**
    >
    > 如果在磁盘空间不足时执行以下命令，可能会导致整个集群无可用空间从而无法写入数据。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3. 等待数据整理结束，通过 **TiKV-Details**/**Titan - kv** 监控面板确认 **Blob file count** 指标降为 0。

4. 更新 TiKV 节点的配置，关闭 Titan。

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

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
