---
title: TiFlash Pipeline Execution Model
summary: Learn about the TiFlash Pipeline Execution Model.
---

# TiFlash Pipeline Execution Model

This document introduces the TiFlash pipeline execution model.

Starting from v7.2.0, TiFlash supports a new execution model, the pipeline execution model. You can control whether to enable the TiFlash pipeline execution model by modifying the system variable [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720).

Inspired by the paper [Morsel-Driven Parallelism: A NUMA-Aware Query Evaluation Framework for the Many-Core Age](https://dl.acm.org/doi/10.1145/2588555.2610507), the TiFlash pipeline execution model provides a fine-grained task scheduling model, which is different from the traditional thread scheduling model. It reduces the overhead of operating system thread scheduling and provides a fine-grained scheduling mechanism.

> **Note:**
>
> - The pipeline execution model is currently an experimental feature and is not recommended to use in production environments.
> - The pipeline execution model does not support the following features. When the following features are enabled, even if `tidb_enable_tiflash_pipeline_model` is set to `ON`, the query pushed down to TiFlash will still be executed using the original stream model.
>
>     - [Join operator spill to disk](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
>     - [TiFlash Disaggregated Storage and Compute Architecture and S3 Support](/tiflash/tiflash-disaggregated-and-s3.md)

## Enable and disable the pipeline execution model

To enable or disable the pipeline execution model, you can use the [`tidb_enable_tiflash_pipeline_model`](/system-variables.md#tidb_enable_tiflash_pipeline_model-new-in-v720) system variable. This variable can take effect at the session level and global level. By default, `tidb_enable_tiflash_pipeline_model` is set to `OFF`, which means that the TiFlash pipeline execution model is disabled. You can use the following statement to view the variable value:

```sql
SHOW VARIABLES LIKE 'tidb_enable_tiflash_pipeline_model';
```

```
+------------------------------------+-------+
| Variable_name                      | Value |
+------------------------------------+-------+
| tidb_enable_tiflash_pipeline_model | OFF   |
+------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_enable_tiflash_pipeline_model';
```

```
+------------------------------------+-------+
| Variable_name                      | Value |
+------------------------------------+-------+
| tidb_enable_tiflash_pipeline_model | OFF   |
+------------------------------------+-------+
```

You can modify the `tidb_enable_tiflash_pipeline_model` variable at the session level and global level.

- To enable the pipeline execution model in the current session, use the following statement:

    ```sql
    SET SESSION tidb_enable_tiflash_pipeline_model=ON;
    ```

- To enable the pipeline execution model at the global level, use the following statement:

    ```sql
    SET GLOBAL tidb_enable_tiflash_pipeline_model=ON;
    ```

    If you set `tidb_enable_tiflash_pipeline_model` to `ON` at the global level, the `tidb_enable_tiflash_pipeline_model` variable at the session level and global level in the new session will be enabled by default.

To disable the pipeline execution model, use the following statement:

```sql
SET SESSION tidb_enable_tiflash_pipeline_model=OFF;
```

```sql
SET GLOBAL tidb_enable_tiflash_pipeline_model=OFF;
```

## Design and implementation

The original TiFlash stream model is a thread scheduling execution model. Each query independently applies for several threads to execute in coordination.

The thread scheduling model has the following two defects:

- In high-concurrency scenarios, too many threads cause a large number of context switches, resulting in high thread scheduling costs.
- The thread scheduling model cannot accurately measure the resource usage of queries or do fine-grained resource control.

The new pipeline execution model makes the following optimizations:

- The queries are divided into multiple pipelines and executed in sequence. In each pipeline, the data blocks are kept in the cache as much as possible to achieve better temporal locality and improve the efficiency of the entire execution process.
- To get rid of the native thread scheduling model of the operating system and implement a more fine-grained scheduling mechanism, each pipeline is instantiated into several tasks and uses the task scheduling model. At the same time, a fixed thread pool is used to reduce the overhead of operating system thread scheduling.

The architecture of the pipeline execution model is as follows:

![TiFlash pipeline execution model design](/media/tiflash/tiflash-pipeline-model.png)

As shown in the preceding figure, the pipeline execution model consists of two main components: the pipeline query executor and the task scheduler.

- The pipeline query executor

    The pipeline query executor converts the query request sent from the TiDB node into a pipeline directed acyclic graph (DAG).

    It will find the pipeline breaker operators in the query and split the query into several pipelines according to the pipeline breakers. Then, it assembles the pipelines into a DAG according to the dependency relationship between the pipelines.

    A pipeline breaker is an operator that has a pause/blocking logic. This type of operator continuously receives data blocks from the upstream operator until all data blocks are received, and then return the processing result to the downstream operator. This type of operator breaks the data processing pipeline, so it is called a pipeline breaker. One of the pipeline breakers is the Aggregation operator, which writes all the data of the upstream operator into a hash table before calculating the data in the hash table and returning the result to the downstream operator.

    After the query is converted into a pipeline DAG, the pipeline query executor executes each pipeline in sequence according to the dependency relationship. The pipeline is instantiated into several tasks according to the query concurrency and submitted to the task scheduler for execution.

- Task scheduler

    The task scheduler executes the tasks submitted by the pipeline query executor. The tasks are dynamically switched between different components in the task scheduler according to the different execution logic.

    - CPU task thread pool

        Executes the CPU-intensive calculation logic in the task, such as data filtering and function calculation.

    - IO task thread pool

        Executes the IO-intensive calculation logic in the task, such as writing intermediate results to disk.

    - Wait reactor

        Executes the wait logic in the task, such as waiting for the network layer to transfer the data packet to the calculation layer.
