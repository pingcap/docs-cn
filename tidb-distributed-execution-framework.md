---
title: TiDB Distributed eXecution Framework (DXF)
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Distributed eXecution Framework (DXF).
---

# TiDB Distributed eXecution Framework (DXF)

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

TiDB adopts a computing-storage separation architecture with excellent scalability and elasticity. Starting from v7.1.0, TiDB introduces a Distributed eXecution Framework (DXF) to further leverage the resource advantages of the distributed architecture. The goal of the DXF is to implement unified scheduling and distributed execution of tasks, and to provide unified resource management capabilities for both overall and individual tasks, which better meets users' expectations for resource usage.

This document describes the use cases, limitations, usage, and implementation principles of the DXF.

## Use cases

In a database management system, in addition to the core transactional processing (TP) and analytical processing (AP) workloads, there are other important tasks, such as DDL operations, IMPORT INTO, TTL, Analyze, and Backup/Restore. These tasks need to process a large amount of data in database objects (tables), so they typically have the following characteristics:

- Need to process all data in a schema or a database object (table).
- Might need to be executed periodically, but at a low frequency.
- If the resources are not properly controlled, they are prone to affect TP and AP tasks, lowering the database service quality.

Enabling the DXF can solve the above problems and has the following three advantages:

- The framework provides unified capabilities for high scalability, high availability, and high performance.
- The DXF supports distributed execution of tasks, which can flexibly schedule the available computing resources of the entire TiDB cluster, thereby better utilizing the computing resources in a TiDB cluster.
- The DXF provides unified resource usage and management capabilities for both overall and individual tasks.

Currently, the DXF supports the distributed execution of the `ADD INDEX` and `IMPORT INTO` statements.

- `ADD INDEX` is a DDL statement used to create indexes. For example:

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- `IMPORT INTO` is used to import data in formats such as `CSV`, `SQL`, and `PARQUET` into an empty table. For more information, see [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md).

## Limitation

- The DXF can only schedule the distributed execution of one `ADD INDEX` task at a time. If a new `ADD INDEX` task is submitted before the current `ADD INDEX` distributed task has finished, the new task is executed through a transaction.
- Adding indexes on columns with the `TIMESTAMP` data type through the DXF is not supported, because it might lead to inconsistency between the index and the data.

## Prerequisites

Before using the DXF to execute `ADD INDEX` tasks, you need to enable the [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) mode.

<CustomContent platform="tidb">

1. Adjust the following system variables related to Fast Online DDL:

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

2. Adjust the following configuration item related to Fast Online DDL:

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630): specifies the local disk path that can be used in Fast Online DDL mode.

> **Note:**
>
> It is recommended that you prepare at least 100 GiB of free space for the TiDB `temp-dir` directory.

</CustomContent>

<CustomContent platform="tidb-cloud">

Adjust the following system variables related to Fast Online DDL:

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

</CustomContent>

## Usage

1. To enable the DXF, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    When the DXF tasks are running, the statements supported by the framework (such as [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)) are executed in a distributed manner. All TiDB nodes run DXF tasks by default.

2. In general, for the following system variables that might affect the distributed execution of DDL tasks, it is recommended that you use their default values:

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt): use the default value `4`. The recommended maximum value is `16`.
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size): use the default value. The recommended maximum value is `1024`.

3. Starting from v7.4.0, for TiDB Self-Hosted, you can adjust the number of TiDB nodes that perform the DXF tasks according to actual needs. After deploying a TiDB cluster, you can set the instance-level system variable [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) for each TiDB node in the cluster. When `tidb_service_scope` of a TiDB node is set to `background`, the TiDB node can execute the DXF tasks. When `tidb_service_scope` of a TiDB node is set to the default value "", the TiDB node cannot execute the DXF tasks. If `tidb_service_scope` is not set for any TiDB node in a cluster, the DXF schedules all TiDB nodes to execute tasks by default.

    > **Note:**
    >
    > - In a cluster with several TiDB nodes, it is strongly recommended to set `tidb_service_scope` to `background` on two or more TiDB nodes. If `tidb_service_scope` is set on a single TiDB node only, when the node is restarted or fails, the task will be rescheduled to other TiDB nodes that lack the `background` setting, which will affect these TiDB nodes.
    > - During the execution of a distributed task, changes to the `tidb_service_scope` configuration will not take effect for the current task, but will take effect from the next task.

## Implementation principles

The architecture of the DXF is as follows:

![Architecture of the DXF](/media/dist-task/dist-task-architect.jpg)

As shown in the preceding diagram, the execution of tasks in the DXF is mainly handled by the following modules:

- Dispatcher: generates the distributed execution plan for each task, manages the execution process, converts the task status, and collects and feeds back the runtime task information.
- Scheduler: replicates the execution of distributed tasks among TiDB nodes to improve the efficiency of task execution.
- Subtask Executor: the actual executor of distributed subtasks. In addition, the Subtask Executor returns the execution status of subtasks to the Scheduler, and the Scheduler updates the execution status of subtasks in a unified manner.
- Resource pool: provides the basis for quantifying resource usage and management by pooling computing resources of the above modules.

## See also

<CustomContent platform="tidb">

* [Execution Principles and Best Practices of DDL Statements](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [Execution Principles and Best Practices of DDL Statements](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>
