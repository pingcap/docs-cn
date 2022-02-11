---
title: TiFlash 部署拓扑
summary: 了解在部署最小拓扑集群的基础上，部署 TiFlash 的拓扑结构。
---

# TiFlash 部署拓扑

本文介绍在部署最小拓扑集群的基础上，部署 [TiFlash](/tiflash/tiflash-overview.md) 的拓扑结构。TiFlash 是列式的存储引擎，已经成为集群拓扑的标配，适合 Real-Time HTAP 业务。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/> 全局目录配置 |
| TiFlash | 1 | 32 VCore 64 GB 2TB (nvme ssd) * 1  | 10.0.1.10 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.10 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

- [简单 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tiflash.yaml)

- [详细 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tiflash.yaml)

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md#tiflash_servers)。

### 关键参数介绍

- 需要将配置模板中 `replication.enable-placement-rules` 设置为 `true`，以开启 PD 的 [Placement Rules](/configure-placement-rules.md) 功能。

- `tiflash_servers` 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。

- TiFlash 具体的参数配置介绍可参考 [TiFlash 参数配置](/tiflash/tiflash-configuration.md)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户家目录下。