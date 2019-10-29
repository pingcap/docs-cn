---
title: Kubernetes 上的 TiDB Binlog Drainer 配置
summary: 了解 Kubernetes 上的 TiDB Binlog Drainer 配置
category: reference
---

# Kubernetes 上的 TiDB Binlog Drainer 配置

本文档介绍 Kubernetes 上 TiDB Binlog drainer 的配置参数。

## 配置参数

下表包含所有用于 `tidb-drainer` chart 的配置参数。关于如何配置这些参数，可参阅[使用 Helm](/dev/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm)。

| 参数 | 说明 | 默认值 |
| :----- | :---- | :----- |
| `clusterName` | 源 TiDB 集群的名称 | `demo` |
| `clusterVersion` | 源 TiDB 集群的版本 | `v3.0.1` |
| `baseImage` | TiDB Binlog 的基础镜像 | `pingcap/tidb-binlog` |
| `imagePullPolicy` | 镜像的拉取策略 | `IfNotPresent` |
| `logLevel` | drainer 进程的日志级别 | `info` |
| `storageClassName` | drainer 所使用的 `storageClass`。`storageClassName` 是 Kubernetes 集群提供的一种存储，可以映射到服务质量级别、备份策略或集群管理员确定的任何策略。详情可参阅 [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `storage` | drainer Pod 的存储限制。请注意，如果 `db-type` 设为 `pd`，则应将本参数值设得大一些 | `10Gi` |
| `disableDetect` |  决定是否禁用事故检测 | `false` |
| `initialCommitTs` |  如果 drainer 没有断点，则用于初始化断点 | `0` |
| `config` | 传递到 drainer 的配置文件。详情可参阅 [drainer.toml](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml) |（见下文）|
| `resources` | drainer Pod 的资源限制和请求 | `{}` |
| `nodeSelector` | 确保 drainer Pod 仅被调度到具有特定键值对作为标签的节点上。详情可参阅 [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tolerations` | 适用于 drainer Pod，允许将 Pod 调度到有指定 taint 的节点上。详情可参阅 [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `affinity` | 定义 drainer Pod 的调度策略和首选项。详情可参阅 [affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-affinity) | `{}` |

`config` 的默认值为：

```toml
detect-interval = 10
compressor = ""
[syncer]
worker-count = 16
disable-dispatch = false
ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"
safe-mode = false
txn-batch = 20
db-type = "file"
[syncer.to]
dir = "/data/pb"
```
