---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# Select Your Cluster Tier

The cluster tier determines the throughput and performance of your cluster.

TiDB Cloud provides the following two options of cluster tiers. Before creating a cluster, you need to consider which option suits your need better.

- [Serverless Tier](#serverless-tier-beta)
- [Dedicated Tier](#dedicated-tier)

## Serverless Tier (Beta)

The TiDB Cloud Serverless Tier (previously called Developer Tier) is a fully managed service of TiDB. It's still in beta and should not be used in production. However, you can use Serverless Tier clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for your datasets.

For each TiDB Cloud account, you can create a maximum of five complimentary Serverless Tier clusters to use during the beta phase.

### User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each Serverless Tier cluster, TiDB Cloud generates a unique prefix to distinguish it from other clusters.

Whenever you use or set a database user name, you must include the prefix in the user name. For example, assume that the prefix of your cluster is `3pTAoNNegb47Uc8`.

- To connect to your cluster:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > Serverless Tier requires TLS connection. To find the CA root path on your system, see [CA root path lists](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#where-is-the-ca-root-path-on-my-system).

- To create a database user:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

To get the prefix for your cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.
2. Click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the dialog, get the prefix from the connection string.

### Serverless Tier special terms and conditions

- Serverless Tier is currently in beta and does not have uptime SLA guarantee during beta phase. If you use Serverless Tier beta to store a commercial or production dataset, any potential risk associated with the use should be taken on your own, and PingCAP shall not be liable for any damage.
- Some of TiDB Cloud features are partially supported or not supported on Serverless Tier. See [Serverless Tier Limitations](/tidb-cloud/serverless-tier-limitations.md) for details.

## Dedicated Tier

The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For Dedicated Tier clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a Dedicated Tier cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot decrease the node storage after your cluster is created.
