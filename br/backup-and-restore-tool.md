---
title: 备份与恢复工具 BR 简介
summary: 了解 BR 工具是什么、有什么用。
aliases: ['/docs-cn/v3.1/br/backup-and-restore-tool/','/docs-cn/v3.1/reference/tools/br/br/','/docs-cn/v3.1/how-to/maintain/backup-and-restore/br/']
---

# 备份与恢复工具 BR 简介

[BR](https://github.com/pingcap/br) 全称为 Backup & Restore，是 TiDB **分布式备份恢复**的命令行工具，用于对 TiDB 集群进行数据备份和恢复。**BR 只支持在 TiDB v3.1 及以上版本使用。**

相比 [`dumpling`](/export-or-backup-using-dumpling.md) 和 [`mydumper`/`loader`](/backup-and-restore-using-mydumper-lightning.md)，BR 更适合**大数据量**的场景。

本文介绍了 BR 的工作原理、推荐部署配置、使用限制以及几种使用方式。

## 工作原理

BR 将备份或恢复操作命令下发到各个 TiKV 节点。TiKV 收到命令后执行相应的备份或恢复操作。

在一次备份或恢复中，各个 TiKV 节点都会有一个对应的备份路径，TiKV 备份时产生的备份文件将会保存在该路径下，恢复时也会从该路径读取相应的备份文件。

![br-arch](/media/br-arch.png)

更多信息请参阅[备份恢复设计方案](https://github.com/pingcap/br/blob/980627aa90e5d6f0349b423127e0221b4fa09ba0/docs/cn/2019-08-05-new-design-of-backup-restore.md)。

### 备份文件类型

备份路径下会生成以下两种类型文件：

- SST 文件：存储 TiKV 备份下来的数据信息
- `backupmeta` 文件：存储本次备份的元信息，包括备份文件数、备份文件的 Key 区间、备份文件大小和备份文件 Hash (sha256) 值

### SST 文件命名格式

SST 文件以 `storeID_regionID_regionEpoch_keyHash_cf` 的格式命名。格式名的解释如下：

- storeID：TiKV 节点编号
- regionID：Region 编号
- regionEpoch：Region 版本号
- keyHash：Range startKey 的 Hash (sha256) 值，确保唯一性
- cf：RocksDB 的 ColumnFamily（默认为 `default` 或 `write`）

## 部署使用 BR 工具

### 推荐部署配置

- 推荐 BR 部署在 PD 节点上。
- 推荐使用一块高性能 SSD 网盘，挂载到 BR 节点和所有 TiKV 节点上，网盘推荐万兆网卡，否则带宽有可能成为备份恢复时的性能瓶颈。

### 使用限制

下面是使用 BR 进行备份恢复的几条限制：

- BR 只支持在 TiDB v3.1 及以上版本使用。
- BR 恢复到 Drainer 的上游集群时，恢复数据无法由 Drainer 同步到下游。
- 在 v3.1 中，只支持在全新的集群上执行恢复操作。

### 最佳实践

下面是使用 BR 进行备份恢复的几种推荐操作：

- 推荐在业务低峰时执行备份操作，这样能最大程度地减少对业务的影响。
- BR 支持在不同拓扑的集群上执行恢复，但恢复期间对在线业务影响很大，建议低峰期或者限速 (`rate-limit`) 执行恢复。
- BR 备份最好串行执行。不同备份任务并行会导致备份性能降低，同时也会影响在线业务。
- BR 恢复最好串行执行。不同恢复任务并行会导致 Region 冲突增多，恢复的性能降低。
- 推荐在 `-s` 指定的备份路径上挂载一个共享存储，例如 NFS。这样能方便收集和管理备份文件。
- 在使用共享存储时，推荐使用高吞吐的存储硬件，因为存储的吞吐会限制备份或恢复的速度。

### 使用方式

在 v3.1 以上的 TiDB 版本中，支持通过命令行工具进行备份恢复。

首先需要下载一个 BR 工具的二进制包，详见[下载链接](/download-ecosystem-tools.md#备份和恢复-br-工具)。

通过命令行工具进行备份恢复的具体操作见[使用备份与恢复工具 BR](/br/use-br-command-line-tool.md)。

## BR 相关文档

+ [使用 BR 命令行备份恢复](/br/use-br-command-line-tool.md)
+ [BR 备份与恢复场景示例](/br/backup-and-restore-use-cases.md)
+ [BR 常见问题](/br/backup-and-restore-faq.md)
