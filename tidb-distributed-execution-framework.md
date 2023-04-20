---
title: TiDB 后端任务分布式框架
summary: TiDB 后端任务分布式框架简介
---

# TiDB 后端任务分布式框架

TiDB 采用计算存储分离架构，具有出色的扩展性和弹性的扩缩容能力。为了进一步挖掘 TiDB 集群分布式架构的资源优势，从 TiDB v7.1.0 开始，引入了一个后端任务分布式执行框架。该框架旨在实现对所有后端任务的统一调度、整体资源使用的管理，并支持集群中所有后端任务在计算节点中以分布式方式执行。

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

## TiDB 后端任务分布式框架的原理

本节介绍了 TiDB 后端任务分布式框架的目标，后端任务的特点，以及该框架的原理。

### 框架的目标

后端任务分布式执行框架的目标是支持 TiDB 集群中所有后端任务在集群中的计算节点中以分布式方式执行。该框架将带来以下三个优点：

- 提供高扩展性、高可用性和高性能的统一能力支持。
- 支持后端任务能够分布式执行，从而更好地利用 TiDB 集群内的计算资源。
- 为接入的后端任务提供统一的资源使用和管理能力，从整体和单个后端任务两个维度提供资源管理的能力，更好地满足用户对于资源使用的预期。

> **Note:**
>
> 本框架不支持 SQL 查询的分布式执行。

### 后端任务

在数据库中，最核心的任务是事务型负载任务 (TP) 和分析型查询任务 (AP)。但除此之外，其他任务也非常重要，例如 DDL 语句、Load Data、TTL、Analyze 和 Backup/Restore 等, 即**后端任务**。

这些任务通常需要处理数据库某一个 schema 或者一个对象的所有数据，这就意味着后端任务通常都会有如下特点：

- 通常需要处理一个 schema 或者一个数据库对象（表）中的所有数据。
- 可能需要周期执行，但是频率不会很高。
- 运行过程中，如果没有很好地控制资源使用，容易对事务型任务和分析型任务造成影响，影响数据库的服务质量。

# 框架的设计与实现原理

TiDB 后端任务分布式执行框架的架构图如下：

![后端任务分布式执行框架的架构](/media/dist-task/dist-task-architect.jpg)

根据上面的架构图，分布式框架中的任务的执行，主要由以下各模块来负责：

- Dispatcher：负责每一个任务的分布式执行计划生成、执行过程管理、任务状态转换、运行时任务信息的收集与反馈等。
- Scheduler：以 TiDB 节点为单位来同步分布式任务的执行，提高后端任务执行效率。
- Subtask Executor：是真正的分布式子任务的执行者，并且将子任务执行状况返回给 Scheduler， 由 Scheduler 来统一更新子任务执行状态。
- 资源池：通过将上述各类模块的计算资源的池化，提供量化资源的使用与管理的基础。

## 启用 TiDB 后端任务分布式框架

如需使用分布式框架，只要设置 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task) 为 `ON`。在运行任务的时候，框架支持的语句即会采用分布式方式执行。

```sql
SET GLOBAL tidb_enable_dist_task = ON;
```

#### 启用前提条件

目前，分布式框架仅支持 `Add index` 任务的分布式执行，使用前，你需要启动 DDL 的快速模式：

**Fast DDL Path:**
从 TiDB v6.5 开始 tidb_ddl_enable_fast_reorg 默认打开，因此 
* [tidb_ddl_enable_fast_reorg](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630)
* [tidb_ddl_disk_quota](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_disk_quota-new-in-v630)

**Config parameter:**

* [temp-dir](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)

> **注意：**
>
> 在升级到 v6.5.0 及以上版本时，建议你检查 TiDB 的 `temp-dir` 路径是否正确挂载了 SSD 磁盘。该参数是 TiDB 的配置参数，设置后需要重启 TiDB 才能生效。因此，在升级前提前进行设置，可以避免再次重启。

### 启用分布式框架相关

此处以启动后端任务的执行 DDL 为例，相关的系统变量如下，这里对于分布式 `Add index` 执行来讲，只需要设置 tidb_ddl_reorg_worker_cnt。**注意** tidb_ddl_reorg_worker_cnt 使用默认值 4 即可，建议最大不超过 16。
tidb_ddl_reorg_batch_size 请保持默认即可，最大不超过 1024。
**System Variables**:

* [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)
* [tidb_ddl_reorg_priority](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_priority)
* [tidb_ddl_error_count_limit](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_error_count_limit)
* [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)

## 另请参阅

* [DDL 执行原理及最佳实践](/ddl-introduction.md)
