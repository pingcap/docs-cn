---
title: 使用 node-mysql2 连接到 TiDB
summary: 本文描述了 TiDB 和 node-mysql2 的连接步骤，并给出了简单示例代码片段。
---

# 使用 node-mysql2 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[node-mysql2](https://github.com/sidorares/node-mysql2) 是一个与 [mysqljs/mysql](https://github.com/mysqljs/mysql) 兼容的面向 Node.js 的 MySQL 驱动。

本文档将展示如何使用 TiDB 和 node-mysql2 来完成以下任务：

- 配置你的环境。
- 使用 node-mysql2 驱动连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 16.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

如果你还没有 TiDB 集群，可以按照以下方式创建：

- （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart.git
cd tidb-nodejs-mysql2-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖 (包括 `mysql2` 和 `dotenv` 依赖包)：

```bash
npm install
```

在你现有的项目当中，你可以通过以下命令安装 `mysql2` 和 `dotenv` 依赖包（`dotenv` 用于从 `.env` 文件中读取环境变量）：

```bash
npm install mysql2 dotenv --save
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
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Generate Password** 按钮生成一个随机的密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为从连接对话框中复制的参数值：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DATABASE='test'
    TIDB_ENABLE_SSL='true'
    ```

   > **Note**
   >
   > 当你使用 Public Endpoint 连接 TiDB Serverless 集群时，**必须**启用 TLS 连接，请将 `TIDB_ENABLE_SSL` 修改为 `true`。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Dedicated 集群，进入集群的 **Overview** 页面。
2. 点击右上角的 **Connect** 按钮，将会出现连接对话框。
3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**，并点击 **CA cert** 下载 CA 文件。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 或按照[配置 IP 访问列表（英文）](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除 **Public** 连接类型外，TiDB Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。详情请参阅[连接 TiDB Dedicated 集群（英文）](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为从连接对话框中复制的参数值：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DATABASE='test'
    TIDB_ENABLE_SSL='true'
    TIDB_CA_PATH='{downloaded_ssl_ca_path}'
    ```

    > **Note**
    >
    > 推荐在使用 Public Endpoint 连接 TiDB Dedicated 集群时，启用 TLS 连接。
    >
    > 为了启用 TLS (SSL) 连接，将 `TIDB_ENABLE_SSL` 修改为 `true`，并使用 `TIDB_CA_PATH` 指定从连接对话框中下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>

<div label="本地部署的 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为你的 TiDB 集群的连接参数值：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DATABASE='test'
    ```

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 4 步：运行代码并查看结果

运行下述命令，执行示例代码：

```bash
npm run start
```

**预期输出结果：**

如果连接成功，你的终端将会输出所连接集群的版本信息：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v7.5.3)
⏳ Loading sample game data...
✅ Loaded sample game data.

🆕 Created a new player with ID 12.
ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-nodejs-mysql2-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart)。

### 连接到 TiDB

下面的代码使用环境变量中定义的连接选项来建立与 TiDB 集群的连接。

```javascript
// 步骤 1. 导入 'mysql2' 和 'dotenv' 依赖包。
import { createConnection } from "mysql2/promise";
import dotenv from "dotenv";
import * as fs from "fs";

// 步骤 2. 将连接参数从 .env 文件中读取到 process.env 中。
dotenv.config();

async function main() {
    // 步骤 3. 创建与 TiDB 集群的连接。
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

    // 步骤 4. 执行 SQL 语句。

    // 步骤 5. 关闭连接。
    await conn.end();
}

void main();
```

> **Note**
>
> 使用 Public Endpoint 连接 TiDB Serverless 时，**必须**启用 TLS 连接，请将 `TIDB_ENABLE_SSL` 修改为 `true`。但是你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书已被 TiDB Serverless 信任。

### 插入数据

```javascript
const [rsh] = await conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```javascript
const [rows] = await conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```javascript
const [rsh] = await conn.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```javascript
const [rsh] = await conn.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

- 推荐使用[连接池](https://sidorares.github.io/node-mysql2/docs#using-connection-pools)来管理数据库连接，以减少频繁建立和销毁连接所带来的性能开销。
- 为了避免 SQL 注入的风险，推荐使用[预处理语句](https://sidorares.github.io/node-mysql2/docs#using-prepared-statements)执行 SQL。
- 在不涉及大量复杂 SQL 语句的场景下，推荐使用 ORM 框架 (例如：[Sequelize](https://sequelize.org/)、[TypeORM](https://typeorm.io/) 或 [Prisma](https://www.prisma.io/)) 来提升你的开发效率。
- 当你在数据表中使用到 `BIGINT` 和 `DECIMAL` 类型列时，需要开启 Driver 的 `supportBigNumbers: true` 选项。
- 为了避免由于网络原因出现的 `read ECONNRESET` Socket 错误，可以在 Driver 上开启 `enableKeepAlive: true` 选项。（相关 Issue: [sidorares/node-mysql2#683](https://github.com/sidorares/node-mysql2/issues/683)）

## 下一步

- 关于 node-mysql2 的更多使用方法，可以参考 [node-mysql2 的 GitHub 仓库](https://github.com/sidorares/node-mysql2)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供了专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
