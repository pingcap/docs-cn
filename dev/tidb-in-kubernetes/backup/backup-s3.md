---
title: Kubernetes 上备份 TiDB 集群到 S3 兼容后端存储
category: how-to
---

# Kubernetes 上备份 TiDB 集群到 S3 兼容后端存储

这篇文档详细描述了如何将 Kubernetes 上的 TiDB 集群数据备份到 S3 兼容的存储上, 这里说到的备份均是指全量备份(定时全量备份和 Ad-hoc 全量备份), 底层通过使用 [`mydumper`](/dev/reference/tools/mydumper.md) 获取集群的逻辑备份，然后在将备份数据上传到远端 S3 兼容的存储上。

## Ad-hoc 全量备份

Ad-hoc 全量备份通过创建一个自定义的 `Backup` CR 对象来描述一次备份，tidb-operator 根据这个 `Backup` 对象来完成具体的备份过程，如果备份过程中出现错误程序不会自动重试，此时需要人工介入处理。目前 S3 兼容的存储中我们只对 `Ceph`、`Amazon S3` 这两种存储做过测试，因此下面我们主要针对 `Ceph` 和 `Amazon S3` 这两种存储的使用来说明。理论上来说其余 S3 兼容的存储也可以正常的工作。

为了更好的说明备份的使用方式，我们假设需要对部署在 Kubernetes `test1` 这个 namespace 中的 TiDB 集群 `demo1` 进行数据备份，下面是具体操作过程：

### Ad-hoc 全量备份环境准备

1. 在 `test1` 这个 namespace 中创建备份需要的 RBAC 相关资源，下载文件 [backup-rbac.yaml](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml)

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test1
    ```

2. 创建 `s3-secret` secret，改 secret 存放了用来访问 S3 兼容存储的凭证

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic s3-secret --from-literal=access_key=xxx --from-literal=secret_key=yyy --namespace=test1
    ```

3. 创建 `backup-demo1-tidb-secret` secret, 里面存放用来访问 TiDB 集群的 root 账号和密钥

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-demo1-tidb-secret --from-literal=user=root --from-literal=password=<password> --namespace=test1
    ```

### 备份数据到 S3 兼容存储

1. 创建 backup CR, 备份数据到 Amazon S3：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-s3.yaml
    ```

    `backup-s3.yaml` 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: Backup
    metadata:
      name: demo1-backup-s3
      namespace: test1
    spec:
      s3:
        provider: aws
        secretName: s3-secret
        # region: us-east-1
        # storageClass: STANDARD_IA
        # acl: private
        # endpoint:
      storageType: s3
      cluster: demo1
      tidbSecretName: backup-demo1-tidb-secret
      storageClassName: local-storage
      storageSize: 10Gi
    ```

2. 创建 backup CR, 备份数据到 ceph：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-s3.yaml
    ```

    backup-s3.yaml 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: Backup
    metadata:
      name: demo1-backup-s3
      namespace: test1
    spec:
      s3:
        provider: ceph
        secretName: s3-secret
        endpoint: http://10.0.0.1:30074
      storageType: s3
      cluster: demo1
      tidbSecretName: backup-demo1-tidb-secret
      storageClassName: local-storage
      storageSize: 10Gi
    ```

上面两个例子中分别将 TiDB 集群的数据全量导出备份到 Amazon S3 和 ceph，Amazon S3 的 `region`、`acl`、`enpoint`、`storageClass` 均可以省略，其余非 Amazon S3 的但是兼容 S3 接口的存储均可使用和 Amazon S3 类似的配置，不需要配置的字段跳过即可，参考 ceph 配置。

Amazon S3 支持的 ACL 策略有如下几种：

* `private`
* `public-read`
* `public-read-write`
* `authenticated-read`
* `bucket-owner-read`
* `bucket-owner-full-control`

如果不设置 ACL 策略，则默认使用 `private` 策略, 这几种访问控制策略的详细介绍参考 AWS [官方文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html)。

Amazon S3 支持的 storageClass 类型有如下几种：

* `STANDARD`
* `REDUCED_REDUNDANCY`
* `STANDARD_IA`
* `ONEZONE_IA`
* `GLACIER`
* `DEEP_ARCHIVE`

如果不设置 `storageClass`，则默认使用 `STANDARD_IA`, 这几种存储类型的详细介绍参考 AWS [官方文档](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html)。

创建好 `Backup` CR 后我们可以通过如下命令查看备份状态：

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -n test1 -owide
 ```

最后是对 backup CR 其余字段的详细解释:

`.spec.metadata.namespace`: 备份 TiDB 集群所在的 namespace

`.spec.storageType`: 代表备份的存储类型，目前主要有 s3 和 gcs

`.spec.cluster`: 备份 TiDB 集群的名字

`.spec.tidbSecretName`: 访问 TiDB 集群所需密码的 secret

`.spec.storageClassName`: 备份时需要指定使用的 PV 类型，如果不指定则默认使用 tidb-operator 启动参数中 `default-backup-storage-class-name` 指定的值，这个值默认为 `standard`

`.spec.storageSize`: 备份时指定需要使用的 PV 大小，这个值要大于备份 TiDB 集群的数据大小

支持的其余 S3 兼容 provider 如下：

* `alibaba`(Alibaba Cloud Object Storage System (OSS) formerly Aliyun)
* `digitalocean`(Digital Ocean Spaces)
* `dreamhost`(Dreamhost DreamObjects)
* `ibmcos`(IBM COS S3)
* `minio`(Minio Object Storage)
* `netease`(Netease Object Storage (NOS))
* `wasabi`(Wasabi Object Storage)
* `other`(Any other S3 compatible provider)

## 定时全量备份

用户通过设置备份策略定时备份 TiDB 集群，同时可配置备份的保留策略避免产生过多的备份，定时全量备份通过自定义的 `BackupSchedule` CR 对象来描述，每次到备份时间点会触发一次全量备份，定时全量备份底层通过 Ad-hoc 全量备份来实现。下面是创建定期全量备份的具体步骤：

### 定时全量备份环境准备

这里和 Ad-hoc 全量备份操作一致

### 定时全部备份数据到 S3 兼容存储

1. 创建 backupSchedule CR 开启 TiDB 集群的定时全量备份，将数据备份到 Amazon S3：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-schedule-s3.yaml
    ```

    backup-schedule-s3.yaml 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: BackupSchedule
    metadata:
      name: demo1-backup-schedule-s3
      namespace: test1
    spec:
      #maxBackups: 5
      #pause: true
      maxReservedTime: "3h"
      schedule: "*/2 * * * *"
      backupTemplate:
        s3:
          provider: aws
          secretName: s3-secret
          # region: us-east-1
          # storageClass: STANDARD_IA
          # acl: private
          # endpoint:
        storageType: s3
        cluster: demo1
        tidbSecretName: backup-demo1-tidb-secret
        storageClassName: local-storage
        storageSize: 10Gi
    ```

2. 创建 backupSchedule CR 开启 TiDB 集群的定时全量备份，将数据备份到 ceph：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-schedule-s3.yaml
    ```

    backup-schedule-s3.yaml 文件内容如下：

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: BackupSchedule
    metadata:
      name: demo1-backup-schedule-ceph
      namespace: test1
    spec:
      #maxBackups: 5
      #pause: true
      maxReservedTime: "3h"
      schedule: "*/2 * * * *"
      backupTemplate:
        s3:
           provider: ceph
           secretName: s3-secret
           endpoint: http://10.0.0.1:30074
        storageType: s3
        cluster: demo1
        tidbSecretName: backup-demo1-tidb-secret
        storageClassName: local-storage
        storageSize: 10Gi
    ```

上面分别列出了两种备份方式，一种备份到 Amazon S3，一种备份到 ceph，如果想定时全量备份到其它的 S3 兼容的存储上，只需要在 `spec.backupTemplate` 指定相应的存储配置即可，这块的配置和 Ad-hoc 全量备份的配置完全一样。

当定时全量备份创建完成后，我们可以通过如下命令查看定时全量备份状态：

{{< copyable "shell-regular" >}}

```shell
kubectl get bks -n test1 -owide
```

查看此定时全量备份下面的所有备份条目：

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -l tidb.pingcap.com/backup-schedule=demo1-backup-schedule-s3 -n test1
 ```

从上面的两个例子中我们可以看出 `backupSchedule` 的配置主要由两部分组成，一部分是 backupSchedule 独有的配置，还有一部分就是 backupTemplate，这个配置上面也提到了，和 Ad-hoc 的配置是完全一样的，因此这里我们就不对这块进行过多的解释。下面主要针对 backupSchedule 独有的一些配置项进行详细介绍：

 `.spec.maxBackups`: 一种备份保留策略，定时备份最多保留的备份个数，超过这个数目，就会将过时的备份删除，如果将这个最大备份保留格式设置为0，则表示保留所有备份。

 `.spec.maxReservedTime`：这个和上面的参数一样，也是种一种备份保留策略，这个是按时间保留，比如设置为 `24h`, 代表只保留最近 24 小时内的备份条目，超过这个时间的备份都会被清除，时间设置格式参考[这里](https://golang.org/pkg/time/#ParseDuration)。如果最大备份保留个数和最大备份保留时间两者都被设置了，则以最大备份保留时间为准。

 `.spec.schedule`：cron 时间调度格式，具体格式参考[这里](https://en.wikipedia.org/wiki/Cron)。

 `.spec.pause`：这个值默认为 false，如果设置为 true，代表暂停定时调度，此时即使到了调度点，也不会进行备份。在定时备份暂停期间，备份 GC 仍然正常进行。从 true 改为 false 则重新开启定时全量备份。
