---
title: Maintain Kubernetes Nodes that Hold the TiDB Cluster
summary: Learn how to maintain Kubernetes nodes that hold the TiDB cluster.
category: how-to
aliases: ['/docs/v3.0/how-to/maintain/tidb-in-kubernetes/k8s-node-for-tidb/']
---

# Maintain Kubernetes Nodes that Hold the TiDB Cluster

TiDB is a highly available database that can run smoothly when some of the database nodes go offline. For this reason, you can safely shut down and maintain the Kubernetes nodes at the bottom layer without influencing TiDB's service. Specifically, you need to adopt various maintenance strategies when handling nodes that hold PD, TiKV, and TiDB instances because of their different features.

This document introduces how to perform a temporary or long-term maintenance task for the Kubernetes nodes.

## Prerequisites

- [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [`tkctl`](/v3.0/tidb-in-kubernetes/reference/tools/tkctl.md)
- [`jq`](https://stedolan.github.io/jq/download/)

> **Note:**
>
> Before you perform a long-term node maintenance, you need to make sure that the remaining resources in the Kubernetes cluster are enough for running the TiDB cluster.

## Maintain nodes that hold PD and TiDB instances

Migrating PD and TiDB instances from a node is relatively fast, so you can proactively evict the instances to other nodes and perform maintenance on the desired node:

1. Check whether there is any TiKV instance on the node to be maintained:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pod --all-namespaces -o wide | grep <node-name>
    ```

    If any TiKV instance is found, see [Maintain nodes that hold TiKV instances](#maintain-nodes-that-hold-tikv-instances).

2. Use the `kubectl cordon` command to prevent new Pods from being scheduled to the node to be maintained:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl cordon <node-name>
    ```

3. Use the `kubectl drain` command to migrate the database instances on the maintenance node to other nodes:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl drain <node-name> --ignore-daemonsets --delete-local-data
    ```

    After running this command, TiDB instances on this node are automatically migrated to another available node, and the PD instance will trigger the auto-failover mechanism after five minutes and complete the nodes.

4. At this time, if you want to make this Kubernetes node offline, you can delete it by running:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete node <node-name>
    ```

    If you want to recover a Kubernetes node, you need to first make sure that it is in a healthy state:

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl get node <node-name>
    ```

    After the node goes into the `Ready` state, you can proceed with the following operations.

5. Use `kubectl uncordon` to lift the scheduling restriction on the node:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl uncordon <node-name>
    ```

6. See whether all Pods get back to normal and are running:

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl get -n $namespace pod -o wide
    ```

    Or:

    {{< copyable "shell-regular" >}}

    ```sql
    watch tkctl get all
    ```

    When you confirm that all Pods are running normally, then you have successfully finished the maintenance task.

## Maintain nodes that hold TiKV instances

Migrating TiKV instances is relatively slow and might lead to unwanted data migration load on the cluster. For this reason, you need to choose different strategies as needed prior to maintaining the nodes that hold TiKV instances:

- If you want to maintain a node that is recoverable in a short term, you can recover the TiKV node from where it is after the maintenance without migrating it elsewhere.
- If you want to maintain a node that is not recoverable in a short term, you need to make a plan for the TiKV migration task.

### Maintain a recoverable node in a short term

For a short-term maintenance, you can increase the TiKV instance downtime that the cluster allows by adjusting the `max-store-down-time` configuration of the PD cluster. You can finish the maintenance and recover the Kubernetes node during this time, and then all TiKV instances on this node will be automatically recovered.

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward svc/<CLUSTER_NAME>-pd 2379:2379
```

{{< copyable "shell-regular" >}}

```shell
pd-ctl -d config set max-store-down-time 10m
```

After configuring `max-store-down-time` to an appropriate value, the follow-up operations are the same as those in [Maintain nodes that hold PD and TiDB instances](#maintain-nodes-that-hold-pd-and-tidb-instances).

### Maintain an irrecoverable node in a short term

For the maintenance on an node that cannot be recovered in a short term (for example, a node has to go offline for a long time), you need to use `pd-ctl` to proactively tell the TiDB cluster to make the corresponding TiKV instances offline, and manually unbind the instances from the node.

1. Use `kubectl cordon` to prevent new Pods from being scheduled to the node to be maintained:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl cordon <node-name>
    ```

2. Check the TiKV instance on the maintenance node:

    {{< copyable "shell-regular" >}}

    ```shell
    tkctl get -A tikv | grep <node-name>
    ```

3. Use `pd-ctl` to proactively put the TiKV instance offline:

    > **Note:**
    >
    > Before you make the TiKV instances offline, you need to make sure that the number of remaining TiKV instances in the cluster is no smaller than the number of TiKV replicas in the PD configuration (configuration item: `max-replicas`). If this is not the case, you need to scale TiKV first.

    Check `store-id` of the TiKV instance:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get tc <CLUSTER_NAME> -ojson | jq '.status.tikv.stores | .[] | select ( .podName == "<POD_NAME>" ) | .id'
    ```

    Make the TiKV instance offline:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl port-forward svc/<CLUSTER_NAME>-pd 2379:2379
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    pd-ctl -d store delete <ID>
    ```

4. Wait for the store to change its status from `state_name` to `Tombstone`:

    {{< copyable "shell-regular" >}}

    ```shell
    watch pd-ctl -d store <ID>
    ```

5. Unbind the TiKV instance from the local drive of the node:

    Get the `PesistentVolumeClaim` used by the Pod:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> pod <pod_name> -ojson | jq '.spec.volumes | .[] | select (.name == "tikv") | .persistentVolumeClaim.claimName'
    ```

    Delete the `PesistentVolumeClaim`:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete -n <namespace> pvc <pvc_name>
    ```

6. Delete the TiKV instance:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete -n <namespace> pod <pod_name>
    ```

7. Check whether the TiKV instance is normally scheduled to another node:

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n <namespace> get pod -o wide
    ```

    If there are more TiKV instances on the maintenance node, you need to follow the above steps until all instances are migrated to other nodes.

8. After you make sure that there is no more TiKV instance on the node, you can evict other instances on the node:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl drain <node-name> --ignore-daemonsets --delete-local-data
    ```

9. Confirm again that there is no more TiKV, TiDB and PD instances running on this node:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pod --all-namespaces | grep <node-name>
    ```

10. (Optional) If this node is made offline for a long time, it is recommended to delete it from the Kubernetes cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    kuebctl delete node <node-name>
    ```

Now, you have successfully finished the maintenance task for the node.
