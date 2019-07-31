---
title: 在 Minikube 集群上部署 TiDB 集群
summary: 在 Minikube 集群上部署 TiDB 集群
category: how-to
---

# 在 Minikube 集群上部署 TiDB 集群

[Minikube](https://kubernetes.io/docs/setup/minikube/) 可以让你在个人电脑上的虚拟机中创建一个 Kubernetes 集群，支持 macOS、Linux 和 Windows 系统。本文介绍如何在 [Minikube](https://kubernetes.io/docs/setup/minikube/) 集群上部署 TiDB 集群。

> **警告：**
>
> - 对于生产环境，不要使用此方式进行部署。
>
> - 尽管 Minikube 支持通过 `--vm-driver=none` 选项使用主机 Docker 而不使用虚拟机，但是目前尚没有针对 TiDB Operator 做过全面的测试，可能会无法正常工作。如果你想在不支持虚拟化的系统（例如，VPS）上试用 TiDB Operator，可以考虑使用 [DinD](/how-to/get-started/deploy-tidb-from-kubernetes-dind.md)。

## 安装 Minikube 并启动 Kubernetes 集群

参考[安装 Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)，在你的机器上安装 Minikube 1.0.0+。

安装完 Minikube 后，可以执行下面命令启动一个 Kubernetes 集群：

{{< copyable "shell-regular" >}}

``` shell
minikube start
```

对于中国大陆用户，可以使用国内 gcr.io mirror 仓库，例如 `registry.cn-hangzhou.aliyuncs.com/google_containers`。

{{< copyable "shell-regular" >}}

``` shell
minikube start --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers
```

或者给 Docker 配置 HTTP/HTTPS 代理。

将下面命令中的 `127.0.0.1:1086` 替换为你自己的 HTTP/HTTPS 代理地址：

{{< copyable "shell-regular" >}}

``` shell
minikube start --docker-env https_proxy=http://127.0.0.1:1086 \
  --docker-env http_proxy=http://127.0.0.1:1086
```

> **注意：**
>
> 由于 Minikube 通过虚拟机（默认）运行，`127.0.0.1` 是虚拟机本身，有些情况下你可能想要使用你的主机的实际 IP。

参考 [Minikube setup](https://kubernetes.io/docs/setup/minikube/) 查看配置虚拟机和 Kubernetes 集群的更多选项。

## 安装 kubectl 并访问集群

Kubernetes 命令行工具 [kubectl](https://kubernetes.io/docs/user-guide/kubectl/)，可以让你执行命令访问 Kubernetes 集群。

参考[文档](https://kubernetes.io/docs/tasks/tools/install-kubectl/) 安装和配置 kubectl。

kubectl 安装完成后，测试 Minikube Kubernetes 集群：

{{< copyable "shell-regular" >}}

``` shell
kubectl cluster-info
```

## 安装 TiDB operator 并运行 TiDB 集群

### 安装 Helm

[Helm](https://helm.sh/) 是 Kubernetes 包管理工具，通过 Helm 可以一键安装 TiDB 的所有分布式组件。安装 Helm 需要同时安装服务端和客户端组件。

{{< copyable "shell-regular" >}}

``` shell
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get | bash
```

安装 helm tiller：

{{< copyable "shell-regular" >}}

``` shell
helm init
```

如果无法访问 gcr.io，你可以尝试 mirror 仓库：

{{< copyable "shell-regular" >}}

``` shell
helm init --upgrade --tiller-image registry.cn-hangzhou.aliyuncs.com/google_containers/tiller:$(helm version --client --short | grep -P -o 'v\d+\.\d+\.\d')
```

安装完成后，执行 `helm version` 会同时显示客户端和服务端组件版本：

{{< copyable "shell-regular" >}}

``` shell
helm version
```

输出类似如下内容：

```
Client: &version.Version{SemVer:"v2.13.1",
GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.13.1",
GitCommit:"618447cbf203d147601b4b9bd7f8c37a5d39fbb4", GitTreeState:"clean"}
```

如果只显示客户端版本，表示 `helm` 无法连接到服务端。通过 `kubectl` 查看 tiller pod 是否在运行：

{{< copyable "shell-regular" >}}

``` shell
kubectl -n kube-system get pods -l app=helm
```

### 添加 Helm 仓库

[Helm 仓库](https://charts.pingcap.org/)存放着 PingCAP 发布的 charts，例如 tidb-operator、tidb-cluster 和 tidb-backup 等等。可使用以下命令添加仓库：

{{< copyable "shell-regular" >}}

``` shell
helm repo add pingcap https://charts.pingcap.org/ && \
helm repo list
```

然后可以查看可用的 chart：

{{< copyable "shell-regular" >}}

``` shell
helm repo update && \
helm search tidb-cluster -l && \
helm search tidb-operator -l
```

### 在 Kubernetes 集群上安装 TiDB Operator

> **注意：**
>
> `<chartVersion>` 在后面文档中代表 chart 版本，例如 `v1.0.0`。

克隆 tidb-operator 代码库并安装 TiDB Operator：

{{< copyable "shell-regular" >}}

``` shell
git clone --depth=1 https://github.com/pingcap/tidb-operator && \
cd tidb-operator && \
kubectl apply -f ./manifests/crd.yaml && \
helm install pingcap/tidb-operator --name tidb-operator --namespace tidb-admin --version=<chartVersion>
```

然后，可以通过如下命令查看 TiDB Operator 的启动情况：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pods --namespace tidb-admin -o wide --watch
```

如果无法访问 gcr.io（Pod 由于 ErrImagePull 无法启动），可以尝试从 mirror 仓库中拉取 kube-scheduler 镜像。可以通过以下命令升级 tidb-operator：

{{< copyable "shell-regular" >}}

``` shell
helm upgrade tidb-operator pingcap/tidb-operator --namespace tidb-admin --set \
  scheduler.kubeSchedulerImageName=registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler --version=<chartVersion>
```

如果 tidb-scheduler 和 tidb-controller-manager 都进入 running 状态，你可以继续下一步启动一个 TiDB 集群。

### 启动 TiDB 集群

通过下面命令启动 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster --name demo --set \
  schedulerName=default-scheduler,pd.storageClassName=standard,tikv.storageClassName=standard,pd.replicas=1,tikv.replicas=1,tidb.replicas=1 --version=<chartVersion>
```

可以通过下面命令观察集群的状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pods --namespace default -l app.kubernetes.io/instance=demo -o wide --watch
```

通过 <kbd>Ctrl</kbd>+<kbd>C</kbd> 停止观察。

## 测试 TiDB 集群

测试 TiDB 集群之前，请确保已经安装 MySQL 客户端。从 Pod 启动、运行到服务可以访问有一些延时，可以通过下面命令查看服务：

{{< copyable "shell-regular" >}}

``` shell
kubectl get svc --watch
```

如果看到 `demo-tidb` 出现，说明服务已经可以访问，可以 <kbd>Ctrl</kbd>+<kbd>C</kbd> 停止。

按照以下步骤访问 TiDB 集群：

1. 转发本地端口到 TiDB 端口。

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl port-forward svc/demo-tidb 4000:4000
    ```

2. 在另一个终端窗口中，通过 MySQL 客户端访问 TiDB：

    {{< copyable "shell-regular" >}}

    ``` shell
    mysql -h 127.0.0.1 -P 4000 -uroot
    ```

    或者可以直接执行 SQL 命令：

    {{< copyable "shell-regular" >}}

    ``` shell
    mysql -h 127.0.0.1 -P 4000 -uroot -e 'select tidb_version();'
    ```

## 监控 TiDB 集群

按照以下步骤监控 TiDB 集群状态：

1. 转发本地端口到 Grafana 端口。

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl port-forward svc/demo-grafana 3000:3000
    ```

2. 打开浏览器，通过 `http://localhost:3000` 访问 Grafana。

    或者，Minikube 提供了 `minikube service` 的方式暴露 Grafana 服务，可以更方便的接入。

    {{< copyable "shell-regular" >}}

    ``` shell
    minikube service demo-grafana
    ```

    上述命令会自动搭建代理并在浏览器中打开 Grafana。

### 删除 TiDB 集群

通过下面命令删除 demo 集群：

{{< copyable "shell-regular" >}}

``` shell
helm delete --purge demo
```

更新 demo 集群使用的 PV 的 reclaim 策略为 Delete：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pv -l app.kubernetes.io/instance=demo -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

删除 PVC：

{{< copyable "shell-regular" >}}

``` shell
kubectl delete pvc -l app.kubernetes.io/managed-by=tidb-operator
```

## FAQ

### Minikube 上的 TiDB 集群不响应或者响应非常慢

Minikube 虚拟机默认配置为 2048 MB 内存和 2 个 CPU。可以在 `minikube start` 时通过`--memory` 和 `--cpus` 选项为其分配更多资源。注意，为了使配置修改生效，你需要重新创建 Minikube 虚拟机。

{{< copyable "shell-regular" >}}

``` shell
minikube delete && \
minikube start --cpus 4 --memory 4096 ...
```
