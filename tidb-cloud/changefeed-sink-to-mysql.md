---
title: Sink to MySQL
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to MySQL.
---

# Sink to MySQL

This document describes how to stream data from TiDB Cloud to MySQL using the **Sink to MySQL** changefeed.

> **Note:**
>
> - To use the changefeed feature, make sure that your TiDB Dedicated cluster version is v6.4.0 or later.
> - For [TiDB Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-serverless), the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 5 changefeeds.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed, you need to complete the following prerequisites:

- Set up your network connection
- Export and load the existing data to MySQL (optional)
- Create corresponding target tables in MySQL if you do not load the existing data and only want to replicate incremental data to MySQL

### Network

Make sure that your TiDB Cluster can connect to the MySQL service.

If your MySQL service is in an AWS VPC that has no public internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
2. Modify the inbound rules of the security group that the MySQL service is associated with.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the inbound rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL instance.

3. If the MySQL URL contains a hostname, you need to allow TiDB Cloud to be able to resolve the DNS hostname of the MySQL service.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your MySQL service is in a Google Cloud VPC that has no public internet access, take the following steps:

1. If your MySQL service is Google Cloud SQL, you must expose a MySQL endpoint in the associated VPC of the Google Cloud SQL instance. You may need to use the [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) which is developed by Google.
2. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the MySQL service and your TiDB cluster.
3. Modify the ingress firewall rules of the VPC where MySQL is located.

    You must add [the CIDR of the region where your TiDB Cloud cluster is located](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-project-cidr) to the ingress firewall rules. Doing so allows the traffic to flow from your TiDB Cluster to the MySQL endpoint.

### Load existing data (optional)

The **Sink to MySQL** connector can only sink incremental data from your TiDB cluster to MySQL after a certain timestamp. If you already have data in your TiDB cluster, you can export and load the existing data of your TiDB cluster into MySQL before enabling **Sink to MySQL**.

To load the existing data:

1. Extend the [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) to be longer than the total time of the following two operations, so that historical data during the time is not garbage collected by TiDB.

    - The time to export and import the existing data
    - The time to create **Sink to MySQL**

    For example:

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. Use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export data from your TiDB cluster, then use community tools such as myloader to load data to the MySQL service.

3. From the [exported files of Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files), get the start position of MySQL sink from the metadata file:

    The following is a part of an example metadata file. The `Pos` of `SHOW MASTER STATUS` is the TSO of the existing data, which is also the start position of MySQL sink.

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

### Create target tables in MySQL

If you do not load the existing data, you need to create corresponding target tables in MySQL manually to store the incremental data from TiDB. Otherwise, the data will not be replicated.

## Create a MySQL sink

After completing the prerequisites, you can sink your data to MySQL.

1. Navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.

2. Click **Create Changefeed**, and select **MySQL** as **Target Type**.

3. Fill in the MySQL endpoints, user name, and password in **MySQL Connection**.

4. Click **Next** to test whether TiDB can connect to MySQL successfully:

    - If yes, you are directed to the next step of configuration.
    - If not, a connectivity error is displayed, and you need to handle the error. After the error is resolved, click **Next** again.

5. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Add filter rules**: you can set filter rules in this column. By default, there is a rule `*. *`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the box on the right.
    - **Tables to be replicated**: this column shows the tables to be replicated. But it does not show the new tables to be replicated in the future or the schemas to be fully replicated.
    - **Tables without valid keys**: this column shows tables without unique and primary keys. For these tables, because no unique identifier can be used by the downstream system to handle duplicate events, their data might be inconsistent during replication. To avoid such issues, it is recommended that you add unique keys or primary keys to these tables before the replication, or set filter rules to filter out these tables. For example, you can filter out the table `test.tbl1` using "!test.tbl1".

6. In **Start Position**, configure the starting position for your MySQL sink.

    - If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, select **Start replication from a specific TSO** and fill in the TSO that you get from Dumpling exported metadata files.
    - If you do not have any data in the upstream TiDB cluster, select **Start replication from now on**.
    - Otherwise, you can customize the start time point by choosing **Start replication from a specific time**.

7. Click **Next** to configure your changefeed specification.

    - In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
    - In the **Changefeed Name** area, specify a name for the changefeed.

8. Click **Next** to review the changefeed configuration.

    If you confirm all configurations are correct, check the compliance of cross-region replication, and click **Create**.

    If you want to modify some configurations, click **Previous** to go back to the previous configuration page.

9. The sink starts soon, and you can see the status of the sink changes from "**Creating**" to "**Running**".

    Click the changefeed name, and you can see more details about the changefeed, such as the checkpoint, replication latency, and other metrics.

10. If you have [loaded the existing data](#load-existing-data-optional) using Dumpling, you need to restore the GC time to its original value (the default value is `10m`) after the sink is created:

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
