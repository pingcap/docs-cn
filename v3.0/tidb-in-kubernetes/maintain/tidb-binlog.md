---
title: TiDB Binlog 运维
summary: 了解如何在 Kubernetes 上运维 TiDB 集群的 TiDB Binlog。
category: how-to
---

# TiDB Binlog 运维

本文档介绍如何在 Kubernetes 上运维 TiDB 集群的 [TiDB Binlog](/v3.0/reference/tools/tidb-binlog/overview.md)。

## 运维准备

- [部署 TiDB Operator](/v3.0/tidb-in-kubernetes/deploy/tidb-operator.md)；
- [安装 Helm](/v3.0/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm) 并配置 PingCAP 官方 chart 仓库。

## 启用 TiDB 集群的 TiDB Binlog

默认情况下，TiDB Binlog 在 TiDB 集群中处于禁用状态。若要创建一个启用 TiDB Binlog 的 TiDB 集群，或在现有 TiDB 集群中启用 TiDB Binlog，可根据以下步骤进行操作：

1. 按照以下说明修改 `values.yaml` 文件：

    * 将 `binlog.pump.create` 的值设为 `true`。
    * 将 `binlog.drainer.create` 的值设为 `true`。
    * 将 `binlog.pump.storageClassName` 和 `binlog.drainer.storageClassName` 设为所在 Kubernetes 集群上可用的 `storageClass`。
    * 将 `binlog.drainer.destDBType` 设为所需的下游存储类型。

        TiDB Binlog 支持三种下游存储类型：

        * PersistenceVolume：默认的下游存储类型。可通过修改 `binlog.drainer.storage` 来为 `drainer` 配置大 PV。

        * 与 MySQL 兼容的数据库：通过将 `binlog.drainer.destDBType` 设置为 `mysql` 来启用。同时，必须在 `binlog.drainer.mysql` 中配置目标数据库的地址和凭据。

        * Apache Kafka：通过将 `binlog.drainer.destDBType` 设置为 `kafka` 来启用。同时，必须在 `binlog.drainer.kafka` 中配置目标集群的 zookeeper 地址和 Kafka 地址。

2. 创建一个新的 TiDB 集群或更新现有的集群：

    * 创建一个启用 TiDB Binlog 的 TiDB 新集群：

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f <values-file>
        ```

    * 更新现有的 TiDB 集群以启用 TiDB Binlog：

        {{< copyable "shell-regular" >}}

        ```shell
        helm upgrade <release-name> pingcap/tidb-cluster --version=<chart-version> -f <values-file>
        ```

## 部署多个 drainer

默认情况下，仅创建一个下游 drainer。可安装 `tidb-drainer` Helm chart 来为 TiDB 集群部署多个 drainer，示例如下：

1. 确保 PingCAP Helm 库是最新的：

    {{< copyable "shell-regular" >}}

    ```shell
    helm repo update
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm search tidb-drainer -l
    ```

2. 获取默认的 `values.yaml` 文件以方便自定义：

    {{< copyable "shell-regular" >}}

    ```shell
    helm inspect values pingcap/tidb-drainer --version=<chart-version> > values.yaml
    ```

3. 修改 `values.yaml` 文件以指定源 TiDB 集群和 drainer 的下游数据库。示例如下：

    ```yaml
    clusterName: example-tidb
    clusterVersion: v3.0.0
    storageClassName: local-storage
    storage: 10Gi
    config: |
      detect-interval = 10
      [syncer]
      worker-count = 16
      txn-batch = 20
      disable-dispatch = false
      ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"
      safe-mode = false
      db-type = "tidb"
      [syncer.to]
      host = "slave-tidb"
      user = "root"
      password = ""
      port = 4000
    ```

    `clusterName` 和 `clusterVersion` 必须匹配所需的源 TiDB 集群。

    有关完整的配置详细信息，请参阅 [Kubernetes 上的 TiDB Binlog Drainer 配置](/v3.0/tidb-in-kubernetes/reference/configuration/tidb-drainer.md)。

4. 部署 drainer：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-drainer --name=<release-name> --namespace=<namespace> --version=<chart-version> -f values.yaml
    ```

    > **注意：**
    >
    > 该 chart 必须与源 TiDB 集群安装在相同的命名空间中。
