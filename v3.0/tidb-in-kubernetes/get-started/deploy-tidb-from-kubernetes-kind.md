---
title: 使用 kind 在 Kubernetes 上部署 TiDB 集群
summary: 使用 kind 在 Kubernetes 上部署 TiDB 集群。
category: how-to
---

# 使用 kind 在 Kubernetes 上部署 TiDB 集群

本文介绍了如何在个人电脑（Linux 或 MacOS）上采用 [kind](https://kind.sigs.k8s.io/) 方式在 Kubernetes 上部署 [TiDB Operator](https://github.com/pingcap/tidb-operator) 和 TiDB 集群。

kind 通过 Docker 容器模拟出一个本地的 Kubernetes 集群。kind 的设计初衷是为了在本地进行 Kubernetes 集群的一致性测试，这意味着你可以使用 kind 模拟出你想要的 Kubernetes 版本集群。你可以在 [Docker hub](https://hub.docker.com/r/kindest/node/tags) 中找到你想要部署的 Kubernetes 版本。

> **警告：**
>
> 对于生产环境，不要使用此方式进行部署。

## 环境准备

部署前，请确认软件、资源等满足如下需求：

- 资源需求：CPU 2 核+、内存 4G+

    > **注意：**
    >
    > 对于 macOS 系统，需要给 Docker 分配 2 核+ CPU 和 4G+ 内存。详情请参考 [Mac 上配置 Docker](https://docs.docker.com/docker-for-mac/#advanced)。

- [Docker](https://docs.docker.com/install/)：版本 >= 17.03
- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client)：版本 >= 2.9.0 并且 < 3.0.0
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)：版本 >= 1.10，建议 1.13 或更高版本

    > **注意：**
    >
    > 不同版本 `kubectl` 输出可能略有不同。

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)：版本 >= 0.4.0
- [net.ipv4.ip_forward](https://linuxconfig.org/how-to-turn-on-off-ip-forwarding-in-linux) 需要被设置为 1

## 第 1 步：通过 kind 部署 Kubernetes 集群

首先，请确认 Docker 进程正常运行。然后你可以通过脚本命令快速启动一个本地的 Kubernetes 集群。

1. Clone 官方提供的代码：

    {{< copyable "shell-regular" >}}

    ``` shell
    git clone --depth=1 https://github.com/pingcap/tidb-operator && \
    cd tidb-operator
    ```

2. 运行脚本，在本地创建一个 Kubernetes 集群：

    {{< copyable "shell-regular" >}}

    ``` shell
    hack/kind-cluster-build.sh
    ```

    > **注意：**
    >
    > 通过该脚本启动的 Kubernetes 集群默认有 6 个节点，Kubernetes 版本默认为 v1.12.8，每个节点默认挂载数为 9。你可以通过启动参数去修改这些参数：
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```shell
    > hack/kind-cluster-build.sh --nodeNum 2 --k8sVersion v1.14.6 --volumeNum 3
    > ```

3. 集群创建完毕后，执行下列命令将 kubectl 的默认配置文件切换到 `kube-config`，从而连接到该本地 Kubernetes 集群：

    {{< copyable "shell-regular" >}}

    ```shell
    export KUBECONFIG="$(kind get kubeconfig-path)"
    ```

4. 查看该 kubernetes 集群信息：

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl cluster-info
    ```

    输出如下类似信息：

    ``` shell
    Kubernetes master is running at https://127.0.0.1:50295
    KubeDNS is running at https://127.0.0.1:50295/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
    ```

5. 查看该 Kubernetes 集群的 `storageClass`：

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl get storageClass
    ```

    输出如下类似信息：

    ``` shell
    NAME                 PROVISIONER                    AGE
    local-storage        kubernetes.io/no-provisioner   7m50s
    standard (default)   kubernetes.io/host-path        8m29s
    ```

## 第 2 步：在 Kubernetes 集群上部署 TiDB Operator

参考[部署 TiDB Operator](/v3.0/tidb-in-kubernetes/deploy/tidb-operator.md#安装-tidb-operator)中的操作。

## 第 3 步：在 Kubernetes 集群中部署 TiDB 集群

参考[标准 Kubernetes 上的 TiDB 集群](/v3.0/tidb-in-kubernetes/deploy/general-kubernetes.md#部署-tidb-集群)中的操作。

## 访问数据库和监控面板

参考[查看监控面板](/v3.0/tidb-in-kubernetes/monitor/tidb-in-kubernetes.md#查看监控面板)中的操作。

## 删除 TiDB 集群 与 Kubernetes 集群

删除本地 TiDB 集群可参考[销毁 TiDB 集群](/v3.0/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md#销毁-kubernetes-上的-tidb-集群)。

通过下面命令删除该 Kubernetes 集群：

{{< copyable "shell-regular" >}}

``` shell
kind delete cluster
```
