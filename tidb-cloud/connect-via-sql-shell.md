---
title: 通过 SQL Shell 连接
summary: 了解如何通过 SQL Shell 连接到您的 TiDB 集群。
---

# 通过 SQL Shell 连接

在 TiDB Cloud SQL Shell 中，您可以尝试 TiDB SQL，快速测试 TiDB 与 MySQL 的兼容性，并管理数据库用户权限。

> **注意：**
>
> 您不能使用 SQL Shell 连接到 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。要连接到您的 TiDB Cloud Serverless 集群，请参见[连接到 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。

要使用 SQL shell 连接到您的 TiDB 集群，请执行以下步骤：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 您可以使用左上角的组合框在组织、项目和集群之间切换。

2. 点击目标集群的名称进入其集群概览页面，然后在左侧导航栏中点击**设置** > **网络**。
3. 在**网络**页面上，点击右上角的 **Web SQL Shell**。
4. 在提示的**输入密码**行中，输入当前集群的 root 密码。然后您的应用程序就连接到了 TiDB 集群。
