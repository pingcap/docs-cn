---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of a Dedicated Tier cluster.

> **Note:**
>
> You cannot change the size of a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier) cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure both node size and node quantity for TiDB.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiDB node size

The supported node sizes include the following:

- 2 vCPU, 8 GiB (Beta)
- 4 vCPU, 16 GiB
- 8 vCPU, 16 GiB
- 16 vCPU, 32 GiB

> **Note:**
>
> If the node size of TiDB is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiDB can only be used with 2 vCPU TiKV. 4 vCPU TiDB can only be used with 4 vCPU TiKV.
> - TiFlash is unavailable.

### TiDB node quantity

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure node size, node quantity, and node storage for TiKV.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiKV node size

The supported node sizes include the following:

- 2 vCPU, 8 GiB (Beta)
- 4 vCPU, 16 GiB
- 8 vCPU, 32 GiB
- 8 vCPU, 64 GiB
- 16 vCPU, 64 GiB

> **Note:**
>
> If the node size of TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - 2 vCPU TiKV can only be used with 2 vCPU TiDB. 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

### TiKV node quantity

The number of TiKV nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

TiDB Cloud deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

Recommended number of TiKV nodes: `ceil(compressed size of your data ÷ TiKV storage usage ratio ÷ one TiKV capacity) × the number of replicas`

Supposing the size of your MySQL dump files is 5 TB and the TiDB compression ratio is 40%, the storage needed is 2048 GiB.

Generally, the usage ratio of TiKV storage is not recommended to exceed 80%.

For example, if you configure the node storage of each TiKV node on AWS as 1024 GiB, the required number of TiKV nodes is as follows:

Minimum number of TiKV nodes: `ceil(2048 ÷ 0.8 ÷ 1024) × 3 = 9`

### TiKV node storage

The supported node storage of different TiKV node sizes is as follows:

| Node size | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 2 vCPU    | 200 GiB          | 500 GiB          | 200 GiB              |
| 4 vCPU    | 200 GiB          | 2048 GiB         | 500 GiB              |
| 8 vCPU    | 200 GiB          | 4096 GiB         | 500 GiB              |
| 16 vCPU   | 200 GiB          | 4096 GiB         | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiKV node storage after the cluster creation.

## Size TiFlash

TiFlash synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure node size, node quantity, and node storage for TiFlash.

### TiFlash node size

The supported node sizes include the following:

- 8 vCPU, 64 GiB
- 16 vCPU, 128 GiB

Note that TiFlash is unavailable when the vCPU size of TiDB or TiKV is set as **2 vCPU, 8 GiB (Beta)** or **4 vCPU, 16 GiB**.

### TiFlash node quantity

TiDB Cloud deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud cluster and create at least two replicas of the data for high availability in your production environment.

The minimum number of TiFlash nodes depends on the TiFlash replica counts for specific tables:

Minimum number of TiFlash nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the node storage of each TiFlash node on AWS as 1024 GiB, and set 2 replicas for table A (the compressed size is 800 GiB) and 1 replica for table B (the compressed size is 100 GiB), then the required number of TiFlash nodes is as follows:

Minimum number of TiFlash nodes: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlash node storage

The supported node storage of different TiFlash node sizes is as follows:

| Node size | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 8 vCPU    | 200 GiB          | 2048 GiB         | 500 GiB              |
| 16 vCPU   | 200 GiB          | 2048 GiB         | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiFlash node storage after the cluster creation.
