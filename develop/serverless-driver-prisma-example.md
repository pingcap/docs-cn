---
title: TiDB Cloud serverless driver Prisma 教程
summary: 学习如何将 TiDB Cloud serverless driver 与 Prisma ORM 一起使用。
---

# TiDB Cloud serverless driver Prisma 教程

[Prisma](https://www.prisma.io/docs) 是一款开源的下一代 ORM（对象关系映射），可以帮助开发者以直观、高效且安全的方式操作数据库。TiDB Cloud 提供了 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)，使你能够通过 [TiDB Cloud serverless driver](/develop/serverless-driver.md) 在 HTTPS 上使用 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)。与传统的 TCP 方式相比，[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) 带来了以下优势：

- 在 serverless 环境下提升 Prisma Client 的性能
- 支持在边缘环境下使用 Prisma Client

本教程介绍如何在 serverless 环境和边缘环境中使用 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)。

> **建议：**
>
> 除了 TiDB Cloud Starter 集群，本教程的步骤也适用于 TiDB Cloud Essential 集群。

## 安装

你需要安装 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) 和 [TiDB Cloud serverless driver](/develop/serverless-driver.md)。你可以使用 [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器进行安装。

以 npm 为例，你可以运行以下命令进行安装：

```shell
npm install @tidbcloud/prisma-adapter
npm install @tidbcloud/serverless
```

## 启用 `driverAdapters`

要使用 Prisma adapter，你需要在 `schema.prisma` 文件中启用 `driverAdapters` 特性。例如：

```prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
}
```

## 初始化 Prisma Client

在使用 Prisma Client 之前，你需要用 `@tidbcloud/prisma-adapter` 进行初始化。

对于 v6.6.0 之前的 `@tidbcloud/prisma-adapter`：

```js
import { connect } from '@tidbcloud/serverless';
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// 初始化 Prisma Client
const connection = connect({ url: ${DATABASE_URL} });
const adapter = new PrismaTiDBCloud(connection);
const prisma = new PrismaClient({ adapter });
```

对于 v6.6.0 或更高版本的 `@tidbcloud/prisma-adapter`：

```js
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// 初始化 Prisma Client
const adapter = new PrismaTiDBCloud({ url: ${DATABASE_URL} });
const prisma = new PrismaClient({ adapter });
```

之后，Prisma Client 的查询将通过 TiDB Cloud serverless driver 进行处理。

## 在 Node.js 环境中使用 Prisma adapter

本节提供了在 Node.js 环境下使用 `@tidbcloud/prisma-adapter` 的示例。

### 前置条件

完成本教程，你需要准备以下内容：

- [Node.js](https://nodejs.org/en) >= 18.0.0
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器
- 一个 TiDB Cloud Starter 集群。如果你还没有，可以[创建一个 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md)

### 步骤 1. 创建项目

1. 创建一个名为 `prisma-example` 的项目：

    ```
    mkdir prisma-example
    cd prisma-example
    ```

2. 安装 `@tidbcloud/prisma-adapter` 驱动适配器、`@tidbcloud/serverless` serverless driver 以及 Prisma CLI。

   以下命令以 npm 作为包管理器。执行 `npm install @tidbcloud/serverless` 会在你的项目目录下创建 `node_modules` 目录和 `package.json` 文件。

    ```
    npm install @tidbcloud/prisma-adapter
    npm install @tidbcloud/serverless
    npm install prisma --save-dev
    ```

3. 在 `package.json` 文件中，通过添加 `type: "module"` 指定 ES module：

   ```json
   {
     "type": "module",
     "dependencies": {
       "@prisma/client": "^6.6.0",
       "@tidbcloud/prisma-adapter": "^6.6.0",
       "@tidbcloud/serverless": "^0.1.0"
     },
     "devDependencies": {
       "prisma": "^6.6.0"
     }
   }
   ```

### 步骤 2. 配置环境

1. 在 TiDB Cloud Starter 集群的概览页面，点击右上角的 **Connect**，然后在弹出的对话框中获取你的数据库连接字符串。连接字符串格式如下：

    ```
    mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict
    ```

2. 在项目根目录下创建一个名为 `.env` 的文件，定义名为 `DATABASE_URL` 的环境变量，并将该变量中的 `[]` 占位符替换为连接字符串中的对应参数。

    ```dotenv
    DATABASE_URL='mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict'
    ```

   > **注意：**
   >
   > `@tidbcloud/prisma-adapter` 仅支持通过 HTTPS 使用 Prisma Client。对于 [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) 和 [Prisma Introspection](https://www.prisma.io/docs/concepts/components/introspection)，仍然使用传统的 TCP 连接。如果你只需要使用 Prisma Client，可以将 `DATABASE_URL` 简化为 `mysql://[username]:[password]@[host]/[database]` 格式。

3. 安装 `dotenv` 以从 `.env` 文件加载环境变量：

   ```
   npm install dotenv
   ```

### 步骤 3. 定义 schema

1. 创建一个名为 `schema.prisma` 的文件。在该文件中，包含 `driverAdapters` 预览特性，并引用 `DATABASE_URL` 环境变量。示例文件如下：

   ```
   // schema.prisma
   generator client {
     provider        = "prisma-client-js"
     previewFeatures = ["driverAdapters"]
   }
   
   datasource db {
     provider     = "mysql"
     url          = env("DATABASE_URL")
   } 
   ```

2. 在 `schema.prisma` 文件中，为你的数据库表定义数据模型。以下示例定义了一个名为 `user` 的数据模型。

   ```
   // schema.prisma
   generator client {
     provider        = "prisma-client-js"
     previewFeatures = ["driverAdapters"]
   }
   
   datasource db {
     provider     = "mysql"
     url          = env("DATABASE_URL")
   } 
   
   // 根据你的数据库表定义数据模型
   model user {
     id    Int     @id @default(autoincrement())
     email String? @unique(map: "uniq_email") @db.VarChar(255)
     name  String? @db.VarChar(255)
   }
   ```

3. 使用 Prisma schema 同步你的数据库。你可以手动在 TiDB Cloud Starter 集群中创建数据库表，也可以使用 Prisma CLI 自动创建：

    ```
    npx prisma db push
    ```

   该命令会通过传统的 TCP 连接在 TiDB Cloud Starter 集群中创建 `user` 表，而不是通过 `@tidbcloud/prisma-adapter` 的 HTTPS 连接。这是因为它使用了与 Prisma Migrate 相同的引擎。关于该命令的更多信息，请参见 [Prototype your schema](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)。

4. 生成 Prisma Client：

    ```
    npx prisma generate
    ```

   该命令会根据 Prisma schema 生成 Prisma Client。

### 步骤 4. 执行 CRUD 操作

1. 创建一个名为 `hello-word.js` 的文件，并添加以下代码以初始化 Prisma Client：

   ```js
   import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
   import { PrismaClient } from '@prisma/client';
   import dotenv from 'dotenv';
   
   // 设置
   dotenv.config();
   const connectionString = `${process.env.DATABASE_URL}`;
   
   // 初始化 Prisma Client
   const adapter = new PrismaTiDBCloud({ url: connectionString });
   const prisma = new PrismaClient({ adapter });
   ```

2. 使用 Prisma Client 执行一些 CRUD 操作。例如：

   ```js
   // 插入
   const user = await prisma.user.create({
     data: {
       email: 'test@pingcap.com',
       name: 'test',
     },
   })
   console.log(user)
   
   // 查询
   console.log(await prisma.user.findMany())
   
   // 删除
   await prisma.user.delete({
      where: {
         id: user.id,
      },
   })
   ```

3. 使用 Prisma Client 执行一些事务操作。例如：

   ```js
   const createUser1 = prisma.user.create({
     data: {
       email: 'test1@pingcap.com',
       name: 'test1',
     },
   })
   const createUser2 = prisma.user.create({
     data: {
       email: 'test1@pingcap.com',
       name: 'test1',
     },
   })
   const createUser3 = prisma.user.create({
     data: {
       email: 'test2@pingcap.com',
       name: 'test2',
     },
   })
   
   try {
     await prisma.$transaction([createUser1, createUser2]) // 由于邮箱地址重复，操作失败
   } catch (e) {
     console.log(e)
   }
   
   try {
     await prisma.$transaction([createUser2, createUser3]) // 由于邮箱地址唯一，操作成功
   } catch (e) {
     console.log(e)
   }
   ```

## 在边缘环境中使用 Prisma adapter

你可以在边缘环境（如 Vercel Edge Functions 和 Cloudflare Workers）中使用 v5.11.0 或更高版本的 `@tidbcloud/prisma-adapter`。

- [Vercel Edge Function 示例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-vercel-example)
- [Cloudflare Workers 示例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-cloudflare-worker-example)
