---
title: 集群拓扑信息配置
category: how-to
---

# 集群拓扑信息配置

## 概述

PD 能够根据 TiKV 集群的拓扑结构进行调度，使得 TiKV 的容灾能力最大化。

阅读本章前，请先确保阅读 [Ansible 部署方案](/v2.1/how-to/deploy/orchestrated/ansible.md) 和 [Docker 部署方案](/v2.1/how-to/deploy/orchestrated/docker.md)。

## TiKV 上报拓扑信息

可以通过 TiKV 的启动参数或者配置文件来让 TiKV 上报拓扑信息给 PD。

假设拓扑结构分为三级：zone > rack > host，可以通过 labels 来指定这些信息。

启动参数：

```
tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
```

配置文件：

```toml
[server]
labels = "zone=<zone>,rack=<rack>,host=<host>"
```

## PD 理解 TiKV 拓扑结构

可以通过 PD 的配置文件让 PD 理解 TiKV 集群的拓扑结构。

```toml
[replication]
max-replicas = 3
location-labels = ["zone", "rack", "host"]
```

其中 `location-labels` 需要与 TiKV 的 `labels` 名字对应，这样 PD 才能知道这些 `labels` 代表了 TiKV 的拓扑结构。

## PD 基于 TiKV 拓扑结构进行调度

PD 能够根据我们提供的拓扑信息作出最优的调度，我们只需要关心什么样的拓扑结构能够达到我们想要的效果。

假设我们使用三副本，并且希望一个数据中心挂掉的情况下，还能继续保持 TiDB 集群的高可用状态，我们至少需要四个数据中心。

假设我们有四个数据中心 (zone)，每个数据中心有两个机架 (rack)，每个机架上有两个主机 (host)。
每个主机上面启动一个 TiKV 实例：

```
# zone=z1
tikv-server --labels zone=z1,rack=r1,host=h1
tikv-server --labels zone=z1,rack=r1,host=h2
tikv-server --labels zone=z1,rack=r2,host=h1
tikv-server --labels zone=z1,rack=r2,host=h2

# zone=z2
tikv-server --labels zone=z2,rack=r1,host=h1
tikv-server --labels zone=z2,rack=r1,host=h2
tikv-server --labels zone=z2,rack=r2,host=h1
tikv-server --labels zone=z2,rack=r2,host=h2

# zone=z3
tikv-server --labels zone=z3,rack=r1,host=h1
tikv-server --labels zone=z3,rack=r1,host=h2
tikv-server --labels zone=z3,rack=r2,host=h1
tikv-server --labels zone=z3,rack=r2,host=h2

# zone=z4
tikv-server --labels zone=z4,rack=r1,host=h1
tikv-server --labels zone=z4,rack=r1,host=h2
tikv-server --labels zone=z4,rack=r2,host=h1
tikv-server --labels zone=z4,rack=r2,host=h2
```

也就是说，我们有 16 个 TiKV 实例，分布在 4 个不同的数据中心，8 个不同的机架，16 个不同的机器。

在这种拓扑结构下，PD 会优先把每一份数据的不同副本调度到不同的数据中心。
这时候如果其中一个数据中心挂了，不会影响 TiDB 集群的高可用状态。
如果这个数据中心一段时间内恢复不了，PD 会把这个数据中心的副本迁移出去。

总的来说，PD 能够根据当前的拓扑结构使得集群容灾能力最大化，所以如果我们希望达到某个级别的容灾能力，
就需要根据拓扑机构在不同的地理位置提供多于备份数 (`max-replicas`) 的机器。
