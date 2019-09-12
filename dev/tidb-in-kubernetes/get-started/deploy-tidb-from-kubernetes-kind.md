---
title: 使用 kind 在 Kubernetes 上部署 TiDB 集群
summary: 使用 kind 在 Kubernetes 上部署 TiDB 集群
category: how-to
---

# 使用 kind 在 Kubernetes 上部署 TiDB 集群

本文介绍了如何在个人电脑 （Linux 或 MacOS) 上采用 [kind](https://kind.sigs.k8s.io/) 方式在 Kubernetes 上部署 [TiDB Operator](https://github.com/pingcap/tidb-operator) 和 TiDB 集群。

kind 通过 Docker 容器模拟出一个单点的 Kubernetes 集群。 kind 的设计初衷是为了在本地进行 Kubernetes 集群的一致性测试，这意味着你可以使用 kind 模拟出你想要的 Kubernetes 版本集群，你可以在 [Docker hub](https://hub.docker.com/r/kindest/node/tags) 中找到你想要部署的 Kubernetes 版本。

> **警告：**
>
> 对于生产环境，不要使用此方式进行部署。

## 环境准备

部署前，请确认软件、资源等满足如下需求：

- 资源需求 CPU 2+，Memory 4G+

    > **注意：**
    >
    > 对于 macOS 系统，需要给 Docker 分配 2+ CPU 和 4G+ Memory。详情请参考 [Mac 上配置 Docker](https://docs.docker.com/docker-for-mac/#advanced)。

- [Docker](https://docs.docker.com/install/)：>= 17.03
- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client): 版本 >= 2.9.0 并且 < 3.0.0
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl): 至少 1.10，建议 1.13 或更高版本

    > **注意：**
    >
    > 不同版本 `kubectl` 输出可能略有不同。

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/): 版本 >= 0.5.1

## 第 1 步: 通过 kind 部署 Kubernetes 集群

首先，请确认 Docker 进程正常运行。然后你可以通过 kind 命令快速启动一个本地的单点 Kubernetes 集群( kind 0.5.1 默认为 1.15.3 版本）。

创建集群,这里我们先手动指定为 1.14.3 版本:

> **注意：**
>
> 了解使用 kind 的更多细节，请参考 [kind 官方文档](https://kind.sigs.k8s.io/docs/user/quick-start/)

{{< copyable "shell-regular" >}}

```shell
kind create cluster --image kindest/node:v1.14.3
```

等待集群创建完毕以后，我们切换 kube-config 文件来连接到本地 Kubernetes 集群:

{{< copyable "shell-regular" >}}

```shell
export KUBECONFIG="$(kind get kubeconfig-path)"
kubectl cluster-info
```

## 第 2 步: 在 kind Kubernetes 集群上部署 TiDB Operator

> **注意：**
>
> `<chartVersion>` 在后续文档中代表 chart 版本，例如 `v1.0.0`。

如果 K8s 集群启动并正常运行，可以通过 `helm` 添加 chart 仓库并安装 TiDB Operator。

1. 添加 Helm chart 仓库：

    {{< copyable "shell-regular" >}}

    ``` shell
    helm repo add pingcap https://charts.pingcap.org/ && \
    helm repo list && \
    helm repo update && \
    helm search tidb-cluster -l && \
    helm search tidb-operator -l
    ```

2. 查看 kind Kubernetes 集群的 StorageClass

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl get storageClass
    ```

    输出类似如下内容：

    ```
    $ kubectl get storageClass
    NAME                 PROVISIONER               AGE
    standard (default)   kubernetes.io/host-path   20h
    ```

    > **注意：**
    >
    > `<storageClass>` 在后续文档中代表当前 Kubernetes 集群的 StorageClass Name，例如 `standard` 。

3. 安装 TiDB Operator:

    {{< copyable "shell-regular" >}}

    ``` shell
    helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --set scheduler.kubeSchedulerImageName=registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler --set defaultStorageClassName=<storageClass> --version=<chartVersion>
    ```

    然后等待几分钟确保 TiDB Operator 正常运行：

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=tidb-operator
    ```

    输出类似如下内容：

    ```
    NAME                                       READY     STATUS    RESTARTS   AGE
    tidb-controller-manager-5cd94748c7-jlvfs   1/1       Running   0          1m
    tidb-scheduler-56757c896c-clzdg            2/2       Running   0          1m
    ```

## 第 3 步: 在 kind Kubernetes 集群中部署 TiDB 集群

通过 `helm` 和 TiDB Operator，我们可以很轻松的部署一套 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=demo --namespace=tidb --set pd.storageClassName=<storageClass> --set tikv.storageClassName=<storageClass> --version=<chartVersion>
```

等待几分钟，确保 TiDB 所有组件正常创建并进入 `ready` 状态，可以通过下面命令持续观察：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pods --namespace tidb -l app.kubernetes.io/instance=demo -o wide --watch
```

当所有 Pod 状态为 `Running`，<kbd>Ctrl</kbd>+<kbd>C</kbd>  停止 watch。

通过下面步骤获取集群信息：

{{< copyable "shell-regular" >}}

``` shell
kubectl get tidbcluster -n tidb
```

输出类似如下信息：

```
NAME   PD                       STORAGE   READY   DESIRE   TIKV                       STORAGE   READY   DESIRE   TIDB                       READY   DESIRE
demo   pingcap/pd:v3.0.0-rc.1   1Gi       3       3        pingcap/tikv:v3.0.0-rc.1   10Gi      3       3        pingcap/tidb:v3.0.0-rc.1   2       2
```

{{< copyable "shell-regular" >}}

``` shell
kubectl get statefulset -n tidb
```

输出类似如下信息：

```
NAME        DESIRED   CURRENT   AGE
demo-pd     3         3         1m
demo-tidb   2         2         1m
demo-tikv   3         3         1m
```

{{< copyable "shell-regular" >}}

``` shell
kubectl get service -n tidb
```

输出类似如下信息：

```
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                          AGE
demo-discovery    ClusterIP   10.96.146.139    <none>        10261/TCP                        1m
demo-grafana      NodePort    10.111.80.73     <none>        3000:32503/TCP                   1m
demo-pd           ClusterIP   10.110.192.154   <none>        2379/TCP                         1m
demo-pd-peer      ClusterIP   None             <none>        2380/TCP                         1m
demo-prometheus   NodePort    10.104.97.84     <none>        9090:32448/TCP                   1m
demo-tidb         NodePort    10.102.165.13    <none>        4000:32714/TCP,10080:32680/TCP   1m
demo-tidb-peer    ClusterIP   None             <none>        10080/TCP                        1m
demo-tikv-peer    ClusterIP   None             <none>        20160/TCP                        1m
```

{{< copyable "shell-regular" >}}

``` shell
kubectl get configmap -n tidb
```

输出类似如下信息：

```
NAME                              DATA   AGE
demo-monitor                      5      1m
demo-monitor-dashboard-extra-v3   2      1m
demo-monitor-dashboard-v2         5      1m
demo-monitor-dashboard-v3         5      1m
demo-pd                           2      1m
demo-tidb                         2      1m
demo-tikv                         2      1m
```

{{< copyable "shell-regular" >}}

``` shell
kubectl get pod -n tidb
```

输出类似如下信息：

```
NAME                              READY     STATUS      RESTARTS   AGE
demo-discovery-649c7bcbdc-t5r2k   1/1       Running     0          1m
demo-monitor-58745cf54f-gb8kd     2/2       Running     0          1m
demo-pd-0                         1/1       Running     0          1m
demo-pd-1                         1/1       Running     0          1m
demo-pd-2                         1/1       Running     0          1m
demo-tidb-0                       1/1       Running     0          1m
demo-tidb-1                       1/1       Running     0          1m
demo-tikv-0                       1/1       Running     0          1m
demo-tikv-1                       1/1       Running     0          1m
demo-tikv-2                       1/1       Running     0          1m
```

## 访问数据库和监控面板

通过 `kubectl port-forward` 暴露服务到主机，可以访问 TiDB 集群。命令中的端口格式为：`<主机端口>:<k8s 服务端口>`。

- 通过 MySQL 客户端访问 TiDB

    在访问 TiDB 集群之前，请确保已安装 MySQL client。

    1. 使用 `kubectl` 暴露 TiDB 服务端口：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl port-forward svc/demo-tidb 4000:4000 --namespace=tidb
        ```

        > **注意：**
        >
        > 如果代理建立成功，会打印类似输出：`Forwarding from 0.0.0.0:4000 -> 4000`。测试完成后按 `Ctrl + C` 停止代理并退出。

    2. 然后，通过 MySQL 客户端访问 TiDB，打开一个新终端标签或者一个新终端窗口，执行下面命令：

        {{< copyable "shell-regular" >}}

        ``` shell
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

- 查看监控面板

    1. 使用 `kubectl` 暴露 Grafana 服务端口：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl port-forward svc/demo-grafana 3000:3000 --namespace=tidb
        ```

        > **注意：**
        >
        > 如果代理建立成功，会打印类似输出：`Forwarding from 0.0.0.0:3000 -> 3000`。测试完成后按 `Ctrl + C` 停止代理并退出。

    2. 然后，在浏览器中打开 `http://localhost:3000` 访问 Grafana 监控面板：

        * 默认用户名：admin
        * 默认密码：admin

## 删除 TiDB 或 kind Kubernetes 集群

通过下面命令删除 demo 集群：

{{< copyable "shell-regular" >}}

``` shell
helm delete --purge demo
```

通过下面命令删除 kind Kubernetes 集群:

{{< copyable "shell-regular" >}}

``` shell
kind delete cluster
```