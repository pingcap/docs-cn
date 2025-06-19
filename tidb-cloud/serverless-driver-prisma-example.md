---
title: TiDB Cloud Serverless 驱动程序 Prisma 教程
summary: 学习如何将 TiDB Cloud serverless 驱动程序与 Prisma ORM 一起使用。
---

# TiDB Cloud Serverless 驱动程序 Prisma 教程

[Prisma](https://www.prisma.io/docs) 是一个开源的下一代 ORM（对象关系映射），帮助开发者以直观、高效和安全的方式与数据库交互。TiDB Cloud 提供了 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)，使你能够通过 HTTPS 使用 [TiDB Cloud serverless 驱动程序](/tidb-cloud/serverless-driver.md)来使用 [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client)。与传统的 TCP 方式相比，[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) 带来以下好处：

- 在 serverless 环境中提供更好的 Prisma Client 性能
- 能够在边缘环境中使用 Prisma Client

本教程介绍如何在 serverless 环境和边缘环境中使用 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)。

## 安装

你需要同时安装 [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) 和 [TiDB Cloud serverless 驱动程序](/tidb-cloud/serverless-driver.md)。你可以使用 [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器进行安装。

以 npm 为例，你可以运行以下命令进行安装：

```shell
npm install @tidbcloud/prisma-adapter
npm install @tidbcloud/serverless
```

## 启用 `driverAdapters`

要使用 Prisma 适配器，你需要在 `schema.prisma` 文件中启用 `driverAdapters` 功能。例如：

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

在使用 Prisma Client 之前，你需要使用 `@tidbcloud/prisma-adapter` 对其进行初始化。

对于早于 v6.6.0 的 `@tidbcloud/prisma-adapter`：

```js
import { connect } from '@tidbcloud/serverless';
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const connection = connect({ url: ${DATABASE_URL} });
const adapter = new PrismaTiDBCloud(connection);
const prisma = new PrismaClient({ adapter });
```

对于 v6.6.0 或更高版本的 `@tidbcloud/prisma-adapter`：

```js
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const adapter = new PrismaTiDBCloud({ url: ${DATABASE_URL} });
const prisma = new PrismaClient({ adapter });
```

然后，来自 Prisma Client 的查询将被发送到 TiDB Cloud serverless 驱动程序进行处理。

## 在 Node.js 环境中使用 Prisma 适配器

本节提供了在 Node.js 环境中使用 `@tidbcloud/prisma-adapter` 的示例。

### 开始之前

要完成本教程，你需要以下内容：

- [Node.js](https://nodejs.org/en) >= 18.0.0。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果你没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 第 1 步：创建项目

1. 创建一个名为 `prisma-example` 的项目：

    ```
    mkdir prisma-example
    cd prisma-example
    ```

2. 安装 `@tidbcloud/prisma-adapter` 驱动适配器、`@tidbcloud/serverless` serverless 驱动程序和 Prisma CLI。

   以下命令使用 npm 作为包管理器。执行 `npm install @tidbcloud/serverless` 将在你的项目目录中创建一个 `node_modules` 目录和一个 `package.json` 文件。

    ```
    npm install @tidbcloud/prisma-adapter
    npm install @tidbcloud/serverless
    npm install prisma --save-dev
    ```

3. 在 `package.json` 文件中，通过添加 `type: "module"` 来指定 ES 模块：

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

### 第 2 步：设置环境

1. 在你的 TiDB Cloud Serverless 集群的概览页面上，点击右上角的**连接**，然后从显示的对话框中获取数据库的连接字符串。连接字符串看起来像这样：

    ```
    mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict
    ```

2. 在项目的根目录中，创建一个名为 `.env` 的文件，定义一个名为 `DATABASE_URL` 的环境变量，如下所示，然后将此变量中的占位符 `[]` 替换为连接字符串中的相应参数。

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

### 第 3 步：定义你的架构

1. 创建一个名为 `schema.prisma` 的文件。在此文件中，包含 `driverAdapters` 预览功能并引用 `DATABASE_URL` 环境变量。以下是示例文件：

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

2. 在 `schema.prisma` 文件中，为你的数据库表定义一个数据模型。在以下示例中，定义了一个名为 `user` 的数据模型。

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
   
   // define a data model according to your database table
   model user {
     id    Int     @id @default(autoincrement())
     email String? @unique(map: "uniq_email") @db.VarChar(255)
     name  String? @db.VarChar(255)
   }
   ```

3. 将你的数据库与 Prisma 架构同步。你可以手动在 TiDB Cloud Serverless 集群中创建数据库表，或使用 Prisma CLI 自动创建它们，如下所示：

    ```
    npx prisma db push
    ```

   此命令将通过传统的 TCP 连接（而不是通过使用 `@tidbcloud/prisma-adapter` 的 HTTPS 连接）在你的 TiDB Cloud Serverless 集群中创建 `user` 表。这是因为它使用与 Prisma Migrate 相同的引擎。有关此命令的更多信息，请参阅[原型化你的架构](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)。

4. 生成 Prisma Client：

    ```
    npx prisma generate
    ```

   此命令将基于 Prisma 架构生成 Prisma Client。

### 第 4 步：执行 CRUD 操作

1. 创建一个名为 `hello-word.js` 的文件，并添加以下代码来初始化 Prisma Client：

   ```js
   import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
   import { PrismaClient } from '@prisma/client';
   import dotenv from 'dotenv';
   
   // setup
   dotenv.config();
   const connectionString = `${process.env.DATABASE_URL}`;
   
   // Initialize Prisma Client
   const adapter = new PrismaTiDBCloud({ url: connectionString });
   const prisma = new PrismaClient({ adapter });
   ```

2. 使用 Prisma Client 执行一些 CRUD 操作。例如：

   ```js
   // Insert
   const user = await prisma.user.create({
     data: {
       email: 'test@pingcap.com',
       name: 'test',
     },
   })
   console.log(user)
   
   // Query
   console.log(await prisma.user.findMany())
   
   // Delete
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
     await prisma.$transaction([createUser1, createUser2]) // Operations fail because the email address is duplicated
   } catch (e) {
     console.log(e)
   }
   
   try {
     await prisma.$transaction([createUser2, createUser3]) // Operations success because the email address is unique
   } catch (e) {
     console.log(e)
   }
   ```

## 在边缘环境中使用 Prisma 适配器

你可以在边缘环境（如 Vercel Edge Functions 和 Cloudflare Workers）中使用 v5.11.0 或更高版本的 `@tidbcloud/prisma-adapter`。

- [Vercel Edge Function 示例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-vercel-example)
- [Cloudflare Workers 示例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-cloudflare-worker-example)
