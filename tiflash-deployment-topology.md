---
title:TiFlash部署拓扑
summary: 介绍 TiFlash 部署 TiDB 集群的拓扑结构。
category: how-to
---

# TiFlash 部署拓扑

本文介绍 TiFlash 部署拓扑以及部署 TiFlash 的注意事项。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口 <br>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | 默认端口 <br> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口 <br> 全局目录配置 |
| TiFlash | 1 | 32 VCore 64 GB 2TB (nvme ssd) * 1  | 10.0.1.10 | 默认端口 <br> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.10 | 默认端口 <br> 全局目录配置 |

## 关键参数配置

- [部署 TiFlash](/tiflash/deploy-tiflash.md) 需要在 topology.yaml 配置文件中将 `replication.enable-placement-rules` 设置为 `true`，以开启 PD 的 [Placement Rules](/configure-placement-rules.md) 功能。

- tiflash_servers 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。

- TiFlash 具体的参数配置介绍可参考 [TiFlash 参数配置](#tiflash-参数)。

## 通过 TiUP 部署集群的配置文件模版 topology.yaml

### 部署目标

通过 `tidb` 用户管理集群，部署一套 TiFlash 单实例的 HTAP 集群，端口默认，部署目录为 `/tidb-deploy`，数据目录为 `/tidb-data`。

### 拓扑模版

[简单 TiFlash 部署模版](/simple-tiflash.yaml)
[复杂 TiFlash 部署模版](/complex-tiflash.yaml)

> **注意：**
>
> - 无需手动创建 tidb 用户，TiUP cluster 组件会在部署主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。