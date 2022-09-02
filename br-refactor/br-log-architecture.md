---
title: TiDB 日志备份和 PITR 功能架构
summary: 了解 TiDB 的日志备份和 PITR 的架构设计
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。 下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程

## 日志备份和 PITR

日志备份和 PITR 的架构实现如下：

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

### 进行日志备份

BR

1. 接收备份命令 (`br log start`)
   - 获得任务启动的 checkpoint ts (start ts)、备份存储地址
   - 在 pd 注册日志备份任务（log backup task）

TiDB

1. 监控日志备份进度
   - 获得每个 TiKV 节点的日志的 checkpoint ts，
   - **Calculate global checkpoint ts**：根据所有子任务的 checkpoint ts 计算整个备份任务的 global checkpoint ts，然后保存到 pd 中（该状态可以通过 `br log status` 查询）

TiKV

1. 监控日志备份任务变动
   - tikv 节点 log backup executor 模块，监听 pd 中日志备份任务的创建，然后运行或更新相应的子任务

2. 持续地备份 KV 变更日志
   - **Backup kv change**：log backup executor 模块读取 kv 数据变更，并且写入到自定义格式的备份文件
   - **Generate self metadata**：log backup executor 定期从 pd 查询日志备份 global checkpoint ts，根据备份数据生成 self log backup metadata，包含 self checkpoint ts、global checkpoint ts、备份文件信息
   - **Upload data and metadata**：log backup executor 定期将日志备份数据和 self log backup metadata 上传到备份存储中
   - **Configure TiDB data GC**：请求 PD 阻止大于 self checkpoint ts 的未备份的数据被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉


### 进行 PITR 恢复

BR

1. 接收备份命令 (`br restore point`)
   - 获得快照备份数据地址、日志备份数据地址、要恢复到的时间点 resolved-ts
   - 查询备份数据中恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在

2. 准备数据恢复
   - **Pause TiDB data GC**: 配置 TiDB 集群，防止接下来要备份的数据被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉
   - **Restore schema**: 读取备份数据的 schema， 恢复的 database 和 table (注意新建表的 table id 与备份数据可能不一样)

3. 恢复全量备份
   -  进行快照备份数据恢复，恢复流程参考 [恢复快照备份数据]()

4. 恢复日志备份
   - **Calculate recovery data**: 读取日志备份数据，计算需要恢复的日志备份数据
   - **Fetch TiKV and region info**: 访问 pd 获取所有 region 和 kv range 对应关系
   - **Request TiKV to restore data**: 创建 LogRestoreRquest 发送到对应的 tikv LogRestoreRquest 包含要恢复的日志备份数据信息

5. 获取恢复结果
   - 存在备份数据恢复失败，则恢复任务失败
   - 全部备份数据都恢复成功后，则恢复任务成功

TiKV

1. 初始化 log restore worker
   - tikv 节点接收到 LogRestoreRquest 后，启动 log restore worker
   - log restore worker 计算恢复数据需要读取的日志备份数据

2. 恢复日志备份数据
    - **Download KV data**：log restore worker 根据 LogRestoreRquest 中要恢复的备份数据，从备份存储中 download 相应的备份数据到本地
    - **Rewrite KVs**：log restore worker 根据恢复集群表的 table ID 对备份数据的 kv 进行 rewrite，将原有的 tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
    - **Apply KVs**：log restore worker 将处理好的 kv 通过 raft api 写 kv store
    - **Report restore result**：log restore worker 返回恢复结果给 br

### 日志备份文件