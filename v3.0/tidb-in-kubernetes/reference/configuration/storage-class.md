---
title: Kubernetes 上的持久化存储类型配置
category: reference
aliases: ['/docs-cn/v3.0/tidb-in-kubernetes/reference/configuration/local-pv/']
---

# Kubernetes 上的持久化存储类型配置

TiDB 集群中 PD、TiKV、监控等组件以及 TiDB Binlog 和备份等工具都需要使用将数据持久化的存储。Kubernetes 上的数据持久化需要使用 [PersistentVolume (PV)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)。Kubernetes 提供多种[存储类型](https://kubernetes.io/docs/concepts/storage/volumes/)，主要分为两大类：

* 网络存储

    存储介质不在当前节点，而是通过网络方式挂载到当前节点。一般有多副本冗余提供高可用保证，在节点出现故障时，对应网络存储可以再挂载到其它节点继续使用。

* 本地存储

    存储介质在当前节点，通常能提供比网络存储更低的延迟，但没有多副本冗余，一旦节点出故障，数据就有可能丢失。如果是 IDC 服务器，节点故障可以一定程度上对数据进行恢复，但公有云上使用本地盘的虚拟机在节点故障后，数据是**无法找回**的。

PV 一般由系统管理员或 volume provisioner 自动创建，PV 与 Pod 是通过 [PersistentVolumeClaim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims) 进行关联的。普通用户在使用 PV 时并不需要直接创建 PV，而是通过 PVC 来申请使用 PV，对应的 volume provisioner 根据 PVC 创建符合要求的 PV，并将 PVC 与该 PV 进行绑定。

> **警告：**
>
> 为了数据安全，任何情况下都不要直接删除 PV，除非对 volume provisioner 原理非常清楚。

## TiDB 集群推荐存储类型

TiKV 自身借助 Raft 实现了数据复制，出现节点故障后，PD 会自动进行数据调度补齐缺失的数据副本，同时 TiKV 要求存储有较低的读写延迟，所以生产环境强烈推荐使用本地 SSD 存储。

PD 同样借助 Raft 实现了数据复制，但作为存储集群元信息的数据库，并不是 IO 密集型应用，所以一般本地普通 SAS 盘或网络 SSD 存储（例如 AWS 上 gp2 类型的 EBS 存储卷，GCP 上的持久化 SSD 盘）就可以满足要求。

监控组件以及 TiDB Binlog、备份等工具，由于自身没有做多副本冗余，所以为保证可用性，推荐用网络存储。其中 TiDB Binlog 的 pump 和 drainer 组件属于 IO 密集型应用，需要较低的读写延迟，所以推荐用高性能的网络存储（例如 AWS 上的 io1 类型的 EBS 存储卷，GCP 上的持久化 SSD 盘）。

在利用 TiDB Operator 部署 TiDB 集群或者备份工具的时候，需要持久化存储的组件都可以通过 values.yaml 配置文件中对应的 `storageClassName` 设置存储类型。不设置时默认都使用 `local-storage`。

## 网络 PV 配置

Kubernetes 1.11 及以上的版本支持[网络 PV 的动态扩容](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/)，但用户需要为相应的 `StorageClass` 开启动态扩容支持。

{{< copyable "shell-regular" >}}

```shell
kubectl patch storageclass <storage-class-name> -p '{"allowVolumeExpansion": true}'
```

开启动态扩容后，通过下面方式对 PV 进行扩容：

1. 修改 PVC 大小

    假设之前 PVC 大小是 10 Gi，现在需要扩容到 100 Gi

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pvc -n <namespace> <pvc-name> -p '{"spec": {"resources": {"requests": {"storage": "100Gi"}}}'
    ```

2. 查看 PV 扩容成功

    扩容成功后，通过 `kubectl get pvc -n <namespace> <pvc-name>` 显示的大小仍然是初始大小，但查看 PV 大小会显示已经扩容到预期的大小。

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pv | grep <pvc-name>
    ```

## 本地 PV 配置

Kubernetes 当前支持静态分配的本地存储。可使用 [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) 项目中的 `local-volume-provisioner` 程序创建本地存储对象。创建流程如下：

1. 参考 Kubernetes 提供的[操作文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md)，在集群节点中预分配本地存储。

2. 部署 `local-volume-provisioner` 程序。

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml
    ```

    通过下面命令查看 Pod 和 PV 状态：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get po -n kube-system -l app=local-volume-provisioner && \
    kubectl get pv | grep local-storage
    ```

    `local-volume-provisioner` 会为发现目录 (discovery directory) 下的每一个挂载点创建一个 PV。注意，在 GKE 上，默认只能创建大小为 375 GiB 的本地卷。

更多信息，可参阅 [Kubernetes 本地存储](https://kubernetes.io/docs/concepts/storage/volumes/#local)和 [local-static-provisioner 文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview)。

### 最佳实践

- Local PV 的路径是本地存储卷的唯一标示符。为了保证唯一性并避免冲突，推荐使用设备的 UUID 来生成唯一的路径
- 如果想要 IO 隔离，建议每个存储卷使用一块物理盘会比较恰当，在硬件层隔离
- 如果想要容量隔离，建议每个存储卷一个分区或者每个存储卷使用一块物理盘来实现

更多信息，可参阅 local-static-provisioner 的[最佳实践文档](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md)。

### 示例

如果监控、TiDB Binlog、备份等组件都使用本地盘存储数据，可以挂载普通 SAS 盘，并分别创建不同的 `StorageClass` 供这些组件使用，具体操作如下：

- 给监控数据使用的盘，可以参考[步骤](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs)挂载盘，创建目录，并将新建的目录以 bind mount 方式挂载到 `/mnt/disks` 目录，后续创建 `local-storage` `StorageClass`。

    > **注意：**
    >
    > 该步骤中创建的目录个数取决于规划的 TiDB 集群数量。1 个目录会对应创建 1 个 PV。每个 TiDB 集群的监控数据会使用 1 个 PV。

- 给 TiDB Binlog 和备份数据使用的盘，可以参考[步骤](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs)挂载盘，创建目录，并将新建的目录以 bind mount 方式挂载到 `/mnt/backup` 目录，后续创建 `backup-storage` `StorageClass`。

    > **注意：**
    >
    > 该步骤中创建的目录个数取决于规划的 TiDB 集群数量、每个集群内的 Pump 数量及备份方式。1 个目录会对应创建 1 个 PV。每个 Pump 会使用 1 个 PV，每个 drainer 会使用 1 个 PV，每次 [Ad-hoc 全量备份](/v3.0/tidb-in-kubernetes/maintain/backup-and-restore.md#ad-hoc-全量备份)会使用 1 个 PV，所有[定时全量备份](/v3.0/tidb-in-kubernetes/maintain/backup-and-restore.md#定时全量备份)会共用 1 个 PV。

- 给 PD 数据使用的盘，可以参考[步骤](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs)挂载盘，创建目录，并将新建的目录以 bind mount 方式挂载到 `/mnt/sharedssd` 目录，后续创建 `shared-ssd-storage` `StorageClass`。

    > **注意：**
    >
    > 该步骤中创建的目录个数取决于规划的 TiDB 集群数量及每个集群内的 PD 数量。1 个目录会对应创建 1 个 PV。每个 PD 会使用一个 PV。

- 给 TiKV 数据使用的盘，可通过[普通挂载](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#use-a-whole-disk-as-a-filesystem-pv)方式将盘挂载到 `/mnt/ssd` 目录，后续创建 `ssd-storage` `StorageClass`。

盘挂载完成后，需要根据上述磁盘挂载情况修改 [`local-volume-provisioner` yaml 文件](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml)，配置发现目录并创建必要的 `StorageClass`。以下是根据上述挂载修改的 yaml 文件示例：

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: "local-storage"
provisioner: "kubernetes.io/no-provisioner"
volumeBindingMode: "WaitForFirstConsumer"
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: "ssd-storage"
provisioner: "kubernetes.io/no-provisioner"
volumeBindingMode: "WaitForFirstConsumer"
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: "shared-ssd-storage"
provisioner: "kubernetes.io/no-provisioner"
volumeBindingMode: "WaitForFirstConsumer"
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: "backup-storage"
provisioner: "kubernetes.io/no-provisioner"
volumeBindingMode: "WaitForFirstConsumer"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-provisioner-config
  namespace: kube-system
data:
  nodeLabelsForPV: |
    - kubernetes.io/hostname
  storageClassMap: |
    shared-ssd-storage:
      hostDir: /mnt/sharedssd
      mountDir: /mnt/sharedssd
    ssd-storage:
      hostDir: /mnt/ssd
      mountDir: /mnt/ssd
    local-storage:
      hostDir: /mnt/disks
      mountDir: /mnt/disks
    backup-storage:
      hostDir: /mnt/backup
      mountDir: /mnt/backup
---

......

          volumeMounts:

            ......

            - mountPath: /mnt/ssd
              name: local-ssd
              mountPropagation: "HostToContainer"
            - mountPath: /mnt/sharedssd
              name: local-sharedssd
              mountPropagation: "HostToContainer"
            - mountPath: /mnt/disks
              name: local-disks
              mountPropagation: "HostToContainer"
            - mountPath: /mnt/backup
              name: local-backup
              mountPropagation: "HostToContainer"
      volumes:

        ......

        - name: local-ssd
          hostPath:
            path: /mnt/ssd
        - name: local-sharedssd
          hostPath:
            path: /mnt/sharedssd
        - name: local-disks
          hostPath:
            path: /mnt/disks
        - name: local-backup
          hostPath:
            path: /mnt/backup
......

```

最后通过 `kubectl apply` 命令部署 `local-volume-provisioner` 程序。

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml
```

后续创建 TiDB 集群或备份等组件的时候，再配置相应的 `StorageClass` 供其使用。

## 数据安全

一般情况下 PVC 在使用完删除后，与其绑定的 PV 会被 provisioner 清理回收再放入资源池中被调度使用。为避免数据意外丢失，可在全局配置 `StorageClass` 的回收策略 (reclaim policy) 为 `Retain` 或者只将某个 PV 的回收策略修改为 `Retain`。`Retain` 模式下，PV 不会自动被回收。

* 全局配置

    `StorageClass` 的回收策略一旦创建就不能再修改，所以只能在创建时进行设置。如果创建时没有设置，可以再创建相同 provisioner 的 `StorageClass`，例如 GKE 上默认的 pd 类型的 `StorageClass` 默认保留策略是 `Delete`，可以再创建一个名为 `pd-standard` 的保留策略是 `Retain` 的存储类型，并在创建 TiDB 集群时将相应组件的 `storageClassName` 修改为 `pd-standard`。

    {{< copyable "" >}}

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: pd-standard
    parameters:
      type: pd-standard
    provisioner: kubernetes.io/gce-pd
    reclaimPolicy: Retain
    volumeBindingMode: Immediate
    ```

* 配置单个 PV

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

> **注意：**
>
> TiDB Operator 默认会自动将 PD 和 TiKV 的 PV 保留策略修改为 `Retain` 以确保数据安全。

PV 保留策略是 `Retain` 时，如果确认某个 PV 的数据可以被删除，需要通过下面的操作来删除 PV 以及对应的数据：

1. 删除 PV 对应的 PVC 对象：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete pvc <pvc-name> --namespace=<namespace>
    ```

2. 设置 PV 的保留策略为 `Delete`，PV 会被自动删除并回收：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    ```

要了解更多关于 PV 的保留策略可参考[修改 PV 保留策略](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/)。
