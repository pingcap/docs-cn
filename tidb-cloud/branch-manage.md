---
title: 管理 TiDB Cloud Serverless 分支
summary: 了解如何管理 TiDB Cloud Serverless 分支。
---

# 管理 TiDB Cloud Serverless 分支

本文档介绍如何使用 [TiDB Cloud 控制台](https://tidbcloud.com) 管理 TiDB Cloud Serverless 分支。如需使用 TiDB Cloud CLI 进行管理，请参阅 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)。

## 所需权限

- 要[创建分支](#创建分支)或[连接到分支](#连接到分支)，你必须具有组织的 `Organization Owner` 角色或目标项目的 `Project Owner` 角色。
- 要[查看项目中集群的分支](#查看分支)，你必须属于该项目。

有关权限的更多信息，请参阅[用户角色](/tidb-cloud/manage-user-access.md#user-roles)。

## 创建分支

> **注意：**
>
> 你只能为 2023 年 7 月 5 日之后创建的 TiDB Cloud Serverless 集群创建分支。更多限制请参阅[限制和配额](/tidb-cloud/branch-overview.md#limitations-and-quotas)。

要创建分支，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 在左侧导航栏中点击**分支**。
3. 在**分支**页面的右上角，点击**创建分支**。此时会显示一个对话框。

    或者，要从现有父分支创建分支，找到目标父分支所在的行，然后在**操作**列中点击 **...** > **创建分支**。

4. 在**创建分支**对话框中，配置以下选项：

    - **名称**：输入分支的名称。
    - **父分支**：选择原始集群或现有分支。`main` 代表当前集群。
    - **包含数据截至**：选择以下其中一项：
        - **当前时间点**：从当前状态创建分支。
        - **指定日期和时间**：从指定时间创建分支。

5. 点击**创建**。

根据集群中的数据大小，分支创建将在几分钟内完成。

## 查看分支

要查看集群的分支，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 在左侧导航栏中点击**分支**。

    集群的分支列表将显示在右侧窗格中。

## 连接到分支

要连接到分支，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 在左侧导航栏中点击**分支**。
3. 在要连接的目标分支所在行中，点击**操作**列中的 **...**。
4. 在下拉列表中点击**连接**。此时会显示连接信息对话框。
5. 点击**生成密码**或**重置密码**以创建或重置 root 密码。
6. 使用连接信息连接到分支。

或者，你也可以从集群概览页面获取连接字符串：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 点击右上角的**连接**。
3. 在`分支`下拉列表中选择要连接的分支。
4. 点击**生成密码**或**重置密码**以创建或重置 root 密码。
5. 使用连接信息连接到分支。

## 删除分支

要删除分支，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 在左侧导航栏中点击**分支**。
3. 在要删除的目标分支所在行中，点击**操作**列中的 **...**。
4. 在下拉列表中点击**删除**。
5. 确认删除。

## 重置分支

重置分支会将其与父分支的最新数据同步。

> **注意：**
> 
> 此操作不可逆。在重置分支之前，请确保已备份任何重要数据。

要重置分支，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称以进入其概览页面。
2. 在左侧导航栏中点击**分支**。
3. 在要重置的目标分支所在行中，点击**操作**列中的 **...**。
4. 在下拉列表中点击**重置**。
5. 确认重置。

## 下一步

- [将 TiDB Cloud Serverless 分支集成到 GitHub CI/CD 流程中](/tidb-cloud/branch-github-integration.md)
