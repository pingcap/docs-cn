---
title: TiCDC 部署拓扑
summary: 介绍 TiCDC 部署 TiDB 集群的拓扑结构。
category: how-to
aliases: ['/docs-cn/dev/reference/tools/ticdc/deploy/','/docs-cn/dev/ticdc/deploy-ticdc/']
---

> **注意：**
>
> TiCDC 目前为实验特性，不建议在生产环境中使用。

# TiCDC 部署拓扑

本文介绍 TiCDC 部署的拓扑，以及如何在最小拓扑的基础上同时部署 TiCDC。TiCDC 是 4.0 版本开始支持的 TiDB 增量数据同步工具，支持多种下游 (TiDB/MySQL/MQ)。相比于 TiDB Binlog，TiCDC 有延迟更低、天然高可用等优点。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/> 全局目录配置 |
| CDC | 3 | 8 VCore 16GB * 1 | 10.0.1.11 <br/> 10.0.1.12 <br/> 10.0.1.13 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.11 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

[简单 TiCDC 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-cdc.yaml)

[详细 TiCDC 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-cdc.yaml)

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户家目录下。
