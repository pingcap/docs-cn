---
title: 50 TB 数据导入最佳实践
summary: 本文根据大单表导入的经验，总结出了一套导入大量数据的最佳实践，希望对大数据量、大单表导入有所帮助。
---

# 50 TB 数据导入最佳实践

TiDB Lightning（[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)）是一款用于空表导入、空集群初始化的全量和高效的数据导入工具。并且 TiDB Lightning 以文件作为数据源。TiDB Lightning 提供了两种运行方式：单实例和[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)，满足不同规模的源文件导入。

- 如果源文件数据规模在 10 TB 以内，建议通过单个 TiDB Lightning 实例进行导入。
- 如果源文件数据规模超过 10 TB，建议通过多个 TiDB Lightning 实例进行[并行导入](/tidb-lightning/tidb-lightning-distributed-import.md)。
- 如果源文件数据规模特别大（比如达到 50 TB 及以上），在使用并行导入的同时，还需要针对源数据特点、表定义、参数配置等进行一定的准备和调优，才能更好、更快的完成大规模的数据导入。

本文主要介绍了影响 TiDB Lightning 数据导入的一些关键因素及操作步骤。我们在内部环境和客户现场都曾成功导入过 50 TB 以上的大单表数据，基于这些真实的应用场景，沉淀了本文中的最佳实践。这些最佳实践可以帮助你成功导入大型数据。

本文中的以下内容同时适用于导入多表和导入大单表：

- [关键因素](#关键因素)
- [准备源文件](#准备源文件)
- [预估存储空间](#预估存储空间)
- [配置参数](#配置参数)
- [解决 "checksum mismatch" 问题](#解决-checksum-mismatch-问题)
- [开启断点续传](#开启断点续传)
- [故障处理](#故障处理)

由于导入大单表的特殊性，以下章节单独介绍了相关最佳实践：

- [导入大单表的最佳实践](#导入大单表的最佳实践)

## 关键因素

在导入数据时，有一些关键因素会影响导入性能，甚至可能导致导入失败。一些常见的关键因素如下：

- 源文件

    - 单个文件内数据是否按照主键有序。有序可以达到最优导入性能。
    - 多个 TiDB Lightning 实例对应的源文件内容是否按照主键有交叠。交叠越小，导入性能越好。

- 表定义

    - 每个表二级索引数量、大小会影响导入速度。索引越少，导入越快，导入后空间占用越小。
    - 索引数据大小 = 索引数量 \* 索引大小 \* 数据行数。

- 压缩率

    数据导入 TiDB 集群后会被压缩存储，而压缩率无法预先计算，只有数据真正导入到 TiKV 集群后才能知道。可以先导入少量数据（如 10%），获取到集群对应的压缩率，然后以此作为全部数据导入后的压缩率。

- 配置参数

    以下配置参数的设置也会影响数据导入：

    - `region-concurrency`：TiDB Lightning 主逻辑处理的并发度。
    - `send-kv-pairs`：TiDB Lightning 发送给 TiKV 单次请求的 Key、Value 数量。
    - `disk-quota`：使用物理导入模式时，配置 TiDB Lightning 本地临时文件使用的磁盘配额 (disk quota)。
    - `GOMEMLIMIT`：TiDB Lightning 采用 Go 语言实现，需要合理配置 `GOMEMLIMIT`。

    关于 TiDB Lightning 参数信息，请参考 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

- 数据校验

    数据和索引导入完成后，会对每个表执行 [`ADMIN CHECKSUM`](/sql-statements/sql-statement-admin-checksum-table.md)，然后跟 TiDB Lightning 本地 Checksum 值做对比。当有很多表或单个表行数很多时，Checksum 阶段耗时会很长。

- 执行计划

    Checksum 通过后会对每个表执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)，构建最佳的执行计划。当有很多表或单个表很大时，ANALYZE 阶段耗时会很长。

- 相关 Issue

    在实际导入 50 TB 数据的过程中，存在一些在海量源文件及大规模集群下才会暴露出的一些问题。在选择产品版本时，请检查是否包含对应的 Issue 修复。以下 Issue 在 v6.5.3、v7.1.0 及更新的版本都已修复。

    - [Issue-14745](https://github.com/tikv/tikv/issues/14745)：导入完成后 TiKV Import 目录遗留大量临时文件。
    - [Issue-6426](https://github.com/tikv/pd/issues/6426)：PD [范围调度](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#导入时暂停-pd-调度的范围)接口存在未打散 Region 的情况，导致 Scatter Region 超时。v6.2.0 之前采用停止全局调度的方式，不会出现该问题。
    - [Issue-43079](https://github.com/pingcap/tidb/pull/43079)：TiDB Lightning 对 NotLeader 错误的重试未刷新 Region Peers 信息。
    - [Issue-43291](https://github.com/pingcap/tidb/issues/43291)：TiDB Lightning 未对临时文件删除的情况（"No such file or directory"）进行重试。

## 准备源文件

- 生成文件时，单个文件内，尽量按照主键排序；如果表定义没有主键，可以添加一个自增主键，此时对文件内容顺序无要求。
- 多个 TiDB Lightning 实例在划分源文件时，尽量降低主键交叠。如果生成文件时全局有序，可以按照范围划分文件给不同 TiDB Lightning 实例，达到最佳导入效果。
- 在生成文件时，每个文件尽量控制在 96 MB 以下。
- 如果文件特别大，超过 256 MB，需要开启 [strict-format](/migrate-from-csv-files-to-tidb.md#第-4-步导入性能优化可选)。

## 预估存储空间

目前有以下两种有效的空间预估方法：

- 假设数据总大小为 A，索引总大小为 B，副本数为 3，压缩率为 α（一般在在 2.5 左右），则总的占用空间为：(A+B)*3/α。该方法主要用于不进行任何数据导入时的估算，以此规划集群拓扑。
- 预先导入 10% 的数据，实际占用空间再乘以 10，即可认为是该批数据最终的空间占用。该方法更加准确，尤其是对于导入大量数据时比较有效。

注意要预留 20% 的存储空间，后台任务如压缩、复制快照等会使用部分存储空间。

## 配置参数

需要正确设置以下配置参数：

- `region-concurrency`：TiDB Lightning 主逻辑处理的并发度。在并行导入时，可以设置为 CPU 核数的 75%，防止出现资源过载带来 OOM 问题。
- `send-kv-pairs`：TiDB Lightning 发送给 TiKV 单次请求的 Key、Value 数量，建议按照 send-kv-pairs * row-size < 1 MB 调整该值。v7.2.0 版本会用 `send-kv-size` 代替该参数，且无需单独设置。
- `disk-quota`：尽量保证 TiDB Lightning 排序目录空间大于数据源大小。如无法保证，可以设置 `disk-quota` 为 TiDB Lightning 排序目录空间的 80%。此时 TiDB Lightning 会按照 `disk-quota` 的大小为一个批次去排序、写入，导入性能低于完整排序。
- `GOMEMLIMIT`：TiDB Lightning 采用 Go 语言实现，设置 `GOMEMLIMIT` 为实例内存的 80%，降低因为 Go GC 机制带来的 OOM 概率。

关于 TiDB Lightning 参数信息，请参考 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

## 解决 "checksum mismatch" 问题

在数据校验过程中，可能会出现冲突数据，报错信息为："checksum mismatch"。出现该问题，可以按照以下思路解决：

1. 排查源数据是否有主键、唯一键冲突，解决冲突后再重新导入。从过往经验来看，这是主要原因及解决方式。
2. 表主键、唯一键定义是否合理。如果不合理，更改表定义后重新导入。
3. 开启[冲突检测功能](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#冲突数据检测)。该功能是在上述两个步骤排查后，认为源数据中有少量（低于 10%）不可预期的冲突数据，需要 TiDB Lightning 帮助检测、解决冲突数据。

## 开启断点续传

大体量的数据导入，一定要参照[断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)文档，开启断点续传，并推荐优先使用 MySQL 作为 Driver，避免因为 TiDB Lightning 运行在容器环境，容器退出后断点信息被一并删除。

如果导入过程中遇到下游 TiKV 空间不足，可以手动执行 `kill` 命令关闭（不要带 `-9` 选项）所有 TiDB Lightning 实例，待扩容后，基于断点信息继续导入。

## 导入大单表的最佳实践

多表导入会带来 Checksum、Analyze 时间的增加，甚至超过数据导入本身，但是一般不需要调整配置。如果多表中存在单个或多个大表的情况，可以把这类大表的源文件划分出来，单独进行导入。

本小节重点介绍大单表导入的最佳实践。大单表没有严格的定义，一般认为符合以下任一条件者即为大单表：

- 大小超过 10 TB
- 行数超过 10 亿、列超过 50 的宽表

### 准备源文件

根据上述源文件准备的步骤产生源文件，对于大单表，如果你不能做到全局有序，但是可以做到文件内按主键有序，且是标准的 CSV 文件，可以尽量生成单个大文件（每个 20 GB），然后开启 [strict-format](/migrate-from-csv-files-to-tidb.md#第-4-步导入性能优化可选)，既可以降低 TiDB Lightning 实例之间的交叠，又能在导入前由 TiDB Lightning 进行大文件切分，达到最佳的导入速度。

### 规划集群拓扑

TiDB Lightning 按照每个实例处理 5 TB 到 10 TB 源数据进行准备，每个机器节点部署一个 TiDB Lightning 实例，机器节点规格可以参照 [TiDB Lightning 实例必要条件及限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)。

### 调整配置参数

需要调整以下配置参数：

- `region-concurrency` 设置为 TiDB Lightning 实例核数的 75%。
- `send-kv-pairs` 设置为 `3200`。适用于 v7.1.0 及更早的版本。v7.2.0 开始引入了 `send-kv-size` 参数，无需配置。
- `GOMEMLIMIT` 调整为实例所在节点内存的 80%。

如果导入过程中发现 PD Scatter Region 的时延超过 30 分钟，可以从以下维度调优：

- 排查 TiKV 集群是否遇到 IO 瓶颈。
- 调高 TiKV `raftstore.apply-pool-size`，从默认值 `2` 调整为 `4` 或 `8`。
- 降低 TiDB Lightning `region-split-concurrency` 为 CPU 核数的一半，最低可调整为 `1`。

### 关闭执行计划

当存在单个大表的情况，建议关掉 `analyze`（`analyze="off"`）。在导入结束后，再手动执行 [ANALYZE TABLE](/sql-statements/sql-statement-analyze-table.md#analyze)。

## 故障处理

如果在使用 TiDB Lightning 的过程中遇到问题，请参考 [TiDB Lightning 故障处理](/tidb-lightning/troubleshoot-tidb-lightning.md)。
