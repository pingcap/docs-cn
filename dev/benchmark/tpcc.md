---
title: TiDB TPC-C 性能对比测试报告 - v3.0 对比 v2.1
category: benchmark
---

# TiDB TPC-C 性能对比测试报告 - v3.0 对比 v2.1

## 测试目的

对比 TiDB 3.0 版本和 2.1 版本的 TPC-C 性能表现。

## 测试版本、时间、地点

TiDB 版本：v3.0.0 vs. v2.1.13

时间：2019 年 6 月

地点：北京

## 测试环境

IDC 机器：

| 类别 | 名称 |
| :-: | :-: |
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | 1.5TB SSD \* 2 |  

本文使用开源的 BenchmarkSQL 5.0 作为 TPC-C 测试工具并添加对 MySQL 协议支持， 可以通过以下命令下载测试程序:

```shell
git clone -b 5.0-mysql-support-opt https://github.com/pingcap/benchmarksql.git
```

## 测试方案

使用 BenchmarkSQL 向集群导入 **1000 warehouse** 的数据。通过 HAProxy 代理，分别以递增并发数向集群发送请求，单次并发测试时间 10 分钟。

### TiDB 版本信息

### v3.0.0

| 组件 | GitHash |
| :-: | :-: |
| TiDB | 46c38e15eba43346fb3001280c5034385171ee20 |
| TiKV | a467f410d235fa9c5b3c355e3b620f81d3ac0e0c |
| PD | 70aaa5eee830e21068f1ba2d4c9bae59153e5ca3 |

### v2.1.13

| 组件 | GitHash |
| :-: | :-: |
| TiDB | 6b5b1a6802f9b8f5a22d8aab24ac80729331e1bc |
| TiKV | b3cf3c8d642534ea6fa93d475a46da285cc6acbf |
| PD | 886362ebfb26ef0834935afc57bcee8a39c88e54 |

### TiDB 参数配置

```toml
[log]
level = "error"
[performance]
max-procs = 20
[prepared_plan_cache]
enabled = true
```

### TiKV 参数配置

```txt
[readpool.storage]
normal-concurrency = 8
[server]
grpc-concurrency = 8
[raftstore]
sync-log = false
[rocksdb.defaultcf]
block-cache-size = "60GB"
[rocksdb.writecf]
block-cache-size = "20GB"
```

### 集群拓扑

| 机器 IP | 部署实例 |
| :-: | :-: |
| 172.16.4.75 | 2\*TiDB 2\*TiKV 1\*pd |
| 172.16.4.76 | 2\*TiDB 2\*TiKV 1\*pd |
| 172.16.4.77 | 2\*TiDB 2\*TiKV 1\*pd |

## 测试结果

| 版本 | threads | tpmC |
| :-: | :-: | :-: |
| v3.0 | 128  | 37400.76 |
| v3.0 | 256  | 39931.79  |
| v3.0 | 512  | 40272.34 |
| v2.1 | 128  | 10641.71  |
| v2.1 | 256  | 10861.62 |
| v2.1 | 512  | 10965.39 |

![tpcc](/media/tpcc-2.1-3.0.png)

v3.0 比 v2.1 在 TPC-C 性能上，**提升了 400%**。
