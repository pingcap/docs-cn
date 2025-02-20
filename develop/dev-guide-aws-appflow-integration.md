---
title: TiDB 与 Amazon AppFlow 集成
summary: 介绍 TiDB 与 Amazon AppFlow 的逐步集成方式。
---

# TiDB 与 Amazon AppFlow 集成

[Amazon AppFlow](https://aws.amazon.com/appflow/) 是一项完全托管的集成服务，你可以使用 Amazon AppFlow 在软件即服务 (SaaS) 应用程序服务之间安全地传输数据。使用 Amazon AppFlow，你可以在 TiDB 与许多 Amazon AppFlow 连接器提供者直接传输数据，如 Salesforce、Amazon S3、LinkedIn 及 GitHub 等。你可以查看 AWS 的[支持的数据源与数据目标服务](https://docs.aws.amazon.com/appflow/latest/userguide/app-specific.html)文档，以获取更多信息。

本文将介绍如何将 TiDB 与 Amazon AppFlow 集成，并以集成 TiDB Cloud Serverless 集群为例。

如果你还没有 TiDB 集群，可以创建一个免费的 [TiDB Cloud Serverless](https://tidbcloud.com/console/clusters) 集群，仅需约 30 秒即可创建完成。

## 依赖

- [Git](https://git-scm.com/)
- [JDK](https://openjdk.org/install/) 11 及以上
- [Maven](https://maven.apache.org/install.html) 3.8 及以上
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) version 2
- [AWS Serverless Application Model Command Line Interface (AWS SAM CLI)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) 1.58.0 版本及以上
- 满足以下需求的 AWS [Identity and Access Management (IAM) 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)：

    - 此用户可使用 [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) 登录 AWS。
    - 此用户需拥有以下权限：

        - `AWSCertificateManagerFullAccess`: 用于读写 [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)。
        - `AWSCloudFormationFullAccess`: SAM CLI 使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 来声明式的使用 AWS 资源。
        - `AmazonS3FullAccess`: AWS CloudFormation 使用 [Amazon S3](https://aws.amazon.com/s3/?nc2=h_ql_prod_fs_s3) 进行发布。
        - `AWSLambda_FullAccess`: 当前，[AWS Lambda](https://aws.amazon.com/lambda/?nc2=h_ql_prod_fs_lbd) 是部署与实现 Amazon AppFlow 自定义连接器的唯一办法。
        - `IAMFullAccess`: SAM CLI 需要创建 `ConnectorFunctionRole` 来操作此自定义连接器。

- [SalesForce](https://developer.salesforce.com) 账户。

## 第 1 步：注册 TiDB 连接器

### Clone 源代码仓库

Clone TiDB 与 Amazon AppFlow 的[连接器源代码仓库](https://github.com/pingcap-inc/tidb-appflow-integration):

```bash
git clone https://github.com/pingcap-inc/tidb-appflow-integration
```

### 构建并上传 AWS Lambda

1. 构建 Jar 包：

    ```bash
    cd tidb-appflow-integration
    mvn clean package
    ```

2. （可选）如果你从未配置过你的 AWS **Access Key ID** 及 **Secret Access Key**，你需要配置它。

    ```bash
    aws configure
    ```

3. 上传你的 Jar 包作为一个 AWS Lambda:

    ```bash
    sam deploy --guided
    ```

    > **注意：**
    >
    > - `--guided` 选项使用提示来引导你完成部署。你的输入将被存储在一个配置文件中，默认文件名为 `samconfig.toml`。
    > - 使用 `stack_name` 指定你要部署的 AWS Lambda 的名称。
    > - 本文使用 AWS 作为 TiDB Cloud Serverless 的云提供商。
    > - 如需使用 Amazon S3 作为源或目标，需将 AWS Lambda 的区域设置为与 Amazon S3 的区域相同。
    > - 如果你曾运行过 `sam deploy --guided` 命令，可以直接运行 `sam deploy` 来代替，SAM CLI 会使用保存的配置文件 `samconfig.toml` 来简化交互。

    如果你得到相似的输出，这意味着你的 AWS Lambda 已经部署成功。

    ```
    Successfully created/updated stack - <stack_name> in <region>
    ```

4. 在 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home)中，你可看到方才上传的 Lambda。值得关注的是，你需要在窗口的右上角选择正确的机房，否则你无法看到 Lambda。

    ![lambda dashboard](/media/develop/aws-appflow-step-lambda-dashboard.png)

### 使用 Lambda 注册一个连接器

1. 在 [AWS Management 控制台](https://console.aws.amazon.com)中，切换到 [Amazon AppFlow > Connectors](https://console.aws.amazon.com/appflow/home#/gallery) 并点击 **Register new connector**.

    ![register connector](/media/develop/aws-appflow-step-register-connector.png)

2. 在 **Register a new connector** 对话框中，选择你方才上传的 Lambda 函数，并在 **Connector label** 框中为你的连接器命名。

    ![register connector dialog](/media/develop/aws-appflow-step-register-connector-dialog.png)

3. 点击 **Register**。随后，一个 TiDB 连接器将注册成功。

## 第 2 步：创建流

切换到 [Amazon AppFlow > Flows](https://console.aws.amazon.com/appflow/home#/list)，并点击 **Create flow**.

![create flow](/media/develop/aws-appflow-step-create-flow.png)

### 设置流名称

输入流名称，并点击 **Next**。

![name flow](/media/develop/aws-appflow-step-name-flow.png)

### 设置流的源与目标

选择 **Source details** 与 **Destination details**。TiDB 连接器同时支持这两种模式。

1. 选择源类型名称。这个文档将以 **Salesforce** 作为示例。

    ![salesforce source](/media/develop/aws-appflow-step-salesforce-source.png)

    在你注册 Salesforce 后，Salesforce 将添加一些示例数据到你的平台中。接下来的步骤将使用 **Account** 对象作为源数据。

    ![salesforce data](/media/develop/aws-appflow-step-salesforce-data.png)

2. 点击 **Connect**。

    1. 在 **Connect to Salesforce** 对话框中，指定此连接器的名称，并且点击 **Continue**。

        ![connect to salesforce](/media/develop/aws-appflow-step-connect-to-salesforce.png)

    2. 点击 **Allow** 来确认 AWS 可以读取你 Salesforce 的数据。

        ![allow salesforce](/media/develop/aws-appflow-step-allow-salesforce.png)

    > **注意：**
    >
    > 如果您的公司已经使用了 Salesforce 的 Professional Edition，REST API默认是不启用的。您可能需要注册一个新的 Developer Edition 来使用 REST API。你可以在此 [Salesforce 论坛主题](https://developer.salesforce.com/forums/?id=906F0000000D9Y2IAK)中了解更多信息。

3. 在 **Destination details** 区域，选择 **TiDB-Connector** 作为目标后，**Connect** 按钮将显示。

    ![tidb dest](/media/develop/aws-appflow-step-tidb-dest.png)

4. 点击 **Connect** 后，你需要在 TiDB 中，为 Salesforce 的 **Account** 对象创建一个 `sf_account` 表。值得注意的是，这个表的格式与 [Amazon AppFlow 教程](https://docs.aws.amazon.com/appflow/latest/userguide/flow-tutorial-set-up-source.html)中的不同。

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

5. 在 `sf_account` 表创建后，点击 **Connect**。将显示一个连接器对话框。
6. 在 **Connect to TiDB-Connector** 对话框中，输入 TiDB 集群的连接属性。如果你正在使用 TiDB Cloud Serverless Tier 集群，你需要设置 **TLS** 选项为 `Yes`。这将使你的 TiDB 连接器使用 TLS 连接。随后，点击 **Connect**。

    ![tidb connection message](/media/develop/aws-appflow-step-tidb-connection-message.png)

7. 现在，你可以获取到你指定数据库中的所有表。在下拉框中选择 **sf_account** 表.

    ![database](/media/develop/aws-appflow-step-database.png)

    下方截图展示了将 Salesforce 的 **Account** 对象转移到 TiDB 的 `sf_account` 表中的配置：

    ![complete flow](/media/develop/aws-appflow-step-complete-flow.png)

8. 在 **Error handling** 区域中，选择 **Stop the current flow run**。在 **Flow trigger** 区域中，选择 **Run on demand** 触发类型，这意味着你需要手动触发这个流。随后，点击 **Next**。

    ![complete step1](/media/develop/aws-appflow-step-complete-step1.png)

### 设置映射规则

映射 Salesforce 的 **Account** 对象字段到 TiDB 的 `sf_account` 表中，随后点击 **Next**.

- `sf_account` 表是新创建在 TiDB 中的，因此它是空的。

    ```sql
    test> SELECT * FROM sf_account;
    +----+------+------+---------------+--------+----------+
    | id | name | type | billing_state | rating | industry |
    +----+------+------+---------------+--------+----------+
    +----+------+------+---------------+--------+----------+
    ```

- 设置映射规则时，你可以在左侧选择源字段名称，再在右侧选择目标字段名称。随后，点击 **Map fields**，这样就成功完成了一条规则地设置。

    ![add mapping rule](/media/develop/aws-appflow-step-add-mapping-rule.png)

- 以下映射规则（**源字段名称** -> **目标字段名称**）在本教程中是必要的：

    - Account ID -> id
    - Account Name -> name
    - Account Type -> type
    - Billing State/Province -> billing_state
    - Account Rating -> rating
    - Industry -> industry

    ![mapping a rule](/media/develop/aws-appflow-step-mapping-a-rule.png)

    ![show all mapping rules](/media/develop/aws-appflow-step-show-all-mapping-rules.png)

### （可选）设置过滤器

如果你希望增加一些数据字段的过滤器，你可以在此处设置。否则，可点击 **Next** 以跳过此步骤。

![filters](/media/develop/aws-appflow-step-filters.png)

### 确认并创建流

确认即将创建的流信息。如果检查无误，点击 **Create flow**.

![review](/media/develop/aws-appflow-step-review.png)

## 第 2 步：运行流

在新创建的流页面中，在右上角点击 **Run flow**。

![run flow](/media/develop/aws-appflow-step-run-flow.png)

以下截图是流运行成功的一个示例：

![run success](/media/develop/aws-appflow-step-run-success.png)

查询 `sf_account` 表，你可以看到数据已经从 Salesforce 的 **Account** 对象中被写入至此：

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

## 值得注意的点

- 如果有任何错误出现，你可以在 AWS Management 控制它使用 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 页面来获取日志。
- 此文档的步骤基于 AWS Blog: [Building custom connectors using the Amazon AppFlow Custom Connector SDK](https://aws.amazon.com/blogs/compute/building-custom-connectors-using-the-amazon-appflow-custom-connector-sdk/)。
- [TiDB Cloud Serverless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta) **并非**生产环境。
- 为了防止篇幅过长，本文中的例子只展示了 `Insert` 策略，但 `Update` 和 `Upsert` 策略也经过测试，可以使用。