---
title: 滚动升级 Kubernetes 上的 TiDB 集群
category: how-to
---

# 滚动升级 Kubernetes 上的 TiDB 集群

滚动更新 TiDB 集群时，会按 PD、TiKV、TiDB 的顺序，串行删除 Pod，并创建新版本的 Pod，当新版本的 Pod 正常运行后，再处理下一个 Pod。

滚动升级过程会自动处理 PD、TiKV 的 Leader 迁移与 TiDB 的 DDL Owner 迁移。因此，在多节点的部署拓扑下（最小环境：PD \* 3、TiKV \* 3、TiDB \* 2），滚动更新 TiKV、PD 不会影响业务正常运行。

对于有连接重试功能的客户端，滚动更新 TiDB 同样不会影响业务。对于无法进行重试的客户端，滚动更新 TiDB 则会导致连接到被关闭节点的数据库连接失效，造成部分业务请求失败。对于这类业务，推荐在客户端添加重试功能或在低峰期进行 TiDB 的滚动升级操作。

滚动更新可以用于升级 TiDB 版本，也可以用于更新集群配置。

## 升级 TiDB 版本

1. 修改集群的 `values.yaml` 文件中的 `tidb.image`、`tikv.image`、`pd.image` 的值为新版本镜像；
2. 执行 `helm upgrade` 命令进行升级：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release-name> pingcap/tidb-cluster -f values.yaml --version=<chart-version>
    ```

3. 查看升级进度：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n <namespace> get pod -o wide
    ```

    当所有 Pod 都重建完毕进入 `Running` 状态后，升级完成。

## 更新 TiDB 集群配置

默认条件下，修改配置文件不会自动应用到 TiDB 集群中，只有在实例重启时，才会重新加载新的配置文件。

您可以开启配置文件自动更新特性，在每次配置文件更新时，自动执行滚动更新，将修改后的配置应用到集群中。操作步骤如下：

1. 修改集群的 `values.yaml` 文件，将 `enableConfigMapRollout` 的值设为 `true`；
2. 根据需求修改 `values.yaml` 中需要调整的集群配置项；
3. 执行 `helm upgrade` 命令进行升级：

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release-name> pingcap/tidb-cluster -f values.yaml --version=<chart-version>
    ```

4. 查看升级进度：

    {{< copyable "shell-regular" >}}

    ```shell
    watch kubectl -n <namespace> get pod -o wide
    ```

    当所有 Pod 都重建完毕进入 `Running` 状态后，升级完成。

> **注意：**
>
> - 将 `enableConfigMapRollout` 特性从关闭状态打开时，即使没有配置变更，也会触发一次 PD、TiKV、TiDB 的滚动更新。
> - 目前 PD 的 `scheduler` 和 `replication` 配置（`values.yaml` 中的 `maxStoreDownTime` 和 `maxReplicas` 字段）在集群安装完成后无法自动更新，需要通过 [pd-ctl](/dev/reference/tools/pd-control.md) 手动更新。

## 强制升级 TiDB 集群

如果 PD 集群因为 PD 配置错误，PD 镜像 tag 错误，NodeAffinity 等原因不可用，[TiDB 集群伸缩](/dev/tidb-in-kubernetes/scale-in-kubernetes.md)，[升级 TiDB 版本](#升级-tidb-版本)和[更新 TiDB 集群配置](#更新-tidb-集群配置)都无法操作。这种情况下，可使用 `force-upgrade`（TiDB Operator 版本 > v1.0.0-beta.3 ）强制升级集群以恢复集群功能。具体操作步骤如下：

{{< copyable "shell-regular" >}}

```shell
kubectl annotate --overwrite tc <release-name> -n <namespace> tidb.pingcap.com/force-upgrade=true
```

然后执行对应操作中的 `helm upgrade` 命令。

> **注意：**
>
> PD 集群恢复后，**必须**执行下面命令禁用强制升级功能，否则下次升级过程可能会出现异常：
>
> {{< copyable "shell-regular" >}}
>
> ```shell
> kubectl annotate tc <release-name> -n <namespace> tidb.pingcap.com/force-upgrade-
> ```
