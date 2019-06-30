---
title: TiDB Sysbench Performance Test Report -- v3.0 vs. v2.1
category: benchmark
---

# TiDB Sysbench Performance Test Report -- v3.0 vs. v2.1

## Test purpose

This test aims to compare the performance of TiDB 3.0 and TiDB 2.1 in the OLTP scenario.

## Test version, time, and place

TiDB version: v3.0.0 vs. v2.1.13

Time: June, 2019

Place: Beijing

## Test environment

This test runs on AWS EC2 and uses the CentOS-7.6.1810-Nitro (ami-028946f4cffc8b916) image. The components and types of instances are as follows:

| Component  |  Instance type  |
| :--- | :-------- |
|  PD   | r5d.xlarge |
| TiKV  | c5d.4xlarge |
| TiDB  | c5.4xlarge |

Sysbench version: 1.0.17

## Test plan

Use Sysbench to import **16 tables, with 10,000,000 pieces of data in each table**. Start three sysbench to add pressure to three TiDB instances. The number of concurrent requests increases incrementally. A single concurrent test lasts 5 minutes.

Prepare data using the following command:

```sh
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    prepare --tables=16 --table-size=10000000
```

Then test TiDB using the following command:

```sh
sysbench $testname \
    --threads=$threads \
    --time=300 \
    --report-interval=15 \
    --rand-type=uniform \
    --rand-seed=$RANDOM \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    run --tables=16 --table-size=10000000
```

### TiDB version information

### v3.0.0

| Component  |                 GitHash                |
| :--- | :-------------------------------------- |
| TiDB  | `8efbe62313e2c1c42fd76d35c6f020087eef22c2` |
| TiKV  | `a467f410d235fa9c5b3c355e3b620f81d3ac0e0c` |
|  PD   | `70aaa5eee830e21068f1ba2d4c9bae59153e5ca3` |

### v2.1.13

| Component  |                 GitHash                  |
| :--- | :-------------------------------------- |
| TiDB  | `6b5b1a6802f9b8f5a22d8aab24ac80729331e1bc` |
| TiKV  | `b3cf3c8d642534ea6fa93d475a46da285cc6acbf` |
|  PD   | `886362ebfb26ef0834935afc57bcee8a39c88e54` |

### TiDB parameter configuration

Enable the prepared plan cache in both TiDB v2.1 and v3.0 (`point select` and `read write` are not enabled in v2.1 for optimization reasons):

```toml
[prepared-plan-cache]
enabled = true
```

Then configure global variables:

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_disable_txn_auto_retry=0;
```

In addition, make the following configuration in v3.0:

```toml
[tikv-client]
max-batch-wait-time = 2000000
```

### TiKV parameter configuration

Configure the global variable in both TiDB v2.1 and v3.0:

```toml
log-level = "error"
[readpool.storage]
normal-concurrency = 10
[server]
grpc-concurrency = 6
[rocksdb.defaultcf]
block-cache-size = "14GB"
[rocksdb.writecf]
block-cache-size = "8GB"
[rocksdb.lockcf]
block-cache-size = "1GB"
```

In addition, make the following configuration in v3.0:

```toml
[raftstore]
apply-pool-size = 3
store-pool-size = 3
```

### Cluster topology

|                 Machine IP                  |  Deployment instance  |
| :-------------------------------------- | :--------- |
|                172.31.8.8                | 3 * Sysbench |
| 172.31.7.80, 172.31.5.163, 172.31.11.123 |      PD      |
| 172.31.4.172, 172.31.1.155, 172.31.9.210 |     TiKV     |
| 172.31.7.80, 172.31.5.163, 172.31.11.123 |     TiDB     |

## Test result

### `Point Select` test

**v2.1:**

| Threads |   QPS    | 95% latency(ms) |
| :------- | :-------- | :------------- |
| 150     | 240304.06 |            1.61 |
| 300     | 276635.75 |            2.97 |
| 600     | 307838.06 |            5.18 |
| 900     | 323667.93 |            7.30 |
| 1200    | 330925.73 |            9.39 |
| 1500    | 336250.38 |           11.65 |

<!-- plan cache enabled
| Threads |    QPS    | 95% latency(ms) |
| :------- | :--------| :-------------- |
| 150     | 175247.08 |            2.35 |
| 300     | 189423.99 |            4.41 |
| 600     | 197425.51 |            8.43 |
| 900     | 202451.18 |           12.08 |
| 1200    | 204908.95 |           15.83 |
| 1500    | 206572.53 |           19.65 |
-->

**v3.0:**

| Threads |    QPS    | 95% latency(ms) |
| :------- | :-------- | :-------------- |
| 150     | 334219.04 |            0.64 |
| 300     | 456444.86 |            1.10 |
| 600     | 512177.48 |            2.11 |
| 900     | 525945.13 |            3.13 |
| 1200    | 534577.36 |            4.18 |
| 1500    | 533944.64 |            5.28 |

![point select](/media/sysbench_v4_point_select.png)

### `Update Non-Index` test

**v2.1:**

| Threads |   QPS    | 95% latency (ms) |
| :------- | :------- | :-------------- |
| 150     | 21785.37 |            8.58 |
| 300     | 28979.27 |           13.70 |
| 600     | 34629.72 |           24.83 |
| 900     | 36410.06 |           43.39 |
| 1200    | 37174.15 |           62.19 |
| 1500    | 37408.88 |           87.56 |

**v3.0:**

| Threads |   QPS    | 95% latency (ms) |
| :------- | :------- | :-------------- |
| 150     | 28045.75 |            6.67 |
| 300     | 39237.77 |            9.91 |
| 600     | 49536.56 |           16.71 |
| 900     | 55963.73 |           22.69 |
| 1200    | 59904.02 |           29.72 |
| 1500    | 62247.95 |           42.61 |

![update non-index](/media/sysbench_v4_update_non_index.png)

### `Update Index` test

**v2.1:**

| Threads |   QPS    | 95% latency(ms) |
| :------- | :------- | :-------------- |
| 150     | 14378.24 |           13.22 |
| 300     | 16916.43 |           24.38 |
| 600     | 17636.11 |           57.87 |
| 900     | 17740.92 |           95.81 |
| 1200    | 17929.24 |          130.13 |
| 1500    | 18012.80 |          161.51 |

**v3.0:**

| Threads |   QPS    | 95% latency(ms) |
| :------- | :------- | :-------------- |
| 150     | 19047.32 |           10.09 |
| 300     | 24467.64 |           16.71 |
| 600     | 28882.66 |           31.94 |
| 900     | 30298.41 |           57.87 |
| 1200    | 30419.40 |           92.42 |
| 1500    | 30643.55 |          125.52 |

![update index](/media/sysbench_v4_update_index.png)

### `Read Write` test

**v2.1:**

| Threads |   TPS   |   QPS    | 95% latency(ms) |
| :------- | :------ | :------- | :-------------- |
| 150     |  85140.60 |           44.98 |
| 300     |  96773.01 |           82.96 |
| 600     | 105139.81 |          153.02 |
| 900     | 110041.83 |          215.44 |
| 1200    | 113242.70 |          277.21 |
| 1500    | 114542.19 |          337.94 |

<!-- plan cache enabled
| Treads |    QPS    | 95% latency(ms) |
| :------- | :-------- | :-------------- |
| 150     |  81339.88 |           47.47 |
| 300     |  94455.29 |           86.00 |
| 600     | 103125.91 |          161.51 |
| 900     | 105984.81 |          235.74 |
| 1200    | 106639.19 |          320.17 |
| 1500    | 107312.93 |          390.30 |
-->

**v3.0:**

| Threads |    QPS    | 95% latency(ms) |
| :------- | :-------- | :-------------- |
| 150     | 105692.08 |           35.59 |
| 300     | 129769.69 |           58.92 |
| 600     | 141430.86 |          114.72 |
| 900     | 144371.76 |          170.48 |
| 1200    | 143344.37 |          223.34 |
| 1500    | 144567.91 |          277.21 |

![read write](/media/sysbench_v4_read_write.png)
