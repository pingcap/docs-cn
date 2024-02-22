---
title: 双区域多 AZ 部署 TiDB
summary: 介绍在两个区域多个可用区部署 TiDB 的方式。
---

# 双区域多 AZ 部署 TiDB

本文档简要介绍双区域多可用区 (Availability Zone, AZ) 部署的架构模型及配置。

本文中的区域指的是地理隔离的不同位置，AZ 指的是区域内部划分的相互独立的资源集合，本文描述的方案同样适用于在两个城市部署三个数据中心（两地三中心）的场景。

## 简介

双区域多 AZ 架构，即生产数据 AZ、同区域灾备 AZ、跨区域灾备 AZ 的高可用容灾方案。在这种模式下，两个区域的三个 AZ 互联互通，如果一个 AZ 发生故障或灾难，其他 AZ 可以正常运行并对关键业务或全部业务实现接管。相比同区域多 AZ 方案，双区域三 AZ 具有跨区域级高可用能力，可以应对区域级自然灾害。

TiDB 分布式数据库采用 Raft 算法，可以原生支持双区域三 AZ 架构，并保证集群数据的一致性和高可用。而且，同区域 AZ 网络延迟相对较小，可以把业务流量同时派发到同区域两个 AZ，并通过控制 Region Leader 和 PD Leader 分布实现同区域 AZ 共同负载业务流量。

## 架构

本文以北京和西安部署集群为例，阐述 TiDB 分布式数据库双区域三 AZ 架构的部署模型。

假设北京有两个 AZ，AZ1 和 AZ2，西安有一个 AZ，AZ3。北京同区域两 AZ 之间网络延迟低于 3 ms，北京与西安之间的网络使用 ISP 专线，延迟约为 20 ms。

下图为集群部署架构图，具体如下：

- 集群采用双区域三 AZ 部署方式，分别为北京 AZ1，北京 AZ2，西安 AZ3。
- 集群采用 5 副本模式，其中 AZ1 和 AZ2 分别放 2 份副本，AZ3 放 1 份副本；TiKV 按机柜设置 Label，即每个机柜上有 1 份副本。
- 副本间通过 Raft 协议保证数据的一致性和高可用，对用户完全透明。

![双区域三 AZ 集群架构图](/media/three-data-centers-in-two-cities-deployment-01.png)

该架构具备高可用能力，同时通过 PD 调度保证 Region Leader 只出现在同区域的两个 AZ。相比于三 AZ，即 Region Leader 分布不受限制的方案，双区域三 AZ 方案有以下优缺点：

- **优点**

    - Region Leader 都在同区域 AZ，延迟低，数据写入速度更优。
    - 双 AZ 可同时对外提供服务，资源利用率更高。
    - 任一 AZ 失效后，另一 AZ 接管服务，业务可用并且不发生数据丢失。

- **缺点**

    - 因为数据一致性是基于 Raft 算法实现，当同区域两个 AZ 同时失效时，因为远程灾备 AZ 只剩下一份副本，不满足 Raft 算法大多数副本存活的要求。最终将导致集群暂时不可用，需要从一副本恢复集群，丢失少部分还没同步的热数据。这种情况出现概率较小。
    - 由于使用了网络专线，该架构下网络设施成本较高。
    - 双区域三 AZ 需设置 5 副本，数据冗余度增加，空间成本攀升。

### 详细示例

北京、西安双区域三 AZ 配置详解：

![双区域三 AZ 配置详图](/media/three-data-centers-in-two-cities-deployment-02.png)

如上图所示，北京有两个可用区 AZ1 和 AZ2，可用区 AZ1 有三套机架 rac1、rac2 和 rac3，可用区 AZ2 有两套机架 rac4 和 rac5；西安可用区 AZ3 有一套机架 rac6。

AZ1 的 rac1 机架中，一台服务器部署了 TiDB 和 PD 服务，另外两台服务器部署了 TiKV 服务，其中，每台 TiKV 服务器部署了两个 TiKV 实例 (tikv-server)，rac2、rac4、rac5 和 rac6 类似。

机架 rac3 上部署了 TiDB Server、中控及监控服务器。TiDB Server 用于日常管理维护和备份。中控和监控服务器上部署了 Prometheus、Grafana 以及恢复工具。

另可增加备份服务器，其上部署 Drainer，Drainer 以输出 file 文件的方式将 binlog 数据保存到指定位置，实现增量备份的目的。

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
  tikv:
    server.grpc-compression-type: gzip
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"
  - host: 10.63.10.13
    name: "pd-13"
  - host: 10.63.10.14
    name: "pd-14"

tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12
  - host: 10.63.10.13
  - host: 10.63.10.14

tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { az: "1", replication zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { az: "1", replication zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { az: "2", replication zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { az: "2", replication zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { az: "3", replication zone: "5", rack: "5", host: "34" }
      raftstore.raft-min-election-timeout-ticks: 50
      raftstore.raft-max-election-timeout-ticks: 60

monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### Labels 设计

在双区域三 AZ 部署方式下，对于 Labels 的设计需要充分考虑到系统的可用性和容灾能力，建议根据部署的物理结构来定义 AZ、replication zone、rack 和 host 四个等级。

![Label 逻辑定义图](/media/three-data-centers-in-two-cities-deployment-03.png)

PD 设置中添加 TiKV label 的等级配置。

```
server_configs:
  pd:
    replication.location-labels:  ["az","replication zone","rack","host"]
```

tikv_servers 设置基于 TiKV 真实物理部署位置的 Label 信息，方便 PD 进行全局管理和调度。

```
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { az: "1", replication zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { az: "1", replication zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { az: "2", replication zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { az: "2", replication zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { az: "3", replication zone: "5", rack: "5", host: "34" }
```

### 参数配置优化

在双区域三 AZ 的架构部署中，从性能优化的角度，除了常规参数配置外，还需要对集群中相关组件参数进行调整。

- 启用 TiKV gRPC 消息压缩。由于需要在网络中传输集群数据，可开启 gRPC 消息压缩，降低网络流量。

    ```
    server.grpc-compression-type: gzip
    ```

- 优化跨区域 AZ3 的 TiKV 节点网络，修改 TiKV 的如下参数，拉长跨区域副本参与选举的时间，避免跨区域 TiKV 中的副本参与 Raft 选举。

    ```
    raftstore.raft-min-election-timeout-ticks: 50
    raftstore.raft-max-election-timeout-ticks: 60
    ```

> **注意:**
>
> 通过 `raftstore.raft-min-election-timeout-ticks` 和 `raftstore.raft-max-election-timeout-ticks` 为 TiKV 节点配置较大的 election timeout tick 可以大幅降低该节点上的 Region 成为 Leader 的概率。但在发生灾难的场景中，如果部分 TiKV 节点宕机，而其它存活的 TiKV 节点 Raft 日志落后，此时只有这个配置了较大的 election timeout tick 的 TiKV 节点上的 Region 能成为 Leader。由于此 TiKV 节点上的 Region 需要至少等待 `raftstore.raft-min-election-timeout-ticks` 设置的时间后才能发起选举，因此尽量避免将此配置值设置得过大，以免在这种场景下影响集群的可用性。

- 调度设置。在集群启动后，通过 `tiup ctl:v<CLUSTER_VERSION> pd` 工具进行调度策略修改。修改 TiKV Raft 副本数按照安装时规划好的副本数进行设置，在本例中为 5 副本。

    ```
    config set max-replicas 5
    ```

- 禁止向跨区域 AZ 调度 Raft Leader，当 Raft Leader 在跨区域 AZ 时，会造成不必要的本区域 AZ 与远程 AZ 间的网络消耗，同时，网络带宽和延迟也会对 TiDB 的集群性能产生影响。

    ```
    config set label-property reject-leader dc 3
    ```

    > **注意：**
    >
    > TiDB 5.2 及以上版本默认不支持 `label-property` 配置。若要设置副本策略，请使用 [Placement Rules](/configure-placement-rules.md)。

- 设置 PD 的优先级，为了避免出现跨区域 AZ 的 PD 成为 Leader，可以将本区域 AZ 的 PD 优先级调高（数字越大，优先级越高），将跨区域的 PD 优先级调低。

    ```
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
