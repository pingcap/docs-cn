---
title: 使用 DinD 在 Kubernetes 上部署 TiDB 集群
summary: 使用 DinD 在 Kubernetes 上部署 TiDB 集群
category: how-to
---

# 使用 DinD 在 Kubernetes 上部署 TiDB 集群

本文介绍了如何在个人电脑（Linux 或 macOS 系统）上采用 [Docker in Docker](https://hub.docker.com/_/docker/) (DinD) 方式在 Kubernetes 上部署 [TiDB Operator](https://github.com/pingcap/tidb-operator) 和 TiDB 集群。

DinD 将 Docker 容器作为虚拟机运行，并在第一层 Docker 容器中运行另一层 Docker 容器。[kubeadm-dind-cluster](https://github.com/kubernetes-sigs/kubeadm-dind-cluster) 使用 DinD 技术在 Docker 容器中运行 Kubernetes 集群。TiDB Operator 通过完善过的一套 DinD 脚本来管理 DinD Kubernetes 集群。

## 环境准备

部署前，请确认软件、资源等满足如下需求：

- 资源需求 CPU 2+，Memory 4G+

    > **注意：**
    >
    > 对于 macOS 系统，需要给 Docker 分配 2+ CPU 和 4G+ Memory。详情请参考 [Mac 上配置 Docker](https://docs.docker.com/docker-for-mac/#advanced)。

- [Docker](https://docs.docker.com/install/)：>= 17.03

    > **注意：**
    >
    > - 由于 DinD 不能在 Docker Toolbox 或者 Docker Machine 上运行，[Legacy Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/) 用户必须卸载 Legacy Docker Toolbox 并安装 [Docker for Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac)。
    > - 安装过程中，`kubeadm` 会检查 Docker 版本。如果 Docker 版本比 18.06 更新，安装过程会打印警告信息。集群可能仍然能正常工作，但是为保证更好的兼容性，建议 Docker 版本在 17.03 和 18.06 之间。你可以在 [这里](https://download.docker.com/) 下载旧版本 Docker。

- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client): 版本 >= 2.9.0 并且 < 3.0.0
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl): 至少 1.10，建议 1.13 或更高版本

    > **注意：**
    >
    > 不同版本 `kubectl` 输出可能略有不同。

- 对于 Linux 用户， 如果使用 5.x 或者更高版本内核，安装过程中 `kubeadm` 可能会打印警告信息。集群可能仍然能正常工作，但是为保证更好的兼容性，建议使用 3.10+ 或者 4.x 版本内核。

- 需要 `root` 权限操作 Docker 进程

- 文件系统支持

    对于 Linux 用户，如果主机使用 XFS 文件系统（CentOS 7 默认），格式化的时候必须指定 `ftype=1` 选项以启用 `d_type` 支持，详见
    [Docker 文档](https://docs.docker.com/storage/storagedriver/overlayfs-driver/)。

    可以通过命令 `xfs_info / | grep ftype` 检查你的文件系统是否支持 `d_type`，`/` 是 Docker 进程的数据目录。

    如果根目录 `/` 使用 XFS 但是没有启用 `d_type`，但是另一个分区启用了 `d_type` 或者使用另外一种文件系统，可以修改 Docker 的数据目录使用那个分区。

    假设支持的文件系统挂载到路径 `/data`，通过下面步骤配置 Docker 使用它：

    {{< copyable "shell-root" >}}

    ``` shell
    mkdir -p /data/docker && \
    systemctl stop docker.service && \
    mkdir -p /etc/systemd/system/docker.service.d/
    ```

    覆盖 Docker service 文件：

    {{< copyable "shell-root" >}}

    ``` shell
    cat << EOF > /etc/systemd/system/docker.service.d/docker-storage.conf
    [Service]
    ExecStart=
    ExecStart=/usr/bin/dockerd --data-root /data/docker -H fd:// --containerd=/run/containerd/containerd.sock
    EOF
    ```

    重启 Docker 进程：

    {{< copyable "shell-root" >}}

    ``` shell
    systemctl daemon-reload && \
    systemctl start docker.service
    ```

## 第 1 步：通过 DinD 部署 Kubernetes 集群

首先，请确认 Docker 进程正常运行，你可以通过代码库中的脚本使用 DinD 为 TiDB Operator 部署一套 Kubernentes 集群（1.12 版本）。

Clone 代码：

{{< copyable "shell-regular" >}}

``` shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator
```

创建集群：

{{< copyable "shell-regular" >}}

``` shell
manifests/local-dind/dind-cluster-v1.12.sh up
```

如果集群创建过程中拉取镜像失败，可以像下面这样在执行脚本时设置环境变量 `KUBE_REPO_PREFIX` 为 `uhub.ucloud.cn/pingcap`（Docker 镜像会从 [UCloud Docker Registry](https://docs.ucloud.cn/compute/uhub/index) 拉取）：

{{< copyable "shell-regular" >}}

``` shell
KUBE_REPO_PREFIX=uhub.ucloud.cn/pingcap manifests/local-dind/dind-cluster-v1.12.sh up
```

或者为 DinD 配置 HTTP 代理：

{{< copyable "shell-regular" >}}

``` shell
export DIND_HTTP_PROXY=http://<ip>:<port> && \
export DIND_HTTPS_PROXY=http://<ip>:<port> && \
export DIND_NO_PROXY=.svc,.local,127.0.0.1,0,1,2,3,4,5,6,7,8,9 && \
manifests/local-dind/dind-cluster-v1.12.sh up
```

由于系统环境或者配置的不同，集群创建过程中可能会输出一些警告信息，但是脚本应该正确执行并正常退出，没有任何错误。可以通过下面命令确认 k8s 集群已经启动并正常运行：

{{< copyable "shell-regular" >}}

``` shell
kubectl cluster-info
```

输出类似下面内容：

```
Kubernetes master is running at http://127.0.0.1:8080
KubeDNS is running at http://127.0.0.1:8080/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
kubernetes-dashboard is running at http://127.0.0.1:8080/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy
```

列出节点信息（DinD 环境中，其实是 Docker 容器）：

{{< copyable "shell-regular" >}}

``` shell
kubectl get nodes -o wide
```

输出类似如下内容：

```
NAME          STATUS   ROLES    AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION               CONTAINER-RUNTIME
kube-master   Ready    master   11m     v1.12.5   10.192.0.2    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-1   Ready    <none>   9m32s   v1.12.5   10.192.0.3    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-2   Ready    <none>   9m32s   v1.12.5   10.192.0.4    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
kube-node-3   Ready    <none>   9m32s   v1.12.5   10.192.0.5    <none>        Debian GNU/Linux 9 (stretch)   3.10.0-957.12.1.el7.x86_64   docker://18.9.0
```

## 第 2 步：在 DinD Kubernetes 集群中部署 TiDB Operator

> **注意：**
>
> ${chartVersion} 在后续文档中代表 chart 版本，例如 `v1.0.0-beta.3`。

如果 K8s 集群启动并正常运行，可以通过 `helm` 添加 chart 仓库并安装 TiDB Operator。

1. 添加 Helm chart 仓库：

    {{< copyable "shell-regular" >}}

    ``` shell
    helm repo add pingcap http://charts.pingcap.org/ && \
    helm repo list && \
    helm repo update && \
    helm search tidb-cluster -l && \
    helm search tidb-operator -l
    ```

2. 安装 TiDB Operator：

    {{< copyable "shell-regular" >}}

    ``` shell
    helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --set scheduler.kubeSchedulerImageName=mirantis/hypokube --set scheduler.kubeSchedulerImageTag=final --version=${chartVersion}
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

## 第 3 步：在 DinD Kubernetes 集群中部署 TiDB 集群

通过 `helm` 和 TiDB Operator，我们可以很轻松的部署一套 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name=demo --namespace=tidb --version=${chartVersion}
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

> **注意：**
>
> 如果你不是在本地 PC 而是在远程主机上部署的 DinD 环境，可能无法通过 localhost 访问远程主机的服务。如果使用 `kubectl` 1.13 或者更高版本，可以在执行 `kubectl port-forward` 命令时添加 `--address 0.0.0.0` 选项，在 `0.0.0.0` 暴露端口而不是默认的 `127.0.0.1`。

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

    2. 然后，在浏览器中打开 http://localhost:3000 访问 Grafana 监控面板：

        * 默认用户名：admin
        * 默认密码：admin

- 永久远程访问

    尽管这是一个非常简单的演示集群，不适用于实际使用，如果能不通过 `kubectl port-forward` 就能远程访问也会比较有用，当然，你需要一个终端。

    TiDB、Prometheus 和 Grafana 默认通过 `NodePort` 服务暴露，所以可以为它们搭建一个反向代理。

    1. 使用下面命令找到这些服务的 NodePort：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl get service -n tidb | grep NodePort
        ```

        输出类似如下内容：

        ```
        demo-grafana      NodePort    10.111.80.73     <none>        3000:32503/TCP                   1m
        demo-prometheus   NodePort    10.104.97.84     <none>        9090:32448/TCP                   1m
        demo-tidb         NodePort    10.102.165.13    <none>        4000:32714/TCP,10080:32680/TCP   1m
        ```

        在这个输出示例中，各服务的 NodePort 为：Grafana 32503、Prometheus 32448、TiDB 32714。

    2. 列出集群的节点 IP 地址。

        DinD 是在 Docker 容器中运行的 K8s 集群，所以服务端口暴露到了容器地址上，而不是主机上。可以通过下面命令列出 Docker 容器的 IP 地址：

        {{< copyable "shell-regular" >}}

        ``` shell
        kubectl get nodes -o yaml | grep address
        ```

        输出类似如下内容：

        ```
        addresses:
        - address: 10.192.0.2
        - address: kube-master
        addresses:
        - address: 10.192.0.3
        - address: kube-node-1
        addresses:
        - address: 10.192.0.4
        - address: kube-node-2
        addresses:
        - address: 10.192.0.5
        - address: kube-node-3
        ```

        在反向代理中使用这些 IP 地址。

    3. 搭建反向代理。

        任意一个（或者所有）容器 IP 可以配置为反向代理的 upstream。你可以使用任何支持 TCP (TiDB) 或者 HTTP (Grafana 和 Prometheus) 的反向代理提供远程访问。HAPROXY 和 NGINX 是两个常用的选择。

## 水平伸缩 TiDB 集群

你可以通过简单地修改 `replicas` 来扩容或者缩容 TiDB 集群。

1. 获取当前使用的 tidb-cluster chart 对应的 values.yaml：

    {{< copyable "shell-regular" >}}

    ``` shell
    mkdir -p /home/tidb/demo && \
    helm inspect values pingcap/tidb-cluster --version=${chartVersion} > /home/tidb/demo/values-demo.yaml
    ```
  
2. 编辑 `/home/tidb/demo/values-demo.yaml`。

    例如，要扩容集群，可以将 TiKV `replicas` 从 3 修改为 5，或者将 TiDB `replicas` 从 2 修改为 3。

3. 执行下面命令升级集群：

    {{< copyable "shell-regular" >}}

    ``` shell
    helm upgrade demo pingcap/tidb-cluster --namespace=tidb -f /home/tidb/demo/values-demo.yaml --version=${chartVersion}
    ```

> **注意：**
>
> 如果要缩容 TiKV，因为要安全地迁移数据，缩容需要的时间取决于已有数据量的大小。

通过 `kubectl get pod -n tidb` 命令验证每个组件的数量是否等于在 `/home/tidb/demo/values-demo.yaml` 中设置的数量，并且所有 Pod 都已处于 `Running` 状态。

## 升级 TiDB 集群

1. 编辑文件 `/home/tidb/demo/values-demo.yaml`。

    例如，修改PD、TiKV 和 TiDB `image` 为 `v3.0.0-rc.2`。

2. 执行如下命令升级集群：

    {{< copyable "shell-regular" >}}

    ``` shell
    helm upgrade demo pingcap/tidb-cluster --namespace=tidb -f /home/tidb/demo/values-demo.yaml --version=${chartVersion}
    ```

通过 `kubectl get pod -n tidb` 命令确认所有 Pod 处于 `Running` 状态。然后你可以访问数据库并通过 `tidb_version()` 确认版本：

{{< copyable "sql" >}}

``` sql
select tidb_version();
```

输出类似如下内容：

```
*************************** 1. row ***************************
tidb_version(): Release Version: v3.0.0-rc.2
Git Commit Hash: 06f3f63d5a87e7f0436c0618cf524fea7172eb93
Git Branch: HEAD
UTC Build Time: 2019-05-28 12:48:52
GoVersion: go version go1.12 linux/amd64
Race Enabled: false
TiKV Min Version: 2.1.0-alpha.1-ff3dd160846b7d1aed9079c389fc188f7f5ea13e
Check Table Before Drop: false
1 row in set (0.001 sec)
```

## 销毁 TiDB 集群

测试结束后，使用如下命令销毁 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm delete demo --purge
```

> **注意：**
>
> 上述命令只是删除运行的 Pod，数据仍然会保留。

如果你不再需要那些数据，可以通过下面命令清除数据（注意，这将永久删除数据）。

{{< copyable "shell-regular" >}}

``` shell
kubectl get pv -l app.kubernetes.io/namespace=tidb -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}' && \
kubectl delete pvc --namespace tidb --all
```

## 停止、重启 Kubernetes 集群

* 如果要停止 DinD Kubernetes 集群，可以执行下面命令：

    {{< copyable "shell-regular" >}}

    ``` shell
    manifests/local-dind/dind-cluster-v1.12.sh stop
    ```

    可以通过 `docker ps` 命令验证所有 Docker 容器都已停止运行。

* 如果停止 DinD Kubernetes 集群后又要重新启动，可以执行下面命令：

    {{< copyable "shell-regular" >}}

    ``` shell
    manifests/local-dind/dind-cluster-v1.12.sh start
    ```

## 销毁 DinD Kubernetes 集群

如果要删除 DinD Kubernetes 集群，可以执行下面命令：

{{< copyable "shell-regular" >}}

``` shell
manifests/local-dind/dind-cluster-v1.12.sh clean && \
sudo rm -rf data/kube-node-*
```

> **警告：**
>
> 销毁 DinD Kubernetes 集群后，必须清除数据，否则当你重新创建新集群时，TiDB 集群会启动失败。
