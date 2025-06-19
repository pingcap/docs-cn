---
title: 将 TiDB Cloud 与 Cloudflare 集成
summary: 了解如何将 Cloudflare Workers 与 TiDB Cloud 一起部署。
---

# 将 TiDB Cloud 与 Cloudflare Workers 集成

[Cloudflare Workers](https://workers.cloudflare.com/) 是一个允许您响应特定事件（如 HTTP 请求或数据库更改）运行代码的平台。Cloudflare Workers 易于使用，可用于构建各种应用程序，包括自定义 API、无服务器函数和微服务。它特别适用于需要低延迟性能或需要快速扩展的应用程序。

由于 Cloudflare Workers 运行在 V8 引擎上，无法直接建立 TCP 连接，您可能会发现从 Cloudflare Workers 连接到 TiDB Cloud 比较困难。您可以使用 [TiDB Cloud 无服务器驱动](/tidb-cloud/serverless-driver.md)通过 HTTP 连接帮助您连接到 Cloudflare Workers。

本文档将逐步说明如何使用 TiDB Cloud 无服务器驱动连接到 Cloudflare Workers。

> **注意：**
>
> TiDB Cloud 无服务器驱动只能在 TiDB Cloud Serverless 中使用。

## 开始之前

在尝试本文中的步骤之前，您需要准备以下内容：

- TiDB Cloud 账号和 TiDB Cloud 上的 TiDB Cloud Serverless 集群。更多详情，请参阅 [TiDB Cloud 快速入门](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)。
- [Cloudflare Workers 账号](https://dash.cloudflare.com/login)。
- 已安装 [npm](https://docs.npmjs.com/about-npm)。

## 步骤 1：设置 Wrangler

[Wrangler](https://developers.cloudflare.com/workers/wrangler/) 是官方的 Cloudflare Worker CLI。您可以使用它来生成、构建、预览和发布您的 Workers。

1. 安装 Wrangler：

   ```
   npm install wrangler
   ```

2. 要验证 Wrangler，请运行 wrangler login：

    ```
    wrangler login
    ```

3. 使用 Wrangler 创建一个 worker 项目：

    ```
    wrangler init tidb-cloud-cloudflare
    ```

4. 在终端中，您将被问到一系列与项目相关的问题。对所有问题选择默认值。

## 步骤 2：安装无服务器驱动

1. 进入您的项目目录：

    ```
    cd tidb-cloud-cloudflare
    ```

2. 使用 npm 安装无服务器驱动：

    ```
    npm install @tidbcloud/serverless
    ```

   这会在 `package.json` 中添加无服务器驱动依赖。

## 步骤 3：开发 Cloudflare Worker 函数

您需要根据需要修改 `src/index.ts`。

例如，如果您想显示所有数据库，可以使用以下代码：

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

## 步骤 4：在环境中设置 DATABASE_URL

`DATABASE_URL` 遵循 `mysql://username:password@host/database` 格式。您可以使用 wrangler cli 设置环境变量：

```
wrangler secret put <DATABASE_URL>
```

您也可以通过 Cloudflare Workers 仪表板编辑 `DATABASE_URL` 密钥。

## 步骤 5：发布到 Cloudflare Workers

现在您已准备好部署到 Cloudflare Workers。

在您的项目目录中，运行以下命令：

```
npx wrangler publish
```

## 步骤 6：尝试您的 Cloudflare Workers

1. 转到 [Cloudflare 仪表板](https://dash.cloudflare.com)找到您的 worker。您可以在概览页面上找到您的 worker 的 URL。

2. 访问该 URL，您将获得结果。

## 示例

请参阅 [Cloudflare Workers 示例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)。
