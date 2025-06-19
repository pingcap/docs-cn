---
title: 使用 node-mysql2 连接 TiDB
summary: 了解如何使用 node-mysql2 连接 TiDB。本教程提供使用 node-mysql2 操作 TiDB 的 Node.js 示例代码片段。
---

# 使用 node-mysql2 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [node-mysql2](https://github.com/sidorares/node-mysql2) 是一个快速的、兼容 [mysqljs/mysql](https://github.com/mysqljs/mysql) 的 Node.js MySQL 驱动程序。

在本教程中，您可以学习如何使用 TiDB 和 node-mysql2 完成以下任务：

- 设置环境。
- 使用 node-mysql2 连接到 TiDB 集群。
- 构建并运行应用程序。您也可以查看基本 CRUD 操作的[示例代码片段](#示例代码片段)。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，您需要：

- 在您的机器上安装 [Node.js](https://nodejs.org/en) >= 16.x。
- 在您的机器上安装 [Git](https://git-scm.com/downloads)。
- 一个正在运行的 TiDB 集群。

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)创建本地集群。

</CustomContent>

## 运行示例应用程序连接到 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart.git
cd tidb-nodejs-mysql2-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `mysql2` 和 `dotenv`）：

```shell
npm install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于您的现有项目，运行以下命令安装包：

```shell
npm install mysql2 dotenv --save
```

</details>

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接工具**设置为 `General`。
    - **操作系统**与您运行应用程序的操作系统匹配。

4. 如果您还没有设置密码，点击**生成密码**生成随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下设置环境变量，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

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

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请在首次连接之前点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按如下设置环境变量，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

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
    > 要启用 TLS 连接，将 `TIDB_ENABLE_SSL` 修改为 `true`，并使用 `TIDB_CA_PATH` 指定从连接对话框下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下设置环境变量，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

   如果您在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

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

您可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和如何运行它，请查看 [tidb-samples/tidb-nodejs-mysql2-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart) 仓库。

### 使用连接选项连接

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```javascript
// 步骤 1. 导入 'mysql' 和 'dotenv' 包。
import { createConnection } from "mysql2/promise";
import dotenv from "dotenv";
import * as fs from "fs";

// 步骤 2. 从 .env 文件加载环境变量到 process.env。
dotenv.config();

async function main() {
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
   const conn = await createConnection(options);

   // 步骤 4. 执行一些 SQL 操作...

   // 步骤 5. 关闭连接。
   await conn.end();
}

void main();
```

> **注意**
>
> 对于 TiDB Cloud Serverless，使用公共端点时，您**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。但是，您**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书受 TiDB Cloud Serverless 信任。

### 插入数据

以下查询创建一个 `Player` 记录并返回一个 `ResultSetHeader` 对象：

```javascript
const [rsh] = await conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询通过 ID `1` 返回一个 `Player` 记录：

```javascript
const [rows] = await conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `1` 的 `Player` 增加 `50` 个硬币和 `50` 个物品：

```javascript
const [rsh] = await conn.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息，请参见[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `1` 的 `Player` 记录：

```javascript
const [rsh] = await conn.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

- 使用[连接池](https://github.com/sidorares/node-mysql2#using-connection-pools)管理数据库连接可以减少频繁建立和销毁连接带来的性能开销。
- 为了避免 SQL 注入，建议使用[预处理语句](https://github.com/sidorares/node-mysql2#using-prepared-statements)。
- 在不涉及太多复杂 SQL 语句的场景中，使用 [Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/) 等 ORM 框架可以大大提高开发效率。
- 在处理数据库中的大数字（`BIGINT` 和 `DECIMAL` 列）时，建议启用 `supportBigNumbers: true` 选项。
- 建议启用 `enableKeepAlive: true` 选项，以避免因网络问题导致的套接字错误 `read ECONNRESET`。（相关问题：[sidorares/node-mysql2#683](https://github.com/sidorares/node-mysql2/issues/683)）

## 下一步

- 从 [node-mysql2 文档](https://github.com/sidorares/node-mysql2#readme)了解更多 node-mysql2 驱动程序的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
