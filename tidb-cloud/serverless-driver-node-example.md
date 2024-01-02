---
title: TiDB Cloud Serverless Driver Node.js Tutorial
summary: Learn how to use TiDB Cloud serverless driver in a local Node.js project.
---

# TiDB Cloud Serverless Driver Node.js Tutorial

This tutorial describes how to use TiDB Cloud serverless driver in a local Node.js project.

> **Note:**
>
> - This tutorial is applicable to TiDB Serverless clusters only. 
> - To learn how to use TiDB Cloud serverless driver with Cloudflare Workers, Vercel Edge Functions, and Netlify Edge Functions, check out our [Insights into Automotive Sales](https://car-sales-insight.vercel.app/) and the [sample repository](https://github.com/tidbcloud/car-sales-insight).

## Before you begin

To complete this step-by-step tutorial, you need the following:

- [Node.js](https://nodejs.org/en) >= 18.0.0.
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).

## Step 1. Create a local Node.js project

1. Create a project named `node-example`:

    ```shell
    mkdir node-example
    cd node-example
    ```

2. Install the TiDB Cloud serverless driver using npm or your preferred package manager.

    The following command takes installation with npm as an example. Executing this command will create a `node_modules` directory and a `package.json` file in your project directory.

    ```
    npm install @tidbcloud/serverless
    ```

## Step 2. Use the serverless driver

The serverless driver supports both CommonJS and ES modules. The following steps take the usage of the ES module as an example.

1. On the overview page of your TiDB Cloud Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks like this:

    ```
   mysql://[username]:[password]@[host]/[database]
    ```
   
2. In the `package.json` file, specify the ES module by adding `type: "module"`. 

    For example:

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.0.7",
      }
    }
    ```

3. Create a file named `index.js` in your project directory and add the following code:

    ```js
    import { connect } from '@tidbcloud/serverless'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Serverless cluster information
    console.log(await conn.execute("show tables"))
    ```

4. Run your project with the following command:

    ```
    node index.js
    ```

## Compatability with earlier versions of Node.js

If you are using Node.js earlier than 18.0.0, which does not have a global `fetch` function, you can take the following steps to get `fetch`:

1. Install a package that provides `fetch`, such as `undici`:

    ```
    npm install undici
    ``` 

2. Pass the `fetch` function to the `connect` function:

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```