---
title: DM Benchmark Report
summary: Learn about the DM benchmark report.
category: benchmark
aliases: ['/docs/benchmark/dm-v1-alpha/']
---

# DM Benchmark Report

This DM benchmark report describes the test purpose, environment, scenario, and result.

## Test purpose

The purpose of this test is to test the performance of DM incremental replication.

> **Note:**
>
> The results of the testing might vary based on different environmental dependencies.

## Test environment

### Machine information

System information:

| Machine IP   | Operation system              | Kernel version               | File system type |
|--------------|-------------------------------|------------------------------|------------------|
| 192.168.0.6  | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |
| 192.168.0.7  | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |
| 192.168.0.8  | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |
| 192.168.0.9  | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |
| 192.168.0.10 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |
| 192.168.0.11 | CentOS Linux release 7.6.1810 | 3.10.0-957.1.3.el7.x86\_64   | ext4             |

Hardware information:

| Type         | 192.168.0.9, 192.168.0.10, 192.168.0.11               |  192.168.0.6, 192.168.0.7, 192.168.0.8                |
|--------------|-------------------------------------------------------|-------------------------------------------------------|
| CPU          | 8 vCPUs, Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz | 4 vCPUs, Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz |
| Memory       | 16G                                                   | 8G                                                    |
| Disk         | 1T Aliyun ESSD                                        | 256G Aliyun ESSD                                      |
| Network card | 1 Gigabit Ethernet, 1000Mb/s                          | 1 Gigabit Ethernet, 1000Mb/s                          |

### Cluster topology

| Machine IP   | Deployment instance |
|--------------|------------|
| 192.168.0.9  | TiKV \* 1, TiDB \* 1  |
| 192.168.0.10 | TiKV \* 1  |
| 192.168.0.11 | TiKV \* 1  |
| 192.168.0.6  | PD \* 1, MySQL \* 1, DM-worker \* 1  |
| 192.168.0.8  | PD \* 1, MySQL \* 1, DM-worker \* 1  |
| 192.168.0.7  | PD \* 1, DM-master \* 1  |

### Version information

- MySQL version: 5.7.25-log

- TiDB version: v3.0.0-beta-27-g6398788

- DM version: v1.0.0-alpha-10-g4d01d79

- Sysbench version: 1.0.9

## Test scenario

### Data flow

MySQL1 (192.168.0.8) -> DM-worker1 (192.168.0.6) -> TiDB (192.168.0.9)

### Test procedure

- Set up environment
- Use sysbench to create the table and generate the initial data in upstream MySQL
- Start DM-task in the `all` mode
- Use sysbench to generate incremental data in upstream MySQL

### Use sysbench to generate data load in upstream MySQL

Upstream sysbench test script:

```
sysbench --test=oltp_insert --tables=2 --num-threads=1024 --mysql-host=192.168.0.8 --mysql-port=3306 --mysql-user=root --mysql-db=dm_poc --db-driver=mysql --report-interval=10 --time=900 run
```

The structure of the table used for the test:

``` sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` char(60) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### The deployment and configuration details

```
// TiKV configuration
sync-log = false
[defaultcf]
block-cache-size = "4GB"
[writecf]
block-cache-size = "4GB"
[raftdb.defaultcf]
block-cache-size = "4GB"

// DM task syncer unit configuration
syncer:
    worker-count: 256
    batch: 100
    max-retry: 20
```

## Test result

| items | threads | qps                                       | tps    | 95% Latency (ms)            |
| ----- | ------- | ----------------------------------------- | ------ | --------------------------- |
| MySQL | 1024    | 15.10k                                    | 15.10k | 121.08                      |
| DM    | 256     | 13.89k                                    | 13.89k | 210 (txn execution latency) |
| TiDB  | -       | 18.53k (Begin/Commit 2.4k Replace 13.80k) | 2.27k  | 29                          |

### Monitor screenshots

#### DM key indicator monitor

![](/media/dm-benchmark-01.png)

#### TiDB key indicator monitor

![](/media/dm-benchmark-02.png)
![](/media/dm-benchmark-03.png)
