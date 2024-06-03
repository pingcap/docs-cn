---
title: PD 微服务部署拓扑
summary: 了解在部署最小拓扑集群的基础上，部署 PD 微服务的拓扑结构。
---

# PD 微服务部署拓扑

本文介绍在部署最小拓扑集群的基础上，部署 [PD 微服务](/pd-microservices.md) 的拓扑结构。

## 拓扑信息

| 实例                 | 个数 | 物理机配置                        | IP                                        | 配置                        |
| :------------------- | :--- | :-------------------------------- | :---------------------------------------- | :-------------------------- |
| TiDB                 | 2    | 16 VCore 32GB \* 1                | 10.0.1.1 <br/> 10.0.1.2                   | 默认端口 <br/> 全局目录配置 |
| PD                   | 3    | 4 VCore 8GB \* 1                  | 10.0.1.3 <br/> 10.0.1.4 <br/> 10.0.1.5    | 默认端口 <br/> 全局目录配置 |
| TSO                  | 2    | 4 VCore 8GB \* 1                  | 10.0.1.6 <br/> 10.0.1.7                   | 默认端口 <br/> 全局目录配置 |
| Scheduling           | 2    | 4 VCore 8GB \* 1                  | 10.0.1.8 <br/> 10.0.1.9                   | 默认端口 <br/> 全局目录配置 |
| TiKV                 | 3    | 16 VCore 32GB 2TB (nvme ssd) \* 1 | 10.0.1.10 <br/> 10.0.1.11 <br/> 10.0.1.12 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1    | 4 VCore 8GB \* 1 500GB (ssd)      | 10.0.1.13                                 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

<details>
<summary>简单 PD 微服务配置模版</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
  listen_host: 0.0.0.0
  arch: "amd64"
  pd_mode: "ms"

monitored:
  # # The communication port for reporting system information of each node in the TiDB cluster.
  node_exporter_port: 9200
  # # Blackbox_exporter communication port, used for TiDB cluster port monitoring.
  blackbox_exporter_port: 9215
  # # Storage directory for deployment files, startup scripts, and configuration files of monitoring components.
  # deploy_dir: "/tidb-deploy/monitored-9100"
  # # Data storage directory of monitoring components.
  # data_dir: "/tidb-data/monitored-9100"
  # # Log storage directory of the monitoring component.
  # log_dir: "/tidb-deploy/monitored-9100/log"

# # Server configs are used to specify the configuration of PD Servers.
pd_servers:
  # # The ip address of the PD Server.
  - host: 10.0.1.3
  - host: 10.0.1.4
  - host: 10.0.1.5

# # Server configs are used to specify the configuration of TiDB Servers.
tidb_servers:
  # # The ip address of the TiDB Server.
  - host: 10.0.1.1
  - host: 10.0.1.2

# # Server configs are used to specify the configuration of TiKV Servers.
tikv_servers:
  # # The ip address of the TiKV Server.
  - host: 10.0.1.10
  - host: 10.0.1.11
  - host: 10.0.1.12

tso_servers:
  # # The ip address of the TSO Server.
  - host: 10.0.1.6
  - host: 10.0.1.7

scheduling_servers:
  # # The ip address of the Scheduling Server.
  - host: 10.0.1.8
  - host: 10.0.1.9

# # Server configs are used to specify the configuration of Prometheus Server.
monitoring_servers:
  # # The ip address of the Monitoring Server.
  - host: 10.0.1.13

# # Server configs are used to specify the configuration of Grafana Servers.
grafana_servers:
  # # The ip address of the Grafana Server.
  - host: 10.0.1.13
```

</details>

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

### 关键参数介绍

- `tso_servers` 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。
- TSO 具体的参数配置介绍可参考 [TSO 参数配置](/tso-configuration-file.md)。
- `scheduling_servers` 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。
- Scheduling 具体的参数配置介绍可参考 [Scheduling 参数配置](/scheduling-configuration-file.md)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
