---
title: TiProxy 性能测试报告
summary: TiProxy 的性能测试报告、与 HAProxy 的性能对比。
---

# TiProxy 性能测试报告

本次报告测试了 TiProxy 在 OLTP 场景下的 Sysbench 性能表现，并和 [HAProxy](https://www.haproxy.org/) 的性能做了对比。

结果显示：

- TiProxy 的 QPS 上限受工作负载类型的影响。在 Sysbench 的基本工作负载、同等 CPU 使用率的情况下，TiProxy 的 QPS 比 HAProxy 低约 20% 至 40%
- TiProxy 能承载的 TiDB server 实例数量根据工作负载类型而变化。在 Sysbench 的基本工作负载下，一台 TiProxy 能承载 4 至 10 台同机型的 TiDB server 实例
- TiProxy 的性能比 HAProxy 更受数据量的影响。在返回的数据量为 10000 行、同等 CPU 使用率的情况下，TiProxy 的 QPS 比 HAProxy 低约 30%
- TiProxy 的性能随 vCPU 的数量接近线性增长，因此增加 vCPU 的数量可以有效提高 QPS 上限

## 测试环境

### 硬件配置

| 服务类型 | 实例机型 | CPU 架构 | 实例数 |
| --- | --- | --- | --- |
| TiProxy | 4C8G | AMD64 | 1 |
| HAProxy | 4C8G | AMD64 | 1 |
| PD | 4C8G | AMD64 | 3 |
| TiDB | 8C16G | AMD64 | 8 |
| TiKV | 8C16G | AMD64 | 8 |
| Sysbench | 8C16G | AMD64 | 1 |

### 软件版本

| 服务类型 | 软件版本 |
| --- | --- |
| TiProxy | v0.2.0 |
| HAProxy | 2.9.0 |
| PD | v7.6.0 |
| TiDB | v7.6.0 |
| TiKV | v7.6.0 |
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
| 20  | 43935 | 0.45      | 0.63        | 210%            | 900%          |
| 50  | 87870 | 0.57      | 0.77        | 350%            | 1700%         |
| 100 | 91611 | 1.09      | 1.79        | 400%            | 1800%         |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 20 | 43629 | 0.46      | 0.63        | 130%            | 900% |
| 50 | 102934 | 0.49      | 0.61        | 320%            | 2000% |
| 100 | 157880 | 0.63      | 0.81        | 400%            | 3000% |

### Read Only 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 71816 | 11.14     | 12.98       | 340% | 2500% |
| 100 | 79299 | 20.17     | 23.95       | 400% | 2800% |
| 200 | 83371 | 38.37     | 46.63       | 400% | 2900% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 74945 | 10.67     | 12.08       | 250% | 2500% |
| 100 | 118526 | 13.49     | 18.28       | 350% | 4000% |
| 200 | 131102 | 24.39     | 34.33       | 390% | 4300% |

### Write Only 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 100 | 67762 | 8.85      | 15.27       | 310% | 3200% |
| 300 | 81113 | 22.18     | 38.25       | 390% | 3900% |
| 500 | 79260 | 37.83     | 56.84       | 400% | 3800% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 100 | 74501 | 8.05      | 12.30       | 220% | 3500% |
| 300 | 97942 | 18.36     | 31.94       | 280% | 4300% |
| 500 | 105352 | 28.44     | 49.21       | 300% | 4500% |

### Read Write 测试结果

TiProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | TiProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 60170 | 16.62     | 18.95       | 280% | 2700% |
| 100 | 81691 | 24.48     | 31.37       | 340% | 3600% |
| 200 | 88755 | 45.05     | 54.83       | 400% | 4000% |

HAProxy 测试结果：

| 并发数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 |
|-----| --- |-----------|-------------|-----------------|---------------|
| 50 | 58151 | 17.19     | 20.37       | 240% | 2600% |
| 100 | 94123 | 21.24     | 26.68       | 370% | 4100% |
| 200 | 107423 | 37.21     | 45.79       | 400% | 4700% |

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
| 10   | 92100 | 1.09      | 1.34        | 330%            | 3700%         | 150          | 150          |
| 100  | 57931 | 1.73      | 2.30        | 370%            | 2800%         | 840          | 840          |
| 1000 | 8249 | 12.12     | 18.95       | 250%            | 1300%         | 1140         | 1140         |
| 10000 | 826 | 120.77    | 363.18      | 230%            | 600%          | 1140         | 1140         |

HAProxy 测试结果：

| 返回行数 | QPS | 平均延迟 (ms) | P95 延迟 (ms) | HAProxy CPU 使用率 | TiDB CPU 总使用率 | 入站流量 (MiB/s) | 出站流量 (MiB/s) |
|------| --- |-----------|-------------|-----------------|---------------|--------------|--------------|
| 10 | 93202 | 1.07 | 1.30 | 330%            | 3800% | 145 | 145 |
| 100 | 64348 | 1.55 | 1.86 | 350%            | 3100% | 830 | 830 |
| 1000 | 8944 | 11.18 | 14.73 | 240%            | 1400% | 1100 | 1100 |
| 10000 | 908 | 109.96 | 139.85 | 180%            | 600% | 1130 | 1130 |

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
