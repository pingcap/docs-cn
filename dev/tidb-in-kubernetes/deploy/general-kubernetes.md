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
mkdir -p /home/tidb/<releaseName> && \
helm inspect values pingcap/tidb-cluster --version=<chartVersion> > /home/tidb/<releaseName>/values-<releaseName>.yaml
```

> **注意：**
>
> `/home/tidb` 可以替换为你想用的目录。下文会用 `values.yaml` 指代 `/home/tidb/<releaseName>/values-<releaseName>.yaml`。

根据需要修改上述配置文件，有关配置信息请参考 [TiDB 集群部署配置文档](/tidb-in-kubernetes/reference/configuration/tidb-cluster.md)。

## 部署 TiDB 集群

TiDB Operator 部署并配置完成后，可以通过下面命令部署 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=<releaseName> --namespace=<namespace> --version=<chartVersion> -f /home/tidb/<releaseName>/values-<releaseName>.yaml
```

通过下面命令可以查看 Pod 状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n <namespace> -l app.kubernetes.io/instance=<releaseName>
```
