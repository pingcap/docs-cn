---
title: Sink to Apache Kafka
Summary: Learn how to create a changefeed to stream data from TiDB Cloud to Apache Kafka. 
---

# Sink to Apache Kafka

> **Warning:**
>
> Currently, **Sink to Apache Kafka** is an experimental feature. It is not recommended that you use it for production environments.

This document describes how to stream data from TiDB Cloud to Apache Kafka using the **Sink to Apache Kafka** changefeed.

## Prerequisites

### Network

Make sure that your TiDB Cluster can connect to the Apache Kafka service.

If your Apache Kafka service is in an AWS VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster. 
2. Modify the inbound rules of the security group that the Apache Kafka service is associated with. 

    You must add the CIDR of the region where your TiDB Cloud cluster is located to the inbound rules. The CIDR can be found on the VPC Peering page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

3. If the Apache Kafka URL contains hostnames, you need to allow TiDB Cloud to be able to resolve the DNS hostnames of the Apache Kafka brokers.

    1. Follow the steps in [Enable DNS resolution for a VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns).
    2. Enable the **Accepter DNS resolution** option.

If your Apache Kafka service is in a GCP VPC that has no internet access, take the following steps:

1. [Set up a VPC peering connection](/tidb-cloud/set-up-vpc-peering-connections.md) between the VPC of the Apache Kafka service and your TiDB cluster. 
2. Modify the ingress firewall rules of the VPC where Apache Kafka is located. 

    You must add the CIDR of the Region where your TiDB Cloud cluster is located to the ingress firewall rules. The CIDR can be found on the VPC Peering page. Doing so allows the traffic to flow from your TiDB cluster to the Kafka brokers.

### Topic

You must prepare a Topic before creating an Apache Kafka Sink. Based on table, the Sink will distribute data to different partitions of the Topic.

## Create a Sink

After completing the Prerequisites, you can sink your data to Apache Kafka.

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Sink to Apache Kafka**.
3. Fill the Kafka URL and Kafka Topic.
4. Click **Test Connectivity**. If your TiDB Cluster can connect to the Apache Kafka service, the **Confirm** button is displayed.
5. Click **Confirm** and after a while, the sink will begin its work, and the status of the sink will be changed to "**Producing**".

## Delete a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click the trash button of **Sink to Apache Kafka**

## Restrictions

Because TiDB Cloud uses TiCDC to establish changefeeds, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).
