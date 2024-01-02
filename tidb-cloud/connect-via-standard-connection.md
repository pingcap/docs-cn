---
title: Connect to TiDB Dedicated via Standard Connection
summary: Learn how to connect to your TiDB Cloud cluster via standard connection.
---

# Connect to TiDB Dedicated via Standard Connection

This document describes how to connect to your TiDB Dedicated cluster via standard connection. The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB Dedicated cluster via a SQL client from your laptop.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster via standard connection, see [Connect to TiDB Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md).

To connect to a TiDB Dedicated cluster via standard connection, take the following steps:

1. Open the overview page of the target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Create a traffic filter for the cluster. Traffic filter is a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

    If the traffic filter is already set, skip the following sub-steps. If the traffic filter is empty, take the following sub-steps to add one.

    1. Click one of the buttons to add some rules quickly.

        - **Add My Current IP Address**
        - **Allow Access from Anywhere**

    2. Provide an optional description for the newly added IP address or CIDR range.

    3. Click **Create Filter** to confirm the changes.

4. Under **Step 2: Download CA cert** in the dialog, click **Download CA cert** for TLS connection to TiDB clusters. The CA cert supports TLS 1.2 version by default.

    > **Note:**
    >
    > - The CA cert is only available for TiDB Dedicated clusters.
    > - Currently, TiDB Cloud only provides the connection strings and sample code for these connection methods: MySQL, MyCLI, JDBC, Python, Go, and Node.js.

5. Under **Step 3: Connect with a SQL client** in the dialog, click the tab of your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

    Note that you need to use the path of the downloaded CA file as the argument of the `--ssl-ca` option in the connection string.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
