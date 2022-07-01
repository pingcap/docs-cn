---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of your TiDB cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure both vCPUs size and node quantity for TiDB.

### TiDB vCPUs size

The supported vCPU size includes 4 vCPU (Beta), 8 vCPU, and 16 vCPU.

> **Note:**
>
> If the vCPU size of TiDB is set as **4 vCPU (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiDB can only be used with TiKV with 4 vCPU.
> - TiFlash<sup>beta</sup> is not supported.

### TiDB node quantity

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure vCPUs size, node quantity, and storage size for TiKV.

### TiKV vCPUs size

The supported size includes 4 vCPU (Beta), 8 vCPU, and 16 vCPU.

> **Note:**
>
> If the vCPUs size of TiKV is set as **4 vCPU (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiKV can only be used with TiDB with 4 vCPU.
> - TiFlash<sup>beta</sup> is not supported.

### TiKV node quantity

The number of TiKV nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

TiDB Cloud deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

Minimum number of TiKV nodes: `ceil(compressed size of your data ÷ one TiKV capacity) × the number of replicas`

Supposing the size of your MySQL dump files is 5 TB and the TiDB compression ratio is 70%, the storage needed is 3584 GB.

For example, if you configure the storage size of each TiKV node on AWS as 1024 GB, the required number of TiKV nodes is as follows:

Minimum number of TiKV nodes: `ceil(3584 ÷ 1024) × 3 = 12`

### TiKV storage size

You can configure the TiKV storage size only when you create or restore a cluster.

## Size TiFlash<sup>beta</sup>

TiFlash<sup>beta</sup> synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure vCPUs size, node quantity, and storage size for TiFlash<sup>beta</sup>.

### TiFlash<sup>beta</sup> vCPUs size

The supported vCPUs size includes 8 vCPU and 16 vCPU.

If the vCPUs size of TiDB or TiKV is set as **4 vCPU (Beta)**, TiFlash<sup>beta</sup> is not supported.

### TiFlash<sup>beta</sup> node quantity

TiDB Cloud deploys TiFlash<sup>beta</sup> nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash<sup>beta</sup> nodes in each TiDB Cloud cluster and create at least 2 replicas of the data for high availability in your production environment.

The minimum number of TiFlash<sup>beta</sup> nodes depends on the TiFlash<sup>beta</sup> replica counts for specific tables:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the storage size of each TiFlash<sup>beta</sup> node on AWS as 1024 GB, and set 2 replicas for table A (the compressed size is 800 GB) and 1 replica for table B (the compressed size is 100 GB), then the required number of TiFlash<sup>beta</sup> nodes is as follows:

Minimum number of TiFlash<sup>beta</sup> nodes: `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`

### TiFlash<sup>beta</sup> storage size

You can configure the TiFlash<sup>beta</sup> storage size only when you create or restore a cluster.