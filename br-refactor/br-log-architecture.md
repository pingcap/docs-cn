---
title: 日志备份和 PITR 功能架构
summary: 了解 TiDB 的日志备份和 PITR 的架构设计。
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程。

# 日志备份和 PITR 功能架构

日志备份和 PITR 的架构实现如下：

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

## 进行日志备份

BR

1. 接收备份命令 (`br log start`)
   - 解析获取日志备份任务 checkpoint ts (start ts)、备份存储地址
   - **Register log backup task**：在 pd 注册日志备份任务（log backup task）

TiDB

1. 监控日志备份任务进度
   - **Polling subtasks**：轮询所有 TiKV 节点，获取其日志备份子任务的 checkpoint ts
   - **Report global checkpoint ts**：计算整个备份任务的 global checkpoint ts，然后保存到 pd 中（该状态可以通过 `br log status` 查询）

TiKV

1. 监控日志备份任务创建/更新
   - **Watch task**：tikv 节点 log backup executor 监听 pd 中日志备份任务的创建/更新，然后运行/更新相应的子任务

2. 持续地备份 KV 变更日志
   - **read kv change data**：log backup executor 读取 kv 数据变更，然后保存到自定义格式的备份文件中
   - **Fetch Global checkpoint ts**：log backup executor 定期从 pd 查询 global checkpoint ts
   - **Generate self metadata**：生成 self log backup metadata，包含 self checkpoint ts、global checkpoint ts、备份文件信息
   - **Upload kv & metadata**：log backup executor 定期将日志备份数据和 self log backup metadata 上传到备份存储中
   - **Configure GC**：请求 PD 阻止大于 self checkpoint ts 且未备份的数据被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉


## 进行 PITR

BR

1. 接收备份命令 (`br restore point`)
   - 解析获取全量备份数据地址、日志备份数据地址、恢复到的时间点 resolved-ts
   - 查询备份数据中恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在

2. 恢复 schema
   - **Restore schema**: 读取备份数据的 schema， 恢复的 database 和 table (注意新建表的 table id 与备份数据可能不一样)

3. 恢复全量备份
   -  进行快照备份数据恢复，恢复流程参考 [恢复快照备份数据](/br-refactor/br-snapshot-architecture.md#恢复某个快照备份数据)

4. 恢复日志备份
   - **Read backup data**: 读取日志备份数据，计算需要恢复的日志备份数据
   - **Fetch region info**: 访问 pd 获取所有 region 和 kv range 对应关系
   - **Request TiKV to restore data**: 创建 LogRestoreRquest 发送到对应的 tikv LogRestoreRquest 包含要恢复的日志备份数据信息

5. 获取恢复结果
   - 存在备份数据恢复失败，则恢复任务失败
   - 全部备份数据都恢复成功后，则恢复任务成功

TiKV

1. 初始化 log restore worker
   - tikv 节点接收到 LogRestoreRquest 后，启动 log restore worker
   - log restore worker 计算恢复数据需要读取的日志备份数据

2. 恢复日志备份数据
    - **Download KVs**：log restore worker 根据 LogRestoreRquest 中要恢复的备份数据，从备份存储中下载相应的备份数据到本地
    - **Rewrite KVs**：log restore worker 根据恢复集群表的 table ID 对备份数据的 kv 进行重写。tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
    - **Apply KVs**：log restore worker 将处理好的 kv 通过 raft 接口写 kv store
    - **Report restore result**：log restore worker 返回恢复结果给 br

## 日志备份文件