---
title: TiDB Cloud Serverless 驱动程序 Drizzle 教程
summary: 了解如何将 TiDB Cloud serverless 驱动程序与 Drizzle 配合使用。
---

# TiDB Cloud Serverless 驱动程序 Drizzle 教程

[Drizzle ORM](https://orm.drizzle.team/) 是一个轻量级且高性能的 TypeScript ORM，专注于开发者体验。从 `drizzle-orm@0.31.2` 开始，它支持 [drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)，使您能够通过 HTTPS 使用 [TiDB Cloud serverless 驱动程序](/tidb-cloud/serverless-driver.md)。

本教程介绍如何在 Node.js 环境和边缘环境中将 TiDB Cloud serverless 驱动程序与 Drizzle 配合使用。

## 在 Node.js 环境中使用 Drizzle 和 TiDB Cloud serverless 驱动程序

本节介绍如何在 Node.js 环境中将 TiDB Cloud serverless 驱动程序与 Drizzle 配合使用。

### 开始之前

要完成本教程，您需要：

- [Node.js](https://nodejs.org/en) >= 18.0.0。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或您首选的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果您还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

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

3. 在项目的根目录中找到 `package.json` 文件，然后通过添加 `"type": "module"` 来指定 ES 模块：

   ```json
   {
     "type": "module",
     "dependencies": {
       "@tidbcloud/serverless": "^0.1.1",
       "drizzle-orm": "^0.31.2"
     }
   }
   ```

4. 在项目的根目录中添加一个 `tsconfig.json` 文件来定义 TypeScript 编译器选项。以下是示例文件：

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

### 步骤 2. 设置环境

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称进入其概览页面。

2. 在概览页面上，点击右上角的**连接**，在**连接方式**下拉列表中选择 `Serverless Driver`，然后点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

    连接字符串的格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

3. 在本地环境中设置环境变量 `DATABASE_URL`。例如，在 Linux 或 macOS 中，您可以运行以下命令：

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### 步骤 3. 使用 Drizzle 查询数据

1. 在您的 TiDB Cloud Serverless 集群中创建一个表。

   您可以使用 [TiDB Cloud 控制台中的 SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)执行 SQL 语句。以下是示例：

   ```sql
   CREATE TABLE `test`.`users` (
    `id` BIGINT PRIMARY KEY auto_increment,
    `full_name` TEXT,
    `phone` VARCHAR(256)
   );
   ```

2. 在项目的根目录中创建一个名为 `hello-world.ts` 的文件，并添加以下代码：

   ```ts
   import { connect } from '@tidbcloud/serverless';
   import { drizzle } from 'drizzle-orm/tidb-serverless';
   import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';

   // 初始化
   const client = connect({ url: process.env.DATABASE_URL });
   const db = drizzle(client);

   // 定义模式
   export const users = mysqlTable('users', {
     id: serial("id").primaryKey(),
     fullName: text('full_name'),
     phone: varchar('phone', { length: 256 }),
   });
   export type User = typeof users.$inferSelect; // 查询时的返回类型
   export type NewUser = typeof users.$inferInsert; // 插入类型

   // 插入和选择数据
   const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
   await db.insert(users).values(user)
   const result: User[] = await db.select().from(users);
   console.log(result);
   ```

### 步骤 4. 运行 TypeScript 代码

1. 安装 `ts-node` 将 TypeScript 转换为 JavaScript，然后安装 `@types/node` 为 Node.js 提供 TypeScript 类型定义。

   ```shell
   npm install -g ts-node
   npm i --save-dev @types/node
   ```

2. 使用以下命令运行 TypeScript 代码：

   ```shell
   ts-node --esm hello-world.ts
   ```

## 在边缘环境中使用 Drizzle 和 TiDB Cloud serverless 驱动程序

本节以 Vercel Edge Function 为例。

### 开始之前

要完成本教程，您需要：

- 一个提供边缘环境的 [Vercel](https://vercel.com/docs) 账户。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或您首选的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果您还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 步骤 1. 创建项目

1. 安装 Vercel CLI：

    ```shell
    npm i -g vercel@latest
    ```

2. 使用以下终端命令创建一个名为 `drizzle-example` 的 [Next.js](https://nextjs.org/) 项目：

   ```shell
   npx create-next-app@latest drizzle-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
   ```

3. 导航到 `drizzle-example` 目录：

   ```shell
   cd drizzle-example
   ```

4. 安装 `drizzle-orm` 和 `@tidbcloud/serverless` 包：

   ```shell
   npm install drizzle-orm @tidbcloud/serverless --force
   ```

### 步骤 2. 设置环境

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标 TiDB Cloud Serverless 集群的名称进入其概览页面。

2. 在概览页面上，点击右上角的**连接**，在**连接方式**下拉列表中选择 `Serverless Driver`，然后点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

    连接字符串的格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

### 步骤 3. 创建边缘函数

1. 在您的 TiDB Cloud Serverless 集群中创建一个表。

   您可以使用 [TiDB Cloud 控制台中的 SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)执行 SQL 语句。以下是示例：

   ```sql
   CREATE TABLE `test`.`users` (
    `id` BIGINT PRIMARY KEY auto_increment,
    `full_name` TEXT,
    `phone` VARCHAR(256)
   );
   ```

2. 在项目的 `app` 目录中创建一个文件 `/api/edge-function-example/route.ts`，并添加以下代码：

   ```ts
   import { NextResponse } from 'next/server';
   import type { NextRequest } from 'next/server';
   import { connect } from '@tidbcloud/serverless';
   import { drizzle } from 'drizzle-orm/tidb-serverless';
   import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';
   export const runtime = 'edge';

   // 初始化
   const client = connect({ url: process.env.DATABASE_URL });
   const db = drizzle(client);

   // 定义模式
   export const users = mysqlTable('users', {
     id: serial("id").primaryKey(),
     fullName: text('full_name'),
     phone: varchar('phone', { length: 256 }),
   });
   export type User = typeof users.$inferSelect; // 查询时的返回类型
   export type NewUser = typeof users.$inferInsert; // 插入类型

   export async function GET(request: NextRequest) {
     // 插入和选择数据
     const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
     await db.insert(users).values(user)
     const result: User[] = await db.select().from(users);
     return NextResponse.json(result);
   }
   ```

3. 在本地测试您的代码：

   ```shell
   export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
   next dev
   ```

4. 导航到 `http://localhost:3000/api/edge-function-example` 以获取路由的响应。

### 步骤 4. 将代码部署到 Vercel

1. 使用 `DATABASE_URL` 环境变量将代码部署到 Vercel：

   ```shell
   vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod
   ```

   部署完成后，您将获得项目的 URL。

2. 导航到 `${Your-URL}/api/edge-function-example` 页面以获取路由的响应。

## 下一步

- 了解更多关于 [Drizzle](https://orm.drizzle.team/docs/overview) 和 [drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless) 的信息。
- 了解如何[将 TiDB Cloud 与 Vercel 集成](/tidb-cloud/integrate-tidbcloud-with-vercel.md)。
