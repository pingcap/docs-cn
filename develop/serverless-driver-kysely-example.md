---
title: TiDB Cloud Serverless Driver Kysely 教程
summary: 学习如何在 Kysely 中使用 TiDB Cloud serverless driver。
---

# TiDB Cloud Serverless Driver Kysely 教程 <!-- Draft translated by AI -->

[Kysely](https://kysely.dev/docs/intro) 是一个类型安全且支持自动补全的 TypeScript SQL 查询构建器。TiDB Cloud 提供了 [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)，使你能够通过 [TiDB Cloud serverless driver](/develop/serverless-driver.md) 在 HTTPS 上使用 Kysely。与传统的 TCP 方式相比，[ @tidbcloud/kysely ](https://github.com/tidbcloud/kysely) 带来了以下优势：

- 在 serverless 环境下拥有更好的性能。
- 能够在 edge 环境中使用 Kysely。

本教程介绍了如何在 Node.js 环境和 edge 环境中，将 TiDB Cloud serverless driver 与 Kysely 结合使用。

## 在 Node.js 环境中使用 TiDB Cloud Kysely 方言

本节介绍如何在 Node.js 环境中，将 TiDB Cloud serverless driver 与 Kysely 结合使用。

### 前置条件

完成本教程，你需要：

- [Node.js](https://nodejs.org/en) >= 18.0.0。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 步骤 1. 创建项目

1. 创建一个名为 `kysely-node-example` 的项目：

    ```
    mkdir kysely-node-example
    cd kysely-node-example
    ```

2. 安装 `kysely`、`@tidbcloud/kysely` 和 `@tidbcloud/serverless` 包：

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

3. 在项目根目录下，找到 `package.json` 文件，并通过添加 `"type": "module"` 指定 ES module：

   ```json
   {
     "type": "module",
     "dependencies": {
       "@tidbcloud/kysely": "^0.0.4",
       "@tidbcloud/serverless": "^0.0.7",
       "kysely": "^0.26.3",
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

### 步骤 2. 设置环境

1. 在 TiDB Cloud Serverless 集群的 overview 页面，点击右上角的 **Connect**，然后在弹出的对话框中获取你的数据库连接字符串。连接字符串格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

2. 在本地环境中设置环境变量 `DATABASE_URL`。例如，在 Linux 或 macOS 下，可以运行以下命令：

    ```bash
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```
   
### 步骤 3. 使用 Kysely 查询数据

1. 在你的 TiDB Cloud Serverless 集群中创建一张表并插入一些数据。

    你可以使用 [TiDB Cloud 控制台中的 SQL Editor](/ai/explore-data-with-chat2query.md) 执行 SQL 语句。以下为示例：

   ```sql
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
   insert into test.person values (1,'pingcap','male')
   ```

2. 在项目根目录下，创建名为 `hello-world.ts` 的文件，并添加以下代码：

   ```ts
   import { Kysely,GeneratedAlways,Selectable } from 'kysely'
   import { TiDBServerlessDialect } from '@tidbcloud/kysely'
   
   // Types
   interface Database {
     person: PersonTable
   }
   
   interface PersonTable {
     id: GeneratedAlways<number>
     name: string
     gender: "male" | "female"
   }
   
   // Dialect
   const db = new Kysely<Database>({
     dialect: new TiDBServerlessDialect({
       url: process.env.DATABASE_URL
     }),
   })
   
   // Simple Querying
   type Person = Selectable<PersonTable>
   export async function findPeople(criteria: Partial<Person> = {}) {
     let query = db.selectFrom('person')
   
     if (criteria.name){
       query = query.where('name', '=', criteria.name)
     }
   
     return await query.selectAll().execute()
   }
   
   console.log(await findPeople())
   ```

### 步骤 4. 运行 Typescript 代码

1. 安装 `ts-node` 用于将 TypeScript 转换为 JavaScript，并安装 `@types/node` 以为 Node.js 提供 TypeScript 类型定义。

   ```
   npm install -g ts-node
   npm i --save-dev @types/node
   ```
   
2. 使用以下命令运行 Typescript 代码：

   ```
   ts-node --esm hello-world.ts
   ```

## 在 edge 环境中使用 TiDB Cloud Kysely 方言

本节以 Vercel Edge Function 中的 TiDB Cloud Kysely 方言为例进行说明。

### 前置条件

完成本教程，你需要：

- 一个提供 edge 环境的 [Vercel](https://vercel.com/docs) 账号。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

### 步骤 1. 创建项目

1. 安装 Vercel CLI：

    ```
    npm i -g vercel@latest
    ```

2. 使用以下终端命令创建一个名为 `kysely-example` 的 [Next.js](https://nextjs.org/) 项目：

   ```
   npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
   cd kysely-example
   ```
   
3. 安装 `kysely`、`@tidbcloud/kysely` 和 `@tidbcloud/serverless` 包：

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

### 步骤 2. 设置环境

在 TiDB Cloud Serverless 集群的 overview 页面，点击右上角的 **Connect**，然后在弹出的对话框中获取你的数据库连接字符串。连接字符串格式如下：

```
mysql://[username]:[password]@[host]/[database]
```

### 步骤 3. 创建 edge function

1. 在你的 TiDB Cloud Serverless 集群中创建一张表并插入一些数据。

    你可以使用 [TiDB Cloud 控制台中的 SQL Editor](/ai/explore-data-with-chat2query.md) 执行 SQL 语句。以下为示例：

   ```sql
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
   insert into test.person values (1,'pingcap','male')
   ```

2. 在项目的 `app` 目录下，创建文件 `/api/edge-function-example/route.ts`，并添加以下代码：

   ```ts
   import { NextResponse } from 'next/server';
   import type { NextRequest } from 'next/server';
   import { Kysely,GeneratedAlways,Selectable } from 'kysely'
   import { TiDBServerlessDialect } from '@tidbcloud/kysely'
   
   export const runtime = 'edge';
   
   // Types
   interface Database {
     person: PersonTable
   }
   
   interface PersonTable {
     id: GeneratedAlways<number>
     name: string
     gender: "male" | "female" | "other"
   }
   
   // Dialect
   const db = new Kysely<Database>({
     dialect: new TiDBServerlessDialect({
       url: process.env.DATABASE_URL
     }),
   })
   
   // Query
   type Person = Selectable<PersonTable>
   async function findPeople(criteria: Partial<Person> = {}) {
     let query = db.selectFrom('person')
   
     if (criteria.name){
       query = query.where('name', '=', criteria.name)
     }
   
     return await query.selectAll().execute()
   }
   
   export async function GET(request: NextRequest) {
   
     const searchParams = request.nextUrl.searchParams
     const query = searchParams.get('query')
   
     let response = null;
     if (query) {
       response = await findPeople({name: query})
     } else {
       response = await findPeople()
     }
   
     return NextResponse.json(response);
   }
   ```
   
   上述代码接收一个查询参数 `query` 并返回查询结果。如果未提供该参数，则返回 `person` 表中的所有记录。

3. 本地测试你的代码：

   ```
   export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
   next dev
   ```
   
4. 访问 `http://localhost:3000/api/edge-function-example`，即可获取该路由的响应。

### 步骤 4. 部署代码到 Vercel

1. 使用 `DATABASE_URL` 环境变量将代码部署到 Vercel：

   ```
   vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod
   ```

    部署完成后，你将获得项目的 URL。

2. 访问 `${Your-URL}/api/edge-function-example` 页面，即可获取该路由的响应。

## 后续操作

- 了解更多关于 [Kysely](https://kysely.dev/docs/intro) 和 [@tidbcloud/kysely](https://github.com/tidbcloud/kysely) 的信息
- 学习如何 [将 TiDB Cloud 集成到 Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)
