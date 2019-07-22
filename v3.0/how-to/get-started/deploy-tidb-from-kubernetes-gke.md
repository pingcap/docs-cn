---
title: 在 GCP 上通过 Kubernetes 部署 TiDB 集群
summary: 在 GCP 上通过 Kubernetes 部署 TiDB 集群教程
category: how-to
aliases: ['/docs-cn/v3.0/how-to/get-started/local-cluster/install-from-kubernetes-gke/']
---

# 在 GCP 上通过 Kubernetes 部署 TiDB 集群

本文介绍如何使用 [TiDB Operator](https://github.com/pingcap/tidb-operator) 在 GCP 上部署 TiDB 集群。本教程需要在 [Google Cloud Shell](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/pingcap/tidb-operator&tutorial=docs/google-kubernetes-tutorial.md) 上运行。

所包含的步骤如下：

- 启动一个包含 3 个节点的 Kubernetes 集群（可选）
- 安装 Kubernetes 包管理工具 Helm
- 部署 TiDB Operator
- 部署 TiDB 集群
- 访问 TiDB 集群
- 扩容 TiDB 集群
- 删除 Kubernetes 集群（可选）

## 选择一个项目

本教程会启动一个包含 3 个 `n1-standard-1` 类型节点的 Kubernetes 集群。价格信息可以参考[这里](https://cloud.google.com/compute/pricing)。

继续之前请选择一个项目：

<walkthrough-project-billing-setup key="project-id">
</walkthrough-project-billing-setup>

## 启用 API

本教程需要使用计算和容器 API。继续之前请启用：

<walkthrough-enable-apis apis="container.googleapis.com,compute.googleapis.com">
</walkthrough-enable-apis>

## 配置 gcloud

这一步配置 glcoud 默认访问你要用的项目和[可用区](https://cloud.google.com/compute/docs/regions-zones/)，可以简化后面用到的命令：

{{< copyable "shell-regular" >}}

``` shell
gcloud config set project {{project-id}} && \
gcloud config set compute/zone us-west1-a
```

## 启动 3 个节点的 Kubernetes 集群

下面命令启动一个包含 3 个 `n1-standard-1` 类型节点的 Kubernetes 集群。

命令执行需要几分钟时间：

{{< copyable "shell-regular" >}}

``` shell
gcloud container clusters create tidb
```

集群启动完成后，将其设置为默认集群：

{{< copyable "shell-regular" >}}

``` shell
gcloud config set container/cluster tidb
```

最后验证 `kubectl` 可以访问集群并且 3 个节点正常运行：

{{< copyable "shell-regular" >}}

``` shell
kubectl get nodes
```

如果所有节点状态为 `Ready`，恭喜你，你已经成功搭建你的第一个 Kubernetes 集群。

## 安装 Helm

Helm 是 Kubernetes 包管理工具，通过 Helm 可以一键安装 TiDB 的所有分布式组件。安装 Helm 需要同时安装服务端和客户端组件。

安装 `helm`：

{{< copyable "shell-regular" >}}

``` shell
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get | bash
```

复制 `helm` 到你的 `$HOME` 目录下，这样即使 Google Cloud Shell 超时断开连接，再次登录后仍然可以访问 Helm：

{{< copyable "shell-regular" >}}

``` shell
mkdir -p ~/bin && \
cp /usr/local/bin/helm ~/bin && \
echo 'PATH="$PATH:$HOME/bin"' >> ~/.bashrc
```

Helm 正常工作需要一定的权限：

{{< copyable "shell-regular" >}}

``` shell
kubectl apply -f ./manifests/tiller-rbac.yaml && \
helm init --service-account tiller --upgrade
```

`tiller` 是 Helm 的服务端组件，初始化完成需要几分钟时间：

{{< copyable "shell-regular" >}}

``` shell
watch "kubectl get pods --namespace kube-system | grep tiller"
```

当 Pod 状态为 `Running`，<kbd>Ctrl</kbd>+<kbd>C</kbd>  停止并继续下一步。

## 添加 Helm 仓库

PingCAP Helm 仓库中存放着 PingCAP 发布的 charts，例如 tidb-operator、tidb-cluster 和 tidb-backup 等等。使用下面命令添加仓库：

{{< copyable "shell-regular" >}}

``` shell
helm repo add pingcap http://charts.pingcap.org/ && \
helm repo list
```

然后你可以查看可用的 chart：

{{< copyable "shell-regular" >}}

``` shell
helm repo update && \
helm search tidb-cluster -l && \
helm search tidb-operator -l
```

## 部署 TiDB 集群

> **注意：**
>
> ${chartVersion} 在后面文档中代表 chart 版本，例如 `v1.0.0-beta.3`。

第一个要安装的 TiDB 组件是 TiDB Operator，TiDB Operator 是管理组件，结合 Kubernetes 启动 TiDB 集群并保证集群正常运行。执行下面命令之前请确保在 `tidb-operator` 目录下：

{{< copyable "shell-regular" >}}

``` shell
kubectl apply -f ./manifests/crd.yaml && \
kubectl apply -f ./manifests/gke/persistent-disk.yaml && \
helm install pingcap/tidb-operator -n tidb-admin --namespace=tidb-admin --version=${chartVersion}
```

可以通过下面命令观察 Operator 启动情况：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pods --namespace tidb-admin -o wide --watch
```

如果 tidb-scheduler 和 tidb-controller-manager 状态都为 `Running`，<kbd>Ctrl</kbd>+<kbd>C</kbd> 停止并继续下一步部署一个 TiDB 集群！

## 部署你的第一个 TiDB 集群

我们可以一键部署一个 TiDB 集群：

{{< copyable "shell-regular" >}}

``` shell
helm install pingcap/tidb-cluster -n demo --namespace=tidb --set pd.storageClassName=pd-ssd,tikv.storageClassName=pd-ssd --version=${chartVersion}
```

集群启动需要几分钟时间，可以通过下面命令观察状态：

{{< copyable "shell-regular" >}}

``` shell
kubectl get pods --namespace tidb -o wide --watch
```

TiDB 集群包含 2 个 TiDB pod，3 个 TiKV pod 和 3 个 PD pod。如果所有 pod 状态都为 `Running`，<kbd>Ctrl</kbd>+<kbd>C</kbd> 停止并继续！

## 访问 TiDB 集群

从 pod 启动、运行到服务可以访问有一些延时，可以通过下面命令查看服务：

{{< copyable "shell-regular" >}}

``` shell
kubectl get svc -n tidb --watch
```

如果看到 `demo-tidb` 出现，说明服务已经可以访问，可以 <kbd>Ctrl</kbd>+<kbd>C</kbd> 停止。

要访问 Kubernetes 集群中的 TiDB 服务，可以在 TiDB 服务和 Google Cloud Shell 之间建立一条隧道。建议这种方式只用于调试，因为如果 Google Cloud Shell 重启，隧道不会自动重新建立。要建立隧道：

{{< copyable "shell-regular" >}}

``` shell
kubectl -n tidb port-forward svc/demo-tidb 4000:4000 &>/tmp/port-forward.log &
```

在 Cloud Shell 上运行：

{{< copyable "shell-regular" >}}

``` shell
sudo apt-get install -y mysql-client && \
mysql -h 127.0.0.1 -u root -P 4000
```

在 MySQL 终端中输入一条 MySQL 命令：

{{< copyable "sql" >}}

``` sql
select tidb_version();
```

如果用 Helm 安装的过程中没有指定密码，现在可以设置：

{{< copyable "sql" >}}

``` sql
SET PASSWORD FOR 'root'@'%' = '<change-to-your-password>';
```

> **注意：**
>
> 这条命令中包含一些特殊字符，Google Cloud Shell 无法自动填充，你需要手动复制、粘贴到控制台中。

恭喜，你已经启动并运行一个兼容 MySQL 的分布式 TiDB 数据库！

## 扩容 TiDB 集群

我们可以一键扩容 TiDB 集群。如下命令可以扩容 TiKV：

{{< copyable "shell-regular" >}}

``` shell
helm upgrade demo pingcap/tidb-cluster --set pd.storageClassName=pd-ssd,tikv.storageClassName=pd-ssd,tikv.replicas=5 --version=${chartVersion}
```

TiKV 的 Pod 数量从 3 增加到了 5。可以通过下面命令查看：

{{< copyable "shell-regular" >}}

``` shell
kubectl get po -n tidb
```

## 访问 Grafana 面板

要访问 Grafana 面板，可以在 Grafana 服务和 shell 之间建立一条隧道，可以使用如下命令：

{{< copyable "shell-regular" >}}

``` shell
kubectl -n tidb port-forward svc/demo-grafana 3000:3000 &>/dev/null &
```

在 Cloud Shell 中，点击 Web Preview 按钮并输入端口 3000，将打开一个新的浏览器标签页访问 Grafana 面板。或者也可以在新浏览器标签或者窗口中直接访问 URL：[https://ssh.cloud.google.com/devshell/proxy?port=3000](https://ssh.cloud.google.com/devshell/proxy?port=3000)。

如果没有使用 Cloud Shell，可以在浏览器中访问 `localhost:3000`。

## 销毁 TiDB 集群

如果不再需要这个 TiDB 集群，可以使用下面命令删除集群：

{{< copyable "shell-regular" >}}

``` shell
helm delete demo --purge
```

上面的命令只会删除运行的 Pod，但是数据还会保留。如果你不再需要那些数据，可以执行下面的命令清除数据和动态创建的持久化磁盘：

{{< copyable "shell-regular" >}}

``` shell
kubectl delete pvc -n tidb -l app.kubernetes.io/instance=demo,app.kubernetes.io/managed-by=tidb-operator && \
kubectl get pv -l app.kubernetes.io/namespace=tidb,app.kubernetes.io/managed-by=tidb-operator,app.kubernetes.io/instance=demo -o name | xargs -I {} kubectl patch {} -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

## 删除 Kubernetes 集群

实验结束后，可以使用如下命令删除 Kubernetes 集群：

{{< copyable "shell-regular" >}}

``` shell
gcloud container clusters delete tidb
```

## 更多信息

我们还提供简单的[基于 Terraform 的部署方案](/how-to/deploy/orchestrated/tidb-in-kubernetes/gcp-gke.md)。
