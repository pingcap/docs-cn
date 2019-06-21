---
title: 服务暴露
category: how-to
---

# 服务暴露

在 Kubernetes 集群内访问 TiDB 时，使用 TiDB service 域名 `<tidbcluster-name>-tidb.<namespace>` 即可。若需要在集群外访问，则需将 TiDB 服务端口暴露出去。在 tidb-cluster helm chart 中，通过 values 文件中的 `tidb.service` 字段进行配置：

{{< copyable "" >}}

```yaml
tidb:
  service:
    type: NodePort
    # externalTrafficPolicy: Cluster
    # annotations:
    # cloud.google.com/load-balancer-type: Internal
```

## NodePort

在没有 LoadBalancer 时，可选择通过 NodePort 暴露。NodePort 有两种模式：

- `externalTrafficPolicy=Cluster`：集群所有的机器都会给 TiDB 分配 TCP
- `externalTrafficPolicy=Local`：只有运行 TiDB 的机器会分配 TCP 端口，用于访问本地的 TiDB 实例

    使用 Local 模式时，建议打开 tidb-scheduler 的 `StableScheduling` 特性。tidb-scheduler 会尽可能在升级过程中将新 TiDB 实例调度到原机器，这样集群外的客户端便不需要在 TiDB 重启后更新配置。

### 查看 NodePort 模式下对外暴露的 IP/PORT

查看 Service 分配的 Node Port，可通过获取 TiDB 的 Service 对象来获知：

{{< copyable "shell-regular" >}}

```shell
namespace=<your-tidb-namesapce>
```

{{< copyable "shell-regular" >}}

```shell
release=<your-tidb-release-name>
```

{{< copyable "shell-regular" >}}

```shell
kubectl -n ${namespace} get svc ${release}-tidb -ojsonpath="{.spec.ports[?(@.name=='mysql-client')].nodePort}{'\n'}"
```

查看可通过哪些节点的 IP 访问 TiDB 服务，有两种情况：

- `externalTrafficPolicy` 为 `Cluster` 时，所有节点 IP 均可
- `externalTrafficPolicy` 为 `Local` 时，可通过以下命令获取指定集群的 TiDB 实例所在的节点

    {{< copyable "shell-regular" >}}

    ```shell
    release=<your-tidb-release-name>
    ```
    
    {{< copyable "shell-regular" >}}

    ```shell
    kubectl -n stability-cluster1 get pods -l "app.kubernetes.io/component=tidb,app.kubernetes.io/instance=${release}" -ojsonpath="{range .items[*]}{.spec.nodeName}{'\n'}{end}"
    ```

## LoadBalancer

若运行在有 LoadBalancer 的环境，比如 GCP/AWS 平台，建议使用云平台的 LoadBalancer 特性。

访问 [Kubernetes Service 文档](https://kubernetes.io/docs/concepts/services-networking/service/)，了解更多 Service 特性以及云平台 Load Balancer 支持。
