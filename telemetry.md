---
title: 遥测
summary: 介绍遥测的场景，如何禁用功能和查看遥测状态。
aliases: ['/docs-cn/dev/telemetry/']
---

# 遥测

TiDB、TiUP 及 TiDB Dashboard 默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品，例如，通过这些使用信息，PingCAP 可以了解常见的 TiDB 集群操作，从而确定新功能优先级。

## 哪些使用情况信息会被收集？

以下章节具体描述了各个组件收集并分享的使用情况信息。若收集的使用情况信息有变化，将在版本更新说明中告知。

> **注意：**
>
> 在**任何情况**下，集群中用户存储的数据都**不会**被收集。另请参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)。

### TiDB

当 TiDB 遥测功能开启时，TiDB 集群将会以 6 小时为周期收集使用情况信息并分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- 集群的部署情况，包括各个组件所在的硬件信息（CPU、内存、磁盘）、组件版本号、操作系统版本号等
- 系统的查询请求状态，例如查询请求次数、持续时长等
- 系统组件的使用情况，例如 Async Commit 、builtinFunction 功能是否有被使用
- 内建函数的使用情况，包括 SQL 查询中各种函数的使用频次，其中不包含函数参数的具体信息

可以通过执行以下 SQL 语句查看 TiDB 收集的使用情况信息内容：

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB Dashboard

当 TiDB Dashboard 遥测功能开启时，用户在 TiDB Dashboard 网页界面上进行操作时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- 界面访问情况，如访问的 TiDB Dashboard 功能页面名称
- 用户浏览器及操作系统信息，如浏览器名称和版本号、操作系统名称、屏幕分辨率等

可以使用 [Chrome 开发者工具](https://developers.google.com/web/tools/chrome-devtools)的[网络功能](https://developers.google.com/web/tools/chrome-devtools/network)或 [Firefox 开发者工具](https://developer.mozilla.org/zh-CN/docs/Tools)的[网络监视器功能](https://developer.mozilla.org/zh-CN/docs/Tools/Network_Monitor)查看 TiDB Dashboard 发送的使用情况信息内容。

### TiUP

当 TiUP 遥测功能开启时，执行 TiUP 命令时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiUP 命令的执行情况，如命令执行是否成功、命令执行耗时等
- 使用 TiUP 进行部署的情况，如部署的目标机器硬件信息、组件版本号、修改过的部署配置名称等

使用 TiUP 时，可通过设置 `TIUP_CLUSTER_DEBUG=enable` 环境变量输出执行命令时收集的使用情况信息，例如：

{{< copyable "shell-regular" >}}

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

## 禁用遥测功能

### 部署 TiDB 时禁用 TiDB 遥测

部署 TiDB 集群时，可以为每个 TiDB 集群设置 [`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 以禁用 TiDB 遥测功能。也可以在已部署的 TiDB 集群上修改该配置项，但需要重启集群后才能生效。

以下是在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = false
```

启动 TiDB 时指定命令行参数 `--config=tidb_config.toml` 使得该配置生效。

详情参见 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md#--config)、[TiDB 配置文件描述](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = false
```

启动 TiUP Playground 时，指定命令行参数 `--db.config tidb_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.config tidb_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.tidb.config.enable-telemetry: false`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

### 动态禁用 TiDB 遥测

对于已部署的 TiDB 集群，还可以修改系统全局变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 动态禁用 TiDB 遥测功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

配置文件的禁用优先级高于全局变量。若通过配置文件禁用了遥测功能，则全局变量的配置将不起作用，遥测功能总是处于关闭状态。

### 禁用 TiDB Dashboard 遥测

可以修改 PD 配置中 [`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry) 禁用 TiDB Dashboard 遥测功能。对于已启动的集群，该配置需要重启后才能生效。

以下列出在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

启动 PD 时指定命令行参数 `--config=pd_config.toml` 使得该配置生效。

详情参见 [PD 配置参数](/command-line-flags-for-pd-configuration.md#--config)、[PD 配置文件描述](/pd-configuration-file.md#enable-telemetry)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

启动 TiUP Playground 时，指定命令行参数 `--pd.config pd_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config pd_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.pd.config.dashboard.enable-telemetry: false`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

### 禁用 TiUP 遥测

可通过执行以下命令禁用 TiUP 遥测功能：

{{< copyable "shell-regular" >}}

```shell
tiup telemetry disable
```

## 查看遥测启用状态

对于 TiDB 遥测，可通过执行以下 SQL 语句查看遥测状态：

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

若 `DATA_PREVIEW` 列为空，说明遥测没有开启，否则说明遥测已开启。还可以从 `LAST_STATUS` 列了解上次分享使用情况信息的时间、是否成功等。

对于 TiUP 遥测，可通过执行以下命令查看遥测状态：

{{< copyable "shell-regular" >}}

```shell
tiup telemetry status
```

## 使用情况信息合规性

为了满足不同国家或地区对于此类信息的合规性要求，使用情况信息会按照不同的操作者 IP 地址发送到位于不同国家的服务器，具体如下：

- 若为中国大陆 IP 地址，使用情况信息将会发送并存储于中国大陆境内的公有云服务器。
- 若为中国大陆以外 IP 地址，使用情况信息将会发送并存储于美国的公有云服务器。

可参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)了解详情。
