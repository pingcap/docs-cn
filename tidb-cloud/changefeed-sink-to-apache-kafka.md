---
title: Sink to Apache Kafka (Beta)
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.
---

# Sink to Apache Kafka (Beta)

This document describes how to create a changefeed to stream data from TiDB Cloud to Apache Kafka.

> **Note:**
>
> - Currently, Kafka sink is in **beta**. To use the changefeed feature, make sure that your TiDB Dedicated cluster version is v6.4.0 or later.
> - For [TiDB Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-serverless), the changefeed feature is unavailable.

## Restrictions

- For each TiDB Cloud cluster, you can create up to 5 changefeeds.
- Currently, TiDB Cloud does not support uploading self-signed TLS certificates to connect to Kafka brokers.
- Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios).
- If the table to be replicated does not have a primary key or a non-null unique index, the absence of a unique constraint during replication could result in duplicated data being inserted downstream in some retry scenarios.

## Prerequisites

Before creating a changefeed to stream data to Apache Kafka, you need to complete the following prerequisites:

- Set up your network connection
- Add permissions for Kafka ACL authorization

### Network

Make sure that your TiDB cluster can connect to the Apache Kafka service.

If your Apache Kafka service is in an AWS VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster.
2. Modify the inbound rules of the security group that the Apache Kafka service is associated with.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

3. If the Apache Kafka URL contains hostnames, you need to allow TiDB Cloud to be able to resolve the DNS hostnames of the Apache Kafka brokers.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your Apache Kafka service is in a Google Cloud VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster.
2. Modify the ingress firewall rules of the VPC where Apache Kafka is located.

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the **VPC Peering** page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

### Kafka ACL authorization

To allow TiDB Cloud changefeeds to stream data to Apache Kafka and create Kafka topics automatically, ensure that the following permissions are added in Kafka:

- The `Create` and `Write` permissions are added for the topic resource type in Kafka.
- The `DescribeConfigs` permission is added for the cluster resource type in Kafka.

For example, if your Kafka cluster is in Confluent Cloud, you can see [Resources](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) and [Adding ACLs](https://docs.confluent.io/platform/current/kafka/authorization.html#adding-acls) in Confluent documentation for more information.

## Step 1. Open the changefeed page for Apache Kafka

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of the target TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Click **Create Changefeed**, and select **Kafka** as **Target Type**.

## Step 2. Configure the changefeed target

1. Under **Brokers Configuration**, fill in your Kafka brokers endpoints. You can use commas `,` to separate multiple endpoints.
2. Select your Kafka version. If you do not know that, use Kafka V2.
3. Select a desired compression type for the data in this changefeed.
4. Enable the **TLS Encryption** option if your Kafka has enabled TLS encryption and you want to use TLS encryption for the Kafka connection.
5. Select the **Authentication** option according to your Kafka authentication configuration.

    - If your Kafka does not require authentication, keep the default option **DISABLE**.
    - If your Kafka requires authentication, select the corresponding authentication type, and then fill in the user name and password of your Kafka account for authentication.

6. Click **Next** to check the configurations you set and go to the next page.

## Step 3. Set the changefeed

1. Customize **Table Filter** to filter the tables that you want to replicate. For the rule syntax, refer to [table filter rules](/table-filter.md).

    - **Add filter rules**: you can set filter rules in this column. By default, there is a rule `*.*`, which stands for replicating all tables. When you add a new rule, TiDB Cloud queries all the tables in TiDB and displays only the tables that match the rules in the **Tables to be replicated** column.
    - **Tables to be replicated**: this column shows the tables to be replicated. But it does not show the new tables to be replicated in the future or the schemas to be fully replicated.
    - **Tables without valid keys**: this column shows tables without unique and primary keys. For these tables, because no unique identifier can be used by the downstream system to handle duplicate events, their data might be inconsistent during replication. To avoid such issues, it is recommended that you add unique keys or primary keys to these tables before the replication, or set filter rules to filter out these tables. For example, you can filter out the table `test.tbl1` using "!test.tbl1".

2. In the **Data Format** area, select your desired format of Kafka messages.

   - Avro is a compact, fast, and binary data format with rich data structures, which is widely used in various flow systems. For more information, see [Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol).
   - Canal-JSON is a plain JSON text format, which is easy to parse. For more information, see [Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json).

3. Enable the **TiDB Extension** option if you want to add TiDB-extension fields to the Kafka message body.

    For more information about TiDB-extension fields, see [TiDB extension fields in Avro data format](https://docs.pingcap.com/tidb/stable/ticdc-avro-protocol#tidb-extension-fields) and [TiDB extension fields in Canal-JSON data format](https://docs.pingcap.com/tidb/stable/ticdc-canal-json#tidb-extension-field).

4. If you select **Avro** as your data format, you will see some Avro-specific configurations on the page. You can fill in these configurations as follows:

    - In the **Decimal** and **Unsigned BigInt** configurations, specify how TiDB Cloud handles the decimal and unsigned bigint data types in Kafka messages.
    - In the **Schema Registry** area, fill in your schema registry endpoint. If you enable **HTTP Authentication**, the fields for user name and password are displayed and automatically filled in with your TiDB cluster endpoint and password.

5. In the **Topic Distribution** area, select a distribution mode, and then fill in the topic name configurations according to the mode.

    If you select **Avro** as your data format, you can only choose the **Distribute changelogs by table to Kafka Topics** mode in the **Distribution Mode** drop-down list.

    The distribution mode controls how the changefeed creates Kafka topics, by table, by database, or creating one topic for all changelogs.

   - **Distribute changelogs by table to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each table, choose this mode. Then, all Kafka messages of a table are sent to a dedicated Kafka topic. You can customize topic names for tables by setting a topic prefix, a separator between a database name and table name, and a suffix. For example, if you set the separator as `_`, the topic names are in the format of `<Prefix><DatabaseName>_<TableName><Suffix>`.

        For changelogs of non-row events, such as Create Schema Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will create a topic accordingly to collect such changelogs.

   - **Distribute changelogs by database to Kafka Topics**

        If you want the changefeed to create a dedicated Kafka topic for each database, choose this mode. Then, all Kafka messages of a database are sent to a dedicated Kafka topic. You can customize topic names of databases by setting a topic prefix and a suffix.

        For changelogs of non-row events, such as Resolved Ts Event, you can specify a topic name in the **Default Topic Name** field. The changefeed will create a topic accordingly to collect such changelogs.

   - **Send all changelogs to one specified Kafka Topic**

        If you want the changefeed to create one Kafka topic for all changelogs, choose this mode. Then, all Kafka messages in the changefeed will be sent to one Kafka topic. You can define the topic name in the **Topic Name** field.

6. In the **Partition Distribution** area, you can decide which partition a Kafka message will be sent to:

   - **Distribute changelogs by index value to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to different partitions, choose this distribution method. The index value of a row changelog will determine which partition the changelog is sent to. This distribution method provides a better partition balance and ensures row-level orderliness.

   - **Distribute changelogs by table to Kafka partition**

        If you want the changefeed to send Kafka messages of a table to one Kafka partition, choose this distribution method. The table name of a row changelog will determine which partition the changelog is sent to. This distribution method ensures table orderliness but might cause unbalanced partitions.

7. In the **Topic Configuration** area, configure the following numbers. The changefeed will automatically create the Kafka topics according to the numbers.

   - **Replication Factor**: controls how many Kafka servers each Kafka message is replicated to.
   - **Partition Number**: controls how many partitions exist in a topic.

8. Click **Next**.

## Step 4. Configure your changefeed specification

1. In the **Changefeed Specification** area, specify the number of Replication Capacity Units (RCUs) to be used by the changefeed.
2. In the **Changefeed Name** area, specify a name for the changefeed.
3. Click **Next** to check the configurations you set and go to the next page.

## Step 5. Review the configurations

On this page, you can review all the changefeed configurations that you set.

If you find any error, you can go back to fix the error. If there is no error, you can click the check box at the bottom, and then click **Create** to create the changefeed.
