---
title: TiDB Sysbench 性能对比测试报告 - v5.1.0 对比 v5.0.2
---

# TiDB Sysbench 性能对比测试报告 - v5.1.0 对比 v5.0.2

## 测试概况

本次测试对比了 TiDB v5.1.0 和 v5.0.2 在 OLTP 场景下的 Sysbench 性能表现。结果显示，v5.1.0 相比于 v5.0.2，Point Select 场景性能提升了 19.4%，Read Write 和 Update Index 场景性能略有下降。

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
| PD        | v5.0.2、v5.1.0   |
| TiDB      | v5.0.2、v5.1.0   |
| TiKV      | v5.0.2、v5.1.0   |
| Sysbench  | 1.0.20     |

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

1. 通过 TiUP 部署 TiDB v5.1.0 和 v5.0.2。
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

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|137732.27|1.86|158861.67|2|15.34%|
|300|201420.58|2.91|238038.44|2.71|18.18%|
|600|303631.52|3.49|428573.21|2.07|41.15%|
|900|383628.13|3.55|464863.22|3.89|21.18%|
|1200|391451.54|5.28|413656.74|13.46|5.67%|
|1500|410276.93|7.43|471418.78|10.65|14.90%|

v5.1.0 对比 v5.0.2，Point Select 性能提升了 19.4%。

![Point Select](/media/sysbench_v510vsv502_point_select.png)

### Update Non-index 性能

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|29248.2|7.17|29362.7|8.13|0.39%|
|300|40316.09|12.52|39651.52|13.7|-1.65%|
|600|51011.11|22.28|47047.9|27.66|-7.77%|
|900|58814.16|27.66|59331.84|28.67|0.88%|
|1200|65286.52|32.53|67745.39|31.37|3.77%|
|1500|68300.86|39.65|67899.17|44.17|-0.59%|

v5.1.0 对比 v5.0.2，Update Non-index 性能下降了 0.8%。

![Update Non-index](/media/sysbench_v510vsv502_update_non_index.png)

### Update Index 性能

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|15066.54|14.73|14829.31|14.73|-1.57%|
|300|18535.92|24.83|17401.01|29.72|-6.12%|
|600|22862.73|41.1|21923.78|44.98|-4.11%|
|900|25286.74|57.87|24916.76|58.92|-1.46%|
|1200|27566.18|70.55|27800.62|69.29|0.85%|
|1500|28184.76|92.42|28679.72|86|1.76%|

v5.1.0 对比 v5.0.2，Update Index 性能下降了 1.8%。

![Update Index](/media/sysbench_v510vsv502_update_index.png)

### Read Write 性能

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|66415.33|56.84|66591.49|57.87|0.27%|
|300|82488.39|97.55|81226.41|101.13|-1.53%|
|600|99195.36|173.58|97357.86|179.94|-1.85%|
|900|107382.76|253.35|101665.95|267.41|-5.32%|
|1200|112389.23|337.94|107426.41|350.33|-4.42%|
|1500|113548.73|450.77|109805.26|442.73|-3.30%|

v5.1.0 对比 v5.0.2，Read Write 性能下降了 2.7%。

![Read Write](/media/sysbench_v510vsv502_read_write.png)
