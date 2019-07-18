---
title: 在标准 Kubernetes 上部署 TiDB 集群
category: how-to
---

# 部署 TiDB 集群

本文主要描述了如何在一般的 Kubernetes 集群上通过 TiDB Operator 部署 TiDB 集群

## 前置条件

### TiDB Operator 部署完成

如果该 Kubernetes 集群中尚未部署 TiDB Operator，请参考：[TiDB Operator](/how-to/deploy/tidb-operator.md) 完成 TiDB Operator 的部署

### Helm 添加仓库

{{< copyable "shell-regular" >}}

``` shell
helm repo add pingcap http://charts.pingcap.org/
```

{{< copyable "shell-regular" >}}

``` shell
helm repo list
```

然后可以查看可用的 chart：

{{< copyable "shell-regular" >}}

``` shell
helm repo update
```

{{< copyable "shell-regular" >}}

``` shell
helm search tidb-cluster -l
```

{{< copyable "shell-regular" >}}

``` shell
helm search tidb-operator -l
```

## 配置

通过下面命令获取待安装的 tidb-cluster chart 的 `values.yaml` 配置文件：

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/${releaseName} && \
helm inspect values pingcap/tidb-cluster --version=${chartVersion} > /home/tidb/${releaseName}/values-${releaseName}.yaml
```

> **注意：**
>
> `/home/tidb` 可以替换为你想用的目录。下文会用 `values.yaml` 指代 `/home/tidb/${releaseName}/values-${releaseName}.yaml`。

根据需要修改上述配置文件，有关配置信息请参考 [TiDB 集群部署配置文档](/reference/configuration/tidb-in-kubernetes/cluster-configuration.md)。

## 部署

TiDB Operator 部署并配置完成后，可以通过下面命令部署 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=${releaseName} --namespace=${namespace} --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

通过下面命令可以查看 Pod 状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n ${namespace} -l app.kubernetes.io/instance=${releaseName}
```