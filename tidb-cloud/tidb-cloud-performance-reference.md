---
title: TiDB Cloud Performance Reference
summary: Learn TiDB Cloud performance test results.
---

# TiDB Cloud Performance Reference

This document provides [Sysbench](https://github.com/akopytov/sysbench) performance test results of different TiDB cluster scales, which can be used as a reference when you [determine the cluster size](/tidb-cloud/size-your-cluster.md).

> **Note:**
>
> The tests are performed on TiDB v6.1.1, and the test results are based on the condition that the P95 latency is below 105 ms.

In this document, the transaction models `Read Only`, `Read Write`, and `Write Only` represent read workloads, mixed workloads, and write workloads. 

## 2 vCPU performance

Currently, the 2 vCPU support of TiDB and TiKV is still in beta.

Test scales:

- TiDB (2 vCPU, 8 GiB) \* 1; TiKV (2 vCPU, 8 GiB) \* 3
- TiDB (2 vCPU, 8 GiB) \* 2; TiKV (2 vCPU, 8 GiB) \* 3

Test results:

**TiDB (2 vCPU, 8 GiB) \* 1; TiKV (2 vCPU, 8 GiB) \* 3**

| Transaction model | Threads | QPS      | TPS    | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|----------|--------|----------------------|------------------|
| Read Only         | 15      | 3,496.77 | 218.55 | 68.63                | 95.81            |
| Read Write        | 5       | 1,545.90 | 77.29  | 64.68                | 94.10            |
| Write Only        | 40      | 4,326.57 | 721.10 | 55.47                | 90.78            |

**TiDB (2 vCPU, 8 GiB) \* 2; TiKV (2 vCPU, 8 GiB) \* 3**

Test results:

| Transaction model | Threads | QPS      | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|----------|----------|----------------------|------------------|
| Read Only         | 30      | 7,584.08 | 474.00   | 63.29                | 99.33            |
| Read Write        | 10      | 2,680.58 | 134.03   | 74.61                | 104.84           |
| Write Only        | 80      | 7,618.77 | 1,269.79 | 63.00                | 97.55            |

## 4 vCPU performance

Test scales:

- TiDB (4 vCPU, 16 GiB) \* 1; TiKV (4 vCPU, 16 GiB) \* 3
- TiDB (4 vCPU, 16 GiB) \* 2; TiKV (4 vCPU, 16 GiB) \* 3

Test results:

**TiDB (4 vCPU, 16 GiB) \* 1; TiKV (4 vCPU, 16 GiB) \* 3**

| Transaction model | Threads | QPS      | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|----------|----------|----------------------|------------------|
| Read Only         | 35      | 8,064.89 | 504.06   | 69.43                | 104.84           |
| Read Write        | 25      | 6,747.60 | 337.38   | 74.10                | 102.97           |
| Write Only        | 90      | 8,805.21 | 1,467.53 | 61.32                | 99.33            |

**TiDB (4 vCPU, 16 GiB) \* 2; TiKV (4 vCPU, 16 GiB) \* 3**

| Transaction model | Threads | QPS       | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|-----------|----------|----------------------|------------------|
| Read Only         | 65      | 16,805.76 | 1,050.36 | 61.88                | 95.81            |
| Read Write        | 45      | 12,940.36 | 647.02   | 69.55                | 99.33            |
| Write Only        | 200     | 19,265.93 | 3,210.99 | 62.28                | 102.97           |

## 8 vCPU performance

Test scales:

- TiDB (8 vCPU, 16 GiB) \* 2; TiKV (8 vCPU, 32 GiB) \* 3
- TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 3
- TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 6
- TiDB (8 vCPU, 16 GiB) \* 6; TiKV (8 vCPU, 32 GiB) \* 9
- TiDB (8 vCPU, 16 GiB) \* 9; TiKV (8 vCPU, 32 GiB) \* 6
- TiDB (8 vCPU, 16 GiB) \* 12; TiKV (8 vCPU, 32 GiB) \* 9

Test results:

**TiDB (8 vCPU, 16 GiB) \* 2; TiKV (8 vCPU, 32 GiB) \* 3**

| Transaction model | Threads | QPS       | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|-----------|----------|----------------------|------------------|
| Read Only         | 150     | 37,863.64 | 2,366.48 | 63.38                | 99.33            |
| Read Write        | 100     | 30,218.42 | 1,510.92 | 66.18                | 94.10            |
| Write Only        | 350     | 30,763.72 | 5,127.29 | 68.26                | 104.84           |

**TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 3**

| Transaction model | Threads | QPS       | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|-----------|----------|----------------------|------------------|
| Read Only         | 300     | 74,190.40 | 4,636.90 | 64.69                | 104.84           |
| Read Write        | 200     | 53,351.84 | 2,667.59 | 74.97                | 97.55            |
| Write Only        | 400     | 36,036.40 | 5,926.66 | 67.49                | 95.81            |

**TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 6**

| Transaction model | Threads | QPS       | TPS       | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|-----------|-----------|----------------------|------------------|
| Read Only         | 300     | 75,713.04 | 4,732.06  | 63.39                | 102.97           |
| Read Write        | 200     | 62,640.62 | 3,132.03  | 63.85                | 95.81            |
| Write Only        | 750     | 73,840.22 | 12,306.70 | 60.93                | 104.84           |

**TiDB (8 vCPU, 16 GiB) \* 6; TiKV (8 vCPU, 32 GiB) \* 9**

| Transaction model | Threads | QPS        | TPS       | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|------------|-----------|----------------------|------------------|
| Read Only         | 450     | 113,407.94 | 7,088.00  | 63.48                | 104.84           |
| Read Write        | 300     | 92,387.31  | 4,619.37  | 64.93                | 99.33            |
| Write Only        | 1100    | 112,631.72 | 18,771.95 | 58.59                | 99.33            |

**TiDB (8 vCPU, 16 GiB) \* 9; TiKV (8 vCPU, 32 GiB) \* 6**

| Transaction model | Threads | QPS        | TPS       | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|------------|-----------|----------------------|------------------|
| Read Only         | 650     | 168,486.65 | 10,530.42 | 61.72                | 101.13           |
| Read Write        | 400     | 106,853.63 | 5,342.68  | 74.86                | 101.13           |
| Write Only        | 950     | 88,461.20  | 14,743.53 | 64.42                | 102.97           |

**TiDB (8 vCPU, 16 GiB) \* 12; TiKV (8 vCPU, 32 GiB) \* 9**

| Transaction model | Threads | QPS        | TPS       | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|------------|-----------|----------------------|------------------|
| Read Only         | 800     | 211,882.77 | 13,242.67 | 60.40                | 101.13           |
| Read Write        | 550     | 139,393.46 | 6,969.67  | 78.90                | 104.84           |
| Write Only        | 1500    | 139,330.14 | 23,221.69 | 64.58                | 99.33            |

## 16 vCPU performance

Test scales:

- TiDB (16 vCPU, 32 GiB) \* 1; TiKV (16 vCPU, 64 GiB) \* 3
- TiDB (16 vCPU, 32 GiB) \* 2; TiKV (16 vCPU, 64 GiB) \* 3

Test results:

**TiDB (16 vCPU, 32 GiB) \* 1; TiKV (16 vCPU, 64 GiB) \* 3**

| Transaction model | Threads | QPS      | TPS     | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|----------|---------|----------------------|------------------|
| Read Only         | 125     | 37448.41 | 2340.53 | 53.40                | 89.16            |
| Read Write        | 100     | 28903.99 | 1445.20 | 69.19                | 104.84           |
| Write Only        | 400     | 40878.68 | 6813.11 | 58.71                | 101.13           |

**TiDB (16 vCPU, 32 GiB) \* 2; TiKV (16 vCPU, 64 GiB) \* 3**

| Transaction model | Threads | QPS      | TPS      | Average latency (ms) | P95 latency (ms) |
|-------------------|---------|----------|----------|----------------------|------------------|
| Read Only         | 300     | 77238.30 | 4827.39  | 62.14                | 102.97           |
| Read Write        | 200     | 58241.15 | 2912.06  | 68.67                | 97.55            |
| Write Only        | 700     | 68829.89 | 11471.65 | 61.01                | 101.13           |
