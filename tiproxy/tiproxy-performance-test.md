---
title: TiProxy 性能测试报告
summary: TiProxy 的性能测试报告、与 HAProxy 的性能对比。
---

# TiProxy 性能测试报告

本次报告测试了 TiProxy 在 OLTP 场景下的 Sysbench 性能表现，并和 [HAProxy](https://www.haproxy.org/) 的性能做了对比。

结果显示：

- TiProxy 的 QPS 上限受工作负载类型的影响。在 Sysbench 的基本工作负载、同等 CPU 使用率的情况下，TiProxy 的 QPS 比 HAProxy 低约 25%
- TiProxy 能承载的 TiDB server 实例数量根据工作负载类型而变化。在 Sysbench 的基本工作负载下，一台 TiProxy 能承载 5 至 12 台同机型的 TiDB server 实例
- 查询结果集的行数对 TiProxy 的 QPS 有显著影响，且影响程度与 HAProxy 相同
- TiProxy 的性能随 vCPU 的数量接近线性增长，因此增加 vCPU 的数量可以有效提高 QPS 上限
- 长连接的数量、短连接的创建频率对 TiProxy 的 QPS 影响很小
- TiProxy 的 CPU 使用率越高，开启[捕获流量](/tiproxy/tiproxy-traffic-replay.md)功能对 QPS 的影响越大。当 TiProxy 的 CPU 使用率约为 70% 时，开启流量捕获会导致平均 QPS 下降约 3%，最低 QPS 下降约 7%，后者的下降是由压缩流量文件导致的 QPS 周期性下降。

## 测试环境

### 硬件配置

| 服务类型 | 实例机型 | CPU 型号 | 实例数 |
| --- | --- | --- | --- |
| TiProxy | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |
| HAProxy | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |
| PD | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 3 |
| TiDB | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8 |
| TiKV | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8 |
| Sysbench | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |

### 软件版本

| 服务类型 | 软件版本 |
| --- | --- |
| TiProxy | v1.0.0 |
| HAProxy | 2.9.0 |
| PD | v8.0.0 |
| TiDB | v8.0.0 |
| TiKV | v8.0.0 |
| Sysbench | 1.0.17 |

### 参数配置

#### TiProxy 参数配置

本次测试中，客户端与 TiProxy 之间、TiProxy 与 TiDB server 之间均未开启 TLS 连接。

```yaml
proxy.conn-buffer-size: 131072
```

#### HAProxy 配置 - haproxy.cfg 文件

```yaml
global                                      # 全局配置。
    log         127.0.0.1 local2            # 定义全局的 syslog 服务器，最多可以定义两个。
    pidfile     /var/run/haproxy.pid        # 将 HAProxy 进程的 PID 写入 pidfile。
    maxconn     4096                        # 单个 HAProxy 进程可接受的最大并发连接数，等价于命令行参数 "-n"。
    nbthread    4                           # 最大线程数。线程数的上限与 CPU 数量相同。
    user        haproxy                     # 同 UID 参数。
    group       haproxy                     # 同 GID 参数，建议使用专用用户组。
    daemon                                  # 让 HAProxy 以守护进程的方式工作于后台，等同于命令行参数 “-D” 的功能。当然，也可以在命令行中用 “-db” 参数将其禁用。
    stats socket /var/lib/haproxy/stats     # 统计信息保存位置。

defaults                                    # 默认配置。
    log global                              # 日志继承全局配置段的设置。
    retries 2                               # 向上游服务器尝试连接的最大次数，超过此值便认为后端服务器不可用。
    timeout connect  2s                     # HAProxy 与后端服务器连接超时时间。如果在同一个局域网内，可设置成较短的时间。
    timeout client 30000s                   # 客户端与 HAProxy 连接后，数据传输完毕，即非活动连接的超时时间。
    timeout server 30000s                   # 服务器端非活动连接的超时时间。

listen tidb-cluster                         # 配置 database 负载均衡。
    bind 0.0.0.0:3390                       # 浮动 IP 和 监听端口。
    mode tcp                                # HAProxy 要使用第 4 层的传输层。
    balance leastconn                       # 连接数最少的服务器优先接收连接。`leastconn` 建议用于长会话服务，例如 LDAP、SQL、TSE 等，而不是短会话协议，如 HTTP。该算法是动态的，对于启动慢的服务器，服务器权重会在运行中作调整。
    server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # 检测 4000 端口，检测频率为每 2000 毫秒一次。如果 2 次检测为成功，则认为服务器可用；如果 3 次检测为失败，则认为服务器不可用。
    server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
    server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## 基本工作负载测试

### 测试方案

该测试的目的是对比 point select、read only、write only、read write 四种工作负载下 TiProxy 与 HAProxy 的 QPS。每种工作负载分别使用不同的并发度测试 TiProxy 和 HAProxy，对比 QPS。

执行的测试命令：

```bash
sysbench $testname \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Point Select 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 20  | 41273 | 0.48      | 0.64        | 190%            | 900%          |
| 50  | 100255 | 0.50      | 0.62        | 330%            | 1900%         |
| 100 | 137688 | 0.73      | 1.01        | 400%            | 2600%         |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 20 | 44833 | 0.45      | 0.61        | 140%            | 1000% |
| 50 | 103631 | 0.48      | 0.61        | 270%            | 2100% |
| 100 | 163069 | 0.61      | 0.77        | 360%            | 3100% |

### Read Only 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 72076 | 11.09     | 12.75       | 290% | 2500% |
| 100 | 109704 | 14.58     | 17.63       | 370% | 3800% |
| 200 | 117519 | 27.21     | 32.53       | 400% | 4100% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 75760 | 10.56     | 12.08       | 250% | 2600% |
| 100 | 121730 | 13.14     | 15.83       | 350% | 4200% |
| 200 | 131712 | 24.27     | 30.26       | 370% | 4500% |

### Write Only 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 100 | 81957 | 7.32      | 10.27       | 290% | 3900% |
| 300 | 103040 | 17.45     | 31.37       | 330% | 4700% |
| 500 | 104869 | 28.59     | 52.89       | 340% | 4800% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 100 | 81708 | 7.34      | 10.65       | 240% | 3700% |
| 300 | 106008 | 16.95     | 31.37       | 320% | 4800% |
| 500 | 122369 | 24.45     | 47.47       | 350% | 5300% |

### Read Write 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 58571 | 17.07     | 19.65       | 250% | 2600% |
| 100 | 88432 | 22.60     | 29.19       | 330% | 3900% |
| 200 | 108758 | 36.73     | 51.94       | 380% | 4800% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 61226 | 16.33     | 19.65       | 190% | 2800% |
| 100 | 96569 | 20.70     | 26.68       | 290% | 4100% |
| 200 | 120163 | 31.28     | 49.21       | 340% | 5200% |

## 结果集测试

### 测试方案

该测试的目的是对比不同结果集行数对性能的影响。该测试固定使用 100 并发数，分别使用行数为 10、100、1000、10000 的结果集，对比 TiProxy 和 HAProxy 的 QPS。

执行的测试命令：

```bash
sysbench oltp_read_only \
    --threads=100 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    --skip_trx=true \
    --point_selects=0 \
    --sum_ranges=0 \
    --order_ranges=0 \
    --distinct_ranges=0 \
    --simple_ranges=1 \
    --range_size=$range_size
    run --tables=32 --table-size=1000000
```

### 测试结果

TiProxy 测试结果：

| 返回行数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 | 入站流量 (MiB/s) | 出站流量 (MiB/s) |
|------| --- |-----------|-------------|-----------------|---------------|--------------|--------------|
| 10   | 80157 | 1.25      | 1.61        | 340%            | 2600%         | 140          | 140          |
| 100  | 55936 | 1.79      | 2.43        | 370%            | 2800%         | 820          | 820          |
| 1000 | 10313 | 9.69     | 13.70       | 310%            | 1500%         | 1370         | 1370         |
| 10000 | 1064 | 93.88    | 142.39      | 250%            | 600%          | 1430         | 1430         |

HAProxy 测试结果：

| 返回行数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 | 入站流量 (MiB/s) | 出站流量 (MiB/s) |
|------| --- |-----------|-------------|-----------------|---------------|--------------|--------------|
| 10 | 94376 | 1.06 | 1.30 | 250%            | 4000% | 150          | 150          |
| 100 | 70129 | 1.42 | 1.76 | 270%            | 3300% | 890          | 890          |
| 1000 | 9501 | 11.18 | 14.73 | 240%            | 1500% | 1180         | 1180         |
| 10000 | 955 | 104.61 | 320.17 | 180%            | 1200% | 1200         | 1200         |

## 扩展性测试

### 测试方案

该测试的目的是验证 TiProxy 的性能与规格成正比，以确保升级 TiProxy 的规格能提升其 QPS 上限。该测试分别使用不同 vCPU 数量的 TiProxy 实例和并发数，对比 QPS。

执行的测试命令：

```bash
sysbench oltp_point_select \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### 测试结果

| 核数  | 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----|-----| --- |-----------|-------------|-----------------|---------------|
| 2   | 40  | 58508 | 0.68      | 0.97        | 190%            | 1200%         |
| 4   | 80  | 104890 | 0.76      | 1.16        | 390%            | 2000%         |
| 6   | 120 | 155520 | 0.77      | 1.14        | 590%            | 2900%         |
| 8   | 160 | 202134 | 0.79      | 1.18        | 800%            | 3900%         |

## 长连接测试

### 测试方案

该测试的目的是验证客户端使用长连接时，大量空闲连接对 QPS 的影响很小。该测试分别创建 5000、10000、15000 个空闲的长连接，然后执行 `sysbench`。

测试中 TiProxy 的 `conn-buffer-size` 配置保持默认值：

```yaml
proxy.conn-buffer-size: 32768
```

执行的测试命令：

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### 测试结果

| 连接数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiProxy 内存使用 (MB) | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|---------------|
| 5000 | 96620 | 0.52     | 0.64       | 330% | 920 | 1800% |
| 10000 | 96143 | 0.52     | 0.65       | 330% | 1710 | 1800% |
| 15000 | 96048 | 0.52     | 0.65       | 330% | 2570 | 1900% |

## 短连接测试

### 测试方案

该测试的目的是验证在客户端使用短连接时，频繁创建和销毁连接对 QPS 的影响很小。该测试在执行 `sysbench` 的同时，启动另一个客户端程序，分别每秒创建并断开 100、200、300 个短连接。

执行的测试命令：

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### 测试结果

| 每秒新建连接数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 100 | 95597 | 0.52     | 0.65       | 330% | 1800% |
| 200 | 94692 | 0.53     | 0.67       | 330% | 1800% |
| 300 | 94102 | 0.53     | 0.68       | 330% | 1900% |

## 捕获流量测试

### 测试方案

该测试的目的是测试[捕获流量](/tiproxy/tiproxy-traffic-replay.md)对 TiProxy 性能的影响。该测试使用 TiProxy v1.3.0 版本，在执行 `sysbench` 之前分别关闭和开启流量捕获，同时调整并发度，以对比 QPS 和 TiProxy 的 CPU 使用率。由于周期性的压缩流量文件会引起 QPS 波动，本测试除了对比平均 QPS，也对比了最低 QPS。

执行的测试命令：

```bash
sysbench oltp_read_write \
    --threads=$threads \
    --time=1200 \
    --report-interval=5 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### 测试结果

| 并发数 | 捕获流量 | 平均 QPS | 最低 QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 |
| - |-----| --- | --- |-----------|-------------|-----------------|
| 20 | 关闭 | 27653 | 26999 | 14.46     | 16.12       | 140% |
| 20 | 启用 | 27519 | 26922 | 14.53     | 16.41       | 170% |
| 50 | 关闭 | 58014 | 56416 | 17.23     | 20.74       | 270% |
| 50 | 启用 | 56211 | 52236 | 17.79     | 21.89       | 280% |
| 100 | 关闭 | 85107 | 84369 | 23.48     | 30.26       | 370% |
| 100 | 启用 | 79819 | 69503 | 25.04     | 31.94       | 380% |
