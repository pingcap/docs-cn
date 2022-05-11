---
title: TiDB Sysbench 性能对比测试报告 - v6.0.0 对比 v5.4.0
---

# TiDB Sysbench 性能对比测试报告 - v6.0.0 对比 v5.4.0

## 测试概况

本次测试对比了 TiDB v6.0.0 和 v5.4.0 在 OLTP 场景下的 Sysbench 性能表现。结果显示，相比于 v5.4.0，v6.0.0 的 Read Write 负载性能有大幅提升，提升了 16.17%。其他负载性能基本与 v5.4.0 的持平。

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
| PD        | v5.4.0、v6.0.0   |
| TiDB      | v5.4.0、v6.0.0   |
| TiKV      | v5.4.0、v6.0.0   |
| Sysbench  | 1.1.0-df89d34   |

### 参数配置

两个版本使用相同的配置

#### TiDB 参数配置

{{< copyable "" >}}

```yaml
log.level: "error"
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
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
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

#### HAProxy 配置 - haproxy.cfg 文件

更多有关 HAProxy 在 TiDB 上的使用，可参阅 [HAProxy 在 TiDB 中的最佳实践](/best-practices/haproxy-best-practices.md)。

{{< copyable "" >}}

```yaml
global                                     # 全局配置。
   pidfile     /var/run/haproxy.pid        # 将 HAProxy 进程的 PID 写入 pidfile。
   maxconn     4000                        # 每个 HAProxy 进程所接受的最大并发连接数。
   user        haproxy                     # 同 UID 参数。
   group       haproxy                     # 同 GID 参数，建议使用专用用户组。
   nbproc      64                          # 在后台运行时创建的进程数。在启动多个进程转发请求时，确保该值足够大，保证 HAProxy 不会成为瓶颈。
   daemon                                  # 让 HAProxy 以守护进程的方式工作于后台，等同于命令行参数“-D”的功能。当然，也可以在命令行中用“-db”参数将其禁用。

defaults                                   # 默认配置。
   log global                              # 日志继承全局配置段的设置。
   retries 2                               # 向上游服务器尝试连接的最大次数，超过此值便认为后端服务器不可用。
   timeout connect  2s                     # HAProxy 与后端服务器连接超时时间。如果在同一个局域网内，可设置成较短的时间。
   timeout client 30000s                   # 客户端与 HAProxy 连接后，数据传输完毕，即非活动连接的超时时间。
   timeout server 30000s                   # 服务器端非活动连接的超时时间。

listen tidb-cluster                        # 配置 database 负载均衡。
   bind 0.0.0.0:3390                       # 浮动 IP 和 监听端口。
   mode tcp                                # HAProxy 要使用第 4 层的传输层。
   balance leastconn                      # 连接数最少的服务器优先接收连接。`leastconn` 建议用于长会话服务，例如 LDAP、SQL、TSE 等，而不是短会话协议，如 HTTP。该算法是动态的，对于启动慢的服务器，服务器权重会在运行中作调整。
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # 检测 4000 端口，检测频率为每 2000 毫秒一次。如果 2 次检测为成功，则认为服务器可用；如果 3 次检测为失败，则认为服务器不可用。
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## 测试方案

1. 通过 TiUP 部署 TiDB v6.0.0 和 v5.4.0。
2. 通过 Sysbench 导入 16 张表，每张表有 1000 万行数据。
3. 分别对每个表执行 `analyze table` 命令。
4. 备份数据，用于不同并发测试前进行数据恢复，以保证每次数据一致。
5. 启动 Sysbench 客户端，进行 `point_select`、`read_write`、`update_index` 和 `update_non_index` 测试。通过 HAProxy 向 TiDB 加压，每种负载每个并发数各测试 20 分钟。
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
    --time=1200 \
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

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS 提升 (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|260085.19|265207.73|1.82|1.93|1.97|
|600|378098.48|365173.66|2.48|2.61|-3.42|
|900|441294.61|424031.23|3.75|3.49|-3.91|

v6.0.0 对比 v5.4.0，Point Select 性能基本持平，略下降了 1.79%。

![Point Select](/media/sysbench_v540vsv600_point_select.png)

### Update Non-index 性能

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS 提升 (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|41528.7|40814.23|11.65|11.45|-1.72|
|600|53220.96|51746.21|19.29|20.74|-2.77|
|900|59977.58|59095.34|26.68|28.16|-1.47|

v6.0.0 对比 v5.4.0，Update Non-index 性能基本持平，略下降了 1.98%。

![Update Non-index](/media/sysbench_v540vsv600_update_non_index.png)

### Update Index 性能

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS 提升 (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|18659.11|18187.54|23.95|25.74|-2.53|
|600|23195.83|22270.81|40.37|44.17|-3.99|
|900|25798.31|25118.78|56.84|57.87|-2.63|

v6.0.0 对比 v5.4.0，Update Index 性能下降了 3.05%。

![Update Index](/media/sysbench_v540vsv600_update_index.png)

### Read Write 性能

| Threads   | v5.4.0 TPS  | v6.0.0 TPS | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS 提升 (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|4141.72|4829.01|97.55|82.96|16.59|
|600|4892.76|5693.12|173.58|153.02|16.36|
|900|5217.94|6029.95|257.95|235.74|15.56|

v6.0.0 对比 v5.4.0，Read Write 性能有大幅提升，提升了 16.17%。

![Read Write](/media/sysbench_v540vsv600_read_write.png)
