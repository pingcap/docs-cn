---
title: TiDB 备份和恢复功能架构
summary: 了解 TiDB 的备份和恢复功能的架构设计
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务对各个 TiDB 集群的存储节点进行备份或者恢复。 下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程

## 快照数据备份和恢复

快照数据备份和恢复的架构实现如下：

对 TiDB 集群进行快照数据备份时：

1. br 收到 `br backup full` 命令

  + 解析并校验用户操作的输入，获得快照 TSO（backup ts） 、备份存储地址

2. br 配置 TiDB 集群，防止接下来要备份的数据被 GC 机制回收掉
3. br 分配和调度备份任务

  + 访问 pd 获取所有 tikv 节点访问地址，以及数据分布的位置信息
  + 创建 BackupRequest 发送给相应的 tikv 节点，BackupRequest 包含有 backup ts、需要备份的 kvs，备份存储访问信息

4. br 监听每个 BackupRequest 的执行结果，并对结果进行处理

  + 局部备份数据备份因为 region 调度发生变化，则计算这些数据的数据分布位置，然后发送给对应的 tikv 节点进行重新备份
  + 存在数据备份失败，则备份任务失败
  + 全部数据备份成功后，则备份任务成功

5. br 备份 schema，并且按照表对备份数据计算 checksum
6. br 生成 backup metadata，并写入备份存储。backup metadata 包含 backup ts，备份的表，表对应的备份文件，table data checksum 和文件 checksum 等信息
7. tikv 节点执行备份任务

  + tikv 节点接收到 BackupRequest 后，启动 backup worker 进程
  + 从 raft group 角色为 leader 的 region 读取对应 backup ts 的数据
  + 将读取到的数据生成 SST 文件，保存在本地临时目录中
  + 上传 SST 到备份存储中
  + 返回备份结果给 br，包含备份结果、备份的文件信等信息

恢复某个快照备份数据时：

1. br 收到 `br restore` 命令
  + 解析并校验用户操作的输入，获得快照备份数据存储地址
  + 计算需要恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在
2. br 请求 pd 关闭一切调度
3. br 读取备份数据的 schema 信息， 创建需要恢复的 database 和 table
4. br 访问 pd 分配恢复数据的 region。这里需要注意 pd 生成 region 可能经过随机调度，与备份集群的数据分布不一样
  + br 根据的备份数据的信息 - table 、对应的备份数据文件数量和大小，请求 PD 为备份数据 split region，并且 scatter region 使得 region 均匀的分布到存储节点上
5. br 根据 pd 调度结果，创建 RestoreRquest 发送到对应的 tikv 节点，RestoreRquest 包含要恢复的备份数据等信息
6. br 监听每个 RestoreRquest 的执行结果，并对结果进行处理
  + 存在备份数据恢复失败，则恢复任务失败
  + 全部备份都回复成功后，则恢复任务成功
7. tikv 节点恢复备份数据
  + tikv 节点接收到 RestoreRquest 后，启动一个 restore worker
  + 根据 RestoreRquest 中要恢复的备份数据，从备份存储中 download 相应的备份数据到本地
  + 根据 br 创建的表的 table ID 对备份数据的 kv 进行 rewrite，将原有的 tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
  + 将处理好的 SST 文件 ingest 到 rocksdb
  + 返回恢复结果给 br

## 日志备份和恢复

日志备份和恢复的架构实现如下：

![BR log backup and restore architecture](/media/br/br-log-arch.png)

进行日志备份时：

1. br 收到 `br log start` 命令
   + 解析并教研用户操作的输入。 获得日志备份起始 ts 作为任务启动的 checkpoint ts、备份存储地址
2. br 配置 TiDB 集群，防止接下来要备份的数据被 GC 机制回收掉
3. br 在 pd 注册日志备份任务，并在 pd 保存 log backup metadata，metadata 包含日志备份位置 checkpoint ts、备份存储地址等信息
4. pd 持续监听 tikv 节点日志备份子任务进展
  + 获得日志备份子任务的状态、checkpoint ts
  + 根据所有子任务的状态，更新日志备份任务状态、checkpoint ts 等。 该状态可以通过 `br log status` 查询
5. pd 定期生成最新的 log backup metadata，发送 tikv 节点，经其保存到云到存储
6. tikv 节点执行日志备份任务
  + tikv 节点启动一个 log backup executor 模块监听 PD 中日志备份任务的创建，发现任务创建后开始运行相应的子任务
  + backup executor 模块读取 kv 数据变更，并且写入到本地 SST 文件。
  + tikv backup executor 定期将本地 SST 文件发送到备份存储中
  + tikv 定期上报任务进展给 PD
  + tikv 获取 PD 的 log backup metadata，将其保存到备份存储中

进行 PITR 恢复时：

1. br 收到 `br restore point` 命令。
  + 解析并校验用户操作的输入，获得快照备份数据和日志备份数据的存储地址
  + 计算需要恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在
2. br 请求 pd 关闭一切调度
3. br 读取备份数据的 schema 信息， 创建需要恢复的 database 和 table
4. br 进行快照备份数据恢复，恢复流程参考恢复某个快照备份数据
5. br 读取备份存储中的日志备份数据，并计算筛选出来需要恢复的日志备份数据。
6. br 访问 pd 分配恢复日志备份数据的 region
  + br 根据的日志备份备份数据的信息 - table 、对应的备份数据文件数量和大小，请求 PD 为备份数据 split region，并且 scatter region 使得 region 均匀的分布到存储节点上
7. br 根据 pd 调度结果，创建 LogRestoreRquest 发送到对应的 tikv LogRestoreRquest 包含要恢复的日志备份数据等信息
8. br 监听每个 LogRestoreRquest 的执行结果，并对结果进行处理
  + 存在备份数据恢复失败，则恢复任务失败
  + 全部备份数据都恢复成功后，则恢复任务成功
9. tikv 节点恢复日志备份数据
  + tikv 节点接收到 LogRestoreRquest 后，启动一个 restore worker
  + 根据 LogRestoreRquest 中要恢复的备份数据，从备份存储中 download 相应的备份数据到本地
  + 根据 br 创建的表的 table ID 对备份数据的 kv 进行 rewrite，将原有的 tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
  + 将处理好的 kv 写入到 kv engine
  + 返回恢复结果给 br