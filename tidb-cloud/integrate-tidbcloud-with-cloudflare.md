---
title: Integrate TiDB Cloud with Cloudflare
summary: Learn how to deploy Cloudflare Workers with TiDB Cloud.
---

# Integrate TiDB Cloud with Cloudflare Workers

[Cloudflare Workers](https://workers.cloudflare.com/) is a platform that allows you to run code in response to specific events, such as HTTP requests or changes to a database. Cloudflare Workers is easy to use and can be used to build a variety of applications, including custom APIs, serverless functions, and microservices. It is particularly useful for applications that require low-latency performance or need to scale quickly.

You may find it hard to connect to TiDB Cloud from Cloudflare Workers because Cloudflare Workers runs on the V8 engine which cannot make direct TCP connections. You can use [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md) to help you connect to Cloudflare Workers over HTTP connection.

This document shows how to connect to Cloudflare Workers with TiDB Cloud serverless driver step by step.

> **Note:**
>
> TiDB Cloud serverless driver can only be used in TiDB Serverless.

## Before you begin

Before you try the steps in this article, you need to prepare the following things:

- A TiDB Cloud account and a TiDB Serverless cluster on TiDB Cloud. For more details, see [TiDB Cloud Quick Start](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster).
- A [Cloudflare Workers account](https://dash.cloudflare.com/login).
- [npm](https://docs.npmjs.com/about-npm) is installed.

## Step 1: Set up Wrangler

[Wrangler](https://developers.cloudflare.com/workers/wrangler/) is the official Cloudflare Worker CLI. You can use it to generate, build, preview, and publish your Workers.

1. Install Wrangler:

   ```
   npm install wrangler
   ```

2. To authenticate Wrangler, run wrangler login:

    ```
    wrangler login
    ```

3. Use Wrangler to create a worker project:

    ```
    wrangler init tidb-cloud-cloudflare
    ```

4. In your terminal, you will be asked a series of questions related to your project. Choose the default values for all questions.

## Step 2: Install the serverless driver

1. Enter your project directory:

    ```
    cd tidb-cloud-cloudflare
    ```

2. Install the serverless driver with npm:

    ```
    npm install @tidbcloud/serverless
    ```

   This adds the serverless driver dependency in `package.json`.

## Step 3: Develop the Cloudflare Worker function

You need to modify the `src/index.ts` according to your needs.

For example, if you want to show all the databases, you can use the following code:

```ts
import { connect } from '@tidbcloud/serverless'


export interface Env {
   DATABASE_URL: string;
}

export default {
   async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
      const conn = connect({url:env.DATABASE_URL})
      const resp = await conn.execute("show databases")
      return new Response(JSON.stringify(resp));
   },
};
```

## Step 4: Set the DATABASE_URL in your environment

The `DATABASE_URL` follows the `mysql://username:password@host/database` format. You can set the environment variable with wrangler cli:

```
wrangler secret put <DATABASE_URL>
```

You can also edit the `DATABASE_URL` secret via the Cloudflare Workers dashboard.

## Step 5: Publish to Cloudflare Workers

You're now ready to deploy to Cloudflare Workers.

In your project directory, run the following command:

```
npx wrangler publish
```

## Step 6: Try your Cloudflare Workers

1. Go to [Cloudflare dashboard](https://dash.cloudflare.com) to find your worker. You can find the URL of your worker on the overview page.

2. Visit the URL and you will get the result.

## Examples

See the [Cloudflare Workers example](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers).