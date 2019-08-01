---
title: 维护 TiDB 集群所在的 Kubernetes 节点
category: how-to
---

# 维护 TiDB 集群所在的 Kubernetes 节点

TiDB 是高可用数据库，可以在部分数据库节点下线的情况下正常运行，因此，我们可以安全地对底层 Kubernetes 节点进行停机维护。在具体操作时，针对 PD、TiKV 和 TiDB 实例的不同特性，我们需要采取不同的操作策略。

本文档将详细介绍如何对 Kubernetes 节点进行临时或长期的维护操作。

环境准备：

- [`kubectl`](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [`tkctl`](/reference/tools/tkctl.md)
- [`jq`](https://stedolan.github.io/jq/download/)

> **注意：**
>
> 长期维护节点前，需要保证 Kubernetes 集群的剩余资源足够运行 TiDB 集群。

## 维护 PD 和 TiDB 实例所在节点

PD 和 TiDB 实例的迁移较快，可以采取主动驱逐实例到其它节点上的策略进行节点维护：

1. 检查待维护节点上是否有 TiKV 实例：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pod --all-namespaces -o wide | grep <node-name>
    ```

    假如存在 TiKV 实例，请参考[维护 TiKV 实例所在节点](#维护-tikv-实例所在节点)。

2. 使用 `kubectl cordon` 命令防止新的 Pod 调度到待维护节点上：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl cordon <node-name>
    ```

3. 使用 `kubectl drain` 命令将待维护节点上的数据库实例迁移到其它节点上：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl drain <node-name> --ignore-daemonsets --delete-local-data
    ```

    运行后，该节点上的 TiDB 实例会自动迁移到其它可用节点上，PD 实例则会在 5 分钟后触发自动故障转移补齐节点。

4. 此时，假如希望下线该 Kubernetes 节点，则可以将该节点删除：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete node <node-name>
    ```

    假如希望恢复 Kubernetes 节点，则需要在恢复节点后确认其健康状态：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl get node <node-name>
    ```

    观察到节点进入 `Ready` 状态后，继续操作。

5. 使用 `kubectl uncordon` 命令解除节点的调度限制：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl uncordon <node-name>
    ```

6. 观察 Pod 是否全部恢复正常运行：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl get -n $namespace pod -o wide
    ```

    或者：

    {{< copyable "shell-regular" >}}

    ```sql
    watch tkctl get all
    ```

    Pod 恢复正常运行后，操作结束。

## 维护 TiKV 实例所在节点

TiKV 实例迁移较慢，并且会对集群造成一定的数据迁移负载，因此在维护 TiKV 实例所在节点前，需要根据维护需求选择操作策略：

- 假如是维护短期内可恢复的节点，则不需要迁移 TiKV 节点，在维护结束后原地恢复节点；
- 假如是维护短期内不可恢复的节点，则需要规划 TiKV 的迁移工作。

### 维护短期内可恢复的节点

针对短期维护，我们可以通过调整 PD 集群的 `max-store-down-time` 配置来增大集群所允许的 TiKV 实例下线时间，在此时间内维护完毕并恢复 Kubernetes 节点后，所有该节点上的 TiKV 实例会自动恢复。

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward svc/<CLUSTER_NAME>-pd 2379:2379
```

{{< copyable "shell-regular" >}}

```shell
pd-ctl -d config set max-store-down-time 10m
```

调整 `max-store-down-time` 到合理的值后，后续的操作方式与[维护 PD 和 TiDB 实例所在节点](#维护-pd-和-tidb-实例所在节点)相同。

### 维护短期内不可恢复的节点

针对短期内不可恢复的节点维护，如节点长期下线等情形，需要使用 `pd-ctl` 主动通知 TiDB 集群下线对应的 TiKV 实例，再手动解除 TiKV 实例与该节点的绑定。

1. 使用 `kubectl cordon` 命令防止新的 Pod 调度到待维护节点上：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl cordon <node-name>
    ```

2. 查看待维护节点上的 TiKV 实例：

    {{< copyable "shell-regular" >}}

    ```shell
    tkctl get -A tikv | grep <node-name>
    ```

3. 使用 `pd-ctl` 主动下线 TiKV 实例。

    > **注意：**
    >
    > 下线 TiKV 实例前，需要保证集群中剩余的 TiKV 实例数不少于 PD 配置中的 TiKV 数据副本数（配置项：`max-replicas`）。假如不符合该条件，需要先操作扩容 TiKV。

    查看 TiKV 实例的 `store-id`：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get tc <CLUSTER_NAME> -ojson | jq '.status.tikv.stores | .[] | select ( .podName == "<POD_NAME>" ) | .id'
    ```

    下线实例：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl port-forward svc/<CLUSTER_NAME>-pd 2379:2379
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    pd-ctl -d store delete <ID>
    ```

4. 等待 store 状态（`state_name`）转移为 `Tombstone`：

    {{< copyable "shell-regular" >}}

    ```shell
    watch pd-ctl -d store <ID>
    ```

5. 解除 TiKV 实例与节点本地盘的绑定。

    查询 Pod 使用的 `PesistentVolumeClaim`：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> pod <pod_name> -ojson | jq '.spec.volumes | .[] | select (.name == "tikv") | .persistentVolumeClaim.claimName'
    ```

    删除该 `PesistentVolumeClaim`：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete -n <namespace> pvc <pvc_name>
    ```

6. 删除 TiKV 实例：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl delete -n <namespace> pod <pod_name>
    ```

7. 观察该 TiKV 实例是否正常调度到其它节点上：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n <namespace> get pod -o wide
    ```

    假如待维护节点上还有其它 TiKV 实例，则重复同样的操作步骤直到所有的 TiKV 实例都迁移到其它节点上。

8. 确认节点不再有 TiKV 实例后，再逐出节点上的其它实例：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl drain <node-name> --ignore-daemonsets --delete-local-data
    ```

9. 再次确认节点不再有任何 TiKV、TiDB 和 PD 实例运行：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pod --all-namespaces | grep <node-name>
    ```

10. 最后（可选），假如是长期下线节点，建议将节点从 Kubernetes 集群中删除：

    {{< copyable "shell-regular" >}}

    ```shell
    kuebctl delete node <node-name>
    ```

至此，操作完成。
