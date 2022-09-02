---
title: TiDB 日志备份和 PITR 功能架构
summary: 了解 TiDB 的日志备份和 PITR 的架构设计
---

TiDB 的备份恢复功能，以 br、tidb-operator 为使用入口，创建相应的备份或恢复子任务在各个 TiKV 存储节点运行，进行日志备份或者恢复。 下面以使用 br 工具进行备份恢复为例，介绍备份和恢复的流程

## 日志备份和 PITR

日志备份和 PITR 的架构实现如下：

![BR log backup and PITR architecture](/media/br/br-log-arch.png)

进行日志备份时：

1. br 收到 `br log start` 命令，开启一个日志备份任务在 TiDB 集群中持续运行
   - 解析并教研用户操作的输入。 获得任务启动的 checkpoint ts、备份存储地址
   - 配置 TiDB 集群，防止接下来要备份的数据被 [TiDB GC 机制](/garbage-collection-overview.md)回收掉
   - br 在 pd 注册日志备份任务（log backup task）。log backup task 包含 checkpoint ts、备份存储地址等信息
2. tikv 节点持续执行日志备份任务，直到备份任务出错或者被停止
   - tikv 节点 log backup executor 模块，监听 pd 中日志备份任务的创建和变更，运行或更新相应的子任务
   - log backup executor 模块读取 kv 数据变更，并且写入到自定义格式的备份文件
   - log backup executor 定期从 pd 查询日志备份 checkpoint，根据备份数据生成 self log backup metadata
   - log backup executor 定期将本地 SST 文件和 self log backup metadata 上传到备份存储中
   - 日志备份任务异常后，更新 pd 中日志任务的状态
3. tidb 持续轮训每个 tikv 节点，查询日志备份子任务进展
   - 获得每个 TiKV 节点的日志的 checkpoint ts，
   - 根据所有子任务的 checkpoint ts 计算整个备份任务的 global checkpoint，然后保存到 pd 中（该状态可以通过 `br log status` 查询）

进行 PITR 恢复时：

1. br 收到 `br restore point` 命令，执行 PITR 操作
   - 解析并校验用户操作的输入
     - 获得快照备份数据地址、日志备份数据地址、要恢复到的时间点 resolved-ts
     - 查询备份数据中恢复数据对象（db/table），并检查要恢复的表是否符合要求不存在
     - 请求 pd 关闭自动的 region split/merge/schedule
     - 读取备份数据的 schema 信息， 创建需要恢复的 database 和 table
     - 进行快照备份数据恢复，恢复流程参考恢复某个快照备份数据
     - 进行日志备份数据恢复
       - 读取日志备份数据，计算日志备份文件对应的 kv 范围
       - 查询 pd，对应 kv 范围所在的 region
       - 创建 LogRestoreRquest 发送到对应的 tikv LogRestoreRquest 包含要恢复的日志备份数据信息
     - 监听每个 LogRestoreRquest 的执行结果，并对结果进行处理
       - 存在备份数据恢复失败，则恢复任务失败
       - 全部备份数据都恢复成功后，则恢复任务成功
2. tikv 节点恢复日志备份数据
   - tikv 节点接收到 LogRestoreRquest 后，启动 log restore worker
   - log restore worker 根据 LogRestoreRquest 中要恢复的备份数据，从备份存储中 download 相应的备份数据到本地
   - log restore worker 根据恢复集群表的 table ID 对备份数据的 kv 进行 rewrite，将原有的 tableID 替换为新创建的 tableID，同样的 indexID 也需要相同的处理
   - log restore worker 将处理好的 kv 通过 raft api 写 kv store 
   - log restore worker 返回恢复结果给 br

### 日志备份文件