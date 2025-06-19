---
title: 使用 DBeaver 连接 TiDB
summary: 了解如何使用 DBeaver Community 连接 TiDB。
---

# 使用 DBeaver 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [DBeaver Community](https://dbeaver.io/download/) 是一个免费的跨平台数据库工具，适用于开发人员、数据库管理员、分析师以及所有处理数据的人员。

在本教程中，您将学习如何使用 DBeaver Community 连接到您的 TiDB 集群。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- [DBeaver Community **23.0.3** 或更高版本](https://dbeaver.io/download/)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 连接到 TiDB

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与您的操作环境相匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `DBeaver`
    - **操作系统**与您的环境匹配。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

5. 启动 DBeaver 并点击左上角的**新建数据库连接**。在**连接到数据库**对话框中，从列表中选择 **TiDB**，然后点击**下一步**。

    ![在 DBeaver 中选择 TiDB 作为数据库](/media/develop/dbeaver-select-database.jpg)

6. 从 TiDB Cloud 连接对话框中复制连接字符串。在 DBeaver 中，选择 **URL** 作为**连接方式**，并将连接字符串粘贴到 **URL** 字段中。

7. 在**身份验证（数据库原生）**部分，输入您的**用户名**和**密码**。示例如下：

    ![配置 TiDB Cloud Serverless 的连接设置](/media/develop/dbeaver-connection-settings-serverless.jpg)

8. 点击**测试连接**以验证与 TiDB Cloud Serverless 集群的连接。

    如果显示**下载驱动程序文件**对话框，点击**下载**获取驱动程序文件。

    ![下载驱动程序文件](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，将显示如下的**连接测试**对话框。点击**确定**关闭它。

    ![连接测试结果](/media/develop/dbeaver-connection-test.jpg)

9. 点击**完成**保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**连接类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 DBeaver 并点击左上角的**新建数据库连接**。在**连接到数据库**对话框中，从列表中选择 **TiDB**，然后点击**下一步**。

    ![在 DBeaver 中选择 TiDB 作为数据库](/media/develop/dbeaver-select-database.jpg)

5. 将适当的连接字符串复制并粘贴到 DBeaver 连接面板中。DBeaver 字段与 TiDB Cloud Dedicated 连接字符串的映射关系如下：

    | DBeaver 字段 | TiDB Cloud Dedicated 连接字符串 |
    |---------------| ------------------------------- |
    | 服务器主机    | `{host}`                        |
    | 端口         | `{port}`                        |
    | 用户名       | `{user}`                        |
    | 密码         | `{password}`                    |

    示例如下：

    ![配置 TiDB Cloud Dedicated 的连接设置](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6. 点击**测试连接**以验证与 TiDB Cloud Dedicated 集群的连接。

    如果显示**下载驱动程序文件**对话框，点击**下载**获取驱动程序文件。

    ![下载驱动程序文件](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，将显示如下的**连接测试**对话框。点击**确定**关闭它。

    ![连接测试结果](/media/develop/dbeaver-connection-test.jpg)

7. 点击**完成**保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 DBeaver 并点击左上角的**新建数据库连接**。在**连接到数据库**对话框中，从列表中选择 **TiDB**，然后点击**下一步**。

    ![在 DBeaver 中选择 TiDB 作为数据库](/media/develop/dbeaver-select-database.jpg)

2. 配置以下连接参数：

    - **服务器主机**：您的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **端口**：您的 TiDB Self-Managed 集群的端口号。
    - **用户名**：用于连接到您的 TiDB Self-Managed 集群的用户名。
    - **密码**：该用户名的密码。

    示例如下：

    ![配置 TiDB Self-Managed 的连接设置](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3. 点击**测试连接**以验证与 TiDB Self-Managed 集群的连接。

    如果显示**下载驱动程序文件**对话框，点击**下载**获取驱动程序文件。

    ![下载驱动程序文件](/media/develop/dbeaver-download-driver.jpg)

    如果连接测试成功，将显示如下的**连接测试**对话框。点击**确定**关闭它。

    ![连接测试结果](/media/develop/dbeaver-connection-test.jpg)

4. 点击**完成**保存连接配置。

</div>
</SimpleTab>

## 下一步

- 从 [DBeaver 的文档](https://github.com/dbeaver/dbeaver/wiki)了解更多 DBeaver 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
