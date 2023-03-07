---
title: TiDB Lightning 简介
aliases: ['/docs-cn/stable/tidb-lightning/tidb-lightning-overview/','/docs-cn/v4.0/tidb-lightning/tidb-lightning-overview/','/docs-cn/stable/reference/tools/tidb-lightning/overview/']
---

# TiDB Lightning 简介

TiDB Lightning 是一个将全量数据高速导入到 TiDB 集群的工具，可[在此下载](/download-ecosystem-tools.md#tidb-lightning)。

TiDB Lightning 有以下两个主要的使用场景：

- **迅速**导入**大量新**数据。
- 恢复所有备份数据。

目前，TiDB Lightning 支持：

- 导入 [Dumpling](/dumpling-overview.md)、CSV 或 [Amazon Aurora Parquet](/migrate-from-aurora-using-lightning.md) 输出格式的数据源。
- 从本地盘或 [Amazon S3 云盘](/br/backup-and-restore-storages.md)读取数据。

## TiDB Lightning 整体架构

![TiDB Lightning 整体架构](/media/tidb-lightning-architecture.png)

TiDB Lightning 整体工作原理如下：

1. 在导入数据之前，`tidb-lightning` 会自动将 TiKV 集群切换为“导入模式” (import mode)，优化写入效率并停止自动压缩。

2. `tidb-lightning` 会在目标数据库建立架构和表，并获取其元数据。

3. 每张表都会被分割为多个连续的**区块**，这样来自大表 (200 GB+) 的数据就可以用增量方式并行导入。

4. `tidb-lightning` 会为每一个区块准备一个“引擎文件 (engine file)”来处理键值对。`tidb-lightning` 会并发读取 SQL dump，将数据源转换成与 TiDB 相同编码的键值对，然后将这些键值对排序写入本地临时存储文件中。

5. 当一个引擎文件数据写入完毕时，`tidb-lightning` 便开始对目标 TiKV 集群数据进行分裂和调度，然后导入数据到 TiKV 集群。

    引擎文件包含两种：**数据引擎**与**索引引擎**，各自又对应两种键值对：行数据和次级索引。通常行数据在数据源里是完全有序的，而次级索引是无序的。因此，数据引擎文件在对应区块写入完成后会被立即上传，而所有的索引引擎文件只有在整张表所有区块编码完成后才会执行导入。

6. 整张表相关联的所有引擎文件完成导入后，`tidb-lightning` 会对比本地数据源及下游集群的校验和 (checksum)，确保导入的数据无损，然后让 TiDB 分析 (`ANALYZE`) 这些新增的数据，以优化日后的操作。同时，`tidb-lightning` 调整 `AUTO_INCREMENT` 值防止之后新增数据时发生冲突。

    表的自增 ID 是通过行数的**上界**估计值得到的，与表的数据文件总大小成正比。因此，最后的自增 ID 通常比实际行数大得多。这属于正常现象，因为在 TiDB 中自增 ID [不一定是连续分配的](/mysql-compatibility.md#自增-id)。

7. 在所有步骤完毕后，`tidb-lightning` 自动将 TiKV 切换回“普通模式” (normal mode)，此后 TiDB 集群可以正常对外提供服务。

如果需要导入的目标集群是 v3.x 或以下的版本，需要使用 Importer-backend 来完成数据的导入。在这个模式下，`tidb-lightning` 需要将解析的键值对通过 gRPC 发送给 `tikv-importer` 并由 `tikv-importer` 完成数据的导入；TiDB Lightning 还支持使用 TiDB-backend 作为后端导入数据。TiDB-backend 使用和 Loader 类似，`tidb-lightning` 将数据转换为 `INSERT` 语句，然后直接在目标集群上执行这些语句。详见 [TiDB Lightning Backends](/tidb-lightning/tidb-lightning-backends.md)。

## 使用限制

TiDB Lightning 与 TiFlash 一起使用时需要注意：

* 如果集群版本小于 v4.0.6，若先对表创建 TiFlash 副本，再使用 TiDB Lightning 导入数据，会导致数据导入失败。需要在使用 TiDB Lightning 成功导入数据至表后，再对相应的表创建 TiFlash 副本。
* 如果集群版本以及 TiDB Lightning 版本均大于等于 v4.0.6，无论是否已为一张表创建 TiFlash 副本，你均可以使用 TiDB Lightning 导入数据至该表。但该场景下 TiDB Lightning 导入数据耗费的时间更长，具体取决于 TiDB Lightning 部署机器的网卡带宽、TiFlash 节点的 CPU 及磁盘负载、TiFlash 副本数等因素。
