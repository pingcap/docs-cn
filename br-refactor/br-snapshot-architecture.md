---
title: TiDB 快照备份和恢复功能架构
summary: 了解 TiDB 快照备份和恢复功能的架构设计
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。 下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程

## 快照数据备份和恢复

快照数据备份和恢复的架构实现如下：

![BR snapshot backup and restore architecture](/media/br/br-snapshot-arch.png)

### 对 TiDB 集群进行快照数据备份

BR 
  1. Command resolution (`br backup full`)
  - 获得快照点（backup ts）、备份存储地址，确定备份对象

  2. Backup scheudle
  - **Pause TiDB data GC**: 配置 TiDB 集群，防止接下来要备份的数据被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉
  - **Fetch TiKV and region info**: 访问 pd 获取所有 tikv 节点访问地址，以及数据的 region 分布的位置信息
  - **Request TiKV to backup data**: 创建 BackupRequest 发送给相应的 tikv 节点，BackupRequest 包含 backup ts、需要备份的 kv region、备份存储地址

  3. Watch & handle backup result
  - 局部数据因为 region split/merge/schedule 而备份失败。br 重新计算这些数据的 region 分布位置，然后发送给对应的 tikv 节点进行重新备份
  - 任意数据被判断备份失败，则备份任务失败
  - 全部数据备份成功后，则进入 backup finalization

  4. Backup finalization
  - **Backup schema**：备份 schema 并且计算 table data checksum
  - **Put backup metadata**：生成 backup metadata，并上传到备份存储。 backup metadata 包含 backup ts、表和对应的备份文件、data checksum 和 file checksum 等信息

TiKV
  1. Initial backup worker 
  - tikv 节点接收到 BackupRequest 后，启动 backup worker
  - backup worker 计算需要备份的 kv region

  2. Backup data
  - **Scan KVs**：backup worker region (only leader) 读取 backup ts 的快照数据
  - **Generate SST file**：backup worker 将读取到的数据生成 SST 文件，保存在本地临时目录中
  - **Put SST file**: backup worker 上传 SST 到备份存储中
  - **Report backup result**：backup worker 返回备份结果给 br，包含备份结果、备份的文件信等信息

### 恢复某个快照备份数据

BR 
1. Command resolution (`br restore`)
  - 获得快照备份数据存储地址、要恢复 db/table
  - 检查要恢复的 table 是否符合要求不存在

2. Restore scheudle
  - **Pause region scheudle**：请求 pd 在恢复期间关闭自动的 region split/merge/schedule
  - **Restore schema**: 读取备份数据的 schema， 恢复的 database 和 table (注意新建表的 table id 与备份数据可能不一样)
  - **Split & scatter region**：br 基于备份数据信息，请求 pd 分配 region（split region), 并调度 region 均匀分布到存储节点上（scatter region）。每个 region 都有明确的数据范围[start key, end key] 用于解析来恢复数据写入。
  - **Request TiKV to restore data**：根据 pd 分配 region 结果，创建 RestoreRquest 发送到对应的 tikv 节点，RestoreRquest 包含要恢复的备份数据、新建表的 table ID

3. Watch & handle restore result
  - 存在备份数据恢复失败，则恢复任务失败
  - 全部备份都回复成功后，则恢复任务成功

TiKV

1. Initial restore worker 
  - tikv 节点接收到 RestoreRquest 后，启动一个 restore worker
  - restore worker 计算恢复数据需要读取的备份数据

2. Restore data
  - **Download SST**：restore worker 从备份存储中 download 相应的备份数据到本地
  - **Rewrite KV**：restore worker 根据新建表 table ID， 对备份数据相应表的 kv 进行重写 —— 将原有的 tableID 替换为新创建的 tableID。同样的 indexID 也需要相同的处理
  - **Ingest SST**：restore worker 将处理好的 SST 文件 ingest 到 rocksdb 中
  - **Report restore result**：restore worker 返回恢复结果给 br

快照数据备份恢复流程的详细设计可以参考[备份恢复设计方案](https://github.com/pingcap/tidb/blob/master/br/docs/cn/2019-08-05-new-design-of-backup-restore.md)。

### 快照数据备份文件

快照备份会产生几种类型文件：

- `SST` 文件：存储 TiKV 备份下来的数据信息
- `backupmeta` 文件：存储本次备份的元信息，包括备份文件数、备份文件的 Key 区间、备份文件大小和备份文件 Hash (sha256) 值
- `backup.lock` 文件：用于防止多次备份到同一目录

#### SST 文件的命名格式

SST 文件以 `storeID_regionID_regionEpoch_keyHash_timestamp_cf` 的格式命名。格式名的解释如下：

- storeID：TiKV 节点编号
- regionID：Region 编号
- regionEpoch：Region 版本号
- keyHash：Range startKey 的 Hash (sha256) 值，确保唯一性
- timestamp：TiKV 节点生成 SST 文件名时刻的 Unix 时间戳
- cf：RocksDB 的 ColumnFamily（只备份 cf 为 `default` 或 `write` 的数据）

当备份数据到 Amazon S3 或网络盘上时，SST 文件以 `regionID_regionEpoch_keyHash_timestamp_cf` 的格式命名。

#### SST 文件存储格式

- 关于 SST 文件存储格式，可以参考 [RocksDB SST table 介绍](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)。
- 关于 SST 文件中存储的备份数据编码格式，可以参考 [TiDB 表数据与 Key-Value 的映射关系](/tidb-computing.md#表数据与-key-value-的映射关系)。

#### 备份文件布局

将数据备份到 Google Cloud Storage 或 Azure Blob Storage 上时，SST 文件、 backupmeta 文件和 backup.lock 文件在同一目录下。布局如下：

```
.
└── 20220621
    ├── backupmeta
    |—— backup.lock
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
```

将数据备份到 Amazon S3 或网络盘上时，SST 文件会根据 storeID 划分子目录。布局如下：

```
.
└── 20220621
    ├── backupmeta
    |—— backup.lock
    ├── store1
    │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── store100
    │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── store2
    │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── store3
    ├── store4
    └── store5
```
