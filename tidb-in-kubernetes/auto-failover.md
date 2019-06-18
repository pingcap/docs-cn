---
title: 故障自动转移
category: how-to
---

# 故障自动转移

自动故障转移是指在 TiDB 集群的某些节点出现故障时，Operator 会自动添加一个节点，保证 TiDB 集群的高可用，类似于 k8s 的 Deployment 的行为。

由于 Opererator 是基于 StatefulSet 来管理 Pod 的，但 StatefulSet 在某些 Pod 发生故障时不会自动的创建新节点来替换旧节点，所以，Operator 扩展了 StatefulSet 的这种行为，添加了 failover 功能。

Auto Failover 功能在 Operator 默认是关闭的，需要在部署 Operator 的时候开启，开启方法为设置 `charts/tidb-operator/values.yaml` 文件的 `controllerManager.autoFailover` 为 `true`：

```shell
controllerManager:
 serviceAccount: tidb-controller-manager
 logLevel: 2
 replicas: 1
 resources:
   limits:
     cpu: 250m
     memory: 150Mi
   requests:
     cpu: 80m
     memory: 50Mi
 # autoFailover is whether tidb-operator should auto failover when failure occurs
 autoFailover: true
 # pd failover period default(5m)
 pdFailoverPeriod: 5m
 # tikv failover period default(5m)
 tikvFailoverPeriod: 5m
 # tidb failover period default(5m)
 tidbFailoverPeriod: 5m
```

`pdFailoverPeriod`，`tikvFailoverPeriod`，`tidbFailoverPeriod` 默认都为 5 分钟，它们的含义是在确认实例故障后的等待超时时间，超过这个时间后，Operator 就开始做自动的故障转移。

# 实现原理

TiDB 集群有 PD/TiKV/TiDB 三个组件，它们各自的故障转移策略又有不同，下面分别做介绍：

## PD 故障转移策略：

假设 PD 集群有 3 个节点，如果一个 PD 节点挂掉超过 5 分钟（pdFailoverPeriod 可配置），Operator 首先会将这个 PD 节点下线，然后再添加一个新的 PD 节点。此时会有 4 个 Pod 同时存在，待挂掉的 PD 节点恢复后，Operator 会将新启动的节点删除掉，恢复成原来的 3 个节点。

## TiKV 故障转移策略：

当一个 TiKV 节点无法正常工作后，该 TiKV 节点的状态会变为 Disconnected，30 分钟后会变成 Down 状态，Operator 会在此基础上再等待 5 分钟（tikvFailoverPeriod 可配置），如果该 TiKV 节点仍不能恢复，就会新起一个 TiKV 节点。待挂掉的 TiKV 节点恢复后，Operator 不会自动删除新起的节点，用户需要通过手工减少 TiKV 节点，恢复成原来的节点数，操作方法如下：

```shell
kubectl patch tc -n <namespace> <clusterName> --type='json' -p='[{"op": "remove", "path": "/status/tikv/failureStores"}]'
```

## TiDB 故障转移策略：

假设 TiDB 集群有 3 个节点，TiDB 的故障转移策略跟 k8s Deployment 的是一致的，如果一个 TiDB 节点挂掉超过 5 分钟（tidbFailoverPeriod 可配置），Operator 会添加一个新的 TiDB 节点。此时会有 4 个 Pod 同时存在，待挂掉的 TiDB 节点恢复后，Operator 会将新启动的节点删除掉，恢复成原来的 3 个节点。
