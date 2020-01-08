---
title: 重启 Kubernetes 上的 TiDB 集群
summary: 了解如何重启 Kubernetes 集群上的 TiDB 集群。
category: how-to
---

# 重启 Kubernetes 上的 TiDB 集群

本文描述了如何强制重启 Kubernetes 集群上的 TiDB 集群，包括重启某个 Pod，重启某个组件的所有 Pod 和重启 TiDB 集群的所有 Pod。

> **注意：**
>
> TiDB Operator v1.0.x 版本只支持强制重启 Pod。
>
> - 在强制重启 PD Pod 过程中，如果被重启的 PD Pod 是 Leader，重启过程不会自动迁移 Leader，这会导致 PD 服务短时间中断。
> - 在强制重启 TiKV Pod 过程中，不会自动迁移 TiKV 的 Region Leader，会导致访问对应数据的请求异常。
> - 在强制重启 TiDB Pod 过程中，会导致访问对应 TiDB 的请求失败。

## 强制重启某个 Pod

要强制重启某个 Pod，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> <pod-name>
```

## 强制重启某个组件的所有 Pod

通过以下命令可以列出组件目前有哪些 Pod：

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

要强制重启某个组件的所有 Pod，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

把 `<component-name>` 分别替换为 `pd`、`tidb`、`tikv`，可以分别强制重启 `PD`、`TiDB`、`TiKV` 组件所有 Pod。

## 强制重启 TiDB 集群的所有 Pod

通过以下命令可以列出 TiDB 集群目前有哪些 Pod，包括 `monitor`、`discovery` 等：

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```

要强制重启 TiDB 集群的所有 Pod，包括 `monitor`、`discovery` 等，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```
