---
title: TiDB 分布式执行框架 (DXF)
summary: 了解 TiDB 分布式执行框架 (DXF) 的使用场景、限制、使用方法和实现原理。
---

# TiDB 分布式执行框架 (DXF)

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

TiDB 采用计算存储分离架构，具有出色的可扩展性和弹性。从 v7.1.0 开始，TiDB 引入了**分布式执行框架（Distributed eXecution Framework，DXF）**，以进一步利用分布式架构的资源优势。DXF 的目标是实现任务的统一调度和分布式执行，并为整体和单个任务提供统一的资源管理能力，更好地满足用户对资源使用的期望。

本文档描述了 DXF 的使用场景、限制、使用方法和实现原理。

## 使用场景

在数据库管理系统中，除了核心的事务处理（TP）和分析处理（AP）工作负载外，还有其他重要任务，如 DDL 操作、[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)、[TTL](/time-to-live.md)、[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 和备份/恢复。这些任务需要处理数据库对象（表）中的大量数据，因此通常具有以下特点：

- 需要处理 schema 或数据库对象（表）中的所有数据。
- 可能需要定期执行，但频率较低。
- 如果资源控制不当，容易影响 TP 和 AP 任务，降低数据库服务质量。

启用 DXF 可以解决上述问题，并具有以下三个优势：

- 框架提供统一的高可扩展性、高可用性和高性能能力。
- DXF 支持任务的分布式执行，可以灵活调度整个 TiDB 集群的可用计算资源，从而更好地利用 TiDB 集群中的计算资源。
- DXF 为整体和单个任务提供统一的资源使用和管理能力。

目前，DXF 支持 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句的分布式执行。

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 是用于创建索引的 DDL 语句。例如：

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 用于将 CSV、SQL 和 Parquet 等格式的数据导入空表。

## 限制

DXF 最多只能同时调度 16 个任务（包括 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 任务）。

## 前提条件

在使用 DXF 执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务之前，你需要启用[快速在线 DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 模式。

<CustomContent platform="tidb">

1. 调整以下与快速在线 DDL 相关的系统变量：

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于启用快速在线 DDL 模式。从 TiDB v6.5.0 开始默认启用。
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制快速在线 DDL 模式下可以使用的本地磁盘最大配额。

2. 调整以下与快速在线 DDL 相关的配置项：

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)：指定快速在线 DDL 模式下可以使用的本地磁盘路径。

> **注意：**
>
> 建议为 TiDB `temp-dir` 目录准备至少 100 GiB 的可用空间。

</CustomContent>

<CustomContent platform="tidb-cloud">

调整以下与快速在线 DDL 相关的系统变量：

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于启用快速在线 DDL 模式。从 TiDB v6.5.0 开始默认启用。
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制快速在线 DDL 模式下可以使用的本地磁盘最大配额。

</CustomContent>

## 使用方法

1. 要启用 DXF，请将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 的值设置为 `ON`。从 v8.1.0 开始，此变量默认启用。对于 v8.1.0 或更高版本的新创建集群，你可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    当 DXF 任务运行时，框架支持的语句（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）以分布式方式执行。默认情况下，所有 TiDB 节点都运行 DXF 任务。

2. 通常，对于可能影响 DDL 任务分布式执行的以下系统变量，建议使用其默认值：

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：使用默认值 `4`。建议的最大值是 `16`。
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：使用默认值。建议的最大值是 `1024`。

## 任务调度

默认情况下，DXF 调度所有 TiDB 节点执行分布式任务。从 v7.4.0 开始，对于 TiDB 自管理集群，你可以通过配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 来控制哪些 TiDB 节点可以被 DXF 调度执行分布式任务。

- 对于 v7.4.0 到 v8.0.0 的版本，[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 的可选值为 `''` 或 `background`。如果当前集群有 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会将任务调度到这些节点执行。如果当前集群没有 `tidb_service_scope = 'background'` 的 TiDB 节点（无论是由于故障还是正常缩容），DXF 会将任务调度到 `tidb_service_scope = ''` 的节点执行。

- 从 v8.1.0 开始，你可以将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为任何有效值。当提交分布式任务时，任务会绑定到当前连接的 TiDB 节点的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值，DXF 只会将任务调度到具有相同 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值的 TiDB 节点执行。但是，为了与早期版本的配置兼容，如果在 `tidb_service_scope = ''` 的节点上提交分布式任务，且当前集群有 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会将任务调度到 `tidb_service_scope = 'background'` 的 TiDB 节点执行。

从 v8.1.0 开始，如果在任务执行期间添加了新节点，DXF 会根据上述规则决定是否将任务调度到新节点执行。如果你不希望新添加的节点执行任务，建议提前为这些新添加的节点设置不同的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)。

> **注意：**
>
> - 对于 v7.4.0 到 v8.0.0 的版本，在具有多个 TiDB 节点的集群中，强烈建议在两个或更多 TiDB 节点上将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为 `background`。如果此变量仅在单个 TiDB 节点上设置，当该节点重启或故障时，任务将被重新调度到 `tidb_service_scope = ''` 的 TiDB 节点，这会影响在这些 TiDB 节点上运行的应用程序。
> - 在分布式任务执行期间，对 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 配置的更改不会对当前任务生效，但会从下一个任务开始生效。

## 实现原理

DXF 的架构如下：

![DXF 的架构](/media/dist-task/dist-task-architect.jpg)

如上图所示，DXF 中的任务执行主要由以下模块处理：

- Dispatcher：为每个任务生成分布式执行计划，管理执行过程，转换任务状态，收集和反馈运行时任务信息。
- Scheduler：在 TiDB 节点之间复制分布式任务的执行，以提高任务执行效率。
- Subtask Executor：分布式子任务的实际执行器。此外，Subtask Executor 将子任务的执行状态返回给 Scheduler，Scheduler 统一更新子任务的执行状态。
- 资源池：通过池化上述模块的计算资源，为资源使用和管理的量化提供基础。

## 另请参阅

<CustomContent platform="tidb">

* [DDL 语句的执行原理和最佳实践](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [DDL 语句的执行原理和最佳实践](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>
