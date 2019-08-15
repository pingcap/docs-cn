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

根据需要修改上述配置文件，有关配置信息请参考 [TiDB 集群部署配置文档](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md)。

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
