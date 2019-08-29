---
title: Deploy TiDB Operator in Kubernetes
summary: Learn how to deploy TiDB Operator in Kubernetes.
category: how-to
---

# Deploy TiDB Operator in Kubernetes

This document describes how to deploy TiDB Operator in Kubernetes.

## Prerequisites

Before deploying TiDB Operator, make sure the following items are installed on your machine:

* Kubernetes >= v1.12
* [DNS addons](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/)
* [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) enabled (optional)
* [Helm](https://helm.sh) version >= v2.8.2 and < v3.0.0

> **Note:**
>
> - Although TiDB Operator can use network volume to persist TiDB data, this can affect performance a lot because TiDB stores multiple replicas itself. So it is highly recommended to set up [local volume](https://kubernetes.io/docs/concepts/storage/volumes/#local) for better performance.
>
> - Network volumes in a multi-availability zone setup require Kubernetes v1.12 or higher version. It is recommended to use networked volumes to store backup data in `tidb-bakup` chart.

## Deploy Kubernetes cluster

TiDB Operator runs in Kubernetes cluster. You can refer to [the document of how to set up Kubernetes](https://kubernetes.io/docs/setup/) to set up a Kubernetes cluster. Make sure that the Kubernetes version is v1.12 or higher. If you are using AWS, GKE or local machines, here are quick-start tutorials:

* [Local DinD tutorial](/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind.md)
* [Google GKE tutorial](/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-gke.md)
* [AWS EKS tutorial](/tidb-in-kubernetes/deploy/aws-eks.md)

If you are deploying in a different environment, a proper DNS addon must be installed in the Kubernetes cluster. You can follow the [official documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/) to set up a DNS addon.

TiDB Operator uses [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to persist the data of TiDB cluster (including the database, monitoring data, backup data), so the Kubernetes cluster must provide at least one kind of persistent volume. For better performance, it is recommended to use local SSD disk as the volumes. Follow [this step](#configure-local-persistent-volume) to auto-provision local persistent volumes.

It is suggested to enable [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) in the Kubernetes cluster. Otherwise, you need to set `rbac.create` to `false` in the `values.yaml` of both `tidb-operator` and `tidb-cluster` charts.

Because TiDB uses many file descriptors by default, the worker node and its Docker daemon's `ulimit` values must be greater than or equal to `1048576`.

1. Configure the `ulimit` value of the work node. See [How to set `ulimit` values](https://access.redhat.com/solutions/61334).

    {{< copyable "shell-regular" >}}

    ```shell
    sudo vim /etc/security/limits.conf
    ```

    Set the `nofile` values of `soft` and `hard` of the root account to be greater than or equal to `1048576`.

2. Configure the `ulimit` value of the Docker service.

    {{< copyable "shell-regular" >}}

    ```shell
    sudo vim /etc/systemd/system/docker.service
    ```

    Set `LimitNOFILE` to be greater than or equal to `1048576`.

## Install Helm

Refer to [Use Helm](/tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) to install Helm and configre it with the official PingCAP chart Repo.

## Configure local persistent volume

### Prepare local volumes

Refer to [Local PV Configuration](/tidb-in-kubernetes/reference/configuration/local-pv.md) to set up local persistent volumes in your Kubernetes cluster.

### Deploy local-static-provisioner

After mounting all data disks on Kubernetes nodes, you can deploy [local-volume-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) that can automatically provision the mounted disks as Local PersistentVolumes.

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml
```

Check the Pod and PV status with the following commands:

{{< copyable "shell-regular" >}}

```shell
kubectl get po -n kube-system -l app=local-volume-provisioner && \
kubectl get pv | grep local-storage
```

The local-volume-provisioner creates a volume for each mounted disk. Note that on GKE, this will create local volumes of only 375GiB in size and that you need to manually alter the setup to create larger disks.

## Install TiDB Operator

TiDB Operator uses [CRD (Custom Resource Definition)](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/) to extend Kubernetes. Therefore, to use TiDB Operator, you must first create the `TidbCluster` custom resource type, which is a one-time job in your Kubernetes cluster.

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/crd.yaml && \
kubectl get crd tidbclusters.pingcap.com
```

After `TidbCluster` custom resource type is created, install TiDB Operator in your Kubernetes cluster.

1. Get the `values.yaml` file of the `tidb-operator` chart you want to install.

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /home/tidb/tidb-operator && \
    helm inspect values pingcap/tidb-operator --version=<chart-version> > /home/tidb/tidb-operator/values-tidb-operator.yaml
    ```

    > **Note:**
    >
    > `<chart-version>` represents the chart version of TiDB Operator. For example, `v1.0.0`. You can view the currently supported versions by running the `helm search -l tidb-operator` command.

2. Install TiDB Operator.

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=<chart-version> -f /home/tidb/tidb-operator/values-tidb-operator.yaml && \
    kubectl get po -n tidb-admin -l app.kubernetes.io/name=tidb-operator
    ```

## Customize TiDB Operator

To customize TiDB Operator, modify `/home/tidb/tidb-operator/values-tidb-operator.yaml`. The rest sections of the document use `values.yaml` to refer to `/home/tidb/tidb-operator/values-tidb-operator.yaml`

TiDB Operator contains two components:

* tidb-controller-manager
* tidb-scheduler

These two components are stateless and deployed via `Deployment`. You can customize resource `limit`, `request`, and `replicas` in the `values.yaml` file.

After modifying `values.yaml`, run the following command to apply this modification:

{{< copyable "shell-regular" >}}

```shell
helm upgrade tidb-operator pingcap/tidb-operator --version=<chart-version> -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```
