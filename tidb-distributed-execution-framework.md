---
title: TiDB 后端任务分布式框架
summary: 了解 TiDB 后端任务分布式框架的使用场景与限制、使用方法和实现原理。
---

# TiDB 后端任务分布式框架

TiDB 采用计算存储分离架构，具有出色的扩展性和弹性的扩缩容能力。从 v7.1.0 开始，TiDB 引入了一个后端任务分布式执行框架，以进一步发挥分布式架构的资源优势。该框架的目标是实现对所有后端任务的统一调度与分布式执行，并为接入的后端任务提供统一的资源管理能力，从整体和单个后端任务两个维度提供资源管理的能力，更好地满足用户对于资源使用的预期。

本文档介绍了 TiDB 后端任务分布式框架的使用场景与限制、使用方法和实现原理。

> **注意：**
>
> 本框架不支持 SQL 查询的分布式执行。

## 使用场景与限制

在数据库中，除了核心的事务型负载任务 (TP) 和分析型查询任务 (AP)，也存在着其他重要任务，如 DDL 语句、IMPORT INTO、TTL、Analyze 和 Backup/Restore 等，即**后端任务**。这些任务需要处理数据库对象（表）中的大量数据，通常具有如下特点：

- 需要处理一个 schema 或者一个数据库对象（表）中的所有数据。
- 可能需要周期执行，但频率较低。
- 如果资源控制不当，容易对事务型任务和分析型任务造成影响，影响数据库的服务质量。

启用 TiDB 后端任务分布式框架能够解决上述问题，并且具有以下三个优势：

- 提供高扩展性、高可用性和高性能的统一能力支持。
- 支持后端任务分布式执行，可以在整个 TiDB 集群可用的计算资源范围内进行灵活的调度，从而更好地利用 TiDB 集群内的计算资源。
- 提供统一的资源使用和管理能力，从整体和单个后端任务两个维度提供资源管理的能力。

目前，后端任务分布式框架支持分布式执行 `ADD INDEX` 和 `IMPORT INTO`。

- `ADD INDEX`，即 DDL 创建索引的场景。例如以下 SQL 语句：

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- `IMPORT INTO` 用于将 `CSV`、`SQL`、`PARQUET` 等格式的数据导入到一张空表中。详情请参考 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)。

## 启用前提

使用分布式框架前，你需要启动 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 模式。

1. 调整 Fast Online DDL 相关的系统变量：

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)：从 TiDB v6.5.0 开始默认打开，用于启用快速模式。
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-从-v630-版本开始引入)：用于控制快速模式可使用的本地磁盘最大配额。

2. 调整 Fast Online DDL 相关的配置项：

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)：指定快速模式能够使用的本地盘路径。

> **注意：**
>
> 在升级到 v6.5.0 及以上版本时，建议你检查 TiDB 的 `temp-dir` 路径是否正确挂载了 SSD 磁盘，并确保运行 TiDB 的操作系统用户对该目录有读写权限，否则在运行时可能产生不可预知的问题。该参数是 TiDB 的配置参数，设置后需要重启 TiDB 才能生效。因此，在升级前提前进行设置，可以避免再次重启。

## 启用步骤

1. 启用分布式框架，只需将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 设置为 `ON`：

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    在运行后端任务时，框架支持的语句（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）会采用分布式方式执行。默认集群内部所有节点均会执行后端任务。

2. 根据实际需求，调整可能影响 DDL 任务分布式执行的系统变量：

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：使用默认值 `4` 即可，建议最大不超过 `16`。
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：使用默认值即可，建议最大不超过 `1024`。

3. 从 v7.4.0 开始，你可以根据实际需求，调整执行后端任务的 TiDB 节点数量，在部署 TiDB 后为每一个 TiDB 节点设置 Instance 级别系统变量 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。`tidb_service_scope` 设置为 `background` 时，TiDB 节点可执行后端任务。`tidb_service_scope` 设置为默认值 "" 时，TiDB 节点不可执行后端任务。如果所有节点均未配置 `tidb_service_scope`，框架将调度所有节点执行后端任务。

    > **注意：**
    >
    > - 在分布式任务执行过程中，如果某些 TiDB 节点下线，分布式任务将随机分配子任务到其他可用的 TiDB 节点上，此时无法通过 `tidb_service_scope` 来动态控制子任务的分配。 
    > - 在分布式任务执行过程中，修改 `tidb_service_scope` 的配置不会对当前任务生效，会从下次任务开始生效。

> **建议：**
>
> 对于分布式执行 `ADD INDEX` 语句，只需要设置 `tidb_ddl_reorg_worker_cnt`。

## 实现原理

TiDB 后端任务分布式框架的架构图如下：

![后端任务分布式框架的架构](/media/dist-task/dist-task-architect.jpg)

根据上图，分布式框架中任务的执行主要由以下模块负责：

- Dispatcher：负责生成每个任务的分布式执行计划，管理执行过程，转换任务状态以及收集和反馈运行时任务信息等。
- Scheduler：以 TiDB 节点为单位来同步分布式任务的执行，提高后端任务执行效率。
- Subtask Executor：是实际的分布式子任务执行者，并将子任务的执行情况返回给 Scheduler，由 Scheduler 统一更新子任务的执行状态。
- 资源池：通过对上述各种模块中计算资源进行池化，提供量化资源的使用与管理的基础。

## 另请参阅

* [DDL 执行原理及最佳实践](/ddl-introduction.md)
