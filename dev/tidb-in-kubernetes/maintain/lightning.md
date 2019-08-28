---
title: 恢复 Kubernetes 上的 TiDB 集群数据
summary: 使用 TiDB Lightning 快速恢复 Kubernetes 上的 TiDB 集群数据。
category: how-to
---

# 恢复 Kubernetes 上的 TiDB 集群数据

本文介绍了如何使用 [TiDB Lightning](https://github.com/pingcap/tidb-lightning) 快速恢复 Kubernetes 上的 TiDB 集群数据。

TiDB Lightning 包含两个组件：tidb-lightning 和 tikv-importer。在 Kubernetes 上，tikv-importer 位于 TiDB 集群的 Helm chart 内，被部署为一个副本数为 1 (`replicas=1`) 的 `StatefulSet`；tidb-lightning 位于单独的 Helm chart 内，被部署为一个 `Job`。

为了使用 TiDB Lightning 恢复数据，tikv-importer 和 tidb-lightning 都必须分别部署。

## 部署 tikv-importer

tikv-importer 可以在一个现有的 TiDB 集群上启用，或者在新建 TiDB 集群时启用。

* 在新建一个 TiDB 集群时启用 tikv-importer：

    1. 在 `tidb-cluster` 的 `values.yaml` 文件中将 `importer.create` 设置为 `true`。

    2. 部署该集群。

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<tidb-cluster-release-name> --namespace=<namespace> -f values.yaml --version=<chart-version>
        ```

* 配置一个现有的 TiDB 集群以启用 tikv-importer：

    1. 在该 TiDB 集群的 `values.yaml` 文件中将 `importer.create` 设置为 `true`。

    2. 升级该 TiDB 集群。

        {{< copyable "shell-regular" >}}

        ```shell
        helm upgrade <tidb-cluster-release-name> pingcap/tidb-cluster -f values.yaml --version=<chart-version>
        ```

## 部署 tidb-lightning

1. 配置 TiDB Lightning

    使用如下命令获得 TiDB Lightning 的默认配置。

    {{< copyable "shell-regular" >}}

    ```shell
    helm inspect values pingcap/tidb-lightning --version=<chart-version> > tidb-lightning-values.yaml
    ```

    tidb-lightning Helm chart 支持恢复本地或远程的备份数据。

    * 本地模式

        本地模式要求 Mydumper 备份数据位于其中一个 Kubernetes 节点上。要启用该模式，你需要将 `dataSource.local.nodeName` 设置为该节点名称，将 `dataSource.local.hostPath` 设置为 Mydumper 备份数据目录路径，该路径中需要包含名为 `metadata` 的文件。

    * 远程模式

        与本地模式不同，远程模式需要使用 [rclone](https://rclone.org) 将 Mydumper 备份 tarball 文件从网络存储中下载到 PV 中。远程模式能在 rclone 支持的任何云存储下工作，目前已经有以下存储进行了相关测试：[Google Cloud Storage (GCS)](https://cloud.google.com/storage/)、[AWS S3](https://aws.amazon.com/s3/) 和 [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/)。

        1. 确保 `values.yaml` 中的 `dataSource.local.nodeName` 和 `dataSource.local.hostPath` 被注释掉。

        2. 新建一个包含 rclone 配置的 `Secret`。rclone 配置实例如下所示。只要求配置一种云存储。有关其他的云存储，请参考 [rclone 官方文档](https://rclone.org/)。

            {{< copyable "" >}}

            ```yaml
            apiVersion: v1
            kind: Secret
            metadata:
              name: cloud-storage-secret
            type: Opaque
            stringData:
              rclone.conf: |
              [s3]
              type = s3
              provider = AWS
              env_auth = false
              access_key_id = <my-access-key>
              secret_access_key = <my-secret-key>
              region = us-east-1
              [ceph]
              type = s3
              provider = Ceph
              env_auth = false
              access_key_id = <my-access-key>
              secret_access_key = <my-secret-key>
              endpoint = <ceph-object-store-endpoint>
              region = :default-placement
              [gcs]
              type = google cloud storage
              # The service account must include Storage Object Viewer role
              # The content can be retrieved by `cat <service-account-file.json> | jq -c .`
              service_account_credentials = <service-account-json-file-content>
            ```

            使用你的实际配置替换上述配置中的占位符，并将该文件存储为 `secret.yaml`。然后通过 `kubectl apply -f secret.yaml -n <namespace>` 命令创建该 `Secret`。

        3. 将 `dataSource.remote.storageClassName` 设置为 Kubernetes 集群中现有的一个存储类型。

2. 部署 TiDB Lightning

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-lightning --name=<tidb-lightning-release-name> --namespace=<namespace> --set failFast=true -f tidb-lightning-values.yaml --version=<chart-version>
    ```

当 TiDB Lightning 未能成功恢复数据时，不能简单地直接重启进程，必须进行**手动干预**，否则将很容易出现错误。因此，tidb-lightning 的 `Job` 重启策略被设置为 `Never`。

> **注意：**
>
> 目前，即使数据被成功恢复，TiDB Lightning 也会[报出非零错误码并退出](https://github.com/pingcap/tidb-lightning/pull/230)，这会导致 `Job` 失败。因此，数据恢复成功与否需要通过查看 tidb-lightning pod 的日志进行确认。

如果 TiDB Lightning 未能成功恢复数据，需要采用以下步骤进行手动干预：

1. 运行 `kubectl delete job -n <namespace> <tidb-lightning-release-name>-tidb-lightning`，删除 lightning `Job`。

2. 运行 `helm template pingcap/tidb-lightning --name <tidb-lightning-release-name> --set failFast=false -f tidb-lightning-values.yaml | kubectl apply -n <namespace> -f -`，重新创建禁用 `failFast` 的 lightning `Job`。

3. 当 lightning pod 重新运行时，在 lightning 容器中执行 `kubectl exec -it -n <namesapce> <tidb-lightning-pod-name> sh` 命令。

4. 运行 `cat /proc/1/cmdline`，获得启动脚本。

5. 参考[故障排除指南](/how-to/troubleshoot/tidb-lightning.md#tidb-lightning-troubleshooting)，对 lightning 进行诊断。

## 销毁 TiDB Lightning

目前，TiDB Lightning 只能在线下恢复数据。当恢复过程结束、TiDB 集群需要向外部应用提供服务时，可以销毁 TiDB Lightning 以节省开支。

删除 tikv-importer 的步骤：

1. 在 TiDB 集群 chart 的 `values.yaml` 文件中将 `importer.create` 设置为 `false`。

2. 然后运行 `helm upgrade <tidb-cluster-release-name> pingcap/tidb-cluster -f values.yaml`。

删除 tidb-lightning 的方法：

* 运行 `helm delete <tidb-lightning-release-name> --purge`。
