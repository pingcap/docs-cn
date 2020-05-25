---
title: TiDB-binlog 部署拓扑
summary: 介绍 TiDB-binlog 部署 TiDB 集群的拓扑结构。
category: how-to
---

# TiDB-binlog 部署拓扑

本文介绍 TiDB-binlog 部署拓扑以及重要参数

## 拓扑信息

| 实例 |个数| 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
|TiDB | 3 | 16 VCore 32 GB | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口配置；<br>开启 enable_binlog； <br> 开启 ignore-error |
| PD | 3 | 4 VCore 8 GB | 10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | 默认端口配置 |
| TiKV | 3 | 16 VCore 32 GB | 10.0.1.7 <br> 10.0.1.8 <br> 10.0.1.9 | 默认端口配置 |
| Pump| 3 |8 VCore 16GB |10.0.1.1 <br> 10.0.1.7 <br> 10.0.1.8 | 默认端口配置； <br> 设置 GC 时间 7 天 |
| Drainer | 1 | 8 VCore 16GB | 10.0.1.12 | 默认端口配置；<br> 设置默认初始化 commitTS -1 为最近的时间戳 <br> 配置下游目标 TiDB 10.0.1.12:4000 |

## 通过 TiUP 部署集群的配置文件模版 topology.yaml

### 部署目标

设置默认部署目录 `/tidb-deploy` 和数据目录 `/tidb-data`，通过 TiDB Binlog 同步到下游机器 10.0.1.12:4000。

### 拓扑模版

[简单 TiDB-binlog 配置模板](/simple-tidb-binlog.yaml)

[详细 TiDB-binlog 配置模板](/complex-tidb-binlog.yaml)

### 关键参数介绍

- `binlog.enable: true`

    开启 binlog 服务，默认为 false。

- `binlog.ignore-error: true`

    高可用场景建议开启，如果设置为 true，发生错误时，TiDB 会停止写入 binlog，并且在监控项 tidb_server_critical_error_total 上计数加 1；如果设置为 false，一旦写入 binlog 失败，会停止整个 TiDB 的服务。

> **注意：**
>
> - 编辑配置文件模版时，如无需自定义端口或者目录，仅修改 IP 即可。 
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在部署主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
