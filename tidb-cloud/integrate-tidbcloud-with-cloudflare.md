---
title: Integrate TiDB Cloud with Cloudflare
summary: Learn how deploy Cloudflare Workers with TiDB Cloud.
---

# Integrate TiDB Cloud with Cloudflare Workers

[Cloudflare Workers](https://workers.cloudflare.com/) is a platform that allows you to run code in response to specific events, such as HTTP requests or changes to a database. Cloudflare Workers is easy to use and can be used to build a variety of applications, including custom APIs, serverless functions, and microservices. It is particularly useful for applications that require low-latency performance or need to scale quickly.

However, you may find it hard to connect to TiDB Cloud from Cloudflare Workers because Cloudflare Workers runs on the V8 engine which cannot make direct TCP connections.

Fortunately, Prisma has your back with the [Data Proxy](https://www.prisma.io/docs/data-platform/data-proxy). It can help you use Cloudflare Workers to process and manipulate the data being transmitted over a TCP connection.

This document shows how to deploy Cloudflare Workers with TiDB Cloud and Prisma Data Proxy step by step.

> **Note:**
>
> If you want to connect a locally deployed TiDB to Cloudflare Workers, you can try [worker-tidb](https://github.com/shiyuhang0/worker-tidb), which uses Cloudflare tunnels as a proxy. However, worker-tidb is not recommended for production use.

## Before you begin

Before you try the steps in this article, you need to prepare the following things:

- A TiDB Cloud account and a TiDB Serverless cluster on TiDB Cloud. For more details, see [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster).
- A [Cloudflare Workers account](https://dash.cloudflare.com/login).
- A [Prisma Data Platform account](https://cloud.prisma.io/).
- A [GitHub account](https://github.com/login).
- Install Node.js and npm.
- Install dependencies using `npm install -D prisma typescript wrangler`

## Step 1: Set up Wrangler

[Wrangler](https://developers.cloudflare.com/workers/wrangler/) is the official Cloudflare Worker CLI. You can use it to generate, build, preview, and publish your Workers.

1. To authenticate Wrangler, run wrangler login:

    ```
    wrangler login
    ```

2. Use Wrangler to create a worker project:

    ```
    wrangler init prisma-tidb-cloudflare
    ```

3. In your terminal, you will be asked a series of questions related to your project. Choose the default values for all questions.

## Step 2: Set up Prisma

1. Enter your project directory:

    ```
    cd prisma-tidb-cloudflare
    ```

2. Use the `prisma init` command to set up Prisma:

    ```
    npx prisma init
    ```

    This creates a Prisma schema in `prisma/schema.prisma`.

3. Inside `prisma/schema.prisma`, add the schema according to your tables in TiDB. Assume that you have `table1` and `table2` in TiDB, you can add the following schema:

    ```
    generator client {
      provider = "prisma-client-js"
    }

    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }

    model table1 {
      id   Int                   @id @default(autoincrement())
      name String
    }

    model table2 {
      id   Int                   @id @default(autoincrement())
      name String
    }
    ```

    This data model will be used to store incoming requests from your Worker.

## Step 3: Push your project to GitHub

1. [Create a repository](https://github.com/new) named `prisma-tidb-cloudflare` on GitHub.

2. After you create the repository, you can push your project to GitHub:

    ```
    git remote add origin https://github.com/<username>/prisma-tidb-cloudflare
    git add .
    git commit -m "initial commit"
    git push -u origin main
    ```

## Step 4: Import your Project into the Prisma Data Platform

With Cloudflare Workers, you cannot directly access your database because there is no TCP support. Instead, you can use Prisma Data Proxy as described above.

1. To get started, sign in to the [Prisma Data Platform](https://cloud.prisma.io/) and click **New Project**.
2. Fill in the **Connection string** with this pattern `mysql://USER:PASSWORD@HOST:PORT/DATABASE?sslaccept=strict`. You can find the connection information in your [TiDB Cloud console](https://tidbcloud.com/console/clusters).
3. Leave the **Static IPs** as disabled because TiDB Serverless is accessible from any IP address.
4. Select a Data Proxy region that is geographically close to your TiDB Cloud cluster location. Then click **Create project**.

   ![Configure project settings](/media/tidb-cloud/cloudflare/cloudflare-project.png)

5. Fill in the repository, and click **Link Prisma schema** in the **Get Started** page.
6. Click **Create a new connection string** and you will get a new connection string that starts with `prisma://.` Copy this connection string and save it for later.

   ![Create new connection string](/media/tidb-cloud/cloudflare/cloudflare-start.png)

7. Click **Skip and continue to Data Platform** to go to the Data Platform.

## Step 5: Set the Data Proxy Connection string in your environment

1. Add the Data Proxy connection string to your local environment `.env` file:

    ```
    DATABASE_URL=prisma://aws-us-east-1.prisma-data.com/?api_key=•••••••••••••••••"
    ```

2. Add the Data Proxy connection to Cloudflare Workers with secret:

    ```
    wrangler secret put DATABASE_URL
    ```

3. According to the prompt, enter the Data Proxy connection string.

> **Note:**
>
> You can also edit the `DATABASE_URL` secret via the Cloudflare Workers dashboard.

## Step 6: Generate a Prisma Client

Generate a Prisma Client that connects through the [Data Proxy](https://www.prisma.io/docs/data-platform/data-proxy):

```
npx prisma generate --data-proxy
```

## Step 7: Develop the Cloudflare Worker function

You need to change the `src/index.ts` according to your needs.

For example, if you want to query different tables with an URL variable, you can use the following code:

```js
import { PrismaClient } from '@prisma/client/edge'
const prisma = new PrismaClient()

addEventListener('fetch', (event) => {
  event.respondWith(handleEvent(event))
})

async function handleEvent(event: FetchEvent): Promise<Response> {
  // Get URL parameters
  const { request } = event
  const url = new URL(request.url);
  const table = url.searchParams.get('table');
  let limit = url.searchParams.get('limit');
  const limitNumber = limit? parseInt(limit): 100;

  // Get model
  let model
  for (const [key, value] of Object.entries(prisma)) {
    if (typeof value == 'object' && key == table) {
      model = value
      break
    }
  }
  if(!model){
    return new Response("Table not defined")
  }

  // Get data
  const result = await model.findMany({ take: limitNumber })
  return new Response(JSON.stringify({ result }))
}
```

## Step 8: Publish to Cloudflare Workers

You're now ready to deploy to Cloudflare Workers.

In your project directory, run the following command:

```
npx wrangler publish
```

## Step 9: Try your Cloudflare Workers

1. Go to [Cloudflare dashboard](https://dash.cloudflare.com) to find your worker. You can find the URL of your worker on the overview page.

2. Visit the URL with your table name: `https://{your-worker-url}/?table={table_name}`. You will get the result from the corresponding TiDB table.

## Update the project

### Change the serverless function

If you want to change the serverless function, update `src/index.ts` and publish it to Cloudflare Workers again.

### Create a new table

If you create a new table and want to query it, take the following steps:

1. Add a new model in `prisma/schema.prisma`.
2. Push the changes to your repository.

    ```
    git add prisma
    git commit -m "add new model"
    git push
    ```

3. Generate the Prisma Client again.

    ```
    npx prisma generate --data-proxy
    ```

4. Publish the Cloudflare Worker again.

    ```
    npx wrangler publish
    ```
