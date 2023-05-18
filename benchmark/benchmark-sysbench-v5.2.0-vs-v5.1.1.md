---
title: TiDB Sysbench 性能对比测试报告 - v5.2.0 对比 v5.1.1
---

# TiDB Sysbench 性能对比测试报告 - v5.2.0 对比 v5.1.1

## 测试概况

本次测试对比了 TiDB v5.2.0 和 v5.1.1 在 OLTP 场景下的 Sysbench 性能表现。结果显示，v5.2.0 相比于 v5.1.1，Point Select 场景性能提升了 11.03%，其余场景性能略有下降。

## 测试环境 (AWS EC2)

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
| PD        | v5.1.1、v5.2.0   |
| TiDB      | v5.1.1、v5.2.0   |
| TiKV      | v5.1.1、v5.2.0   |
| Sysbench  | 1.1.0-ead2689   |

### 参数配置

两个版本使用相同的配置

#### TiDB 参数配置

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV 参数配置

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
server.enable-request-batch: false
```

#### TiDB 全局变量配置

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

1. 通过 TiUP 部署 TiDB v5.2.0 和 v5.1.1。
2. 通过 Sysbench 导入 16 张表，每张表有 1000 万行数据。
3. 分别对每个表执行 `analyze table` 命令。
4. 备份数据，用于不同并发测试前进行数据恢复，以保证每次数据一致。
5. 启动 Sysbench 客户端，进行 `point_select`、`read_write`、`update_index` 和 `update_non_index` 测试。通过 HAProxy 向 TiDB 加压，测试 5 分钟。
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

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|143014.13|2.35|174402.5|1.23|21.95%|
|300|199133.06|3.68|272018|1.64|36.60%|
|600|389391.65|2.18|393536.4|2.11|1.06%|
|900|468338.82|2.97|447981.98|3.3|-4.35%|
|1200|448348.52|5.18|468241.29|4.65|4.44%|
|1500|454376.79|7.04|483888.42|6.09|6.49%|

v5.2.0 对比 v5.1.1，Point Select 性能提升了 11.03%。

![Point Select](/media/sysbench_v511vsv520_point_select.png)

### Update Non-index 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|31198.68|6.43|30714.73|6.09|-1.55%|
|300|43577.15|10.46|42997.92|9.73|-1.33%|
|600|57230.18|17.32|56168.81|16.71|-1.85%|
|900|65325.11|23.1|64098.04|22.69|-1.88%|
|1200|71528.26|28.67|69908.15|28.67|-2.26%|
|1500|76652.5|33.12|74371.79|33.72|-2.98%|

v5.2.0 对比 v5.1.1，Update Non-index 性能下降了 1.98%。

![Update Non-index](/media/sysbench_v511vsv520_update_non_index.png)

### Update Index 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|15641.04|13.22|15320|13.46|-2.05%|
|300|19787.73|21.89|19161.35|22.69|-3.17%|
|600|24566.74|36.89|23616.07|38.94|-3.87%|
|900|27516.57|50.11|26270.04|54.83|-4.53%|
|1200|29421.10|63.32|28002.65|69.29|-4.82%|
|1500|30957.84|77.19|28624.44|95.81|-7.54%|

v5.2.0 对比 v5.1.1，Update Index 性能下降了 4.33%。

![Update Index](/media/sysbench_v511vsv520_update_index.png)

### Read Write 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|68471.02|57.87|69246|54.83|1.13%|
|300|86573.09|97.55|85340.42|94.10|-1.42%|
|600|101760.75|176.73|102221.31|173.58|0.45%|
|900|111877.55|248.83|109276.45|257.95|-2.32%|
|1200|117479.4|337.94|114231.33|344.08|-2.76%|
|1500|119662.91|419.45|116663.28|434.83|-2.51%|

v5.2.0 对比 v5.1.1，Read Write 性能下降了 1.24%。

![Read Write](/media/sysbench_v511vsv520_read_write.png)
