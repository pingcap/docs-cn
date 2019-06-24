---
title: Performance test result for TiDB using Sysbench
category: benchmark
draft: true
---

# Performance test result for TiDB using Sysbench

## Test purpose

The purpose of this test is to test the performance and horizontal scalability of TiDB in OLTP scenarios.

> **Note:**
>
> The results of the testing might vary based on different environmental dependencies.

## Test version, date and place

TiDB version: v1.0.0

Date: October 20, 2017

Place: Beijing

## Test environment

- IDC machines:

  | Category  |  Detail       |
  | :--------| :---------|
  | OS       | Linux (CentOS 7.3.1611)       |
  | CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
  | RAM | 128GB |
  | DISK | 1.5T SSD * 2  + Optane SSD * 1 |

- Sysbench version: 1.0.6

- Test script: https://github.com/pingcap/tidb-bench/tree/cwen/not_prepared_statement/sysbench.   

## Test scenarios

### Scenario one: RW performance test using Sysbench

The structure of the table used for the test:

``` sql
CREATE TABLE `sbtest` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `k` int(10) unsigned NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB  
``` 

The deployment and configuration details:

```
// TiDB deployment
172.16.20.4    4*tikv    1*tidb    1*sysbench
172.16.20.6    4*tikv    1*tidb    1*sysbench
172.16.20.7    4*tikv    1*tidb    1*sysbench
172.16.10.8    1*tidb    1*pd      1*sysbench

// Each physical node has three disks.
data3: 2 tikv (Optane SSD) 
data2: 1 tikv
data1: 1 tikv

// TiKV configuration
sync-log = false
grpc-concurrency = 8
grpc-raft-conn-num = 24 
[defaultcf]
block-cache-size = "12GB"
[writecf]
block-cache-size = "5GB"
[raftdb.defaultcf]
block-cache-size = "2GB"

// MySQL deployment
// Use the semi-synchronous replication and asynchronous replication to deploy two replicas respectively.
172.16.20.4    master    
172.16.20.6    slave        
172.16.20.7    slave
172.16.10.8    1*sysbench 
Mysql version: 5.6.37

// MySQL configuration
thread_cache_size = 64
innodb_buffer_pool_size = 64G
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 0  
datadir = /data3/mysql  
max_connections = 2000 
```

- OLTP RW test
    
    | - | Table count | Table size | Sysbench threads | TPS | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
    | TiDB | 32 | 1 million | 64 * 4 | 3834 | 76692 | 67.04 ms / 110.88 ms |
    | TiDB | 32 | 1 million | 128 * 4 | 4172 | 83459 | 124.00 ms / 194.21 ms  |
    | TiDB | 32 | 1 million | 256 * 4 | 4577 | 91547 | 228.36 ms / 334.02 ms |
    | TiDB | 32 | 5 million | 256 * 4 | 4032 | 80657 | 256.62 ms / 443.88 ms |
    | TiDB | 32 | 10 million | 256 * 4 | 3811 | 76233 | 269.46 ms / 505.20 ms |
    | Mysql | 32 | 1 million | 64 | 2392 | 47845 | 26.75 ms / 73.13 ms |
    | Mysql | 32 | 1 million | 128 | 2493 | 49874 | 51.32 ms / 173.58 ms  |
    | Mysql | 32 | 1 million | 256 | 2561 | 51221 | 99.95 ms  / 287.38 ms |
    | Mysql | 32 | 5 million | 256 | 1902 | 38045 | 134.56 ms / 363.18 ms |
    | Mysql | 32 | 10 million | 256 | 1770 | 35416 | 144.55 ms / 383.33 ms  |

![](/media/sysbench-01.png)

![](/media/sysbench-02.png)

- `Select` RW test

    | - | Table count | Table size | Sysbench threads | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: |
    | TiDB | 32 | 1 million | 64 * 4 |  160299 | 1.61ms / 50.06 ms |
    | TiDB | 32 | 1 million | 128 * 4 | 183347 | 2.85 ms / 8.66 ms  |
    | TiDB | 32 | 1 million | 256 * 4 |  196515 | 5.42 ms / 14.43 ms |
    | TiDB | 32 | 5 million | 256 * 4 |  187628 | 5.66 ms / 15.04 ms |
    | TiDB | 32 | 10 million | 256 * 4 |  187440 | 5.65 ms / 15.37 ms  |
    | Mysql | 32 | 1 million | 64 |  359572 | 0.18 ms /  0.45 ms  |
    | Mysql | 32 | 1 million | 128 |  410426  |0.31 ms / 0.74 ms  |
    | Mysql | 32 | 1 million | 256 |  396867 | 0.64 ms / 1.58 ms  |
    | Mysql | 32 | 5 million | 256 |  386866 | 0.66 ms / 1.64 ms |
    | Mysql | 32 | 10 million | 256 |  388273 | 0.66 ms / 1.64 ms  |

![](/media/sysbench-03.png)

![](/media/sysbench-04.png)

- `Insert` RW test

    | - | Table count | Table size | Sysbench threads | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: |
    | TiDB | 32 | 1 million | 64 * 4 | 25308 | 10.12 ms / 25.40 ms |
    | TiDB | 32 | 1 million | 128 * 4 | 28773 | 17.80 ms / 44.58 ms   |
    | TiDB | 32 | 1 million | 256 * 4 | 32641 | 31.38 ms / 73.47 ms |
    | TiDB | 32 | 5 million | 256 * 4 | 30430 | 33.65 ms / 79.32 ms |
    | TiDB | 32 | 10 million | 256 * 4 | 28925 | 35.41 ms / 78.96 ms |
    | Mysql | 32 | 1 million | 64 | 14806 | 4.32 ms / 9.39 ms |
    | Mysql | 32 | 1 million | 128 | 14884 | 8.58  ms / 21.11 ms |
    | Mysql | 32 | 1 million | 256 | 14508 | 17.64 ms / 44.98 ms  |
    | Mysql | 32 | 5 million | 256 | 10593 | 24.16 ms / 82.96 ms  |
    | Mysql | 32 | 10 million | 256 | 9813 | 26.08 ms / 94.10 ms  |  
 
![](/media/sysbench-05.png)

![](/media/sysbench-06.png)   

### Scenario two: TiDB horizontal scalability test

The deployment and configuration details:

```
// TiDB deployment 
172.16.20.3    4*tikv    
172.16.10.2    1*tidb    1*pd     1*sysbench

// Each physical node has three disks. 
data3: 2 tikv (Optane SSD) 
data2: 1 tikv 
data1: 1 tikv 

// TiKV configuration 
sync-log = false
grpc-concurrency = 8
grpc-raft-conn-num = 24 
[defaultcf]
block-cache-size = "12GB"
[writecf]
block-cache-size = "5GB"
[raftdb.defaultcf]
block-cache-size = "2GB"
``` 

- OLTP RW test

    | - | Table count | Table size | Sysbench threads | TPS | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
    | 1 TiDB physical node | 32 | 1 million | 256 * 1 | 2495 | 49902 | 102.42 ms / 125.52 ms |
    | 2 TiDB physical nodes | 32 | 1 million | 256 * 2 | 5007 | 100153 | 102.23 ms / 125.52 ms  |
    | 4 TiDB physical nodes | 32 | 1 million | 256 * 4 | 8984 | 179692 | 114.96 ms / 176.73 ms |
    | 6 TiDB physical nodes | 32 | 5 million | 256 * 6 | 12953 | 259072 | 117.80 ms / 200.47 ms  |

![](/media/sysbench-07.png)

- `Select` RW test

    | - | Table count | Table size | Sysbench threads | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: |
    | 1 TiDB physical node | 32 | 1 million | 256 * 1 | 71841 | 3.56 ms / 8.74 ms |
    | 2 TiDB physical nodes | 32 | 1 million | 256 * 2 | 146615 | 3.49 ms / 8.74 ms |
    | 4 TiDB physical nodes | 32 | 1 million | 256 * 4 | 289933 | 3.53 ms / 8.74 ms  |
    | 6 TiDB physical nodes | 32 | 5 million | 256 * 6 | 435313 | 3.55 ms / 9.17 ms  |

![](/media/sysbench-08.png)

- `Insert` RW test

    | - | Table count | Table size | Sysbench threads | QPS | Latency(avg / .95) |
    | :---: | :---: | :---: | :---: | :---: | :---: |
    | 3 TiKV physical node | 32 | 1 million |256 * 3 | 40547 | 18.93 ms / 38.25 ms |
    | 5 TiKV physical nodes | 32 | 1 million | 256 * 3 | 60689 | 37.96 ms / 29.9 ms |
    | 7 TiKV physical nodes | 32 | 1 million | 256 * 3 | 80087 | 9.62 ms / 21.37 ms |

![](/media/sysbench-09.png)
