---
title: 使用 MySQL Workbench 连接到 TiDB
summary: 了解如何使用 MySQL Workbench 连接到 TiDB。
---

# 使用 MySQL Workbench 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[MySQL Workbench](https://www.mysql.com/products/workbench/) 是为 MySQL 数据库用户提供的 GUI 工具集。

> **警告**
>
> - 尽管由于 MySQL Workbench 兼容 MySQL，你可以使用 MySQL Workbench 连接到 TiDB，但 MySQL Workbench 并不完全支持 TiDB。由于 MySQL Workbench 将 TiDB 视为 MySQL，因此在使用过程中可能会遇到一些问题。
> - 建议使用其它 TiDB 完全支持的 GUI 工具进行连接，例如 DataGrip，DBeaver 以及 VS Code SQLTools。TiDB 完全支持的 GUI 工具的完整列表，参考 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-support.md#gui)。

在本文档中，你可以学习如何使用 MySQL Workbench 连接到 TiDB 集群。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本文中的操作，你需要：

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** 或以上版本。
- 准备一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建一个：**

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)，创建一个 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建一个本地集群。

## 连接到 TiDB

根据你选择的 TiDB 部署方式连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Endpoint Type** 选择 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `MySQL Workbench`。
    - **Operating System** 为你的运行环境。

4. 点击 **Generate Password** 生成一个随机密码。

    > **小贴士**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 启动 MySQL Workbench，并点击 **MySQL Connections** 标题旁边的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Hostname**：输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **Username**：输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...**  或 **Store in Vault**，输入 TiDB Serverless 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of TiDB Serverless in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    下图显示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Serverless](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. 点击 **Test Connection** 以验证与 TiDB Serverless 集群的连接。

8. 如果连接测试成功，你可以看到 **Successfully made the MySQL connection** 信息。点击 **OK** 保存连接配置。

</div>
<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 点击 **Allow Access from Anywhere**。

    有关如何获取连接字符串的更多详细信息，参考 [TiDB Dedicated 标准连接（英文）](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 启动 MySQL Workbench，并点击 **MySQL Connections** 标题旁边的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Hostname**: 输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **Username**：输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：点击 **Store in Keychain ...**，输入 TiDB Dedicated 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of TiDB Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    下图显示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. 点击 **Test Connection** 以验证与 TiDB Dedicated 集群的连接。

7. 如果连接测试成功，你可以看到 **Successfully made the MySQL connection** 信息。点击 **OK** 保存连接配置。

</div>
<div label="TiDB Self-Hosted">

1. 启动 MySQL Workbench，并点击 **MySQL Connections** 标题旁边的 **+**。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2. 在 **Setup New Connection** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Hostname**：输入本地部署 TiDB 集群的 IP 地址或域名。
    - **Port**：输入本地部署 TiDB 集群的端口号。
    - **Username**：输入用于连接到 TiDB 的用户名。
    - **Password**：点击 **Store in Keychain ...**，输入用于连接 TiDB 集群的密码，然后点击 **OK** 保存密码。

        ![MySQL Workbench: store the password of TiDB Self-Hosted in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    下图显示了连接参数的示例：

    ![MySQL Workbench: configure connection settings for TiDB Self-Hosted](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. 点击 **Test Connection** 以验证与本地部署 TiDB 集群的连接。

4. 如果连接测试成功，你可以看到 **Successfully made the MySQL connection** 信息。点击 **OK** 保存连接配置。

</div>
</SimpleTab>

## 下一步

- 关于 MySQL Workbench 的更多使用方法，可以参考 [MySQL Workbench 官方文档](https://dev.mysql.com/doc/workbench/en/)。
- 你可以继续阅读[开发者文档](/develop/dev-guide-overview.md)，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide) 支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，或从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。
