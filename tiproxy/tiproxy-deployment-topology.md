---
title: TiProxy 部署拓扑
summary: 了解在部署最小拓扑集群的基础上，部署 TiProxy 的拓扑结构。
---

# TiProxy 部署拓扑

本文介绍在部署最小拓扑集群的基础上，部署 [TiProxy](/tiproxy/tiproxy-overview.md) 的拓扑结构。

TiProxy 是 TiDB 的 L7 代理，可以平衡连接并迁移会话。

## 拓扑信息

| 实例 | 个数 | 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 3 | 16 VCore 32GB * 3 | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 3 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 3 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/>  全局目录配置 |
| TiProxy | 1 | 4 VCore 8 GB * 1  | 10.0.1.11 | 默认端口 <br/>  全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.13 | 默认端口 <br/>  全局目录配置 |

### 拓扑模版

<details>
<summary>简单 TiProxy 配置模版</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

pd_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3

tidb_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6

tikv_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9

tiproxy_servers:
  - host: 10.0.1.11

monitoring_servers:
  - host: 10.0.1.13

grafana_servers:
  - host: 10.0.1.13

alertmanager_servers:
  - host: 10.0.1.13
```

</details>

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

### 关键参数介绍

- `tiproxy_servers` 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。
- TiProxy 具体的参数配置介绍可参考 [TiProxy 参数配置](/tiproxy/tiproxy-configuration.md)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
