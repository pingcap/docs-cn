---
title: Kubernetes 上的 TiDB 集群备份恢复
category: how-to
---

# Kubernetes 上的 TiDB 集群备份与恢复

## 概览

这篇文档详细描述了如何对 Kubernetes 上的 TiDB 集群进行数据备份和数据恢复。

Kubernetes 上的 TiDB 集群支持两种备份策略：

* [全量备份](#全量备份)（定时执行或 Ad-hoc）：使用 [`mydumper`](/reference/tools/mydumper.md) 获取集群的逻辑备份；
* [增量备份](#增量备份)：使用 [`TiDB Binlog`](https://www.pingcap.com/docs/dev/reference/tools/tidb-binlog/overview/) 将 TiDB 集群的数据实时复制到其它数据库中或实时获得增量数据备份；

目前，Kubernetes 上的 TiDB 集群只对 `mydumper` 获取的全量备份数据提供自动化的数据恢复操作。恢复 `TiDB-Binlog` 获取的增量数据需要手动进行。

## 全量备份

全量备份使用 `mydumper` 来获取 TiDB 集群的逻辑备份数据。全量备份任务会创建一个 PVC([PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)) 来存储数据。

默认配置下，备份任务使用 PV ([Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes)) 来存储备份数据。你也可以通过修改配置将备份数据存储到 [Google Cloud Storage](https://cloud.google.com/storage/)，[Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) 或 [Amazon S3](https://aws.amazon.com/s3/) 中，在这种情况下，数据在上传到对象存储前，会临时存储在 PV 中。参考 [Kubernetes 上的 TiDB 集群备份配置](/reference/configuration/tidb-in-kubernetes/backup-configuration.md) 了解所有的配置选项。

你可以配置一个定时执行的全量备份任务，也可以临时执行一个全量备份任务。

### 定时全量备份

定时全量备份是一个与 TiDB 集群一同创建的定时任务，它会像 `crontab` 任务那样周期性地运行。

你可以修改 TiDB 集群的 `values.yaml` 文件来配置定时全量备份：

* 将 `scheduledBackup.create` 设置为 `true`；
* 将 `scheduledBackup.storageClassName` 设置为用于存储数据的 PV 的 `storageClass`；

    > **注意：**
    >
    > 你必须将定时全量备份使用的 PVC 的 [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) 设置为 `Retain` 来确保你的数据安全。

* 按照 `[Cron](https://en.wikipedia.org/wiki/Cron)` 格式设置 `scheduledBackup.schedule` 来定义任务的执行周期与时间；
* 创建一个包含数据库用户名和密码的 Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) 该用户必须拥有数据备份所需的数据库相关权限，同时，将 `scheduledBackup.secretName` 设置为该 `Secret` 的名字（默认为 `backup-secret`）：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* 通过 `helm install` 创建一个配置了定时全量备份的 TiDB 集群，针对现有集群，则使用 `helm upgrade` 为集群打开定时全量备份：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release_name> pingcap/tidb-cluster -f values.yaml --version=<tidb-operator-version>
    ```

### Ad-hoc 全量备份

Ad-hoc 全量备份封装在 `pingcap/tidb-backup` 这个 Helm chart 中。根据 `values.yaml` 文件中的 `mode`  配置，该 chart 可以执行全量备份或数据恢复。我们会在 [数据恢复](#数据恢复) 一节中描述如何执行数据恢复。

你可以通过下面的步骤执行一次 Ad-hoc 全量备份：

* 修改 `values.yaml`：
    * 将 `clusterName` 设置为目标 TiDB 集群名字；
    * 将 `mode` 设置为 `backup`；
    * 将 `storage.className` 设置为用于存储数据的 PV 的 `storageClass`；
    * 根据数据量调整 `storage.size`；

    > **注意：**
    >
    > 你必须将 Ad-hoc 全量备份使用的 PVC 的 [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) 设置为 `Retain` 来确保你的数据安全。

* 创建一个包含数据库用户名和密码的 Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) 该用户必须拥有数据备份所需的数据库相关权限，同时，将 `values.yaml` 中的 `secretName` 设置为该 `Secret` 的名字（默认为 `backup-secret`）：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* 使用下面的命令执行一次 Ad-hoc 全量备份：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --name=<backup-name> --namespace=<namespace> -f values.yaml --version=<tidb-operator-version>
    ```

### 查看备份

对于存储在 PV 中的备份，你可以使用下面的命令进行查看：

{{< copyable "shell-regular" >}}

```shell
kubectl get pvc -n <namespace> -l app.kubernetes.io/component=backup,pingcap.com/backup-cluster-name=<cluster-name>
```

假如你将数据存储在 [Google Cloud Storage](https://cloud.google.com/storage/)，[Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) 或 [Amazon S3](https://aws.amazon.com/s3/) 中，你可以用这些存储系统自带的图形界面或命令行工具查看全量备份。

## 数据恢复

 使用 `pingcap/tidb-backup` 这个 Helm chart 进行数据恢复，步骤如下：

* 修改 `values.yaml`：
    * 将 `clusterName` 设置为目标 TiDB 集群名；
    * 将 `mode` 设置为 `restore`；
    * 将 `name`  设置为用于恢复的备份名字（你可以参考[查看备份](#查看备份)来寻找可用的备份数据）。假如备份数据存储在 [Google Cloud Storage](https://cloud.google.com/storage/)，[Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) 或 [Amazon S3](https://aws.amazon.com/s3/) 中，你必须保证这些存储的相关配置与执行[全量备份](#全量备份)时一致。
* 创建一个包含数据库用户名和密码的 Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) 该用户必须拥有数据备份所需的数据库相关权限，同时，将 `values.yaml` 中的 `secretName` 设置为该 `Secret` 的名字（默认为 `backup-secret`，假如你在[全量备份](#全量备份)时已经创建了该 Secret，则可以跳过这步）：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* 恢复数据：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --namespace=<namespace> --name=<restore-name> -f values.yaml --version=<tidb-operator-version>
    ```

## 增量备份

增量备份使用 [TiDB Binlog](https://www.pingcap.com/docs/dev/reference/tools/tidb-binlog/overview/) 工具从 TiDB 集群收集 Binlog，并提供实时备份和向其它数据库的实时同步能力。

增量备份是默认关闭的，你可以通过修改 `values.yaml` 中的下列配置项来开启增量备份：

* 将 `binlog.pump.create` 设置为 `true`；
* 将 `binlog.drainer.create` 设置为 `true`；
* 将 `binlog.pump.storageClassName` 和 `binlog.drainer.storageClassName` 设置为你的 Kubernetes 集群中可用的 `storageClass`；
* 根据需求将 `binlog.drainer.destDBType` 设置为合适的下游存储，下面将详细叙述。

增量备份支持三种下游存储：

* PV：默认的下游存储，这种情况下，你可以考虑为 `drainer` 配置更大的 PV 空间（通过修改 `binlog.drainer.storage` 配置）；
* 兼容 MySQL 协议的数据库：通过设置 `binlog.drainer.destDBType` 为 `mysql` 来开启，你必须同时在 `binlog.drainer.mysql` 中配置目标数据库的地址和认证信息；
* Apache Kafka：通过设置 `binlog.drainer.destDBType` 为 `kafka` 来开启，你必须同时在 `binlog.drainer.kafka` 中配置目标集群的 Zookeeper 地址和 Kafka 地址。
