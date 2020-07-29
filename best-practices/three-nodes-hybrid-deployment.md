---
title: 三节点混合部署最佳实践
---

# 三节点混合部署的最佳实践

在对性能要求不是很高同时需要控制成本的场景下，将 TiDB，TiKV，PD 混合部署在三台机器上是一个可行的方案。
本文以 TPC-C 作为工作负载，提供一些在三节点混合部署场景下部署和参数调整的建议。

## 部署环境和测试方法

三台 16C 32G 的物理机，每节点混合部署 1 TiDB + 1 TiKV + 1 PD。

由于 PD 和 TiKV 都会存储信息到磁盘，磁盘的写入读取延迟会直接影响到 PD 和 TiKV 的服务延迟，为了防止 PD 和 TiKV 对磁盘资源的争抢导致相互影响，推荐 PD 和 TiKV 采用不同的磁盘。

使用 tiup bench tpcc 5000 warehouses，每次以 128 terminals 的并发测试 12 小时。主要观察集群性能的稳定性指标。

下图是默认参数配置下，12 小时内集群 QPS 的监控，可以看倒有比较明显的抖动。

![QPS with default config](/media/best-practices/three-nodes-default-config-qps.png)

调整参数后，稳定性得到了改善。

![QPS with modified config](/media/best-practices/three-nodes-final-config-qps.png)

## 参数调整

抖动的主要原因是，默认的线程池和后台任务资源分配针对的是资源比较充足的机器。在混合部署的场景下，因为可用资源需要被多个组件共享，所以需要通过配置参数进行限制。

本次测试最终采用的配置为

```
tikv:
    readpool.unified.max-thread-count: 6
    server.grpc-concurrency: 2
    storage.scheduler-worker-pool-size: 2
    gc.max-write-bytes-per-sec: 300K
    rocksdb.max-background-jobs: 3
    rocksdb.max-sub-compactions: 1
    rocksdb.rate-bytes-per-sec: “200M”

  tidb:
    performance.committer-concurrency: 4
    performance.max-procs: 8
```

接下来会分别介绍这几个参数的意义和调整方法。

### TiKV 线程池大小配置

这部分会调整一些与前台业务有关的线程池的资源配比。
缩减这些线程池会损失一些性能，但在混合部署场景下可用资源有限，本身也难以达到很高的性能，所以选择牺牲一小部分性能去换取整体的稳定性。

这些配置项的修改，可以以默认配置为基础运行一次实际负载的测试，观察各线程池的实际使用量，缩减利用率不高的线程池大小。

#### `readpool.unified.max-thread-count`

该参数默认取值为机器线程数的 80%，因为是混合部署场景，我们需要手动计算并指定该值。
可以先设置成期望 TiKV 使用的 CPU 线程数的 80%。

#### `server.grpc-concurrency`

该参数默认为 4，因为现在的部署方案 CPU 有限，实际请求数也不会很高。
可以把这个这个值调低，后续观察监控面板保持其使用率在 80% 以下即可。

本次测试最后选择设置为 2，通过 gRPC pool CPU 面板观察，利用率正好在 80% 左右。

![gRPC Pool CPU](/media/best-practices/three-nodes-grpc-pool-usage.png)

#### `storage.scheduler-worker-pool-size`

该参数在 TiKV 检测到机器 CPU 数大于等于 16 时默认为 8，小于 16 时默认为 4。
它主要用于将复杂的事务请求转化为简单的 key-value 读写。但是 scheduler 线程池本身不进行任何写操作。

一般来说该线程池的利用率保持在 50%-75% 之间是比较好的，和 gRPC 线程池情况类似，混合部署时默认参数取值偏大，资源利用不充分。
本次测试最后选择设置为 2，通过 Scheduler worker CPU 面板观察，利用率比较符合最佳实践。

![Scheduler Worker CPU](/media/best-practices/three-nodes-scheduler-pool-usage.png)

### TiKV 后台任务资源配置

除前台任务之外，TiKV 还会持续的有后台任务进行数据的整理和过期数据的清除。
默认配置为这些后台任务分配了比较多的资源以应对大流量的写入。
混合部署场景下，默认配置就不是很合适了，需要通过部分参数对其资源使用量进行限制。

#### `rocksdb.max-background-jobs` 和 `rocksdb.max-sub-compactions`

RocksDB 线程池是进行 Compact 和 Flush 任务的线程池，默认大小为 8。这明显超出了我们实际可以使用的资源，需要限制。
`rocksdb.max-sub-compactions` 是单个 compaction 任务的子任务并发数，默认值为 3，在写入流量不大的情况下可以进行限制。

这次测试最终将 `rocksdb.max-background-jobs` 设置为 3，将 `rocksdb.max-sub-compactions` 设置为 1。
在 12 小时的 TPC-C 负载下没有发生 write stall，根据实际负载进行这两项参数的优化时，可以逐步调低这两个配置，并通过监控观察

* 如果遇到了 Write Stall，可以先调大 `rocksdb.max-background-jobs` 的取值
* 如果还是存在问题可将 `rocksdb.max-sub-compactions` 设置为 2 或者 3

#### `rocksdb.rate-bytes-per-sec`

这一参数用于限制后台 compaction 任务的磁盘流量，默认配置下没有进行任何限制。
为了避免 compaction 挤占前台服务资源，可以根据硬盘的顺序读写速度进行调整，为正常的服务保留足够多的磁盘带宽。
类似 compaction 线程池的调整方法，调整后也是根据是否 Write Stall 来判断取值是否合理。

#### `gc.max_write_bytes_per_sec`

因为 TiDB 是 MVCC 的模型，TiKV 还需要周期性的在后台清除旧版本的数据。当可用资源有限的时候，这个操作会引起周期性的性能抖动。`gc.max_write_bytes_per_sec` 可以用来这一操作的资源限制。

![GC Impact](/media/best-practices/three-nodes-gc-impact.png)

除了在配置文件中设置该参数之外，还可以通过 tikv-ctl 动态调节，可以为调整该参数提供便利

```
tiup ctl tikv --host=${ip:port} modify-tikv-config -n gc.max_write_bytes_per_sec -v ${limit}
```

> **注意：**
>
> 对于更新频繁的业务场景，限制 GC 流量可能会导致 MVCC 版本堆积，进而影响读取性能。
所以这个参数的取值需要进行多次尝试，在性能抖动和性能衰退之间找一个可以比较平衡的取值。
TiKV 后续也会提供新的优化方案改进这一问题。

### TiDB 参数调整

TiDB 执行算子的优化参数一般是通过系统变量进行调整，例如 tidb_hash_join_concurrency, tidb_index_lookup_join_concurrency 等。

这次测试中没有对这块参数进行调整，如果实际的业务负载测试中出现因为执行算子消耗过多 CPU 资源的情况，可以针对业务场景对特定的算子资源进行限制。
这部分内容可以参考 [TiDB 系统变量文档](/tidb-specific-system-variables.md)

#### `performance.max-procs`

这个参数控制着整个 Go 进程能使用的 CPU 核心数量，默认情况下为当前机器或者 cgroups 的 CPU 数量。

Go 运行时会定期使用一定比例的线程进行 GC 等后台工作，在混部模式下如果不对这一参数进行限制，GC 等后台操作就会使用过多 CPU。
