---
title: TiDB 全局排序
summary: 了解 TiDB 全局排序的使用场景、限制、用法和实现原理。
---

<!-- markdownlint-disable MD029 -->
<!-- markdownlint-disable MD046 -->

# TiDB 全局排序

> **注意：**
>
> - 目前，全局排序过程会消耗 TiDB 节点大量的计算和内存资源。在用户业务应用运行的同时进行在线添加索引等场景时，建议向集群添加新的 TiDB 节点，为这些节点配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 变量，并连接到这些节点创建任务。这样，分布式框架会将任务调度到这些节点，将工作负载与其他 TiDB 节点隔离，以减少执行 `ADD INDEX` 和 `IMPORT INTO` 等后台任务对用户业务应用的影响。
> - 使用全局排序功能时，建议使用至少 16 核 CPU 和 32 GiB 内存的 TiDB 节点，以避免 OOM。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概述

TiDB 全局排序功能增强了数据导入和 DDL（数据定义语言）操作的稳定性和效率。它作为 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 中的通用算子，提供云上的全局排序服务。

目前，全局排序功能支持使用 Amazon S3 作为云存储。

## 使用场景

全局排序功能增强了 `IMPORT INTO` 和 `CREATE INDEX` 的稳定性和效率。通过对任务处理的数据进行全局排序，它提高了向 TiKV 写入数据的稳定性、可控性和可扩展性。这为数据导入和 DDL 任务提供了更好的用户体验，以及更高质量的服务。

全局排序功能在统一的 DXF 中执行任务，确保在全局范围内高效并行地对数据进行排序。

## 限制

目前，全局排序功能不作为负责排序查询结果的查询执行过程的组件。

## 用法

要启用全局排序，请按照以下步骤操作：

1. 通过将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 的值设置为 `ON` 来启用 DXF。从 v8.1.0 开始，此变量默认启用。对于 v8.1.0 或更高版本的新创建集群，可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

<CustomContent platform="tidb">

2. 将 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 设置为正确的云存储路径。参见[示例](/br/backup-and-restore-storages.md)。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>
<CustomContent platform="tidb-cloud">

2. 将 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 设置为正确的云存储路径。参见[示例](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>

> **注意：**
>
> 对于 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)，你也可以使用 [`CLOUD_STORAGE_URI`](/sql-statements/sql-statement-import-into.md#withoptions) 选项指定云存储路径。如果 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 和 `CLOUD_STORAGE_URI` 都配置了有效的云存储路径，则对于 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)，`CLOUD_STORAGE_URI` 的配置会生效。

## 实现原理

全局排序功能的算法如下：

![全局排序算法](/media/dist-task/global-sort.jpeg)

详细的实现原理如下：

### 步骤 1：扫描和准备数据

1. TiDB 节点扫描特定范围的数据（数据源可以是 CSV 数据或 TiKV 中的表数据）后：

    1. TiDB 节点将它们编码为键值对。
    2. TiDB 节点将键值对排序成几个块数据段（数据段是本地排序的），每个段是一个文件并上传到云存储中。

2. TiDB 节点还记录每个段的一系列实际键值范围（称为统计文件），这是实现可扩展排序的关键准备。这些文件随后与实际数据一起上传到云存储中。

### 步骤 2：排序和分发数据

从步骤 1 中，全局排序程序获取已排序块的列表及其对应的统计文件，这些文件提供了本地排序块的数量。程序还有一个可供 PD 用于拆分和分散的实际数据范围。执行以下步骤：

1. 对统计文件中的记录进行排序，将它们划分为大小几乎相等的范围，这些范围是将并行执行的子任务。
2. 将子任务分发给 TiDB 节点执行。
3. 每个 TiDB 节点独立地将子任务的数据排序成范围，并且无重叠地将它们写入 TiKV。
