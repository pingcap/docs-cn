---
title: Persistent Storage Class Configuration in Kubernetes
summary: Learn how to configure local PVs and network PVs.
category: reference
aliases: ['/docs/dev/tidb-in-kubernetes/reference/configuration/local-pv/']
---

# Persistent Storage Class Configuration in Kubernetes

TiDB cluster components such as PD, TiKV, TiDB monitoring, TiDB Binlog and `tidb-backup` require the persistent storage of data. To persist the data in Kubernetes, you need to use [PersistentVolume (PV)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). Kubernetes supports several types of [storage classes](https://kubernetes.io/docs/concepts/storage/volumes/), which are mainly divided into two parts:

- Network storage

    The network storage medium is not on the current node, but is mounted to the node through the network. Generally, there are redundant replicas to guarantee high availability. When the node fails, the corresponding network storage can be re-mounted to another node for further use.

- Local storage

    The local storage medium is on the current node, and typically can provide lower latency than the network storage. Because there are no redundant replicas, once the node fails, data might be lost. If it is an IDC server, data can be restored to a certain extent. If it is a virtual machine using the local disk on the public cloud, data **cannot** be retrieved after the node fails.

PVs are created automatically by the system administrator or volume provisioner. PVs and Pods are bound by [PersistentVolumeClaim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims). Users request for using a PV through a PVC instead of creating a PV directly. The corresponding volume provisioner creates a PV that meets the requirements of PVC and then binds the PV to the PVC.

> **Warning:**
>
> For data safety, do not delete a PV in any case unless you are familiar with the underlying volume provisioner.

## Recommended storage classes for TiDB clusters

TiKV uses the Raft protocol to replicate data. When a node fails, PD automatically schedules data to fill the missing data replicas; TiKV requires low read and write latency, so local SSD storage is strongly recommended in the production environment.

PD also uses Raft to replicate data. PD is not an I/O-intensive application, but a database for storing cluster meta information, so a local SAS disk or network SSD storage such as EBS General Purpose SSD (gp2) volumes on AWS or SSD persistent disks on GCP can meet the requirements.

To ensure availability, it is recommended to use network storage for components such as TiDB monitoring, TiDB Binlog and `tidb-backup` because they do not have redundant replicas. TiDB Binlog's Pump and Drainer components are I/O-intensive applications that require low read and write latency, so it is recommended to use high-performance network storage such as EBS Provisioned IOPS SSD (io1) volumes on AWS or SSD persistent disks on GCP.

When deploying TiDB clusters or `tidb-backup` with TiDB Operator, you can configure `StorageClass` for the components that require persistent storage via the corresponding `storageClassName` field in the `values.yaml` configuration file. The `StorageClassName` is set to `local-storage` by default.

## Network PV configuration

Kubernetes 1.11 and later versions support [volume expansion of network PV](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/), but you need to run the following command to enable volume expansion for the corresponding `StorageClass`:

{{< copyable "shell-regular" >}}

```shell
kubectl patch storageclass <storage-class-name> -p '{"allowVolumeExpansion": true}'
```

After volume expansion is enabled, expand the PV using the following method:

1. Edit the PersistentVolumeClaim (PVC) object:

    Suppose the PVC is 10 Gi and now we need to expand it to 100 Gi.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pvc -n <namespace> <pvc-name> -p '{"spec": {"resources": {"requests": {"storage": "100Gi"}}}'
    ```

2. View the size of the PV:

    After the expansion, the size displayed by running `kubectl get pvc -n <namespace> <pvc-name>` is still the original one. But if you run the following command to view the size of the PV, it shows that the size has been expanded to the expected one.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pv | grep <pvc-name>
    ```

## Local PV configuration

Kubernetes currently supports statically allocated local storage. To create a local storage object, use `local-volume-provisioner` in the [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) repository. The procedure is as follows:

1. Pre-allocate local storage in cluster nodes. See the [operation guide](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) provided by Kubernetes.

2. Deploy `local-volume-provisioner`.

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

    `local-volume-provisioner` creates a PV for each mounting point under discovery directory. Note that on GKE, `local-volume-provisioner` creates a local volume of only 375 GiB in size by default.

For more information, refer to [Kubernetes local storage](https://kubernetes.io/docs/concepts/storage/volumes/#local) and [local-static-provisioner document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview).

### Best practices

- A local PV's path is its unique identifier. To avoid conflicts, it is recommended to use the UUID of the device to generate a unique path.
- For I/O isolation, a dedicated physical disk per PV is recommended to ensure hardware-based isolation.
- For capacity isolation, a partition per PV or a physical disk per PV is recommended.

Refer to [Best Practices](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md) for more information on local PV in Kubernetes.

## Disk mount examples

If the components such as monitoring, TiDB Binlog, and `tidb-backup` use local disks to store data, you can mount SAS disks and create separate `StorageClass` for them to use. Procedures are as follows:

- For a disk storing monitoring data, follow the [steps](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs) to mount the disk. First, create multiple directories in disk, and bind mount them into `/mnt/disks` directory. Then, create `local-storage` `StorageClass` for them to use.

    >**Note:**
    >
    > The number of directories you create depends on the planned number of TiDB clusters. For each directory, a corresponding PV will be created. The monitoring data in each TiDB cluster uses one PV.

- For a disk storing TiDB Binlog and backup data, follow the [steps](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs) to mount the disk. First, create multiple directories in disk, and bind mount them into `/mnt/backup` directory. Then, create `backup-storage` `StorageClass` for them to use.

    >**Note:**
    >
    > The number of directories you create depends on the planned number of TiDB clusters, the number of Pumps in each cluster, and your backup method. For each directory, a corresponding PV will be created. Each Pump uses one PV and each Drainer uses one PV. Each [Ad-hoc full backup](/tidb-in-kubernetes/maintain/backup-and-restore.md#ad-hoc-full-backup) task uses one PV, and all [scheduled full backup](/tidb-in-kubernetes/maintain/backup-and-restore.md#scheduled-full-backup) tasks share one PV.

- For a disk storing data in PD, follow the [steps](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#sharing-a-disk-filesystem-by-multiple-filesystem-pvs) to mount the disk. First, create multiple directories in disk, and bind mount them into `/mnt/sharedssd` directory. Then, create `shared-ssd-storage` `StorageClass` for them to use.

    >**Note:**
    >
    > The number of directories you create depends on the planned number of TiDB clusters, and the number of PD servers in each cluster. For each directory, a corresponding PV will be created. Each PD server uses one PV.

- For a disk storing data in TiKV, you can [mount](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md#use-a-whole-disk-as-a-filesystem-pv) it into `/mnt/ssd` directory, and create `ssd-storage` `StorageClass` for it to use.

Based on the disk mounts above, you need to modify the [`local-volume-provisioner` YAML file](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml) accordingly, configure discovery directory and create the necessary `StorageClass`. Here is an example of a modified YAML file:

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

Finally, execute the `kubectl apply` command to deploy `local-volume-provisioner`.

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/local-dind/local-volume-provisioner.yaml
```

When you later deploy tidb clusters, deploy TiDB Binlog for incremental backups, or do full backups, configure the corresponding `StorageClass` for use.

## Data safety

In general, after a PVC is no longer used and deleted, the PV bound to it is reclaimed and placed in the resource pool for scheduling by the provisioner. To avoid accidental data loss, you can globally configure the reclaim policy of the `StorageClass` to `Retain` or only change the reclaim policy of a single PV to `Retain`. With the `Retain` policy, a PV is not automatically reclaimed.

- Configure globally:

    The reclaim policy of a `StorageClass` is set at creation time and it cannot be updated once it is created. If it is not set when created, you can create another `StorageClass` of the same provisioner. For example, the default reclaim policy of the `StorageClass` for persistent disks on Google Kubernetes Engine (GKE) is `Delete`. You can create another `StorageClass` named `pd-standard` with its reclaim policy as `Retain`, and change the `storageClassName` of the corresponding component to `pd-standard` when creating a TiDB cluster.

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

- Configure a single PV:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

> **Note:**
>
> By default, to ensure data safety, TiDB Operator automatically changes the reclaim policy of the PVs of PD and TiKV to `Retain`.

When the reclaim policy of PVs is set to `Retain`, if the data of a PV can be deleted, delete this PV and the corresponding data according to the following steps:

1. Delete the PVC object corresponding to the PV:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete pvc <pvc-name> --namespace=<namespace>
    ```

2. Set the reclaim policy of the PV to `Delete`. Then the PV is automatically deleted and reclaimed.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
    ```

For more details, refer to [Change the Reclaim Policy of a PersistentVolume](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/).
