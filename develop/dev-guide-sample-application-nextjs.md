---
title: 在 Next.js 中使用 mysql2 连接 TiDB
summary: 本文介绍如何在 Next.js 中使用 TiDB 和 mysql2 构建 CRUD 应用程序，并提供简单的示例代码。
---

# 在 Next.js 中使用 mysql2 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [mysql2](https://github.com/sidorares/node-mysql2) 是一个流行的 Node.js 驱动程序。

在本教程中，你将学习如何在 Next.js 中使用 TiDB 和 mysql2 完成以下任务：

- 设置环境
- 使用 mysql2 连接到 TiDB 集群
- 构建并运行应用程序。你还可以找到基本 CRUD 操作的[示例代码片段](#示例代码片段)

> **注意**
>
> 本教程适用于 TiDB Cloud Serverless 和自托管的 TiDB。

## 前提条件

完成本教程需要：

- [Node.js **18**](https://nodejs.org/en/download/) 或更高版本
- [Git](https://git-scm.com/downloads)
- TiDB 集群

<CustomContent platform="tidb">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 运行示例应用程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

> **注意**
>
> 完整的代码片段和运行说明，请参考 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub 仓库。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `mysql2`）：

```bash
npm install
```

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署选项连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1. 导航到[**集群**页面](https://tidbcloud.com/project/clusters)，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与你的操作环境相匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与你的环境匹配

    > **注意**
    >
    > 在 Node.js 应用程序中，你不需要提供 SSL CA 证书，因为 Node.js 在建立 TLS (SSL) 连接时默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)。

4. 点击**生成密码**创建随机密码。

    > **提示**
    >
    > 如果你之前已经创建过密码，可以使用原密码或点击**重置密码**生成新密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    将 `{}` 中的占位符替换为连接对话框中获得的值。

7. 保存 `.env` 文件。

</div>

<div label="TiDB 自托管">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    将 `{}` 中的占位符替换为**连接**窗口中获得的值。如果你在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 步骤 4：运行代码并检查结果

1. 启动应用程序：

   ```bash
   npm run dev
   ```

2. 打开浏览器并访问 `http://localhost:3000`。（检查终端中的实际端口号，默认为 `3000`）

3. 点击 **RUN SQL** 执行示例代码。

4. 检查终端中的输出。如果输出类似于以下内容，则连接成功：

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

你可以参考以下示例代码片段来完成自己的应用程序开发。

完整的示例代码和运行方法，请查看 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) 仓库。

### 连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```javascript
// src/lib/tidb.js
import mysql from 'mysql2';

let pool = null;

export function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB 主机，例如：{gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB 端口，默认：4000
    user: process.env.TIDB_USER, // TiDB 用户，例如：{prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB 用户的密码
    database: process.env.TIDB_DATABASE || 'test', // TiDB 数据库名称，默认：test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // 在 serverless 函数环境中将 connectionLimit 设置为 "1" 可以优化资源使用，降低成本，确保连接稳定性，并实现无缝扩展。
    maxIdle: 1, // 最大空闲连接数，默认值与 `connectionLimit` 相同
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

以下查询创建一个 `Player` 记录并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询通过 ID `1` 返回一个 `Player` 记录：

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 增加 `50` 个金币和 `50` 个物品：

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

## 实用注意事项

- 使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)管理数据库连接可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入，建议使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在不涉及太多复杂 SQL 语句的场景下，使用 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/) 等 ORM 框架可以大大提高开发效率。

## 下一步

- 要了解如何使用 ORM 和 Next.js 构建复杂应用程序的更多详细信息，请参阅[我们的书店演示](https://github.com/pingcap/tidb-prisma-vercel-demo)。
- 从 [node-mysql2 文档](https://sidorares.github.io/node-mysql2/docs/documentation)了解更多 node-mysql2 驱动程序的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
