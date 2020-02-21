---
title: 使用 kind 在 Kubernetes 上部署 TiDB 集群
summary: 使用 kind 在 Kubernetes 上部署 TiDB 集群。
category: how-to
aliases: ['/docs-cn/v3.0/tidb-in-kubernetes/get-started/deploy-tidb-from-kubernetes-dind/']
---

# 使用 kind 在 Kubernetes 上部署 TiDB 集群

本文介绍了如何在个人电脑（Linux 或 MacOS）上采用 [kind](https://kind.sigs.k8s.io/) 方式在 Kubernetes 上部署 [TiDB Operator](https://github.com/pingcap/tidb-operator) 和 TiDB 集群。

kind 通过使用 Docker 容器作为集群节点模拟出一个本地的 Kubernetes 集群。kind 的设计初衷是为了在本地进行 Kubernetes 集群的一致性测试。Kubernetes 集群版本取决于 kind 使用的镜像，你可以指定任一镜像版本用于集群节点，并在 [Docker hub](https://hub.docker.com/r/kindest/node/tags) 中找到想要部署的 Kubernetes 版本。

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
- [Helm Client](https://helm.sh/docs/intro/install/)：版本 >= 2.9.0 并且 < 3.0.0
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)：版本 >= 1.10，建议 1.13 或更高版本

    > **注意：**
    >
    > 不同 kubectl 版本，输出可能略有不同。

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/)：版本 >= 0.4.0
- [net.ipv4.ip_forward](https://linuxconfig.org/how-to-turn-on-off-ip-forwarding-in-linux) 需要被设置为 `1`

## 第 1 步：通过 kind 部署 Kubernetes 集群

首先确认 Docker 进程正常运行，然后你可以通过脚本命令快速启动一个本地的 Kubernetes 集群。

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

1. 安装 Helm 并配置 PingCAP 官方 chart 仓库，参考 [使用 Helm](/tidb-in-kubernetes/reference/tools/in-kubernetes.md#使用-helm) 小节中的操作。

2. 部署 TiDB Operator，参考 [安装 TiDB Operator](/tidb-in-kubernetes/deploy/tidb-operator.md#安装-tidb-operator) 小节中的操作。

## 第 3 步：在 Kubernetes 集群中部署 TiDB 集群

参考[在标准 Kubernetes 上部署 TiDB 集群](/tidb-in-kubernetes/deploy/general-kubernetes.md#部署-tidb-集群)中的操作。

## 访问数据库和监控面板

通过 `kubectl port-forward` 暴露服务到主机，可以访问 TiDB 集群。命令中的端口格式为：`<主机端口>:<k8s 服务端口>`。

- 通过 MySQL 客户端访问 TiDB

    在访问 TiDB 集群之前，请确保已安装 MySQL client。

    1. 使用 kubectl 暴露 TiDB 服务端口：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl port-forward svc/<release-name>-tidb 4000:4000 --namespace=<namespace>
        ```

        > **注意：**
        >
        > 如果代理建立成功，会打印类似输出：`Forwarding from 0.0.0.0:4000 -> 4000`。测试完成后按 `Ctrl + C` 停止代理并退出。

    2. 然后，通过 MySQL 客户端访问 TiDB，打开一个**新**终端标签或窗口，执行下面的命令：

        {{< copyable "shell-regular" >}}

        ``` shell
        mysql -h 127.0.0.1 -P 4000 -u root
        ```

- 查看监控面板

    1. 使用 kubectl 暴露 Grafana 服务端口：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl port-forward svc/<release-name>-grafana 3000:3000 --namespace=<namespace>
        ```

        > **注意：**
        >
        > 如果代理建立成功，会打印类似输出：`Forwarding from 0.0.0.0:3000 -> 3000`。测试完成后按 `Ctrl + C` 停止代理并退出。

    2. 然后，在浏览器中打开 <http://localhost:3000> 访问 Grafana 监控面板：

        - 默认用户名：admin
        - 默认密码：admin

    > **注意：**
    >
    > 如果你不是在本地 PC 而是在远程主机上部署的 kind 环境，可能无法通过 localhost 访问远程主机的服务。
    >
    > 如果使用 kubectl 1.13 或者更高版本，可以在执行 `kubectl port-forward` 命令时添加 `--address 0.0.0.0` 选项，在 `0.0.0.0` 暴露端口而不是默认的 `127.0.0.1`：
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```
    > kubectl port-forward --address 0.0.0.0 -n tidb svc/<release-name>-grafana 3000:3000
    > ```
    >
    > 然后，在浏览器中打开 `http://<远程主机 IP>:3000` 访问 Grafana 监控面板。

## 删除 TiDB 集群 与 Kubernetes 集群

删除本地 TiDB 集群可参考[销毁 TiDB 集群](/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md#销毁-kubernetes-上的-tidb-集群)。

通过下面命令删除该 Kubernetes 集群：

{{< copyable "shell-regular" >}}

``` shell
kind delete cluster
```
