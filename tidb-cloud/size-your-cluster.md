---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# Determine Your TiDB Size

This document describes how to determine the size of a Dedicated Tier cluster.

> **Note:**
>
> A [Developer Tier cluster](/tidb-cloud/select-cluster-tier.md#developer-tier) comes with a default cluster size, which cannot be changed.

## Size TiDB

TiDB is for computing only and does not store data. It is horizontally scalable.

You can configure both node size and node quantity for TiDB.

### TiDB node size

The supported node sizes include the following:

- 4 vCPU, 16 GiB (Beta)
- 8 vCPU, 16 GiB
- 16 vCPU, 32 GiB

> **Note:**
>
> If the node size of TiDB is set as **4 vCPU, 16 GiB (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiDB can only be used with 4 vCPU TiKV.
> - TiFlash is unavailable.

### TiDB node quantity

For high availability, it is recommended that you configure at least two TiDB nodes for each TiDB Cloud cluster.

For more information about how to determine the TiDB size, see [Performance reference](#performance-reference).

## Size TiKV

TiKV is responsible for storing data. It is horizontally scalable.

You can configure node size, node quantity, and storage size for TiKV.

### TiKV node size

The supported node sizes include the following:

- 4 vCPU, 16 GiB (Beta)
- 8 vCPU, 32 GiB
- 8 vCPU, 64 GiB
- 16 vCPU, 64 GiB

> **Note:**
>
> If the node size of TiKV is set as **4 vCPU, 16 GiB (Beta)**, note the following restrictions:
>
> - The node quantity of TiDB can only be set to 1 or 2, and the node quantity of TiKV is fixed to 3.
> - TiKV can only be used with 4 vCPU TiDB.
> - TiFlash is unavailable.

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

For more information about how to determine the TiKV size, see [Performance reference](#performance-reference).

### TiKV storage size

- 8 vCPU or 16 vCPU TiKV supports up to 4 TiB storage capacity.
- 4 vCPU TiKV supports up to 2 TiB storage capacity.

> **Note:**
>
> You cannot decrease the TiKV storage size after the cluster creation.

## Size TiFlash

TiFlash synchronizes data from TiKV in real time and supports real-time analytics workloads right out of the box. It is horizontally scalable.

You can configure node size, node quantity, and storage size for TiFlash.

### TiFlash node size

The supported node sizes include the following:

- 8 vCPU, 64 GiB
- 16 vCPU, 128 GiB

Note that TiFlash is unavailable when the vCPU size of TiDB or TiKV is set as **4 vCPU, 16 GiB (Beta)**.

### TiFlash node quantity

TiDB Cloud deploys TiFlash nodes evenly to different availability zones in a region. It is recommended that you configure at least two TiFlash nodes in each TiDB Cloud cluster and create at least two replicas of the data for high availability in your production environment.

The minimum number of TiFlash nodes depends on the TiFlash replica counts for specific tables:

Minimum number of TiFlash nodes: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

For example, if you configure the storage size of each TiFlash node on AWS as 1024 GB, and set 2 replicas for table A (the compressed size is 800 GB) and 1 replica for table B (the compressed size is 100 GB), then the required number of TiFlash nodes is as follows:

Minimum number of TiFlash nodes: `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`

### TiFlash storage size

TiFlash supports up to 2 TiB storage capacity.

> **Note:**
>
> You cannot decrease the TiFlash storage size after the cluster creation.

## Performance reference

This section provides [TPC-C](https://www.tpc.org/tpcc/) and [Sysbench](https://github.com/akopytov/sysbench) performance test results of five popular TiDB cluster scales, which can be taken as a reference when you determine the cluster size.

Test environment:

- TiDB version: v5.4.0
- Warehouses: 5000
- Data size: 366 G
- Table size: 10000000
- Table count: 16

You can click any of the following scales to check its performance data.

<details>
<summary>TiDB: 4 vCPU * 2; TiKV: 4 vCPU * 3</summary>

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|---------------|
    | TPCC              | 300     | 14,532 | 13,137 | 608           |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|---------------|
    | Insert            | 300     | 8,848  | 8,848  | 36            |
    | Point Select      | 600     | 46,224 | 46,224 | 13            |
    | Read Write        | 150     | 719    | 14,385 | 209           |
    | Update Index      | 150     | 4,346  | 4,346  | 35            |
    | Update Non-index  | 600     | 13,603 | 13,603 | 44            |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 1,200   | 15,208 | 13,748 | 2,321        |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|---------------|
    | Insert            | 1,500   | 11,601 | 11,601 | 129           |
    | Point Select      | 600     | 46,224 | 46,224 | 13            |
    | Read Write        | 150     | 14,385 | 719    | 209           |
    | Update Index      | 1,200   | 6,526  | 6,526  | 184           |
    | Update Non-index  | 1,500   | 14,351 | 14,351 | 105           |

</details>

<details>
<summary>TiDB: 8 vCPU * 2; TiKV: 8 vCPU * 3</summary>

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 600     | 32,266 | 29,168 | 548          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|---------------|
    | Insert            | 600     | 17,831 | 17,831 | 34            |
    | Point Select      | 600     | 93,287 | 93,287 | 6             |
    | Read Write        | 300     | 29,729 | 1,486  | 202           |
    | Update Index      | 300     | 9,415  | 9,415  | 32            |
    | Update Non-index  | 1,200   | 31,092 | 31,092 | 39            |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 1,200   | 33,394 | 30,188 | 1,048        |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|---------------|
    | Insert            | 2,000   | 23,633 | 23,633 | 84            |
    | Point Select      | 600     | 93,287 | 93,287 | 6             |
    | Read Write        | 600     | 30,464 | 1,523  | 394           |
    | Update Index      | 2,000   | 15,146 | 15,146 | 132           |
    | Update Non-index  | 2,000   | 34,505 | 34,505 | 58            |

</details>

<details>
<summary>TiDB: 8 vCPU * 4; TiKV: 8 vCPU * 6</summary>

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 1,200   | 62,918 | 56,878 | 310          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 1,200   | 33,892  | 33,892  | 23            |
    | Point Select      | 1,200   | 185,574 | 181,255 | 4             |
    | Read Write        | 600     | 59,160  | 2,958   | 127           |
    | Update Index      | 600     | 18,735  | 18,735  | 21            |
    | Update Non-index  | 2,400   | 60,629  | 60,629  | 23            |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 2,400   | 65,452 | 59,169 | 570          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 4,000   | 47,029  | 47,029  | 43            |
    | Point Select      | 1,200   | 185,574 | 181,255 | 4             |
    | Read Write        | 1,200   | 60,624  | 3,030   | 197           |
    | Update Index      | 4,000   | 30,140  | 30,140  | 67            |
    | Update Non-index  | 4,000   | 68,664  | 68,664  | 29            |

</details>

<details>
<summary>TiDB: 16 vCPU * 2; TiKV: 16 vCPU * 3</summary>

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 1,200   | 67,941 | 61,419 | 540          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 1,200   | 35,096  | 35,096  | 34            |
    | Point Select      | 1,200   | 228,600 | 228,600 | 5             |
    | Read Write        | 600     | 73,150  | 3,658   | 164           |
    | Update Index      | 600     | 18,886  | 18,886  | 32            |
    | Update Non-index  | 2,000   | 63,837  | 63,837  | 31            |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Latency (ms) |
    |-------------------|---------|--------|--------|--------------|
    | TPCC              | 1,200   | 67,941 | 61,419 | 540          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 2,000   | 43,338  | 43,338  | 46            |
    | Point Select      | 1,200   | 228,600 | 228,600 | 5             |
    | Read Write        | 1,200   | 73,631  | 3,682   | 326           |
    | Update Index      | 3,000   | 29,576  | 29,576  | 101           |
    | Update Non-index  | 3,000   | 64,624  | 64,624  | 46            |

</details>

<details>
<summary>TiDB: 16 vCPU * 4; TiKV: 16 vCPU * 6</summary>

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC    | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|--------------|
    | TPCC              | 2,400   | 133,164 | 120,380 | 305          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 2,400   | 69,139  | 69,139  | 22            |
    | Point Select      | 2,400   | 448,056 | 448,056 | 4             |
    | Read Write        | 1,200   | 145,568 | 7,310   | 97            |
    | Update Index      | 1,200   | 36,638  | 36,638  | 20            |
    | Update Non-index  | 4,000   | 125,129 | 125,129 | 17            |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC    | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|--------------|
    | TPCC              | 2,400   | 133,164 | 120,380 | 305          |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Latency (ms) |
    |-------------------|---------|---------|---------|---------------|
    | Insert            | 4,000   | 86,242  | 86,242  | 25            |
    | Point Select      | 2,400   | 448,056 | 448,056 | 4             |
    | Read Write        | 2,400   | 146,526 | 7,326   | 172           |
    | Update Index      | 6,000   | 58,856  | 58,856  | 51            |
    | Update Non-index  | 6,000   | 128,601 | 128,601 | 24            |

</details>
