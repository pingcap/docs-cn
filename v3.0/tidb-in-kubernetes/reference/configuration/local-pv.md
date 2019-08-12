---
title: 本地 PV 配置
category: reference
aliases: ['/docs-cn/v3.0/reference/configuration/tidb-in-kubernetes/local-pv-configuration/']
---

# 本地 PV 配置

TiDB 是一款高可用的数据库。TiDB 的存储层 TiKV 对数据进行复制，容忍节点不可用。TiKV 使用高 IOPS 和高吞吐量的本地存储，比如 Local SSDs 时，可提高数据库性能。

Kubernetes 当前支持静态分配的本地存储。可使用 [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) 项目中的 `local-volume-provisioner` 程序创建本地存储对象。创建流程如下：

1. 参考 Kubernetes 提供的[操作文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md)，在 TiKV 集群节点中预分配本地存储。
2. 参考 Helm 的[部署案例](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm)，部署 `local-volume-provisioner` 程序。

更多信息，可参阅 [Kubernetes 本地存储](https://kubernetes.io/docs/concepts/storage/volumes/#local)和 [local-static-provisioner 文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview)。

## 数据安全

- 默认 local PV 不被使用时，会被 provisioner 回收供其他程序使用。为避免数据意外丢失，可配置 storage class 的 reclaim policy 为 `Retain` 。`Retain` 模式下，PV 不会自动被回收。当确认某个 PV 的数据可以被删除时，单独修改其 reclaim policy 为 `Delete` 。如何修改 PV reclaimPolicy 可参考[此文档](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/)。

## 最佳实践

- Local PV 的路径是本地存储卷的唯一标示符，为了保证唯一性避免冲突，推荐使用设备的 UUID 来生成唯一的路径
- 如果想要 IO 隔离，建议每个存储卷使用一块物理盘会比较恰当，在硬件层隔离
- 如果想要容量隔离，建议每个存储卷一个分区来实现

更多信息，可参阅 local-static-provisioner 的[最佳实践文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md)。
