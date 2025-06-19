---
title: TiDB Cloud Serverless 驱动程序 Node.js 教程
summary: 学习如何在本地 Node.js 项目中使用 TiDB Cloud serverless 驱动程序。
---

# TiDB Cloud Serverless 驱动程序 Node.js 教程

本教程介绍如何在本地 Node.js 项目中使用 TiDB Cloud serverless 驱动程序。

> **注意：**
>
> - 本教程仅适用于 TiDB Cloud Serverless 集群。
> - 要了解如何在 Cloudflare Workers、Vercel Edge Functions 和 Netlify Edge Functions 中使用 TiDB Cloud serverless 驱动程序，请查看我们的[汽车销售分析](https://car-sales-insight.vercel.app/)和[示例代码库](https://github.com/tidbcloud/car-sales-insight)。

## 开始之前

要完成本分步教程，你需要：

- [Node.js](https://nodejs.org/en) >= 18.0.0
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你偏好的包管理器
- 一个 TiDB Cloud Serverless 集群。如果你还没有，可以[创建一个 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

## 步骤 1. 创建本地 Node.js 项目

1. 创建一个名为 `node-example` 的项目：

    ```shell
    mkdir node-example
    cd node-example
    ```

2. 使用 npm 或你偏好的包管理器安装 TiDB Cloud serverless 驱动程序。

    以下命令以 npm 安装为例。执行此命令将在你的项目目录中创建一个 `node_modules` 目录和一个 `package.json` 文件。

    ```
    npm install @tidbcloud/serverless
    ```

## 步骤 2. 使用 serverless 驱动程序

serverless 驱动程序同时支持 CommonJS 和 ES 模块。以下步骤以使用 ES 模块为例。

1. 在 TiDB Cloud Serverless 集群的概览页面上，点击右上角的**连接**，然后从显示的对话框中获取数据库的连接字符串。连接字符串格式如下：

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

2. 在 `package.json` 文件中，通过添加 `type: "module"` 来指定 ES 模块。

    例如：

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.0.7",
      }
    }
    ```

3. 在项目目录中创建一个名为 `index.js` 的文件，并添加以下代码：

    ```js
    import { connect } from '@tidbcloud/serverless'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // 替换为你的 TiDB Cloud Serverless 集群信息
    console.log(await conn.execute("show tables"))
    ```

4. 使用以下命令运行你的项目：

    ```
    node index.js
    ```

## 与早期版本 Node.js 的兼容性

如果你使用的是 18.0.0 之前的 Node.js 版本（没有全局 `fetch` 函数），可以按照以下步骤获取 `fetch`：

1. 安装提供 `fetch` 的包，例如 `undici`：

    ```
    npm install undici
    ```

2. 将 `fetch` 函数传递给 `connect` 函数：

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```
