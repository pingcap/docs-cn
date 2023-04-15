---
title: TiDB 后端任务分布式框架介绍
aliases: ['/docs-cn/tidb-distributed-parallel-execution-framework/']
---

# 背景介绍
TiDB 是一款纯分布式，因为使用计算存储分离架构，能够拥有良好的扩展性，支持弹性的扩缩容。 为了进一步挖掘出 TiDB 集群分布式架构的资源优势，
我们从 v7.1 开始引入一个统一后端任务分布式执行框架来完成对于所有后端任务的统一调度与整体资源使用方面的管理。
关于 TiDB 的介绍请参阅：[TiDB 简介](/overview.md)

# 后端任务分布式执行框架原理
## 后端任务简介
在数据库中除了事务型负载任务（TP）和分析型查询任务（AP）这两种最核心的任务之外，还有一些非常重要其他任务，例如：DDL 语句，Load Data，TTL, Auto-Analyze and BR 等等。
这些任务的特点都是通常需要处理数据库某一个schema或者一个对象的所有数据，这就意味着后端任务通常都会有如下特点：
1. 通常需要处理全量的一个 schema 或者一个数据库对象（表）中所有数据；
2. 可能需要周期执行，但是频率不会很高；
3. 运行过程如果资源管控没有做好，容易造成对上面说的事务型任务和分析型任务造成影响，影响数据库的服务质量；

## 框架架构
本章将会介绍后端任务分布式执行框架的目标与支持范围，同时会为读者介绍 TiDB 后端任务的原理与启动操作等；
![dist-task-architect.jpg](media%2Fdist-task%2Fdist-task-architect.jpg)
## 目标
顾名思义，后端任务分布式执行框架，我们用来支持 TiDB 集群中的所有后端任务在所有计算节点中分布式执行，。
框架将带来如下三个优点：
1. 框架为 TiDB 后端任务的执行提供统一的高扩展，高可用以及高性能的能力支持。
2. 后端任务能够分布式执行之后，可以更好的利用 TiDB 集群内的计算资源。
3. 框架也可以为接入的后端任务提供统一的资源管控能力，可以从整体和后端任务两个维度提供资源管控的能力，更好的满足用户对于资源使用的预期。
## 非目标
本框架将不会支持 SQL 查询的分布式执行。

## 框架原理简介
本部分将简单介绍框架的设计与实现原理，根据上面的架构图所示，分布式框架的执行主要由以下几个模块来负责：
Dispatcher：负载每一个任务的计划生成，执行流程管理，状态转换，运行时任务状态反馈等任务，是后端任务执行的调度模块；
Scheduler：为了提升后端任务执行效率，我们增加了 scheduler 模块，用来以 TiDB Node 为单位来同步分布式任务的执行；
Subtask executor：是真正的分布式 subtask 在每个 TiDB Node 上面执行并行子任务的执行者，并且每个 executor 会将执行状况返回给 Scheduler 然后由 Scheduler 来统一更新子任务执行状态。
资源池：通过对于上述各类模块的

# 分布式框架的应用和使用
分布式框架的使用非常简单，只需要设置 `tidb_enable_dist_task` 为 `ON`, 框架支持的语句将会在运行任务的时候，将会采用分布式方式执行。
```sql
mysql> set global tidb_enable_dist_task = ON|OFF;
```
### 启用后端分布式框架的前提条件
因为第一期分布式框架将会第一个支持 `Add index` 任务的分布式执行，如果需要启动分布式执行需要同时启动 DDL 的快速模式：
**Fast DDL Path:**
* [tidb_ddl_enable_fast_reorg](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630)
* [tidb_ddl_disk_quota](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_disk_quota-new-in-v630)

**Config parameter:**
* [temp-dir](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)

**Note：** 需要检查 TiDB 的 temp-dir 路径是否正确挂载了 SSD 磁盘，因为这个参数是 TiDB 的配置参数，设置后需要重启 TiDB 才能生效。建议用户在升级到 v6.5 之后的版本时需要检查一下，提前设置；

### 启动后端任务的执行 DDL 为例
**System Variables**:

* [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)
* [tidb_ddl_reorg_priority](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_priority)
* [tidb_ddl_error_count_limit](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_error_count_limit)
* [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)

### 异常处理
目前，异常处理将会比较粗粒度，在执行过程中发生任何不可充实的异常，我们都将回滚执行的任务。

### 故障排查
目前，故障排查主要手段是分析，TiDB 的日志，找到错误的日志，分析错误根因

# 后端任务分布式框架的演进历程
这里我们目前只给出 LTS 版的的计划，可能会根据实际落地情况做一些调整。
## TiDB v7.1 计划
1. 框架的基础模块构建，提供基本的分布式执行能力；
2. 支持 DDL 分区表 `Add index` 的分布式执行；

## 未来工作
1. 持续提升框架的稳定性与执行任务性能；
2. 更多后端任务分布式执行的支持；
3. 提供暂停｜恢复 后端任务的能力，允许用户对于后端任务有一定的控制能力；
4. 提供更好的后端任务运行时资源管控能力；

另请参阅：
* [DDL 执行原理及最佳实践](/ddl-introduction.md)


