#### 部署需求

通过 `tidb` 用户做集群管理，使用默认 `22` 端口，部署目录为 `/tidb-deploy`，数据目录为 `/tidb-data`。

#### 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiKV | 3 | 16 VCore 32GB * 1 | 10.0.1.1 <br> 10.0.1.2 <br> 10.0.1.3 | 默认端口 <br> 全局目录配置 |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.7 <br> 10.0.1.8 <br> 10.0.1.9 | 默认端口 <br>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br> 10.0.1.5 <br> 10.0.1.6 | 默认端口 <br> 全局目录配置 |
| TiFlash | 1 | 32 VCore 64 GB * 1 | 10.0.1.10 | 默认端口 <br> 全局目录配置 |

#### 配置文件模版 topology.yaml

> **注意：**
>
> - 无需手动创建 tidb 用户，TiUP cluster 组件会在部署主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
>
> - [部署 TiFlash](/tiflash/deploy-tiflash.md) 需要在 topology.yaml 配置文件中将 `replication.enable-placement-rules` 设置为 `true`，以开启 PD 的 [Placement Rules](/configure-placement-rules.md) 功能。
>
> - tiflash_servers 实例级别配置 `"-host"` 目前只支持 IP，不支持域名。
>
> - TiFlash 具体的参数配置介绍可参考 [TiFlash 参数配置](#tiflash-参数)。

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

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
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9

tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3

tiflash_servers:
  - host: 10.0.1.10

monitoring_servers:
  - host: 10.0.1.4

grafana_servers:
  - host: 10.0.1.4

alertmanager_servers:
  - host: 10.0.1.4
```

更详细的配置为：

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
# # - TiDB: https://pingcap.com/docs/stable/reference/configuration/tidb-server/configuration-file/
# # - TiKV: https://pingcap.com/docs/stable/reference/configuration/tikv-server/configuration-file/
# # - PD: https://pingcap.com/docs/stable/reference/configuration/pd-server/configuration-file/
# # All configuration items use points to represent the hierarchy, e.g:
# #   readpool.storage.use-unified-pool
# #      
# # You can overwrite this configuration via the instance-level `config` field.

server_configs:
  tidb:
    log.slow-threshold: 300
    binlog.enable: false
    binlog.ignore-error: false
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
    replication.enable-placement-rules: true
  tiflash:
    logger.level: "info"
  # pump:
  #   gc: 7

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
  - host: 10.0.1.7
    # ssh_port: 22
    # port: 4000
    # status_port: 10080
    # deploy_dir: "/tidb-deploy/tidb-4000"
    # log_dir: "/tidb-deploy/tidb-4000/log"
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.tidb` values.
    # config:
    #   log.slow-query-file: tidb-slow-overwrited.log
  - host: 10.0.1.8
  - host: 10.0.1.9

tikv_servers:
  - host: 10.0.1.1
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
  - host: 10.0.1.2
  - host: 10.0.1.3

tiflash_servers:
  - host: 10.0.1.10
    # ssh_port: 22
    # tcp_port: 9000
    # http_port: 8123
    # flash_service_port: 3930
    # flash_proxy_port: 20170
    # flash_proxy_status_port: 20292
    # metrics_port: 8234
    # deploy_dir: /tidb-deploy/tiflash-9000
    # data_dir: /tidb-data/tiflash-9000
    # log_dir: /tidb-deploy/tiflash-9000/log
    # numa_node: "0,1"
    # # The following configs are used to overwrite the `server_configs.tiflash` values.
    # config:
    #   logger.level: "info"
    # learner_config:
    #   log-level: "info"
  # - host: 10.0.1.15
  # - host: 10.0.1.16

# pump_servers:
#   - host: 10.0.1.17
#     ssh_port: 22
#     port: 8250
#     deploy_dir: "/tidb-deploy/pump-8249"
#     data_dir: "/tidb-data/pump-8249"
#     log_dir: "/tidb-deploy/pump-8249/log"
#     numa_node: "0,1"
#     # The following configs are used to overwrite the `server_configs.drainer` values.
#     config:
#       gc: 7
#   - host: 10.0.1.18
#   - host: 10.0.1.19

# drainer_servers:
#   - host: 10.0.1.17
#     port: 8249
#     data_dir: "/tidb-data/drainer-8249"
#     # If drainer doesn't have a checkpoint, use initial commitTS as the initial checkpoint.
#     # Will get a latest timestamp from pd if commit_ts is set to -1 (the default value).
#     commit_ts: -1
#     deploy_dir: "/tidb-deploy/drainer-8249"
#     log_dir: "/tidb-deploy/drainer-8249/log"
#     numa_node: "0,1"
#     # The following configs are used to overwrite the `server_configs.drainer` values.
#     config:
#       syncer.db-type: "mysql"
#       syncer.to.host: "127.0.0.1"
#       syncer.to.user: "root"
#       syncer.to.password: ""
#       syncer.to.port: 3306
#   - host: 10.0.1.19

# cdc_servers:
#   - host: 10.0.1.20
#     ssh_port: 22
#     port: 8300
#     deploy_dir: "/tidb-deploy/cdc-8300"
#     log_dir: "/tidb-deploy/cdc-8300/log"
#     numa_node: "0,1"
#   - host: 10.0.1.21
#   - host: 10.0.1.22

monitoring_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # port: 9090
    # deploy_dir: "/tidb-deploy/prometheus-8249"
    # data_dir: "/tidb-data/prometheus-8249"
    # log_dir: "/tidb-deploy/prometheus-8249/log"

grafana_servers:
  - host: 10.0.1.4
    # port: 3000
    # deploy_dir: /tidb-deploy/grafana-3000

alertmanager_servers:
  - host: 10.0.1.4
    # ssh_port: 22
    # web_port: 9093
    # cluster_port: 9094
    # deploy_dir: "/tidb-deploy/alertmanager-9093"
    # data_dir: "/tidb-data/alertmanager-9093"
    # log_dir: "/tidb-deploy/alertmanager-9093/log"
```