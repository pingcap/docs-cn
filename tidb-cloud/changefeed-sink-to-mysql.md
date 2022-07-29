---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# Sink to MySQL

> **Warning:**
>
> Currently, **Sink to MySQL** is an experimental feature. It is not recommended that you use it for production environments.

This document describes how to stream data from TiDB Cloud to MySQL using the **Sink to MySQL** changefeed.

## Prerequisites

### Network

Make sure that your TiDB Cluster can connect to the MySQL service.

If your MySQL service is in an AWS VPC that has no public internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
2. Modify the inbound rules of the security group that the MySQL service is associated with. 

    You must add the CIDR of the Region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the VPC Peering Page. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL instance.

3. If the MySQL URL contains a hostname, you need to allow TiDB Cloud to be able to resolve the DNS hostname of the MySQL service. 

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your MySQL service is in a GCP VPC that has no public internet access, take the following steps:

1. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You may need to use the [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) which is developed by Google.
2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster. 
3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add the CIDR of the Region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the VPC Peering Page. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL endpoint.

### Full load data

The **Sink to MySQL** connector can only sink incremental data from your TiDB cluster to MySQL after a certain timestamp. If you already have data in your TiDB cluster, you must export and load the full load data of your TiDB cluster into MySQL before enabling **Sink to MySQL**:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the full load data
    - The time to create **Sink to MySQL**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. Use [Dumpling](/dumpling-overview.md) to export data from your TiDB cluster, then use community tools such as [mydumper/myloader](https://centminmod.com/mydumper.html) to load data to the MySQL service.

3. From the [exported files of Dumpling](/dumpling-overview.md#format-of-exported-files), get the TSO from the metadata file:

    {{< copyable "shell-regular" >}}

    ```shell
    cat metadata
    ```

    The following is an example output. The "Pos" of "SHOW MASTER STATUS" is the TSO of the full load data.

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ``` 

## Create a Sink

After completing the prerequisites, you can sink your data to MySQL.

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Sink to MySQL**.
3. Fill in the MySQL URL, user, and password.
    - If you already have data in your TiDB Cluster, you must fill in a specific TSO number that Dumpling provides.
    - If you do not have any data in your TiDB Cluster, you can choose the "current" TSO.
4. Click **Test Connectivity**. If your TiDB Cluster can connect to the MySQL service, the **Confirm** button is displayed.
5. Click **Confirm** and after a while, the sink will begin its work, and the status of the sink will be changed to "**Producing**".
6. After the operation is complete, set the GC time back (the default value is `10m`):

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```

## Delete a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click the trash button of **Sink to MySQL**.

## Restrictions

Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).
