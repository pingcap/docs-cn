---
title: 使用 AWS CloudFormation 将 TiDB Cloud Serverless 与 Amazon Lambda 集成
summary: 逐步介绍如何将 TiDB Cloud Serverless 与 Amazon Lambda 和 CloudFormation 集成。
---

# 使用 AWS CloudFormation 将 TiDB Cloud Serverless 与 Amazon Lambda 集成

本文档提供了一个分步指南，介绍如何使用 [AWS CloudFormation](https://aws.amazon.com/cloudformation/) 将云原生分布式 SQL 数据库 [TiDB Cloud Serverless](https://www.pingcap.com/tidb-cloud/) 与无服务器和事件驱动的计算服务 [AWS Lambda](https://aws.amazon.com/lambda/) 集成。通过将 TiDB Cloud Serverless 与 Amazon Lambda 集成，你可以通过 TiDB Cloud Serverless 和 AWS Lambda 利用微服务的可扩展性和成本效益。AWS CloudFormation 自动化了 AWS 资源的创建和管理，包括 Lambda 函数、API Gateway 和 Secrets Manager。

## 解决方案概述

在本指南中，你将创建一个包含以下组件的功能完整的在线书店：

- AWS Lambda 函数：使用 Sequelize ORM 和 Fastify API 框架处理请求并从 TiDB Cloud Serverless 集群查询数据。
- AWS Secrets Manager SDK：检索和管理 TiDB Cloud Serverless 集群的连接配置。
- AWS API Gateway：处理 HTTP 请求路由。
- TiDB Cloud Serverless：云原生分布式 SQL 数据库。

AWS CloudFormation 用于创建项目所需的资源，包括 Secrets Manager、API Gateway 和 Lambda 函数。

书店项目的结构如下：

![AWS Lambda 结构概览](/media/develop/aws-lambda-structure-overview.png)

## 前提条件

在开始之前，请确保你具备以下条件：

- 一个可以访问以下 AWS 服务的 AWS 账户：
    - [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
    - [Secrets Manager](https://aws.amazon.com/secrets-manager/)
    - [API Gateway](https://aws.amazon.com/api-gateway/)
    - [Lambda services](https://aws.amazon.com/lambda/)
    - [S3](https://aws.amazon.com/s3/)
    - [IAM Roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- 一个 [TiDB Cloud](https://tidbcloud.com) 账户和一个 TiDB Cloud Serverless 集群。获取 TiDB Cloud Serverless 集群的连接信息：

    ![TiDB Cloud 连接信息](/media/develop/aws-lambda-tidbcloud-connection-info.png)

- API 测试工具，如 [Postman](https://www.postman.com/) 和 [cURL](https://curl.se/)。本文档中的大多数示例使用 cURL。对于 Windows 用户，建议使用 Postman。
- 将项目的[最新发布资产](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest)下载到本地计算机，其中包括 `cloudformation_template.yml` 和 `cloudformation_template.json` 文件。

> **注意：**
>
> - 创建 AWS 资源时，建议使用 `us-east-1` 作为集群区域。这是因为此演示中的 Lambda 函数代码将区域硬编码为 `us-east-1`，并且代码包存储在 `us-east-1` 区域。
> - 如果你使用不同的区域，需要按照以下说明修改 Lambda 函数代码，重新构建它，并将代码包上传到你自己的 S3 存储桶。

<details>
<summary>如果使用 <code>us-east-1</code> 以外的区域，请修改并重新构建 Lambda 函数代码</summary>

如果你使用 `us-east-1` 作为集群区域，请跳过本节并转到[步骤 1：使用 AWS CloudFormation 设置项目](#步骤-1-使用-aws-cloudformation-设置书店项目)。

如果你使用 `us-east-1` 以外的其他 AWS 区域来创建 AWS 资源，则需要修改 Lambda 函数代码，重新构建它，并将代码包上传到你自己的 S3 存储桶。

为避免本地开发环境问题，建议使用云原生开发环境，如 [Gitpod](https://www.gitpod.io/)。

要重新构建代码包并将其上传到你自己的 S3 存储桶，请执行以下操作：

1. 初始化开发环境。

    - 打开 [Gitpod](https://gitpod.io/#/https://github.com/pingcap/TiDB-Lambda-integration) 工作区并使用你的 GitHub 账户登录。

2. 修改 Lambda 函数代码。

    1. 在左侧边栏中打开 `aws-lambda-cloudformation/src/secretManager.ts` 文件。
    2. 找到第 22 行，然后修改 `region` 变量以匹配你自己的区域。

3. 重新构建代码包。

    1. 安装依赖项。

        1. 在 Gitpod 中打开终端。
        2. 进入工作目录：

            ```shell
            cd aws-lambda-cloudformation
            ```

        3. 安装依赖项：

            ```shell
            yarn
            ```

    2. 重新构建代码包。

        1. 构建代码包。

            ```shell
            yarn build
            ```

        2. 检查 `aws-lambda-cloudformation/dist/index.zip` 文件。
        3. 右键点击 `index.zip` 文件并选择**下载**。

4. 将重新构建的代码包上传到你自己的 S3 存储桶。

    1. 访问 AWS 管理控制台中的 [S3 服务](https://console.aws.amazon.com/s3)。
    2. 在你选择的区域中创建一个新的存储桶。
    3. 将 `index.zip` 文件上传到存储桶。
    4. 记下 S3 存储桶名称和区域，以供后续使用。

</details>

## 步骤 1. 使用 AWS CloudFormation 设置书店项目

要使用 AWS CloudFormation 设置书店项目，请执行以下操作：

1. 导航到 AWS 管理控制台并访问 [AWS CloudFormation 服务](https://console.aws.amazon.com/cloudformation)。
2. 点击**创建堆栈** > **使用新资源（标准）**。
3. 在**创建堆栈**页面，完成堆栈创建过程。

    1. 在**前提条件**区域，选择**选择现有模板**。
    2. 在**指定模板**区域，选择**上传模板文件**，点击**选择文件**上传模板文件（YAML 或 JSON），然后点击**下一步**。

        如果你还没有该文件，请从 [GitHub](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest) 下载。该文件包含用于创建项目所需资源的 AWS CloudFormation 模板。

        ![创建堆栈](/media/develop/aws-lambda-cf-create-stack.png)

    3. 指定堆栈详细信息。

        - 如果你使用 `us-east-1` 作为集群区域，请按照以下截图填写字段：

            ![指定 AWS Lambda 堆栈详细信息](/media/develop/aws-lambda-cf-stack-config.png)

            - **Stack name**：输入堆栈名称。
            - **S3Bucket**：输入存储 zip 文件的 S3 存储桶。
            - **S3Key**：输入 S3 密钥。
            - **TiDBDatabase**：输入 TiDB Cloud 集群名称。
            - **TiDBHost**：输入用于访问 TiDB Cloud 数据库的主机 URL。输入 `localhost`。
            - **TiDBPassword**：输入用于访问 TiDB Cloud 数据库的密码。
            - **TiDBPort**：输入用于访问 TiDB Cloud 数据库的端口。
            - **TiDBUser**：输入用于访问 TiDB Cloud 数据库的用户名。

        - 如果你使用 `us-east-1` 以外的其他 AWS 区域，请按照以下步骤操作：

            1. 参考[如果使用 `us-east-1` 以外的区域，请修改并重新构建 Lambda 函数代码](#前提条件)修改 Lambda 函数代码，重新构建它，并将代码包上传到你自己的 S3 存储桶。
            2. 在堆栈详细信息字段中，根据你自己的配置在 `S3Bucket` 和 `S3Key` 参数中指定 S3 存储桶名称和区域。
            3. 按照上述截图填写其他字段。

    4. 配置堆栈选项。你可以使用默认配置。

        ![配置堆栈选项](/media/develop/aws-lambda-cf-stack-config-option.png)

    5. 检查并创建堆栈。

        ![检查并创建堆栈](/media/develop/aws-lambda-cf-stack-config-review.png)

## 步骤 2. 使用书店项目

堆栈创建完成后，你可以按照以下方式使用项目：

1. 在 AWS 管理控制台中访问 [API Gateway 服务](https://console.aws.amazon.com/apigateway)，点击 `TiDBCloudApiGatewayV2` API，然后在左侧窗格中点击 **API: TiDBCloudApiGatewayV2**。

2. 从**概览**页面复制 `调用 URL`。此 URL 作为 API 端点。

    ![API Gateway 调用 URL](/media/develop/aws-lambda-get-apigateway-invoke-url.png)

3. 使用 API 测试工具（如 Postman 和 cURL）测试 API：

    - 初始化模拟图书：

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{"count":100}' https://<your-api-endpoint>/book/init
        ```

    - 获取所有图书：

        ```shell
        curl https://<your-api-endpoint>/book
        ```

    - 通过图书 ID 获取图书：

        ```shell
        curl https://<your-api-endpoint>/book/<book-id>
        ```

    - 创建图书：

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{ "title": "Book Title", "type": "Test", "publishAt": "2022-12-15T21:01:49.000Z", "stock": 123, "price": 12.34, "authors": "Test Test" }' https://<your-api-endpoint>/book
        ```

    - 更新图书：

        ```shell
        curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Book Title(updated)" }' https://<your-api-endpoint>/book/<book-id>
        ```

    - 删除图书：

        ```shell
        curl -X DELETE https://<your-api-endpoint>/book/<book-id>
        ```

## 步骤 3. 清理资源

为避免不必要的费用，请清理所有已创建的资源。

1. 访问 [AWS 管理控制台](https://console.aws.amazon.com/cloudformation)。
2. 删除你创建的 AWS CloudFormation 堆栈。
