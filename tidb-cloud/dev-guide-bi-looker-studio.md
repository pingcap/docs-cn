---
title: 使用 Looker Studio 连接 TiDB Cloud Serverless
summary: 了解如何使用 Looker Studio 连接 TiDB Cloud Serverless。
---

# 使用 Looker Studio 连接 TiDB Cloud Serverless

TiDB 是一个兼容 MySQL 的数据库，TiDB Cloud Serverless 是一个全托管的 TiDB 服务，而 [Looker Studio](https://lookerstudio.google.com/) 是一个免费的基于 Web 的 BI 工具，可以可视化来自各种来源的数据。

在本教程中，您可以学习如何使用 Looker Studio 连接到 TiDB Cloud Serverless 集群。

> **注意：**
>
> 本教程中的大多数步骤也适用于 TiDB Cloud Dedicated。但是，对于 TiDB Cloud Dedicated，您需要注意以下事项：
> 
> - 按照[从文件导入数据到 TiDB Cloud](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) 导入您的数据集。
> - 按照[连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md) 获取集群的连接信息。连接到 TiDB Cloud Dedicated 时，您需要允许来自 `142.251.74.0/23` 的访问。有关来自 Looker Studio 的连接的更多信息，请参见 [Looker Studio 文档](https://support.google.com/looker-studio/answer/7088031#zippy=%2Cin-this-article)。

## 前提条件

要完成本教程，您需要：

- 一个 Google 账号
- 一个 TiDB Cloud Serverless 集群

**如果您还没有 TiDB Cloud Serverless 集群，可以按照以下方式创建：**

- [创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)

## 步骤 1. 导入数据集

您可以导入 TiDB Cloud Serverless 交互式教程中提供的标准普尔 500 指数数据集。

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，点击右下角的 **?**。将显示**帮助**对话框。

2. 在对话框中，点击**交互式教程**，然后点击 **S&P 500 分析**。

3. 选择您的 TiDB Cloud Serverless 集群，然后点击**导入数据集**将标准普尔 500 指数数据集导入到您的集群。

4. 导入状态变为**已导入**后，点击**退出教程**关闭此对话框。

如果在导入过程中遇到任何问题，您可以按照以下方式取消此导入任务：

1. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击您的 TiDB Cloud Serverless 集群的名称进入其概览页面。
2. 在左侧导航栏中，点击**数据** > **导入**。
3. 找到名为 **sp500-insight** 的导入任务，点击**操作**列中的 **...**，然后点击**取消**。

## 步骤 2. 获取集群的连接信息

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，将**连接方式**设置为 `General`，然后点击**生成密码**创建随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，请使用原始密码或点击**重置密码**生成新密码。

4. 下载 [CA 证书](https://letsencrypt.org/certs/isrgrootx1.pem)。

    > **提示：**
    >
    > TiDB Cloud Serverless 要求客户端和集群之间建立安全的 TLS 连接，因此您需要在 Looker Studio 的连接设置中使用此 CA 证书。

## 步骤 3. 使用 Looker Studio 连接到 TiDB 集群

1. 登录 [Looker Studio](https://lookerstudio.google.com/)，然后在左侧导航栏中点击**创建** > **报告**。

2. 在显示的页面上，搜索并选择 **MySQL** 连接器，然后点击**授权**。

3. 在**基本**设置面板中，配置连接参数。

    - **主机名或 IP**：输入 TiDB Cloud Serverless 连接对话框中的 `HOST` 参数。
    - **端口（可选）**：输入 TiDB Cloud Serverless 连接对话框中的 `PORT` 参数。
    - **数据库**：输入要连接的数据库。对于本教程，输入 `sp500insight`。
    - **用户名**：输入 TiDB Cloud Serverless 连接对话框中的 `USERNAME` 参数。
    - **密码**：输入 TiDB Cloud Serverless 连接对话框中的 `PASSWORD` 参数。
    - **启用 SSL**：选中此选项，然后点击 **MySQL SSL 客户端配置文件**右侧的上传图标，上传从[步骤 2](#步骤-2-获取集群的连接信息) 下载的 CA 文件。

    ![Looker Studio：为 TiDB Cloud Serverless 配置连接设置](/media/tidb-cloud/looker-studio-configure-connection.png)

4. 点击**验证**。

如果验证成功，您可以看到数据库中的表。

## 步骤 4. 创建简单图表

现在，您可以使用 TiDB 集群作为数据源，并使用数据创建简单的图表。

1. 在右侧面板中，点击**自定义查询**。

    ![Looker Studio：自定义查询](/media/tidb-cloud/looker-studio-custom-query.png)

2. 将以下代码复制到**输入自定义查询**区域，然后点击右下角的**添加**。

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

    如果看到**您即将向此报告添加数据**对话框，请点击**添加到报告**。然后，报告中将显示一个表格。

3. 在报告的工具栏中，点击**添加图表**，然后在 `折线图` 类别中选择 `组合图表`。

4. 在右侧的**图表**设置面板中，配置以下参数：

    - 在**设置**标签页中：
        - **维度**：`sector`。
        - **指标**：`companies` 和 `total_market_cap`。
    - 在**样式**标签页中：
      - 系列 #1：选择 `折线图` 选项和 `右` 轴。
      - 系列 #2：选择 `柱状图` 选项和 `左` 轴。
    - 其他字段保持默认值。

然后，您可以看到类似如下的组合图表：

![Looker Studio：简单的组合图表](/media/tidb-cloud/looker-studio-simple-chart.png)

## 下一步

- 从 [Looker Studio 帮助](https://support.google.com/looker-studio)了解更多 Looker Studio 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。
