---
title: 恢复 S3 兼容存储上的备份数据
category: how-to
---

# 恢复 S3 兼容存储上的备份数据

本文描述了将 Kubernetes 上通过 TiDB Operator 备份的数据恢复到 TiDB 集群的操作过程。底层通过使用 [`loader`](/reference/tools/loader.md) 来恢复数据。

本文使用的备份方式基于 TiDB Operator 新版（v1.1 及以上）的 CRD 实现。基于 Helm Charts 实现的备份恢复方式可参考[基于 Helm Charts 实现的 TiDB 集群备份恢复](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md)。

以下示例将兼容 S3 的存储（指定路径）上的备份数据恢复到 TiDB 集群。

## 环境准备

1. 下载文件 [`backup-rbac.yaml`](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml)，并在 `test2` 这个 namespace 中创建恢复备份所需的 RBAC 资源，所需命令如下：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test2
    ```

2. 创建 `restore-demo2-tidb-secret` secret，该 secret 存放用来访问 TiDB 集群的 root 账号和密钥：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic restore-demo2-tidb-secret --from-literal=user=root --from-literal=password=<password> --namespace=test2
    ```

## 将指定备份恢复到 TiDB 集群

1. 创建 restore custom resource (CR)，将指定的备份数据恢复至 TiDB 集群：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f restore.yaml
    ```

    `restore.yaml` 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: Restore
    metadata:
      name: demo2-restore
      namespace: test2
    spec:
      to:
        host: <tidb-host-ip>
        port: <tidb-port>
        user: <tidb-user>
        secretName: restore-demo2-tidb-secret
      s3:
        provider: ceph
        endpoint: http://10.233.2.161
        secretName: ceph-secret
        path: s3://<path-to-backup>
      storageClassName: local-storage
      storageSize: 1Gi
    ```

2. 创建好 `Restore` CR 后可通过以下命令查看恢复的状态：

    {{< copyable "shell-regular" >}}

     ```shell
     kubectl get rt -n test2 -owide
     ```

以上示例将兼容 S3 的存储（`spec.s3.path` 路径下）中的备份数据恢复到 TiDB 集群 (`spec.to.host`)。有关兼容 S3 的存储的配置项，可以参考 [backup-s3.yaml](/tidb-in-kubernetes/maintain/backup-and-restore/backup-s3.md#备份数据到兼容-s3-的存储)。

更多 `Restore` CR 字段的详细解释：

* `.spec.metadata.namespace`：`Restore` CR 所在的 namespace。
* `.spec.to.host`：待恢复 TiDB 集群的访问地址。
* `.spec.to.port`：待恢复 TiDB 集群的访问端口。
* `.spec.to.user`：待恢复 TiDB 集群的访问用户。
* `.spec.to.tidbSecretName`：待恢复 TiDB 集群所需凭证的 secret。
* `.spec.storageClassName`：指定恢复时所需的 PV 类型。如果不指定该项，则默认使用 TiDB Operator 启动参数中 `default-backup-storage-class-name` 指定的值（默认为 `standard`）。
* `.spec.storageSize`：指定恢复集群时所需的 PV 大小。该值应大于备份 TiDB 集群的数据大小。
