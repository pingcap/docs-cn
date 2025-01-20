---
title: 跨数据中心部署拓扑
summary: 介绍跨数据中心部署 TiDB 集群的拓扑结构。
---

# 跨数据中心部署拓扑

本文以典型的两地三中心为例，介绍跨数据中心部署的拓扑以及关键参数。本文示例所涉及的城市是上海（即 `sha`）和北京（即 `bja` 和 `bjb`）。

## 拓扑信息

|实例 | 个数 | 物理机配置 | BJ IP | SH IP |配置 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| TiDB |5 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 <br/> 10.0.1.4 | 10.0.1.5 | 默认端口 <br/>  全局目录配置 |
| PD | 5 | 4 VCore 8GB * 1 |10.0.1.6 <br/> 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 10.0.1.10 | 默认端口 <br/> 全局目录配置 |
| TiKV | 5 | 16 VCore 32GB 4TB (nvme ssd) * 1 | 10.0.1.11 <br/> 10.0.1.12 <br/> 10.0.1.13 <br/> 10.0.1.14 | 10.0.1.15 | 默认端口 <br/> 全局目录配置 |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.16 || 默认端口 <br/> 全局目录配置 |

> **注意：**
>
> 该表中拓扑实例的 IP 为示例 IP。在实际部署时，请替换为实际的 IP。

### 拓扑模版

<details>
<summary>跨机房配置模板</summary>

```yaml
# Tip: PD priority needs to be manually set using the PD-ctl client tool. such as, member Leader_priority PD-name numbers.
# Global variables are applied to all deployments and used as the default value of
# the deployments if a specific deployment value is missing.
#
# Abbreviations used in this example:
# sh: Shanghai Zone
# bj: Beijing Zone
# sha: Shanghai Datacenter A
# bja: Beijing Datacenter A
# bjb: Beijing Datacenter B

global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
monitored:
  node_exporter_port: 9100
  blackbox_exporter_port: 9115
  deploy_dir: "/tidb-deploy/monitored-9100"
server_configs:
  tidb:
    log.level: debug
    log.slow-query-file: tidb-slow.log
  tikv:
    server.grpc-compression-type: gzip
    readpool.storage.use-unified-pool: true
    readpool.storage.low-concurrency: 8
  pd:
    replication.location-labels: ["zone","dc","rack","host"]
    replication.max-replicas: 5
    label-property:  # TiDB 5.2 及以上版本默认不支持 label-property 配置。若要设置副本策略，请使用 Placement Rules。
      reject-leader:
        - key: "dc"
          value: "sha"
pd_servers:
 - host: 10.0.1.6
 - host: 10.0.1.7
 - host: 10.0.1.8
 - host: 10.0.1.9
 - host: 10.0.1.10
tidb_servers:
 - host: 10.0.1.1
 - host: 10.0.1.2
 - host: 10.0.1.3
 - host: 10.0.1.4
 - host: 10.0.1.5
tikv_servers:
 - host: 10.0.1.11
   ssh_port: 22
   port: 20160
   status_port: 20180
   deploy_dir: "/tidb-deploy/tikv-20160"
   data_dir: "/tidb-data/tikv-20160"
   config:
     server.labels:
       zone: bj
       dc: bja
       rack: rack1
       host: host1
 - host: 10.0.1.12
   ssh_port: 22
   port: 20161
   status_port: 20181
   deploy_dir: "/tidb-deploy/tikv-20161"
   data_dir: "/tidb-data/tikv-20161"
   config:
     server.labels:
       zone: bj
       dc: bja
       rack: rack1
       host: host2
 - host: 10.0.1.13
   ssh_port: 22
   port: 20160
   status_port: 20180
   deploy_dir: "/tidb-deploy/tikv-20160"
   data_dir: "/tidb-data/tikv-20160"
   config:
     server.labels:
       zone: bj
       dc: bjb
       rack: rack1
       host: host1
 - host: 10.0.1.14
   ssh_port: 22
   port: 20161
   status_port: 20181
   deploy_dir: "/tidb-deploy/tikv-20161"
   data_dir: "/tidb-data/tikv-20161"
   config:
     server.labels:
       zone: bj
       dc: bjb
       rack: rack1
       host: host2
 - host: 10.0.1.15
   ssh_port: 22
   port: 20160
   deploy_dir: "/tidb-deploy/tikv-20160"
   data_dir: "/tidb-data/tikv-20160"
   config:
     server.labels:
       zone: sh
       dc: sha
       rack: rack1
       host: host1
     readpool.storage.use-unified-pool: true
     readpool.storage.low-concurrency: 10
     raftstore.raft-min-election-timeout-ticks: 50
     raftstore.raft-max-election-timeout-ticks: 60
monitoring_servers:
 - host: 10.0.1.16
grafana_servers:
 - host: 10.0.1.16
```

</details>

以上 TiDB 集群拓扑文件中，详细的配置项说明见[通过 TiUP 部署 TiDB 集群的拓扑文件配置](/tiup/tiup-cluster-topology-reference.md)。

### 关键参数配置

本节介绍跨数据中心部署 TiDB 集群的关键参数配置。

#### TiKV 参数

- 设置 gRPC 的压缩格式，默认为 `none`。为提高跨机房部署场景的目标节点间 gRPC 包的传输速度，建议设置为 gzip 格式。

    ```yaml
    server.grpc-compression-type: gzip
    ```

- label 配置

    由于采用跨机房部署 TiKV，为了避免物理机宕机导致 Raft Group 默认的 5 副本中丢失 3 副本，使集群不可用的问题，可以通过 label 来实现 PD 智能调度，保证同中心、同机柜、同机器 TiKV 实例不会出现 Raft Group 有 3 副本的情况。

- TiKV 配置

    相同物理机配置相同的 host 级别 label 信息：

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

- 防止异地 TiKV 节点发起不必要的 Raft 选举，需要将异地 TiKV 节点发起选举时经过最少的 tick 个数和最多经过的 tick 个数都调大，这两个参数默认设置均为 `0`。

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 50
    raftstore.raft-max-election-timeout-ticks: 60
    ```

> **注意:**
>
> 通过 `raftstore.raft-min-election-timeout-ticks` 和 `raftstore.raft-max-election-timeout-ticks` 为 TiKV 节点配置较大的 election timeout tick 可以大幅降低该节点上的 Region 成为 Leader 的概率。但在发生灾难的场景中，如果部分 TiKV 节点宕机，而其它存活的 TiKV 节点 Raft 日志落后，此时只有这个配置了较大的 election timeout tick 的 TiKV 节点上的 Region 能成为 Leader。由于此 TiKV 节点上的 Region 需要至少等待 `raftstore.raft-min-election-timeout-ticks` 设置的时间后才能发起选举，因此尽量避免将此配置值设置得过大，以免在这种场景下影响集群的可用性。

#### PD 参数

- PD 元数据信息记录 TiKV 集群的拓扑信息，根据四个维度调度 Raft Group 副本。

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

- 调整 Raft Group 的副本数据量为 5，保证集群的高可用性。

    ```yaml
    replication.max-replicas: 5
    ```

- 拒绝异地机房 TiKV 的 Raft 副本选举为 Leader。

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

    > **注意：**
    >
    > TiDB 5.2 及以上版本默认不支持 `label-property` 配置。若要设置副本策略，请使用 [Placement Rules](/configure-placement-rules.md)。

有关 Label 的使用和 Raft Group 副本数量，详见[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)。

> **注意：**
>
> - 无需手动创建配置文件中的 `tidb` 用户，TiUP cluster 组件会在目标主机上自动创建该用户。可以自定义用户，也可以和中控机的用户保持一致。
> - 如果部署目录配置为相对路径，会部署在用户的 Home 目录下。
