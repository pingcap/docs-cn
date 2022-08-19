---
title: TiDB Sysbench 性能对比测试报告 - v6.2.0 对比 v6.1.0
---

# TiDB Sysbench 性能对比测试报告 - v6.2.0 对比 v6.1.0

## 测试概况

本次测试对比了 TiDB v6.2.0 和 v6.1.0 在 OLTP 场景下的 Sysbench 性能表现。结果显示，两个版本性能基本持平，相比于 v6.1.0，v6.2.0 的 Point Select 性能下降了 3.58%。

## 测试环境 (AWS EC2)

### 硬件配置

| 服务类型 | EC2 类型   | 实例数 |
| :------- | :--------- | :----- |
| PD       | m5.xlarge  | 3      |
| TiKV     | i3.4xlarge | 3      |
| TiDB     | c5.4xlarge | 3      |
| Sysbench | c5.9xlarge | 1      |

### 软件版本

| 服务类型 | 软件版本       |
| :------- | :------------- |
| PD       | v6.1.0、v6.2.0 |
| TiDB     | v6.1.0、v6.2.0 |
| TiKV     | v6.1.0、v6.2.0 |
| Sysbench | 1.1.0-df89d34  |

### 参数配置

两个版本使用相同的配置。

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
server.grpc-concurrency: 6
readpool.unified.max-thread-count: 10
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
set global tidb_prepared_plan_cache_size=1000;
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

1. 通过 TiUP 部署 TiDB v6.2.0 和 v6.1.0。
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

| Threads | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95% latency (ms) | v6.2.0 95% latency (ms) | TPS 提升 (%) |
| :------ | :--------- | :--------- | :---------------------- | :---------------------- | :----------- |
| 300     | 243530.01  | 236885.24  | 1.93                    | 2.07                    | -2.73        |
| 600     | 304121.47  | 291395.84  | 3.68                    | 4.03                    | -4.18        |
| 900     | 327301.23  | 314720.02  | 5                       | 5.47                    | -3.84        |

v6.2.0 对比 v6.1.0，Point Select 性能下降了 3.58%。

![Point Select](/media/sysbench_v610vsv620_point_select.png)

### Update Non-index 性能

| Threads | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95% latency (ms) | v6.2.0 95% latency (ms) | TPS 提升 (%) |
| :------ | :--------- | :--------- | :---------------------- | :---------------------- | :----------- |
| 300     | 42608.8    | 42372.82   | 11.45                   | 11.24                   | -0.55        |
| 600     | 54264.47   | 53672.69   | 18.95                   | 18.95                   | -1.09        |
| 900     | 60667.47   | 60116.14   | 26.2                    | 26.68                   | -0.91        |

v6.2.0 对比 v6.1.0，Update Non-index 性能基本持平，下降了 0.85%。

![Update Non-index](/media/sysbench_v610vsv620_update_non_index.png)

### Update Index 性能

| Threads | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95% latency (ms) | v6.2.0 95% latency (ms) | TPS 提升 (%) |
| :------ | :--------- | :--------- | :---------------------- | :---------------------- | :----------- |
| 300     | 19384.75   | 19353.58   | 23.52                   | 23.52                   | -0.16        |
| 600     | 24144.78   | 24007.57   | 38.25                   | 37.56                   | -0.57        |
| 900     | 26770.9    | 26589.84   | 51.94                   | 52.89                   | -0.68        |

v6.2.0 对比 v6.1.0，Update Index 性能基本持平，下降了 0.47%。

![Update Index](/media/sysbench_v610vsv620_update_index.png)

### Read Write 性能

| Threads | v6.1.0 TPS | v6.2.0 TPS | v6.1.0 95% latency (ms) | v6.2.0 95% latency (ms) | TPS 提升 (%) |
| :------ | :--------- | :--------- | :---------------------- | :---------------------- | :----------- |
| 300     | 4849.67    | 4797.59    | 86                      | 84.47                   | -1.07        |
| 600     | 5643.89    | 5565.17    | 161.51                  | 161.51                  | -1.39        |
| 900     | 5954.91    | 5885.22    | 235.74                  | 235.74                  | -1.17        |

v6.2.0 对比 v6.1.0，Read Write 性能下降了 1.21%。

![Read Write](/media/sysbench_v610vsv620_read_write.png)
