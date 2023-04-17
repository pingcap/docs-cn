---
title: TiDB 后端任务分布式框架介绍
summary: 介绍 TiDB 后端任务分布式框架的原理与使用。
---

# TiDB 后端任务分布式框架介绍

TiDB 采用计算存储分离架构，具有出色的扩展性和弹性的扩缩容能力。为了进一步挖掘 TiDB 集群分布式架构的资源优势，从 TiDB v7.1.0 开始，引入了一个后端任务分布式执行框架，以实现对所有后端任务的统一调度、整体资源使用的管理。

本文档介绍了 TiDB 后端任务分布式执行框架的原理与使用。

## 框架原理

本节介绍

### 后端任务

在数据库中，最核心的任务是事务型负载任务（TP）和分析型查询任务（AP）。但除此之外，其他任务也非常重要，例如 DDL 语句、Load Data、TTL、Auto-Analyze and BR 等。

这些任务通常需要处理数据库某一个 schema 或者一个对象的所有数据，这就意味着后端任务通常都会有如下特点：

- 通常需要处理全量的一个 schema 或者一个数据库对象（表）中所有数据。
- 可能需要周期执行，但是频率不会很高。
- 运行过程中，如果没有很好地控制资源使用，容易对事务型任务和分析型任务造成影响，影响数据库的服务质量。

### 框架架构

本章将会介绍后端任务分布式执行框架的目标与支持范围，同时会介绍 TiDB 后端任务的原理与启动操作等。

![dist-task-architect.jpg](media/dist-task/dist-task-architect.jpg)

#### 目标

后端任务分布式执行框架的目标是支持 TiDB 集群中所有后端任务在集群中的计算节点中以分布式方式执行。该框架将带来以下三个优点：

1. 提供高扩展性、高可用性和高性能的统一能力支持。
2. 后端任务能够分布式执行，从而更好地利用 TiDB 集群内的计算资源。
3. 为接入的后端任务提供统一的资源使用和管理能力，从整体和单个后端任务两个维度提供资源管理的能力，更好地满足用户对于资源使用的预期。

> **Note:**
>
> 本框架将不会支持 SQL 查询的分布式执行。

### 框架的设计与实现原理

本部分将简单介绍框架的设计与实现原理，根据上面的架构图，分布式框架中的任务的执行主要由以下几个模块来负责：

- Dispatcher：负载每一个任务的分布式执行计划的生成，执行过程管理，任务状态转换，运行时任务信息收集与反馈等。
- Scheduler：以 TiDB Node 为单位来同步分布式任务的执行，提高后端任务执行效率。
- Subtask executor：是真正的分布式子任务的执行者，并且将子任务执行状况返回给 Scheduler， 由 Scheduler 来统一更新子任务执行状态。
- 资源池：通过对于上述各类模块的计算资源的池化，提供量化资源的使用与管理的基础。

## 分布式框架的应用和使用

分布式框架的使用非常简单，只需要设置 `tidb_enable_dist_task` 为 `ON`，在运行任务的时候，框架支持的语句将会采用分布式方式执行。

```sql
SET GLOBAL tidb_enable_dist_task = ON|OFF;
```

### 前提条件

因为第一期分布式框架将会第一个支持 `Add index` 任务的分布式执行，如果需要启动分布式执行需要同时启动 DDL 的快速模式：

**Fast DDL Path:**

* [tidb_ddl_enable_fast_reorg](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630)
* [tidb_ddl_disk_quota](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_disk_quota-new-in-v630)

**Config parameter:**
* [temp-dir](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)

> **注意：**
>
> 需要检查 TiDB 的 temp-dir 路径是否正确挂载了 SSD 磁盘，因为这个参数是 TiDB 的配置参数，设置后需要重启 TiDB 才能生效。建议用户在升级到 v6.5 之后的版本时需要检查一下，提前设置；

### 使用示例

此处以启动后端任务的执行 DDL 为例：

**System Variables**:

* [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)
* [tidb_ddl_reorg_priority](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_priority)
* [tidb_ddl_error_count_limit](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_error_count_limit)
* [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)

## 异常处理和故障排查

在执行过程中，如果发生任何不可修复的异常，TiDB 将回滚执行的任务。目前，故障排查主要是通过分析 TiDB 的日志来找到错误日志，分析错误根本原因。

# 后端任务分布式框架的演进历程
目前，我们只提供了 LTS 版的的一个粗力度的计划，可能会根据实际落地情况做一些调整。

## 第一阶段计划交付的框架能力
1. 构建框架的基础模块，提供基本的分布式执行能力。
2. 支持 DDL 分区表的 Add index 的分布式执行。

## 未来工作
1. 持续提升框架的鲁棒性与执行任务性能。
2. 提供更多后端任务分布式执行的支持。
3. 提供暂停/恢复后端任务的能力，让用户对后端任务有一定的控制能力。
4. 提供更好的后端任务运行时资源管控能力。

另请参阅：
* [DDL 执行原理及最佳实践](/ddl-introduction.md)


