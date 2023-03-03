---
title: TiFlash 存算分离架构与 S3 支持
summary: 了解 TiFlash 存算分离架构与 S3 支持。
---

# TiFlash 存算分离架构与 S3 支持

> ** 警告: **
>
> TiFlash 存算分离架构目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tiflash/issues) 反馈。

TiFlash 默认使用存算一体的架构进行部署，即 TiFlash 节点既是存储节点，也是计算节点。从 TiDB v7.0.0 开始，TiFlash 支持存算分离架构，并且将数据存储在 AWS S3，或者兼容 S3 API 的对象存储中（比如 MinIO）。

## 架构介绍

![TiFlash Write and Compute Separation Architect](/media/tiflash/tiflash-s3.png)

如图，在存算分离架构中，TiFlash 原有进程的不同部分的功能，被拆分到两种不同的节点中，分别是 Write Node 和 Compute Node。这两种节点可以分别部署，各自扩展，即你可以选择部署任意数量的 Write Node 或者 Compute Node。

- TiFlash Write Node 

  负责接收 TiKV 的 Raft logs 数据，将数据转换成列存格式，并每隔一小段时间将这段时间的所有数据更新打包上传到 S3 中。此外，Write Node 也负责管理 S3 上的数据，比如不断整理数据使之有更好的查询性能，以及删除无用的数据等。

  Write Node 利用本地磁盘（通常是 NVMe SSD）来缓存最新写入的数据，从而避免内存使用过多。

  Write Node 比原来存算一体的 TiFlash 节点有更快的扩容和缩容速度，即增加或者删除 Write Node 后，数据能更快地在 Write Node 之间达到平衡。原理是 Write Node 把所有数据存储到了 S3，运行时只需要在本地存储很少的数据。扩容和缩容本质上是 Region Peer 在节点间的迁移。当某个 Write Node 要将某个 Region Peer 移动到自己之上管理时，它只需要从 Region Peer 所在的 Write Node 上传到 S3 的最新文件中下载少量关于此 Region 的元数据，再从 TiKV 同步最近的 Region 更新，就可以追上 Region Leader 的进度，从而完成 Region Peer 的迁移。

- TiFlash Compute Node 

  负责执行从 TiDB 节点发过来的查询请求。它首先访问 Write Node 以获取数据的快照 (data snapshots)，然后分别从 Write Node 读取最新的数据（即尚未上传到 S3 的数据），从 S3 读取剩下的大部分数据。

  Compute Node 利用本地磁盘（通常是 NVMe SSD）来作为数据文件的缓存，从而避免相同的数据反复从远端（Write Node 或者 S3）读取，以提高查询性能。

  Compute Node 是无状态节点，它拥有秒级的扩容和缩容速度。你可以利用这个特性降低成本：
  
  - 在查询负载较低时，减少 Compute Node 的数量，从而节省成本。在没有查询时，甚至可以停掉所有 Compute Node。
  - 在查询负载变高时，快速增加 Compute Node 的数量，保证查询性能。

## 使用场景

TiFlash 存算分离架构适合于希望获得更高性价比的数据分析服务的场景。在这个架构下，存储和计算资源可以单独按需扩展。在这些场景将会有比较大收益：

- 数据量虽然很大，但是只有少量数据被频繁查询；其他大部分数据属于冷数据，很少被查询。此时经常被查询的数据通常已被缓存在 Compute Node 的本地 SSD 上，可以提供较快查询性能；而其他大部分冷数据则存储在成本较低的 S3 或者其他对象存储上，从而节省存储成本。

- 计算资源需求有明显的波峰和波谷。比如重型的对账查询通常放在晚上执行，此时对计算资源要求较高，可以考虑临时扩展 Compute Node；其他时间可以用较少的 Compute Node 完成查询任务。

## 使用方式

默认情况下，TiUP 会将 TiFlash 部署为存算一体架构。如需将 TiFlash 部署为存算分离架构，请参考以下步骤手动进行配置：

1. 确保 TiDB 集群中没有任何 TiFlash 节点。如果有，则需要将所有表的 TiFlash 副本数设置为 0，然后缩容掉所有 TiFlash 节点。比如：

```shell
mysql> select * from information_schema.tiflash_replica; # Show all tables with TiFlash replica
mysql> alter table table_x set tiflash replica 0;        # Remove TiFlash replicas from all tables

tiup cluster scale-in mycuster -N tiflash # Scale in all TiFlash nodes
tiup cluster display mycluster            # Wait until all TiFlash nodes are in tombstone status
tiup cluster prune mycluster              # Remove the tiflash nodes in tombestone status
```

2. 准备 TiFlash 的拓扑配置文件，比如 scale-out.topo.yaml 的配置内容如下：

```yaml
tiflash_servers:
  - host: 172.31.8.1
    config:
      flash.disaggregated_mode: tiflash_storage             # This is a Write Node
      storage.s3.endpoint: http://s3.{region}.amazonaws.com # A URL of S3
      storage.s3.bucket: my_bucket                          # All data is stored in this S3 bucket.
      storage.main.dir: ["/data1/tiflash/data"]             # The write buffer directory
  - host: 172.31.9.1
    config:
      flash.disaggregated_mode: tiflash_compute             # This is a Compute Node
      storage.s3.endpoint: http://s3.{region}.amazonaws.com # A URL of S3
      storage.s3.bucket: my_bucket                          # All data is stored in this S3 bucket.
      storage.s3.cache_dir: /data1/tiflash/cache            # Cache directory.
      storage.s3.cache_capacity: 858993459200               # 800GiB
  - host: 172.31.9.2
    config:
      flash.disaggregated_mode: tiflash_compute             # This is a Compute Node
      storage.s3.endpoint: http://s3.{region}.amazonaws.com # A URL of S3
      storage.s3.bucket: my_bucket                          # All data is stored in this S3 bucket.
      storage.s3.cache_dir: /data1/tiflash/cache            # Cache directory.
      storage.s3.cache_capacity: 858993459200               # 800GiB
```

3. 执行扩容 TiFlash 节点，并重新设置 TiFlash replica

```shell
tiup cluster scale-out mycluster ./scale-out.topo.yaml

mysql> alter table table_x set tiflash replica 1;
```

## 使用限制

- TiFlash 不支持在两个架构之间原地切换。在切换架构前，需要把原有 TiFlash 节点全部删除
- 从一种架构迁移到另外一种架构，需要重新同步所有 TiFlash 的数据
- 不允许不同架构的节点同时存在一个集群中
- 存算分离架构只支持使用 S3 API 的对象存储；存算一体架构只支持本地存储
- 使用 S3 存储的情况下，无法启用 "[静态加密](https://docs.pingcap.com/tidb/dev/encryption-at-rest)" 功能，因为 TiFlash 节点无法知道不是本节点生成的文件的密钥