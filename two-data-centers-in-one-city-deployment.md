---
title: 同城两中心自适应同步模式部署
summary: 了解同城使用两中心自适应同步模式部署方式。
---

# 同城两中心自适应同步模式部署

本文介绍同城两中心的部署模式，相关架构、示例配置、副本方法、启用该模式的方法。

TiDB 在 on-premises 部署的场景下，通常采用多中心部署方案，以保证高可用和容灾能力。多中心部署方案包括两地三中心部署模式、同城三中心部署模式等多种部署模式。本文介绍同城两中心部署方案，即在一座城市部署两个数据中心，成本更低，同样能满足高可用和容灾要求。该部署方案采用自适应同步模式，即 Data Replication Auto Synchronous，简称 DR Auto-Sync。

同城两中心部署方案下，两个数据中心距离在 50km 以内，通常位于同一个城市或两个相邻城市（例如北京和廊坊），数据中心间的网络连接延迟小于 1.5ms，带宽大于 10Gbps。

## 部署架构

本文以某城市为例，城里有两个数据中心 IDC1 和 IDC2，分为位于城东和城西。

下图为集群部署架构图，具体如下：

- 集群采用同城两种中心部署方案，主数据中心 IDC1 在城东，从数据中心 IDC2 在城西。
- 集群采用推荐的 4 副本模式，其中 IDC1 中放 2 个 Voter 副本，IDC2 中放 1 个 Voter 副本 + 1 个 Learner 副本；TiKV 按机房的实际情况打上合适的 Label。
- 副本间通过 Raft 协议保证数据的一致性和高可用，对用户完全透明。

![两地三中心集群架构图](/media/two-dc-replication-1.png)

该部署方案定义了三种状态来控制和标示集群的同步状态，该状态约束了 TiKV 的同步方式。集群的复制模式可以自动在三种状态之间自适应的切换。详见[状态转换](#状态转换)。

- **sync**：同步复制模式，此时从数据中心 (DR) 至少有一个副本与主数据中心 (PRIMARY) 进行同步，Raft 算法保证每条日志 (log) 按 Label 同步复制到 DR。
- **async**：异步复制模式，此时不保证 DR 与 PRIMARY 完全同步，Raft 算法使用经典的 majority 方式复制日志。
- **sync-recover**：恢复同步，此时不保证 DR 与 PRIMARY 完全同步，Raft 逐步切换成 Label 复制，切换成功后汇报给 PD。

## 配置

### 示例

以下 `tiup topology.yaml` 示例拓扑文件为同城两中心典型的拓扑配置：

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

为了按照规划的集群拓扑进行部署，你需要使用 [Placement Rules](/configure-placement-rules.md) 来规划集群副本的放置位置。以 4 副本和 2 Voter 副本在主中心，1 Voter 和 1 Learner 在副中心的部署方式为例，可使用 Placement Rules 进行如下副本配置：

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

### 启用自适应同步模式

副本的复制模式是由 PD 节点控制的。如果要使用 DR Auto-sync 自适应同步模式，需要在部署集群前先配置好 PD 的配置文件，如下所示：

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

在以上配置文件中：

+ `replication-mode` 为待启用的复制模式，以上示例中设置为 `dr-auto-sync`。默认使用 majority 算法。
+ `label-key` 用于区分不同的数据中心，需要和 Placement Rules 相匹配。其中主中心为 "east"，从中心为 "west"。
+ `primary-replicas` 是在主数据中心 Voter 副本的数量。
+ `dr-replicas` 是在从数据中心 Voter 副本的数量。
+ `wait-store-timeout` 是当出现网络隔离或者故障时，切换到异步复制模式的等待时间。如果超过这个时间还没恢复，则自动切换到异步复制模式。默认时间为 60s。

如果需要检查当前集群的复制状态，可以通过以下 API 获取：

{{< copyable "shell-regular" >}}

```bash
curl http://pd_ip:pd_port/pd/api/v1/replication_mode/status
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

- 当集群一切正常时，会进入同步复制模式来最大化的保障灾备机房的数据完整性。
- 当机房间网络断连或灾备机房发生整体故障时，在经过一段提前设置好的保护窗口之后，集群会进入异步复制状态，来保障业务的可用性。
- 当网络重连或灾备机房整体恢复之后，灾备机房的 TiKV 节点会重新加入到集群，逐步同步数据并最终转为同步复制模式。

状态转换的细节过程如下：

1. **初始化**：集群在初次启动时处于 sync（同步复制）模式，PD 会下发信息给 TiKV，所有 TiKV 节点会严格按照 sync 模式的要求进行工作。

2. **同步切异步**：PD 通过定时检查 TiKV 的心跳信息来判断 TiKV 是否宕机或断连。如果宕机数超过 PRIMARY/DR 各自副本的数量 `primary-replicas` 和 `dr-replicas`，意味着无法完成同步复制，需要切换状态。当宕机时间超过了 `wait-store-timeout` 设定的时间，PD 将集群状态切换成 async（异步复制）模式。然后 PD 再将 async 状态下发到所有 TiKV 节点，TiKV 的复制模式由双中心同步方式转为原生的 Raft 大多数落实方式 (majority)。

3. **异步切同步**：PD 通过定时检查 TiKV 的心跳信息来判断 TiKV 是否恢复连接，如果宕机数小于 PRIMARY/DR 各自副本的数量，意味着可以切回同步了。PD 会将集群复制状态先切换至 sync-recover 并将该状态下发给所有 TiKV 节点。TiKV 的所有 Region 逐步切换成双机房同步复制模式，切换成功后通过心跳将状态同步信息给 PD。PD 记录 TiKV 上 Region 的状态并统计恢复进度。当 TiKV 的所有 Region 都完成了同步复制模式的切换，PD 将集群复制状态切换为 sync。

### 灾难恢复

本节介绍同城两中心部署提供的容灾恢复方案。

当处于同步复制状态的集群发生了灾难，可进行 `RPO = 0` 的数据恢复：

- 如果主数据中心发生故障，丢失了大多数 Voter 副本，但是从数据中心有完整的数据，可从中心恢复数据。此时需要人工介入，通过专业工具恢复（恢复方式请联系 TiDB 团队）。

- 如果从中心发生故障，丢失了少数 Voter 副本，能自动切换成 async 异步复制模式。

当不处于同步复制状态的集群发生了灾难，不能保证满足 `RPO = 0` 进行数据恢复：

- 如果丢失了大多数 Voter 副本，需要人工介入，通过专业工具恢复（恢复方式请联系 TiDB 团队）。
