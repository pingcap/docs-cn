---
title: TiDB Sysbench Performance Test Report -- v2.0.0 vs. v1.0.0
category: benchmark
---

# TiDB Sysbench Performance Test Report -- v2.0.0 vs. v1.0.0

## Test purpose

This test aims to compare the performances of TiDB 1.0 and TiDB 2.0.

## Test version, time, and place

TiDB version: v1.0.8 vs. v2.0.0-rc6

Time: April 2018

Place: Beijing, China

## Test environment

IDC machine

| Type | Name |
| -------- | --------- |
| OS | linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD * 1 |

## Test plan

### TiDB version information

### v1.0.8

| Component | GitHash |
| -------- | --------- |
| TiDB | 571f0bbd28a0b8155a5ee831992c986b90d21ab7 |
| TiKV | 4ef5889947019e3cb55cc744f487aa63b42540e7 |
| PD | 776bcd940b71d295a2c7ed762582bc3aff7d3c0e |

### v2.0.0-rc6

| Component | GitHash |
| :--------: | :---------: |
| TiDB | 82d35f1b7f9047c478f4e1e82aa0002abc8107e7 |
| TiKV | 7ed4f6a91f92cad5cd5323aaebe7d9f04b77cc79 |
| PD | 2c8e7d7e33b38e457169ce5dfb2f461fced82d65 |

### TiKV parameter configuration

- v1.0.8

    ```
    sync-log = false
    grpc-concurrency = 8
    grpc-raft-conn-num = 24
    ```

- v2.0.0-rc6

    ```
    sync-log = false
    grpc-concurrency = 8
    grpc-raft-conn-num = 24
    use-delete-range: false
    ```

### Cluster topology

| Machine IP | Deployment instance |
|--------------|------------|
| 172.16.21.1 | 1*tidb 1*pd 1*sysbench |
| 172.16.21.2 | 1*tidb 1*pd 1*sysbench |
| 172.16.21.3 | 1*tidb 1*pd 1*sysbench |
| 172.16.11.4 | 1*tikv |
| 172.16.11.5 | 1*tikv |
| 172.16.11.6 | 1*tikv |
| 172.16.11.7 | 1*tikv |
| 172.16.11.8 | 1*tikv |
| 172.16.11.9 | 1*tikv |

## Test result

### Standard `Select` test

| Version | Table count | Table size | Sysbench threads |QPS | Latency (avg/.95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| v2.0.0-rc6 | 32 | 10 million | 128 * 3 |  201936 | 1.9033 ms/5.67667 ms |
| v2.0.0-rc6 | 32 | 10 million | 256 * 3 | 208130 | 3.69333 ms/8.90333 ms  |
| v2.0.0-rc6 | 32 | 10 million | 512 * 3 |  211788 | 7.23333 ms/15.59 ms |
| v2.0.0-rc6 | 32 | 10 million | 1024 * 3 |  212868 | 14.5933 ms/43.2133 ms |
| v1.0.8  | 32 | 10 million | 128 * 3 |  188686 | 2.03667 ms/5.99 ms  |
| v1.0.8  | 32 | 10 million | 256 * 3 |  195090  |3.94 ms/9.12 ms  |
| v1.0.8  | 32 | 10 million | 512 * 3 |  203012 | 7.57333 ms/15.3733 ms  |
| v1.0.8  | 32 | 10 million | 1024 * 3 |  205932 | 14.9267 ms/40.7633 ms |

According to the statistics above, the `Select` query performance of TiDB 2.0 GA has increased by about 10% at most than that of TiDB 1.0 GA.

### Standard OLTP test

| Version | Table count | Table size | Sysbench threads | TPS | QPS | Latency (avg/.95) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---:|
| v2.0.0-rc6 | 32 | 10 million | 128 * 3 | 5404.22 | 108084.4 | 87.2033 ms/110 ms |
| v2.0.0-rc6 | 32 | 10 million | 256 * 3 | 5578.165 | 111563.3 | 167.673 ms/275.623 ms |
| v2.0.0-rc6 | 32 | 10 million | 512 * 3 | 5874.045 | 117480.9 | 315.083 ms/674.017 ms |
| v2.0.0-rc6 | 32 | 10 million | 1024 * 3 | 6290.7 | 125814 | 529.183 ms/857.007 ms |
| v1.0.8 | 32 | 10 million | 128 * 3 | 5523.91 | 110478 | 69.53 ms/88.6333 ms |
| v1.0.8 | 32 | 10 million | 256 * 3 | 5969.43 | 119389 |128.63 ms/162.58 ms |
| v1.0.8 | 32 | 10 million | 512 * 3 | 6308.93 | 126179 | 243.543 ms/310.913 ms |
| v1.0.8 | 32 | 10 million | 1024 * 3 | 6444.25 | 128885 | 476.787ms/635.143 ms |

According to the statistics above, the OLTP performance of TiDB 2.0 GA and TiDB 1.0 GA is almost the same.

### Standard `Insert` test

| Version | Table count | Table size | Sysbench threads | QPS | Latency (avg/.95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| v2.0.0-rc6 | 32 | 10 million | 128 * 3 | 31707.5 | 12.11 ms/21.1167 ms |
| v2.0.0-rc6 | 32 | 10 million | 256 * 3 | 38741.2 | 19.8233 ms/39.65 ms |
| v2.0.0-rc6 | 32 | 10 million | 512 * 3 | 45136.8 | 34.0267 ms/66.84 ms |
| v2.0.0-rc6 | 32 | 10 million | 1024 * 3 | 48667 | 63.1167 ms/121.08 ms |
| v1.0.8 | 32 | 10 million | 128 * 3 | 31125.7 | 12.3367 ms/19.89 ms |
| v1.0.8 | 32 | 10 million | 256 * 3 | 36800 | 20.8667 ms/35.3767 ms |
| v1.0.8 | 32 | 10 million | 512 * 3 | 44123 | 34.8067 ms/63.32 ms |
| v1.0.8 | 32 | 10 million | 1024 * 3 | 48496 | 63.3333 ms/118.92 ms |

According to the statistics above, the `Insert` query performance of TiDB 2.0 GA has increased slightly than that of TiDB 1.0 GA.
