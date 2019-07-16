---
title: 管理 Kubernetes 上的 TiDB 集群
category: how-to
---

# 管理 Kubernetes 上的 TiDB 集群

TiDB Operator 可以在同一个 Kubernetes 集群上管理多个 TiDB 集群。

以下变量会在后续文档中用到：

```
releaseName="demo"
namespace="tidb"
chartVersion="v1.0.0-beta.3"
```

## GKE

在 GKE 上，本地 SSD 卷默认大小限制为 375 GB，性能比永久性磁盘要差。

为提高性能，必须保证以下两点：

* 安装 Linux Guest Environment，只能用于 Ubuntu 系统，不能用于 Container-Optimized OS。
* 确保 SSD 挂载选项中包含 `nobarrier`。

TiDB 提供的 [Daemonset](https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/gke/local-ssd-provision/local-ssd-provision.yaml) 能够：

+ 解决性能问题
+ 使用 UUID 重新安装本地 SSD 磁盘，以提高安全性
+ 在 Ubuntu 上使用 LVM 工具将所有本地 SSD 磁盘组合成一个大磁盘
+ 运行 local-volume-provisioner

terraform 部署将自动安装该 Daemonset。

> **注意：**
>
> 整合多块本地 SSD 盘的部署方式。假设一个虚拟机上只有一个进程，则需要使用本地 SSD。

## 访问 TiDB 集群

默认情况下，TiDB 服务通过 [`NodePort`](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport) 暴露。可以通过修改为 `ClusterIP` 禁止集群外访问。如果 Kubernetes 集群支持，可以修改为 [`LoadBalancer`](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) 对外暴露服务。

{{< copyable "shell-regular" >}}

``` shell
kubectl get svc -n ${namespace}
```

TiDB 集群默认没有设置 root 密码。在 Helm 中设置密码不安全，因此可以在 `values.yaml` 中给 `tidb.passwordSecretName` 设置一个 K8s secret。注意，这仅用于初始化用户：一旦 TiDB 集群初始化完成，你可以删除这个 secret。secret 的格式为 `user=password`。你可以通过下面命令设置 root 用户密码：

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

TiDB Operator 支持垂直和水平伸缩。存储的垂直伸缩需要注意以下事项：

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
> 目前，集群创建后修改 PD 的 `schedule` 和 `replication` 配置（`values.yaml` 中的 `maxStoreDownTime` 和 `maxReplicas` 参数，PD 配置文件中所有 `[schedule]` 和 `[replication]` 部分的配置）然后运行 `helm upgrade` 无法生效。集群创建后，你必须通过 `pd-ctl` 配置这些参数，请参考 [pd-ctl](/reference/tools/pd-control.md)。

如果 PD 集群不可用，[TiDB 集群伸缩](#tidb-集群伸缩)、[升级 TiDB 集群](#升级-tidb-集群)和[修改 TiDB 集群配置](#修改-tidb-集群配置)都无法操作，从 TiDB Operator 版本 > v1.0.0-beta.3 开始，支持 `force-upgrade`，在 PD 集群不可用的情况下，允许用户通过下面步骤强制升级集群以恢复集群功能：

{{< copyable "shell-regular" >}}

```shell
kubectl annotate --overwrite tc ${releaseName} -n ${namespace} tidb.pingcap.com/force-upgrade=true
```

然后执行对应操作中的 `helm upgrade` 命令。

PD 集群恢复后，**必须**执行下面命令禁用强制升级功能，否则下次升级过程可能会出现异常：

{{< copyable "shell-regular" >}}

```shell
kubectl annotate tc ${releaseName} -n ${namespace} tidb.pingcap.com/force-upgrade-
```

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

配置与访问监控系统的细节请参阅[监控系统部署](/how-to/monitor/tidb-in-kubernetes.md)。

## 日志

查看与收集日志的方法请参阅[日志收集](/how-to/maintain/tidb-in-kubernetes/log-collecting.md)文档。

## 备份和恢复

TiDB Operator 为 TiDB 集群提供高度自动化的备份和恢复操作。你可以方便地为 TiDB 集群执行全量备份或者增量备份，也可以在集群宕机的情况下恢复 TiDB 集群。
