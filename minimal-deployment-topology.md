---
title: 最小拓扑架构
summary: 介绍 TiDB 集群的最小拓扑。
---

# 最小拓扑架构

本文档介绍 TiDB 集群最小部署的拓扑架构。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |2 | 16 VCore 32 GiB <br/> 100 GiB 用于存储| 10.0.1.1 <br/> 10.0.1.2 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8 GiB <br/> 100 GiB 用于存储|10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32 GiB <br/> 2 TiB (NVMe SSD) 用于存储 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8 GiB <br/> 500 GiB (SSD) 用于存储 | 10.0.1.10 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

[简单最小配置模板](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)

[详细最小配置模板](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
