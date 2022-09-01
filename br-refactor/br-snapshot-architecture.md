---
title: TiDB 快照备份和恢复功能架构
summary: 了解 TiDB 快照备份和恢复功能的架构设计
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。 下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程

## 快照数据备份和恢复

快照数据备份和恢复的架构实现如下：

![BR snapshot backup and restore architecture](/media/br/br-snapshot-arch.png)

对 TiDB 集群进行快照数据备份时：

1. br 收到 `br backup full` 命令
   -  解析并校验用户操作的输入，获得快照 TSO（backup ts） 、备份存储地址
2. br 配置 TiDB 集群，防止接下来要备份的数据被 GC 机制回收掉
3. br 分配和调度备份任务
   - 访问 pd 获取所有 tikv 节点访问地址，以及数据分布的位置信息
   - 创建 BackupRequest 发送给相应的 tikv 节点，BackupRequest 包含有 backup ts、需要备份的 kvs，备份存储访问信息
4. br 监听每个 BackupRequest 的执行结果，并对结果进行处理
   - 局部备份数据备份因为 region 调度发生变化，则计算这些数据的数据分布位置，然后发送给对应的 tikv 节点进行重新备份
   - 存在数据备份失败，则备份任务失败
   - 全部数据备份成功后，则备份任务成功
5. br 备份 schema，并且按照表对备份数据计算 checksum
6. br 生成 backup metadata，并写入备份存储。backup metadata 包含 backup ts，备份的表，表对应的备份文件，table data checksum 和文件 checksum 等信息
7. tikv 节点执行备份任务
   - tikv 节点接收到 BackupRequest 后，启动 backup worker 进程
   - 从 raft group 角色为 leader 的 region 读取对应 backup ts 的数据
   - 将读取到的数据生成 SST 文件，保存在本地临时目录中
   - 上传 SST 到备份存储中
   - 返回备份结果给 br，包含备份结果、备份的文件信等信息

恢复某个快照备份数据时：

1. br 收到 `br restore` 命令
   - 解析并校验用户操作的输入，获得快照备份数据存储地址
   - 计算需要恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在
2. br 请求 pd 关闭一切调度
3. br 读取备份数据的 schema 信息， 创建需要恢复的 database 和 table
4. br 访问 pd 分配恢复数据的 region。这里需要注意 pd 生成 region 可能经过随机调度，与备份集群的数据分布不一样
   - br 根据的备份数据的信息 - table 、对应的备份数据文件数量和大小，请求 PD 为备份数据 split region，并且 scatter region 使得 region 均匀的分布到存储节点上
5. br 根据 pd 调度结果，创建 RestoreRquest 发送到对应的 tikv 节点，RestoreRquest 包含要恢复的备份数据等信息
6. br 监听每个 RestoreRquest 的执行结果，并对结果进行处理
   - 存在备份数据恢复失败，则恢复任务失败
   - 全部备份都回复成功后，则恢复任务成功
7. tikv 节点恢复备份数据
   - tikv 节点接收到 RestoreRquest 后，启动一个 restore worker
   - 根据 RestoreRquest 中要恢复的备份数据，从备份存储中 download 相应的备份数据到本地
   - 根据 br 创建的表的 table ID 对备份数据的 kv 进行 rewrite，将原有的 tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
   - 将处理好的 SST 文件 ingest 到 rocksdb
   - 返回恢复结果给 br

快照备份恢复流程的详细设计可以参考[备份恢复设计方案](https://github.com/pingcap/tidb/blob/master/br/docs/cn/2019-08-05-new-design-of-backup-restore.md)。

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
