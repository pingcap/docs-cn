---
title: TiDB Cloud Serverless Driver Drizzle 教程
summary: 学习如何在 Drizzle 中使用 TiDB Cloud serverless driver。
---

# TiDB Cloud Serverless Driver Drizzle 教程 <!-- Draft translated by AI -->

[Drizzle ORM](https://orm.drizzle.team/) 是一款轻量级且高性能的 TypeScript ORM，注重开发者体验。从 `drizzle-orm@0.31.2` 开始，Drizzle 支持 [drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)，你可以通过 [TiDB Cloud serverless driver](//serverless-driver.md) 以 HTTPS 方式连接 Drizzle。

本教程介绍如何在 Node.js 环境和边缘环境中，将 TiDB Cloud serverless driver 与 Drizzle 搭配使用。

## 在 Node.js 环境中使用 Drizzle 和 TiDB Cloud serverless driver

本节介绍如何在 Node.js 环境中，将 TiDB Cloud serverless driver 与 Drizzle 搭配使用。

### 前置条件

完成本教程，你需要准备以下内容：

- [Node.js](https://nodejs.org/en) >= 18.0.0。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 步骤 1. 创建项目

1. 创建一个名为 `drizzle-node-example` 的项目：

    ```shell
    mkdir drizzle-node-example
    cd drizzle-node-example
    ```

2. 安装 `drizzle-orm` 和 `@tidbcloud/serverless` 包：

   ```shell
   npm install drizzle-orm @tidbcloud/serverless
   ```

3. 在项目根目录下，找到 `package.json` 文件，并通过添加 `"type": "module"` 指定 ES module：

   ```json
   {
     "type": "module",
     "dependencies": {
       "@tidbcloud/serverless": "^0.1.1",
       "drizzle-orm": "^0.31.2"
     }
   }
   ```

4. 在项目根目录下，添加 `tsconfig.json` 文件以定义 TypeScript 编译选项。以下是示例文件：

   ```json
   {
     "compilerOptions": {
       "module": "ES2022",
       "target": "ES2022",
       "moduleResolution": "node",
       "strict": false,
       "declaration": true,
       "outDir": "dist",
       "removeComments": true,
       "allowJs": true,
       "esModuleInterop": true,
       "resolveJsonModule": true
     }
   }
   ```

### 步骤 2. 配置环境

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Serverless 集群名称，进入集群概览页。

2. 在概览页右上角点击 **Connect**，在 **Connect With** 下拉列表中选择 `Serverless Driver`，然后点击 **Generate Password** 生成随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或者点击 **Reset Password** 生成新密码。

    连接字符串格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

3. 在本地环境中设置环境变量 `DATABASE_URL`。例如，在 Linux 或 macOS 下，可以运行以下命令：

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### 步骤 3. 使用 Drizzle 查询数据

1. 在你的 TiDB Cloud Serverless 集群中创建一张表。

   你可以使用 [TiDB Cloud 控制台的 SQL Editor](/ai/explore-data-with-chat2query.md) 执行 SQL 语句。以下为示例：

   ```sql
   CREATE TABLE `test`.`users` (
    `id` BIGINT PRIMARY KEY auto_increment,
    `full_name` TEXT,
    `phone` VARCHAR(256)
   );
   ```

2. 在项目根目录下，创建名为 `hello-world.ts` 的文件，并添加以下代码：

   ```ts
   import { connect } from '@tidbcloud/serverless';
   import { drizzle } from 'drizzle-orm/tidb-serverless';
   import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';

   // Initialize
   const client = connect({ url: process.env.DATABASE_URL });
   const db = drizzle(client);

   // Define schema
   export const users = mysqlTable('users', {
     id: serial("id").primaryKey(),
     fullName: text('full_name'),
     phone: varchar('phone', { length: 256 }),
   });
   export type User = typeof users.$inferSelect; // return type when queried
   export type NewUser = typeof users.$inferInsert; // insert type

   // Insert and select data
   const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
   await db.insert(users).values(user)
   const result: User[] = await db.select().from(users);
   console.log(result);
   ```

### 步骤 4. 运行 Typescript 代码

1. 安装 `ts-node` 用于将 TypeScript 转换为 JavaScript，并安装 `@types/node` 以为 Node.js 提供 TypeScript 类型定义。

   ```shell
   npm install -g ts-node
   npm i --save-dev @types/node
   ```

2. 使用以下命令运行 Typescript 代码：

   ```shell
   ts-node --esm hello-world.ts
   ```

## 在边缘环境中使用 Drizzle 和 TiDB Cloud serverless driver

本节以 Vercel Edge Function 为例进行说明。

### 前置条件

完成本教程，你需要准备以下内容：

- 一个支持边缘环境的 [Vercel](https://vercel.com/docs) 账号。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 步骤 1. 创建项目

1. 安装 Vercel CLI：

    ```shell
    npm i -g vercel@latest
    ```

2. 使用以下命令创建一个名为 `drizzle-example` 的 [Next.js](https://nextjs.org/) 项目：

   ```shell
   npx create-next-app@latest drizzle-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
   ```

3. 进入 `drizzle-example` 目录：

   ```shell
   cd drizzle-example
   ```

4. 安装 `drizzle-orm` 和 `@tidbcloud/serverless` 包：

   ```shell
   npm install drizzle-orm @tidbcloud/serverless --force
   ```

### 步骤 2. 配置环境

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入你项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，点击目标 TiDB Cloud Serverless 集群名称，进入集群概览页。

2. 在概览页右上角点击 **Connect**，在 **Connect With** 下拉列表中选择 `Serverless Driver`，然后点击 **Generate Password** 生成随机密码。

    > **Tip:**
    >
    > 如果你之前已经创建过密码，可以继续使用原密码，或者点击 **Reset Password** 生成新密码。

    连接字符串格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

### 步骤 3. 创建边缘函数

1. 在你的 TiDB Cloud Serverless 集群中创建一张表。

   你可以使用 [TiDB Cloud 控制台的 SQL Editor](/ai/explore-data-with-chat2query.md) 执行 SQL 语句。以下为示例：

   ```sql
   CREATE TABLE `test`.`users` (
    `id` BIGINT PRIMARY KEY auto_increment,
    `full_name` TEXT,
    `phone` VARCHAR(256)
   );
   ```

2. 在项目的 `app` 目录下，创建文件 `/api/edge-function-example/route.ts`，并添加以下代码：

   ```ts
   import { NextResponse } from 'next/server';
   import type { NextRequest } from 'next/server';
   import { connect } from '@tidbcloud/serverless';
   import { drizzle } from 'drizzle-orm/tidb-serverless';
   import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';
   export const runtime = 'edge';

   // Initialize
   const client = connect({ url: process.env.DATABASE_URL });
   const db = drizzle(client);

   // Define schema
   export const users = mysqlTable('users', {
     id: serial("id").primaryKey(),
     fullName: text('full_name'),
     phone: varchar('phone', { length: 256 }),
   });
   export type User = typeof users.$inferSelect; // return type when queried
   export type NewUser = typeof users.$inferInsert; // insert type

   export async function GET(request: NextRequest) {
     // Insert and select data
     const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
     await db.insert(users).values(user)
     const result: User[] = await db.select().from(users);
     return NextResponse.json(result);
   }
   ```

3. 本地测试你的代码：

   ```shell
   export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
   next dev
   ```

4. 访问 `http://localhost:3000/api/edge-function-example`，获取路由返回的响应。

### 步骤 4. 部署代码到 Vercel

1. 使用 `DATABASE_URL` 环境变量将代码部署到 Vercel：

   ```shell
   vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod
   ```

   部署完成后，你会获得项目的 URL。

2. 访问 `${Your-URL}/api/edge-function-example` 页面，获取路由返回的响应。

## 后续操作

- 了解更多关于 [Drizzle](https://orm.drizzle.team/docs/overview) 和 [drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless) 的信息。
- 学习如何 [集成 TiDB Cloud 与 Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。