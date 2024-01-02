---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# Integrate TiDB Cloud with Netlify

[Netlify](https://netlify.com/) is an all-in-one platform for automating modern web projects. It replaces your hosting infrastructure, continuous integration, and deployment pipeline with a single workflow and integrates dynamic functionality like serverless functions, user authentication, and form handling as your projects grow.

This document describes how to deploy a fullstack app on Netlify with TiDB Cloud as the database backend. You can also learn how to use Netlify edge function with our TiDB Cloud serverless driver.

## Prerequisites

Before the deployment, make sure the following prerequisites are met.

### A Netlify account and CLI

You are expected to have a Netlify account and CLI. If you do not have any, refer to the following links to create one:

* [Sign up for a Netlify account](https://app.netlify.com/signup).
* [Get Netlify CLI](https://docs.netlify.com/cli/get-started/).

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to the following to create one:

- [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)
- [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md)

One TiDB Cloud cluster can connect to multiple Netlify sites.

### All IP addresses allowed for traffic filter in TiDB Cloud

For TiDB Dedicated clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection. This is because Netlify deployments use dynamic IP addresses.

TiDB Serverless clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

## Step 1. Get the example project and the connection string

To help you get started quickly, TiDB Cloud provides a fullstack example app in TypeScript with Next.js using React and Prisma Client. It is a simple blog site where you can post and delete your own blogs. All the content is stored in TiDB Cloud through Prisma.

### Fork the example project and clone it to your own space

1. Fork the [Fullstack Example with Next.js and Prisma](https://github.com/tidbcloud/nextjs-prisma-example) repository to your own GitHub repository.

2. Clone the forked repository to your own space:

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### Get the TiDB Cloud connection string

For a TiDB Serverless cluster, you can get the connection string either from [TiDB Cloud CLI](/tidb-cloud/cli-reference.md) or from [TiDB Cloud console](https://tidbcloud.com/).

For a TiDB Dedicated cluster, you can get the connection string only from the TiDB Cloud console.

<SimpleTab>
<div label="TiDB Cloud CLI">

> **Tip:**
>
> If you have not installed Cloud CLI, refer to [TiDB Cloud CLI Quick Start](/tidb-cloud/get-started-with-cli.md) for quick installation before taking the following steps.

1. Get the connection string of a cluster in interactive mode:

    ```shell
    ticloud cluster connect-info
    ```

2. Follow the prompts to select your cluster, client, and operating system. Note that the client used in this document is `Prisma`.

    ```
    Choose the cluster
    > [x] Cluster0(13796194496)
    Choose the client
    > [x] Prisma
    Choose the operating system
    > [x] macOS/Alpine (Detected)
    ```

    The output is as follows, where you can find the connection string for Prisma in the `url` value.

    ```shell
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **Note:**
    >
    > When you use the connection string later, note the following:
    >
    > - Replace the parameters in the connection string with actual values.
    > - The example app in this document requires a new database, so you need to replace `<Database>` with a unique new name.

</div>
<div label="TiDB Cloud console">

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner. In the displayed dialog, you can get the following connection parameters from the connection string.

    - `${host}`
    - `${port}`
    - `${user}`
    - `${password}`

2. Fill the connection parameters in the following connection string:

    ```shell
    mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
    ```

    > **Note:**
    >
    > When you use the connection string later, note the following:
    >
    > - Replace the parameters in the connection string with actual values.
    > - The example app in this document requires a new database, so you need to replace `<Database>` with a unique new name.

</div>
</SimpleTab>

## Step 2. Deploy the example app to Netlify

1. In Netlify CLI, authenticate your Netlify account and obtain an access token.

    ```shell
    netlify login
    ```

2. Start the automatic setup. This step connects your repository for continuous deployment, so Netlify CLI needs access to create a deploy key and a webhook on the repository.

    ```shell
    netlify init
    ```

    When you are prompted, choose **Create & configure a new site**, and grant GitHub access. Use the default values for all other options.

    ```shell
    Adding local .netlify folder to .gitignore file...
    ? What would you like to do? +  Create & configure a new site
    ? Team: your_username’s team
    ? Site name (leave blank for a random name; you can change it later):

    Site Created

    Admin URL: https://app.netlify.com/sites/mellow-crepe-e2ca2b
    URL:       https://mellow-crepe-e2ca2b.netlify.app
    Site ID:   b23d1359-1059-49ed-9d08-ed5dba8e83a2

    Linked to mellow-crepe-e2ca2b


    ? Netlify CLI needs access to your GitHub account to configure Webhooks and Deploy Keys. What would you like to do? Authorize with GitHub through app.netlify.com
    Configuring Next.js runtime...

    ? Your build command (hugo build/yarn run build/etc): npm run netlify-build
    ? Directory to deploy (blank for current dir): .next

    Adding deploy key to repository...
    (node:36812) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
    (Use `node --trace-warnings ...` to show where the warning was created)
    Deploy key added!

    Creating Netlify GitHub Notification Hooks...
    Netlify Notification Hooks configured!

    Success! Netlify CI/CD Configured!

    This site is now configured to automatically deploy from github branches & pull requests

    Next steps:

    git push       Push to your git repository to trigger new site builds
    netlify open   Open the Netlify admin URL of your site
    ```

3. Set environment variables. To connect to your TiDB Cloud cluster from your own space and the Netlify space, you need to set the `DATABASE_URL` as the connection string obtained from [Step 1](#step-1-get-the-example-project-and-the-connection-string).

    ```shell
    # set the environment variable for your own space
    export DATABASE_URL='mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'

    # set the environment variable for the Netlify space
    netlify env:set DATABASE_URL 'mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    ```

    Check your environment variables.

    ```shell
    # check the environment variable for your own space
    env | grep DATABASE_URL

    # check the environment variable for the Netlify space
    netlify env:list
    ```

4. Build the app locally and migrate the schema to your TiDB Cloud cluster.

    > **Tips:**
    >
    > If you want to skip the local deployment and directly deploy the app to Netlify, just go to step 6.

    ```shell
    npm install .
    npm run netlify-build
    ```

5. Run the application locally. You can start a local development server to preview your site.

    ```shell
    netlify dev
    ```

    Then, go to `http://localhost:3000/` in your browser to explore its UI.

6. Deploy the app to Netlify. Once you are satisfied with the local preview, you can deploy your site to Netlify using the following command. `--trigger` means deployment without uploading local files. If you made any local changes, make sure that you have committed them to your GitHub repository.

    ```shell
    netlify deploy --prod --trigger
    ```

    Go to your Netlify console to check the deployment state. After the deployment is done, the site for the app will have a public IP address provided by Netlify so that everyone can access it.

## Use the edge function

The example app mentioned in the section above runs on the Netlify serverless function. This section shows you how to use the edge function with [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md). The edge function is a feature provided by Netlify, which allows you to run serverless functions on the edge of the Netlify CDN.

To use the edge function, take the following steps:

1. Create a directory named `netlify/edge-functions` in the root directory of your project. 

2. Create a file named `hello.ts` in the directory and add the following code:

    ```typescript
    import { connect } from 'https://esm.sh/@tidbcloud/serverless'
    
    export default async () => {
      const conn = connect({url: Netlify.env.get('DATABASE_URL')})
      const result = await conn.execute('show databases')
      return new Response(JSON.stringify(result));
    }
   
    export const config = { path: "/api/hello" };
    ```

3. Set the `DATABASE_URL` environment variables. You can get the connection information from the [TiDB Cloud console](https://tidbcloud.com/).

    ```shell
    netlify env:set DATABASE_URL 'mysql://<username>:<password>@<host>/<database>'
    ```

4. Deploy the edge function to Netlify.

    ```shell
    netlify deploy --prod --trigger
    ```

Then you can go to your Netlify console to check the state of the deployment. After the deployment is done, you can access the edge function through the `https://<netlify-host>/api/hello` URL.
