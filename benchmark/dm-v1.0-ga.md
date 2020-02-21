---
title: DM 1.0-GA Benchmark Report
summary: Learn about the DM benchmark report.
category: benchmark
---

# DM 1.0-GA Benchmark Report

This benchmark report describes the test purpose, environment, scenario, and result for DM 1.0-GA.

## Test purpose

The purpose of this test is to test the performance of DM full import and incremental replication.

## Test environment

### Machine information

System information:

| Machine IP  | Operation system              | Kernel version            | File system type |
| :---------: | :---------------------------: | :-----------------------: | :--------------: |
| 172.16.4.39 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |
| 172.16.4.40 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |
| 172.16.4.41 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |
| 172.16.4.42 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |
| 172.16.4.43 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |
| 172.16.4.44 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86_64 | ext4             |

Hardware information:

| Type         | Specification                                      |
| :----------: | :------------------------------------------------: |
| CPU          | 40 CPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| Memory       | 192GB, 12 * 16GB DIMM DDR4 2133 MHz                |
| Disk         | Intel DC P4510 4TB NVMe PCIe 3.0                   |
| Network card | 10 Gigabit Ethernet                                |

Others:

* Network rtt between servers: rtt min/avg/max/mdev = 0.074/0.088/0.121/0.019 ms

### Cluster topology

| Machine IP  | Deployment instance                |
| :---------: | :--------------------------------: |
| 172.16.4.39 | PD1, DM-worker1, DM-master         |
| 172.16.4.40 | PD2, MySQL1                        |
| 172.16.4.41 | PD3, TiDB                          |
| 172.16.4.42 | TiKV1                              |
| 172.16.4.43 | TiKV2                              |
| 172.16.4.44 | TiKV3                              |

### Version information

- MySQL version: 5.7.27-log
- TiDB version: v4.0.0-alpha-198-gbde7f440e
- DM version: v1.0.1
- Sysbench version: 1.0.17

## Test scenario

### Data flow

MySQL1 (172.16.4.40) -> DM-worker1 (172.16.4.39) -> TiDB (172.16.4.41)

### Public configuration or data

#### Database table structure used for the test

{{< copyable "sql" >}}

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` char(60) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

#### Database configuration

We use TiDB Ansible to deploy the TiDB cluster, and use default configuration provided in TiDB Ansible.

### Full import benchmark case

#### Test procedure

- Set up environment
- Use sysbench to create the table and generate the initial data in upstream MySQL
- Start DM-task in the `full` mode

Sysbench test script used for preparing initial data:

{{< copyable "shell-regular" >}}

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### Full import benchmark result

| item                            | dump thread | mydumper extra-args             | dump speed (MB/s) |
| :-----------------------------: | :---------: | :-----------------------------: | :---------------: |
| enable single table concurrent  | 32          | "-r 320000 --regex '^sbtest.*'" | 191.03            |
| disable single table concurrent | 32          | "--regex '^sbtest.*'"           | 72.22             |

| item      | latency of execute transaction (s) | statement per transaction | data size (GB) | time (s) | import speed (MB/s) |
| :-------: | :--------------------------------: | :-----------------------: | :------------: | :------: | :-----------------: |
| load data | 1.737                              | 4878                      | 38.14          | 2346.9   | 16.64               |

#### Benchmark result with different pool size in load unit

Full import data size in benchmark case is 3.78 GB, which is generated from sysbench by the following script:

{{< copyable "shell-regular" >}}

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=5000000 prepare
```

| load pool size | latency of execution txn (s) | import time (s) | import speed (MB/s) | TiDB 99 duration (s) |
| :------------: | :--------------------------: | :-------------: | :-----------------: | :------------------: |
| 2              | 0.250                        | 425.9           | 9.1                 | 0.23                 |
| 4              | 0.523                        | 360.1           | 10.7                | 0.41                 |
| 8              | 0.986                        | 267.0           | 14.5                | 0.93                 |
| 16             | 2.022                        | 265.9           | 14.5                | 2.68                 |
| 32             | 3.778                        | 262.3           | 14.7                | 6.39                 |
| 64             | 7.452                        | 281.9           | 13.7                | 8.00                 |

#### Benchmark result with different row count in per statement

Full import data size in this benchmark case is 3.78 GB, load unit pool size uses 32. The statement count is controlled by mydumper parameters.

| row count in per statement | mydumper extra-args  | latency of execution txn (s) | import time (s) | import speed (MB/s) | TiDB 99 duration (s) |
| :------------------------: | :------------------: | :--------------------------: | :-------------: | :-----------------: | :------------------: |
|            7426            | -s 1500000 -r 320000 |            6.982             |  258.3          |     15.0            |        10.34         |
|            4903            | -s 1000000 -r 320000 |            3.778             |  262.3          |     14.7            |         6.39         |
|            2470            | -s 500000 -r 320000  |            1.962             |  271.36         |     14.3            |         2.00         |
|            1236            | -s 250000 -r 320000  |            1.911             |  283.3          |     13.7            |         1.50         |
|            618             | -s 125000 -r 320000  |            0.683             |  299.9          |     12.9            |         0.73         |
|            310             |  -s 62500 -r 320000  |            0.413             |  322.6          |     12.0            |         0.49         |

### Increase replication benchmark case

#### Test procedure

- Set up environment
- Use sysbench to create the table and generate the initial data in upstream MySQL
- Start DM-task in the `all` mode, and wait until the task enters `sync` unit
- Use sysbench to generate incremental data in upstream MySQL, use `query-status` to watch the DM replication status, and observe the monitoring metrics of DM and TiDB on Grafana

#### Benchmark result for incremental replication

Upstream sysbench test script:

{{< copyable "shell-regular" >}}

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

DM sync unit `worker-count` is 32, and `batch` size is 100 in this benchmark case.

| items                      | qps                                                            | tps                                                          | 95% Latency                  |
| :------------------------: | :------------------------------------------------------------: | :----------------------------------------------------------: | :--------------------------: |
| MySQL                      | 42.79k                                                         | 42.79k                                                       | 1.18ms                       |
| DM relay log unit          | -                                                              | 11.3MB/s                                                     | 45us (read duration)         |
| DM binlog replication unit | 22.97k (binlog event received qps, not including skipped events) | -                                                            | 20ms (txn execution latency) |
| TiDB                       | 31.30k (Begin/Commit 3.93k Insert 22.76k)                      | 4.16k                                                        | 95%: 6.4ms 99%: 9ms          |

#### Benchmark result with different sync unit concurrency

| sync unit worker-count | DM tps | DM execution latency (ms) | TiDB qps | TiDB 99 duration (ms) |
| :--------------------: | :----: | :-----------------------: | :------: | :-------------------: |
| 4                      | 7074   | 63                        | 7.1k     | 3                     |
| 8                      | 14684  | 64                        | 14.9k    | 4                     |
| 16                     | 23486  | 56                        | 24.9k    | 6                     |
| 32                     | 23345  | 28                        | 29.2k    | 10                    |
| 64                     | 23302  | 30                        | 31.2k    | 16                    |
| 1024                   | 22225  | 70                        | 56.9k    | 70                    |

#### Benchmark result with different SQL distribution

| sysbench type | relay log flush speed (MB/s) | DM tps | DM execution latency (ms) | TiDB qps | TiDB 99 duration (ms) |
| :-----------: | :--------------------------: | :----: | :-----------------------: | :------: | :-------------------: |
| insert_only   | 11.3                         | 23345  | 28                        | 29.2k    | 10                    |
| write_only    | 18.7                         | 33470  | 129                       | 34.6k    | 11                    |

## Recommended parameters

### dump unit

We recommend that the statement size be 200 KB~1 MB, and row count in each statement be approximately 1000~5000, which is based on the actual row size in your scenario.

### load unit

We recommend that you set `pool-size` to 16.

### sync unit

We recommend that you set `batch` size to 100 and `worker-count` to 16~32.
