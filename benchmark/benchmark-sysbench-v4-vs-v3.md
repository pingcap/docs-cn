---
title: TiDB Sysbench 性能对比测试报告 - v4.0 对比 v3.0
aliases: ['/docs-cn/stable/benchmark/benchmark-sysbench-v4-vs-v3/','/docs-cn/v4.0/benchmark/benchmark-sysbench-v4-vs-v3/']
---

# TiDB Sysbench 性能对比测试报告 - v4.0 对比 v3.0

## 测试目的

测试对比 TiDB v4.0 和 v3.0 在 OLTP 场景下的性能。

## 测试环境 (AWS EC2）

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
readpool.unifiy-read-pool: true
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

v4.0 对比 v3.0，Point Select 性能提升了 14%。

![Point Select](/media/sysbench_v4vsv3_point_select.png)

### Update Non-index 性能

v4.0 对比 v3.0，Update Non-index 性能提升了 15%。

![Update Non-index](/media/sysbench_v4vsv3_update_non_index.png)

### Update Index 性能

v4.0 对比 v3.0，Update Index 性能提升了 17%。

![Update Index](/media/sysbench_v4vsv3_update_index.png)

### Read Write 性能

v4.0 对比 v3.0，Read Write 性能提升了 31%。

![Read Write](/media/sysbench_v4vsv3_read_write.png)
