---
title: 使用 mysql.js 连接 TiDB
summary: 学习如何使用 mysql.js 连接 TiDB。本教程提供使用 mysql.js 操作 TiDB 的 Node.js 示例代码片段。
---

# 使用 mysql.js 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [mysql.js](https://github.com/mysqljs/mysql) 驱动是一个纯 Node.js JavaScript 客户端，实现了 MySQL 协议。

在本教程中，你可以学习如何使用 TiDB 和 mysql.js 驱动完成以下任务：

- 设置环境。
- 使用 mysql.js 驱动连接到 TiDB 集群。
- 构建并运行应用程序。你也可以查看基本 CRUD 操作的[示例代码片段](#示例代码片段)。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，你需要：

- 在你的机器上安装 [Node.js](https://nodejs.org/zh-cn) >= 16.x。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 一个正在运行的 TiDB 集群。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#部署本地测试集群)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

## 运行示例程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart.git
cd tidb-nodejs-mysqljs-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例程序所需的包（包括 `mysql` 和 `dotenv`）：

```shell
npm install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于你的现有项目，运行以下命令安装包：

```shell
npm install mysql dotenv --save
```

</details>

### 步骤 3：配置连接信息

根据你选择的 TiDB 部署方式连接到 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群名称进入集群概览页面。

2. 点击右上角的**连接**，将显示连接对话框。

3. 确保连接对话框中的配置与你的运行环境相匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接方式**设置为 `General`。
    - **操作系统**与运行应用程序的操作系统匹配。

4. 如果你还没有设置密码，点击**生成密码**生成随机密码。

5. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下方式设置环境变量，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

    > **注意**
    >
    > 对于 TiDB Cloud Serverless，使用公共端点时**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群名称进入集群概览页面。

2. 点击右上角的**连接**，将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**专用端点**和 **VPC 对等连接**连接类型。更多信息，请参阅[连接到 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下方式设置环境变量，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH={downloaded_ssl_ca_path}
    ```

    > **注意**
    >
    > 使用公共端点连接到 TiDB Cloud Dedicated 时，建议启用 TLS 连接。
    >
    > 要启用 TLS 连接，请将 `TIDB_ENABLE_SSL` 修改为 `true`，并使用 `TIDB_CA_PATH` 指定从连接对话框下载的 CA 证书文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，将相应的占位符 `{}` 替换为集群的连接参数。示例配置如下：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    如果你在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：运行代码并检查结果

运行以下命令执行示例代码：

```shell
npm start
```

如果连接成功，控制台将输出 TiDB 集群的版本，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和如何运行它，请查看 [tidb-samples/tidb-nodejs-mysqljs-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart) 仓库。

### 使用连接选项连接

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```javascript
// 步骤 1. 导入 'mysql' 和 'dotenv' 包。
import { createConnection } from "mysql";
import dotenv from "dotenv";
import * as fs from "fs";

// 步骤 2. 从 .env 文件加载环境变量到 process.env。
dotenv.config();

// 步骤 3. 创建到 TiDB 集群的连接。
const options = {
    host: process.env.TIDB_HOST || '127.0.0.1',
    port: process.env.TIDB_PORT || 4000,
    user: process.env.TIDB_USER || 'root',
    password: process.env.TIDB_PASSWORD || '',
    database: process.env.TIDB_DATABASE || 'test',
    ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
        minVersion: 'TLSv1.2',
        ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
    } : null,
}
const conn = createConnection(options);

// 步骤 4. 执行一些 SQL 操作...

// 步骤 5. 关闭连接。
conn.end();
```

> **注意**
>
> 对于 TiDB Cloud Serverless，使用公共端点时，你**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。但是，你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书受 TiDB Cloud Serverless 信任。

### 插入数据

以下查询创建一条 `Player` 记录并返回新创建记录的 ID：

```javascript
conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100], (err, ok) => {
   if (err) {
       console.error(err);
   } else {
       console.log(ok.insertId);
   }
});
```

更多信息，请参阅[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询通过 ID `1` 返回一条 `Player` 记录：

```javascript
conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1], (err, rows) => {
   if (err) {
      console.error(err);
   } else {
      console.log(rows[0]);
   }
});
```

更多信息，请参阅[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 增加 `50` 个金币和 `50` 个商品：

```javascript
conn.query(
   'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
   [50, 50, 1],
   (err, ok) => {
      if (err) {
         console.error(err);
      } else {
          console.log(ok.affectedRows);
      }
   }
);
```

更多信息，请参阅[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```javascript
conn.query('DELETE FROM players WHERE id = ?;', [1], (err, ok) => {
    if (err) {
        reject(err);
    } else {
        resolve(ok.affectedRows);
    }
});
```

更多信息，请参阅[删除数据](/develop/dev-guide-delete-data.md)。

## 使用提示

- 使用[连接池](https://github.com/mysqljs/mysql#pooling-connections)管理数据库连接可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入攻击，建议在执行 SQL 之前使用[转义查询值](https://github.com/mysqljs/mysql#escaping-query-values)。

    > **注意**
    >
    > `mysqljs/mysql` 包尚不支持预处理语句，它只在客户端转义值（相关问题：[mysqljs/mysql#274](https://github.com/mysqljs/mysql/issues/274)）。
    >
    > 如果你想使用此功能来避免 SQL 注入或提高批量插入/更新的效率，建议使用 [mysql2](https://github.com/sidorares/node-mysql2) 包。

- 在没有大量复杂 SQL 语句的场景下，使用 ORM 框架可以提高开发效率，例如：[Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 和 [Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md)。
- 在处理数据库中的大数字（`BIGINT` 和 `DECIMAL` 列）时，建议启用 `supportBigNumbers: true` 选项。

## 下一步

- 从 [mysql.js 文档](https://github.com/mysqljs/mysql#readme)了解更多 mysql.js 驱动的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节了解 TiDB 应用程序开发的最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区寻求帮助，或者[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区寻求帮助，或者[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
