---
title: Maintain TiDB Binlog
summary: Learn how to maintain TiDB Binlog of a TiDB cluster in Kubernetes.
category: how-to
---

# Maintain TiDB Binlog

This document describes how to maintain [TiDB Binlog](/v3.0/reference/tidb-binlog/overview.md) of a TiDB cluster in Kubernetes.

## Prerequisites

- [Deploy TiDB Operator](/v3.0/tidb-in-kubernetes/deploy/tidb-operator.md);
- [Install Helm](/v3.0/tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) and configure it with the official PingCAP chart.

## Enable TiDB Binlog of a TiDB cluster

TiDB Binlog is disabled in the TiDB cluster by default. To create a TiDB cluster with TiDB Binlog enabled, or enable TiDB Binlog in an existing TiDB cluster:

1. Modify the `values.yaml` file as described below:

    * Set `binlog.pump.create` to `true`.
    * Set `binlog.drainer.create` to `true`.
    * Set `binlog.pump.storageClassName` and `binlog.drainer.storageClassName` to an available `storageClass` in your Kubernetes cluster.
    * Set `binlog.drainer.destDBType` to your desired downstream storage as needed, which is explained in details below.

        TiDB Binlog supports three types of downstream storage:

        * PersistenceVolume: the default downstream storage. You can configure a large PV for `drainer` (by modifying `binlog.drainer.storage`) in this case.
        * MySQL compatible databases: enabled by setting `binlog.drainer.destDBType` to `mysql`. Meanwhile, you must configure the address and credential of the target database in `binlog.drainer.mysql`.
        * Apache Kafka: enabled by setting `binlog.drainer.destDBType` to `kafka`. Meanwhile, you must configure the zookeeper address and Kafka address of the target cluster in `binlog.drainer.kafka`.

2. Set affinity and anti-affinity for TiDB and the Pump component:

    > **Note:**
    >
    > If you enable TiDB Binlog in the production environment, it is recommended to set affinity and anti-affinity for TiDB and the Pump component; if you enable TiDB Binlog in a test environment on the internal network, you can skip this step.

    By default, TiDB's affinity is set to `{}`. Currently, each TiDB instance does not have a corresponding Pump instance by default. When TiDB Binlog is enabled, if Pump and TiDB are separately deployed and network isolation occurs, and `ignore-error` is enabled, TiDB loses binlogs. In this situation, it is recommended to deploy a TiDB instance and a Pump instance on the same node using the affinity feature, and to split Pump instances on different nodes using the anti-affinity feature. For each node, only one Pump instance is required.

    > Note:
    >
    > `<release-name>` needs to be replaced with the `Helm-release-name` of the target `tidb-cluster` chart.

    * Configure `tidb.affinity` as follows:

        {{< copyable "" >}}

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

    * Configure `binlog.pump.affinity` as follows:

        {{< copyable "" >}}

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

3. Create a new TiDB cluster or update an existing cluster:

    * Create a new TiDB cluster with TiDB Binlog enabled:

        {{< copyable "shell-regular" >}}

        ```shell
        helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f <values-file>
        ```

    * Update an existing TiDB cluster to enable TiDB Binlog:

        > Note:
        >
        > If you set the affinity for TiDB and its components, updating the existing TiDB cluster causes rolling updates of the TiDB components in the cluster.

        {{< copyable "shell-regular" >}}

        ```shell
        helm upgrade <release-name> pingcap/tidb-cluster --version=<chart-version> -f <values-file>
        ```

## Deploy multiple drainers

By default, only one downstream drainer is created. You can install the `tidb-drainer` Helm chart to deploy more drainers for a TiDB cluster, as described below:

1. Make sure that the PingCAP Helm repository is up to date:

    {{< copyable "shell-regular" >}}

    ```shell
    helm repo update
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm search tidb-drainer -l
    ```

2. Get the default `values.yaml` file to facilitate customization:

    ```shell
    helm inspect values pingcap/tidb-drainer --version=<chart-version> > values.yaml
    ```

3. Modify the `values.yaml` file to specify the source TiDB cluster and the downstream database of the drainer. Here is an example:

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

    The `clusterName` and `clusterVersion` must match the desired source TiDB cluster.

    For complete configuration details, refer to [TiDB Binlog Drainer Configurations in Kubernetes](/v3.0/tidb-in-kubernetes/reference/configuration/tidb-drainer.md).

4. Deploy the drainer:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-drainer --name=<release-name> --namespace=<namespace> --version=<chart-version> -f values.yaml
    ```

    > **Note:**
    >
    > This chart must be installed to the same namespace as the source TiDB cluster.
