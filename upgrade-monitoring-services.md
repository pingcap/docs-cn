---
title: 升级集群监控组件
aliases: ['/docs-cn/dev/deploy-monitoring-services/','/docs-cn/dev/monitor-a-tidb-cluster/','/docs-cn/dev/how-to/monitor/monitor-a-cluster/']
---

# 升级 TiDB 集群监控组件

使用 TiUP 部署 TiDB 集群时，TiUP 会同时自动部署 Prometheus、Grafana 和 Alertmanager 等监控组件，并且在集群扩容中自动为新增节点添加监控配置。通过 TiUP 自动部署的监控组件并不是三方组件的最新版本，如果你需要使用新版本中的功能，可以按照本文的方法升级所需的监控组件。

需要注意的是，TiUP 会使用自己的配置参数覆盖监控组件的配置，如果你直接通过替换文件方式升级监控组件，该升级可能在对集群进行 deploy/scale-out/scale-in/reload 等操作中被 TiUP 所覆盖，导致升级出错。如果需要升级 Prometheus、Grafana 和 Alertmanager，请参考本文的升级步骤。

> **注意：**
>
> - 如果监控组件不是由 TiUP 部署和管理，可以直接升级监控组件，无需参考本文档。
> - TiDB 并未对监控组件新版本的兼容性进行测试，可能存在升级后部分功能无法正常使用的问题，如果遇到问题可以在 TiDB github 中上报 Issue，我们会尽快解决。
> - 本文所述功能在 TiUP v1.9.0 及后续版本支持，使用本功能前请检查 TiUP 版本号。

## 升级 Prometheus 

TiDB 安装包中自带 Prometheus 组件包，该组件包中的 Prometheus 软件版本是固定的。推荐使用 TiDB 官方安装包中自带的 Prometheus 版本，如果您需要使用更高版本的 Prometheus 软件，可以在Prometheus 官网的[Release Note 页面](https://github.com/prometheus/prometheus/releases)查看新版本特性，选择适合您生产环境的版本，或者咨询 PingCAP 技术支持服务寻求版本建议。升级操作需要先从 Prometheus 官网下载所需版本的软件安装包，然后重新构造可被 TiUP 使用的 Prometheus 组件安装包。

### 第 1 步：从 Prometheus 官网下载新版本安装包

从[ Prometheus 官网下载页面](https://prometheus.io/download/)下载组件安装包, 并解压。


### 第 2 步：下载 TiDB 官方 Prometheus 安装包

从 [ TiDB 官网下载页面](https://cn.pingcap.com/product/#SelectProduct)下载 TiDB-community-server 软件包，解压后找到 Prometheus 安装包，文件名为 “prometheus-v{version}-linux-amd64.tar.gz”。解压该安装包。

```bash
tar -xzf prometheus-v{version}-linux-amd64.tar.gz
```

### 第 3 步：构造新的适用于 TiUP 的 Prometheus 组件包

复制第 1 步中解压的文件，替换第 2 步解压后 prometheus 子目录(./prometheus-v{version}-linux-amd64/prometheus)下的对应文件。替换完成后重新压缩,并将新压缩包命名为“prometheus-v{newversion}.tar.gz”。

{{< copyable "shell-regular" >}}

```bash
cd prometheus-v{version}-linux-amd64.tar.gz
tar -zcvf ../prometheus-v{new-version}.tar.gz ./
```

> **注意：**
>
> - {new-version} 可以由用户自行指定，无特殊要求。

### 第 4 步：使用新的组件包升级 Prometheus 

执行以下命令升级 Prometheus。

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch <cluster-name> prometheus-{new-version}.tar.gz -R prometheus
```
升级完成后，可以打开 Prometheus 主页（地址通常是 http://<Prometheus-server-host-name>:9090）,点击顶部导航菜单“Status” 然后打开 “Runtime & Build Information” 页面，查看 Prometheus 的版本信息，确认升级成功。

## 升级 Grafana

TiDB 安装包中自带 Grafana 组件包，该组件包中的 Grafana 软件版本是固定的。推荐使用 TiDB 官方安装包中自带的 Grafana 版本，如果您需要使用更高版本的 Grafana 软件，可以在 Grafana 官网的[Release Note 页面](https://grafana.com/docs/grafana/latest/whatsnew/)查看新版本特性，选择适合您生产环境的版本，或者咨询 PingCAP 技术支持服务寻求版本建议。升级操作需要先从 Grafana 官网下载所需版本的软件安装包，然后重新构造可被 TiUP 使用的 Grafana 组件安装包。

### 第 1 步：从 Grafana 官网的下载新版本安装包

从[ Grafana 官网下载页面](https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1)下载组件安装包, 并解压。


### 第 2 步：下载 TiDB 官方 Grafana 安装包

从 [ TiDB 官网下载页面](https://cn.pingcap.com/product/#SelectProduct)下载 TiDB-community-server 软件包，解压后找到 Grafana 安装包，文件名为 “grafana-v{version}-linux-amd64.tar.gz”。解压该安装包。

```bash
tar -xzf grafana-v{version}-linux-amd64.tar.gz
```

### 第 3 步：构造新的适用于 TiUP 的 Grafana 组件包

复制第 1 步中解压的文件，替换第 2 步解压后目录(./grafana-v{version}-linux-amd64/prometheus)下的对应文件。替换完成后重新压缩,并将新压缩包命名为“grafna-v{newversion}.tar.gz”。

{{< copyable "shell-regular" >}}

```bash
cd grafana-v{version}-linux-amd64.tar.gz
tar -zcvf ../grafana-v{new-version}.tar.gz ./
```

> **注意：**
>
> - {new-version} 可以由用户自行指定，无特殊要求。

### 第 4 步：使用新的组件包升级 Grafana 

执行以下命令升级 Grafana。

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch <cluster-name> grafana-v{new-version}.tar.gz -R grafana
```
升级完成后，可以打开 Grafana 主页（地址通常是 http://<Grafana-server-host-name>:3000, 查看 Grafana 的版本信息，确认升级成功。

## 升级 AlertManager

TiDB 安装包中直接使用了 AlertManager 官方组件包，升级时只需要下载所需的新版本官方组件包。

### 第 1 步：从 AlertManager 官网的下载新版本安装包

从[ AlertManager 官网下载页面](https://prometheus.io/download/)下载组件安装包。

### 第 2 步：使用新的组件包升级 AlertManager

执行以下命令升级 AlertManager。

{{< copyable "shell-regular" >}}

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager
```

