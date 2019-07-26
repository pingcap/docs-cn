---
Title: Scale TiDB in Kubernetes
summary: Learn how to horizontally and vertically scale up and down a TiDB cluster in Kubernetes.
Category: how-to
---

# Scale TiDB in Kubernetes

This document introduces how to horizontally and vertically scale up and down a TiDB cluster in Kubernetes.

## Horizontal scaling

Horizontally scaling TiDB means that you scale TiDB up or down by adding or remove nodes in your pool of resources. When you scale a TiDB cluster, PD, TiKV, and TiDB are scaled up or down sequentially according to the values of their replicas. Scaling up operations add nodes based on the node ID in ascending order, while scaling down operations remove nodes based on the node ID in descending order.

### Horizontal scaling operations

To perform a horizontal scaling operation:

1. Modify `pd.replicas`, `tidb.replicas`, `tikv.replicas` in the `value.yaml` file of the cluster to a desired value.

2. Run the `helm upgrade` command to scale up or down:

    {{< copyable "shell-regular" >}}

    ```shell
    Helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

3. View the cluster's scaling status:

    {{< copyable "shell-regular" >}}

    ```shell
    Watch kubectl -n ${namespace} get pod -o wide
    ```

    When the number of Pods for all components reaches the preset value and all components are in the `Running` state, the horizontal scaling is completed.

> **Note:**
>
> - The PD and TiKV components do not trigger scaling up and down operations during the rolling update.
> - When being scaled down, the PD and TiKV components call the corresponding interface to take offline the PD and TiKV nodes being deleted. This involves data migration operations, so it might take some time to finish the process.
> - The PVC of the deleted node is retained during the scaling down process, and because the PV's `Reclaim Policy` is set to `Retain`, the data can be retrieved even if the PVC is deleted.

## Vertical scaling

Vertically scaling TiDB means that you scale TiDB up or down by increasing or decreasing the limit of resources on the node. Vertically scaling is essentially the rolling update of the nodes.

### Vertical scaling operations

To perform a vertical scaling operation:

1. Modify `tidb.resources`, `tikv.resources`, `pd.resources` in the `values.yaml` file to a desired value.

2. Run the `helm upgrade` command to upgrade:

    {{< copyable "shell-regular" >}}

    ```shell
    Helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

3. View the progress of the upgrade:

    {{< copyable "shell-regular" >}}

    ```shell
    Watch kubectl -n ${namespace} get pod -o wide
    ```

    When all Pods are rebuilt and in the `Running` state, the vertical scaling is completed.

> **Note:**
>
> - If the resource's `requests` field is modified during the vertical scaling process, because PD and TiKV use `Local PV`, they need to be scheduled back to the original node after the upgrade. At this time, if the original node does not have enough resources, the Pod ends up staying in the `Pending` status and thus impacts the service.
> - TiDB is a horizontally scalable database, so it is recommended to take advantage of this strength rather than overlaying resources like you do with a traditional database.
