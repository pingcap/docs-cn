---
title: TiDB Sysbench 性能测试报告 - v1.0.0
category: benchmark
draft: true
aliases: ['/docs-cn/benchmark/sysbench/']
---

# TiDB Sysbench 性能测试报告 - v1.0.0

## 测试目的

测试 TiDB 在 OLTP 场景下的性能以及水平扩展能力。

> **注意：**
>
> 不同的测试环境可能使测试结果发生改变。

## 测试版本、时间、地点

TiDB 版本：v1.0.0
时间：2017 年 10 月 20 日
地点：北京

## 测试环境

IDC 机器

| 类别       |  名称       |
| :--------: | :---------: |
| OS       | linux (CentOS 7.3.1611)       |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | 1.5T SSD \* 2  + Optane SSD \* 1 |

Sysbench 版本: 1.0.6

测试脚本: <https://github.com/pingcap/tidb-bench/tree/cwen/not_prepared_statement/sysbench>

## 测试方案

### 场景一：sysbench 标准性能测试

测试表结构

```
CREATE TABLE `sbtest` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `k` int(10) unsigned NOT NULL DEFAULT '0',
  `c` char(120) NOT NULL DEFAULT '',
  `pad` char(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB
```

部署方案以及配置参数

```
// TiDB 部署方案
172.16.20.4    4*tikv    1*tidb    1*sysbench
172.16.20.6    4*tikv    1*tidb    1*sysbench
172.16.20.7    4*tikv    1*tidb    1*sysbench
172.16.10.8    1*tidb    1*pd      1*sysbench

// 每个物理节点有三块盘：
data3: 2 tikv  (Optane SSD)
data2: 1 tikv
data1: 1 tikv

// TiKV 参数配置
sync-log = false
grpc-concurrency = 8
grpc-raft-conn-num = 24
[defaultcf]
block-cache-size = "12GB"
[writecf]
block-cache-size = "5GB"
[raftdb.defaultcf]
block-cache-size = "2GB"

// Mysql 部署方案
// 分别使用半同步复制和异步复制，部署两副本
172.16.20.4    master
172.16.20.6    slave
172.16.20.7    slave
172.16.10.8    1*sysbench
Mysql version: 5.6.37

// Mysql 参数配置
thread_cache_size = 64
innodb_buffer_pool_size = 64G
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 0
datadir = /data3/mysql
max_connections = 2000
```

* 标准 oltp 测试

| - | table count | table size | sysbench threads | tps | qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TiDB | 32 | 100 万 | 64 * 4 | 3834 | 76692 | 67.04 ms / 110.88 ms |
| TiDB | 32 | 100 万 | 128 * 4 | 4172 | 83459 | 124.00 ms / 194.21 ms  |
| TiDB | 32 | 100 万 | 256 * 4 | 4577 | 91547 | 228.36 ms / 334.02 ms |
| TiDB | 32 | 500 万 | 256 * 4 | 4032 | 80657 | 256.62 ms / 443.88 ms |
| TiDB | 32 | 1000 万 | 256 * 4 | 3811 | 76233 | 269.46 ms / 505.20 ms |
| Mysql | 32 | 100 万 | 64 | 2392 | 47845 | 26.75 ms / 73.13 ms |
| Mysql | 32 | 100 万 | 128 | 2493 | 49874 | 51.32 ms / 173.58 ms  |
| Mysql | 32 | 100 万 | 256 | 2561 | 51221 | 99.95 ms  / 287.38 ms |
| Mysql | 32 | 500 万 | 256 | 1902 | 38045 | 134.56 ms / 363.18 ms |
| Mysql | 32 | 1000 万 | 256 | 1770 | 35416 | 144.55 ms / 383.33 ms  |

![sysbench-01](/media/sysbench-01.png)

![sysbench-02](/media/sysbench-02.png)

* 标准 select 测试

| - | table count | table size | sysbench threads |qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| TiDB | 32 | 100 万 | 64 * 4 |  160299 | 1.61ms / 50.06 ms |
| TiDB | 32 | 100 万 | 128 * 4 | 183347 | 2.85 ms / 8.66 ms  |
| TiDB | 32 | 100 万 | 256 * 4 |  196515 | 5.42 ms / 14.43 ms |
| TiDB | 32 | 500 万 | 256 * 4 |  187628 | 5.66 ms / 15.04 ms |
| TiDB | 32 | 1000 万 | 256 * 4 |  187440 | 5.65 ms / 15.37 ms  |
| Mysql | 32 | 100 万 | 64 |  359572 | 0.18 ms /  0.45 ms  |
| Mysql | 32 | 100 万 | 128 |  410426  |0.31 ms / 0.74 ms  |
| Mysql | 32 | 100 万 | 256 |  396867 | 0.64 ms / 1.58 ms  |
| Mysql | 32 | 500 万 | 256 |  386866 | 0.66 ms / 1.64 ms |
| Mysql | 32 | 1000 万 | 256 |  388273 | 0.66 ms / 1.64 ms  |

![sysbench-03](/media/sysbench-03.png)

![sysbench-04](/media/sysbench-04.png)

* 标准 insert 测试

| - | table count | table size | sysbench threads | qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| TiDB | 32 | 100 万 | 64 * 4 | 25308 | 10.12 ms / 25.40 ms |
| TiDB | 32 | 100 万 | 128 * 4 | 28773 | 17.80 ms / 44.58 ms   |
| TiDB | 32 | 100 万 | 256 * 4 | 32641 | 31.38 ms / 73.47 ms |
| TiDB | 32 | 500 万 | 256 * 4 | 30430 | 33.65 ms / 79.32 ms |
| TiDB | 32 | 1000 万 | 256 * 4 | 28925 | 35.41 ms / 78.96 ms |
| Mysql | 32 | 100 万 | 64 | 14806 | 4.32 ms / 9.39 ms |
| Mysql | 32 | 100 万 | 128 | 14884 | 8.58  ms / 21.11 ms |
| Mysql | 32 | 100 万 | 256 | 14508 | 17.64 ms / 44.98 ms  |
| Mysql | 32 | 500 万 | 256 | 10593 | 24.16 ms / 82.96 ms  |
| Mysql | 32 | 1000 万 | 256 | 9813 | 26.08 ms / 94.10 ms  |

![sysbench-05](/media/sysbench-05.png)

![sysbench-06](/media/sysbench-06.png)

### 场景二：TiDB 水平扩展能力测试

部署方案以及配置参数

```
// TiDB 部署方案
172.16.20.3    4*tikv
172.16.10.2    1*tidb    1*pd     1*sysbench

每个物理节点有三块盘：
data3: 2 tikv  (Optane SSD)
data2: 1 tikv
data1: 1 tikv

// TiKV 参数配置
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

* 标准 oltp 测试

| - | table count | table size | sysbench threads | tps | qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 物理节点 TiDB | 32 | 100 万 | 256 * 1 | 2495 | 49902 | 102.42 ms / 125.52 ms |
| 2 物理节点 TiDB | 32 | 100 万 | 256 * 2 | 5007 | 100153 | 102.23 ms / 125.52 ms  |
| 4 物理节点 TiDB | 32 | 100 万 | 256 * 4 | 8984 | 179692 | 114.96 ms / 176.73 ms |
| 6 物理节点 TiDB | 32 | 500 万 | 256 * 6 | 12953 | 259072 | 117.80 ms / 200.47 ms  |

![sysbench-07](/media/sysbench-07.png)

* 标准 select 测试

| - | table count | table size | sysbench threads | qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 物理节点 TiDB | 32 | 100 万 | 256 * 1 | 71841 | 3.56 ms / 8.74 ms |
| 2 物理节点 TiDB | 32 | 100 万 | 256 * 2 | 146615 | 3.49 ms / 8.74 ms |
| 4 物理节点 TiDB | 32 | 100 万 | 256 * 4 | 289933 | 3.53 ms / 8.74 ms  |
| 6 物理节点 TiDB | 32 | 500 万 | 256 * 6 | 435313 | 3.55 ms / 9.17 ms  |

![sysbench-08](/media/sysbench-08.png)

* 标准 insert 测试

| - | table count | table size | sysbench threads | qps | latency(avg / .95) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 3 物理节点 TiKV | 32 | 100 万 |256 * 3 | 40547 | 18.93 ms / 38.25 ms |
| 5 物理节点 TiKV | 32 | 100 万 | 256 * 3 | 60689 | 37.96 ms / 29.9 ms |
| 7 物理节点 TiKV | 32 | 100 万 | 256 * 3 | 80087 | 9.62 ms / 21.37 ms |

![sysbench-09](/media/sysbench-09.png)
