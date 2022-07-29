---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# Select Your Cluster Tier

The cluster tier determines the throughput and performance of your cluster.

TiDB Cloud provides the following two options of cluster tiers. Before creating a cluster, you need to consider which option suits your need better.

- [Developer Tier](#developer-tier)
- [Dedicated Tier](#dedicated-tier)

## Developer Tier

The TiDB Cloud Developer Tier is a one-year free trial of [TiDB Cloud](https://pingcap.com/products/tidbcloud), the fully managed service of TiDB. You can use Developer Tier clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for non-commercial datasets.

Each Developer Tier cluster is a full-featured TiDB cluster and comes with the following:

- 1 TiDB shared node
- 1 TiKV shared node (with 1 GiB of OLTP storage)
- 1 TiFlash shared node (with 1 GiB of OLAP storage)

Developer Tier clusters run on shared nodes. Although each node is run in its own container on a virtual machine (VM), that VM is also running other TiDB, TiKV, or TiFlash nodes. As a result, shared nodes will have reduced performance when compared to standard, dedicated TiDB Cloud nodes. However, as all nodes are running in separate containers and have dedicated cloud disks, data stored in a Developer Tier cluster is isolated and will never be exposed to other TiDB clusters.

For each TiDB Cloud account, you can use one complimentary Developer Tier cluster to use for one year. Although you can only run one Developer Tier cluster at a time, you can delete and recreate the cluster as many times as you wish.

The one-year free trial begins the day the first Developer Tier cluster is created.

### User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each Developer Tier cluster, TiDB Cloud generates a unique prefix to distinguish it from other clusters.

Whenever you use or set a database user name, you must include the prefix in the user name. For example, assume that the prefix of your cluster is `3pTAoNNegb47Uc8`.

- To connect to your cluster:

    ```shell
    mysql --connect-timeout 15 -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test -p
    ```

- To create a database user:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

To get the prefix for your cluster, take the following steps:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page of your project and click the name of your cluster.
2. In the cluster information pane on the left, click **Connect**. The **Connect to TiDB** dialog is displayed.
3. In the dialog, locate **Step 2: Connect with a SQL client** and get the prefix.

### Automatic hibernation and resuming

Once a Developer Tier cluster remains idle for 24 hours, the cluster hibernates automatically.

The hibernation does not affect your data stored in the cluster but only stops the monitoring information collection and computing resource consumption.

During the hibernation, the status of the cluster is still displayed as **Normal**, and you can see a message about hibernation in the TiDB Cloud console.

Anytime you want to use your Developer Tier cluster again, just connect to your cluster using your MySQL client driver or ORM framework as you usually do. The cluster will be resumed within 50 seconds and back to service automatically.

Alternatively, you can log in to the TiDB Cloud console, and then click **Resume** for the cluster on the **Active Clusters** page.

### Developer Tier special terms and conditions

- No uptime SLA guarantee.
- No high availability or automatic failover.
- Upgrades to clusters might incur significant downtimes.
- The backup and restore feature is unavailable. You can use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.
- The maximum number of connections to the Developer Tier cluster is 50.
- You cannot create any changefeeds (Apache Kafka Sink and MySQL Sink) or use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) to replicate incremental data.
- You cannot use VPC Peering to connect to clusters.
- You cannot scale clusters to larger storage, standard nodes, or increase the number of nodes.
- You cannot use a third-party monitoring service.
- You cannot customize the port number of a TiDB cluster.
- The data transfer is limited to a total of 20 GiB in and out per week. If the 20 GiB limit is reached, the network traffic will be throttled to 10 KB/s.

## Dedicated Tier

The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For Dedicated Tier clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a Dedicated Tier cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot decrease the cluster storage size after your cluster is created.