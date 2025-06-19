---
title: 使用 Prisma 连接 TiDB
summary: 了解如何使用 Prisma 连接 TiDB。本教程提供使用 Prisma 操作 TiDB 的 Node.js 示例代码片段。
---

# 使用 Prisma 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [Prisma](https://github.com/prisma/prisma) 是一个流行的开源 Node.js ORM 框架。

在本教程中，您可以学习如何使用 TiDB 和 Prisma 完成以下任务：

- 设置环境。
- 使用 Prisma 连接到 TiDB 集群。
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
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 `prisma`）：

```shell
npm install
```

<details>
<summary><b>为现有项目安装依赖</b></summary>

对于您的现有项目，运行以下命令安装包：

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### 步骤 3：提供连接参数

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **分支**设置为 `main`。
    - **连接工具**设置为 `Prisma`。
    - **操作系统**与您运行应用程序的操作系统匹配。

4. 如果您还没有设置密码，点击**生成密码**生成随机密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 编辑 `.env` 文件，按如下设置环境变量 `DATABASE_URL`，并将相应的占位符 `{}` 替换为连接对话框中的连接字符串：

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **注意**
    >
    > 对于 TiDB Cloud Serverless，使用公共端点时，您**必须**通过设置 `sslaccept=strict` 启用 TLS 连接。

7. 保存 `.env` 文件。
8. 在 `prisma/schema.prisma` 中，设置 `mysql` 作为连接提供程序，并将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

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

5. 编辑 `.env` 文件，按如下设置环境变量 `DATABASE_URL`，将相应的占位符 `{}` 替换为连接对话框中的连接参数：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **注意**
    >
    > 对于 TiDB Cloud Serverless，使用公共端点时，**建议**通过设置 `sslaccept=strict` 启用 TLS 连接。当您设置 `sslaccept=strict` 启用 TLS 连接时，您**必须**通过 `sslcert=/path/to/ca.pem` 指定从连接对话框下载的 CA 证书的文件路径。

6. 保存 `.env` 文件。
7. 在 `prisma/schema.prisma` 中，设置 `mysql` 作为连接提供程序，并将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 编辑 `.env` 文件，按如下设置环境变量 `DATABASE_URL`，将相应的占位符 `{}` 替换为您的 TiDB 集群的连接参数：

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

   如果您在本地运行 TiDB，默认主机地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

4. 在 `prisma/schema.prisma` 中，设置 `mysql` 作为连接提供程序，并将 `env("DATABASE_URL")` 作为连接 URL：

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### 步骤 4：初始化数据库模式

运行以下命令调用 [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) 使用 `prisma/prisma.schema` 中定义的数据模型初始化数据库。

```shell
npx prisma migrate dev
```

**`prisma.schema` 中定义的数据模型：**

```prisma
// 定义 Player 模型，表示 `players` 表。
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// 定义 Profile 模型，表示 `profiles` 表。
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // 使用外键定义 `Player` 和 `Profile` 模型之间的 1:1 关系。
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

要了解如何在 Prisma 中定义数据模型，请查看[数据模型](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model)文档。

**预期执行输出：**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

此命令还将根据 `prisma/prisma.schema` 生成用于访问 TiDB 数据库的 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)。

### 步骤 5：运行代码

运行以下命令执行示例代码：

```shell
npm start
```

**示例代码中的主要逻辑：**

```typescript
// 步骤 1. 导入自动生成的 `@prisma/client` 包。
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // 步骤 2. 创建一个新的 `PrismaClient` 实例。
  const prisma = new PrismaClient();
  try {

    // 步骤 3. 使用 Prisma Client 执行一些 CRUD 操作...

  } finally {
    // 步骤 4. 断开 Prisma Client 连接。
    await prisma.$disconnect();
  }
}

void main();
```

**预期执行输出：**

如果连接成功，终端将输出 TiDB 集群的版本，如下所示：

```
🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

有关完整的示例代码和如何运行它，请查看 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart) 仓库。

### 插入数据

以下查询创建一个 `Player` 记录，并返回创建的 `Player` 对象，其中包含由 TiDB 生成的 `id` 字段：

```javascript
const player: Player = await prisma.player.create({
   data: {
      name: 'Alice',
      coins: 100,
      goods: 200,
      createdAt: new Date(),
   }
});
```

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

以下查询返回 ID 为 `101` 的 `Player` 对象，如果未找到记录则返回 `null`：

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

以下查询为 ID 为 `101` 的 `Player` 增加 `50` 个硬币和 `50` 个物品：

```javascript
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

更多信息，请参见[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

以下查询删除 ID 为 `101` 的 `Player`：

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 实用说明

### 外键约束与 Prisma 关系模式

要检查[引用完整性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)，您可以使用外键约束或 Prisma 关系模式：

- [外键](https://docs.pingcap.com/tidb/stable/foreign-key)是从 TiDB v6.6.0 开始支持的实验性功能，它允许跨表引用相关数据，并使用外键约束维护数据一致性。

    > **警告：**
    >
    > **外键适用于小型和中型数据量场景。**在大数据量场景中使用外键可能会导致严重的性能问题，并可能对系统产生不可预测的影响。如果您计划使用外键，请先进行彻底的验证，并谨慎使用。

- [Prisma 关系模式](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode)是在 Prisma Client 端模拟引用完整性。但是，应该注意的是，这会带来性能影响，因为它需要额外的数据库查询来维护引用完整性。

## 下一步

- 从 [Prisma 文档](https://www.prisma.io/docs)了解更多 ORM 框架 Prisma 驱动程序的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[查询数据](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
