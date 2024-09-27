---
title: TiDB Binlog 部署拓扑
summary: 介绍如何在部署最小拓扑集群的基础上，同时部署 TiDB Binlog。
aliases: ['/zh/tidb/dev/tidb-binlog-deployment-topology/','/docs-cn/dev/tidb-binlog-deployment-topology/']
---

# TiDB Binlog 部署拓扑

本文介绍在部署最小拓扑集群的基础上，同时部署 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)。TiDB Binlog 可提供准实时备份和同步功能。

> **警告：**
>
> 从 v7.5.0 开始，[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 的数据同步功能被废弃。从 v8.3.0 开始，TiDB Binlog 被完全废弃，并计划在未来版本中移除。如需进行增量数据同步，请使用 [TiCDC](/ticdc/ticdc-overview.md)。如需按时间点恢复 (point-in-time recovery, PITR)，请使用 [PITR](/br/br-pitr-guide.md)。

## 拓扑信息

| 实例 |个数| 物理机配置 | IP | 配置 |
| :-- | :-- | :-- | :-- | :-- |
|TiDB | 3 | 16 VCore 32 GB | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口配置；<br/>开启 enable_binlog； <br/> 开启 ignore-error |
| PD | 3 | 4 VCore 8 GB | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口配置 |
| TiKV | 3 | 16 VCore 32 GB | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口配置 |
| Pump| 3 |8 VCore 16GB |10.0.1.1 <br/> 10.0.1.7 <br/> 10.0.1.8 | 默认端口配置； <br/> 设置 GC 时间 7 天 |
| Drainer | 1 | 8 VCore 16GB | 10.0.1.12 | 默认端口配置；<br/> 设置默认初始化 commitTS -1 为最近的时间戳 <br/> 配置下游目标 TiDB 10.0.1.12:4000 |

### 拓扑模版

<details>
<summary>简单 TiDB Binlog 配置模板（下游为 MySQL）</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

server_configs:
  tidb:
    binlog.enable: true
    binlog.ignore-error: true

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

pump_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
drainer_servers:
  - host: 10.0.1.12
    config:
      syncer.db-type: "tidb"
      syncer.to.host: "10.0.1.12"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 4000

monitoring_servers:
  - host: 10.0.1.10

grafana_servers:
  - host: 10.0.1.10

alertmanager_servers:
  - host: 10.0.1.10
```

</details>

<details>
<summary>简单 TiDB Binlog 配置模板（下游为 file）</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

server_configs:
  tidb:
    binlog.enable: true
    binlog.ignore-error: true

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

pump_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
drainer_servers:
  - host: 10.0.1.12
    # drainer meta data directory path
    data_dir: "/path/to/save/data"
    config:
      syncer.db-type: "file"
      # directory to save binlog file, default same as data-dir(save checkpoint file) if this is not configured.
      # syncer.to.dir: "/path/to/save/binlog"

monitoring_servers:
  - host: 10.0.1.10

grafana_servers:
  - host: 10.0.1.10

alertmanager_servers:
  - host: 10.0.1.10
```

</details>

<details>
<summary>详细 TiDB Binlog 配置模板</summary>

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
    binlog.enable: true
    binlog.ignore-error: true
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

pump_servers:
  - host: 10.0.1.1
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8250"
    data_dir: "/tidb-data/pump-8250"
    # The following configs are used to overwrite the `server_configs.pump` values.
    config:
      gc: 7
  - host: 10.0.1.2
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8250"
    data_dir: "/tidb-data/pump-8250"
    # The following configs are used to overwrite the `server_configs.pump` values.
    config:
      gc: 7
  - host: 10.0.1.3
    ssh_port: 22
    port: 8250
    deploy_dir: "/tidb-deploy/pump-8250"
    data_dir: "/tidb-data/pump-8250"
    # The following configs are used to overwrite the `server_configs.pump` values.
    config:
      gc: 7
drainer_servers:
  - host: 10.0.1.12
    port: 8249
    deploy_dir: "/tidb-deploy/drainer-8249"
    data_dir: "/tidb-data/drainer-8249"
    # If drainer doesn't have a checkpoint, use initial commitTS as the initial checkpoint.
    # Will get a latest timestamp from pd if commit_ts is set to -1 (the default value).
    commit_ts: -1
    # The following configs are used to overwrite the `server_configs.drainer` values.
    config:
      syncer.db-type: "tidb"
      syncer.to.host: "10.0.1.12"
      syncer.to.user: "root"
      syncer.to.password: ""
      syncer.to.port: 4000
      syncer.to.checkpoint:
        schema: "tidb_binlog"
        type: "tidb"
        host: "10.0.1.14"
        user: "root"
        password: "123"
        port: 4000
  - host: 10.0.1.13
    port: 8249
    deploy_dir: "/tidb-deploy/drainer-8249"
    data_dir: "/tidb-data/drainer-8249"
    # If Drainer does not have a checkpoint, use the initial commitTS as the initial checkpoint.
    # If commit_ts is set to -1 (the default value), you will get a latest timestamp from PD.
    commit_ts: -1
    # The following configurations are used to overwrite the `server_configs.drainer` values.
    config:
      syncer.db-type: "kafka"
      syncer.replicate-do-db:
      - db1
      - db2
      syncer.to.kafka-addrs: "10.0.1.20:9092,10.0.1.21:9092,10.0.1.22:9092"
      syncer.to.kafka-version: "2.4.0"
      syncer.to.topic-name: "asyouwish"

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

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

### 关键参数介绍

拓扑配置模版的关键参数如下：

- `server_configs.tidb.binlog.enable: true`

    开启 TiDB Binlog 服务，默认为 false。

- `server_configs.tidb.binlog.ignore-error: true`

    高可用场景建议开启，如果设置为 true，发生错误时，TiDB 会停止写入 TiDB Binlog，并且在监控项 `tidb_server_critical_error_total` 上计数加 1；如果设置为 false，一旦写入 TiDB Binlog 失败，会停止整个 TiDB 的服务。

- `drainer_servers.config.syncer.db-type`

    TiDB Binlog 的下游类型，目前支持 `mysql`、`tidb`、`kafka` 和 `file`。

- `drainer_servers.config.syncer.to`

    TiDB Binlog 的下游配置。根据 `db-type` 的不同，该选项可配置下游数据库的连接参数、Kafka 的连接参数、文件保存路径。详细说明可参见 [TiDB Binlog 配置说明](/tidb-binlog/tidb-binlog-configuration-file.md#syncerto)。

> **注意：**
>
> - 编辑配置文件模版时，如无需自定义端口或者目录，仅修改 IP 即可。
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
