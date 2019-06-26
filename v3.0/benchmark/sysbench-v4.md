---
title: TiDB Sysbench 性能对比测试报告 - v3.0 对比 v2.1
category: benchmark
aliases: ['/docs-cn/benchmark/sysbench-v4/']
---

# TiDB Sysbench 性能对比测试报告 - v3.0 对比 v2.1

## 测试目的

对比 TiDB 3.0 版本和 2.1 版本在 OLTP 场景下的性能。

## 测试版本、时间、地点

TiDB 版本：v3.0.0-rc.2 vs. v2.1.8

时间：2019 年 6 月

地点：北京

## 测试环境

测试在 AWS EC2 上进行，使用 CentOS-7.6.1810-Nitro (ami-028946f4cffc8b916) 镜像，各组件实例类型如下：

| 组件  |  实例类型  |
| :---: | :--------: |
|  PD   | r5d.xlarge |
| TiKV  | c5d.xlarge |
| TiDB  | c5d.xlarge |

Sysbench 版本：1.0.17

## 测试方案

使用 Sysbench 向集群导入 **16 张表，每张数据 1000 万**。起 3 个 sysbench 分别向 3 个 tidb 发压，请求并发数逐步增加，单次测试时间 5 分钟。

准备数据命令：
```sh
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    prepare --tables=16 --table-size=10000000
```

执行测试命令：
```sh
sysbench $testname \
    --threads=$threads \
    --time=300 \
    --report-interval=15 \
    --rand-type=uniform \
    --rand-seed=$RANDOM \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    run --tables=16 --table-size=10000000
```

### TiDB 版本信息

### v3.0.0-rc.2

| 组件  |                 GitHash                  |
| :---: | :--------------------------------------: |
| TiDB  | `e5dcc9b354dfa3b6b3a34cbd5949b2bec56b5bea` |
| TiKV  | `59a0f2b1dd45baea9bfdb4aab69b50fdbded08af` |
|  PD   | `c44ddf4abaaf54bcc99955b787bfe26b35fcfe8e` |

### v2.1.8

| 组件  |                 GitHash                  |
| :---: | :--------------------------------------: |
| TiDB  | `9a2d2da372947a50a02f9b9238a49f2db7ab9971` |
| TiKV  | `f58ed66cee9a10d605e56c878b1bf91c7b711a54` |
|  PD   | `1961ce08dcdead4198fa23a7ed079b135768c206` |

### TiDB 参数配置

2.1 和 3.0 中设置全局变量:
```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
```
3.0 还做了如下配置修改:
```toml
[prepared-plan-cache]
enabled = true
[tikv-client]
max-batch-wait-time = 1000000
```

### TiKV 参数配置

2.1 和 3.0 使用如下配置：
```toml
[readpool.storage]
normal-concurrency = 12
[server]
grpc-concurrency = 8
```
3.0 还做了如下配置：
```toml
[raftstore]
apply-pool-size = 4
store-pool-size = 4
```

### 集群拓扑

|                 机器 IP                  |  部署实例   |
| :--------------------------------------: | :---------: |
|               172.31.25.16               | 3\*Sysbench |
| 172.31.10.75, 172.31.3.211, 172.31.11.12 |     PD      |
| 172.31.8.167, 172.31.6.107, 172.31.14.99 |    TiKV     |
|  172.31.1.94, 172.31.15.193, 172.31.2.6  |    TiDB     |

## 测试结果

### Point Select 测试

**v2.1**

| threads |    qps    | 95% latency(ms) |
| ------- | --------: | --------------: |
| 150     | 137171.43 |            1.25 |
| 300     | 221861.81 |            2.00 |
| 600     | 266727.44 |            4.25 |
| 900     | 282689.31 |            6.32 |
| 1200    | 290614.52 |            8.43 |
| 1500    | 296218.09 |           10.27 |

**v3.0**

| threads |    qps    | 95% latency(ms) |
| ------- | --------: | --------------: |
| 150     | 158908.53 |            1.04 |
| 300     | 279335.92 |            1.30 |
| 600     | 422278.72 |            2.11 |
| 900     | 484304.54 |            3.07 |
| 1200    | 502705.22 |            4.10 |
| 1500    | 509098.83 |            5.18 |

![point select](/media/sysbench_v4_point_select.png)

### Update Non-Index 测试

**v2.1**

| threads |   qps    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 20755.37 |            8.90 |
| 300     | 27598.11 |           14.21 |
| 600     | 32072.08 |           33.12 |
| 900     | 32503.02 |           56.84 |
| 1200    | 32361.03 |           90.78 |
| 1500    | 32393.35 |          116.80 |


**v3.0**

| threads |   qps    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 24710.00 |            8.43 |
| 300     | 30347.88 |           13.95 |
| 600     | 38685.87 |           23.52 |
| 900     | 45567.08 |           30.81 |
| 1200    | 49982.75 |           39.65 |
| 1500    | 55717.09 |           51.02 |

![update non-index](/media/sysbench_v4_update_non_index.png)

### Update Index 测试

**v2.1**

| threads |   qps    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 13167.36 |           14.73 |
| 300     | 14670.16 |           31.94 |
| 600     | 15508.57 |           75.82 |
| 900     | 16290.25 |          116.80 |
| 1200    | 16060.43 |          164.45 |
| 1500    | 16219.86 |          204.11 |


**v3.0**

| threads |   qps    | 95% latency(ms) |
| ------- | -------: | --------------: |
| 150     | 15202.94 |           13.46 |
| 300     | 18874.35 |           23.52 |
| 600     | 23882.45 |           40.37 |
| 900     | 25602.60 |           63.32 |
| 1200    | 25340.77 |          104.84 |
| 1500    | 26294.65 |          155.80 |

![update index](/media/sysbench_v4_update_index.png)

### Read Write 测试

**v2.1**

| threads |   tps   |   qps    | 95% latency(ms) |
| ------- | ------: | -------: | --------------: |
| 150     | 3182.82 | 63656.28 |           57.87 |
| 300     | 3828.92 | 76578.28 |          101.13 |
| 600     | 4304.55 | 86091.07 |          183.21 |
| 900     | 4527.28 | 90545.70 |          272.27 |
| 1200    | 4726.97 | 94539.33 |          350.33 |
| 1500    | 4869.35 | 97386.99 |          427.07 |


**v3.0**

| threads |   tps   |    qps    | 95% latency(ms) |
| ------- | ------: | --------: | --------------: |
| 150     | 3703.97 |  74079.43 |           50.11 |
| 300     | 4890.35 |  97806.84 |           77.19 |
| 600     | 5644.47 | 112889.45 |          142.39 |
| 900     | 6095.21 | 121904.23 |          204.11 |
| 1200    | 6168.28 | 123365.48 |          267.41 |
| 1500    | 6429.45 | 128589.10 |          314.45 |

![read write](/media/sysbench_v4_read_write.png)