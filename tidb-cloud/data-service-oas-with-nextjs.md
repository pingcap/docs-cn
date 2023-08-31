---
title: Use the OpenAPI Specification of a Data App with Next.js
summary: Learn how to use the OpenAPI Specification of a Data App to generate client code and develop a Next.js application.
---

# Use the OpenAPI Specification of a Data App with Next.js

This document introduces how to use the OpenAPI Specification of a [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) to generate client code and develop a Next.js application.

## Before you begin

Before using OpenAPI Specification with Next.js, make sure that you have the following:

- A TiDB cluster. For more information, see [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) or [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md).
- [Node.js](https://nodejs.org/en/download)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [yarn](https://yarnpkg.com/getting-started/install)

This document uses a TiDB Serverless cluster as an example.

## Step 1. Prepare data

To begin with, create a table `test.repository` in your TiDB cluster and insert some sample data into it. The following example inserts some open source projects developed by PingCAP as data for demonstration purposes.

To execute the SQL statements, you can use [Chat2Query](/tidb-cloud/explore-data-with-chat2query.md) in the [TiDB Cloud console](https://tidbcloud.com).

```sql
-- Select the database
USE test;

-- Create the table
CREATE TABLE repository (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(64) NOT NULL,
        url varchar(256) NOT NULL
);

-- Insert some sample data into the table
INSERT INTO repository (name, url)
VALUES ('tidb', 'https://github.com/pingcap/tidb'),
        ('tikv', 'https://github.com/tikv/tikv'),
        ('pd', 'https://github.com/tikv/pd'),
        ('tiflash', 'https://github.com/pingcap/tiflash');
```

## Step 2. Create a Data App

After the data is inserted, navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page in the [TiDB Cloud console](https://tidbcloud.com). Create a Data App that links to your TiDB cluster, create an API key for the Data App, and then create a `GET /repositories` endpoint in the Data App. The corresponding SQL statement for this endpoint is as follows, which fetches all rows from the `test.repository` table:

```sql
SELECT * FROM test.repository;
```

For more information, see [Get started with Data Service](/tidb-cloud/data-service-get-started.md).

## Step 3. Generate client code

The following uses Next.js as an example to demonstrate how to generate client code using the OpenAPI Specification of a Data App.

1. Create a Next.js project named `hello-repos`.

    To create a Next.js project using the official template, use the following command and keep all the default options when prompted:

    ```shell
    yarn create next-app hello-repos
    ```

    Change the directory to the newly created project using the following command:

    ```shell
    cd hello-repos
    ```

2. Install dependencies.

    This document uses [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) to automatically generate API client libraries from the OpenAPI Specification.

    To install OpenAPI Generator as a development dependency, run the following command:

    ```shell
    yarn add @openapitools/openapi-generator-cli --dev
    ```

3. Download the OpenAPI Specification and save it as `oas/doc.json`.

    1. On the TiDB Cloud [**Data Service**](https://tidbcloud.com/console/data-service) page, click your Data App name in the left pane to view the App settings.
    2. In the **API Specification** area, click **Download**, select the JSON format, and then click **Authorize** if prompted.
    3. Save the downloaded file as `oas/doc.json` in the `hello-repos` project directory.

    For more information, see [Download the OpenAPI Specification](/tidb-cloud/data-service-manage-data-app.md#download-the-openapi-specification).

    The structure of the `oas/doc.json` file is as follows:

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

4. Generate the client code:

    ```shell
    yarn run openapi-generator-cli generate -i oas/doc.json --generator-name typescript-fetch -o gen/api
    ```

    This command generates the client code using the `oas/doc.json` specification as input and outputs the client code to the `gen/api` directory.

## Step 4. Develop your Next.js application

You can use the generated client code to develop your Next.js application.

1. In the `hello-repos` project directory, create a `.env.local` file with the following variables, and then set the variable values to the public key and private key of your Data App.

    ```
    TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY=YOUR_PUBLIC_KEY
    TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY=YOUR_PRIVATE_KEY
    ```

    To create an API key for a Data App, see [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

2. In the `hello-repos` project directory, replace the content of `app/page.tsx` with the following code, which fetches data from the `GET /repositories` endpoint and renders it:

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

    > **Note:**
    >
    > If the linked clusters of your Data App are hosted in different regions, you wil see multiple items in the `servers` section of the downloaded OpenAPI Specification file. In this case, you also need to configure the endpoint path in the `config` object as follows:
    >
    >  ```js
    >  const config = new Configuration({
    >      username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
    >      password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
    >      basePath: "https://${YOUR_REGION}.data.dev.tidbcloud.com/api/v1beta/app/${YOUR_DATA_APP_ID}/endpoint"
    >    });
    >  ```
    >
    > Make sure to replace `basePath` with the actual endpoint path of your Data App. To get `${YOUR_REGION}` and `{YOUR_DATA_APP_ID}`, check the **Endpoint URL** in the endpoint **Properties** panel.

## Step 5. Preview your Next.js application

> **Note:**
>
> Make sure that all required dependencies are installed and correctly configured before previewing.

To preview your application in a local development server, run the following command:

```shell
yarn dev
```

You can then open <http://localhost:3000> in your browser and see the data from the `test.repository` database displayed on the page.
