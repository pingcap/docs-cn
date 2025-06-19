---
title: TiDB Cloud 集群事件
summary: 了解如何使用事件页面查看 TiDB Cloud 集群的事件。
---

# TiDB Cloud 集群事件

TiDB Cloud 会在集群层面记录历史事件。*事件*表示 TiDB Cloud 集群中的一个变更。你可以在**事件**页面查看已记录的事件，包括事件类型、状态、消息、触发时间和触发用户。

本文档介绍如何使用**事件**页面查看 TiDB Cloud 集群的事件，并列出支持的事件类型。

## 查看事件页面

要在**事件**页面查看事件，请按照以下步骤操作：

1. 在项目的 [**集群**](https://tidbcloud.com/project/clusters) 页面，点击目标集群的名称以进入其概览页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在左侧导航栏中，点击**监控** > **事件**。

## 已记录的事件

TiDB Cloud 记录以下类型的集群事件：

| 事件类型 | 描述 |
|:--- |:--- |
| CreateCluster | 创建集群 |
| PauseCluster | 暂停集群 |
| ResumeCluster | 恢复集群 |
| ModifyClusterSize | 修改集群大小 |
| BackupCluster | 备份集群 |
| ExportBackup | 导出备份 |
| RestoreFromCluster | 恢复集群 |
| CreateChangefeed | 创建 changefeed |
| PauseChangefeed | 暂停 changefeed |
| ResumeChangefeed | 恢复 changefeed |
| DeleteChangefeed | 删除 changefeed |
| EditChangefeed | 编辑 changefeed |
| ScaleChangefeed | 调整 changefeed 规格 |
| FailedChangefeed | Changefeed 失败 |
| ImportData | 向集群导入数据 |
| UpdateSpendingLimit | 更新 TiDB Cloud Serverless 可扩展集群的支出限制 |
| ResourceLimitation | 更新 TiDB Cloud Serverless 集群的资源限制 |

对于每个事件，会记录以下信息：

- 事件类型
- 状态
- 消息
- 时间
- 触发者

## 事件保留策略

事件数据保留 7 天。
