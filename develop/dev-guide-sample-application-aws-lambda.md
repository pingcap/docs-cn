---
title: 在 AWS Lambda 函数中使用 mysql2 连接到 TiDB
summary: 本文介绍如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 构建一个 CRUD 应用程序，并给出了简单示例代码片段。
---

# 在 AWS Lambda 函数中使用 mysql2 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[AWS Lambda 函数](https://aws.amazon.com/lambda/)是一个计算服务，[mysql2](https://github.com/sidorares/node-mysql2) 是当前流行的开源 Node.js Driver 之一。

本文档将展示如何在 AWS Lambda 函数中使用 TiDB 和 mysql2 来完成以下任务：

- 配置你的环境。
- 使用 mysql2 驱动连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。
- 部署你的 AWS Lambda 函数。

> **Note**
>
> 本文档适用于 TiDB Serverless 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 18.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。
- 准备一个具有管理员权限的 [AWS IAM 用户](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_users.html)。
- 在你的机器上安装 [AWS CLI](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/getting-started-install.html)。
- 在你的机器上安装 [AWS SAM CLI](https://docs.aws.amazon.com/zh_cn/serverless-application-model/latest/developerguide/install-sam-cli.html)。

如果你还没有 TiDB 集群，可以按照以下方式创建：

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

如果你还没有 AWS 账户或用户，可以按照 [Lambda 入门](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/getting-started.html)文档中的步骤来创建它们。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

> **Note**
>
> 完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart)。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 mysql2）：

```bash
npm install
```

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的选项配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为运行示例代码所在的操作系统。

    > **Note**
    >
    > 在 Node.js 应用程序中，你无需提供 SSL CA 证书，因为在建立 TLS (SSL) 连接时，默认情况下 Node.js 使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 如果你还没有设置密码，点击 **Generate Password** 按钮生成一个随机的密码。

    > **Tip**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 编辑 `env.json` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为从连接对话框中复制的参数值：

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

</div>

<div label="本地部署的 TiDB">

编辑 `env.json` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为你的 TiDB 集群的连接参数值：

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

</div>

</SimpleTab>

### 第 4 步：运行代码并查看结果

1. （前置需求）安装 [AWS SAM CLI](https://docs.aws.amazon.com/zh_cn/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建应用程序包：

    ```bash
    npm run build
    ```

3. 调用示例 Lambda 函数：

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4. 检查终端中的输出。如果输出类似于以下内容，则表示连接成功：

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

确认连接成功后，你可以按照[部署 AWS Lambda 函数](#部署-aws-lambda-函数)中的步骤进行部署。

## 部署 AWS Lambda 函数

你可以通过 [SAM CLI](#通过-sam-cli-部署推荐) 或 [AWS Lambda 控制台](#通过网页控制台部署)部署 AWS Lambda 函数。

### 通过 SAM CLI 部署（推荐）

1. （[前置需求](#前置需求)）安装 [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)。

2. 构建应用程序包：

    ```bash
    npm run build
    ```

3. 更新 [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml) 文件中的环境变量：

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4. 参考[使用短期凭证进行身份验证](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-authentication-short-term.html)文档，设置 AWS 环境变量：

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5. 部署 AWS Lambda 函数：

    ```bash
    sam deploy --guided

    # Example:

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

### 通过网页控制台部署

1. 构建应用程序包：

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2. 访问 [AWS Lambda 控制台](https://console.aws.amazon.com/lambda/home#/functions)。

3. 按照[使用 Node.js 构建 Lambda 函数](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/lambda-nodejs.html)中的步骤创建一个 Node.js Lambda 函数。

4. 按照 [Lambda 部署程序包](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip)中的步骤，上传 `dist/index.zip` 文件。

5. 在 Lambda 函数中[复制并配置相应的连接字符串](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/configuration-envvars.html)。

    1. 在 Lambda 控制台的[**函数**](https://console.aws.amazon.com/lambda/home#/functions)页面中，选择**配置** > **环境变量**。
    2. 点击**编辑**。
    3. 按照以下步骤添加数据库访问凭证：

        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_HOST`，在**值**中输入主机名。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_PORT`，在**值**中输入端口号（默认 `4000`）。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_USER`，在**值**中输入用户名。
        - 选择**添加环境变量**，然后在**键**中输入 `TIDB_PASSWORD`，在**值**中输入数据库的密码。
        - 点击**保存**。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart)。

### 连接到 TiDB

下面的代码使用环境变量中定义的连接选项来建立与 TiDB 集群的连接。

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB password
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
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

下面的查询会创建一条单独的 `Player` 记录，并返回一个 `ResultSetHeader` 对象：

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

下面的查询会返回一条 `Player` 记录，其 ID 为 `1`：

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

下面的查询会将 ID 为 `1` 的 `Player` 记录的 `coins` 和 `goods` 字段的值分别增加 `50`：

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

下面的查询会删除一条 `Player` 记录，其 ID 为 `1`：

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 推荐使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)来管理数据库连接，以减少频繁建立和销毁连接所带来的性能开销。
- 为了避免 SQL 注入的风险，推荐使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)执行 SQL。
- 在不涉及大量复杂 SQL 语句的场景下，推荐使用 ORM 框架（例如：[Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/)）来提升你的开发效率。
- 如需为你的应用程序构建一个 RESTful API，建议[将 AWS Lambda 与 Amazon API Gateway 结合使用](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/services-apigateway.html)。
- 关于使用 TiDB Serverless 和 AWS Lambda 设计高性能应用程序的更多信息，可以参考[这篇博客](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)。

## 下一步

- 关于在 AWS Lambda 函数中使用 TiDB 的更多细节，可以参考 [`TiDB-Lambda-integration/aws-lambda-bookstore` 示例程序](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)。你也可以使用 AWS API Gateway 为你的应用程序构建 RESTful API。
- 关于 mysql2 的更多使用方法，可以参考 [mysql2 的官方文档](https://sidorares.github.io/node-mysql2/zh-CN/docs)。
- 关于 AWS Lambda 的更多使用方法，可以参考 [AWS Lambda 开发者指南](https://docs.aws.amazon.com/zh_cn/lambda/latest/dg/welcome.html)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://pingkai.cn/learn)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.cn/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，或从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。
