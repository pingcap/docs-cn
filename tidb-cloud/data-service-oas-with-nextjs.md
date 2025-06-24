---
title: 将数据应用的 OpenAPI 规范与 Next.js 一起使用
summary: 了解如何使用数据应用的 OpenAPI 规范生成客户端代码并开发 Next.js 应用程序。
---

# 将数据应用的 OpenAPI 规范与 Next.js 一起使用

本文介绍如何使用[数据应用](/tidb-cloud/tidb-cloud-glossary.md#data-app)的 OpenAPI 规范生成客户端代码并开发 Next.js 应用程序。

## 开始之前

在将 OpenAPI 规范与 Next.js 一起使用之前，请确保你具有以下条件：

- 一个 TiDB 集群。更多信息，请参见[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)或[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。
- [Node.js](https://nodejs.org/en/download)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [yarn](https://yarnpkg.com/getting-started/install)

本文以 TiDB Cloud Serverless 集群为例。

## 步骤 1. 准备数据

首先，在你的 TiDB 集群中创建一个 `test.repository` 表并向其中插入一些示例数据。以下示例插入一些由 PingCAP 开发的开源项目作为演示数据。

要执行 SQL 语句，你可以使用 [TiDB Cloud 控制台](https://tidbcloud.com)中的 [SQL 编辑器](/tidb-cloud/explore-data-with-chat2query.md)。

```sql
-- 选择数据库
USE test;

-- 创建表
CREATE TABLE repository (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(64) NOT NULL,
        url varchar(256) NOT NULL
);

-- 向表中插入一些示例数据
INSERT INTO repository (name, url)
VALUES ('tidb', 'https://github.com/pingcap/tidb'),
        ('tikv', 'https://github.com/tikv/tikv'),
        ('pd', 'https://github.com/tikv/pd'),
        ('tiflash', 'https://github.com/pingcap/tiflash');
```

## 步骤 2. 创建数据应用

插入数据后，在 [TiDB Cloud 控制台](https://tidbcloud.com)中导航到[**数据服务**](https://tidbcloud.com/project/data-service)页面。创建一个链接到你的 TiDB 集群的数据应用，为该数据应用创建一个 API 密钥，然后在数据应用中创建一个 `GET /repositories` 端点。此端点的对应 SQL 语句如下，它从 `test.repository` 表中获取所有行：

```sql
SELECT * FROM test.repository;
```

更多信息，请参见[开始使用数据服务](/tidb-cloud/data-service-get-started.md)。

## 步骤 3. 生成客户端代码

以下以 Next.js 为例，演示如何使用数据应用的 OpenAPI 规范生成客户端代码。

1. 创建一个名为 `hello-repos` 的 Next.js 项目。

    要使用官方模板创建 Next.js 项目，请使用以下命令，并在提示时保持所有默认选项：

    ```shell
    yarn create next-app hello-repos
    ```

    使用以下命令切换到新创建的项目目录：

    ```shell
    cd hello-repos
    ```

2. 安装依赖。

    本文使用 [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) 从 OpenAPI 规范自动生成 API 客户端库。

    要将 OpenAPI Generator 安装为开发依赖项，请运行以下命令：

    ```shell
    yarn add @openapitools/openapi-generator-cli --dev
    ```

3. 下载 OpenAPI 规范并将其保存为 `oas/doc.json`。

    1. 在 TiDB Cloud [**数据服务**](https://tidbcloud.com/project/data-service)页面，点击左侧窗格中的数据应用名称以查看应用设置。
    2. 在 **API 规范**区域，点击**下载**，选择 JSON 格式，如果出现提示，点击**授权**。
    3. 将下载的文件保存为 `hello-repos` 项目目录中的 `oas/doc.json`。

    更多信息，请参见[下载 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#下载-openapi-规范)。

    `oas/doc.json` 文件的结构如下：

    ```json
    {
      "openapi": "3.0.3",
      "components": {
        "schemas": {
          "getRepositoriesResponse": {
            "properties": {
              "data": {
                "properties": {
                  "columns": { ... },
                  "result": { ... },
                  "rows": {
                    "items": {
                      "properties": {
                        "id": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "url": {
                          "type": "string"
                        }
    ...
      "paths": {
        "/repositories": {
          "get": {
            "operationId": "getRepositories",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/getRepositoriesResponse"
                    }
                  }
                },
                "description": "OK"
              },
    ...
    ```

4. 生成客户端代码：

    ```shell
    yarn run openapi-generator-cli generate -i oas/doc.json --generator-name typescript-fetch -o gen/api
    ```

    此命令使用 `oas/doc.json` 规范作为输入生成客户端代码，并将客户端代码输出到 `gen/api` 目录。

## 步骤 4. 开发你的 Next.js 应用程序

你可以使用生成的客户端代码开发你的 Next.js 应用程序。

1. 在 `hello-repos` 项目目录中，创建一个包含以下变量的 `.env.local` 文件，然后将变量值设置为你的数据应用的公钥和私钥。

    ```
    TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY=YOUR_PUBLIC_KEY
    TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY=YOUR_PRIVATE_KEY
    ```

    要为数据应用创建 API 密钥，请参见[创建 API 密钥](/tidb-cloud/data-service-api-key.md#创建-api-密钥)。

2. 在 `hello-repos` 项目目录中，用以下代码替换 `app/page.tsx` 的内容，该代码从 `GET /repositories` 端点获取数据并渲染它：

    ```js
    import {DefaultApi, Configuration} from "../gen/api"

    export default async function Home() {
      const config = new Configuration({
        username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
        password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
      });
      const apiClient = new DefaultApi(config);
      const resp = await apiClient.getRepositories();
      return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <ul className="font-mono text-2xl">
            {resp.data.rows.map((repo) => (
              <a href={repo.url}>
                <li key={repo.id}>{repo.name}</li>
              </a>
            ))}
          </ul>
        </main>
      )
    }
    ```

    > **注意：**
    >
    > 如果你的数据应用链接的集群位于不同的区域，你将在下载的 OpenAPI 规范文件的 `servers` 部分看到多个项目。在这种情况下，你还需要在 `config` 对象中配置端点路径，如下所示：
    >
    >  ```js
    >  const config = new Configuration({
    >      username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
    >      password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
    >      basePath: "https://${YOUR_REGION}.data.dev.tidbcloud.com/api/v1beta/app/${YOUR_DATA_APP_ID}/endpoint"
    >    });
    >  ```
    >
    > 确保将 `basePath` 替换为你的数据应用的实际端点路径。要获取 `${YOUR_REGION}` 和 `{YOUR_DATA_APP_ID}`，请查看端点**属性**面板中的**端点 URL**。

## 步骤 5. 预览你的 Next.js 应用程序

> **注意：**
>
> 在预览之前，请确保已安装并正确配置所有必需的依赖项。

要在本地开发服务器中预览你的应用程序，请运行以下命令：

```shell
yarn dev
```

然后，你可以在浏览器中打开 [http://localhost:3000](http://localhost:3000)，看到从 `test.repository` 数据库显示的数据。
