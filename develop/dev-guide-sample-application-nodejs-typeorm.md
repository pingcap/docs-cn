---
title: 使用 TypeORM 连接到 TiDB
summary: 本文描述了 TiDB 和 TypeORM 的连接步骤，并给出了简单示例代码片段。
---

# 使用 TypeORM 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[TypeORM](https://typeorm.io/) 是当前流行的 Node.js ORM 框架之一。

本文档将展示如何使用 TiDB 和 TypeORM 来完成以下任务：

- 配置你的环境。
- 使用 TypeORM 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和本地部署的 TiDB。

## 前置需求

为了能够顺利完成本教程，你需要提前：

- 在你的机器上安装 [Node.js](https://nodejs.org/en) 16.x 或以上版本。
- 在你的机器上安装 [Git](https://git-scm.com/downloads)。
- 准备一个 TiDB 集群。

如果你还没有 TiDB 集群，可以按照以下方式创建：

- （推荐方式）参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 `typeorm` 和 `mysql2` 依赖包）：

```bash
npm install
```

<details>
<summary><b>在现有的项目中安装依赖</b></summary>

在你现有的项目当中，你可以通过以下命令安装所需要的依赖包：

- `typeorm`：面向 Node.js 应用的 ORM 框架。
- `mysql2`：面向 Node.js 的 MySQL Driver 包。你也可以使用 `mysql`。
- `dotenv`：用于从 `.env` 文件中读取环境变量。
- `typescript`：TypeScript 编译器。
- `ts-node`：用于在不编译的情况下直接执行 TypeScript 代码。
- `@types/node`：用于提供 Node.js 的 TypeScript 类型定义。

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
```

</details>

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Serverless 集群，进入集群的 **Overview** 页面。

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
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

    > **Note**
    >
    > 当你使用 Public Endpoint 连接 TiDB Cloud Serverless 集群时，**必须**启用 TLS 连接，请将 `TIDB_ENABLE_SSL` 修改为 `true`。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Cloud Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Dedicated 集群，进入集群的 **Overview** 页面。
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
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH={downloaded_ssl_ca_path}
    ```

    > **Note**
    >
    > 推荐在使用 Public Endpoint 连接 TiDB Cloud Dedicated 集群时，启用 TLS 连接。为了启用 TLS (SSL) 连接，将 `TIDB_ENABLE_SSL` 修改为 `true`，并使用 `TIDB_CA_PATH` 指定从连接对话框中下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。

</div>

<div label="本地部署的 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为你的 TiDB 集群的连接参数值：

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 4 步：初始化表结构

运行以下命令，使用 TypeORM CLI 初始化数据库。TypeORM CLI 会根据 `src/migrations` 文件夹中的迁移文件生成 SQL 语句并执行。

```shell
npm run migration:run
```

<details>
<summary><b>预期的执行输出</b></summary>

下面的 SQL 语句创建了 `players` 表和 `profiles` 表，并通过外键关联了两个表。

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

迁移文件是根据 `src/entities` 文件夹中定义的实体生成的。要了解如何在 TypeORM 中定义实体，请参考 [TypeORM: Entities](https://typeorm.io/entities)。

### 第 5 步：运行代码并查看结果

运行以下命令，执行示例代码：

```shell
npm start
```

**预期输出结果：**

如果连接成功，你的终端将会输出所连接集群的版本信息：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.3.0)
🆕 Created a new player with ID 2.
ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
🚮 Deleted 1 player data.
```

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart)。

### 连接到 TiDB

下面的代码使用环境变量中定义的连接选项来建立与 TiDB 集群的连接。

```typescript
// src/dataSource.ts

// 加载 .env 文件中的环境变量到 process.env。
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

> **Note**
>
> 使用 Public Endpoint 连接 TiDB Cloud Serverless 时，**必须**启用 TLS 连接，请将 `TIDB_ENABLE_SSL` 修改为 `true`。
>
> 但是你**不需要**通过 `TIDB_CA_PATH` 指定 SSL CA 证书，因为 Node.js 默认使用内置的 [Mozilla CA 证书](https://wiki.mozilla.org/CA/Included_Certificates)，该证书已被 TiDB Cloud Serverless 信任。

### 插入数据

下面的代码创建了一条 `Player` 记录，并返回该记录的 `id` 字段，该字段由 TiDB 自动生成：

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

下面的代码查询 ID 为 101 的 `Player` 记录，如果没有找到则返回 `null`：

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

下面的代码将 `Player` 记录的 `goods` 字段增加 `50`：

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

下面的代码删除 ID 为 `101` 的 `Player` 记录：

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

### 执行原生 SQL 查询

下面的代码执行原生 SQL 语句 (`SELECT VERSION() AS tidb_version;`) 并返回 TiDB 集群的版本信息：

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

更多信息参考 [TypeORM: DataSource API](https://typeorm.io/data-source-api)。

## 注意事项

### 外键约束

使用[外键约束](/foreign-key.md)（实验特性）可以通过在数据库层面添加检查来确保数据的[引用完整性](https://zh.wikipedia.org/wiki/参照完整性)。但是，在大数据量的场景下，这可能会导致严重的性能问题。

你可以通过使用 `createForeignKeyConstraints` 选项来控制在构建实体之间的关系时是否创建外键约束（默认值为 `true`）。

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

更多信息，请参考 [TypeORM FAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation) 和 [TiDB 外键约束](/foreign-key.md)。

## 下一步

- 关于 TypeORM 的更多使用方法，可以参考 [TypeORM 的官方文档](https://typeorm.io)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。
