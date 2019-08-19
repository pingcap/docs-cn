---
title: 在标准 Kubernetes 上部署 TiDB 集群
category: how-to
---

# 在标准 Kubernetes 上部署 TiDB 集群

本文主要描述了如何在标准的 Kubernetes 集群上通过 TiDB Operator 部署 TiDB 集群

## 前置条件

* 参考 [TiDB Operator](/tidb-in-kubernetes/deploy/tidb-operator.md) 完成集群中的 TiDB Operator 部署；
* 参考 [使用 Helm](/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm) 安装 Helm 并配置 PingCAP 官方 chart 仓库。

## 配置 TiDB 集群

通过下面命令获取待安装的 tidb-cluster chart 的 `values.yaml` 配置文件：

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/<release-name> && \
helm inspect values pingcap/tidb-cluster --version=<chart-version> > /home/tidb/<release-name>/values-<release-name>.yaml
```

> **注意：**
>
> - `/home/tidb` 可以替换为你想用的目录。
> - `release-name` 将会作为 Kubernetes 相关资源（例如 Pod，Service 等）的前缀名，可以起一个方便记忆的名字，要求全局唯一，通过 `helm ls -q` 可以查看集群中已经有的 `release-name`。
> - `chart-version` 是 tidb-cluster chart 发布的版本，可以通过 `helm search -l tidb-cluster` 查看当前支持的版本。
> - 下文会用 `values.yaml` 指代 `/home/tidb/<release-name>/values-<release-name>.yaml`。

默认集群使用 `local-storage` 存储类型，生产环境推荐使用本地存储，但实际 Kubernetes 集群中本地存储可能按磁盘类型进行了分类，例如 `nvme-disks`, `sas-disks`，如果是 demo 环境或功能性验证，可以使用网络存储，例如 `ebs`, `nfs` 等，另外 TiDB 集群不同组件对磁盘的要求不一样。所以部署集群前要根据当前 Kubernetes 集群支持的存储类型以及使用场景为 TiDB 集群各组件选择合适的存储类型，通过修改 `values.yaml` 中各组件的 `storageClassName` 字段设置存储类型。关于 Kubernetes 集群支持哪些存储类型，请联系系统管理员确定。

如果创建集群时设置了集群中不存在的存储类型，则会导致集群创建处于 Pending 状态，需要将[集群彻底销毁掉](/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md)。

默认部署的集群拓扑是：3 个 PD，3 个 TiKV，2 个 TiDB 和 1 个监控。TiDB Operator 扩展调度器根据数据高可用要求 Kubernetes 集群至少有 3 个节点，否则请减小默认部署的 PD 和 TiKV 个数为 1，或者将 `values.yaml` 中 `schedulerName` 改为 Kubernetes 内置调度器 `default-scheduler`。

其它更多配置参数请参考 [TiDB 集群部署配置文档](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md)。

## 部署 TiDB 集群

TiDB Operator 部署并配置完成后，可以通过下面命令部署 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f /home/tidb/<release-name>/values-<release-name>.yaml
```

通过下面命令可以查看 Pod 状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n <namespace> -l app.kubernetes.io/instance=<release-name>
```

单个 Kubernetes 集群中可以利用 TiDB Operator 部署管理多套 TiDB 集群，重复上面命令并将 `release-name` 替换成不同名字即可。不同集群可以在相同 `namespace` 中也可以是在不同 `namespace` 中，可根据实际需求选择。
