---
title: 使用 MySQL Workbench 连接 TiDB
summary: 了解如何使用 MySQL Workbench 连接 TiDB。
---

# 使用 MySQL Workbench 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [MySQL Workbench](https://www.mysql.com/products/workbench/) 是一个面向 MySQL 数据库用户的 GUI 工具集。

> **警告：**
>
> - 虽然由于 TiDB 的 MySQL 兼容性，您可以使用 MySQL Workbench 连接到 TiDB，但 MySQL Workbench 并不完全支持 TiDB。由于它将 TiDB 视为 MySQL，在使用过程中可能会遇到一些问题。
> - 建议使用其他官方支持 TiDB 的 GUI 工具，如 [DataGrip](/develop/dev-guide-gui-datagrip.md)、[DBeaver](/develop/dev-guide-gui-dbeaver.md) 和 [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)。有关 TiDB 完全支持的 GUI 工具的完整列表，请参见[TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md#gui)。

在本教程中，您可以学习如何使用 MySQL Workbench 连接到您的 TiDB 集群。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** 或更高版本。
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

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接工具**设置为 `MySQL Workbench`。
    - **操作系统**与您的环境匹配。

4. 点击**生成密码**创建随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码或点击**重置密码**生成新密码。

5. 启动 MySQL Workbench，点击 **MySQL 连接**标题附近的 **+**。

    ![MySQL Workbench：添加新连接](/media/develop/mysql-workbench-add-new-connection.png)

6. 在**设置新连接**对话框中，配置以下连接参数：

    - **连接名称**：为此连接指定一个有意义的名称。
    - **主机名**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **端口**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **用户名**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **密码**：点击**存储在钥匙串中...**或**存储在保管库中**，输入 TiDB Cloud Serverless 集群的密码，然后点击**确定**存储密码。

        ![MySQL Workbench：在钥匙串中存储 TiDB Cloud Serverless 的密码](/media/develop/mysql-workbench-store-password-in-keychain.png)

    以下图片显示了连接参数的示例：

    ![MySQL Workbench：为 TiDB Cloud Serverless 配置连接设置](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. 点击**测试连接**验证与 TiDB Cloud Serverless 集群的连接。

8. 如果连接测试成功，您会看到**成功建立 MySQL 连接**消息。点击**确定**保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请在首次连接之前点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 MySQL Workbench，点击 **MySQL 连接**标题附近的 **+**。

    ![MySQL Workbench：添加新连接](/media/develop/mysql-workbench-add-new-connection.png)

5. 在**设置新连接**对话框中，配置以下连接参数：

    - **连接名称**：为此连接指定一个有意义的名称。
    - **主机名**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **端口**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **用户名**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **密码**：点击**存储在钥匙串中...**，输入 TiDB Cloud Dedicated 集群的密码，然后点击**确定**存储密码。

        ![MySQL Workbench：在钥匙串中存储 TiDB Cloud Dedicated 的密码](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    以下图片显示了连接参数的示例：

    ![MySQL Workbench：为 TiDB Cloud Dedicated 配置连接设置](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. 点击**测试连接**验证与 TiDB Cloud Dedicated 集群的连接。

7. 如果连接测试成功，您会看到**成功建立 MySQL 连接**消息。点击**确定**保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 MySQL Workbench，点击 **MySQL 连接**标题附近的 **+**。

    ![MySQL Workbench：添加新连接](/media/develop/mysql-workbench-add-new-connection.png)

2. 在**设置新连接**对话框中，配置以下连接参数：

    - **连接名称**：为此连接指定一个有意义的名称。
    - **主机名**：输入您的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **端口**：输入您的 TiDB Self-Managed 集群的端口号。
    - **用户名**：输入用于连接 TiDB 的用户名。
    - **密码**：点击**存储在钥匙串中...**，输入用于连接 TiDB 集群的密码，然后点击**确定**存储密码。

        ![MySQL Workbench：在钥匙串中存储 TiDB Self-Managed 的密码](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    以下图片显示了连接参数的示例：

    ![MySQL Workbench：为 TiDB Self-Managed 配置连接设置](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. 点击**测试连接**验证与 TiDB Self-Managed 集群的连接。

4. 如果连接测试成功，您会看到**成功建立 MySQL 连接**消息。点击**确定**保存连接配置。

</div>
</SimpleTab>

## 常见问题

### 如何处理连接超时错误"错误代码：2013。在查询期间与 MySQL 服务器的连接丢失"？

此错误表示查询执行时间超过了超时限制。要解决此问题，您可以通过以下步骤调整超时设置：

1. 启动 MySQL Workbench 并导航到**工作台首选项**页面。
2. 在 **SQL 编辑器** > **MySQL 会话**部分，配置 **DBMS 连接读取超时间隔（秒）**选项。这设置了查询在 MySQL Workbench 与服务器断开连接之前可以花费的最长时间（以秒为单位）。

    ![MySQL Workbench：在 SQL 编辑器设置中调整超时选项](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

更多信息，请参见 [MySQL Workbench 常见问题](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)。

## 下一步

- 从 [MySQL Workbench 文档](https://dev.mysql.com/doc/workbench/en/)了解更多 MySQL Workbench 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
