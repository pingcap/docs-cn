---
title: TiDB Sysbench 性能对比测试报告 - v2.1 对比 v2.0
category: benchmark
aliases: ['/docs-cn/benchmark/sysbench-v3/']
---

# TiDB Sysbench 性能对比测试报告 - v2.1 对比 v2.0

## 测试目的

对比 TiDB 2.1 版本和 2.0 版本在 OLTP 场景下的性能。

## 测试版本、时间、地点

TiDB 版本：v2.1.0-rc.2 vs. v2.0.6

时间：2018 年 9 月

地点：北京

## 测试环境

IDC 机器：

| 类别 | 名称 |
| :-: | :-: |
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD \* 1 |

Sysbench 版本：1.1.0

## 测试方案

使用 Sysbench 向集群导入 **16 张表，每张数据 1000 万**。通过 HAProxy 代理，分别以递增并发数向集群发送请求，单次并发测试时间 5 分钟。

### TiDB 版本信息

### v2.1.0-rc.2

| 组件 | GitHash |
| :-: | :-: |
| TiDB | 08e56cd3bae166b2af3c2f52354fbc9818717f62 |
| TiKV | 57e684016dafb17dc8a6837d30224be66cbc7246 |
| PD | 6a7832d2d6e5b2923c79683183e63d030f954563 |

### v2.0.6

| 组件 | GitHash |
| :-: | :-: |
| TiDB | b13bc08462a584a085f377625a7bab0cc0351570 |
| TiKV | 57c83dc4ebc93d38d77dc8f7d66db224760766cc |
| PD | b64716707b7279a4ae822be767085ff17b5f3fea |

### TiDB 参数配置

两版本 TiDB 均使用**默认配置**。

### TiKV 参数配置

两版本 TiKV 均使用如下配置：

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
| 172.16.30.31 | 1\*Sysbench 1\*HAProxy |
| 172.16.30.32 | 1\*TiDB 1\*pd 1\*TiKV |
| 172.16.30.33 | 1\*TiDB 1\*TiKV |
| 172.16.30.34 | 1\*TiDB 1\*TiKV |

## 测试结果

### Point Select 测试

| 版本 | threads | qps | 95% latency(ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 111481.09 | 1.16  |
| v2.1 | 128  | 145102.62 | 2.52  |
| v2.1 | 256  | 161311.9  | 4.57  |
| v2.1 | 512  | 184991.19 | 7.56  |
| v2.1 | 1024 | 230282.74 | 10.84 |
| v2.0 | 64   | 75285.87  | 1.93  |
| v2.0 | 128  | 92141.79  | 3.68  |
| v2.0 | 256  | 107464.93 | 6.67  |
| v2.0 | 512  | 121350.61 | 11.65 |
| v2.0 | 1024 | 150036.31 | 17.32 |

![point select](/media/sysbench_v3_point_select.png)

v2.1 比 v2.0 在 Point Select 查询性能上，**提升了 50%**。

### Update Non-Index 测试

| 版本 | threads | qps | 95% latency(ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 18946.09 | 5.77   |
| v2.1 | 128  | 22022.82 | 12.08  |
| v2.1 | 256  | 24679.68 | 25.74  |
| v2.1 | 512  | 25107.1  | 51.94  |
| v2.1 | 1024 | 27144.92 | 106.75 |
| v2.0 | 64   | 16316.85 | 6.91   |
| v2.0 | 128  | 20944.6  | 11.45  |
| v2.0 | 256  | 24017.42 | 23.1   |
| v2.0 | 512  | 25994.33 | 46.63  |
| v2.0 | 1024 | 27917.52 | 92.42  |

![update non-index](/media/sysbench_v3_update_non_index.png)

v2.1 与 v2.0 在 Update Non-Index 写入性能上基本一致。

### Update Index 测试

| 版本 | threads | qps | 95% latency(ms) |
| :-: | :-: | :-: | :-: |
| v2.1 | 64   | 9934.49  | 12.08  |
| v2.1 | 128  | 10505.95 | 25.28  |
| v2.1 | 256  | 11007.7  | 55.82  |
| v2.1 | 512  | 11198.81 | 106.75 |
| v2.1 | 1024 | 11591.89 | 200.47 |
| v2.0 | 64   | 9754.68  | 11.65  |
| v2.0 | 128  | 10603.31 | 24.38  |
| v2.0 | 256  | 11011.71 | 50.11  |
| v2.0 | 512  | 11162.63 | 104.84 |
| v2.0 | 1024 | 12067.63 | 179.94 |

![update index](/media/sysbench_v3_update_index.png)

v2.1 与 v2.0 在 Update Index 写入性能上基本一致。
