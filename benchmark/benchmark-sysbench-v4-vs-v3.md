---
title: TiDB Sysbench 性能对比测试报告 - v4.0 对比 v3.0
---

# TiDB Sysbench 性能对比测试报告 - v4.0 对比 v3.0

## 测试目的

测试对比 TiDB v4.0 和 v3.0 在 OLTP 场景下的性能。

## 测试环境 (AWS EC2)

### 硬件配置

| 服务类型   | EC2 类型   |    实例数  |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | m5.4xlarge|     1     |

### 软件版本

| 服务类型   | 软件版本   |
|:----------|:-----------|
| PD        | 3.0、4.0   |
| TiDB      | 3.0、4.0   |
| TiKV      | 3.0、4.0   |
| Sysbench  | 1.0.20     |

### 参数配置

#### TiDB v3.0 参数配置

{{< copyable "" >}}

```yaml
log.level: “error”
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v3.0 参数配置

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
readpool.coprocessor.normal-concurrency: 5
```

#### TiDB v4.0 参数配置

{{< copyable "" >}}

```yaml
log.level: “error”
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

#### 全局变量配置

{{< copyable "sql" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_disable_txn_auto_retry=0;
```

## 测试方案

1. 通过 TiUP 部署 TiDB v4.0 和 v3.0。
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

| Threads   | v3.0 QPS   | v3.0 95% latency (ms)   | v4.0 QPS   | v4.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 117085.701 |     1.667     | 118165.1357        | 1.608 |     0.92%     |
| 300      | 200621.4471|     2.615     | 207774.0859        | 2.032 |     3.57%     |
| 600      | 283928.9323|     4.569     | 320673.342        | 3.304 |     12.94%     |
| 900  | 343218.2624|     6.686     | 383913.3855        | 4.652 |     11.86%     |
| 1200  | 347200.2366|     8.092     | 408929.4372        | 6.318 |     17.78%     |
| 1500  | 366406.2767|     10.562     | 418268.8856        | 7.985 |     14.15%     |

v4.0 对比 v3.0，Point Select 性能提升了 14%。

![Point Select](/media/sysbench_v4vsv3_point_select.png)

### Update Non-index 性能

| Threads   | v3.0 QPS   | v3.0 95% latency (ms)   | v4.0 QPS   | v4.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 15446.41024 |     11.446     | 16954.39971        | 10.844 |     9.76%     |
| 300      | 22276.15572|     17.319     | 24364.44689        | 16.706 |     9.37%     |
| 600      | 28784.88353|     29.194     | 31635.70833        | 28.162 |     9.90%    |
| 900  | 32194.15548|     42.611     | 35787.66078        | 38.942 |     11.16%     |
| 1200  | 33954.69114|     58.923     | 38552.63158        | 51.018 |     13.54%     |
| 1500  | 35412.0032|     74.464     | 40859.63755        | 62.193 |     15.38%     |

v4.0 对比 v3.0，Update Non-index 性能提升了 15%。

![Update Non-index](/media/sysbench_v4vsv3_update_non_index.png)

### Update Index 性能

| Threads   | v3.0 QPS   | v3.0 95% latency (ms)   | v4.0 QPS   | v4.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 11164.40571 |     16.706     | 11954.73635        | 16.408 |     7.08%     |
| 300      | 14460.98057|     28.162     | 15243.40899        | 28.162 |     5.41%     |
| 600      | 17112.73036|     53.85     | 18535.07515        | 50.107 |     8.31%    |
| 900  | 18233.83426|     86.002     | 20339.6901        | 70.548 |     11.55%     |
| 1200  | 18622.50283|     127.805     | 21390.25122        | 94.104 |     14.86%     |
| 1500  | 18980.34447|     170.479     | 22359.996        | 114.717 |     17.81%     |

v4.0 对比 v3.0，Update Index 性能提升了 17%。

![Update Index](/media/sysbench_v4vsv3_update_index.png)

### Read Write 性能

| Threads   | v3.0 QPS   | v3.0 95% latency (ms)   | v4.0 QPS   | v4.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
| 150        | 43768.33633 |     71.83     | 53912.63705        | 59.993 |     23.18%     |
| 300      | 55655.63589|     121.085     | 71327.21336        | 97.555 |     28.16%     |
| 600      | 64642.96992|     223.344     | 84487.75483        | 176.731 |     30.70%    |
| 900  | 68947.25293|     325.984     | 90177.94612        | 257.95 |     30.79%     |
| 1200  | 71334.80099|     434.829     | 92779.71507        | 344.078 |     30.06%     |
| 1500  | 72069.9115|     580.017     | 95088.50812        | 434.829 |     31.94%     |

v4.0 对比 v3.0，Read Write 性能提升了 31%。

![Read Write](/media/sysbench_v4vsv3_read_write.png)
