---
title: 在 Kubernetes 上部署 TiDB Operator
summary: 了解如何在 Kubernetes 上部署 TiDB Operator
category: how-to
aliases: ['/docs-cn/v3.0/how-to/deploy/tidb-in-kubernetes/tidb-operator/']
---

# 在 Kubernetes 上部署 TiDB Operator

本文介绍如何在 Kubernetes 上部署 TiDB Operator。

## 准备环境

TiDB Operator 部署前，请确认以下软件需求：

* Kubernetes v1.12 或者更高版本
* [DNS 插件](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/)
* [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
* [RBAC](https://kubernetes.io/docs/admin/authorization/rbac) 启用（可选）
* [Helm](https://helm.sh) 版本 >= v2.8.2 && < v3.0.0

> **注意：**
>
> - 尽管 TiDB Operator 可以使用网络卷持久化 TiDB 数据，TiDB 数据自身会存多副本，再走额外的网络卷通常会比较慢。强烈建议搭建[本地卷](https://kubernetes.io/docs/concepts/storage/volumes/#local)以提高性能。
> - 跨多可用区的网络卷需要 Kubernetes v1.12 或者更高版本。在 `tidb-backup` chart 配置中，建议使用网络卷存储备份数据。

## 部署 Kubernetes 集群

TiDB Operator 运行在 Kubernetes 集群，你可以使用[这里](https://kubernetes.io/docs/setup/)列出的任何一种方法搭建一套 Kubernetes 集群。只要保证 Kubernetes 版本大于等于 v1.12。如果你使用 AWS、GKE 或者本机，下面是快速上手教程：

* [Local DinD 教程](/v3.0/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind.md)
* [Google GKE 教程](/v3.0/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-gke.md)
* [AWS EKS 教程](/v3.0/tidb-in-kubernetes/deploy/aws-eks.md)

如果你要使用不同环境，必须在 Kubernetes 集群中安装 DNS 插件。可以根据[官方文档](https://kubernetes.io/docs/tasks/access-application-cluster/configure-dns-cluster/)搭建 DNS 插件。

TiDB Operator 使用[持久化卷](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)持久化存储 TiDB 集群数据（包括数据库，监控和备份数据），所以 Kubernetes 集群必须提供至少一种持久化卷。为提高性能，建议使用本地 SSD 盘作为持久化卷。可以根据[这一步](#配置本地持久化卷)自动配置本地持久化卷。

Kubernetes 集群建议启用 [RBAC](https://kubernetes.io/docs/admin/authorization/rbac)。否则，需要在 `tidb-operator` 和 `tidb-cluster` chart 的 `values.yaml` 中设置 `rbac.create` 为 `false`。

TiDB 默认会使用很多文件描述符，工作节点和上面的 Docker 进程的 `ulimit` 必须设置大于等于 `1048576`：

* 设置工作节点的 `ulimit` 值，详情可以参考[如何设置 ulimit](https://access.redhat.com/solutions/61334)

    {{< copyable "shell-regular" >}}

    ```shell
    sudo vim /etc/security/limits.conf
    ```

    设置 root 账号的 `soft` 和 `hard` 的 `nofile` 大于等于 `1048576`

* 设置 Docker 服务的 `ulimit`

    {{< copyable "shell-regular" >}}

    ```shell
    sudo vim /etc/systemd/system/docker.service
    ```

    设置 `LimitNOFILE` 大于等于 `1048576`。

## 安装 Helm

参考 [使用 Helm](/v3.0/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm) 安装 Helm 并配置 PingCAP 官方 chart 仓库。

## 配置本地持久化卷

### 准备本地卷

参考[本地 PV 配置](/v3.0/tidb-in-kubernetes/reference/configuration/storage-class.md#本地-pv-配置)在你的 Kubernetes 集群中配置本地持久化卷。

## 安装 TiDB Operator

TiDB Operator 使用 [CRD (Custom Resource Definition)](https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/) 扩展 Kubernetes，所以要使用 TiDB Operator，必须先创建 `TidbCluster` 自定义资源类型。只需要在你的 Kubernetes 集群上创建一次即可：

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/crd.yaml && \
kubectl get crd tidbclusters.pingcap.com
```

创建 `TidbCluster` 自定义资源类型后，接下来在 Kubernetes 集群上安装 TiDB Operator。

1. 获取你要安装的 `tidb-operator` chart 中的 `values.yaml` 文件：

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /home/tidb/tidb-operator && \
    helm inspect values pingcap/tidb-operator --version=<chart-version> > /home/tidb/tidb-operator/values-tidb-operator.yaml
    ```

    > **注意：**
    >
    > `<chart-version>` 在后续文档中代表 chart 版本，例如 `v1.0.0`，可以通过 `helm search -l tidb-operator` 查看当前支持的版本。

2. 配置 TiDB Operator

    TiDB Operator 里面会用到 `k8s.gcr.io/kube-scheduler` 镜像，如果下载不了该镜像，可以修改 `/home/tidb/tidb-operator/values-tidb-operator.yaml` 文件中的 `scheduler.kubeSchedulerImage` 为 `registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler`。

3. 安装 TiDB Operator

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=<chart-version> -f /home/tidb/tidb-operator/values-tidb-operator.yaml && \
    kubectl get po -n tidb-admin -l app.kubernetes.io/name=tidb-operator
    ```

## 自定义 TiDB Operator

通过修改 `/home/tidb/tidb-operator/values-tidb-operator.yaml` 中的配置自定义 TiDB Operator。后续文档使用 `values.yaml` 指代 `/home/tidb/tidb-operator/values-tidb-operator.yaml`。

TiDB Operator 有两个组件：

* tidb-controller-manager
* tidb-scheduler

这两个组件是无状态的，通过 `Deployment` 部署。你可以在 `values.yaml` 中自定义资源 `limit`、`request` 和 `replicas`。

修改为 `values.yaml` 后，执行下面命令使配置生效：

{{< copyable "shell-regular" >}}

```shell
helm upgrade tidb-operator pingcap/tidb-operator --version=<chart-version> -f /home/tidb/tidb-operator/values-tidb-operator.yaml
```
