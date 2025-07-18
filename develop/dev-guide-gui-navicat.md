---
title: 使用 Navicat 连接到 TiDB
summary: 了解如何使用 Navicat 连接到 TiDB。
---

# 使用 Navicat 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Navicat](https://www.navicat.com) 是为数据库用户提供的 GUI 工具集。本教程使用 [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) 工具连接 TiDB。

在本文档中，你可以学习如何使用 Navicat 连接到 TiDB 集群。

> **注意**
>
> 本文档适用于 {{{ .starter }}}、TiDB Cloud Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本文中的操作，你需要：

- [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) **17.1.6** 或以上版本。
- 一个 Navicat Premium 的付费账号。
- 准备一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建一个：**

- （推荐方式）参考[创建 {{{ .starter }}} 集群](/develop/dev-guide-build-cluster-in-cloud.md)，创建一个 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建一个本地集群。

## 连接到 TiDB

根据你选择的 TiDB 部署方式连接到 TiDB 集群。

<SimpleTab>
<div label="{{{ .starter }}}">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 选择 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `Navicat`。
    - **Operating System** 为你的运行环境。

4. 点击 **Generate Password** 生成一个随机密码。

    > **建议：**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 中勾选 **PingCAP**，并双击右侧面板中的 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**：输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **User Name**：输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：输入 {{{ .starter }}} 集群的密码。

    ![Navicat: configure connection general panel for {{{ .starter }}}](/media/develop/navicat-premium-connection-config-serverless-general.png)

7. 点击 **SSL** 选项卡，选择 **Use SSL**，**Use authentication** 以及 **Verify server certificate against CA** 复选框。并在 **CA Certificate** 字段中填入从 TiDB Cloud 连接对话框中获取的 `CA` 文件路径。

    ![Navicat: configure connection SSL panel for {{{ .starter }}}](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8. 点击 **Test Connection** 以验证与 {{{ .starter }}} 集群的连接。

9. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **OK** 完成连接配置。

</div>
<div label="TiDB Cloud Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，点击你目标集群的名字，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 或按照[配置 IP 访问列表（英文）](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。详情请参阅[连接 TiDB Cloud Dedicated 集群（英文）](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 点击 **CA cert** 下载 CA 文件。

5. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 中勾选 **PingCAP**，并双击右侧面板中的 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**: 输入从 TiDB Cloud 连接对话框中的得到的 `HOST` 参数。
    - **Port**：输入从 TiDB Cloud 连接对话框中的得到的 `PORT` 参数。
    - **User Name**: 输入从 TiDB Cloud 连接对话框中的得到的 `USERNAME` 参数。
    - **Password**：输入 TiDB Cloud Dedicated 集群的密码。

    ![Navicat: configure connection general panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7. 点击 **SSL** 选项卡，选择 **Use SSL**，**Use authentication** 以及 **Verify server certificate against CA** 复选框。然后，在 **CA Certificate** 字段中选择第 4 步下载的 CA 文件。

    ![Navicat: configure connection SSL panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8. 点击 **Test Connection** 以验证与 TiDB Cloud Dedicated 集群的连接。

9. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **OK** 完成连接配置。

</div>
<div label="本地部署 TiDB">

1. 启动 Navicat Premium，点击左上角的 **Connection**，在 **Vendor Filter** 中勾选 **PingCAP**，并双击右侧面板中的 **TiDB**。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

2. 在 **New Connection (TiDB)** 对话框中，配置以下连接参数：

    - **Connection Name**：为该连接指定一个有意义的名称。
    - **Host**：输入本地部署 TiDB 集群的 IP 地址或域名。
    - **Port**：输入本地部署 TiDB 集群的端口号。
    - **User Name**：输入用于连接到 TiDB 的用户名。
    - **Password**：输入用于连接到 TiDB 的密码。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3. 点击 **Test Connection** 以验证与本地部署 TiDB 集群的连接。

4. 如果连接测试成功，你可以看到 **Connection Successful** 信息。点击 **OK** 完成连接配置。

</div>
</SimpleTab>

## 下一步

- 你可以继续阅读[开发者文档](/develop/dev-guide-overview.md)，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide) 支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，或从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。
