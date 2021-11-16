---
title: 通过拓扑 label 进行副本调度
aliases: ['/docs-cn/stable/schedule-replicas-by-topology-labels/','/docs-cn/v4.0/schedule-replicas-by-topology-labels/','/docs-cn/stable/how-to/deploy/geographic-redundancy/location-awareness/','/docs-cn/stable/location-awareness/','/docs-cn/v4.0/how-to/deploy/geographic-redundancy/location-awareness/']
---

# 通过拓扑 label 进行副本调度

为了提升 TiDB 集群的高可用性和数据容灾能力，我们推荐让 TiKV 节点尽可能在物理层面上分散，例如让 TiKV 节点分布在不同的机架甚至不同的机房。PD 调度器根据 TiKV 的拓扑信息，会自动在后台通过调度使得 Region 的各个副本尽可能隔离，从而使得数据容灾能力最大化。

要让这个机制生效，需要在部署时进行合理配置，把集群的拓扑信息（特别是 TiKV 的位置）上报给 PD。阅读本章前，请先确保阅读 [TiUP 部署方案](/production-deployment-using-tiup.md)。

## 根据集群拓扑配置 labels

### 设置 TiKV 的 `labels` 配置

TiKV 支持在命令行参数或者配置文件中以键值对的形式绑定一些属性，我们把这些属性叫做标签（label）。TiKV 在启动后，会将自身的标签上报给 PD，因此我们可以使用标签来标识 TiKV 节点的地理位置。

比如集群的拓扑结构分成三层：机房（zone) -> 机架（rack）-> 主机（host），就可以使用这 3 个标签来设置 TiKV 的位置。

使用命令行参数的方式：

{{< copyable "" >}}

```
tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
```

使用配置文件的方式：

{{< copyable "" >}}

```toml
[server]
labels = "zone=<zone>,rack=<rack>,host=<host>"
```

### 设置 PD 的 `location-labels` 配置

根据前面的描述，标签可以是用来描述 TiKV 属性的任意键值对，但 PD 无从得知哪些标签是用来标识地理位置的，而且也无从得知这些标签的层次关系。因此，PD 也需要一些配置来使得 PD 理解 TiKV 节点拓扑。

PD 上的配置叫做 `location-labels`，在集群初始化之前，可以通过 PD 的配置文件进行配置。

{{< copyable "" >}}

```toml
[replication]
location-labels = ["zone", "rack", "host"]
```

如果需要在 PD 集群初始化完成后进行配置，则需要使用 pd-ctl 工具进行在线更改：

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set location-labels zone,rack,host
```

其中，`location-labels` 配置是一个字符串数组，每一项与 TiKV 的 `labels` 的 key 是对应的，且其中每个 key 的顺序代表了不同标签的层次关系。

> **注意：**
>
> 必须同时配置 PD 的 `location-labels` 和 TiKV 的 `labels` 参数，否则 PD 不会根据拓扑结构进行调度。

### 使用 TiUP 进行配置（推荐）

如果使用 TiUP 部署集群，可以在[初始化配置文件](/production-deployment-using-tiup.md#第-3-步编辑初始化配置文件)中统一进行 location 相关配置。TiUP 会负责在部署时生成对应的 TiKV 和 PD 配置文件。

下面的例子定义了 `zone/host` 两层拓扑结构。集群的 TiKV 分布在三个 zone，每个 zone 内有两台主机，其中 z1 每台主机部署两个 TiKV 实例，z2 和 z3 每台主机部署 1 个实例。以下例子中 `tikv-n` 代表第 n 个 TiKV 节点的 IP 地址。

```
server_configs:
  pd:
    replication.location-labels: ["zone", "host"]

tikv_servers:
# z1
  - host: tikv-1
    config:
      server.labels:
        zone: z1
        host: h1
   - host: tikv-2
    config:
      server.labels:
        zone: z1
        host: h1
  - host: tikv-3
    config:
      server.labels:
        zone: z1
        host: h2
  - host: tikv-4
    config:
      server.labels:
        zone: z1
        host: h2
# z2
  - host: tikv-5
    config:
      server.labels:
        zone: z2
        host: h1
   - host: tikv-6
    config:
      server.labels:
        zone: z2
        host: h2
# z3
  - host: tikv-7
    config:
      server.labels:
        zone: z3
        host: h1
  - host: tikv-8
    config:
      server.labels:
        zone: z3
        host: h2
```

详情参阅 [TiUP 跨数据中心部署拓扑](/geo-distributed-deployment-topology.md)。

<details>
<summary> <strong>使用 TiDB Ansible 进行配置</strong> </summary>

如果使用 TiDB Ansible 部署集群，可以直接在 `inventory.ini` 文件中统一进行 location 相关配置。`tidb-ansible` 会负责在部署时生成对应的 TiKV 和 PD 配置文件。

下面的例子定义了 `zone/host` 两层拓扑结构。集群的 TiKV 分布在三个 zone，每个 zone 内有两台主机，其中 z1 每台主机部署两个 TiKV 实例，z2 和 z3 每台主机部署 1 个实例。

```
[tikv_servers]
# z1
tikv-1 labels="zone=z1,host=h1"
tikv-2 labels="zone=z1,host=h1"
tikv-3 labels="zone=z1,host=h2"
tikv-4 labels="zone=z1,host=h2"
# z2
tikv-5 labels="zone=z2,host=h1"
tikv-6 labels="zone=z2,host=h2"
# z3
tikv-7 labels="zone=z3,host=h1"
tikv-8 labels="zone=z3,host=h2"

[pd_servers:vars]
location_labels = ["zone", "host"]
```

</details>

## 基于拓扑 label 的 PD 调度策略

PD 在副本调度时，会按照 label 层级，保证同一份数据的不同副本尽可能分散。

下面以上一节的拓扑结构为例分析。

假设集群副本数设置为 3（`max-replicas=3`），因为总共有 3 个 zone，PD 会保证每个 Region 的 3 个副本分别放置在 z1/z2/z3，这样当任何一个数据中心发生故障时，TiDB 集群依然是可用的。

假如集群副本数设置为 5（`max-replicas=5`），因为总共只有 3 个 zone，在这一层级 PD 无法保证各个副本的隔离，此时 PD 调度器会退而求其次，保证在 host 这一层的隔离。也就是说，会出现一个 Region 的多个副本分布在同一个 zone 的情况，但是不会出现多个副本分布在同一台主机。

在 5 副本配置的前提下，如果 z3 出现了整体故障或隔离，并且 z3 在一段时间后仍然不能恢复（由 `max-store-down-time` 控制），PD 会通过调度补齐 5 副本，此时可用的主机只有 3 个了，故而无法保证 host 级别的隔离，于是可能出现多个副本被调度到同一台主机的情况。

总的来说，PD 能够根据当前的拓扑结构使得集群容灾能力最大化，所以如果我们希望达到某个级别的容灾能力，
就需要根据拓扑结构在对应级别提供多于副本数 (`max-replicas`) 的机器。
