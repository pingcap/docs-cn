---
title: 备份与恢复工具 BR 的设计
summary: 了解 BR 的设计细节。
---

## BR 架构

BR 将备份或恢复操作命令下发到各个 TiKV 节点。TiKV 收到命令后执行相应的备份或恢复操作。

在一次备份或恢复中，各个 TiKV 节点都会有一个对应的备份路径，TiKV 备份时产生的备份文件将会保存在该路径下，恢复时也会从该路径读取相应的备份文件。

![br-arch](/media/br-arch.png)

## BR 设计

备份恢复流程的详细设计可以参考[备份恢复设计方案](https://github.com/pingcap/br/blob/980627aa90e5d6f0349b423127e0221b4fa09ba0/docs/cn/2019-08-05-new-design-of-backup-restore.md)。

## 备份文件介绍

下面介绍一下 BR 会生成的备份文件格式设计。

### 备份文件的类型

备份路径下会生成以下几种类型文件：

- `SST` 文件：存储 TiKV 备份下来的数据信息
- `backupmeta` 文件：存储本次备份的元信息，包括备份文件数、备份文件的 Key 区间、备份文件大小和备份文件 Hash (sha256) 值
- `backup.lock` 文件：用于防止多次备份到同一目录

### SST 文件的命名格式

SST 文件以 `storeID_regionID_regionEpoch_keyHash_cf` 的格式命名。格式名的解释如下：

- storeID：TiKV 节点编号
- regionID：Region 编号
- regionEpoch：Region 版本号
- keyHash：Range startKey 的 Hash (sha256) 值，确保唯一性
- cf：RocksDB 的 ColumnFamily（默认为 `default` 或 `write`）

### SST 文件存储格式

- SST 文件存储格式可以参考这篇 [RocksDB SST table 介绍](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)。
- SST 文件中存储的备份数据编码格式可以参考 [TiDB 表数据与 Key-Value 的映射关系](/tidb-computing.md#表数据与-key-value-的映射关系)。
