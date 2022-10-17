---
title: 日志备份和 PITR 功能架构
summary: 了解 TiDB 的日志备份和 PITR 的架构设计。
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程。

# 日志备份和 PITR 功能架构

日志备份和 PITR 的架构实现如下：

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

## 进行日志备份

日志备份的流程如下：

![BR log backup process design](/media/br/br-log-backup-ts.png)

系统组件和关键概念：

* **local meta**：表示单 TiKV 节点备份下来的数据元信息，主要包括：local checkpoint ts、global checkpoint ts、备份文件信息。
* **local checkpoint ts**： (in local metadata)：表示这个 TiKV 中所有小于 local checkpoint ts 的日志数据已经备份到目标存储。
* **global checkpoint ts**：表示所有 TiKV 中小于 global checkpoint ts 的日志数据已经备份到目标存储。它由运行在 TiDB 中的 Coordinator 模块收集所有 TiKV 的 local checkpoint ts 计算所得，然后上报给 PD。
* **TiDB Coordinator 组件**： TiDB 集群的某个节点会被选举为 Coordinator，负责收集和计算整个日志备份任务的进度（global checkpoint ts）。该组件设计上无状态，在其故障后可以从存活的 TiDB 节点中重新选出一个节点作为 Coordinator。
* **TiKV log observer 组件**：运行在 TiDB 集群的每个 TiKV 节点，负责从 tikv 读取和备份日志数据。 TiKV 节点故障的话，该节点负责备份数据范围，在 region 重新选举后，会被其他 tikv 节点负责，这些节点会从 global checkpoint ts 重新备份故障范围的数据。

完整的备份交互流程描述如下：

1. BR 接收备份命令 (`br log start`)
   * 解析获取日志备份任务的 checkpoint ts (日志备份起始位置)、备份存储地址
   * **Register log backup task**：在 pd 注册日志备份任务（log backup task）

2. TiKV 监控日志备份任务创建/更新
   * **Fetch log backup task**：每个 tikv 节点的 log backup observer 监听 pd 中日志备份任务的创建/更新，然后备份该节点上在备份范围内的数据

3. TiKV log backup observer 持续地备份 KV 变更日志
   * **Read kv change data**：读取 kv 数据变更，然后保存到[自定义格式的备份文件](#日志备份文件)中
   * **Fetch global checkpoint ts**：定期从 pd 查询 global checkpoint ts
   * **Generate local metadata**：定期生成 local metadata（包含 local checkpoint ts、global checkpoint ts、备份文件信息）
   * **Upload log data & metadata**：定期将日志备份数据和 local metadata 上传到备份存储中
   * **Configure GC**：请求 PD 阻止未备份的数据（大于 local checkpoint ts）被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉

4. TiDB Coordinator 监控日志备份进度
   * **Watch backup progress**：轮询所有 TiKV 节点，获取各个 region 的备份进度 (region checkpoint ts）
   * **Report global checkpoint ts**：根据各个 region checkpoint ts，计算整个日志备份任务的进度（global checkpoint ts），然后上报给 pd

5. PD 持久化日志备份任务状态。可以通过 `br log status` 查询

## 进行 PITR

Point in time recovery 的流程如下：

![Point in time recovery process design](/media/br/pitr-ts.png)

1. BR 接收备份命令 (`br restore point`)
   * 解析获取全量备份数据地址、日志备份数据地址、恢复到的时间点
   * 查询备份数据中恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在

2. BR 恢复全量备份
   * 进行快照备份数据恢复，恢复流程参考 [恢复快照备份数据](/br/br-snapshot-architecture.md#恢复快照备份数据)

3. BR 恢复日志备份
   * **Read backup data**: 读取日志备份数据，计算需要恢复的日志备份数据
   * **Fetch region info**: 访问 pd 获取所有 region 和 kv range 对应关系
   * **Request TiKV to restore data**: 创建日志恢复请求发送到对应的 tikv 日志恢复请求包含要恢复的日志备份数据信息

4. TiKV 接受 BR 的恢复请求，初始化 log restore worker
   * log restore worker 获取需要恢复的日志备份数据

5. TiKV 恢复日志备份数据
   * **Download KVs**：log restore worker 根据日志回复请求中要恢复的备份数据，从备份存储中下载相应的备份数据到本地
   * **Rewrite KVs**：log restore worker 根据恢复集群表的 table ID 对备份数据的 kv 进行重写 —— 将原有的 [kv 编码](/tidb-computing.md#表数据与-key-value-的映射关系)中的 tableID 替换为新创建的 tableID。同样的 indexID 也需要相同的处理
   * **Apply KVs**：log restore worker 将处理好的 kv 通过 raft 接口写 store（rocksdb） 中
   * **Report restore result**：log restore worker 返回恢复结果给 br

6. BR 从各个 TiKV 获取恢复结果
   * 如果局部数据恢复因为 RegionNotFound/EpochNotMatch 等原因失败，比如 TiKV 节点故障，br 重试恢复这些数据
   * 如果存在备份数据不可重试的恢复失败，则恢复任务失败
   * 全部备份数据都恢复成功后，则恢复任务成功

## 日志备份文件

快照备份会产生几种类型文件：

- `{min_ts}-{uuid}.log` 文件：存储备份下来的 kv 数据变更记录。其中 {min_ts} 是该文件中所有 kv 数据变更记录数对应的最小 ts；{uuid} 是生成该文件的时候随机生成的。
- `{checkpoint_ts}-{uuid}.meta` 文件: 每个 tikv 节点每次上传日志备份数据时会生成一个该文件，保存本次上传的所有日志备份数据文件 其中 {checkpoint_ts} 是本节点的日志备份的 checkpoint，所有 tikv 节点的最小的 checkpoint 就是日志备份任务最新的 checkpoint；{uuid} 是生成该文件的时候随机生成的。
- `{store_id}.ts` 文件：每个 tikv 节点每次上传日志备份数据时会使用 global checkpoint ts 更新该文件。 其中 {store_id} 是 tikv 的 store ID。 
- `v1_stream_trancate_safepoint.txt` 文件：保存最近一次通过 `br log truncate` 删除日志备份数据后，存储中最早的日志备份数据对应的 ts。

### 备份文件布局

```
.
├── v1
│   ├── backupmeta
│   │   ├── {min_restored_ts}-{uuid}.meta
│   │   ├── {checkpoint}-{uuid}.meta
│   ├── global_checkpoint
│   │   ├── {store_id}.ts
│   ├── {date}
│   │   ├── {hour}
│   │   │   ├── {store_id}
│   │   │   │   ├── {min_ts}-{uuid}.log
│   │   │   │   ├── {min_ts}-{uuid}.log
├── v1_stream_trancate_safepoint.txt 
```   

具体示例如下

```
.
├── v1
│   ├── backupmeta
│   │   ├── ...
│   │   ├── 435213818858112001-e2569bda-a75a-4411-88de-f469b49d6256.meta
│   │   ├── 435214043785779202-1780f291-3b8a-455e-a31d-8a1302c43ead.meta
│   │   ├── 435214443785779202-224f1408-fff5-445f-8e41-ca4fcfbd2a67.meta
│   ├── global_checkpoint
│   │   ├── 1.ts
│   │   ├── 2.ts
│   │   ├── 3.ts
│   ├── 20220811
│   │   ├── 03
│   │   │   ├── 1
│   │   │   │   ├── ...
│   │   │   │   ├── 435213866703257604-60fcbdb6-8f55-4098-b3e7-2ce604dafe54.log
│   │   │   │   ├── 435214023989657606-72ce65ff-1fa8-4705-9fd9-cb4a1e803a56.log
│   │   │   ├── 2
│   │   │   │   ├── ...
│   │   │   │   ├── 435214102632857605-11deba64-beff-4414-bc9c-7a161b6fb22c.log
│   │   │   │   ├── 435214417205657604-e6980303-cbaa-4629-a863-1e745d7b8aed.log
│   │   │   ├── 3
│   │   │   │   ├── ...
│   │   │   │   ├── 435214495848857605-7bf65e92-8c43-427e-b81e-f0050bd40be0.log
│   │   │   │   ├── 435214574492057604-80d3b15e-3d9f-4b0c-b133-87ed3f6b2697.log
├── v1_stream_trancate_safepoint.txt 
```
