---
title: Kubernetes 上的 TiDB 集群故障诊断
category: how-to
aliases: ['/docs-cn/v3.0/how-to/troubleshoot/tidb-in-kubernetes/']
---

# Kubernetes 上的 TiDB 集群故障诊断

本文介绍了 Kubernetes 上 TiDB 集群的一些常见故障以及诊断解决方案。

## 诊断模式

当 Pod 处于 `CrashLoopBackoff` 状态时，Pod 内会容器不断退出，导致无法正常使用 `kubectl exec` 或 `tkctl debug`，给诊断带来不便。为了解决这个问题，TiDB in Kubernetes 提供了 PD/TiKV/TiDB Pod 诊断模式。在诊断模式下，Pod 内的容器启动后会直接挂起，不会再进入重复 Crash 的状态，此时，便可以通过 `kubectl exec` 或 `tkctl debug` 连接 Pod 内的容器进行诊断。

操作方式：

首先，为待诊断的 Pod 添加 Annotation：

{{< copyable "shell-regular" >}}

```shell
kubectl annotate pod <pod-name> -n <namespace> runmode=debug
```

在 Pod 内的容器下次重启时，会检测到该 Annotation，进入诊断模式。等待 Pod 进入 Running 状态即可开始诊断：

{{< copyable "shell-regular" >}}

```shell
watch kubectl get pod <pod-name> -n <namespace>
```

下面是使用 `kubectl exec` 进入容器进行诊断工作的例子：

{{< copyable "shell-regular" >}}

```shell
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh
```

诊断完毕，修复问题后，删除 Pod：

```shell
kubectl delete pod <pod-name> -n <namespace>
```

Pod 重建后会自动回到正常运行模式。

## 集群意外删除后恢复

TiDB Operator 使用 PV (Persistent Volume)、PVC (Persistent Volume Claim) 来存储持久化的数据，如果不小心使用 `helm delete` 意外删除了集群，PV/PVC 对象以及数据都会保留下来，以最大程度保证数据安全。

此时集群恢复的办法就是使用 `helm install` 命令来创建一个同名的集群，之前保留下来未被删除的 PV/PVC 以及数据会被复用：

{{< copyable "shell-regular" >}}

```shell
helm install pingcap/tidb-cluster -n <release-name> --namespace=<namespace> --version=<chart-version> -f values.yaml
```

## Pod 未正常创建

通过 `helm install` 创建集群后，如果 Pod 没有创建，则可以通过以下方式进行诊断：

{{< copyable "shell-regular" >}}

```shell
kubectl get tidbclusters -n <namespace>
kubectl get statefulsets -n <namespace>
kubectl describe statefulsets -n <namespace> <release-name>-pd
```

## Pod 之间网络不通

针对 TiDB 集群而言，绝大部分 Pod 间的访问均通过 Pod 的域名（使用 Headless Service 分配）进行，例外的情况是 TiDB Operator 在收集集群信息或下发控制指令时，会通过 PD Service 的 `service-name` 访问 PD 集群。

当通过日志或监控确认 Pod 间存在网络连通性问题，或根据故障情况推断出 Pod 间网络连接可能不正常时，可以按照下面的流程进行诊断，逐步缩小问题范围：

1. 确认 Service 和 Headless Service 的 Endpoints 是否正常：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl -n <namespace> get endpoints <release-name>-pd
    kubectl -n <namespace> get endpoints <release-name>-tidb
    kubectl -n <namespace> get endpoints <release-name>-pd-peer
    kubectl -n <namespace> get endpoints <release-name>-tikv-peer
    kubectl -n <namespace> get endpoints <release-name>-tidb-peer
    ```

    以上命令展示的 `ENDPOINTS` 字段中，应当是由逗号分隔的 `cluster_ip:port` 列表。假如字段为空或不正确，请检查 Pod 的健康状态以及 `kube-controller-manager` 是否正常工作。

2. 进入 Pod 的 Network Namespace 诊断网络问题：

    {{< copyable "shell-regular" >}}

    ```
    tkctl debug -n <namespace> <pod-name>
    ```

    远端 shell 启动后，使用 `dig` 命令诊断 DNS 解析，假如 DNS 解析异常，请参照[诊断 Kubernetes DNS 解析](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)进行故障排除：

    {{< copyable "shell-regular" >}}

    ```shell
    dig <HOSTNAME>
    ```

    使用 `ping` 命令诊断到目的 IP 的三层网络是否连通（目的 IP 为使用 `dig` 解析出的 ClusterIP）:

    {{< copyable "shell-regular" >}}

    ```shell
    ping <TARGET_IP>
    ```

    假如 ping 检查失败，请参照[诊断 Kubernetes 网络](https://www.praqma.com/stories/debugging-kubernetes-networking/)进行故障排除。

    假如 ping 检查正常，继续使用 `telnet` 检查目标端口是否打开：

    {{< copyable "shell-regular" >}}

    ```shell
    telnet <TARGET_IP> <TARGET_PORT>
    ```

    假如 `telnet` 检查失败，则需要验证 Pod 的对应端口是否正确暴露以及应用的端口是否配置正确：

    {{< copyable "shell-regular" >}}

    ```shell
    # 检查端口是否一致
    kubectl -n <namespace> get po <pod-name> -ojson | jq '.spec.containers[].ports[].containerPort'

    # 检查应用是否被正确配置服务于指定端口上
    # PD, 未配置时默认为 2379 端口
    kubectl -n <namespace> -it exec <pod-name> -- cat /etc/pd/pd.toml | grep client-urls
    # TiKV, 未配置时默认为 20160 端口
    kubectl -n <namespace> -it exec <pod-name> -- cat /etc/tikv/tikv.toml | grep addr
    # TiDB, 未配置时默认为 4000 端口
    kubectl -n <namespace> -it exec <pod-name> -- cat /etc/tidb/tidb.toml | grep port
    ```

## Pod 处于 Pending 状态

Pod 处于 Pending 状态，通常都是资源不满足导致的，比如：

* 使用持久化存储的 PD、TiKV、Monitor Pod 使用的 PVC 的 StorageClass 不存在或 PV 不足
* Kubernetes 集群中没有节点能满足 Pod 申请的 CPU 或内存

此时，可以通过 `kubectl describe pod` 命令查看 Pending 的具体原因：

{{< copyable "shell-regular" >}}

```
kubectl describe po -n <namespace> <pod-name>
```

如果是 CPU 或内存资源不足，可以通过降低对应组件的 CPU 或内存资源申请使其能够得到调度，或是增加新的 Kubernetes 节点。

如果是 PVC 的 StorageClass 找不到，则需要将 TiDB Pod 删除，并且将对应的 PVC 也都删除，然后在 `values.yaml` 里面将 `storageClassName` 修改为集群中可用的 StorageClass 名字，可以通过以下命令获取集群中可用的 StorageClass：

{{< copyable "shell-regular" >}}

```
kubectl get storageclass
```

如果集群中有 StorageClass，但可用的 PV 不足，则需要添加对应的 PV 资源。对于 Local PV，可以参考[本地 PV 配置](/tidb-in-kubernetes/reference/configuration/local-pv.md)进行扩充。

## Pod 处于 CrashLoopBackOff 状态

Pod 处于 CrashLoopBackOff 状态意味着 Pod 内的容器重复地异常退出（异常退出后，容器被 Kubelet 重启，重启后又异常退出，如此往复）。可能导致 CrashLoopBackOff 的原因有很多，此时，最有效的定位办法是查看 Pod 内容器的日志：

{{< copyable "shell-regular" >}}

```shell
kubectl -n <namespace> logs -f <pod-name>
```

假如本次日志没有能够帮助诊断的有效信息，可以添加 `-p` 参数输出容器上次启动时的日志信息：

{{< copyable "shell-regular" >}}

```shell
kubectl -n <namespace> logs -p <pod-name>
```

确认日志中的错误信息后，可以根据 [tidb-server 启动报错](/how-to/troubleshoot/cluster-setup.md#tidb-server-启动报错)，[tikv-server 启动报错](/how-to/troubleshoot/cluster-setup.md#tikv-server-启动报错)，[pd-server 启动报错](/how-to/troubleshoot/cluster-setup.md#pd-server-启动报错)中的指引信息进行进一步排查解决。

另外，TiKV 在 ulimit 不足时也会发生启动失败的状况，对于这种情况，可以修改 Kubernetes 节点的 `/etc/security/limits.conf` 调大 ulimit：

```
root        soft        nofile        1000000
root        hard        nofile        1000000
root        soft        core          unlimited
root        soft        stack         10240
```

假如通过日志无法确认失败原因，ulimit 也设置正常，那么可以通过[诊断模式](#诊断模式)进行进一步排查。

## 无法访问 TiDB 服务

TiDB 服务访问不了时，首先确认 TiDB 服务是否部署成功，确认方法如下：

查看该集群的所有组件是否全部都启动了，状态是否为 Running。

{{< copyable "shell-regular" >}}

```shell
kubectl get po -n <namespace>
```

检查 TiDB 组件的日志，看日志是否有报错。

{{< copyable "shell-regular" >}}

```shell
kubectl logs -f <tidb-pod-name> -n <namespace> -c tidb
```

如果确定集群部署成功，则进行网络检查：

1. 如果你是通过 `NodePort` 方式访问不了 TiDB 服务，请在 node 上尝试使用 service domain 或 clusterIP 访问 TiDB 服务，假如 serviceName 或 clusterIP 的方式能访问，基本判断 Kubernetes 集群内的网络是正常的，问题可能出在下面两个方面：

    * 客户端到 node 节点的网络不通。
    * 查看 TiDB service 的 `externalTrafficPolicy` 属性是否为 Local。如果是 Local 则客户端必须通过 TiDB Pod 所在 node 的 IP 来访问。

2. 如果 service domain 或 clusterIP 方式也访问不了 TiDB 服务，尝试用 TiDB服务后端的 `<PodIP>:4000` 连接看是否可以访问，如果通过 PodIP 可以访问 TiDB 服务，可以确认问题出在 service domain 或 clusterIP 到 PodIP 之间的连接上，排查项如下：

    * 检查 DNS 服务是否正常：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get po -n kube-system -l k8s-app=kube-dns
        dig <tidb-service-domain>
        ```

    * 检查各个 node 上的 kube-proxy 是否正常运行：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl get po -n kube-system -l k8s-app=kube-proxy
        ```

    * 检查 node 上的 iptables 规则中 TiDB 服务的规则是否正确

        {{< copyable "shell-regular" >}}

        ```shell
        iptables-save -t nat |grep <clusterIP>
        ```

    * 检查对应的 endpoint 是否正确

3. 如果通过 PodIP 访问不了 TiDB 服务，问题出在 Pod 层面的网络上，排查项如下：

    * 检查 node 上的相关 route 规则是否正确
    * 检查网络插件服务是否正常
    * 参考上面的 [Pod 之间网络不通](#pod-之间网络不通)章节

## TiKV Store 异常进入 Tombstone 状态

正常情况下，当 TiKV Pod 处于健康状态时（Pod 状态为 `Running`），对应的 TiKV Store 状态也是健康的（Store 状态为 `UP`）。但并发进行 TiKV 组件的扩容和缩容可能会导致部分 TiKV Store 异常并进入 Tombstone 状态。此时，可以按照以下步骤进行修复：

1. 查看 TiKV Store 状态：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> tidbcluster <release-name> -ojson | jq '.status.tikv.stores'
    ```

2. 查看 TiKV Pod 运行状态：

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get -n <namespace> po -l app.kubernetes.io/component=tikv
    ```

3. 对比 Store 状态与 Pod 运行状态。假如某个 TiKV Pod 所对应的 Store 处于 `Offline` 状态，则表明该 Pod 的 Store 正在异常下线中。此时，可以通过下面的命令取消下线进程，进行恢复：

    1. 打开到 PD 服务的连接：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl port-forward -n <namespace> svc/<cluster-name>-pd <local-port>:2379 &>/tmp/portforward-pd.log &
        ```

    2. 上线对应 Store：

        {{< copyable "shell-regular" >}}

        ```shell
        curl -X POST http://127.0.0.1:2379/pd/api/v1/store/<store-id>/state?state=Up
        ```

4. 假如某个 TiKV Pod 所对应的 `lastHeartbeatTime` 最新的 Store 处于 `Tombstone` 状态 ，则表明异常下线已经完成。此时，需要重建 Pod 并绑定新的 PV 进行恢复：

    1. 将该 Store 对应 PV 的 `reclaimPolicy` 调整为 `Delete`：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl patch $(kubectl get pv -l app.kubernetes.io/instance=<release-name>,tidb.pingcap.com/store-id=<store-id> -o name) -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}
        ```

    2. 删除 Pod 使用的 PVC：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl delete -n <namespace> pvc tikv-<pod-name> --wait=false
        ```

    3. 删除 Pod，等待 Pod 重建：

        {{< copyable "shell-regular" >}}

        ```shell
        kubectl delete -n <namespace> pod <pod-name>
        ```

    Pod 重建后，会以在集群中注册一个新的 Store，恢复完成。
