---
title: 使用 Visual Studio Code 连接 TiDB
summary: 了解如何使用 Visual Studio Code 或 GitHub Codespaces 连接 TiDB。
---

# 使用 Visual Studio Code 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [Visual Studio Code (VS Code)](https://code.visualstudio.com/) 是一个轻量级但功能强大的源代码编辑器。本教程使用 [SQLTools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) 扩展，该扩展将 TiDB 作为[官方驱动程序](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql)支持。

在本教程中，您将学习如何使用 Visual Studio Code 连接到您的 TiDB 集群。

> **注意：**
>
> - 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。
> - 本教程也适用于 Visual Studio Code 远程开发环境，如 [GitHub Codespaces](https://github.com/features/codespaces)、[Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) 和 [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl)。

## 前提条件

要完成本教程，您需要：

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) **1.72.0** 或更高版本。
- Visual Studio Code 的 [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 扩展。要安装它，您可以使用以下方法之一：
    - 点击<a href="vscode:extension/mtxr.sqltools-driver-mysql">此链接</a>直接启动 VS Code 并安装扩展。
    - 导航到 [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) 并点击**安装**。
    - 在 VS Code 的**扩展**标签页中，搜索 `mtxr.sqltools-driver-mysql` 找到 **SQLTools MySQL/MariaDB/TiDB** 扩展，然后点击**安装**。
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

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接方式**设置为 `VS Code`。
    - **操作系统**与您的环境匹配。

    > **提示：**
    >
    > 如果您的 VS Code 运行在远程开发环境中，请从列表中选择远程操作系统。例如，如果您使用的是 Windows Subsystem for Linux (WSL)，请切换到相应的 Linux 发行版。如果您使用的是 GitHub Codespaces，则无需这样做。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

5. 启动 VS Code 并在导航窗格中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分下，点击 **Add New Connection** 并选择 **TiDB** 作为数据库驱动程序。

    ![VS Code SQLTools：添加新连接](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. 在设置窗格中，配置以下连接参数：

    - **Connection name**：为此连接指定一个有意义的名称。
    - **Connection group**：（可选）为此连接组指定一个有意义的名称。具有相同组名的连接将被分组在一起。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **Database**：输入要连接的数据库。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Enabled**。TiDB Cloud Serverless 需要安全连接。在 **SSL Options (node.TLSSocket)** 区域，将 **Certificate Authority (CA) Certificate File** 字段配置为 TiDB Cloud 连接对话框中的 `CA` 参数。

            > **注意：**
            >
            > 如果您在 Windows 或 GitHub Codespaces 上运行，可以将 **SSL** 留空。默认情况下，SQLTools 信任由 Let's Encrypt 策划的知名 CA。更多信息，请参见 [TiDB Cloud Serverless 根证书管理](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)。

    ![VS Code SQLTools：配置 TiDB Cloud Serverless 的连接设置](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. 点击 **TEST CONNECTION** 以验证与 TiDB Cloud Serverless 集群的连接。

    1. 在弹出窗口中，点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入您在步骤 4 中创建的密码。

        ![VS Code SQLTools：输入密码连接到 TiDB Cloud Serverless](/media/develop/vsc-sqltools-password.jpg)

8. 如果连接测试成功，您会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**连接类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 启动 VS Code 并在导航窗格中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分下，点击 **Add New Connection** 并选择 **TiDB** 作为数据库驱动程序。

    ![VS Code SQLTools：添加新连接](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. 在设置窗格中，配置以下连接参数：

    - **Connection name**：为此连接指定一个有意义的名称。
    - **Connection group**：（可选）为此连接组指定一个有意义的名称。具有相同组名的连接将被分组在一起。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入 TiDB Cloud 连接对话框中的 `host` 参数。
    - **Port**：输入 TiDB Cloud 连接对话框中的 `port` 参数。
    - **Database**：输入要连接的数据库。
    - **Username**：输入 TiDB Cloud 连接对话框中的 `user` 参数。
    - **Password mode**：选择 **SQLTools Driver Credentials**。
    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools：配置 TiDB Cloud Dedicated 的连接设置](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. 点击 **TEST CONNECTION** 以验证与 TiDB Cloud Dedicated 集群的连接。

    1. 在弹出窗口中，点击 **Allow**。
    2. 在 **SQLTools Driver Credentials** 对话框中，输入 TiDB Cloud Dedicated 集群的密码。

    ![VS Code SQLTools：输入密码连接到 TiDB Cloud Dedicated](/media/develop/vsc-sqltools-password.jpg)

7. 如果连接测试成功，您会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 VS Code 并在导航窗格中选择 **SQLTools** 扩展。在 **CONNECTIONS** 部分下，点击 **Add New Connection** 并选择 **TiDB** 作为数据库驱动程序。

    ![VS Code SQLTools：添加新连接](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. 在设置窗格中，配置以下连接参数：

    - **Connection name**：为此连接指定一个有意义的名称。
    - **Connection group**：（可选）为此连接组指定一个有意义的名称。具有相同组名的连接将被分组在一起。
    - **Connect using**：选择 **Server and Port**。
    - **Server Address**：输入您的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **Port**：输入您的 TiDB Self-Managed 集群的端口号。
    - **Database**：输入要连接的数据库。
    - **Username**：输入用于连接到您的 TiDB Self-Managed 集群的用户名。
    - **Password mode**：

        - 如果密码为空，选择 **Use empty password**。
        - 否则，选择 **SQLTools Driver Credentials**。

    - 在 **MySQL driver specific options** 区域，配置以下参数：

        - **Authentication Protocol**：选择 **default**。
        - **SSL**：选择 **Disabled**。

    ![VS Code SQLTools：配置 TiDB Self-Managed 的连接设置](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. 点击 **TEST CONNECTION** 以验证与 TiDB Self-Managed 集群的连接。

    如果密码不为空，在弹出窗口中点击 **Allow**，然后输入 TiDB Self-Managed 集群的密码。

    ![VS Code SQLTools：输入密码连接到 TiDB Self-Managed](/media/develop/vsc-sqltools-password.jpg)

4. 如果连接测试成功，您会看到 **Successfully connected!** 消息。点击 **SAVE CONNECTION** 保存连接配置。

</div>
</SimpleTab>

## 下一步

- 从 [Visual Studio Code 的文档](https://code.visualstudio.com/docs)了解更多 Visual Studio Code 的用法。
- 从 SQLTools 的[文档](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools)和 [GitHub 仓库](https://github.com/mtxr/vscode-sqltools)了解更多 VS Code SQLTools 扩展的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
