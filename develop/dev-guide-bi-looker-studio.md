---
title: 使用 Looker Studio 连接 TiDB Cloud
summary: 了解如何使用 Looker Studio 连接 TiDB Cloud。
---

# 使用 Looker Studio 连接 TiDB Cloud <!-- Draft translated by AI -->

TiDB 是一个兼容 MySQL 的数据库，TiDB Cloud 是一款完全托管的数据库即服务（DBaaS），可将 TiDB 部署到你的云环境中，[Looker Studio](https://lookerstudio.google.com/) 是一款免费的基于 Web 的 BI 工具，可以可视化来自多种数据源的数据。

本教程以 TiDB Cloud Starter 集群为例，演示如何使用 Looker Studio 连接 TiDB Cloud。

> **注意：**
>
> - 除了 TiDB Cloud Starter 集群外，本文档中的步骤同样适用于 TiDB Cloud Essential 集群。
> - 本教程的大部分步骤也适用于 TiDB Cloud Dedicated。但对于 TiDB Cloud Dedicated，你需要注意以下事项：
>     - 按照 [从文件导入数据到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) 导入你的数据集。
>     - 按照 [连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md) 获取你的集群连接信息。连接 TiDB Cloud Dedicated 时，你需要允许来自 `142.251.74.0/23` 的访问。关于 Looker Studio 的连接详情，请参阅 [Looker Studio 文档](https://support.google.com/looker-studio/answer/7088031#zippy=%2Cin-this-article)。

## 前置条件

完成本教程，你需要：

- 一个 Google 账号
- 一个 TiDB Cloud Starter 集群

**如果你还没有 TiDB Cloud Starter 集群，可以按如下方式创建：**

- [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-cluster)

## 步骤 1. 导入数据集

你可以导入 TiDB Cloud Starter 交互式教程中提供的 S&P 500 数据集。

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击右下角的 **?**。此时会弹出 **Help** 对话框。

2. 在对话框中，点击 **Interactive Tutorials**，然后点击 **S&P 500 Analysis**。

3. 选择你的 TiDB Cloud Starter 集群，然后点击 **Import Dataset**，将 S&P 500 数据集导入到你的集群中。

4. 当导入状态变为 **IMPORTED** 后，点击 **Exit Tutorial** 关闭该对话框。

如果在导入过程中遇到问题，你可以按如下方式取消该导入任务：

1. 在 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击你的 TiDB Cloud Starter 集群名称，进入其概览页面。
2. 在左侧导航栏，点击 **Data** > **Import**。
3. 找到名为 **sp500-insight** 的导入任务，在 **Action** 列点击 **...**，然后点击 **Cancel**。

## 步骤 2. 获取集群连接信息

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标集群名称，进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，将 **Connect With** 设置为 `General`，然后点击 **Generate Password** 生成一个随机密码。

    > **提示：**
    >
    > 如果你之前已经创建过密码，请使用原密码，或点击 **Reset Password** 生成新密码。

4. 下载 [CA cert](https://letsencrypt.org/certs/isrgrootx1.pem)。

    > **提示：**
    >
    > TiDB Cloud Starter 要求客户端与集群之间建立安全的 TLS 连接，因此你需要在 Looker Studio 的连接设置中使用该 CA 证书。

## 步骤 3. 使用 Looker Studio 连接 TiDB 集群

1. 登录 [Looker Studio](https://lookerstudio.google.com/)，在左侧导航栏点击 **Create** > **Report**。

2. 在弹出页面中，搜索并选择 **MySQL** 连接器，然后点击 **AUTHORIZE**。

3. 在 **BASIC** 设置面板中，配置连接参数。

    - **Host Name or IP**：输入 TiDB Cloud Starter 连接对话框中的 `HOST` 参数。
    - **Port(Optional)**：输入 TiDB Cloud Starter 连接对话框中的 `PORT` 参数。
    - **Database**：输入你要连接的数据库。本教程中输入 `sp500insight`。
    - **Username**：输入 TiDB Cloud Starter 连接对话框中的 `USERNAME` 参数。
    - **Password**：输入 TiDB Cloud Starter 连接对话框中的 `PASSWORD` 参数。
    - **Enable SSL**：勾选此项，然后点击 **MySQL SSL Client Configuration Files** 右侧的上传图标，上传在 [步骤 2](#step-2-get-the-connection-information-for-your-cluster) 下载的 CA 文件。

    ![Looker Studio: 配置 TiDB Cloud Starter 连接设置](/media/tidb-cloud/looker-studio-configure-connection.png)

4. 点击 **AUTHENTICATE**。

认证成功后，你可以看到数据库中的表。

## 步骤 4. 创建一个简单图表

现在，你可以将 TiDB 集群作为数据源，创建一个简单的数据图表。

1. 在右侧面板点击 **CUSTOM QUERY**。

    ![Looker Studio: 自定义查询](/media/tidb-cloud/looker-studio-custom-query.png)

2. 将以下代码复制到 **Enter Custom Query** 区域，然后点击右下角的 **Add**。

    ```sql
    SELECT sector,
        COUNT(*)                                                                      AS companies,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC )                                   AS companies_ranking,
        SUM(market_cap)                                                               AS total_market_cap,
        ROW_NUMBER() OVER (ORDER BY SUM(market_cap) DESC )                            AS total_market_cap_ranking,
        SUM(revenue_growth * weight) / SUM(weight)                                    AS avg_revenue_growth,
        ROW_NUMBER() OVER (ORDER BY SUM(revenue_growth * weight) / SUM(weight) DESC ) AS avg_revenue_growth_ranking
    FROM companies
        LEFT JOIN index_compositions ic ON companies.stock_symbol = ic.stock_symbol
    GROUP BY sector
    ORDER BY 5 ASC;
    ```

    如果弹出 **You are about to add data to this report** 对话框，点击 **ADD TO REPORT**。随后，报表中会显示一个表格。

3. 在报表工具栏点击 **Add a chart**，然后在 `Line` 分类下选择 `Combo chart`。

4. 在右侧 **Chart** 设置面板，配置以下参数：

    - 在 **SETUP** 标签页：
        - **Dimension**：`sector`
        - **Metric**：`companies` 和 `total_market_cap`
    - 在 **STYLE** 标签页：
      - Series #1：选择 `Line` 选项并设置为 `Right` 轴。
      - Series #2：选择 `Bars` 选项并设置为 `Left` 轴。
    - 其他字段保持默认。

此时，你可以看到如下所示的组合图表：

![Looker Studio: 一个简单的组合图表](/media/tidb-cloud/looker-studio-simple-chart.png)

## 后续步骤

- 通过 [Looker Studio 帮助中心](https://support.google.com/looker-studio) 了解更多 Looker Studio 的用法。
- 通过 [开发者指南](/develop/dev-guide-overview.md) 各章节，学习 TiDB 应用开发最佳实践，例如 [插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md) 和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，考试通过后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

欢迎在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。