---
title: 在 AWS Lambda 函数中使用 mysql2 连接 TiDB
summary: 本文介绍如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 构建 CRUD 应用程序，并提供简单的示例代码片段。
---

# 在 AWS Lambda 函数中使用 mysql2 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[AWS Lambda 函数](https://aws.amazon.com/lambda/)是一个计算服务，而 [mysql2](https://github.com/sidorares/node-mysql2) 是一个流行的 Node.js 开源驱动程序。

在本教程中，您可以学习如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 完成以下任务：

- 设置环境。
- 使用 mysql2 连接到 TiDB 集群。
- 构建并运行应用程序。您也可以查看[示例代码片段](#示例代码片段)，了解基本的 CRUD 操作。
- 部署 AWS Lambda 函数。

> **注意**
>
> 本教程适用于 TiDB Cloud Serverless 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- [Node.js **18**](https://nodejs.org/en/download/) 或更高版本。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。
- 一个具有管理员权限的 [AWS 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)。
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

如果您没有 AWS 账号或用户，可以按照 [Lambda 入门](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)指南中的步骤创建。

## 运行示例程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

> **注意**
>
> 有关完整的代码片段和运行说明，请参考 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub 仓库。

### 步骤 1：克隆示例程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `mysql2`）：

```bash
npm install
```

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与您的环境匹配。

    > **注意**
    >
    > 在 Node.js 应用程序中，您不必提供 SSL CA 证书，因为 Node.js 在建立 TLS (SSL) 连接时默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 点击**生成密码**创建随机密码。

    > **提示**
    >
    > 如果您之前已经生成了密码，可以使用原始密码或点击**重置密码**生成新密码。

5. 将相应的连接字符串复制并粘贴到 `env.json` 中。示例如下：

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
        "TIDB_PORT": "4000",
        "TIDB_USER": "{prefix}.root",
        "TIDB_PASSWORD": "{password}"
      }
    }
    ```

    将 `{}` 中的占位符替换为连接对话框中获得的值。

</div>

<div label="TiDB Self-Managed">

将相应的连接字符串复制并粘贴到 `env.json` 中。示例如下：

```json
{
  "Parameters": {
    "TIDB_HOST": "{tidb_server_host}",
    "TIDB_PORT": "4000",
    "TIDB_USER": "root",
    "TIDB_PASSWORD": "{password}"
  }
}
```

将 `{}` 中的占位符替换为**连接**窗口中获得的值。

</div>

</SimpleTab>

### 步骤 4：运行代码并检查结果

1. （前提条件）安装 [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建打包：

    ```bash
    npm run build
    ```

3. 调用示例 Lambda 函数：

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4. 检查终端中的输出。如果输出类似于以下内容，则连接成功：

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

确认连接成功后，您可以按照[下一节](#部署-aws-lambda-函数)部署 AWS Lambda 函数。

## 部署 AWS Lambda 函数

您可以使用 [SAM CLI](#sam-cli-部署推荐) 或 [AWS Lambda 控制台](#web-控制台部署)部署 AWS Lambda 函数。

### SAM CLI 部署（推荐）

1. （[前提条件](#前提条件)）安装 [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建打包：

    ```bash
    npm run build
    ```

3. 更新 [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml) 中的环境变量：

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4. 设置 AWS 环境变量（参考[短期凭证](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)）：

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5. 部署 AWS Lambda 函数：

    ```bash
    sam deploy --guided

    # 示例：

    # Configuring SAM deploy
    # ======================

    #        Looking for config file [samconfig.toml] :  Not found

    #        Setting default arguments for 'sam deploy'
    #        =========================================
    #        Stack Name [sam-app]: tidb-aws-lambda-quickstart
    #        AWS Region [us-east-1]:
    #        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
    #        Confirm changes before deploy [y/N]:
    #        #SAM needs permission to be able to create roles to connect to the resources in your template
    #        Allow SAM CLI IAM role creation [Y/n]:
    #        #Preserves the state of previously provisioned resources when an operation fails
    #        Disable rollback [y/N]:
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        Save arguments to configuration file [Y/n]:
    #        SAM configuration file [samconfig.toml]:
    #        SAM configuration environment [default]:

    #        Looking for resources needed for deployment:
    #        Creating the required resources...
    #        Successfully created!
    ```

### Web 控制台部署

1. 构建打包：

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2. 访问 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home#/functions)。

3. 按照[创建 Lambda 函数](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html)中的步骤创建一个 Node.js Lambda 函数。

4. 按照 [Lambda 部署包](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip)中的步骤上传 `dist/index.zip` 文件。

5. [复制并配置相应的连接字符串](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)到 Lambda 函数中。

    1. 在 Lambda 控制台的[函数](https://console.aws.amazon.com/lambda/home#/functions)页面中，选择**配置**标签，然后选择**环境变量**。
    2. 选择**编辑**。
    3. 要添加数据库访问凭证，请执行以下操作：
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_HOST`，在**值**中输入主机名。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_PORT`，在**值**中输入端口（默认为 4000）。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_USER`，在**值**中输入用户名。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_PASSWORD`，在**值**中输入创建数据库时选择的密码。
        - 选择**保存**。

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和运行方法，请查看 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) 仓库。

### 连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB 主机，例如：{gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB 端口，默认：4000
    user: process.env.TIDB_USER, // TiDB 用户，例如：{prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB 密码
    database: process.env.TIDB_DATABASE || 'test', // TiDB 数据库名称，默认：test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // 在无服务器函数环境中将 connectionLimit 设置为 "1" 可以优化资源使用，降低成本，确保连接稳定性，并实现无缝扩展。
    maxIdle: 1, // 最大空闲连接数，默认值与 `connectionLimit` 相同
    enableKeepAlive: true,
  });
}

export function getPool(): mysql.Pool {
  if (!pool) {
    pool = connect();
  }
  return pool;
}
```

### 插入数据

以下查询创建一个 `Player` 记录并返回一个 `ResultSetHeader` 对象：

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回 ID 为 `1` 的单个 `Player` 记录：

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 添加 `50` 个金币和 `50` 个物品：

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

- 使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)管理数据库连接可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入，建议使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在不涉及太多复杂 SQL 语句的场景中，使用 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/) 等 ORM 框架可以大大提高开发效率。
- 要为应用程序构建 RESTful API，建议[将 AWS Lambda 与 API Gateway 结合使用](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)。
- 有关使用 TiDB Cloud Serverless 和 AWS Lambda 设计高性能应用程序，请参考[此博客](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)。

## 下一步

- 有关如何在 AWS Lambda 函数中使用 TiDB 的更多详细信息，请参见我们的 [TiDB-Lambda-integration/aws-lambda-bookstore Demo](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)。您还可以使用 AWS API Gateway 为您的应用程序构建 RESTful API。
- 从 [`mysql2` 文档](https://sidorares.github.io/node-mysql2/docs/documentation)了解更多 `mysql2` 的用法。
- 从 [`Lambda` 的 AWS 开发者指南](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)了解更多 AWS Lambda 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
