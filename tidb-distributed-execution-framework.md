---
title: TiDB 分布式执行框架
summary: 了解 TiDB 分布式执行框架的使用场景、限制、使用方法和实现原理。
---

# TiDB 分布式执行框架

TiDB 采用计算存储分离架构，具有出色的扩展性和弹性的扩缩容能力。从 v7.1.0 开始，TiDB 引入了一个分布式执行框架，以进一步发挥分布式架构的资源优势。该框架的目标是对基于该框架的任务进行统一调度与分布式执行，并提供整体和单个任务两个维度的资源管理能力，更好地满足用户对于资源使用的预期。

本文档介绍了 TiDB 分布式执行框架的使用场景、限制、使用方法和实现原理。

## 使用场景

在数据库中，除了核心的事务型负载任务 (TP) 和分析型查询任务 (AP)，也存在着其他重要任务，如 DDL 语句、[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)、[TTL](/time-to-live.md)、[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 和 Backup/Restore 等。这些任务需要处理数据库对象（表）中的大量数据，通常具有如下特点：

- 需要处理一个 schema 或者一个数据库对象（表）中的所有数据。
- 可能需要周期执行，但频率较低。
- 如果资源控制不当，容易对事务型任务和分析型任务造成影响，影响数据库的服务质量。

启用 TiDB 分布式执行框架能够解决上述问题，并且具有以下三个优势：

- 提供高扩展性、高可用性和高性能的统一能力支持。
- 支持任务分布式执行，可以在整个 TiDB 集群可用的计算资源范围内进行灵活的调度，从而更好地利用 TiDB 集群内的计算资源。
- 提供统一的资源使用和管理能力，从整体和单个任务两个维度提供资源管理的能力。

目前，分布式执行框架支持分布式执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 这两类任务。

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)，即 DDL 创建索引的场景。例如以下 SQL 语句：

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 即通过该 SQL 语句将 CSV、SQL、PARQUET 等格式的数据导入到一张空表中。

## 使用限制

分布式执行框架最多同时调度 16 个任务（包括 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）。

### `ADD INDEX` 的使用限制

- 在 v8.1.0 之前，集群内同时只能有一个 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务进行分布式执行。如果在当前的 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 分布式任务还未执行完成时就提交了一个新的 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务，则新提交的 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务不会被该框架调度，而是直接通过事务的方式来执行。
- 从 v8.1.0 开始，分布式执行框架支持并行执行多个 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务。
- 不支持通过分布式执行框架对数据类型为 `TIMESTAMP` 的列添加索引，否则会导致索引和数据不一致的问题。

## 启用前提

如需使用分布式执行框架执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务，需要先开启 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入) 模式。

1. 调整 Fast Online DDL 相关的系统变量：

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-从-v630-版本开始引入)：从 TiDB v6.5.0 开始默认打开，用于启用快速模式。
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-从-v630-版本开始引入)：用于控制快速模式可使用的本地磁盘最大配额。

2. 调整 Fast Online DDL 相关的配置项：

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-从-v630-版本开始引入)：指定快速模式能够使用的本地盘路径。

> **注意：**
>
> 建议 TiDB 的 `temp-dir` 目录至少有 100 GiB 的可用空间。

## 启用步骤

1. 启用分布式执行框架，只需将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 设置为 `ON`。该变量从 v8.1.0 起默认开启，对于新建的 v8.1.0 或更高版本集群，可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    在运行任务时，框架支持的语句（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）会采用分布式方式执行。默认集群内部所有节点均会执行任务。

2. 一般情况下，对于下列影响 DDL 任务分布式执行的系统变量，使用其默认值即可。

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：使用默认值 `4` 即可，建议最大不超过 `16`。
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：使用默认值即可，建议最大不超过 `1024`。

## 任务调度

默认情况下，分布式执行框架将会调度所有 TiDB 节点执行分布式任务。从 v7.4.0 起，你可以通过设置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 来控制分布式执行框架将会调度哪些 TiDB 节点执行分布式任务。

- 在 v7.4.0 到 v8.0.0 及其之间的版本中，[`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 的可选值为 `''` 或 `background`。如果当前集群存在 `tidb_service_scope = 'background'` 的 TiDB 节点，分布式执行框架会将该任务调度到 `tidb_service_scope = 'background'` 的节点上运行。如果当前集群不存在 `tidb_service_scope = 'background'` 的节点，无论是因为故障还是正常的缩容，分布式执行框架会将任务调度到 `tidb_service_scope = ''` 的节点上运行。

- 从 v8.1.0 起，[`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 可设置为任意合法值。当提交分布式任务时，该任务会绑定当前连接的 TiDB 节点的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 值，分布式执行框架只会将该任务调度到具有相同 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 值的 TiDB 节点上运行。但是，为了兼容之前版本的配置，如果分布式任务是在 `tidb_service_scope = ''` 的节点上提交的，且当前集群存在 `tidb_service_scope = 'background'` 的节点，分布式执行框架会将该任务调度到 `tidb_service_scope = 'background'` 的 TiDB 节点上运行。

从 v8.1.0 起，如果在任务运行过程中扩容新节点，分布式执行框架会根据上述规则决定是否将任务调度到新的节点来执行。如果不希望新扩容的节点运行任务，建议提前为这些节点设置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入)。

> **注意：**
>
> - 在 v7.4.0 到 v8.0.0 及其之间的版本中，对于包含多个 TiDB 节点的集群，强烈建议选择两个或更多的 TiDB 节点将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 设置为 `background`。若仅在单个 TiDB 节点上设置此变量，当该节点发生重启或故障时，任务会被重新调度到 `tidb_service_scope = ''` 的 TiDB 节点，会对这些 TiDB 节点的业务产生影响。
> - 在分布式任务执行过程中，修改 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-从-v740-版本开始引入) 的配置不会对当前任务生效，会从下次任务开始生效。

## 实现原理

TiDB 分布式执行框架的架构图如下：

![分布式执行框架的架构](/media/dist-task/dist-task-architect.jpg)

根据上图，分布式执行框架中任务的执行主要由以下模块负责：

- Dispatcher：负责生成每个任务的分布式执行计划，管理执行过程，转换任务状态以及收集和反馈运行时任务信息等。
- Scheduler：以 TiDB 节点为单位来同步分布式任务的执行，提高执行效率。
- Subtask Executor：是实际的分布式子任务执行者，并将子任务的执行情况返回给 Scheduler，由 Scheduler 统一更新子任务的执行状态。
- 资源池：通过对上述各种模块中计算资源进行池化，提供量化资源的使用与管理的基础。

## 另请参阅

* [DDL 执行原理及最佳实践](/ddl-introduction.md)
