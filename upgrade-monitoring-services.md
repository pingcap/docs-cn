---
title: 升级集群监控组件
summary: 介绍如何升级 TiDB 集群监控组件 Prometheus、Grafana 和 Alertmanager。
---

# 升级 TiDB 集群监控组件

使用 TiUP 部署 TiDB 集群时，TiUP 会同时自动部署 Prometheus、Grafana 和 Alertmanager 等监控组件，并且在集群扩容中自动为新增节点添加监控配置。通过 TiUP 自动部署的监控组件并不是这些三方组件的最新版本，如果你需要使用最新的三方组件，可以按照本文的方法升级所需的监控组件。

当管理集群时，TiUP 会使用自己的配置参数覆盖监控组件的配置。如果你直接通过替换监控组件配置文件的方式升级监控组件，在之后对集群进行 `deploy`、`scale-out`、`scale-in`、`reload` 等 TiUP 操作时，该升级可能被 TiUP 所覆盖，导致升级出错。如果需要升级 Prometheus、Grafana 和 Alertmanager，请参考本文介绍的升级步骤，而不是直接替换配置文件。

> **注意：**
>
> - 如果现有的监控组件是[手动部署](/deploy-monitoring-services.md)的，而不是由 TiUP 部署的，你可以直接升级监控组件，无需参考本文。
> - TiDB 并未对监控组件新版本的兼容性进行测试，可能存在升级后部分功能无法正常使用的问题。如果遇到问题，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。
> - 本文所述功能在 TiUP v1.9.0 及后续版本支持，使用本功能前请检查 TiUP 版本号。
> - 使用 TiUP 升级 TiDB 群集时，TiUP 会将监控组件重新部署为其默认版本。因此，你需要在升级 TiDB 后重新升级监控组件。

## 升级 Prometheus

为了更好地兼容 TiDB，推荐使用 TiDB 官方安装包中自带的 Prometheus 组件安装包，该组件包中的 Prometheus 版本是固定的。如果你需要使用更高版本的 Prometheus，可以在 Prometheus 官网的 [Release Note 页面](https://github.com/prometheus/prometheus/releases)查看新版本特性，选择适合你生产环境的版本，或者咨询 PingCAP 技术支持服务寻求版本建议。

在以下升级步骤中，你需要先从 Prometheus 官网下载所需版本的软件安装包，然后将其构造为可被 TiUP 使用的 Prometheus 组件安装包。

### 第 1 步：从 Prometheus 官网下载新版本安装包

从 [Prometheus 官网下载页面](https://prometheus.io/download/)下载组件安装包，并解压。

### 第 2 步：下载 TiDB 官方 Prometheus 安装包

1. 在 [TiDB 官网下载页面](https://cn.pingcap.com/product/#SelectProduct)下载 `TiDB-community-server` 软件包，并解压。
2. 在解压文件中，找到 `prometheus-v{version}-linux-amd64.tar.gz`，并解压。

    ```bash
    tar -xzf prometheus-v{version}-linux-amd64.tar.gz
    ```

### 第 3 步：构造新的适用于 TiUP 的 Prometheus 组件包

1. 复制第 1 步中解压的文件，替换第 2 步解压后的 `./prometheus-v{version}-linux-amd64/prometheus` 目录下的对应文件。
2. 重新压缩替换文件后的 `./prometheus-v{version}-linux-amd64` 目录，并将新的压缩包命名为 `prometheus-v{new-version}.tar.gz`。其中，`{new-version}` 可以由你自行指定。

    ```bash
    cd prometheus-v{version}-linux-amd64
    tar -zcvf ../prometheus-v{new-version}.tar.gz ./
    ```

### 第 4 步：使用新的组件包升级 Prometheus

执行以下命令升级 Prometheus。

```bash
tiup cluster patch <cluster-name> prometheus-v{new-version}.tar.gz -R prometheus --overwrite
```

升级完成后，可以打开 Prometheus 主页（地址通常是 `http://<Prometheus-server-host-name>:9090`），点击顶部导航菜单中的 **Status**，然后打开 **Runtime & Build Information** 页面，查看 Prometheus 的版本信息，确认升级成功。

## 升级 Grafana

为了更好地兼容 TiDB，推荐使用 TiDB 官方安装包中自带的 Grafana 组件安装包，该组件包中的 Grafana 版本是固定的。如果你需要使用更高版本的 Grafana，可以在 Grafana 官网的 [Release Note 页面](https://grafana.com/docs/grafana/latest/whatsnew/)查看新版本特性，选择适合你生产环境的版本，或者咨询 PingCAP 技术支持服务寻求版本建议。

在以下升级步骤中，你需要先从 Grafana 官网下载所需版本的软件安装包，然后将其构造为可被 TiUP 使用的 Grafana 组件安装包。

### 第 1 步：从 Grafana 官网的下载新版本安装包

1. 从 [Grafana 官网下载页面](https://grafana.com/grafana/download?pg=get&plcmt=selfmanaged-box1-cta1)下载组件安装包。你可以根据需要选择下载 `OSS` 版或 `Enterprise` 版。
2. 解压下载的软件包。

### 第 2 步：下载 TiDB 官方 Grafana 安装包

1. 在 [TiDB 官网下载页面](https://cn.pingcap.com/product/#SelectProduct)下载 `TiDB-community-server` 软件包，并解压。
2. 在解压文件中，找到 `grafana-v{version}-linux-amd64.tar.gz`，并解压。

    ```bash
    tar -xzf grafana-v{version}-linux-amd64.tar.gz
    ```

### 第 3 步：构造新的适用于 TiUP 的 Grafana 组件包

1. 复制第 1 步中解压的文件，替换第 2 步解压后的 `./grafana-v{version}-linux-amd64/` 目录下的对应文件。
2. 重新压缩替换文件后的 `./grafana-v{version}-linux-amd64` 目录，并将新的压缩包命名为 `grafana-v{new-version}.tar.gz`。其中，`{new-version}` 可以由你自行指定。

    ```bash
    cd grafana-v{version}-linux-amd64
    tar -zcvf ../grafana-v{new-version}.tar.gz ./
    ```

### 第 4 步：使用新的组件包升级 Grafana

执行以下命令升级 Grafana。

```bash
tiup cluster patch <cluster-name> grafana-v{new-version}.tar.gz -R grafana --overwrite
```

升级完成后，可以打开 Grafana 主页（地址通常是 `http://<Grafana-server-host-name>:3000`），查看 Grafana 的版本信息，确认升级成功。

## 升级 Alertmanager

TiDB 安装包中直接使用了 Alertmanager 官方组件包，因此升级 Alertmanager 时你只需要下载并安装新版本的官方组件包。

### 第 1 步：从 Prometheus 官网下载新版本安装包

从 [Prometheus 官网下载页面](https://prometheus.io/download/#alertmanager)下载 `alertmanager` 组件安装包。

### 第 2 步：使用新的组件包升级 Alertmanager

执行以下命令升级 Alertmanager：

```bash
tiup cluster patch <cluster-name> alertmanager-v{new-version}-linux-amd64.tar.gz -R alertmanager --overwrite
```

升级完成后，可以打开 Alertmanager 主页（地址通常是 `http://<Alertmanager-server-host-name>:9093`），点击顶部导航菜单中的 **Status**，然后查看 Alertmanager 的版本信息，确认升级成功。