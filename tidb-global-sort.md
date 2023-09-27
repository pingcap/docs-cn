---
title: TiDB 全局排序
summary: 了解 TiDB 全局排序功能的使用场景、限制、使用方法和实现原理。
---

# TiDB 全局排序

> **Warning:**
>
> 该功能目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 功能概览

TiDB 全局排序功能增强了数据导入和 DDL（数据定义语言）操作的稳定性和执行效率。全局排序作为[分布式执行框架](/tidb-distributed-execution-framework.md)中的通用算子，通过分布式执行框架，在云上提供全局排序服务。

你可以轻松扩展全局排序来支持多种共享存储接口，例如 S3 和 POSIX，实现与不同存储系统的无缝集成。全局排序功能可以灵活地为各种使用场景提供高效和适配的数据排序服务。

## 目标

全局排序功能旨在提高 `IMPORT INTO` 和 `CREATE INDEX` 的效率。通过将全局排序集成到后端任务中，可以提高稳定性、可控性和可扩展性，提供更好的用户体验和更高质量的服务。

全局排序功能在统一的分布式并行执行框架中执行任务，保证数据在全局范围内的高效并行排序。

## 限制

目前，全局排序功能无法用于查询过程中对查询结果进行排序。

## 使用方法

要开启全局排序功能，执行以下步骤：

1. 将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-从-v710-版本开始引入) 的值设置为 `ON`，开启分布式执行框架：

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

2. 将 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-从-v740-版本开始引入) 设置为正确的云存储路径。参见[示例](/br/backup-and-restore-storages.md)。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

## 实现原理

全局排序功能的算法如下图所示：

![全局排序功能算法](/media/dist-task/global-sort.jpeg)

详细的实现原理如下：

### 第 1 步：扫描和准备数据

1. TiDB 节点扫描特定范围的数据后：

    1. TiDB 节点将扫描的数据编码为 Key-Value 对。
    2. TiDB 节点将 Key-Value 对排序为多个块数据段，每个段是一个文件，并将这些文件上传到云存储中。

2. TiDB 节点记录了每个段的连续实际键值范围（被称为统计信息文件），这是可扩展排序实现的关键准备工作。这些文件随实际数据一起上传到云存储中。

### 第 1 步：排序和分发数据

从第一步中，全局排序的程序获取了一个已排序块的列表及其对应的统计信息文件，这些文件记录了本地已排序块的数量。此外，全局排序程序还记录了一个实际数据范围，可以由 PD 用于拆分和打散。接下来将执行以下步骤：

1. 将统计信息文件中的记录排序，将其分成大小相近的范围，这些范围是将并行执行的子任务。
2. 将子任务分发给 TiDB 节点执行。
3. 每个 TiDB 节点独立地对子任务的数据进行排序，并在没有重叠的情况下将数据导入到 TiKV 中。
