---
title: Kubernetes 上的 TiDB 集群扩缩容
category: how-to
---

# Kubernetes 上的 TiDB 集群扩缩容

本文介绍 TiDB 在 Kubernetes 中如何进行水平扩缩容和垂直扩缩容。

## 水平扩缩容

TiDB 水平扩缩容操作指的是通过增加或减少节点的数量，来达到集群扩缩容的目的。扩缩容 TiDB 集群时，会按照填入的 replicas 值，对 PD、TiKV、TiDB 进行顺序扩缩容操作。扩容操作按照节点编号由小到大增加节点，缩容操作按照节点编号由大到小删除节点。

### 水平扩缩容操作

1. 修改集群的 `value.yaml` 文件中的 `pd.replicas`、`tidb.replicas`、`tikv.replicas` 至期望值。

2. 执行 `helm upgrade` 命令进行扩缩容：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

3. 查看集群水平扩缩容状态：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n ${namespace} get pod -o wide
    ```

    当所有组件的 Pod 数量都达到了预设值，并且都进入  `Running` 状态后，水平扩缩容完成。

> **注意：**
>
> - PD、TiKV 组件在滚动升级的过程中不会触发扩缩容操作。
> - PD、TiKV 组件在缩容过程中都会调用接口下线正在删除的 PD、TiKV 组件在下线时会涉及到数据迁移的操作，所以会消耗比较长的时间。
> - PD、TiKV 组件在缩容过程中被删除的节点的 PVC 会保留，并且由于 PV 的 `Reclaim Policy` 设置为 `Retain`，即使 PVC 被删除，数据依然可以找回。

## 垂直扩缩容

垂直扩缩容操作指的是通过增加或减少节点的资源限制，来达到集群扩缩容的目的。垂直扩缩容本质上是节点滚动升级的过程。

### 垂直扩缩容操作

1. 修改 `values.yaml` 文件中的 `tidb.resources`、`tikv.resources`、`pd.resources` 至期望值。

2. 执行 `helm upgrade` 命令进行升级：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade ${releaseName} pingcap/tidb-cluster -f values.yaml --version=v1.0.0-beta.3
    ```

3. 查看升级进度：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n ${namespace} get pod -o wide
    ```

    当所有 Pod 都重建完毕进入 `Running` 状态后，垂直扩缩容完成。

> **注意：**
>
> - 如果在垂直扩容时修改了资源的 `requests` 字段，由于 PD、TiKV 使用了 `Local PV`，升级后还需要调度回原节点，如果原节点资源不够，则会导致 Pod 一直处于 `Pending` 状态而影响服务。
> - TiDB 作为一个可水平扩展的数据库，推荐发挥 TiDB 集群可水平扩展的优势，而不是类似传统数据库仅仅是进行资源的叠加。
