---
title: 使用 Prisma 连接到 TiDB
summary: 本文描述了 TiDB 和 Prisma 的连接步骤，并给出了简单示例代码片段。
---

# 使用 Prisma 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Prisma](https://www.prisma.io/) 是当前流行的 Node.js ORM 框架之一。

本文档将展示如何使用 TiDB 和 Prisma 来构造一个简单的 CRUD 应用程序。

- 配置你的环境。
- 使用 Prisma 连接到 TiDB 集群。
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
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖 (包括 `prisma` 依赖包)：

```bash
npm install
```

在你现有的项目当中，你可以通过以下命令安装所需要的依赖包：

```bash
npm install prisma typescript ts-node @types/node --save-dev
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
    - **Connect With** 选择 `Prisma`。
    - **Operating System** 为运行示例代码所在的操作系统。

    > **Note**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Generate Password** 按钮生成一个随机的密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的连接字符串：

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **Note**
    >
    > 在使用 Public Endpoint 连接 TiDB Serverless 集群时，**必须**启用 TLS 连接，请将 `sslaccept` 参数设置为 `strict`。

7. 保存 `.env` 文件。
8. 在 `prisma/schema.prisma` 文件中，将 `provider` 修改为 `mysql`，并将 `url` 修改为 `env("DATABASE_URL")`：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

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

5. 编辑 `.env` 文件，按照如下格式设置环境变量 `DATABASE_URL`，将占位符 `{}` 替换为从连接对话框中复制的参数值：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

   > **Note**
   >
   > 推荐在使用 Public Endpoint 连接 TiDB Dedicated 集群时，启用 TLS 连接。
   >
   > 为了启用 TLS (SSL) 连接，将 `DATABASE_URL` 末尾添加 `sslaccept=strict` 参数，并使用 `sslcert=/path/to/ca.pem` 参数指定从连接对话框中下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。
7. 在 `prisma/schema.prisma` 文件中，将 `provider` 修改为 `mysql`，并将 `url` 修改为 `env("DATABASE_URL")`：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>

<div label="本地部署的 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按照如下格式设置连接信息，将占位符 `{}` 替换为你的 TiDB 集群的连接参数值：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

   如果你在本地运行 TiDB 集群，默认的 Host 是 `127.0.0.1`, 默认用户名为 `root`, 密码为空。

3. 保存 `.env` 文件。
4. 在 `prisma/schema.prisma` 文件中，将 `provider` 修改为 `mysql`，并将 `url` 修改为 `env("DATABASE_URL")`：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>

</SimpleTab>

### 第 4 步：初始化表结构

运行以下命令，使用 [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) 根据 `prisma/schema.prisma` 文件中的数据模型定义来初始化数据库表结构：

```shell
npx prisma migrate dev
```

**`prisma.schema` 文件中的模型定义：**

```prisma
// 定义一个 Player 模型，表示 `players` 表。
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// 定义一个 Profile 模型，表示 `profiles` 表。
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // 定义 `Player` 和 `Profile` 模型之间的 1:1 关系，并使用外键约束。
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

你可以通过查阅 Prisma 的 [Data model](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model) 文档来了解如何在 `prisma.schema` 文件里定义数据模型。

**预期执行结果：**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

这个命令同时会根据 `prisma/schema.prisma` 文件中的模型定义，生成用于与数据库交互的 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client) 的代码。

### 第 5 步：运行代码并查看结果

运行下述命令，执行示例代码：

```bash
npm start
```

**示例代码中的主要逻辑：**

```typescript
// 步骤 1. 导入自动生成的 `@prisma/client` 依赖包。
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // 步骤 2. 创建一个新的 `PrismaClient` 实例。
  const prisma = new PrismaClient();
  try {

    // 步骤 3. 使用 Prisma Client 执行一些 CRUD 操作。

  } finally {
    // 步骤 4. 断开 Prisma Client 的连接。
    await prisma.$disconnect();
  }
}

void main();
```

**预期输出结果：**

如果连接成功，在你的终端上会输出所连接集群的版本信息。

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.1)
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart)。

### 插入数据

下面的查询会创建一条新的 `Player` 记录，并返回一个包含自增 ID 的 `Player` 对象：

```typescript
const player: Player = await prisma.player.create({
  data: {
    name: 'Alice',
    coins: 100,
    goods: 200,
    createdAt: new Date(),
  }
});
console.log(player.id);
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

下面的查询会返回 ID 为 `101` 的 `Player` 记录，如果没有找到对应的记录，会返回 `null`：

```javascript
const player: Player | null = prisma.player.findUnique({
    where: {
        id: 101,
    }
});
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

下面的查询会将 ID 为 `101` 的 `Player` 记录的 `coins` 和 `goods` 字段的值分别增加 50：

```typescript
await prisma.player.update({
  where: {
    id: 101,
  },
  data: {
    coins: {
      increment: 50,
    },
    goods: {
      increment: 50,
    },
  }
});
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

下面的查询会删除 ID 为 `101` 的 `Player` 记录：

```typescript
await prisma.player.delete({
  where: {
    id: 101,
  }
});
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 注意事项

### 外键约束与 Prisma Relation Mode

你可以使用外键约束或 Prisma Relation Mode 来检查[参照完整性](https://zh.wikipedia.org/wiki/%E5%8F%82%E7%85%A7%E5%AE%8C%E6%95%B4%E6%80%A7)：

- [外键](/foreign-key.md)是 TiDB 从 v6.6.0 开始支持的实验特性，外键允许跨表交叉引用相关数据，外键约束则可以保证相关数据的一致性。

    > **警告：**
    >
    > 外键功能通常适用于为**中小规模**的数据提供完整性和一致性约束校验，但是在大数据量和分布式数据库系统下，使用外键可能会导致严重的性能问题，并对系统产生不可预知的影响。如果计划使用外键，请进行充分验证后谨慎使用。

- [Prisma Relation Mode](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode) 是 Prisma Client 端对外键约束的模拟。该特性会对应用程序的性能产生一些影响，因为它需要额外的数据库查询来维护参照完整性。

## 下一步

- 关于 Prisma 的更多使用方法，可以参考 [Prisma 的官方文档](https://www.prisma.io/docs)。
- 你可以继续阅读开发者文档的其它章节来获取更多 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)，[更新数据](/develop/dev-guide-update-data.md)，[删除数据](/develop/dev-guide-delete-data.md)，[单表读取](/develop/dev-guide-get-data-from-single-table.md)，[事务](/develop/dev-guide-transaction-overview.md)，[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
