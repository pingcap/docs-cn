---
title: 同城两中心自适应同步模式部署
summary: 介绍同城使用两中心自适应同步模式部署方式
aliases: ['/docs-cn/dev/two-data-centers-in-one-city-deployment/']
---

# 同城两中心部署模式 DR Auto-Sync

本文主要介绍同城两中心的部署模式 Data Replication Auto Synchronous

## 简介

TiDB 在 on-promise 部署的场景中，为了保证高可用和容灾能力，一般是多中心部署。在多中心部署方式中，有多种选择方案，包括两地三中心的部署模式，同城三中心等。这里介绍的是一种成本更低，在同城两中心部署同样能满足高可用和容灾要求的部署方式 Data Replication Auto Synchronous, 简称 DR Auto-Sync。

```
同城两中心：网络连接延迟 <1.5ms, 带宽 >10Gbps 的两个数据中心，一般位于同个城市或两个相邻城市（如北京和廊坊），距离在 50km 以内。
```

## 架构

本文以某地为例，有两个数据中心 IDC1、IDC2。分为位于城东和城西。

下图为集群部署架构图，具体如下：

- 集群采用同城两种中心部署方式，主中心 IDC1 城东 。从中心 IDC2 城西；
- 集群采用推荐的 4 副本模式，其中 IDC1 放 2 个 Voter 副本，IDC2 放 1 个 Voter 副本 + 1 个 Learner 副本；TiKV 按机实际情况打上合适的 Label。
- 副本间通过 Raft 协议保证数据的一致性和高可用，对用户完全透明。

![两地三中心集群架构图](/media/two-dc-replication-1.png)

我们定义了三种状态来控制和标示集群的同步状态，该状态约束了 TiKV 的复制方式：

- **sync**：同步复制，此时 DR 与 Primary 至少有一个副本与 Primary 同步，Raft 保证每条 log 按 label 同步复制到 DR
- **async**：异步复制，此时不保证 DR 与 Primary 完全同步，Raft 使用经典的 majority 方式复制 log
- **sync-recover**：恢复同步，此时不保证 DR 与 Primary 完全同步，Raft 逐步切换成 label 复制，切换成功后汇报给 PD

## 配置

### 示例

以下为一个 `tiup topology.yaml` 文件示例：

```
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  pd:
    replication.location-labels:  ["zone","rack","host"]

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"


tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12


tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { zone: "east", rack: "east-1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { zone: "east", rack: "east-2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { zone: "west", rack: "west-1", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { zone: "west", rack: "west-2", host: "33" }


monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### Placement Rules 规划

为了按照预想的集群的拓扑进行部署，我们需要使用 [placement rules](/configure-placement-rules.md) 来规划集群副本的放置位置。以 4 副本，2 voter 副本在主中心，1 voter + 1 learner 在副中心的部署方式为例： 

```
cat rule.json
[
  {
    "group_id": "pd",
    "id": "zone-east",
    "start_key": "",
    "end_key": "",
    "role": "voter",
    "count": 2,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "east"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host",
    ]
  },
  {
    "group_id": "pd",
    "id": "zone-west",
    "start_key": "",
    "end_key": "",
    "role": "voter",
    "count": 1,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "west"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host"
    ]
  },
  {
    "group_id": "pd",
    "id": "zone-west",
    "start_key": "",
    "end_key": "",
    "role": "learner",
    "count": 1,
    "label_constraints": [
      {
        "key": "zone",
        "op": "in",
        "values": [
          "west"
        ]
      }
    ],
    "location_labels": [
      "zone",
      "rack",
      "host"
    ]
  }
]
```

### 启用 DR Auto-sync 模式

副本的复制模式是由 PD 节点控制的。如果要使用 `dr-auto-sync` 模式，需要在部署集群先配置好 PD 的配置文件，如下所示：

{{< copyable "" >}}

```toml
[replication-mode]
replication-mode = "dr-auto-sync"
[replication-mode.dr-auto-sync]
label-key = "zone"
primary = "east"
dr = "west"
primary-replicas = 2
dr-replicas = 1
wait-store-timeout = "1m"
wait-sync-timeout = "1m"
```

在上述配置文件中：

+ `replication-mode` 是启用设置复制模式，这里设置为 `dr-auto-sync`。默认情况为 majority。
+ `label-key` 用于区分不同的数据中心，需要和 placement rule 相匹配。其中主中心为 east，副中心为 west。
+ `primary-replicas` 在主中心 voter 副本的数量。
+ `dr-replicas` 是在副中心 voter 副本的数量。
+ `wait-store-timeout` 是当出现网络隔离或者故障是，切换到异步模式的等待时间。如果超过这个时间还没恢复则自动切换到异步复制模式。默认 60s。

如果需要检查当前集群的复制状态，可以通过 API:

{{< copyable "shell-regular" >}}

```bash
% curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
```

{{< copyable "shell-regular" >}}

```bash
{
  "mode": "dr-auto-sync",
  "dr-auto-sync": {
    "label-key": "zone",
    "state": "sync"
  }
}
```

#### 状态转换

简单来讲，集群的复制模式可以自动在三种状态之间自适应的切换：
    
- 当集群一切正常时，会进入同步复制模式来最大化的保障灾备机房的数据完整性
- 当机房间网络断连或灾备机房发生整体故障时，在经过一段提前设置好的保护窗口之后，集群会进入异步复制状态，来保障业务的可用性
- 当网络重连或灾备机房整体恢复之后，灾备机房的 TiKV 会重新加入到集群，逐步同步数据并最终转为同步复制模式

状态转换的细节过程如下：

1. **初始化**：集群在第一次启动时是 sync 状态，PD 会下发信息给 TiKV，所有 TiKV 会严格按照 sync 模式的要求进行工作。

2. **同步切异步**：PD 通过定时检查 TiKV 的心跳信息来判断 TiKV 是否宕机/断连。如果宕机数超过 Primary/DR 各自副本的数量 `primary-replicas` 和 `dr-replicas`，意味着无法完成同步复制了，需要切换状态。当宕机时间超过了 `wait-store-timeout`设定的时间，PD 将集群状态切换成 async。然后 PD 再将 async 状态下发到所有 TiKV，TiKV 的复制方式由双中心同步方式转为原生的 Raft 大多数落实方式。

3. **异步切同步**：PD 通过定时检查 TiKV 的心跳信息来判断 TiKV 是否恢复连接，如果宕机数小于 Primary/DR 各自副本的数量，意味着可以切回同步了。PD 会将集群复制状态先切换至 sync-recover 并将该状态下发给所有 TiKV。TiKV 的所有 region 逐步切换成双机房同步复制模式，切换成功后状态通过心跳同步信息给 PD。PD 记录 TiKV 上 region 的状态并统计恢复进度。当 TiKV 的所有 Region 都完成了同步复制模式的切换，PD 将集群复制状态切换为 sync。

### 灾难恢复

当集群处于 `sync` 发生灾难，可满足 `RPO = 0` 恢复：

- 主中心 PRIMARY 故障，丢失了大多数 Voter 副本，但是 DR 从中心有完整的数据，可从 DR 从中心恢复数据。此时需要人工介入，通过专业工具恢复（恢复方式请联系 TiDB 团队）。

- 从中心 DR 故障，丢失了少数 Voter 副本，能自动切换成 Async 模式。

当集群不处于 `sync` 发生灾难，不能保证满足 `RPO = 0` 恢复：

- 如果丢失了大多数 Voter 副本，需要人工介入，通过专业工具恢复（恢复方式请联系 TiDB 团队）。