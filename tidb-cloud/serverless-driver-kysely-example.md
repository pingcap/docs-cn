---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Kysely.
---

# TiDB Cloud Serverless Driver Kysely Tutorial

[Kysely](https://kysely.dev/docs/intro) is a type-safe and autocompletion-friendly TypeScript SQL query builder. TiDB Cloud offers [@tidbcloud/kysely](https://github.com/tidbcloud/kysely), enabling you to use Kysely over HTTPS with [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md). Compared with the traditional TCP way, [@tidbcloud/kysely](https://github.com/tidbcloud/kysely) brings the following benefits:

- Better performance in serverless environments.
- Ability to use Kysely in edge environments.

This tutorial describes how to use TiDB Cloud serverless driver with Kysely in Node.js environments and edge environments.

## Use TiDB Cloud Kysely dialect in Node.js environments

This section describes how to use TiDB Cloud serverless driver with Kysely in Node.js environments.

### Before you begin

To complete this tutorial, you need the following:

- [Node.js](https://nodejs.org/en) >= 18.0.0.
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).

### Step 1. Create a project

1. Create a project named `kysely-node-example`:

    ```
    mkdir kysely-node-example
    cd kysely-node-example
    ```

2. Install the `kysely`, `@tidbcloud/kysely`, and `@tidbcloud/serverless` packages:

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

3. In the root directory of your project, locate the `package.json` file, and then specify the ES module by adding `type: "module"` to the file:

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
   
4. In the root directory of your project, add a `tsconfig.json` file to define the TypeScript compiler options. Here is an example file:

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

### Step 2. Set the environment

1. On the overview page of your TiDB Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks like this:

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

2. Set the environment variable `DATABASE_URL` in your local environment. For example, in Linux or macOS, you can run the following command:

    ```bash
    export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
    ```
   
### Step 3. Use Kysely to query data

1. Create a table in your TiDB Serverless cluster and insert some data. 

    You can use [Chat2Query in the TiDB Cloud console](/tidb-cloud/explore-data-with-chat2query.md) to execute SQL statements. Here is an example:

   ```sql
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
   insert into test.person values (1,'pingcap','male')
   ```

2. In the root directory of your project, create a file named `hello-word.ts` and add the following code:

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

### Step 4. Run the Typescript code

1. Install `ts-node` to transform TypeScript into JavaScript, and then install `@types/node` to provide TypeScript type definitions for Node.js.

   ```
   npm install -g ts-node
   npm i --save-dev @types/node
   ```
   
2. Run the Typescript code with the following command:

   ```
   ts-node --esm hello-world.ts
   ```

## Use TiDB Cloud Kysely dialect in edge environments

This section takes the TiDB Cloud Kysely dialect in Vercel Edge Function as an example.

### Before you begin

To complete this tutorial, you need the following:

- A [Vercel](https://vercel.com/docs) account that provides edge environment.
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).

### Step 1. Create a project

1. Install the Vercel CLI:

    ```
    npm i -g vercel@latest
    ```

2. Create a [Next.js](https://nextjs.org/) project called `kysely-example` using the following terminal commands:

   ```
   npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
   cd kysely-example
   ```
   
3. Install the `kysely`, `@tidbcloud/kysely`, and `@tidbcloud/serverless` packages:

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

### Step 2. Set the environment

On the overview page of your TiDB Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks like this:

```
mysql://[username]:[password]@[host]/[database]
```

### Step 3. Create an edge function

1. Create a table in your TiDB Serverless cluster and insert some data.

    You can use [Chat2Query in the TiDB Cloud console](/tidb-cloud/explore-data-with-chat2query.md) to execute SQL statements. Here is an example:

   ```sql
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
   insert into test.person values (1,'pingcap','male')
   ```

2. In the `app` directory of your project, create a file `/api/edge-function-example/route.ts` and add the following code:

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
   
   The preceding code accepts a query parameter `query` and returns the result of the query. If the query parameter is not provided, it returns all records in the `person` table.

3. Test your code locally:

   ```
   export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
   next dev
   ```
   
4. Navigate to `http://localhost:3000/api/edge-function-example` to get the response from your route.

### Step 4. Deploy your code to Vercel

1. Deploy your code to Vercel with the `DATABASE_URL` environment variable:

   ```
   vercel -e DATABASE_URL=mysql://[username]:[password]@[host]/[database] --prod
   ```

    After the deployment is complete, you will get the URL of your project. 

2. Navigate to the `${Your-URL}/api/edge-function-example` page to get the response from your route.

## What's next

- Learn more about [Kysely](https://kysely.dev/docs/intro) and [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)
- Learn how to [integrate TiDB Cloud with Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)