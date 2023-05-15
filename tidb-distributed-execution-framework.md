---
title: TiDB 后端任务分布式框架
summary: 了解 TiDB 后端任务分布式框架的使用场景与限制、使用方法和实现原理。
---

# TiDB 后端任务分布式框架

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。

TiDB 采用计算存储分离架构，具有出色的扩展性和弹性的扩缩容能力。从 TiDB v7.1.0 开始引入了一个后端任务分布式执行框架，以进一步挖掘 TiDB 分布式架构的资源优势。该框架的目标是实现对所有后端任务的统一调度与分布式执行，并为接入的后端任务提供统一的资源管理能力，从整体和单个后端任务两个维度提供资源管理的能力，更好地满足用户对于资源使用的预期。

本文档介绍了 TiDB 后端任务分布式框架的使用场景与限制、使用方法和实现原理。

这些任务通常需要处理相应需要处理大量的用户存储在数据库中的数据，这就意味着后端任务通常都会有如下特点：


# 相关背景知识简介
## 后端任务简介
在数据库中，除了最核心的事务型负载任务 (TP) 和分析型查询任务 (AP) ，也存在着其他重要任务，如 DDL 语句、Load Data、TTL、Analyze 和 Backup/Restore 等，即**后端任务**, 这些任务通常需要处理数据库对象（表）中的大量用户数据，后段任务具有如下特点：

- 需要处理一个 schema 或者一个数据库对象（表）中的所有数据。
- 可能需要周期执行，但频率较低。
- 如果资源控制不当，容易对事务型任务和分析型任务造成影响，影响数据库的服务质量。

# 框架的目标
后端任务分布式执行框架的目标是支持 TiDB 集群中所有后端任务在集群中的计算节点中以分布式方式执行。该框架将带来以下三个优点：

- 提供高扩展性、高可用性和高性能的统一能力支持。
- 支持后端任务分布式执行，可以在整个 TiDB 集群可用的计算资源范围内进行灵活的调度，从而更好地利用 TiDB 集群内的计算资源。
- 提供统一的资源使用和管理能力，从整体和单个后端任务两个维度提供资源管理的能力。

## 使用场景与限制
目前，后端任务分布式框架仅支持以快速模式分布式执行 `ADD INDEX`，即 DDL 创建索引的场景。例如以下 SQL 语句：

```sql
ALTER TABLE t1 ADD INDEX idx1(c1);
CREATE INDEX idx1 ON table t1(c1);
```

> **注意：**
>
> 本框架不支持 SQL 查询的分布式执行。

## 启用前提

目前，分布式框架仅支持 `Add index` 启动快速模式任务的分布式执行，使用前，你需要启动[Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)模式。

* 调整 Fast Online DDL 相关系统变量：

  * [tidb_ddl_enable_fast_reorg](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_enable_fast_reorg-new-in-v630)：从 TiDB v6.5 开始 `tidb_ddl_enable_fast_reorg` 默认打开，用来启动快速模式。
  * [tidb_ddl_disk_quota](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_disk_quota-new-in-v630): 用来控制快速模式可使用的本地磁盘最大配额。

* 调整 Fast Online DDL 相关的配置项：

  * [temp-dir](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)：配置参数用来指定，快速模式能够使用的本地盘路径；

> **注意：**
>
> 在升级到 v6.5.0 及以上版本时，建议你检查 TiDB 的 `temp-dir` 路径是否正确挂载了 SSD 磁盘。该参数是 TiDB 的配置参数，设置后需要重启 TiDB 才能生效。因此，在升级前提前进行设置，可以避免再次重启。

## 启用步骤
1. 完成启用前提的操作。
2. 启用分布式框架，只需将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task) 设置为 `ON`：

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    在运行任务的时候，运行后端任务时，框架支持的语句会采用分布式方式执行。

## 调整可能影响 DDL 任务分布式执行的其他相关参数

    * [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)：使用默认值 `4` 即可，建议最大不超过 `16`。
    * [tidb_ddl_reorg_priority](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_priority)
    * [tidb_ddl_error_count_limit](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_error_count_limit)
    * [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)：使用默认值即可，建议最大不超过 `1024`。

    <Tip>
    对于分布式 `ADD INDEX` 语句，只需要设置 `tidb_ddl_reorg_worker_cnt`。
    </Tip>

# 框架实现原理

TiDB 后端任务分布式框架的架构图如下：

![后端任务分布式框架的架构](/media/dist-task/dist-task-architect.jpg)

根据上图，分布式框架中任务的执行主要由以下模块负责：

- Dispatcher：负责生成每个任务的分布式执行计划，管理执行过程，转换任务状态以及收集和反馈运行时任务信息等。
- Scheduler：以 TiDB 节点为单位来同步分布式任务的执行，提高后端任务执行效率。
- Subtask Executor：是实际的分布式子任务执行者，并将子任务的执行情况返回给 Scheduler，由 Scheduler 统一更新子任务的执行状态。
- 资源池：通过对上述各种模块中计算资源进行池化，提供量化资源的使用与管理的基础。

# 另请参阅

* [DDL 执行原理及最佳实践](/ddl-introduction.md)
