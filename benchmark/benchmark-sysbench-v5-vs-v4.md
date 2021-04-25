---
title: TiDB Sysbench 性能对比测试报告 - v5.0 对比 v4.0
---

# TiDB Sysbench 性能对比测试报告 - v5.0 对比 v4.0

## 测试目的

测试对比 TiDB v5.0 和 v4.0 在 OLTP 场景下的性能。

## 测试环境 (AWS EC2）

### 硬件配置

| 服务类型   | EC2 类型   |    实例数  |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | c5.9xlarge|     1     |

### 软件版本

| 服务类型   | 软件版本   |
|:----------|:-----------|
| PD        | 4.0、5.0   |
| TiDB      | 4.0、5.0   |
| TiKV      | 4.0、5.0   |
| Sysbench  | 1.0.20     |

### 参数配置

#### TiDB v4.0 参数配置

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v4.0 参数配置

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.request-batch-enable-cross-command: false
server.grpc-concurrency: 6
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
```

#### TiDB v5.0 参数配置

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v5.0 参数配置

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 8
raftdb.max-background-jobs: 4
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
enable-request-batch: false
```

#### TiDB v4.0 全局变量配置

{{< copyable "sql" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
```

#### TiDB v5.0 全局变量配置

{{< copyable "sql" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_enable_async_commit = 1;
set global tidb_enable_1pc = 1;
set global tidb_guarantee_linearizability = 0;
set global tidb_enable_clustered_index = 1; 

```

## 测试方案

1. 通过 TiUP 部署 TiDB v5.0 和 v4.0。
2. 通过 Sysbench 导入 16 张表，每张表有 1000 万行数据。
3. 分别对每个表执行 `analyze table` 命令。
4. 备份数据，用于不同并发测试前进行数据恢复，以保证每次数据一致。
5. 启动 Sysbench 客户端，进行 `point_select`、`read_write`、`update_index` 和 `update_non_index` 测试。通过 AWS NLB 向 TiDB 加压，单轮预热 1 分钟，测试 5 分钟。
6. 每轮完成后停止集群，使用之前的备份的数据覆盖，再启动集群。

### 准备测试数据

执行以下命令来准备测试数据：

{{< copyable "shell-regular" >}}

```bash
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    --mysql-user=root \
    --mysql-password=password \
    prepare --tables=16 --table-size=10000000
```

### 执行测试命令

执行以下命令来执行测试：

{{< copyable "shell-regular" >}}

```bash
sysbench $testname \
    --threads=$threads \
    --time=300 \
    --report-interval=1 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    run --tables=16 --table-size=10000000
```

## 测试结果

### Point Select 性能

| Threads   | v4.0 QPS   | v4.0 95% latency (ms)   | v5.0 QPS   | v5.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 159451.19        | 1.32        | 177876.25        | 1.23        | 11.56%     |
| 300        | 244790.38        | 1.96        | 252675.03        | 1.82        | 3.22%     |
| 600        | 322929.05        | 3.75        | 331956.84        | 3.36        | 2.80%     |
| 900        | 364840.05        | 5.67        | 365655.04        | 5.09        | 0.22%     |
| 1200        | 376529.18        | 7.98        | 366507.47        | 7.04        | -2.66%     |
| 1500        | 368390.52        | 10.84        | 372476.35        | 8.90        | 1.11%     |

v5.0 对比 v4.0，Point Select 性能提升了 2.7%。

![Point Select](/media/sysbench_v5vsv4_point_select.png)

### Update Non-index 性能

| Threads   | v4.0 QPS   | v4.0 95% latency (ms)   | v5.0 QPS   | v5.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 17243.78        | 11.04        | 30866.23        | 6.91        | 79.00%     |
| 300        | 25397.06        | 15.83        | 45915.39        | 9.73        | 80.79%     |
| 600        | 33388.08        | 25.28        | 60098.52        | 16.41        | 80.00%     |
| 900        | 38291.75        | 36.89        | 70317.41        | 21.89        | 83.64%     |
| 1200        | 41003.46        | 55.82        | 76376.22        | 28.67        | 86.27%     |
| 1500        | 44702.84        | 62.19        | 80234.58        | 34.95        | 79.48%     |

v5.0 对比 v4.0，Update Non-index 性能提升了 81%。

![Update Non-index](/media/sysbench_v5vsv4_update_non_index.png)

### Update Index 性能

| Threads   | v4.0 QPS   | v4.0 95% latency (ms)   | v5.0 QPS   | v5.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 11736.21        | 17.01        | 15631.34        | 17.01        | 33.19%     |
| 300        | 15435.95        | 28.67        | 19957.06        | 22.69        | 29.29%     |
| 600        | 18983.21        | 49.21        | 23218.14        | 41.85        | 22.31%     |
| 900        | 20855.29        | 74.46        | 26226.76        | 53.85        | 25.76%     |
| 1200        | 21887.64        | 102.97        | 28505.41        | 69.29        | 30.24%     |
| 1500        | 23621.15        | 110.66        | 30341.06        | 82.96        | 28.45%     |

v5.0 对比 v4.0，Update Index 性能提升了 28%。

![Update Index](/media/sysbench_v5vsv4_update_index.png)

### Read Write 性能

| Threads   | v4.0 QPS   | v4.0 95% latency (ms)   | v5.0 QPS   | v5.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 59979.91        | 61.08        | 66098.57        | 55.82        | 10.20%     |
| 300        | 77118.32        | 102.97        | 84639.48        | 90.78        | 9.75%     |
| 600        | 90619.52        | 183.21        | 101477.46        | 167.44        | 11.98%     |
| 900        | 97085.57        | 267.41        | 109463.46        | 240.02        | 12.75%     |
| 1200        | 106521.61        | 331.91        | 115416.05        | 320.17        | 8.35%     |
| 1500        | 116278.96        | 363.18        | 118807.5        | 411.96        | 2.17%     |

v5.0 对比 v4.0，Read Write 性能提升了 9%。

![Read Write](/media/sysbench_v5vsv4_read_write.png)
