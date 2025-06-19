---
title: 使用 TypeORM 连接 TiDB
summary: 学习如何使用 TypeORM 连接 TiDB。本教程提供使用 TypeORM 操作 TiDB 的 Node.js 示例代码片段。
---

# 使用 TypeORM 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [TypeORM](https://github.com/TypeORM/TypeORM) 是一个流行的 Node.js 开源 ORM 框架。

在本教程中，你可以学习如何使用 TiDB 和 TypeORM 完成以下任务：

- 设置你的环境。
- 使用 TypeORM 连接到你的 TiDB 集群。
- 构建并运行你的应用程序。你也可以找到基本 CRUD 操作的[示例代码片段](#示例代码片段)。

> **注意**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed。

## 前提条件

要完成本教程，你需要：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) >= 16.x。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 一个正在运行的 TiDB 集群。

**如果你还没有 TiDB 集群，可以按照以下方式创建：**

<CustomContent platform="tidb">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)来创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建你自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)来创建本地集群。

</CustomContent>

## 运行示例程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 第 1 步：克隆示例程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### 第 2 步：安装依赖

运行以下命令来安装示例程序所需的包（包括 `typeorm` 和 `mysql2`）：

```shell
npm install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于你的现有项目，运行以下命令来安装这些包：

- `typeorm`：Node.js 的 ORM 框架。
- `mysql2`：Node.js 的 MySQL 驱动程序。你也可以使用 `mysql` 驱动程序。
- `dotenv`：从 `.env` 文件加载环境变量。
- `typescript`：将 TypeScript 代码编译为 JavaScript。
- `ts-node`：直接运行 TypeScript 代码而无需编译。
- `@types/node`：为 Node.js 提供 TypeScript 类型定义。

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
```

</details>

### 第 3 步：配置连接信息

根据你选择的 TiDB 部署选项连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接方式**设置为 `General`。
    - **操作系统**与运行应用程序的操作系统匹配。

4. 如果你还没有设置密码，点击**生成密码**来生成随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

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
    > 对于 TiDB Cloud Serverless，在使用公共端点时，你**必须**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择 **Public**，然后点击 **CA cert** 下载 CA 证书。

    如果你还没有配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。更多信息，请参阅[连接到你的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

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
    > 对于 TiDB Cloud Dedicated，在使用公共端点时**建议**通过 `TIDB_ENABLE_SSL` 启用 TLS 连接。当你设置 `TIDB_ENABLE_SSL=true` 时，你**必须**通过 `TIDB_CA_PATH=/path/to/ca.pem` 指定从连接对话框下载的 CA 证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下方式设置环境变量，将相应的占位符 `{}` 替换为你的 TiDB 集群的连接参数：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    如果你在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 第 4 步：初始化数据库架构

运行以下命令调用 TypeORM CLI 来使用 `src/migrations` 文件夹中迁移文件中编写的 SQL 语句初始化数据库：

```shell
npm run migration:run
```

<details>
<summary><b>预期执行输出</b></summary>

以下 SQL 语句创建一个 `players` 表和一个 `profiles` 表，这两个表通过外键关联。

```sql
query: SELECT VERSION() AS `version`
query: SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'migrations'
query: CREATE TABLE `migrations` (`id` int NOT NULL AUTO_INCREMENT, `timestamp` bigint NOT NULL, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB
query: SELECT * FROM `test`.`migrations` `migrations` ORDER BY `id` DESC
0 migrations are already loaded in the database.
1 migrations were found in the source code.
1 migrations are new migrations must be executed.
query: START TRANSACTION
query: CREATE TABLE `profiles` (`player_id` int NOT NULL, `biography` text NOT NULL, PRIMARY KEY (`player_id`)) ENGINE=InnoDB
query: CREATE TABLE `players` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `coins` decimal NOT NULL, `goods` int NOT NULL, `created_at` datetime NOT NULL, `profilePlayerId` int NULL, UNIQUE INDEX `uk_players_on_name` (`name`), UNIQUE INDEX `REL_b9666644b90ccc5065993425ef` (`profilePlayerId`), PRIMARY KEY (`id`)) ENGINE=InnoDB
query: ALTER TABLE `players` ADD CONSTRAINT `fk_profiles_on_player_id` FOREIGN KEY (`profilePlayerId`) REFERENCES `profiles`(`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
query: INSERT INTO `test`.`migrations`(`timestamp`, `name`) VALUES (?, ?) -- PARAMETERS: [1693814724825,"Init1693814724825"]
Migration Init1693814724825 has been  executed successfully.
query: COMMIT
```

</details>

迁移文件是从 `src/entities` 文件夹中定义的实体生成的。要了解如何在 TypeORM 中定义实体，请参考 [TypeORM：实体](https://typeorm.io/entities)。

### 第 5 步：运行代码并检查结果

运行以下命令执行示例代码：

```shell
npm start
```

**预期执行输出：**

如果连接成功，终端将输出 TiDB 集群的版本，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
🆕 Created a new player with ID 2.
ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可以参考以下示例代码片段来完成自己的应用程序开发。

要查看完整的示例代码及其运行方法，请查看 [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart) 仓库。

### 使用连接选项连接

以下代码使用环境变量中定义的选项建立与 TiDB 的连接：

```typescript
// src/dataSource.ts

// Load environment variables from .env file to process.env.
require('dotenv').config();

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.TIDB_HOST || '127.0.0.1',
  port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000,
  username: process.env.TIDB_USER || 'root',
  password: process.env.TIDB_PASSWORD || '',
  database: process.env.TIDB_DATABASE || 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
    minVersion: 'TLSv1.2',
    ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
  } : null,
  synchronize: process.env.NODE_ENV === 'development',
  logging: false,
  entities: [Player, Profile],
  migrations: [__dirname + "/migrations/**/*{.ts,.js}"],
});
```

> **注意**
>
> 对于 TiDB Cloud Serverless，在使用公共端点时，你必须启用 TLS 连接。在此示例代码中，请在 `.env` 文件中将环境变量 `TIDB_ENABLE_SSL` 设置为 `true`。
>
> 但是，你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书受 TiDB Cloud Serverless 信任。

### 插入数据

以下查询创建一条 `Player` 记录，并返回创建的 `Player` 对象，其中包含由 TiDB 生成的 `id` 字段：

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

更多信息，请参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回 ID 为 101 的单个 `Player` 对象，如果未找到记录则返回 `null`：

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

更多信息，请参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `101` 的 `Player` 添加 `50` 个物品：

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

更多信息，请参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `101` 的 `Player`：

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

更多信息，请参考[删除数据](/develop/dev-guide-delete-data.md)。

### 执行原始 SQL 查询

以下查询执行原始 SQL 语句（`SELECT VERSION() AS tidb_version;`）并返回 TiDB 集群的版本：

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

更多信息，请参考 [TypeORM：DataSource API](https://typeorm.io/data-source-api)。

## 实用说明

### 外键约束

使用[外键约束](https://docs.pingcap.com/tidb/stable/foreign-key)（实验性功能）通过在数据库端添加检查来确保数据的[参照完整性](https://en.wikipedia.org/wiki/Referential_integrity)。但是，这可能会在大数据量场景下导致严重的性能问题。

你可以使用 `createForeignKeyConstraints` 选项（默认值为 `true`）来控制在构建实体之间的关系时是否创建外键约束。

```typescript
@Entity()
export class ActionLog {
    @PrimaryColumn()
    id: number

    @ManyToOne((type) => Person, {
        createForeignKeyConstraints: false,
    })
    person: Person
}
```

更多信息，请参考 [TypeORM FAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation) 和[外键约束](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints)。

## 下一步

- 从 [TypeORM 的文档](https://typeorm.io/)了解更多 TypeORM 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 通过专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)学习，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
