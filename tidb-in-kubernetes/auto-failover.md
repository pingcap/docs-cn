---
title: 故障自动转移
category: how-to
---

# 故障自动转移

故障自动转移是指在 TiDB 集群的某些节点出现故障时，TiDB Operator 会自动添加一个节点，保证 TiDB 集群的高可用，类似于 K8s 的 Deployment 行为。

由于 TiDB Opererator 基于 StatefulSet 来管理 Pod，但 StatefulSet 在某些 Pod 发生故障时不会自动创建新节点来替换旧节点，所以，TiDB Operator 扩展了 StatefulSet 的这种行为，添加了 failover 功能。

Auto Failover 功能在 TiDB Opererator 中默认关闭，需要在部署 TiDB Opererator 时开启，开启方法为设置 `charts/tidb-operator/values.yaml` 文件的 `controllerManager.autoFailover` 为 `true`：

{{< copyable "shell-regular" >}}

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

`pdFailoverPeriod`，`tikvFailoverPeriod`，`tidbFailoverPeriod` 默认均为 5 分钟，它们的含义是在确认实例故障后的等待超时时间，超过这个时间后， TiDB Operator 就开始做自动的故障转移。

## 实现原理

TiDB 集群有 PD/TiKV/TiDB 三个组件，它们各自的故障转移策略又有不同，本节将详细介绍。

### PD 故障转移策略

假设 PD 集群有 3 个节点，如果一个 PD 节点挂掉超过 5 分钟（pdFailoverPeriod 可配置），Operator 首先会将这个 PD 节点下线，然后再添加一个新的 PD 节点。此时会有 4 个 Pod 同时存在，待挂掉的 PD 节点恢复后，TiDB Operator 会将新启动的节点删除掉，恢复成原来的 3 个节点。

### TiKV 故障转移策略

当一个 TiKV 节点无法正常工作后，该 TiKV 节点的状态会变为 Disconnected，30 分钟（可在部署集群时通过修改 `pd.maxStoreDownTime` 来配置）后会变成 Down 状态，TiDB Operator 会在此基础上再等待 5 分钟（tikvFailoverPeriod 可配置），如果该 TiKV 节点仍不能恢复，就会新起一个 TiKV 节点。待挂掉的 TiKV 节点恢复后，TiDB Operator 不会自动删除新起的节点，用户需要通过手工减少 TiKV 节点，恢复成原来的节点数，操作方法是将该 TiKV 节点从 `TidbCluster` 对象的 `status.tikv.failureStores` 字段中删除：

{{< copyable "shell-regular" >}}

```shell
kubectl edit tc -n <namespace> <clusterName>
...
status
  tikv:
    failureStores:
      "1":
        podName: cluster1-tikv-0
        storeID: "1"
      "2":
        podName: cluster1-tikv-1
        storeID: "2"
...
```

`cluster1-tikv-0` 节点恢复后，将其删除后变为：

{{< copyable "shell-regular" >}}

```shell
...
status
  tikv:
    failureStores:
      "2":
        podName: cluster1-tikv-1
        storeID: "2"
...
```

### TiDB 故障转移策略

假设 TiDB 集群有 3 个节点，TiDB 的故障转移策略跟 k8s Deployment 的是一致的，如果一个 TiDB 节点挂掉超过 5 分钟（tidbFailoverPeriod 可配置），Operator 会添加一个新的 TiDB 节点。此时会有 4 个 Pod 同时存在，待挂掉的 TiDB 节点恢复后，Operator 会将新启动的节点删除掉，恢复成原来的 3 个节点。
