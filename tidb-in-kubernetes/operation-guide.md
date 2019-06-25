---
title: Kubernetes 上的 TiDB 集群运维
summary: TiDB 集群运维文档
category: how-to
---

# Kubernetes 上的 TiDB 集群运维

TiDB Operator 可以在同一个 Kubernetes 集群上管理多个 TiDB 集群。

以下变量会在后续文档中用到：

```
releaseName="demo"
namespace="tidb"
chartVersion="v1.0.0-beta.3"
```

Helm 安装完成后，通过下面命令获取要安装的 tidb-cluster chart 的 `values.yaml` 配置文件：

{{< copyable "shell-regular" >}}

```shell
mkdir -p /home/tidb/${releaseName} && \
helm inspect values pingcap/tidb-cluster --version=${chartVersion} > /home/tidb/${releaseName}/values-${releaseName}.yaml
```

> **注意：**
>
> `/home/tidb` 可以替换为你想用的目录，下文会用 `values.yaml` 指代 `/home/tidb/${releaseName}/values-${releaseName}.yaml`。

## 配置

TiDB Operator 把 `values.yaml` 作为 TiDB 集群的配置文件。`values.yaml` 提供了默认基本配置，你可以直接用它来快速部署，但是如果你有特殊配置需求或者要部署生产环境，你可以手动修改 `values.yaml` 中的变量。

* 资源配置

    * CPU & Memory

        默认部署并没有为任何 Pod 设置 CPU 或者 Memory 的 request 或者 limit，这样 TiDB 集群可以运行在小的 Kubernetes 集群，例如 DinD 或者默认的 GKE 集群，以方便测试。但是对于生产环境，最好根据[推荐配置](/how-to/deploy/hardware-recommendations.md)调整 CPU、Memory 和存储资源。

        资源 limit 应该大于等于资源 request，建议设置 limit 等于 request，这样可以获得 [`Guaranteed` QoS]( https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/#create-a-pod-that-gets-assigned-a-qos-class-of-guaranteed)。

    * 存储

        `values.yaml` 中的变量 `pd.storageClassName` 和 `tikv.storageClassName` 用于配置 PD 和 TiKV 的 `StorageClass`，默认配置为最小需求的 `local-storage`。
        
        如果你不想使用默认的 `StorageClass` 或者你的 Kubernetes 集群不支持 `local-storage`，可以通过下面命令找到可用的 `StorageClass` 并选择来配置 TiDB 集群。

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl get sc
        ```

* 容灾配置

    TiDB 是一个分布式数据库。容灾意味着任何一个物理节点宕机，不仅要保证 TiDB 服务可用，还要保证数据的完整性和可用性。

    要在 Kubernetes 集群上保证 TiDB 集群的容灾，可通过服务和数据的调度解决这个问题。

    * TiDB 实例容灾

        TiDB Operator 通过扩展调度器保证 PD、TiKV 和 TiDB 主机级别的容灾。TiDB 集群设置这个扩展调度器作为默认调度器，具体配置为 `values.yaml` 中的 `schedulerName` 变量。

        另一方面，通过 `affinity` 中的 `PodAntiAffinity` 配置保证其他拓扑级别（例如，机架、可用区、区域）的容灾。详细配置可参看 [pod affnity & anti affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#inter-pod-affinity-and-anti-affinity-beta-feature)。另外，`values.yaml` 中 `pd.affinity` 字段以注释形式提供了一个典型的容灾配置示例。

    * 数据容灾

        数据容灾是由 TiDB 集群自己保证的。TiDB Operator 只需要通过 TiKV Pod 所在的节点的特定标签获取拓扑信息，然后 PD 会根据拓扑信息自动调度数据副本。由于目前 TiDB Operator 只能识别特定标签，因此你只能通过下面标签设置拓扑信息：

        * `region`：节点所在区域
        * `zone`：节点所在可用区
        * `rack`：节点所在机架
        * `kubernetes.io/hostname`：节点 hostname

        你需要通过下面命令给节点打上拓扑信息标签（不一定要打上所有标签）：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl label node <nodeName> region=<regionName> zone=<zoneName> rack=<rackName> kubernetes.io/hostname=<hostName>
        ```

对于其他设置，`values.yaml` 文件中的变量都带有自解释的注释，你可以在安装之前按需修改。

## GKE

在 GKE 上，本地 SSD 卷默认大小限制为 375 GB，性能比永久性磁盘要差。

为提高性能，你必须保证以下两点：

* 安装 Linux Guest Environment，只能用于 Ubuntu 系统，不能用于 COS。
* 确保 SSD 挂载选项中包含 `nobarrier`。

我们提供一个解决上述问题的 [Daemonset](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/gke/local-ssd-optimize.yaml)。还提供一个解决上述性能问题并且将多块 SSD 盘配置成一个 LVM 的
[Daemonset](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/gke/local-ssd-provision/local-ssd-provision.yaml)。通过 Terraform 部署的时候会自动安装。

> **注意：**
>
> 整合多块本地 SSD 盘的部署方式假设一个虚拟机上只有一个进程需要使用本地 SSD。

## 部署 TiDB 集群

TiDB Operator 和 Helm 部署完成并配置完成，可以通过下面命令部署 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=${releaseName} --namespace=${namespace} --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

通过下面命令可以查看 Pod 状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n ${namespace} -l app.kubernetes.io/instance=${releaseName}
```

## 访问 TiDB 集群

默认情况下，TiDB 服务通过 [`NodePort`](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport) 暴露。可以通过修改为 `ClusterIP` 禁止集群外访问或者如果 Kubernetes 集群支持，可以修改为 [`LoadBalancer`](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) 对外暴露服务。

{{< copyable "shell-regular" >}}

``` shell
kubectl get svc -n ${namespace}
```

TiDB 集群默认没有设置 root 密码。在 Helm 中设置密码不安全，你可以在 `values.yaml` 中给 `tidb.passwordSecretName` 设置一个 K8s secret。注意，这仅用于初始化用户：一旦 TiDB 集群初始化完成，你可以删除这个 secret。secret 的格式为 `user=password`，你可以通过下面命令设置 root 用户密码：

{{< copyable "shell-regular" >}}

``` shell
kubectl create namespace ${namespace} && \
kubectl create secret generic tidb-secret --from-literal=root=<root-password> --namespace=${namespace}
```

你可以通过这个 `Secret` 获取密码：

{{< copyable "shell-regular" >}}

``` shell
PASSWORD=$(kubectl get secret -n ${namespace} tidb-secret -ojsonpath="{.data.root}" | base64 --decode) && \
echo ${PASSWORD}
```

* 在 Kubernetes 集群内访问 TiDB

    如果你的应用部署在同一个 Kubernetes 集群，你可以通过域名 `demo-tidb.tidb.svc` 和端口  `4000` 访问 TiDB。`demo` 是 `releaseName`，后面的 `tidb` 是通过 `helm install` 部署 TiDB 集群时指定的 namespace。

* 在 Kubernetes 集群外访问 TiDB

    * 使用 kubectl portforward

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl port-forward -n ${namespace} svc/${releaseName}-tidb 4000:4000 &>/tmp/portforward-tidb.log
        ```

        {{< copyable "shell-regular" >}}

        ``` shell
        mysql -h 127.0.0.1 -P 4000 -u root -p
        ```

    * 使用 LoadBalancer

        如果设置 `tidb.service.type` 为 `LoadBalancer` 并且 Kubernetes 集群支持 LoadBalancer，那么会为 TiDB 服务创建一个 LoadBalancer。你可以通过 LoadBalancer IP 和端口 `4000` 访问 TiDB。有些云平台支持内部负载均衡器，例如，在 GKE 上你可以在 `tidb.service.annotations` 中添加 `cloud.google.com/load-balancer-type: Internal` 为 TiDB 创建内部负载均衡器。

    * 使用 NodePort

        你可以通过节点 IP 和 TiDB 服务的 NodePort 访问 TiDB。NodePort 是 `4000` 后面的端口，一般大于 `30000`。

## TiDB 集群伸缩

TiDB Operator 支持垂直和水平伸缩。存储的垂直伸缩需要注意以下各项：

* 使用 Kubernetes v1.11 或者更高版本，请参考[官方博客](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/)。
* 后端 StorageClass 支持调整大小（目前只有少数几个网络 StorageClass 支持调整大小）。
* 当使用本地持久化存储卷，即使 CPU 和 Memory 的垂直伸缩也可能有问题，因为节点上可能资源不够。因此，当负载增加时，建议做水平伸缩而不是垂直伸缩。

### 水平伸缩

要扩缩容 TiDB 集群，只要修改 `values.yaml` 中 PD、TiKV 和 TiDB 的 `replicas`，然后执行下面命令：

{{< copyable "shell-regular" >}}

```shell
helm upgrade ${releaseName} pingcap/tidb-cluster --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

### 垂直伸缩

要垂直伸缩 TiDB 集群，修改 `values.yaml` 文件中 PD、TiKV 和 TiDB 的 CPU、Memory 或者存储的 request 和 limit，然后执行上述命令。

> **注意：**
>
> 请阅读上面垂直伸缩的注意事项。在 issue [#35](https://github.com/pingcap/tidb-operator/issues/35) 解决之前，你必须在 `values.yaml` 中手动为 TiKV 配置 `BlockCacheSize`。

## 升级 TiDB 集群

升级 TiDB 集群和伸缩 TiDB 集群类似，在 `values.yaml` 中修改 PD、TiKV 和 TiDB 的 `image`，然后执行如下命令：

{{< copyable "shell-regular" >}}

```shell
helm upgrade ${releaseName} pingcap/tidb-cluster --version=${chartVersion} -f /home/tidb/${releaseName}/values-${releaseName}.yaml
```

对于小版本升级，更新 `image` 就可以。但是对于大版本升级，最好是根据文档开始部分介绍的步骤，从新版本 chart 中获取新版本 `values.yaml`，和旧版本 `values.yaml` 合并成新的 `values.yaml`，然后执行上述升级命令。

## 修改 TiDB 集群配置

从 `v1.0.0` 版本开始，TiDB Operator 支持配置更新后滚动升级集群。为了后向兼容，这个特性默认关闭，你可以在 `values.yaml` 中设置 `enableConfigMapRollout` 为 `true` 启用它。

> **注意：**
>
> 如果集群已经在运行，即使没有配置修改，打开这个参数并运行 `helm upgrade` 也会触发 PD、TiKV 和 TiDB 滚动升级。
>
> 目前，集群创建后修改 PD 的 `schedule` 和 `replication` 配置（`values.yaml` 中的`maxStoreDownTime` 和 `maxReplicas` 参数，PD 配置文件中所有 `[schedule]` 和 `[replication]` 部分的配置 ）然后运行 `helm upgrade` 无法生效。集群创建后，你必须通过 `pd-ctl` 配置这些参数，请参考：[pd-ctl](/reference/tools/pd-control/)。

## 销毁 TiDB 集群

要销毁 TiDB 集群，执行以下命令：

{{< copyable "shell-regular" >}}

```shell
helm delete ${releaseName} --purge
```

上述命令只是删除运行的 Pod，数据仍然会保留。如果你不再需要那些数据，可以通过下面命令清除数据：

{{< copyable "shell-regular" >}}

```shell
kubectl delete pvc -n ${namespace} -l app.kubernetes.io/instance=${releaseName},app.kubernetes.io/managed-by=tidb-operator && \
kubectl get pv -l app.kubernetes.io/namespace=${namespace},app.kubernetes.io/managed-by=tidb-operator,app.kubernetes.io/instance=${releaseName} -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

> **警告：** 
>
> 上述命令会彻底删除数据，务必考虑清楚再执行。

## 监控

TiDB 通过 Prometheus 和 Grafana 监控 TiDB 集群。TiDB 集群创建时，会同时创建、配置 Prometheus 和 Grafana pod 收集并展示监控指标。

监控数据默认没有持久化，如果由于某些原因监控容器重启，数据会丢失。可以在 `values.yaml` 中设置 `monitor.persistent` 为 `true` 来持久化监控数据。

可以通过 `kubectl portforward` 查看监控面板：

{{< copyable "shell-regular" >}}

```shell
kubectl port-forward -n ${namespace} svc/${releaseName}-grafana 3000:3000 &>/tmp/portforward-grafana.log
```

然后在浏览器中打开 http://localhost:3000，默认用户名和密码都为 `admin`。

Grafana 服务默认通过 `NodePort` 暴露，如果 Kubernetes 集群支持负载均衡器，你可以修改为 `LoadBalancer`，然后通过负载均衡器访问面板。

### 查看 TiDB 慢查询日志

默认情况下，TiDB 会打印慢查询日志到标准输出，和正常日志混在一起。你可以通过 `grep` 关键词 `SLOW_QUERY` 查看慢查询日志：

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n ${namespace} ${tidbPodName} | grep SLOW_QUERY
```

或者，你也可以配置 `separateSlowLog` 输出慢查询日志到一个sidecar 容器：

```yaml
# Uncomment the following line to enable separate output of the slow query log
    # separateSlowLog: true
```

运行 `helm upgrade` 使配置生效，然后你可以通过名为 `slowlog` 的 sidecar 容器查看慢查询日志：

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n ${namespace} ${tidbPodName} -c slowlog
```

如果要从多个 Pod 获取日志，推荐 [`stern`](https://github.com/wercker/stern)。

{{< copyable "shell-regular" >}}

```shell
stern -n ${namespace} tidb -c slowlog
```

## 备份和恢复

TiDB Operator 为 TiDB 集群提供高度自动化的备份和恢复操作。你可以方便地为 TiDB 集群执行全量备份或者增量备份，也可以在集群宕机的情况下恢复 TiDB 集群。要了解备份和恢复的具体操作，请参考[备份和恢复 TiDB 集群]。
