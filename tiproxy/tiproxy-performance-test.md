---
title: TiProxy Performance Test Report
summary: Learn the performance of TiProxy and the comparison with HAProxy.
---

# TiProxy Performance Test Report

This report tests the performance of TiProxy in the OLTP scenario of Sysbench and compares it with [HAProxy](https://www.haproxy.org/).

The results are as follows:

- The QPS upper limit of TiProxy is affected by the type of workload. Under the basic workloads of Sysbench and the same CPU usage, the QPS of TiProxy is about 20% to 40% lower than that of HAProxy.
- The number of TiDB server instances that TiProxy can hold varies according to the type of workload. Under the basic workloads of Sysbench, a TiProxy can hold 4 to 10 TiDB server instances of the same model.
- The performance of TiProxy is more affected by the number of vCPUs, compared to HAProxy. When the returned data is 10,000 rows and the CPU usage is the same, the QPS of TiProxy is about 30% lower than that of HAProxy.
- The performance of TiProxy increases almost linearly with the number of vCPUs. Therefore, increasing the number of vCPUs can effectively improve the QPS upper limit.

## Test environment

### Hardware configuration

| Service | Machine Type | CPU Architecture | Instance Count |
| --- | --- | --- | --- |
| TiProxy | 4C8G | AMD64 | 1 |
| HAProxy | 4C8G | AMD64 | 1 |
| PD | 4C8G | AMD64 | 3 |
| TiDB | 8C16G | AMD64 | 8 |
| TiKV | 8C16G | AMD64 | 8 |
| Sysbench | 8C16G | AMD64 | 1 |

### Software

| Service | Software version |
| --- | --- |
| TiProxy | v0.2.0 |
| HAProxy | 2.9.0 |
| PD | v7.6.0 |
| TiDB | v7.6.0 |
| TiKV | v7.6.0 |
| Sysbench | 1.0.17 |

### Configuration

#### TiProxy configuration

In the test, TLS is not enabled between the client and TiProxy, or between TiProxy and TiDB server.

```yaml
proxy.conn-buffer-size: 131072
```

#### HAProxy configuration - `haproxy.cfg` file

```yaml
global                                      # Global configuration.
    log         127.0.0.1 local2            # Specifies the global syslog server. You can define up to two.
    pidfile     /var/run/haproxy.pid        # Write the PID of the HAProxy process to pidfile.
    maxconn     4096                        # The maximum number of concurrent connections that a single HAProxy process can accept, equivalent to the command line parameter "-n".
    nbthread    4                           # The maximum number of threads. The upper limit of the number of threads is the same as the number of CPUs.
    user        haproxy                     # Same as UID parameter.
    group       haproxy                     # Same as GID parameter. A dedicated user group is recommended.
    daemon                                  # Run HAProxy as a daemon in the background, which is equivalent to the command line parameter "-D". You can also disable it with the "-db" parameter on the command line.
    stats socket /var/lib/haproxy/stats     # The location where the statistics are saved.

defaults                                    # Default configuration.
    log global                              # Inherit the settings of the global configuration section.
    retries 2                               # The maximum number of times to try to connect to the upstream server. If the number of retries exceeds this value, the backend server is considered unavailable.
    timeout connect  2s                     # The timeout period for HAProxy to connect to the backend server. If the server is located on the same LAN as HAProxy, set it to a shorter time.
    timeout client 30000s                   # The timeout period for the client to be inactive after the data transmission is completed.
    timeout server 30000s                   # The timeout period for the server to be inactive.

listen tidb-cluster                         # Configure database load balancing.
    bind 0.0.0.0:3390                       # Floating IP address and listening port.
    mode tcp                                # HAProxy uses layer 4, the transport layer.
    balance leastconn                      # The server with the least number of connections receives the connection first. `leastconn` is recommended for long session services, such as LDAP, SQL, and TSE, rather than short session protocols, such as HTTP. This algorithm is dynamic, and the server weight is adjusted during operation for slow-start servers.
    server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3      # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
    server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
    server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## Basic workload test

### Test plan

This test aims to compare the QPS of TiProxy and HAProxy under four types of workloads: point select, read only, write only, and read write. Each type of workload is tested with different concurrency to compare the QPS of TiProxy and HAProxy.

The following command is used to perform the test:

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

### Point Select

TiProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 20 | 43935 | 0.45 | 0.63 | 210% | 900% |
| 50 | 87870 | 0.57 | 0.77 | 350% | 1700% |
| 100 | 91611 | 1.09 | 1.79 | 400% | 1800% |

HAProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 20 | 43629 | 0.46 | 0.63 | 130% | 900% |
| 50 | 102934 | 0.49 | 0.61 | 320% | 2000% |
| 100 | 157880 | 0.63 | 0.81 | 400% | 3000% |

### Read Only

TiProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 50 | 71816 | 11.14 | 12.98 | 340% | 2500% |
| 100 | 79299 | 20.17 | 23.95 | 400% | 2800% |
| 200 | 83371 | 38.37 | 46.63 | 400% | 2900% |

HAProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 50 | 74945 | 10.67 | 12.08 | 250% | 2500% |
| 100 | 118526 | 13.49 | 18.28 | 350% | 4000% |
| 200 | 131102 | 24.39 | 34.33 | 390% | 4300% |

### Write Only

TiProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 100 | 67762 | 8.85 | 15.27 | 310% | 3200% |
| 300 | 81113 | 22.18 | 38.25 | 390% | 3900% |
| 500 | 79260 | 37.83 | 56.84 | 400% | 3800% |

HAProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 100 | 74501 | 8.05 | 12.30 | 220% | 3500% |
| 300 | 97942 | 18.36 | 31.94 | 280% | 4300% |
| 500 | 105352 | 28.44 | 49.21 | 300% | 4500% |

### Read Write

TiProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 50 | 60170 | 16.62 | 18.95 | 280% | 2700% |
| 100 | 81691 | 24.48 | 31.37 | 340% | 3600% |
| 200 | 88755 | 45.05 | 54.83 | 400% | 4000% |

HAProxy test results:

| Threads | QPS | Avg latency(ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- |
| 50 | 58151 | 17.19 | 20.37 | 240% | 2600% |
| 100 | 94123 | 21.24 | 26.68 | 370% | 4100% |
| 200 | 107423 | 37.21 | 45.79 | 400% | 4700% |

## Result set test

### Test plan

This test aims to compare the performance of TiProxy and HAProxy under different result set row numbers. This test uses 100 concurrency, and compares the QPS of TiProxy and HAProxy with result set row numbers of 10, 100, 1000, and 10000.

The following command is used to perform the test:

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

### Test results

TiProxy test results:

| Range Size | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage | Inbound Network (MiB/s) | Outbound Network (MiB/s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 92100 | 1.09 | 1.34 | 330% | 3700% | 150 | 150 |
| 100 | 57931 | 1.73 | 2.30 | 370% | 2800% | 840 | 840 |
| 1000 | 8249 | 12.12 | 18.95 | 250% | 1300% | 1140 | 1140 |
| 10000 | 826 | 120.77 | 363.18 | 230% | 600% | 1140 | 1140 |

HAProxy test results:

| Range Size | QPS | Avg latency(ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU Usage | Inbound Network (MiB/s) | Outbound Network (MiB/s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | 93202 | 1.07 | 1.30 | 330% | 3800% | 145 | 145 |
| 100 | 64348 | 1.55 | 1.86 | 350% | 3100% | 830 | 830 |
| 1000 | 8944 | 11.18 | 14.73 | 240% | 1400% | 1100 | 1100 |
| 10000 | 908 | 109.96 | 139.85 | 180% | 600% | 1130 | 1130 |

## Scalability test

### Test plan

This test aims to verify that the performance of TiProxy is proportional to its specifications, to ensure that upgrading the specifications of TiProxy can improve its QPS upper limit. This test uses TiProxy instances with different vCPU numbers and concurrency to compare the QPS.

The following command is used to perform the test:

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

### Test results

| vCPU | Threads | QPS | Avg latency(ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU Usage |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 40 | 58508 | 0.68 | 0.97 | 190% | 1200% |
| 4 | 80 | 104890 | 0.76 | 1.16 | 390% | 2000% |
| 6 | 120 | 155520 | 0.77 | 1.14 | 590% | 2900% |
| 8 | 160 | 202134 | 0.79 | 1.18 | 800% | 3900% |
