---
title: 监控 TiDB 集群
summary: 了解如何监控 TiDB 集群。
---

# 监控 TiDB 集群

本文档介绍如何在 TiDB Cloud 上监控 TiDB 集群。

## 集群状态和节点状态

您可以在集群页面上查看每个运行中集群的当前状态。

### 集群状态

| 集群状态 | 描述 |
|:--|:--|
| **Available** | 集群运行正常且可用。 |
| **Creating** | 集群正在创建中。在创建过程中集群不可访问。 |
| **Importing** | 正在向集群导入数据。 |
| **Maintaining** | 集群正在维护中。 |
| **Modifying** | 集群正在修改中。 |
| **Unavailable** | 集群发生故障且 TiDB 无法恢复。 |
| **Pausing** | 集群正在暂停中。 |
| **Paused** | 集群已暂停。 |
| **Resuming** | 集群正在从暂停状态恢复。 |
| **Restoring** | 集群当前正在从备份中恢复。 |

### TiDB 节点状态

> **注意：**
>
> TiDB 节点状态仅适用于 TiDB Cloud Dedicated 集群。

| TiDB 节点状态 | 描述 |
|:--|:--|
| **Available** | TiDB 节点运行正常且可用。 |
| **Creating** | TiDB 节点正在创建中。 |
| **Unavailable** | TiDB 节点不可用。 |
| **Deleting** | TiDB 节点正在删除中。 |

### TiKV 节点状态

> **注意：**
>
> TiKV 节点状态仅适用于 TiDB Cloud Dedicated 集群。

| TiKV 节点状态 | 描述 |
|:--|:--|
| **Available** | TiKV 节点运行正常且可用。 |
| **Creating** | TiKV 节点正在创建中。 |
| **Unavailable** | TiKV 节点不可用。 |
| **Deleting** | TiKV 节点正在删除中。 |

## 监控指标

在 TiDB Cloud 中，您可以从以下页面查看集群的常用指标：

- **概览**页面
- **指标**页面

### 概览页面

**概览**页面提供集群的常规指标。

要在集群概览页面查看指标，请执行以下步骤：

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面。

    > **提示：**
    >
    > 您可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 查看**核心指标**部分。

### 指标页面

**指标**页面提供集群的完整指标集。通过查看这些指标，您可以轻松识别性能问题并确定当前的数据库部署是否满足您的需求。

要在**指标**页面查看指标，请执行以下步骤：

1. 在项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群的名称以进入其概览页面。

    > **提示：**
    >
    > 您可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏中，点击**监控** > **指标**。

更多信息，请参见 [TiDB Cloud 内置指标](/tidb-cloud/built-in-monitoring.md)。
