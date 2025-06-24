---
title: 使用 Navicat 连接 TiDB
summary: 了解如何使用 Navicat 连接 TiDB。
---

# 使用 Navicat 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [Navicat](https://www.navicat.com) 是一套面向数据库用户的 GUI 工具。本教程使用 [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) 工具连接 TiDB。

在本教程中，你将学习如何使用 Navicat 连接到你的 TiDB 集群。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，你需要：

- [Navicat Premium](https://www.navicat.com) **17.1.6** 或更高版本。
- Navicat Premium 的付费账户。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 连接到 TiDB

根据你选择的 TiDB 部署选项连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接工具**设置为 `Navicat`。
    - **操作系统**与你的环境匹配。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果你之前已经创建了密码，你可以使用原始密码，也可以点击**重置密码**生成一个新密码。

5. 启动 Navicat Premium，点击左上角的**连接**，从**供应商过滤器**列表中选择 **PingCAP**，然后双击右侧面板中的 **TiDB**。

    ![Navicat：添加新连接](/media/develop/navicat-premium-add-new-connection.png)

6. 在**新建连接 (TiDB)** 对话框中，配置以下连接参数：

    - **连接名**：为此连接指定一个有意义的名称。
    - **主机**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **端口**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **用户名**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **密码**：输入 TiDB Cloud Serverless 集群的密码。

    ![Navicat：为 TiDB Cloud Serverless 配置连接常规面板](/media/develop/navicat-premium-connection-config-serverless-general.png)

7. 点击 **SSL** 标签，选中**使用 SSL**、**使用身份验证**和**根据 CA 验证服务器证书**复选框。然后，将 TiDB Cloud 连接对话框中的 `CA` 文件选择到 **CA 证书**字段中。

    ![Navicat：为 TiDB Cloud Serverless 配置连接 SSL 面板](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8. 点击**测试连接**以验证与 TiDB Cloud Serverless 集群的连接。

9. 如果连接测试成功，你会看到**连接成功**消息。点击**确定**完成连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择 **Public**。

    如果你还没有配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息，请参见[连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 点击 **CA cert** 下载 CA 证书。

5. 启动 Navicat Premium，点击左上角的**连接**，从**供应商过滤器**列表中选择 **PingCAP**，然后双击右侧面板中的 **TiDB**。

    ![Navicat：添加新连接](/media/develop/navicat-premium-add-new-connection.png)

6. 在**新建连接 (TiDB)** 对话框中，配置以下连接参数：

    - **连接名**：为此连接指定一个有意义的名称。
    - **主机**：输入 TiDB Cloud 连接对话框中的 `HOST` 参数。
    - **端口**：输入 TiDB Cloud 连接对话框中的 `PORT` 参数。
    - **用户名**：输入 TiDB Cloud 连接对话框中的 `USERNAME` 参数。
    - **密码**：输入 TiDB Cloud Dedicated 集群的密码。

    ![Navicat：为 TiDB Cloud Dedicated 配置连接常规面板](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7. 点击 **SSL** 标签，选中**使用 SSL**、**使用身份验证**和**根据 CA 验证服务器证书**复选框。然后，将步骤 4 中下载的 CA 文件选择到 **CA 证书**字段中。

    ![Navicat：为 TiDB Cloud Dedicated 配置连接 SSL 面板](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8. 点击**测试连接**以验证与 TiDB Cloud Dedicated 集群的连接。

9. 如果连接测试成功，你会看到**连接成功**消息。点击**确定**完成连接配置。

</div>
<div label="TiDB Self-Managed">

1. 启动 Navicat Premium，点击左上角的**连接**，从**供应商过滤器**列表中选择 **PingCAP**，然后双击右侧面板中的 **TiDB**。

    ![Navicat：添加新连接](/media/develop/navicat-premium-add-new-connection.png)

2. 在**新建连接 (TiDB)** 对话框中，配置以下连接参数：

    - **连接名**：为此连接指定一个有意义的名称。
    - **主机**：输入你的 TiDB Self-Managed 集群的 IP 地址或域名。
    - **端口**：输入你的 TiDB Self-Managed 集群的端口号。
    - **用户名**：输入用于连接 TiDB 的用户名。
    - **密码**：输入用于连接 TiDB 的密码。

    ![Navicat：为自托管 TiDB 配置连接常规面板](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3. 点击**测试连接**以验证与 TiDB Self-Managed 集群的连接。

4. 如果连接测试成功，你会看到**连接成功**消息。点击**确定**完成连接配置。

</div>
</SimpleTab>

## 下一步

- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
