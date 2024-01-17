---
title: 在 Next.js 中使用 mysql2 连接 TiDB
summary: 本文介绍了如何在 Next.js 中使用 TiDB 和 mysql2 构建一个 CRUD 应用程序，并提供了一个简单的代码示例。
---

# 在 Next.js 中使用 mysql2 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，[node-mysql2](https://github.com/sidorares/node-mysql2) 是一个与 [mysqljs/mysql](https://github.com/mysqljs/mysql) 兼容的面向 Node.js 的 MySQL 驱动，[Next.js](https://nextjs.org/) 是一个 React 框架，用于构建快速、可扩展的现代应用程序。

在本教程中，您将学习如何在 Next.js 中使用 TiDB 和 mysql2 来完成以下任务：

- 配置你的环境。
- 使用 node-mysql2 驱动连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Serverless 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 18.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

> **注意**
>
>要获取完整的代码片段和运行说明，请参考 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub存储库。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### 步骤 2：安装依赖

运行以下命令来安装示例应用程序所需的包（包括 mysql2 和 Next.js）：

```bash
npm install
```

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项，连接到您的 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 导航到 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在右上角点击 **Connect**。将显示一个连接对话框。

3. 确认对话框中的选项配置和你的运行环境一致。

    - **Endpoint Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为运行示例代码所在的操作系统。

    > **Note**
    >
    > 在 Node.js 应用程序中，您无需提供 SSL CA 证书，因为在建立 TLS（SSL）连接时，默认情况下 Node.js 使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 如果你还没有设置密码，点击 **Generate Password** 按钮生成一个随机的密码。

    > **Tip**
    >
    > 如果您之前生成过密码，您可以使用原始密码，或者点击 **Reset Password** 来生成一个新密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

7. 保存 `.env` 文件。

</div>

<div label="TiDB Self-Hosted">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    如果您在本地运行 TiDB，则默认的主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 步骤 4：运行示例应用程序

1. 运行示例应用程序:

   ```bash
   npm run dev
   ```

2. 打开您的浏览器并访问 `http://localhost:3000`（请查看您的终端以获取实际的端口号，默认为`3000`）。

3. 点击**RUN SQL**以执行示例代码。

4. 在终端中检查输出。如果输出类似于以下内容，则连接成功：

   ```json
   {
     "results": [
       {
         "Hello World": "Hello World"
       }
     ]
   }
   ```

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

要获取完整的示例代码和运行方式，请查看 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) 存储库。

### 连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```javascript
// src/lib/tidb.js
import mysql from 'mysql2';

let pool = null;

export function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // The password of TiDB user.
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

export function getPool() {
  if (!pool) {
    pool = createPool();
  }
  return pool;
}
```

### 插入数据

以下查询创建一个单独的 `Players` 记录并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

要了解更多信息，请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回一个 `Players` 记录，其 ID 为 `1`：

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

要了解更多信息，请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询将 `50` 个硬币和 `50` 个商品添加到 `ID` 为 `1` 的 `Player` 中：

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

要了解更多信息，请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除一个 `Players` 记录，其 ID 为 `1`：

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

要了解更多信息，请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 推荐使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)来管理数据库连接，以减少频繁建立和销毁连接所带来的性能开销。
- 为了避免 SQL 注入的风险，推荐使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)执行 SQL。
- 在不涉及大量复杂 SQL 语句的场景下，推荐使用 ORM 框架 (例如：[Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/)) 来提升你的开发效率。

## 下一步

- 要了解如何使用 ORM 和 Next.js 构建复杂应用程序的更多细节，请参阅我们的 [书店演示](https://github.com/pingcap/tidb-prisma-vercel-demo)。
- 关于 node-mysql2 的更多使用方法，可以参考 [node-mysql2 的 GitHub 仓库](https://github.com/sidorares/node-mysql2)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助吗？

访问我们的 [支持资源](/support.md) 以寻求帮助。
