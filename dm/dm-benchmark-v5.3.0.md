---
title: DM 5.3.0 Benchmark Report
summary: Learn about the performance of 5.3.0.
---

# DM 5.3.0 Benchmark Report

This benchmark report describes the test purpose, environment, scenario, and results for DM 5.3.0.

## Test purpose

The purpose of this test is to evaluate the performance of DM full import and incremental replication and to conclude recommended configurations for DM migration tasks based on the test results.

## Test environment

### Machine information

System information:

| Machine IP  | Operating System           | Kernel version           | File system type |
| :---------: | :---------------------------: | :-------------------: | :--------------: |
| 172.16.6.1 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.6.2 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |
| 172.16.6.3 | CentOS Linux release 7.8.2003 | 3.10.0-957.el7.x86_64 | ext4             |

Hardware information:

| Type         | Specification                                       |
| :----------: | :-------------------------------------------------: |
| CPU          | Intel(R) Xeon(R) Silver 4214R @ 2.40GHz, 48 Cores |
| Memory       | 192G, 12 * 16GB DIMM DDR4 2133 MHz                   |
| Disk         | Intel SSDPE2KX040T8 4TB                             |
| Network card | 10 Gigabit Ethernet                                 |

Others:

* Network rtt between servers: rtt min/avg/max/mdev = 0.045/0.064/0.144/0.024 ms

### Cluster topology

| Machine IP  | Deployed instance                |
| :---------: | :--------------------------------: |
| 172.16.6.1 | PD1, TiDB1, TiKV1, MySQL1, DM-master1 |
| 172.16.6.2 | PD2, TiDB2, TiKV2, DM-worker1 |
| 172.16.6.3 | PD3, TiDB3, TiKV3 |

### Version information

- MySQL version: 5.7.36-log
- TiDB version: v5.2.1
- DM version: v5.3.0
- Sysbench version: 1.1.0

## Test scenario

You can use a simple data migration flow, that is, MySQL1 (172.16.6.1) -> DM-worker(172.16.6.2) -> TiDB(load balance) (172.16.6.4), to do the test. For detailed test scenario description, see [performance test](/dm/dm-performance-test.md).

### Full import benchmark case

For detailed full import test method, see [Full Import Benchmark Case](/dm/dm-performance-test.md#full-import-benchmark-case).

#### Full import benchmark results

To enable multi-thread concurrent data export via Dumpling, you can configure the `threads` parameter in the `mydumpers` configuration item. This speeds up data export.

| Item       | Data size (GB)  | Threads  | Rows    | Statement-size  | Time (s)  | Dump speed (MB/s)   |
| :----------: | :---------: |:-------: | :-----: | :-------------: | :----------: | :---------------: |
| dump data    | 38.1       | 32       | 320000   | 1000000         | 45       | 846           |

| Item    | Data size (GB)  | Pool size | Statement per TXN | Max latency of TXN execution (s) | Time (s) | Import speed (MB/s) |
| :-------: | :--------: | :-------: | :-------------------: | :----------------: | :----------: | :-------------: |
| load data | 38.1       | 32        | 4878                  | 76              | 2740       | 13.9          |

#### Benchmark results with different pool sizes in load unit

In this test, the full amount of data imported using `sysbench` is 3.78 GB. The following is detailed information of the test data:

| load unit pool size| Max latency of TXN execution (s) | Import time (s) | Import Speed (MB/s) | TiDB 99 duration (s) |
| :---------------------: | :---------------: | :----------: | :-------------: | :------------------: |
| 2                       | 0.71              | 397         | 9.5             | 0.61                 |
| 4                       | 1.21              | 363         | 10.4            | 1.03                 |
| 8                       | 3.30              | 279         | 13.5            | 2.11                 |
| 16                      | 5.56              | 200         | 18.9            | 3.04                 |
| 32                      | 6.92              | 218         | 17.3            | 6.56                 |
| 64                      | 8.59              | 231         | 16.3            | 8.62                 |

#### Benchmark results with different row count per statement

In this test, the full amount of imported data is 3.78 GB and the `pool-size` of load unit is set to 32. The statement count is controlled by `statement-size`, `rows`, or `extra-args` parameters in the `mydumpers` configuration item.

| Row count per statement       | mydumpers extra-args | Max latency of TXN execution (s) | Import time (s) | Import speed (MB/s) | TiDB 99 duration (s) |
| :------------------------: | :-----------------------: | :--------------: | :----------: | :-------------: | :------------------: |
|            7506            | -s 1500000 -r 320000      |   8.34           |  229         |     16.5        |        10.64         |
|            5006            | -s 1000000 -r 320000      |   6.12           |  218         |     17.3        |         7.23         |
|            2506            | -s 500000 -r 320000       |   4.27           |  232         |     16.2        |         3.24         |
|            1256            | -s 250000 -r 320000       |   2.25           |  235         |     16.0        |         1.92         |
|            629             | -s 125000 -r 320000       |   1.03           |  246         |     15.3        |         0.91         |
|            315             | -s 62500 -r 320000        |   0.63           |  249         |     15.1        |         0.44         |

### Incremental replication benchmark case

For detailed incremental replication test method, see [Incremental Replication Benchmark Case](/dm/dm-performance-test.md#incremental-replication-benchmark-case).

#### Incremental replication benchmark result

In this test, the `worker-count` of sync unit is set to 32 and `batch` is set to 100.

| Items                       | QPS                | TPS                          | 95% latency                     |
| :------------------------: | :----------------------------------------------------------: | :-------------------------------------------------------------: | :--------------------------: |
| MySQL                      | 40.65k                                                       | 40.65k                                                          | 1.10ms                       |
| DM binlog replication unit | 29.1k (The number of binlog events received per unit of time, not including skipped events)              | -                                                               | 92ms (txn execution time)          |
| TiDB                       | 32.0k (Begin/Commit 1.5 Insert 29.72k)                    | 3.52k                                                           | 95%: 6.2ms 99%: 8.3ms          |

#### Benchmark results with different sync unit concurrency

| sync unit worker-count | DM QPS           | Max DM execution latency (ms)   | TiDB QPS | TiDB 99 duration (ms) |
| :---------------------------: | :-------------: | :-----------------------: | :------: | :-------------------: |
| 4                             | 10.2           | 40                       | 10.5k    | 4                     |
| 8                             | 17.6k           | 64                       | 18.9k    | 5                     |
| 16                            | 29.5k           | 80                       | 30.5k    | 7                     |
| 32                            | 29.1k           | 92                       | 32.0k    | 9                     |
| 64                            | 27.4k           | 88                       | 37.7k    | 14                    |
| 1024                          | 22.9k           | 85                       | 57.5k    | 25                    |

#### Benchmark results with different SQL distribution

| Sysbench type| DM QPS | Max DM execution latency (ms) | TiDB QPS | TiDB 99 duration (ms) |
| :--------------: | :-------------: | :------------------: | :------: | :-------------------: |
| insert_only      | 29.1k          | 64                   | 32.0k    | 8                    |
| write_only       | 23.5k           | 296                  | 24.2k     | 18                    |

## Recommended parameter configuration

### dump unit

We recommend that the statement size be 200 KB~1 MB, and row count in each statement be approximately 1000~5000, which is based on the actual row size in your scenario.

### load unit

We recommend that you set `pool-size` to 16~32.

### sync unit

We recommend that you set `batch` to 100 and `worker-count` to 16~32.
