---
title: TiDB Scheduler 扩展调度器
category: components
---

# TiDB Scheduler 扩展调度器

本文介绍 TiDB Scheduler 扩展调度器的工作原理。

## TiDB 集群调度需求

TiDB 集群核心包括 PD，TiKV 以及 TiDB 三个组件，每个组件又都是由多个节点组成，PD 是一个 Raft 集群，TiKV 是一个多 Group Raft 集群，并且这两个组件又都是有状态的。因此，默认 K8s 的调度器的调度规则已经无法满足 TiDB 集群的调度需求，需要扩展 K8s 的调度规则，目前，TiDB Operator 实现了如下几种自定义的调度规则：

### PD 组件

确保每个 Node 节点上调度的 PD 个数小于 `Replicas / 2`，例如：

| PD 集群规模（Replicas）  | 每个节点最多可调度的 PD 数量 |
| ------------- | ------------- |
| 1  | 1  |
| 2  | 1  |
| 3  | 1  |
| 4  | 1  |
| 5  | 2  |
| ...  |   |

### TiKV 组件

如果 K8s 节点数小于 3 个（K8s 集群节点数小于 3 个是无法实现 TiKV 高可用的），则可以任意调度；否则，每个节点上可调度的 TiKV 个数的计算公式为：Ceil (Replicas / 3) ，例如：

| TiKV 集群规模（Replicas）  | 每个节点最多可调度的 TiKV 数量 | 最佳调度分布 |
| ------------- | ------------- | ------------- |
| 3  | 1  | 1，1，1  |
| 4  | 2  | 1，1，2  |
| 5  | 2  | 1，2，2  |
| 6  | 2  | 2，2，2  |
| 7  | 3  | 2，2，3  |
| 8  | 3  | 2，3，3  |
| ...  |   |   |

### TiDB 组件

实现了稳定调度：在 TiDB 组件滚动更新的时候，尽量将其调度回原来的节点，这对于手动将 Node IP + NodePort 挂载在 LB 后端的场景比较有帮助，避免升级集群后 Node IP 发生变更需要重新调整 LB，这样可以减少滚动更新时对集群的影响。

## 工作原理

![TiDB Scheduler Overview](/media/tidb-scheduler-overview.png)

TiDB Scheduler 通过实现 K8s 调度器扩展（[Scheduler extender](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/scheduler_extender.md)）来添加自定义调度规则的。

TiDB Scheduler 组件部署为一个或者多个 Pod，但同时只有一个 Pod 在工作。Pod 内部有两个 Container，一个 Container 是原生的 `kube-scheduler`，另外一个 Container 是 `tidb-scheduler`，实现为一个 K8s scheduler extender。

TiDB Operator 创建的所有 Pod 的 `.spec.schedulerName` 属性会被设置为 `tidb-scheduler`，即都用 TiDB Scheduler 自定义调度器来调度。如果是测试集群，并且不要求高可用，可以将 `.spec.schedulerName` 改成 `default-scheduler` 使用 K8s 内置的调度器。一个 Pod 的调度流程是这样的：

- `kube-scheduler` 拉取所有 `.spec.schedulerName` 为 `tidb-scheduler` 的
   Pod，对于每个 Pod 会首先经过 K8s 默认调度规则过滤；
- 在这之后，`kube-scheduler` 会发请求到 `tidb-scheduler` 服务，`tidb-scheduler` 会通过一些自定义的调度规则（见上述介绍）对发送过来的 Node 节点进行过滤，最终将剩余可调度的 Node 节点返回给 `tidb-scheduler`；
- 最终由 `kube-scheduler` 决定最终调度的 Node 节点。

如果出现 Pod 无法调度，请参考此[文档](/tidb-in-kubernetes/troubleshoot.md#pod-处于-pending-状态)诊断和解决。
