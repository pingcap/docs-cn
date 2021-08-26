---
title: TiDB Sysbench 性能对比测试报告 - v5.2.0 对比 v5.1.1
---

# TiDB Sysbench 性能对比测试报告 - v5.2.0 对比 v5.1.1

## 测试概况

本次测试对比了 TiDB v5.2.0 和 v5.1.1 在 OLTP 场景下的 Sysbench 性能表现。结果显示，v5.2.0 相比于 v5.1.1，Point Select 场景性能提升了 10.99%，其余场景性能略有下降。
补充说明：v5.2.0 默认设置了 security.auto-tls: true。

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
|150|160676.9|1.64|179631.85|1.37|11.80%|
|300|203228.6|3.82|257122.76|2.03|26.52%|
|600|378170.8|2.48|404131.11|2.11|6.86%|
|900|374396.84|4.91|440576.03|4.03|17.68%|
|1200|451324.31|5.28|444254.87|6.79|-1.57%|
|1500|433282.09|7.84|453505.33|9.91|4.67%|

v5.2.0 对比 v5.1.1，Point Select 性能提升了 10.99%。

![Point Select](/media/sysbench_v511vsv520_point_select.png)

### Update Non-index 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|32404.14|6.09|31085.33|6.09|-4.07%|
|300|44218.98|10.65|44331.95|9.73|0.26%|
|600|57589.33|17.95|56314.28|16.71|-2.21%|
|900|64720.28|23.95|65126.74|22.69|0.63%|
|1200|72202.15|28.67|70388.61|28.67|-2.51%|
|1500|77143.18|33.72|75882.73|33.72|-1.63%|

v5.2.0 对比 v5.1.1，Update Non-index 性能下降了 1.59%。

![Update Non-index](/media/sysbench_v511vsv520_update_non_index.png)

### Update Index 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|15826.6|13.7|15505.09|13.46|-2.03%|
|300|20054.43|22.28|19490.27|21.89|-2.81%|
|600|25045.25|36.24|23675.51|38.25|-5.47%|
|900|27724.19|50.11|26583.06|54.83|-4.12%|
|1200|29208.04|66.84|27974.63|73.13|-4.22%|
|1500|30815.46|82.96|29295.68|90.78|-4.93%|

v5.2.0 对比 v5.1.1，Update Index 性能下降了 3.93%。

![Update Index](/media/sysbench_v511vsv520_update_index.png)

### Read Write 性能

| Threads   | v5.1.1 QPS   | v5.1.1 95% latency (ms)   | v5.2.0 QPS   | v5.2.0 95% latency (ms)   | QPS 提升   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|71416.14|54.83|71179.40|53.85|-0.33%|
|300|87729.61|95.81|87847.18|94.1|0.13%|
|600|103187.64|176.73|102699.47|179.94|-0.47%|
|900|111595.33|248.83|110568.85|267.41|-0.92%|
|1200|119105.44|320.17|114207.05|356.7|-4.11%|
|1500|120574.91|404.61|117691.04|450.77|-2.39%|

v5.2.0 对比 v5.1.1，Read Write 性能下降了 1.35%。

![Read Write](/media/sysbench_v511vsv520_read_write.png)
