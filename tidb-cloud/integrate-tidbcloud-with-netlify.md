---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# Integrate TiDB Cloud with Netlify

[Netlify](https://netlify.com/) is an all-in-one platform for automating modern web projects. It replaces your hosting infrastructure, continuous integration, and deployment pipeline with a single workflow and integrates dynamic functionality like serverless functions, user authentication, and form handling as your projects grow.

This guide describes how to connect your TiDB Cloud clusters to Netlify projects.

## Prerequisites

Before connecting, make sure the following prerequisites are met.

### A Netlify account and a deployed site

You are expected to have an account and a site in Netlify. If you do not have any, refer to the following links to create one:

* [Sign up a new account](https://app.netlify.com/signup).
* [Add a site](https://docs.netlify.com/welcome/add-new-site/) in Netlify. If you do not have an application to deploy, you can use the [TiDB Cloud Starter Template](https://github.com/tidbcloud/nextjs-prisma-example) to have a try.

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

One TiDB Cloud cluster can connect to multiple Netlify sites.

### All IP addresses allowed for traffic filter in TiDB Cloud

For Dedicated Tier clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Netlify deployments use dynamic IP addresses.

Serverless Tier clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

## Connect via manually setting environment variables

1. Follow the steps in [Connect to a TiDB Cloud cluster via standard connection](/tidb-cloud/connect-via-standard-connection.md) to set a password and get the connection information of your TiDB cluster.

    > **Note:**
    >
    > For Dedicated Tier clusters, make sure that you have also set the **Allow Access from Anywhere** traffic filter in this step.

2. Go to your **Netlify dashboard** > **Netlify project** > **Site settings** > **Environment Variables**, and then [update variables](https://docs.netlify.com/environment-variables/get-started/#update-variables-with-the-netlify-ui) according to the connection information of your TiDB cluster.

    Here we use a Prisma application as an example. The following is a datasource setting in the Prisma schema file for a TiDB Cloud Serverless Tier cluster:

    ```
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

    In Netlify, you can declare the environment variables as follows.

    - **Key** = DATABASE_URL
    - **Values** = `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

    You can get the information of `<User>`, `<Password>`, `<Endpoint>`, `<Port>`, and `<Database>` in the TiDB Cloud console.

![Set an environment variable in Netlify](/media/tidb-cloud/integration-netlify-environment-variables.jpg)

After re-deploying the site, you can use this new environment variable to connect to your TiDB Cloud cluster.