---
title: 管理本地 PV
category: how-to
---

# 管理本地 PV

TiDB 是一款高可用的数据库。TiDB 的存储层 TiKV 对数据进行复制，容忍节点不可用。TiKV 使用高
 IOPS 和高吞吐量的本地存储，比如 Local SSDs 时，可提高数据库性能。

Kubernetes 当前支持静态分配的本地存储。可使用
[local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) 项目中的
local-volume-provisioner 程序创建本地存储对象。创建流程如下：

1. 参考 Kubernetes 提供的[操作文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md)，在 TiKV 集群节点中预分配本地存储。
2. 参考 Helm 的 [部署案例](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm)，部署 local-volume-provisioner 程序。

更多信息，可参阅 [Kubernetes 本地存储](https://kubernetes.io/docs/concepts/storage/volumes/#local)和 [local-static-provisioner 文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview)。
