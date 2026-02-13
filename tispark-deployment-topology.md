---
title: TiSpark 部署拓扑
summary: 介绍 TiUP 部署包含 TiSpark 组件的 TiDB 集群的拓扑结构。
aliases: ['/zh/tidb/stable/tispark-deployment-topology/','/zh/tidb/dev/tispark-deployment-topology/']
---

# TiSpark 部署拓扑

本文介绍 TiSpark 部署的拓扑，以及如何在最小拓扑的基础上同时部署 TiSpark。TiSpark 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。它借助 Spark 平台，同时融合 TiKV 分布式集群的优势，和 TiDB 一起为用户一站式解决 HTAP (Hybrid Transactional/Analytical Processing) 的需求。

关于 TiSpark 的架构介绍与使用，参见 [TiSpark 用户指南](/tispark-overview.md)。

> **警告：**
>
> TiUP Cluster 的 TiSpark 支持目前为废弃状态，不建议使用。

## 拓扑信息

|实例 | 个数 | 物理机配置 | IP |配置 |
| :-- | :-- | :-- | :-- | :-- |
| TiDB |3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | 默认端口 <br/>  全局目录配置 |
| PD | 3 | 4 VCore 8GB * 1 |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | 默认端口 <br/> 全局目录配置 |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 默认端口 <br/> 全局目录配置 |
| TiSpark | 3 | 8 VCore 16GB * 1 | 10.0.1.21 (master) <br/> 10.0.1.22 (worker) <br/> 10.0.1.23 (worker) | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.11 | 默认端口 <br/> 全局目录配置 |

> **注意：**
>
> 该表中拓扑实例的 IP 为示例 IP。在实际部署时，请替换为实际的 IP。

### 拓扑模版

<details>
<summary>简单 TiSpark 配置模板</summary>

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


# NOTE: TiSpark support is an experimental feature, it's not recommend to be used in
# production at present.
# To use TiSpark, you need to manually install Java Runtime Environment (JRE) 8 on the
# host, see the OpenJDK doc for a reference: https://openjdk.java.net/install/
# NOTE: Only 1 master node is supported for now
tispark_masters:
  - host: 10.0.1.21

# NOTE: multiple worker nodes on the same host is not supported by Spark
tispark_workers:
  - host: 10.0.1.22
  - host: 10.0.1.23

monitoring_servers:
  - host: 10.0.1.10

grafana_servers:
  - host: 10.0.1.10

alertmanager_servers:
  - host: 10.0.1.10
```

</details>

<details>
<summary>详细 TiSpark 配置模板</summary>

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

# NOTE: TiSpark support is an experimental feature, it's not recommend to be used in
# production at present.
# To use TiSpark, you need to manually install Java Runtime Environment (JRE) 8 on the
# host, see the OpenJDK doc for a reference: https://openjdk.java.net/install/
# If you have already installed JRE 1.8 at a location other than the default of system's
# package management system, you may use the "java_home" field to set the JAVA_HOME variable.
# NOTE: Only 1 master node is supported for now
tispark_masters:
  - host: 10.0.1.21
    # ssh_port: 22
    # port: 7077
    # web_port: 8080
    # deploy_dir: "/tidb-deploy/tispark-master-7077"
    # java_home: "/usr/local/bin/java-1.8.0"
    # spark_config:
    #   spark.driver.memory: "2g"
    #   spark.eventLog.enabled: "False"
    #   spark.tispark.grpc.framesize: 268435456
    #   spark.tispark.grpc.timeout_in_sec: 100
    #   spark.tispark.meta.reload_period_in_sec: 60
    #   spark.tispark.request.command.priority: "Low"
    #   spark.tispark.table.scan_concurrency: 256
    # spark_env:
    #   SPARK_EXECUTOR_CORES: 5
    #   SPARK_EXECUTOR_MEMORY: "10g"
    #   SPARK_WORKER_CORES: 5
    #   SPARK_WORKER_MEMORY: "10g"

# NOTE: multiple worker nodes on the same host is not supported by Spark
tispark_workers:
  - host: 10.0.1.22
    # ssh_port: 22
    # port: 7078
    # web_port: 8081
    # deploy_dir: "/tidb-deploy/tispark-worker-7078"
    # java_home: "/usr/local/bin/java-1.8.0"
  - host: 10.0.1.23

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

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md#tispark_masters)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。

## 环境要求

由于 TiSpark 基于 Apache Spark 集群，在启动包含 TiSpark 组件的 TiDB 集群前，需要在部署了 TiSpark 组件的服务器上安装 Java 运行时环境(JRE) 8，否则将无法启动相关组件。

TiUP 不提供自动安装 JRE 的支持，该操作需要用户自行完成。JRE 8 的安装方法可以参考 [OpenJDK 的文档说明](https://openjdk.java.net/install/)。

如果部署服务器上已经安装有 JRE 8，但不在系统的默认包管理工具路径中，可以通过在拓扑配置中设置 `java_home` 参数来指定要使用的 JRE 环境所在的路径。该参数对应系统环境变量 `JAVA_HOME`。
