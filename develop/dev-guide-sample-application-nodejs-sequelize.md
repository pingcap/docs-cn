---
title: 使用 Sequelize 连接到 TiDB
summary: 本文描述了 TiDB 和 Sequelize 的连接步骤，并给出了简单示例代码片段。
---

# 使用 Sequelize 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Sequelize](https://sequelize.org/) 是当前流行的 Node.js ORM 框架之一。

本文档将展示如何使用 TiDB 和 Sequelize 来构造一个简单的 CRUD 应用程序。

- 配置你的环境。
- 使用 Sequelize 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 18.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

**如果您没有 TiDB 集群，可以按照以下步骤创建一个：**

- （推荐）请按照 [创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md) 的指引，创建您自己的 TiDB Cloud 集群。
- 按照 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产 TiDB 集群](/production-deployment-using-tiup.md) 的指引，创建一个本地集群。

## 运行示例应用程序并连接到 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

> **注意**
>
> 完整的代码片段和运行说明，请参考 [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart) GitHub 仓库。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```bash
git clone git@github.com:tidb-samples/tidb-nodejs-sequelize-quickstart.git
cd tidb-nodejs-sequelize-quickstart
```

### 步骤 2：安装依赖

运行以下命令来安装示例应用程序所需的包（包括 sequelize）：

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
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    ```

7. 保存 `.env` 文件。

</div>

<div label="TiDB Dedicated">

1. 导航到 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

2. 在右上角点击 **Connect**。将显示一个连接对话框。

3. 点击 **Allow Access from Anywhere**，然后点击 **Download TiDB cluster CA** 来下载 CA 证书。

    要了解更多关于如何获取连接字符串的详细信息，请参考 [TiDB Dedicated 标准连接](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```shell
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    TIDB_ENABLE_SSL='true'
    TIDB_CA_PATH='{path/to/ca}'
    ```

6. 保存 `.env` 文件。

</div>

<div label="TiDB Self-Hosted">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```shell
    TIDB_HOST='{host}'
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

运行以下命令来执行示例代码：

```shell
npm start
```

<details>
<summary>**预期输出（部分）：**</summary>

```shell
INFO (app/10117): Getting sequelize instance...
Executing (default): SELECT 1+1 AS result
Executing (default): DROP TABLE IF EXISTS `players`;
Executing (default): CREATE TABLE IF NOT EXISTS `players` (`id` INTEGER NOT NULL auto_increment  COMMENT 'The unique ID of the player.', `coins` INTEGER NOT NULL COMMENT 'The number of coins that the player had.', `goods` INTEGER NOT NULL COMMENT 'The number of goods that the player had.', `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB;
Executing (default): SHOW INDEX FROM `players`
Executing (default): INSERT INTO `players` (`id`,`coins`,`goods`,`createdAt`,`updatedAt`) VALUES (1,100,100,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(2,200,200,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(3,300,300,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(4,400,400,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(5,500,500,'2023-08-31 09:10:11','2023-08-31 09:10:11');
Executing (default): SELECT `id`, `coins`, `goods`, `createdAt`, `updatedAt` FROM `players` AS `players` WHERE `players`.`coins` > 300;
Executing (default): UPDATE `players` SET `coins`=?,`goods`=?,`updatedAt`=? WHERE `id` = ?
Executing (default): DELETE FROM `players` WHERE `id` = 6
```

</details>

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-nodejs-sequelize-quickstart](https://github.com/tidb-samples/tidb-nodejs-sequelize-quickstart)。

### 连接到 TiDB

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```typescript
// src/lib/tidb.ts
import { Sequelize } from 'sequelize';

export function initSequelize() {
  return new Sequelize({
    dialect: 'mysql',
    host: process.env.TIDB_HOST || 'localhost',     // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: Number(process.env.TIDB_PORT) || 4000,    // TiDB port, default: 4000
    username: process.env.TIDB_USER || 'root',      // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD || 'root',  // TiDB password
    database: process.env.TIDB_DB_NAME || 'test',   // TiDB database name, default: test
    dialectOptions: {
      ssl:
        process.env?.TIDB_ENABLE_SSL === 'true'     // (Optional) Enable SSL
          ? {
              minVersion: 'TLSv1.2',
              rejectUnauthorized: true,
              ca: process.env.TIDB_CA_PATH          // (Optional) Path to the custom CA certificate
                ? readFileSync(process.env.TIDB_CA_PATH)
                : undefined,
            }
          : null,
    },
}

export async function getSequelize() {
  if (!sequelize) {
    sequelize = initSequelize();
    try {
      await sequelize.authenticate();
      logger.info('Connection has been established successfully.');
    } catch (error) {
      logger.error('Unable to connect to the database:');
      logger.error(error);
      throw error;
    }
  }
  return sequelize;
}
```

### 插入数据

以下查询创建一个单独的 `Players` 记录并返回一个 `Players` 对象：

```typescript
logger.info('Creating a new player...');
const newPlayer = await playersModel.create({
  id: 6,
  coins: 600,
  goods: 600,
});
logger.info('Created a new player.');
logger.info(newPlayer.toJSON());
```

要了解更多信息，请参考 [插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回一个 `Players` 记录，其金币数量大于 `300`：

```typescript
logger.info('Reading all players with coins > 300...');
const allPlayersWithCoinsGreaterThan300 = await playersModel.findAll({
  where: {
    coins: {
      [Op.gt]: 300,
    },
  },
});
logger.info('Read all players with coins > 300.');
logger.info(allPlayersWithCoinsGreaterThan300.map((p) => p.toJSON()));
```

要了解更多信息，请参考 [查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询将 `ID` 为 `6` 的 `Players` 的金币数量和物品数量设置为 `700`，这个记录是在 [插入数据](#插入数据) 部分创建的：

```typescript
logger.info('Updating the new player...');
await newPlayer.update({ coins: 700, goods: 700 });
logger.info('Updated the new player.');
logger.info(newPlayer.toJSON());
```

要了解更多信息，请参考 [更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除了在 [插入数据](#插入数据) 部分创建的 `Player` 记录，其 `ID` 为 `6`：

```typescript
logger.info('Deleting the new player...');
await newPlayer.destroy();
const deletedNewPlayer = await playersModel.findByPk(6);
logger.info('Deleted the new player.');
logger.info(deletedNewPlayer?.toJSON());
```

要了解更多信息，请参考 [删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 从 [Sequelize的文档](https://sequelize.org/) 中了解更多关于ORM框架Sequelize驱动程序的用法。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助吗？

访问我们的 [支持资源](/support.md) 以寻求帮助。
