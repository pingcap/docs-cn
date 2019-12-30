---
title: 重启 TiDB 集群
category: how-to
---

# 重启 TiDB 集群

本文描述了如何重启 Kubernetes 集群上的 TiDB 集群，包括重启某个 Pod，重启某个组件的所有 Pod 和 重启 TiDB 集群的所有 Pod。

## 重启某个 Pod

要重启某个 Pod，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> <pod-name>
```

## 重启某个组件的所有 Pod

通过以下命令可以列出组件目前有哪些 Pod：

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

要重启某个组件的所有 Pod，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

把 `<component-name>` 分别替换为 `pd`、`tidb`、`tikv`，可以分别重启 `PD`、`TiDB`、`TiKV` 组件所有 Pod。

## 重启 TiDB 集群的所有 Pod

通过以下命令可以列出 TiDB 集群目前有哪些 Pod，包括 `monitor`、`discovery` 等：

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```

要重启 TiDB 集群的所有 Pod，包括 `monitor`、`discovery` 等，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```
