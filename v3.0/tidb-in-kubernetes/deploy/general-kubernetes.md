---
title: Deploy TiDB on General Kubernetes
summary: Learn how to deploy a TiDB cluster on general Kubernetes.
category: how-to
aliases: ['/docs/v3.0/how-to/deploy/tidb-in-kubernetes/general-kubernetes/']
---

# Deploy TiDB on General Kubernetes

This document describes how to deploy a TiDB cluster on general Kubernetes.

## Prerequisites

- [Deploy TiDB Operator](/v3.0/tidb-in-kubernetes/deploy/tidb-operator.md);
- [Install Helm](/v3.0/tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) and configure it with the official PingCAP chart.

## Configure TiDB cluster

Use the following commands to get the `values.yaml` configuration file of the tidb-cluster chart to be deployed.

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/<release-name> && \
helm inspect values pingcap/tidb-cluster --version=<chart-version> > /home/tidb/<release-name>/values-<release-name>.yaml
```

> **Note:**
>
> - You can replace `/home/tidb` with any directory as you like.
> - `release-name` is the prefix of resources used by TiDB in Kubernetes (such as Pod, Service, etc.). You can give it a name that is easy to memorize but this name must be *globally unique*. You can view existing `release-name`s in the cluster by running the `helm ls -q` command.
> - `chart-version` is the version released by the `tidb-cluster` chart. You can view the currently supported versions by running the `helm search -l tidb-cluster` command.
> - In the rest of this document, `values.yaml` refers to `/home/tidb/<release-name>/values-<releaseName>.yaml`.

### Storage class

The TiDB cluster uses `local-storage` by default.

- For the production environment, local storage is recommended. The actual local storage in Kubernetes clusters might be sorted by disk types, such as `nvme-disks` and `sas-disks`.
- For the demonstration environment or functional verification, you can use network storage, such as `ebs` and `nfs`.

Different components of a TiDB cluster have different disk requirements. Before deploying a TiDB cluster, select the appropriate storage class for each component according to the storage classes supported by the current Kubernetes cluster and usage scenario. You can set the storage class by modifying `storageClassName` of each component in `values.yaml`. For the [storage classes](/v3.0/tidb-in-kubernetes/reference/configuration/local-pv.md) supported by the Kubernetes cluster, check with your system administrator.

> **Note:**
>
> If you set a storage class that does not exist in the TiDB cluster that you are creating, then the cluster creation goes to the Pending state. In this situation, you must [destroy the TiDB cluster in Kubernetes](/v3.0/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md).

### Cluster topology

If you set up a storage class that does not exist in the TiDB cluster that you are creating, then the cluster creation is in the Pending state. In this situation, you must [destroy the TiDB cluster in Kubernetes](/v3.0/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md).

The deployed cluster topology by default has 3 PD Pods, 3 TiKV Pods, 2 TiDB Pods, and 1 Monitor Pod. In this deployment topology, the scheduler extender of TiDB Operator requires at least 3 nodes in the Kubernetes cluster to provide high availability. If the number of Kubernetes cluster nodes is less than 3, 1 PD Pod goes to the Pending state, and neither TiKV Pods nor TiDB Pods are created.

When the number of nodes in the Kubernetes cluster is less than 3, to start the TiDB cluster, you can reduce both the number of PD Pods and TiKV Pods in the default deployment to `1`, or modify the `schedulerName` in `values.yaml` to `default-scheduler`, a built-in scheduler in Kubernetes.

> **Warning:**
>
> `default-scheduler` is only applicable to the demonstration environment. After `schedulerName` is modified to `default-scheduler`, the scheduling of TiDB clusters neither guarantees high availability of data nor supports features such as [TiDB stable scheduling](https://github.com/pingcap/tidb-operator/blob/master/docs/design-proposals/tidb-stable-scheduling.md).

For more configuration parameters, see [TiDB cluster configurations in Kubernetes](/v3.0/tidb-in-kubernetes/reference/configuration/tidb-cluster.md).

## Deploy TiDB Cluster

After you deploy and configure TiDB Operator, deploy the TiDB cluster using the following commands:

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f /home/tidb/<release-name>/values-<release-name>.yaml
```

You can view the Pod status using the following command:

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n <namespace> -l app.kubernetes.io/instance=<release-name>
```

You can use TiDB Operator to deploy and manage multiple sets of TiDB clusters in a single Kubernetes cluster by repeating the above command and replacing `release-name` with a different name. Different clusters can be in the same or different `namespace`. You can select different clusters according to your actual needs.