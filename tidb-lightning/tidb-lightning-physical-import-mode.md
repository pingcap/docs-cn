---
title: 物理导入模式
summary: 了解 TiDB Lightning 的物理导入模式。
---

# 物理导入模式简介

物理导入模式 (Physical Import Mode) 是 TiDB Lightning 支持的一种数据导入方式。物理导入模式不经过 SQL 接口，而是直接将数据以键值对的形式插入 TiKV 节点，是一种高效、快速的导入模式。使用物理导入模式时，单个 TiDB Lightning 实例可导入的数据量为 10 TiB，理论上导入的数据量可以随着 TiDB Lightning 实例数量的增加而增加，目前已经有多个用户验证基于[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)功能可以导入的数据量达 50 TiB。

使用前请务必自行阅读[必要条件及限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)。

物理导入模式对应的后端模式为 `local`。可以在配置文件 `tidb-lightning.toml` 中修改：

```toml
[tikv-importer]
# 导入模式配置，设为 "local" 即使用物理导入模式
backend = "local"
```

## 原理说明

1. 在导入数据之前，`tidb-lightning` 会自动将 TiKV 节点切换为“导入模式” (import mode)，优化写入效率并停止自动压缩。以下为各版本的 TiDB Lightning 决定暂停调度的策略：

    - 自 v7.1.0 开始，你可以通过 [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md) 来控制是否暂停全局调度。
    - v6.2.0 ~ v7.0.0 版本的 TiDB Lightning 会根据 TiDB 集群的版本决定是否暂停全局调度。当 TiDB 集群版本 >= v6.1.0，只会暂停目标表数据范围所在 Region 的调度，并在目标表导入完成后恢复调度。其他版本则会暂停全局调度。
    - 当 TiDB Lightning 版本 < v6.2.0 时，`tidb-lightning` 会暂停全局调度。

2. `tidb-lightning` 在目标数据库建立表结构，并获取其元数据。

    如果将 `add-index-by-sql` 设置为 `true`，`tidb-lightning` 会使用 SQL 接口添加索引，并且会在导入数据前移除目标表的所有次级索引。默认值为 `false`，和历史版本保持一致。

3. 每张表都会被分割为多个连续的**区块**，这样来自大表 (200 GB+) 的数据就可以多个并发导入。

4. `tidb-lightning` 会为每一个区块准备一个“引擎文件 (engine file)”来处理键值对。`tidb-lightning` 会并发读取 SQL dump，将数据源转换成与 TiDB 相同编码的键值对，然后将这些键值对排序写入本地临时存储文件中。

5. 当一个引擎文件数据写入完毕时，`tidb-lightning` 便开始对目标 TiKV 集群数据进行分裂和调度，然后导入数据到 TiKV 集群。

    引擎文件包含两种：**数据引擎**与**索引引擎**，各自又对应两种键值对：行数据和次级索引。通常行数据在数据源里是完全有序的，而次级索引是无序的。因此，数据引擎文件在对应区块写入完成后会被立即上传，而所有的索引引擎文件只有在整张表所有区块编码完成后才会执行导入。

    注意当 `tidb-lightning` 使用 SQL 接口添加索引时（即 `add-index-by-sql` 设置为 `true`），索引引擎将不会写入数据，因为此时目标表的次级索引已经在第 2 步中被移除。

6. 整张表相关联的所有引擎文件完成导入后，`tidb-lightning` 会对比本地数据源及下游集群的校验和 (checksum)，确保导入的数据无损，然后添加在第 2 步中被移除的次级索引或让 TiDB 分析 (`ANALYZE`) 这些新增的数据，以优化日后的操作。同时，`tidb-lightning` 调整 `AUTO_INCREMENT` 值防止之后新增数据时发生冲突。

    表的自增 ID 是通过行数的**上界**估计值得到的，与表的数据文件总大小成正比。因此，最后的自增 ID 通常比实际行数大得多。这属于正常现象，因为在 TiDB 中自增 ID [不一定是连续分配的](/mysql-compatibility.md#自增-id)。

7. 在所有步骤完毕后，`tidb-lightning` 自动将 TiKV 切换回“普通模式” (normal mode)，并恢复可能被暂停的全局调度，此后 TiDB 集群可以正常对外提供服务。

## 必要条件及限制

### 运行环境需求

**操作系统**：建议使用新的、纯净版 CentOS 7 实例，你可以在本地虚拟化一台主机，或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程中，默认会占满 CPU，建议单独部署在一台主机上。如果条件不允许，你可以将 TiDB Lightning 和其他组件（比如 `tikv-server`）部署在同一台机器上，然后设置 `region-concurrency` 配置项的值为逻辑 CPU 数的 75%，以限制 TiDB Lightning 对 CPU 资源的使用。

**内存和 CPU**：

建议使用 32 核以上的 CPU 和 64 GiB 以上内存以获得更好的性能。

> **注意：**
>
> 导入大量数据时，一个并发对内存的占用在 2 GiB 左右，也就是说总内存占用最大可达到 region-concurrency * 2 GiB。`region-concurrency` 默认与逻辑 CPU 的数量相同。如果内存的大小（GiB）小于逻辑 CPU 数量的两倍或运行时出现 OOM，需要手动调低 `region-concurrency` 参数以避免 TiDB Lightning OOM。

**存储空间**：配置项 `sorted-kv-dir` 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。建议与 `data-source-dir` 使用不同的存储设备，独占 IO 会获得更好的导入性能，且建议优先考虑配置闪存等高性能存储介质。

**网络**：建议使用 10 Gbps 以太网卡。

### 版本要求

- TiDB Lightning 版本 ≥ 4.0.3。
- TiDB 集群版本 ≥ v4.0.0。
- 如果目标 TiDB 集群是 v3.x 或以下的版本，需要使用 Importer-backend 来完成数据的导入。在这个模式下，`tidb-lightning` 需要将解析的键值对通过 gRPC 发送给 `tikv-importer` 并由 `tikv-importer` 完成数据的导入。

### 使用限制

- 请勿直接使用物理导入模式向已经投入生产的 TiDB 集群导入数据，这将对在线业务产生严重影响。如需向生产集群导入数据，请参考[导入时限制调度范围从集群降低到表级别](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#导入时暂停-pd-调度的范围)。

- 如果你的 TiDB 生产集群上有延迟敏感型业务，并且并发较小，**不建议**使用 TiDB Lightning 物理导入模式导入数据到该集群，因为可能会影响在线业务。

- 默认情况下，不应同时启动多个 TiDB Lightning 实例向同一 TiDB 集群导入数据，而应考虑使用[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)特性。

- 使用多个 TiDB Lightning 向同一目标导入时，请勿混用不同的 backend，即不可同时使用物理导入模式和逻辑导入模式导入同一 TiDB 集群。

- 在导入数据的过程中，请勿在目标表进行 DDL 和 DML 操作，否则会导致导入失败或数据不一致。导入期间也不建议进行读操作，因为读取的数据可能不一致。请在导入操作完成后再进行读写操作。

- 单个 TiDB Lightning 进程导入单表不应超过 10 TB。使用并行导入时，TiDB Lightning 实例不应超过 10 个。

### 与其他组件一同使用的注意事项

- TiDB Lightning 与 TiFlash 一起使用时需要注意：

    - 无论是否已为一张表创建 TiFlash 副本，你都可以使用 TiDB Lightning 导入数据至该表。但该场景下，TiDB Lightning 导入数据耗费的时间更长，具体取决于 TiDB Lightning 部署机器的网卡带宽、TiFlash 节点的 CPU 及磁盘负载及 TiFlash 副本数等因素。

- TiDB Lightning 字符集相关的注意事项：

    - TiDB Lightning 在 v5.4.0 之前不支持导入 `charset=GBK` 的表。

- TiDB Lightning 与 TiCDC 一起使用时需要注意：

    - TiCDC 无法捕获物理导入模式插入的数据。

- TiDB Lightning 与 BR 一起使用时需要注意：

    - BR 快照备份 TiDB Lightning 正在导入的表，会导致该表备份的数据不一致。
    - BR 执行基于 AWS EBS 卷快照的备份，会导致 TiDB Lightning 导入数据失败。
    - TiDB Lightning 物理导入模式导入的数据不支持[日志备份](/br/br-pitr-guide.md#开启日志备份)，因此无法通过 Point-in-time recovery (PITR) 恢复。
