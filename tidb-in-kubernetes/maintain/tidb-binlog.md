---
title: TiDB Binlog 运维
summary: 了解如何在 Kubernetes 上运维 TiDB 集群的 TiDB Binlog。
category: how-to
---

# TiDB Binlog 运维

本文档介绍如何在 Kubernetes 上运维 TiDB 集群的 [TiDB Binlog](/reference/tidb-binlog/overview.md)。

## 运维准备

- [部署 TiDB Operator](/tidb-in-kubernetes/deploy/tidb-operator.md)；
- [安装 Helm](/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm) 并配置 PingCAP 官方 chart 仓库。

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

2. 为 TiDB 与 Pump 组件设置亲和性和反亲和性：

    > **注意：**
    >
    > 如果在生产环境中开启 TiDB Binlog，建议为 TiDB 与 Pump 组件设置亲和性和反亲和性。如果在内网测试环境中尝试使用开启 TiDB Binlog，可以跳过此步。

    默认情况下，TiDB 的 affinity 亲和性设置为 `{}`。由于目前 Pump 组件与 TiDB 组件默认并非一一对应，当启用 TiDB Binlog 时，如果 Pump 与 TiDB 组件分开部署并出现网络隔离，而且 TiDB 组件还开启了 `ignore-error`，则会导致 TiDB 丢失 Binlog。推荐通过亲和性特性将 TiDB 组件与 Pump 部署在同一台 Node 上，同时通过反亲和性特性将 Pump 分散在不同的 Node 上，每台 Node 上至多仅需一个 Pump 实例。

    > **注意：**
    >
    > `<release-name>` 需要替换为目标 `tidb-cluster` 的 Helm release name。

    * 将 `tidb.affinity` 按照如下设置：

        ```yaml
        tidb:
          affinity:
            podAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                - labelSelector:
                    matchExpressions:
                      - key: "app.kubernetes.io/component"
                        operator: In
                        values:
                          - "pump"
                      - key: "app.kubernetes.io/managed-by"
                        operator: In
                        values:
                          - "tidb-operator"
                      - key: "app.kubernetes.io/name"
                        operator: In
                        values:
                          - "tidb-cluster"
                      - key: "app.kubernetes.io/instance"
                        operator: In
                        values:
                          - <release-name>
                  topologyKey: kubernetes.io/hostname
        ```

    * 将 `binlog.pump.affinity` 按照如下设置：

        ```yaml
        binlog:
          pump:
            affinity:
              podAffinity:
                preferredDuringSchedulingIgnoredDuringExecution:
                - weight: 100
                  podAffinityTerm:
                    labelSelector:
                      matchExpressions:
                      - key: "app.kubernetes.io/component"
                        operator: In
                        values:
                        - "tidb"
                      - key: "app.kubernetes.io/managed-by"
                        operator: In
                        values:
                        - "tidb-operator"
                      - key: "app.kubernetes.io/name"
                        operator: In
                        values:
                        - "tidb-cluster"
                      - key: "app.kubernetes.io/instance"
                        operator: In
                        values:
                        - <release-name>
                    topologyKey: kubernetes.io/hostname
              podAntiAffinity:
                preferredDuringSchedulingIgnoredDuringExecution:
                - weight: 100
                  podAffinityTerm:
                    labelSelector:
                      matchExpressions:
                      - key: "app.kubernetes.io/component"
                        operator: In
                        values:
                        - "pump"
                      - key: "app.kubernetes.io/managed-by"
                        operator: In
                        values:
                        - "tidb-operator"
                      - key: "app.kubernetes.io/name"
                        operator: In
                        values:
                        - "tidb-cluster"
                      - key: "app.kubernetes.io/instance"
                        operator: In
                        values:
                        - <release-name>
                    topologyKey: kubernetes.io/hostname
        ```

3. 创建一个新的 TiDB 集群或更新现有的集群：

    * 创建一个启用 TiDB Binlog 的 TiDB 新集群：

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f <values-file>
        ```

    * 更新现有的 TiDB 集群以启用 TiDB Binlog：

        > **注意：**
        >
        > 如果设置了 TiDB 组件的亲和性，那么更新现有的 TiDB 集群将引起 TiDB 集群中的 TiDB 组件滚动更新。

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

    有关完整的配置详细信息，请参阅 [Kubernetes 上的 TiDB Binlog Drainer 配置](/tidb-in-kubernetes/reference/configuration/tidb-drainer.md)。

4. 部署 drainer：

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-drainer --name=<release-name> --namespace=<namespace> --version=<chart-version> -f values.yaml
    ```

    > **注意：**
    >
    > 该 chart 必须与源 TiDB 集群安装在相同的命名空间中。
