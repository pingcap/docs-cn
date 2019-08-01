---
title: Kubernetes 上的 TiDB 集群备份配置
category: reference
aliases: ['/docs-cn/V3.0/reference/configuration/tidb-in-kubernetes/cluster-configuration/']
---

# Kubernetes 上的 TiDB 集群备份配置

`tidb-backup` 是一个用于 Kubernetes 上 TiDB 集群备份和恢复的 Helm Chart。本文详细介绍了 `tidb-backup` 的可配置参数。

## `mode`

+ 运行模式
+ 默认："backup"
+ 可选值为 `backup`（备份集群数据）和 `restore`（恢复集群数据）

## `clusterName`

+ 目标集群名字
+ 默认："demo"
+ 指定要从哪个集群进行备份或将数据恢复到哪个集群中

## `name`

+ 备份名
+ 默认值："fullbackup-<date>"，`<date>` 是备份的开始时间，精确到分钟
+ 备份名用于区分不同的备份数据

## `secretName`

+ 访问目标集群时使用的凭据
+ 默认："backup-secret"
+ 该 Kubernetes Secret 中需要存储目标集群的登录用户名和密码，你可以通过以下命令来创建这个 Secret：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=root --from-literal=password=<password>
    ```

## `storage.className`

+ Kubernetes StorageClass
+ 默认："local-storage"
+ 备份任务需要绑定一个持久卷 (Persistent Volume, PV) 来永久或临时存储备份数据，`StorageClass` 用于声明持久卷使用的存储类型，需要确保该 `StorageClass` 在 Kubernetes 集群中存在。

## `storage.size`

+ 持久卷的空间大小
+ 默认："100Gi"

## `backupOptions`

+ 备份参数
+ 默认："--chunk-filesize=100"
+ 为备份数据时使用的 [mydumper](https://github.com/maxbube/mydumper/blob/master/docs/mydumper_usage.rst#options) 指定额外的运行参数

## `restoreOptions`

+ 恢复参数
+ 默认："-t 16"
+ 为恢复数据时使用的 [Loader](/reference/tools/loader.md) 指定额外的运行参数

## `gcp.bucket`

+ Google Cloud Storage 的 bucket 名字
+ 默认：""
+ 用于存储备份数据到 Google Cloud Storage 上

> **注意：**
>
> 一旦设置了 `gcp` 下的任何参数，备份和恢复就会使用 Google Cloud Storage 进行数据存储。也就是说，假如要设置 `gcp` 下的参数，就需要保证所有 `gcp` 相关参数都得到正确配置，否则会造成备份恢复失败。

## `gcp.secretName`

+ 访问 GCP 时使用的凭据
+ 默认：""
+ 该 Kubernetes Secret 中需要存储 GCP 的 Service Account 凭据，你可以参考 [Google Cloud Documentation](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually) 来下载凭据文件，然后通过下面的命令创建 Secret：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic gcp-backup-secret -n <namespace> --from-file=./credentials.json
    ```

## `ceph.endpoint`

+ Ceph 对象存储的 Endpoint
+ 默认：""
+ 用于访问 Ceph 对象存储

> **注意：**
>
> 一旦设置了 `ceph` 下的任何参数，备份和恢复就会使用 Ceph 对象存储进行数据存储。也就是说，假如要设置 `ceph` 下的参数，就需要保证所有 `ceph` 相关参数都得到正确配置，否则会造成备份恢复失败。

## `ceph.bucket`

+ Ceph 对象存储的 bucket 名字
+ 默认：""
+ 用于存储数据到 Ceph 对象存储上

## `ceph.secretName`

+ 访问 Ceph 对象存储时使用的凭据
+ 默认：""
+ 该 Kubernetes Secret 中需要存储访问 Ceph 时使用的 `access_key` 和 `secret_key`。可使用如下命令来创建这个 Secret：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic ceph-backup-secret -n <namespace> --from-literal=access_key=<access-key> --from-literal=secret_key=<secret-key>
    ```
