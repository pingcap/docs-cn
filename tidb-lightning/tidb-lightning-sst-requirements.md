---
title: TiDB Lightning SST Mode 必要条件及限制
---

# TiDB Lightning SST Mode 必要条件及限制

## 运行环境需求

**操作系统**：本文档示例使用的是若干新的、纯净版 CentOS 7 实例，你可以在本地虚拟化一台主机，或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程中，默认会占满 CPU，建议单独部署在一台主机上。如果条件不允许，你可以将 TiDB Lightning 和其他组件（比如`tikv-server`）部署在同一台机器上，然后设置`region-concurrency` 配置项的值为逻辑 CPU 数的 75%，以限制 TiDB Lightning 对 CPU 资源的使用。

**内存和 CPU**：

建议使用 32 核以上的 CPU 和 64 GiB 以上内存以获得更好的性能，关于更多性能与硬件之间的关系，请参考[性能调优](/tidb-lightning/tidb-lightning-sst-tuning.md)。

> **说明：**
>
> 导入大量数据时，一个并发对内存的占用在 2 GiB 左右，也就是说总内存占用最大可达到 region-concurrency * 2 GiB。`region-concurrency` 默认与逻辑 CPU 的数量相同。如果内存的大小（GiB）小于逻辑 CPU 数量的两倍或运行时出现 OOM，需要手动调低 `region-concurrency` 参数以避免 TiDB Lightning OOM。

**存储空间**：配置项 `sorted-kv-dir` 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。建议与 `data-source-dir` 使用不同的存储设备，独占 IO 会获得更好的导入性能，且建议优先考虑配置闪存等高性能存储介质。

**网络**：建议使用 10Gbps 以太网卡。

## 版本要求

- TiDB Lightning 版本 ≥ 4.0.3。
- TiDB 集群版本 ≥ v4.0.0。
- 如果目标 TiDB 集群是 v3.x 或以下的版本，需要使用 Importer-backend 来完成数据的导入。在这个模式下，`tidb-lightning` 需要将解析的键值对通过 gRPC 发送给 `tikv-importer` 并由 `tikv-importer` 完成数据的导入。

## 使用限制

- 请勿使用 local-backend 模式向已经投入生产的 TiDB 集群导入数据，这将对在线业务产生严重影响。

- 默认情况下，不应同时启动多个 TiDB Lightning 实例向同一 TiDB 集群导入数据，而应考虑使用[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)特性。

- 使用多个 TiDB Lightning 向同一目标导入时，请勿混用不同的 backend，例如，不可同时使用 Local-backend 和 TiDB-backend 导入同一 TiDB 集群。

## 与其他组件一同使用的注意事项

- TiDB Lightning 与 TiFlash 一起使用时需要注意：

    - 无论是否已为一张表创建 TiFlash 副本，你都可以使用 TiDB Lightning 导入数据至该表。但该场景下，TiDB Lightning 导入数据耗费的时间更长，具体取决于 TiDB Lightning 部署机器的网卡带宽、TiFlash 节点的 CPU 及磁盘负载及 TiFlash 副本数等因素。

- TiDB Lightning 字符集相关的注意事项：

    - TiDB Lightning 在 v5.4.0 之前不支持导入 `charset=GBK` 的表。

- TiDB Lightning 与 TiCDC 一起使用时需要注意：

    - TiCDC 无法捕获 SST Mode 插入的数据。