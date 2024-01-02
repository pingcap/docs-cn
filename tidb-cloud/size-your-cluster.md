---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of a TiDB Dedicated cluster.

> **Note:**
>
> You cannot change the size of a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) cluster.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure node number, vCPU, and RAM for TiDB.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiDB vCPU and RAM

The supported vCPU and RAM sizes include the following:

- 4 vCPU, 16 GiB
- 8 vCPU, 16 GiB
- 16 vCPU, 32 GiB

> **Note:**
>
> If the vCPU and RAM size of TiDB is set as **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node number of TiDB can only be set to 1 or 2, and the node number of TiKV is fixed to 3.
> - 4 vCPU TiDB can only be used with 4 vCPU TiKV.
> - TiFlash is unavailable.

### TiDB node number

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

In general, TiDB performance increases linearly with the number of TiDB nodes. However, when the number of TiDB nodes exceeds 8, the performance increment becomes slightly less than linearly proportional. For each additional 8 nodes, the performance deviation coefficient is about 5%.

For example:

- When there are 9 TiDB nodes, the performance deviation coefficient is about 5%, so the TiDB performance is about `9 * (1 - 5%) = 8.55` times the performance of a single TiDB node.
- When there are 16 TiDB nodes, the performance deviation coefficient is about 10%, so the TiDB performance is `16 * (1 - 10%) = 14.4` times the performance of a single TiDB node.

For a specified latency of a TiDB node, the TiDB performance varies depending on the different read-write ratios.

The performance of an 8 vCPU, 16 GiB TiDB node in different workloads is as follows:

| Workload | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
|----------|-------------------|-------------------|-------------------|
| Read     | 18,900            | 9,450             | 6,300             |
| Mixed    | 15,500            | 7,750             | 5,200             |
| Write    | 18,000            | 9,000             | 6,000             |

If the number of TiDB nodes is less than 8, the performance deviation coefficient is nearly 0%, so the TiDB performance of 16 vCPU, 32 GiB TiDB nodes is roughly twice that of 8 vCPU, 16 GiB TiDB nodes. If the number of TiDB nodes exceeds 8, it is recommended to choose 16 vCPU, 32 GiB TiDB nodes as this will require fewer nodes, which means smaller performance deviation coefficient.

When planning your cluster size, you can estimate the number of TiDB nodes according to your workload type, your overall expected performance (QPS), and the performance of a single TiDB node corresponding to the workload type using the following formula:

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

In the formula, you need to calculate `node num = ceil(overall expected performance ÷ performance per node)` first to get a rough node number, and then use the corresponding performance deviation coefficient to get the final result of the node number.

For example, your overall expected performance is 110,000 QPS under a mixed workload, your P95 latency is about 100 ms, and you want to use 8 vCPU, 16 GiB TiDB nodes. Then, you can get the estimated TiDB performance of an 8 vCPU, 16 GiB TiDB node from the preceding table (which is `15,500`), and calculate a rough number of TiDB nodes as follows:

`node num = ceil(110,000 ÷ 15,500) = 8`

As the performance deviation coefficient of 8 nodes is about 5%, the estimated TiDB performance is `8 * 15,500 * (1 - 5%) = 117,800`, which can meet your expected performance of 110,000 QPS.

Therefore, 8 TiDB nodes (8 vCPU, 16 GiB) are recommended for you.

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure node number, vCPU and RAM, and storage for TiKV.

To learn performance test results of different cluster scales, see [TiDB Cloud Performance Reference](/tidb-cloud/tidb-cloud-performance-reference.md).

### TiKV vCPU and RAM

The supported vCPU and RAM sizes include the following:

- 4 vCPU, 16 GiB
- 8 vCPU, 32 GiB
- 8 vCPU, 64 GiB
- 16 vCPU, 64 GiB

> **Note:**
>
> If the vCPU and RAM size of TiKV is set as **4 vCPU, 16 GiB**, note the following restrictions:
>
> - The node number of TiDB can only be set to 1 or 2, and the node number of TiKV is fixed to 3.
> - 4 vCPU TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

### TiKV node number

The number of TiKV nodes should be **at least 1 set (3 nodes in 3 different Available Zones)**.

TiDB Cloud deploys TiKV nodes evenly to all availability zones (at least 3) in the region you select to achieve durability and high availability. In a typical 3-replica setup, your data is distributed evenly among the TiKV nodes across all availability zones and is persisted to the disk of each TiKV node.

> **Note:**
>
> When you scale your TiDB cluster, nodes in the 3 availability zones are increased or decreased at the same time. For how to scale in or scale out a TiDB cluster based on your needs, see [Scale Your TiDB Cluster](/tidb-cloud/scale-tidb-cluster.md).

Although TiKV is mainly used for data storage, the performance of the TiKV node also varies depending on different workloads. Therefore, when planning the number of TiKV nodes, you need to estimate it according to both your [**data volume**](#estimate-tikv-node-number-according-to-data-volume) and [expected performance](#estimate-tikv-node-number-according-to-expected-performance), and then take the larger of the two estimates as the recommended node number.

#### Estimate TiKV node number according to data volume

You can calculate a recommended number of TiKV nodes according to your data volume as follows:

`node num = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

Generally, it is recommended to keep the usage ratio of TiKV storage below 80%. The number of replicas in TiDB Cloud is 3 by default. The maximum storage capacity of an 8 vCPU, 64 GiB TiKV node is 4096 GiB.

Based on historical data, the average TiKV compression ratio is around 40%.

Suppose that the size of your MySQL dump files is 20 TB and the TiKV compression ratio is 40%. Then, you can calculate a recommended number of TiKV nodes according to your data volume as follows:

`node num = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### Estimate TiKV node number according to expected performance

Similarly as TiDB performance, TiKV performance increases linearly with the number of TiKV nodes. However, when the number of TiKV nodes exceeds 8, the performance increment becomes slightly less than linearly proportional. For each additional 8 nodes, the performance deviation coefficient is about 5%.

For example:

- When there are 9 TiKV nodes, the performance deviation coefficient is about 5%, so the TiKV performance is about `9 * (1 - 5%) = 8.55` times the performance of a single TiKV node.
- When there are 18 TiKV nodes, the performance deviation coefficient is about 10%, so the TiKV performance is `18 * (1 - 10%) = 16.2` times the performance of a single TiKV node.

For a specified latency of a TiKV node, the TiKV performance varies depending on the different read-write ratios.

The performance of an 8 vCPU, 32 GiB TiKV node in different workloads is as follows:

| Workload | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
|----------|-------------------|-------------------|-------------------|
| Read     | 28,000            | 14,000            | 7,000             |
| Mixed    | 17,800            | 8,900             | 4,450             |
| Write    | 14,500            | 7,250             | 3,625             |

If the number of TiKV nodes is less than 8, the performance deviation coefficient is nearly 0%, so the performance of 16 vCPU, 64 GiB TiKV nodes is roughly twice that of 8 vCPU, 32 GiB TiKV nodes. If the number of TiKV nodes exceeds 8, it is recommended to choose 16 vCPU, 64 GiB TiKV nodes as this will require fewer nodes, which means smaller performance deviation coefficient.

When planning your cluster size, you can estimate the number of TiKV nodes according to your workload type, your overall expected performance (QPS), and the performance of a single TiKV node corresponding to the workload type using the following formula:

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

In the formula, you need to calculate `node num = ceil(overall expected performance ÷ performance per node)` first to get a rough node number, and then use the corresponding performance deviation coefficient to get the final result of the node number.

For example, your overall expected performance is 110,000 QPS under a mixed workload, your P95 latency is about 100 ms, and you want to use 8 vCPU, 32 GiB TiKV nodes. Then, you can get the estimated TiKV performance of an 8 vCPU, 32 GiB TiKV node from the preceding table (which is `17,800`), and calculate a rough number of TiKV nodes as follows:

`node num = ceil(110,000 / 17,800 ) = 7`

As 7 is less than 8, the performance deviation coefficient of 7 nodes is 0. The estimated TiKV performance is `7 * 17,800 * (1 - 0) = 124,600`, which can meet your expected performance of 110,000 QPS.

Therefore, 7 TiKV nodes (8 vCPU, 32 GiB) are recommended for you according to your expected performance.

Next, you can compare the TiKV node number calculated according to data volume with the number calculated according to your expected performance, and take the larger one as a recommended number of your TiKV nodes.

### TiKV node storage

The supported node storage of different TiKV vCPUs is as follows:

| TiKV vCPU | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 4 vCPU    | 200 GiB          |     2048 GiB     | 500 GiB              |
| 8 vCPU    | 200 GiB          |     4096 GiB     | 500 GiB              |
| 16 vCPU   | 200 GiB          |     6144 GiB     | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiKV node storage after the cluster creation.

## Size TiFlash

TiFlash synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure node number, vCPU and RAM, and storage for TiFlash.

### TiFlash vCPU and RAM

The supported vCPU and RAM sizes include the following:

- 8 vCPU, 64 GiB
- 16 vCPU, 128 GiB

Note that TiFlash is unavailable when the vCPU and RAM size of TiDB or TiKV is set as **4 vCPU, 16 GiB**.

### TiFlash node number

TiDB Cloud deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud cluster and create at least two replicas of the data for high availability in your production environment.

The minimum number of TiFlash nodes depends on the TiFlash replica counts for specific tables:

Minimum number of TiFlash nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the node storage of each TiFlash node on AWS as 1024 GiB, and set 2 replicas for table A (the compressed size is 800 GiB) and 1 replica for table B (the compressed size is 100 GiB), then the required number of TiFlash nodes is as follows:

Minimum number of TiFlash nodes: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlash node storage

The supported node storage of different TiFlash vCPUs is as follows:

| TiFlash vCPU | Min node storage | Max node storage | Default node storage |
|:---------:|:----------------:|:----------------:|:--------------------:|
| 8 vCPU    | 200 GiB          | 2048 GiB         | 500 GiB              |
| 16 vCPU   | 200 GiB          | 2048 GiB         | 500 GiB              |

> **Note:**
>
> You cannot decrease the TiFlash node storage after the cluster creation.
