---
title: 在 Next.js 中使用 mysql2 连接到 TiDB
summary: 本文介绍了如何在 Next.js 中使用 TiDB 和 mysql2 构建一个 CRUD 应用程序，并给出了简单示例代码片段。
---

# 在 Next.js 中使用 mysql2 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库，[mysql2](https://github.com/sidorares/node-mysql2) 是当前流行的开源 Node.js Driver 之一。

本文档将展示如何在 Next.js 中使用 TiDB 和 mysql2 来完成以下任务：

- 配置你的环境。
- 使用 mysql2 驱动连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **Note**
>
> 本文档适用于 TiDB Serverless 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 18.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

如果你还没有 TiDB 集群，可以按照以下方式创建：

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

> **Note**
>
> 完整代码及其运行方式，见代码仓库 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart)。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 mysql2 和 Next.js）：

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

    - **Endpoint Type** 为 `Public`。
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

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为从连接对话框中复制的参数值：

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

7. 保存 `.env` 文件。

</div>

<div label="本地部署的 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为你的 TiDB 集群的连接参数值：

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    如果你在本地运行 TiDB 集群，默认的主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 4 步：运行代码并查看结果

1. 运行示例应用程序：

    ```bash
    npm run dev
    ```

2. 打开浏览器，在地址栏输入 `http://localhost:3000`，访问示例应用程序。请查看你的终端以获取实际的端口号，默认为 `3000`。

3. 点击 **RUN SQL** 执行示例代码。

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

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart)。

### 连接到 TiDB

下面的代码使用环境变量中定义的连接选项来建立与 TiDB 集群的连接。

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

下面的查询会创建一条单独的 `Player` 记录，并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

下面的查询会返回一条 `Player` 记录，其 ID 为 `1`：

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

下面的查询会将 ID 为 `1` 的 `Player` 记录的 `coins` 和 `goods` 字段的值分别增加 `50`：

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

下面的查询会删除一条 `Player` 记录，其 ID 为 `1`：

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 推荐使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)来管理数据库连接，以减少频繁建立和销毁连接所带来的性能开销。
- 为了避免 SQL 注入的风险，推荐使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)执行 SQL。
- 在不涉及大量复杂 SQL 语句的场景下，推荐使用 ORM 框架（例如：[Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/)）来提升你的开发效率。

## 下一步

- 关于使用 ORM 框架和 Next.js 构建复杂应用程序的更多细节，可以参考 [tidb-prisma-vercel-demo](https://github.com/pingcap/tidb-prisma-vercel-demo)。
- 关于 mysql2 的更多使用方法，可以参考 [mysql2 的官方文档](https://sidorares.github.io/node-mysql2/zh-CN/docs)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://pingkai.cn/learn)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.cn/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，或从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。
