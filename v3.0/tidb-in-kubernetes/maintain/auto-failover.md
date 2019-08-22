---
title: Automatic Failover
summary: Learn the automatic failover policies of TiDB cluster components on Kubernetes.
category: how-to
aliases: ['/docs/v3.0/how-to/maintain/tidb-in-kubernetes/auto-failover/']
---

# Automatic Failover

Automatic failover means that when a node in the TiDB cluster fails, TiDB Operator automatically adds a new one to ensure the high availability of the cluster. It works similarly with the `Deployment` behavior in Kubernetes.

TiDB Operator manages Pods based on `StatefulSet`, which does not automatically create a new node to replace the original node when a Pod goes down. For this reason, the automatic failover feature is added to TiDB Operator, which expands the behavior of `StatefulSet`.

The automatic failover feature is disabled by default in TiDB Operator. You can enable it by setting `controllerManager.autoFailover` to `true` in the `charts/tidb-operator/values.yaml` file when deploying TiDB Operator:

```yaml
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

By default, `pdFailoverPeriod`, `tikvFailoverPeriod` and `tidbFailoverPeriod` are set to be 5 minutes, which is the waiting timeout after an instance failure is identified. After this time, TiDB Operator begins the automatic failover process.

## Automatic failover policies

There are three components in a TiDB cluster - PD, TiKV, and TiDB, each of which has its own automatic failover policy. This section gives an in-depth introduction to these policies.

### Failover with PD

Assume that there are 3 nodes in a PD cluster. If a PD node is down for over 5 minutes (configurable by modifying `tidbFailoverPeriod`), TiDB Operator takes this node offline first, and creates a new PD node. At this time, there are 4 nodes in the cluster. If the failed PD node gets back online, TiDB Operator deletes the newly created node and the number of nodes gets back to 3.

### Failover with TiKV

When a TiKV node fails, its status turns to `Disconnected`. After 30 minutes (configurable by modifying `pd.maxStoreDownTime` when deploying the cluster), it turns to `Down`. After waiting for 5 minutes (configurable by modifying `tikvFailoverPeriod`), TiDB Operator creates a new TiKV node if this TiKV node is still down. If the failed TiKV node gets back online, TiDB Operator does not automatically delete the newly created node, and you need to manually drop it and restore the original number of nodes. To do this, you can delete the TiKV node from the `status.tikv.failureStores` field of the `TidbCluster` object:

{{< copyable "shell-regular" >}}

```shell
kubectl edit tc -n <namespace> <clusterName>
```

```
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

After the `cluster1-tikv-0` node turns back to normal, you can delete it as shown below:

```
...
status
  tikv:
    failureStores:
      "2":
        podName: cluster1-tikv-1
        storeID: "2"
...
```

### Failover with TiDB

The TiDB automatic failover policy works the same way as `Deployment` does in Kubernetes. Assume that there are 3 nodes in a TiDB cluster. If a TiDB node is down for over 5 minutes (configurable by modifying `tidbFailoverPeriod`), TiDB Operator creates a new TiDB node. At this time, there are 4 nodes in the cluster. When the failed TiDB node gets back online, TiDB Operator deletes the newly created node and the number of nodes gets back to 3.
