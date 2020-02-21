---
title: 在 Kubernetes 上备份 TiDB 集群到 GCS
category: how-to
---

# 在 Kubernetes 上备份 TiDB 集群到 GCS

本文档详细描述了如何将 Kubernetes 上 TiDB 集群的数据备份到 [Google Cloud Storage (GCS)](https://cloud.google.com/storage/docs/) 上。本文档中的“备份”，均是指全量备份（Ad-hoc 全量备份和定时全量备份），底层通过使用 [`mydumper`](/reference/tools/mydumper.md) 获取集群的逻辑备份，然后再将备份数据上传到远端 GCS。

## Ad-hoc 全量备份

Ad-hoc 全量备份通过创建一个自定义的 `Backup` custom resource (CR) 对象来描述一次备份。TiDB Operator 根据这个 `Backup` 对象来完成具体的备份过程。如果备份过程中出现错误，程序不会自动重试，此时需要手动处理。

为了更好地描述备份的使用方式，本文档提供如下备份示例。示例假设对部署在 Kubernetes `test1` 这个 namespace 中的 TiDB 集群 `demo1` 进行数据备份，下面是具体操作过程。

### Ad-hoc 全量备份环境准备

1. 下载文件 [backup-rbac.yaml](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml)，并执行以下命令在 `test1` 这个 namespace 中创建备份需要的 RBAC 相关资源：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test1
    ```

2. 创建 `gcs-secret` secret。该 secret 存放用于访问 GCS 的凭证。`google-credentials.json` 文件存放用户从 GCP console 上下载的 service account key。具体操作参考 [GCP 官方文档](https://cloud.google.com/docs/authentication/getting-started)。

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic gcs-secret --from-file=credentials=./google-credentials.json -n test1
    ```

3. 创建 `backup-demo1-tidb-secret` secret。该 secret 存放用于访问 TiDB 集群的 root 账号和密钥。

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-demo1-tidb-secret --from-literal=user=root --from-literal=password=<password> --namespace=test1
    ```

### 备份数据到 GCS

创建 `Backup` CR，并将数据备份到 GCS。

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f backup-gcs.yaml
```

`backup-gcs.yaml` 文件内容如下：

```yaml
---
apiVersion: pingcap.com/v1alpha1
kind: Backup
metadata:
  name: demo1-backup-gcs
  namespace: test1
spec:
  gcs:
    secretName: gcs-secret
    projectId: <your-project-id>
    # location: us-east1
    # storageClass: STANDARD_IA
    # objectAcl: private
    # bucketAcl: private
  storageType: gcs
  cluster: demo1
  tidbSecretName: backup-demo1-tidb-secret
  storageClassName: local-storage
  storageSize: 10Gi
```

以上示例将 TiDB 集群的数据全量导出备份到 GCS。GCS 配置中的 `location`、`objectAcl`、`bucketAcl`、`storageClass` 项均可以省略。

配置中的 `projectId` 代表 GCP 上用户项目的唯一标识。具体获取该标识的方法可参考 [GCP 官方文档](https://cloud.google.com/resource-manager/docs/creating-managing-projects)。

GCS 支持以下几种 `storageClass` 类型：

* `MULTI_REGIONAL`
* `REGIONAL`
* `NEARLINE`
* `COLDLINE`
* `DURABLE_REDUCED_AVAILABILITY`

如果不设置 `storageClass`，则默认使用 `COLDLINE`。这几种存储类型的详细介绍可参考 [GCS 官方文档](https://cloud.google.com/storage/docs/storage-classes)。

GCS 支持以下几种 object ACL 策略：

* `authenticatedRead`
* `bucketOwnerFullControl`
* `bucketOwnerRead`
* `private`
* `projectPrivate`
* `publicRead`

如果不设置 object ACL 策略，则默认使用 `private` 策略。这几种访问控制策略的详细介绍可参考 [GCS 官方文档](https://cloud.google.com/storage/docs/access-control/lists)。

GCS 支持以下几种 bucket ACL 策略：

* `authenticatedRead`
* `private`
* `projectPrivate`
* `publicRead`
* `publicReadWrite`

如果不设置 bucket ACL 策略，则默认策略为 `private`。这几种访问控制策略的详细介绍可参考 [GCS 官方文档](https://cloud.google.com/storage/docs/access-control/lists)。

创建好 `Backup` CR 后，可通过以下命令查看备份状态：

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -n test1 -owide
 ```

更多 `Backup` CR 字段的详细解释：

`.spec.metadata.namespace`：备份 TiDB 集群所在的 namespace。

`.spec.storageType`：备份的存储类型。目前主要有 S3 和 GCS 两种。

`.spec.cluster`：备份 TiDB 集群的名字。

`.spec.tidbSecretName`：访问 TiDB 集群所需凭证的 secret。

`.spec.storageClassName`：备份时指定所需的 PV 类型。如果不指定该项，则默认使用 TiDB Operator 启动参数中 `default-backup-storage-class-name` 指定的值，这个值默认为 `standard`。

`.spec.storageSize`：备份时指定所需的 PV 大小。该值应大于备份 TiDB 集群数据的大小。

## 定时全量备份

用户通过设置备份策略来对 TiDB 集群进行定时备份，同时设置备份的保留策略以避免产生过多的备份。定时全量备份通过自定义的 `BackupSchedule` CR 对象来描述。每到备份时间点会触发一次全量备份，定时全量备份底层通过 Ad-hoc 全量备份来实现。下面是创建定时全量备份的具体步骤：

### 定时全量备份环境准备

同 [Ad-hoc 全量备份环境准备](#ad-hoc-全量备份环境准备)。

### 定时全量备份数据到 GCS

创建 `BackupSchedule` CR 开启 TiDB 集群的定时全量备份，将数据备份到 GCS：

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f backup-schedule-gcs.yaml
```

`backup-schedule-gcs.yaml` 文件内容如下：

```yaml
---
apiVersion: pingcap.com/v1alpha1
kind: BackupSchedule
metadata:
  name: demo1-backup-schedule-gcs
  namespace: test1
spec:
  #maxBackups: 5
  #pause: true
  maxReservedTime: "3h"
  schedule: "*/2 * * * *"
  backupTemplate:
    gcs:
      secretName: gcs-secret
      projectId: <your-project-id>
      # location: us-east1
      # storageClass: STANDARD_IA
      # objectAcl: private
      # bucketAcl: private
    storageType: gcs
    cluster: demo1
    tidbSecretName: backup-demo1-tidb-secret
    storageClassName: local-storage
    storageSize: 10Gi
```

定时全量备份创建完成后，可以通过以下命令查看定时全量备份的状态：

{{< copyable "shell-regular" >}}

```shell
kubectl get bks -n test1 -owide
```

查看定时全量备份下面所有的备份条目：

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -l tidb.pingcap.com/backup-schedule=demo1-backup-schedule-gcs -n test1
 ```

从以上示例可知，`backupSchedule` 的配置由两部分组成。一部分是 `backupSchedule` 独有的配置，另一部分是 `backupTemplate`。`backupTemplate` 指定 GCS 存储相关的配置，该配置与 Ad-hoc 全量备份到 GCS 的配置完全一样，可参考[备份数据到 GCS](#备份数据到-gcs)。下面介绍 `backupSchedule` 独有的配置项：

`.spec.maxBackups`：一种备份保留策略，决定定时备份最多可保留的备份个数。超过该数目，就会将过时的备份删除。如果将该项设置为 `0`，则表示保留所有备份。

`.spec.maxReservedTime`：一种备份保留策略，按时间保留备份。比如将该参数设置为 `24h`，表示只保留最近 24 小时内的备份条目。超过这个时间的备份都会被清除。时间设置格式参考[`func ParseDuration`](https://golang.org/pkg/time/#ParseDuration)。如果同时设置最大备份保留个数和最长备份保留时间，则以最长备份保留时间为准。

`.spec.schedule`：Cron 的时间调度格式。具体格式可参考 [Cron](https://en.wikipedia.org/wiki/Cron)。

`.spec.pause`：该值默认为 `false`。如果将该值设置为 `true`，表示暂停定时调度。此时即使到了调度时间点，也不会进行备份。在定时备份暂停期间，备份 Garbage Collection (GC) 仍然正常进行。将 `true` 改为 `false` 则重新开启定时全量备份。
