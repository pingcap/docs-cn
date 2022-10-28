---
title: Connect to Your TiDB Cluster
summary: Connect to your TiDB cluster via a SQL client or SQL shell.
---

# Connect to Your TiDB Cluster

After your TiDB cluster is created on TiDB Cloud, you can use one of the following methods to connect to your TiDB cluster. You can access your cluster via a SQL client, or quickly via SQL Shell in the TiDB Cloud Console.

+ Connect via a SQL client

    - [Connect via standard connection](#connect-via-standard-connection): The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.
    - [Connect via private endpoint](#connect-via-private-endpoint-recommended): Private endpoint connection provides a private endpoint to allow clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management. Note that you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier) using the private endpoint.
    - [Connect via VPC peering](#connect-via-vpc-peering): If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account. Note that you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier) using VPC peering.

- [Connect via SQL shell](#connect-via-sql-shell): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges

> **Tip:**
>
> For production environments, it is recommended to use the [private endpoint](#connect-via-private-endpoint-recommended) connection.

## Connect via standard connection

<SimpleTab>
<div label="Serverless Tier">

To connect to a Serverless Tier cluster via standard connection, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, and click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.

3. Under **Connect with a SQL client** in the dialog, click the tab of your preferred connection method, and then connect to your cluster with the connection string.

    > **Note:**
    >
    > - When you connect to a Serverless Tier cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).
    > - Serverless Tier clusters only support TLS connection. For more information, see [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md).

</div>

<div label="Dedicated Tier">

To connect to a Dedicated Tier cluster via standard connection, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, and click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.

3. Create a traffic filter for the cluster. Traffic filter is a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

    If the traffic filter is already set, skip the following sub-steps. If the traffic filter is empty, take the following sub-steps to add one.

    1. Click one of the buttons to add some rules quickly.

        - **Add My Current IP Address**
        - **Allow Access from Anywhere**

    2. Provide an optional description for the newly added IP address or CIDR range.

    3. Click **Create Filter** to confirm the changes.

4. Under **Step 2: Download TiDB cluster CA** in the dialog, click **Download TiDB cluster CA** for TLS connection to TiDB clusters. The TiDB cluster CA supports TLS 1.2 version by default.

    > **Note:**
    >
    > - The TiDB cluster CA is only available for Dedicated Tier clusters.
    > - Currently, TiDB Cloud only provides the connection strings and sample code for these connection methods: MySQL, MyCLI, JDBC, Python, Go, and Node.js.

5. Under **Step 3: Connect with a SQL client** in the dialog, click the tab of your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

    Note that you need to use the path of the downloaded CA file as the argument of the `--ssl-ca` option in the connection string.

</div>
</SimpleTab>

## Connect via private endpoint (recommended)

> **Note:**
>
> This method does not work for Serverless Tier clusters because you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier) using private endpoint.

To connect to your TiDB cluster via private endpoint, perform the following steps:

1. In the TiDB Cloud console, navigate to the **Clusters** page.
2. Locate your cluster, and click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.
3. Select the **Private Endpoint** tab.
4. Set up a private endpoint. See [Set Up Private Endpoint Connections](/tidb-cloud/set-up-private-endpoint-connections.md#set-up-a-private-endpoint-with-aws).

    If you have created a private endpoint, it is displayed under **Step 1: Create Private Endpoint**.

5. Under **Step 2: Connect your application**, click the tab of your preferred connection method, and then connect to your cluster with the connection string. The placeholders `<cluster_endpoint_name>:<port>` in the connection string are automatically replaced with the real values.

> **Tip:**
>
> If you cannot connect to the cluster, the reason might be that the security group of your VPC endpoint in AWS is not properly set. See [this FAQ](/tidb-cloud/set-up-private-endpoint-connections.md#troubleshooting) for solutions.

## Connect via VPC peering

> **Note:**
>
> This method does not work for Serverless Tier clusters because you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier) using VPC peering.

To connect to your TiDB cluster via VPC peering, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, click **Connect** in the upper-right corner of the cluster area, and select the **VPC Peering** tab in the connection dialog.

3. Set up VPC peering. See [Set up VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) for details.

4. Click **Get Endpoint** and wait for a few minutes. Then the connection command displays in the dialog.

5. Under **Step 2: Connect with a SQL client** in the dialog box, click the tab of your preferred connection method, and then connect to your cluster with the connection string.

## Connect via SQL Shell

To connect to your TiDB cluster using SQL shell, perform the following steps:

1. Navigate to the **Clusters** page.

2. Locate your cluster, click **Connect** in the upper-right corner of the cluster area, and select the **Web SQL Shell** tab in the connection dialog.

3. Click **Open SQL Shell**.

4. On the prompted **TiDB password** line, enter the root password of the current cluster. Then your application is connected to the TiDB cluster.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
