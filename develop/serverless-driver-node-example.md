---
title: TiDB Cloud serverless driver Node.js 教程
summary: 学习如何在本地 Node.js 项目中使用 TiDB Cloud serverless driver。
aliases: ['/zh/tidbcloud/serverless-driver-node-example/']
---

# TiDB Cloud serverless driver Node.js 教程

本教程介绍如何在本地 Node.js 项目中使用 TiDB Cloud serverless driver。

> **注意：**
>
> - 除了 TiDB Cloud Starter 集群，本教程的步骤也适用于 TiDB Cloud Essential 集群。
> - 如果你想了解如何在 Cloudflare Workers、Vercel Edge Functions 和 Netlify Edge Functions 中使用 TiDB Cloud serverless driver，请参考 [Insights into Automotive Sales](https://car-sales-insight.vercel.app/) 和[示例仓库](https://github.com/tidbcloud/car-sales-insight)。

## 开始之前

要完成本教程中的步骤，你需要准备以下内容：

- [Node.js](https://nodejs.org/en) >= 18.0.0。
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 或你喜欢的包管理器。
- 一个 TiDB Cloud Starter 集群。如果你还没有，可以[创建一个 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md)。

## 步骤 1. 创建本地 Node.js 项目

1. 创建一个名为 `node-example` 的项目：

    ```shell
    mkdir node-example
    cd node-example
    ```

2. 使用 npm 或你喜欢的包管理器安装 TiDB Cloud serverless driver。

    以下命令以 npm 安装为例。执行该命令后，会在你的项目目录下创建 `node_modules` 目录和 `package.json` 文件。

    ```
    npm install @tidbcloud/serverless
    ```

## 步骤 2. 使用 serverless driver

serverless driver 同时支持 CommonJS 和 ES modules。以下步骤以 ES module 的用法为例。

1. 在你的 TiDB Cloud Starter 集群的概览页面，点击右上角的 **Connect**，然后在弹出的对话框中获取你的数据库连接字符串。连接字符串格式如下：

    ```
   mysql://[username]:[password]@[host]/[database]
    ```
   
2. 在 `package.json` 文件中，通过添加 `type: "module"` 来指定 ES module。

    例如：

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.0.7",
      }
    }
    ```

3. 在你的项目目录下创建一个名为 `index.js` 的文件，并添加以下代码：

    ```js
    import { connect } from '@tidbcloud/serverless'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // 替换为你的 TiDB Cloud Starter 集群信息
    console.log(await conn.execute("show tables"))
    ```

4. 使用以下命令运行你的项目：

    ```
    node index.js
    ```

## 与 Node.js 早期版本的兼容性

如果你使用的 Node.js 版本低于 18.0.0，不包含全局 `fetch` 函数，可以通过以下步骤获取 `fetch`：

1. 安装一个提供 `fetch` 的包，例如 `undici`：

    ```
    npm install undici
    ``` 

2. 将 `fetch` 函数传递给 `connect` 函数：

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```