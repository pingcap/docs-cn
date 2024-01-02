---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Prisma ORM.
---

# TiDB Cloud Serverless Driver Prisma Tutorial

[Prisma](https://www.prisma.io/docs) is an open source next-generation ORM (Object-Relational Mapping) that helps developers interact with their database in an intuitive, efficient, and safe way. TiDB Cloud offers [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter), enabling you to use [Prisma Client](https://www.prisma.io/docs/concepts/components/prisma-client) over HTTPS with [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md). Compared with the traditional TCP way, [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) brings the following benefits:

- Better performance in serverless environments
- Possibility of using Prisma client in the edge environments (see [#21394](https://github.com/prisma/prisma/issues/21394) for more information)

This tutorial describes how to use TiDB Cloud serverless driver with the Prisma adapter.

## Use the Prisma adapter in Node.js environments

### Before you begin

To complete this tutorial, you need the following:

- [Node.js](https://nodejs.org/en) >= 18.0.0.
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).

### Step 1. Create a project

1. Create a project named `prisma-example`:

    ```
    mkdir prisma-example
    cd prisma-example
    ```

2. Install the `@tidbcloud/prisma-adapter` driver adapter, the `@tidbcloud/serverless` serverless driver, and the Prisma CLI.

   The following commands use npm as the package manager. Executing `npm install @tidbcloud/serverless` will create a `node_modules` directory and a `package.json` file in your project directory.

    ```
    npm install @tidbcloud/prisma-adapter
    npm install @tidbcloud/serverless
    npm install prisma --save-dev
    ```
 
3. In the `package.json` file, specify the ES module by adding `type: "module"`:

   ```json
   {
     "type": "module",
     "dependencies": {
       "@prisma/client": "^5.5.2",
       "@tidbcloud/prisma-adapter": "^5.5.2",
       "@tidbcloud/serverless": "^0.0.7"
     },
     "devDependencies": {
       "prisma": "^5.5.2"
     }
   }
   ```

### Step 2. Set the environment

1. On the overview page of your TiDB Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks like this:

    ```
    mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict
    ```

2. In the root directory of your project, create a file named `.env`, define an environment variable named `DATABASE_URL` as follows, and then replace the placeholders `[]` in this variable with the corresponding parameters in the connection string.

    ```dotenv
    DATABASE_URL="mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict"
    ```

   > **Note:**
   >
   > `@tidbcloud/prisma-adapter` only supports the use of Prisma Client over HTTPS. For [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate) and [Prisma Introspection](https://www.prisma.io/docs/concepts/components/introspection), the traditional TCP connection is still used. If you only need to use Prisma Client, you can simplify `DATABASE_URL` to the `mysql://[username]:[password]@[host]/[database]` format.

3. Install `dotenv` to load the environment variable from the `.env` file:

   ```
   npm install dotenv
   ```

### Step 3. Define your schema

1. Create a file named `schema.prisma`. In this file, include the `driverAdapters` preview feature and reference the `DATABASE_URL` environment variable. Here is an example file:

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

2. In the `schema.prisma` file, define a data model for your database table. In the following example, a data model named `user` is defined.

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

3. Synchronize your database with the Prisma schema. You can either manually create the database tables in your TiDB Serverless cluster or use the Prisma CLI to create them automatically as follows:

    ```
    npx prisma db push
    ```
   
    This command will create the `user` table in your TiDB Serverless cluster through the traditional TCP connection, rather than through the HTTPS connection using `@tidbcloud/prisma-adapter`. This is because it uses the same engine as Prisma Migrate. For more information about this command, see [Prototype your schema](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push).

4. Generate Prisma Client:

    ```
    npx prisma generate
    ```

    This command will generate Prisma Client based on the Prisma schema.

### Step 4. Execute CRUD operations

1. Create a file named `hello-word.js` and add the following code to initialize Prisma Client:

   ```js
   import { connect } from '@tidbcloud/serverless';
   import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
   import { PrismaClient } from '@prisma/client';
   import dotenv from 'dotenv';
   
   // setup
   dotenv.config();
   const connectionString = `${process.env.DATABASE_URL}`;
   
   // Initialize Prisma Client
   const connection = connect({ url: connectionString });
   const adapter = new PrismaTiDBCloud(connection);
   const prisma = new PrismaClient({ adapter });
   ```

2. Execute some CRUD operations with Prisma Client. For example:

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
   
3. Execute some transaction operations with Prisma Client. For example:

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
   
## Use the Prisma adapter in edge environments

Currently, `@tidbcloud/prisma-adapter` is not compatible with edge environments such as Vercel Edge Function and Cloudflare Workers. However, there are plans to support these environments. For more information, see [#21394](https://github.com/prisma/prisma/issues/21394).