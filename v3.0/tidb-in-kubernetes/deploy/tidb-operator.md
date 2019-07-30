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
> + Although TiDB Operator can use network volume to persist TiDB data, this process could be very slow due to the redundant replication. It is highly recommended to set up [local volume](https://kubernetes.io/docs/concepts/storage/volumes/#local) for better performance.
>
> + Network volumes in a multi-availability zone setup require Kubernetes v1.12 or higher version. It is recommended to use networked volumes to store backup data in `tidb-bakup` chart.

## Deploy Kubernetes cluster

TiDB Operator runs in Kubernetes cluster. You can use one of the methods listed [here](https://kubernetes.io/docs/setup/pick-right-solution/) to set up a Kubernetes cluster. Make sure that the Kubernetes version is v1.10 or higher. If you are using AWS, GKE or local machine, here are quick-start tutorials:

* [Local DinD tutorial](/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind.md)
* [Google GKE tutorial](/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-gke.md)
* [AWS EKS tutorial](/tidb-in-kubernetes/deploy/aws-eks.md)

If you are deploying in a different environment, a proper DNS addon must be installed in the Kubernetes cluster. You can follow the [official documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/) to set up a DNS addon.

TiDB Operator uses [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to persist the data of TiDB cluster (including the database, monitoring data, backup data), so the Kubernetes cluster must provide at least one kind of persistent volume. For better performance, it is recommended to use local SSD disk as the volumes. Follow [this step](#configure-local-persistent-volume) to auto-provision local persistent volumes.

It is suggested to enable [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) in the Kubernetes cluster. Otherwise, you need to set `rbac.create` to `false` in the `values.yaml` of both `tidb-operator` and `tidb-cluster` charts.

Because TiDB uses many file descriptors by default, the [worker node](https://access.redhat.com/solutions/61334) and its Docker daemon's `ulimit` must be configured to `1048576` or bigger:

{{< copyable "shell-regular" >}}

```shell
sudo vim /etc/systemd/system/docker.service
```

Set `LimitNOFILE` to `1048576` or bigger.

## Install Helm

Refer to [Use Helm](/tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) to install Helm and configre it with the official PingCAP chart Repo.

## Configure Local Persistent Volume

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

TiDB Operator uses [CRD](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/) to extend Kubernetes. Therefore, to use TiDB Operator, you should first create `TidbCluster` custom resource, which is a one-time job in your Kubernetes cluster.

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/crd.yaml && \
kubectl get crd tidbclusters.pingcap.com
```

After `TidbCluster` custom resource is created, install TiDB Operator in your Kubernetes cluster.

> **Note:**
>
> `<chartVersion>` will be used in the rest sections of the documents to represent the chart version. For example, `v1.0.0`.

Use the following command to get the `values.yaml` file of the `tidb-operator` chart you want to install:

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/tidb-operator && \
helm inspect values pingcap/tidb-operator --version=<chartVersion> > /home/tidb/tidb-operator/values-tidb-operator.yaml
```

Set `scheduler.kubeSchedulerImage` in the `/home/tidb/tidb-operator/values-tidb-operator.yaml` file as same as the image of your kubernetes cluster.

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=<chartVersion> -f /home/tidb/tidb-operator/values-tidb-operator.yaml && \
kubectl get po -n tidb-admin -l app.kubernetes.io/name=tidb-operator
```

## Customize TiDB Operator

To customize TiDB Operator, modify `/home/tidb/tidb-operator/values-tidb-operator.yaml`. The rest sections of the document use `values.yaml` to refer to `/home/tidb/tidb-operator/values-tidb-operator.yaml`

TiDB Operator contains two components:

* tidb-controller-manager
* tidb-scheduler

These two components are stateless and deployed via `Deployment`. You can customize `replicas` and resource limits/requests as you wish in the `values.yaml`.

After modifying `values.yaml`, run the following command to apply this modification:

{{< copyable "shell-regular" >}}

```shell
helm upgrade tidb-operator pingcap/tidb-operator --version=<chartVersion> -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```
