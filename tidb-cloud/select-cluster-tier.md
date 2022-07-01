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
- 1 TiKV shared node (with 500 MiB of OLTP storage)
- 1 TiFlash<sup>beta</sup> shared node (with 500 MiB of OLAP storage)

Developer Tier clusters run on shared nodes. Although each node is run in its own container on a virtual machine (VM), that VM is also running other TiDB, TiKV, or TiFlash<sup>beta</sup> nodes. As a result, shared nodes will have reduced performance when compared to standard, dedicated TiDB Cloud nodes. However, as all nodes are running in separate containers and have dedicated cloud disks, data stored in a Developer Tier cluster is isolated and will never be exposed to other TiDB clusters.

For each TiDB Cloud account, you can use one complimentary Developer Tier cluster to use for one year. Although you can only run one Developer Tier cluster at a time, you can delete and recreate the cluster as many times as you wish.

The one-year free trial begins the day the first Developer Tier cluster is created.

### Developer Tier special terms and conditions

- No uptime SLA guarantee.
- No high availability or automatic failover.
- Upgrades to clusters might incur significant downtimes.
- Each cluster allows one automatic daily backup and two manual backups.
- The maximum number of connections to the Dev Tier cluster is 50.
- You cannot create any changefeeds (Apache Kafka Sink and MySQL Sink) or use [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) to replicate incremental data.
- You cannot use VPC Peering to connect to clusters.
- You cannot scale clusters to larger storage, standard nodes, or increase the number of nodes.
- You cannot use a third-party monitoring service.
- You cannot customize the port number of a TiDB cluster.
- The data transfer is limited to a total of 20 GiB in and out per week. If the 20 GiB limit is reached, the network traffic will be throttled to 10 KB/s.
- The cluster will be backed up and shut down after 7 days of inactivity. To use the cluster again, you can restore it from previous backups.

## Dedicated Tier

The TiDB Cloud Dedicated Tier is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For Dedicated Tier clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash<sup>beta</sup> easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a Dedicated Tier cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot change the cluster storage size after your cluster is created.