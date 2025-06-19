---
title: 使用 JetBrains DataGrip 连接 TiDB
summary: 了解如何使用 JetBrains DataGrip 连接 TiDB。本教程同样适用于其他 JetBrains IDE（如 IntelliJ、PhpStorm 和 PyCharm）中可用的 Database Tools and SQL 插件。
---

# 使用 JetBrains DataGrip 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html) 是一个功能强大的数据库和 SQL 集成开发环境（IDE）。本教程将指导您使用 DataGrip 连接到 TiDB 集群。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

您可以通过两种方式使用 DataGrip：

- 作为独立工具使用 [DataGrip IDE](https://www.jetbrains.com/datagrip/download)。
- 在 JetBrains IDE（如 IntelliJ、PhpStorm 和 PyCharm）中使用 [Database Tools and SQL 插件](https://www.jetbrains.com/help/idea/relational-databases.html)。

本教程主要关注独立的 DataGrip IDE。使用 JetBrains IDE 中的 Database Tools and SQL 插件连接 TiDB 的步骤类似。当您从任何 JetBrains IDE 连接到 TiDB 时，也可以参考本文档中的步骤。

## 前提条件

要完成本教程，您需要：

- [DataGrip **2023.2.1** 或更高版本](https://www.jetbrains.com/datagrip/download/)或非社区版的 [JetBrains](https://www.jetbrains.com/) IDE。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

## 连接到 TiDB

根据您选择的 TiDB 部署选项连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `DataGrip`
    - **操作系统**与您的环境匹配。

4. 点击**生成密码**创建随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，可以使用原始密码或点击**重置密码**生成新密码。

5. 启动 DataGrip 并创建一个项目来管理您的连接。

    ![在 DataGrip 中创建项目](/media/develop/datagrip-create-project.jpg)

6. 在新创建的项目中，点击**数据库浏览器**面板左上角的 **+**，然后选择**数据源** > **其他** > **TiDB**。

    ![在 DataGrip 中选择数据源](/media/develop/datagrip-data-source-select.jpg)

7. 从 TiDB Cloud 连接对话框复制连接字符串。然后，将其粘贴到 **URL** 字段中，其余参数将自动填充。示例结果如下：

    ![为 TiDB Cloud Serverless 配置 URL 字段](/media/develop/datagrip-url-paste.jpg)

    如果显示**下载缺失的驱动程序文件**警告，点击**下载**获取驱动程序文件。

8. 点击**测试连接**验证与 TiDB Cloud Serverless 集群的连接。

    ![测试与 TiDB Cloud Serverless 集群的连接](/media/develop/datagrip-test-connection.jpg)

9. 点击**确定**保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择 **Public**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**连接类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 DataGrip 并创建一个项目来管理您的连接。

    ![在 DataGrip 中创建项目](/media/develop/datagrip-create-project.jpg)

5. 在新创建的项目中，点击**数据库浏览器**面板左上角的 **+**，然后选择**数据源** > **其他** > **TiDB**。

    ![在 DataGrip 中选择数据源](/media/develop/datagrip-data-source-select.jpg)

6. 将适当的连接字符串复制并粘贴到 DataGrip 的**数据源和驱动程序**窗口中。DataGrip 字段与 TiDB Cloud Dedicated 连接字符串的映射关系如下：

    | DataGrip 字段 | TiDB Cloud Dedicated 连接字符串 |
    | -------------- | ------------------------------- |
    | Host           | `{host}`                        |
    | Port           | `{port}`                        |
    | User           | `{user}`                        |
    | Password       | `{password}`                    |

    示例如下：

    ![为 TiDB Cloud Dedicated 配置连接参数](/media/develop/datagrip-dedicated-connect.jpg)

7. 点击 **SSH/SSL** 标签，选中**使用 SSL** 复选框，并在 **CA 文件**字段中输入 CA 证书路径。

    ![为 TiDB Cloud Dedicated 配置 CA](/media/develop/datagrip-dedicated-ssl.jpg)

    如果显示**下载缺失的驱动程序文件**警告，点击**下载**获取驱动程序文件。

8. 点击**高级**标签，滚动找到 **enabledTLSProtocols** 参数，并将其值设置为 `TLSv1.2,TLSv1.3`。

    ![为 TiDB Cloud Dedicated 配置 TLS](/media/develop/datagrip-dedicated-advanced.jpg)

9. 点击**测试连接**验证与 TiDB Cloud Dedicated 集群的连接。

    ![测试与 TiDB Cloud Dedicated 集群的连接](/media/develop/datagrip-dedicated-test-connection.jpg)

10. 点击**确定**保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 DataGrip 并创建一个项目来管理您的连接。

    ![在 DataGrip 中创建项目](/media/develop/datagrip-create-project.jpg)

2. 在新创建的项目中，点击**数据库浏览器**面板左上角的 **+**，然后选择**数据源** > **其他** > **TiDB**。

    ![在 DataGrip 中选择数据源](/media/develop/datagrip-data-source-select.jpg)

3. 配置以下连接参数：

    - **Host**：您的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **Port**：您的 TiDB Self-Managed 集群的端口号。
    - **User**：用于连接到 TiDB Self-Managed 集群的用户名。
    - **Password**：用户名的密码。

    示例如下：

    ![为 TiDB Self-Managed 配置连接参数](/media/develop/datagrip-self-hosted-connect.jpg)

    如果显示**下载缺失的驱动程序文件**警告，点击**下载**获取驱动程序文件。

4. 点击**测试连接**验证与 TiDB Self-Managed 集群的连接。

    ![测试与 TiDB Self-Managed 集群的连接](/media/develop/datagrip-self-hosted-test-connection.jpg)

5. 点击**确定**保存连接配置。

</div>
</SimpleTab>

## 下一步

- 从 [DataGrip 文档](https://www.jetbrains.com/help/datagrip/getting-started.html)了解更多 DataGrip 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
