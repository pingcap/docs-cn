---
title: TiDB Sysbench Performance Test Report -- v2.1 vs. v2.0
category: benchmark
aliases: ['/docs/benchmark/sysbench-v3/']
---

# TiDB Sysbench Performance Test Report -- v2.1 vs. v2.0

## Test purpose

This test aims to compare the performance of TiDB 2.1 and TiDB 2.0 for OLTP where the working set fits in memory.

## Test version, time, and place

TiDB version: v2.1.0-rc.2 vs. v2.0.6

Time: September, 2018

Place: Beijing, China

## Test environment

IDC machine:

| Type | Name |
| :-: | :-: |
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD \* 1 |

Sysbench version: 1.1.0

## Test plan

Use Sysbench to import **16 tables, with 10,000,000 pieces of data in each table**. With the HAProxy, requests are sent to the cluster at an incremental concurrent number. A single concurrent test lasts 5 minutes.

### TiDB version information

### v2.1.0-rc.2

| Component | GitHash |
| :-: | :-: |
| TiDB | 08e56cd3bae166b2af3c2f52354fbc9818717f62 |
| TiKV | 57e684016dafb17dc8a6837d30224be66cbc7246 |
| PD | 6a7832d2d6e5b2923c79683183e63d030f954563 |

### v2.0.6

| Component | GitHash |
| :-: | :-: |
| TiDB | b13bc08462a584a085f377625a7bab0cc0351570 |
| TiKV | 57c83dc4ebc93d38d77dc8f7d66db224760766cc |
| PD | b64716707b7279a4ae822be767085ff17b5f3fea |

### TiDB parameter configuration

The default TiDB configuration is used in both v2.1 and v2.0.

### TiKV parameter configuration

The following TiKV configuration is used in both v2.1 and v2.0:

```txt
[readpool.storage]
normal-concurrency = 8
[server]
grpc-concurrency = 8
[raftstore]
sync-log = false
[rocksdb.defaultcf]
block-cache-size = "60GB"
[rocksdb.writecf]
block-cache-size = "20GB"
```

### Cluster topology

| Machine IP | Deployment instance |
| :-: | :-: |
| 172.16.30.31 | 1\*Sysbench 1\*HAProxy |
| 172.16.30.32 | 1\*TiDB 1\*pd 1\*TiKV |
| 172.16.30.33 | 1\*TiDB 1\*TiKV |
| 172.16.30.34 | 1\*TiDB 1\*TiKV |

## Test result

### `Point Select` test

| Version | Threads | QPS | 95% Latency (ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 111481.09 | 1.16  |
| v2.1 | 128  | 145102.62 | 2.52  |
| v2.1 | 256  | 161311.9  | 4.57  |
| v2.1 | 512  | 184991.19 | 7.56  |
| v2.1 | 1024 | 230282.74 | 10.84 |
| v2.0 | 64   | 75285.87  | 1.93  |
| v2.0 | 128  | 92141.79  | 3.68  |
| v2.0 | 256  | 107464.93 | 6.67  |
| v2.0 | 512  | 121350.61 | 11.65 |
| v2.0 | 1024 | 150036.31 | 17.32 |

![point select](/media/sysbench_v3_point_select.png)

According to the statistics above, the `Point Select` query performance of TiDB 2.1 has increased by **50%** than that of TiDB 2.0.

### `Update Non-Index` test

| Version | Threads | QPS | 95% Latency (ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 18946.09 | 5.77   |
| v2.1 | 128  | 22022.82 | 12.08  |
| v2.1 | 256  | 24679.68 | 25.74  |
| v2.1 | 512  | 25107.1  | 51.94  |
| v2.1 | 1024 | 27144.92 | 106.75 |
| v2.0 | 64   | 16316.85 | 6.91   |
| v2.0 | 128  | 20944.6  | 11.45  |
| v2.0 | 256  | 24017.42 | 23.1   |
| v2.0 | 512  | 25994.33 | 46.63  |
| v2.0 | 1024 | 27917.52 | 92.42  |

![update non-index](/media/sysbench_v3_update_non_index.png)

According to the statistics above, the `Update Non-Index` write performance of TiDB 2.1 and TiDB 2.0 is almost the same.

### `Update Index` test

| Version | Threads | QPS | 95% Latency (ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 9934.49  | 12.08  |
| v2.1 | 128  | 10505.95 | 25.28  |
| v2.1 | 256  | 11007.7  | 55.82  |
| v2.1 | 512  | 11198.81 | 106.75 |
| v2.1 | 1024 | 11591.89 | 200.47 |
| v2.0 | 64   | 9754.68  | 11.65  |
| v2.0 | 128  | 10603.31 | 24.38  |
| v2.0 | 256  | 11011.71 | 50.11  |
| v2.0 | 512  | 11162.63 | 104.84 |
| v2.0 | 1024 | 12067.63 | 179.94 |

![update index](/media/sysbench_v3_update_index.png)

According to the statistics above, the `Update Index` write performance of TiDB 2.1 and TiDB 2.0 is almost the same.
