---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# Select Your Cluster Tier

The cluster tier determines the throughput and performance of your cluster.

TiDB Cloud provides the following two options of cluster tiers. Before creating a cluster, you need to consider which option suits your need better.

- [Serverless Tier](#serverless-tier)
- [Dedicated Tier](#dedicated-tier)

## Serverless Tier

The TiDB Cloud Serverless Tier (previously called Developer Tier) is a fully managed service of TiDB. It's still in beta and should not be used in production. However, you can use Serverless Tier clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for your datasets.

For each TiDB Cloud account, you can create a complimentary Serverless Tier cluster to use during the beta phase. Although you can only run one Serverless Tier cluster at a time, you can delete and recreate the cluster as many times as you wish.

### User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each Serverless Tier cluster, TiDB Cloud generates a unique prefix to distinguish it from other clusters.

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

1. Navigate to the **Clusters** page.
2. Click **Connect** in the upper-right corner of the cluster area. A connection dialog box is displayed.
3. In the dialog, locate **Step 2: Connect with a SQL client** and get the prefix in the connection string.

### Serverless Tier special terms and conditions

- Serverless Tier does not have uptime SLA guarantee during beta phase. If you use Serverless Tier beta to store a commercial or production dataset, any potential risk associated with the use should be taken on your own, and PingCAP shall not be liable for any damage.
- The backup and restore feature is unavailable. You can use [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) to export your data as a backup.
- You cannot create any changefeeds (Apache Kafka Sink and MySQL Sink) or use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) to replicate incremental data.
- You cannot use VPC Peering or private endpoint to connect to Serverless Tier clusters.
- You cannot scale clusters to larger storage, standard nodes, or increase the number of nodes.
- You cannot [pause or resume](/tidb-cloud/pause-or-resume-tidb-cluster.md) a Serverless Tier cluster.
- You cannot view the [Monitoring page](/tidb-cloud/built-in-monitoring.md).
- You cannot use the third-party monitoring service.
- You cannot customize the port number of a TiDB cluster.
- The data transfer is limited to a total of 20 GiB in and out per week. If the 20 GiB limit is reached, the network traffic will be throttled to 10 KB/s.

## Dedicated Tier

The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For Dedicated Tier clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a Dedicated Tier cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot decrease the node storage after your cluster is created.
