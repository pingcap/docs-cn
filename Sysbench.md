---
title: Sysbench 性能测试报告
category: introduction
---

# 测试目的

测试对比 TiDB v4.0 和 v3.0 OLTP 场景下的性能。

## 测试环境 （AWS EC2）

### 硬件配置

| 服务类型   | EC2 类型   |    节点数  |      
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiDB      | i3.4xlarge|     3     |
| TiKV      | c5.4xlarge|     3     |
| Sysbench  | m5.4xlarge|     1     |

### 软件版本

| 服务类型   | 软件版本        
|:----------|:-----------|
| PD        | 3.0、4.0   |
| TiDB      | 3.0、4.0   |
| TiKV      | 3.0、4.0   |
| Sysbench  | 1.0.20     |

### 配置参数

#### v3.0

#### tidb:
    log.level: “error”
    performance.max-procs: 20
    prepared-plan-cache.enabled: true
    tikv-client.max-batch-wait-time: 2000000
    
#### tikv:
    storage.scheduler-worker-pool-size: 5
    raftstore.store-pool-size: 3
    raftstore.apply-pool-size: 3
    rocksdb.max-background-jobs: 3
    raftdb.max-background-jobs: 3
    raftdb.allow-concurrent-memtable-write: true
    server.grpc-concurrency: 6
    readpool.storage.normal-concurrency: 10
    readpool.coprocessor.normal-concurrency: 5

### v4.0
#### tidb:
    log.level: "error"
    performance.max-procs: 20
    prepared-plan-cache.enabled: true
    tikv-client.max-batch-wait-time: 2000000
    
#### tikv:
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

#### 全局变量

- set global tidb_hashagg_final_concurrency=1;

- set global tidb_hashagg_partial_concurrency=1;

- set global tidb_disable_txn_auto_retry=0;

### 测试方案

- 通过 TiUP 部署 TiDB v4.0 和 v3.0。

- 通过 Sysbench 导入 16 张表，每张表数据 1000 万数据。

- 分别对每个表执行 `analyze table` 命令。

- 备份数据用于不同并发测试前进行恢复以保证每次数据一致。

- 启动 Sysbench 客户端，测试 point_select, read_write，update_index, update_non_index，通过 aws nlb 向 TIDB 加压，单次预热 1 分钟，测试 5 分钟。

- 每轮完成后停止集群，使用之前的备份的数据覆盖，再启动集群

### 准备数据命令：

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
 
### 执行测试命令：

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

### 测试结果

#### Point Select

![Point Select](/media/sysbench_v4vsv3_point_select.png)

#### Update Non-index

![Update Non-index](/media/sysbench_v4vsv3_update_non_index.png)

#### Update Index

![Update Index](/media/sysbench_v4vsv3_update_index.png)

#### Read Write

![Read Write](/media/sysbench_v4vsv3_read_write.png)


