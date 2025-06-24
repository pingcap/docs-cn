---
title: 将 TiDB 与 Amazon AppFlow 集成
summary: 介绍如何逐步将 TiDB 与 Amazon AppFlow 集成。
---

# 将 TiDB 与 Amazon AppFlow 集成

[Amazon AppFlow](https://aws.amazon.com/appflow/) 是一个完全托管的 API 集成服务，您可以使用它将软件即服务（SaaS）应用程序连接到 AWS 服务，并安全地传输数据。使用 Amazon AppFlow，您可以在 TiDB 和许多类型的数据提供商之间导入和导出数据，例如 Salesforce、Amazon S3、LinkedIn 和 GitHub。有关更多信息，请参见 AWS 文档中的[支持的源和目标应用程序](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)。

本文介绍如何将 TiDB 与 Amazon AppFlow 集成，并以集成 TiDB Cloud Serverless 集群为例。

如果您没有 TiDB 集群，可以[创建一个 TiDB Cloud Serverless 集群](https://docs.pingcap.com/tidbcloud/create-tidb-cluster-serverless)，这是免费的，大约 30 秒即可创建完成。

## 前提条件

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 或更高版本
- [Maven](https://maven.apache.org/install.html) 3.8 或更高版本
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 版本 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 或更高版本
- 一个具有以下要求的 AWS [Identity and Access Management (IAM) 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)：

    - 用户可以使用[访问密钥](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)访问 AWS。
    - 用户具有以下权限：

        - `AWSCertificateManagerFullAccess`：用于读写 [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)。
        - `AWSCloudFormationFullAccess`：SAM CLI 使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 声明 AWS 资源。
        - `AmazonS3FullAccess`：AWS CloudFormation 使用 [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) 进行发布。
        - `AWSLambda_FullAccess`：目前，[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) 是为 Amazon AppFlow 实现新连接器的唯一方式。
        - `IAMFullAccess`：SAM CLI 需要为连接器创建 `ConnectorFunctionRole`。

- 一个 [SalesForce](https://developer.salesforce.com) 账户。

## 步骤 1. 注册 TiDB 连接器

### 克隆代码

克隆 TiDB 和 Amazon AppFlow 的[集成示例代码仓库](https://github.com/pingcap-inc/tidb-appflow-integration)：

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### 构建和上传 Lambda

1. 构建包：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. （可选）如果您尚未配置 AWS 访问密钥 ID 和密钥，请进行配置。

    ```bash
    aws configure
    ```

3. 将您的 JAR 包作为 Lambda 上传：

    ```bash
    sam deploy --guided
    ```

    > **注意：**
    >
    > - `--guided` 选项使用提示来引导您完成部署。您的输入将存储在配置文件中，默认为 `samconfig.toml`。
    > - `stack_name` 指定您正在部署的 AWS Lambda 的名称。
    > - 此提示指南使用 AWS 作为 TiDB Cloud Serverless 的云提供商。要使用 Amazon S3 作为源或目标，您需要将 AWS Lambda 的 `region` 设置为与 Amazon S3 相同的区域。
    > - 如果您之前已经运行过 `sam deploy --guided`，您可以直接运行 `sam deploy`，SAM CLI 将使用配置文件 `samconfig.toml` 来简化交互。

    如果您看到类似以下的输出，则说明此 Lambda 已成功部署。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. 转到 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home)，您可以看到刚刚上传的 Lambda。请注意，您需要在窗口右上角选择正确的区域。

    ![lambda 仪表板](/media/develop/aws-appflow-step-lambda-dashboard.png)

### 使用 Lambda 注册连接器

1. 在 [AWS 管理控制台](https://console.aws.amazon.com)中，导航到 [Amazon AppFlow > 连接器](https://console.aws.amazon.com/appflow/home#/gallery)，然后点击**注册新连接器**。

    ![注册连接器](/media/develop/aws-appflow-step-register-connector.png)

2. 在**注册新连接器**对话框中，选择您上传的 Lambda 函数，并使用连接器名称指定连接器标签。

    ![注册连接器对话框](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. 点击**注册**。然后，TiDB 连接器就注册成功了。

## 步骤 2. 创建流

导航到 [Amazon AppFlow > 流](https://console.aws.amazon.com/appflow/home#/list)，然后点击**创建流**。

![创建流](/media/develop/aws-appflow-step-create-flow.png)

### 设置流名称

输入流名称，然后点击**下一步**。

![命名流](/media/develop/aws-appflow-step-name-flow.png)

### 设置源和目标表

选择**源详情**和**目标详情**。TiDB 连接器可以在两者中使用。

1. 选择源名称。本文以 **Salesforce** 作为示例源。

    ![salesforce 源](/media/develop/aws-appflow-step-salesforce-source.png)

    注册到 Salesforce 后，Salesforce 会向您的平台添加一些示例数据。以下步骤将使用 **Account** 对象作为示例源对象。

    ![salesforce 数据](/media/develop/aws-appflow-step-salesforce-data.png)

2. 点击**连接**。

    1. 在**连接到 Salesforce** 对话框中，指定此连接的名称，然后点击**继续**。

        ![连接到 salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. 点击**允许**以确认 AWS 可以读取您的 Salesforce 数据。

        ![允许 salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注意：**
    >
    > 如果您的公司已经使用了 Salesforce 专业版，REST API 默认是禁用的。您可能需要注册一个新的开发者版本来使用 REST API。有关更多信息，请参见 [Salesforce 论坛主题](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)。

3. 在**目标详情**区域，选择 **TiDB-Connector** 作为目标。此时会显示**连接**按钮。

    ![tidb 目标](/media/develop/aws-appflow-step-tidb-dest.png)

4. 在点击**连接**之前，您需要在 TiDB 中为 Salesforce **Account** 对象创建一个 `sf_account` 表。请注意，此表架构与 [Amazon AppFlow 教程](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)中的示例数据不同。

    ```sql
    CREATE TABLE `sf_account` (
        `id` varchar(255) NOT NULL,
        `name` varchar(150) NOT NULL DEFAULT '',
        `type` varchar(150) NOT NULL DEFAULT '',
        `billing_state` varchar(255) NOT NULL DEFAULT '',
        `rating` varchar(255) NOT NULL DEFAULT '',
        `industry` varchar(255) NOT NULL DEFAULT '',
        PRIMARY KEY (`id`)
    );
    ```

5. 创建 `sf_account` 表后，点击**连接**。此时会显示一个连接对话框。
6. 在**连接到 TiDB-Connector** 对话框中，输入 TiDB 集群的连接属性。如果您使用 TiDB Cloud Serverless 集群，需要将 **TLS** 选项设置为 `Yes`，这样 TiDB 连接器就会使用 TLS 连接。然后，点击**连接**。

    ![tidb 连接消息](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. 现在您可以获取为连接指定的数据库中的所有表。从下拉列表中选择 **sf_account** 表。

    ![数据库](/media/develop/aws-appflow-step-database.png)

    以下截图显示了将数据从 Salesforce **Account** 对象传输到 TiDB 中的 `sf_account` 表的配置：

    ![完成流](/media/develop/aws-appflow-step-complete-flow.png)

8. 在**错误处理**区域，选择**停止当前流运行**。在**流触发器**区域，选择**按需运行**触发器类型，这意味着您需要手动运行流。然后，点击**下一步**。

    ![完成步骤 1](/media/develop/aws-appflow-step-complete-step1.png)

### 设置映射规则

将 Salesforce 中 **Account** 对象的字段映射到 TiDB 中的 `sf_account` 表，然后点击**下一步**。

- `sf_account` 表是在 TiDB 中新创建的，它是空的。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- 要设置映射规则，您可以在左侧选择源字段名称，在右侧选择目标字段名称。然后，点击**映射字段**，规则就设置好了。

    ![添加映射规则](/media/develop/aws-appflow-step-add-mapping-rule.png)

- 本文需要以下映射规则（源字段名称 -> 目标字段名称）：

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![映射规则](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![显示所有映射规则](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （可选）设置过滤器

如果您想为数据字段添加一些过滤器，可以在此处设置。否则，跳过此步骤并点击**下一步**。

![过滤器](/media/develop/aws-appflow-step-filters.png)

### 确认并创建流

确认要创建的流的信息。如果一切看起来都没问题，点击**创建流**。

![审查](/media/develop/aws-appflow-step-review.png)

## 步骤 3. 运行流

在新创建的流的页面上，点击右上角的**运行流**。

![运行流](/media/develop/aws-appflow-step-run-flow.png)

以下截图显示了流运行成功的示例：

![运行成功](/media/develop/aws-appflow-step-run-success.png)

查询 `sf_account` 表，您可以看到来自 Salesforce **Account** 对象的记录已经写入其中：

```sql
test> SELECT * FROM sf_account;
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| id                 | name                                | type               | billing_state | rating | industry       |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
| 001Do000003EDTlIAO | Sample Account for Entitlements     | null               | null          | null   | null           |
| 001Do000003EDTZIA4 | Edge Communications                 | Customer - Direct  | TX            | Hot    | Electronics    |
| 001Do000003EDTaIAO | Burlington Textiles Corp of America | Customer - Direct  | NC            | Warm   | Apparel        |
| 001Do000003EDTbIAO | Pyramid Construction Inc.           | Customer - Channel | null          | null   | Construction   |
| 001Do000003EDTcIAO | Dickenson plc                       | Customer - Channel | KS            | null   | Consulting     |
| 001Do000003EDTdIAO | Grand Hotels & Resorts Ltd          | Customer - Direct  | IL            | Warm   | Hospitality    |
| 001Do000003EDTeIAO | United Oil & Gas Corp.              | Customer - Direct  | NY            | Hot    | Energy         |
| 001Do000003EDTfIAO | Express Logistics and Transport     | Customer - Channel | OR            | Cold   | Transportation |
| 001Do000003EDTgIAO | University of Arizona               | Customer - Direct  | AZ            | Warm   | Education      |
| 001Do000003EDThIAO | United Oil & Gas, UK                | Customer - Direct  | UK            | null   | Energy         |
| 001Do000003EDTiIAO | United Oil & Gas, Singapore         | Customer - Direct  | Singapore     | null   | Energy         |
| 001Do000003EDTjIAO | GenePoint                           | Customer - Channel | CA            | Cold   | Biotechnology  |
| 001Do000003EDTkIAO | sForce                              | null               | CA            | null   | null           |
+--------------------+-------------------------------------+--------------------+---------------+--------+----------------+
```

## 注意事项

- 如果出现任何问题，您可以导航到 AWS 管理控制台上的 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 页面获取日志。
- 本文中的步骤基于[使用 Amazon AppFlow Custom Connector SDK 构建自定义连接器](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)。
- [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) **不是**生产环境。
- 为了防止篇幅过长，本文中的示例仅显示了 `Insert` 策略，但 `Update` 和 `Upsert` 策略也经过测试并可以使用。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
