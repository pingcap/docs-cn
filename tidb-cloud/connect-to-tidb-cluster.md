---
title: Connect to Your TiDB Cluster
summary: Connect to your TiDB cluster via a SQL client or SQL shell.
---

# Connect to Your TiDB Cluster

After your TiDB cluster is created on TiDB Cloud, you can use one of the following three methods to connect to your TiDB cluster. You can access your cluster via a SQL client, or quickly via SQL Shell in the TiDB Cloud Console.

+ Connect via a SQL client

    - [Connect via standard connection](#connect-via-standard-connection): The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster from your laptop.
    - [Connect via VPC peering](#connect-via-vpc-peering): If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account. Note that you cannot connect to [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier) using VPC peering.

- [Connect via SQL shell](#connect-via-sql-shell): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges

## Connect via standard connection

To connect to your TiDB cluster via standard connection, perform the following steps:

1. Navigate to the **Active Clusters** page and click the name of your newly created cluster.

2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.

3. Create the traffic filter for the cluster. Traffic filter is a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

    If the traffic filter is already set, skip the following sub-steps. If the traffic filter is empty, take the following sub-steps to add one.

    1. Click one of the buttons to add some rules quickly.

        - **Add My Current IP Address**
        - **Allow Access from Anywhere**

    2. Provide an optional description for the newly added IP address or CIDR range.

    3. Click **Create Filter** to confirm the changes.

4. Under **Step 2: Connect with a SQL client** in the dialog box, click the tab of your preferred connection method, and then connect to your cluster with the connection string.

> **Note:**
>
> For [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier), when you connect to your cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

## Connect via VPC peering

> **Note:**
>
> This method does not work for Developer Tier clusters because you cannot connect to [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier) using VPC peering.

To connect to your TiDB cluster via VPC peering, perform the following steps:

1. Navigate to the **Active Clusters** page and click the name of your newly created cluster.

2. Click **Connect**, and select the **VPC Peering** tab at the **Connect to TiDB** dialog.

3. Set up VPC peering. See [Set up VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) for details.

4. Click **Get Endpoint** and wait for a few minutes. Then the connection command displays in the dialog.

5. Use a SQL client to connect to TiDB from your server which has set up VPC peering with TiDB Cloud.

    {{< copyable "shell" >}}

    ```shell
    mysql -u root -h <endpoint> -P <port number> -p
    ```

## Connect via SQL Shell

To connect to your TiDB cluster using SQL shell, perform the following steps:

1. Navigate to the **Active Clusters** page and click the name of your newly created cluster.

2. Click **Connect**, and select the **Web SQL Shell** tab at the **Connect to TiDB** dialog.

3. Click **Open SQL Shell**.

4. On the prompted **TiDB password** line, enter the root password of the current cluster. Then your application is connected to the TiDB cluster.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](https://docs.pingcap.com/tidb/stable/basic-sql-operations).
