---
title: Deploy TiDB Operator in Kubernetes
summary: Learn how to deploy TiDB Operator in Kubernetes.
category: how-to
---

# Deploy TiDB Operator in Kubernetes

This document describes how to deploy TiDB Operator in Kubernetes.

## Prerequisites

Before deploying TiDB Operator, make sure the following items are installed on your machine:

* Kubernetes >= v1.10
* [DNS addons](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/)
* [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) enabled (optional)
* [Helm](https://helm.sh) version >= v2.8.2 and < v3.0.0
* Kubernetes v1.12 or later version is required for zone-aware persistent volumes.

> **Note:** 
>
> + Although TiDB Operator can use network volume to persist TiDB data, this process could be very slow due to the redundant replication. It is highly recommended to set up [local volume](https://kubernetes.io/docs/concepts/storage/volumes/#local) for better performance.
>
> + Network volumes in a multi-availability zone setup require Kubernetes v1.12 or higher version. It is recommended to use networked volumes to store backup data in `tidb-bakup` chart.

## Deploy Kubernetes cluster

TiDB Operator runs in Kubernetes cluster. You can use one of the methods listed [here](https://kubernetes.io/docs/setup/pick-right-solution/) to set up a Kubernetes cluster. Make sure that the Kubernetes version is v1.10 or higher. If you are using AWS, GKE or local machine, here are quick-start tutorials:

* [Local DinD tutorial](/how-to/get-started/deploy-tidb-from-kubernetes-dind.md)
* [Google GKE tutorial](/how-to/get-started/deploy-tidb-from-kubernetes-gke.md)
* [AWS EKS tutorial](/how-to/deploy/orchestrated/tidb-in-kubernetes/aws-eks.md)

If you are deploying in a different environment, a proper DNS addon must be installed in the Kubernetes cluster. You can follow the [official documentation](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/) to set up a DNS addon.

TiDB Operator uses [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to persist the data of TiDB cluster (including the database, monitoring data, backup data), so the Kubernetes cluster must provide at least one kind of persistent volume. For better performance, it is recommended to use local SSD disk as the volumes. Follow [this step](#local-persistent-volume) to auto-provision local persistent volumes.

It is suggested to enable [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) in the Kubernetes cluster. Otherwise, you need to set `rbac.create` to `false` in the `values.yaml` of both `tidb-operator` and `tidb-cluster` charts.

Because TiDB uses many file descriptors by default, the [worker node](https://access.redhat.com/solutions/61334) and its Docker daemon's `ulimit` must be configured to `1048576` or bigger:


{{< copyable "shell-regular" >}}

```shell
sudo vim /etc/systemd/system/docker.service
```

Set `LimitNOFILE` to `1048576` or bigger.

## Install Helm

You can follow the Helm [official documentation](https://helm.sh) to install Helm in your Kubernetes cluster. The following instructions are listed here for quick reference:

1. Install helm client

    {{< copyable "shell-regular" >}}

    ```shell
    curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
    ```

    Or if on macOS, you can use homebrew to install Helm by `brew install kubernetes-helm`.

2. Install Helm server

   Make sure that tiller pod is running.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/tiller-rbac.yaml && \
    helm init --service-account=tiller --upgrade
    ```
   
   Confirm that the tiller pod is in the `running` state by the following command:
   
   {{< copyable "shell-regular" >}}
   
    ```shell
    kubectl get po -n kube-system -l name=tiller
    ```

   If `RBAC` is not enabled for the Kubernetes cluster, then `helm init --upgrade` should be enough.
   
3. Add Helm repo

   PingCAP Helm repo houses PingCAP managed charts, such as tidb-operator, tidb-cluster and tidb-backup, etc. Add and check the repo with following commands:
   
    {{< copyable "shell-regular" >}}
   
    ```shell
    helm repo add pingcap http://charts.pingcap.org/ && \
    helm repo list
    ```

   Then you can check the avaliable charts:
   
    {{< copyable "shell-regular" >}}
   
    ```shell
    helm repo update && \
    helm search tidb-cluster -l && \
    helm search tidb-operator -l
    ```
    
## Local Persistent Volume

### Prepare local volumes

See the [operation guide in sig-storage-local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) which explains how to set up and clean up local volumes on the nodes.

Also see [best practices](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md) for production environment.

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
> `${chartVersion}` will be used in the rest sections of the documents to represent the chart version. For example, `v1.0.0-beta.3`.

Use the following command to get the `values.yaml` file of the `tidb-operator` chart you want to install:

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/tidb-operator && \
helm inspect values pingcap/tidb-operator --version=${chartVersion} > /home/tidb/tidb-operator/values-tidb-operator.yaml
```

Set `scheduler.kubeSchedulerImage` in the `/home/tidb/tidb-operator/values-tidb-operator.yaml` file as same as the image of your kubernetes cluster.

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=${chartVersion} -f /home/tidb/tidb-operator/values-tidb-operator.yaml && \
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
helm upgrade tidb-operator pingcap/tidb-operator --version=${chartVersion} -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```

## Upgrade TiDB Operator

To upgrade TiDB Operator, modify the image version in the `values.yaml` file and then run `helm upgrade`:

{{< copyable "shell-regular" >}}

```shell
helm upgrade tidb-operator pingcap/tidb-operator --version=${chartVersion} -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```

When a new version of `tidb-operator` is released, you only need to update `operatorImage` in `values.yaml` and run the above command. But to guarantee safety, you must get the new `values.yaml` file from the new `tidb-operator` chart and merge the old `values.yaml` file with the new one. And then upgrade as above.

TiDB Operator is used for maintaining TiDB cluster. This means that when TiDB cluster is up and running, you can even stop TiDB Operator without affecting TiDB cluster that works well until you need to maintain the cluster for scaling, upgrading, etc.

## Upgrade Kubernetes

When there is a major version upgrade of Kubernetes, you need to make sure that `kubeSchedulerImageTag` matches the version. By default, this value is generated by Helm during the installation or upgrade process. To reset this value, execute `helm upgrade`.
