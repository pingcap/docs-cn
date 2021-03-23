---
title: TiDB Lightning 术语表
summary: 了解 TiDB Lightning 相关的术语及定义。
---

# TiDB Lightning 术语表

本术语表提供了 TiDB Lightning 相关的术语和定义，这些术语会出现在 TiDB Lightning 的日志、监控指标、配置和文档中。

<!-- A -->

## A

### Analyze

统计信息分析。指重建 TiDB 表中的统计信息，即运行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 语句。

因为 TiDB Lightning 不通过 TiDB 导入数据，统计信息不会自动更新，所以 TiDB Lightning 在导入后显式地分析每个表。如果不需要该操作，可以将 `post-restore.analyze` 设置为 `false`。

### `AUTO_INCREMENT_ID`

用于为自增列分配默认值的自增 ID 计数器。每张表都有一个相关联的 `AUTO_INCREMENT_ID` 计数器。在 TiDB 中，该计数器还用于分配行 ID。

因为 TiDB Lightning 不通过 TiDB 导入数据，`AUTO_INCREMENT_ID` 计数器不会自动更新，所以 TiDB Lightning 显式地将 `AUTO_INCREMENT_ID` 改为一个有效值。即使表中没有自增列，这步仍是会执行。

<!-- B -->

## B

### Backend

也称作 Back end（后端），用于接受 TiDB Lightning 解析结果。

详情参阅 [TiDB Lightning Backends](/tidb-lightning/tidb-lightning-backends.md)。

<!-- C -->

## C

### Checkpoint

断点。用于保证 TiDB Lightning 在导入数据时不断地将进度保存到本地文件或远程数据库中。这样即使进程崩溃，TiDB Lightning 也能从中间状态恢复。

详情参见 [TiDB Lightning 断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)。

### Checksum

校验和。一种用于[验证导入数据正确性](/tidb-lightning/tidb-lightning-faq.md#如何校验导入的数据的正确性)的方法。

在 TiDB Lightning 中，表的校验和是由 3 个数字组成的集合，由该表中每个键值对的内容计算得出。这些数字分别是：

* 键值对的数量
* 所有键值对的总长度
* 每个键值对 [CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) 按位异或的结果

TiDB Lightning 通过比较每个表的[本地校验和](#local-checksum)和[远程校验和](#remote-checksum)来验证导入数据的正确性。如果有任一对校验和不匹配，导入进程就会停止。如果你需要跳过校验和检查，可以将 `post-restore.checksum` 设置为 `false` 。

遇到校验和不匹配的问题时，参考[常见问题](/tidb-lightning/tidb-lightning-faq.md#checksum-failed-checksum-mismatched-remote-vs-local)进行处理。

### Chunk

一段连续的源数据，通常相当于数据源中的单个文件。

如果单个文件太大，TiDB Lightning 可以将单个文件拆分成多个文件块。

### Compaction

压缩。指将多个小 SST 文件合并为一个大 SST 文件并清理已删除的条目。TiDB Lightning 导入数据时，TiKV 在后台会自动压缩数据。

> **注意：**
>
> 出于遗留原因，你仍然可以将 TiDB Lightning 配置为在每次导入表时进行显式压缩，但是官方不推荐采用该操作，且该操作的相关设置默认是禁用的。
>
> 技术细节参阅 [RocksDB 关于压缩的说明](https://github.com/facebook/rocksdb/wiki/Compaction)。

<!-- D -->

## D

### Data engine

数据引擎。用于对实际的行数据进行排序的[引擎](#engine)。

当一个表数据很多的时候，表的数据会被放置在多个数据引擎中以改善任务流水线并节省 TiKV Importer 的空间。默认条件下，每 100 GB 的 SQL 数据会打开一个新的数据引擎（可通过 `mydumper.batch-size` 配置项进行更改）。

TiDB Lightning 同时处理多个数据引擎（可通过 `lightning.table-concurrency` 配置项进行更改）。

<!-- E -->

## E

### Engine

引擎。在 TiKV Importer 中，一个引擎就是一个用于排序键值对的 RocksDB 实例。

TiDB Lightning 通过引擎将数据传送到 TiKV Importer 中。TiDB Lightning 先打开一个引擎，向其发送未排序的键值对，然后关闭引擎。随后，引擎会对收到的键值对进行排序操作。这些关闭的引擎可以进一步上传至 TiKV store 中为 [Ingest](#ingest) 做准备。

引擎使用 TiKV Importer 的 `import-dir` 作为临时存储，有时也会被称为引擎文件 (engine files)。

另见[数据引擎](#data-engine)和[索引引擎](#index-engine)。

<!-- F -->

## F

### Filter

配置列表，用于指定需要导入或不允许导入的表。

详情见[表库过滤](/table-filter.md)。

<!-- I -->

## I

### Import mode

导入模式。指通过降低读取速度和减少空间使用，来优化 TiKV 写入的配置模式。

导入过程中，TiDB Lightning 自动在导入模式和[普通模式](#normal-mode)中来回切换。如果 TiKV 卡在导入模式，你可以使用 `tidb-lightning-ctl` [强制切换回普通模式](/tidb-lightning/tidb-lightning-faq.md#为什么用过-tidb-lightning-之后tidb-集群变得又慢又耗-cpu)。

### Index engine

索引引擎。用于对索引进行排序的[引擎](#engine)。

不管表中有多少索引，每张表都只对应**一个**索引引擎。

TiDB Lightning 可同时处理多个索引引擎（可通过 `lightning.index-concurrency` 配置项进行更改）。由于每张表正好对应一个索引引擎，`lightning.index-concurrency` 配置项也限定了可同时处理的表的最大数量。

### Ingest

指将 [SST 文件](#sst-file)的全部内容插入到 RocksDB（TiKV）store 中的操作。

与逐个插入键值对相比，Ingest 的效率非常高。因此，该操作直接决定了 TiDB Lightning 的性能。

技术细节参阅 [RocksDB 关于创建、Ingest SST 文件的 wiki 页面](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files)。

<!-- K -->

## K

### KV pair

即 key-value pair（键值对）。

### KV encoder

用于将 SQL 或 CSV 行解析为键值对的例程。多个 KV encoder 会并行运行以加快处理速度。

<!-- L -->

## L

### Local checksum

本地校验和。在将键值对发送到 TiKV Importer 前，由 TiDB Lightning 计算的表的校验和。

<!-- N -->

## N

### Normal mode

普通模式。未启用[导入模式](#import-mode)时的模式。

<!-- P -->

## P

### Post-processing

指整个数据源被解析发送到 TiKV Importer 之后的一段时间。此时 TiDB Lightning 正在等待 TiKV Importer 上传、[Ingest](#ingest) [SST 文件](#sst-file)。

<!-- R -->

## R

### Remote checksum

远程校验和。指导入 TiDB 后所计算的表的[校验和](#checksum)。

<!-- S -->

## S

### Scattering

指随机再分配 [Region](/glossary.md#regionpeerraft-group) 中 leader 和 peer 的操作。Scattering 确保导入的数据在 TiKV store 中均匀分布，这样可以降低 PD 调度的压力。

### Splitting

指 TiKV Importer 在上传之前会将单个引擎文件拆分为若干小 [SST 文件](#sst-file)的操作。这是因为引擎文件通常很大（约为 100 GB），在 TiKV 中不适合视为单一的 [Region](/glossary.md#regionpeerraft-group)。拆分的文件大小可通过 `import.region-split-size` 配置项更改。

### SST file

Sorted string table file（排序字符串表文件）。SST 文件是一种在 RocksDB 中（因而也是 TiKV 中）键值对集合在本地的存储形式。

TiKV Importer 从关闭的[引擎](#engine)中生成 SST 文件。这些 SST 文件接着被上传、[ingest](#ingest) 到 TiKV store 中。
