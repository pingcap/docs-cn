---
title: TiCDC 部署拓扑
summary: 介绍 TiCDC 部署 TiDB 集群的拓扑结构。
aliases: ['/docs-cn/dev/ticdc-deployment-topology/','/docs-cn/dev/reference/tools/ticdc/deploy/','/docs-cn/dev/ticdc/deploy-ticdc/']
---

# TiCDC 部署拓扑

> **注意：**
>
> TiCDC 从 v4.0.6 起成为正式功能，可用于生产环境。

本文介绍 [TiCDC](/ticdc/ticdc-overview.md) 部署的拓扑，以及如何在最小拓扑的基础上同时部署 TiCDC。TiCDC 是 4.0 版本开始支持的 TiDB 增量数据同步工具，支持多种下游（TiDB、MySQL、Kafka、MQ、存储服务等），有延迟低、天然高可用等优点。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/> 全局目录配置 |
| CDC | 3 | 8 VCore 16GB * 1 | 10.0.1.11 <br/> 10.0.1.12 <br/> 10.0.1.13 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.11 | 默认端口 <br/> 全局目录配置 |

### 拓扑模版

<details>
<summary>简单 TiCDC 配置模板</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3

tikv_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9

cdc_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9

monitoring_servers:
  - host: 10.0.1.10

grafana_servers:
  - host: 10.0.1.10

alertmanager_servers:
  - host: 10.0.1.10
```

</details>

<details>
<summary>详细 TiCDC 配置模板</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

# # Monitored variables are applied to all the machines.
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  # deploy_dir: "/tidb-deploy/monitored-9100"
  # data_dir: "/tidb-data/monitored-9100"
  # log_dir: "/tidb-deploy/monitored-9100/log"

# # Server configs are used to specify the runtime configuration of TiDB components.
# # All configuration items can be found in TiDB docs:
# # - TiDB: https://docs.pingcap.com/zh/tidb/stable/tidb-configuration-file
# # - TiKV: https://docs.pingcap.com/zh/tidb/stable/tikv-configuration-file
# # - PD: https://docs.pingcap.com/zh/tidb/stable/pd-configuration-file
# # All configuration items use points to represent the hierarchy, e.g:
# #   readpool.storage.use-unified-pool
# #
# # You can overwrite this configuration via the instance-level `config` field.

server_configs:
  tidb:
    log.slow-threshold: 300
  tikv:
    # server.grpc-concurrency: 4
    # raftstore.apply-pool-size: 2
    # raftstore.store-pool-size: 2
    # rocksdb.max-sub-compactions: 1
    # storage.block-cache.capacity: "16GB"
    # readpool.unified.max-thread-count: 12
    readpool.storage.use-unified-pool: false
    readpool.coprocessor.use-unified-pool: true
  pd:
    schedule.leader-schedule-limit: 4
    schedule.region-schedule-limit: 2048
    schedule.replica-schedule-limit: 64
  cdc:
    # capture-session-ttl: 10
    # sorter.sort-dir: "/tmp/cdc_sort"
    # gc-ttl: 86400

pd_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # name: "pd-1"
    # client_port: 2379
    # peer_port: 2380
    # deploy_dir: "/tidb-deploy/pd-2379"
    # data_dir: "/tidb-data/pd-2379"
    # log_dir: "/tidb-deploy/pd-2379/log"
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.pd` values.
    # config:
    #   schedule.max-merge-region-size: 20
    #   schedule.max-merge-region-keys: 200000
  - host: 10.0.1.5
  - host: 10.0.1.6

tidb_servers:
  - host: 10.0.1.1
    # ssh_port: 22
    # port: 4000
    # status_port: 10080
    # deploy_dir: "/tidb-deploy/tidb-4000"
    # log_dir: "/tidb-deploy/tidb-4000/log"
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.tidb` values.
    # config:
    #   log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.2
  - host: 10.0.1.3

tikv_servers:
  - host: 10.0.1.7
    # ssh_port: 22
    # port: 20160
    # status_port: 20180
    # deploy_dir: "/tidb-deploy/tikv-20160"
    # data_dir: "/tidb-data/tikv-20160"
    # log_dir: "/tidb-deploy/tikv-20160/log"
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.tikv` values.
    # config:
    #   server.grpc-concurrency: 4
    #   server.labels: { zone: "zone1", dc: "dc1", host: "host1" }

  - host: 10.0.1.8
  - host: 10.0.1.9

cdc_servers:
  - host: 10.0.1.1
    port: 8300
    deploy_dir: "/tidb-deploy/cdc-8300"
    data_dir: "/tidb-data/cdc-8300"
    log_dir: "/tidb-deploy/cdc-8300/log"
    # gc-ttl: 86400
    # ticdc_cluster_id: "cluster1"
  - host: 10.0.1.2
    port: 8300
    deploy_dir: "/tidb-deploy/cdc-8300"
    data_dir: "/tidb-data/cdc-8300"
    log_dir: "/tidb-deploy/cdc-8300/log"
    # gc-ttl: 86400
    # ticdc_cluster_id: "cluster1"
  - host: 10.0.1.3
    port: 8300
    deploy_dir: "/tidb-deploy/cdc-8300"
    data_dir: "/tidb-data/cdc-8300"
    log_dir: "/tidb-deploy/cdc-8300/log"
    # gc-ttl: 86400
    # ticdc_cluster_id: "cluster2"

monitoring_servers:
  - host: 10.0.1.10
    # ssh_port: 22
    # port: 9090
    # deploy_dir: "/tidb-deploy/prometheus-8249"
    # data_dir: "/tidb-data/prometheus-8249"
    # log_dir: "/tidb-deploy/prometheus-8249/log"

grafana_servers:
  - host: 10.0.1.10
    # port: 3000
    # deploy_dir: /tidb-deploy/grafana-3000

alertmanager_servers:
  - host: 10.0.1.10
    # ssh_port: 22
    # web_port: 9093
    # cluster_port: 9094
    # deploy_dir: "/tidb-deploy/alertmanager-9093"
    # data_dir: "/tidb-data/alertmanager-9093"
    # log_dir: "/tidb-deploy/alertmanager-9093/log"
```

</details>

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md#cdc_servers)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
