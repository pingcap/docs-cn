---
title: 使用 Navicat 连接 TiDB
summary: 了解如何使用 Navicat 连接到 TiDB。
---

# 使用 Navicat 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Navicat](https://www.navicat.com) 是为数据库用户提供的 GUI 工具集。本教程使用 [Navicat for MySQL](https://www.navicat.com/en/products/navicat-for-mysql) 工具连接 TiDB。

> **警告**
>
> - 尽管由于 Navicat 兼容 MySQL，你可以使用 Navicat 连接到 TiDB，但 Navicat 并不完全支持 TiDB。由于 Navicat 将 TiDB 视为 MySQL，因此在使用过程中可能会遇到一些问题。[Navicat 用户管理兼容性](https://github.com/pingcap/tidb/issues/45154) 存在一个已知问题。更多 Navicat 和 TiDB 之间的兼容性问题，参考 [TiDB GitHub 问题页面](https://github.com/pingcap/tidb/issues?q=is%3Aissue+navicat+is%3Aopen)。
> - 推荐使用其他官方支持 TiDB 的 GUI 工具，例如 DataGrip，DBeaver 以及 VS Code SQLTools。TiDB 完全支持的 GUI 工具的完整列表，参考 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md#gui)。

在本文档中，你可以学习如何使用 Navicat 连接到 TiDB 集群。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本文中的操作，你需要：

- [Navicat for MySQL](https://www.navicat.com/en/download/navicat-for-mysql) **16.3.2** 或以上版本。
- 一个 Navicat for MySQL 的付费账号。
- 准备一个 TiDB 集群。

**如果你未有 TiDB 集群，可以按如下方式创建一个：**

- （推荐） 参考 [使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md) 来创建一个 TiDB Cloud 集群。
- 参考 [部署本地测试集群](/quick-start-with-tidb.md#部署本地测试集群) 或 [部署生产 TiDB 集群](/production-deployment-using-tiup.md) 来创建一个本地集群。

## 连接到 TiDB

根据你选择的 TiDB 部署选项连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，并进入集群的 Overview 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Endpoint Type** 选择 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `Navicat`。
    - **Operating System** 为你的运行环境。

4. 点击 **Generate Password** 生成一个随机密码。

    > **小贴士**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 启动 Navicat for MySQL，点击左上角的 **Connection**，并从下拉列表中选择 **MySQL**。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6. 在 **New Connection (MySQL)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**：输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **User Name**：输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：输入 TiDB Serverless 集群的密码。

    ![Navicat: configure connection general panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-general.png)

7. 点击 **SSL** 标签，选择 **Use SSL**，**Use authentication** 以及 **Verify server certificate against CA** 复选框。并在 **CA Certificate** 字段中填入从 TiDB Cloud 连接对话框中获取的 `CA` 文件路径。

    ![Navicat: configure connection SSL panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-ssl.png)

8. 点击 **Test Connection** 以验证与 TiDB Serverless 集群的连接。

9. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **Save** 完成连接配置。

</div>
<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，并进入集群的 Overview 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 点击 **Allow Access from Anywhere**。

    有关如何获取连接字符串的更多详细信息，参考 [TiDB Dedicated 标准连接](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 点击 **Download CA cert** 下载 CA 文件。

5. 启动 Navicat for MySQL，点击左上角的 **Connection**，并从下拉列表中选择 **MySQL**。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6. 在 **New Connection (MySQL)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**: 输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **User Name**: 输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：输入 TiDB Dedicated 集群的密码。

    ![Navicat: configure connection general panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-general.png)

7. 点击 **SSL** 标签，选择 **Use SSL**，**Use authentication** 以及 **Verify server certificate against CA** 复选框。然后，在 **CA Certificate** 字段中选择第 4 步下载的 CA 文件。

    ![Navicat: configure connection SSL panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-ssl.jpg)

8. 点击 **Test Connection** 以验证与 TiDB Dedicated 集群的连接。

9. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **Save** 完成连接配置。

</div>
<div label="TiDB Self-Hosted">

1. 启动 Navicat for MySQL，点击左上角的 **Connection**，并从下拉列表中选择 **MySQL**。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

2. 在 **New Connection (MySQL)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**：输入本地部署 TiDB 集群的 IP 地址或域名。
    - **Port**：输入本地部署 TiDB 集群的端口号。
    - **User Name**：输入用于连接到 TiDB 的用户名。
    - **Password**：输入用于连接到 TiDB 的密码。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-connection-config-self-hosted-general.png)

3. 点击 **Test Connection** 以验证与本地部署 TiDB 集群的连接。

4. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **Save** 完成连接配置。

</div>
</SimpleTab>

## 下一步

- 你可以继续阅读 [开发者文档](/develop/dev-guide-overview.md)，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide) 支持，并在考试后提供相应的 [资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，或从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。
