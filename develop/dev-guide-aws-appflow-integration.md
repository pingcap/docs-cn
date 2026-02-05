---
title: TiDB 与 Amazon AppFlow 集成指南
summary: 了解如何将 TiDB 集成到 Amazon AppFlow。
---

# TiDB 与 Amazon AppFlow 集成指南

[Amazon AppFlow](https://aws.amazon.com/appflow/) 是一项全托管的 API 集成服务，可用于将软件即服务 (SaaS) 应用与 AWS 服务连接，并安全地传输数据。通过 Amazon AppFlow，你可以在 TiDB 与多种数据提供方之间导入和导出数据，例如 Salesforce、Amazon S3、LinkedIn 和 GitHub。更多信息请参见 AWS 文档中的[支持的源和目标应用](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)。

本文档介绍了如何将 TiDB 与 Amazon AppFlow 进行集成，并以集成 TiDB Cloud Starter 集群为例进行说明。

如果你还没有 TiDB 集群，可以创建一个 [TiDB Cloud Starter](https://tidbcloud.com/console/clusters) 集群，该集群免费，且大约 30 秒即可创建完成。

## 前提条件

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 或更高版本
- [Maven](https://maven.apache.org/install.html) 3.8 或更高版本
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 版本 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 或更高版本
- 一个满足以下要求的 AWS [Identity and Access Management (IAM) 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)：

    - 该用户可以通过 [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) 访问 AWS。
    - 该用户拥有以下权限：

        - `AWSCertificateManagerFullAccess`：用于读写 [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)。
        - `AWSCloudFormationFullAccess`：SAM CLI 使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 来声明 AWS 资源。
        - `AmazonS3FullAccess`：AWS CloudFormation 使用 [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) 进行发布。
        - `AWSLambda_FullAccess`：目前，[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) 是为 Amazon AppFlow 实现新连接器的唯一方式。
        - `IAMFullAccess`：SAM CLI 需要为连接器创建 `ConnectorFunctionRole`。

- 一个 [SalesForce](https://developer.salesforce.com) 账号。

## 第 1 步：注册 TiDB 连接器

### 克隆代码

克隆 TiDB 与 Amazon AppFlow 的[集成示例代码仓库](https://github.com/pingcap-inc/tidb-appflow-integration)：

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### 构建并上传 Lambda

1. 构建包：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. （可选）如果你还没有配置 AWS access key ID 和 secret access key，请进行配置。

    ```bash
    aws configure
    ```

3. 将你的 JAR 包上传为 Lambda：

    ```bash
    sam deploy --guided
    ```

    > **注意：**
    >
    > - `--guided` 选项会通过提示引导你完成部署。你的输入会被存储在配置文件中，默认是 `samconfig.toml`。
    > - `stack_name` 用于指定正在部署的 AWS Lambda 的名称。
    > - 引导流程默认使用 AWS 作为 TiDB Cloud Starter 的云服务商。如果你要将 Amazon S3 作为源或目标，需要将 AWS Lambda 的 `region` 设置为与 Amazon S3 相同。
    > - 如果你之前已经运行过 `sam deploy --guided`，可以直接运行 `sam deploy`，SAM CLI 会使用 `samconfig.toml` 配置文件简化交互。

    如果你看到类似如下输出，说明 Lambda 部署成功。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. 进入 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home)，你可以看到刚刚上传的 Lambda。注意需要在窗口右上角选择正确的 region。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### 使用 Lambda 注册连接器

1. 在 [AWS 管理控制台](https://console.aws.amazon.com) 中，前往 [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery)，然后点击 **Register new connector**。

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2. 在 **Register a new connector** 对话框中，选择你上传的 Lambda 函数，并使用连接器名称指定 connector label。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. 点击 **Register**。此时，TiDB 连接器注册成功。

## 第 2 步：创建 flow

前往 [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list)，点击 **Create flow**。

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### 设置 flow 名称

输入 flow 名称，然后点击 **Next**。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### 设置源表和目标表

选择 **Source details** 和 **Destination details**。TiDB 连接器可以在这两者中使用。

1. 选择源名称。本文档以 **Salesforce** 作为示例源。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    注册 Salesforce 后，Salesforce 会在你的平台中添加一些示例数据。接下来的步骤将以 **Account** 对象作为示例源对象。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2. 点击 **Connect**。

    1. 在 **Connect to Salesforce** 对话框中，指定该连接的名称，然后点击 **Continue**。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. 点击 **Allow**，以确认 AWS 可以读取你的 Salesforce 数据。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注意：**
    >
    > 如果你的公司已经在使用 Salesforce 专业版 (Professional Edition)，默认情况下未启用 REST API。你可能需要注册一个新的 Salesforce 开发者版 (Developer Edition) 才能使用 REST API。更多信息请参考 [Salesforce 论坛相关话题](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)。

3. 在 **Destination details** 区域，选择 **TiDB-Connector** 作为目标端。此时会显示 **Connect** 按钮。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4. 在点击 **Connect** 之前，你需要在 TiDB 中为 Salesforce 的 **Account** 对象创建一个 `sf_account` 表。注意该表结构与 [Tutorial of Amazon AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html) 中的示例数据不同。

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

5. 创建好 `sf_account` 表后，点击 **Connect**。会弹出连接对话框。
6. 在 **Connect to TiDB-Connector** 对话框中，输入 TiDB 集群的连接属性。如果你使用的是 TiDB Cloud Starter 集群，需要将 **TLS** 选项设置为 `Yes`，这样 TiDB 连接器会使用 TLS 连接。然后点击 **Connect**。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. 现在你可以获取到在连接中指定的数据库里的所有表。从下拉列表中选择 **sf_account** 表。

    ![database](/media/develop/aws-appflow-step-database.png)

    下图展示了将 Salesforce **Account** 对象的数据传输到 TiDB 中 `sf_account` 表的配置：

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8. 在 **Error handling** 区域，选择 **Stop the current flow run**。在 **Flow trigger** 区域，选择 **Run on demand** 触发类型，表示你需要手动运行 flow。然后点击 **Next**。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### 设置映射规则

将 Salesforce 中 **Account** 对象的字段映射到 TiDB 的 `sf_account` 表，然后点击 **Next**。

- `sf_account` 表是新建的，当前为空。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- 设置映射规则时，你可以在左侧选择源字段名，在右侧选择目标字段名。然后点击 **Map fields**，即可设置一条规则。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- 本文示例需要以下映射规则（源字段名 -> 目标字段名）：

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （可选）设置过滤器

如果你想为数据字段添加一些过滤条件，可以在此处设置。否则，跳过此步骤，并点击 **Next**。

![filters](/media/develop/aws-appflow-step-filters.png)

### 确认并创建 flow

确认即将创建的 flow 的信息。如果一切无误，点击 **Create flow**。

![review](/media/develop/aws-appflow-step-review.png)

## 第 3 步：运行 flow

在新建 flow 的页面右上角，点击 **Run flow**。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

下图展示了 flow 成功运行的示例：

![run success](/media/develop/aws-appflow-step-run-success.png)

查询 `sf_account` 表，你可以看到 Salesforce **Account** 对象中的记录已经写入该表：

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

- 如果遇到问题，可以在 AWS 管理控制台的 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 页面查看日志。
- 本文档中的步骤基于 [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)。
- [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) **不是**生产环境。
- 为避免篇幅过长，本文档示例仅展示了 `Insert` 策略，`Update` 和 `Upsert` 策略也已测试并可用。

## 需要帮助？

- 在 [AskTUG 论坛](https://asktug.com/?utm_source=docs-cn-dev-guide) 上提问
- [提交 TiDB Cloud 工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 工单](/support.md)
