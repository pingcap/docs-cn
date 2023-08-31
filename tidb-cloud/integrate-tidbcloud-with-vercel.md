---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

<!-- markdownlint-disable MD029 -->

# Integrate TiDB Cloud with Vercel

[Vercel](https://vercel.com/) is a platform for frontend developers, providing the speed and reliability innovators need to create at the moment of inspiration.

Using TiDB Cloud with Vercel enables you to build new frontend applications faster with a MySQL-compatible relational model and grow your app with confidence with a platform built for resilience, scale, and the highest levels of data privacy and security.

This guide describes how to connect your TiDB Cloud clusters to Vercel projects using one of the following methods:

* [Connect via the TiDB Cloud Vercel integration](#connect-via-the-tidb-cloud-vercel-integration)
* [Connect via manually configuring environment variables](#connect-via-manually-setting-environment-variables)

For both of the preceding methods, TiDB Cloud provides the following options for programmatically connecting to your database:

- Direct connection: connect your TiDB Cloud cluster to your Vercel project directly using MySQL's standard connection system.
- [Data App](/tidb-cloud/data-service-manage-data-app.md): access data of your TiDB Cloud cluster through a collection of HTTP endpoints.

## Prerequisites

Before connection, make sure the following prerequisites are met.

### A Vercel account and a Vercel project

You are expected to have an account and a project in Vercel. If you do not have any, refer to the following Vercel documents to create one:

* [Creating a new personal account](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account) or [Creating a new team](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team).
* [Creating a project](https://vercel.com/docs/concepts/projects/overview#creating-a-project) in Vercel, or if you do not have an application to deploy, you can use the [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter) to have a try.

One Vercel project can only connect to one TiDB Cloud cluster. To change the integration, you need to first disconnect the current cluster and then connect to a new cluster.

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to the following to create one:

- [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **Note:**
    >
    > The TiDB Cloud Vercel integration supports creating TiDB Serverless clusters. You can also create one later during the integration process.

- [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md)

    > **Note:**
    >
    > For TiDB Dedicated clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, because Vercel deployments use [dynamic IP addresses](https://vercel.com/guides/how-to-allowlist-deployment-ip-address). If you use the TiDB Cloud Vercel integration, TiDB Cloud automatically adds a `0.0.0.0/0` traffic filter to your cluster in the integration workflow if there is none.

To [integrate with Vercel via the TiDB Cloud Vercel Integration](#connect-via-the-tidb-cloud-vercel-integration), you are expected to be in the `Organization Owner` role of your organization or the `Project Owner` role of the target project in TiDB Cloud. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

One TiDB Cloud cluster can connect to multiple Vercel projects.

### A Data App and endpoints

If you want to connect to your TiDB Cloud cluster via a [Data App](/tidb-cloud/data-service-manage-data-app.md), you are expected to have the target Data App and endpoints in TiDB Cloud in advance. If you do not have any, refer to the following to create one:

1. In the [TiDB Cloud console](https://tidbcloud.com), go to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. [Create a Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) for your project.
3. [Link the Data App](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) to the target TiDB Cloud cluster.
4. [Manage endpoints](/tidb-cloud/data-service-manage-endpoint.md) so that you can customize them to execute SQL statements.

One Vercel project can only connect to one TiDB Cloud Data App. To change the Data App for your Vercel project, you need to first disconnect the current App and then connect to a new App.

## Connect via the TiDB Cloud Vercel integration

To connect via the TiDB Cloud Vercel integration, go to the [TiDB Cloud integration](https://vercel.com/integrations/tidb-cloud) page from the [Vercel's Integrations Marketplace](https://vercel.com/integrations). Using this method, you can choose which cluster to connect to, and TiDB Cloud will automatically generate all the necessary environment variables for your Vercel projects.

The detailed steps are as follows:

<SimpleTab>
<div label="Direct connection">

1. Click **Add Integration** in the upper-right area of the [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud) page. The **Add TiDB Cloud** dialog is displayed.
2. Select the scope of your integration in the drop-down list and click **Continue**.
3. Select the Vercel projects to which the integration will be added and click **Continue**.
4. Confirm the required permissions for integration and click **Add Integration**. Then you are directed to an integration page of the TiDB Cloud console.
5. On the integration page, do the following:

    1. Select your target Vercel projects and click **Next**.
    2. Select your target TiDB Cloud organization and project.
    3. Select **Cluster** as your connection type.
    4. Select your target TiDB Cloud cluster. If the **Cluster** drop-down list is empty or you want to select a new TiDB Serverless cluster, click **+ Create Cluster** in the list to create one.
    5. Select the framework that your Vercel projects are using. If the target framework is not listed, select **General**. Different frameworks determine different environment variables.
    6. Click **Add Integration and Return to Vercel**.

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6. Get back to your Vercel dashboard, go to your Vercel project, click **Settings** > **Environment Variables**, and check whether the environment variables for your target TiDB cluster have been automatically added.

    If the following variables have been added, the integration is completed.

    **General**

    ```shell
    TIDB_HOST
    TIDB_PORT
    TIDB_USER
    TIDB_PASSWORD
    ```

    For TiDB Dedicated clusters, the root CA is set in this variable:

    ```
    TIDB_SSL_CA
    ```

    **Prisma**

    ```
    DATABASE_URL
    ```

</div>

<div label="Data App">

1. Click **Add Integration** in the upper-right area of the [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud) page. The **Add TiDB Cloud** dialog is displayed.
2. Select the scope of your integration in the drop-down list and click **Continue**.
3. Select the Vercel projects to which the integration will be added and click **Continue**.
4. Confirm the required permissions for integration and click **Add Integration**. Then you are directed to an integration page of the TiDB Cloud console.
5. On the integration page, do the following:

    1. Select your target Vercel projects and click **Next**.
    2. Select your target TiDB Cloud organization and project.
    3. Select **Data App** as your connection type.
    4. Select your target TiDB Data App.
    6. Click **Add Integration and Return to Vercel**.

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6. Get back to your Vercel dashboard, go to your Vercel project, click **Settings** > **Environment Variables**, and check whether the environment variables for your target Data App have been automatically added.

    If the following variables have been added, the integration is completed.

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

## Connect via manually setting environment variables

<SimpleTab>
<div label="Direct connection">

1. Get the connection information of your TiDB cluster.

    You can get the connection information from the connection dialog of your cluster. To open the dialog, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner.

    > **Note:**
    >
    > For TiDB Dedicated clusters, make sure that you have set the **Allow Access from Anywhere** traffic filter in this step.

2. Go to your Vercel dashboard > Vercel project > **Settings** > **Environment Variables**, and then [declare each environment variable value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) according to the connection information of your TiDB cluster.

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

Here we use a Prisma application as an example. The following is a datasource setting in the Prisma schema file for a TiDB Serverless cluster:

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

In Vercel, you can declare the environment variables as follows:

- **Key** = `DATABASE_URL`
- **Value** = `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

You can get the information of `<User>`, `<Password>`, `<Endpoint>`, `<Port>`, and `<Database>` in the TiDB Cloud console.

</div>
<div label="Data App">

1. Follow the steps in [Manage a Data APP](/tidb-cloud/data-service-manage-data-app.md) and [Manage an Endpoint](/tidb-cloud/data-service-manage-endpoint.md) to create a Data App and its endpoints if you have not done that.

2. Go to your Vercel dashboard > Vercel project > **Settings** > **Environment Variables**, and then [declare each environment variable value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) according to the connection information of your Data App.

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    In Vercel, you can declare the environment variables as follows.

    - **Key** = `DATA_APP_BASE_URL`
    - **Value** = `<DATA_APP_BASE_URL>`
    - **Key** = `DATA_APP_PUBLIC_KEY`
    - **Value** = `<DATA_APP_PUBLIC_KEY>`
    - **Key** = `DATA_APP_PRIVATE_KEY`
    - **Value** = `<DATA_APP_PRIVATE_KEY>`

    You can get the information of `<DATA_APP_BASE_URL>`, `<DATA_APP_PUBLIC_KEY>`, `<DATA_APP_PRIVATE_KEY>` from your [Data Service](https://tidbcloud.com/console/data-service) page of the TiDB Cloud console.

</div>
</SimpleTab>

## Configure connections

If you have installed [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud), you can add or remove connections inside the integration.

1. In your Vercel dashboard, click **Integrations**.
2. Click **Manage** in the TiDB Cloud entry.
3. Click **Configure**.
4. Click **Add Link** or **Remove** to add or remove connections.

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    When you remove a connection, environment variables set by the integration workflow are removed from the Vercel project either. The traffic filter and the data of the TiDB Cloud cluster are not affected.
