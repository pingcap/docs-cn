---
title: 重启 TiDB 集群
category: how-to
---

# 重启 TiDB 集群

本文描述了如何重启 Kubernetes 集群上的 TiDB 集群，包括重启某个 Pod，重启某个组件的所有 Pod 和 重启 TiDB 集群的所有 Pod。

## 重启某个 Pod

### 强制重启某个 Pod

要强制重启某个 Pod，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> <pod-name>
```

### 优雅重启 PD Pod

强制重启 PD Pod 过程中，如果被重启的 PD Pod 是 leader，重启过程不会自动迁移 leader，会导致 PD 服务短时间中断，如果要保证重启过程中服务不中断，请按照如下步骤实现优雅重启 PD：

1. 登录 PD 集群 Pod。

{{< copyable "shell-regular" >}}

```shell
kubectl exec -it -n <namespace> <tidb-cluster-name>-pd-0 sh
```

2. 进入 PD Pod 后，执行如下命令，进入 pd-ctl 交互界面。

{{< copyable "shell-regular" >}}

```shell
./pd-ctl -i -u http://127.0.0.1:2379
```

3. 在 pd-ctl 交互界面，通过 `member` 命令找到当前 PD 集群都有哪些 member，通过 `member leader show` 命令找到当前 leader，具体操作步骤请参考[链接](https://pingcap.com/docs-cn/stable/reference/tools/pd-control/#member-delete--leader_priority--leader-show--resign--transfer-member_name)。

4. 对于 follower member，参考[强制重启步骤](#强制重启某个-Pod)，重启 Pod。

5. 对于 leader，在 pc-ctl 交互界面，通过 `member leader resign` 命令 resign 当前 PD leader，并通过 `member leader show` 命令确认 leader 已经迁移到另外的 PD Pod，参考[强制重启步骤](#强制重启某个-Pod)，重启这个 PD Pod。

### 优雅重启 TiKV Pod

强制重启 TiKV Pod 过程中，不会自动迁移 TiKV 的 region leader，会导致访问对应数据的请求异常，如果要保证重启过程中服务不受影响，请按照如下步骤实现优雅重启 TiKV：

1. 登录 PD 集群 Pod。

{{< copyable "shell-regular" >}}

```shell
kubectl exec -it -n <namespace> <tidb-cluster-name>-pd-0 sh
```

2. 进入 PD Pod 后，执行如下命令，进入 pd-ctl 交互界面。

{{< copyable "shell-regular" >}}

```shell
./pd-ctl -i -u http://127.0.0.1:2379
```

3. 在 pd-ctl 交互界面，通过 `store` 命令可以看到当前 TiKV 集群都有哪些 store 及其对应的 id 和 address，通过 `store <id>` 命令输出中的 `leader_count` 可以看到当前 store 中有多少 leader，具体操作步骤请参考[链接](https://pingcap.com/docs-cn/stable/reference/tools/pd-control/#store-delete--label--weight-store_id--jqquery-string)。

4. 对于要删除的 Pod，在 pd-ctl 交互界面，通过 `scheduler add evict-leader-scheduler <id>` 命令把对应 store 上的 region leader 调度到别的 store，并通过 `store <id>` 命令，确认当前 store 中已经没有 region leader，参考[强制重启步骤](#强制重启某个-Pod)，重启 Pod。

5. Pod 重启完成后，在 pd-ctl 交互界面，通过 `scheduler remove evict-leader-scheduler-<id>` 命令把对应 store 上的 scheduler 删掉，并通过 `store <id>` 命令，确认当前 store 中已经有 region leader 调度上来。

### 优雅重启 TiDB Pod

强制重启 TiDB Pod 过程中，会导致访问对应 TiDB 的请求失败。
如果 TiDB 集群前面有负载均衡器，需要在重启 Pod 之前将对应的 TiDB IP 从负载均衡器配置中移除，重启完成后，再添加到负载均衡器配置中。

## 重启某个组件的所有 Pod

### 强制重启某个组件的所有 Pod

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

### 优雅重启 PD 组件所有 Pod

强制重启 PD Pod 过程中，如果被重启的 PD Pod 是 leader，重启过程不会自动迁移 leader，会导致 PD 服务短时间中断，如果要保证重启过程中服务不中断，请按照如下步骤实现优雅重启：

1. 登录 PD 集群 Pod。

{{< copyable "shell-regular" >}}

```shell
kubectl exec -it -n <namespace> <tidb-cluster-name>-pd-0 sh
```

2. 进入 PD Pod 后，执行如下命令，进入 pd-ctl 交互界面。

{{< copyable "shell-regular" >}}

```shell
./pd-ctl -i -u http://127.0.0.1:2379
```

3. 在 pd-ctl 交互界面，通过 `member`、`member leader show` 命令找到当前 PD 集群都有哪些 member，并找到当前 leader，具体操作步骤请参考[链接](https://pingcap.com/docs-cn/stable/reference/tools/pd-control/#member-delete--leader_priority--leader-show--resign--transfer-member_name)。

4. 参考[强制重启步骤](#强制重启某个-Pod)，重启所有 follower member。

5. 在 pc-ctl 交互界面，通过 `member leader resign` 命令 resign 当前 PD leader，并通过 `member leader show` 命令确认 leader 已经迁移到另外的 PD Pod，参考[强制重启步骤](#强制重启某个-Pod)，重启这个 PD Pod。

### 优雅重启 TiKV 组件所有 Pod

参考[优雅重启 TiKV Pod](#优雅重启-TiKV-Pod) 一个一个重启 TiKV 组件所有 Pod。

### 优雅重启 TiDB 组件所有 Pod

参考[优雅重启 TiDB Pod](#优雅重启-TiDB-Pod) 一个一个重启 TiDB 组件所有 Pod。

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

> **注意：**
>
> 强制重启集群内所有 Pod 会导致对应组件业务中断，对于 PD、TiKV、TiDB 建议分别参考[优雅重启 PD 组件所有 Pod](#优雅重启-PD-组件所有-Pod)、[优雅重启 TiKV 组件所有 Pod](#优雅重启-TiKV-组件所有-Pod) 和[优雅重启 TiDB 组件所有 Pod](#优雅重启-TiDB-组件所有-Pod) 实现优雅重启。