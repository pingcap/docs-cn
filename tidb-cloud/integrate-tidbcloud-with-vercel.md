---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

# Integrate TiDB Cloud with Vercel

[Vercel](https://vercel.com/) is the platform for frontend developers, providing the speed and reliability innovators need to create at the moment of inspiration.

Using TiDB Cloud with Vercel enables you to build new frontend applications faster with a MySQL-compatible relational model and grow your app with confidence with a platform built for resilience, scale, and the highest levels of data privacy and security.

This guide describes how to connect your TiDB Cloud clusters to Vercel projects using one of the following methods:

* [Connect via the TiDB Cloud Vercel integration](#connect-via-the-tidb-cloud-vercel-integration)
* [Connect via manually configuring environment variables](#connect-via-manually-setting-environment-variables)

## Prerequisites

Before connection, make sure the following prerequisites are met.

### A Vercel account and a Vercel project

You are expected to have an account and a project in Vercel. If you do not have any, refer to the following Vercel documents to create one:

* [Creating a new personal account](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account) or [Creating a new team](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team).
* [Creating a project](https://vercel.com/docs/concepts/projects/overview#creating-a-project) in Vercel, or if you do not have an application to deploy, you can use the [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter) to have a try.

One Vercel project can only connect to one TiDB Cloud cluster. To change the integration, you need to first disconnect the current cluster and then connect to a new cluster.

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

To integrate with Vercel, you are expected to have the "Owner" access to your organization or the "Member" access to the target project in TiDB Cloud. For more information, see [Configure member roles](/tidb-cloud/manage-user-access.md#configure-member-roles).

One TiDB Cloud cluster can connect to multiple Vercel projects.

### All IP addresses allowed for traffic filter in TiDB Cloud

Make sure that the traffic filter of your TiDB Cloud cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Vercel deployments use [dynamic IP  addresses](https://vercel.com/guides/how-to-allowlist-deployment-ip-address). If you use the TiDB Cloud Vercel integration, TiDB Cloud automatically adds a `0.0.0.0/0` traffic filter to your cluster in the integration workflow if there is none.

## Connect via the TiDB Cloud Vercel integration

To connect via the TiDB Cloud Vercel integration, go to the [TiDB Cloud integration](https://vercel.com/integrations/tidb-cloud) page from the [Vercel's Integrations Marketplace](https://vercel.com/integrations). Using this method, you can choose which cluster to connect to, and TiDB Cloud will automatically generate all the necessary environment variables for your Vercel projects.

The detailed steps are as follows:

1. Click **Add Integration** in the upper-right area of the [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud) page. The **Add TiDB Cloud** dialog is displayed.
2. Select the scope of your integration in the drop-down list and click **CONTINUE**.
3. Select the Vercel Projects to which the integration will be added and click **CONTINUE**.
4. Confirm the required permissions for integration and click **ADD INTEGRATION**. Then you are directed to an integration page of the TiDB Cloud console.
5. On the integration page, select the target Vercel projects, and select the target TiDB Cloud cluster after providing the cluster information. Each TiDB Cloud cluster belongs to [an organization and a project](/tidb-cloud/manage-user-access.md#view-the-organization-and-project).
6. Click **Add Integration and Return to Vercel**.
7. Back to your Vercel dashboard, go to your Vercel project, click **Settings** > **Environment Variables**, and confirm that the environment variables have been automatically added.

    If the variables have been added, the connection is completed.

After you have completed the integration setup and successfully connected a TiDB Cloud cluster to your Vercel projects, the information necessary for the connection is automatically set in the projects' environment variables. The following are some common variables:

```
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

For Dedicated Tier clusters, the root CA is set in this variable:

```
TIDB_SSL_CA
```

## Connect via manually setting environment variables

To use this method, make sure that you have set the **Allow Access from Anywhere** traffic filter in the [**Security Settings**](/tidb-cloud/configure-security-settings.md) dialog and save the password.

1. Follow the steps in [Connect to a TiDB Cloud cluster via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to get the connection information of your TiDB cluster. 
2. Go to your Vercel dashboard > Vercel project > **Settings** > **Environment Variables**, and then [declare each environment variable value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) according to the connection information of your TiDB cluster.

The following is an example of the connection variables for a TiDB Cloud Dedicated Tier cluster:

```
var connection = mysql.createConnection({
  host: '<your_host>',
  port: 4000,
  user: 'root',
  password: '<your_password>',
  database: 'test',
  ssl: {
    ca: fs.readFileSync('ca.pem'),
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true
  }
});
```

In Vercel, you can declare the variables as follows. You can customize the name according to your project need.

* **NAME** = TIDB\_HOST **VALUE** = `<your_host>`
* **NAME** = TIDB\_PORT **VALUE** = 4000
* **NAME** = TIDB\_USER **VALUE** = root
* **NAME** = TIDB\_PASSWORD **VALUE** = `<your_password>`
* **NAME** = TIDB\_SSL\_CA **VALUE** = `<content_of_ca.pem>`

## Configure connections

If you have installed [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud), you can add or remove connections inside the integration.

1. In your Vercel dashboard, click **Integrations**.
2. Click **Manage** in the TiDB Cloud entry.
3. Click **Configure**.
4. Click **Add Project** or **Remove** to add or remove connections.

When you remove a connection, environment variables set by the integration workflow are removed from the Vercel project either. The traffic filter and the data of the TiDB Cloud cluster are not affected.
